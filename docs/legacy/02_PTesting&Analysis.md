# 3. Legacy Performance Testing and Analysis

> [!WARNING]
> **This document contains historical testing records from previous Piolín prototypes and experimental architectures.**
>
> The hardware, software, measurements, and numerical results preserved here do **not** represent the current WRO Future Engineers 2026 Piolín configuration unless the same information is explicitly confirmed in current documentation.
>
> Previous experiments referenced in this file include combinations of:
>
> ```text
> PixyCam
> HuskyLens development
> Alternative ultrasonic arrangements
> Raspberry Pi experiments
> Arduino-based prototypes
> Previous steering-control concepts
> ```
>
> Current configuration:
>
> [Hardware Overview](../components/01_Hardwareoverview.md)  
> [HuskyLens](../components/07_HuskyLens.md)  
> [Ultrasonic Sensors](../components/05_UltrasonicSensors.md)  
> [Legacy Documentation Notice](00_LEGACY_NOTICE.md)

---

## 3.1 Purpose of This Document

Piolín passed through several experimental architectures before reaching its current EV3-centered configuration.

During those stages, the team recorded observations related to:

```text
Vision detection

Lighting sensitivity

Ultrasonic measurements

Noise filtering

Steering control

Processing latency

Electrical reliability

Controller selection
```

The purpose of this file is to preserve those previous measurements and observations as part of the engineering record.

The results should be interpreted using the following principle:

```text
Historical Hardware
        +
Historical Software
        +
Historical Test Conditions
        ↓
Historical Result
```

A numerical result obtained from an earlier prototype should not automatically be used to describe the final robot.

---

# 3.2 Historical Vision Subsystem Analysis

Vision-system performance was investigated during multiple stages of Piolín's development.

Earlier work included the **PixyCam 2.1**, while later development moved toward a HuskyLens-based architecture.

The objective of these experiments was to determine how reliably a camera-based subsystem could identify relevant colored objects under changing environmental conditions.

Conceptually:

```text
VISIBLE TARGET
      ↓
CAMERA
      ↓
OBJECT DETECTION
      ↓
VALID DETECTION?
      │
  ┌───┴───┐
  ▼       ▼
 YES      NO
  │       │
  ▼       ▼
Usable   Missed /
Data     Invalid Data
```

The camera experiments demonstrated that detection quality depended not only on software configuration but also on the physical environment.

---

# 3.3 Historical Vision Error Metric

One archived method used to describe visual-tracking performance was a frame-based error percentage.

The historical relationship was:

```text
VISION_ERROR =
(DROPPED_FRAMES + FALSE_POSITIVES)
/
TOTAL_FRAMES
× 100
```

In mathematical form:

```text
E_VISION =
((F_DROPPED + F_FALSE_POSITIVE) / F_TOTAL) × 100
```

where:

```text
F_DROPPED
=
Frames in which the expected target was present
but no valid detection was returned


F_FALSE_POSITIVE
=
Frames in which an unrelated region was
interpreted as the target


F_TOTAL
=
Total number of frames considered
```

This metric was useful because it separated two different vision failures:

```text
MISS
↓
Target exists but is not detected


FALSE POSITIVE
↓
Detection exists but target is incorrect
```

> [!NOTE]
> The frame counts and percentages preserved below are **historical records from an earlier development document**.
>
> They are not presented as validated performance measurements of the current HuskyLens system.

---

# 3.4 Archived Vision Benchmark Table

The original development documentation recorded the following comparison:

| Historical Environment Profile | Recorded Light Level | PixyCam 2.1 Recorded Error | Later HuskyLens Recorded Error |
| :--- | :---: | :---: | :---: |
| **Standard Ambient** | 450 lx | 4.2% | 0.8% |
| **High Overhead Glare** | 1,200 lx | 14.8% | 2.1% |
| **Low-Contrast Shadowing** | 150 lx | 18.5% | 2.9% |
| **Recorded Composite Mean** | — | 12.5% | 1.93% |

These values are retained because they show the type of quantitative comparison considered during development.

They should not be interpreted as current competition specifications.

The important engineering observation from these experiments was broader:

```text
Lighting Conditions
        ↓
Visual Appearance Changes
        ↓
Detection Reliability Can Change
```

This reinforced the need to consider camera placement, lighting conditions, target training, and fallback sensing when designing the obstacle-recognition architecture.

---

# 3.5 Lessons From the PixyCam Comparison

The PixyCam experiments demonstrated that color-based vision could provide useful object information, but also exposed sensitivity to the visual environment.

The observed development concerns included:

```text
Glare

Shadowing

Color appearance

Field of view

Target position

Camera orientation
```

These findings contributed to the later decision to change the vision subsystem.

The evolution was:

```text
PixyCam Experiments
        ↓
Vision Limitations Observed
        ↓
Architecture Reconsidered
        ↓
HuskyLens Introduced
        ↓
Arduino Nano Interface
        ↓
Current Vision Architecture
```

For the current system, use:

[HuskyLens Component Documentation](../components/07_HuskyLens.md)

---

# 3.6 Historical Ultrasonic Experiments

Piolín also passed through different ultrasonic configurations during development.

Some archived testing material described a **three-direction ranging prototype** using left, center, and right distance measurements.

The historical concept was:

```text
             LEFT        FRONT        RIGHT
              \            |            /
               \           |           /
                \          |          /
                 \         |         /
                     ROBOT
```

Some prototype documentation represented those sensors using GPIO identifiers.

Those GPIO labels belong to an earlier non-final electronics concept and should not be confused with the current EV3 port assignment.

The current Piolín configuration is:

```text
S1 → Front Ultrasonic

S2 → Right Ultrasonic

S3 → Left Ultrasonic

S4 → Color Sensor
```

Current documentation:

[Ultrasonic Sensors](../components/05_UltrasonicSensors.md)

---

# 3.7 Current vs. Historical Ultrasonic Architecture

The historical material may contain representations such as:

```text
Left Sensor   → GPIO15

Center Sensor → GPIO17

Right Sensor  → GPIO23
```

These are **not current Piolín connections**.

The final architecture is:

```text
                     FRONT
                       ↑

               Front US — S1


Left US — S3 ← [ PIOLÍN ] → Right US — S2
```

The current responsibilities are:

```text
S2 + S3
   ↓
Lateral wall geometry
```

and:

```text
S1
   ↓
Frontal safety
```

The previous GPIO-based arrangement is preserved only as evidence of an earlier prototype architecture.

---

# 3.8 Historical Ultrasonic Noise Filtering

Previous software experiments also investigated the use of median-based filtering to reduce the influence of isolated abnormal distance readings.

The general principle was:

```text
Raw Readings
     ↓
Small Measurement Window
     ↓
Median Value
     ↓
Navigation Input
```

An archived experimental rule compared an individual distance measurement against the running median.

The historical relationship was:

```text
DELTA_D =
ABS(D_N - MEDIAN)
```

and one prototype used:

```text
DELTA_D > 5 cm
```

as an outlier condition.

> [!NOTE]
> The `5 cm` value belongs to a previous experiment and is preserved for historical context.
>
> It is not documented here as a current Piolín ultrasonic threshold.

The useful engineering concept was the use of a **median filter** rather than blindly reacting to every isolated reading.

---

# 3.9 Why Median Filtering Was Investigated

Ultrasonic measurements can occasionally contain values that differ significantly from neighboring readings.

A single abnormal reading can create a large steering correction if used directly.

Conceptually:

```text
Normal Reading
      ↓
Normal Reading
      ↓
Abnormal Reading
      ↓
Normal Reading
```

Without filtering:

```text
One abnormal reading
        ↓
Large navigation error
        ↓
Strong unnecessary correction
```

With a short median filter:

```text
269
271
1120
   ↓
MEDIAN
   ↓
271
```

The median is less affected by one extreme value than a simple arithmetic mean.

This concept remained useful throughout Piolín's sensor-development process.

---

# 3.10 Archived Ultrasonic Accuracy Table

An earlier development record contained the following ranging table:

| Reference Distance | Recorded Raw Mean | Recorded Filtered Mean | Recorded Standard Deviation |
| :--- | :---: | :---: | :---: |
| **5.0 cm** | 5.2 cm | 5.02 cm | 0.08 cm |
| **15.0 cm** | 15.6 cm | 15.04 cm | 0.12 cm |
| **30.0 cm** | 31.2 cm | 30.11 cm | 0.24 cm |
| **50.0 cm** | 52.8 cm | 50.29 cm | 0.45 cm |

These values are retained as **legacy benchmark records**.

They are not presented as calibration data for the current EV3 ultrasonic installation because the sensor arrangement, mounting geometry, hardware interface, and software environment changed during development.

For current sensor interpretation, use:

[Current Ultrasonic Sensor Documentation](../components/05_UltrasonicSensors.md)

and:

[Ultrasonic Sensor Data](../power_sensors/02_USSensorD.md)

---

# 3.11 Historical Control-Loop Experiments

Piolín's development also included several steering-control experiments.

Some previous architectures investigated PID-style control.

The general mathematical model was:

```text
u(t) =
Kp × e(t)
+
Ki × integral(e(t))
+
Kd × derivative(e(t))
```

where:

```text
u(t)
=
Controller output


e(t)
=
Current navigation error


Kp
=
Proportional gain


Ki
=
Integral gain


Kd
=
Derivative gain
```

The objective was to convert a measured error into a steering command.

Different development stages used different definitions of the error depending on the available sensors.

---

# 3.12 Historical Vision-Center Error

One previous camera-control concept defined a target horizontal image position.

For example:

```text
X_TARGET = 160
```

The visual error was then:

```text
ERROR =
X_TARGET - X_MEASURED
```

This represented the difference between the desired camera-frame position and the detected object's horizontal position.

Conceptually:

```text
CAMERA FRAME

0 ---------------- 160 ---------------- 320
                    ↑
                 X_TARGET
```

If the object appeared at:

```text
X_MEASURED = 130
```

then:

```text
ERROR = 160 - 130

ERROR = 30
```

That error could then be passed into a steering controller.

The specific `160` reference belongs to the historical camera geometry and should not be interpreted as a current HuskyLens steering parameter.

---

# 3.13 Why Camera Error Was Not Vehicle Position

An important lesson from the vision-control experiments was that camera coordinates and physical vehicle coordinates are not the same thing.

```text
IMAGE ERROR
     ≠
PHYSICAL WALL DISTANCE
```

and:

```text
IMAGE ERROR
     ≠
PHYSICAL STEERING ANGLE
```

The same object can appear at a similar horizontal camera coordinate while being located at very different physical distances from the robot.

Therefore, the camera alone could not describe the complete track geometry.

This was one reason Piolín continued to combine vision with distance sensing.

---

# 3.14 Historical Controller Experiments

The original development documentation described a PID relationship in which visual error was used as the control input.

Conceptually:

```text
Visual Detection
      ↓
X Position
      ↓
Error
      ↓
PID / Proportional Logic
      ↓
Steering Command
      ↓
Actuator
```

This represented one of several control approaches explored during development.

It should not be interpreted as a statement that the current Piolín obstacle strategy uses this exact mathematical controller.

Current control behavior should be documented from the current software and strategy files.

---

# 3.15 Raspberry Pi Prototype Experiments

Some archived performance notes also refer to a **Raspberry Pi 5-based prototype architecture**.

That platform is not part of the current Piolín robot.

The historical concept involved a more conventional electronics architecture with:

```text
Raspberry Pi

GPIO

PWM

External steering actuator

Camera processing
```

This was fundamentally different from the final EV3 architecture.

The current robot uses:

```text
LEGO EV3
    ↓
Motor A
Motor B
S1–S4
```

with:

```text
HuskyLens
    ↓
Arduino Nano
    ↓
USB
    ↓
EV3
```

The Raspberry Pi material is preserved because it documents a previous direction considered during development.

---

# 3.16 Historical PWM Timing Experiment

One archived section described moving a steering signal from software-controlled timing to a Raspberry Pi hardware PWM channel.

The historical objective was to reduce variation in actuator timing while other software processes were running.

The general concept was:

```text
SOFTWARE TIMING
      ↓
Dependent on processor scheduling


HARDWARE PWM
      ↓
Dedicated timing source
```

The old documentation recorded a change from:

```text
18 ms
```

to:

```text
1.2 ms
```

for a particular latency measurement.

> [!WARNING]
> These values belong to the archived Raspberry Pi prototype documentation.
>
> They do not describe the current LEGO EV3 steering system and should not be used as current Piolín performance specifications.

The useful engineering lesson was that actuator timing can depend strongly on controller architecture.

---

# 3.17 Historical Oscillation Claim

The archived Raspberry Pi notes also reported a steering-settling value of:

```text
220 ms
```

during aggressive recovery behavior.

This value is preserved only as part of the historical record.

It should not be interpreted as a verified current steering-settling time.

The current Piolín steering system is mechanically and electrically different:

```text
CURRENT

LEGO EV3
    ↓
Motor B
    ↓
Ackermann Linkage
    ↓
Front Wheels
```

compared with the previous prototype concept:

```text
LEGACY

Raspberry Pi
    ↓
PWM
    ↓
External actuator
```

The two systems should not be compared directly without a controlled test methodology.

---

# 3.18 Power Problems in the Raspberry Pi Prototype

The original development notes also recorded electrical instability during experiments with the Raspberry Pi architecture.

Reported issues included:

```text
High controller power demand

Unstable actuator supply

Connector sensitivity

Voltage instability

Mechanical vibration affecting connections
```

These problems influenced later decisions about controller and power-system architecture.

The important engineering relationship was:

```text
Complex Processing Platform
        ↓
Higher Electrical Requirements
        ↓
Power Integration Becomes More Difficult
```

This contributed to the search for a simpler embedded-control architecture.

---

# 3.19 Arduino Mega Prototype

Another historical stage involved an **Arduino Mega 2560**.

The Mega was considered as an alternative embedded controller because it removed the operating-system layer present in the Raspberry Pi architecture.

Conceptually:

```text
Raspberry Pi Prototype
        ↓
Electrical / Integration Problems
        ↓
Arduino Mega Prototype
        ↓
Simpler Embedded Control
```

This should not be confused with the Arduino Nano used in the current robot.

The roles were different.

```text
LEGACY ARDUINO MEGA
        ↓
Experimental controller architecture


CURRENT ARDUINO NANO
        ↓
Vision communication interface
```

The current Nano is not the main motor controller.

The LEGO EV3 remains the main controller.

---

# 3.20 Why the Arduino Mega Was Not the Final Controller

Although the Arduino-based experiments reduced some of the complexity associated with the Raspberry Pi prototype, Piolín's architecture continued to evolve.

The final design returned vehicle control to the LEGO EV3 environment.

The progression can be summarized as:

```text
Alternative Computing Experiments
        ↓
Raspberry Pi
        ↓
Electrical / Integration Challenges
        ↓
Arduino-Based Experiments
        ↓
Architecture Reconsidered
        ↓
LEGO EV3 Retained as Main Controller
```

The current hierarchy is:

```text
                MAIN CONTROLLER
                   LEGO EV3
                       ▲
                       │ USB
                       │
                 Arduino Nano
                       ▲
                       │
                   HuskyLens
```

This provides a clearer separation between vehicle control and vision communication.

---

# 3.21 Historical vs. Current Controller Architectures

| Function | Historical Experiments | Current Piolín |
| :--- | :--- | :--- |
| **Main Processing** | Raspberry Pi / Arduino experiments | LEGO EV3 |
| **Motor Control** | External PWM / prototype control | EV3 Motor Ports A and B |
| **Steering** | External actuator concepts | EV3 Motor B |
| **Vision** | PixyCam / other camera experiments | HuskyLens |
| **Vision Interface** | Different historical approaches | Arduino Nano |
| **Distance Sensing** | GPIO / experimental arrays | EV3 S1–S3 |
| **Color Sensor** | Development configurations | EV3 S4 |
| **Operating System Dependency** | Present in Raspberry Pi stage | EV3 software environment |

The table shows why numerical performance data from previous architectures cannot automatically be transferred to the final robot.

---

# 3.22 Why Direct Performance Comparisons Require Caution

A comparison between two robot architectures is meaningful only when the relevant conditions are controlled.

For example:

```text
Same lighting

Same target

Same camera position

Same software

Same mechanical vehicle

Same movement speed

Same evaluation metric
```

Without those controls, a numerical difference may represent changes in several variables at once.

This is particularly important in Piolín's legacy documentation because the robot changed significantly between development stages.

Therefore:

```text
Legacy Value
    ≠
Final Robot Specification
```

unless the value is independently confirmed in current documentation.

---

# 3.23 Most Important Lessons From the Historical Testing

The value of these experiments is not limited to the exact numerical results.

Several broader engineering lessons emerged.

### Vision

```text
Lighting affects visual detection

Field of view affects detection timing

Camera position affects perception

Visual identity does not replace distance sensing
```

### Ultrasonic Sensing

```text
Individual readings may contain outliers

Filtering can improve stability

Sensor orientation changes measurement meaning

Wall geometry must be interpreted according to state
```

### Control

```text
Sensor error must be translated into physical motion

Aggressive correction can create oscillation

Controller behavior depends on mechanical response
```

### Computing

```text
More processing power can create
more integration complexity
```

### Electrical Architecture

```text
Controller selection
        ↓
Changes power requirements
        ↓
Changes integration requirements
```

These lessons influenced the final robot even though the original hardware was later removed.

---

# 3.24 Transition Toward the Final Piolín Architecture

The historical experiments gradually pushed the project toward a simpler division of responsibilities.

The current architecture is:

```text
                         LEGO EV3
                            │
         ┌──────────────────┼──────────────────┐
         ▼                  ▼                  ▼
     PROPULSION          STEERING           SENSORS
      Motor A             Motor B            S1–S4

                            ▲
                            │
                           USB
                            │
                     Arduino Nano
                            ▲
                            │
                        HuskyLens
```

This final arrangement avoids requiring one processor to perform every task.

The responsibilities are separated:

```text
EV3
 ↓
Vehicle control


Arduino Nano
 ↓
Vision communication


HuskyLens
 ↓
Obstacle recognition


Ultrasonics
 ↓
Distance geometry


Color Sensor
 ↓
Course information
```

---

# 3.25 Why This File Remains in Legacy

This file is preserved because the previous experiments provide evidence of real engineering iteration.

The sequence includes:

```text
Vision Benchmarks
        ↓
Sensor Filtering
        ↓
PID Experiments
        ↓
Alternative Controllers
        ↓
Power Problems
        ↓
Architecture Changes
        ↓
Final EV3-Centered System
```

Without this history, the final robot could appear to have been selected without evaluating alternatives.

The legacy testing documentation demonstrates that PiolínTech explored multiple approaches before settling on the current architecture.

---

# 3.26 Data Reliability Notice

The numerical tables and performance claims in this file come from **archived project notes**.

They should be interpreted as historical development records rather than as current certified measurements.

This includes values related to:

```text
Vision error rates

Lux levels

Frame counts

Ultrasonic accuracy

Standard deviation

Latency

Steering settling time

PWM performance
```

No value in this file should override the current hardware, sensing, software, calibration, or testing documentation.

For current validation data, use:

[Testing Protocol](../reproducibility/07_TestingProtocol.md)

and current subsystem documentation.

---

# 3.27 Do Not Reconstruct Piolín From This File

The following combination is **not** the current Piolín architecture:

```text
Raspberry Pi 5

Arduino Mega 2560 as main controller

GPIO ultrasonic sensors

External PWM steering

PixyCam
```

The current architecture is:

```text
Motor A → Drive

Motor B → Steering

S1 → Front Ultrasonic

S2 → Right Ultrasonic

S3 → Left Ultrasonic

S4 → Color Sensor

USB → Arduino Nano
          ↓
      HuskyLens
```

For reconstruction of the current robot, use:

[Current Hardware](../components/)  
[Current Wiring](../reproducibility/03_wiring.md)  
[Current Electrical Schematic](../reproducibility/04_elecschem.md)  
[Software Setup](../reproducibility/05_softwaresetup.md)

---

# 3.28 Historical Architecture Evolution

The development path represented by this file can be summarized as:

```text
EARLY VISION / SENSOR EXPERIMENTS
             ↓
       PixyCam Testing
             ↓
     Ultrasonic Filtering
             ↓
       PID Experiments
             ↓
 Raspberry Pi Architecture
             ↓
 Electrical / Integration Issues
             ↓
 Arduino-Based Experiments
             ↓
 Architecture Simplification
             ↓
        LEGO EV3
             +
       HuskyLens
             +
      Arduino Nano
             ↓
       CURRENT PIOLÍN
```

The exact sequence of every prototype may contain overlapping development stages, but the central engineering progression is clear: the project moved from increasingly complex experimental architectures toward a more modular final system.

---

# 3.29 Current References

For the current robot, use the following documentation instead of the legacy measurements in this file:

[Hardware Overview](../components/01_Hardwareoverview.md)

[LEGO EV3](../components/02_EV3.md)

[Motors](../components/03_Motors.md)

[Steering Motor](../components/04_SteeringMotor.md)

[Ultrasonic Sensors](../components/05_UltrasonicSensors.md)

[Color Sensor](../components/06_ColorSensor.md)

[HuskyLens](../components/07_HuskyLens.md)

[Power Distribution](../components/09_PowerDistribution.md)

[Testing Protocol](../reproducibility/07_TestingProtocol.md)

[Troubleshooting](../reproducibility/08_Troubleshooting.md)

---

# 3.30 Final Legacy Analysis

The performance-testing material preserved in this document represents a period when PiolínTech was evaluating several competing approaches to perception, control, computing, and electrical integration.

The experiments included:

```text
PixyCam vision
        ↓
Visual detection analysis


Ultrasonic arrays
        ↓
Filtering and ranging analysis


PID concepts
        ↓
Steering-control analysis


Raspberry Pi
        ↓
Processing and PWM experiments


Arduino prototypes
        ↓
Alternative embedded control
```

Several of those systems were eventually removed from the robot, but the problems they exposed influenced the final design.

The most important result of this development was not one individual benchmark number.

It was the gradual refinement of system responsibilities:

```text
PERCEPTION
     ↓
Specialized Sensors


COMMUNICATION
     ↓
Arduino Nano


DECISION MAKING
     ↓
LEGO EV3


ACTUATION
     ↓
Motor A + Motor B
```

The final Piolín architecture is therefore the result of a process of experimentation, comparison, simplification, and integration.

This document should be interpreted as:

> **Historical engineering evidence showing how previous tests and prototype architectures influenced the final Piolín system.**

Return to:

[Legacy Documentation Notice](00_LEGACY_NOTICE.md)

Current configuration:

[Current Hardware](../components/)  
[Current Reproducibility Documentation](../reproducibility/)
