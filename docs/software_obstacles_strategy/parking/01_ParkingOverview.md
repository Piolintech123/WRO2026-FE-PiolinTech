# Parking System Overview

<div align="center">

<img
  src="../../../v-photos/v4/parking_area.jpg"
  alt="Parking area used by Piolín at the end of the course"
  width="720"
/>

<br>

<sub><b>Figure 1.1.</b> Parking is treated as a dedicated final navigation maneuver rather than as an extension of normal driving.</sub>

</div>

Parking is the final autonomous maneuver of Piolín's competition run.

The parking system is not designed around a single sensor condition such as:

```text
Pink detected
→ stop
```

Instead, PiolínTech treats parking as a **high-level state that becomes available only after the robot has accumulated enough evidence that the course has been completed and the parking region is physically relevant**.

For the Obstacle Challenge, the intended parking architecture combines:

```text
COURSE PROGRESSION
        +
PIXY2.1 PINK REFERENCE
        +
LATERAL ULTRASONIC GEOMETRY
        +
MOTOR A ENCODER PROGRESSION
        ↓
PARKING MANEUVER
```

This is intentionally different from allowing one sensor to control the complete maneuver.

The current software still requires physical calibration of the final trajectory, stopping point, alignment, and parking-release conditions. Therefore this document defines the **parking architecture and engineering strategy**, while temporary values from development code are identified as prototype parameters rather than final specifications.

---

## 1. Parking as a Dedicated State

During most of the run, Piolín is solving problems such as:

```text
drive through straight section

follow usable track geometry

detect pillar

pass Red or Green obstacle

recover

handle corner

count course progress
```

Parking has a different objective.

Instead of preparing for another section of track, the vehicle must:

```text
identify that the run is ending

identify the parking region

enter it with a controlled trajectory

align itself

move to the intended final position

stop completely
```

For this reason, parking should have its own state:

```text
PARKING
```

rather than being implemented as a special case inside:

```text
NORMAL
```

or:

```text
AVOID
```

The high-level sequence becomes:

```text
NORMAL COURSE STATES
        ↓
required progression reached
        ↓
PARKING ELIGIBLE
        ↓
parking reference confirmed
        ↓
PARKING
        ↓
alignment / final movement
        ↓
STOP
```

This prevents the robot from accidentally entering parking logic during an earlier part of the course.

---

## 2. Current Parking Sensors

During the Obstacle Challenge, parking can use the same active hardware already installed for navigation:

```text
S1 → Pixy2.1

S2 → LEFT Ultrasonic Sensor

S3 → RIGHT Ultrasonic Sensor

S4 → Color Sensor

Motor A → propulsion + encoder

Motor B → Ackermann steering
```

Each component contributes different information.

| Device | Parking Role |
| :--- | :--- |
| Pixy2.1 | Detect the Pink parking reference |
| S2 LEFT Ultrasonic | Measure left-side physical geometry |
| S3 RIGHT Ultrasonic | Measure right-side physical geometry |
| S4 Color Sensor | Provide accumulated course-progress information |
| Motor A encoder | Measure vehicle progression during final movement |
| Motor B encoder/control | Execute and verify steering position |

The parking system therefore follows the same software philosophy used elsewhere in Piolín:

> **Each sensor answers a specific physical question rather than one sensor being expected to solve the complete maneuver.**

---

## 3. Pink as a Parking Reference

<div align="center">

<img
  src="../../../v-photos/v4/pixy21_parking_detection.jpg"
  alt="Pixy2.1 detecting Piolín's Pink parking reference"
  width="690"
/>

<br>

<sub><b>Figure 1.2.</b> Pixy signature 1 is reserved for the Pink parking reference and is separate from Red and Green obstacle recognition.</sub>

</div>

The current Pixy2.1 signature convention is:

```text
sig1 → Pink → parking

sig2 → Red → obstacle, pass RIGHT

sig3 → Green → obstacle, pass LEFT
```

Pink must remain outside the normal obstacle-selection process.

Conceptually:

```python
def is_obstacle(signature):
    return signature in (2, 3)

def is_parking_reference(signature):
    return signature == 1
```

This separation prevents:

```text
Pink
```

from accidentally producing:

```text
Red/Green avoidance behavior
```

However, detecting Pink alone should **not** immediately start parking.

A Pink object could potentially become visible before the vehicle has completed the required course progression.

The stronger condition is:

```text
Pink detected
+
parking is currently allowed
```

before it becomes relevant to navigation.

---

## 4. Parking Eligibility from Course Progress

Piolín's current development architecture counts confirmed Blue and Orange floor events using S4.

The current full-course model uses:

```text
12 accepted course events
```

as the intended progression reference for:

```text
3 laps / 12 corners
```

A development prototype already demonstrates the transition:

```python
if line_count >= LINES_TO_PARK:
    parking_active = True
```

with:

```python
LINES_TO_PARK = 12
```

This is an important architectural idea.

Parking should not be triggered by:

```text
Pixy alone
```

but should first become **eligible** through course state.

Conceptually:

```python
parking_eligible = (
    course_count >= REQUIRED_COURSE_EVENTS
)
```

Then:

```python
if parking_eligible and pink_confirmed:
    state = PARKING
```

This creates two independent forms of evidence:

```text
Have we completed the course?
```

and:

```text
Can we now identify the parking reference?
```

Only when both become consistent should Piolín commit to the final maneuver.

---

## 5. Why Parking Should Not Depend on Time Alone

A time-based system could attempt:

```text
run for N seconds
→ start parking
```

but elapsed time changes according to:

```text
obstacle placement

avoidance duration

corner behavior

recovery duration

battery condition

drive speed

temporary safety corrections
```

Two successful runs can therefore reach the same physical point at different times.

Course-progress events provide a stronger reference:

```text
physical track landmarks
→ confirmed progress
→ parking eligibility
```

Time can still be useful as:

```text
timeout

diagnostic value

safety fallback
```

but should not be the primary evidence that the course is complete.

---

## 6. Parking Detection Should Also Be Confirmed

The Pink reference should follow the same perception philosophy as Red and Green obstacles:

```text
one camera observation
≠
immediate committed maneuver
```

The intended process is:

```text
sig1 appears
      ↓
valid Pink candidate
      ↓
confirm detection
      ↓
check parking eligibility
      ↓
lock parking target
      ↓
PARKING
```

Conceptually:

```python
if parking_eligible:

    if candidate.signature == PARKING_SIG:
        parking_confirmations += 1

    else:
        parking_confirmations = 0

    if parking_confirmations >= REQUIRED_CONFIRMATIONS:
        state = PARKING
```

This is architectural example code.

The final number of confirmations should be determined through real testing at competition speed.

The trade-off is the same as with obstacle targets:

```text
too few confirmations
→ sensitive to unstable detections
```

```text
too many confirmations
→ late parking reaction
```

---

## 7. Transitioning from Navigation to Parking

The transition into `PARKING` should deliberately disable or reduce navigation behaviors that are no longer useful.

Before parking, the robot may be executing:

```text
NORMAL wall navigation

RECOVER

corner exit
```

Once parking is committed, the objective changes.

The controller should no longer behave as if it were preparing for another obstacle.

Conceptually:

```text
COURSE NAVIGATION
      ↓
parking conditions confirmed
      ↓
finish current safe transition
      ↓
PARKING state
      ↓
parking controller receives trajectory authority
```

The state machine should therefore prevent:

```text
new Red/Green target
```

from unnecessarily replacing a confirmed final parking objective.

Likewise, normal wall-centering should not continuously fight the parking trajectory.

Critical wall protection may remain active where useful.

---

## 8. Parking Trajectory

A useful parking maneuver can be divided into four physical phases:

```text
1. APPROACH

2. ENTRY

3. ALIGNMENT

4. FINAL POSITION
```

### Approach

The robot identifies the parking area and begins reducing uncertainty.

The controller can use:

```text
Pink visual geometry

current steering

S2 / S3 distances

vehicle progression
```

to prepare a stable entry.

### Entry

Piolín steers into the parking space.

Because the robot uses Ackermann-style steering:

```text
Motor B angle
+
Motor A movement
→ curved vehicle trajectory
```

The robot cannot translate sideways directly.

The software must therefore create enough longitudinal distance for the chassis to move into the desired final position.

### Alignment

After entering, Piolín may need a controlled countersteer or steering reduction to become more parallel to the intended final orientation.

### Final Position

Motor A advances or reverses only as far as required to reach the calibrated stopping location.

The exact trajectory remains under physical development.

---

## 9. Using Pixy Geometry During Parking

The Pink target can provide more than a Boolean:

```text
Pink visible / not visible
```

Pixy can also provide:

```text
x

y

width

height
```

These values can help determine whether the parking reference is:

```text
far from the camera center

becoming aligned

becoming visually larger

moving across the field of view
```

A future parking controller may therefore use:

```text
Pink signature
→ confirms target identity
```

and:

```text
Pink x
→ contributes to entry/alignment correction
```

while:

```text
Pink size
→ contributes to target relevance/progression
```

However:

```text
Pixy width
```

should not be presented as an exact parking distance unless that relationship has been physically calibrated.

The camera provides visual geometry, not a direct millimeter measurement.

---

## 10. Ultrasonic Role During Parking

<div align="center">

<img
  src="../../../v-photos/v4/piolin_obstacle_top.jpg"
  alt="Top view of Piolín showing the forward Pixy2.1 and lateral ultrasonic sensors"
  width="720"
/>

<br>

<sub><b>Figure 1.3.</b> Parking combines forward visual information with lateral physical geometry from S2 and S3.</sub>

</div>

The permanent lateral sensors remain:

```text
S2 = LEFT

S3 = RIGHT
```

During parking, they can help answer:

```text
Is Piolín becoming too close to the left boundary?

Is Piolín becoming too close to the right boundary?

Is the lateral geometry becoming more balanced?

Has the robot entered a repeatable physical parking region?
```

The ultrasonic sensors are particularly valuable because the camera may lose some geometric context as the robot turns.

The intended sensor fusion is:

```text
PIXY
→ visual parking reference
```

plus:

```text
S2 / S3
→ physical lateral clearance
```

plus:

```text
ENCODER
→ longitudinal progression
```

This gives the parking controller independent information about several dimensions of the maneuver.

---

## 11. Encoder-Based Final Movement

The development Open controller already demonstrates another useful parking principle: once parking is activated, Motor A encoder progression can be used to control an additional final movement.

The prototype currently contains:

```python
PARK_EXTRA_DEG = 300.0
```

and records a reference encoder position when entering parking.

Architecturally:

```text
enter PARKING
      ↓
store Motor A encoder
      ↓
perform final controlled travel
      ↓
required encoder progression reached
      ↓
stop
```

This is stronger than:

```text
wait N milliseconds
→ stop
```

because Motor A progression is related to actual drivetrain movement.

However:

```text
PARK_EXTRA_DEG = 300
```

is a **development parameter**, not a final parking specification.

The final encoder distance must be calibrated against:

```text
actual parking geometry

entry trajectory

wheel behavior

final stopping objective
```

before being documented as a validated value.

---

## 12. Parking Stop Condition

A final stop should ideally require a combination of state and physical evidence.

The weakest condition would be:

```text
Pink visible
→ stop
```

A stronger architecture is:

```text
parking state active
+
entry complete
+
final progression reached
+
geometry acceptable
      ↓
STOP
```

Conceptually:

```python
if (
    state == PARKING
    and parking_entry_complete
    and final_encoder_reached
    and parking_geometry_valid
):
    state = STOP
```

The exact `parking_geometry_valid` criterion remains under development.

Once `STOP` is reached, the software should deliberately command:

```text
Motor A → stop

Motor B → hold or safe final steering position
```

and should not automatically return to:

```text
NORMAL
```

because parking represents the terminal state of the run.

The state sequence is therefore:

```text
PARKING
   ↓
STOP
```

not:

```text
PARKING
   ↓
NORMAL
```

---

## 13. Parking Failure Diagnosis

Parking problems should be separated according to the stage where behavior first becomes incorrect.

| Symptom | First Area to Inspect |
| :--- | :--- |
| Parking begins before course completion | Course-count / eligibility logic |
| Pink is visible but parking never begins | Pixy sig1 detection / confirmation |
| Red or Green treated as parking | Signature mapping |
| Pink causes obstacle avoidance | Target filtering |
| Correct parking target but entry goes wrong direction | Steering sign / parking trajectory |
| Entry begins too late | Pink relevance / confirmation / speed |
| Piolín enters but remains angled | Alignment phase |
| Piolín enters correctly but overshoots | Final encoder distance / braking |
| Piolín stops too early | Final progression condition |
| Piolín hits wall during entry | Entry geometry / wall safety |
| Robot exits parking state afterward | Terminal `STOP` logic |

The diagnostic sequence should be:

```text
COURSE COMPLETE?
       ↓
PINK DETECTED?
       ↓
PARKING CONFIRMED?
       ↓
ENTRY COMMAND CORRECT?
       ↓
ALIGNMENT CORRECT?
       ↓
FINAL DISTANCE CORRECT?
       ↓
STOP?
```

This prevents one failed final position from causing unnecessary changes to earlier detection logic.

---

## 14. Current Development Status

The parking architecture is defined more clearly than the final maneuver geometry.

Current established concepts include:

```text
parking is a dedicated state

course progression gates parking eligibility

Pixy sig1 identifies Pink

Pink is separate from Red/Green obstacle detection

S2 remains LEFT

S3 remains RIGHT

ultrasonics can provide lateral parking context

Motor A encoder can provide final progression evidence

parking ends in STOP
```

Current development values include:

```text
LINES_TO_PARK = 12

PARK_EXTRA_DEG = 300
```

but these must be interpreted differently.

```text
LINES_TO_PARK = 12
```

matches the current intended:

```text
3 laps / 12 course events
```

progression model.

By contrast:

```text
PARK_EXTRA_DEG = 300
```

is a prototype movement value and remains subject to physical calibration.

Still under development are:

```text
final Pink confirmation threshold

parking target relevance

entry steering profile

entry speed

alignment strategy

final encoder travel

final ultrasonic geometry criteria

final stopping tolerance
```

The repository should continue distinguishing these tunable parameters from the stable high-level architecture.

---

## 15. Intended Parking Pipeline

The final conceptual system is:

```text
                     COURSE NAVIGATION
                            │
                            ▼
                   COURSE COUNT UPDATED
                            │
                            ▼
                 REQUIRED PROGRESS REACHED?
                            │
                           YES
                            │
                            ▼
                    PARKING ELIGIBLE
                            │
                            ▼
                      PIXY sig1?
                            │
                           YES
                            │
                            ▼
                   CONFIRM PINK TARGET
                            │
                            ▼
                     LOCK PARKING
                            │
                            ▼
                         PARKING
                            │
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
          PIXY x          S2 / S3       MOTOR A
       visual target      clearances      encoder
             │              │              │
             └──────────────┼──────────────┘
                            ▼
                         APPROACH
                            │
                            ▼
                           ENTRY
                            │
                            ▼
                        ALIGNMENT
                            │
                            ▼
                     FINAL MOVEMENT
                            │
                            ▼
                   final conditions met?
                            │
                           YES
                            │
                            ▼
                           STOP
```

This architecture prevents any single sensor from being treated as absolute proof that parking is complete.

---

## 16. Final Engineering Assessment

Piolín's parking strategy is designed as a **sensor-fused terminal maneuver**.

It begins only after the robot has accumulated sufficient course-progress evidence and then uses the Pink Pixy2.1 reference to identify the parking objective.

The intended logic is:

```text
COURSE PROGRESSION
        ↓
PARKING ELIGIBLE
        ↓
PINK TARGET
        ↓
CONFIRM / LOCK
        ↓
APPROACH
        ↓
ENTRY
        ↓
ALIGNMENT
        ↓
FINAL MOVEMENT
        ↓
STOP
```

The sensors maintain separate responsibilities:

```text
S4
→ course progression
```

```text
Pixy2.1 sig1
→ visual parking reference
```

```text
S2 / S3
→ lateral physical geometry
```

```text
Motor A encoder
→ longitudinal progression
```

This separation is especially important because:

```text
Pink detected
```

does not necessarily mean:

```text
course completed
```

and:

```text
course completed
```

does not necessarily mean:

```text
robot is already correctly positioned for parking
```

Both state information and physical evidence are required.

The current prototype values demonstrate that the software architecture already supports progression-triggered parking and encoder-based final travel, but the final trajectory and stopping parameters remain calibration tasks.

The central parking principle is:

> **Piolín should not park because one sensor says the parking area exists. It should first know that parking is logically allowed, confirm the physical parking reference, execute a dedicated entry and alignment maneuver, and stop only when the final physical progression is consistent with the intended parked state.**

This structure allows PiolínTech to tune parking detection, entry geometry, alignment, final movement, and stopping behavior independently without destabilizing the rest of the autonomous navigation system.

---

<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
