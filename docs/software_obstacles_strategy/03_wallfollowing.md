# 3. Wall Following and Lateral Geometry

<div align="center">

<img
  src="../../v-photos/v4/ultrasonic_pair_top.jpg"
  alt="Piolín lateral ultrasonic sensor pair"
  width="720"
/>

<br>

<sub><b>Figure 3.1.</b> Piolín uses two permanently lateral ultrasonic sensors to estimate track-relative geometry and protect the vehicle from the course boundaries.</sub>

</div>

Piolín does not use wall following as a simple rule such as:

```text
wall too close
→ steer away
```

The current software development uses the two lateral ultrasonic sensors as a **geometric sensing system**.

The permanent physical mapping is:

```text
S2 = LEFT Ultrasonic Sensor

S3 = RIGHT Ultrasonic Sensor
```

These identities never change.

What changes is how their information is interpreted according to:

```text
course direction

current navigation state

pillar position

corner geometry

recovery state
```

For the Obstacle Challenge, ultrasonic sensing has three principal responsibilities:

```text
NORMAL GEOMETRY
→ keep Piolín in a useful track position

SAFETY
→ prevent excessive approach to a wall

RECOVERY
→ help restore the vehicle after passing a pillar
```

The ultrasonic controller is therefore an important part of navigation, but it should not continuously override the Pixy2.1 obstacle objective.

---

## 3.1 Why Two Lateral Sensors Are Used

<div align="center">

<img
  src="../../v-photos/v4/PiolinUSlabeling.png"
  alt="Piolín ultrasonic labeling with S2 left and S3 right"
  width="720"
/>

<br>

<sub><b>Figure 3.2.</b> Current physical convention used by the software: S2 is always LEFT and S3 is always RIGHT.</sub>

</div>

A single lateral ultrasonic sensor can estimate distance from one wall.

Two sensors provide additional geometric information.

Conceptually:

```text
LEFT US
   │
   ▼
distance to left geometry

RIGHT US
   │
   ▼
distance to right geometry
```

Together, they help answer:

```text
Where is Piolín laterally?

Does the geometry still resemble a straight corridor?

Is one wall becoming dangerously close?

Has the geometry changed after passing a pillar?
```

This allows the software to use more information than a simple one-wall threshold.

---

# 3.2 Physical Identity vs. Logical Role

The software must preserve the distinction between:

```text
PHYSICAL SIDE
```

and:

```text
NAVIGATION ROLE
```

Physically:

```text
S2 = LEFT

S3 = RIGHT
```

These should remain constant in:

```text
wiring

software variable meaning

debug output

testing documentation
```

Logical concepts can change.

For example, in an Open-style counterclockwise interpretation:

```text
LEFT
→ inner

RIGHT
→ outer
```

while clockwise navigation reverses the logical inner/outer roles.

The important software rule is:

> **Do not rename physical sensors when the navigation direction changes. Compute their logical role instead.**

This prevents one of the most dangerous wall-control errors: applying a correct mathematical correction to the wrong physical side.

---

# 3.3 Reading and Filtering the Ultrasonic Sensors

The current Piolín prototype already separates raw ultrasonic access from navigation.

A raw read is first constrained to a physically useful range:

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

The purpose is to prevent one invalid or extreme sensor response from directly becoming an extreme steering request.

The prototype then uses a short three-sample median filter:

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

and updates each sensor buffer with:

```python
def update_buffer(buffer, value):
    buffer[0] = buffer[1]
    buffer[1] = buffer[2]
    buffer[2] = value

    return median3(buffer)
```

This gives the control architecture:

```text
RAW ULTRASONIC
      ↓
range validation
      ↓
short median filter
      ↓
usable distance
```

The filter remains intentionally short.

A large moving average could produce very smooth readings but also introduce too much delay for a moving vehicle.

---

# 3.4 Geometry Instead of Direct Threshold Steering

A major idea in Piolín's current control prototype is that the ultrasonic readings are first transformed into an estimate of track-relative position.

The controller does not immediately convert each sensor value into steering.

Instead:

```text
LEFT + RIGHT DISTANCE
        ↓
GEOMETRIC MODEL
        ↓
ESTIMATED POSITION
        ↓
POSITION ERROR
        ↓
STEERING REQUEST
```

One two-sensor position estimate used during development is:

```python
x_two_us = (
    TRACK_WIDTH_MM
    + Di
    - Do
) / 2.0
```

where:

```text
Di
→ current logical inner-side measurement

Do
→ current logical outer-side measurement
```

A second estimate can rely mainly on the inner-side sensor:

```python
x_inner = (
    Di
    + SENSOR_OFFSET_MM
)
```

These estimates represent different assumptions about the surrounding geometry.

---

# 3.5 Measuring Geometric Coherence

The controller also checks whether both ultrasonic readings still resemble the geometry expected on a straight section.

The current prototype calculates:

```python
geometry_error = abs(
    (Di + Do)
    - EXPECTED_SUM_MM
)
```

The idea is:

```text
Di + Do approximately expected
→ geometry resembles a straight corridor
```

while:

```text
Di + Do very different
→ geometry may no longer match the simple straight model
```

This can occur during:

```text
corner entry

corner exit

pillar interaction

temporary ultrasonic misalignment

unusual wall geometry
```

Rather than switching abruptly from one model to another, Piolín calculates a continuous weight:

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

This creates a confidence-like transition.

---

# 3.6 Continuous Fusion of Two Geometry Estimates

The estimates are then fused:

```python
x_est = (
    weight * x_two_us
    + (1.0 - weight) * x_inner
)
```

Conceptually:

```text
geometry looks strongly like a straight
        ↓
trust the two-sensor estimate more
```

while:

```text
geometry becomes less coherent
        ↓
reduce dependence on that assumption
```

This is important because the software does not need to decide abruptly:

```text
STRAIGHT MODEL ON
```

or:

```text
STRAIGHT MODEL OFF
```

Instead, confidence changes progressively.

The same principle is useful in the Obstacle Challenge because pillar maneuvers temporarily distort the lateral measurements that would otherwise describe a clean corridor.

---

# 3.7 Converting Position Error into Steering

Once Piolín has an estimated position, the controller calculates an error relative to the desired trajectory:

```python
error = (
    x_est
    - target_center_mm
)
```

The current prototype converts this error through a nonlinear response:

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

    return -magnitude
```

This provides two useful behaviors.

Near the desired trajectory:

```text
small error
→ small or zero correction
```

Farther away:

```text
larger error
→ progressively stronger correction
```

The deadband is particularly important because a continuously active controller can otherwise react to every millimeter of ultrasonic noise and cause:

```text
left correction

right correction

left correction

right correction
```

which appears physically as zig-zag.

---

# 3.8 Orientation Damping from Geometry

The current development controller also attempts to distinguish between:

```text
Piolín is laterally displaced
```

and:

```text
Piolín is rapidly moving sideways / rotating
```

by observing how the geometric estimate changes between control cycles.

The prototype calculates:

```python
dx = (
    x_est
    - last_x_est
)
```

and filters it:

```python
filtered_dx = (
    HEADING_FILTER_ALPHA
    * dx
    + (1.0 - HEADING_FILTER_ALPHA)
    * filtered_dx
)
```

The resulting term is only allowed strong authority when the geometry still looks sufficiently straight:

```python
heading_authority = clamp(
    (weight - 0.35) / 0.65,
    0.0,
    1.0
)
```

Then:

```python
signed_heading = (
    HEADING_DAMPING_GAIN
    * filtered_dx
    * heading_authority
)
```

This creates a damping effect.

Conceptually:

```text
position controller
→ where Piolín should be
```

while:

```text
geometry damping
→ how aggressively it is currently moving away from that position
```

For the Obstacle Challenge, this exact formula may change, but the architectural idea remains useful: **do not let normal wall correction become an uncontrolled oscillation.**

---

# 3.9 Wall Following Is Not Wall Safety

One of the most important distinctions in the software is:

```text
NORMAL WALL CONTROL
```

is not the same as:

```text
EMERGENCY WALL PROTECTION
```

Normal geometry control answers:

```text
Where should Piolín travel?
```

Wall safety answers:

```text
Is Piolín becoming physically unsafe?
```

These should have different authority.

The current prototype already implements this separation through:

```python
def side_wall_guard(left_mm, right_mm):
```

The function first determines whether either wall has entered the safety region:

```python
left_danger = left_mm < WALL_SOFT_MM
right_danger = right_mm < WALL_SOFT_MM

if not left_danger and not right_danger:
    return False, 0.0, None
```

If no wall is physically concerning:

```text
wall safety does nothing
```

and the normal controller remains active.

---

# 3.10 Progressive Wall-Safety Response

When one wall becomes too close, the current prototype calculates progressively stronger escape behavior rather than using one fixed response.

Conceptually:

```text
SOFT REGION
→ early moderate reaction

HARD REGION
→ stronger escape

CRITICAL REGION
→ maximum protection + reduced speed
```

The current implementation contains the same structure:

```python
if d <= WALL_CRITICAL_MM:
    mag = WALL_ESCAPE_MAX
    speed = WALL_CRITICAL_SPEED

elif d <= WALL_HARD_MM:
    # progressively stronger response
    speed = WALL_SLOW_SPEED

else:
    # early / softer response
    speed = WALL_SLOW_SPEED
```

The exact numerical thresholds are development calibration values and should not be treated as universal specifications.

The architectural principle is:

> **The closer the physical danger becomes, the more authority the safety controller receives.**

---

# 3.11 Correct Escape Direction

The safety layer follows the physical wall side.

If the left wall becomes too close:

```text
LEFT WALL CLOSE
→ move RIGHT
```

The prototype expresses that as:

```python
if chosen == "LEFT":
    return True, STEER_RIGHT * mag, speed
```

If the right wall becomes too close:

```text
RIGHT WALL CLOSE
→ move LEFT
```

and the opposite command is returned.

This behavior depends on preserving:

```text
LEFT sensor identity

RIGHT sensor identity
```

correctly.

For current Piolín documentation and final software:

```text
S2 = LEFT

S3 = RIGHT
```

must remain consistent across all wall-safety calculations.

---

# 3.12 Safety Override in the Main Controller

The most important part of `side_wall_guard()` is not only how it calculates an escape command.

It is **where that command is applied**.

The prototype main loop does:

```python
wall_active, wall_cmd, wall_speed = side_wall_guard(
    left,
    right
)

if wall_active:
    combined_offset = wall_cmd
```

This means:

```text
normal controller says one thing
      ↓
wall becomes physically unsafe
      ↓
safety replaces the normal command
```

rather than:

```text
normal command
+
safety command
```

This reduces the possibility that two opposing commands cancel one another.

The same concept is central to the final Obstacle architecture.

---

# 3.13 Wall Following During Pillar Avoidance

<div align="center">

<img
  src="../../v-photos/v4/obstacle_red_run.jpg"
  alt="Piolín navigating around a red pillar"
  width="700"
/>

<br>

<sub><b>Figure 3.3.</b> During an active pillar maneuver, normal wall following should not continuously pull Piolín away from the required obstacle trajectory.</sub>

</div>

During normal driving:

```text
wall geometry
→ major navigation influence
```

During pillar avoidance:

```text
Pixy obstacle objective
→ major navigation influence
```

The wall system changes role.

It becomes mainly:

```text
boundary awareness

critical safety

pass-context information
```

Consider a Red pillar.

The required rule is:

```text
RED
→ PASS RIGHT
```

Suppose normal wall following simultaneously believes Piolín should move left toward its preferred corridor position.

If both controllers have equal authority:

```text
pillar controller → RIGHT

wall controller → LEFT

result → weak / unstable command
```

This can cause:

```text
late avoidance

zig-zag

incorrect clearance

apparent steering inversion
```

The solution is not necessarily stronger Pixy steering.

The software architecture should first ensure that the normal wall controller does not fight the active obstacle state.

---

# 3.14 State-Dependent Wall Authority

The intended controller authority changes according to the state machine.

| State | Normal Wall Geometry | Wall Safety |
| :--- | :---: | :---: |
| `ACQUIRE` | High | Highest if required |
| `NORMAL` | High | Highest if required |
| `TARGET_ACQUIRE` | Moderate / High | Highest if required |
| `AVOID` | Reduced | Highest if critical |
| `PASS_CONFIRM` | Context dependent | Highest if critical |
| `RECOVER` | Increasing | Highest if critical |
| `CORNER` | Reduced / specialized | Active |
| `PARKING` | Context dependent | Active |

The intended concept is:

```text
NORMAL
wall geometry controls trajectory
```

```text
AVOID
pillar controller controls trajectory
wall safety only prevents dangerous boundary approach
```

```text
RECOVER
wall geometry gradually becomes important again
```

This prevents controller conflict.

---

# 3.15 Wall Information During Pass Confirmation

The ultrasonic sensors also become useful for determining whether the current pillar has physically been passed.

Pixy target loss alone is not sufficient because:

```text
Piolín turns
      ↓
camera orientation changes
      ↓
pillar may leave image
```

even while the pillar remains physically beside the vehicle.

A lateral ultrasonic sensor may observe a sequence similar to:

```text
open track geometry
      ↓
pillar enters beside robot
      ↓
distance changes
      ↓
robot advances
      ↓
distance opens again
```

This can provide additional evidence for:

```text
PASS_CONFIRM
```

The exact final pass-confirmation algorithm remains under development, but the architectural relationship is:

```text
PIXY
→ visual obstacle state

ULTRASONICS
→ physical lateral context
```

---

# 3.16 Wall Following During Recovery

<div align="center">

<img
  src="../../v-photos/v4/obstacle_green_run.jpg"
  alt="Piolín navigating around a green pillar"
  width="700"
/>

<br>

<sub><b>Figure 3.4.</b> After a pillar is cleared, S2 and S3 become increasingly important for restoring useful track geometry.</sub>

</div>

After `PASS_CONFIRM`, the vehicle enters:

```text
RECOVER
```

At this point the objective changes from:

```text
avoid pillar
```

to:

```text
restore stable course geometry
```

The two ultrasonic sensors can again estimate:

```text
left clearance

right clearance

lateral position

whether normal corridor assumptions are becoming valid again
```

The transition should be progressive.

An immediate switch from:

```text
strong obstacle steering
```

to:

```text
strong opposite wall-centering
```

can produce another zig-zag.

Instead:

```text
pillar cleared
      ↓
countersteer
      ↓
geometry becomes more normal
      ↓
wall controller authority increases
      ↓
NORMAL
```

This is one reason recovery is treated as its own state.

---

# 3.17 Steering Smoothing After Wall Calculation

Even after the wall system calculates a desired steering value, the current prototype does not send it directly to Motor B.

The steering target is limited per control cycle:

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

Then Motor B follows that target:

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

This creates the complete wall-control chain:

```text
ULTRASONIC DATA
      ↓
FILTER
      ↓
GEOMETRIC ESTIMATE
      ↓
POSITION ERROR
      ↓
WALL STEERING REQUEST
      ↓
STATE / SAFETY ARBITRATION
      ↓
SMOOTH TARGET
      ↓
MOTOR B CONTROLLER
      ↓
FRONT WHEELS
```

That separation is important because an oscillation can originate at several different layers.

---

# 3.18 Speed Is Part of Wall Control

The current prototype also reduces drive speed in conditions where strong steering or wall danger requires more reaction time.

The main loop includes logic equivalent to:

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

This is important because Piolín is a physical Ackermann-style vehicle.

At higher speed:

```text
same sensor delay
→ more physical distance traveled
```

and:

```text
same steering-motor response time
→ greater trajectory error before wheels reach target
```

Therefore a wall controller cannot be calibrated independently from propulsion speed.

For Obstacles, speed may also change during:

```text
target approach

active avoidance

critical wall safety

recovery

parking
```

---

# 3.19 Debugging Wall Following

The wall controller should expose enough data to identify whether a problem comes from sensing, geometry, control, or actuation.

The existing prototype already prints values including:

```python
print(
    "L:", int(left),
    "R:", int(right),
    "DI:", int(Di),
    "DO:", int(Do),
    "X:", round(x_est, 1),
    "TARGET_X:", round(active_target_center, 1),
    "ERR:", round(error, 1),
    "W:", round(weight, 2),
    "WALL_STEER:", round(steering_offset, 1),
    "WALL_SAFE:", wall_active,
    "CMD:", round(combined_offset, 1),
    "TARGET:", round(current_target, 1),
    "REAL:", round(steer.angle(), 1)
)
```

For Obstacle Challenge testing, a useful wall-related telemetry line should include:

```text
STATE

S2 LEFT

S3 RIGHT

estimated geometry

normal wall request

wall safety active?

pillar request

final steering command

actual Motor B angle
```

This helps answer questions such as:

```text
Did the sensor read incorrectly?

Did the geometry estimate become incorrect?

Did wall control request the wrong direction?

Did obstacle control override it?

Did safety override everything?

Did Motor B physically follow the final command?
```

---

# 3.20 Diagnosing Common Wall-Following Failures

### Piolín zig-zags in a straight

Check:

```text
steering center

S2/S3 noise

deadband

normal correction strength

target smoothing

drive speed
```

Do not immediately increase filtering.

Too much filtering may simply move the oscillation later in time.

---

### Piolín consistently moves toward one wall

Check:

```text
S2 = LEFT?

S3 = RIGHT?

steering sign correct?

mechanical steering centered?

target geometry reasonable?
```

A persistent bias is often more likely to be:

```text
mapping

trim

mechanical center
```

than random sensor noise.

---

### Piolín corrects too late

Possible causes include:

```text
drive speed too high

wall controller too weak

sensor filtering too slow

safety threshold too close

steering motor response too slow
```

The cause should be identified before simply increasing steering magnitude.

---

### Piolín detects a pillar correctly but obstacle avoidance feels weak

Check whether:

```text
normal wall following is still active with too much authority
```

during `AVOID`.

This can create:

```text
pillar request
+
opposite centering request
→ weak result
```

The problem may therefore be **control arbitration**, not Pixy detection.

---

### Piolín passes the pillar but hits a wall afterward

Do not automatically weaken obstacle avoidance.

The actual failure may be:

```text
RECOVER
```

Check:

```text
target release timing

countersteering

S2/S3 reacquisition

wall-controller reactivation
```

The original pillar trajectory may already be correct.

---

# 3.21 Current Prototype vs. Final Obstacle Wall Control

The current Python geometry controller is useful evidence of Piolín's wall-following development, but it should not be interpreted as the exact final Obstacle Challenge controller.

Current prototype concepts that are expected to remain useful include:

```text
short ultrasonic filtering

fixed physical left/right identity

geometric position estimation

continuous confidence weighting

deadband

nonlinear steering response

orientation damping

independent wall safety

state-dependent speed

target smoothing

closed-loop Motor B control
```

Elements that may change during final Obstacle development include:

```text
exact target position

exact geometry equation

filter parameters

wall thresholds

steering gains

safety thresholds

authority during pillar avoidance

recovery criteria
```

The software architecture is being preserved while the numerical control parameters continue to be calibrated.

---

# 3.22 Intended Obstacle Wall-Control Flow

The final conceptual flow is:

```text
                    S2 LEFT            S3 RIGHT
                       │                  │
                       └────────┬─────────┘
                                ▼
                       VALIDATE / FILTER
                                │
                                ▼
                       GEOMETRY ESTIMATE
                                │
                                ▼
                       NORMAL WALL REQUEST
                                │
                                │
                    ┌───────────┴───────────┐
                    │                       │
                    ▼                       ▼
              NAVIGATION STATE       WALL SAFETY CHECK
                    │                       │
           ┌────────┼────────┐              │
           │        │        │              │
           ▼        ▼        ▼              │
        NORMAL    AVOID   RECOVER            │
           │        │        │              │
           │        │        │              │
      wall has   pillar has wall becomes    │
      authority  priority  important again  │
           │        │        │              │
           └────────┴────────┘              │
                    │                       │
                    ▼                       │
              BASE STEERING                 │
                    │                       │
                    └───────────┬───────────┘
                                ▼
                       SAFETY OVERRIDE?
                                │
                                ▼
                         FINAL STEERING
                                │
                                ▼
                         TARGET SMOOTHING
                                │
                                ▼
                            MOTOR B
```

This separation prevents normal wall following from unintentionally becoming the obstacle controller.

---

# 3.23 Final Engineering Assessment

Piolín's wall-following strategy is based on **lateral geometry**, not simply on reacting independently to each wall.

The two permanent ultrasonic sensors:

```text
S2 = LEFT

S3 = RIGHT
```

provide measurements that can be filtered, compared, and converted into an estimate of the vehicle's track-relative position.

The current prototype already demonstrates several important software patterns directly in Python:

```text
raw-distance validation

median filtering

two-sensor geometry estimation

continuous confidence weighting

nonlinear error correction

deadband

geometric damping

progressive wall safety

state-dependent speed

steering smoothing

closed-loop Motor B control
```

For the Obstacle Challenge, however, wall following must operate within the larger state machine.

During:

```text
NORMAL
```

wall geometry can strongly influence Piolín's trajectory.

During:

```text
AVOID
```

the Pixy2.1 pillar objective should have greater navigation authority, while the ultrasonics continue supplying:

```text
boundary context

critical wall protection
```

After the pillar is cleared:

```text
RECOVER
```

gradually returns authority to the ultrasonic geometry controller.

This distinction is essential because a controller that constantly tries to return Piolín to its preferred wall position can directly fight the steering needed to pass a pillar.

The core principle is:

> **Wall following should guide Piolín when the track is the main objective, protect Piolín when a boundary becomes dangerous, and support recovery after a pillar—but it should not override the required obstacle trajectory during an active avoidance maneuver.**

By separating normal geometry control, wall safety, obstacle authority, and recovery, PiolínTech can tune each behavior independently while preserving one understandable final steering command.

---

<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
