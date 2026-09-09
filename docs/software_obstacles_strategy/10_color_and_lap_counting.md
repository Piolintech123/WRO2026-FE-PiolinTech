# 10. Color Events and Lap Counting

<div align="center">

<img
  src="../../v-photos/v4/color_sensor_s4_installed.jpg"
  alt="Piolín downward-facing Color Sensor installed on S4"
  width="680"
/>

<br>

<sub><b>Figure 10.1.</b> The S4 Color Sensor converts physical Blue and Orange floor markings into course-progression events.</sub>

</div>

Piolín uses the downward-facing EV3 Color Sensor on **Sensor Port S4** as a physical course-state reference.

The Color Sensor does not continuously determine steering and does not detect the Red and Green traffic pillars. Instead, it observes the floor beneath the robot and converts specific course markings into discrete software events.

The software architecture separates:

```text
FLOOR CLASSIFICATION
        ↓
EVENT CONFIRMATION
        ↓
ONE PHYSICAL MARKING
        ↓
ONE SOFTWARE EVENT
        ↓
COURSE PROGRESSION
```

This distinction is essential because Piolín's main control loop executes many times while the sensor remains physically above the same colored strip.

Without event logic:

```text
BLUE
BLUE
BLUE
BLUE
```

could incorrectly become:

```text
4 course events
```

when physically Piolín crossed only one marking.

The intended result is:

```text
one physical marking
→ one confirmed event
```

---

## 10.1 Role of S4 in the Software Architecture

The permanent Color Sensor mapping is:

```text
S4 → EV3 Color Sensor
```

and remains the same in both competition configurations.

```text
OPEN

S1 → Gyro
S2 → Left US
S3 → Right US
S4 → Color
```

```text
OBSTACLES

S1 → Pixy2.1
S2 → Left US
S3 → Right US
S4 → Color
```

The sensor responsibilities remain separate:

```text
S4 COLOR SENSOR
→ floor landmarks
→ direction / progression
```

```text
PIXY2.1
→ Red / Green pillars
→ Pink parking reference
```

```text
S2 / S3
→ lateral geometry
```

This separation keeps course progression independent from obstacle perception.

---

# 10.2 Blue and Orange Floor Events

<div align="center">

<img
  src="../../v-photos/v4/color_sensor_blue_mark.jpg"
  alt="Piolín Color Sensor over a Blue floor marking"
  width="650"
/>

<br>

<sub><b>Figure 10.2.</b> Blue is one of the physical course landmarks used by Piolín's progression logic.</sub>

</div>

<div align="center">

<img
  src="../../v-photos/v4/color_sensor_orange_mark.jpg"
  alt="Piolín Color Sensor over an Orange floor marking"
  width="650"
/>

<br>

<sub><b>Figure 10.3.</b> Orange is the second course-marking category used by S4.</sub>

</div>

At the course-state level, the classifier should provide a simple result:

```text
BLUE

ORANGE

NONE
```

The lap-counting layer should not need to know whether the classifier internally used:

```text
built-in EV3 color categories
```

or:

```text
RGB + reflection thresholds
```

That responsibility belongs to the RGB detection layer.

The progression layer only needs to know:

```text
Has a valid Blue or Orange event occurred?
```

This allows RGB calibration to change without requiring the lap-counting logic to be rewritten.

---

# 10.3 The First Event Can Establish Direction

The first confirmed floor event has a special role.

Piolín's current course-direction convention is:

```text
BLUE first
→ COUNTERCLOCKWISE
```

```text
ORANGE first
→ CLOCKWISE
```

Conceptually:

```python
if direction is None:

    if floor_event == "BLUE":
        direction = "COUNTERCLOCKWISE"

    elif floor_event == "ORANGE":
        direction = "CLOCKWISE"
```

Once established, direction becomes persistent.

The software should not repeatedly redefine direction each time another floor color is detected.

The architecture is:

```text
START

direction = UNKNOWN
      ↓
first confirmed floor event
      ↓
direction selected
      ↓
direction remains fixed
```

Later Blue and Orange events primarily contribute to:

```text
course progression

corner / landmark count

lap tracking

parking eligibility
```

rather than redefining travel direction.

---

# 10.4 Raw Color Detection Is Not Yet a Count

One of Piolín's prototypes already demonstrates an important intermediate step: a detected color first becomes a **candidate**.

The code uses:

```python
candidate_color = None
candidate_count = 0
```

When a color appears:

```python
if detected == candidate_color:
    candidate_count += 1

else:
    candidate_color = detected
    candidate_count = 1
```

The event is only accepted after enough consistent observations:

```python
if candidate_count >= COLOR_CONFIRMATIONS:
```

This produces:

```text
RAW READING
     ↓
CANDIDATE
     ↓
CONFIRMATION
     ↓
VALID EVENT
```

The purpose is to prevent one unstable sensor sample from immediately changing course state.

The final number of required confirmations remains a calibration parameter because there is a trade-off:

```text
more confirmation
→ stronger noise rejection
→ slower event response
```

versus:

```text
less confirmation
→ faster response
→ greater sensitivity to unstable readings
```

---

# 10.5 Event Latching

Once a valid marking has been counted, Piolín must temporarily prevent another count.

One prototype uses:

```python
ready_for_new_color = False
```

after accepting a floor event.

Another development controller expresses the same idea with:

```python
line_latched = True
```

Architecturally both mean:

```text
CURRENT PHYSICAL MARKING
HAS ALREADY BEEN REGISTERED
```

The sequence becomes:

```text
normal floor
      ↓
colored marking
      ↓
confirm
      ↓
COUNT ONCE
      ↓
LATCH
      ↓
ignore repeated readings
```

This state memory is necessary because one physical marking can remain beneath S4 for many loop iterations.

---

# 10.6 Re-Arming After Leaving the Marking

The simpler prototype does not immediately allow a second event.

Instead, it waits for several readings without a recognized floor color:

```python
if detected is None:
    release_count += 1

    if release_count >= COLOR_RELEASE_CONFIRMATIONS:
        ready_for_new_color = True
        release_count = 0
```

This creates:

```text
COUNT
  ↓
LOCK
  ↓
wait until marking has been left
  ↓
confirm normal floor
  ↓
RE-ARM
```

This is more robust than:

```text
count
→ immediately ready again
```

because the boundary of a colored region may produce alternating measurements such as:

```text
BLUE

NONE

BLUE
```

within a very short physical distance.

A release requirement helps prevent this transition from becoming two separate course events.

---

# 10.7 Encoder Separation as a Second Protection Layer

Piolín's more advanced prototype also includes a **minimum physical progression requirement** between line counts.

The development code defines:

```python
MIN_LINE_ENCODER_DEG = 650.0
```

and checks the traveled Motor A encoder distance before accepting another event:

```python
enough_encoder = (
    line_count == 0
    or (enc_now - last_line_encoder)
       >= MIN_LINE_ENCODER_DEG
)
```

The architectural idea is more important than the current temporary number.

Piolín uses two forms of evidence:

```text
1. SENSOR RELEASE

2. VEHICLE PROGRESSION
```

before deciding that a newly detected marking can plausibly be a different course landmark.

The complete logic becomes:

```text
new color candidate
      ↓
confirmed
      ↓
not currently latched?
      ↓
enough physical travel since last event?
      ↓
COUNT
```

This adds robustness if the sensor briefly transitions through an uncertain region while still near the same marking.

The encoder threshold is a current working value and should be recalibrated if drivetrain geometry or event spacing changes.

---

# 10.8 Counting Course Progress

The current development target uses:

```text
12 significant course events / corners
```

to represent the intended:

```text
3 laps
```

of the Open-style course progression.

A prototype stores:

```python
line_count = 0
```

and increments only after a valid event:

```python
line_count += 1
```

A simpler prototype uses:

```python
count += 1
```

with:

```python
TOTAL_COUNTS = 12
```

The architecture should maintain one authoritative progression variable.

Conceptually:

```python
course_count = 0

def register_floor_event(event):
    global course_count

    course_count += 1
```

The event should be incremented by the event-management layer, not from every raw S4 reading.

This preserves:

```text
sensor reading
≠
course progression
```

until confirmation has occurred.

---

# 10.9 Deriving Lap Information

If the final course model uses four significant corner/landmark events per lap, the high-level course state can be derived conceptually from the count.

For example:

```text
events 0–3
→ Lap 1 progression

events 4–7
→ Lap 2 progression

events 8–11
→ Lap 3 progression

event 12
→ expected full-course progression reached
```

The exact implementation does not need to continuously store both:

```text
lap count
```

and:

```text
event count
```

if one can reliably be derived from the other.

A possible software model is:

```python
corner_count = course_count
lap_index = corner_count // 4
```

but the final implementation should match the actual event semantics used by the finished controller.

The important principle is that lap state should come from **confirmed physical course progression**, not from an independent timer.

---

# 10.10 Why Time Alone Is Not Enough

A weak progression strategy would be:

```text
drive for N seconds
→ assume one lap finished
```

This is sensitive to:

```text
battery condition

obstacle maneuvers

corner speed

recovery time

mechanical differences
```

Piolín instead uses physical landmarks as course-state evidence.

The sensor-based model is:

```text
physical track event
      ↓
confirmed S4 event
      ↓
increment progression
```

This gives the state machine a better relationship with the real course.

Time may still be useful for:

```text
timeouts

diagnostics

safety limits
```

but it should not be the primary lap-counting mechanism.

---

# 10.11 Course Counting During Obstacles

The Obstacle Challenge introduces an important complication: Piolín may temporarily move away from its normal trajectory while passing a pillar.

The floor-counting system should therefore remain independent of:

```text
AVOID

PASS_CONFIRM

RECOVER
```

as much as practical.

A valid course event can update:

```text
course_count
```

without directly commanding Motor B.

The state machine can then use the progression value as context.

For example:

```text
course_count says next corner is expected
```

can support:

```text
CORNER state
```

while:

```text
final progression reached
```

can support:

```text
PARKING enabled
```

The floor event itself should therefore update **state information**, not bypass the state machine.

---

# 10.12 Counting and Corner Handling

The relationship between color events and corner handling should be:

```text
FLOOR EVENT
      ↓
course state updated
      ↓
corner may now be expected
      ↓
geometry confirms transition
      ↓
CORNER
```

rather than:

```text
color appears
→ Motor B immediately turns
```

An early prototype intentionally used direct color-to-turn behavior:

```python
turn_for_color(candidate_color)
```

because it was useful for proving the basic sequence:

```text
detect
→ turn
→ count
```

The final architecture is more modular.

A stronger separation is:

```text
S4
→ reports physical landmark
```

```text
COURSE STATE
→ determines what this landmark means
```

```text
CORNER CONTROLLER
→ executes the physical turn
```

This makes it possible to improve RGB detection without changing corner steering and vice versa.

---

# 10.13 Counting and Parking

<div align="center">

<img
  src="../../v-photos/v4/parking_area.jpg"
  alt="Piolín parking area used for final progression testing"
  width="700"
/>

<br>

<sub><b>Figure 10.4.</b> Course counting determines when parking is allowed, but parking remains a separate high-level maneuver.</sub>

</div>

One development prototype currently activates parking when:

```python
if line_count >= LINES_TO_PARK:
    parking_active = True
```

with:

```python
LINES_TO_PARK = 12
```

This is useful because it demonstrates a clean architectural transition:

```text
COURSE COUNT
      ↓
required progression reached
      ↓
PARKING STATE ENABLED
```

The final parking maneuver should still use additional physical information.

For example, during Obstacles:

```text
sig1 = Pink
```

is reserved for the visual parking reference.

A stronger final condition is therefore:

```text
required course progression reached
+
parking state enabled
+
valid parking reference
+
appropriate physical geometry
```

before performing the final maneuver.

This prevents:

```text
Pink visible early
```

from starting parking before the course is complete.

---

# 10.14 Counter Reset and State Initialization

At the beginning of a new run, all progression variables should begin from a known state.

Conceptually:

```python
course_count = 0

direction = None

line_latched = False

candidate_color = None

candidate_count = 0

release_count = 0

last_line_encoder = None
```

This prevents information from a previous test from affecting the next run.

A correct startup sequence should therefore initialize:

```text
hardware

steering state

course direction

event detector

course progression

parking eligibility
```

before autonomous motion begins.

State initialization is especially important during repeated competition testing because one forgotten persistent variable can create behavior that appears random between runs.

---

# 10.15 Useful Debug Telemetry

Course-state debugging should expose enough information to determine why an event was or was not counted.

Useful values include:

```text
raw floor classification

candidate color

confirmation count

event latch

release count

Motor A encoder

last accepted encoder

course count

direction

current navigation state
```

For example:

```text
FLOOR: BLUE
CANDIDATE: BLUE
CONF: 2
LOCK: False
ENC: ...
COUNT: 5
DIR: CCW
```

After the event:

```text
EVENT: BLUE
COUNT: 6
LOCK: True
```

and later:

```text
FLOOR: NONE
RELEASE: 3
LOCK: False
```

This makes duplicate-counting problems much easier to diagnose.

---

# 10.16 Common Counting Failures

| Symptom | First Layer to Check |
| :--- | :--- |
| One line counted twice | Latch / release logic |
| One line counted several times | Event state not persisting |
| Valid line not counted | RGB/classification or confirmation |
| Works slowly but misses at speed | Confirmation delay / sampling |
| Two nearby events become one | Release or encoder separation too strict |
| Same line counts again after brief `None` | Release too permissive |
| First Blue gives wrong direction | Initial direction mapping |
| First Orange gives wrong direction | Initial direction mapping |
| Direction changes later | Direction state being overwritten |
| Count reaches 12 too early | Duplicate event(s) |
| Count never reaches expected total | Missed event(s) |
| Parking activates too early | Progression or duplicate count |
| Parking never activates | Missing event / wrong threshold |

The diagnostic order should be:

```text
RAW FLOOR VALUE
      ↓
CLASSIFICATION
      ↓
CONFIRMATION
      ↓
LATCH / RELEASE
      ↓
COURSE COUNT
      ↓
HIGH-LEVEL STATE
```

Changing parking logic will not fix a color event that was already counted twice several corners earlier.

---

# 10.17 Current Prototype Values vs. Final Logic

Several values currently appear in development code, including:

```text
TOTAL_COUNTS = 12

LINES_TO_PARK = 12

COLOR_CONFIRMATIONS = 2

COLOR_RELEASE_CONFIRMATIONS = 3

MIN_LINE_ENCODER_DEG = 650
```

These values are useful evidence of the current development direction.

However, they should be interpreted carefully.

```text
12 events
```

represents the current intended full-course progression model.

By contrast:

```text
confirmation count

release count

minimum encoder separation
```

are calibration values and may change as:

```text
driving speed

RGB detection

course geometry

sensor installation
```

are finalized.

The repository should therefore distinguish:

```text
COURSE STRUCTURE
```

from:

```text
DETECTION TUNING
```

rather than presenting every current constant as permanent.

---

# 10.18 Complete Event and Lap-Counting Pipeline

The current intended progression architecture can be represented as:

```text
                         TRACK FLOOR
                              │
                              ▼
                       COLOR SENSOR S4
                              │
                              ▼
                     FLOOR CLASSIFIER
                              │
                 ┌────────────┼────────────┐
                 │            │            │
                 ▼            ▼            ▼
               BLUE         ORANGE        NONE
                 │            │            │
                 └──────┬─────┘            │
                        ▼                  │
                 BUILD CANDIDATE           │
                        │                  │
                        ▼                  │
                   CONFIRM EVENT           │
                        │                  │
                        ▼                  │
                  CURRENTLY LATCHED?
                        │
                       NO
                        │
                        ▼
              ENOUGH PHYSICAL PROGRESS?
                        │
                       YES
                        │
                        ▼
                  REGISTER EVENT
                        │
                        ▼
                   INCREMENT COUNT
                        │
              ┌─────────┴─────────┐
              │                   │
              ▼                   ▼
     direction unknown?      direction known
              │                   │
             YES                  │
              │                   │
              ▼                   │
    BLUE → COUNTERCLOCKWISE        │
    ORANGE → CLOCKWISE             │
              │                   │
              └─────────┬─────────┘
                        ▼
                     LATCH
                        │
                        ▼
                  LEAVE MARKING
                        │
                        ▼
                 CONFIRM RELEASE
                        │
                        ▼
                     RE-ARM
                        │
                        ▼
               NEXT COURSE EVENT
                        │
                        ▼
               progression complete?
                        │
                       YES
                        │
                        ▼
                 PARKING ELIGIBLE
```

This keeps physical sensing, event management, course state, and final maneuver control separated.

---

# 10.19 Final Engineering Assessment

Piolín's lap-counting architecture does not treat every Color Sensor reading as an independent event.

Instead, S4 measurements pass through several software layers:

```text
CLASSIFY

CONFIRM

LATCH

COUNT

RELEASE

RE-ARM
```

This ensures that:

```text
one physical marking
```

is intended to become:

```text
one course event
```

rather than many repeated events from consecutive control cycles.

Piolín's prototypes already demonstrate two complementary protections.

The first uses:

```text
candidate confirmation
+
neutral-floor release
```

while the more advanced controller additionally uses:

```text
minimum Motor A encoder separation
```

between accepted events.

Together, these patterns provide a strong basis for final progression tracking.

The first confirmed event can additionally establish the course direction:

```text
BLUE first
→ COUNTERCLOCKWISE

ORANGE first
→ CLOCKWISE
```

while later events update course progression without redefining that direction.

The current development model uses:

```text
12 accepted course events
```

as the intended completion reference for:

```text
3 laps / 12 corners
```

before the final parking stage becomes available.

However, the event-confirmation thresholds and minimum encoder separation remain tunable parameters rather than immutable specifications.

Most importantly, course counting remains separate from direct steering.

```text
S4
→ physical landmark
```

```text
event detector
→ confirmed course event
```

```text
course state
→ progression information
```

```text
state machine
→ decides whether cornering, obstacle handling, or parking is appropriate
```

The central principle is:

> **Piolín should count physical progress, not software loop iterations. A floor marking becomes course state only after the sensor evidence has been confirmed, duplicate detections have been rejected, and the controller is confident that a new physical landmark has actually been crossed.**

This architecture allows PiolínTech to improve RGB classification, corner handling, lap tracking, and parking independently while preserving one reliable representation of where the robot is in the course.

---

<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
