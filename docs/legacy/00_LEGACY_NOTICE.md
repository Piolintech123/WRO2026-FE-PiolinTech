# Legacy Documentation Notice

This directory contains **historical documentation from previous Piolín configurations, experiments, prototypes, and development stages**.

The files preserved inside `docs/legacy/` are part of the engineering history of the PiolínTech WRO Future Engineers 2026 project. They help explain how the robot evolved, which alternatives were explored, and why some components or strategies were eventually replaced.

They do **not** represent the current robot configuration.

> [!WARNING]
> **Do not use the files inside this directory as the primary reference for building, wiring, programming, or reproducing the current Piolín robot.**
>
> If information in a legacy document conflicts with the current documentation, the **current documentation takes priority**.

---

## Current Documentation

Use these sections for the current Piolín architecture:

[Current Hardware](../components/)  
[Mobility and Mechanical Design](../mobility_mechanical/)  
[Power and Sensors](../power_sensors/)  
[Software and Obstacle Strategy](../software_obstacles_strategy/)  
[Systems Engineering](../systems_engineering/)  
[Reproducibility](../reproducibility/)

---

# 1. Why This Directory Exists

Piolín was developed through several hardware and software iterations before reaching its current WRO Future Engineers 2026 architecture.

The development process was not:

```text
First Design
    ↓
Final Robot
```

Instead, it followed a repeated engineering cycle:

```text
Concept
   ↓
Prototype
   ↓
Implementation
   ↓
Observation
   ↓
Problem Identification
   ↓
Modification
   ↓
New Version
```

Different versions of Piolín explored different sensors, cameras, control strategies, mechanical arrangements, and electrical configurations.

Some systems worked but were later replaced by approaches that integrated better with the complete robot. Others were useful mainly because they exposed problems that influenced the next design.

Instead of deleting those files, they are preserved here as evidence of the engineering process.

---

# 2. Legacy Documentation vs. Current Documentation

A legacy document is not necessarily incorrect.

It may accurately describe a version of Piolín that existed earlier in the project.

The important distinction is:

```text
LEGACY DOCUMENTATION
        ↓
Describes a previous Piolín configuration


CURRENT DOCUMENTATION
        ↓
Describes the current Piolín configuration
```

For example, an older document may describe a gyroscope connected to an EV3 sensor port.

That may have been correct for that specific development stage.

However, it should not be used to reproduce the current robot because the final Piolín configuration no longer uses a gyroscope.

The same principle applies to previous camera systems, ultrasonic arrangements, wiring diagrams, dimensions, software logic, and navigation strategies.

---

# 3. Current Piolín Hardware Reference

The current Piolín architecture uses the **LEGO Mindstorms EV3 as the main controller**.

The final EV3 port assignment is:

| EV3 Interface | Current Component | Main Responsibility |
| :--- | :--- | :--- |
| **Motor Port A** | Drive Motor | Rear propulsion |
| **Motor Port B** | Steering Motor | Ackermann-style steering |
| **Sensor Port S1** | Front Ultrasonic Sensor | Frontal safety |
| **Sensor Port S2** | Right Ultrasonic Sensor | Right-wall geometry |
| **Sensor Port S3** | Left Ultrasonic Sensor | Left-wall geometry |
| **Sensor Port S4** | LEGO Color Sensor | Floor-marking detection |
| **USB** | Arduino Nano | Vision communication |

The current architecture can be summarized as:

```text
                         LEGO EV3
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
       ACTUATION          SENSING          PROCESSING
          │                 │                 │
          ▼                 ▼                 ▼
     Motor A + B          S1–S4              EV3
                                              ▲
                                              │
                                             USB
                                              │
                                       Arduino Nano
                                              ▲
                                              │
                                          HuskyLens
```

The EV3 remains responsible for the final vehicle-control decisions.

For detailed current hardware documentation, see:

[Hardware Overview](../components/01_Hardwareoverview.md)  
[LEGO EV3](../components/02_EV3.md)  
[Motors](../components/03_Motors.md)  
[Steering System](../components/04_SteeringMotor.md)  
[Ultrasonic Sensors](../components/05_UltrasonicSensors.md)  
[Color Sensor](../components/06_ColorSensor.md)  
[HuskyLens](../components/07_HuskyLens.md)  
[Battery](../components/08_Battery.md)  
[Power Distribution](../components/09_PowerDistribution.md)  
[Other Components](../components/10_OtherComponents.md)

---

# 4. Current Vision Architecture

The current obstacle-recognition system uses a **HuskyLens** together with an **Arduino Nano**.

The confirmed communication architecture is:

```text
HUSKYLENS
     ↓
ARDUINO NANO
     ↓
USB
     ↓
LEGO EV3
```

The Arduino Nano is not Piolín's main controller.

Its purpose is to support the vision communication subsystem.

The LEGO EV3 remains responsible for:

```text
Propulsion control

Steering control

Ultrasonic navigation

Color-sensor interpretation

Navigation state

Safety behavior

Obstacle-response decisions
```

Current vision documentation:

[HuskyLens Component Documentation](../components/07_HuskyLens.md)

---

# 5. Previous PixyCam System

Piolín previously used a **PixyCam-based vision concept**.

This system is no longer part of the current robot.

The development progression was:

```text
PixyCam
   ↓
Previous Vision Architecture
   ↓
Development and Evaluation
   ↓
Vision Architecture Changed
   ↓
HuskyLens + Arduino Nano
   ↓
Current Vision System
```

The PixyCam files are preserved because they show an important part of Piolín's visual-perception development.

They should be interpreted as engineering history rather than current build instructions.

[Legacy PixyCam Documentation](02_CameraPixy.md)

For the current system, use:

[Current HuskyLens Documentation](../components/07_HuskyLens.md)

---

# 6. Previous Gyroscope Configuration

A LEGO gyroscope was also used during earlier stages of Piolín's development.

Legacy files may therefore contain references to:

```text
Gyro angle

Heading correction

Gyro initialization

Angle-based turns

Gyro reset

Gyro-dependent navigation
```

The current Piolín architecture does **not** use the gyroscope.

The current EV3 sensor configuration is:

```text
S1 → Front Ultrasonic Sensor

S2 → Right Ultrasonic Sensor

S3 → Left Ultrasonic Sensor

S4 → Color Sensor
```

Any historical configuration showing:

```text
S1 → Gyroscope
```

or:

```text
S1 → Unused
```

does not represent the current robot.

[Legacy Gyroscope Configuration](01_GConfig.md)

For the current S1 configuration, use:

[Current Ultrasonic Sensor Documentation](../components/05_UltrasonicSensors.md)

---

# 7. Ultrasonic Sensor Evolution

Piolín's ultrasonic architecture changed significantly during development.

Previous versions may describe:

```text
Two ultrasonic sensors

Diagonal sensor orientations

Different inner-wall strategies

Different outer-wall strategies

Gyroscope occupying S1

S1 remaining unused
```

The current robot uses **three ultrasonic sensors**:

```text
                     FRONT
                       ↑

                Front US — S1


Left US — S3 ← [ PIOLÍN ] → Right US — S2
```

Their current responsibilities are separated clearly.

The two lateral sensors provide navigation geometry:

```text
S2 + S3
   ↓
Wall Geometry
   ↓
Navigation
```

The front sensor provides frontal safety:

```text
S1
 ↓
Frontal Distance
 ↓
Safety
```

The front ultrasonic sensor is not part of the normal inner/outer wall-distance equations.

For the current configuration, see:

[Ultrasonic Sensors](../components/05_UltrasonicSensors.md)

---

# 8. Current Inner and Outer Sensor Assignment

The left and right ultrasonic sensors remain physically fixed on the robot.

Their navigation roles change depending on the direction of travel.

The direction is established using the color sensor.

For counterclockwise travel:

```text
BLUE detected first
        ↓
COUNTERCLOCKWISE
        ↓
LEFT US  S3 = INNER

RIGHT US S2 = OUTER
```

For clockwise travel:

```text
ORANGE detected first
         ↓
CLOCKWISE
         ↓
RIGHT US S2 = INNER

LEFT US  S3 = OUTER
```

This is the current sensing relationship.

Older documents may contain different interpretations because they were created for earlier navigation architectures.

Current documentation:

[Color Sensor](../components/06_ColorSensor.md)  
[Ultrasonic Sensors](../components/05_UltrasonicSensors.md)

---

# 9. Legacy Measurements and Geometry

Some historical Piolín files contain physical measurements or calculations that belonged to earlier versions of the robot.

These may include:

```text
Wheelbase measurements

Front or rear track measurements

Sensor offsets

Wall-distance targets

Steering relationships

Robot dimensions

Navigation constants
```

Those values should not automatically be interpreted as final measurements.

The confirmed current overall robot dimensions are:

| Parameter | Current Value |
| :--- | :---: |
| **Length** | **210 mm** |
| **Width** | **150 mm** |
| **Height** | **230 mm** |
| **Mass** | **0.80476 kg** |

The confirmed wheel dimensions are:

| Wheel | Current Diameter |
| :--- | :---: |
| **Front Wheels** | **38.1 mm** |
| **Rear Wheels** | **~61.0 mm** |

If a measurement exists only inside a legacy document and does not appear in the current documentation, it should be treated as a **historical development value**.

---

# 10. Legacy Software

Previous Piolín programs are also preserved when they provide useful evidence of software development.

Legacy code may contain:

```text
Gyroscope navigation

Previous ultrasonic configurations

Alternative corner algorithms

Older steering formulas

PixyCam processing

Prototype obstacle avoidance

Experimental thresholds

Previous state-machine concepts
```

These programs may not be compatible with the current robot.

Their purpose is primarily to show:

```text
What was implemented
        ↓
What behavior was observed
        ↓
What limitations appeared
        ↓
What was changed
        ↓
How the final architecture developed
```

A legacy program should therefore not automatically be treated as current competition code simply because it remains in the repository.

---

# 11. Legacy Electrical Documentation

Previous Piolín electrical diagrams are also preserved in this directory.

These include:

```text
PTScheme.png

PTechcircuit_image.png
```

They represent earlier stages of the robot's electronic architecture.

If these diagrams conflict with current wiring documentation, use the current reproducibility files.

[Current Wiring](../reproducibility/03_wiring.md)  
[Current Electrical Schematic](../reproducibility/04_elecschem.md)

The legacy diagrams remain useful for understanding how the electronic system evolved.

---

# 12. Historical Testing and Analysis

The file:

[Legacy Testing and Analysis](03_PTesting&Analysis.md)

contains previous testing and analysis associated with earlier Piolín configurations.

Results from those experiments should be interpreted according to the hardware and software used when they were recorded.

A result produced by:

```text
Previous Hardware
        +
Previous Sensor Layout
        +
Previous Software
        +
Previous Vision System
        ↓
Historical Result
```

does not automatically describe the current robot.

However, those results remain valuable because they can explain why later engineering decisions were made.

---

# 13. Files in This Directory

The legacy directory currently contains:

```text
docs/
└── legacy/
    ├── 00_LEGACY_NOTICE.md
    ├── 01_GConfig.md
    ├── 02_CameraPixy.md
    ├── 03_PTesting&Analysis.md
    ├── PTScheme.png
    └── PTechcircuit_image.png
```

Their roles are:

| File | Purpose |
| :--- | :--- |
| `00_LEGACY_NOTICE.md` | Explains how historical documentation should be interpreted |
| `01_GConfig.md` | Previous gyroscope-related configuration |
| `02_CameraPixy.md` | Previous PixyCam vision architecture |
| `03_PTesting&Analysis.md` | Historical testing and analysis |
| `PTScheme.png` | Previous system or electrical scheme |
| `PTechcircuit_image.png` | Previous circuit representation |

These files are preserved intentionally as engineering evidence.

---

# 14. Why Replaced Designs Are Preserved

Deleting every replaced design would remove much of the evidence showing how Piolín was engineered.

The final robot was produced through iteration.

```text
DESIGN
   ↓
BUILD
   ↓
IMPLEMENT
   ↓
OBSERVE
   ↓
IDENTIFY LIMITATION
   ↓
MODIFY
   ↓
REPEAT
```

A system that was eventually removed may still have been valuable because it revealed:

```text
Sensor limitations

Mechanical problems

Vision limitations

Integration problems

Software conflicts

Navigation weaknesses
```

Preserving these stages makes it possible to trace the reasoning behind the final robot.

---

# 15. Current vs. Legacy Quick Reference

| System | Previous / Legacy | Current Piolín |
| :--- | :--- | :--- |
| **Main Controller** | Experimental configurations | LEGO EV3 |
| **Drive** | Earlier mechanical configurations | Motor A rear propulsion |
| **Steering** | Previous steering iterations | Motor B Ackermann-style steering |
| **S1** | Gyroscope or unused in previous versions | Front Ultrasonic |
| **S2** | Previous ultrasonic configurations | Right Ultrasonic |
| **S3** | Previous ultrasonic configurations | Left Ultrasonic |
| **S4** | Previous color logic versions | Color Sensor |
| **Vision Sensor** | PixyCam | HuskyLens |
| **Vision Interface** | Previous configurations | Arduino Nano |
| **Nano to EV3** | Not part of earlier systems | USB |
| **Gyroscope** | Used experimentally | Not part of final configuration |
| **Wall Navigation** | Several experimental approaches | S2 + S3 lateral ultrasonics |
| **Frontal Safety** | Previous or absent configuration | S1 front ultrasonic |

This table is intended as a quick reference when reviewing older project files.

---

# 16. Documentation Priority

If two documents disagree about the current robot, use the following priority:

```text
CURRENT REPRODUCIBILITY DOCUMENTATION
                 ↓
CURRENT HARDWARE DOCUMENTATION
                 ↓
CURRENT MOBILITY AND SENSOR DOCUMENTATION
                 ↓
CURRENT SOFTWARE AND STRATEGY DOCUMENTATION
                 ↓
SYSTEMS ENGINEERING DOCUMENTATION
                 ↓
LEGACY DOCUMENTATION
```

Legacy documentation has the lowest priority when determining the **current physical configuration**.

It remains highly useful when studying the engineering process and previous design decisions.

---

# 17. Reproducing the Current Robot

Do not reproduce Piolín by combining components from different historical versions.

For example, this would create an incorrect configuration:

```text
Current EV3
    +
Legacy Gyroscope
    +
Legacy PixyCam
    +
Old Ultrasonic Arrangement
    +
Current Components
```

Those elements did not form the current robot as one complete system.

The correct reconstruction path is:

```text
Current Components
        ↓
Current Mechanical Configuration
        ↓
Current Wiring
        ↓
Current Software Environment
        ↓
Current Calibration
        ↓
Final Piolín
```

Use the current documentation below:

[Current Hardware](../components/)  
[Mobility and Mechanical Design](../mobility_mechanical/)  
[Power and Sensors](../power_sensors/)  
[Software and Strategy](../software_obstacles_strategy/)  
[Reproducibility](../reproducibility/)

---

# 18. Reproducibility Documentation

For reconstructing the final Piolín robot, use:

[Bill of Materials](../reproducibility/02_BOM.pdf)  
[Wiring](../reproducibility/03_wiring.md)  
[Electrical Schematic](../reproducibility/04_elecschem.md)  
[Software Setup](../reproducibility/05_softwaresetup.md)  
[Calibration](../reproducibility/06_HowToCalibrate.md)  
[Testing Protocol](../reproducibility/07_TestingProtocol.md)  
[Troubleshooting](../reproducibility/08_Troubleshooting.md)

The recommended reconstruction sequence is:

```text
Bill of Materials
        ↓
Wiring
        ↓
Electrical Architecture
        ↓
Software Setup
        ↓
Calibration
        ↓
Validation
        ↓
Final Piolín
```

---

# 19. Engineering Value of the Legacy Directory

The legacy directory provides evidence that Piolín's current configuration was reached through engineering decisions rather than being selected without development.

The project evolved across several interconnected areas:

```text
Mechanical Design
       ↓
Vehicle Behavior


Sensors
       ↓
Environmental Perception


Vision
       ↓
Obstacle Recognition


Electronics
       ↓
System Integration


Software
       ↓
Autonomous Control
```

A change in one subsystem often affected another.

For example, changing a sensor arrangement could require software changes. Changing the camera architecture could affect communication hardware. Changing steering geometry could alter how wall measurements were interpreted.

The legacy files help preserve these relationships.

---

# 20. How Legacy Information Should Be Used

Use the **current documentation** for:

```text
Current hardware

Robot construction

Port assignments

Sensor configuration

Electrical connections

Software setup

Current navigation architecture

Competition operation

Reproducibility
```

Use the **legacy documentation** for:

```text
Engineering history

Previous experiments

Replaced components

Alternative designs

Development-stage calculations

Previous software strategies

Design evolution

Decision justification
```

The simplest rule is:

> **Legacy documentation explains where Piolín came from. Current documentation explains what Piolín is now.**

---

# 21. Current Piolín Architecture

The final current architecture described by the main repository documentation is:

```text
                            LEGO EV3
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
          MOTOR A           MOTOR B           SENSORS
           Drive            Steering             │
                                                │
                            ┌────────────────────┼────────────────────┐
                            ▼                    ▼                    ▼
                           S1                   S2                   S3
                        Front US            Right US             Left US

                                                 │
                                                 ▼
                                                S4
                                           Color Sensor


                            LEGO EV3
                               ▲
                               │ USB
                               │
                         Arduino Nano
                               ▲
                               │
                           HuskyLens
```

This is the architecture that should be used when interpreting the current hardware and reproducibility documentation.

---

# 22. Where to Start

For the final WRO Future Engineers 2026 Piolín robot, begin here:

[Current Hardware Documentation](../components/)

[Mobility and Mechanical Documentation](../mobility_mechanical/)

[Power and Sensor Documentation](../power_sensors/)

[Software and Obstacle Strategy](../software_obstacles_strategy/)

[Systems Engineering](../systems_engineering/)

[Reproducibility Documentation](../reproducibility/)

---

# 23. Final Notice

The files inside `docs/legacy/` are intentionally preserved as part of the **PiolínTech engineering record**.

They document configurations and experiments that contributed to the development of the robot but are no longer representative of its final architecture.

The progression should be interpreted as:

```text
Experiment
    ↓
Observation
    ↓
Limitation Identified
    ↓
Engineering Decision
    ↓
Redesign
    ↓
Implementation
    ↓
Current System
```

Legacy documentation should therefore be read as **evidence of Piolín's development process**, not as an alternative set of instructions for building the final robot.

For the current specification, always use:

[Current Hardware](../components/)  
[Current Reproducibility Documentation](../reproducibility/)
