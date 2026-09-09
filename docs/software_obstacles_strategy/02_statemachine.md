# 2. State Machine

<div align="center">

<img
  src="../../v-photos/v4/piolin_obstacle_top.jpg"
  alt="Top view of Piolín in its Obstacle Challenge configuration"
  width="740"
/>

<br>

<sub><b>Figure 2.1.</b> Piolín's Obstacle Challenge controller is being organized as a state machine so that perception, obstacle avoidance, recovery, cornering, and parking do not compete for steering authority simultaneously.</sub>

</div>

Piolín's Obstacle Challenge software is being developed around an explicit **state-machine architecture**.

The purpose of the state machine is to answer one fundamental question during every control cycle:

> **What is Piolín currently trying to accomplish?**

Without an explicit state, several valid controllers could attempt to command Motor B at the same time.

For example:

```text
wall geometry
→ steer toward the preferred track position
```

while:

```text
Red pillar
→ pass to the RIGHT
```

and simultaneously:

```text
right wall too close
→ steer LEFT for safety
```

If these commands are applied without context, they can cancel one another or create unstable steering.

The state machine solves this by defining which objective currently has authority.

The intended high-level sequence is:

```text
START
  ↓
ACQUIRE
  ↓
NORMAL
  ↓
TARGET_ACQUIRE
  ↓
AVOID
  ↓
PASS_CONFIRM
  ↓
RECOVER
  ↓
NORMAL
```

with additional transitions to:

```text
CORNER

PARKING

STOP
```

The exact thresholds and some transition conditions are still being calibrated. Therefore, this document defines the **current software design direction**, not a frozen final competition implementation.

---

## 2.1 Why Piolín Needs Explicit States

A purely reactive controller might operate like:

```text
if Red:
    steer right

if Green:
    steer left

if left wall close:
    steer right

if right wall close:
    steer left
```

The problem is that several conditions can be true simultaneously.

For example:

```text
RED detected
+
right wall becoming close
+
normal controller wants center
```

The software then has three different steering objectives.

Piolín instead uses the idea:

```text
SENSORS
    ↓
INTERPRETATION
    ↓
CURRENT STATE
    ↓
ACTIVE CONTROLLER
    ↓
FINAL COMMAND
```

Each state decides:

```text
which sensor information matters most

which controller has priority

which events can cause a transition

which events should temporarily be ignored
```

This makes the vehicle behavior easier to understand and debug.

---

# 2.2 State Concepts Already Present in the Prototypes

The final Obstacle state machine is still under development, but Piolín's existing programs already contain several examples of state-based behavior.

One current controller distinguishes between:

```text
ACQUIRE
```

and:

```text
NORMAL
```

using the traveled distance:

```python
acquire_progress = clamp(
    travelled / ACQUIRE_DISTANCE_DEG,
    0.0,
    1.0
)
```

The resulting controller behavior changes according to that progress:

```python
if acquire_progress < 1.0:
    drive.run(ACQUIRE_SPEED)

elif abs(combined_offset) >= TURN_STEER_THRESHOLD:
    drive.run(TURN_SPEED)

else:
    drive.run(DRIVE_SPEED)
```

The same prototype later enters a different final condition:

```python
if parking_active:
```

which changes both steering and propulsion behavior.

This already demonstrates the core idea:

```text
SAME ROBOT

different state
      ↓
different controller behavior
```

The Obstacle Challenge expands that concept to pillar detection and recovery.

---

# 2.3 Event States Already Used by Piolín

The simpler floor-color prototype provides an especially useful model for obstacle-state design.

It distinguishes between:

```text
candidate detected

candidate confirmed

event accepted

event locked

event released
```

The prototype stores:

```python
candidate_color = None
candidate_count = 0

ready_for_new_color = True
release_count = 0
```

A color does not immediately become a navigation event.

It first becomes a candidate:

```python
if detected == candidate_color:
    candidate_count += 1
else:
    candidate_color = detected
    candidate_count = 1
```

Only after confirmation:

```python
if candidate_count >= COLOR_CONFIRMATIONS:
```

is the event accepted.

Afterward, the system prevents the same physical line from triggering repeatedly:

```python
ready_for_new_color = False
release_count = 0
```

and waits for a release condition before becoming ready again.

This creates:

```text
DETECT
  ↓
CONFIRM
  ↓
LOCK
  ↓
PHYSICAL EVENT OCCURS
  ↓
RELEASE
  ↓
READY AGAIN
```

The same architecture is being generalized for Pixy obstacle handling.

---

# 2.4 Planned Obstacle State Model

The current design direction uses the following major states:

| State | Primary Objective |
| :--- | :--- |
| `START` | Initialize and validate the robot |
| `ACQUIRE` | Enter a safe usable track trajectory |
| `NORMAL` | Maintain general track geometry |
| `TARGET_ACQUIRE` | Evaluate and confirm a relevant Pixy target |
| `AVOID` | Pass the selected pillar on the required side |
| `PASS_CONFIRM` | Determine whether the pillar is physically cleared |
| `RECOVER` | Restore useful track geometry |
| `CORNER` | Execute a track corner without obstacle control conflict |
| `PARKING` | Execute the final parking sequence |
| `STOP` | Safely stop propulsion and steering activity |

The intended cycle is not necessarily:

```text
NORMAL
→ AVOID
→ NORMAL
```

because a successful obstacle maneuver requires more than simply steering around the pillar.

Instead:

```text
NORMAL
      ↓
TARGET_ACQUIRE
      ↓
AVOID
      ↓
PASS_CONFIRM
      ↓
RECOVER
      ↓
NORMAL
```

This separates perception, avoidance, clearance confirmation, and recovery into different responsibilities.

---

# 2.5 START State

`START` exists to establish known initial conditions before Piolín begins normal autonomous movement.

Its responsibilities include:

```text
initialize Motor A

initialize Motor B

verify S1 Pixy2.1

verify S2 Left Ultrasonic

verify S3 Right Ultrasonic

verify S4 Color Sensor

establish steering center

clear temporary target information

clear course-state variables
```

The authoritative Obstacle configuration is:

```text
A  = propulsion

B  = steering

S1 = Pixy2.1

S2 = LEFT Ultrasonic

S3 = RIGHT Ultrasonic

S4 = Color Sensor
```

The state should only leave `START` when the software has enough information to begin controlled motion.

Conceptually:

```python
state = START

if hardware_ready:
    state = ACQUIRE
```

This is representative architecture rather than the final literal implementation.

The important point is that normal motion should not begin while the controller still has undefined state information.

---

# 2.6 ACQUIRE State

`ACQUIRE` handles the initial transition from an arbitrary valid starting position toward a safer normal trajectory.

This idea already exists directly in Piolín's current development code.

Instead of immediately forcing the robot toward one fixed wall target, the prototype measures its actual starting geometry:

```python
start_center_mm = estimate_center_position(
    start_left,
    start_right
)
```

Then it progressively moves the desired target:

```python
active_target_center = (
    start_center_mm
    + acquire_progress
    * (TARGET_CENTER_MM - start_center_mm)
)
```

This prevents:

```text
large initial geometric error
      ↓
large steering request
      ↓
robot crosses aggressively
      ↓
collision
```

The architectural lesson is important for Obstacles as well.

`ACQUIRE` should be a transitional state where:

```text
steering authority is limited

speed can be lower

large abrupt corrections are discouraged

safe geometry is established
```

Once Piolín reaches a usable trajectory:

```text
ACQUIRE
    ↓
NORMAL
```

---

# 2.7 NORMAL State

`NORMAL` is the default driving state when no immediate pillar maneuver, corner, parking action, or critical safety condition requires stronger authority.

Its main information comes from:

```text
S2 Left Ultrasonic

S3 Right Ultrasonic
```

The objective is not necessarily to force Piolín to the exact mathematical center of the entire corridor.

Instead, it should maintain:

```text
usable lateral geometry

safe wall clearance

stable trajectory

readiness for the next pillar or corner
```

During `NORMAL`, Pixy2.1 continues observing the environment.

However:

```text
visible pillar
```

does not automatically mean:

```text
immediately enter AVOID
```

A visual block first passes through the target-acquisition process.

Conceptually:

```python
if state == NORMAL:

    normal_steering = calculate_wall_geometry()

    if relevant_pixy_candidate:
        state = TARGET_ACQUIRE
```

This prevents weak or distant detections from instantly changing the vehicle trajectory.

---

# 2.8 TARGET_ACQUIRE State

<div align="center">

<img
  src="../../v-photos/v4/pixy21_red_detection.jpg"
  alt="Pixy2.1 detecting a red obstacle"
  width="680"
/>

<br>

<sub><b>Figure 2.2.</b> Visual detection should first create a candidate target; a single Pixy observation does not necessarily need to trigger a complete avoidance maneuver.</sub>

</div>

`TARGET_ACQUIRE` exists between:

```text
Pixy sees something
```

and:

```text
Piolín commits to avoiding it
```

The camera may provide:

```text
signature

x

y

width

height
```

The software should evaluate whether the block is:

```text
a valid obstacle signature

sufficiently relevant

consistent with the current trajectory

more relevant than other visible blocks
```

The obstacle signatures are:

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

A target-acquisition sequence may conceptually resemble the confirmation architecture already tested with floor colors:

```text
candidate
    ↓
confirmation
    ↓
accepted target
```

Possible future code structure:

```python
if candidate.signature in (RED_SIG, GREEN_SIG):
    candidate_hits += 1

if candidate_hits >= TARGET_CONFIRMATIONS:
    active_target = candidate
    state = AVOID
```

This snippet represents the intended architecture; the final numerical confirmation rule is still under development.

---

# 2.9 Target Selection and Multiple Blocks

Pixy2.1 can see more than one valid object.

For example:

```text
near Red

far Green
```

or:

```text
Red left in frame

Green near center
```

The state machine must prevent target-selection logic from constantly changing the active maneuver.

`TARGET_ACQUIRE` is where candidate comparison belongs.

A conceptual pipeline is:

```text
PIXY BLOCKS
     ↓
remove invalid signatures
     ↓
evaluate relevance
     ↓
compare candidates
     ↓
choose best target
     ↓
confirm
     ↓
lock
```

The exact relevance formula is not final.

It may eventually use a combination of:

```text
signature

x

y

width

height

previous target

current vehicle state
```

The important architecture decision is that **selection occurs before avoidance**.

---

# 2.10 AVOID State

Once a target is confirmed, Piolín enters `AVOID`.

This state has one dominant objective:

```text
pass the active pillar on the side required by its color
```

The rule never changes:

```text
RED
→ PASS RIGHT
```

```text
GREEN
→ PASS LEFT
```

Pixy image position does not redefine that rule.

Therefore:

```text
signature
→ determines maneuver side
```

while:

```text
x / y / width / height
→ influence geometry and maneuver strength
```

A conceptual controller is:

```python
if state == AVOID:

    if active_target.signature == RED_SIG:
        required_side = RIGHT

    elif active_target.signature == GREEN_SIG:
        required_side = LEFT
```

The controller can then calculate steering based on:

```text
required side

target image geometry

current wall clearance

vehicle state
```

but the required passing side remains fixed.

---

# 2.11 Control Priority During AVOID

One important reason for having `AVOID` as an explicit state is to stop the normal wall controller from fighting the obstacle maneuver.

During `NORMAL`:

```text
wall geometry
→ main trajectory influence
```

During `AVOID`:

```text
pillar objective
→ main trajectory influence
```

while:

```text
wall sensors
→ safety/context
```

This distinction is critical.

Suppose:

```text
Red pillar
→ obstacle controller requests RIGHT
```

while:

```text
normal centering
→ requests LEFT
```

If both controllers receive equal authority:

```text
RIGHT + LEFT
→ weak or unstable response
```

The state machine instead establishes:

```text
if AVOID:
    obstacle controller dominates
```

Normal geometry should not continuously undo the maneuver.

---

# 2.12 Safety Is Higher Than the Navigation State

Although `AVOID` has strong authority, critical wall safety remains above it.

This principle is already present in the prototype:

```python
wall_active, wall_cmd, wall_speed = side_wall_guard(
    left,
    right
)

if wall_active:
    combined_offset = wall_cmd
```

The important architectural relationship is:

```text
NAVIGATION COMMAND
       ↓
SAFETY CHECK
       ↓
FINAL COMMAND
```

The state machine may request:

```text
PASS RIGHT
```

but if Piolín reaches an unsafe right-wall distance, the physical safety layer can temporarily reduce or redirect that command.

The hierarchy becomes approximately:

```text
CRITICAL WALL SAFETY

        ↓

ACTIVE MANEUVER

        ↓

NORMAL GEOMETRY
```

Safety does not decide which pillar to pass.

It only prevents the selected maneuver from driving Piolín into an immediate physical boundary.

---

# 2.13 Why AVOID Must Lock the Target

Without target locking, Pixy can observe different objects during the same maneuver.

For example:

```text
Red selected
      ↓
Piolín starts right
      ↓
camera angle changes
      ↓
Green becomes more visible
      ↓
controller switches left
```

That would produce unstable behavior.

The state machine therefore maintains:

```text
active_target
```

through the maneuver.

Conceptually:

```python
if state == AVOID:
    target = active_target
```

rather than:

```python
if state == AVOID:
    target = newest_pixy_block
```

This is the obstacle equivalent of the event latch already tested in Piolín's color code.

The current color system does:

```python
ready_for_new_color = False
```

after accepting one event.

Obstacle logic follows the same principle:

```text
current target active
→ do not freely accept another target yet
```

---

# 2.14 PASS_CONFIRM State

One of the most important distinctions in the state machine is:

```text
target disappeared from camera
```

is not the same as:

```text
pillar physically passed
```

When Piolín steers around a pillar, the camera also rotates with the chassis.

The pillar may leave Pixy's field of view simply because the camera is no longer pointing toward it.

Therefore the transition should not be:

```text
Pixy target gone
      ↓
NORMAL
```

Instead:

```text
AVOID
  ↓
visual evidence decreases
  ↓
PASS_CONFIRM
```

`PASS_CONFIRM` evaluates whether the physical maneuver has actually progressed far enough to release the target.

Useful evidence can include:

```text
recent Pixy target history

S2 distance

S3 distance

change in lateral geometry

vehicle progression

current maneuver side
```

The exact final confirmation threshold remains under development.

---

# 2.15 Ultrasonic Pass Confirmation

The lateral ultrasonic sensors can provide physical evidence after Piolín travels alongside a pillar.

Conceptually, one lateral sensor may observe:

```text
open geometry
      ↓
pillar approaches beside robot
      ↓
distance changes
      ↓
pillar moves behind robot
      ↓
distance opens again
```

That pattern can help determine that the vehicle has passed the obstacle.

The intended relationship is:

```text
PIXY
→ helps initiate and guide the maneuver
```

while:

```text
S2 / S3
→ help determine physical clearance
```

This prevents camera target loss from being the only pass criterion.

---

# 2.16 RECOVER State

<div align="center">

<img
  src="../../v-photos/v4/obstacle_green_run.jpg"
  alt="Piolín performing a green obstacle maneuver"
  width="700"
/>

<br>

<sub><b>Figure 2.3.</b> After passing a pillar, Piolín must transition through recovery before normal wall-relative navigation fully resumes.</sub>

</div>

Once the pillar is confirmed as cleared:

```text
PASS_CONFIRM
      ↓
RECOVER
```

The goal changes completely.

During `AVOID`:

```text
clear pillar on required side
```

During `RECOVER`:

```text
restore useful track geometry
```

The recovery controller can use:

```text
S2

S3

current steering angle

recent maneuver direction
```

to produce a controlled countersteer.

The desired sequence is:

```text
pillar cleared
      ↓
countersteer begins
      ↓
vehicle returns toward safe geometry
      ↓
steering demand reduces
      ↓
normal geometry becomes valid
      ↓
NORMAL
```

The transition should not create an immediate full reversal of Motor B.

---

# 2.17 Preventing Avoidance and Recovery from Fighting

The difference between `AVOID` and `RECOVER` is important because both can request opposite steering.

For example:

```text
Red
→ avoidance steers RIGHT
```

then:

```text
pillar cleared
→ recovery may steer LEFT
```

If the state changes too early:

```text
Piolín steers back into pillar
```

If it changes too late:

```text
Piolín continues toward outside wall
```

Therefore:

```text
PASS_CONFIRM
```

exists between them.

The transition becomes:

```text
AVOID

still clearing pillar
       ↓
do not recover yet

PASS_CONFIRM

clearance evidence sufficient
       ↓
RECOVER
```

This is more robust than switching based on one missing Pixy frame.

---

# 2.18 Returning from RECOVER to NORMAL

Recovery should also have a release condition.

Piolín should not remain in `RECOVER` indefinitely.

A future transition can be based on evidence such as:

```text
lateral geometry inside acceptable region

steering demand reduced

walls no longer unsafe

current obstacle no longer physically relevant
```

Conceptually:

```python
if state == RECOVER:

    if geometry_is_stable:
        active_target = None
        state = NORMAL
```

The exact `geometry_is_stable` definition remains a calibration problem.

The architectural requirement is that the active target is not discarded until the maneuver that depends on it is complete.

---

# 2.19 CORNER State

Obstacle navigation must coexist with track corners.

A corner is not simply a stronger wall correction.

It represents a different geometric condition.

Therefore a dedicated `CORNER` state can prevent normal wall geometry or pillar recovery from interpreting corner measurements incorrectly.

Conceptually:

```text
NORMAL
  ↓
corner evidence
  ↓
CORNER
  ↓
turn completed
  ↓
geometry reacquired
  ↓
NORMAL
```

If an obstacle and corner occur near one another, the final controller will need a clear arbitration rule.

That interaction is still being developed.

The architecture should avoid a situation where:

```text
corner controller
+
pillar controller
+
normal wall controller
```

all receive full authority simultaneously.

---

# 2.20 Color Sensor and State Progression

S4 remains a course-state sensor.

The existing prototype already demonstrates how one physical color region can be converted into one software event.

The important code pattern is:

```python
if candidate_count >= COLOR_CONFIRMATIONS:
```

followed by:

```python
ready_for_new_color = False
```

and later:

```python
if release_count >= COLOR_RELEASE_CONFIRMATIONS:
    ready_for_new_color = True
```

This architecture allows S4 to update higher-level information such as:

```text
course progress

corner count

lap state

parking eligibility
```

without allowing one marking to create multiple state transitions.

The state machine can therefore receive:

```text
new_floor_event
```

instead of directly processing every raw color sample.

---

# 2.21 PARKING State

<div align="center">

<img
  src="../../v-photos/v4/parking_area.jpg"
  alt="Piolín parking area used during final-state development"
  width="700"
/>

<br>

<sub><b>Figure 2.4.</b> Parking is treated as a dedicated high-level state rather than as an immediate response to one visual or floor detection.</sub>

</div>

`PARKING` should only become available when the course state indicates that the run is sufficiently complete.

During Obstacles:

```text
sig1 = Pink
```

is reserved as the parking visual reference.

However:

```text
Pink detected
```

should not automatically mean:

```text
state = PARKING
```

because a visual detection without course context could occur at the wrong time.

The stronger conceptual transition is:

```text
required course progression complete
+
parking allowed
+
valid parking reference
      ↓
PARKING
```

The current Open prototype already demonstrates the value of having a separate parking state:

```python
if line_count >= LINES_TO_PARK:
    parking_active = True
    parking_start_encoder = enc_now
```

and then:

```python
if parking_active:
```

uses a different drive/steering behavior.

The final obstacle-parking condition will be more specialized, but the architectural pattern remains valid.

---

# 2.22 STOP State

`STOP` represents the final safe state.

Its objective is simple:

```text
stop propulsion

return or hold steering safely

end active navigation
```

The existing prototypes already use patterns such as:

```python
drive.stop(Stop.BRAKE)
```

and:

```python
steer.stop(Stop.BRAKE)
```

or:

```python
drive.hold()
```

depending on the active environment and test.

A final program should ensure that unexpected program termination also leaves the vehicle in a safe condition whenever practical.

---

# 2.23 State Transitions Should Use Evidence, Not Time Alone

Timed maneuvers are useful during early development.

For example, one prototype currently uses:

```python
drive.run(TURN_SPEED)
wait(TURN_TIME_MS)
```

for a simple color-triggered turn.

That is useful for proving that:

```text
detect event
→ perform maneuver
→ return to center
```

works as a basic state sequence.

However, the final Obstacle state machine should increasingly prefer transitions based on physical evidence.

Instead of:

```text
avoid for 700 ms
→ assume pillar passed
```

the intended architecture is closer to:

```text
avoid
      ↓
observe target geometry
      ↓
observe lateral geometry
      ↓
confirm clearance
      ↓
recover
```

Time can still be used for:

```text
timeouts

short target-memory windows

safety limits
```

but should not be the only representation of physical position.

---

# 2.24 Main State Variable

A final implementation may use a centralized state variable.

For example:

```python
STATE_START = 0
STATE_ACQUIRE = 1
STATE_NORMAL = 2
STATE_TARGET_ACQUIRE = 3
STATE_AVOID = 4
STATE_PASS_CONFIRM = 5
STATE_RECOVER = 6
STATE_CORNER = 7
STATE_PARKING = 8
STATE_STOP = 9

state = STATE_START
```

or descriptive strings/enumerations.

The exact representation is less important than having one authoritative state.

The main loop can then become conceptually:

```python
while running:

    read_sensors()
    update_perception()

    if state == STATE_START:
        handle_start()

    elif state == STATE_ACQUIRE:
        handle_acquire()

    elif state == STATE_NORMAL:
        handle_normal()

    elif state == STATE_TARGET_ACQUIRE:
        handle_target_acquire()

    elif state == STATE_AVOID:
        handle_avoid()

    elif state == STATE_PASS_CONFIRM:
        handle_pass_confirm()

    elif state == STATE_RECOVER:
        handle_recover()

    elif state == STATE_CORNER:
        handle_corner()

    elif state == STATE_PARKING:
        handle_parking()

    elif state == STATE_STOP:
        stop_robot()
```

This is **illustrative architecture**, not copied final competition code.

It shows how individual behaviors can remain isolated while sharing one central sensor-update loop.

---

# 2.25 Proposed State Data

Some variables should persist across multiple control cycles because a state machine has memory.

Possible high-level state data includes:

```python
state
active_target
target_signature
target_last_seen
target_confirmations
course_progress
parking_enabled
```

Target information may conceptually contain:

```text
signature

x

y

width

height

time / cycle last observed
```

This allows the software to distinguish:

```text
"I currently see a Red block"
```

from:

```text
"I am currently passing the Red pillar
that was selected several cycles ago."
```

That distinction is essential for stable target locking.

---

# 2.26 State and Controller Priority

The state machine and safety system together determine the controller hierarchy.

A simplified design is:

| Condition / State | Main Steering Authority |
| :--- | :--- |
| Critical wall condition | Wall safety override |
| `AVOID` | Pillar avoidance |
| `PASS_CONFIRM` | Existing maneuver + clearance logic |
| `RECOVER` | Recovery controller |
| `CORNER` | Corner controller |
| `ACQUIRE` | Initial geometry controller |
| `NORMAL` | Normal wall/track geometry |
| `PARKING` | Parking controller |

The final steering flow becomes:

```text
STATE
  ↓
STATE CONTROLLER
  ↓
requested steering
  ↓
SAFETY OVERRIDE?
  ↓
bounded steering
  ↓
smooth target
  ↓
Motor B
```

This is preferable to allowing every available controller to independently command Motor B.

---

# 2.27 Debugging the State Machine

State information should be visible during development.

A useful Obstacle diagnostic line could contain:

```text
STATE

ACTIVE TARGET

SIGNATURE

X

WIDTH

S2

S3

FINAL COMMAND
```

For example:

```text
STATE: AVOID
SIG: RED
X: ...
W: ...
S2: ...
S3: ...
CMD: RIGHT
```

or:

```text
STATE: RECOVER
TARGET: RED
S2: ...
S3: ...
CMD: LEFT
```

This makes failures easier to classify.

Suppose Piolín physically moves left around a Red pillar.

If debug reports:

```text
STATE = AVOID
TARGET = RED
COMMAND = RIGHT
```

then the state machine and Red/Right rule may be correct.

The failure is probably downstream:

```text
steering sign

Motor B actuation

physical linkage
```

But if debug reports:

```text
STATE = RECOVER
```

before the Red pillar has actually been passed, then the likely failure is:

```text
state transition occurred too early
```

State telemetry therefore provides much more information than observing only the final trajectory.

---

# 2.28 Intended Complete State Flow

The current design can be summarized as:

```text
                              START
                                │
                                ▼
                             ACQUIRE
                                │
                                ▼
                              NORMAL
                                │
                 ┌──────────────┼──────────────┐
                 │              │              │
                 ▼              ▼              ▼
          course corner?   pillar candidate?  run complete?
                 │              │              │
                YES            YES            YES
                 │              │              │
                 ▼              ▼              ▼
              CORNER      TARGET_ACQUIRE     PARKING
                 │              │              │
                 │        target confirmed?    │
                 │              │              │
                 │             YES             │
                 │              │              │
                 │              ▼              │
                 │            AVOID            │
                 │              │              │
                 │     pillar visually/        │
                 │     geometrically leaving   │
                 │              │              │
                 │              ▼              │
                 │        PASS_CONFIRM         │
                 │              │              │
                 │       physically passed?    │
                 │              │              │
                 │             YES             │
                 │              │              │
                 │              ▼              │
                 │           RECOVER           │
                 │              │              │
                 │       geometry usable?      │
                 │              │              │
                 │             YES             │
                 │              │              │
                 └──────────────┴──────────────┘
                                │
                                ▼
                              NORMAL


                            PARKING
                                │
                                ▼
                               STOP
```

At any relevant point:

```text
CRITICAL WALL SAFETY
```

can temporarily override the requested steering command.

This preserves physical safety without turning wall following into the dominant obstacle controller.

---

# 2.29 What Is Already Supported and What Is Still Experimental

The state-machine design is based on concepts already demonstrated in Piolín's current prototypes.

### Already represented in code

```text
ACQUIRE vs NORMAL behavior

state-dependent speed

parking state

sensor-event confirmation

event latching

event release

wall-safety override

steering target smoothing

persistent variables across control cycles

debug state information
```

### Being adapted for Obstacles

```text
TARGET_ACQUIRE

Pixy candidate confirmation

multi-block target selection

target lock

AVOID

PASS_CONFIRM

ultrasonic pillar-clearance confirmation

RECOVER

corner/obstacle arbitration

Obstacle parking
```

The documentation should therefore not claim that every state transition shown here is already finalized in competition code.

Instead, the state machine describes how the current tested programming patterns are being organized into the final Obstacle Challenge controller.

---

# 2.30 Final Engineering Assessment

Piolín's state machine provides the memory and context required for reliable autonomous behavior.

A sensor reading alone cannot tell the complete story.

For example:

```text
Green visible
```

does not tell the robot whether it is:

```text
seeing Green for the first time

already avoiding that Green pillar

losing the same Green pillar from view

recovering after passing it

seeing a different Green pillar next
```

Those situations can contain similar Pixy measurements but require different vehicle responses.

The state machine provides that missing context.

The intended architecture separates the obstacle maneuver into:

```text
TARGET_ACQUIRE
→ decide which pillar matters
```

```text
AVOID
→ execute the required passing side
```

```text
PASS_CONFIRM
→ determine whether physical clearance occurred
```

```text
RECOVER
→ restore useful track geometry
```

before returning to:

```text
NORMAL
```

The fixed competition rules remain:

```text
RED
→ PASS RIGHT

GREEN
→ PASS LEFT
```

and the state machine does not allow image position to redefine them.

Patterns already tested in Piolín's Python programs—such as `ACQUIRE/NORMAL` behavior, event confirmation, latching, release conditions, safety override, state-dependent speed, and parking activation—provide the basis for this design even though the final obstacle implementation is still evolving.

The central state-machine principle is:

> **Piolín should always know what maneuver it is currently executing before deciding how a new sensor observation should affect the motors.**

By making that context explicit, PiolínTech can prevent control conflicts, maintain obstacle identity through temporary camera loss, separate avoidance from recovery, and debug failures according to the exact state in which they occurred.

---

<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
