# 6. Obstacle Avoidance Strategy

<div align="center">

<img
  src="../../v-photos/v4/piolin_obstacle_isometric.jpg"
  alt="Piolín in its current Obstacle Challenge configuration"
  width="740"
/>

<br>

<sub><b>Figure 6.1.</b> Piolín's Obstacle Challenge strategy combines Pixy2.1 perception, lateral ultrasonic geometry, state-based control, and Ackermann steering.</sub>

</div>

Piolín's obstacle strategy is designed around one central principle:

> **The camera decides which obstacle matters and which side must be passed; the state machine decides when the maneuver is active; the ultrasonic sensors provide physical context and safety; and the steering controller produces one final Motor B command.**

The current Obstacle Challenge hardware is:

```text
Motor A → propulsion

Motor B → steering

S1 → Pixy2.1

S2 → LEFT Ultrasonic Sensor

S3 → RIGHT Ultrasonic Sensor

S4 → Color Sensor
```

The fixed obstacle rules are:

```text
RED
→ PASS RIGHT
```

```text
GREEN
→ PASS LEFT
```

These rules never depend on where the pillar appears in the camera image.

Piolín's current obstacle strategy is still under development. Therefore, this document describes the **intended maneuver architecture and the control principles already supported by the team's prototype code**, while leaving final steering magnitudes, timing, visual thresholds, and recovery limits open for calibration.

---

## 6.1 Complete Obstacle Maneuver

A complete pillar maneuver is not simply:

```text
detect
→ steer around pillar
```

Piolín divides the process into several stages:

```text
NORMAL
  ↓
TARGET_ACQUIRE
  ↓
APPROACH
  ↓
AVOID
  ↓
PASS_CONFIRM
  ↓
RECOVER
  ↓
NORMAL
```

Each stage solves a different problem.

| Phase | Main Question |
| :--- | :--- |
| `NORMAL` | Is there a relevant obstacle ahead? |
| `TARGET_ACQUIRE` | Which visible pillar should Piolín commit to? |
| `APPROACH` | How close/relevant is the selected obstacle becoming? |
| `AVOID` | How does Piolín pass it on the required side? |
| `PASS_CONFIRM` | Has the pillar actually been cleared? |
| `RECOVER` | How does Piolín return to useful track geometry? |

This separation prevents one steering rule from attempting to solve every part of the maneuver.

---

# 6.2 Step 1 — Detect and Select the Relevant Pillar

<div align="center">

<img
  src="../../v-photos/v4/pixy21_red_detection.jpg"
  alt="Pixy2.1 detecting a red pillar"
  width="680"
/>

<br>

<sub><b>Figure 6.2.</b> Pixy2.1 identifies the obstacle and provides image geometry used to determine whether the target is relevant.</sub>

</div>

Pixy2.1 can provide block information including:

```text
signature

x

y

width

height
```

Before any obstacle steering begins, the software should:

```text
read blocks
      ↓
reject invalid signatures
      ↓
evaluate relevance
      ↓
select one candidate
      ↓
confirm candidate
      ↓
lock target
```

The selected target becomes:

```text
active_target
```

and should remain the current obstacle until the physical maneuver is complete.

Conceptually:

```python
if state == NORMAL:

    candidate = select_relevant_target(blocks)

    if candidate_is_confirmed(candidate):
        active_target = candidate
        state = APPROACH
```

This is illustrative architecture. The exact candidate-scoring function is still being tuned.

---

# 6.3 Step 2 — Determine the Required Passing Side

The passing side is determined only by the Pixy signature.

A useful software function is conceptually:

```python
def required_pass_side(signature):

    if signature == RED_SIG:
        return RIGHT

    if signature == GREEN_SIG:
        return LEFT

    return None
```

The current mapping is:

```text
sig2 → RED → RIGHT

sig3 → GREEN → LEFT
```

This remains true regardless of image position.

For example:

```text
Red pillar appears left of camera center
```

still means:

```text
PASS RIGHT
```

and:

```text
Green pillar appears right of camera center
```

still means:

```text
PASS LEFT
```

The image coordinate describes **where the obstacle is**, not **which side the rules require**.

---

# 6.4 Step 3 — Controlled Approach

The robot should not necessarily produce its strongest steering command as soon as a valid pillar becomes visible.

Instead, target influence should increase as the obstacle becomes more relevant.

Conceptually:

```text
distant target
→ observe
```

```text
target becoming relevant
→ prepare maneuver
```

```text
close / important target
→ obstacle controller gains authority
```

Apparent block dimensions can provide useful qualitative evidence:

```text
small block
→ likely farther / less dominant
```

```text
larger block
→ likely more relevant
```

but:

```text
block width
≠
exact physical distance
```

unless separately calibrated.

A future approach controller may therefore calculate an obstacle authority value:

```python
obstacle_authority = target_relevance(active_target)
```

and constrain it using the same bounded-control philosophy already used in Piolín's prototypes:

```python
obstacle_authority = clamp(
    obstacle_authority,
    0.0,
    1.0
)
```

This allows obstacle control to increase progressively instead of turning one visual sample into maximum steering.

---

# 6.5 Step 4 — Enter the AVOID State

Once the target is sufficiently relevant, Piolín enters:

```text
AVOID
```

At this point the obstacle objective becomes the primary navigation objective.

During normal driving:

```text
wall geometry
→ strong influence
```

During active avoidance:

```text
pillar objective
→ strong influence
```

while the ultrasonic system changes role to:

```text
boundary context

critical wall safety

pass-confirmation support
```

This distinction is critical.

Suppose Piolín is passing a Red pillar:

```text
Red
→ RIGHT
```

while normal wall following wants to return left toward its preferred trajectory.

If both controllers are equally strong:

```text
RIGHT obstacle request
+
LEFT centering request
=
weak / unstable steering
```

The state machine prevents this conflict by reducing normal wall authority during `AVOID`.

---

# 6.6 Red Pillar Strategy

<div align="center">

<img
  src="../../v-photos/v4/obstacle_red_run.jpg"
  alt="Piolín performing a red pillar avoidance maneuver"
  width="710"
/>

<br>

<sub><b>Figure 6.3.</b> A Red obstacle requires Piolín to pass on the right while preserving enough wall clearance to complete the maneuver safely.</sub>

</div>

For Red:

```text
RED
→ PASS RIGHT
```

The conceptual sequence is:

```text
Red confirmed
      ↓
target locked
      ↓
prepare right-side trajectory
      ↓
steer progressively RIGHT
      ↓
maintain clearance
      ↓
pillar moves beside vehicle
      ↓
confirm pillar cleared
      ↓
countersteer / recover LEFT as needed
```

The steering direction should remain consistent with the obstacle rule throughout the active pass.

A possible state-level structure is:

```python
if state == AVOID:

    if active_target.signature == RED_SIG:
        obstacle_command = calculate_red_pass(
            active_target,
            left_mm,
            right_mm
        )
```

The exact `calculate_red_pass()` function remains under development.

The important rule is that Red classification itself should never become left-pass logic because of:

```text
camera angle

pillar x-position

previous corner direction

normal wall control
```

---

# 6.7 Green Pillar Strategy

<div align="center">

<img
  src="../../v-photos/v4/obstacle_green_run.jpg"
  alt="Piolín performing a green pillar avoidance maneuver"
  width="710"
/>

<br>

<sub><b>Figure 6.4.</b> A Green obstacle requires the mirrored logical objective: pass to the left.</sub>

</div>

For Green:

```text
GREEN
→ PASS LEFT
```

The maneuver becomes:

```text
Green confirmed
      ↓
target locked
      ↓
prepare left-side trajectory
      ↓
steer progressively LEFT
      ↓
maintain clearance
      ↓
pillar moves beside vehicle
      ↓
confirm pillar cleared
      ↓
countersteer / recover RIGHT as needed
```

Conceptually:

```python
if state == AVOID:

    if active_target.signature == GREEN_SIG:
        obstacle_command = calculate_green_pass(
            active_target,
            left_mm,
            right_mm
        )
```

Red and Green may eventually require slightly different calibrated steering values because the real Ackermann mechanism may not be perfectly symmetrical.

However, their logical rules remain exact opposites:

```text
RED → RIGHT

GREEN → LEFT
```

---

# 6.8 Obstacle Steering Is a Bias, Not a Camera Servo

One dangerous design would be to make Motor B directly chase the center of the visual block.

For example:

```text
pillar left in image
→ steer left
```

This is not appropriate for Piolín because the robot is not trying to **drive toward the pillar**.

It is trying to create a safe trajectory around it.

A better architecture treats Pixy as a source of obstacle geometry.

Conceptually:

```text
required passing side
+
target relevance
+
target x-position
+
wall context
      ↓
obstacle steering request
```

The image coordinate can change how strongly the robot reacts, but the desired trajectory remains defined by the obstacle rule.

A conceptual control term could therefore resemble:

```python
visual_error = active_target.x - PIXY_CENTER_X

visual_term = clamp(
    VISUAL_GAIN * visual_error,
    -VISUAL_LIMIT,
    VISUAL_LIMIT
)
```

followed by a side-specific bias:

```python
if required_side == RIGHT:
    requested = RIGHT_BASE_BIAS + visual_term

elif required_side == LEFT:
    requested = LEFT_BASE_BIAS + visual_term
```

This is architectural example code only.

The final equation and signs must come from physical testing.

---

# 6.9 Progressive Steering Instead of Instant Maximum Turn

Piolín's existing prototypes already contain a steering-target smoothing system:

```python
def smooth_target(target):
    global current_target

    diff = target - current_target

    diff = clamp(
        diff,
        -TARGET_STEP,
        TARGET_STEP
    )

    current_target += diff

    return current_target
```

This is particularly useful during obstacle avoidance.

Without smoothing:

```text
Red detected
→ steering jumps immediately to strong right
```

then:

```text
target x changes
→ steering suddenly changes again
```

which can create:

```text
zig-zag

mechanical shock

overshoot

unstable camera movement
```

The intended command chain is:

```text
obstacle controller
      ↓
requested steering
      ↓
state/safety arbitration
      ↓
smooth_target()
      ↓
steering_to()
      ↓
Motor B
```

The steering motor therefore receives a controlled target rather than raw camera noise.

---

# 6.10 Motor B Position Control

The current prototype already separates target steering from Motor B actuation:

```python
def steering_to(target):
    error = target - steer.angle()

    if abs(error) <= STEER_TOLERANCE:
        steer.stop(Stop.BRAKE)
        return

    speed = STEER_MOTOR_KP * error

    speed = clamp(
        speed,
        -MAX_STEER_MOTOR_SPEED,
        MAX_STEER_MOTOR_SPEED
    )

    steer.run(int(speed))
```

The Obstacle controller can retain this architecture.

That produces:

```text
NAVIGATION OBJECTIVE
      ↓
STEERING TARGET
      ↓
MOTOR POSITION ERROR
      ↓
MOTOR B SPEED
      ↓
PHYSICAL FRONT-WHEEL ANGLE
```

This distinction becomes very useful when debugging inverted pillar behavior.

If:

```text
target says RIGHT
```

but:

```text
physical wheels go LEFT
```

the vision system should not be changed.

The failure exists downstream in steering interpretation or actuation.

---

# 6.11 Ultrasonic Safety During Avoidance

<div align="center">

<img
  src="../../v-photos/v4/ultrasonic_pair_top.jpg"
  alt="Piolín lateral ultrasonic sensors used during obstacle avoidance"
  width="700"
/>

<br>

<sub><b>Figure 6.5.</b> S2 and S3 remain active during obstacle maneuvers to provide physical boundary context and emergency wall protection.</sub>

</div>

The lateral ultrasonic sensors remain active throughout the pillar maneuver.

Their current physical mapping is:

```text
S2 = LEFT

S3 = RIGHT
```

During `AVOID`, they should not normally decide the required passing side.

Instead, they protect against unsafe boundaries.

The current prototype already provides a useful safety pattern:

```python
wall_active, wall_cmd, wall_speed = side_wall_guard(
    left,
    right
)

if wall_active:
    combined_offset = wall_cmd
```

This demonstrates a clean priority structure:

```text
normal / obstacle controller
      ↓
critical safety check
      ↓
final steering
```

For Obstacles, the intended hierarchy is:

```text
CRITICAL WALL SAFETY
        ↓
ACTIVE OBSTACLE MANEUVER
        ↓
NORMAL WALL GEOMETRY
```

The wall-safety threshold should not be so aggressive that normal avoidance becomes impossible.

It should protect the robot when clearance becomes genuinely unsafe.

---

# 6.12 Speed Control During Avoidance

Motor A speed should change according to the maneuver state.

The current prototype already uses:

```python
if wall_active:
    drive.run(wall_speed)

elif acquire_progress < 1.0:
    drive.run(ACQUIRE_SPEED)

elif abs(combined_offset) >= TURN_STEER_THRESHOLD:
    drive.run(TURN_SPEED)

else:
    drive.run(DRIVE_SPEED)
```

The Obstacle Challenge can use the same principle.

Conceptually:

```text
NORMAL
→ normal speed
```

```text
TARGET_ACQUIRE
→ controlled approach
```

```text
AVOID
→ obstacle maneuver speed
```

```text
CRITICAL WALL
→ slower safety speed
```

```text
RECOVER
→ controlled recovery speed
```

Why this matters:

```text
higher speed
→ more distance traveled while sensors update
→ more distance traveled while Motor B changes angle
```

Therefore stronger avoidance does not always mean:

```text
increase steering
```

Sometimes the correct improvement is:

```text
reduce speed
→ allow steering and perception more time
```

---

# 6.13 Step 5 — Pass Confirmation

Piolín should not release the current pillar simply because Pixy stops seeing it.

The sequence:

```text
target visible
      ↓
vehicle turns
      ↓
camera rotates
      ↓
target disappears
```

does not prove:

```text
pillar passed
```

The state machine therefore uses:

```text
PASS_CONFIRM
```

between avoidance and recovery.

Evidence may include:

```text
recent target history

Pixy target movement

S2 / S3 behavior

vehicle progression

current maneuver side
```

Conceptually:

```python
if state == AVOID:

    if visual_target_is_leaving:
        state = PASS_CONFIRM
```

Then:

```python
if state == PASS_CONFIRM:

    if pillar_is_physically_cleared():
        state = RECOVER
```

The exact `pillar_is_physically_cleared()` criteria are still being calibrated.

---

# 6.14 Using Lateral Geometry to Confirm the Pass

A pillar can temporarily alter the reading of one lateral ultrasonic sensor.

A possible physical sequence is:

```text
normal open geometry

pillar approaches beside sensor

distance becomes smaller / changes

Piolín advances past pillar

distance opens again
```

That change can provide useful pass evidence.

The intended sensor fusion is:

```text
Pixy
→ visual evidence that target is moving out of forward relevance
```

plus:

```text
lateral ultrasonic
→ physical evidence that obstacle is moving behind vehicle
```

This is stronger than:

```text
no camera block
→ release immediately
```

because the camera can lose the target due to steering alone.

---

# 6.15 Step 6 — Recovery

A successful pillar pass is only half of the maneuver.

The complete sequence is:

```text
DETECT
  ↓
AVOID
  ↓
PASS
  ↓
RECOVER
```

During `RECOVER`, the objective changes from:

```text
move around pillar
```

to:

```text
prepare for the next section of track
```

The controller can use:

```text
S2

S3

current steering position

previous passing direction
```

to create a controlled countersteer.

For a Red pass:

```text
avoid RIGHT
      ↓
pillar cleared
      ↓
controlled recovery LEFT
```

For a Green pass:

```text
avoid LEFT
      ↓
pillar cleared
      ↓
controlled recovery RIGHT
```

However, recovery should not simply be the exact opposite maximum steering command.

The goal is:

```text
restore useful geometry
```

not:

```text
mirror the entire avoidance trajectory
```

---

# 6.16 Recovery Must Not Begin Too Early

One of the most dangerous failure modes is:

```text
pillar still beside Piolín
      ↓
recovery begins
      ↓
vehicle turns back toward pillar
```

This is why `PASS_CONFIRM` exists.

The transition should be:

```text
AVOID
  ↓
obstacle becomes visually peripheral
  ↓
PASS_CONFIRM
  ↓
physical clearance confirmed
  ↓
RECOVER
```

not:

```text
Pixy missed one frame
→ RECOVER
```

A target-memory system can preserve the active obstacle briefly even if the camera loses it.

---

# 6.17 Recovery Must Not Begin Too Late

The opposite failure is also possible.

If Piolín remains in avoidance for too long:

```text
pillar already passed
      ↓
robot continues right/left
      ↓
outside wall approaches
```

The result may be:

```text
successful obstacle pass
+
wall collision
```

In that situation the solution should not automatically be:

```text
weaken pillar avoidance
```

because the obstacle maneuver may already be correct.

The real problem may be:

```text
late target release

late countersteer

weak recovery
```

This distinction is one of the main reasons obstacle handling is divided into states.

---

# 6.18 Return to NORMAL

Recovery should continue until the lateral geometry becomes sufficiently useful again.

The intended transition is:

```text
RECOVER
      ↓
S2/S3 geometry stabilizes
      ↓
steering demand decreases
      ↓
old target no longer relevant
      ↓
clear active_target
      ↓
NORMAL
```

Conceptually:

```python
if state == RECOVER:

    recovery_command = calculate_recovery(
        left_mm,
        right_mm
    )

    if geometry_is_stable:
        active_target = None
        state = NORMAL
```

The exact stability condition remains a calibration value.

The important architectural point is that the old target is not released before the maneuver that depends on it has actually finished.

---

# 6.19 Consecutive Obstacles

A robust strategy must handle more than one isolated pillar.

After recovery, Piolín may encounter:

```text
RED → RED

GREEN → GREEN

RED → GREEN

GREEN → RED
```

A correct state reset should allow:

```text
first target selected
      ↓
first target passed
      ↓
first target released
      ↓
recovery
      ↓
new target selected
```

The software should avoid two opposite failures:

```text
target released too early
→ changes pillar mid-pass
```

and:

```text
target released too late
→ ignores next pillar
```

The target lifecycle therefore becomes:

```text
CANDIDATE
→ CONFIRMED
→ LOCKED
→ PASSED
→ RELEASED
```

This is conceptually similar to the event-latching strategy already used in Piolín's Color Sensor prototype.

---

# 6.20 Obstacles Near Corners

Obstacle avoidance becomes more difficult when a pillar appears close to a track corner.

Possible active objectives include:

```text
finish corner

select pillar

pass pillar

avoid wall

recover geometry
```

The software should not allow all controllers to receive full steering authority simultaneously.

A conceptual priority is:

```text
CRITICAL SAFETY
      ↓
CURRENT COMMITTED MANEUVER
      ↓
NEXT HIGH-LEVEL OBJECTIVE
      ↓
NORMAL WALL CONTROL
```

For example, if Piolín is already deeply committed to `CORNER`, a newly visible distant pillar may be observed without immediately replacing corner control.

After corner exit:

```text
target relevance can increase
```

and the robot can transition into:

```text
TARGET_ACQUIRE
```

The exact handling of a very close pillar during a corner remains an active development area.

---

# 6.21 Failure Recovery and Defensive Behavior

The strategy should also define what happens when perception becomes uncertain.

Examples include:

```text
Pixy temporarily loses target

two targets have similar relevance

ultrasonic reading spikes

wall becomes unexpectedly close
```

The controller should prefer predictable behavior over rapid state reversal.

For example:

```text
one missing Pixy frame
```

should not automatically cause:

```text
LEFT maneuver
→ RIGHT maneuver
```

Likewise, one ultrasonic spike should not instantly create an extreme wall escape if the rest of the geometry remains plausible.

The architecture therefore combines:

```text
short filtering

target confirmation

target lock

bounded steering

state memory

independent wall safety
```

to reduce the effect of isolated measurements.

---

# 6.22 Strategy Debugging

The obstacle controller should expose enough information to identify the first incorrect decision.

Useful debug information includes:

```text
STATE

ACTIVE TARGET

SIGNATURE

PASS SIDE

X

Y

WIDTH

HEIGHT

S2 LEFT

S3 RIGHT

OBSTACLE COMMAND

WALL SAFETY

FINAL COMMAND

MOTOR B ANGLE
```

For example:

```text
STATE: AVOID
SIG: 2
PASS: RIGHT
X: ...
W: ...
S2: ...
S3: ...
OBS_CMD: RIGHT
SAFE: False
FINAL: RIGHT
```

If Piolín physically turns left in that situation, the obstacle-detection and state layers are probably correct.

The problem is likely downstream.

By contrast:

```text
SIG: 2
PASS: LEFT
```

would immediately reveal a Red/Right mapping error.

Debug output allows the team to trace:

```text
OBSERVATION
→ INTERPRETATION
→ STATE
→ COMMAND
→ PHYSICAL RESPONSE
```

instead of diagnosing only from the final collision.

---

# 6.23 Current Code Patterns Reused in the Strategy

The final Obstacle controller is not yet complete, but several control patterns already exist in Piolín's current prototypes.

| Existing Pattern | Obstacle Strategy Use |
| :--- | :--- |
| `clamp()` | Bound steering and controller values |
| Median filtering | Reject isolated ultrasonic spikes |
| `smooth_target()` | Prevent abrupt steering reversals |
| `steering_to()` | Closed-loop Motor B actuation |
| `side_wall_guard()` | Critical boundary protection |
| State-dependent speed | Different speeds for approach/avoid/recovery |
| Candidate confirmation | Confirm Pixy target |
| Event latch | Lock active pillar |
| Release condition | Confirm pillar passed before new target |
| Debug output | Trace obstacle decision chain |

What remains under active development is primarily the **Obstacle-specific logic between those reusable layers**.

This includes:

```text
final Pixy relevance function

exact approach transition

Red steering profile

Green steering profile

visual-error weighting

wall authority during avoidance

pillar-pass confirmation

recovery conditions

corner interaction

parking
```

These should remain labeled as tunable until repeated track testing validates them.

---

# 6.24 Complete Intended Obstacle Flow

The full strategy can be represented as:

```text
                           NORMAL
                              │
                              ▼
                      PIXY SEES BLOCKS
                              │
                              ▼
                    VALIDATE CANDIDATES
                              │
                              ▼
                    SELECT MOST RELEVANT
                              │
                              ▼
                         CONFIRM TARGET
                              │
                              ▼
                          LOCK TARGET
                              │
                              ▼
                           APPROACH
                              │
                              ▼
                    target relevant enough?
                              │
                             YES
                              │
                              ▼
                            AVOID
                              │
                 ┌────────────┴────────────┐
                 │                         │
                 ▼                         ▼
             RED target                GREEN target
                 │                         │
                 ▼                         ▼
           PASS RIGHT                  PASS LEFT
                 │                         │
                 └────────────┬────────────┘
                              │
                              ▼
                     WALL SAFETY CHECK
                              │
                              ▼
                      FINAL STEERING
                              │
                              ▼
                        TARGET LEAVING?
                              │
                             YES
                              │
                              ▼
                       PASS_CONFIRM
                              │
                    physically cleared?
                              │
                             YES
                              │
                              ▼
                           RECOVER
                              │
                    geometry stable?
                              │
                             YES
                              │
                              ▼
                     RELEASE TARGET
                              │
                              ▼
                           NORMAL
```

At any stage where wall distance becomes physically critical:

```text
WALL SAFETY
```

can temporarily override the maneuver command.

---

# 6.25 Final Engineering Assessment

Piolín's obstacle strategy is designed as a complete **target lifecycle and vehicle maneuver**, not as a direct color-to-steering reaction.

The perception system determines:

```text
Which pillar matters?
```

The Pixy signature determines:

```text
Which side is required?
```

The obstacle controller determines:

```text
How strongly should Piolín move toward that passing trajectory?
```

The ultrasonic sensors determine:

```text
Is the physical geometry still safe?

Has the pillar likely been passed?

How should Piolín recover afterward?
```

The state machine determines:

```text
Which of these objectives currently has authority?
```

The final chain is:

```text
DETECT
→ SELECT
→ CONFIRM
→ LOCK
→ APPROACH
→ AVOID
→ PASS_CONFIRM
→ RECOVER
→ RELEASE
```

The rules remain fixed:

```text
RED
→ PASS RIGHT
```

```text
GREEN
→ PASS LEFT
```

while Pixy coordinates and apparent size influence how the maneuver develops rather than changing the required side.

The strategy also deliberately prevents normal wall following from continuously fighting obstacle avoidance. During `AVOID`, Pixy-based obstacle control receives greater navigation authority, while S2 and S3 remain available for critical wall safety and physical context.

After the pillar is cleared, authority transitions back toward the lateral geometry system through `RECOVER`.

Several pieces of this architecture already have direct equivalents in Piolín's prototype Python programs: bounded values, ultrasonic filtering, steering target smoothing, Motor B position control, wall-safety override, state-dependent speed, candidate confirmation, event locking, release conditions, and detailed debugging.

The numerical obstacle behavior itself remains under development.

The central strategy principle is:

> **Piolín should commit to one relevant obstacle, preserve the rule associated with its color, complete the entire physical pass before releasing it, and deliberately recover the vehicle before searching for the next maneuver.**

This approach gives PiolínTech a clearer way to improve pillar detection, passing trajectories, safety, and recovery independently while preserving one understandable autonomous strategy.

---

<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
