#!/usr/bin/env pybricks-micropython

# ================================================================
# PIOLIN - WRO FUTURE ENGINEERS 2026
# ROUND 2 / OBSTACLE CHALLENGE - EV3 V1
#
# EARLY PIXY + ULTRASONIC OBSTACLE PROTOTYPE
#
# Hardware:
#   Motor A = rear propulsion
#   Motor B = Ackermann steering
#
#   S1 = Pixy2.1
#   S2 = LEFT EV3 Ultrasonic Sensor
#   S3 = RIGHT EV3 Ultrasonic Sensor
#   S4 = EV3 Color Sensor
#
# Pixy2.1 signatures:
#   Signature 1 = PINK  / parking reference
#   Signature 2 = RED   / pass RIGHT
#   Signature 3 = GREEN / pass LEFT
#
# Main idea:
#   - Drive using simple lateral ultrasonic correction.
#   - Detect Red / Green pillars with Pixy2.1.
#   - The SIGNATURE fixes the legal passing side.
#   - Camera X/Y/size only change the strength of the maneuver.
#   - Side ultrasonics remain active as wall protection.
#   - Briefly remember a pillar if Pixy loses it.
#
# This file represents an early Round 2 development baseline.
# It is NOT the final Phase 4 obstacle controller.
#
# Missing from this V1:
#   - complete pillar pass-confirmation state
#   - dedicated RECOVER state
#   - full corner state machine
#   - three-lap completion logic
#   - final parking sequence
#   - advanced controller arbitration
# ================================================================


from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, UltrasonicSensor, ColorSensor
from pybricks.parameters import Port, Button, Stop
from pybricks.tools import wait, StopWatch

from pixycamev3.pixy2 import Pixy2


# ================================================================
# EV3
# ================================================================

EV3 = EV3Brick()


# ================================================================
# HARDWARE
# ================================================================

MOTOR_DRIVE = Motor(Port.A)
MOTOR_STEER = Motor(Port.B)

# Obstacle configuration:
# Pixy2.1 replaces the Open-round gyro on S1.
PIXY = Pixy2(
    port=1,
    i2c_address=0x54
)

# Physical identities are fixed.
US_LEFT = UltrasonicSensor(Port.S2)
US_RIGHT = UltrasonicSensor(Port.S3)

COLOR_SENSOR = ColorSensor(Port.S4)


# ================================================================
# PIXY SIGNATURES
# ================================================================

SIG_PINK = 1
SIG_RED = 2
SIG_GREEN = 3

# Signature bit mask:
#
# sig1 -> bit 0
# sig2 -> bit 1
# sig3 -> bit 2
#
# 0b00000111 = signatures 1, 2 and 3
PIXY_SIGNATURE_MASK = 0x07

MAX_PIXY_BLOCKS = 8


# ================================================================
# STEERING POLARITY
# ================================================================

# Piolin steering convention:
#
# positive steering -> LEFT
# negative steering -> RIGHT

STEER_LEFT = 1
STEER_RIGHT = -1

CENTER = 0


# ================================================================
# SPEED
# ================================================================

# On this Piolin build:
# negative Motor A speed = forward

SPEED_NORMAL = -280
SPEED_PILLAR = -200
SPEED_WALL_DANGER = -170


# ================================================================
# STEERING LIMITS
# ================================================================

MAX_STEER_ANGLE = 34

MAX_NORMAL_STEER = 13
MAX_PILLAR_STEER = 30

STEERING_MOTOR_SPEED = 800

# Limit how much the requested angle can change per loop.
# This reduces abrupt left/right oscillation.
MAX_STEER_STEP = 3.0

current_steer = 0.0


# ================================================================
# ULTRASONIC FILTERING
# ================================================================

# Measurements are handled in millimeters.

MIN_VALID_US_MM = 30
MAX_VALID_US_MM = 2000

FILTER_ALPHA = 0.40

filtered_left = None
filtered_right = None


# ================================================================
# NORMAL LATERAL CONTROL
# ================================================================

# V1 uses the difference between left and right distances as a
# simple lateral correction.
#
# This is NOT the more advanced Phase 4 geometry controller.

WALL_KP = 0.035

WALL_DEADBAND_MM = 25

# Strong protection if Piolin becomes too close to either side.
WALL_DANGER_MM = 180

WALL_DANGER_STEER = 25


# ================================================================
# PIXY VALIDATION
# ================================================================

# Ignore extremely small detections.
MIN_BLOCK_WIDTH = 4
MIN_BLOCK_HEIGHT = 5
MIN_BLOCK_AREA = 25

# Pixy2 image geometry is approximately:
# width  = 316
# height = 208

MIN_VALID_X = 0
MAX_VALID_X = 315

MIN_VALID_Y = 15
MAX_VALID_Y = 207


# ================================================================
# PILLAR CONTROL
# ================================================================

# These X positions do NOT decide the passing side.
#
# They only describe the desired image geometry while executing
# the already selected maneuver.

RED_TARGET_X = 85
GREEN_TARGET_X = 230


# Minimum steering when a relevant pillar is detected.
PILLAR_BASE_STEER = 11

# Additional steering as the pillar becomes more relevant.
PILLAR_MAX_EXTRA = 17

# Influence of horizontal image error on steering magnitude.
PIXY_X_GAIN = 0.035


# ================================================================
# TARGET MEMORY
# ================================================================

# Pixy may briefly lose the pillar while Piolin rotates.
# Do not immediately cancel the maneuver.

TARGET_MEMORY_MS = 300

last_target_signature = None
last_target_angle = 0.0
last_target_time = -10000

locked_tracking_index = None


# ================================================================
# LOOP
# ================================================================

LOOP_DELAY_MS = 20

clock = StopWatch()


# ================================================================
# GENERAL UTILITIES
# ================================================================

def clamp(value, minimum, maximum):

    if value < minimum:
        return minimum

    if value > maximum:
        return maximum

    return value


# ================================================================
# DISTANCE READING
# ================================================================

def read_ultrasonic(sensor):
    """
    Read one ultrasonic sensor.

    Pybricks returns distance in millimeters.

    Invalid or extreme readings return None instead of being used
    directly by the controller.
    """

    try:
        value = sensor.distance()

    except Exception:
        return None

    if value < MIN_VALID_US_MM:
        return None

    if value > MAX_VALID_US_MM:
        return None

    return float(value)


def update_ultrasonics():
    """
    Read and low-pass filter S2 and S3.

    Returns:
        left_mm, right_mm
    """

    global filtered_left
    global filtered_right

    raw_left = read_ultrasonic(US_LEFT)
    raw_right = read_ultrasonic(US_RIGHT)

    if raw_left is not None:

        if filtered_left is None:
            filtered_left = raw_left

        else:
            filtered_left = (
                FILTER_ALPHA * raw_left
                + (1.0 - FILTER_ALPHA) * filtered_left
            )

    if raw_right is not None:

        if filtered_right is None:
            filtered_right = raw_right

        else:
            filtered_right = (
                FILTER_ALPHA * raw_right
                + (1.0 - FILTER_ALPHA) * filtered_right
            )

    return filtered_left, filtered_right


# ================================================================
# STEERING MOTOR
# ================================================================

def set_steering(target, immediate=False):
    """
    Command Motor B while keeping the steering angle inside
    the mechanical software limit.

    Normal commands are rate-limited to reduce oscillation.
    """

    global current_steer

    target = clamp(
        target,
        -MAX_STEER_ANGLE,
        MAX_STEER_ANGLE
    )

    if immediate:

        current_steer = target

    else:

        difference = target - current_steer

        difference = clamp(
            difference,
            -MAX_STEER_STEP,
            MAX_STEER_STEP
        )

        current_steer += difference

    MOTOR_STEER.track_target(
        current_steer
    )


# ================================================================
# NORMAL WALL / LATERAL CONTROL
# ================================================================

def normal_steering(left, right):
    """
    Early lateral controller.

    If both sensors are valid, compare left and right clearance.

    If Piolin is closer to the left:
        steer RIGHT.

    If Piolin is closer to the right:
        steer LEFT.
    """

    if left is None or right is None:
        return 0.0

    error = left - right

    if abs(error) <= WALL_DEADBAND_MM:
        return 0.0

    correction = WALL_KP * error

    return clamp(
        correction,
        -MAX_NORMAL_STEER,
        MAX_NORMAL_STEER
    )


# ================================================================
# WALL SAFETY
# ================================================================

def wall_safety(left, right):
    """
    Strong local wall protection.

    Returns:
        steering angle if intervention is needed
        None otherwise
    """

    left_danger = (
        left is not None
        and left <= WALL_DANGER_MM
    )

    right_danger = (
        right is not None
        and right <= WALL_DANGER_MM
    )

    # If both are close, escape from the closer side.
    if left_danger and right_danger:

        if left < right:
            return -WALL_DANGER_STEER

        else:
            return WALL_DANGER_STEER

    # Too close to left wall -> steer right.
    if left_danger:
        return -WALL_DANGER_STEER

    # Too close to right wall -> steer left.
    if right_danger:
        return WALL_DANGER_STEER

    return None


# ================================================================
# PIXY BLOCK VALIDATION
# ================================================================

def valid_pillar(block):
    """
    Check whether a Pixy block is useful for obstacle navigation.
    """

    if block.sig not in (
        SIG_RED,
        SIG_GREEN
    ):
        return False

    if block.x_center < MIN_VALID_X:
        return False

    if block.x_center > MAX_VALID_X:
        return False

    if block.y_center < MIN_VALID_Y:
        return False

    if block.y_center > MAX_VALID_Y:
        return False

    if block.width < MIN_BLOCK_WIDTH:
        return False

    if block.height < MIN_BLOCK_HEIGHT:
        return False

    area = block.width * block.height

    if area < MIN_BLOCK_AREA:
        return False

    return True


# ================================================================
# TARGET SELECTION
# ================================================================

def choose_target(blocks):
    """
    Select one relevant Red or Green pillar.

    V1 already avoids blindly using the first Pixy block.

    If the previous tracking index is still visible, preserve it.
    Otherwise select the strongest candidate using image area and
    vertical position.

    Larger / lower blocks are generally treated as more relevant,
    but this is image-space relevance, not a metric distance.
    """

    global locked_tracking_index

    candidates = []

    for block in blocks:

        if valid_pillar(block):
            candidates.append(block)

    if not candidates:

        locked_tracking_index = None
        return None

    # ------------------------------------------------------------
    # KEEP THE SAME PIXY TRACK IF POSSIBLE
    # ------------------------------------------------------------

    if locked_tracking_index is not None:

        for block in candidates:

            block_index = getattr(
                block,
                "tracking_index",
                None
            )

            if block_index == locked_tracking_index:
                return block

    # ------------------------------------------------------------
    # SELECT MOST RELEVANT CANDIDATE
    # ------------------------------------------------------------

    def relevance(block):

        area = (
            block.width
            * block.height
        )

        # Y receives additional weight because a pillar lower in the
        # image is usually more relevant to the immediate maneuver.
        return area + block.y_center * 2

    target = max(
        candidates,
        key=relevance
    )

    locked_tracking_index = getattr(
        target,
        "tracking_index",
        None
    )

    return target


# ================================================================
# PIXY READING
# ================================================================

def read_pixy():
    """
    Request Pixy Color Connected Components blocks.

    Returns:
        selected Red/Green target
        None if no useful pillar is visible
    """

    try:

        count, blocks = PIXY.get_blocks(
            PIXY_SIGNATURE_MASK,
            MAX_PIXY_BLOCKS
        )

    except Exception as error:

        print(
            "PIXY ERROR:",
            error
        )

        return None

    if count <= 0:
        return None

    available = []

    for i in range(count):
        available.append(blocks[i])

    return choose_target(
        available
    )


# ================================================================
# PILLAR PROXIMITY / RELEVANCE
# ================================================================

def pillar_relevance(block):
    """
    Estimate how strongly Piolin should react.

    This does NOT attempt to convert Pixy coordinates into physical
    centimeters.

    It only creates a normalized image-space relevance value.
    """

    area = (
        block.width
        * block.height
    )

    # Y grows as the object moves lower in the image.
    y_factor = (
        block.y_center
        - MIN_VALID_Y
    ) / float(
        MAX_VALID_Y
        - MIN_VALID_Y
    )

    y_factor = clamp(
        y_factor,
        0.0,
        1.0
    )

    # Area factor is intentionally capped.
    area_factor = area / 1800.0

    area_factor = clamp(
        area_factor,
        0.0,
        1.0
    )

    return max(
        y_factor,
        area_factor
    )


# ================================================================
# PILLAR STEERING
# ================================================================

def pillar_steering(block):
    """
    Calculate obstacle steering.

    CRITICAL RULE:

        Signature determines SIDE.

        RED   -> RIGHT
        GREEN -> LEFT

    Camera X never changes that rule.

    X and apparent proximity only determine HOW STRONGLY Piolin
    steers toward the already selected side.
    """

    relevance = pillar_relevance(
        block
    )

    # ------------------------------------------------------------
    # RED -> PASS RIGHT
    # ------------------------------------------------------------

    if block.sig == SIG_RED:

        side = STEER_RIGHT

        desired_x = RED_TARGET_X

        color_name = "RED"

    # ------------------------------------------------------------
    # GREEN -> PASS LEFT
    # ------------------------------------------------------------

    else:

        side = STEER_LEFT

        desired_x = GREEN_TARGET_X

        color_name = "GREEN"

    # ------------------------------------------------------------
    # MAGNITUDE
    # ------------------------------------------------------------

    proximity_extra = (
        PILLAR_MAX_EXTRA
        * relevance
    )

    x_error = abs(
        desired_x
        - block.x_center
    )

    x_extra = (
        PIXY_X_GAIN
        * x_error
    )

    magnitude = (
        PILLAR_BASE_STEER
        + proximity_extra
        + x_extra
    )

    magnitude = clamp(
        magnitude,
        PILLAR_BASE_STEER,
        MAX_PILLAR_STEER
    )

    angle = (
        side
        * magnitude
    )

    print(
        color_name,
        "x:",
        block.x_center,
        "y:",
        block.y_center,
        "w:",
        block.width,
        "h:",
        block.height,
        "steer:",
        round(angle, 1)
    )

    return angle


# ================================================================
# TARGET MEMORY
# ================================================================

def remember_target(block, angle, now):
    """
    Store the most recent confirmed pillar command.
    """

    global last_target_signature
    global last_target_angle
    global last_target_time

    last_target_signature = (
        block.sig
    )

    last_target_angle = angle

    last_target_time = now


def remembered_target(now):
    """
    Keep the previous obstacle direction for a short time if Pixy
    briefly loses the pillar.

    Returns:
        remembered steering angle
        None if memory has expired
    """

    if last_target_signature is None:
        return None

    age = (
        now
        - last_target_time
    )

    if age > TARGET_MEMORY_MS:
        return None

    return last_target_angle


# ================================================================
# FLOOR SENSOR DEBUG
# ================================================================

def read_floor():
    """
    Read S4.

    V1 does not yet use S4 for the complete three-lap state machine,
    but keeping the sensor active allows course-mark testing and
    later expansion.
    """

    try:
        return COLOR_SENSOR.color()

    except Exception:
        return None


# ================================================================
# START
# ================================================================

def wait_for_start():
    """
    Wheels must be physically centered before starting.

    RIGHT button starts.
    DOWN button aborts.
    """

    EV3.screen.clear()

    EV3.screen.print(
        "ROUND 2 V1"
    )

    EV3.screen.print(
        "CENTER WHEELS"
    )

    EV3.screen.print(
        "RIGHT = START"
    )

    EV3.screen.print(
        "DOWN = STOP"
    )

    while Button.RIGHT in EV3.buttons.pressed():
        wait(20)

    while Button.RIGHT not in EV3.buttons.pressed():

        if Button.DOWN in EV3.buttons.pressed():
            return False

        wait(20)

    while Button.RIGHT in EV3.buttons.pressed():
        wait(20)

    return True


# ================================================================
# STOP
# ================================================================

def stop_robot():
    """
    Safe shutdown.
    """

    MOTOR_DRIVE.brake()

    try:
        set_steering(
            0,
            immediate=True
        )

        wait(100)

    except Exception:
        pass

    MOTOR_STEER.hold()


# ================================================================
# MAIN
# ================================================================

def main():

    global current_steer
    global locked_tracking_index

    # ------------------------------------------------------------
    # MANUAL STEERING ZERO
    # ------------------------------------------------------------

    # Physically center the front wheels before this line executes.
    MOTOR_STEER.reset_angle(0)

    current_steer = 0.0

    locked_tracking_index = None

    set_steering(
        0,
        immediate=True
    )

    # ------------------------------------------------------------
    # WAIT FOR OPERATOR
    # ------------------------------------------------------------

    if not wait_for_start():
        stop_robot()
        return

    EV3.screen.clear()

    EV3.screen.print(
        "OBSTACLE V1"
    )

    try:

        while True:

            # ----------------------------------------------------
            # EMERGENCY STOP
            # ----------------------------------------------------

            if Button.DOWN in EV3.buttons.pressed():
                break

            now = clock.time()

            # ----------------------------------------------------
            # SENSORS
            # ----------------------------------------------------

            left, right = (
                update_ultrasonics()
            )

            target = read_pixy()

            floor = read_floor()

            # ----------------------------------------------------
            # PRIORITY 1:
            # WALL SAFETY
            # ----------------------------------------------------

            safety_angle = wall_safety(
                left,
                right
            )

            # ----------------------------------------------------
            # PRIORITY 2:
            # ACTIVE PILLAR
            # ----------------------------------------------------

            if target is not None:

                requested_angle = (
                    pillar_steering(
                        target
                    )
                )

                remember_target(
                    target,
                    requested_angle,
                    now
                )

                drive_speed = (
                    SPEED_PILLAR
                )

                mode = "PILLAR"

            else:

                # ------------------------------------------------
                # TEMPORARY CAMERA LOSS
                # ------------------------------------------------

                memory_angle = (
                    remembered_target(
                        now
                    )
                )

                if memory_angle is not None:

                    requested_angle = (
                        memory_angle
                    )

                    drive_speed = (
                        SPEED_PILLAR
                    )

                    mode = "MEMORY"

                # ------------------------------------------------
                # PRIORITY 3:
                # NORMAL LATERAL CONTROL
                # ------------------------------------------------

                else:

                    requested_angle = (
                        normal_steering(
                            left,
                            right
                        )
                    )

                    drive_speed = (
                        SPEED_NORMAL
                    )

                    mode = "NORMAL"

                    locked_tracking_index = None

            # ----------------------------------------------------
            # WALL SAFETY OVERRIDE
            # ----------------------------------------------------

            if safety_angle is not None:

                requested_angle = (
                    safety_angle
                )

                drive_speed = (
                    SPEED_WALL_DANGER
                )

                mode = "WALL SAFE"

            # ----------------------------------------------------
            # ACTUATION
            # ----------------------------------------------------

            set_steering(
                requested_angle
            )

            MOTOR_DRIVE.run(
                drive_speed
            )

            # ----------------------------------------------------
            # DEBUG
            # ----------------------------------------------------

            print(
                mode,
                "L:",
                int(left) if left is not None else None,
                "R:",
                int(right) if right is not None else None,
                "STEER:",
                round(current_steer, 1),
                "FLOOR:",
                floor
            )

            wait(
                LOOP_DELAY_MS
            )

    finally:

        stop_robot()

        EV3.screen.clear()

        EV3.screen.print(
            "STOPPED"
        )


# ================================================================
# ENTRY POINT
# ================================================================

if __name__ == "__main__":
    main()
