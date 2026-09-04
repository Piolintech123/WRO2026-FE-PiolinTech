# 3. Motors and Actuation System

Piolín uses **two independently controlled LEGO EV3 motors**, each with a clearly separated mechanical responsibility. One motor provides propulsion while the second controls the steering mechanism.

This separation is fundamental to Piolín's vehicle architecture. Unlike a differential-drive robot, Piolín does not turn by changing the speed of two independent drive wheels. Instead, the robot uses a car-like configuration in which the rear drivetrain produces forward movement and the front wheels change direction through an Ackermann steering mechanism.

The final motor assignment is:

| EV3 Port | Motor Role | Mechanical Function |
| :--- | :--- | :--- |
| **Port A** | Drive Motor | Provides propulsion through the rear drivetrain |
| **Port B** | Steering Motor | Controls the front Ackermann steering mechanism |

The two actuators therefore control two different variables:

```text
MOTOR A
   ↓
Vehicle Speed
   ↓
Forward / Reverse Motion


MOTOR B
   ↓
Steering Position
   ↓
Vehicle Direction
```

This allows the EV3 to control speed and direction independently.

> [!IMPORTANT]
> Piolín does **not** use differential steering in its final configuration.  
> Motor A provides propulsion while Motor B physically changes the direction of the front wheels.

---

## 3.1 Motor Architecture

The final actuation system is centered around the EV3 motor outputs.

```text
                         LEGO EV3
                            │
               ┌────────────┴────────────┐
               │                         │
               ▼                         ▼
           PORT A                    PORT B
               │                         │
               ▼                         ▼
         DRIVE MOTOR               STEERING MOTOR
               │                         │
               ▼                         ▼
        Rear Drivetrain           Steering Linkage
               │                         │
               ▼                         ▼
          Rear Wheels             Front Wheels
               │                         │
               └────────────┬────────────┘
                            ▼
                     VEHICLE MOTION
```

The drive and steering systems are mechanically related through the movement of the complete robot, but they are controlled independently by software.

This is important because Piolín can reduce propulsion speed while keeping a strong steering command, or maintain a higher forward speed while making only a small steering correction.

---

# 3.2 Drive Motor

The **drive motor connected to EV3 Port A** is responsible for Piolín's propulsion.

Its output is transmitted to the rear drivetrain, which converts motor rotation into vehicle movement. The rear wheels therefore provide the primary traction force that moves Piolín around the competition field.

The complete propulsion chain is:

```text
EV3 Port A
     ↓
Drive Motor
     ↓
Mechanical Transmission
     ↓
Rear Axle
     ↓
Rear Wheels
     ↓
Forward / Reverse Motion
```

Because the drive motor is connected directly to the EV3, Piolín does not require an external H-bridge or separate motor controller for its final propulsion system.

This keeps the actuation architecture integrated with the same controller that reads the sensors and calculates the navigation behavior.

---

## 3.3 Rear Wheel Geometry

Piolín's final rear wheels have a measured diameter of approximately:

```text
REAR_DIAMETER = 2.4 in
```

Using the conversion:

```text
1 in = 25.4 mm
```

the diameter becomes:

```text
REAR_DIAMETER = 2.4 × 25.4
```

```text
REAR_DIAMETER = 60.96 mm
```

Therefore:

```text
REAR_DIAMETER ≈ 61.0 mm
```

The corresponding radius is approximately:

```text
REAR_RADIUS ≈ 30.5 mm
```

The wheel circumference can be calculated using:

```text
CIRCUMFERENCE = PI × DIAMETER
```

Therefore:

```text
CIRCUMFERENCE = PI × 60.96
```

which gives approximately:

```text
REAR_CIRCUMFERENCE ≈ 191.5 mm
```

This means that one complete rotation of a rear wheel corresponds geometrically to approximately **191.5 mm of travel** if the wheel rolls without slipping.

| Rear Wheel Parameter | Value |
| :--- | :---: |
| **Diameter** | **~61.0 mm** |
| **Radius** | **~30.5 mm** |
| **Circumference** | **~191.5 mm** |
| **Primary Function** | Propulsion |

---

## 3.4 Motor Rotation and Vehicle Movement

The drive motor includes encoder feedback, allowing the EV3 to know how much the motor has rotated.

Motor rotation can therefore be related to theoretical wheel travel.

For a complete wheel rotation:

```text
1 rotation = 360°
```

and:

```text
DISTANCE = WHEEL_ROTATIONS × WHEEL_CIRCUMFERENCE
```

Using Piolín's rear wheel circumference:

```text
DISTANCE = WHEEL_ROTATIONS × 191.5 mm
```

For example:

```text
1 wheel rotation ≈ 191.5 mm
```

```text
2 wheel rotations ≈ 383.0 mm
```

```text
5 wheel rotations ≈ 957.5 mm
```

The same relationship can be written using degrees:

```text
WHEEL_ROTATIONS = ROTATION_DEGREES / 360
```

therefore:

```text
DISTANCE =
(ROTATION_DEGREES / 360) × 191.5 mm
```

This relationship describes the geometric connection between wheel rotation and vehicle movement.

In real operation, the actual physical distance can differ slightly because of tire deformation, drivetrain play, wheel slip, and friction between the tire and the competition surface.

For this reason, the encoder is treated as a **repeatable rotational reference**, rather than as a perfect measurement of absolute ground distance.

---

## 3.5 Why Encoder Feedback Is Important

Without encoder feedback, propulsion would need to rely almost completely on time.

A command such as:

```text
Drive for 1 second
```

does not necessarily produce exactly the same physical displacement every time because motor load, battery condition, mechanical resistance, and surface friction can affect the result.

Encoder information provides a more direct reference:

```text
Motor rotates
      ↓
Encoder measures rotation
      ↓
EV3 knows motor displacement
```

This is especially useful for controlled movements where the software needs a repeatable reference for how far the drivetrain has rotated.

The encoder does not eliminate physical wheel slip, but it provides a much more useful mechanical reference than elapsed time alone.

---

# 3.6 Speed and Wheel Rotation

The speed of Piolín is directly related to the rotational speed of the rear wheels.

The relationship between wheel RPM and theoretical vehicle velocity is:

```text
LINEAR_SPEED =
(RPM × WHEEL_CIRCUMFERENCE) / 60
```

Using Piolín's rear-wheel circumference:

```text
WHEEL_CIRCUMFERENCE = 0.1915 m
```

the equation becomes:

```text
LINEAR_SPEED =
(RPM × 0.1915) / 60
```

For example, a wheel rotating at:

```text
100 RPM
```

would correspond geometrically to:

```text
LINEAR_SPEED =
(100 × 0.1915) / 60
```

```text
LINEAR_SPEED ≈ 0.319 m/s
```

This value is an example of the mathematical relationship between rotational speed and linear velocity. It is not presented as Piolín's measured competition speed.

The actual speed of the complete robot also depends on motor command, battery condition, mechanical load, drivetrain resistance, tire behavior, and the current navigation state.

---

# 3.7 Vehicle Mass and Drive Force

Piolín's final measured mass is approximately:

```text
MASS = 0.80476 kg
```

The basic relationship between mass, acceleration, and force is:

```text
FORCE = MASS × ACCELERATION
```

For Piolín:

```text
FORCE = 0.80476 × ACCELERATION
```

If an idealized acceleration of:

```text
1 m/s²
```

is considered, the inertial force would be:

```text
FORCE = 0.80476 × 1
```

```text
FORCE ≈ 0.805 N
```

This calculation represents only the ideal force associated with accelerating the robot's mass.

In the physical drivetrain, additional force is required to overcome axle friction, tire deformation, rolling resistance, transmission resistance, and other mechanical losses.

Those additional forces are not assigned arbitrary coefficients in this document because they are physical properties of the complete robot rather than fixed theoretical constants.

---

# 3.8 Wheel Torque Relationship

Torque at the driven wheel is related to tangential ground force through:

```text
TORQUE = FORCE × WHEEL_RADIUS
```

Piolín's rear wheel radius is approximately:

```text
REAR_RADIUS = 0.0305 m
```

Using the idealized force example:

```text
FORCE ≈ 0.805 N
```

the corresponding wheel torque would be:

```text
TORQUE = 0.805 × 0.0305
```

```text
TORQUE ≈ 0.0246 N·m
```

This is an ideal mechanical calculation showing the relationship between robot mass, acceleration, wheel radius, and wheel torque. It does not represent the complete real torque requirement because mechanical losses are also present.

The wheel radius produces an important engineering relationship:

```text
LARGER WHEEL
      │
      ├── Greater travel per rotation
      │
      └── Greater torque required
          for the same ground force


SMALLER WHEEL
      │
      ├── Less travel per rotation
      │
      └── Lower torque required
          for the same ground force
```

Piolín's approximately 61 mm rear wheels therefore influence both vehicle speed and drivetrain load.

---

# 3.9 Why Stall Torque Does Not Describe Normal Driving

A motor's stall torque represents the torque produced when the motor shaft cannot rotate.

At stall:

```text
MOTOR SPEED = 0
```

This is very different from normal autonomous driving.

Piolín requires the motor to produce torque while simultaneously rotating at a useful speed. Therefore, stall torque alone does not describe the actual performance of the propulsion system during a competition run.

Motor behavior generally follows the relationship:

```text
Higher mechanical load
        ↓
Lower motor speed
        ↓
Higher required torque
```

while:

```text
Lower mechanical load
        ↓
Higher achievable speed
```

The final propulsion system is therefore considered as a balance between **speed and available torque**, rather than as a system designed around maximum stall torque.

---

# 3.10 Variable Propulsion Speed

Motor A does not operate at one permanent speed throughout the entire course.

Different navigation situations require different propulsion behavior.

During a straight section, Piolín can use a relatively higher speed because the steering corrections are normally smaller and the track geometry is predictable.

During a corner, lower propulsion speed can provide the steering system with more physical time to change the robot's trajectory.

During obstacle avoidance, the drive speed can also be controlled so that the steering mechanism has enough time to produce the commanded avoidance path.

The general relationship is:

```text
STRAIGHT
   ↓
Higher practical speed


CORNER
   ↓
Controlled speed


OBSTACLE MANEUVER
   ↓
Controlled speed


FRONTAL EMERGENCY
   ↓
STOP
```

This means that propulsion is part of Piolín's navigation logic rather than simply an ON/OFF function.

---

# 3.11 Interaction Between Speed and Steering

The drive motor does not determine steering angle, but its speed strongly affects the trajectory produced by the steering system.

The actual path of the robot depends on both:

```text
DRIVE SPEED
     +
STEERING ANGLE
     ↓
ROBOT TRAJECTORY
```

A strong steering command at high propulsion speed can produce a very different physical result from the same steering command at a lower speed.

At higher speed, inertia can carry Piolín farther before the steering system changes its direction sufficiently. At a lower speed, the same steering angle can produce a more controlled trajectory.

For this reason, propulsion and steering are treated as interconnected control variables even though they are physically controlled by separate motors.

---

# 3.12 Drive Motor During Straight Navigation

During straight track sections, Motor A provides continuous propulsion while the steering motor performs small directional corrections.

Conceptually:

```text
                 STRAIGHT SECTION
                        │
                        ▼
                    MOTOR A
                Forward Propulsion
                        │
                        +
                        │
                    MOTOR B
              Small Corrections
                        │
                        ▼
                Stable Trajectory
```

The ultrasonic sensors continuously provide information about Piolín's relationship with the track walls.

The EV3 can therefore maintain propulsion while modifying steering independently.

This separation prevents normal wall-following corrections from requiring changes to the drivetrain architecture.

---

# 3.13 Drive Motor During Corner Navigation

When Piolín enters a corner, the steering demand becomes significantly larger than during a straight section.

The propulsion system must therefore work together with the Ackermann steering mechanism.

```text
Corner detected
      ↓
Navigation state changes
      ↓
Steering demand increases
      +
Drive speed controlled
      ↓
Vehicle follows corner
```

Reducing propulsion when necessary allows the front wheels more time to redirect the robot before Piolín reaches the next wall.

The drive motor therefore contributes indirectly to corner accuracy even though Motor B is responsible for the physical steering angle.

---

# 3.14 Drive Motor During Obstacle Avoidance

During the Obstacle Challenge, the propulsion system must also respond to pillar detections from the vision subsystem.

The HuskyLens provides obstacle information through the Arduino Nano, and the EV3 determines the corresponding avoidance behavior.

The relationship becomes:

```text
HuskyLens
     ↓
Arduino Nano
     ↓
LEGO EV3
     ↓
Obstacle Decision
     │
     ├──────────────┐
     ▼              ▼
  MOTOR A         MOTOR B
Controlled       Avoidance
  Speed          Steering
     │              │
     └──────┬───────┘
            ▼
      Obstacle Path
```

Piolín can therefore modify both propulsion and steering during an avoidance maneuver without changing the physical drivetrain configuration.

---

# 3.15 Emergency Propulsion Stop

The front ultrasonic sensor connected to S1 provides a high-priority safety input for the drive system.

The sensor does not continuously control Motor A. Instead, it can interrupt normal propulsion if the EV3 determines that something is dangerously close directly ahead.

```text
Front Ultrasonic
       │
       ▼
Frontal danger?
       │
   ┌───┴───┐
   │       │
  NO      YES
   │       │
   ▼       ▼
Normal   Stop /
Drive    Brake
```

This creates an independent relationship between frontal safety and propulsion.

Even if Piolín is currently executing wall-following, corner handling, or obstacle avoidance, a sufficiently dangerous frontal condition can take priority over the normal drive command.

This does not guarantee that every physical collision is impossible. It provides an additional safety layer designed to reduce the risk of continued propulsion toward a directly detected frontal obstacle.

---

# 3.16 Physical Braking Behavior

A motor command can change immediately, but the physical robot cannot stop with zero distance.

Piolín has mass and therefore momentum while moving.

The physical sequence is:

```text
Stop command
     ↓
Motor braking begins
     ↓
Vehicle decelerates
     ↓
Robot stops
```

This distinction is important because software stopping and physical stopping are not the same event.

The propulsion system therefore interacts directly with Piolín's safety architecture. Higher vehicle speed produces greater momentum, while controlled speed gives the robot more room to respond to navigation and safety information.

---

# 3.17 Battery and Motor Behavior

The EV3 supplies the motors from the robot's battery system.

Motor behavior can therefore change as electrical conditions change.

The power path is:

```text
BATTERY
   ↓
LEGO EV3
   ↓
┌───────────────┐
│               │
▼               ▼
MOTOR A       MOTOR B
Drive         Steering
```

Both motors can operate simultaneously, meaning that propulsion and steering share the same EV3 power source.

Mechanical load also affects motor behavior. A steering mechanism under increased resistance and a drivetrain accelerating the complete robot can create a different electrical demand than a motor operating with little mechanical load.

The battery and power-distribution architecture are documented separately in the dedicated component sections.

---

# 3.18 Mechanical Sources of Propulsion Error

The encoder measures motor rotation, but several mechanical elements exist between motor rotation and real vehicle movement.

```text
MOTOR ENCODER
      ↓
MOTOR SHAFT
      ↓
DRIVETRAIN
      ↓
REAR WHEELS
      ↓
TIRE / FLOOR INTERACTION
      ↓
REAL VEHICLE MOVEMENT
```

Mechanical play, axle resistance, loose wheel connections, tire deformation, and wheel slip can all affect the relationship between motor rotation and physical displacement.

This is why Piolín's propulsion system is treated as a complete mechanical chain rather than as the motor alone.

A software command can be correct while the resulting physical movement differs because of mechanical behavior elsewhere in the drivetrain.

---

# 3.19 Steering Motor Relationship

The second EV3 motor, connected to **Port B**, is responsible for controlling Piolín's front-wheel steering mechanism.

Unlike Motor A, Motor B is not used to create forward propulsion.

Its job is to move the mechanical linkage that changes the angle of the front wheels.

```text
MOTOR A
   ↓
PROPULSION


MOTOR B
   ↓
STEERING
```

The two motors therefore complement each other.

Motor A determines how Piolín advances through the track, while Motor B determines the direction of that movement.

The steering motor, its encoder reference, mechanical linkage, steering limits, and relationship with Ackermann geometry are documented in detail in:

```text
docs/components/04_SteeringMotor.md
```

---

# 3.20 Why Two Separate Motors Were Selected

Using independent propulsion and steering actuators gives Piolín greater control over its vehicle behavior.

With differential steering, wheel speed differences are responsible for both propulsion and rotation.

Piolín instead separates those functions:

```text
              DIFFERENTIAL SYSTEM

Left Motor ──┐
             ├── Speed + Direction
Right Motor ─┘


              PIOLÍN SYSTEM

Drive Motor ─────── Propulsion
Steering Motor ──── Direction
```

This arrangement more closely resembles the control architecture of a conventional road vehicle.

The separation also makes the software easier to reason about. A propulsion adjustment changes speed without intentionally changing steering geometry, while a steering adjustment changes vehicle direction without requiring independent left/right drive-wheel commands.

---

# 3.21 Motor Responsibility by Navigation Situation

The two motors work together differently depending on Piolín's current navigation state.

| Navigation Situation | Drive Motor A | Steering Motor B |
| :--- | :--- | :--- |
| **Straight Navigation** | Provides forward propulsion | Performs small wall-following corrections |
| **Corner Entry** | Maintains controlled movement | Begins stronger steering |
| **Corner** | Controls corner speed | Holds required turning direction |
| **Corner Exit** | Returns toward straight speed | Reduces steering toward center |
| **Obstacle Approach** | Provides controlled approach | Prepares avoidance trajectory |
| **Obstacle Avoidance** | Controls forward movement | Produces avoidance steering |
| **Recovery** | Continues propulsion | Re-centers trajectory |
| **Frontal Emergency** | **Stops / brakes** | No normal navigation priority |

This demonstrates that the motors are not independent from the software state machine even though their mechanical roles remain separate.

---

# 3.22 Integration With Piolín's Complete Hardware System

The motor system forms the final output stage of Piolín's autonomous architecture.

```text
                    ENVIRONMENT
                        │
          ┌─────────────┼─────────────┐
          │             │             │
          ▼             ▼             ▼
     ULTRASONICS      COLOR       HUSKYLENS
          │             │             │
          │             │         ARDUINO
          │             │             │
          └─────────────┴──────┬──────┘
                               ▼
                            LEGO EV3
                               │
                        Navigation Logic
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
                 MOTOR A               MOTOR B
                 DRIVE                STEERING
                    │                     │
                    ▼                     ▼
              Rear Wheels          Front Wheels
                    │                     │
                    └──────────┬──────────┘
                               ▼
                        ROBOT MOVEMENT
```

The sensors describe what is happening around Piolín. The EV3 interprets that information. The two motors then convert those decisions into physical motion.

This closes the autonomous control loop.

---

# 3.23 Engineering Considerations

The final motor architecture involves several important engineering trade-offs.

| Design Choice | Main Advantage | Engineering Consideration |
| :--- | :--- | :--- |
| **Dedicated drive motor** | Independent propulsion control | Requires separate steering actuator |
| **Dedicated steering motor** | Vehicle-like directional control | Adds mechanical steering linkage |
| **Rear propulsion** | Compatible with front Ackermann steering | Rear traction influences acceleration |
| **~61 mm drive wheels** | Larger travel per wheel rotation | Greater torque requirement for a given ground force |
| **Encoder feedback** | Repeatable rotational reference | Cannot directly detect wheel slip |
| **Variable drive speed** | Allows different behavior for straights and corners | Requires software coordination |
| **EV3 direct motor control** | Simple integration with main controller | Both motors share the EV3 power system |
| **Independent emergency stop** | Can interrupt unsafe forward motion | Physical stopping still requires distance |

The final design was therefore not selected simply to maximize motor power or wheel speed. It was selected to create a drivetrain that works predictably with Piolín's steering geometry, sensors, and autonomous software.

---

# 3.24 Final Motor Architecture Summary

Piolín's final actuation system uses two EV3-controlled motors with clearly separated responsibilities.

```text
                   LEGO EV3
                      │
        ┌─────────────┴─────────────┐
        │                           │
        ▼                           ▼
     PORT A                      PORT B
        │                           │
        ▼                           ▼
  DRIVE MOTOR                 STEERING MOTOR
        │                           │
        ▼                           ▼
 REAR DRIVETRAIN             ACKERMANN LINKAGE
        │                           │
        ▼                           ▼
   REAR WHEELS                  FRONT WHEELS
        │                           │
        └─────────────┬─────────────┘
                      ▼
                PIOLÍN MOTION
```

The drive motor provides propulsion through the rear drivetrain and works with approximately **61 mm rear wheels**, giving a theoretical rolling circumference of approximately **191.5 mm**.

The steering motor operates independently and changes the direction of the front wheels through Piolín's Ackermann mechanism.

The most important feature of this architecture is not the presence of two motors by itself. It is the **separation of responsibilities** between them.

> **Motor A controls how Piolín moves forward. Motor B controls where Piolín moves.**

This separation allows propulsion, steering, sensing, and safety logic to work together as parts of one complete autonomous vehicle system.

Detailed information about the steering actuator and mechanical steering linkage is provided in the next section, `04_SteeringMotor.md`.
