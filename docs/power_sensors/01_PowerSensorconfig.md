# 1. Power and Sensor Configuration

Piolín's sensing architecture is organized around the **LEGO Mindstorms EV3**, which acts as the main vehicle controller and receives the measurements required for autonomous navigation.

The current configuration combines:

```text
Three Ultrasonic Sensors
        +
One Downward Color Sensor
        +
HuskyLens Vision System
        +
Arduino Nano Interface
        +
LEGO EV3
```

The system is intentionally divided by responsibility.

The lateral ultrasonic sensors describe the geometry of the track walls.

The front ultrasonic sensor provides an independent frontal safety reference.

The color sensor identifies floor markings and course-state information.

The HuskyLens provides obstacle identity during the Obstacle Challenge.

The Arduino Nano supports communication between the vision subsystem and the EV3.

The EV3 combines these inputs and makes the final navigation decisions.

The complete information flow is:

```text
                    ENVIRONMENT
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
      WALLS          FLOOR MARKS      PILLARS
        │               │               │
        ▼               ▼               ▼
 ULTRASONICS        COLOR SENSOR      HUSKYLENS
        │               │               │
        │               │               ▼
        │               │          ARDUINO NANO
        │               │               │
        │               │              USB
        │               │               │
        └───────────────┴───────────────┘
                        ▼
                     LEGO EV3
                        │
                        ▼
                NAVIGATION DECISION
                        │
               ┌────────┴────────┐
               ▼                 ▼
            Motor A           Motor B
             Drive            Steering
```

This document describes the current sensor and power architecture of the final Piolín robot.

Historical systems involving the gyroscope, PixyCam, Raspberry Pi, or alternative controller arrangements are documented separately in:

[Legacy Documentation](../legacy/00_LEGACY_NOTICE.md)

---

## 1.1 Current EV3 Port Configuration

The final sensor and actuator assignment is:

| EV3 Interface | Component | Current Responsibility |
| :--- | :--- | :--- |
| **Motor A** | Drive Motor | Rear propulsion |
| **Motor B** | Steering Motor | Ackermann steering |
| **S1** | Front Ultrasonic Sensor | Frontal safety |
| **S2** | Right Ultrasonic Sensor | Right-side wall geometry |
| **S3** | Left Ultrasonic Sensor | Left-side wall geometry |
| **S4** | LEGO Color Sensor | Floor-marking detection |
| **USB** | Arduino Nano | Vision-data communication |

The configuration can be represented as:

```text
                         LEGO EV3
                            │
       ┌──────────┬─────────┼─────────┬──────────┐
       ▼          ▼         ▼         ▼          ▼
      S1         S2        S3        S4         USB
       │          │         │         │           │
       ▼          ▼         ▼         ▼           ▼
 Front US     Right US   Left US    Color     Arduino Nano
                                                  ▲
                                                  │
                                              HuskyLens
```

This port map should be used when interpreting all current Piolín documentation.

---

# 1.2 Sensor Responsibility Separation

A central design principle of the current architecture is that each sensor has a **specific responsibility**.

The system does not treat all sensors as interchangeable sources of distance or navigation information.

```text
S1 FRONT ULTRASONIC
        ↓
Frontal safety


S2 RIGHT ULTRASONIC
        ↓
Right-side geometry


S3 LEFT ULTRASONIC
        ↓
Left-side geometry


S4 COLOR SENSOR
        ↓
Floor / course state


HUSKYLENS
        ↓
Obstacle identity
```

This separation simplifies the interpretation of sensor data and reduces the risk that one subsystem is assigned conflicting roles.

---

# 1.3 Main Controller

The LEGO EV3 remains the main controller of Piolín.

Its responsibilities include:

```text
Reading S1–S4

Receiving Nano vision information

Interpreting navigation state

Calculating steering response

Controlling Motor A

Controlling Motor B

Managing safety conditions
```

The Arduino Nano does not replace the EV3.

The HuskyLens does not directly control the motors.

The architecture is therefore:

```text
SENSORS
   ↓
INFORMATION
   ↓
EV3
   ↓
DECISION
   ↓
ACTUATORS
```

This creates a clear boundary between **perception** and **vehicle control**.

---

# 1.4 Current Power Architecture

The EV3 battery system is the primary energy source for the EV3-controlled vehicle subsystem.

Conceptually:

```text
EV3 BATTERY
     ↓
LEGO EV3
     ├── Motor A
     ├── Motor B
     ├── S1
     ├── S2
     ├── S3
     └── S4
```

The EV3 therefore acts as both:

```text
Main controller
```

and:

```text
Central power-distribution point
for the EV3-connected vehicle hardware
```

The exact battery chemistry, nominal voltage, capacity, and measured current consumption are not specified here because those values have not been established as confirmed final specifications in the current project documentation.

For component-level information, see:

[Battery](../components/08_Battery.md)

[Power Distribution](../components/09_PowerDistribution.md)

---

# 1.5 Power and Data Must Be Distinguished

One important documentation rule is to distinguish:

```text
DATA CONNECTION
```

from:

```text
POWER CONNECTION
```

For the current vision system, the confirmed relationship is:

```text
HuskyLens
    ↓
Arduino Nano
    ↓
USB
    ↓
LEGO EV3
```

The Nano-to-EV3 USB connection is confirmed as the vision-data connection.

This document does not infer an unconfirmed HuskyLens-to-Nano electrical protocol or power-routing method.

Therefore:

```text
CONFIRMED
Nano ↔ EV3 via USB
```

while details not explicitly verified should not be presented as final wiring facts.

This distinction improves reproducibility and prevents assumptions from being mixed with confirmed architecture.

---

# 1.6 Sensor Data Categories

Piolín receives several fundamentally different types of information.

| Sensor | Data Category | What It Describes |
| :--- | :--- | :--- |
| **S1 Front US** | Distance | Space directly ahead |
| **S2 Right US** | Distance | Right-side wall geometry |
| **S3 Left US** | Distance | Left-side wall geometry |
| **S4 Color** | Optical / color | Floor marking beneath robot |
| **HuskyLens** | Vision / classification | Obstacle identity |

These data types answer different questions.

```text
ULTRASONIC
"How far?"


COLOR
"What floor event?"


VISION
"What obstacle?"
```

The EV3 combines those answers according to the current navigation state.

---

# 1.7 Physical Sensor Arrangement

The final sensor arrangement can be represented conceptually as:

```text
                         FRONT
                           ↑

                       HuskyLens

                    Front US — S1


          Left US — S3       S2 — Right US
                 ←      [ PIOLÍN ]      →


                         S4
                         │
                         ▼
                  TRACK SURFACE
```

The three ultrasonic sensors observe different spatial regions.

The color sensor observes the track below the vehicle.

The HuskyLens observes the region in front of Piolín.

This physical arrangement creates complementary perception rather than duplicated sensing.

---

# 1.8 Lateral Ultrasonic Geometry

The lateral ultrasonic sensors are:

```text
S2 = RIGHT

S3 = LEFT
```

Their confirmed approximate mounting height is:

```text
43.2 mm above the floor
```

They are oriented laterally rather than being used as front-facing obstacle detectors.

Their primary task is to describe the robot's relationship with the side boundaries of the course.

Conceptually:

```text
LEFT WALL                    RIGHT WALL
    │                            │
    │                            │
    ▼                            ▼
  [S3] ←────── [ PIOLÍN ] ─────→ [S2]
```

Because their interpretation depends on course direction, their physical labels and logical roles must be distinguished.

---

# 1.9 Physical Side vs. Logical Role

The sensor positions never change:

```text
S3 = physically LEFT

S2 = physically RIGHT
```

However, the navigation roles:

```text
INNER

OUTER
```

change according to the selected travel direction.

This creates two different concepts:

```text
PHYSICAL SENSOR
```

and:

```text
LOGICAL SENSOR ROLE
```

The software assigns the logical role after determining the direction of travel.

---

# 1.10 Counterclockwise Configuration

If the first valid direction marker is blue:

```text
BLUE
  ↓
COUNTERCLOCKWISE
```

then:

```text
S3 LEFT
=
INNER SENSOR
```

and:

```text
S2 RIGHT
=
OUTER SENSOR
```

The relationship is:

```text
COUNTERCLOCKWISE

Outer wall                  Inner wall
    │                           │
    ▼                           ▼
   S2       [ PIOLÍN ]         S3
 RIGHT                       LEFT
```

The left side becomes the primary inner-wall navigation reference.

---

# 1.11 Clockwise Configuration

If the first valid direction marker is orange:

```text
ORANGE
   ↓
CLOCKWISE
```

then:

```text
S2 RIGHT
=
INNER SENSOR
```

and:

```text
S3 LEFT
=
OUTER SENSOR
```

Conceptually:

```text
CLOCKWISE

Inner wall                  Outer wall
    │                           │
    ▼                           ▼
   S2       [ PIOLÍN ]         S3
 RIGHT                       LEFT
```

The same physical sensor hardware therefore supports both course directions.

---

# 1.12 Why Dynamic Assignment Is Useful

Without dynamic assignment, the code would need separate navigation logic for:

```text
Left-wall following
```

and:

```text
Right-wall following
```

Instead, the software can conceptually define:

```text
D_INNER
```

and:

```text
D_OUTER
```

then map the physical sensors once the course direction is known.

For example:

```text
if direction == COUNTERCLOCKWISE:

    D_INNER = LEFT_US
    D_OUTER = RIGHT_US
```

and:

```text
if direction == CLOCKWISE:

    D_INNER = RIGHT_US
    D_OUTER = LEFT_US
```

This simplifies the navigation architecture.

---

# 1.13 Front Ultrasonic Sensor

S1 is dedicated to the forward direction.

Its purpose is fundamentally different from S2 and S3.

```text
S1
 ↓
Forward distance
 ↓
Frontal safety
```

The front ultrasonic sensor does **not** participate in the normal:

```text
D_INNER

D_OUTER
```

wall-following geometry.

This keeps frontal collision protection independent from the side-wall navigation model.

---

# 1.14 Why S1 Is Kept Separate

Suppose the lateral system reports:

```text
Good wall position
```

while the front sensor reports:

```text
Very limited forward clearance
```

The lateral measurements alone would not describe the frontal risk.

Therefore:

```text
SIDE GEOMETRY
      ≠
FRONT GEOMETRY
```

The dedicated S1 sensor provides a second spatial dimension to the safety architecture.

Conceptually:

```text
Normal wall controller
        ↓
Continue forward
```

but:

```text
Front safety condition
        ↓
Can override normal movement
```

The exact software threshold belongs to current calibration and code, not to this architecture overview.

---

# 1.15 Three-Ultrasonic Spatial Model

The current ultrasonic configuration gives Piolín three principal ranging directions:

```text
LEFT
  ↓
S3


FRONT
  ↓
S1


RIGHT
  ↓
S2
```

Conceptually:

```text
                S1
                ↑
                │

       S3 ← [ PIOLÍN ] → S2
```

This does **not** provide complete 360-degree ranging.

Instead, it provides three deliberately selected directions corresponding to the most useful track boundaries for the current navigation strategy.

---

# 1.16 Ultrasonic Distance Interpretation

The ultrasonic sensors provide distance information based on acoustic time of flight.

The general physical principle is:

```text
Sensor emits sound
        ↓
Sound reaches surface
        ↓
Echo returns
        ↓
Travel time is measured
```

The basic physical relationship is:

```text
d =
(v × t) / 2
```

where:

```text
d
=
Distance


v
=
Speed of sound


t
=
Round-trip travel time
```

The division by two is required because the acoustic pulse travels to the surface and back.

In Piolín, the LEGO sensor interface provides usable distance information to the EV3, so the navigation software does not need to manually calculate the acoustic timing.

---

# 1.17 Distance Does Not Equal Robot Position

An ultrasonic sensor reports distance from the **sensor**, not automatically from the center of the vehicle.

Therefore:

```text
SENSOR DISTANCE
        ≠
CENTERLINE DISTANCE
```

unless the sensor offset is also known and included.

Similarly:

```text
Side distance changes
```

does not uniquely prove that Piolín translated sideways.

The reading can also change because:

```text
Robot rotated

Wall ended

Wall geometry changed

Sensor orientation changed
```

This is why ultrasonic data must be interpreted together with navigation state.

---

# 1.18 Normal Straight-Wall State

During a normal straight section, the inner wall is the principal geometric reference.

The information flow is:

```text
INNER ULTRASONIC
        ↓
Distance measurement
        ↓
Compare with navigation reference
        ↓
Steering correction
        ↓
Robot trajectory changes
        ↓
New distance measurement
```

This creates a closed feedback loop.

The outer ultrasonic sensor remains available as additional geometric information and safety context.

Detailed wall-following logic is documented in:

[Wall Following](../software_obstacles_strategy/03_wallfollowing.md)

---

# 1.19 Corner Sensor Transition

At a corner, the sensor geometry changes significantly.

The current strategy relies on this transition.

```text
NORMAL STRAIGHT
      ↓
Inner wall visible
      ↓
Approach corner
      ↓
Inner wall ends
      ↓
Inner reading increases / changes
      ↓
Corner state
```

As Piolín turns:

```text
Outer geometry becomes useful
```

and later:

```text
Inner wall reappears
```

which helps identify corner exit.

This is a major reason the lateral sensors are documented as a **geometry pair** rather than two independent obstacle detectors.

---

# 1.20 Corner Geometry Without a Gyroscope

The current Piolín architecture does not use a gyroscope.

Corner navigation instead derives information from:

```text
Inner wall disappearance

Outer wall geometry

Inner wall reacquisition

Vehicle motion
```

The transition is:

```text
INNER PRESENT
     ↓
INNER LOST
     ↓
TURN
     ↓
OUTER REFERENCE
     ↓
INNER REACQUIRED
     ↓
EXIT
```

This allows the navigation system to remain referenced to the physical track.

The previous gyro-based architecture is preserved in:

[Legacy Gyroscope Configuration](../legacy/01_GConfig.md)

---

# 1.21 Color Sensor Configuration

The color sensor occupies:

```text
S4
```

and is mounted downward toward the track surface.

Its main responsibilities are:

```text
Determine initial travel direction

Detect valid floor-marking events

Track course progression
```

It does not directly control the steering motor.

The information path is:

```text
Floor marking
     ↓
Color sensor
     ↓
EV3
     ↓
Course-state update
     ↓
Navigation interpretation
```

Current component documentation:

[Color Sensor](../components/06_ColorSensor.md)

---

# 1.22 Direction Detection

At the beginning of the run, the color system identifies the initial direction.

The current interpretation is:

```text
BLUE FIRST
    ↓
COUNTERCLOCKWISE
```

and:

```text
ORANGE FIRST
     ↓
CLOCKWISE
```

This decision affects the meaning of the lateral sensors.

Therefore:

```text
COLOR EVENT
     ↓
TRAVEL DIRECTION
     ↓
INNER / OUTER SENSOR ASSIGNMENT
```

The color sensor indirectly changes wall-navigation behavior by defining the course orientation.

---

# 1.23 Course Progress Tracking

The track contains repeated colored floor markings.

Piolín uses valid color events to help determine course progression across the three-lap run.

The conceptual relationship is:

```text
Vehicle moves
      ↓
Color sensor crosses marking
      ↓
Valid event confirmed
      ↓
Progress counter changes
```

Because the sensor can remain physically over the same colored region for several sampling cycles, the software must distinguish:

```text
ONE PHYSICAL MARKING
```

from:

```text
MANY SENSOR READINGS
```

This motivates event-locking and cooldown logic.

Detailed implementation belongs to:

[RGB Detection](../software_obstacles_strategy/09_RGBdetection.md)

and:

[Software Architecture](../software_obstacles_strategy/01_SWArchitecture.md)

---

# 1.24 Color Detection and Physical Mounting

The reliability of the color sensor depends partly on its mechanical configuration.

The current sensor is:

```text
Downward-facing
```

and uses a casing intended to reduce unwanted surrounding light reaching the observed floor region.

Conceptually:

```text
AMBIENT LIGHT
    \       /
     \     /
      [CASING]
         │
    COLOR SENSOR
         │
         ▼
       FLOOR
```

This demonstrates an important systems principle:

```text
MECHANICAL DESIGN
      can improve
SENSOR QUALITY
```

without changing the electronics.

The corresponding 3D model is available at:

[Color Sensor Casing](../../models/3dprint/ColorSensorCasing.stl)

---

# 1.25 Vision Subsystem Configuration

The current obstacle-vision architecture uses:

```text
HuskyLens
     ↓
Arduino Nano
     ↓
USB
     ↓
LEGO EV3
```

The vision subsystem is mainly required during the Obstacle Challenge.

Its role is different from the ultrasonic system.

```text
ULTRASONIC
      ↓
Distance / geometry


HUSKYLENS
      ↓
Obstacle identity
```

This separation allows the robot to know both:

```text
What is ahead?
```

and:

```text
Where are the walls?
```

---

# 1.26 Current Obstacle Identification

The current HuskyLens configuration uses:

```text
ID 1 = GREEN PILLAR

ID 2 = RED PILLAR
```

The required passing behavior is:

```text
GREEN
   ↓
Pass on LEFT
```

and:

```text
RED
  ↓
Pass on RIGHT
```

The HuskyLens does not directly move the robot.

Instead:

```text
Obstacle
   ↓
HuskyLens
   ↓
Classification
   ↓
Arduino Nano
   ↓
EV3
   ↓
Vehicle response
```

Detailed vision documentation:

[HuskyLens](../components/07_HuskyLens.md)

[HuskyLens Vision](../software_obstacles_strategy/08_CameraHLVision.md)

---

# 1.27 Open Challenge Sensor Configuration

During the Open Challenge, the core navigation architecture does not require the vision subsystem for wall navigation.

The principal sensor flow is:

```text
S1 FRONT US
      ↓
Frontal safety


S2 + S3
      ↓
Wall navigation


S4
      ↓
Direction + course progress
```

Conceptually:

```text
               OPEN CHALLENGE

                    LEGO EV3
                       ▲
          ┌────────────┼────────────┐
          │            │            │
         S1          S2/S3          S4
          │            │            │
          ▼            ▼            ▼
       FRONT        WALLS         FLOOR
       SAFETY      NAVIGATION      STATE
```

This provides a relatively compact sensing architecture for the Open round.

---

# 1.28 Obstacle Challenge Sensor Configuration

The Obstacle Challenge adds obstacle identity to the same base system.

```text
                OBSTACLE CHALLENGE

                      LEGO EV3
                         ▲
       ┌──────────┬──────┼──────┬───────────┐
       │          │             │           │
      S1        S2/S3           S4         USB
       │          │             │           │
       ▼          ▼             ▼           ▼
    FRONT       WALLS          FLOOR       NANO
    SAFETY     NAVIGATION      STATE        ▲
                                            │
                                        HUSKYLENS
```

The base wall-navigation architecture therefore remains available while the vision system contributes obstacle information.

This modularity is important because obstacle perception should not replace track-boundary sensing.

---

# 1.29 Sensor Fusion

Piolín's navigation does not treat one sensor as a universal solution.

Instead, the system combines specialized measurements.

For example, during obstacle avoidance:

```text
HuskyLens
     ↓
Required passing side
```

while:

```text
Lateral US
     ↓
Available wall clearance
```

and:

```text
Front US
     ↓
Frontal safety
```

The EV3 combines these constraints.

Conceptually:

```text
OBSTACLE IDENTITY
       +
WALL GEOMETRY
       +
FRONT SAFETY
       +
COURSE STATE
       ↓
FINAL NAVIGATION DECISION
```

This is the central sensor-fusion principle of Piolín.

---

# 1.30 Sensor Priority Concept

Different sensors may simultaneously suggest different movement priorities.

A useful system hierarchy is:

```text
FRONTAL COLLISION SAFETY
          ↓
LATERAL WALL SAFETY
          ↓
OBSTACLE / CORNER LOGIC
          ↓
NORMAL WALL FOLLOWING
```

This hierarchy does not mean each sensor directly overrides the motors independently.

Instead, it represents the relative importance of different navigation constraints when the EV3 calculates the final action.

The result should always be:

```text
Many sensor inputs
        ↓
One coherent vehicle command
```

---

# 1.31 Why Sensor Roles Should Not Conflict

Suppose the camera determines:

```text
Move left to pass obstacle
```

while the left ultrasonic indicates:

```text
Wall clearance is becoming small
```

If the camera were allowed to control steering independently:

```text
Correct obstacle behavior
        ↓
Possible wall collision
```

The better architecture is:

```text
Vision request
       +
Wall constraint
       ↓
EV3 arbitration
       ↓
Constrained steering command
```

This illustrates why centralized decision-making is important.

---

# 1.32 Sensor Sampling and Vehicle Motion

Sensor data is only meaningful in relation to time and movement.

Between two readings:

```text
Piolín may have moved

Piolín may have rotated

Wall geometry may have changed
```

At greater vehicle speed, the robot travels farther between sensor updates.

Therefore:

```text
SENSOR UPDATE RATE
        +
VEHICLE SPEED
        ↓
PHYSICAL RESPONSE DISTANCE
```

This is why drivetrain speed affects sensing performance even though the sensors themselves do not control propulsion.

---

# 1.33 Sensor Noise and Filtering

Real sensor data can contain variation.

A navigation system should therefore avoid assuming that every single reading is a perfect representation of the environment.

For ultrasonic sensing, a short median-based filter can conceptually operate as:

```text
Reading 1
Reading 2
Reading 3
     ↓
MEDIAN
     ↓
Navigation value
```

For example:

```text
245 mm
247 mm
690 mm
```

has a median of:

```text
247 mm
```

which is less influenced by the isolated extreme reading than an immediate single-sample reaction.

Detailed filtering behavior should be documented in:

[Ultrasonic Sensor Data](02_USSensorD.md)

rather than duplicated fully here.

---

# 1.34 Sensor Validation vs. Sensor Calibration

Two concepts should be distinguished.

### Validation

```text
Does the sensor behave reliably
enough for the intended role?
```

### Calibration

```text
Which measured values should the
software use for this robot?
```

For example:

```text
Ultrasonic validation
        ↓
Check distance behavior
```

while:

```text
Wall calibration
        ↓
Determine useful navigation references
```

Detailed calibration procedures belong in:

[Sensor Calibration](05_Calibration.md)

and:

[How to Calibrate](../reproducibility/06_HowToCalibrate.md)

---

# 1.35 Sensor Geometry and Mechanical Stability

Sensor behavior depends on mechanical mounting.

For example:

```text
Ultrasonic mount rotates
        ↓
Observed surface changes
        ↓
Distance changes
```

even if the vehicle center remains nearly unchanged.

Similarly:

```text
HuskyLens angle changes
        ↓
Field of view changes
```

and:

```text
Color sensor height changes
        ↓
Observed floor region changes
```

Therefore, the sensor system depends directly on:

[Chassis Design](../mobility_mechanical/02_chassis.md)

Mechanical stability is part of sensing reliability.

---

# 1.36 Sensor Failure Propagation

A sensor-related problem can propagate through the full control system.

Example:

```text
Sensor mount moves
        ↓
Measurement changes
        ↓
EV3 calculates new error
        ↓
Motor B changes steering
        ↓
Vehicle trajectory changes
```

The resulting behavior may look like a steering problem even though the original cause was the sensor geometry.

This is why troubleshooting should consider:

```text
Sensor electronics

Sensor mounting

Software interpretation

Mechanical response
```

together.

---

# 1.37 Power Demand Changes With Robot State

Electrical demand is not constant throughout a run.

Different operating states can place different loads on the EV3-controlled system.

For example:

```text
Straight movement
```

may involve moderate drive and steering activity.

A corner can require:

```text
Drive motor
+
Larger steering movement
```

while an obstacle maneuver can require:

```text
Drive changes
+
Steering reversals
+
Sensor processing
+
Vision communication
```

Therefore:

```text
ROBOT STATE
      ↓
Changes electrical demand
```

No numerical current values are presented here because they have not been measured as confirmed final data.

---

# 1.38 Power Stability and Sensor Reliability

Power stability matters because the control system relies on continuous operation of:

```text
EV3

Motors

Ultrasonic sensors

Color sensor
```

and communication with the supporting vision subsystem.

A power interruption can appear as:

```text
Sensor unavailable

Controller reset

Motor response loss

Communication interruption
```

For this reason, electrical reliability is treated as part of overall autonomous reliability rather than as a separate issue.

Detailed electrical architecture:

[Power Distribution](../components/09_PowerDistribution.md)

[Electrical Schematic](../reproducibility/04_elecschem.md)

---

# 1.39 Wiring as Part of Sensor Configuration

Sensor assignment includes both:

```text
Logical port
```

and:

```text
Physical connection
```

The final EV3 sensor connections should remain:

```text
S1 → Front Ultrasonic

S2 → Right Ultrasonic

S3 → Left Ultrasonic

S4 → Color Sensor
```

Changing physical connections without changing software configuration can cause the EV3 to interpret:

```text
Left as right

Right as front

Front as another sensor
```

depending on the mismatch.

Therefore, port consistency is essential for reproducibility.

Current wiring:

[Wiring](../reproducibility/03_wiring.md)

---

# 1.40 Sensor Configuration Verification

Before interpreting a navigation failure, the current configuration should first be verified conceptually:

```text
Is S1 physically the front ultrasonic?

Is S2 physically the right ultrasonic?

Is S3 physically the left ultrasonic?

Is S4 the downward color sensor?

Is the Nano connected to EV3 through USB?

Are sensor mounts still aligned?
```

This simple verification can prevent debugging software based on an incorrect physical configuration.

---

# 1.41 Current vs. Legacy Sensor Architecture

The final configuration differs significantly from previous Piolín systems.

| Function | Legacy Examples | Current Piolín |
| :--- | :--- | :--- |
| **S1** | Gyroscope / unused | Front Ultrasonic |
| **S2** | Different US arrangements | Right Ultrasonic |
| **S3** | Different US arrangements | Left Ultrasonic |
| **S4** | Color Sensor | Color Sensor |
| **Vision** | PixyCam | HuskyLens |
| **Vision Interface** | Previous concepts | Arduino Nano |
| **Main Controller** | Alternative experiments | LEGO EV3 |
| **Gyroscope** | Used experimentally | Not installed |
| **Frontal ranging** | Previous / absent | Dedicated S1 |

Historical information should not be mixed with the current sensor configuration.

See:

[Legacy Documentation Notice](../legacy/00_LEGACY_NOTICE.md)

---

# 1.42 Sensor Responsibility Matrix

| Information Needed | Sensor / System |
| :--- | :--- |
| **Forward clearance** | S1 Front Ultrasonic |
| **Right wall distance** | S2 Right Ultrasonic |
| **Left wall distance** | S3 Left Ultrasonic |
| **Inner wall distance** | S2 or S3 depending on direction |
| **Outer wall distance** | S2 or S3 depending on direction |
| **Initial course direction** | S4 Color Sensor |
| **Course progress** | S4 Color Sensor |
| **Green pillar identity** | HuskyLens |
| **Red pillar identity** | HuskyLens |
| **Vision communication** | Arduino Nano |
| **Final interpretation** | LEGO EV3 |
| **Propulsion response** | Motor A |
| **Steering response** | Motor B |

This table summarizes the current information architecture.

---

# 1.43 Open Challenge Information Flow

The Open Challenge can be represented as:

```text
                       TRACK
                         │
           ┌─────────────┼─────────────┐
           ▼             ▼             ▼
       SIDE WALLS    FRONT SPACE    FLOOR MARKS
           │             │             │
           ▼             ▼             ▼
        S2 / S3          S1            S4
           │             │             │
           └─────────────┼─────────────┘
                         ▼
                      LEGO EV3
                         │
                         ▼
                  NAVIGATION STATE
                         │
               ┌─────────┴─────────┐
               ▼                   ▼
            Motor A             Motor B
```

The vision system is not required to define ordinary Open-round wall navigation.

---

# 1.44 Obstacle Challenge Information Flow

The Obstacle Challenge adds a fourth perception path:

```text
                         TRACK
                           │
       ┌───────────┬───────┼───────┬────────────┐
       ▼           ▼               ▼            ▼
   SIDE WALLS  FRONT SPACE      FLOOR MARKS   PILLAR
       │           │               │            │
       ▼           ▼               ▼            ▼
    S2 / S3        S1              S4       HuskyLens
       │           │               │            │
       │           │               │        Arduino Nano
       │           │               │            │
       └───────────┴───────┬───────┴────────────┘
                           ▼
                        LEGO EV3
                           │
                           ▼
                  SENSOR FUSION / STATE
                           │
                 ┌─────────┴─────────┐
                 ▼                   ▼
              Motor A             Motor B
```

This structure keeps the EV3 as the central decision-making element even when vision is active.

---

# 1.45 Why the Architecture Is Modular

The sensing system is modular because each subsystem can be understood independently:

```text
WALL MODULE
=
S2 + S3


FRONT SAFETY MODULE
=
S1


COURSE-STATE MODULE
=
S4


VISION MODULE
=
HuskyLens + Nano
```

These modules converge at:

```text
LEGO EV3
```

This provides several engineering advantages:

```text
Clear responsibilities

Simpler debugging

Easier testing

Better documentation

Reduced dependence on one sensor
```

A failure in one sensor category can therefore be investigated without redefining the entire robot architecture.

---

# 1.46 Sensor Redundancy vs. Complementarity

Piolín's sensors are mostly **complementary**, not simple duplicates.

For example:

```text
S1
```

cannot replace:

```text
S2 / S3
```

because forward distance and lateral distance describe different geometry.

Similarly:

```text
HuskyLens
```

cannot replace:

```text
Color Sensor
```

because obstacle identity and floor markings are different information classes.

The architecture therefore gains robustness through **different sensing modalities**, rather than by measuring the same quantity multiple times with identical sensors.

---

# 1.47 Environmental Reference Philosophy

The current architecture intentionally relies on the actual competition environment.

The main navigation references are:

```text
Walls

Floor markings

Pillars
```

The robot extracts information from those physical features using specialized sensors.

This can be summarized as:

```text
PHYSICAL TRACK
      ↓
SENSOR MEASUREMENT
      ↓
ENVIRONMENTAL STATE
      ↓
VEHICLE CONTROL
```

This is different from the legacy gyro concept, which attempted to maintain an independent angular reference.

---

# 1.48 Sensor-to-Action Traceability

Every current sensor has a traceable path to a vehicle behavior.

### Front ultrasonic

```text
Front distance
      ↓
Safety decision
      ↓
Drive / motion response
```

### Lateral ultrasonics

```text
Wall distance
      ↓
Navigation error
      ↓
Steering correction
```

### Color sensor

```text
Floor event
      ↓
Course state
      ↓
Navigation interpretation
```

### HuskyLens

```text
Pillar identity
      ↓
Passing side
      ↓
Obstacle maneuver
```

This traceability is important because it allows each design claim to be connected to software, hardware, and testing evidence.

---

# 1.49 Confirmed Sensor Specifications Used in This Section

The current confirmed configuration is:

| Parameter | Confirmed Value |
| :--- | :--- |
| **Main controller** | LEGO EV3 |
| **S1** | Front Ultrasonic |
| **S2** | Right Ultrasonic |
| **S3** | Left Ultrasonic |
| **S4** | Color Sensor |
| **Vision sensor** | HuskyLens |
| **Vision interface** | Arduino Nano |
| **Nano → EV3** | USB |
| **Lateral US mounting height** | ~43.2 mm |
| **Gyroscope** | Not installed |
| **PixyCam** | Not installed |
| **Raspberry Pi** | Not part of final architecture |

No unconfirmed values are claimed here for:

```text
Front ultrasonic mounting height

Final wall target distances

Front emergency threshold

Battery voltage

Battery capacity

Motor current

Sensor current

Vision-system power consumption

HuskyLens-to-Nano protocol
```

Those values should only be added when confirmed from the current robot or current code.

---

# 1.50 Configuration Summary

Piolín's final WRO Future Engineers 2026 power and sensor architecture is centered around the LEGO EV3.

The sensing system is organized as:

```text
S1
↓
FRONT SAFETY


S2 + S3
↓
LATERAL GEOMETRY


S4
↓
COURSE STATE


HUSKYLENS
↓
OBSTACLE IDENTITY


ARDUINO NANO
↓
VISION COMMUNICATION


LEGO EV3
↓
FINAL DECISION
```

The power and information architecture can therefore be summarized as:

```text
                  EV3 BATTERY
                       ↓
                    LEGO EV3
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
       MOTORS        SENSORS      PROCESSING
       A + B         S1–S4          EV3


                    LEGO EV3
                       ▲
                       │ USB
                       │
                 Arduino Nano
                       ▲
                       │
                   HuskyLens
```

The design deliberately separates:

```text
Power

Sensing

Communication

Decision making

Actuation
```

while connecting them through one centralized vehicle-control architecture.

This allows Piolín to use the physical track as its primary navigation reference:

```text
WALLS
  ↓
Ultrasonics


FLOOR
  ↓
Color Sensor


PILLARS
  ↓
HuskyLens
```

and convert those observations into controlled vehicle movement through the EV3.

The resulting sensor architecture supports both competition modes:

```text
OPEN CHALLENGE
=
3 Ultrasonics
+
Color Sensor
+
EV3
```

and:

```text
OBSTACLE CHALLENGE
=
Open Challenge Base
+
HuskyLens
+
Arduino Nano
```

while maintaining the same core vehicle-control structure.

---

## Continue Reading

[Ultrasonic Sensor Data](02_USSensorD.md)

[Color Sensor Configuration](03_color_sensor.md)

[HuskyLens Vision System](04_huskylens.md)

[Sensor Calibration](05_Calibration.md)

---

## Related Hardware Documentation

[Hardware Overview](../components/01_Hardwareoverview.md)

[Ultrasonic Sensors](../components/05_UltrasonicSensors.md)

[Color Sensor](../components/06_ColorSensor.md)

[HuskyLens](../components/07_HuskyLens.md)

[Battery](../components/08_Battery.md)

[Power Distribution](../components/09_PowerDistribution.md)

---

## Reproducibility

[Wiring](../reproducibility/03_wiring.md)

[Electrical Schematic](../reproducibility/04_elecschem.md)

[Calibration Procedure](../reproducibility/06_HowToCalibrate.md)

[Testing Protocol](../reproducibility/07_TestingProtocol.md)

---

## Navigation

[Wall Following](../software_obstacles_strategy/03_wallfollowing.md)

[Corner Handling](../software_obstacles_strategy/04_cornerhandling.md)

[Obstacle Detection](../software_obstacles_strategy/05_obstacledetec.md)

[Obstacle Strategy](../software_obstacles_strategy/06_obstaclestrateg.md)

[HuskyLens Vision](../software_obstacles_strategy/08_CameraHLVision.md)

[RGB Detection](../software_obstacles_strategy/09_RGBdetection.md)
