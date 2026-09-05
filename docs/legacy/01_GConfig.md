# 1. Legacy Gyroscope Navigation Configuration

> [!WARNING]
> **This document describes a previous Piolín navigation architecture.**
>
> The gyroscope described in this file is **not part of the current WRO Future Engineers 2026 robot configuration**.
>
> In the current Piolín architecture:
>
> ```text
> S1 → Front Ultrasonic Sensor
> S2 → Right Ultrasonic Sensor
> S3 → Left Ultrasonic Sensor
> S4 → Color Sensor
> ```
>
> Current hardware documentation:
>
> [Ultrasonic Sensors](../components/05_UltrasonicSensors.md)  
> [Hardware Overview](../components/01_Hardwareoverview.md)  
> [Legacy Documentation Notice](00_LEGACY_NOTICE.md)

---

## 1.1 Purpose of This Document

During an earlier stage of Piolín's development, a **LEGO gyroscope** was integrated into the navigation system to provide heading information independently from the track walls.

At that stage, Piolín's navigation concept combined two different types of environmental reference:

```text
ULTRASONIC SENSORS
        ↓
Relative position to walls


GYROSCOPE
        ↓
Relative chassis heading
```

The objective was to create a **hybrid navigation framework** in which wall measurements could guide normal track following while the gyroscope could maintain or recover a desired vehicle orientation when wall information became less reliable.

This configuration was useful as an engineering experiment because it introduced a second navigation reference that did not depend directly on the presence of a nearby wall.

The system was later replaced as Piolín's final sensor architecture evolved.

---

# 1.2 Historical Sensor Configuration

In this legacy configuration, the gyroscope occupied **EV3 Sensor Port S1**.

A simplified historical arrangement was:

| EV3 Port | Legacy Component | Historical Role |
| :--- | :--- | :--- |
| **S1** | Gyroscope | Heading reference |
| **S2** | Right Ultrasonic Sensor | Wall measurement |
| **S3** | Left Ultrasonic Sensor | Wall measurement |
| **S4** | Color Sensor | Floor-marking detection |

The architecture therefore looked approximately like this:

```text
                         LEGO EV3
                            │
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
            S1             S2             S3
             │              │              │
             ▼              ▼              ▼
           GYRO          RIGHT US       LEFT US

                            │
                            ▼
                           S4
                            │
                            ▼
                     COLOR SENSOR
```

This is no longer Piolín's current configuration.

The current S1 port is now used by the **front ultrasonic sensor**.

---

# 1.3 Why the Gyroscope Was Introduced

The ultrasonic sensors provided useful information about Piolín's position relative to nearby walls.

However, wall measurements alone do not directly describe the robot's heading.

For example, a side ultrasonic sensor may report a changing distance because:

```text
The robot moved sideways

or

The robot rotated

or

The wall geometry changed
```

During sections where a wall ended, became difficult to observe, or where the robot changed trajectory significantly, the ultrasonic readings could temporarily become harder to interpret.

The gyroscope was introduced to provide another reference:

```text
Walls available
      ↓
Ultrasonic navigation useful


Walls temporarily unreliable
      ↓
Gyroscope heading reference useful
```

The intended concept was not to replace ultrasonic navigation completely.

Instead, the two systems were meant to complement each other.

---

# 1.4 Hybrid Navigation Concept

The historical navigation architecture divided responsibilities between wall-based sensing and heading-based sensing.

```text
                     NAVIGATION
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
      ULTRASONIC SYSTEM         GYROSCOPE
             │                       │
             ▼                       ▼
       Wall Geometry           Heading Error
             │                       │
             └───────────┬───────────┘
                         ▼
                      LEGO EV3
                         │
                         ▼
                  Steering Command
```

The ultrasonic system answered:

> **Where is Piolín relative to the surrounding walls?**

The gyroscope answered:

> **How far has Piolín rotated relative to its stored heading reference?**

The EV3 could then decide which source of information was more useful for the current navigation state.

---

# 1.5 Gyroscope Measurement Principle

The gyroscope measures rotational motion of the robot.

In Piolín's mounting orientation, the relevant motion was rotation around the approximately vertical axis of the chassis.

Conceptually:

```text
             TOP VIEW

                 ↑
              Forward

          ┌─────────────┐
          │             │
          │   PIOLÍN    │
          │             │
          └─────────────┘

             ↺       ↻
          Rotation around
          vertical axis
```

The sensor provides angular information that can be used by the EV3 as a heading reference.

If the robot begins at:

```text
0°
```

and rotates approximately 90 degrees, the sensor reading can be used to identify that change in orientation.

The value is relative to the reference established when the gyroscope is reset.

It is therefore better understood as a **relative heading estimate**, not as an absolute global compass heading.

---

# 1.6 Establishing a Zero Reference

Before using the gyroscope for heading control, the software established a known angular reference.

A simplified historical initialization looked like:

```python
GYRO_SENSOR = GyroSensor(Port.S1)

def calibrate_gyro():
    GYRO_SENSOR.reset_angle(0)
    wait(500)
```

The purpose was:

```text
Robot placed in known orientation
        ↓
Gyroscope reset
        ↓
Current heading defined as 0°
        ↓
Future rotation measured
relative to that reference
```

The robot needed to remain physically stable while the reference was established.

This gave the program a consistent starting point for later heading calculations.

---

# 1.7 Gyroscope Drift

One limitation identified with gyroscope-based navigation was **drift**.

A gyroscope can gradually accumulate heading error even when the physical orientation of the robot has changed very little.

Conceptually:

```text
Physical robot heading
        ↓
Approximately constant


Gyroscope estimate
        ↓
Slowly changes over time
```

Possible contributors include sensor noise, vibration, initialization conditions, and accumulated integration error.

This means the gyroscope reading could not be treated as a perfect representation of physical orientation indefinitely.

The historical architecture therefore depended on resetting or referencing the gyro from a known state when appropriate.

This limitation was one of the practical considerations associated with gyro-based navigation.

---

# 1.8 Heading Error

The basic steering concept used a target heading and compared it with the current gyroscope reading.

The heading error was:

```text
HEADING_ERROR =
TARGET_HEADING - CURRENT_HEADING
```

For example:

```text
TARGET_HEADING  = 0°

CURRENT_HEADING = -5°

HEADING_ERROR   = 5°
```

The sign and magnitude of the error indicated how far the robot had rotated away from the desired orientation.

This value could then be converted into a steering correction.

---

# 1.9 Proportional Heading Control

The historical control concept used a proportional relationship:

```text
STEERING_CORRECTION =
HEADING_ERROR × Kp
```

where:

```text
Kp = proportional gain
```

A simplified historical implementation was:

```python
def maintain_absolute_heading(target_heading, Kp_gyro=0.8):
    current_heading = GYRO_SENSOR.angle()

    heading_error = target_heading - current_heading

    steering_command = heading_error * Kp_gyro

    set_steering(steering_command)
    MOTOR_DRIVE.run(SPEED_FAST)
```

> [!NOTE]
> The code in this document is preserved as a **legacy implementation example**.
>
> Constants such as `Kp_gyro = 0.8` belong to this previous development stage and should not be interpreted as values for the current Piolín robot.

The controller behaved conceptually as follows:

```text
Small heading error
        ↓
Small steering correction


Large heading error
        ↓
Larger steering correction
```

As Piolín approached the desired heading, the proportional error decreased and the steering correction also became smaller.

---

# 1.10 Historical Heading-Control Diagram

<div align="center">
  <img
    width="500"
    height="300"
    alt="Legacy Piolín gyroscope navigation concept"
    src="https://github.com/user-attachments/assets/9f7be4f1-9829-4199-83e8-58336f3ecd26"
  />
  <br>
  <sub><b>Figure 1.1.</b> Historical gyroscope-based heading-control concept used during Piolín's development.</sub>
</div>

The image above belongs to the legacy navigation architecture documented in this file.

It should not be interpreted as the current sensor configuration.

---

# 1.11 Example Heading Correction

Suppose Piolín's target heading was:

```text
TARGET = 0°
```

and the gyro reported:

```text
CURRENT = -10°
```

Then:

```text
ERROR = 0 - (-10)
```

```text
ERROR = 10°
```

Using the historical proportional gain:

```text
Kp = 0.8
```

the resulting proportional command would be:

```text
STEERING_COMMAND = 10 × 0.8
```

```text
STEERING_COMMAND = 8
```

This did **not** necessarily mean that the physical front wheels moved exactly eight degrees.

As explained in the steering documentation, Piolín's steering motor encoder command and the physical front-wheel steering angle are not identical.

The value represented a control command passed to the steering system.

---

# 1.12 Why Proportional Control Was Preferred Over Simple Binary Correction

A simple heading controller could use only two states:

```text
Heading too far left
        ↓
Steer right strongly


Heading too far right
        ↓
Steer left strongly
```

This is effectively a binary or bang-bang approach.

The proportional concept instead allowed the steering command to depend on the size of the error.

```text
Large error
    ↓
Strong correction


Medium error
    ↓
Medium correction


Small error
    ↓
Small correction
```

This was intended to reduce abrupt changes as the chassis approached the desired orientation.

However, the physical response still depended on:

```text
Vehicle speed

Steering geometry

Mechanical play

Tire friction

Motor response

Robot inertia
```

The proportional controller therefore improved the control structure but did not eliminate physical overshoot automatically.

---

# 1.13 Gyroscope-Based Turns

The gyroscope was also explored as a reference for corner execution.

Instead of turning for a fixed amount of time, the robot could continue turning until a target angular change had been reached.

The concept was:

```text
Current Heading
      ↓
Define Target Heading
      ↓
Apply Steering
      ↓
Read Gyroscope
      ↓
Target Reached?
   ┌─────┴─────┐
   │           │
  NO          YES
   │           │
   ▼           ▼
Continue     Reduce /
Turning      Center Steering
```

This provided an angular reference independent of elapsed time.

---

# 1.14 Historical Precision-Turn Example

A simplified historical implementation was:

```python
def execute_precision_turn(target_turn_angle):
    if target_turn_angle > GYRO_SENSOR.angle():
        set_steering(MAX_STEER_ANGLE)
    else:
        set_steering(-MAX_STEER_ANGLE)

    while abs(GYRO_SENSOR.angle() - target_turn_angle) > 2:
        MOTOR_DRIVE.run(SPEED_START)
        wait(10)

    set_steering(0)
```

The program repeatedly compared:

```text
CURRENT GYRO ANGLE
```

with:

```text
TARGET TURN ANGLE
```

and continued driving while the difference remained greater than the historical tolerance.

The value:

```text
2°
```

was part of this previous implementation.

It should not be interpreted as a verified universal stopping tolerance or as a current Piolín parameter.

---

# 1.15 Momentum and Angular Overshoot

One problem with stopping a turn exactly when the gyro reaches a target angle is that the physical vehicle has inertia.

Conceptually:

```text
Gyro reaches target
        ↓
Software changes command
        ↓
Robot still has momentum
        ↓
Physical rotation continues briefly
```

This can create angular overshoot.

For example:

```text
Target = 90°

Software reacts at ≈90°

Physical robot continues rotating

Final orientation > 90°
```

The exact amount depends on the physical system and operating conditions.

The historical code used a tolerance around the target angle as one way of reducing unnecessary correction around the final heading.

This was an engineering approximation rather than a guarantee of exact final orientation.

---

# 1.16 Steering and Gyroscope Integration

The gyroscope did not directly move Piolín.

Its information passed through the EV3 control software before reaching the steering motor.

```text
GYROSCOPE
    ↓
Heading Measurement
    ↓
LEGO EV3
    ↓
Heading Error
    ↓
Steering Calculation
    ↓
Motor B
    ↓
Ackermann Linkage
    ↓
Front Wheels
```

This maintained the same basic separation used elsewhere in Piolín:

```text
Sensor
   ↓
Information


EV3
   ↓
Decision


Motor
   ↓
Actuation
```

The gyroscope therefore acted as a perception/reference device, not as a direct steering controller.

---

# 1.17 Gyroscope and Ultrasonic Sensor Fusion

The main objective of the historical framework was to combine heading information with wall measurements.

The architecture could be represented as:

```text
                   ENVIRONMENT
                       │
            ┌──────────┴──────────┐
            ▼                     ▼
          WALLS               ROTATION
            │                     │
            ▼                     ▼
      ULTRASONICS             GYROSCOPE
            │                     │
            └──────────┬──────────┘
                       ▼
                    LEGO EV3
                       │
                Navigation State
                       │
                       ▼
                 Steering System
```

During wall-following sections, ultrasonic measurements could provide the primary navigation reference.

During temporary geometry changes, the gyro could provide additional heading information.

This was the reason the architecture was described as **hybrid navigation**.

---

# 1.18 Navigation Through Temporary Wall Loss

One situation investigated during development was temporary loss of a useful lateral wall reference.

For example:

```text
Normal straight
      ↓
Lateral wall visible
      ↓
Ultrasonic reference available
```

followed by:

```text
Wall ends / geometry opens
      ↓
Ultrasonic distance increases
      ↓
Wall reference becomes less useful
```

The gyro concept attempted to maintain a previously established heading during this transition.

```text
Wall reference disappears
         ↓
Maintain target heading
         ↓
Continue movement
         ↓
Wall reference returns
         ↓
Resume wall-based control
```

This was one of the main motivations for experimenting with the sensor.

---

# 1.19 Gyroscope During Obstacle Avoidance

The gyroscope was also considered useful during obstacle avoidance because an obstacle maneuver could intentionally move Piolín away from the wall-following path.

A conceptual sequence was:

```text
Normal Wall Following
        ↓
Obstacle Detected
        ↓
Avoidance Maneuver
        ↓
Wall Reference Changes
        ↓
Gyro Heading Used as Additional Reference
        ↓
Recovery
        ↓
Wall Following Restored
```

The intention was to prevent a temporary obstacle maneuver from permanently changing the robot's reference heading.

This remained part of the historical architecture rather than the final Piolín obstacle solution.

---

# 1.20 Encoder and Gyroscope Combination

The historical navigation concept also explored combining drivetrain encoder information with gyro heading.

These sensors describe different quantities:

```text
ENCODER
   ↓
Motor / wheel rotation reference


GYROSCOPE
   ↓
Angular orientation reference
```

Together they could conceptually support motion such as:

```text
Travel for a defined encoder interval
            +
Maintain a gyro heading
```

A legacy concept described maintaining gyro-based heading while driving for a defined amount of drivetrain rotation.

The exact encoder values used in these experiments belong to the previous software configuration and are not current Piolín parameters.

---

# 1.21 Limitations of the Gyroscope Architecture

Although the gyroscope provided useful additional heading information, the system also introduced new dependencies.

Important limitations included:

| Limitation | Effect |
| :--- | :--- |
| **Gyroscope drift** | Heading estimate could gradually change |
| **Initialization sensitivity** | Incorrect zero reference affected later headings |
| **Vibration sensitivity** | Mechanical movement could affect measurement stability |
| **Additional sensor dependency** | Navigation relied on another sensor state |
| **S1 occupation** | One EV3 sensor port was unavailable for another sensor |
| **Heading does not equal position** | Correct heading does not guarantee correct lateral placement |
| **Physical inertia** | Robot could overshoot target orientation |
| **Mechanical steering response** | Gyro command still depended on physical steering behavior |

The most important conceptual limitation was:

> **Knowing Piolín's heading does not automatically tell the robot where it is inside the track.**

For example, Piolín could be perfectly parallel to a wall while still being too close to it.

Therefore:

```text
GYRO
   ↓
Heading information
```

was not a replacement for:

```text
ULTRASONIC
   ↓
Wall-distance information
```

The system still required multiple sensing references.

---

# 1.22 Why the Gyroscope Was Removed From the Final Architecture

As Piolín evolved, the sensor architecture changed.

The final system required three ultrasonic sensing directions:

```text
FRONT

LEFT

RIGHT
```

The EV3's four sensor ports were ultimately assigned as:

```text
S1 → Front Ultrasonic

S2 → Right Ultrasonic

S3 → Left Ultrasonic

S4 → Color Sensor
```

This gave Piolín:

```text
Two lateral wall references
        +
Dedicated frontal safety
        +
Floor course-state detection
```

The final navigation concept therefore prioritized environmental geometry and frontal safety over maintaining a separate gyro heading reference.

The resulting transition was:

```text
LEGACY

S1 → Gyroscope
S2 → Right US
S3 → Left US
S4 → Color


            ↓


CURRENT

S1 → Front US
S2 → Right US
S3 → Left US
S4 → Color
```

The removal of the gyro was therefore part of a broader system-level redesign rather than simply the removal of one sensor.

---

# 1.23 Legacy vs. Current Navigation Philosophy

The historical gyro architecture emphasized:

```text
Wall Geometry
      +
Heading Reference
```

The current architecture emphasizes:

```text
Lateral Wall Geometry
        +
Frontal Safety
        +
Course-State Information
        +
Vision During Obstacle Challenge
```

A simplified comparison is:

| Navigation Function | Legacy Gyro Architecture | Current Architecture |
| :--- | :--- | :--- |
| **Heading reference** | Gyroscope | Derived from environmental/navigation behavior |
| **Left wall** | Ultrasonic | S3 Ultrasonic |
| **Right wall** | Ultrasonic | S2 Ultrasonic |
| **Front safety** | No dedicated final S1 US in this configuration | S1 Ultrasonic |
| **Floor markings** | Color Sensor | S4 Color Sensor |
| **Obstacle identity** | Different development configurations | HuskyLens + Nano |
| **Main controller** | EV3 | EV3 |

The two architectures should not be combined when reconstructing the robot.

---

# 1.24 Current Navigation Replacement

The current Piolín Open Challenge does not require gyro heading control.

Instead, the navigation sequence uses the geometry observed by the lateral ultrasonic sensors.

Conceptually:

```text
Determine Direction
        ↓
Assign Inner Wall
        ↓
Follow Inner Wall
        ↓
Inner Wall Disappears
        ↓
Corner Transition
        ↓
Outer Wall Becomes Temporary Reference
        ↓
Inner Wall Reappears
        ↓
Corner Exit
        ↓
Return to Inner-Wall Navigation
```

The front ultrasonic sensor remains separate:

```text
S1 FRONT US
      ↓
Frontal Safety
```

This architecture is documented in the current files rather than this legacy section.

[Current Ultrasonic Sensors](../components/05_UltrasonicSensors.md)  
[Current Color Sensor](../components/06_ColorSensor.md)  
[Current Hardware Overview](../components/01_Hardwareoverview.md)

---

# 1.25 Engineering Value of the Gyroscope Experiment

Although the gyroscope was removed from the final robot, the experiment contributed useful engineering knowledge.

It demonstrated the difference between:

```text
HEADING
```

and:

```text
POSITION
```

It also demonstrated that adding another sensor does not automatically make navigation more reliable.

Every additional sensor introduces:

```text
New data
     +
New calibration dependency
     +
New software logic
     +
New failure modes
     +
New integration requirements
```

The gyro experiment helped PiolínTech evaluate whether heading information justified those additional dependencies within the complete WRO architecture.

The final design decision was to allocate S1 to frontal ultrasonic sensing instead.

---

# 1.26 Why This File Is Preserved

This file remains in `docs/legacy/` because it provides evidence of Piolín's navigation evolution.

The historical progression can be summarized as:

```text
Two lateral ultrasonic references
        +
Gyroscope heading reference
        ↓
Hybrid navigation experiments
        ↓
Evaluation of heading control
        ↓
Sensor architecture reconsidered
        ↓
Gyroscope removed
        ↓
S1 assigned to front ultrasonic
        ↓
Three-ultrasonic final architecture
```

Removing this document would hide an important part of the reasoning that led to the current sensor configuration.

---

# 1.27 Do Not Use This Configuration for the Current Robot

The following configuration is **legacy**:

```text
S1 → Gyroscope
```

Do not combine it with current Piolín documentation.

The current configuration is:

```text
A  → Drive Motor

B  → Steering Motor


S1 → Front Ultrasonic

S2 → Right Ultrasonic

S3 → Left Ultrasonic

S4 → Color Sensor


USB → Arduino Nano
           ↓
       HuskyLens
```

For reconstruction of the final robot, use:

[Current Hardware](../components/)  
[Current Wiring](../reproducibility/03_wiring.md)  
[Current Electrical Schematic](../reproducibility/04_elecschem.md)

---

# 1.28 Final Legacy Summary

The gyroscope was an important experimental component during Piolín's development.

Its historical role was to provide a relative heading reference that could complement ultrasonic wall measurements.

The architecture was based on:

```text
GYROSCOPE
     ↓
Heading Measurement
     ↓
Heading Error
     ↓
Proportional Correction
     ↓
Motor B
     ↓
Ackermann Steering
```

It was also explored for:

```text
Straight heading maintenance

Angular corner control

Temporary wall-loss navigation

Obstacle recovery

Encoder + heading motion
```

However, the gyro introduced additional dependencies such as drift, initialization requirements, and occupation of EV3 Sensor Port S1.

As Piolín's final sensing architecture evolved, S1 was reassigned to a **forward-facing ultrasonic sensor**, providing a dedicated frontal safety measurement while the two lateral ultrasonic sensors continued handling wall geometry.

The final progression is therefore:

```text
LEGACY SYSTEM

Gyroscope + 2 Lateral Ultrasonics + Color
                     ↓
            Engineering Evaluation
                     ↓
          Sensor Architecture Changed
                     ↓

CURRENT SYSTEM

Front Ultrasonic
        +
Left Ultrasonic
        +
Right Ultrasonic
        +
Color Sensor
        +
HuskyLens / Arduino Nano
```

The gyroscope documentation is preserved because it demonstrates a real stage in Piolín's engineering process.

It should be interpreted as:

> **A historical navigation experiment that contributed to the final architecture, not as a component of the current robot.**

Return to:

[Legacy Documentation Notice](00_LEGACY_NOTICE.md)

Current configuration:

[Hardware Overview](../components/01_Hardwareoverview.md)  
[Ultrasonic Sensors](../components/05_UltrasonicSensors.md)  
[Color Sensor](../components/06_ColorSensor.md)  
[HuskyLens](../components/07_HuskyLens.md)
