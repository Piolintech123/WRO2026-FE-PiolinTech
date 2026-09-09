# Legacy Documentation Notice

<div align="center">

<img
  src="../../v-photos/v4/piolin_open_isometric.jpg"
  alt="Current Piolín Open Challenge configuration"
  width="700"
/>

<br>

<sub><b>Figure L0.1.</b> Current Piolín Open Challenge configuration. The Gyro Sensor occupies S1 while S2, S3, and S4 retain their permanent assignments.</sub>

</div>

The files inside `docs/legacy/` document **earlier Piolín prototypes, experiments, abandoned architectures, and engineering decisions that are no longer part of the current WRO Future Engineers 2026 competition vehicle**.

They are intentionally preserved because unsuccessful or replaced approaches are still valuable engineering evidence.

However, they must **not** be interpreted as current assembly, wiring, calibration, or software instructions.

> [!IMPORTANT]
> When information in `docs/legacy/` conflicts with the current documentation, the current documentation takes priority.

---

## L0.1 Current Piolín Architecture

Piolín currently uses one common LEGO Mindstorms EV3 vehicle platform for both competition rounds.

The permanent hardware assignments are:

```text
Motor A
→ LEGO EV3 Large Motor
→ rear propulsion


Motor B
→ LEGO EV3 Medium Motor
→ Ackermann-style steering


S2
→ LEFT Ultrasonic Sensor


S3
→ RIGHT Ultrasonic Sensor


S4
→ downward-facing Color Sensor
````

Sensor Port S1 changes according to the challenge.

### Open Challenge

```text
S1
→ LEGO EV3 Gyro Sensor
```

### Obstacle Challenge

```text
S1
→ Pixy2.1
```

The Gyro Sensor and Pixy2.1 are **not installed simultaneously** in the current architecture.

---

## L0.2 Current Open Challenge Configuration

During Open, Piolín uses:

```text
A  = Large Motor / propulsion

B  = Medium Motor / steering

S1 = Gyro Sensor

S2 = LEFT Ultrasonic

S3 = RIGHT Ultrasonic

S4 = Color Sensor
```

The two lateral ultrasonic sensors provide track-relative geometry.

The Gyro Sensor provides rotational information.

The Color Sensor provides course-state information such as Blue and Orange floor events.

The current navigation philosophy is therefore based on complementary measurements:

```text
Ultrasonics
→ lateral geometry


Gyro
→ orientation


Color
→ course state
```

A permanent front ultrasonic sensor is **not part of the current Open architecture**.

---

## L0.3 Current Obstacle Challenge Configuration

<div align="center">

<img
src="../../v-photos/v4/piolin_obstacle_isometric.jpg"
alt="Current Piolín Obstacle Challenge configuration"
width="700"
/>

<br>

<sub><b>Figure L0.2.</b> Current Piolín Obstacle Challenge configuration with Pixy2.1 replacing the Gyro Sensor on S1.</sub>

</div>

During Obstacles, Piolín uses:

```text
A  = Large Motor / propulsion

B  = Medium Motor / steering

S1 = Pixy2.1

S2 = LEFT Ultrasonic

S3 = RIGHT Ultrasonic

S4 = Color Sensor
```

The Gyro Sensor is not installed in this configuration.

Pixy2.1 provides visual information about colored targets, while the lateral ultrasonic sensors continue providing physical track context.

The current Pixy signature convention is:

```text
SIG 1
→ PINK
→ parking reference


SIG 2
→ RED
→ pass RIGHT


SIG 3
→ GREEN
→ pass LEFT
```

These signatures must not be confused with older HuskyLens IDs.

---

# L0.4 Systems Considered Legacy

The following components and architectures belong to previous stages of Piolín's development and are **not part of the current competition baseline**:

```text
HuskyLens

Arduino Nano vision bridge

HuskyLens → Nano → USB → EV3 communication

permanent front ultrasonic sensor

three-ultrasonic configurations

older diagonal ultrasonic arrangements

older Pixy experiments

gyro-free Open architectures

older sensor-port assignments

older steering and navigation parameters
```

These systems may appear in:

```text
legacy documentation

old source code

test logs

historical photos

development notes
```

but they should not be copied directly into the current robot.

---

# L0.5 The HuskyLens + Arduino Nano Stage

One of Piolín's most important legacy systems used:

```text
HuskyLens
    ↓ I2C
Arduino Nano
    ↓ USB Serial
EV3
```

The Nano acted as a communication bridge.

The historical HuskyLens identification used:

```text
ID 1
→ GREEN


ID 2
→ RED
```

This architecture was useful because it demonstrated that external visual perception could be integrated with the EV3.

It also exposed several important engineering problems, including:

```text
false detections

lighting sensitivity

intermittent detections

limited field of view

target-loss ambiguity

target management

communication complexity

controller conflicts
```

These lessons influenced the design of the current Pixy2.1 system.

The historical system is documented in:

[HuskyLens Legacy Documentation](01_HuskyLens.md)

---

# L0.6 Why the HuskyLens System Was Replaced

The HuskyLens was not removed because it was completely incapable of recognizing colored targets.

The problem was the complete autonomous system around it.

A detection had to pass through:

```text
target
  ↓
HuskyLens
  ↓
I2C
  ↓
Arduino Nano
  ↓
formatted data
  ↓
USB
  ↓
EV3
  ↓
parser
  ↓
navigation state
  ↓
steering
```

Each additional stage created another possible source of failure.

The current Pixy2.1 architecture reduces that communication chain:

```text
Pixy2.1
   ↓
EV3
```

This reduced integration complexity while preserving the visual information required for obstacle navigation.

---

# L0.7 Legacy Ultrasonic Configurations

Piolín also experimented with different ultrasonic arrangements.

These included:

```text
frontal ultrasonic sensing

three-ultrasonic configurations

different side-sensor orientations

earlier diagonal mounting concepts
```

The current architecture instead uses exactly:

```text
S2 = LEFT lateral Ultrasonic

S3 = RIGHT lateral Ultrasonic
```

in both rounds.

The two sensors remain physically LEFT and RIGHT.

Software may later interpret them as:

```text
INNER

OUTER
```

depending on course direction.

Historical code using different port assignments should therefore not be used as the current wiring reference.

---

# L0.8 Legacy Gyro Decisions

The role of the Gyro Sensor changed several times during development.

At one stage, Piolín explored navigation without a gyro and attempted to infer most track behavior through wall geometry.

That work showed that lateral ultrasonic sensing could provide valuable environmental information.

However, wall distance and vehicle orientation are not the same physical quantity.

The current Open architecture therefore combines:

```text
two lateral ultrasonics
+
gyro
```

instead of choosing only one of them.

The gyro-free stage remains useful engineering history, but it is not the current Open configuration.

---

# L0.9 Legacy Front Ultrasonic Sensor

Earlier designs also used or considered a front ultrasonic sensor.

That sensor provided direct frontal distance information, but EV3 sensor-port availability created a systems-level trade-off.

The current architecture reserves S1 for:

```text
Gyro
during Open
```

or:

```text
Pixy2.1
during Obstacles
```

because those sensors provide information that cannot be reproduced as effectively by the permanent lateral sensors.

The final current robot therefore does not include a permanent front ultrasonic sensor.

---

# L0.10 Historical Parameters Are Not Current Specifications

Legacy software may contain values for:

```text
motor speeds

steering limits

turn timing

wall distances

ultrasonic thresholds

camera thresholds

sensor orientation

parking movement

vehicle dimensions
```

These values belong to the physical robot and software version on which they were tested.

Piolín has changed mechanically and electronically during development.

Therefore:

> **A historical parameter should not automatically be reused as a current calibration value.**

The current V4 robot should be physically measured and calibrated independently.

---

# L0.11 Physical Measurements

Older measurements for:

```text
robot length

robot width

robot height

vehicle mass

wheel diameter

wheelbase

track width

sensor offsets
```

must not automatically be presented as current specifications.

The current competition robot should be remeasured before final numerical values are published.

Until then, the current documentation should explicitly identify those measurements as pending rather than using precise but outdated values.

---

# L0.12 Purpose of Keeping Legacy Documentation

Legacy documentation is preserved for three main reasons.

### Engineering traceability

It explains how Piolín reached its current architecture.

### Failure analysis

It records problems that influenced later design decisions.

### Reproducibility of the development process

A reader can understand not only:

```text
what Piolín uses now
```

but also:

```text
what was tested

what failed

what was changed

why the current system was selected
```

This is particularly important in an engineering project because the final robot alone does not show the complete design process.

---

# L0.13 How Legacy Information Should Be Read

A legacy file should be interpreted as:

```text
HISTORICAL CONFIGURATION
        ↓
OBSERVED PROBLEM
        ↓
TEST / ANALYSIS
        ↓
ENGINEERING LESSON
        ↓
CURRENT DESIGN DECISION
```

It should **not** be interpreted as:

```text
current assembly instructions
```

or:

```text
current wiring instructions
```

unless the same information is independently confirmed in the current documentation.

---

# L0.14 Current vs. Legacy Summary

| System                | Current Architecture | Legacy / Previous Development                    |
| :-------------------- | :------------------- | :----------------------------------------------- |
| Main controller       | EV3                  | EV3 remained central                             |
| Propulsion            | Large Motor on A     | Earlier tuning and mechanical versions           |
| Steering              | Medium Motor on B    | Earlier steering configurations                  |
| Left distance sensor  | S2 LEFT Ultrasonic   | Previous assignments/orientations                |
| Right distance sensor | S3 RIGHT Ultrasonic  | Previous assignments/orientations                |
| Floor sensor          | S4 Color Sensor      | Earlier calibration methods                      |
| Open S1               | Gyro Sensor          | Gyro-free and earlier gyro strategies            |
| Obstacle S1           | Pixy2.1              | HuskyLens, Nano bridge, earlier Pixy experiments |
| Front ultrasonic      | Not installed        | Experimental / previous                          |
| Arduino Nano          | Not installed        | HuskyLens communication bridge                   |
| HuskyLens             | Not installed        | Previous obstacle-vision system                  |
| Gyro in Obstacles     | Not installed        | Not current                                      |
| Pixy in Open          | Not installed        | Not current                                      |

This table should be used as a quick reference whenever older files are being reviewed.

---

# L0.15 Legacy Documentation Structure

The current legacy section contains:

```text
docs/legacy/

00_LEGACY_NOTICE.md

01_HuskyLens.md

02_PTesting&Analysis.md
```

`00_LEGACY_NOTICE.md` establishes which architecture is current and which information should be treated as historical.

`01_HuskyLens.md` documents the previous HuskyLens + Arduino Nano perception architecture and the engineering lessons learned from it.

`02_PTesting&Analysis.md` records prototype testing, failure analysis, and the development methodology used to identify problems before the final architecture stabilized.

The goal is to preserve useful engineering history without allowing it to become confused with current reconstruction instructions.

---

# L0.16 Final Legacy Principle

Piolín's legacy documentation demonstrates that removing a component or abandoning a strategy does not mean that the experiment had no value.

Several current design decisions came directly from earlier failures.

The evolution can be summarized as:

```text
PROTOTYPE
    ↓
TEST
    ↓
FAILURE OR LIMITATION
    ↓
ANALYSIS
    ↓
DESIGN CHANGE
    ↓
CURRENT ARCHITECTURE
```

The current baseline is:

```text
OPEN

S1 = Gyro
S2 = LEFT Ultrasonic
S3 = RIGHT Ultrasonic
S4 = Color
```

and:

```text
OBSTACLES

S1 = Pixy2.1
S2 = LEFT Ultrasonic
S3 = RIGHT Ultrasonic
S4 = Color
```

Everything else in the Legacy section exists to explain how PiolínTech arrived at that architecture.

The central principle is:

> **Legacy documentation preserves engineering evidence, but current documentation defines the robot that should actually be reconstructed and used.**

---

<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
Aquí los diagramas no añaden suficiente valor: el aviso debe ser **rápido de entender y muy claro sobre current vs. legacy**. Los diagramas históricos específicos pertenecen, si realmente hacen falta, dentro de `01_HuskyLens.md` o `02_PTesting&Analysis.md`.
