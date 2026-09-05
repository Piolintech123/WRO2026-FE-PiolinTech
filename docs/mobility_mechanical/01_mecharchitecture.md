# 1. Mechanical Architecture

Piolín is a compact autonomous vehicle designed for the **WRO Future Engineers 2026** competition.

Its mechanical architecture is based on a car-like layout with:

```text
Rear-wheel propulsion
        +
Front-wheel Ackermann steering
        +
Rigid LEGO Technic chassis
        +
Dedicated sensor mounting
        +
Central LEGO EV3 control
```

The objective of the mechanical design is not simply to support the electronics.

The chassis must convert software commands into predictable physical motion while keeping the sensors in stable positions relative to the track.

For this reason, Piolín was developed as an integrated system in which:

```text
MECHANICS
    ↓
Determines physical movement


SENSORS
    ↓
Describe the environment


SOFTWARE
    ↓
Calculates the response


MOTORS
    ↓
Execute that response
```

The current mechanical configuration described in this document represents the final Piolín architecture rather than earlier experimental versions.

For historical configurations, see:

[Legacy Documentation](../legacy/00_LEGACY_NOTICE.md)

---

## 1.1 Mechanical Design Philosophy

Piolín follows a conventional vehicle architecture rather than a differential-drive robot layout.

The vehicle separates propulsion and steering into two independent mechanical functions:

```text
PROPULSION
    ↓
Rear wheels
    ↓
Motor A


STEERING
    ↓
Front wheels
    ↓
Motor B
    ↓
Ackermann linkage
```

This separation was selected because the Future Engineers track is fundamentally a road-navigation problem.

Instead of independently changing the speed of left and right drive wheels to turn, Piolín changes the orientation of the front wheels while the rear drivetrain continues providing forward motion.

The result is a motion model closer to a small automobile.

---

# 1.2 Current Mechanical Configuration

The final Piolín mechanical architecture is organized around the LEGO Mindstorms EV3 and a LEGO Technic structural chassis.

The main physical subsystems are:

| Subsystem | Current Configuration | Main Mechanical Function |
| :--- | :--- | :--- |
| **Chassis** | LEGO Technic structure | Supports and aligns all subsystems |
| **Drive System** | Rear propulsion | Produces longitudinal motion |
| **Drive Motor** | Motor A | Powers drivetrain |
| **Steering System** | Front Ackermann-style linkage | Changes vehicle direction |
| **Steering Motor** | Motor B | Actuates steering mechanism |
| **Rear Wheels** | ~61.0 mm diameter | Propulsion interface with track |
| **Front Wheels** | 38.1 mm diameter | Directional steering wheels |
| **Sensor Structure** | Front + lateral + downward mounts | Maintains sensor geometry |
| **Vision Mount** | Forward HuskyLens mounting | Supports obstacle perception |
| **Main Controller Mount** | LEGO EV3 integrated into chassis | Central control and structural mass |

The mechanical layout can be represented conceptually as:

```text
                         FRONT
                           ↑

                     HuskyLens
                         │
                         ▼

                  Front Ultrasonic
                         │

          Front Left Wheel     Front Right Wheel
                 \                 /
                  \               /
                   ACKERMANN LINKAGE
                          │
                          ▼
                       Motor B
                       Steering


                    [ LEGO EV3 ]


                        Motor A
                          │
                          ▼
                    Rear Drivetrain
                     /           \
                    /             \
          Rear Left Wheel     Rear Right Wheel

                           ↓
                          REAR
```

This diagram is conceptual and is intended to show subsystem relationships rather than exact scale.

---

# 1.3 Confirmed Overall Dimensions

The current Piolín robot has the following confirmed overall dimensions:

| Parameter | Final Measured Value |
| :--- | :---: |
| **Length** | **210 mm** |
| **Width** | **150 mm** |
| **Height** | **230 mm** |
| **Mass** | **0.80476 kg** |

These dimensions describe the assembled robot rather than an isolated chassis frame.

They include the integrated mechanical structure, controller, sensors, and mounted electronics that form the current Piolín configuration.

The approximate bounding volume is therefore:

```text
210 mm
Length

150 mm
Width

230 mm
Height
```

The compact footprint is important because the vehicle must maneuver between track boundaries while still carrying the sensing and vision systems required for autonomous operation.

---

# 1.4 Vehicle Reference Axes

To describe Piolín's movement consistently, the vehicle can be represented using three primary axes.

```text
                    Z
                    ↑
                    │
                    │
                    ●──────→ X
                   /
                  /
                 Y
```

For the purposes of this documentation:

```text
Longitudinal direction
=
Forward / backward motion


Lateral direction
=
Left / right position


Vertical direction
=
Height above track
```

The principal vehicle behaviors therefore correspond to:

```text
TRANSLATION
    ↓
Movement along the track


STEERING
    ↓
Rotation of the vehicle heading


LATERAL POSITION
    ↓
Distance relative to track walls
```

This distinction is important because the sensors and mechanical system do not measure or control all three quantities in the same way.

---

# 1.5 Propulsion Architecture

Piolín uses a dedicated rear propulsion system controlled by **Motor A**.

The propulsion chain can be described as:

```text
Motor A
   ↓
Mechanical drivetrain
   ↓
Rear axle / driven wheels
   ↓
Track surface
   ↓
Vehicle translation
```

The drive system has one primary responsibility:

> Convert motor rotation into forward or backward vehicle movement.

It does not determine the steering direction.

That responsibility belongs to the front steering system.

This separation allows the software to treat:

```text
SPEED
```

and:

```text
STEERING
```

as different control variables.

Current propulsion documentation:

[Drive Motor and Motor System](../components/03_Motors.md)

[Drivetrain](05_drivetrain.md)

---

# 1.6 Rear Wheel Geometry

The current rear wheel diameter is approximately:

```text
D_REAR ≈ 61.0 mm
```

Therefore:

```text
R_REAR ≈ 30.5 mm
```

The theoretical circumference is:

```text
C_REAR = PI × D_REAR
```

so:

```text
C_REAR ≈ PI × 61.0
```

```text
C_REAR ≈ 191.5 mm
```

This means that one ideal full wheel rotation corresponds to approximately:

```text
191.5 mm
```

of linear travel if slip and deformation are neglected.

For an encoder rotation of `THETA` degrees, the idealized linear displacement can be written as:

```text
DISTANCE =
(THETA / 360) × C_REAR
```

or:

```text
DISTANCE ≈
(THETA / 360) × 191.5 mm
```

This relationship is useful when relating motor encoder rotation to physical vehicle movement.

Actual vehicle displacement can differ because of tire deformation, steering, surface interaction, and wheel slip.

---

# 1.7 Front Steering Architecture

Piolín uses front-wheel steering actuated by **Motor B**.

The steering chain is:

```text
Motor B
   ↓
Steering linkage
   ↓
Left and right steering arms
   ↓
Front wheels
   ↓
Vehicle turning path
```

The mechanism is based on an **Ackermann-style steering geometry**.

Instead of keeping both front wheels at exactly the same steering angle, the mechanical linkage allows the inner and outer wheels to follow different trajectories during a turn.

This is important because:

```text
INNER FRONT WHEEL
      ↓
Follows smaller radius


OUTER FRONT WHEEL
      ↓
Follows larger radius
```

A car-like steering arrangement therefore reduces the geometric conflict that would occur if both wheels were forced to follow the same circular path.

Current steering documentation:

[Steering Motor](../components/04_SteeringMotor.md)

[Steering Geometry](04_steering.md)

---

# 1.8 Front Wheel Geometry

The current front wheel diameter is:

```text
D_FRONT = 38.1 mm
```

Therefore:

```text
R_FRONT = 19.05 mm
```

and the theoretical circumference is:

```text
C_FRONT = PI × D_FRONT
```

```text
C_FRONT ≈ 119.7 mm
```

The front wheels are smaller than the rear propulsion wheels.

Their primary mechanical responsibility is directional control rather than drivetrain propulsion.

The different wheel sizes therefore correspond to different subsystem roles:

| Wheel Set | Diameter | Main Role |
| :--- | :---: | :--- |
| **Front** | **38.1 mm** | Steering |
| **Rear** | **~61.0 mm** | Propulsion |

---

# 1.9 Ackermann Steering Principle

When a vehicle turns, the inner and outer front wheels cannot follow the same turning radius.

Conceptually:

```text
                 TURN CENTER
                      ●


                R_INNER
           ────────────────
                  ↗

       INNER WHEEL      OUTER WHEEL
            \               \
             \               \
              \               \
               [   PIOLÍN   ]
```

For an ideal Ackermann vehicle, the wheel angles satisfy:

```text
cot(THETA_OUTER) - cot(THETA_INNER)
=
W / L
```

where:

```text
THETA_INNER
=
Inner front-wheel steering angle


THETA_OUTER
=
Outer front-wheel steering angle


W
=
Front track width


L
=
Wheelbase
```

The corresponding ideal angles for a vehicle following a radius `R` can be represented as:

```text
THETA_INNER =
atan(L / (R - W/2))
```

and:

```text
THETA_OUTER =
atan(L / (R + W/2))
```

The current documentation does not assign numerical values to `W` or `L` because final confirmed measurements for those dimensions are not being claimed here.

The equations describe the mechanical principle behind the steering architecture.

---

# 1.10 Motor Angle vs. Physical Wheel Angle

An important characteristic of Piolín's steering mechanism is that:

```text
STEERING MOTOR ANGLE
        ≠
PHYSICAL FRONT WHEEL ANGLE
```

Motor B rotates through the LEGO steering linkage before changing the front-wheel orientation.

The relationship is therefore:

```text
Motor Encoder Position
        ↓
Linkage Motion
        ↓
Steering Rack / Steering Arms
        ↓
Physical Wheel Angle
```

This relationship depends on the geometry of the mechanical linkage.

For this reason, a command such as:

```text
Motor B = 20°
```

should not automatically be interpreted as:

```text
Front wheels = 20°
```

The motor encoder describes actuator position.

The physical wheel angle describes the resulting mechanical steering geometry.

This distinction is essential when interpreting steering software.

---

# 1.11 Mechanical Steering Center

The steering system requires a mechanical center reference.

Conceptually:

```text
LEFT STEERING
      ←

      [ CENTER ]

                →

          RIGHT STEERING
```

At the neutral steering position, the front wheels are approximately aligned with the longitudinal direction of the chassis.

The software uses this mechanical center as the reference from which left and right steering commands are applied.

If the physical steering center does not correspond to the assumed software center, Piolín can develop a continuous directional bias even when the navigation controller requests straight movement.

Therefore:

```text
SOFTWARE ZERO
      ↓
must correspond closely to
      ↓
MECHANICAL CENTER
```

This is one of the most important interfaces between software calibration and mechanical construction.

---

# 1.12 Mechanical Steering Limits

The steering mechanism also has finite physical travel.

Conceptually:

```text
MAXIMUM LEFT
     │
     │<------ SAFE MECHANICAL RANGE ------>│
                                           │
                                      MAXIMUM RIGHT
```

Software steering commands should remain within a range that the physical mechanism can achieve without forcing the linkage beyond its intended motion.

Excessive steering commands can result in:

```text
Mechanical binding

High motor load

Linkage stress

Reduced repeatability

Delayed steering recovery
```

The final software therefore treats steering as a constrained actuator rather than an unlimited angular command.

---

# 1.13 Chassis Structure

The chassis is built primarily from LEGO Technic structural elements.

Its responsibilities include:

```text
Holding the drivetrain

Supporting the steering system

Maintaining wheel alignment

Supporting the EV3

Supporting ultrasonic sensors

Supporting the color sensor

Supporting the vision system

Protecting cable routing
```

The chassis must keep these elements aligned relative to one another.

This is especially important because sensor data is interpreted using the physical orientation of the sensors.

For example:

```text
Lateral sensor rotates
        ↓
Measured surface changes
        ↓
Distance interpretation changes
```

Mechanical structure therefore directly affects navigation data.

---

# 1.14 Structural Rigidity

A steering controller assumes that the commanded mechanical geometry remains reasonably consistent.

If the chassis or steering structure deforms significantly under load, then:

```text
Commanded steering position
        ↓
Mechanical geometry changes unexpectedly
        ↓
Vehicle response changes
```

For this reason, Piolín's structural architecture aims to limit unnecessary movement between:

```text
Motor

Steering linkage

Wheel mounts

Sensor mounts

EV3 frame
```

The purpose is not to claim that the LEGO structure has zero deformation.

Instead, the design attempts to maintain sufficient structural consistency for repeatable autonomous control.

---

# 1.15 Mechanical and Software Coupling

The software cannot be separated completely from the physical vehicle.

For example, suppose the program requests:

```text
Steering = LEFT
```

The actual vehicle response depends on:

```text
Motor B movement

Linkage geometry

Wheel angle

Vehicle speed

Tire interaction

Vehicle mass

Track surface
```

Therefore:

```text
SOFTWARE COMMAND
        ↓
MECHANICAL RESPONSE
        ↓
ACTUAL VEHICLE TRAJECTORY
```

The mechanical architecture defines the physical system that the control algorithm is attempting to regulate.

---

# 1.16 Sensor Mounting as Part of Mechanical Design

The sensors are not simply electronic accessories attached anywhere on the robot.

Their positions and orientations are part of the mechanical architecture.

Current Piolín uses:

```text
S1 → Front Ultrasonic

S2 → Right Ultrasonic

S3 → Left Ultrasonic

S4 → Downward Color Sensor
```

The HuskyLens is mounted forward for obstacle perception.

Each sensor is positioned according to its function.

---

# 1.17 Lateral Ultrasonic Mounting

The two lateral ultrasonic sensors are mounted to observe the walls on either side of Piolín.

Their approximate mounting height above the track surface is:

```text
43.2 mm
```

The arrangement is:

```text
                   FRONT
                     ↑

              ┌─────────────┐
              │             │
LEFT US  ←    │   PIOLÍN    │    →  RIGHT US
   S3         │             │         S2
              └─────────────┘
```

These sensors provide the physical wall geometry used by the navigation software.

Because their readings depend on their orientation, rigid mounting is important.

Current documentation:

[Ultrasonic Sensors](../components/05_UltrasonicSensors.md)

---

# 1.18 Front Ultrasonic Mounting

The front ultrasonic sensor is mounted facing forward.

Its mechanical role differs from the lateral pair.

```text
                   FRONT WALL
                       │
                       │
                       ▼

               [ FRONT US S1 ]
                       │
                       │
                  [ PIOLÍN ]
```

The front sensor provides an independent frontal-distance reference used for safety.

It does not participate in the normal inner-wall and outer-wall navigation geometry.

This is an important mechanical and software separation.

---

# 1.19 Color Sensor Mounting

The color sensor is mounted underneath Piolín and faces the track surface.

Conceptually:

```text
             [ PIOLÍN ]
                 │
                 ▼
           COLOR SENSOR
                 │
                 ▼
        TRACK FLOOR MARKING
```

Its orientation is fundamentally different from the ultrasonic sensors.

The ultrasonic sensors observe surrounding geometry.

The color sensor observes the surface directly below the robot.

A casing around the color sensor helps isolate its observation area from surrounding light and supports more consistent floor-color detection.

Current documentation:

[Color Sensor](../components/06_ColorSensor.md)

---

# 1.20 Vision-System Mounting

The HuskyLens is installed toward the front of Piolín.

Its mechanical placement determines:

```text
Field of view

Visible obstacle region

Detection timing

Occlusion from robot structure
```

Therefore, the camera mount is part of the navigation architecture rather than merely a support bracket.

Conceptually:

```text
              CAMERA FIELD OF VIEW
                   \           /
                    \         /
                     \       /
                      \     /
                     HuskyLens
                         │
                     [ PIOLÍN ]
```

The vision system is used during the Obstacle Challenge.

It does not replace the ultrasonic wall-navigation geometry.

Current vision documentation:

[HuskyLens](../components/07_HuskyLens.md)

---

# 1.21 Controller Placement

The LEGO EV3 is physically integrated into the central robot structure.

This provides:

```text
Short connection paths to sensors

Direct motor connection

Centralized controller placement

Structural integration

Accessible control interface
```

Because the EV3 also contributes a significant part of the robot's mass, its location affects the overall mass distribution.

The mechanical design therefore treats the controller as both:

```text
An electronic component
```

and:

```text
A physical chassis component
```

The final robot mass of:

```text
0.80476 kg
```

includes the integrated controller and associated hardware.

---

# 1.22 Mass and Normal Force

The current measured robot mass is:

```text
m = 0.80476 kg
```

Using:

```text
g = 9.81 m/s²
```

the approximate gravitational force is:

```text
P = m × g
```

```text
P = 0.80476 × 9.81
```

```text
P ≈ 7.89 N
```

Therefore, on a level surface and neglecting dynamic vertical effects, the total normal force from the track is approximately equal in magnitude to:

```text
7.89 N
```

This does not mean that the force is distributed equally across all four wheels.

The actual load distribution depends on the position of the robot's center of mass.

---

# 1.23 Traction and Propulsion

The drive motor produces torque that eventually acts at the rear wheel radius.

The ideal relationship between wheel torque and tangential force is:

```text
F =
TAU / R
```

where:

```text
F
=
Tangential wheel force


TAU
=
Wheel torque


R
=
Wheel radius
```

For Piolín's rear wheels:

```text
R_REAR ≈ 0.0305 m
```

so:

```text
F ≈
TAU / 0.0305
```

This is an ideal mechanical relationship.

The actual force available to accelerate the vehicle is also limited by tire-track interaction and drivetrain losses.

---

# 1.24 Longitudinal Acceleration

The relationship between net longitudinal force and acceleration is:

```text
F_NET =
m × a
```

Therefore:

```text
a =
F_NET / m
```

Using Piolín's measured mass:

```text
a =
F_NET / 0.80476
```

This demonstrates why robot mass affects dynamic response.

For the same available net drive force:

```text
Higher mass
    ↓
Lower acceleration


Lower mass
    ↓
Higher acceleration
```

However, mechanical design must balance low mass with sufficient rigidity and component support.

---

# 1.25 Turning Dynamics

When Piolín follows a curved trajectory, the vehicle experiences lateral acceleration.

The ideal relationship is:

```text
A_LATERAL =
V² / R
```

where:

```text
V
=
Vehicle speed


R
=
Turn radius
```

This means that lateral demand grows with the **square of speed**.

For example, doubling speed at the same turning radius produces approximately four times the lateral acceleration requirement.

This is one reason steering behavior and vehicle speed cannot be tuned independently.

```text
HIGHER SPEED
      ↓
Greater lateral demand
      ↓
Greater sensitivity to steering geometry
```

---

# 1.26 Why Speed Affects Steering

A steering command that works correctly at one velocity may produce a different trajectory at another.

The mechanical relationship is:

```text
STEERING ANGLE
      +
VEHICLE SPEED
      ↓
ACTUAL TURNING PATH
```

At greater speed:

```text
Momentum increases

Lateral acceleration increases

Available reaction time decreases
```

Therefore, Piolín's software can use different propulsion behavior depending on whether the robot is:

```text
Following a straight

Entering a corner

Avoiding an obstacle

Recovering its position
```

The drivetrain and steering system must therefore be considered together.

---

# 1.27 Inner and Outer Wheel Paths

During a turn, all four wheels follow different trajectories.

Conceptually:

```text
                 CENTER OF TURN
                       ●

      FRONT INNER         FRONT OUTER
           \                   \
            \                   \
             \                   \

       REAR INNER           REAR OUTER
```

The inner wheels travel along smaller-radius paths than the outer wheels.

The Ackermann steering mechanism helps align the front wheels with these different paths.

This reduces the need for the tires to slide laterally simply to satisfy the steering geometry.

---

# 1.28 Sensor Geometry During Turns

Turning also changes what the ultrasonic sensors observe.

During a straight:

```text
SIDE SENSOR
     ↓
Approximately perpendicular wall observation
```

During a turn:

```text
Robot heading changes
        ↓
Sensor orientation changes relative to wall
        ↓
Measured distance changes
```

Therefore, a distance change does not always mean that the robot translated directly toward or away from the wall.

It may also be caused by chassis rotation.

This is one reason the mechanical steering model is important to the navigation software.

---

# 1.29 Mechanical Architecture During Cornering

The current Open Challenge strategy is closely linked to the vehicle mechanics.

The navigation sequence is approximately:

```text
Follow Inner Wall
        ↓
Approach Corner
        ↓
Inner Wall Ends
        ↓
Steering Changes
        ↓
Vehicle Rotates
        ↓
Outer Wall Becomes Useful Reference
        ↓
Inner Wall Reappears
        ↓
Steering Reduced
        ↓
Straight Navigation Restored
```

The software can only interpret these sensor transitions correctly if the mechanical response to steering is sufficiently repeatable.

Therefore:

```text
CORNER LOGIC
      depends on
STEERING MECHANICS
```

and:

```text
SENSOR INTERPRETATION
      depends on
CHASSIS ORIENTATION
```

---

# 1.30 Mechanical Architecture During Obstacle Avoidance

During the Obstacle Challenge, Piolín must temporarily leave its normal wall-following trajectory to pass a colored pillar.

The mechanical sequence becomes:

```text
Normal path
    ↓
Obstacle identified
    ↓
Steering changes
    ↓
Vehicle moves around obstacle
    ↓
Wall geometry changes
    ↓
Obstacle cleared
    ↓
Steering recovery
    ↓
Normal navigation restored
```

The ability to recover depends strongly on the steering mechanism.

A camera may identify the correct obstacle, but the physical vehicle must still execute the requested trajectory.

Therefore:

```text
VISION
   ↓
Identifies obstacle


SOFTWARE
   ↓
Chooses response


MECHANICS
   ↓
Determines whether the trajectory
can physically be executed
```

---

# 1.31 Separation of Mechanical Responsibilities

Piolín's mechanical design intentionally separates major responsibilities.

| Mechanical Element | Primary Responsibility |
| :--- | :--- |
| **Rear drivetrain** | Vehicle propulsion |
| **Motor A** | Drive actuation |
| **Front steering mechanism** | Directional geometry |
| **Motor B** | Steering actuation |
| **Chassis** | Structural alignment |
| **Front wheels** | Direction control |
| **Rear wheels** | Traction and propulsion |
| **Sensor mounts** | Stable sensing geometry |
| **Vision mount** | Stable forward camera orientation |
| **EV3 mount** | Controller integration |

This separation makes mechanical behavior easier to understand and software behavior easier to trace.

---

# 1.32 Mechanical Failure Propagation

A mechanical problem can appear initially as a software or sensor problem.

For example:

```text
Loose steering linkage
        ↓
Wheel angle differs from expected
        ↓
Robot moves closer to wall
        ↓
Ultrasonic error increases
        ↓
Software commands stronger correction
```

The software may appear unstable even though the original cause was mechanical.

Similarly:

```text
Sensor mount moves
        ↓
Distance reading changes
        ↓
Navigation error changes
        ↓
Steering response changes
```

For this reason, mechanical consistency is fundamental to autonomous navigation.

---

# 1.33 Why a Car-Like Architecture Was Retained

The final vehicle continues to use Ackermann-style steering because it provides a clear mechanical relationship between:

```text
Steering actuator
        ↓
Front wheel direction
        ↓
Vehicle heading
```

This architecture also matches the general geometry of the WRO Future Engineers driving task.

The robot must repeatedly perform:

```text
Straight navigation

Corners

Obstacle bypasses

Position recovery

Parking-related movement
```

A front-steered chassis provides one consistent vehicle model for all of these behaviors.

---

# 1.34 Current Mechanical Architecture vs. Legacy Designs

Earlier Piolín documentation contains different sensor configurations, navigation assumptions, and prototype architectures.

These should not be mixed with the current mechanical configuration.

The final system is:

```text
CURRENT PIOLÍN

Rear propulsion
        +
Motor A
        +
Front Ackermann steering
        +
Motor B
        +
Three ultrasonic sensors
        +
Downward color sensor
        +
HuskyLens / Arduino Nano
        +
LEGO EV3
```

Historical configurations involving:

```text
Gyroscope

PixyCam

Raspberry Pi

Arduino Mega as main controller

Alternative ultrasonic arrangements
```

belong to:

[Legacy Documentation](../legacy/00_LEGACY_NOTICE.md)

---

# 1.35 Mechanical System Hierarchy

The complete current mechanical hierarchy can be summarized as:

```text
                         PIOLÍN
                            │
          ┌─────────────────┼─────────────────┐
          ▼                 ▼                 ▼
       STRUCTURE         MOBILITY          SENSING
          │                 │                 │
          │          ┌──────┴──────┐          │
          │          ▼             ▼          │
          │       DRIVE         STEERING      │
          │          │             │          │
          │       Motor A       Motor B       │
          │          │             │          │
          │       Rear Wheels   Ackermann     │
          │                        │           │
          │                   Front Wheels    │
          │                                    │
          └────────────────┬───────────────────┘
                           ▼
                    PHYSICAL VEHICLE
                           │
                           ▼
                      TRACK MOTION
```

Sensor information and software decisions operate on top of this physical architecture.

---

# 1.36 Relationship With the Rest of the Repository

This document provides the high-level mechanical architecture.

More detailed mechanical documentation is separated into dedicated files:

[Chassis Design](02_chassis.md)

[Robot Mobility](03_RMobility.md)

[Steering System](04_steering.md)

[Drivetrain](05_drivetrain.md)

[Mechanical Testing](06_testing.md)

Hardware-specific documentation is available in:

[Motors](../components/03_Motors.md)

[Steering Motor](../components/04_SteeringMotor.md)

[Ultrasonic Sensors](../components/05_UltrasonicSensors.md)

[Other Components](../components/10_OtherComponents.md)

This separation avoids repeating the same information in every section while still connecting the complete mechanical system.

---

# 1.37 Mechanical Architecture Summary

Piolín's final mechanical architecture is based on a clear separation between **propulsion, steering, sensing, and structure**.

The vehicle uses:

```text
Motor A
   ↓
Rear Propulsion


Motor B
   ↓
Ackermann Steering


Front Wheels
   ↓
Directional Control


Rear Wheels
   ↓
Traction and Motion


LEGO Technic Chassis
   ↓
Structural Integration


Sensor Mounts
   ↓
Stable Environmental Measurements
```

The confirmed current physical specifications are:

```text
Length           = 210 mm

Width            = 150 mm

Height           = 230 mm

Mass             = 0.80476 kg

Rear wheel       ≈ 61.0 mm diameter

Front wheel      = 38.1 mm diameter

Lateral US height ≈ 43.2 mm
```

The architecture is designed so that each subsystem has a clearly defined physical responsibility.

The software determines what Piolín should do.

The sensors describe the environment.

The EV3 processes that information.

The motors generate actuation.

The mechanical architecture transforms those commands into real vehicle motion.

```text
ENVIRONMENT
     ↓
SENSORS
     ↓
LEGO EV3
     ↓
CONTROL DECISION
     ↓
MOTOR A + MOTOR B
     ↓
MECHANICAL SYSTEM
     ↓
VEHICLE MOTION
     ↓
NEW ENVIRONMENTAL STATE
```

This closed interaction between sensing, computation, actuation, and mechanics forms the physical foundation of Piolín's autonomous navigation system.

Continue with:

[Chassis Design](02_chassis.md)

Return to:

[Hardware Overview](../components/01_Hardwareoverview.md)
