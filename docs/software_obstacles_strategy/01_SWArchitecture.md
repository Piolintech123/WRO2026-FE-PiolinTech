between the current wheel position and the target angle, multiplying that error by a proportional gain to drive the steering motor swiftly and accurately.

```python
def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))

def set_steering(target_angle):
    target_angle = clamp(target_angle, -MAX_STEER_ANGLE, MAX_STEER_ANGLE)
    diff = target_angle - MOTOR_STEER.angle()
    MOTOR_STEER.run(diff * 15)

```

One of the most advanced architectural choices in this code is the odometry-backed line detection system. Standard, novice-level code relies on temporal debouncing to prevent a robot from counting a thick black line multiple times as it drives over it; they simply command the robot to wait for one second after seeing a line. However, relying on time is a fundamental flaw in physical engineering. If the robot's battery is low, or if it rubs against a wall and slows down, crossing the line might take two seconds, causing the temporal code to double-count the line and ruin the entire lap logic. This architecture abandons time entirely and uses spatial debouncing. By calculating the absolute difference between the current wheel encoder angle and the angle recorded at the last line crossing, the robot measures pure physical distance. It forces the robot to travel exactly 800 degrees of wheel rotation before it is even allowed to acknowledge another line, making the system immune to battery voltage drops, friction, or unexpected physical delays.

```python
def check_line():
    global total_lines, last_line_angle
    
    color = COLOR_SENSOR.color()
    reflection = COLOR_SENSOR.reflection()
    is_line = (color in [ColorSensor.BLACK] or reflection < 20)
    
    moved_distance = abs(MOTOR_DRIVE.angle() - last_line_angle)

    if (moved_distance > 800 and is_line) or (total_lines == 0 and is_line):
        total_lines += 1
        last_line_angle = MOTOR_DRIVE.angle()

```

The first active state of the Finite State Machine is the non-linear initial alignment phase. When the robot is placed on the starting grid, it has no idea which direction the track will flow, so its only goal is to stay perfectly centered between the two walls while accelerating. Standard robots use a simple linear subtraction of the left and right ultrasonic sensors to find the center. However, linear math creates violent reactions: if the robot is placed slightly crooked, the massive initial error causes the wheels to jerk violently, losing traction and fishtailing. This architecture utilizes a square root function to create a logarithmic response curve. The square root acts as a mathematical shock absorber. If the robot is slightly off-center, it corrects sharply, but if it is massively off-center, the square root flattens the mathematical curve, smoothing out the steering command and allowing the robot to glide gracefully into the center of the track without breaking tire traction.

```python
    for _ in range(120):
        r = US_RIGHT.distance() / 10.0  
        c = US_LEFT.distance() / 10.0

        fr = (-2 * math.sqrt(max(0, 11 * r))) + 100
        fc = (-2 * math.sqrt(max(0, 11 * c))) + 100

        target = (fc * 1.3) - (fr * 1.3)
        set_steering(target)

        MOTOR_DRIVE.run(SPEED_START)
        wait(20)

```

Once the initial launch phase is complete, the robot transitions into a state of dynamic sense detection. In this phase, the robot drives blindly forward at maximum speed while polling the color sensor as fast as the processor allows. Because the robot is no longer calculating complex square roots or polling ultrasonic sensors, the CPU is entirely dedicated to catching the microscopic flash of the blue, red, or orange directional marker on the floor. By isolating the color-detection into its own tiny, extremely fast loop, the robot guarantees it will catch the color marker instantly, even while traveling at high speeds. Once the color is identified, it locks the track direction into memory and irreversibly breaks the loop to move into the cruising state.

```python
    detected_mode = None

    while detected_mode is None:
        MOTOR_DRIVE.run(SPEED_FAST)
        color = COLOR_SENSOR.color()

        if color == ColorSensor.BLUE:
            detected_mode = "LEFT_WALL"
        elif color in [ColorSensor.RED, ColorSensor.ORANGE]:
            detected_mode = "RIGHT_WALL"

        wait(10)

```

The third phase is the core endurance loop, utilizing single-wall proportional cruising. Instead of continuing to center itself between two walls, the robot entirely ignores the outside wall and exclusively hugs the inside wall at a highly specific distance of 280 millimeters. This asymmetrical tracking is a massive competitive advantage. Real-world tracks are imperfect, and the distance between the left and right walls constantly fluctuates. A robot trying to center itself will chatter and vibrate as it reacts to the changing track width. By locking onto a single wall, this robot traces a perfect, mathematically smooth geometric racing line. The error is calculated by subtracting the target distance from the current distance, and then multiplied by a proportional gain. This gain dictates how aggressively the robot steers back to its racing line, creating a smooth, fluid motion that minimizes drag and maximizes forward momentum.

```python
    while total_lines < 12:
        check_line()
        MOTOR_DRIVE.run(SPEED_FAST)

        if detected_mode == "LEFT_WALL":
            distance = US_LEFT.distance()
            diff = (distance - TARGET_DIST) * -0.15
            set_steering(diff)

        elif detected_mode == "RIGHT_WALL":
            distance = US_RIGHT.distance()
            diff = (distance - TARGET_DIST) * 0.15
            set_steering(diff)

        wait(10)

```

The final phase of the architecture is the blind sprint. Once the odometry system has successfully verified that the robot has crossed exactly twelve lines, the main endurance loop terminates. However, if the robot were to immediately apply the brakes, the momentum shift could cause it to skid, or worse, the rear chassis might not fully clear the timing gates at the finish line, resulting in a severe penalty. To prevent this, the state machine enters a final, fixed loop that forces the robot to continue executing its single-wall tracking algorithm for exactly 60 more processor cycles. This guarantees that the entire physical mass of the robot blasts completely through the finish line before it safely powers down the drive and steering motors, bringing the autonomous sequence to a highly controlled and deliberate conclusion.

```python
    for _ in range(60):
        MOTOR_DRIVE.run(SPEED_FAST)
        if detected_mode == "LEFT_WALL":
            distance = US_LEFT.distance()
            set_steering((distance - TARGET_DIST) * -0.15)
        else:
            distance = US_RIGHT.distance()
            set_steering((distance - TARGET_DIST) * 0.15)
        wait(10)

    MOTOR_DRIVE.stop(Stop.BRAKE)
    MOTOR_STEER.stop(Stop.BRAKE)
