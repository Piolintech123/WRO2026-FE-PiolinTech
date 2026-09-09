# Phase 3 — Sensor, Vision, and Control Experimentation
<img width="960" height="1280" alt="image" src="https://github.com/user-attachments/assets/56fffe03-1cff-4e25-8722-89304af1c113" />

## 1. Expanding Piolín Beyond Basic Navigation

Phase 3 represents one of the most experimental stages in Piolín's development for WRO Future Engineers 2026.

By this point, the project had already progressed beyond the initial EV3 prototype and had established several important mechanical ideas, including:

```text
LEGO MINDSTORMS EV3 as the main controller

Motor A for propulsion

Motor B for steering

Ackermann-style front steering

ultrasonic navigation experiments

downward Color Sensor integration
```

The next challenge was significantly more complex.

Piolín no longer needed only to answer:

```text
Where am I relative to the track?
```

It also needed to answer:

```text
What object is ahead?

Is it Red or Green?

Which side must I pass?

When has the pillar actually been cleared?

How should I recover afterward?
```

Phase 3 therefore became the main **sensor, vision, and control experimentation phase**.

<div align="center">

<img
  src="https://github.com/user-attachments/assets/56fffe03-1cff-4e25-8722-89304af1c113"
  alt="Piolín during Phase 3 development"
  width="650"
/>

<br>

<sub><b>Figure 1.</b> Piolín during the Phase 3 sensor, vision, and navigation development period.</sub>

</div>

---

## 2. Phase 3 Engineering Objective

The central objective of Phase 3 was not to create one fixed configuration immediately.

Instead, the team deliberately tested different approaches to determine which combination of sensors and software produced the most useful information for autonomous navigation.

The development process can be summarized as:

```text
MECHANICAL PLATFORM FROM PHASE 2
              ↓
TEST SENSOR CONFIGURATIONS
              ↓
TEST ORIENTATION SENSING
              ↓
TEST CAMERA-BASED PERCEPTION
              ↓
TEST OBSTACLE REACTIONS
              ↓
OBSERVE FAILURE MODES
              ↓
SIMPLIFY ARCHITECTURE
              ↓
DEFINE REQUIREMENTS FOR PHASE 4
```

Several Phase 3 configurations were temporary.

This is important:

> **A sensor or architecture appearing during Phase 3 does not mean that it became part of the final robot.**

Phase 3 documents experimentation.

Phase 4 documents the current competition architecture.

---

# 3. The EV3 Remained the Computing Core

Piolín has remained an EV3-based robot throughout its development.

Phase 3 did **not** replace the EV3 with:

```text
Raspberry Pi

external motor controllers

custom GPIO electronics

non-LEGO drive electronics
```

The LEGO MINDSTORMS EV3 continued to provide:

```text
central program execution

sensor communication

Motor A control

Motor B control

encoder feedback
```

This continuity allowed PiolínTech to improve the robot by refining:

```text
sensor selection

mechanical geometry

software architecture

control logic
```

rather than repeatedly replacing the central platform.

---

# 4. Sensor Architecture Experimentation

One of the main Phase 3 questions was:

> **Which sensors provide useful information for each part of the competition?**

Different arrangements were tested during development.

These included experiments involving:

```text
lateral ultrasonic sensing

forward-distance sensing

gyro orientation sensing

floor-color detection

camera-based pillar detection
```

Not all sensors were kept.

This experimentation helped distinguish between sensors that were:

```text
useful in theory
```

and sensors that were:

```text
useful on Piolín's actual physical geometry
```

That difference became extremely important later.

---

## Ultrasonic Sensor Experiments

The team experimented with different ultrasonic positions and roles.

At different points, the design considered information such as:

```text
front obstacle distance

left wall distance

right wall distance

inner wall relationship

outer wall relationship
```

A major lesson was that adding more sensors does not automatically create better navigation.

Each additional sensor introduces:

```text
another measurement

another mounting constraint

another interpretation problem

another possible controller interaction
```

The most useful long-term information came from understanding Piolín's **lateral relationship with the course**.

This eventually contributed to the current permanent convention:

```text
S2 = LEFT Ultrasonic

S3 = RIGHT Ultrasonic
```

but Phase 3 included the experiments that helped reach that decision.

---

# 5. Orientation and Gyro Experiments

Another development direction involved using an EV3 Gyro Sensor to obtain orientation information.

The gyro offered something fundamentally different from the ultrasonic sensors.

```text
ULTRASONICS
→ relationship with nearby surfaces
```

```text
GYRO
→ relationship with heading / rotation
```

This distinction became particularly useful when studying corners.

During a corner:

```text
vehicle rotates
      ↓
ultrasonic beams rotate
      ↓
visible wall geometry changes
```

The gyro could provide an independent indication that Piolín itself had rotated.

This eventually became important enough that gyro sensing was selected for the current **Open Challenge** architecture in Phase 4.

---

# 6. Vision Became Necessary

The Obstacle Challenge introduced a problem that distance sensing alone could not solve.

An ultrasonic sensor may report:

```text
object nearby
```

but the WRO rules require Piolín to distinguish:

```text
RED PILLAR
→ PASS RIGHT
```

from:

```text
GREEN PILLAR
→ PASS LEFT
```

Therefore, Phase 3 introduced camera-based perception as a major development area.

The vision problem was separated into two questions:

```text
WHAT COLOR IS THE OBJECT?
```

and:

```text
WHERE IS THE OBJECT IN THE CAMERA IMAGE?
```

This distinction later became fundamental to the obstacle architecture.

---

# 7. HuskyLens + Arduino Nano Experiment

One of the important Phase 3 experiments used a **HuskyLens** camera together with an **Arduino Nano**.

The objective was to allow an external vision sensor to identify obstacle colors and communicate useful information back to the EV3.

The experimental architecture was conceptually:

```text
PILLAR
   ↓
HUSKYLENS
   ↓
ARDUINO NANO
   ↓
EV3
   ↓
NAVIGATION LOGIC
```

This architecture demonstrated that external vision could be integrated with Piolín.

However, it also introduced additional layers:

```text
camera
+
microcontroller
+
communication interface
+
EV3 software
```

Every additional layer created another possible source of:

```text
communication failure

configuration error

debugging complexity

latency

wiring difficulty
```

The HuskyLens + Nano architecture therefore became valuable engineering evidence, but it was eventually classified as **legacy** rather than the final solution.

---

## What the HuskyLens Experiment Taught Us

The most important lesson was not simply whether HuskyLens could detect a color.

It was that:

```text
DETECTION
≠
RELIABLE NAVIGATION
```

A camera could correctly identify a pillar while Piolín still made the wrong physical maneuver.

This led to a deeper diagnostic chain:

```text
Did camera detect the pillar?
        ↓
Was the color interpreted correctly?
        ↓
Was the correct passing rule selected?
        ↓
Did the controller request the correct direction?
        ↓
Did another controller interfere?
        ↓
Did Motor B physically produce the expected steering?
```

This became one of the foundations of the later layered architecture.

---

# 8. Transition Toward Pixy2.1

Phase 3 also included testing of the **Pixy2.1** vision sensor.

Pixy2.1 provided color-signature and bounding-box information that could be used by Piolín's software.

Useful information included:

```text
signature

x

y

width

height
```

The important architectural idea was:

```text
CAMERA
→ provide perception information
```

not:

```text
CAMERA
→ directly command steering
```

The software could instead use the camera output to build a more structured decision.

This eventually contributed to the current signature convention:

```text
sig1
→ Pink
→ Parking
```

```text
sig2
→ Red
→ PASS RIGHT
```

```text
sig3
→ Green
→ PASS LEFT
```

The current direct Pixy2.1-to-EV3 S1 installation belongs to **Phase 4**, but its selection was the result of the vision experiments performed during Phase 3.

---

# 9. The Left/Right Obstacle Problem

One of the most important software lessons from Phase 3 involved the meaning of:

```text
LEFT
```

and:

```text
RIGHT
```

during obstacle avoidance.

A pillar may appear:

```text
left of the camera

centered

right of the camera
```

but this does **not** change the competition rule.

The rule remains:

```text
RED
→ PASS RIGHT
```

```text
GREEN
→ PASS LEFT
```

The pillar's image coordinate answers:

```text
Where is the target?
```

while its signature answers:

```text
Which side must Piolín pass?
```

Mixing these two concepts could create apparently inverted behavior.

The stronger architecture therefore became:

```text
SIGNATURE
→ determines required side
```

```text
x / y / width / height
→ describe target geometry
```

This separation was a major improvement in Piolín's obstacle reasoning.

---

# 10. From Immediate Reaction to Target Handling

Early vision experiments could behave conceptually like:

```text
camera sees Red
→ steer immediately
```

This created problems when:

```text
detections flickered

several blocks were visible

the target temporarily disappeared

the camera changed angle during steering
```

Phase 3 therefore revealed the need for a target lifecycle.

The concept evolved toward:

```text
DETECT
   ↓
VALIDATE
   ↓
SELECT
   ↓
CONFIRM
   ↓
LOCK
   ↓
AVOID
   ↓
VERIFY PASS
   ↓
RELEASE
```

This was a major conceptual step toward the Phase 4 perception architecture.

It also solved an important problem:

```text
one camera frame
```

should not automatically have enough authority to create:

```text
one maximum steering maneuver
```

---

# 11. Controller Conflict

Another major Phase 3 problem occurred when different systems tried to control Motor B simultaneously.

For example:

```text
RED pillar controller
→ RIGHT
```

while:

```text
wall-following controller
→ LEFT
```

A naive implementation could combine both requests.

The result might be:

```text
weak obstacle reaction

zig-zag

late avoidance

wrong physical passing side

steering that remains stuck after a maneuver
```

This revealed a fundamental architecture problem.

Piolín has:

```text
many possible navigation objectives
```

but only:

```text
one steering actuator
```

Therefore, later software needed a way to decide:

> **Which controller has authority right now?**

This Phase 3 failure directly motivated the Phase 4 control hierarchy:

```text
CRITICAL SAFETY
      ↓
ACTIVE MANEUVER
      ↓
NORMAL NAVIGATION
```

---

# 12. The Need for Recovery

Another important discovery was that avoiding the pillar was only half of the maneuver.

After Piolín moved around an obstacle, it could be left:

```text
angled toward a wall

too far from the normal corridor

still holding obstacle steering

poorly positioned for the next pillar
```

Therefore:

```text
PILLAR PASSED
```

could not automatically mean:

```text
RETURN IMMEDIATELY TO NORMAL
```

The team began treating recovery as its own objective:

```text
AVOID
   ↓
CLEAR PILLAR
   ↓
COUNTERSTEER
   ↓
REACQUIRE COURSE GEOMETRY
   ↓
STABILIZE
   ↓
NORMAL
```

This later became the dedicated:

```text
RECOVER
```

state.

---

# 13. Temporary Camera Loss

Phase 3 testing also showed that the camera does not necessarily see the target continuously throughout a maneuver.

As Piolín turns:

```text
robot rotates
      ↓
camera rotates
      ↓
pillar moves across image
      ↓
pillar may leave field of view
```

Therefore:

```text
TARGET NOT VISIBLE
```

does not necessarily mean:

```text
TARGET PASSED
```

Immediately cancelling obstacle steering when the target disappears could cause Piolín to turn back into the pillar.

The more robust strategy became:

```text
remember active target
+
maintain committed passing side
+
use physical context
+
confirm clearance
```

before releasing the maneuver.

This later became part of the:

```text
PASS_CONFIRM
```

concept.

---

# 14. Floor Sensing Also Became More Structured

The S4 Color Sensor continued to evolve during this phase.

Earlier logic could interpret every loop reading as a new detection.

However:

```text
BLUE
BLUE
BLUE
BLUE
```

while crossing one physical strip should still mean:

```text
ONE EVENT
```

This motivated stronger event handling:

```text
CLASSIFY
   ↓
CONFIRM
   ↓
LATCH
   ↓
COUNT ONCE
   ↓
WAIT FOR NEUTRAL
   ↓
RELEASE
   ↓
RE-ARM
```

This event-based approach later became part of the current Phase 4 course-progress system.

---

# 15. What Did Not Work Well Enough

Phase 3 produced several approaches that were useful experimentally but were not selected as the final architecture.

| Experimental Approach | Limitation Observed | Engineering Response |
|---|---|---|
| More sensors simply for more data | Increased complexity without always improving navigation | Keep sensors with clearly defined roles |
| Forward-distance emphasis | Less useful for continuous lateral course positioning | Prioritize lateral S2/S3 geometry |
| HuskyLens + Nano bridge | Additional communication and integration layers | Move toward direct Pixy2.1 integration |
| Camera directly affecting steering | Unstable reaction to individual detections | Separate perception from control |
| Target choice based only on first visible block | Could select the wrong visual object | Develop relevance-based selection |
| Image `x` used as passing-side logic | Could invert Red/Green behavior | Signature defines passing side |
| Releasing target immediately after visual loss | Maneuver could end before physical clearance | Develop `PASS_CONFIRM` |
| Returning directly to normal after obstacle | Poor course position after passing | Add dedicated recovery behavior |
| Multiple controllers influencing steering equally | Controllers could fight each other | Develop control arbitration |
| Raw color samples counted directly | Duplicate course counts | Develop event confirmation and latching |

These experiments were not wasted work.

Each one exposed a specific architectural weakness that influenced the next version.

---

# 16. Phase 3 Architecture Evolution

The progression of Phase 3 can be summarized as:

```text
PHASE 2 VEHICLE
      ↓
COURSE NAVIGATION
      ↓
SENSOR PLACEMENT EXPERIMENTS
      ↓
GYRO EXPERIMENTS
      ↓
VISION REQUIRED
      ↓
HUSKYLENS + NANO
      ↓
VISION / CONTROL PROBLEMS
      ↓
PIXY2.1 EXPERIMENTS
      ↓
TARGET VALIDATION
      ↓
TARGET LOCK
      ↓
PASS CONFIRMATION
      ↓
RECOVERY
      ↓
CONTROLLER PRIORITY
      ↓
SIMPLIFIED SENSOR ROLES
      ↓
PHASE 4 ARCHITECTURE
```

The most important result of this phase was not one particular sensor.

It was the realization that reliable autonomous navigation required clear separation between:

```text
SENSING

PERCEPTION

DECISION

CONTROL

ACTUATION
```

---

# 17. Phase 2 → Phase 3 → Phase 4

| Engineering Area | Phase 2 | Phase 3 | Phase 4 |
|---|---|---|---|
| Main controller | EV3 | EV3 | **EV3** |
| Steering | Ackermann development | Refinement/testing | **Ackermann, Motor B** |
| Propulsion | Motor A architecture | Refined | **Motor A** |
| Ultrasonics | Placement/navigation development | Multiple role experiments | **S2 LEFT + S3 RIGHT** |
| Color Sensor | Course-mark integration | Event-processing development | **S4 event system** |
| Gyro | Early/partial orientation work | Evaluated for heading | **S1 in Open** |
| Vision | Not mature | HuskyLens/Nano + Pixy experimentation | **S1 Pixy2.1 in Obstacles** |
| Target handling | Not developed | Detection/lock concepts emerge | **Structured perception architecture** |
| Obstacle avoidance | Early | Extensive experimentation | **State-based maneuver architecture** |
| Pass confirmation | Not mature | Need identified | **Dedicated logic** |
| Recovery | Not mature | Need identified | **Dedicated `RECOVER` behavior** |
| Arbitration | Not mature | Controller conflicts identified | **Explicit control priority** |
| Parking | Early/experimental | Requirements developed | **Dedicated subsystem under development** |

---

# 18. Transition to Phase 4

By the end of Phase 3, one of the strongest conclusions was that Piolín did **not** need every sensor active simultaneously.

Instead, the two WRO rounds required different information.

This led to the round-specific architecture:

```text
                 PIOLÍN
                    │
              COMMON HARDWARE
                    │
       ┌────────────┴────────────┐
       │                         │
       ▼                         ▼
      OPEN                   OBSTACLES
       │                         │
       ▼                         ▼
   S1 = GYRO               S1 = PIXY2.1
       │                         │
       └────────────┬────────────┘
                    │
              S2 = LEFT US
              S3 = RIGHT US
              S4 = COLOR
```

This was a major simplification.

Instead of asking:

```text
How can every sensor fit into one universal configuration?
```

the design asked:

```text
What information does each competition round actually require?
```

The answer became the basis of **Phase 4**.

---

## Phase 3 Status

```text
PHASE:       3
STATUS:      LEGACY DEVELOPMENT PHASE
CONTROLLER:  LEGO MINDSTORMS EV3
FOCUS:       SENSOR + VISION + CONTROL EXPERIMENTATION
PREDECESSOR: PHASE 2
SUCCESSOR:   PHASE 4 — CURRENT
```

Phase 3 is preserved because it explains **why the current architecture exists**.

Its central engineering lesson was:

> **Reliable autonomy did not come from adding as many sensors or reactions as possible. It came from giving each sensor a clear responsibility, separating perception from control, maintaining maneuver context, and simplifying the architecture until every important decision could be traced from measurement to physical motion.**

---

<div align="center">

### [← Phase 2](Phase2.md) · [Evolution Overview](README.md) · [Phase 4 →](Phase4.md)

</div>
