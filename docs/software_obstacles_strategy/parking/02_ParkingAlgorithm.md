# 2. Parking Algorithm

<div align="center">

<img
  src="../../../v-photos/v4/parking_area.jpg"
  alt="Parking area used for Piolín final maneuver development"
  width="720"
/>

<br>

<sub><b>Figure 2.1.</b> Piolín's parking algorithm separates eligibility, target acquisition, entry, alignment, final positioning, and stopping into distinct phases.</sub>

</div>

Piolín's parking algorithm is designed as a **terminal state machine** rather than a single steering command.

The robot should not perform:

```text
Pink detected
→ turn
→ stop
```

because seeing the parking reference does not prove that:

```text
the course is complete

Piolín is correctly positioned

the parking target is relevant

the vehicle is aligned

the final stopping position has been reached
```

Instead, the intended algorithm combines:

```text
course progression

Pixy2.1 parking detection

lateral ultrasonic geometry

Motor A encoder progression

Motor B steering control
```

through a sequence of controlled phases.

The high-level algorithm is:

```text
COURSE COMPLETE
      ↓
PARKING ENABLED
      ↓
PINK TARGET CONFIRMED
      ↓
APPROACH
      ↓
ENTRY
      ↓
ALIGNMENT
      ↓
FINAL POSITION
      ↓
STOP
```

The numerical thresholds for target relevance, steering, encoder travel, and stopping geometry remain calibration parameters.

---

## 2.1 Parking Activation Condition

Parking should remain disabled during the normal competition run.

Conceptually:

```python
parking_enabled = False
```

The current course-progress architecture uses confirmed S4 floor events to represent physical progress.

The present development model expects:

```text
12 accepted course events
```

for the complete:

```text
3 laps / 12 corners
```

sequence.

A current prototype already demonstrates this transition:

```python
if line_count >= LINES_TO_PARK:
    parking_active = True
```

with:

```python
LINES_TO_PARK = 12
```

For the final architecture, it is useful to distinguish:

```text
PARKING ELIGIBLE
```

from:

```text
PARKING ACTIVE
```

Conceptually:

```python
parking_eligible = (
    course_count >= REQUIRED_COURSE_EVENTS
)
```

This means:

```text
course complete
→ Piolín is now allowed to search for parking
```

but it does **not** yet mean:

```text
start steering into parking immediately
```

---

## 2.2 Confirming the Pink Parking Target

<div align="center">

<img
  src="../../../v-photos/v4/pixy21_parking_detection.jpg"
  alt="Pixy2.1 detecting the Pink parking reference"
  width="680"
/>

<br>

<sub><b>Figure 2.2.</b> Pixy signature 1 provides the visual parking reference after course progression has enabled the parking subsystem.</sub>

</div>

The current Pixy2.1 mapping is:

```text
sig1 → Pink → Parking

sig2 → Red → PASS RIGHT

sig3 → Green → PASS LEFT
```

The parking detector should therefore filter explicitly for:

```text
signature == 1
```

Conceptually:

```python
PARKING_SIG = 1

def is_parking_target(block):
    return (
        block is not None
        and block.signature == PARKING_SIG
    )
```

However, the target should only matter when:

```python
parking_eligible == True
```

The intended condition is:

```python
if parking_eligible and is_parking_target(candidate):
    # Begin confirmation.
```

This prevents an early Pink detection from interrupting obstacle navigation.

---

## 2.3 Parking Target Confirmation and Lock

One camera frame should not immediately commit Piolín to a terminal maneuver.

The parking target should follow the same:

```text
candidate
→ confirmation
→ lock
```

principle used elsewhere in Piolín's software.

A conceptual implementation is:

```python
if parking_eligible:

    if pink_visible:
        pink_confirmations += 1
    else:
        pink_confirmations = 0

    if pink_confirmations >= PARK_CONFIRMATIONS:
        parking_target_locked = True
```

The exact value of:

```python
PARK_CONFIRMATIONS
```

must be physically calibrated.

Once the Pink target is accepted:

```text
PINK CANDIDATE
      ↓
CONFIRMED
      ↓
LOCKED
```

Piolín should no longer allow an ordinary Red or Green detection to replace the parking objective.

Conceptually:

```python
if parking_target_locked:
    ignore_new_obstacle_target_selection = True
```

This does not necessarily mean Pixy stops reading other blocks.

It means:

```text
parking now owns the high-level navigation objective
```

---

## 2.4 Entering the PARKING State

Once:

```text
course progression is complete
+
Pink is confirmed
```

the state machine can transition:

```python
state = PARKING
```

At this transition, parking-specific variables should be initialized.

Conceptually:

```python
parking_phase = "APPROACH"

parking_start_encoder = drive.angle()

parking_target_locked = True

parking_complete = False
```

This initialization is important because the final maneuver may depend on:

```text
encoder distance traveled since parking started

current parking phase

last Pink position

current ultrasonic geometry
```

rather than global values accumulated throughout the complete run.

The transition should therefore create a new local reference frame for the final maneuver.

---

## 2.5 Parking Algorithm Phases

The intended algorithm divides `PARKING` into four internal phases:

```text
APPROACH
   ↓
ENTRY
   ↓
ALIGN
   ↓
FINAL
```

followed by:

```text
STOP
```

Conceptually:

```python
if state == PARKING:

    if parking_phase == "APPROACH":
        run_parking_approach()

    elif parking_phase == "ENTRY":
        run_parking_entry()

    elif parking_phase == "ALIGN":
        run_parking_alignment()

    elif parking_phase == "FINAL":
        run_final_positioning()
```

The reason for this subdivision is physical.

An Ackermann vehicle normally requires different steering behavior when:

```text
approaching a space

entering it

straightening the chassis

moving to its final position
```

Trying to perform all four with one constant steering command would make the maneuver much harder to tune.

---

## 2.6 Phase 1 — Approach

During `APPROACH`, Piolín should prepare a repeatable entry rather than immediately producing maximum steering.

The relevant information is:

```text
Pink x-position

Pink apparent size

S2 LEFT distance

S3 RIGHT distance

current Motor B angle

Motor A progression
```

The objective is:

```text
identify parking target
      ↓
stabilize approach
      ↓
reach a suitable entry condition
```

A conceptual structure is:

```python
def parking_approach():

    pink = get_locked_parking_target()

    visual_error = (
        pink.x - PIXY_CENTER_X
    )

    steering_request = calculate_parking_approach(
        visual_error
    )

    apply_parking_steering(
        steering_request
    )
```

This is architectural pseudocode.

The final:

```text
Pixy center

gain

steering limit

entry threshold
```

must be measured on the physical robot.

The Pink block should not be treated as a target that Piolín must simply drive directly toward.

Its visual geometry helps establish a controlled parking approach.

---

## 2.7 Transition from Approach to Entry

The parking maneuver should enter its stronger steering phase only after sufficient evidence exists.

A future condition may use several signals:

```text
Pink sufficiently relevant

vehicle sufficiently close to expected entry region

current lateral geometry acceptable
```

Conceptually:

```python
if (
    parking_target_relevant
    and entry_geometry_valid
):
    parking_phase = "ENTRY"
```

The exact condition remains a tuning problem.

The important design decision is to avoid:

```text
Pink first appears
→ maximum parking steering
```

because early strong steering can produce a poor entry angle.

---

## 2.8 Phase 2 — Entry

During `ENTRY`, the objective becomes:

```text
move the vehicle physically into the parking region
```

Piolín uses Ackermann steering, so the chassis cannot move sideways.

The movement is produced by:

```text
Motor B steering angle
+
Motor A forward/reverse movement
```

creating:

```text
curved vehicle trajectory
```

The parking controller therefore needs an intentional steering bias.

Conceptually:

```python
def parking_entry():

    steering_request = parking_entry_steering()

    steering_request = clamp(
        steering_request,
        -PARK_MAX_STEER,
        PARK_MAX_STEER
    )

    target = smooth_target(
        steering_request
    )

    steering_to(target)

    drive.run(PARK_ENTRY_SPEED)
```

The actual steering direction depends on the final parking geometry and competition approach.

It should be determined experimentally rather than hard-coded in documentation before the maneuver is validated.

---

## 2.9 Wall Safety During Entry

<div align="center">

<img
  src="../../../v-photos/v4/piolin_obstacle_top.jpg"
  alt="Top view of Piolín showing Pixy2.1 and both lateral ultrasonic sensors"
  width="710"
/>

<br>

<sub><b>Figure 2.3.</b> S2 and S3 remain available during the parking maneuver to provide physical clearance information while Pixy supplies the visual parking reference.</sub>

</div>

The permanent ultrasonic mapping remains:

```text
S2 = LEFT

S3 = RIGHT
```

Parking should not replace these physical safety measurements with Pixy coordinates.

During entry:

```text
Pixy
→ visual parking objective
```

while:

```text
S2 / S3
→ lateral physical clearance
```

A critical wall condition may therefore limit the parking maneuver.

Conceptually:

```python
wall_active, wall_cmd, safe_speed = side_wall_guard(
    left_mm,
    right_mm
)

if wall_active:
    final_command = wall_cmd
    drive_speed = safe_speed

else:
    final_command = parking_command
```

This follows the same controller hierarchy used elsewhere in Piolín:

```text
CRITICAL SAFETY
      ↓
ACTIVE MANEUVER
      ↓
NORMAL NAVIGATION
```

Normal wall following should not try to recenter Piolín while it is intentionally entering the parking region.

Critical protection may remain active.

---

## 2.10 Transition from Entry to Alignment

The robot should not remain at strong entry steering indefinitely.

At some point:

```text
vehicle enters parking region
      ↓
entry curvature is no longer needed
      ↓
steering must begin returning
```

The transition should ideally be based on physical evidence.

Possible information includes:

```text
Motor A encoder progression

Pink movement in camera

S2/S3 geometry

Motor B angle
```

Conceptually:

```python
if parking_entry_complete():
    parking_phase = "ALIGN"
```

The exact function:

```python
parking_entry_complete()
```

should only be finalized after repeated parking tests.

This is preferable to assuming:

```text
entry always lasts exactly N milliseconds
```

because physical response may vary between runs.

---

## 2.11 Phase 3 — Alignment

Alignment is responsible for correcting the vehicle's final orientation.

The goal is no longer:

```text
enter parking space
```

but:

```text
straighten Piolín inside the parking region
```

A conceptual alignment sequence is:

```text
entry steering
      ↓
controlled countersteer
      ↓
Motor B approaches center / calibrated final angle
      ↓
lateral geometry becomes acceptable
```

A possible controller structure is:

```python
def parking_alignment(
    left_mm,
    right_mm
):

    geometry_error = calculate_parking_geometry(
        left_mm,
        right_mm
    )

    command = (
        PARK_ALIGN_GAIN
        * geometry_error
    )

    command = clamp(
        command,
        -PARK_ALIGN_LIMIT,
        PARK_ALIGN_LIMIT
    )

    return command
```

The exact geometry equation remains under development.

The important principle is that alignment should be based on the **current physical position**, not simply by applying the exact opposite of the entry steering for the exact same amount of time.

The vehicle is no longer in the same geometry it had when the maneuver began.

---

## 2.12 Using S2 and S3 for Final Geometry

A useful parking geometry can potentially compare:

```text
LEFT clearance

RIGHT clearance
```

but the goal does not necessarily have to be:

```text
S2 == S3
```

unless the final intended parking position physically requires equal clearances.

Therefore the software should use a calibrated target:

```text
desired left/right relationship
```

rather than assuming geometric symmetry.

Conceptually:

```python
parking_geometry_error = (
    measured_geometry
    - desired_parking_geometry
)
```

The final target must be obtained from the actual course and Piolín dimensions.

No unmeasured parking distance should be inserted into the source merely because it appears visually centered.

---

## 2.13 Phase 4 — Final Positioning

Once Piolín is sufficiently aligned, the algorithm moves to:

```text
FINAL
```

The purpose of this phase is to control the last longitudinal movement.

One current development prototype already demonstrates an encoder-based parking movement.

It uses a temporary value:

```python
PARK_EXTRA_DEG = 300.0
```

relative to a stored Motor A position.

The useful architectural pattern is:

```python
parking_start_encoder = drive.angle()
```

then:

```python
parking_progress = abs(
    drive.angle()
    - parking_start_encoder
)
```

and finally:

```python
if parking_progress >= FINAL_PARK_ENCODER:
    parking_complete = True
```

The current:

```text
300 degrees
```

is a prototype value.

It should **not** be interpreted as the final validated parking travel.

The final value must be calibrated using:

```text
actual parking entry position

actual wheel behavior

actual space geometry

desired stopping point
```

---

## 2.14 Why Encoder Progression Is Preferred Over Final Timing

A simple final movement could be:

```python
drive.run(...)
wait(500)
drive.stop()
```

but a fixed time represents:

```text
motor command duration
```

rather than:

```text
vehicle progression
```

Encoder-based control instead measures Motor A rotation.

Conceptually:

```text
START FINAL MOVEMENT
        ↓
store encoder
        ↓
move
        ↓
measure encoder difference
        ↓
required progression reached
        ↓
stop
```

This provides a more physical reference.

However, encoders still do not guarantee exact ground distance because:

```text
wheel slip

mechanical variation

surface interaction
```

can affect real vehicle movement.

Therefore the strongest final parking system can combine:

```text
encoder progression
+
lateral geometry
+
parking state
```

rather than depending on the encoder alone.

---

## 2.15 Final Stop Validation

The final stopping condition should require more than:

```text
encoder threshold reached
```

if additional reliable geometry is available.

A conceptual condition is:

```python
parking_ready_to_stop = (
    final_encoder_reached
    and final_geometry_valid
)
```

Then:

```python
if parking_ready_to_stop:
    state = STOP
```

The final geometry condition may eventually include:

```text
acceptable left clearance

acceptable right clearance

acceptable steering angle

parking target no longer requiring correction
```

The exact tolerances remain calibration parameters.

The intent is:

```text
position reached
+
orientation acceptable
+
parking state valid
→ STOP
```

---

## 2.16 Terminal STOP State

`STOP` must be a true terminal state.

Once reached:

```text
no new pillar target

no normal wall following

no corner state

no parking correction
```

should restart navigation.

Conceptually:

```python
if state == STOP:

    drive.stop(Stop.BRAKE)

    steer.stop(Stop.HOLD)
```

and:

```text
remain STOP
```

until the program is deliberately restarted.

The desired state transition is:

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

This prevents the autonomous controller from moving again after a successful final position.

---

## 2.17 Temporary Loss of Pink During Parking

Pixy may lose the Pink reference as Piolín turns.

This does not necessarily mean the parking maneuver should be cancelled.

For example:

```text
ENTRY begins
      ↓
camera rotates
      ↓
Pink leaves field of view
```

At this point the robot may already have enough information to continue the committed maneuver using:

```text
current parking phase

last known Pink geometry

S2/S3

encoder progression
```

The software should therefore distinguish:

```text
Pink temporarily lost after parking commitment
```

from:

```text
Pink was never confirmed
```

Before `PARKING`:

```text
no Pink confirmation
→ do not commit
```

After `PARKING` is locked:

```text
brief visual loss
→ do not instantly return to NORMAL
```

This is consistent with Piolín's general target-lock philosophy.

---

## 2.18 Parking Controller Arbitration

The complete steering system should still produce **one final command**.

During parking, several subsystems may produce information:

```text
Pixy parking correction

parking entry trajectory

alignment controller

ultrasonic wall safety
```

These should not all be blindly added together.

A useful hierarchy is:

```text
CRITICAL WALL SAFETY
        ↓
CURRENT PARKING PHASE
        ↓
minor visual / geometry correction
```

Conceptually:

```python
parking_cmd = calculate_parking_command()

wall_active, wall_cmd, safe_speed = side_wall_guard(
    left_mm,
    right_mm
)

if wall_active:
    final_cmd = wall_cmd

else:
    final_cmd = parking_cmd
```

Then:

```python
target = smooth_target(final_cmd)
steering_to(target)
```

This preserves the same layered architecture used by the rest of Piolín.

---

## 2.19 Suggested Parking State Representation

A clean implementation can maintain:

```python
state = "PARKING"

parking_phase = "APPROACH"

parking_target_locked = True

parking_start_encoder = drive.angle()

parking_complete = False
```

and update:

```python
if parking_phase == "APPROACH":

    if approach_complete():
        parking_phase = "ENTRY"


elif parking_phase == "ENTRY":

    if entry_complete():
        parking_phase = "ALIGN"


elif parking_phase == "ALIGN":

    if alignment_complete():
        parking_phase = "FINAL"


elif parking_phase == "FINAL":

    if final_position_complete():
        state = "STOP"
```

This structure is intentionally conceptual.

Functions such as:

```text
approach_complete()

entry_complete()

alignment_complete()

final_position_complete()
```

represent the places where real track calibration must eventually be inserted.

The state architecture can remain stable even while those physical thresholds are tuned.

---

## 2.20 Debug Telemetry

Parking should expose enough information to determine which phase failed.

A useful terminal output can include:

```text
STATE

PARK PHASE

COURSE COUNT

PINK DETECTED

PINK X

PINK WIDTH

S2 LEFT

S3 RIGHT

ENTRY ENCODER

FINAL ENCODER

PARK COMMAND

WALL SAFETY

FINAL COMMAND

REAL STEERING
```

For example:

```text
STATE: PARKING
PHASE: ENTRY
COUNT: 12
PINK: True
X: ...
W: ...
S2: ...
S3: ...
CMD: ...
```

Later:

```text
STATE: PARKING
PHASE: ALIGN
S2: ...
S3: ...
TARGET: ...
REAL: ...
```

and finally:

```text
STATE: STOP
PARKED: True
```

This allows the team to distinguish:

```text
bad Pink detection
```

from:

```text
good detection but bad entry
```

from:

```text
good entry but bad alignment
```

from:

```text
good alignment but excessive final travel
```

---

## 2.21 Parking Failure Isolation

| Observed Failure | First Algorithm Stage to Inspect |
| :--- | :--- |
| Parking activates before 3 laps | Eligibility / course counting |
| Pink detected but ignored after completion | Pink confirmation |
| Parking begins from an unstable detection | Target confirmation too permissive |
| Piolín enters in wrong direction | Entry steering sign |
| Entry begins too strongly | Entry steering / smoothing |
| Entry begins too late | Approach condition |
| Piolín hits wall while entering | Safety thresholds / entry geometry |
| Pink disappears and robot aborts | Target-lock behavior |
| Piolín reaches space but remains angled | Alignment |
| Piolín oscillates during alignment | Alignment gain / deadband / smoothing |
| Piolín overshoots final position | Encoder travel / speed / braking |
| Piolín stops too early | Final-position condition |
| Piolín starts moving again after parking | STOP state |

The first incorrect phase should be fixed rather than compensating in a later phase.

---

## 2.22 Algorithm Summary

The complete intended algorithm is:

```text
                         COURSE RUNNING
                               │
                               ▼
                         course_count
                               │
                       count >= required?
                               │
                              YES
                               │
                               ▼
                       PARKING ELIGIBLE
                               │
                               ▼
                       Pixy sig1 visible?
                               │
                              YES
                               │
                               ▼
                        CONFIRM PINK
                               │
                               ▼
                         LOCK TARGET
                               │
                               ▼
                           PARKING
                               │
                               ▼
                           APPROACH
                               │
                      target / geometry
                         appropriate?
                               │
                              YES
                               │
                               ▼
                            ENTRY
                               │
                     controlled Ackermann
                          trajectory
                               │
                               ▼
                       entry complete?
                               │
                              YES
                               │
                               ▼
                            ALIGN
                               │
                       S2/S3 geometry
                       + Motor B state
                               │
                               ▼
                    alignment acceptable?
                               │
                              YES
                               │
                               ▼
                            FINAL
                               │
                       Motor A encoder
                       + final geometry
                               │
                               ▼
                      final condition?
                               │
                              YES
                               │
                               ▼
                             STOP
```

A critical wall condition can interrupt the normal parking steering request at any maneuver phase where physical protection is required.

---

## 2.23 Final Engineering Assessment

Piolín's parking algorithm is designed around **progressive commitment and physical verification**.

The robot first determines:

```text
Is parking logically allowed?
```

using course progression.

It then determines:

```text
Is the Pink parking reference actually present?
```

using Pixy2.1.

After confirmation, the parking objective is locked and executed through:

```text
APPROACH

ENTRY

ALIGNMENT

FINAL POSITION
```

rather than one continuous open-loop turn.

Different sensors support different parts of the maneuver:

```text
S4 / course count
→ parking eligibility
```

```text
Pixy2.1 sig1
→ parking target identity
```

```text
Pixy x / apparent size
→ visual parking geometry
```

```text
S2 / S3
→ lateral physical geometry and safety
```

```text
Motor A encoder
→ longitudinal progression
```

```text
Motor B
→ Ackermann steering execution
```

The current prototype also provides a useful proof of concept for:

```text
parking after 12 course events
```

and:

```text
encoder-referenced final travel
```

but its current:

```text
PARK_EXTRA_DEG = 300
```

remains a development value rather than a validated final parking distance.

The final numerical behavior should be obtained by independently tuning:

```text
Pink confirmation

approach condition

entry steering

entry speed

entry completion

alignment target

alignment tolerance

final encoder travel

final speed

STOP condition
```

without changing all of them simultaneously.

The central algorithm principle is:

> **Piolín should enter parking only after the course state permits it, commit only after the Pink reference is confirmed, divide the physical maneuver into controllable phases, and stop only after both progression and final geometry indicate that the terminal position has been reached.**

This approach turns parking from a timed final movement into a structured autonomous subsystem that can be tested and improved independently from the rest of the Obstacle Challenge navigation.

---

<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
