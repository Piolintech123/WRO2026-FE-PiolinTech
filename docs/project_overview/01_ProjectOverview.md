# 1. Project Overview

<div align="center">

<img
  src="../../v-photos/v4/piolin_open_isometric.jpg"
  alt="Piolín autonomous vehicle in its Open Challenge configuration"
  width="740"
/>

<br>

<sub><b>Figure 1.1.</b> Piolín, the autonomous vehicle developed by PiolínTech for WRO Future Engineers 2026.</sub>

</div>

**Piolín** is the autonomous vehicle developed by **PiolínTech** for the **World Robot Olympiad Future Engineers 2026** competition.

The project combines mechanical design, autonomous navigation, embedded programming, sensor integration, computer vision, experimentation, and iterative engineering into one vehicle platform capable of operating in the two Future Engineers challenges:

```text
OPEN CHALLENGE
```

and:

```text
OBSTACLE CHALLENGE
```

Rather than building two different robots, Piolín uses a **common mechanical and electrical platform** whose specialized sensing system changes according to the round.

The fundamental project architecture is:

```text
                    PIOLÍN
                       │
          ┌────────────┴────────────┐
          │                         │
          ▼                         ▼
    OPEN CHALLENGE           OBSTACLE CHALLENGE
          │                         │
       S1 Gyro                  S1 Pixy2.1
          │                         │
          └────────────┬────────────┘
                       │
              COMMON VEHICLE BASE
                       │
            ┌──────────┼──────────┐
            ▼          ▼          ▼
        S2 Left     S3 Right    S4 Color
       Ultrasonic  Ultrasonic    Sensor
            │          │          │
            └──────────┼──────────┘
                       ▼
                      EV3
                  /          \
                 ▼            ▼
              Motor A      Motor B
                 │            │
                 ▼            ▼
              DRIVE        STEERING
```

This architecture allows PiolínTech to solve two different autonomous-navigation problems without redesigning the complete vehicle for each one.

---

## 1.1 Competition Objective

WRO Future Engineers challenges teams to design an autonomous vehicle capable of navigating a structured course without human control after the run begins.

Piolín must combine several capabilities:

```text
drive autonomously

maintain a stable trajectory

detect track geometry

execute repeated corners

determine navigation direction

track course progression

recognize colored obstacles

pass obstacles on the required side

recover after maneuvers

complete multiple laps

perform final positioning / parking
```

The project is therefore not based on one isolated algorithm.

It is a complete autonomous system in which mechanical design, sensing, control logic, and physical testing continuously influence one another.

<div align="center">

<img
  src="../../v-photos/v4/full_track.jpg"
  alt="Full competition-style track used for Piolín development"
  width="740"
/>

<br>

<sub><b>Figure 1.2.</b> Representative track environment used to develop straight driving, cornering, obstacle avoidance, course progression, and parking behavior.</sub>

</div>

---

# 1.2 One Vehicle, Two Configurations

One of the central engineering decisions in Piolín is the use of a **shared vehicle architecture** between the two competition rounds.

The following hardware remains common:

```text
EV3 Brick

EV3 Rechargeable Battery 45501

Motor A — Large Motor

Motor B — Medium Motor

rear drivetrain

Ackermann-style steering

S2 — Left Ultrasonic

S3 — Right Ultrasonic

S4 — Color Sensor

LEGO Technic chassis
```

Only the specialized S1 sensor changes.

### Open Challenge

```text
S1 → EV3 Gyro Sensor
```

### Obstacle Challenge

```text
S1 → Pixy2.1
```

The Gyro and Pixy2.1 are **not installed simultaneously** in the current competition architecture.

This modular approach reduces the number of mechanical and electrical variables that change between rounds.

---

# 1.3 Open Challenge Configuration

<div align="center">

<img
  src="../../v-photos/v4/s1_open_gyro.jpg"
  alt="Piolín Open Challenge configuration using an EV3 Gyro Sensor on S1"
  width="680"
/>

<br>

<sub><b>Figure 1.3.</b> During the Open Challenge, S1 is assigned to the EV3 Gyro Sensor.</sub>

</div>

The current Open hardware mapping is:

| Port | Device | Main Function |
| :---: | :--- | :--- |
| A | EV3 Large Motor | Rear propulsion |
| B | EV3 Medium Motor | Front steering |
| S1 | EV3 Gyro Sensor | Heading and rotational reference |
| S2 | Left Ultrasonic Sensor | Left-side geometry |
| S3 | Right Ultrasonic Sensor | Right-side geometry |
| S4 | EV3 Color Sensor | Floor landmarks and course progression |

The Open Challenge focuses primarily on:

```text
stable straight driving

wall-relative positioning

heading stabilization

corner detection

corner execution

multi-lap consistency

parking
```

The sensing responsibilities are intentionally separated.

```text
GYRO
→ orientation
```

```text
ULTRASONICS
→ lateral geometry
```

```text
COLOR SENSOR
→ physical course-state events
```

The EV3 combines these measurements before producing propulsion and steering commands.

---

## 1.4 Open Navigation Direction

The first valid floor color establishes the direction of travel.

```text
BLUE first
→ COUNTERCLOCKWISE
```

```text
ORANGE first
→ CLOCKWISE
```

This direction becomes a persistent software state.

The ultrasonic sensors themselves never change physical identity:

```text
S2 = LEFT

S3 = RIGHT
```

Instead, their logical roles change.

For counterclockwise navigation:

```text
S2 LEFT
→ inner side

S3 RIGHT
→ outer side
```

For clockwise navigation:

```text
S3 RIGHT
→ inner side

S2 LEFT
→ outer side
```

This distinction between **physical identity** and **logical navigation role** is used throughout the current control architecture.

---

# 1.5 Open Course Progression

Piolín's intended Open run consists of:

```text
3 laps

12 corners
```

The Color Sensor provides physical landmarks that help the EV3 maintain course progression.

A conceptual Open state sequence is:

```text
START
  ↓
reset gyro
  ↓
determine course direction
  ↓
acquire stable track geometry
  ↓
STRAIGHT
  ↓
floor / geometry evidence
  ↓
CORNER
  ↓
gyro supports rotation
  ↓
ultrasonic geometry reacquired
  ↓
STRAIGHT
  ↓
repeat
  ↓
12 corners
  ↓
PARKING
```

The final parking strategy remains under active development, so the repository distinguishes between the **established navigation architecture** and the **final validated parking implementation**.

---

# 1.6 Obstacle Challenge Configuration

<div align="center">

<img
  src="../../v-photos/v4/piolin_obstacle_isometric.jpg"
  alt="Piolín in its current Obstacle Challenge configuration"
  width="740"
/>

<br>

<sub><b>Figure 1.4.</b> Piolín configured for the Obstacle Challenge using Pixy2.1 as the specialized S1 vision sensor.</sub>

</div>

The Obstacle Challenge uses the same drivetrain, steering system, chassis, lateral ultrasonics, and floor sensor.

The active mapping becomes:

| Port | Device | Main Function |
| :---: | :--- | :--- |
| A | EV3 Large Motor | Rear propulsion |
| B | EV3 Medium Motor | Front steering |
| S1 | Pixy2.1 | Forward visual perception |
| S2 | Left Ultrasonic Sensor | Left-side geometry |
| S3 | Right Ultrasonic Sensor | Right-side geometry |
| S4 | EV3 Color Sensor | Floor/course-state information |

The Gyro Sensor is removed for this configuration.

This round introduces a different navigation problem:

```text
identify obstacle
      ↓
determine required passing side
      ↓
generate avoidance trajectory
      ↓
confirm obstacle has been passed
      ↓
recover track geometry
```

---

# 1.7 Pixy2.1 Vision System

<div align="center">

<img
  src="../../v-photos/v4/pixy21_front.jpg"
  alt="Pixy2.1 used as Piolín's forward vision sensor"
  width="690"
/>

<br>

<sub><b>Figure 1.5.</b> Pixy2.1 provides forward color-based object detection during the Obstacle Challenge.</sub>

</div>

Pixy2.1 is connected directly to the EV3 through S1 and currently provides compact visual block information such as:

```text
signature

x

y

width

height
```

Piolín currently uses:

```text
sig1 → Pink → parking reference

sig2 → Red → pass RIGHT

sig3 → Green → pass LEFT
```

The passing rules are fixed:

```text
RED
→ RIGHT
```

```text
GREEN
→ LEFT
```

The position of a pillar inside the camera image does **not** redefine these rules.

Instead:

```text
signature
→ determines obstacle identity / required passing side
```

while:

```text
x, y, width, height
→ describe visual geometry and target relevance
```

The camera therefore provides information to the EV3; it does not directly control Motor B.

---

## 1.8 Pixy2.1 3D-Printed Casing

The current Pixy2.1 installation also includes a **3D-printed casing**.

This casing is part of the active Obstacle Challenge hardware and is considered part of the camera installation rather than a temporary prototype accessory.

Its purpose is to improve the physical integration of the vision sensor by providing a more controlled and repeatable camera installation. It also provides protection and support around the Pixy2.1 assembly and can help reduce some unwanted side illumination depending on the direction of external light.

The camera should therefore be calibrated with the casing installed.

The same engineering principle is used elsewhere on Piolín:

> **When a mechanical enclosure changes the conditions under which a sensor operates, that enclosure becomes part of the calibrated sensing system.**

This also applies to the Color Sensor casing.

---

# 1.9 Vision and Ultrasonic Fusion

Pixy2.1 does not replace the lateral ultrasonic sensors.

The two systems measure different physical information.

```text
PIXY2.1

→ pillar identity
→ image position
→ apparent target size
```

```text
S2 / S3 ULTRASONICS

→ left/right physical geometry
→ wall proximity
→ maneuver recovery context
```

During active obstacle avoidance, Pixy should have enough authority to establish the required trajectory while the ultrasonic sensors continue providing safety and geometric context.

After the pillar is passed, S2/S3 become increasingly important for recovering a useful track position.

The intended transition is:

```text
DETECT
  ↓
SELECT TARGET
  ↓
AVOID
  ↓
PASS
  ↓
COUNTERSTEER
  ↓
RECOVER
  ↓
NORMAL NAVIGATION
```

---

# 1.10 Common Lateral Geometry System

<div align="center">

<img
  src="../../v-photos/v4/PiolinUSlabeling.png"
  alt="Piolín ultrasonic sensor labeling showing S2 left and S3 right"
  width="720"
/>

<br>

<sub><b>Figure 1.6.</b> Permanent ultrasonic convention used throughout both challenges: S2 LEFT and S3 RIGHT.</sub>

</div>

Piolín uses exactly **two permanent ultrasonic sensors**.

```text
S2
→ LEFT
```

```text
S3
→ RIGHT
```

There is no permanent frontal ultrasonic sensor in the current competition architecture.

Earlier versions experimented with other configurations, but the current design gives each lateral sensor a simple and reproducible physical responsibility.

The sensors support:

```text
wall-relative positioning

wall safety

corridor geometry

corner transition information

post-obstacle recovery
```

while the specialized S1 sensor supplies information the ultrasonic system cannot provide.

---

# 1.11 Floor-State Sensing

<div align="center">

<img
  src="../../v-photos/v4/color_sensor_casing.jpg"
  alt="Piolín Color Sensor with its light isolation casing"
  width="660"
/>

<br>

<sub><b>Figure 1.7.</b> Piolín uses a physical casing around the downward-facing Color Sensor to reduce uncontrolled ambient illumination.</sub>

</div>

The Color Sensor remains permanently connected to S4 and observes the floor below Piolín.

The important course colors are:

```text
BLUE

ORANGE
```

The sensor provides discrete physical landmarks rather than continuous wall or heading information.

One physical marking can remain beneath the sensor for several control cycles, so the software must distinguish:

```text
sensor currently sees Blue
```

from:

```text
a NEW Blue event occurred
```

This motivates event-lock, debounce, and re-arm logic in the course-state controller.

The physical casing around the sensor improves the optical environment before those software decisions are made.

---

# 1.12 Mobility Architecture

Piolín uses a vehicle-style mobility architecture rather than differential steering.

The drivetrain is:

```text
Motor A
→ rear propulsion
```

and the steering system is:

```text
Motor B
→ front Ackermann-style steering
```

<div align="center">

<img
  src="../../v-photos/v4/rear_drivetrain_top.jpg"
  alt="Piolín rear propulsion drivetrain"
  width="700"
/>

<br>

<sub><b>Figure 1.8.</b> Rear drivetrain transfers Motor A rotation to the driven rear wheels.</sub>

</div>

<div align="center">

<img
  src="../../v-photos/v4/ackermann_top.jpg"
  alt="Piolín Ackermann-style front steering mechanism"
  width="700"
/>

<br>

<sub><b>Figure 1.9.</b> Front steering mechanism controlled by Motor B.</sub>

</div>

This creates a clear functional separation:

```text
Motor A
→ how Piolín moves longitudinally
```

```text
Motor B
→ how Piolín changes curvature
```

The final vehicle trajectory results from both actuators working together.

A steering command that works correctly at one speed may behave differently at another because the vehicle travels farther while Motor B physically changes the wheel angle.

For this reason, propulsion and steering are calibrated as one mobility system.

---

# 1.13 Why Ackermann-Style Steering

Piolín's steering system is based on the Ackermann principle because the inner and outer front wheels follow different turning paths.

During a turn:

```text
inner wheel
→ tighter path
→ larger steering angle
```

while:

```text
outer wheel
→ wider path
→ smaller steering angle
```

The design is described as **Ackermann-style** rather than claiming perfect theoretical Ackermann geometry.

Real LEGO mechanisms contain:

```text
linkage constraints

mechanical clearance

finite pivot geometry

structural tolerances
```

The final steering behavior is therefore measured on the physical vehicle rather than assumed from an ideal model alone.

---

# 1.14 Central EV3 Controller

The LEGO Mindstorms EV3 Brick is the central controller of Piolín.

It is responsible for:

```text
reading sensors

maintaining navigation state

processing course events

calculating steering commands

controlling propulsion

communicating with Pixy2.1 during Obstacles

recording or displaying diagnostic information
```

The EV3 therefore connects the sensing and mechanical layers.

The complete control loop is:

```text
ENVIRONMENT
     ↓
SENSORS
     ↓
EV3
     ↓
NAVIGATION DECISION
     ↓
MOTOR A + MOTOR B
     ↓
VEHICLE MOVEMENT
     ↓
ENVIRONMENT CHANGES
     ↓
SENSORS
```

Piolín is therefore a closed-loop autonomous vehicle rather than a robot that executes only a fixed sequence of timed movements.

---

# 1.15 Power Architecture

<div align="center">

<img
  src="../../v-photos/v4/ev3_battery_45501.jpg"
  alt="LEGO Mindstorms EV3 Rechargeable DC Battery 45501"
  width="650"
/>

<br>

<sub><b>Figure 1.10.</b> Piolín uses the official EV3 Rechargeable DC Battery 45501 as its central power source.</sub>

</div>

The current robot uses the **LEGO Mindstorms EV3 Rechargeable DC Battery 45501**.

The electrical architecture is intentionally centralized:

```text
Battery 45501
      ↓
EV3
      ↓
motors + sensors
```

The current competition robot does not require:

```text
external propulsion battery

separate vision battery

permanent buck converter

Arduino power system
```

During Obstacles, Pixy2.1 is integrated through the current S1 connection rather than through the previous multi-device bridge.

This reduces the number of electrical subsystems that must be maintained.

---

# 1.16 Electrical Configuration by Round

<div align="center">

<img
  src="../../v-photos/v4/wiring_open.jpg"
  alt="Piolín Open Challenge wiring"
  width="720"
/>

<br>

<sub><b>Figure 1.11.</b> Open Challenge wiring with the Gyro Sensor occupying S1.</sub>

</div>

```text
OPEN

A  → Large Motor
B  → Medium Motor

S1 → Gyro
S2 → Left Ultrasonic
S3 → Right Ultrasonic
S4 → Color Sensor
```

<div align="center">

<img
  src="../../v-photos/v4/wiring_obstacle.jpg"
  alt="Piolín Obstacle Challenge wiring"
  width="720"
/>

<br>

<sub><b>Figure 1.12.</b> Obstacle Challenge wiring with Pixy2.1 occupying S1.</sub>

</div>

```text
OBSTACLES

A  → Large Motor
B  → Medium Motor

S1 → Pixy2.1
S2 → Left Ultrasonic
S3 → Right Ultrasonic
S4 → Color Sensor
```

Only one sensor port changes.

This is one of the main reproducibility advantages of the current architecture.

---

# 1.17 Software Architecture

Because S1 physically contains a different device in each round, Piolín also benefits from maintaining round-specific software rather than forcing both hardware stacks into one large program.

The current development direction is conceptually:

```text
src/
│
├── open_challenge.py
│      ↓
│   Pybricks MicroPython
│      ↓
│   Gyro + S2/S3 + S4
│
└── obstacle_challenge.py
       ↓
    ev3dev2 + SMBus/I2C
       ↓
    Pixy2.1 + S2/S3 + S4
```

This separation reflects the real hardware.

It also makes debugging easier because the active program contains only the interfaces needed for the active round.

---

# 1.18 Open Control Philosophy

Piolín's Open strategy is not based on one sensor dominating the complete vehicle.

Instead, different sensors solve different parts of the navigation problem.

```text
ULTRASONICS
→ lateral position
```

```text
GYRO
→ orientation
```

```text
COLOR
→ course progression
```

The steering controller then combines the available information.

A stable straight should require relatively small Motor B corrections.

A corner temporarily requires stronger steering and greater use of heading/geometry transition information.

Afterward, the robot should reacquire a stable lateral geometry before the next maneuver.

The design goal is therefore not simply:

```text
turn 90 degrees
```

but:

```text
enter corner correctly
+
rotate
+
exit in useful geometry
+
stabilize
```

---

# 1.19 Obstacle Control Philosophy

Obstacle navigation introduces another control objective:

```text
follow track
```

while simultaneously:

```text
pass pillar on required side
```

These goals can temporarily conflict.

The intended hierarchy is therefore state-dependent.

During normal driving:

```text
wall geometry
→ strong influence
```

During active pillar avoidance:

```text
Pixy objective
→ stronger influence

wall sensing
→ safety/context
```

After the obstacle:

```text
countersteer
      ↓
ultrasonic recovery
      ↓
normal geometry
```

This prevents a normal centering controller from continuously fighting the avoidance maneuver.

---

# 1.20 Mechanical and Sensor Interaction

Piolín's sensors cannot be understood separately from its mechanical movement.

For example:

```text
Motor B steers
      ↓
vehicle yaw changes
```

which changes:

```text
gyro heading

ultrasonic wall geometry

Pixy camera viewpoint
```

Similarly:

```text
Motor A increases speed
```

reduces the physical time available for:

```text
sensor confirmation

steering response

corner entry

obstacle avoidance
```

This is why PiolínTech treats the robot as a **mechatronic system** rather than as separate mechanical and software projects.

---

# 1.21 Physical Sensor Conditioning

Two current sensors include custom mechanical solutions that affect their sensing environment.

### Color Sensor

A casing reduces uncontrolled ambient illumination around the downward-facing floor sensor.

### Pixy2.1

The current camera includes a 3D-printed casing that forms part of the installed vision system.

These additions demonstrate a common design philosophy:

```text
first improve physical measurement conditions
        ↓
then calibrate
        ↓
then process in software
```

Software filtering should not be the only solution when the physical sensing environment itself can be improved.

---

# 1.22 Engineering Iteration

Piolín did not reach its current architecture in one design step.

Development included experiments with:

```text
different ultrasonic arrangements

front ultrasonic sensing

different camera solutions

HuskyLens

Arduino Nano integration

different S1 configurations

different steering reinforcement

different navigation controllers
```

Not all of these systems remain in the current robot.

Their value is that they exposed:

```text
limitations

integration problems

unnecessary complexity

better alternatives
```

which influenced the current architecture.

Engineering progress is therefore represented not only by what remains on the robot, but also by what the team deliberately removed.

---

# 1.23 Current vs. Legacy Architecture

The current competition robot should not be confused with earlier prototypes.

### Current Open

```text
S1 Gyro
S2 Left US
S3 Right US
S4 Color
```

### Current Obstacles

```text
S1 Pixy2.1
S2 Left US
S3 Right US
S4 Color
```

### Legacy / Experimental

```text
HuskyLens

Arduino Nano vision bridge

permanent front ultrasonic

older Pixy integration

different ultrasonic orientations

older steering / chassis configurations
```

Legacy development remains useful for documenting engineering evolution but should not appear as part of the current reproduction instructions.

---

# 1.24 Why HuskyLens and Arduino Were Removed

Earlier obstacle-vision development used an architecture containing an intermediate controller.

Conceptually:

```text
HuskyLens
      ↓
Arduino Nano
      ↓
EV3
```

The current vision system is:

```text
Pixy2.1
      ↓
EV3 S1
```

The newer architecture reduces:

```text
active hardware count

communication layers

firmware dependencies

wiring complexity
```

while still providing the color-block information required by Piolín's obstacle strategy.

The older system was therefore not a useless experiment. It provided information that helped the team choose a simpler current architecture.

---

# 1.25 Why the Front Ultrasonic Was Removed

Earlier Piolín configurations also used or considered a front ultrasonic sensor.

The current architecture instead dedicates all four sensor ports to:

```text
S1
→ specialized Gyro or Pixy

S2
→ left geometry

S3
→ right geometry

S4
→ floor state
```

The front sensor was removed because the final system benefits more from the specialized S1 device than from maintaining a third ultrasonic permanently.

This represents a sensor-allocation trade-off rather than simply a missing component.

---

# 1.26 Design Priorities

Piolín's current design is guided by several priorities.

### Mechanical repeatability

The drivetrain, steering, and sensor mounts should remain sufficiently stable that calibration values retain physical meaning.

### Clear sensor responsibilities

Each sensor should solve the type of measurement problem it handles best.

### Reduced unnecessary complexity

A component should remain on the final robot only when its benefit justifies the additional wiring, software, mass, and failure points.

### Reusable vehicle platform

The same drivetrain and steering system should support both challenges.

### Measured rather than assumed performance

Final dimensions, thresholds, success rates, and calibration values should come from the current physical robot.

These priorities influence both hardware and software decisions.

---

# 1.27 Testing and Validation

PiolínTech uses iterative testing to develop the vehicle.

The general process is:

```text
OBSERVE
   ↓
IDENTIFY FAILURE
   ↓
FORM HYPOTHESIS
   ↓
CHANGE ONE RELEVANT VARIABLE
   ↓
TEST AGAIN
   ↓
COMPARE
```

Tests progress from isolated systems toward complete runs.

For example:

```text
steering center
      ↓
straight driving
      ↓
single corner
      ↓
multiple corners
      ↓
complete Open run
```

or:

```text
single color signature
      ↓
single pillar
      ↓
pillar + recovery
      ↓
alternating pillars
      ↓
complete Obstacle run
```

This prevents full-run failures from becoming the only source of diagnostic information.

---

# 1.28 Reproducibility

A major objective of this repository is to document enough engineering information that Piolín's system can be understood and reconstructed.

Reproducibility requires more than a Bill of Materials.

Another builder needs to know:

```text
which component is used

which port it connects to

where it is installed

how it is oriented

which software environment accesses it

how it is calibrated

what role it performs
```

For this reason, the repository includes:

```text
hardware documentation

mechanical documentation

sensor configuration

software architecture

calibration procedures

testing procedures

current-vs-legacy distinction

photographic evidence
```

The goal is to document the **system**, not merely the individual parts.

---

# 1.29 Current Development Status

The hardware architecture described in this document represents Piolín's current V4 system.

However, some autonomous behaviors are still being optimized.

### Open development currently includes

```text
starting acquisition

corner consistency

corner exit geometry

multi-lap stability

final parking behavior
```

### Obstacle development currently includes

```text
Pixy target relevance

multiple-block selection

target locking

pillar pass confirmation

countersteering

post-obstacle recovery

parking
```

These areas should not be described as fully solved until representative testing supports that conclusion.

This distinction keeps the repository technically accurate:

```text
CURRENT DESIGN
≠
FINAL VALIDATED PERFORMANCE
```

---

# 1.30 Values Not Yet Treated as Final Specifications

Piolín has undergone significant mechanical and sensing changes.

For that reason, earlier measurements should not automatically be copied into the current V4 specification.

The following should be measured or reverified before being presented as final:

```text
overall dimensions

vehicle mass

wheel diameters

track widths

wheelbase

final steering angles

turning radius

final ultrasonic targets

final color thresholds

gyro drift

final corner angle behavior

Pixy mounting geometry

final obstacle thresholds

maximum validated speeds

parking displacement

success rates

run times
```

Working values inside source code remain useful for development, but they should be clearly distinguished from validated engineering measurements.

---

# 1.31 System-Level Architecture

The complete current architecture can be represented as:

```text
                         WRO TRACK
                            │
                            ▼
                ┌──────────────────────┐
                │      PERCEPTION      │
                │                      │
                │  S2 LEFT ULTRASONIC  │
                │  S3 RIGHT ULTRASONIC │
                │  S4 COLOR SENSOR     │
                │                      │
                │  OPEN: S1 GYRO       │
                │  OBS:  S1 PIXY2.1    │
                └──────────┬───────────┘
                           │
                           ▼
                     ┌─────────┐
                     │   EV3   │
                     └────┬────┘
                          │
              ┌───────────┴───────────┐
              │                       │
              ▼                       ▼
           MOTOR A                 MOTOR B
              │                       │
              ▼                       ▼
         REAR DRIVE             ACKERMANN
                                STEERING
              │                       │
              └───────────┬───────────┘
                          ▼
                    VEHICLE MOTION
                          │
                          ▼
                  NEW TRACK GEOMETRY
                          │
                          └────────────→ PERCEPTION
```

<div align="center">

<img
  src="../../v-photos/v4/piolin_bottom.jpg"
  alt="Bottom view of Piolín showing its integrated vehicle architecture"
  width="720"
/>

<br>

<sub><b>Figure 1.13.</b> The drivetrain, steering, sensor mounting, structure, and electronics operate as one integrated autonomous vehicle.</sub>

</div>

The system forms a continuous feedback loop.

Every movement changes the geometry observed by the sensors, and every new observation can change the next movement.

---

# 1.32 Final Engineering Assessment

Piolín is designed around a relatively simple but highly integrated systems architecture.

Its main mechanical concept is:

```text
Motor A
→ rear propulsion

Motor B
→ Ackermann-style front steering
```

Its permanent sensing layer is:

```text
S2
→ Left Ultrasonic

S3
→ Right Ultrasonic

S4
→ Color Sensor
```

and its specialized perception layer is:

```text
OPEN
→ S1 Gyro
```

```text
OBSTACLES
→ S1 Pixy2.1
```

This architecture allows one common vehicle platform to solve two different autonomous navigation problems.

The project has also evolved toward **fewer unnecessary components and clearer subsystem responsibilities**. Earlier experiments involving a front ultrasonic sensor, HuskyLens, and Arduino Nano provided useful development experience but were removed when the current architecture offered a simpler or more appropriate solution.

Mechanical modifications such as the Color Sensor casing and the current 3D-printed Pixy2.1 casing are treated as part of their respective sensing systems because they affect the physical conditions under which measurements are made.

The project can therefore be summarized through four connected principles:

```text
STABLE MECHANICS

CLEAR SENSOR RESPONSIBILITIES

STATE-BASED AUTONOMOUS CONTROL

MEASURED ITERATIVE DEVELOPMENT
```

PiolínTech's objective is not merely to make Piolín complete one successful run. The engineering objective is to understand **why the vehicle behaves as it does**, reduce unnecessary sources of variability, document the evolution of the design, and develop an autonomous platform whose behavior can be reproduced and improved systematically.

> **Piolín is treated as one complete mechatronic system in which mechanics, electronics, sensing, software, and testing are designed together rather than as independent parts.**

---

<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
