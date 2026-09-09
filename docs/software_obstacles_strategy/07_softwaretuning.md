# 7. Software Tuning

<div align="center">

<img
  src="../../v-photos/v4/piolin_obstacle_isometric.jpg"
  alt="Piolín in its current Obstacle Challenge configuration"
  width="740"
/>

<br>

<sub><b>Figure 7.1.</b> Software tuning on Piolín is performed on the complete physical robot because steering, speed, vision, wall geometry, and state transitions interact dynamically.</sub>

</div>

Software tuning is the process of converting Piolín's control architecture into reliable physical behavior.

The objective is not to search randomly for a combination of numbers that produces one successful run.

Instead, tuning should answer:

```text
What behavior is failing?

Which software layer controls that behavior?

Which parameter has a physical relationship to the failure?

What changes when that parameter is modified?

Does the improvement repeat?
```

The current Obstacle Challenge controller is still under development, so several parameters remain experimental.

The main tuning areas include:

```text
Pixy target confirmation

target relevance

target locking

obstacle steering strength

visual steering influence

drive speed

wall-controller authority

wall safety

pillar-pass confirmation

post-pillar recovery

corner interaction

parking
```

These values should be calibrated progressively and should not be treated as final specifications until repeated tests support them.

---

## 7.1 Tune the System in the Correct Order

Piolín should not begin software tuning until the physical system is sufficiently repeatable.

The recommended order is:

```text
MECHANICS
    ↓
RAW SENSORS
    ↓
STEERING RESPONSE
    ↓
NORMAL DRIVING
    ↓
VISION DETECTION
    ↓
TARGET SELECTION
    ↓
PILLAR AVOIDANCE
    ↓
PASS CONFIRMATION
    ↓
RECOVERY
    ↓
CORNER INTERACTION
    ↓
PARKING
```

If the steering mechanism is physically misaligned, changing Pixy parameters will not solve the problem.

Likewise, if the camera reports the wrong signature, increasing obstacle steering strength will only make the incorrect decision happen more aggressively.

The general rule is:

> **Tune the earliest incorrect layer first.**

---

# 7.2 Separate Parameters by Responsibility

One of the most important software practices is keeping constants grouped by the physical behavior they influence.

A clean controller can conceptually organize parameters as:

```python
# ------------------------------------------------------------
# DRIVE
# ------------------------------------------------------------

NORMAL_SPEED = ...
AVOID_SPEED = ...
RECOVERY_SPEED = ...

# ------------------------------------------------------------
# STEERING
# ------------------------------------------------------------

MAX_STEER = ...
TARGET_STEP = ...
STEER_TOLERANCE = ...

# ------------------------------------------------------------
# ULTRASONIC / WALL
# ------------------------------------------------------------

WALL_TARGET = ...
WALL_SOFT = ...
WALL_CRITICAL = ...

# ------------------------------------------------------------
# PIXY
# ------------------------------------------------------------

TARGET_CONFIRMATIONS = ...
MIN_TARGET_RELEVANCE = ...
TARGET_LOSS_LIMIT = ...

# ------------------------------------------------------------
# OBSTACLE
# ------------------------------------------------------------

RED_BIAS = ...
GREEN_BIAS = ...
VISUAL_GAIN = ...

# ------------------------------------------------------------
# RECOVERY
# ------------------------------------------------------------

RECOVERY_GAIN = ...
RECOVERY_RELEASE = ...
```

The exact variable names may change in the final program.

The important architectural principle is that a reader should immediately understand whether a value changes:

```text
perception

trajectory

safety

speed

recovery
```

rather than searching through the entire source file.

---

# 7.3 Bound Every Strong Controller

Piolín's current prototype already uses a common utility:

```python
def clamp(value, minimum, maximum):
    if value < minimum:
        return minimum

    if value > maximum:
        return maximum

    return value
```

This pattern is important during tuning because proportional or nonlinear calculations can otherwise produce unexpectedly large commands.

For example:

```python
visual_term = gain * visual_error

visual_term = clamp(
    visual_term,
    -VISUAL_LIMIT,
    VISUAL_LIMIT
)
```

The same concept applies to:

```text
wall correction

obstacle steering

recovery steering

speed reduction
```

A gain should control sensitivity.

A limit should control the maximum authority available to that controller.

These are separate tuning responsibilities.

For example:

```text
high gain + low limit
```

creates a controller that reaches its maximum quickly.

```text
lower gain + higher limit
```

creates a controller that reacts progressively but can eventually become stronger.

Tuning should therefore consider both.

---

# 7.4 Tune Steering Response Before Obstacle Logic

<div align="center">

<img
  src="../../v-photos/v4/ackermann_top.jpg"
  alt="Piolín Ackermann-style steering system"
  width="700"
/>

<br>

<sub><b>Figure 7.2.</b> Software steering values must be tuned against the physical response of Piolín's Ackermann-style steering mechanism.</sub>

</div>

Motor B commands do not directly represent vehicle curvature.

The complete chain is:

```text
software steering target
      ↓
Motor B angle
      ↓
steering linkage
      ↓
front-wheel angles
      ↓
vehicle curvature
```

Therefore the first steering-related questions should be:

```text
Is steering center repeatable?

Does positive steering move the expected direction?

Does negative steering move the opposite direction?

Can Motor B reach its target quickly enough?

Does the linkage bind near the limits?
```

Only after this is confirmed should obstacle steering magnitude be tuned.

Otherwise a navigation problem can actually be an actuator problem.

---

# 7.5 Steering Target Smoothing

The current Piolín prototype limits how much the steering target can change in one control cycle:

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

This parameter is especially important during obstacle avoidance.

### `TARGET_STEP` too large

Possible behavior:

```text
abrupt steering

overshoot

rapid left/right changes

camera movement becomes aggressive

mechanical shock
```

### `TARGET_STEP` too small

Possible behavior:

```text
slow steering response

late pillar avoidance

wide trajectory

wall collision before steering reaches requested value
```

The correct setting balances:

```text
smoothness
```

against:

```text
reaction speed
```

It should be tested using the same representative Motor A speed intended for the maneuver.

---

# 7.6 Tune Speed Together with Steering

Drive speed and steering cannot be calibrated independently.

Suppose Motor B requires a short physical time to move from:

```text
center
```

to:

```text
strong right
```

At low Motor A speed, Piolín travels only a short distance during that steering response.

At high speed:

```text
same Motor B response time
→ much greater physical travel
```

This can make a previously successful obstacle maneuver begin too late.

The current prototype already treats speed as state-dependent:

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

The final Obstacle controller can follow the same principle:

```text
NORMAL
→ normal speed

TARGET_ACQUIRE
→ controlled approach speed

AVOID
→ obstacle speed

RECOVER
→ recovery speed

CRITICAL WALL
→ reduced safety speed
```

If avoidance is consistently late, the first solution should not always be:

```text
increase steering
```

It may be better to reduce the approach or maneuver speed.

---

# 7.7 Tune Pixy Detection Before Pixy Steering

<div align="center">

<img
  src="../../v-photos/v4/pixy21_red_detection.jpg"
  alt="Pixy2.1 red pillar detection during tuning"
  width="680"
/>

<br>

<sub><b>Figure 7.3.</b> Vision detection and steering response should be tuned as separate stages.</sub>

</div>

Before changing obstacle steering values, verify:

```text
Red → sig2

Green → sig3

Pink → sig1
```

Then confirm:

```text
target coordinates behave plausibly

block size changes with approach

target remains visible under representative lighting

camera mounting remains unchanged
```

The current Pixy2.1 should be tested with its **3D-printed casing installed**, because the casing is part of the physical camera configuration.

The tuning sequence should be:

```text
CAMERA DETECTS CORRECTLY
        ↓
TARGET SELECTS CORRECTLY
        ↓
PASS SIDE SELECTS CORRECTLY
        ↓
THEN tune steering
```

If the camera reports:

```text
RED
```

and the state machine correctly reports:

```text
PASS RIGHT
```

then changing camera thresholds will not fix a physical left turn.

The problem is downstream.

---

# 7.8 Target Confirmation and Reaction Delay

The current color-event prototype already demonstrates the concept of confirmation before action:

```python
if detected == candidate_color:
    candidate_count += 1
else:
    candidate_color = detected
    candidate_count = 1
```

followed by:

```python
if candidate_count >= COLOR_CONFIRMATIONS:
```

Pixy target confirmation can use the same architecture.

This creates an important tuning trade-off.

### Too few confirmations

```text
fast reaction
+
higher chance of reacting to unstable detection
```

### Too many confirmations

```text
stable classification
+
later physical reaction
```

The confirmation count should therefore be evaluated dynamically.

A useful test is:

```text
same pillar

same starting position

same speed

repeat several trials
```

and record:

```text
first visible detection

confirmed detection

physical steering start

pillar clearance
```

The correct confirmation setting is the lowest value that remains sufficiently stable under representative conditions.

---

# 7.9 Tune Target Relevance

One of the main goals of relevance tuning is preventing distant pillars from controlling steering too early.

The desired behavior is:

```text
pillar visible far ahead
→ recognized
→ little steering authority
```

then:

```text
pillar becomes relevant
→ controller prepares
```

and finally:

```text
pillar close enough
→ avoidance gains strong authority
```

Potential relevance inputs include:

```text
width

height

x

y

current state

previous target
```

The final formula should be tuned using repeated scenarios.

For example:

| Test | Near Object | Far Object | Correct Target |
| :--- | :--- | :--- | :--- |
| 1 | Red | Green | — |
| 2 | Green | Red | — |
| 3 | Red | Red | — |
| 4 | Green | Green | — |
| 5 | Red center | Green peripheral | — |

The goal is not to create the mathematically most complicated scoring function.

It is to create the simplest function that consistently selects the physically relevant pillar.

---

# 7.10 Tune Obstacle Steering in Isolation

<div align="center">

<img
  src="../../v-photos/v4/obstacle_red_run.jpg"
  alt="Piolín Red obstacle maneuver used for software tuning"
  width="700"
/>

<br>

<sub><b>Figure 7.4.</b> Red and Green avoidance should first be tuned as isolated maneuvers before consecutive-pillar or full-course testing.</sub>

</div>

Obstacle steering should first be tested with one pillar.

Start with:

```text
one Red pillar
```

until Piolín can consistently attempt:

```text
PASS RIGHT
```

Then test:

```text
one Green pillar
```

for:

```text
PASS LEFT
```

Tune behaviors such as:

```text
when avoidance begins

initial steering bias

maximum steering authority

visual correction influence

avoidance speed
```

without simultaneously changing recovery.

A useful development rule is:

```text
first make the PASS correct

then make the RECOVERY correct
```

If Piolín passes the pillar successfully but hits the wall afterward, do not weaken the pass until recovery has been investigated.

---

# 7.11 Red and Green Do Not Need Identical Numbers

<div align="center">

<img
  src="../../v-photos/v4/obstacle_green_run.jpg"
  alt="Piolín Green obstacle maneuver used for software tuning"
  width="700"
/>

<br>

<sub><b>Figure 7.5.</b> The logical Red and Green rules are symmetrical, but the physical steering mechanism may require slightly different calibrated values.</sub>

</div>

The competition rules are perfectly clear:

```text
RED
→ RIGHT
```

```text
GREEN
→ LEFT
```

However, the physical robot may not have perfectly symmetrical steering behavior.

Possible causes include:

```text
Ackermann linkage geometry

mechanical tolerances

Motor B center

weight distribution

sensor placement
```

Therefore the final software may legitimately use slightly different calibrated magnitudes for Red and Green.

For example, conceptually:

```python
RED_BIAS = ...
GREEN_BIAS = ...
```

This does **not** mean the competition logic is different.

It only means the physical actuator may require different calibration to produce comparable trajectories.

Any asymmetry should be justified by measured testing rather than added without evidence.

---

# 7.12 Tune Wall Authority During AVOID

One of the most important tuning parameters is not necessarily a single number.

It is **controller authority**.

During `NORMAL`:

```text
wall geometry
→ strong authority
```

During `AVOID`:

```text
pillar controller
→ strong authority
```

Normal wall following should therefore be weakened or temporarily suspended as a trajectory controller while the pillar maneuver is active.

Critical wall safety remains available.

This distinction matters because:

```text
Red obstacle controller
→ RIGHT
```

can otherwise be opposed by:

```text
normal centering
→ LEFT
```

creating:

```text
weak steering

zig-zag

late pillar pass

apparent inversion
```

The tuning question should therefore be:

```text
Is obstacle steering too weak?
```

but also:

```text
Is another controller fighting it?
```

Increasing obstacle gains without checking arbitration can hide the true problem.

---

# 7.13 Wall-Safety Tuning

The current prototype contains an independent wall-safety controller:

```python
wall_active, wall_cmd, wall_speed = side_wall_guard(
    left,
    right
)

if wall_active:
    combined_offset = wall_cmd
```

This structure should remain logically separate from normal wall following.

The safety system needs to answer:

```text
When should safety begin influencing the robot?

When should it completely override navigation?

How much should speed decrease?
```

If safety activates too early:

```text
pillar maneuver becomes restricted

robot may fail to reach required side
```

If safety activates too late:

```text
robot has insufficient physical distance to escape wall
```

Therefore safety thresholds should be tuned using controlled wall-approach tests, not only during complete obstacle runs.

---

# 7.14 Tune Pass Confirmation Separately

`PASS_CONFIRM` is one of the most important states to calibrate.

The failure modes are opposite.

### Confirmation too early

```text
pillar still beside vehicle
      ↓
RECOVER begins
      ↓
Piolín turns back toward pillar
```

### Confirmation too late

```text
pillar already cleared
      ↓
AVOID continues
      ↓
Piolín approaches outside wall
```

Useful evidence can include:

```text
last Pixy target position

target disappearance history

S2/S3 changes

vehicle progression

current obstacle side
```

The final pass criterion should be tuned using repeated video and telemetry.

A test table can use:

| Trial | Pillar | Visual Loss | US Change | Recovery Start | Result |
| :---: | :--- | :--- | :--- | :--- | :--- |
| 1 | Red | — | — | — | — |
| 2 | Red | — | — | — | — |
| 3 | Green | — | — | — | — |
| 4 | Green | — | — | — | — |

This helps determine whether recovery consistently begins at the correct physical point.

---

# 7.15 Recovery Tuning

Recovery should be tuned only after the basic pillar pass is working.

The goal is:

```text
pillar cleared
      ↓
countersteer
      ↓
vehicle returns toward useful geometry
      ↓
steering reduces
      ↓
NORMAL resumes
```

Important parameters may include:

```text
initial recovery strength

recovery steering limit

recovery speed

wall geometry influence

release threshold
```

The recovery controller should not simply apply:

```text
avoidance steering × -1
```

because the vehicle is now in a different physical position.

The correct objective is not:

```text
undo previous steering
```

but:

```text
restore useful course geometry
```

---

# 7.16 Tune One Failure at a Time

Suppose a Red maneuver fails.

Possible observations might be:

```text
A. Red not detected.

B. Red detected but target selected late.

C. Target selected correctly but steering begins late.

D. Steering begins correctly but is too weak.

E. Pillar is passed correctly but recovery starts too early.

F. Recovery works but next target is not acquired.
```

Each failure belongs to a different tuning layer.

A poor tuning method would be:

```text
increase camera threshold

increase steering

reduce speed

change wall gain

change recovery
```

all at once.

A stronger method is:

```text
identify first incorrect event
      ↓
change parameter linked to that event
      ↓
repeat same scenario
```

This makes every test produce useful engineering information.

---

# 7.17 Debug Telemetry for Tuning

The current Piolín prototype already prints detailed controller information such as:

```python
print(
    "L:", int(left),
    "R:", int(right),
    "X:", round(x_est, 1),
    "ERR:", round(error, 1),
    "WALL_SAFE:", wall_active,
    "CMD:", round(combined_offset, 1),
    "TARGET:", round(current_target, 1),
    "REAL:", round(steer.angle(), 1)
)
```

Obstacle tuning should extend this idea.

A useful obstacle telemetry record can include:

```text
STATE

TARGET SIG

TARGET X

TARGET WIDTH

TARGET HEIGHT

RELEVANCE

CONFIRMATIONS

LOCK ACTIVE

S2 LEFT

S3 RIGHT

OBSTACLE COMMAND

WALL COMMAND

SAFETY ACTIVE

FINAL COMMAND

REAL STEERING
```

For example:

```text
STATE: AVOID
SIG: 2
PASS: RIGHT
X: ...
W: ...
REL: ...
S2: ...
S3: ...
OBS: RIGHT
SAFE: False
FINAL: RIGHT
REAL: ...
```

Telemetry should make it possible to identify the first incorrect stage without guessing from the final collision.

---

# 7.18 Use Video and Telemetry Together

Some obstacle transitions occur too quickly to judge accurately while watching the run live.

Video can reveal:

```text
when the pillar first entered the FOV

when steering began

when the pillar reached the side of the robot

when the camera lost it

when recovery began

when the next wall became relevant
```

Telemetry can reveal:

```text
what state the software believed it was in

which target was active

which command was requested
```

The strongest debugging combination is:

```text
VIDEO
+
TERMINAL OUTPUT
+
TEST ID
```

For example:

```text
video shows wheels turn left
```

while:

```text
terminal says FINAL: RIGHT
```

This immediately moves investigation toward:

```text
Motor B sign

steering conversion

mechanical response
```

instead of Pixy detection.

---

# 7.19 Maintain a Known-Good Baseline

Tuning should always preserve the most recent stable configuration.

A useful workflow is:

```text
KNOWN-GOOD VERSION
       ↓
create one experimental change
       ↓
test repeatedly
       ↓
compare
```

If better:

```text
document
→ commit
→ new baseline
```

If worse:

```text
reject
→ return to known-good
```

This is much safer than repeatedly editing the same file until several successful behaviors disappear.

Important known-good configurations should be associated with:

```text
Git commit

software file

robot hardware configuration

calibration values

test notes
```

rather than remembered only through filenames.

---

# 7.20 Parameter Test Table

A tuning log can use a table such as:

| Test | Parameter | Old Value | New Value | Expected Effect | Result |
| :---: | :--- | :---: | :---: | :--- | :--- |
| T01 | `TARGET_STEP` | — | — | Faster steering response | — |
| T02 | Avoid speed | — | — | More reaction time | — |
| T03 | Red bias | — | — | Stronger pass-right trajectory | — |
| T04 | Green bias | — | — | Stronger pass-left trajectory | — |
| T05 | Target confirmation | — | — | Reduce unstable detections | — |
| T06 | Relevance threshold | — | — | Ignore distant targets | — |
| T07 | Pass release | — | — | Delay recovery | — |
| T08 | Recovery strength | — | — | Faster recentering | — |

The values should be filled from actual experiments.

No unmeasured values should be inserted simply to make the table appear complete.

---

# 7.21 Recommended Tuning Sequence for One Pillar

For a single Red or Green target, tune in this order:

```text
1. Verify correct signature.

2. Verify correct pass side.

3. Verify candidate selection.

4. Verify target confirmation.

5. Verify target lock.

6. Tune approach speed.

7. Tune avoidance steering.

8. Verify wall safety does not fight avoidance.

9. Verify pillar clearance.

10. Tune PASS_CONFIRM.

11. Tune recovery.

12. Verify NORMAL resumes.

13. Repeat several times.
```

Only after both Red and Green work independently should testing move to:

```text
consecutive pillars

mixed colors

pillars near corners

full-course runs
```

This isolates problems much more effectively than beginning with the most complex course.

---

# 7.22 When a Parameter Should Not Be Changed

Some failures clearly belong to another layer.

### Correct Pixy target, wrong physical steering direction

Do not change:

```text
camera thresholds
```

Check:

```text
steering sign

Motor B control
```

### Pillar passed correctly, wall hit afterward

Do not immediately weaken:

```text
avoidance steering
```

Check:

```text
PASS_CONFIRM

RECOVER
```

### Piolín reacts to far pillar

Do not automatically reduce:

```text
all obstacle steering
```

Check:

```text
target relevance
```

### Robot oscillates during every maneuver

Do not immediately change:

```text
Pixy signature training
```

Check:

```text
target smoothing

Motor B response

control arbitration

drive speed
```

Good tuning requires changing the parameter whose physical role actually matches the observed failure.

---

# 7.23 Current vs. Final Tuning Values

The current prototypes contain many working constants.

These are valuable as:

```text
development starting points
```

but should not automatically become:

```text
final Obstacle Challenge specifications
```

The final repository should eventually distinguish:

```text
CURRENT WORKING VALUE

TESTED RANGE

FINAL SELECTED VALUE

TEST EVIDENCE
```

Parameters that still require final validation include:

```text
Obstacle normal speed

approach speed

avoid speed

recovery speed

steering target step

Red steering bias

Green steering bias

visual correction gain

visual correction limit

target confirmation count

target relevance threshold

target-loss tolerance

wall-safety thresholds

pass-confirmation condition

recovery strength

recovery release condition

corner/obstacle authority

parking parameters
```

These should only receive final numerical documentation after representative testing.

---

# 7.24 Complete Software-Tuning Workflow

The full process can be summarized as:

```text
                        OBSERVE FAILURE
                              │
                              ▼
                     IDENTIFY FIRST BAD LAYER
                              │
       ┌──────────────────────┼──────────────────────┐
       │                      │                      │
       ▼                      ▼                      ▼
   PERCEPTION              CONTROL               RECOVERY
       │                      │                      │
       ▼                      ▼                      ▼
 select relevant        choose related          isolate final
 parameter              controller value        maneuver phase
       │                      │                      │
       └──────────────────────┼──────────────────────┘
                              ▼
                     CHANGE ONE VARIABLE
                              │
                              ▼
                      REPEAT SAME TEST
                              │
                              ▼
                     RECORD TELEMETRY
                              │
                              ▼
                       COMPARE VIDEO
                              │
                  ┌───────────┴───────────┐
                  │                       │
                  ▼                       ▼
                BETTER                   WORSE
                  │                       │
                  ▼                       ▼
             repeat tests           reject change
                  │                       │
                  ▼                       ▼
             save version          restore baseline
                  │
                  ▼
           NEXT CONTROL LAYER
```

This process converts tuning from random trial-and-error into traceable engineering work.

---

# 7.25 Final Engineering Assessment

Piolín's software tuning philosophy is based on **controlled experiments and clear controller responsibility**.

The current prototype programs already demonstrate several useful tuning mechanisms:

```text
bounded values with clamp()

short ultrasonic filtering

nonlinear control terms

steering target smoothing

closed-loop Motor B control

state-dependent speed

independent wall safety

candidate confirmation

event locking

release conditions

debug telemetry
```

The final Obstacle Challenge software extends these ideas to:

```text
Pixy target relevance

target confirmation

target lock

Red/Green avoidance

pass confirmation

recovery

corner interaction

parking
```

The obstacle rules themselves are not tuning parameters:

```text
RED
→ PASS RIGHT

GREEN
→ PASS LEFT
```

What must be tuned is how Piolín physically achieves those trajectories.

Likewise:

```text
S2 = LEFT

S3 = RIGHT
```

is a fixed hardware convention and should not be reversed to compensate for a controller problem.

Software tuning should always begin by identifying the first incorrect behavior in the sensor-to-actuator chain:

```text
SENSING
→ INTERPRETATION
→ STATE
→ CONTROLLER
→ FINAL COMMAND
→ PHYSICAL RESPONSE
```

Only the layer where behavior first becomes incorrect should normally be modified.

The central tuning principle is:

> **Do not search for numbers that make one complete run work. Identify one physical behavior, change the smallest relevant parameter set, repeat the same experiment, and preserve the configuration only when the improvement can be reproduced.**

Using this approach allows PiolínTech to improve speed, steering, vision, obstacle avoidance, safety, and recovery without losing track of why a particular software version behaves better than another.

---

<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
