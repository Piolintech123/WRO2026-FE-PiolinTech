# Phase 1 — Initial EV3 Prototype

## 1. Beginning of Piolín

Phase 1 represents the **first physical prototype of Piolín** and the starting point of PiolínTech's development for WRO Future Engineers.

Piolín has always been developed around the **LEGO MINDSTORMS EV3 platform**.

The goal of this first prototype was not to create the final competition robot immediately. Instead, it provided a simple platform for learning how the vehicle behaved and for testing the first autonomous-driving ideas.

The Phase 1 development cycle can be summarized as:

```text
BUILD SIMPLE EV3 VEHICLE
        ↓
TEST BASIC MOVEMENT
        ↓
READ DISTANCE SENSOR
        ↓
EXPERIMENT WITH STEERING
        ↓
OBSERVE PHYSICAL LIMITATIONS
        ↓
REDESIGN FOR NEXT PHASE
```

Phase 1 is now considered a **legacy prototype**, but it established the mechanical and software foundation from which the later versions of Piolín evolved.

---

## 2. Phase 1 Prototype

<div align="center">

<img
  src="https://github.com/user-attachments/assets/94f45de2-0536-41ca-9f66-075bb64a17f1"
  alt="Piolín Phase 1 EV3 prototype"
  width="500"
/>

<br>

<sub><b>Figure 1.</b> Piolín's Phase 1 prototype, built as the team's first EV3 autonomous-vehicle platform.</sub>

</div>

This prototype was built primarily from:

```text
LEGO MINDSTORMS EV3

LEGO Technic structure

EV3 motors

EV3 sensing hardware
```

At this stage, the emphasis was on obtaining a functional moving prototype as quickly as possible so that the team could begin testing real autonomous behavior.

---

## 3. Phase 1 Architecture

The early architecture was intentionally simple.

```text
            ENVIRONMENT
                 │
                 ▼
        EV3 ULTRASONIC SENSOR
                 │
                 ▼
             EV3 BRICK
                 │
          BASIC CONTROL LOGIC
                 │
          ┌──────┴──────┐
          ▼             ▼
       DRIVE          STEERING
       MOTOR           MOTOR
          │             │
          └──────┬──────┘
                 ▼
          ROBOT MOVEMENT
```

The robot relied on the EV3 Brick as its central controller.

Unlike later versions of Piolín, Phase 1 did not yet contain the complete combination of:

```text
dual lateral ultrasonic sensing

floor-event processing

gyro heading stabilization

Pixy2.1 vision

state-based obstacle avoidance

control arbitration

dedicated parking logic
```

Those systems were introduced progressively in later development phases.

---

## 4. Main Hardware

The Phase 1 prototype used a basic LEGO EV3 hardware architecture.

| Subsystem | Phase 1 Implementation |
|---|---|
| Main controller | LEGO MINDSTORMS EV3 Brick |
| Structure | LEGO Technic |
| Actuation | LEGO EV3 motors |
| Distance sensing | EV3 Ultrasonic Sensor |
| Vision system | None |
| Floor-color navigation | Not yet part of the mature architecture |
| Vehicle architecture | Early prototype configuration |
| Power system | LEGO EV3 battery system |

The purpose of the hardware was to provide a reliable starting platform for experimentation.

The EV3 controller itself was **not abandoned in later phases**.

Instead, PiolínTech progressively developed a more capable mechanical, sensing, and software architecture around the EV3 platform.

---

## 5. Early Ultrasonic Sensing

One of the main sensors used during the first prototype was an **EV3 Ultrasonic Sensor**.

The early arrangement was much simpler than Piolín's current lateral sensing architecture.

The basic concept was:

```text
OBJECT / WALL
      ↓
ULTRASONIC READING
      ↓
DISTANCE ESTIMATE
      ↓
BASIC NAVIGATION RESPONSE
```

This allowed the team to begin experimenting with the relationship between:

```text
measured distance
```

and:

```text
vehicle movement
```

However, one distance measurement provided limited information about the vehicle's complete relationship with the surrounding course.

This became an important lesson for later phases.

---

## 6. Early Driving and Steering Experiments

Phase 1 was used to understand how a physical EV3 vehicle responds to software commands.

The team experimented with:

```text
forward movement

steering response

speed

distance sensing

course correction

basic autonomous reactions
```

These tests demonstrated an important difference between:

```text
COMMANDING A TURN
```

and:

```text
ACHIEVING A REPEATABLE PHYSICAL TRAJECTORY
```

The final position of a vehicle depends on more than the software command alone.

Factors such as:

```text
steering geometry

vehicle speed

wheel behavior

mechanical structure

starting position
```

all influence the resulting path.

This realization became one of the reasons later Piolín prototypes placed much greater emphasis on mechanical steering geometry.

---

## 7. Limitations Discovered in Phase 1

Phase 1 was successful as a learning platform, but several limitations became visible during testing.

### Limited environmental information

A simple ultrasonic configuration could detect distance, but it could not describe the complete lateral geometry of the course.

The robot needed more information to answer questions such as:

```text
How close is the left side?

How close is the right side?

Where is the robot inside the corridor?

Is the robot centered or angled?

Has the surrounding geometry changed because of a corner?
```

This motivated later experiments with additional sensing positions.

---

### Basic steering behavior

The early mechanical configuration was useful for initial movement tests, but more controlled vehicle geometry was required for WRO Future Engineers.

The team needed:

```text
more predictable turning

better steering repeatability

vehicle-like corner trajectories

better control over course position
```

This requirement became one of the major drivers of Piolín's later **Ackermann steering development**.

---

### No visual obstacle identification

Phase 1 did not yet contain a camera-based obstacle-perception system.

An ultrasonic sensor can answer approximately:

```text
Something is at this distance.
```

but it cannot independently answer:

```text
Is the pillar Red?

Is the pillar Green?

Which WRO passing rule applies?
```

This distinction became important when PiolínTech later began developing the Obstacle Challenge architecture.

---

### Limited navigation context

Early control was more reactive.

A simple approach can behave conceptually as:

```text
sensor sees condition
      ↓
motor reacts
```

However, WRO Future Engineers requires the robot to understand different situations such as:

```text
straight navigation

corner

pillar approach

pillar avoidance

pillar clearance

recovery

parking
```

This eventually motivated the transition toward a more structured state-based software architecture.

---

## 8. What Phase 1 Taught Us

The most important result of Phase 1 was not a specific speed or competition score.

It was the engineering information obtained from the prototype.

Phase 1 demonstrated that Piolín needed to evolve in several areas.

```text
PHASE 1 OBSERVATION
        ↓
NEXT DESIGN NEED
```

### Sensing

```text
simple distance sensing
        ↓
more complete course geometry
```

### Steering

```text
basic vehicle movement
        ↓
more controlled steering geometry
```

### Navigation

```text
direct reactions
        ↓
structured autonomous behavior
```

### Perception

```text
distance only
        ↓
eventually add visual obstacle identity
```

### Testing

```text
does it move?
        ↓
why does it move this way?
```

This shift in questions represents an important step in PiolínTech's engineering process.

---

## 9. What Was Preserved

Not everything from Phase 1 was replaced.

Several fundamental decisions survived throughout Piolín's development.

Most importantly:

```text
LEGO MINDSTORMS EV3
→ remained the main controller
```

The project continued using:

```text
EV3 motors

EV3-compatible sensor ports

LEGO-based mechanical construction

Python-based autonomous control
```

The later robot is therefore an evolution of the Phase 1 platform rather than a completely unrelated replacement.

The architecture became more sophisticated while preserving the same central EV3 ecosystem.

---

## 10. What Changed After Phase 1

The next development stages focused on improving the areas exposed by this first prototype.

The evolution moved toward:

```text
BETTER MECHANICAL GEOMETRY
        ↓
ACKERMANN STEERING DEVELOPMENT
        ↓
BETTER ULTRASONIC POSITIONING
        ↓
COLOR SENSOR INTEGRATION
        ↓
COURSE NAVIGATION DEVELOPMENT
        ↓
VISION EXPERIMENTATION
        ↓
STATE-BASED CONTROL
        ↓
CURRENT COMPETITION ARCHITECTURE
```

The important point is that these changes occurred **around the EV3 platform**.

Piolín was not converted into a Raspberry Pi robot or into a non-LEGO custom electronics vehicle.

---

## 11. Phase 1 vs. Current Piolín

The difference between the first prototype and the current robot is primarily the maturity of each subsystem.

| Engineering Area | Phase 1 | Current Direction |
|---|---|---|
| Controller | EV3 Brick | EV3 Brick |
| Mechanical design | Initial prototype | Refined vehicle architecture |
| Steering | Early configuration | Ackermann steering driven by Motor B |
| Propulsion | Basic EV3 drive | Rear propulsion driven by Motor A |
| Ultrasonic sensing | Simple early configuration | Two lateral sensors |
| Left ultrasonic identity | Not yet current architecture | S2 = LEFT |
| Right ultrasonic identity | Not yet current architecture | S3 = RIGHT |
| Floor sensing | Early/not mature | S4 Color Sensor |
| Open heading | Not yet current architecture | S1 Gyro |
| Obstacle vision | None | S1 Pixy2.1 |
| Obstacle strategy | Not developed | Dedicated perception and maneuver logic |
| Software structure | Basic/reactive | State-oriented architecture |
| Controller priority | Basic | Control arbitration |
| Parking | Not developed | Dedicated parking subsystem |

This comparison shows that the largest evolution was not simply an increase in computing power.

It was the progressive improvement of:

```text
MECHANICS
+
SENSING
+
PERCEPTION
+
CONTROL
+
SOFTWARE ARCHITECTURE
```

---

## 12. Evolution Toward Phase 2

Phase 1 provided a functional foundation.

Phase 2 would focus more heavily on:

```text
vehicle mechanics

steering development

navigation geometry

sensor placement

repeatable autonomous movement
```

The transition can be summarized as:

```text
PHASE 1
INITIAL EV3 PROTOTYPE
        │
        │
        ├── Basic mobility established
        ├── First sensor experiments
        ├── First autonomous scripts
        ├── Steering behavior observed
        └── Navigation limitations identified
        │
        ▼
PHASE 2
MECHANICAL + NAVIGATION DEVELOPMENT
```

Phase 1 therefore served its intended engineering purpose:

> **Build the simplest useful prototype, observe how the real vehicle behaves, identify the first major limitations, and use those observations to define the next version.**

---

## Phase 1 Status

```text
PHASE:       1
STATUS:      LEGACY
CONTROLLER:  LEGO MINDSTORMS EV3
ROLE:        INITIAL PROTOTYPE
SUCCESSOR:   PHASE 2
```

Although this configuration is no longer the current competition architecture, it remains documented because it shows where Piolín's development began and provides evidence of the engineering decisions that shaped the later robot.

---

<div align="center">

### [Evolution Overview](README.md) · [PiolínTech Main README](../../README.md)

</div>
