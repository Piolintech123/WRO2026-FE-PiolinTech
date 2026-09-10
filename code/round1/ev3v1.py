#!/usr/bin/env pybricks-micropython

# ================================================================
# PIOLIN - WRO FUTURE ENGINEERS 2026
# ROUND 1 / OPEN CHALLENGE - EV3 V1
#
# EARLY OPEN-ROUND PROTOTYPE
#
# Logic:
#   1. Drive straight.
#   2. Detect a floor color marking.
#   3. BLUE   -> turn LEFT.
#      ORANGE -> turn RIGHT.
#   4. Return steering to center.
#   5. Continue forward.
#   6. Count each accepted color event as one corner.
#   7. Stop after 12 accepted events.
#
# Hardware used in this version:
#   Motor A = rear propulsion
#   Motor B = steering
#   S4      = EV3 Color Sensor
#
# This early version does NOT use the ultrasonic sensors or gyro.
# It is preserved as part of Piolin's software evolution.
#
# IMPORTANT:
# This is a legacy/development version and does not represent
# the current Phase 4 Open Challenge controller.
# ================================================================


from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Stop, Button, Color
from pybricks.tools import wait


# ================================================================
# HARDWARE
# ================================================================

ev3 = EV3Brick()

# Motor A = propulsion
drive = Motor(Port.A)

# Motor B = Ackermann steering
steering = Motor(Port.B)

# Downward-facing floor sensor
color_sensor = ColorSensor(Port.S4)


# ================================================================
# MAIN CALIBRATION PARAMETERS
# ================================================================

# Negative values correspond to forward motion on this Piolin build.
NORMAL_SPEED = -620

# Reduced speed while executing a corner.
TURN_SPEED = -420

# Steering motor target used during a color-triggered turn.
TURN_STEERING_ANGLE = 30

# Time spent maintaining the turning trajectory.
#
# This is one of the main calibration parameters in this early
# time-based corner implementation.
TURN_TIME_MS = 650

# Short forward movement after the turn to leave the color region.
POST_TURN_STRAIGHT_MS = 180

# Steering motor movement speed.
STEERING_SPEED = 700

# Change to -1 only if the physical steering direction is reversed.
STEER_DIRECTION = 1

# Three laps correspond to 12 corner events in this early model.
TOTAL_COUNTS = 12

# Number of equal readings required before accepting a color.
COLOR_CONFIRMATIONS = 2

# Number of neutral readings required before accepting a new line.
COLOR_RELEASE_CONFIRMATIONS = 3

# Main-loop delay.
LOOP_DELAY_MS = 10


# ================================================================
# STATE
# ================================================================

count = 0

candidate_color = None
candidate_count = 0

ready_for_new_color = True
release_count = 0


# ================================================================
# STEERING
# ================================================================

def center_steering():
    """
    Return Motor B to the steering-center reference.
    """

    steering.run_target(
        STEERING_SPEED,
        0,
        then=Stop.HOLD,
        wait=True
    )


# ================================================================
# FLOOR COLOR DETECTION
# ================================================================

def read_track_color():
    """
    Classify the current S4 reading.

    Returns:
        'BLUE'
        'ORANGE'
        None

    In this early prototype, the EV3 built-in color classifier
    was used directly.

    Depending on lighting, the orange floor marking could appear
    as RED, YELLOW, or BROWN to the EV3 sensor.
    """

    try:
        detected = color_sensor.color()

    except Exception:
        return None

    if detected == Color.BLUE:
        return 'BLUE'

    if detected in (
        Color.RED,
        Color.YELLOW,
        Color.BROWN
    ):
        return 'ORANGE'

    return None


# ================================================================
# EARLY COLOR-TRIGGERED CORNER LOGIC
# ================================================================

def turn_for_color(detected_color):
    """
    Execute the early time-based turn.

    BLUE:
        turn LEFT

    ORANGE:
        turn RIGHT

    This version uses the floor color itself to determine the turn
    direction and uses time to determine how long the corner lasts.
    """

    if detected_color == 'BLUE':

        target = (
            -TURN_STEERING_ANGLE
            * STEER_DIRECTION
        )

        print('BLUE -> LEFT')

    else:

        target = (
            TURN_STEERING_ANGLE
            * STEER_DIRECTION
        )

        print('ORANGE -> RIGHT')

    # Move Motor B to the requested steering angle.
    steering.run_target(
        STEERING_SPEED,
        target,
        then=Stop.HOLD,
        wait=True
    )

    # Move through the corner.
    drive.run(TURN_SPEED)

    wait(TURN_TIME_MS)

    # Return steering to center.
    center_steering()

    # Leave the color marking before normal detection resumes.
    drive.run(NORMAL_SPEED)

    wait(POST_TURN_STRAIGHT_MS)


# ================================================================
# FINISH
# ================================================================

def stop_finished():
    """
    Stop Piolin after completing the 12 accepted events.
    """

    drive.hold()

    center_steering()

    ev3.screen.clear()

    ev3.screen.draw_text(
        30,
        45,
        'FINISHED 12/12'
    )

    try:
        ev3.speaker.beep(
            1200,
            300
        )

    except Exception:
        pass

    print('FINISHED 12/12')


# ================================================================
# START CONTROL
# ================================================================

def wait_for_start():
    """
    Wait until the EV3 center button is pressed.
    """

    ev3.screen.clear()

    ev3.screen.draw_text(
        25,
        45,
        'PRESS CENTER'
    )

    # Wait for any previous press to be released.
    while Button.CENTER in ev3.buttons.pressed():
        wait(20)

    # Wait for start press.
    while Button.CENTER not in ev3.buttons.pressed():
        wait(20)

    # Wait for release.
    while Button.CENTER in ev3.buttons.pressed():
        wait(20)


# ================================================================
# INITIALIZATION
# ================================================================

# The steering wheels must be physically centered before startup.
steering.reset_angle(0)

center_steering()

wait_for_start()

ev3.screen.clear()

ev3.screen.draw_text(
    35,
    45,
    'COUNT 0/12'
)

drive.run(NORMAL_SPEED)


# ================================================================
# MAIN LOOP
# ================================================================

try:

    while count < TOTAL_COUNTS:

        # DOWN button = manual emergency stop.
        if Button.DOWN in ev3.buttons.pressed():
            break

        detected = read_track_color()

        # --------------------------------------------------------
        # WAITING FOR A NEW FLOOR EVENT
        # --------------------------------------------------------

        if ready_for_new_color:

            if detected is None:

                candidate_color = None
                candidate_count = 0

            else:

                # Same candidate observed again.
                if detected == candidate_color:

                    candidate_count += 1

                # New candidate.
                else:

                    candidate_color = detected
                    candidate_count = 1

                # ------------------------------------------------
                # CONFIRMED COLOR EVENT
                # ------------------------------------------------

                if candidate_count >= COLOR_CONFIRMATIONS:

                    drive.hold()

                    # Execute the corresponding corner.
                    turn_for_color(candidate_color)

                    # Count one physical event.
                    count += 1

                    print(
                        'COUNT: {}/{}'.format(
                            count,
                            TOTAL_COUNTS
                        )
                    )

                    ev3.screen.clear()

                    ev3.screen.draw_text(
                        35,
                        45,
                        'COUNT {}/{}'.format(
                            count,
                            TOTAL_COUNTS
                        )
                    )

                    # Finish after the twelfth event.
                    if count >= TOTAL_COUNTS:
                        break

                    # ------------------------------------------------
                    # LATCH THE CURRENT PHYSICAL LINE
                    # ------------------------------------------------
                    #
                    # Prevent the same floor marking from being counted
                    # repeatedly while S4 remains above it.
                    #

                    ready_for_new_color = False

                    release_count = 0

                    candidate_color = None
                    candidate_count = 0

                    drive.run(NORMAL_SPEED)

        # --------------------------------------------------------
        # WAITING TO LEAVE THE CURRENT LINE
        # --------------------------------------------------------

        else:

            if detected is None:

                release_count += 1

                # Require several neutral readings before re-arming.
                if (
                    release_count
                    >= COLOR_RELEASE_CONFIRMATIONS
                ):

                    ready_for_new_color = True

                    release_count = 0

            else:

                release_count = 0

        wait(LOOP_DELAY_MS)


# ================================================================
# SAFE EXIT
# ================================================================

finally:

    drive.hold()

    center_steering()

    if count >= TOTAL_COUNTS:

        stop_finished()

    else:

        ev3.screen.clear()

        ev3.screen.draw_text(
            45,
            45,
            'STOPPED'
        )

        print('STOPPED')
