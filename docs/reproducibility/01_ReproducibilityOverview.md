# 1. Reproducibility Overview

This section explains how the current **PiolínTech WRO Future Engineers 2026 robot** can be reconstructed, configured, calibrated, and verified from the information contained in this repository.

The purpose of reproducibility is not only to show what Piolín looks like.

A reproducible engineering repository should allow another person to answer:

```text
What hardware is required?

How is the robot mechanically organized?

Where is each sensor connected?

What software environment is required?

Which program is the current one?

How are the sensors calibrated?

How can the reconstructed robot be tested?

Which documents are current and which are historical?
```

Piolín's reproducibility documentation therefore connects:

```text
BILL OF MATERIALS
        ↓
MECHANICAL ASSEMBLY
        ↓
WIRING
        ↓
SOFTWARE
        ↓
CALIBRATION
        ↓
TESTING
        ↓
COMPETITION OPERATION
```

The files in this folder should be followed together rather than treated as independent documents.

---

## 1.1 Current Robot Baseline

The current Piolín architecture is based on a **LEGO Mindstorms EV3** acting as the main vehicle controller.

The confirmed final architecture is:

```text
                         LEGO EV3
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
             Motor A                 Motor B
          Rear Propulsion        Ackermann Steering


                         LEGO EV3
                            ▲
       ┌──────────┬─────────┼─────────┬──────────┐
       │          │         │         │          │
       ▼          ▼         ▼         ▼          ▼
      S1         S2        S3        S4         USB
       │          │         │         │           │
       ▼          ▼         ▼         ▼           ▼
 Front US     Right US   Left US    Color     Arduino Nano
                                                  ▲
                                                  │
                                              HuskyLens
```

The confirmed EV3 port map is:

| Interface | Current Component | Responsibility |
| :--- | :--- | :--- |
| **Motor A** | Drive Motor | Rear propulsion |
| **Motor B** | Steering Motor | Ackermann steering |
| **S1** | Front Ultrasonic Sensor | Frontal safety |
| **S2** | Right Ultrasonic Sensor | Right-side geometry |
| **S3** | Left Ultrasonic Sensor | Left-side geometry |
| **S4** | LEGO Color Sensor | Floor markings and course state |
| **USB** | Arduino Nano | Vision-data communication |

The HuskyLens provides obstacle information through the Arduino Nano.

The Nano communicates with the EV3 through USB.

The EV3 remains the final decision-making controller.

---

# 1.2 Final Hardware Scope

The current competition robot uses:

```text
LEGO EV3

Motor A
Motor B

3 Ultrasonic Sensors

1 Color Sensor

Arduino Nano

HuskyLens

Rear-wheel propulsion

Front Ackermann-style steering

LEGO Technic chassis
```

The current robot does **not** use:

```text
Gyroscope

PixyCam

Raspberry Pi

Arduino Mega as the main controller
```

Those components appeared during previous development stages and are documented separately.

See:

[Legacy Documentation](../legacy/00_LEGACY_NOTICE.md)

---

# 1.3 Confirmed Physical Specifications

The current assembled robot has the following confirmed specifications:

| Parameter | Current Value |
| :--- | :---: |
| **Length** | 210 mm |
| **Width** | 150 mm |
| **Height** | 230 mm |
| **Mass** | 0.80476 kg |
| **Rear wheel diameter** | ~61.0 mm |
| **Rear wheel radius** | ~30.5 mm |
| **Rear wheel circumference** | ~191.5 mm |
| **Front wheel diameter** | 38.1 mm |
| **Front wheel radius** | 19.05 mm |
| **Front wheel circumference** | ~119.7 mm |
| **Lateral ultrasonic height** | ~43.2 mm above floor |

Values such as:

```text
Final wheelbase

Final track width

Final center of mass

Final lateral sensor offsets

Exact camera mounting angle
```

are not presented as confirmed dimensions unless explicitly measured in the current robot documentation.

This prevents older development measurements from being mistaken for final construction specifications.

---

# 1.4 Reproducibility File Map

The files in this folder are organized by reconstruction stage.

```text
docs/reproducibility/

01_ReproducibilityOverview.md
        ↓
Overall reconstruction map


02_BOM.pdf
        ↓
Required components and materials


03_wiring.md
        ↓
Physical electrical / signal connections


04_elecschem.md
        ↓
Electrical architecture


05_softwaresetup.md
        ↓
Software environment and execution


06_HowToCalibrate.md
        ↓
Sensor and vehicle calibration


07_TestingProtocol.md
        ↓
Verification procedure


08_Troubleshooting.md
        ↓
Failure diagnosis
```

The recommended reading order is the same:

```text
OVERVIEW
   ↓
BOM
   ↓
WIRING
   ↓
SOFTWARE
   ↓
CALIBRATION
   ↓
TESTING
   ↓
TROUBLESHOOTING
```

---

# 1.5 Step 1 — Obtain the Required Components

The reconstruction process begins with the Bill of Materials.

See:

[Bill of Materials](02_BOM.pdf)

The BOM identifies the components required for the current Piolín configuration, including:

```text
EV3 controller

Battery

Drive motor

Steering motor

Three ultrasonic sensors

Color sensor

Arduino Nano

HuskyLens

Wheels

LEGO Technic structural parts

Steering components

Drivetrain components

Sensor mounts

Cables

Jumper wires

Color sensor casing
```

The BOM should be interpreted as a **current-build procurement reference**, not as a list of every component ever tested during the development process.

---

# 1.6 BOM Pricing

Component prices represent procurement or replacement-cost references.

They should not be interpreted as permanent fixed prices because:

```text
Amazon pricing changes

Availability changes

Shipping differs

Taxes differ

Import costs differ

Equivalent parts may have different prices
```

Therefore:

```text
BOM PRICE
=
Procurement reference
```

rather than:

```text
Permanent engineering constant
```

The purpose of including cost information is to make reconstruction planning more transparent.

---

# 1.7 Step 2 — Reconstruct the Mechanical Platform

The robot uses a car-like architecture:

```text
FRONT
   ↓
Ackermann steering


REAR
   ↓
Propulsion
```

Motor responsibilities are:

```text
Motor A
=
Drive


Motor B
=
Steering
```

The mechanical documentation should be used while reconstructing the vehicle:

[Mechanical Architecture](../mobility_mechanical/01_mecharchitecture.md)

[Chassis Design](../mobility_mechanical/02_chassis.md)

[Robot Mobility](../mobility_mechanical/03_RMobility.md)

[Ackermann Steering](../mobility_mechanical/04_steering.md)

[Drivetrain](../mobility_mechanical/05_drivetrain.md)

The mechanical system should be established before final sensor calibration because sensor geometry depends on the physical chassis.

---

# 1.8 Mechanical Reconstruction Principle

Piolín should not be reconstructed by copying only its external appearance.

The important functional relationships are:

```text
Motor A
     ↓
Rear propulsion


Motor B
     ↓
Front Ackermann steering


S1
     ↓
Forward-facing


S2
     ↓
Right-facing


S3
     ↓
Left-facing


S4
     ↓
Downward-facing


HuskyLens
     ↓
Forward-facing
```

A visually similar robot with different sensor positions or steering geometry may require different calibration values.

Therefore:

```text
PHYSICAL GEOMETRY
      ↓
determines
      ↓
CALIBRATION
```

---

# 1.9 Step 3 — Install the Sensors

The current sensor arrangement is:

```text
                         FRONT
                           ↑

                       HuskyLens

                         S1
                   Front Ultrasonic


             S3                    S2
        Left Ultrasonic      Right Ultrasonic
                ←              →


                         S4
                         ↓
                    TRACK FLOOR
```

The lateral ultrasonic sensors are mounted approximately:

```text
43.2 mm
```

above the floor.

Their confirmed physical identities are:

```text
S2 = RIGHT

S3 = LEFT
```

These labels should not be reversed during assembly.

---

# 1.10 Step 4 — Install the Color Sensor

The color sensor is connected to:

```text
S4
```

and faces downward.

Its current responsibilities are:

```text
BLUE / ORANGE detection

Initial travel direction

Course progression
```

The color sensor uses a physical casing to reduce unwanted surrounding-light influence.

The printable model is available at:

[Color Sensor Casing STL](../../models/3dprint/ColorSensorCasing.stl)

The casing is part of the sensing system because changing the optical environment can change the measured color values.

---

# 1.11 Step 5 — Install the Vision System

The current obstacle-vision architecture is:

```text
HuskyLens
     ↓
Arduino Nano
     ↓
USB
     ↓
LEGO EV3
```

The confirmed obstacle mapping is:

```text
ID 1
=
GREEN
=
PASS LEFT
```

and:

```text
ID 2
=
RED
=
PASS RIGHT
```

The exact HuskyLens-to-Nano electrical communication protocol should be taken from the current hardware/code once explicitly verified rather than inferred from historical versions.

The confirmed interface between the Nano and EV3 is:

```text
USB
```

---

# 1.12 Step 6 — Complete the Wiring

After the mechanical hardware is installed, all current connections should match the documented port map.

```text
Motor A → Drive

Motor B → Steering

S1 → Front Ultrasonic

S2 → Right Ultrasonic

S3 → Left Ultrasonic

S4 → Color Sensor

Arduino Nano → EV3 USB
```

Detailed connection instructions are provided in:

[Wiring](03_wiring.md)

and:

[Electrical Schematic](04_elecschem.md)

The physical wiring should be verified before running navigation software.

---

# 1.13 Wiring Verification

A simple verification sequence is:

```text
Check Motor A
      ↓
Check Motor B
      ↓
Check S1
      ↓
Check S2
      ↓
Check S3
      ↓
Check S4
      ↓
Check Nano USB
```

Incorrect port mapping can produce behavior that appears to be a software problem.

For example:

```text
Left and right sensors reversed
        ↓
Correct distance measurements
        ↓
Incorrect navigation interpretation
        ↓
Wrong steering
```

Therefore, wiring verification comes before controller tuning.

---

# 1.14 Step 7 — Install the Software Environment

The EV3 requires the software environment documented in:

[Software Setup](05_softwaresetup.md)

The setup documentation should be followed before attempting to calibrate or run the competition software.

The software architecture is documented separately in:

[Software Architecture](../software_obstacles_strategy/01_SWArchitecture.md)

The repository should clearly distinguish:

```text
CURRENT COMPETITION CODE
```

from:

```text
EXPERIMENTAL / LEGACY CODE
```

so a reproducer does not accidentally run an obsolete development version.

---

# 1.15 Software Responsibility Separation

The current architecture conceptually separates:

```text
SENSOR ACQUISITION

STATE INTERPRETATION

NAVIGATION

SAFETY

ACTUATION
```

The data flow is:

```text
SENSORS
   ↓
EV3
   ↓
NAVIGATION STATE
   ↓
CONTROL DECISION
   ↓
Motor A + Motor B
```

The Arduino Nano supports the vision subsystem but does not replace the EV3 as the final motion controller.

---

# 1.16 Open Challenge Configuration

For normal Open Challenge navigation, Piolín uses:

```text
S1
↓
Frontal safety


S2 + S3
↓
Wall geometry


S4
↓
Direction and course progression


EV3
↓
Vehicle control
```

The HuskyLens is not required for ordinary Open-round wall navigation.

The current no-gyro strategy is based on environmental geometry.

---

# 1.17 Open Challenge Direction Mapping

The first valid course color establishes travel direction.

```text
BLUE FIRST
    ↓
COUNTERCLOCKWISE
```

For counterclockwise travel:

```text
S3 LEFT = INNER

S2 RIGHT = OUTER
```

For:

```text
ORANGE FIRST
     ↓
CLOCKWISE
```

the mapping becomes:

```text
S2 RIGHT = INNER

S3 LEFT = OUTER
```

This mapping is essential for reproducing the wall-following behavior correctly.

---

# 1.18 Open Challenge Corner Strategy

The current Open Challenge does not depend on gyro heading.

The simplified sequence is:

```text
FOLLOW INNER WALL
        ↓
INNER WALL DISAPPEARS
        ↓
CONFIRM CORNER
        ↓
TURN
        ↓
OUTER WALL BECOMES
TEMPORARY REFERENCE
        ↓
INNER WALL REAPPEARS
        ↓
CONFIRM CORNER EXIT
        ↓
STABILIZE
        ↓
FOLLOW INNER WALL AGAIN
```

Detailed behavior is documented in:

[Wall Following](../software_obstacles_strategy/03_wallfollowing.md)

[Corner Handling](../software_obstacles_strategy/04_cornerhandling.md)

---

# 1.19 Obstacle Challenge Configuration

The Obstacle Challenge uses the same base vehicle and adds obstacle identity through HuskyLens.

```text
HuskyLens
     ↓
Obstacle identity


S2 + S3
     ↓
Wall constraints


S1
     ↓
Frontal safety


S4
     ↓
Course state


EV3
     ↓
Final vehicle response
```

The camera does not independently control the steering motor.

The EV3 combines the available information before commanding Motor A and Motor B.

---

# 1.20 Obstacle Reproduction Rule

The current obstacle mapping must remain:

```text
GREEN
ID 1
↓
PASS LEFT
```

and:

```text
RED
ID 2
↓
PASS RIGHT
```

If these IDs are re-trained or changed in the camera, the Nano/EV3 interpretation must be updated accordingly.

A mismatched mapping can result in:

```text
Correct camera detection
        ↓
Incorrect obstacle interpretation
        ↓
Wrong passing side
```

---

# 1.21 Step 8 — Calibrate the Sensors

A reconstructed robot should not simply copy numerical constants from an older physical build.

Calibration must correspond to:

```text
CURRENT SENSOR POSITION

CURRENT CHASSIS

CURRENT TRACK

CURRENT SOFTWARE
```

The calibration process is documented in:

[How to Calibrate](06_HowToCalibrate.md)

and the engineering theory behind those values is documented in:

[Sensor Calibration](../power_sensors/05_Calibration.md)

---

# 1.22 Calibration Dependency

The calibration process follows:

```text
MECHANICAL ASSEMBLY
        ↓
SENSOR INSTALLATION
        ↓
RAW SENSOR DATA
        ↓
CALIBRATION
        ↓
SOFTWARE CONSTANTS
```

This means that changing:

```text
Sensor position

Camera position

Color sensor casing

Steering mechanism

Robot geometry
```

can require recalibration.

---

# 1.23 Ultrasonic Calibration

The lateral sensors produce:

```text
D_LEFT

D_RIGHT
```

which are converted into:

```text
D_INNER

D_OUTER
```

according to course direction.

A normal wall-following error can be represented as:

```text
E_WALL =
D_TARGET - D_INNER
```

while a lateral corridor-consistency variable can be represented as:

```text
G =
ABS(
(D_INNER + D_OUTER)
-
C_REF
)
```

The values:

```text
D_TARGET

C_REF

G tolerance
```

must come from current calibration rather than old development constants.

---

# 1.24 Front Ultrasonic Calibration

The S1 front ultrasonic sensor is calibrated independently.

It is not part of:

```text
D_INNER

D_OUTER
```

Its role is:

```text
Forward clearance
      ↓
Frontal safety
```

The current safety threshold should be taken from validated current software/calibration.

No historical or unverified value should be treated as final.

---

# 1.25 Color Calibration

The S4 color sensor should be calibrated for at least:

```text
BLUE

ORANGE

NORMAL FLOOR
```

The sensor classification must also support:

```text
One physical marking
      ↓
One valid course event
```

rather than counting every raw sample.

The intended complete three-lap progression contains:

```text
12 valid BLUE events

12 valid ORANGE events
```

with duplicate readings from the same physical marking rejected by event logic.

---

# 1.26 Vision Calibration

Vision validation must confirm the complete chain:

```text
Physical Green pillar
        ↓
HuskyLens
        ↓
ID 1
        ↓
Nano
        ↓
EV3
        ↓
GREEN state
```

and:

```text
Physical Red pillar
        ↓
HuskyLens
        ↓
ID 2
        ↓
Nano
        ↓
EV3
        ↓
RED state
```

Vision calibration should be performed on the installed robot because camera mounting affects:

```text
Field of view

Detection timing

Object position

Visibility after turns
```

---

# 1.27 Step 9 — Verify the Reconstructed Robot

After calibration, the robot should be verified through the protocol in:

[Testing Protocol](07_TestingProtocol.md)

Testing should move from isolated subsystems toward complete autonomous behavior.

```text
CONNECTION CHECK
      ↓
SENSOR CHECK
      ↓
MOTOR CHECK
      ↓
STEERING CHECK
      ↓
STRAIGHT MOTION
      ↓
WALL FOLLOWING
      ↓
CORNER
      ↓
COLOR EVENTS
      ↓
VISION
      ↓
OBSTACLE AVOIDANCE
      ↓
FULL RUN
```

This makes failures easier to isolate.

---

# 1.28 Mechanical Verification

The mechanical baseline should be checked using:

[Mechanical Testing](../mobility_mechanical/06_testing.md)

Important physical behaviors include:

```text
Steering center

Steering repeatability

Free drivetrain movement

Straight propulsion

Forward/reverse motion

Corner behavior

Sensor-mount stability
```

Software tuning should not be used as the first solution to an unresolved mechanical fault.

---

# 1.29 Sensor Verification

Sensor verification should confirm:

```text
S1 changes with frontal distance

S2 changes with right-wall distance

S3 changes with left-wall distance

S4 distinguishes required floor states

HuskyLens distinguishes expected pillar IDs
```

The goal is to validate the complete sensing chain before evaluating full autonomous navigation.

---

# 1.30 Reproducibility Test Principle

A successful reconstruction should not be evaluated only by one successful competition run.

The stronger question is:

> Does the reconstructed robot respond consistently to the same conditions?

Therefore, validation should use repeated observations where appropriate.

The engineering chain is:

```text
BUILD
  ↓
CALIBRATE
  ↓
TEST
  ↓
REPEAT
  ↓
COMPARE
```

---

# 1.31 Troubleshooting Order

If the reconstructed robot does not behave as expected, use:

[Troubleshooting](08_Troubleshooting.md)

The general diagnosis order is:

```text
1. Physical assembly
        ↓
2. Wiring
        ↓
3. Raw sensor data
        ↓
4. Motor response
        ↓
5. Calibration
        ↓
6. State interpretation
        ↓
7. Control parameters
```

This avoids immediately modifying software when the source of the failure is mechanical or electrical.

---

# 1.32 Reproducibility and Version Control

A major requirement of reproducibility is knowing **which robot version a file describes**.

The repository contains both:

```text
CURRENT SYSTEM
```

and:

```text
DEVELOPMENT HISTORY
```

These must not be mixed.

The current documentation always takes priority for reconstruction.

Legacy documents exist to explain:

```text
What was attempted

What changed

Why the architecture evolved
```

not to provide current build instructions.

---

# 1.33 Current vs. Legacy Quick Reference

| Feature | Current Piolín | Legacy / Experimental |
| :--- | :--- | :--- |
| Main controller | LEGO EV3 | Other concepts tested historically |
| Propulsion | Motor A | Older configurations |
| Steering | Motor B Ackermann-style | Previous steering iterations |
| S1 | Front Ultrasonic | Gyro in older architecture |
| S2 | Right Ultrasonic | Different arrangements existed |
| S3 | Left Ultrasonic | Different arrangements existed |
| S4 | Color Sensor | Color Sensor also used previously |
| Gyroscope | Not installed | Used experimentally |
| Vision | HuskyLens | PixyCam |
| Vision support | Arduino Nano | Arduino Mega / other experiments |
| Nano → EV3 | USB | Not applicable to all legacy stages |
| Raspberry Pi | Not used | Historical prototype |

The complete legacy notice is available at:

[Legacy Documentation Notice](../legacy/00_LEGACY_NOTICE.md)

---

# 1.34 Evidence Required for Reproducibility

Documentation becomes stronger when every major design claim can be traced to evidence.

A useful evidence chain is:

```text
DESIGN CLAIM
      ↓
HARDWARE / SOFTWARE DESCRIPTION
      ↓
PHOTO / DIAGRAM / SOURCE CODE
      ↓
CALIBRATION
      ↓
TEST
      ↓
RESULT
```

Examples:

```text
"Piolín uses Ackermann steering"
        ↓
Steering documentation
        ↓
Physical steering GIF
```

```text
"Piolín detects Green as ID 1"
        ↓
HuskyLens documentation
        ↓
Vision code / test
```

```text
"Piolín follows the inner wall"
        ↓
Ultrasonic architecture
        ↓
Wall-following software
        ↓
Run evidence
```

This traceability makes the repository easier to evaluate and reproduce.

---

# 1.35 Repository Evidence Sources

Useful evidence is distributed through:

[Version Photos](../../v-photos/README.md)

[Videos](../../videos/links.md)

[3D Models](../../models/README.md)

[Electrical Schemes](../../schemes/README.md)

[Mechanical Documentation](../mobility_mechanical/)

[Power and Sensor Documentation](../power_sensors/)

[Software and Obstacle Strategy](../software_obstacles_strategy/)

[Systems Engineering](../systems_engineering/)

These sections should be used together when reconstructing or evaluating Piolín.

---

# 1.36 Reproduction Checklist

Before considering the reconstruction complete, verify:

| Check | Expected State |
| :--- | :--- |
| EV3 installed | Yes |
| Motor A connected | Drive |
| Motor B connected | Steering |
| S1 connected | Front Ultrasonic |
| S2 connected | Right Ultrasonic |
| S3 connected | Left Ultrasonic |
| S4 connected | Color Sensor |
| Nano connected to EV3 | USB |
| HuskyLens installed | Forward-facing |
| Green mapping | ID 1 → Left pass |
| Red mapping | ID 2 → Right pass |
| Color sensor | Downward-facing |
| Color casing installed | Yes |
| Rear propulsion functional | Yes |
| Ackermann steering functional | Yes |
| Ultrasonic readings verified | Yes |
| Color classification calibrated | Yes |
| Vision IDs verified | Yes |
| Software environment installed | Yes |
| Current competition code identified | Yes |
| Calibration completed | Yes |
| Testing protocol completed | Yes |

This checklist verifies architecture and configuration rather than guaranteeing competition performance.

---

# 1.37 Minimal Reconstruction Sequence

For a concise build process:

```text
1
Read BOM
      ↓
2
Build chassis
      ↓
3
Install drivetrain
      ↓
4
Install Ackermann steering
      ↓
5
Install EV3
      ↓
6
Install S1 / S2 / S3
      ↓
7
Install S4 + casing
      ↓
8
Install HuskyLens + Nano
      ↓
9
Complete wiring
      ↓
10
Install software
      ↓
11
Verify raw sensors
      ↓
12
Calibrate
      ↓
13
Run subsystem tests
      ↓
14
Run complete challenge tests
```

This is the shortest path through the complete reproducibility documentation.

---

# 1.38 Full System Reconstruction Map

The complete dependency structure is:

```text
                       BILL OF MATERIALS
                              │
                              ▼
                       PHYSICAL CHASSIS
                              │
                 ┌────────────┴────────────┐
                 ▼                         ▼
             DRIVETRAIN                 STEERING
                 │                         │
                 └────────────┬────────────┘
                              ▼
                         SENSOR MOUNTS
                              │
          ┌───────────┬───────┼───────┬───────────┐
          ▼           ▼               ▼           ▼
         S1         S2 / S3            S4      HuskyLens
          │           │               │           │
          │           │               │        Arduino Nano
          │           │               │           │
          └───────────┴───────┬───────┴───────────┘
                              ▼
                           WIRING
                              │
                              ▼
                           LEGO EV3
                              │
                              ▼
                       SOFTWARE SETUP
                              │
                              ▼
                         CALIBRATION
                              │
                              ▼
                           TESTING
                              │
                              ▼
                       COMPETITION RUN
```

This diagram summarizes the order in which the major systems depend on one another.

---

# 1.39 What Makes Piolín Reproducible

Piolín's reproducibility does not depend on one document.

It depends on connecting:

```text
COMPONENTS

DIMENSIONS

MECHANICAL DESIGN

WIRING

SOFTWARE

CALIBRATION

TESTING

VERSION HISTORY
```

into one traceable engineering system.

The objective is that another technically capable person can move from:

```text
REPOSITORY
```

to:

```text
FUNCTIONAL PIOLÍN BUILD
```

without needing undocumented assumptions about the final architecture.

---

# 1.40 Final Reproducibility Principle

The current Piolín documentation follows this rule:

> **Current build instructions must describe the current robot. Historical experiments must remain available as engineering evidence, but they must not be confused with the final architecture.**

The reconstruction chain is therefore:

```text
CURRENT BOM
      ↓
CURRENT MECHANICS
      ↓
CURRENT WIRING
      ↓
CURRENT SOFTWARE
      ↓
CURRENT CALIBRATION
      ↓
CURRENT TESTING
```

while:

```text
LEGACY
```

remains separate and is used only to explain the evolution of the project.

This separation allows the repository to function simultaneously as:

```text
BUILD DOCUMENTATION

ENGINEERING RECORD

COMPETITION EVIDENCE

REPRODUCIBILITY GUIDE
```

for PiolínTech's WRO Future Engineers 2026 robot.

---

## Reproducibility Documentation

[Bill of Materials](02_BOM.pdf)

[Wiring](03_wiring.md)

[Electrical Schematic](04_elecschem.md)

[Software Setup](05_softwaresetup.md)

[How to Calibrate](06_HowToCalibrate.md)

[Testing Protocol](07_TestingProtocol.md)

[Troubleshooting](08_Troubleshooting.md)

---

## Technical Documentation

[Mechanical Architecture](../mobility_mechanical/01_mecharchitecture.md)

[Chassis Design](../mobility_mechanical/02_chassis.md)

[Robot Mobility](../mobility_mechanical/03_RMobility.md)

[Ackermann Steering](../mobility_mechanical/04_steering.md)

[Drivetrain](../mobility_mechanical/05_drivetrain.md)

[Mechanical Testing](../mobility_mechanical/06_testing.md)

---

## Power and Sensors

[Power and Sensor Configuration](../power_sensors/01_PowerSensorconfig.md)

[Ultrasonic Sensor Data](../power_sensors/02_USSensorD.md)

[Color Sensor](../power_sensors/03_color_sensor.md)

[HuskyLens](../power_sensors/04_huskylens.md)

[Sensor Calibration](../power_sensors/05_Calibration.md)

---

## Software

[Software Architecture](../software_obstacles_strategy/01_SWArchitecture.md)

[State Machine](../software_obstacles_strategy/02_statemachine.md)

[Wall Following](../software_obstacles_strategy/03_wallfollowing.md)

[Corner Handling](../software_obstacles_strategy/04_cornerhandling.md)

[Obstacle Detection](../software_obstacles_strategy/05_obstacledetec.md)

[Obstacle Strategy](../software_obstacles_strategy/06_obstaclestrateg.md)

[Software Tuning](../software_obstacles_strategy/07_softwaretuning.md)

[HuskyLens Vision](../software_obstacles_strategy/08_CameraHLVision.md)

[RGB Detection](../software_obstacles_strategy/09_RGBdetection.md)

---

## Historical Development

[Legacy Documentation Notice](../legacy/00_LEGACY_NOTICE.md)

[Legacy Gyroscope Configuration](../legacy/01_GConfig.md)

[Legacy PixyCam](../legacy/02_CameraPixy.md)

[Legacy Performance Testing](../legacy/03_PTesting&Analysis.md)

---

## Repository Home

[Return to Main README](../../README.md)
