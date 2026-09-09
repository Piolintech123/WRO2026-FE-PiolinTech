# 1. Reproducibility Overview

<div align="center">

<img
  src="../../v-photos/v4/piolin_open_isometric.jpg"
  alt="Piolín in its current Open Challenge configuration"
  width="740"
/>

<br>

<sub><b>Figure 1.1.</b> Piolín's current vehicle platform. Reproducibility requires documenting not only the components, but also their configuration, orientation, software environment, and calibration.</sub>

</div>

Reproducibility is one of the central objectives of the PiolínTech engineering repository.

A robot is not reproducible simply because its source code and component names are available. To reconstruct Piolín successfully, another team or reviewer must also understand **how the hardware is assembled, how each component is connected, which configuration belongs to each competition round, how the sensors are calibrated, which software environment is required, and which parts of the repository describe current hardware rather than historical prototypes**.

For Piolín, reproducibility therefore means documenting the complete chain:

```text
COMPONENTS
    ↓
MECHANICAL INSTALLATION
    ↓
ELECTRICAL CONNECTIONS
    ↓
ROUND CONFIGURATION
    ↓
SOFTWARE ENVIRONMENT
    ↓
CALIBRATION
    ↓
TESTING
    ↓
AUTONOMOUS RUN
```

The objective of this section of the repository is to make Piolín understandable as a complete engineering system rather than as a collection of disconnected files.

---

## 1.1 What Must Be Reproduced

A successful reconstruction must preserve several layers of the project.

### Mechanical architecture

```text
rear-wheel propulsion

Ackermann-style front steering

Motor A drive system

Motor B steering system

sensor positions

sensor orientation

camera mounting
```

### Electrical architecture

```text
EV3 controller

EV3 Rechargeable Battery 45501

motor-port mapping

sensor-port mapping

round-specific S1 device
```

### Software architecture

```text
Open Challenge environment

Obstacle Challenge environment

correct hardware interfaces

correct source-code version
```

### Calibration

```text
steering center

ultrasonic geometry

Color Sensor classification

gyro reference

Pixy signatures and visual geometry
```

### Operational procedure

```text
round conversion

pre-run checks

startup

testing

failure diagnosis
```

All of these layers influence autonomous behavior.

Copying only the software without reproducing the physical assumptions behind it will not necessarily reproduce the same vehicle response.

---

# 1.2 Common Vehicle Platform

Piolín uses one common mechanical platform for both WRO Future Engineers challenges.

The components that remain installed in both rounds are:

| Component | Current Function |
| :--- | :--- |
| LEGO Mindstorms EV3 Brick | Main controller |
| EV3 Rechargeable DC Battery 45501 | Main power source |
| EV3 Large Motor — Port A | Rear propulsion |
| EV3 Medium Motor — Port B | Front steering |
| Left EV3 Ultrasonic — S2 | Left-side geometry |
| Right EV3 Ultrasonic — S3 | Right-side geometry |
| EV3 Color Sensor — S4 | Floor and course-state sensing |
| Ackermann-style steering system | Vehicle direction control |
| Rear drivetrain | Propulsion transmission |

The permanent port rules are:

```text
A  = PROPULSION

B  = STEERING

S2 = LEFT ULTRASONIC

S3 = RIGHT ULTRASONIC

S4 = COLOR SENSOR
```

These mappings should remain identical in:

```text
hardware

source code

testing notes

wiring documentation

troubleshooting procedures
```

A mismatch in only one of these layers can produce behavior that appears to be a navigation problem even when the control logic itself is correct.

---

# 1.3 Two Reproducible Round Configurations

The most important hardware distinction in the current robot is Sensor Port S1.

Piolín has two intentional competition configurations.

### Open Challenge

```text
S1 → EV3 Gyro Sensor
S2 → Left Ultrasonic
S3 → Right Ultrasonic
S4 → Color Sensor
```

### Obstacle Challenge

```text
S1 → Pixy2.1
S2 → Left Ultrasonic
S3 → Right Ultrasonic
S4 → Color Sensor
```

The **Gyro Sensor and Pixy2.1 are never installed simultaneously** in the current architecture.

This is not an optional configuration detail. It is fundamental to reproducing the robot correctly.

<div align="center">

<img
  src="../../v-photos/v4/s1_open_gyro.jpg"
  alt="Piolín Open configuration with EV3 Gyro Sensor on S1"
  width="650"
/>

<br>

<sub><b>Figure 1.2.</b> Open Challenge S1 configuration.</sub>

</div>

<div align="center">

<img
  src="../../v-photos/v4/s1_obstacle_pixy.jpg"
  alt="Piolín Obstacle configuration with Pixy2.1 on S1"
  width="650"
/>

<br>

<sub><b>Figure 1.3.</b> Obstacle Challenge S1 configuration.</sub>

</div>

A reconstruction should therefore treat Piolín as:

```text
ONE VEHICLE
+
TWO VERIFIED SENSOR CONFIGURATIONS
```

rather than attempting to combine all sensors into one permanent hardware arrangement.

---

# 1.4 Reproducing the Open Challenge Configuration

<div align="center">

<img
  src="../../v-photos/v4/wiring_open.jpg"
  alt="Piolín Open Challenge wiring configuration"
  width="740"
/>

<br>

<sub><b>Figure 1.4.</b> Current Open Challenge wiring reference.</sub>

</div>

The Open configuration uses only LEGO Mindstorms EV3 hardware for sensing.

The complete mapping is:

```text
MOTOR PORTS

A → EV3 Large Motor
B → EV3 Medium Motor
```

```text
SENSOR PORTS

S1 → EV3 Gyro Sensor
S2 → LEFT EV3 Ultrasonic Sensor
S3 → RIGHT EV3 Ultrasonic Sensor
S4 → EV3 Color Sensor
```

The Gyro Sensor provides the specialized orientation reference needed for:

```text
heading stabilization

drift reduction

corner rotation

corner-exit support
```

while the two ultrasonic sensors retain their lateral geometric role.

The Color Sensor remains the physical course-state reference.

A correct Open reconstruction therefore requires more than connecting the gyro. The gyro must also preserve its intended physical orientation relative to the chassis.

---

## 1.5 Open Software Reproduction

The current Open development environment uses:

```text
Pybricks MicroPython
```

The active Open program should correspond to the hardware configuration containing:

```text
Gyro on S1

Left US on S2

Right US on S3

Color on S4
```

The startup process must also establish the gyro reference before normal navigation.

Conceptually:

```text
power robot
    ↓
load Open program
    ↓
verify sensors
    ↓
place Piolín at start
    ↓
keep vehicle stationary
    ↓
reset gyro reference
    ↓
begin autonomous run
```

A software file written for the Obstacle Challenge should not be expected to run correctly with this hardware configuration because the S1 interface is completely different.

---

# 1.6 Reproducing the Obstacle Challenge Configuration

<div align="center">

<img
  src="../../v-photos/v4/wiring_obstacle.jpg"
  alt="Piolín Obstacle Challenge wiring configuration"
  width="740"
/>

<br>

<sub><b>Figure 1.5.</b> Current Obstacle Challenge wiring reference with Pixy2.1 on S1.</sub>

</div>

The Obstacle Challenge keeps the same common vehicle hardware but replaces the Gyro Sensor with Pixy2.1.

```text
MOTOR PORTS

A → EV3 Large Motor
B → EV3 Medium Motor
```

```text
SENSOR PORTS

S1 → Pixy2.1
S2 → LEFT EV3 Ultrasonic Sensor
S3 → RIGHT EV3 Ultrasonic Sensor
S4 → EV3 Color Sensor
```

The active robot does not use:

```text
Gyro

HuskyLens

Arduino Nano

permanent front ultrasonic
```

during this configuration.

Pixy2.1 is connected directly through the current S1 interface and supplies the forward visual information required for obstacle navigation.

---

# 1.7 Reproducing the Pixy2.1 Installation

<div align="center">

<img
  src="../../v-photos/v4/pixy21_s1_connection.jpg"
  alt="Pixy2.1 connection to EV3 Sensor Port S1"
  width="680"
/>

<br>

<sub><b>Figure 1.6.</b> Current Pixy2.1 connection used in the Obstacle Challenge.</sub>

</div>

Pixy2.1 is the main non-LEGO sensor in the current vehicle, so its physical integration requires particular attention during reproduction.

The connection path is:

```text
Pixy2.1
    ↓
current connection cable
    ↓
EV3 Sensor Port S1
```

The camera must also preserve approximately the same:

```text
forward orientation

mounting position

pitch

yaw

structural stability
```

because the software interprets visual coordinates relative to the camera frame.

The current camera additionally uses a **3D-printed casing**. That casing is part of the present Obstacle Challenge hardware and should remain installed when reproducing the final vision configuration and performing camera calibration.

The casing serves as part of the physical camera installation by supporting and protecting the vision module and helping maintain a more repeatable operating environment.

Changing the camera mount or casing can change visual calibration even if the Pixy software itself remains unchanged.

---

# 1.8 Pixy Signature Reproduction

The current trained visual categories are:

```text
sig1 → Pink → parking reference

sig2 → Red → pass RIGHT

sig3 → Green → pass LEFT
```

These mappings must agree across:

```text
Pixy training

EV3 source code

documentation
```

A reconstructed camera that uses a different signature numbering scheme will not behave correctly unless the software is changed to match.

The obstacle rules themselves remain fixed:

```text
RED
→ pass RIGHT

GREEN
→ pass LEFT
```

The visual `x` coordinate is used to describe where the target appears in the camera image. It must not be used to redefine which side the robot is required to pass.

---

# 1.9 Reproducing the Permanent Sensors

The two lateral ultrasonic sensors and the Color Sensor remain unchanged between rounds.

<div align="center">

<img
  src="../../v-photos/v4/PiolinUSlabeling.png"
  alt="Piolín permanent ultrasonic sensor mapping"
  width="700"
/>

<br>

<sub><b>Figure 1.7.</b> Permanent ultrasonic identity: S2 LEFT and S3 RIGHT.</sub>

</div>

This physical convention is especially important because the navigation software later assigns the concepts:

```text
INNER

OUTER
```

according to course direction.

For counterclockwise Open navigation:

```text
S2 LEFT
→ inner

S3 RIGHT
→ outer
```

For clockwise Open navigation:

```text
S3 RIGHT
→ inner

S2 LEFT
→ outer
```

The sensors themselves are never physically renamed or swapped.

A reproducible system should always preserve physical identity first and calculate the logical role afterward.

---

# 1.10 Reproducing the Color Sensor Installation

<div align="center">

<img
  src="../../v-photos/v4/color_sensor_casing.jpg"
  alt="Piolín Color Sensor light isolation casing"
  width="650"
/>

<br>

<sub><b>Figure 1.8.</b> The Color Sensor casing is part of the calibrated S4 installation.</sub>

</div>

The Color Sensor is installed downward on S4.

The current installation includes a casing used to reduce uncontrolled ambient illumination around the floor-sensing region.

Reproducing S4 therefore requires preserving more than:

```text
same sensor
+
same port
```

It should also preserve the important physical conditions of the installation:

```text
downward orientation

similar height

stable mounting

light-isolation casing
```

The floor classifier should then be calibrated against the actual:

```text
Blue

Orange

normal floor
```

conditions used during testing.

Current Open direction logic is:

```text
BLUE first
→ counterclockwise

ORANGE first
→ clockwise
```

Later detections primarily contribute to course progression.

---

# 1.11 Reproducing Mechanical Behavior

Software reproduction depends on mechanical reproduction.

Piolín uses:

```text
Motor A
→ rear propulsion
```

and:

```text
Motor B
→ Ackermann-style front steering
```

<div align="center">

<img
  src="../../v-photos/v4/ackermann_top.jpg"
  alt="Piolín Ackermann-style steering mechanism"
  width="700"
/>

<br>

<sub><b>Figure 1.9.</b> Steering geometry is part of the control system because software commands Motor B, but the physical linkage determines the resulting wheel angles.</sub>

</div>

Two robots can run the same source code and still produce different trajectories if they differ mechanically in:

```text
steering center

steering linkage geometry

mechanical play

wheel alignment

drivetrain friction

wheel dimensions

sensor location
```

For this reason, the reproducibility documentation separates:

```text
SOFTWARE COMMAND
```

from:

```text
PHYSICAL RESPONSE
```

The encoder position of Motor B should not automatically be treated as the same quantity as the physical wheel angle.

Likewise, Motor A encoder displacement should not automatically be treated as perfect physical vehicle distance.

---

# 1.12 Reproducing the Drivetrain

<div align="center">

<img
  src="../../v-photos/v4/rear_drivetrain_top.jpg"
  alt="Piolín current rear drivetrain"
  width="700"
/>

<br>

<sub><b>Figure 1.10.</b> Current rear drivetrain used in both competition rounds.</sub>

</div>

The same propulsion drivetrain is retained for Open and Obstacles.

A reconstructed vehicle should preserve the functional chain:

```text
Motor A
    ↓
rear drivetrain
    ↓
rear wheels
    ↓
vehicle movement
```

The final reproduction should verify:

```text
Motor A secure

axles aligned

wheels secure

drivetrain rotates freely

no wheel rub

no excessive binding
```

A drivetrain with significantly different friction can change:

```text
vehicle speed

corner timing

obstacle reaction distance

parking displacement
```

even when the source code is identical.

---

# 1.13 Calibration Is Required After Assembly

Rebuilding the physical hardware is not the end of the reproduction process.

The robot must then be calibrated.

At minimum, the following should be verified:

| Subsystem | Calibration / Verification |
| :--- | :--- |
| Steering | Mechanical center and useful range |
| Motor A | Direction and repeatable drive response |
| S2 | Left ultrasonic geometry |
| S3 | Right ultrasonic geometry |
| S4 | Blue / Orange / normal floor classification |
| Open S1 | Gyro orientation, zero, heading behavior |
| Obstacle S1 | Pixy signatures, image geometry, target behavior |
| Pixy mounting | Camera orientation and 3D casing installed |
| Complete robot | Dynamic straight, corner, obstacle, recovery tests |

Calibration values from an earlier mechanical version should not automatically be reused.

The correct process is:

```text
assemble current hardware
      ↓
verify mounting
      ↓
measure
      ↓
calibrate
      ↓
test
```

rather than:

```text
copy old values
      ↓
assume same behavior
```

---

# 1.14 Software Environment Must Match the Round

Piolín currently uses separate software paths because the specialized sensor interface differs significantly between rounds.

### Open Challenge

```text
Pybricks MicroPython
+
EV3 Gyro
+
EV3 sensors
```

### Obstacle Challenge

```text
ev3dev2
+
SMBus / I2C
+
Pixy2.1
+
EV3 sensors
```

These environments should not be mixed unnecessarily.

A reproducible repository should make it possible to identify:

```text
which source file belongs to which round

which runtime is required

which hardware should be connected

how the program should be started
```

before testing begins.

This avoids debugging a software-environment problem as if it were a sensor or control problem.

---

# 1.15 Recommended Reconstruction Order

A reliable reconstruction should proceed in a controlled order.

```text
1. Build the chassis.

2. Install rear drivetrain.

3. Install Motor A.

4. Install Ackermann steering.

5. Install Motor B.

6. Verify free mechanical movement.

7. Install EV3 and Battery 45501.

8. Connect permanent sensors:
   S2 LEFT US
   S3 RIGHT US
   S4 Color

9. Install the correct S1 device.

10. Verify port mapping.

11. Install the correct software environment.

12. Test motors individually.

13. Test raw sensors individually.

14. Calibrate steering.

15. Calibrate sensors.

16. Perform low-speed subsystem tests.

17. Perform round-specific maneuver tests.

18. Perform complete track tests.
```

This order keeps mechanical, electrical, sensing, and software problems easier to isolate.

---

# 1.16 Pre-Run Reproducibility Check

Before comparing one run with another, the system should begin in approximately the same known condition.

A useful pre-run check is:

```text
MECHANICS

rear wheels secure?
steering linkage secure?
Motor A secure?
Motor B secure?
```

```text
SENSORS

correct S1 installed?
S2 physically left?
S3 physically right?
S4 casing secure?
Pixy casing secure if Obstacles?
```

```text
SOFTWARE

correct round program?
correct runtime?
correct current version?
```

```text
START CONDITION

battery ready?
robot at intended start position?
gyro reset if Open?
Pixy communicating if Obstacles?
```

The purpose is to reduce uncontrolled differences between runs.

---

# 1.17 Testing for Reproducibility

One successful run demonstrates that the system can work.

It does not demonstrate that the system is reproducible.

A useful test should therefore repeat the same physical condition several times.

Examples include:

```text
same steering-center test

same encoder-distance test

same Open corner

same Red pillar approach

same Green pillar approach

same parking approach
```

The result should answer:

> **Does approximately the same starting condition produce approximately the same vehicle behavior?**

If not, the team should determine whether the variability originates in:

```text
mechanics

sensor measurements

software state

starting position

battery condition

environment
```

before further tuning.

---

# 1.18 Documentation and Git Versioning

Reproducibility also depends on being able to identify which software produced a specific test result.

A statement such as:

```text
this code worked
```

is not enough if the file has since changed.

Important tests should be associated with a recognizable:

```text
file version

Git commit

test date

hardware configuration
```

A useful relationship is:

```text
TEST
 │
 ├── hardware configuration
 ├── software version
 ├── calibration state
 ├── starting condition
 └── result
```

This makes successful and unsuccessful experiments useful later.

---

# 1.19 Current vs. Legacy Material

One of the most important reproducibility requirements is preventing obsolete prototypes from being mistaken for current construction instructions.

The current robot uses:

### Open

```text
S1 Gyro
S2 Left US
S3 Right US
S4 Color
```

### Obstacles

```text
S1 Pixy2.1
S2 Left US
S3 Right US
S4 Color
```

The following belong to earlier development rather than the active architecture:

```text
HuskyLens

Arduino Nano vision bridge

permanent front ultrasonic

older Pixy integration

earlier ultrasonic orientations

older chassis configurations
```

Legacy material should remain available because it explains the engineering process, but it must be clearly labeled as historical.

A builder following the current reproduction instructions should not need to guess which architecture is still active.

---

# 1.20 Why Legacy Documentation Still Matters

Reproducibility does not mean deleting every design that failed or was replaced.

Historical documentation provides evidence of:

```text
what was tested

why it was changed

what limitations appeared

why the current solution was selected
```

For example, the previous HuskyLens + Arduino architecture helps explain why the current direct Pixy2.1 integration reduces communication and hardware layers.

The important distinction is:

```text
LEGACY
→ engineering history
```

versus:

```text
CURRENT
→ reconstruction instructions
```

Both can exist in the same repository as long as they are not mixed.

---

# 1.21 Information That Must Be Measured on the Current Robot

Some physical specifications are intentionally not reproduced from older Piolín versions because the robot changed mechanically.

The final reproduction documentation should use new V4 measurements for quantities such as:

```text
overall dimensions

vehicle mass

wheelbase

front track width

rear track width

wheel diameters

effective drivetrain ratio

physical steering angles

Pixy mounting geometry
```

Similarly, final control performance should use measured values for:

```text
turning radius

straight-line deviation

sensor repeatability

corner success rate

pillar success rate

parking success rate

run time
```

Until these are measured, the repository should describe the method rather than invent a specification.

---

# 1.22 Reproducibility Failure Diagnosis

If a reconstructed or recently rebuilt Piolín does not behave as expected, the problem should be isolated layer by layer.

| Symptom | First Reproduction Check |
| :--- | :--- |
| Robot does not move | Motor A, Port A, drivetrain |
| Steering wrong | Motor B, center, linkage, Port B |
| Left/right wall logic inverted | Confirm S2 LEFT / S3 RIGHT |
| Open heading unstable | Gyro orientation and startup reset |
| Color events inconsistent | S4 mounting, casing, calibration |
| Pixy unavailable | S1 connection and Obstacle software |
| Red/Green rule inverted | Pixy signature mapping / software rule |
| Different behavior after rebuild | Mechanical alignment and sensor placement |
| Same code but different trajectory | Calibration, battery, drivetrain, steering |
| Obstacle works but recovery fails | S2/S3 geometry and control-state transition |
| Parking varies | Approach geometry, drivetrain, sensor state |

A useful diagnosis follows:

```text
PHYSICAL ASSEMBLY
       ↓
WIRING
       ↓
RAW SENSOR DATA
       ↓
SOFTWARE INTERPRETATION
       ↓
MOTOR COMMAND
       ↓
PHYSICAL VEHICLE RESPONSE
```

This avoids changing controller parameters when the reconstruction problem exists earlier in the chain.

---

# 1.23 Reproducibility Documentation Structure

The remaining files in this section should provide progressively more specific instructions.

Conceptually:

```text
01_ReproducibilityOverview.md
→ overall reconstruction philosophy and configuration
```

```text
03_wiring.md
→ exact electrical connections
```

```text
04_elecschem.md
→ system-level electrical architecture
```

```text
05_softwaresetup.md
→ runtime, dependencies, deployment
```

```text
06_HowToCalibrate.md
→ physical and software calibration process
```

```text
07_TestingProtocol.md
→ repeatable validation method
```

```text
08_Troubleshooting.md
→ failure isolation and recovery
```

Together, these documents should allow a reader to move from:

```text
"What is Piolín?"
```

to:

```text
"I understand how this version can be reconstructed,
configured, calibrated, and tested."
```

---

# 1.24 Reproducibility Checklist

The current Piolín architecture can be summarized through the following reconstruction checklist:

| Category | Required Condition |
| :--- | :--- |
| Controller | LEGO EV3 Brick |
| Power | EV3 Rechargeable Battery 45501 |
| Propulsion | Large Motor on A |
| Steering | Medium Motor on B |
| Steering geometry | Ackermann-style front steering |
| S2 | LEFT Ultrasonic |
| S3 | RIGHT Ultrasonic |
| S4 | Downward Color Sensor with casing |
| Open S1 | Gyro |
| Obstacle S1 | Pixy2.1 |
| Pixy installation | Forward-facing, direct S1 connection, 3D-printed casing |
| Open software | Pybricks MicroPython |
| Obstacle software | ev3dev2 + SMBus/I2C |
| Current front US | Not installed |
| Current HuskyLens | Not installed |
| Current Arduino Nano | Not installed |
| Gyro + Pixy together | No |
| Calibration | Required after reconstruction |
| Testing | Must begin with isolated subsystems |

This table represents the current architecture rather than earlier experimental versions.

---

# 1.25 Complete Reproducibility Chain

<div align="center">

<img
  src="../../v-photos/v4/piolin_obstacle_isometric.jpg"
  alt="Piolín complete Obstacle Challenge configuration"
  width="740"
/>

<br>

<sub><b>Figure 1.11.</b> Reproducing Piolín means preserving the relationships between mechanics, electronics, sensing, software, and calibration—not simply matching the external appearance.</sub>

</div>

The complete process can be represented as:

```text
                  DOCUMENTATION
                       │
                       ▼
                 COMPONENT SET
                       │
                       ▼
              MECHANICAL ASSEMBLY
                       │
                       ▼
                ELECTRICAL WIRING
                       │
                       ▼
              ROUND CONFIGURATION
                       │
                       ▼
               SOFTWARE INSTALL
                       │
                       ▼
              SENSOR CALIBRATION
                       │
                       ▼
                SUBSYSTEM TEST
                       │
                       ▼
                 DYNAMIC TEST
                       │
                       ▼
                  FULL RUN
                       │
                       ▼
                 TEST RECORD
                       │
                       ▼
                VERSION CONTROL
```

Every stage contributes to the ability to reproduce the final vehicle behavior.

---

# 1.26 Final Engineering Assessment

Reproducibility for Piolín means preserving the **relationships** between its subsystems.

A complete copy requires more than:

```text
same motors

same EV3

same code
```

because autonomous behavior also depends on:

```text
mechanical geometry

sensor orientation

port mapping

camera installation

sensor casing

software environment

calibration

starting conditions

test procedure
```

Piolín's current design improves reproducibility by keeping most of the robot identical between competition rounds.

The permanent architecture is:

```text
A  → propulsion

B  → steering

S2 → left ultrasonic

S3 → right ultrasonic

S4 → Color Sensor
```

while only S1 changes:

```text
OPEN
→ Gyro
```

```text
OBSTACLES
→ Pixy2.1
```

The current Pixy2.1 installation includes its **3D-printed casing**, and the current Color Sensor installation includes its light-isolation casing. Both should be considered part of their calibrated physical systems.

The repository also deliberately separates current and legacy designs so that earlier HuskyLens, Arduino Nano, front-ultrasonic, or previous Pixy experiments remain available as engineering history without becoming misleading reconstruction instructions.

The final principle is:

> **A robot is reproducible when another engineer can understand not only what was built, but how it was configured, why it behaves that way, how it was calibrated, and how to verify that the reconstructed system is actually operating under the same assumptions.**

PiolínTech therefore treats reproducibility as part of the engineering design itself rather than as documentation added only after the robot is finished.

---

<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
