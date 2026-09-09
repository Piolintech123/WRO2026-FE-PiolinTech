# 5. Obstacle Detection

<div align="center">

<img
  src="../../v-photos/v4/pixy21_front.jpg"
  alt="Pixy2.1 installed on Piolín for forward obstacle detection"
  width="700"
/>

<br>

<sub><b>Figure 5.1.</b> Pixy2.1 is Piolín's main forward-perception sensor during the Obstacle Challenge.</sub>

</div>

Obstacle detection in Piolín is not treated as:

```text
camera sees color
→ immediately steer
```

Instead, the software is being designed around a perception pipeline that separates:

```text
RAW PIXY DATA
      ↓
BLOCK VALIDATION
      ↓
TARGET CANDIDATES
      ↓
TARGET RELEVANCE
      ↓
TARGET CONFIRMATION
      ↓
ACTIVE TARGET
```

This distinction is important because Pixy2.1 may simultaneously observe:

```text
the current pillar

a farther pillar

small color regions

background detections

a parking reference
```

Only one of these should normally become the obstacle currently controlling Piolín.

The final detection thresholds are still under development. This document therefore describes the **current detection architecture and selection strategy**, not a finalized numerical vision model.

---

## 5.1 Current Vision Configuration

During the Obstacle Challenge, the active S1 device is:

```text
S1 → Pixy2.1
```

The Gyro Sensor is not installed in this configuration.

Piolín's current Pixy2.1 assembly also includes its **3D-printed casing**, which is treated as part of the calibrated camera installation.

The current trained signatures are:

| Signature | Physical Target | Software Meaning |
| :---: | :--- | :--- |
| `sig1` | Pink | Parking reference |
| `sig2` | Red | Obstacle — pass RIGHT |
| `sig3` | Green | Obstacle — pass LEFT |

The competition rule is fixed:

```text
RED
→ PASS RIGHT
```

```text
GREEN
→ PASS LEFT
```

The pillar's location in the camera image must never reverse those rules.

---

## 5.2 What Pixy2.1 Provides

<div align="center">

<img
  src="../../v-photos/v4/pixy21_red_detection.jpg"
  alt="Pixy2.1 detecting a red pillar"
  width="690"
/>

<br>

<sub><b>Figure 5.2.</b> A Pixy block contains more information than color alone; its image geometry can help determine whether the object is relevant to the current maneuver.</sub>

</div>

The detection layer is expected to work with block information including:

```text
signature

x

y

width

height
```

These values answer different questions.

```text
signature
→ What object category was detected?
```

```text
x
→ Where is it horizontally in the camera frame?
```

```text
y
→ Where is it vertically in the camera frame?
```

```text
width / height
→ How large does it appear?
```

The software should preserve this separation.

For example:

```text
sig2
```

determines:

```text
RED
→ pass RIGHT
```

while `x` can help determine how the target is positioned relative to Piolín's current camera view.

---

# 5.3 Detection Is Not Yet a Driving Command

A major software rule is:

> **Pixy detects objects; it does not directly control Motor B.**

The desired architecture is:

```text
PIXY
  ↓
DETECTION
  ↓
TARGET SELECTION
  ↓
STATE MACHINE
  ↓
OBSTACLE CONTROLLER
  ↓
STEERING ARBITRATION
  ↓
MOTOR B
```

This makes troubleshooting much easier.

For example:

```text
Pixy says RED
```

and:

```text
state machine says PASS RIGHT
```

but:

```text
physical wheels turn LEFT
```

means the error is probably not in color recognition.

The failure is likely later in:

```text
steering sign

control arbitration

Motor B command

mechanical response
```

Separating detection from actuation prevents the camera from being blamed for every trajectory problem.

---

# 5.4 Block Validation

Not every block returned by Pixy should automatically become a valid obstacle candidate.

The first stage should reject information that cannot represent a useful current target.

Conceptually:

```python
RED_SIG = 2
GREEN_SIG = 3

def valid_obstacle_signature(signature):
    return signature in (RED_SIG, GREEN_SIG)
```

A more complete validation function can later check that the block also contains plausible geometry:

```python
def valid_obstacle_block(block):

    if block is None:
        return False

    if block.signature not in (RED_SIG, GREEN_SIG):
        return False

    if block.width <= 0 or block.height <= 0:
        return False

    return True
```

This is **illustrative architecture**, not final Pixy communication code.

The purpose is to prevent:

```text
invalid block

unknown signature

empty geometry
```

from entering the obstacle-selection layer.

---

# 5.5 Candidate Detection and Confirmation

One useful pattern already tested elsewhere in Piolín is requiring repeated evidence before accepting a sensor event.

The current Color Sensor prototype does:

```python
if detected == candidate_color:
    candidate_count += 1
else:
    candidate_color = detected
    candidate_count = 1
```

and only accepts the candidate after:

```python
if candidate_count >= COLOR_CONFIRMATIONS:
```

Obstacle detection can use the same architectural principle.

Conceptually:

```text
one Red frame
→ possible Red candidate
```

```text
several consistent observations
→ confirmed Red target
```

A future implementation may resemble:

```python
if candidate.signature == previous_candidate_signature:
    target_confirmations += 1
else:
    previous_candidate_signature = candidate.signature
    target_confirmations = 1

if target_confirmations >= TARGET_CONFIRMATIONS:
    active_target = candidate
```

The final number of confirmations remains a calibration parameter.

Too little confirmation can create:

```text
false reactions
```

while too much confirmation can create:

```text
late reactions
```

The correct value must be determined dynamically at Piolín's real driving speed.

---

# 5.6 Target Relevance

Visibility alone is not enough.

A very distant pillar may be visible but should not necessarily take control of steering immediately.

The software therefore needs a concept of:

```text
TARGET RELEVANCE
```

A candidate can be evaluated using some combination of:

```text
signature validity

apparent width

apparent height

horizontal position

vertical position

current navigation state

previous target
```

The architecture may conceptually calculate:

```python
def target_relevance(block):

    if not valid_obstacle_block(block):
        return 0.0

    score = 0.0

    # Apparent size can contribute to relevance.
    score += block.width
    score += block.height

    return score
```

This example intentionally does **not** define the final scoring formula.

The final controller may need more sophisticated weighting, but the architectural requirement is:

```text
detect all useful candidates
      ↓
compare relevance
      ↓
select one obstacle
```

rather than:

```text
use first block returned by camera
```

---

# 5.7 Why "First Block Wins" Is Weak

Suppose Pixy sees:

```text
near Red pillar

far Green pillar
```

If the camera happens to return Green first:

```text
blocks[0] = Green
```

a naive controller could begin:

```text
PASS LEFT
```

even though the physically relevant obstacle is the nearby Red pillar.

Therefore:

```text
Pixy list order
```

should not automatically determine:

```text
navigation priority
```

The desired architecture is:

```python
best_target = None
best_score = None

for block in blocks:

    if not valid_obstacle_block(block):
        continue

    score = target_relevance(block)

    if best_target is None or score > best_score:
        best_target = block
        best_score = score
```

Again, this is architectural example code.

The real relevance function remains under calibration.

The important point is that **selection is deliberate**.

---

# 5.8 Signature Determines Passing Side

<div align="center">

<img
  src="../../v-photos/v4/pixy21_green_detection.jpg"
  alt="Pixy2.1 detecting a green obstacle"
  width="690"
/>

<br>

<sub><b>Figure 5.3.</b> Green classification determines the pass-left rule regardless of the block's current horizontal image position.</sub>

</div>

Obstacle identity and obstacle image position must remain separate.

The required function can conceptually be:

```python
def required_pass_side(signature):

    if signature == 2:
        return "RIGHT"

    if signature == 3:
        return "LEFT"

    return None
```

Therefore:

```text
sig2
→ RED
→ RIGHT
```

and:

```text
sig3
→ GREEN
→ LEFT
```

A Red pillar that currently appears at:

```text
x < image center
```

is still:

```text
PASS RIGHT
```

Likewise, a Green pillar appearing at:

```text
x > image center
```

remains:

```text
PASS LEFT
```

This distinction prevents camera perspective from accidentally reversing competition logic.

---

# 5.9 Image Coordinates Affect Steering Strength, Not the Rule

The horizontal coordinate `x` can still be extremely useful.

It helps answer:

```text
How far from the current camera center is the target?
```

Conceptually, the camera can define:

```text
IMAGE CENTER
       │
       ▼
pillar x
       │
       ▼
visual error
```

A future calculation might begin with:

```python
visual_error = block.x - PIXY_CENTER_X
```

and limit that value using the same kind of bounded-control pattern already used elsewhere in Piolín:

```python
visual_error = clamp(
    visual_error,
    -MAX_VISUAL_ERROR,
    MAX_VISUAL_ERROR
)
```

The current prototype already uses `clamp()` extensively:

```python
def clamp(value, minimum, maximum):
    if value < minimum:
        return minimum
    if value > maximum:
        return maximum
    return value
```

The obstacle controller can reuse this principle so that unusual camera values cannot create unlimited steering requests.

However:

```text
visual_error
```

should influence:

```text
magnitude / timing of avoidance
```

not:

```text
whether Red means LEFT or RIGHT
```

---

# 5.10 Apparent Size as Proximity Evidence

The Pixy block's:

```text
width

height
```

provide useful information about apparent target size.

In general:

```text
farther pillar
→ smaller block
```

while:

```text
closer pillar
→ larger block
```

under comparable viewing conditions.

This does **not** mean:

```text
width = exact physical distance
```

unless a separate calibration is performed.

Instead, apparent size can help classify conditions such as:

```text
visible but distant

becoming relevant

close

very close
```

The avoidance architecture can then respond progressively:

```text
small / distant target
→ observe
```

```text
relevant target
→ prepare
```

```text
close target
→ stronger maneuver authority
```

This prevents the vehicle from reacting with maximum steering to every tiny colored block visible at long range.

---

# 5.11 Target Lock

Once a pillar has been confirmed and selected, Piolín should not continuously replace it with whichever block looks best in the next frame.

Instead:

```text
TARGET_ACQUIRE
      ↓
confirmed pillar
      ↓
active_target
      ↓
TARGET LOCK
      ↓
AVOID
```

A conceptual structure is:

```python
if active_target is None:

    candidate = select_relevant_target(blocks)

    if candidate_is_confirmed(candidate):
        active_target = candidate
        state = AVOID
```

Once `active_target` exists:

```python
if state == AVOID:
    use_active_target()
```

rather than:

```python
if state == AVOID:
    active_target = select_relevant_target(blocks)
```

every cycle.

This prevents:

```text
Red
→ Green
→ Red
→ Green
```

switching during one physical pass.

---

# 5.12 Temporary Target Loss

A target can disappear from Pixy without being physically passed.

This is particularly important because:

```text
Piolín steers
      ↓
camera rotates
      ↓
pillar moves across image
      ↓
pillar may leave field of view
```

Therefore:

```text
no block this frame
```

should not automatically mean:

```text
forget target
```

A future state may preserve information such as:

```python
last_target_signature
last_target_x
last_target_width
target_missing_cycles
```

Conceptually:

```text
target visible
      ↓
target temporarily lost
      ↓
retain target identity briefly
      ↓
continue current maneuver
      ↓
use lateral geometry to determine clearance
```

The duration of this memory is still a calibration parameter.

Too short:

```text
maneuver can reverse immediately
```

Too long:

```text
old obstacle can remain locked after it is irrelevant
```

---

# 5.13 Ultrasonics Do Not Identify Pillar Color

The Obstacle Challenge uses sensor fusion, but each sensor retains its own responsibility.

```text
PIXY2.1
→ obstacle identity
```

```text
S2/S3
→ physical lateral geometry
```

The ultrasonic sensors cannot determine:

```text
Red

Green
```

and therefore should not decide:

```text
pass LEFT

pass RIGHT
```

Their role becomes important for:

```text
wall safety

physical proximity context

pillar-pass confirmation

post-pillar recovery
```

This separation reduces ambiguous control logic.

The detection architecture is therefore:

```text
CAMERA
→ WHAT obstacle?
```

while:

```text
ULTRASONICS
→ WHAT physical geometry exists around Piolín?
```

---

# 5.14 Detection and the State Machine

The detection layer should behave differently depending on the current state.

### During `NORMAL`

Pixy searches for new relevant targets.

```text
no target
→ continue normal navigation
```

```text
candidate
→ TARGET_ACQUIRE
```

### During `TARGET_ACQUIRE`

The software confirms and selects the target.

```text
confirmed
→ lock
→ AVOID
```

### During `AVOID`

The selected target remains authoritative.

New distant targets should not freely replace it.

### During `PASS_CONFIRM`

Pixy history and S2/S3 geometry help determine whether the pillar has actually been cleared.

### During `RECOVER`

The previous pillar is becoming irrelevant and the robot prepares to search for another target.

This architecture prevents the camera from having the same authority in every state.

---

# 5.15 Detection Around Corners

Corner handling creates a special vision condition.

When Piolín turns:

```text
chassis rotates

camera rotates

target x changes rapidly

new pillars can enter the field of view
```

Therefore a block appearing suddenly during `CORNER` should not always receive the same relevance as one appearing during a stable straight.

The controller can use:

```text
current state
```

inside target relevance.

Conceptually:

```python
if state == CORNER:
    # Treat new detections more carefully.
    relevance *= CORNER_VISION_FACTOR
```

The exact factor is not final.

The principle is that **visual geometry must be interpreted together with vehicle state**.

This prevents normal camera motion during a turn from being mistaken for sudden obstacle motion.

---

# 5.16 Parking Signature Is Not an Obstacle

<div align="center">

<img
  src="../../v-photos/v4/pixy21_parking_detection.jpg"
  alt="Pixy2.1 detecting the pink parking reference"
  width="680"
/>

<br>

<sub><b>Figure 5.4.</b> Signature 1 is reserved for parking and must remain separate from Red/Green obstacle selection.</sub>

</div>

The current Pixy mapping includes:

```text
sig1
→ Pink
→ parking
```

Pink should therefore not enter the normal Red/Green obstacle-selection pool.

Conceptually:

```python
def valid_obstacle_signature(signature):
    return signature in (2, 3)
```

while parking can be checked separately:

```python
def is_parking_signature(signature):
    return signature == 1
```

This prevents:

```text
Pink region
```

from accidentally producing:

```text
pillar avoidance
```

Likewise, Pink visibility should not immediately start parking.

The state machine should first verify that:

```text
course progress permits parking
```

before the Pink reference gains authority.

---

# 5.17 Detection Diagnostics

The obstacle detector should expose enough information to understand what Pixy sees and why one target was selected.

Useful telemetry includes:

```text
number of blocks

candidate signatures

selected signature

selected x

selected y

selected width

selected height

target score / relevance

target confirmed?

target locked?

current state
```

A useful debug line could look conceptually like:

```text
STATE: TARGET_ACQUIRE
BLOCKS: 2
BEST_SIG: 2
X: ...
W: ...
CONF: 2
LOCK: False
```

and later:

```text
STATE: AVOID
TARGET: RED
PASS: RIGHT
X: ...
W: ...
LOCK: True
```

This makes it possible to distinguish:

```text
camera never detected Red
```

from:

```text
camera detected Red
but target selector chose Green
```

from:

```text
Red selected correctly
but steering controller moved left
```

Those are three completely different failures.

---

# 5.18 Common Detection Failures

| Symptom | Most Likely Detection Layer |
| :--- | :--- |
| No pillar detected | Pixy connection, training, lighting, FOV |
| Red detected as Green | Signature training/mapping |
| Green detected as Red | Signature training/mapping |
| Very distant pillar controls robot | Relevance logic |
| Small background region becomes target | Candidate validation/relevance |
| Correct pillar visible but another selected | Multi-block target selection |
| Robot alternates between Red and Green | Target lock |
| Target disappears during steering and maneuver reverses | Temporary target-loss handling |
| Pink causes obstacle avoidance | Signature filtering |
| Correct Red target selected but robot goes left | Not detection; inspect downstream control |
| Correct Green selected but robot goes right | Not detection; inspect downstream control |

The key diagnostic principle is:

> **Do not change camera detection parameters when debug output already proves the correct target was selected.**

Once selection is correct, troubleshooting should continue downstream.

---

# 5.19 Intended Detection Pipeline

The planned obstacle-detection system can be summarized as:

```text
                         PIXY2.1
                            │
                            ▼
                      READ BLOCKS
                            │
                            ▼
                     VALIDATE DATA
                            │
                            ▼
                  FILTER SIGNATURES
                            │
                ┌───────────┴────────────┐
                │                        │
                ▼                        ▼
          sig2 / sig3                  sig1
          OBSTACLES                   PARKING
                │                        │
                ▼                        │
        BUILD CANDIDATES                  │
                │                        │
                ▼                        │
        SCORE RELEVANCE                  │
                │                        │
                ▼                        │
        SELECT BEST TARGET               │
                │                        │
                ▼                        │
           CONFIRM TARGET                │
                │                        │
                ▼                        │
             LOCK TARGET                 │
                │                        │
                ▼                        │
              AVOID                      │
                │                        │
                ▼                        │
          PASS_CONFIRM                   │
                │                        │
                ▼                        │
          RELEASE TARGET                 │
                │                        │
                └────────────┬───────────┘
                             ▼
                       NEXT STATE
```

The exact numerical scoring and confirmation thresholds are intentionally left open until repeated track testing determines which values are reliable.

---

# 5.20 Final Engineering Assessment

Piolín's obstacle-detection architecture is designed to convert Pixy2.1 block observations into a **stable, context-aware active target** before that target is allowed to influence vehicle steering.

The process is not:

```text
see color
→ turn
```

but:

```text
read
→ validate
→ classify
→ evaluate relevance
→ confirm
→ select
→ lock
→ pass
→ release
```

The current Pixy signature mapping is:

```text
sig1
→ Pink
→ parking
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

The fixed competition rules remain independent of camera position.

```text
signature
→ required passing side
```

while:

```text
x / y / width / height
→ visual geometry and target relevance
```

The detector also remains separate from the lateral ultrasonic system.

```text
Pixy2.1
→ identifies obstacle targets
```

while:

```text
S2 / S3
→ provide physical geometry and safety context
```

Patterns already tested elsewhere in Piolín's Python prototypes—particularly measurement validation, bounded values, candidate confirmation, event locking, and release conditions—provide the architectural basis for the final vision detector.

The exact Pixy target-ranking formula, number of confirmation frames, temporary target-memory duration, relevance thresholds, and multiple-block behavior remain under active development and should not be represented as final calibrated values yet.

The core detection principle is:

> **Seeing a colored block is only the beginning of obstacle perception. Piolín must determine whether the detection is valid, whether it is relevant, whether it is the correct current target, and whether enough evidence exists to commit to that target before steering authority is transferred to the obstacle controller.**

This separation allows the vision system to become more robust without coupling every camera change directly to Motor B behavior.

---

<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
