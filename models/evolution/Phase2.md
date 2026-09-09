# Phase 2 — Mechanical and Navigation Development

## 1. From Prototype to Vehicle Architecture

Phase 2 represents the stage in which Piolín evolved from an initial EV3 mobility prototype into a robot designed more deliberately around the requirements of **WRO Future Engineers**.

The EV3 Brick remained the main controller.

The major change was not a replacement of the computing platform, but a redesign of the systems around it:

```text
PHASE 1
Basic EV3 Prototype
        ↓
PHASE 2
Vehicle-Oriented Mechanical Design
        ↓
Ackermann Steering
        ↓
Dedicated Propulsion + Steering Roles
        ↓
Improved Distance Sensing
        ↓
Floor Mark Detection
        ↓
More Structured Navigation
```

The central objective of Phase 2 was:

> **Make Piolín behave more like a controllable autonomous vehicle rather than a simple mobile EV3 prototype.**

---

## 2. Phase 2 Development Direction

During this phase, PiolínTech concentrated on four major engineering areas:

```text
MECHANICS

STEERING

SENSOR GEOMETRY

COURSE NAVIGATION
```

The team began to treat these areas as connected systems.

For example:

```text
steering geometry
        ↓
changes turning radius
        ↓
changes ultrasonic readings
        ↓
changes navigation behavior
```

This was an important step away from treating software and mechanics as independent parts of the robot.

---

## 3. Ackermann Steering Development

One of the most important mechanical changes in Phase 2 was the development of **Ackermann-style front steering**.

Instead of relying on a robot-style turning method, Piolín began using a car-like steering architecture.

The basic concept is:

```text
                FRONT

          \               /
           \             /
        INNER WHEEL   OUTER WHEEL
          larger       smaller
          steering     steering
          angle        angle

                │
                ▼

        COMMON TURNING REGION
```

During a turn, the inner and outer front wheels should not follow identical arcs.

The inner wheel travels along a tighter radius than the outer wheel.

This made steering geometry an important mechanical design problem rather than simply a software command.

---

## 4. Dedicated Motor Roles

As the vehicle architecture developed, propulsion and steering were assigned separate roles.

The configuration that emerged and continued into the current robot is:

```text
Motor A
→ LEGO EV3 Large Motor
→ rear propulsion
```

and:

```text
Motor B
→ LEGO EV3 Medium Motor
→ front steering
```

This creates a clear functional separation:

```text
MOTOR A
controls vehicle progression
```

```text
MOTOR B
controls trajectory curvature
```

Conceptually:

```text
              EV3 BRICK
                 │
        ┌────────┴────────┐
        │                 │
        ▼                 ▼
     MOTOR A           MOTOR B
   PROPULSION          STEERING
        │                 │
        ▼                 ▼
 REAR DRIVETRAIN    ACKERMANN FRONT
        │                 │
        └────────┬────────┘
                 ▼
          VEHICLE TRAJECTORY
```

This architecture became one of the most persistent design decisions in Piolín's evolution.

---

## 5. Why Steering Geometry Became Important

The first prototype showed that a steering command does not uniquely determine where the robot will go.

The resulting path also depends on:

```text
wheel geometry

steering angle

vehicle speed

wheelbase

mechanical alignment

starting position
```

During Phase 2, PiolínTech increasingly focused on obtaining:

```text
more repeatable curves

more controlled corner entry

less unnecessary steering

more predictable return to straight motion
```

The engineering objective became:

```text
software command
        ↓
repeatable steering geometry
        ↓
repeatable physical trajectory
```

rather than simply:

```text
software says LEFT
→ robot turns somehow
```

---

## 6. Distance-Sensor Development

Phase 2 also expanded the role of ultrasonic sensing.

The early robot had limited information about its relationship with the course.

As development continued, PiolínTech experimented with different sensor arrangements to obtain more useful spatial information.

The key question changed from:

```text
Is there something ahead?
```

to:

```text
Where is Piolín relative to the course boundaries?
```

This required information from both sides of the vehicle.

The architecture gradually moved toward:

```text
LEFT DISTANCE
+
RIGHT DISTANCE
        ↓
COURSE GEOMETRY
```

rather than depending on one isolated distance measurement.

---

## 7. Sensor Placement Was Part of the Experiment

The ultrasonic configuration did not immediately appear in its final form.

During development, the team experimented with:

```text
sensor position

sensor orientation

forward sensing

lateral sensing

different combinations of measurements
```

This was necessary because an ultrasonic sensor does not measure an abstract mathematical wall.

It measures whatever surface intersects its sound cone.

Therefore:

```text
same sensor
+
different mounting angle
=
different information
```

Sensor placement became part of the navigation design.

---

## 8. Evolution Toward Lateral Geometry

A major insight from these experiments was that **lateral ultrasonic measurements** were particularly useful for understanding Piolín's relationship with the corridor.

The concept became:

```text
LEFT WALL / BOUNDARY
        ↓
LEFT DISTANCE
        │
        │
      PIOLÍN
        │
        │
RIGHT DISTANCE
        ↑
RIGHT WALL / BOUNDARY
```

With two side measurements, the software can reason about more than simple proximity.

It can begin to infer:

```text
lateral position

relative corridor geometry

approach to one side

movement away from one side

geometry changes near corners
```

This idea became increasingly important in later navigation algorithms.

---

## 9. Color Sensor Integration

Phase 2 also developed the use of a downward-facing **EV3 Color Sensor** for detecting course markings.

The sensor eventually occupied:

```text
S4
```

and became responsible for observing the colored floor regions used as navigation landmarks.

The key course colors are:

```text
BLUE

ORANGE
```

These markings provided information that ultrasonic sensing alone could not provide.

For example, a wall measurement describes:

```text
physical geometry
```

while a floor marking can describe:

```text
course context
```

The combination created a stronger navigation system.

---

## 10. Direction from the First Floor Mark

An important navigation concept developed around the first detected course marking.

The intended rule became:

```text
FIRST BLUE
→ COUNTERCLOCKWISE
```

and:

```text
FIRST ORANGE
→ CLOCKWISE
```

This allows the same robot to determine the required direction from the course itself rather than depending entirely on a manually selected direction.

The architecture became:

```text
START
   ↓
MOVE / ACQUIRE COURSE
   ↓
DETECT FIRST FLOOR MARK
   ↓
   ┌───────────────┐
   │               │
 BLUE           ORANGE
   │               │
   ▼               ▼
  CCW              CW
```

This principle continued into later versions of Piolín.

---

## 11. From Color Samples to Navigation Landmarks

Early color-based navigation can be implemented very simply:

```text
see color
→ immediately react
```

However, PiolínTech discovered that a physical marking can remain under the sensor for multiple software cycles.

For example:

```text
BLUE
BLUE
BLUE
BLUE
```

does not represent four different course locations.

It represents:

```text
ONE PHYSICAL BLUE MARK
```

This became the beginning of a more important concept:

```text
RAW SENSOR READING
        ↓
COURSE EVENT
```

The mature confirmation, latch, release, and duplicate-protection logic was developed further in later phases, but Phase 2 established the importance of using floor colors as **navigation landmarks** rather than simply raw sensor values.

---

## 12. Navigation Became Geometric

One of the main software changes during Phase 2 was the transition away from purely threshold-based reactions.

A very simple wall strategy behaves like:

```text
too close
→ turn away
```

```text
too far
→ turn toward
```

This can work in simple conditions, but often creates:

```text
late corrections

zig-zag

overcorrection

oscillation
```

PiolínTech began moving toward a more geometric question:

> **Where is the vehicle relative to the corridor, and what steering correction is needed to return toward the desired trajectory?**

Conceptually:

```text
LEFT DISTANCE
      +
RIGHT DISTANCE
      ↓
GEOMETRY ESTIMATE
      ↓
POSITION ERROR
      ↓
STEERING CORRECTION
```

This idea later became much more developed in the Open Challenge controller.

---

## 13. Smaller and Earlier Corrections

Another lesson from navigation testing was that waiting until Piolín reached a dangerous position before correcting produced unstable behavior.

The desired behavior changed toward:

```text
small error
→ small early correction
```

instead of:

```text
large error
→ emergency large correction
```

The control philosophy became:

```text
MEASURE CONTINUOUSLY
      ↓
CORRECT EARLY
      ↓
KEEP STEERING SMALL WHEN POSSIBLE
      ↓
USE STRONG CORRECTION ONLY WHEN NEEDED
```

This principle became important in later wall-following, corner, and recovery development.

---

## 14. Steering and Navigation Interaction

Phase 2 showed that navigation tuning could not be separated from steering mechanics.

For example:

```text
software correction too strong
        ↓
Motor B requests large steering
        ↓
Ackermann geometry creates tight arc
        ↓
ultrasonic geometry changes rapidly
        ↓
controller reacts again
        ↓
oscillation
```

This is a closed-loop interaction.

The team therefore began considering:

```text
steering strength

vehicle speed

sensor geometry

correction timing
```

together.

This systems-level reasoning became increasingly important in later phases.

---

## 15. Early Corner Development

Corners became one of the most difficult navigation situations.

During straight motion:

```text
side sensors
→ observe approximately consistent corridor geometry
```

During a corner:

```text
vehicle rotates
        ↓
sensor beams rotate
        ↓
observed surfaces change
        ↓
straight-wall assumptions become weaker
```

This showed that one navigation rule was not necessarily appropriate for every part of the course.

The early corner work eventually contributed to the later separation between:

```text
NORMAL
```

and:

```text
CORNER
```

behavior.

---

## 16. What Did Not Yet Exist

Phase 2 was still an intermediate development stage.

The robot did not yet have the complete current architecture.

Systems that were not yet mature included:

```text
Pixy2.1 obstacle perception

target relevance ranking

target confirmation and lock

Red / Green pillar state logic

PASS_CONFIRM

post-pillar RECOVER

full control arbitration

mature color-event lifecycle

dedicated parking state machine
```

Those capabilities were developed through the later sensor, vision, and software phases.

---

## 17. Main Phase 2 Engineering Lessons

Phase 2 produced several important conclusions.

### Lesson 1 — Mechanics affect software

```text
steering geometry
→ changes control response
```

The vehicle could not be tuned reliably without understanding the physical steering system.

---

### Lesson 2 — Sensor position determines sensor meaning

```text
ultrasonic value
```

is only useful when the software understands:

```text
where the sensor is mounted
```

and:

```text
what geometry it is actually measuring
```

---

### Lesson 3 — Two-sided information is stronger

```text
one distance
→ proximity
```

while:

```text
left + right
→ geometric context
```

This insight strongly influenced the final ultrasonic architecture.

---

### Lesson 4 — Floor colors are events

The Color Sensor became more useful when markings were considered:

```text
physical course landmarks
```

instead of isolated readings.

---

### Lesson 5 — Early corrections are preferable

A navigation controller should ideally prevent Piolín from reaching a dangerous condition rather than waiting until a collision is almost unavoidable.

---

## 18. What Was Preserved into Later Phases

Several Phase 2 design decisions became permanent features of Piolín.

Most importantly:

```text
LEGO EV3 BRICK
→ remained main controller
```

```text
MOTOR A
→ propulsion
```

```text
MOTOR B
→ steering
```

```text
ACKERMANN
→ remained steering architecture
```

```text
S4 COLOR SENSOR
→ remained floor sensor
```

and the growing preference for:

```text
LATERAL COURSE GEOMETRY
```

continued into the final two-ultrasonic arrangement.

These were not temporary experiments.

They became structural foundations for later versions.

---

## 19. What Continued to Change

Other parts of Phase 2 were still experimental.

These included:

```text
exact ultrasonic placement

number of useful distance sensors

corner detection

navigation tuning

steering correction strength

course-event handling

orientation sensing
```

The next development phase would investigate these problems alongside a much larger new challenge:

```text
VISUAL OBSTACLE PERCEPTION
```

---

## 20. Phase 1 to Phase 2 Comparison

| Engineering Area | Phase 1 | Phase 2 |
|---|---|---|
| Controller | EV3 | EV3 |
| Main objective | Basic autonomous prototype | Vehicle-specific navigation development |
| Structure | Initial LEGO prototype | More deliberate vehicle architecture |
| Steering | Early configuration | Ackermann development |
| Propulsion | Basic EV3 actuation | Dedicated Motor A propulsion |
| Steering actuator | Early EV3 actuation | Dedicated Motor B steering |
| Distance sensing | Simple early sensing | Multi-position ultrasonic experimentation |
| Navigation information | Limited distance information | Increasing use of lateral geometry |
| Floor sensor | Not mature | Color Sensor integration |
| Direction logic | Early/manual concepts | Blue/Orange course-direction development |
| Navigation control | Basic reactive behavior | Increasingly geometric correction |
| Corners | Basic testing | Dedicated corner problem identified |
| Vision | None | Not yet mature |
| Parking | Not developed | Not yet dedicated subsystem |

---

## 21. Phase 2 Architecture Summary

The Phase 2 architecture can be summarized as:

```text
                     EV3 BRICK
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
    ULTRASONIC       COLOR SENSOR      CONTROL
      SENSING             │             LOGIC
          │               │              │
          ▼               ▼              │
      DISTANCE       FLOOR MARKS          │
      GEOMETRY             │              │
          └───────────┬────┘              │
                      ▼                   │
                NAVIGATION STATE          │
                      │                   │
                      └─────────┬─────────┘
                                ▼
                        STEERING REQUEST
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
                 MOTOR A                  MOTOR B
                PROPULSION              STEERING
                    │                       │
                    ▼                       ▼
             REAR DRIVETRAIN       ACKERMANN FRONT
                    │                       │
                    └───────────┬───────────┘
                                ▼
                         PIOLÍN MOVEMENT
```

This architecture was still evolving, but it introduced many of the physical ideas that remain visible in the current robot.

---

## 22. Transition to Phase 3

By the end of Phase 2, Piolín had evolved substantially from the initial prototype.

The development progression was:

```text
PHASE 1
INITIAL EV3 PROTOTYPE
        │
        ├── Basic movement
        ├── Initial sensing
        └── Early autonomous control
        │
        ▼
PHASE 2
MECHANICAL + NAVIGATION DEVELOPMENT
        │
        ├── Ackermann steering
        ├── Dedicated propulsion / steering
        ├── Ultrasonic geometry experiments
        ├── Color Sensor integration
        ├── Direction detection
        └── More structured navigation
        │
        ▼
PHASE 3
SENSOR + VISION EXPERIMENTATION
```

Phase 3 would expand the problem from:

```text
Where am I relative to the track?
```

to also include:

```text
What object am I approaching?

Is it Red or Green?

Which side must I pass?

How do I combine vision with navigation?
```

This transition introduced one of the most experimental periods in Piolín's development.

---

## Phase 2 Status

```text
PHASE:       2
STATUS:      LEGACY DEVELOPMENT PHASE
CONTROLLER:  LEGO MINDSTORMS EV3
FOCUS:       MECHANICS + NAVIGATION
PREDECESSOR: PHASE 1
SUCCESSOR:   PHASE 3
```

Phase 2 is preserved because it documents the stage in which Piolín's current mechanical identity began to emerge.

The central Phase 2 engineering principle was:

> **Reliable autonomous navigation required PiolínTech to design the mechanics, steering geometry, sensor placement, and software control as one interacting vehicle system rather than as independent components.**

---

<div align="center">

### [← Phase 1](Phase1.md) · [Evolution Overview](README.md) · [Phase 3 →](Phase3.md)

</div>
