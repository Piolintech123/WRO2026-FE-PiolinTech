# 1. Software Architecture

<div align="center">

<img
  src="../../v-photos/v4/piolin_obstacle_isometric.jpg"
  alt="Piolín in its current Obstacle Challenge configuration"
  width="740"
/>

<br>

<sub><b>Figure 1.1.</b> Piolín's current Obstacle Challenge platform. The software architecture is being developed from control principles already tested in earlier Piolín programs.</sub>

</div>

Piolín's software is being developed as a **layered autonomous-control system** rather than as one long sequence of timed movements.

The current Obstacle Challenge program is still under development. Therefore, this document describes the **software architecture and control principles guiding the final implementation**, while using fragments of current Piolín prototype code as engineering evidence of how these ideas are already being implemented and tested.

The current Obstacle Challenge hardware is:

```text
Motor A → propulsion

Motor B → steering

S1 → Pixy2.1

S2 → LEFT Ultrasonic Sensor

S3 → RIGHT Ultrasonic Sensor

S4 → Color Sensor
```

The intended software pipeline is:

```text
SENSORS
   ↓
MEASUREMENT VALIDATION
   ↓
PERCEPTION
   ↓
STATE MANAGEMENT
   ↓
CONTROL ARBITRATION
   ↓
STEERING / SPEED COMMAND
   ↓
MOTORS
```

This architecture separates:

```text
what Piolín measures

what Piolín believes is happening

what Piolín is currently trying to do

how the final motor command is produced
```

That separation becomes especially important during the Obstacle Challenge, where wall following, pillar avoidance, recovery, corner handling, and safety can all request different steering behavior.

---

## 1.1 Why the Software Is Layered

The Obstacle Challenge controller must continuously answer different questions:

```text
Is there a relevant pillar ahead?

What color is it?

Which side must Piolín pass?

Where is the pillar in the camera image?

How close is Piolín to the left wall?

How close is Piolín to the right wall?

Is a safety override required?

Has the current pillar actually been passed?

Should Piolín still avoid or begin recovery?

Has a course landmark been crossed?

Is parking currently allowed?
```

These questions should not all be solved inside one steering equation.

Instead, Piolín separates them conceptually into:

```text
PERCEPTION
→ understand sensor information

STATE
→ determine the current maneuver

CONTROL
→ calculate the desired motion

ACTUATION
→ make Motor A and Motor B execute it
```

The current prototypes already contain several examples of this separation.

---

# 1.2 Centralized Utility Functions

One useful characteristic of the current code is that common mathematical operations are isolated in helper functions rather than rewritten throughout the controller.

For example:

```python
def clamp(value, minimum, maximum):
    if value < minimum:
        return minimum
    if value > maximum:
        return maximum
    return value
```

This small function appears throughout the controller whenever a value must remain inside a safe or useful range.

Examples include:

```text
steering limits

gyro correction

sensor-derived terms

wall-escape steering

target changes
```

This is preferable to scattering repeated limit logic throughout the main loop.

Architecturally:

```text
RAW CALCULATION
      ↓
clamp()
      ↓
BOUNDED COMMAND
```

The same idea will remain useful in the final Obstacle Challenge code for limiting:

```text
Pixy steering corrections

wall-safety corrections

recovery steering

target relevance values

drive speeds
```

---

# 1.3 Sensor Filtering Layer

The current Piolín controller already contains a short ultrasonic filtering stage.

Rather than feeding every raw ultrasonic sample directly into navigation, it uses a three-value median filter.

```python
def median3(values):
    a, b, c = values[0], values[1], values[2]

    if a > b:
        a, b = b, a
    if b > c:
        b, c = c, b
    if a > b:
        a, b = b, a

    return b
```

The buffer is then updated with:

```python
def update_buffer(buffer, value):
    buffer[0] = buffer[1]
    buffer[1] = buffer[2]
    buffer[2] = value
    return median3(buffer)
```

This is an important architectural decision because the navigation controller receives a more stable measurement without introducing a long averaging delay.

The design principle is:

```text
RAW SENSOR
     ↓
short validation/filter
     ↓
CONTROL VALUE
```

rather than:

```text
RAW SENSOR
     ↓
immediate steering reaction
```

A short median filter is especially useful for rejecting a single abnormal ultrasonic sample.

At the same time, the filter remains intentionally small because excessive filtering would create:

```text
smoother measurement
+
slower response
```

and Piolín continues traveling while the software is waiting for new data.

The final Obstacle controller can retain this same philosophy for S2 and S3.

---

# 1.4 Sensor Reading Is Separated from Navigation

Another useful pattern in the prototype is the separation between reading a sensor and deciding what Piolín should do with the result.

For example, the ultrasonic reading function first constrains the raw measurement:

```python
def read_raw_us(sensor):
    try:
        d = sensor.distance()
        if d < 20:
            d = 20
        if d > MAX_US_MM:
            d = MAX_US_MM
        return d
    except:
        return MAX_US_MM
```

Then another function handles the filtered pair:

```python
def read_distances():
    l = update_buffer(
        left_buffer,
        read_raw_us(us_left)
    )

    r = update_buffer(
        right_buffer,
        read_raw_us(us_right)
    )

    return float(l), float(r)
```

The important architectural principle is not the temporary variable names used in one development file.

It is the separation:

```text
READ HARDWARE
     ↓
VALIDATE VALUE
     ↓
FILTER VALUE
     ↓
RETURN MEASUREMENT
```

The navigation controller then works with the measurement rather than directly manipulating hardware communication.

For the current robot, the authoritative physical interpretation remains:

```text
S2 = LEFT Ultrasonic

S3 = RIGHT Ultrasonic
```

---

# 1.5 Geometry Is Calculated Before Steering

One of the strongest ideas in the current prototype is that Piolín first estimates its track-relative geometry and only afterward converts that geometric error into steering.

The controller contains two geometric estimates:

```python
x_two_us = (
    TRACK_WIDTH_MM
    + Di
    - Do
) / 2.0
```

and:

```python
x_inner = (
    Di
    + SENSOR_OFFSET_MM
)
```

It then measures whether both ultrasonic readings are geometrically coherent:

```python
geometry_error = abs(
    (Di + Do)
    - EXPECTED_SUM_MM
)
```

A confidence-like weight is produced:

```python
weight = 1.0 - (
    geometry_error
    / GEOMETRY_TRANSITION_MM
)

weight = clamp(
    weight,
    0.0,
    1.0
)
```

Finally, both geometric estimates are fused:

```python
x_est = (
    weight * x_two_us
    + (1.0 - weight) * x_inner
)
```

This is an important architectural pattern.

The code does not simply say:

```text
left sensor too close
→ steer right
```

for every condition.

Instead:

```text
SENSOR DATA
     ↓
GEOMETRIC MODEL
     ↓
ESTIMATED POSITION
     ↓
CONTROL ERROR
     ↓
STEERING
```

For the Obstacle Challenge, the final geometric model may evolve, but the same separation remains valuable.

---

# 1.6 Nonlinear Steering from Geometric Error

The prototype also converts position error into steering through a dedicated function:

```python
def steering_from_error(error_mm):
    if abs(error_mm) <= POSITION_DEADBAND_MM:
        return 0.0

    e_cm = abs(error_mm) / 10.0

    magnitude = (
        0.35 * e_cm
        + 0.012 * e_cm * e_cm
    )

    magnitude = clamp(
        magnitude,
        0.0,
        MAX_STEER_OFFSET
    )

    if error_mm > 0:
        return magnitude
    else:
        return -magnitude
```

This represents another useful architectural choice:

```text
GEOMETRIC ERROR
     ↓
CONTROL FUNCTION
     ↓
REQUESTED STEERING
```

Near the target:

```text
small error
→ small correction
```

while larger errors can create stronger corrections.

This is different from a simple binary controller such as:

```text
too far left
→ full right
```

because strong binary corrections often create oscillation.

For the Obstacle Challenge, similar nonlinear mappings can eventually be used for:

```text
Pixy horizontal error

wall recovery

pillar approach severity
```

without making every visible obstacle immediately produce maximum steering.

---

# 1.7 Steering Target Smoothing

A particularly important part of the current Piolín code is that the desired steering angle does not immediately become the Motor B target.

The prototype first smooths the requested target:

```python
def smooth_target(target):
    global current_target

    diff = target - current_target
    diff = clamp(diff, -TARGET_STEP, TARGET_STEP)

    current_target += diff
    return current_target
```

This means a requested change such as:

```text
0° → 25°
```

can instead become:

```text
0
→ 1.8
→ 3.6
→ 5.4
→ ...
→ 25
```

depending on the configured target step.

The goal is to reduce:

```text
instant steering reversals

mechanical shocks

rapid zig-zag

controller fighting
```

This becomes extremely useful during Obstacles because Pixy detections can move significantly across the image from one frame to the next.

The intended pipeline becomes:

```text
PIXY / WALL / RECOVERY LOGIC
             ↓
      requested steering
             ↓
       smooth_target()
             ↓
      Motor B controller
```

---

# 1.8 Motor B Has Its Own Control Layer

The prototype also separates desired steering from the actual motor command.

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

This means the navigation controller does not directly command:

```text
Motor B speed = fixed value
```

every time it wants to turn.

Instead:

```text
NAVIGATION
→ desired steering position
```

and:

```text
STEERING CONTROLLER
→ moves Motor B toward that position
```

This separation is important for troubleshooting.

If debug output shows:

```text
requested steering = RIGHT
```

but the physical wheels move left, the failure exists in:

```text
actuation / steering sign / mechanism
```

rather than:

```text
Pixy classification
```

That distinction is especially valuable when diagnosing apparently inverted Red/Green obstacle behavior.

---

# 1.9 Independent Wall-Safety Layer

The current prototype includes a particularly important concept for the final Obstacle controller: **wall safety has its own function and can override normal navigation**.

The function first determines whether either lateral wall is becoming unsafe:

```python
left_danger = left_mm < WALL_SOFT_MM
right_danger = right_mm < WALL_SOFT_MM

if not left_danger and not right_danger:
    return False, 0.0, None
```

If a wall is close, the controller determines which side requires attention and calculates a progressive escape magnitude.

A left-side danger ultimately produces:

```python
if chosen == "LEFT":
    return True, STEER_RIGHT * mag, speed
```

while right-side danger produces the opposite response:

```python
return True, STEER_LEFT * mag, speed
```

The main loop then gives this layer priority:

```python
wall_active, wall_cmd, wall_speed = side_wall_guard(
    left,
    right
)

if wall_active:
    combined_offset = wall_cmd
```

This is a major architectural concept.

The controller does not merely add:

```text
wall correction
+
another controller
```

in every situation.

Instead, critical safety can **take control**.

For the final Obstacle Challenge architecture, this idea becomes:

```text
normal geometry
      ↓
pillar avoidance
      ↓
BUT
      ↓
if physical wall becomes critical
      ↓
safety override
```

The exact thresholds remain calibration values.

---

# 1.10 State-Dependent Speed

The prototype also shows that Motor A speed can depend on the current vehicle condition.

For example:

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

This demonstrates an important software principle:

> **Speed is part of the autonomous controller, not an independent constant.**

Piolín may require different speeds during:

```text
normal straight driving

initial acquisition

strong steering

critical wall recovery

pillar approach

pillar avoidance

parking
```

The final Obstacle controller can use the same architecture:

```text
STATE
   ↓
desired steering
+
desired drive speed
```

rather than running Motor A at one constant speed regardless of the maneuver.

---

# 1.11 Event Confirmation from the Current Color Prototype

The second Piolín prototype demonstrates another important architecture: **do not treat one sensor sample as a complete navigation event**.

The code maintains:

```python
candidate_color = None
candidate_count = 0

ready_for_new_color = True
release_count = 0
```

When a color appears, it must remain consistent for multiple readings:

```python
if detected == candidate_color:
    candidate_count += 1
else:
    candidate_color = detected
    candidate_count = 1
```

Only then is the event accepted:

```python
if candidate_count >= COLOR_CONFIRMATIONS:
```

This creates:

```text
RAW DETECTION
      ↓
CANDIDATE
      ↓
CONFIRMATION
      ↓
ACCEPTED EVENT
```

The same architecture is extremely useful for Pixy2.1.

A future obstacle version can conceptually use:

```text
possible Red
      ↓
Red remains plausible
      ↓
confirmed Red target
      ↓
begin pass-right maneuver
```

instead of:

```text
one Red sample
→ immediate maximum steering
```

---

# 1.12 Event Latching and Re-Arming

The same color prototype also prevents one physical line from being counted repeatedly.

After one accepted color event:

```python
ready_for_new_color = False
release_count = 0
candidate_color = None
candidate_count = 0
```

The detector then waits until the robot has clearly left the color:

```python
if detected is None:
    release_count += 1

    if release_count >= COLOR_RELEASE_CONFIRMATIONS:
        ready_for_new_color = True
        release_count = 0
```

Architecturally:

```text
DETECT
  ↓
CONFIRM
  ↓
ACCEPT
  ↓
LOCK
  ↓
WAIT FOR PHYSICAL RELEASE
  ↓
RE-ARM
```

This is one of the most transferable patterns from the current program to obstacle vision.

The Pixy equivalent is:

```text
candidate pillar
      ↓
confirmed target
      ↓
lock target
      ↓
avoid pillar
      ↓
confirm physical clearance
      ↓
release target
      ↓
allow next target
```

This prevents unstable behavior when multiple pillars appear in the camera.

---

# 1.13 Current Obstacle Perception Layer

<div align="center">

<img
  src="../../v-photos/v4/pixy21_front.jpg"
  alt="Pixy2.1 installed on Piolín for obstacle perception"
  width="680"
/>

<br>

<sub><b>Figure 1.6.</b> Pixy2.1 becomes the primary forward-perception device during the Obstacle Challenge.</sub>

</div>

The final Obstacle Challenge controller will replace the Open-specific S1 Gyro logic with Pixy2.1 perception.

The camera provides block information such as:

```text
signature

x

y

width

height
```

The current signature mapping is:

```text
sig1 → Pink → parking reference

sig2 → Red → pass RIGHT

sig3 → Green → pass LEFT
```

The architecture must keep two ideas separate:

```text
SIGNATURE
→ WHAT the pillar is
→ which side must be passed
```

and:

```text
x / y / width / height
→ WHERE the target appears
→ how visually relevant it is
```

Therefore:

```text
RED
→ RIGHT
```

and:

```text
GREEN
→ LEFT
```

remain fixed regardless of the target's image position.

---

# 1.14 Target Selection Before Avoidance

Pixy may provide more than one block.

The final architecture should therefore avoid directly doing:

```text
blocks[0]
→ steering
```

Instead:

```text
READ PIXY
    ↓
VALIDATE BLOCKS
    ↓
FILTER ALLOWED SIGNATURES
    ↓
COMPARE RELEVANCE
    ↓
SELECT TARGET
    ↓
TARGET LOCK
```

A target-selection layer can eventually consider:

```text
signature

x

y

width

height

previous target

current state
```

The final scoring formula is not yet fixed.

This is intentional.

The architecture defines **where target selection belongs** without pretending the current experimental weighting is final.

---

# 1.15 State Machine

The existing code already contains early forms of explicit state behavior such as:

```text
ACQUIRE

NORMAL

PARKING
```

and the color prototype contains:

```text
READY FOR NEW COLOR

WAITING FOR RELEASE
```

The final Obstacle controller expands this idea.

A practical state architecture is:

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

with additional states such as:

```text
CORNER

PARKING

STOP
```

Each state answers one question:

> **What is Piolín currently trying to accomplish?**

That is much easier to reason about than allowing every controller to act simultaneously.

---

# 1.16 Control Arbitration

One of the main reasons for a state machine is to decide which controller should have authority.

Imagine:

```text
Pixy:
Red pillar → move right
```

while:

```text
normal wall controller:
move left toward center
```

If both commands are simply added:

```text
right + left
→ cancellation
→ weak avoidance
```

This can make a correct pillar detector appear broken.

The intended architecture is therefore approximately:

| Priority | Controller |
| :---: | :--- |
| 1 | Critical wall safety |
| 2 | Active pillar avoidance |
| 3 | Active corner handling |
| 4 | Post-pillar recovery |
| 5 | Normal geometry control |

This is conceptually consistent with the prototype's existing pattern:

```python
if wall_active:
    combined_offset = wall_cmd
```

where safety explicitly overrides the normal combined command.

The final controller should always produce **one clear final steering request**.

---

# 1.17 Pillar-Pass Confirmation

A camera target disappearing is not sufficient evidence that the pillar has physically been passed.

Piolín turns the camera whenever the chassis turns.

Therefore:

```text
Pixy target disappeared
```

may mean:

```text
camera rotated away from pillar
```

rather than:

```text
pillar is behind vehicle
```

The intended state transition is:

```text
AVOID
   ↓
visual target becomes peripheral / lost
   ↓
PASS_CONFIRM
   ↓
evaluate S2/S3 geometry
   ↓
pillar clearance confirmed
   ↓
RECOVER
```

This is directly related to the event-release architecture already used in the color prototype:

```text
do not accept a new event
until the previous physical condition has been released
```

For Obstacles:

```text
do not acquire a new pillar
until the current pillar has been physically cleared
```

---

# 1.18 Recovery Is Its Own Controller

<div align="center">

<img
  src="../../v-photos/v4/obstacle_red_run.jpg"
  alt="Piolín performing a red obstacle maneuver"
  width="700"
/>

<br>

<sub><b>Figure 1.7.</b> Obstacle navigation must continue after the pillar is cleared; recovery is treated as a separate control phase.</sub>

</div>

The complete obstacle maneuver is:

```text
DETECT
  ↓
SELECT
  ↓
LOCK
  ↓
AVOID
  ↓
PASS
  ↓
COUNTERSTEER
  ↓
RECOVER
```

Recovery should not be hidden inside the pillar avoidance equation.

It has a different objective.

During avoidance:

```text
move to required side of pillar
```

During recovery:

```text
return toward useful course geometry
```

This makes it possible to tune:

```text
pillar clearance
```

independently from:

```text
post-pillar recentering
```

If Piolín correctly passes a Red pillar but later hits the wall, the engineering problem can then be identified as:

```text
RECOVERY
```

rather than weakening the successful Red avoidance maneuver.

---

# 1.19 Course Events Remain Independent

The Color Sensor on S4 should remain a separate course-state system.

Its job is not to influence Pixy classification directly.

The architecture is:

```text
PIXY2.1
→ forward objects
```

```text
S2 / S3
→ lateral geometry
```

```text
S4
→ floor landmarks
```

The event-confirmation logic already tested in the current color program can continue to prevent duplicate floor events.

Those events can later update:

```text
course progress

corner count

lap state

parking permission
```

without directly commanding obstacle steering.

---

# 1.20 Diagnostics Are Part of the Controller

The current large prototype already provides detailed telemetry such as:

```python
print(
    "MODE:",
    "ACQUIRE" if acquire_progress < 1.0 else "NORMAL",
    "LINES:", line_count,
    "L:", int(left),
    "R:", int(right),
    "X:", round(x_est, 1),
    "ERR:", round(error, 1),
    "GY_ERR:", round(gyro_error, 1),
    "WALL_SAFE:", wall_active,
    "CMD:", round(combined_offset, 1),
    "TARGET:", round(current_target, 1),
    "REAL:", round(steer.angle(), 1)
)
```

This is valuable because it records several layers simultaneously:

```text
current state

sensor information

estimated geometry

controller output

requested steering

actual steering position
```

The Obstacle controller should keep a similarly useful diagnostic structure.

A future Obstacle debug line could logically expose:

```text
STATE

TARGET SIGNATURE

X

Y

WIDTH

HEIGHT

S2

S3

FINAL STEERING COMMAND
```

This lets the team determine whether a failure occurred in:

```text
camera detection

target selection

state

controller arbitration

Motor B response
```

rather than guessing from the final collision.

---

# 1.21 Existing Code vs. Final Obstacle Code

The existing Piolín programs are **development references**, not final Obstacle Challenge source code.

Some current prototype features are Open-specific or temporary, including:

```text
gyro heading control

manual test direction

working wall targets

temporary parking constants

timed curve experiments

prototype line counting

development sensor mappings
```

These details should not automatically be copied into the final Obstacle program.

What is being preserved is the underlying software architecture.

| Existing Code Pattern | Final Obstacle Use |
| :--- | :--- |
| `clamp()` | Keep controller values bounded |
| `median3()` | Short ultrasonic filtering |
| `read_distances()` | Sensor abstraction |
| Geometric fusion | Track-relative geometry |
| `steering_from_error()` | Error-to-steering conversion |
| `smooth_target()` | Steering rate limiting |
| `steering_to()` | Motor B position control |
| `side_wall_guard()` | Independent wall safety |
| State-dependent speed | Maneuver-specific propulsion |
| Candidate confirmation | Pixy target confirmation |
| Event latch | Target lock |
| Release confirmation | Pillar-pass confirmation |
| Debug print | Controller telemetry |

This allows the code to evolve without discarding control principles already tested on Piolín.

---

# 1.22 Planned Program Structure

During fast competition development, one structured source file can still be practical.

As the final controller becomes stable, responsibilities can be separated conceptually into:

```text
src/
│
├── obstacle_challenge.py
│
├── sensors/
│   ├── pixy.py
│   ├── ultrasonic.py
│   └── color.py
│
├── control/
│   ├── steering.py
│   ├── drive.py
│   ├── walls.py
│   └── obstacles.py
│
└── navigation/
    ├── state_machine.py
    └── target_selection.py
```

This is a possible architectural direction, not a requirement to create unnecessary empty modules.

The important part is that responsibilities remain separated logically.

A single file can still implement good architecture if functions and state boundaries remain clear.

---

# 1.23 Complete Intended Control Cycle

The final Obstacle software cycle can be represented as:

```text
while robot_is_running:

    READ SENSORS
         │
         ├── Pixy blocks
         ├── S2 left distance
         ├── S3 right distance
         └── S4 floor state
         │
         ▼
    VALIDATE / FILTER
         │
         ▼
    UPDATE PERCEPTION
         │
         ├── target candidate
         ├── wall geometry
         └── floor event
         │
         ▼
    UPDATE STATE
         │
         ├── NORMAL
         ├── TARGET_ACQUIRE
         ├── AVOID
         ├── PASS_CONFIRM
         ├── RECOVER
         ├── CORNER
         └── PARKING
         │
         ▼
    CALCULATE CONTROL
         │
         ├── obstacle command
         ├── wall command
         ├── safety command
         └── recovery command
         │
         ▼
    ARBITRATE PRIORITY
         │
         ▼
    SMOOTH FINAL STEERING
         │
         ▼
    COMMAND MOTOR B
         │
         ▼
    SELECT DRIVE SPEED
         │
         ▼
    COMMAND MOTOR A
         │
         ▼
    OUTPUT DEBUG DATA
```

This is the architecture toward which the current experimental programs are evolving.

---

# 1.24 Current Development Status

The following ideas are already represented directly in Piolín's current development code:

```text
sensor abstraction

short filtering

geometry estimation

bounded controllers

smooth steering targets

separate Motor B control

wall-safety override

state-dependent speed

candidate confirmation

event locking

release conditions

parking state

diagnostic telemetry
```

The main Obstacle-specific areas that still require development and validation are:

```text
Pixy block parsing

final target relevance model

multiple-target selection

temporary target locking

target-loss tolerance

pillar-pass confirmation

Red trajectory

Green trajectory

wall/obstacle control arbitration

post-pillar recovery

corner integration

final parking
```

The repository should therefore distinguish between:

```text
ARCHITECTURE ALREADY SUPPORTED BY PROTOTYPES
```

and:

```text
FINAL ALGORITHM STILL UNDER DEVELOPMENT
```

---

# 1.25 Final Engineering Assessment

Piolín's software development is moving from several experimental controllers toward one coherent **state-based and layered autonomous architecture**.

The current programs already demonstrate important engineering concepts directly in Python:

```text
short sensor filtering

geometric estimation

bounded nonlinear corrections

steering target smoothing

closed-loop Motor B control

independent wall-safety overrides

state-dependent speed

sensor-event confirmation

event latching

controlled release conditions

diagnostic telemetry
```

These concepts provide a foundation for the final Obstacle Challenge controller.

The intended information flow is:

```text
Pixy2.1
→ obstacle identity and visual geometry

S2/S3
→ physical lateral geometry

S4
→ course events
```

followed by:

```text
PERCEPTION
→ STATE
→ CONTROL ARBITRATION
→ ACTUATION
```

The camera should determine:

```text
WHAT pillar is relevant
```

but not directly control the steering motor.

The state machine should determine:

```text
WHAT Piolín is currently trying to accomplish
```

and the control layer should determine:

```text
HOW to execute that objective safely
```

before Motor B receives one final steering target.

For obstacle rules:

```text
RED
→ PASS RIGHT

GREEN
→ PASS LEFT
```

remains permanent.

Pixy image coordinates influence target geometry and steering magnitude, not the required passing side.

Because the uploaded programs remain development versions, temporary constants and Open-specific logic are treated as evidence of the architecture rather than as final Obstacle Challenge specifications.

The main software principle is:

> **Read and validate the sensors first, interpret the environment second, choose one navigation state third, resolve controller priorities fourth, and only then send a final command to the motors.**

This structure allows PiolínTech to improve target selection, camera processing, wall safety, recovery, or steering independently without rebuilding the entire autonomous controller each time one subsystem changes.

---

<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
