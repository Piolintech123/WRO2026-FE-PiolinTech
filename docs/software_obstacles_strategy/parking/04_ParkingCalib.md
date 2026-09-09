# 4. Parking Calibration

<div align="center">

<img
  src="../../../v-photos/v4/parking_area.jpg"
  alt="Parking area used for Piolín parking calibration"
  width="720"
/>

<br>

<sub><b>Figure 4.1.</b> Parking calibration is performed on the real vehicle and parking geometry rather than by selecting final values from the software model alone.</sub>

</div>

Piolín's parking controller contains several parameters that cannot be finalized only from software calculations.

The final trajectory depends on the physical interaction between:

```text
Ackermann steering

Motor A propulsion

Motor B steering response

Pixy2.1 camera geometry

S2 / S3 ultrasonic measurements

wheel behavior

track surface

parking-area geometry
```

For this reason, PiolínTech treats parking calibration as a sequence of controlled experiments.

The objective is not:

```text
change several numbers
→ run complete course
→ hope parking looks better
```

Instead, the calibration process is:

```text
freeze hardware
      ↓
isolate one parking phase
      ↓
change one relevant parameter
      ↓
repeat same starting condition
      ↓
record result
      ↓
compare
      ↓
keep or reject change
```

The final parking configuration should only be documented as validated after it can be reproduced across repeated trials.

---

## 4.1 Freeze the Physical Configuration First

Parking values are only meaningful for the hardware configuration used during calibration.

Before recording final parameters, the following should remain unchanged:

```text
Pixy2.1 mounting position

Pixy2.1 3D-printed casing

Color Sensor installation

S2 LEFT ultrasonic position

S3 RIGHT ultrasonic position

Motor B steering linkage

rear drivetrain

wheel configuration

EV3 placement
```

The active Obstacle Challenge sensor layout is:

```text
S1 → Pixy2.1

S2 → LEFT Ultrasonic Sensor

S3 → RIGHT Ultrasonic Sensor

S4 → Color Sensor
```

If one of these physical elements changes significantly, the affected parking calibration should be checked again.

For example, moving Pixy2.1 can change:

```text
Pink x-position

apparent Pink width

apparent Pink height

point where the target leaves the field of view
```

while changing steering geometry can modify:

```text
entry radius

alignment response

required encoder travel
```

Calibration therefore belongs to a **specific physical robot configuration**, not only to a software file.

---

## 4.2 Parameters That Require Parking Calibration

The parking subsystem can be divided into several parameter groups.

| Parameter Group | Physical Behavior |
| :--- | :--- |
| Pink confirmation | When parking target becomes trustworthy |
| Pink relevance | When the target is close/relevant enough to begin entry |
| Approach speed | How quickly Piolín reaches entry position |
| Entry steering | Curvature of the main parking arc |
| Entry speed | Distance traveled while steering changes |
| Entry progression | How long/far the first arc continues |
| Alignment steering | Strength of countersteering |
| Alignment progression | How long/far alignment continues |
| Final steering target | Wheel position during final movement |
| Final encoder travel | Longitudinal final progression |
| S2/S3 target geometry | Desired lateral parked relationship |
| Parking tolerances | Acceptable final variation |
| Final speed | Accuracy and stopping behavior |
| STOP condition | Evidence required to finish the run |

These values should not all be tuned simultaneously.

The recommended order is:

```text
VISION
  ↓
APPROACH
  ↓
ENTRY
  ↓
ALIGNMENT
  ↓
FINAL TRAVEL
  ↓
FINAL GEOMETRY
  ↓
STOP
```

---

# 4.3 Calibration Stage 1 — Verify Sensors and Steering

Before testing a parking trajectory, verify that the software receives correct physical information.

### Ultrasonic identity

The permanent convention must be:

```text
S2 = LEFT

S3 = RIGHT
```

This should be verified physically rather than assumed from variable names.

A simple test is:

```text
place object near LEFT sensor
→ S2 reading should decrease

place object near RIGHT sensor
→ S3 reading should decrease
```

The parking controller should never compensate for an incorrect sensor mapping by reversing later control signs.

---

### Steering direction

Verify:

```text
positive parking command
→ expected physical wheel direction

negative parking command
→ opposite physical wheel direction
```

and determine the repeatable Motor B center.

The steering subsystem should behave consistently before the team begins tuning:

```text
entry steering

countersteering

alignment
```

Otherwise every parking result will contain an uncontrolled mechanical variable.

---

### Motor A progression

Check that:

```python
drive.angle()
```

changes consistently with physical vehicle movement.

Encoder progression will later be used to measure:

```text
entry travel

alignment travel

final movement
```

so its sign and interpretation must already be understood.

---

# 4.4 Calibration Stage 2 — Pink Detection

<div align="center">

<img
  src="../../../v-photos/v4/pixy21_parking_detection.jpg"
  alt="Pixy2.1 detecting the Pink parking reference during calibration"
  width="680"
/>

<br>

<sub><b>Figure 4.2.</b> Pink detection should be calibrated before its coordinates or apparent size are used to control a parking trajectory.</sub>

</div>

The current parking signature is:

```text
sig1 → Pink
```

Before tuning steering, verify that Pixy2.1 identifies the parking reference reliably from representative approach positions.

Tests should include:

```text
target approximately centered

target left of image center

target right of image center

farther approach

closer approach

representative track illumination
```

For every trial, record:

```text
signature

x

y

width

height
```

The purpose is to understand the range of values produced by the **actual installed camera**, not to predict them theoretically.

A calibration table can be filled using real measurements:

| Position | Signature | x | y | Width | Height | Stable? |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Far / centered | — | — | — | — | — | — |
| Medium / centered | — | — | — | — | — | — |
| Near / centered | — | — | — | — | — | — |
| Medium / left | — | — | — | — | — | — |
| Medium / right | — | — | — | — | — | — |

No final target-relevance threshold should be selected until this data exists.

---

# 4.5 Calibrating Pink Confirmation

Parking should not activate from one unstable frame.

The conceptual logic is:

```python
if pink_visible:
    pink_confirmations += 1
else:
    pink_confirmations = 0
```

followed by:

```python
if pink_confirmations >= PARK_CONFIRMATIONS:
    parking_target_locked = True
```

Calibration should start with the smallest confirmation requirement that appears reasonably stable.

Then repeatedly approach the parking reference at the intended driving speed.

Observe:

```text
when Pink first appears

when Pink becomes confirmed

when parking steering actually begins
```

If confirmation is too permissive:

```text
target may lock from unstable detections
```

If confirmation is too strict:

```text
Piolín travels too far before entry begins
```

The correct value is therefore not:

```text
the highest stable count
```

but rather:

```text
the lowest confirmation level that remains reliably stable
at the intended operating speed
```

---

# 4.6 Calibration Stage 3 — Establish a Repeatable Approach

The parking entry cannot be tuned if Piolín begins from a different pose every time.

Before tuning the main arc, establish a repeatable:

```text
starting position

vehicle orientation

parking-target visibility

Motor B center
```

A controlled approach test should begin from the same marked location and use the same initial steering state.

The first goal is not to park.

It is simply:

> **Make Piolín reach approximately the same entry condition repeatedly.**

Useful observations include:

```text
Pink x

Pink width

Pink height

S2

S3

Motor B angle
```

at the moment the controller transitions:

```text
APPROACH
→ ENTRY
```

Once this transition becomes repeatable, the entry arc can be calibrated independently.

---

# 4.7 Calibration Stage 4 — Entry Steering and Entry Progression

<div align="center">

<img
  src="../../../v-photos/v4/ackermann_angles.jpg"
  alt="Piolín steering-angle relationship used during parking calibration"
  width="700"
/>

<br>

<sub><b>Figure 4.3.</b> Parking entry calibration relates Motor B steering behavior to the curved trajectory produced by the physical Ackermann mechanism.</sub>

</div>

The entry trajectory depends mainly on:

```text
entry steering

entry speed

entry progression
```

These should be tested systematically.

A useful calibration sequence is:

```text
1. Fix starting pose.

2. Fix entry speed.

3. Select one steering target.

4. Select one encoder progression.

5. Execute only the entry phase.

6. Stop.

7. Record resulting pose.

8. Repeat.
```

Only one of the principal variables should normally change between neighboring tests.

For example:

| Test | Entry Steering | Entry Progression | Entry Speed | Result |
| :---: | :---: | :---: | :---: | :--- |
| E01 | — | — | Fixed | — |
| E02 | slightly changed | same as E01 | Fixed | — |
| E03 | same as best previous | changed | Fixed | — |
| E04 | same | same | changed | — |

This reveals whether the observed failure is primarily caused by:

```text
trajectory curvature
```

or:

```text
distance traveled along that trajectory
```

Those are not the same problem.

---

## Entry too wide

Symptoms:

```text
Piolín does not move far enough laterally

parking space remains too far to one side
```

Possible changes:

```text
increase useful steering curvature

increase appropriate entry progression
```

but change them separately.

---

## Entry too tight

Symptoms:

```text
vehicle rotates aggressively

inside clearance becomes poor

alignment becomes difficult
```

Possible changes:

```text
reduce steering magnitude

reduce progression

reduce speed
```

Again, identify the first physical cause before changing several parameters.

---

# 4.8 Calibration Stage 5 — Alignment

Once the entry phase can repeatedly place Piolín inside a useful parking region, freeze it.

Then calibrate alignment.

Do not keep modifying entry while alignment is being studied unless testing proves the entry itself is still the problem.

The alignment variables are:

```text
countersteering direction

countersteering magnitude

alignment speed

alignment progression

steering release point
```

The objective is:

```text
preserve useful lateral position
+
reduce chassis orientation error
```

A useful experimental sequence is:

```text
known-good entry
      ↓
begin alignment
      ↓
apply one countersteer value
      ↓
move fixed progression
      ↓
stop
      ↓
record final geometry
```

Compare:

```text
S2

S3

Motor B position

visible chassis orientation
```

between trials.

A result that looks more centered but leaves the chassis strongly angled should not automatically be considered better.

Parking geometry includes both:

```text
position
```

and:

```text
orientation
```

---

# 4.9 Ultrasonic Calibration for Final Geometry

<div align="center">

<img
  src="../../../v-photos/v4/ultrasonic_pair_top.jpg"
  alt="Piolín lateral ultrasonic sensors used for parking geometry calibration"
  width="700"
/>

<br>

<sub><b>Figure 4.4.</b> S2 and S3 provide measurable lateral references for defining an acceptable final parking region.</sub>

</div>

After a visually acceptable parked position is achieved manually or through controlled tests, record the actual:

```text
S2 LEFT distance

S3 RIGHT distance
```

Repeat this process several times.

The purpose is to discover the real measurement range associated with acceptable parking.

A calibration worksheet can use:

| Acceptable Pose | S2 LEFT | S3 RIGHT | Motor B Angle | Notes |
| :---: | :---: | :---: | :---: | :--- |
| 1 | — | — | — | — |
| 2 | — | — | — | — |
| 3 | — | — | — | — |
| 4 | — | — | — | — |
| 5 | — | — | — | — |

Then compare the values.

If several successful poses naturally fall within similar ranges, those measurements can support:

```text
LEFT_TARGET

RIGHT_TARGET

LEFT_TOLERANCE

RIGHT_TOLERANCE
```

The targets should come from measured successful geometry.

They should **not** be chosen first and then forced onto the robot.

---

# 4.10 Calibration Stage 6 — Final Encoder Travel

The current development code contains:

```python
PARK_EXTRA_DEG = 300.0
```

This should be treated as:

```text
current prototype travel
```

not:

```text
validated parking distance
```

The final value should be calibrated only after:

```text
approach

entry

alignment
```

are sufficiently repeatable.

Otherwise the starting point of the final movement changes between runs and no single encoder value can be interpreted consistently.

The calibration process is:

```text
known-good approach
      ↓
known-good entry
      ↓
known-good alignment
      ↓
reset/store Motor A encoder
      ↓
perform final movement
      ↓
record endpoint
```

Try several nearby encoder progressions while keeping other conditions fixed.

A log can use:

| Test | Final Encoder Travel | Final Speed | S2 | S3 | Result |
| :---: | :---: | :---: | :---: | :---: | :--- |
| F01 | — | — | — | — | — |
| F02 | — | — | — | — | — |
| F03 | — | — | — | — | — |
| F04 | — | — | — | — | — |

The best value is not necessarily the one that looks perfect once.

It should produce an acceptable final position repeatedly.

---

# 4.11 Final Speed and Braking

Encoder calibration and speed calibration are connected.

Suppose the controller checks:

```python
if encoder_delta >= FINAL_PARK_ENCODER:
    drive.stop()
```

The physical robot still requires some finite time to reduce motion.

At higher speed:

```text
greater momentum / travel during stopping
```

can increase final-position variation.

At lower speed:

```text
better stopping resolution
```

but:

```text
longer maneuver
```

The final phase can therefore intentionally use a lower speed than:

```text
APPROACH

ENTRY
```

if testing shows that doing so improves stopping consistency.

The correct final speed should be selected through measured endpoint repeatability, not only by how fast the maneuver looks.

---

# 4.12 Calibrating the STOP Condition

The terminal condition should eventually combine several pieces of evidence.

Conceptually:

```python
final_encoder_ok = ...

left_geometry_ok = ...

right_geometry_ok = ...

steering_ok = ...
```

Then:

```python
parking_complete = (
    final_encoder_ok
    and left_geometry_ok
    and right_geometry_ok
    and steering_ok
)
```

This architecture should not be interpreted as requiring infinitely precise values.

Each condition should use a calibrated tolerance.

For example:

```python
left_ok = (
    abs(left_mm - LEFT_TARGET)
    <= LEFT_TOLERANCE
)
```

A tolerance should be selected from real repeatability data.

Too narrow:

```text
robot may never accept an otherwise valid parked pose
```

Too wide:

```text
poor final geometry may be accepted
```

The purpose of calibration is to identify an acceptable **region**, not one mathematically exact point.

---

# 4.13 Full Parking Validation

Once all phases work separately, they should be tested together.

The validation sequence should progress from simple to difficult:

```text
known parking starting pose
        ↓
complete parking algorithm
        ↓
repeat
```

then:

```text
slightly varied starting pose
        ↓
complete parking algorithm
```

and finally:

```text
full competition-style run
        ↓
12-course-event progression
        ↓
Pink acquisition
        ↓
parking
```

The final test is important, but it should come **after** the isolated phases work.

Otherwise a failed full run does not reveal whether the error originated in:

```text
approach

entry

alignment

final travel

parking eligibility
```

---

## Suggested Validation Log

| Trial | Start Condition | Pink Lock | Entry | Alignment | Final Position | STOP | Notes |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| 1 | Controlled | — | — | — | — | — | — |
| 2 | Controlled | — | — | — | — | — | — |
| 3 | Controlled | — | — | — | — | — | — |
| 4 | Slight variation | — | — | — | — | — | — |
| 5 | Full run | — | — | — | — | — | — |

The repository should record actual test outcomes rather than inventing a success percentage before sufficient trials exist.

---

# 4.14 Debug Values During Calibration

Parking telemetry should reveal both the current phase and the physical measurements controlling it.

A useful debug line can include:

```text
STATE

PARK_PHASE

COURSE_COUNT

PINK_VISIBLE

PINK_X

PINK_WIDTH

PINK_HEIGHT

S2_LEFT

S3_RIGHT

MOTOR_A_ENCODER

PHASE_ENCODER_DELTA

PARKING_COMMAND

MOTOR_B_TARGET

MOTOR_B_REAL

WALL_SAFETY
```

For example:

```text
STATE: PARKING
PHASE: ENTRY
PINK: True
X: ...
W: ...
S2: ...
S3: ...
ENC_D: ...
CMD: ...
STEER: ...
```

Then:

```text
STATE: PARKING
PHASE: ALIGN
S2: ...
S3: ...
CMD: ...
STEER: ...
```

and finally:

```text
STATE: STOP
FINAL_ENC: ...
S2: ...
S3: ...
```

Video and telemetry should ideally be reviewed together.

The video shows:

```text
what Piolín physically did
```

while the terminal shows:

```text
why the software did it
```

---

# 4.15 Change One Variable at a Time

Parking has many interacting values, so uncontrolled tuning can quickly destroy a previously successful maneuver.

For example, this is a poor experimental change:

```text
increase entry steering

increase speed

change Pink threshold

reduce alignment

change final encoder travel
```

all in the same version.

If the run improves, it becomes impossible to know which modification caused the improvement.

The preferred method is:

```text
BASELINE
   ↓
change ONE primary variable
   ↓
repeat test
   ↓
compare
```

If improved:

```text
save as new baseline
```

If worse:

```text
restore previous baseline
```

This is especially important because parking failures often originate one phase before the visible final error.

For example:

```text
overshoot at final stop
```

may actually begin with:

```text
bad alignment position
```

rather than only with an incorrect final encoder value.

---

# 4.16 Known-Good Parking Configuration

Once a set of parameters works repeatedly, the configuration should be preserved as a known-good baseline.

A calibration record should eventually include:

```text
Git commit

software version

physical robot configuration

Pixy installation

entry parameters

alignment parameters

final-travel parameter

geometry tolerances

test date

test result
```

Conceptually:

```text
PARKING BASELINE
      ↓
experiment branch/version
      ↓
test
      ↓
better?
 ┌────┴────┐
 │         │
YES        NO
 │         │
 ▼         ▼
SAVE      REVERT
```

The goal is to avoid losing a successful parking configuration while experimenting with improvements.

---

# 4.17 Current Values vs. Final Calibration

Some current development values already exist.

For example:

```text
LINES_TO_PARK = 12
```

and:

```text
PARK_EXTRA_DEG = 300
```

These should not be interpreted identically.

`LINES_TO_PARK = 12` reflects the current course-progression model:

```text
3 laps
→ 12 expected course events / corners
```

By contrast:

```text
PARK_EXTRA_DEG = 300
```

is a prototype movement parameter that still requires final parking calibration.

Other values still requiring measurement include:

```text
PARK_CONFIRMATIONS

Pink relevance threshold

approach speed

entry steering

entry encoder progression

entry speed

alignment steering

alignment progression

alignment speed

final steering target

final Motor A progression

final speed

S2 parking target

S3 parking target

parking tolerances
```

Until measured, these values should remain:

```text
TUNABLE
```

rather than:

```text
FINAL
```

---

# 4.18 Calibration Workflow Summary

The complete parking-calibration process is:

```text
                      FREEZE HARDWARE
                            │
                            ▼
                    VERIFY SENSOR SIDES
                            │
                            ▼
                    VERIFY STEERING SIGN
                            │
                            ▼
                     VERIFY PIXY sig1
                            │
                            ▼
                   CALIBRATE PINK LOCK
                            │
                            ▼
                 ESTABLISH REPEATABLE APPROACH
                            │
                            ▼
                     CALIBRATE ENTRY
                       /           \
                 steering        progression
                       \           /
                            ▼
                      FREEZE ENTRY
                            │
                            ▼
                   CALIBRATE ALIGNMENT
                       /           \
                countersteer      travel
                       \           /
                            ▼
                    FREEZE ALIGNMENT
                            │
                            ▼
               MEASURE ACCEPTABLE S2/S3
                            │
                            ▼
                 CALIBRATE FINAL ENCODER
                            │
                            ▼
                    CALIBRATE FINAL SPEED
                            │
                            ▼
                   DEFINE STOP TOLERANCES
                            │
                            ▼
                    REPEAT PARKING TESTS
                            │
                    ┌───────┴────────┐
                    │                │
                    ▼                ▼
               REPEATABLE?          NO
                    │                │
                   YES               └──► identify first
                    │                     incorrect phase
                    ▼
               SAVE BASELINE
                            │
                            ▼
                    FULL-COURSE TEST
```

This order allows every calibration stage to build on a previously verified physical behavior.

---

# 4.19 Final Engineering Assessment

Piolín's parking calibration is designed as a **measurement-driven process**, not random parameter adjustment.

The final maneuver contains several physically different problems:

```text
detect the parking target

reach a repeatable approach

generate the correct Ackermann entry arc

straighten the chassis

move to the final longitudinal position

verify final geometry

stop
```

Each should be calibrated separately before the complete maneuver is evaluated.

The current hardware provides complementary measurements:

```text
Pixy2.1
→ Pink identity and visual geometry
```

```text
S2 / S3
→ lateral physical geometry
```

```text
Motor A encoder
→ progression
```

```text
Motor B encoder
→ steering state
```

Because the Obstacle configuration has no Gyro Sensor, final parking orientation cannot be calibrated using a direct absolute heading value. Instead, the controller relies on repeatable steering phases and the resulting visual, lateral, and encoder geometry.

The current:

```text
PARK_EXTRA_DEG = 300
```

should remain documented as a prototype value until repeated testing determines the final movement required by the real parking geometry.

Likewise, final S2/S3 parking targets and tolerances should be obtained from **successful measured parked poses**, not invented in advance.

The central calibration principle is:

> **First make one phase repeatable, then freeze it and calibrate the next. A parameter becomes part of Piolín's final parking configuration only when its physical effect has been measured and the resulting behavior can be reproduced.**

Following this process allows PiolínTech to show not only the final parking values, but also the engineering reasoning and experimental method used to obtain them.

---

<div align="center">

### [← Back to PiolínTech Main README](../../../README.md)

</div>
