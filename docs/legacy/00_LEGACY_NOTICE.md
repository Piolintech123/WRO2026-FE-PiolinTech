# 00. Legacy Documentation Notice

> [!IMPORTANT]
> The files inside `docs/legacy/` document **historical Piolín prototypes, experiments, abandoned architectures, and earlier development stages**.
>
> They are preserved intentionally as engineering evidence, but they **do not describe the current WRO Future Engineers 2026 competition configuration** and should not be used as current wiring, calibration, software, or reconstruction instructions.

Piolín changed substantially during development. Several sensing architectures, camera systems, port assignments, control strategies, and supporting electronics were tested before the current design was selected.

Rather than deleting those earlier approaches, PiolínTech preserves them inside the `legacy` section because they provide useful evidence of the engineering process. They show what was attempted, what problems appeared, which trade-offs were identified, and why the current architecture was eventually preferred.

However, historical documentation creates a risk if it is read without context. An older file may correctly describe Piolín **at the time it was written** while being technically incorrect for the current robot.

This notice establishes the distinction between:

```text
HISTORICAL ENGINEERING EVIDENCE
```

and:

```text
CURRENT COMPETITION DOCUMENTATION
```

throughout the repository.

---

## 1. What "Legacy" Means in This Repository

A legacy component, program, diagram, or document is something that was genuinely part of Piolín's development but is **not part of the current competition architecture**.

Legacy does not mean:

```text
wrong

useless

failed in every way

deleted from engineering history
```

It means:

```text
not current
```

A previous design may have worked successfully enough to provide valuable information while still being replaced later because another architecture offered:

```text
simpler integration

fewer failure points

better sensing information

more useful EV3 port allocation

better reproducibility

better competition suitability
```

Preserving these stages allows the repository to demonstrate engineering progression rather than presenting the final robot as if it appeared fully developed from the beginning.

---

## 2. Current Piolín Architecture Takes Priority

Whenever a legacy document conflicts with current documentation, the **current documentation takes priority**.

The present Piolín architecture is based on one common EV3 vehicle platform with two round-specific S1 configurations.

The common hardware is:

```text
Main Controller
→ LEGO Mindstorms EV3


Battery
→ LEGO Mindstorms EV3 Rechargeable DC Battery 45501


Motor A
→ LEGO EV3 Large Motor
→ rear propulsion


Motor B
→ LEGO EV3 Medium Motor
→ Ackermann steering


S2
→ LEFT EV3 Ultrasonic Sensor


S3
→ RIGHT EV3 Ultrasonic Sensor


S4
→ EV3 Color Sensor
```

S1 changes according to the competition round.

---

## 3. Current Open Challenge Configuration

The current Open Challenge uses:

```text
A  → Large Motor / propulsion

B  → Medium Motor / steering


S1 → EV3 Gyro Sensor

S2 → LEFT Ultrasonic Sensor

S3 → RIGHT Ultrasonic Sensor

S4 → Color Sensor
```

<div align="center">

<img
  src="../../v-photos/v4/piolin_open_isometric.jpg"
  alt="Current Piolín Open Challenge configuration"
  width="720"
/>

<br>

<sub><b>Figure L.1.</b> Current Piolín Open Challenge configuration. The Gyro Sensor occupies S1 while the two lateral ultrasonic sensors remain on S2 and S3.</sub>

</div>

The current Open software development path uses **Pybricks MicroPython**.

The Open navigation architecture combines:

```text
lateral ultrasonic geometry

gyro-based orientation

floor-color course landmarks

Ackermann steering

rear propulsion
```

The Gyro Sensor is therefore a **current Open component**.

Any legacy document describing Piolín as permanently gyro-free should be interpreted only as evidence from an earlier development stage.

---

## 4. Current Obstacle Challenge Configuration

The current Obstacle Challenge uses the same motors, controller, battery, ultrasonic sensors, Color Sensor, chassis, drivetrain, and steering architecture.

Only S1 changes:

```text
A  → Large Motor / propulsion

B  → Medium Motor / steering


S1 → Pixy2.1

S2 → LEFT Ultrasonic Sensor

S3 → RIGHT Ultrasonic Sensor

S4 → Color Sensor
```

<div align="center">

<img
  src="../../v-photos/v4/piolin_obstacle_isometric.jpg"
  alt="Current Piolín Obstacle Challenge configuration"
  width="720"
/>

<br>

<sub><b>Figure L.2.</b> Current Piolín Obstacle Challenge configuration with Pixy2.1 replacing the Gyro Sensor on S1.</sub>

</div>

The current obstacle-development environment uses an **ev3dev2 and SMBus/I2C-oriented software path** for direct Pixy communication.

The Gyro Sensor is not installed during this configuration.

The current vision architecture is:

```text
Pixy2.1
   ↓
S1
   ↓
EV3
```

rather than the previous HuskyLens–Arduino Nano communication system.

---

## 5. The Current S1 Modular Architecture

The distinction between Open and Obstacles is intentional.

```text
                        EV3 S1
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼
           OPEN                      OBSTACLES
             │                           │
             ▼                           ▼
        Gyro Sensor                  Pixy2.1
```

<div align="center">

<img
  src="../../embed/s1_modular_architecture.png"
  alt="Current Piolín modular S1 architecture"
  width="800"
/>

<br>

<sub><b>Figure L.3.</b> Current S1 architecture. Gyro and Pixy2.1 are round-specific devices and are not installed simultaneously.</sub>

</div>

This is one of the most important facts to keep in mind when reading older Piolín documentation.

Several historical configurations attempted to keep different sensor combinations active simultaneously. The current architecture instead assigns S1 to the sensor that provides the most useful information for the active competition round.

---

# 6. Major Historical Architectures

Several important architectures appear in legacy documentation.

They should be understood as engineering stages rather than current instructions.

---

## 6.1 HuskyLens + Arduino Nano Vision Architecture

One of the major previous obstacle-perception systems used a HuskyLens camera together with an Arduino Nano.

The communication architecture was approximately:

```text
HuskyLens
    ↓
Arduino Nano
    ↓
USB
    ↓
EV3
```

<div align="center">

<img
  src="../../embed/legacy_huskylens_nano_architecture.png"
  alt="Legacy HuskyLens and Arduino Nano architecture"
  width="850"
/>

<br>

<sub><b>Figure L.4.</b> Historical HuskyLens–Nano vision architecture. This system belongs to the engineering history and is not part of the current competition robot.</sub>

</div>

This approach was valuable during development because it demonstrated that Piolín could receive external visual information even when direct EV3-camera integration was difficult.

However, it introduced several additional layers:

```text
camera configuration

camera-to-Nano communication

Nano firmware

Nano-to-EV3 communication

USB interface

EV3 parsing
```

The current Pixy2.1 architecture eliminates the intermediate Nano.

Therefore:

```text
HuskyLens
→ LEGACY


Arduino Nano
→ LEGACY
```

Neither component should appear in the current Bill of Materials, current wiring diagrams, or current reproduction procedure.

---

## 6.2 Earlier Pixy Architectures

Pixy technology also appeared during earlier development phases.

Those experiments should not automatically be confused with the **current Pixy2.1 direct-S1 architecture**.

Earlier Pixy documentation may describe:

```text
different connection methods

different software interfaces

different sensor combinations

different obstacle strategies

prototype testing outside the final architecture
```

<div align="center">

<img
  src="../../embed/legacy_pixy_old_architecture.png"
  alt="Earlier Piolín Pixy architecture"
  width="850"
/>

<br>

<sub><b>Figure L.5.</b> Earlier Pixy development architecture. Historical Pixy experiments are separated from the current direct Pixy2.1 integration.</sub>

</div>

The important distinction is:

```text
OLD PIXY APPROACH
→ legacy
```

versus:

```text
CURRENT PIXY2.1
→ active Obstacle Challenge vision system
```

A component can therefore appear in both historical and current engineering documentation if the **architecture surrounding it changed substantially**.

---

## 6.3 Earlier Gyro Approaches

The Gyro Sensor has also changed roles throughout Piolín's development.

Some earlier designs:

```text
used gyro

removed gyro

replaced gyro with camera hardware

attempted navigation without gyro
```

Because the current Open architecture uses the Gyro Sensor again, older documents describing gyro removal should not be interpreted as the final design.

<div align="center">

<img
  src="../../embed/legacy_gyro_navigation.png"
  alt="Legacy Piolín gyro navigation approaches"
  width="850"
/>

<br>

<sub><b>Figure L.6.</b> Earlier gyro-navigation approaches preserved as engineering history. Gyro use itself is not legacy; the specific older implementations are.</sub>

</div>

This distinction is especially important:

> **The Gyro Sensor is current hardware during Open. Only the previous gyro strategies and configurations are legacy.**

---

# 7. Legacy Ultrasonic Architectures

Piolín's ultrasonic system changed several times.

Historical versions included combinations such as:

```text
three ultrasonic sensors

front ultrasonic sensor

diagonal ultrasonic orientations

different S2/S3 assignments
```

The current physical architecture contains exactly:

```text
S2 = LEFT lateral ultrasonic

S3 = RIGHT lateral ultrasonic
```

and:

```text
NO permanent front ultrasonic
```

<div align="center">

<img
  src="../../embed/evolution_sensor_architecture.png"
  alt="Evolution of Piolín sensor architecture"
  width="880"
/>

<br>

<sub><b>Figure L.7.</b> Piolín's sensing architecture evolved through several experimental layouts before reaching the current two-lateral-sensor and modular-S1 configuration.</sub>

</div>

Any legacy code or diagram that defines:

```text
S2 = RIGHT

S3 = LEFT
```

is not current.

The current convention is always:

```text
S2 = LEFT

S3 = RIGHT
```

This physical mapping does not change with course direction.

The software later assigns:

```text
INNER
```

and:

```text
OUTER
```

according to clockwise or counterclockwise travel.

---

# 8. Legacy Front Ultrasonic Sensor

Several previous versions used a front-facing ultrasonic sensor.

That sensor provided useful frontal-clearance information, but it consumed a sensor port that became more valuable for other round-specific sensing.

The final trade-off became:

```text
permanent front ultrasonic
```

versus:

```text
Gyro during Open
+
Pixy2.1 during Obstacles
```

The current architecture selected the second option.

Therefore:

```text
FRONT ULTRASONIC
→ legacy / experimental
→ not installed in final current architecture
```

Legacy documents may still discuss frontal safety logic because it was genuinely tested.

Those discussions should be interpreted as part of the design process rather than instructions for the present robot.

---

# 9. Legacy Power and Interface Hardware

Earlier development also used or considered additional electrical hardware.

Depending on the specific prototype, legacy files may mention:

```text
Arduino Nano

USB communication

jumper wires

external interface wiring

buck converters

external power concepts
```

These components are not part of the current competition electrical architecture.

The current power system is centered on:

```text
EV3 Rechargeable Battery 45501
        ↓
EV3
        ↓
current motors and sensors
```

No permanent external battery or permanent buck-converter subsystem is part of the current competition robot.

Historical electrical components should therefore remain within legacy documentation unless they are explicitly reintroduced and verified in the current architecture.

---

# 10. Legacy Software Does Not Define Current Hardware

Old source code is valuable because it shows how Piolín's control logic evolved.

However, software can contain assumptions about hardware that no longer exist.

Examples include:

```text
different motor ports

different ultrasonic assignments

front ultrasonic input

HuskyLens serial data

Arduino communication

no gyro

old camera protocols
```

Therefore, an old program should not be used to determine current wiring simply because the program once worked.

The current hardware documentation defines the current robot.

Legacy code defines the robot configuration for which that code was originally developed.

---

## 10.1 Current Software Separation

The current architecture benefits from keeping the round programs logically separate.

Conceptually:

```text
Open Challenge
      ↓
Pybricks
      ↓
S1 Gyro
```

and:

```text
Obstacle Challenge
      ↓
ev3dev2 / SMBus
      ↓
S1 Pixy2.1
```

Trying to interpret an older combined or experimental program as the final architecture can therefore produce incorrect conclusions about the current robot.

---

# 11. Legacy Dimensions and Mechanical Measurements

Historical Piolín documentation may include numerical dimensions such as:

```text
overall length

overall width

height

mass

wheel diameter

wheelbase

track width

sensor offsets
```

Those measurements may have been correct for the physical robot at the time.

However, Piolín has undergone:

```text
chassis modifications

wheel changes

camera changes

sensor repositioning

steering reinforcement
```

Therefore old dimensions should not be copied into current V4 specifications without remeasurement.

This applies especially to previously documented values for:

```text
wheel diameter

vehicle mass

wheelbase

overall dimensions
```

The current repository should only present a numerical value as final when it has been physically verified on the current robot.

---

# 12. Legacy Calibration Values

The same rule applies to calibration.

Historical files may contain values for:

```text
wall distance targets

steering limits

color thresholds

turn duration

corner thresholds

sensor offsets

camera coordinates

PID / PD gains

speed values
```

A calibration constant is valid only for the system on which it was tested.

Changes in:

```text
sensor position

wheel geometry

steering linkage

software environment

camera mount

battery condition

vehicle speed
```

can change the correct value.

Legacy calibration values should therefore be treated as:

```text
historical reference
```

rather than:

```text
current final calibration
```

unless they are explicitly revalidated.

---

# 13. Why Legacy Documentation Is Preserved

Removing every unsuccessful or outdated design would make the repository cleaner, but it would also remove much of the engineering story.

A final robot alone cannot show:

```text
what alternatives were considered

what problems were discovered

which trade-offs were evaluated

why components were removed

why a previous idea was revisited

how the architecture became simpler
```

Legacy documentation provides that evidence.

For example, the current direct Pixy2.1 architecture is easier to understand when compared with the previous:

```text
HuskyLens
→ Nano
→ USB
→ EV3
```

system.

Likewise, the importance of modular S1 becomes clearer when compared with architectures that attempted to use a permanent frontal sensor or other combinations.

---

# 14. Engineering Iteration Is Not Contradiction

A repository containing multiple architectures can appear contradictory if the development timeline is not explained.

In reality, changing an engineering decision after testing is expected.

A typical process is:

```text
DESIGN A
    ↓
BUILD
    ↓
TEST
    ↓
LIMITATION DISCOVERED
    ↓
DESIGN B
    ↓
TEST
    ↓
NEW INFORMATION
    ↓
DESIGN C
```

<div align="center">

<img
  src="../../embed/evolution_vision_system.png"
  alt="Evolution of Piolín vision architecture"
  width="880"
/>

<br>

<sub><b>Figure L.8.</b> Vision-system evolution demonstrates how several valid prototypes contributed information before the current architecture was selected.</sub>

</div>

An older design being replaced does not mean its documentation is inaccurate historical evidence.

It simply means it is no longer the current solution.

---

# 15. How to Read Legacy Files

When reading any file inside `docs/legacy/`, the reader should ask four questions.

```text
1. Which Piolín version or development stage does this describe?

2. Which hardware configuration was installed at that time?

3. What problem was the team attempting to solve?

4. Which conclusions remained relevant to the current robot?
```

The reader should **not** assume:

```text
old port mapping
=
current port mapping
```

or:

```text
old calibration
=
current calibration
```

or:

```text
old component
=
current component
```

without confirmation from the current documentation.

---

# 16. Current vs. Legacy Summary

| Subsystem | Current | Legacy / Historical |
| :--- | :--- | :--- |
| Main controller | EV3 | EV3 remained central through development |
| Drive motor | Large Motor on A | Earlier software mappings may differ |
| Steering motor | Medium Motor on B | Earlier mappings/strategies may differ |
| Left ultrasonic | S2 LEFT | Old mappings may show different side |
| Right ultrasonic | S3 RIGHT | Old mappings may show different side |
| Front ultrasonic | Not installed | Earlier 3-US architectures |
| Open S1 | Gyro | Older gyro implementations or gyro-free periods |
| Obstacle S1 | Pixy2.1 | HuskyLens/Nano and earlier Pixy approaches |
| Color Sensor | S4 | Earlier threshold/event logic |
| Vision bridge | Direct Pixy2.1 → EV3 | HuskyLens → Nano → USB → EV3 |
| Arduino Nano | Not current | Legacy |
| HuskyLens | Not current | Legacy |
| External battery | Not current | Experimental concepts if documented |
| Permanent buck converter | Not current | Experimental concepts if documented |
| Open software | Pybricks path | Earlier ev3dev2/experimental code |
| Obstacle software | ev3dev2/SMBus Pixy path | Husky/Nano and earlier camera code |

This table should be used as a quick reference when historical and current material appear together.

---

# 17. Current Reconstruction Rule

Anyone attempting to reproduce the current Piolín robot should use the following rule:

> **Never reconstruct the current robot from a legacy file unless the same information is confirmed in the current documentation.**

The current reconstruction baseline is:

```text
EV3
+
Battery 45501
+
Large Motor A
+
Medium Motor B
+
S2 Left Ultrasonic
+
S3 Right Ultrasonic
+
S4 Color Sensor
```

with:

```text
OPEN
S1 = Gyro
```

or:

```text
OBSTACLES
S1 = Pixy2.1
```

All other sensor combinations should be considered historical unless explicitly identified as current elsewhere in the repository.

---

# 18. Recommended Legacy Organization

The legacy section should separate fundamentally different historical systems instead of placing every old experiment into one undifferentiated folder.

A useful structure is:

```text
docs/
└── legacy/
    ├── 00_LEGACY_NOTICE.md
    │
    ├── 01_GConfig.md
    ├── 02_CameraPixy_old.md
    ├── 03_PTesting&Analysis.md
    │
    └── huskylens_nano/
        ├── 01_HuskyLensOverview.md
        ├── 02_NanoArchitecture.md
        └── 03_HuskyLensTesting.md
```

The names of the individual historical files can evolve as documentation is reorganized, but the conceptual separation should remain clear.

For example:

```text
CURRENT PIXY2.1
```

should never be mixed with:

```text
OLD PIXY EXPERIMENTS
```

simply because both use a Pixy camera.

Similarly:

```text
CURRENT OPEN GYRO
```

should remain distinct from:

```text
OLD GYRO CONTROL APPROACHES
```

---

# 19. Legacy Evidence Should Remain Authentic

Historical documentation should not be rewritten to pretend that the team knew the final solution from the beginning.

If an older prototype genuinely used:

```text
three ultrasonics
```

the legacy file should say so.

If the team genuinely attempted:

```text
HuskyLens + Nano
```

that architecture should remain documented.

If a historical approach produced problems, those problems should also be retained.

The purpose of the legacy section is not to make every old design appear successful.

Its purpose is to preserve the actual engineering process.

---

# 20. Legacy Images and Diagrams

Historical photographs and diagrams should remain clearly separated from current V4 evidence.

Current robot photographs are stored under the current V4 image set, while historical evidence should retain its original context or be identified as legacy.

A useful rule is:

```text
CURRENT V4 PHOTO
→ evidence of current hardware


LEGACY PHOTO
→ evidence of historical development
```

A historical photograph should never be used as evidence for a current port assignment, camera connection, or sensor configuration unless the current robot independently confirms the same arrangement.

---

# 21. Legacy Code

Historical source code should also remain available when it provides useful engineering context.

Legacy code can demonstrate:

```text
previous wall-following methods

old corner strategies

camera experiments

sensor filtering

failed or partially successful approaches
```

However, it should be labeled so that a reader does not accidentally deploy it on the current hardware expecting the current architecture.

When practical, legacy code documentation should identify:

```text
expected hardware

expected port mapping

software environment

historical purpose
```

This makes the code educational without making it misleading.

---

# 22. Why Failed Approaches Are Valuable

A failed experiment can provide more engineering information than an untested idea.

For example, a prototype may reveal:

```text
camera field-of-view limitation

communication instability

sensor noise

mechanical interference

port-allocation conflict

control oscillation
```

That observation can directly influence the next design.

The engineering value therefore comes from the complete sequence:

```text
hypothesis
→ implementation
→ observation
→ interpretation
→ redesign
```

rather than only from whether the prototype completed the competition course.

---

# 23. Current Architecture as the Result of Iteration

The current architecture is not simply a collection of the newest components.

It represents lessons learned from earlier systems.

The current design keeps:

```text
EV3-centered control

two lateral ultrasonic references

downward Color Sensor

Large Motor propulsion

Medium Motor Ackermann steering
```

while introducing a deliberate round-specific choice:

```text
Gyro for Open

Pixy2.1 for Obstacles
```

and removing unnecessary layers such as:

```text
front ultrasonic

HuskyLens

Arduino Nano

additional interface wiring
```

The result is a smaller number of active subsystems with clearer responsibilities.

---

# 24. Legacy Documentation Principle

PiolínTech preserves legacy documentation according to one guiding principle:

> **Previous engineering decisions should remain visible as evidence of development, but they must never be allowed to obscure the definition of the current robot.**

The repository therefore separates:

```text
WHAT WE TRIED
```

from:

```text
WHAT PIOLÍN USES NOW
```

Both are important.

The first demonstrates the engineering process.

The second provides reproducible competition documentation.

<div align="center">

<img
  src="../../v-photos/v4/piolin_open_top.jpg"
  alt="Current Piolín Open architecture top view"
  width="700"
/>

<br>

<sub><b>Figure L.9.</b> Current Open hardware should always be verified against present documentation rather than inferred from a historical prototype.</sub>

</div>

<div align="center">

<img
  src="../../v-photos/v4/piolin_obstacle_top.jpg"
  alt="Current Piolín Obstacle architecture top view"
  width="700"
/>

<br>

<sub><b>Figure L.10.</b> Current Obstacle hardware with Pixy2.1 on S1. Legacy camera configurations are preserved separately and are not current reconstruction references.</sub>

</div>

This separation allows the repository to remain both technically accurate and historically complete.

---

<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
