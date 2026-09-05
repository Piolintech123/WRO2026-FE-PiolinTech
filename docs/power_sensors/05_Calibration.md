# 5. Sensor Calibration

Piolín's sensors must be calibrated as part of the **complete installed robot**, not as isolated electronic components.

A sensor can operate correctly electrically while still producing poor navigation information if:

```text
Its mounting position changed

Its orientation changed

The track environment changed

Its thresholds were copied from an older robot version

Its software interpretation no longer matches the hardware
```

For this reason, calibration connects:

```text
PHYSICAL ROBOT
      +
SENSOR DATA
      +
SOFTWARE CONSTANTS
      ↓
USABLE NAVIGATION INFORMATION
```

The current Piolín sensing architecture includes:

```text
S1 → Front Ultrasonic

S2 → Right Ultrasonic

S3 → Left Ultrasonic

S4 → Downward Color Sensor

HuskyLens
 ↓
Arduino Nano
 ↓
USB
 ↓
LEGO EV3
```

Each subsystem requires a different type of calibration because each measures a different property of the environment.

The purpose of this document is to describe the **calibration model, variables, reasoning, and validation criteria** used by Piolín.

For a reproducible step-by-step calibration sequence, see:

[How to Calibrate Piolín](../reproducibility/06_HowToCalibrate.md)

---

## 5.1 Calibration Philosophy

Calibration should answer:

> What does this sensor output mean on the current physical Piolín robot?

It should not simply answer:

> What value did an older program use?

The preferred engineering process is:

```text
CURRENT HARDWARE
      ↓
MEASURE REAL ENVIRONMENT
      ↓
RECORD SENSOR OUTPUT
      ↓
IDENTIFY USEFUL RANGES
      ↓
SELECT CALIBRATION CONSTANTS
      ↓
TEST IN MOTION
      ↓
CONFIRM REPEATABILITY
```

This prevents historical development constants from becoming permanent assumptions.

---

# 5.2 Calibration vs. Tuning

Calibration and control tuning are related but different.

### Calibration

Calibration defines how sensor measurements correspond to the physical environment.

Examples:

```text
What ultrasonic distance represents
the desired wall relationship?


What RGB measurements represent BLUE?


What RGB measurements represent ORANGE?


Which HuskyLens ID represents GREEN?
```

### Tuning

Tuning determines how strongly the robot reacts to the calibrated information.

Examples:

```text
How much steering should be applied?


How fast should Motor A run?


How aggressive should obstacle recovery be?
```

Therefore:

```text
CALIBRATION
      ↓
Defines measurement meaning


TUNING
      ↓
Defines control response
```

Control gains should not be used to compensate for incorrectly calibrated sensors.

---

# 5.3 Calibration vs. Validation

Another important distinction is:

### Calibration

```text
Determine the values
the system should use
```

### Validation

```text
Verify those values still work
under representative conditions
```

For example:

```text
Calibrate BLUE range
        ↓
Run robot repeatedly over BLUE marking
        ↓
Verify consistent detection
```

A calibration value should not be considered final merely because it works once.

---

# 5.4 Current Sensor Calibration Responsibilities

| Sensor / System | Calibration Purpose |
| :--- | :--- |
| **S1 Front Ultrasonic** | Determine useful frontal safety interpretation |
| **S2 Right Ultrasonic** | Establish right-side distance behavior |
| **S3 Left Ultrasonic** | Establish left-side distance behavior |
| **S2 + S3 together** | Establish wall-following and corridor geometry |
| **S4 Color Sensor** | Distinguish Blue, Orange, and ordinary floor |
| **HuskyLens** | Confirm pillar IDs and reliable target recognition |
| **Nano → EV3 communication** | Confirm that vision identity reaches EV3 correctly |

These calibration tasks should remain separate because a correct value for one sensor does not validate another.

---

# 5.5 Calibration Dependency Chain

Piolín's calibration is hierarchical.

```text
MECHANICAL GEOMETRY
        ↓
SENSOR POSITION
        ↓
RAW MEASUREMENT
        ↓
FILTERING
        ↓
CLASSIFICATION / INTERPRETATION
        ↓
NAVIGATION STATE
        ↓
CONTROL
```

A change near the beginning of this chain can invalidate everything after it.

For example:

```text
Ultrasonic mount changes
        ↓
Measured wall distance changes
        ↓
Old D_TARGET becomes inaccurate
```

or:

```text
Color sensor height changes
        ↓
RGB values shift
        ↓
Old color thresholds become unreliable
```

For this reason, mechanical configuration should be stabilized before final sensor calibration.

---

# 5.6 Current Physical Calibration Baseline

The confirmed current robot configuration includes:

| Parameter | Current Value |
| :--- | :---: |
| **Robot length** | 210 mm |
| **Robot width** | 150 mm |
| **Robot height** | 230 mm |
| **Robot mass** | 0.80476 kg |
| **Lateral ultrasonic mounting height** | ~43.2 mm |
| **S1** | Front Ultrasonic |
| **S2** | Right Ultrasonic |
| **S3** | Left Ultrasonic |
| **S4** | Color Sensor |
| **Vision sensor** | HuskyLens |
| **Vision interface** | Arduino Nano |
| **Nano → EV3** | USB |

These values identify the physical configuration to which the current calibration process applies.

No previous geometry should be assumed equivalent unless it is re-measured on this configuration.

---

# 5.7 Calibration Order

A useful calibration order is:

```text
1. Verify mechanical assembly
        ↓
2. Verify port assignments
        ↓
3. Verify raw ultrasonic data
        ↓
4. Calibrate lateral wall geometry
        ↓
5. Calibrate frontal safety interpretation
        ↓
6. Calibrate floor-color classification
        ↓
7. Validate color-event processing
        ↓
8. Validate HuskyLens IDs
        ↓
9. Validate camera visibility
        ↓
10. Validate combined sensor behavior
```

This order moves from basic physical measurement toward higher-level sensor fusion.

---

# 5.8 Port Verification

Before numerical calibration, the software and hardware mapping must agree.

The current assignment is:

```text
S1 = FRONT

S2 = RIGHT

S3 = LEFT

S4 = COLOR
```

The USB vision path is:

```text
Arduino Nano
     ↓
USB
     ↓
LEGO EV3
```

A port mismatch can make perfectly accurate sensor data appear incorrect.

For example:

```text
Software expects RIGHT on S2

but physical LEFT sensor is connected there
        ↓
Navigation roles are reversed
```

Therefore, port verification always precedes calibration.

---

# 5.9 Raw Ultrasonic Baseline

Before applying filtering or navigation equations, each ultrasonic sensor should be inspected using its raw distance output.

Conceptually:

```text
S1
↓
D_FRONT_RAW


S2
↓
D_RIGHT_RAW


S3
↓
D_LEFT_RAW
```

The purpose is to determine whether:

```text
Distance increases when the wall moves away

Distance decreases when the wall moves closer

Readings remain physically plausible

Sensor orientation corresponds to expected surface
```

This separates sensor acquisition from navigation logic.

---

# 5.10 Ultrasonic Calibration Must Use the Installed Robot

The lateral sensors are mounted at approximately:

```text
43.2 mm above the floor
```

and face directly toward their respective sides.

Their calibration therefore depends on:

```text
Sensor position

Sensor orientation

Robot width

Track wall geometry
```

A distance measured by a sensor mounted differently on an older Piolín version should not automatically become the calibration constant for the current robot.

---

# 5.11 Physical Distance Reference

To calibrate an ultrasonic sensor, the team compares:

```text
Known physical distance
```

with:

```text
Reported sensor distance
```

Conceptually:

```text
WALL
 │
 │ ← known distance → [ SENSOR ]
 │
```

For a series of physical positions:

```text
D_TRUE
```

and corresponding sensor values:

```text
D_MEASURED
```

the measurement error is:

```text
E_D =
D_MEASURED - D_TRUE
```

and absolute error is:

```text
ABS_ERROR =
ABS(D_MEASURED - D_TRUE)
```

No final accuracy percentage is claimed unless measured on the current sensor installation.

---

# 5.12 Repeated Ultrasonic Measurements

One reading does not describe repeatability.

At each physical reference distance, several samples should be observed:

```text
D1
D2
D3
...
DN
```

The arithmetic mean is:

```text
D_MEAN =
(D1 + D2 + ... + DN) / N
```

and the variation between samples helps determine whether the measurement is stable enough for navigation.

However, the mean should not automatically be used as the navigation filter.

A median can be more robust when isolated ultrasonic outliers occur.

---

# 5.13 Median Calibration Check

Piolín's ultrasonic processing can use a short median concept.

For example:

```text
Reading 1 = 248 mm
Reading 2 = 250 mm
Reading 3 = 710 mm
```

then:

```text
MEDIAN = 250 mm
```

This helps distinguish:

```text
Typical local geometry
```

from:

```text
One isolated extreme sample
```

The example above is illustrative rather than a current recorded Piolín calibration result.

---

# 5.14 Lateral Sensor Calibration

S2 and S3 form the primary wall-navigation pair.

The calibration must establish how each sensor behaves at the robot's intended track position.

The physical variables are:

```text
D_LEFT

D_RIGHT
```

which later become:

```text
D_INNER

D_OUTER
```

according to travel direction.

The calibration process should therefore first work with physical left/right values before converting them into dynamic logical roles.

---

# 5.15 Inner-Wall Reference

During normal straight navigation, Piolín uses a desired relationship to the inner wall.

This can be represented as:

```text
D_TARGET
```

The wall-following error becomes:

```text
E_WALL =
D_TARGET - D_INNER
```

`D_TARGET` should be obtained from the current physical robot positioned in a useful track-relative location.

It should not be selected solely because an older program used the same number.

---

# 5.16 Why `D_TARGET` Is a Calibration Constant

Changing:

```text
Sensor position
```

or:

```text
Robot width
```

can change the correct sensor reading even if the desired vehicle center trajectory remains the same.

Therefore:

```text
Desired physical path
        ↓
Current sensor geometry
        ↓
Measured D_TARGET
```

The sensor target belongs to the complete installed geometry.

---

# 5.17 Inner-Wall Target Calibration

Conceptually, the target is established by:

```text
Place Piolín at desired straight-track position
        ↓
Align chassis in representative orientation
        ↓
Observe inner ultrasonic
        ↓
Repeat measurements
        ↓
Determine stable reference range
```

The resulting value can be represented as:

```text
D_TARGET
```

or a small acceptable interval:

```text
D_TARGET_MIN
to
D_TARGET_MAX
```

depending on the final software design.

---

# 5.18 Deadband Calibration

A steering controller should not necessarily react to every millimeter of measurement variation.

A deadband can be defined around the wall target.

```text
TARGET - DB
      ↓
acceptable region
      ↓
TARGET + DB
```

Conceptually:

```python
if abs(D_TARGET - D_INNER) <= DEADBAND:
    wall_error = 0
```

The deadband should be large enough to avoid unnecessary steering caused by measurement variation but small enough to maintain useful wall positioning.

Its final value belongs to current code calibration.

---

# 5.19 Deadband Trade-Off

If the deadband is too small:

```text
Tiny measurement changes
        ↓
Constant steering adjustments
        ↓
Possible zig-zag
```

If the deadband is too large:

```text
Robot can drift significantly
        ↓
No correction triggered
```

Therefore:

```text
DEADBAND
=
Noise tolerance
vs.
Position control
```

It should be selected from actual robot behavior.

---

# 5.20 Outer Sensor Calibration

The outer sensor should also be observed during the same straight-wall calibration.

The purpose is not necessarily to use:

```text
D_OUTER
```

as the main steering target.

Instead, it provides:

```text
Secondary geometry

Wall-safety information

Corner context

Geometry consistency
```

The relationship between the two lateral readings is especially useful.

---

# 5.21 Corridor Reference

During a valid straight-wall condition:

```text
D_INNER + D_OUTER
```

should remain within a characteristic range for the current robot and track geometry.

A reference can be represented as:

```text
C_REF
```

with:

```text
C_CURRENT =
D_INNER + D_OUTER
```

and:

```text
G =
ABS(C_CURRENT - C_REF)
```

`C_REF` should be derived from current straight-section measurements rather than inherited from a previous robot version.

---

# 5.22 Geometry Tolerance

The system can define a tolerance around:

```text
C_REF
```

to determine whether the usual corridor model is still plausible.

Conceptually:

```text
G <= G_TOL
      ↓
Normal corridor plausible
```

while:

```text
G > G_TOL
      ↓
Geometry has changed significantly
```

Possible causes include:

```text
Corner opening

Different wall orientation

Outlier measurement

Obstacle interference
```

The final value of:

```text
G_TOL
```

should be selected from current sensor data.

---

# 5.23 Why Corridor Calibration Helps Corner Detection

During a straight:

```text
Both sensors observe
the expected side boundaries
```

At a corner:

```text
One expected wall ends
```

and:

```text
D_INNER + D_OUTER
```

can change substantially.

Therefore, calibrating the normal corridor range provides a baseline against which geometry transitions can be recognized.

This complements direct:

```text
D_INNER
```

thresholds and state history.

---

# 5.24 Lateral Position Calibration

If the final physical lateral sensor offsets are measured, sensor values can be converted toward a common vehicle reference.

Conceptually:

```text
D_LEFT_C =
D_LEFT + O_LEFT
```

and:

```text
D_RIGHT_C =
D_RIGHT + O_RIGHT
```

where:

```text
O_LEFT
O_RIGHT
```

represent the sensor-to-reference offsets.

Then lateral position in a corridor of width `W` can be estimated as:

```text
X_EST =
(W + D_INNER_C - D_OUTER_C) / 2
```

No final offset values are claimed here because current final offsets have not been confirmed.

---

# 5.25 Why Old Sensor Offsets Are Not Reused

Legacy Piolín measurements contain previous development offsets and wall references.

Those values were associated with:

```text
Different robot geometry

Different sensor arrangement

Different navigation versions
```

Therefore:

```text
LEGACY OFFSET
      ≠
CURRENT OFFSET
```

unless physically re-measured and confirmed.

Historical geometry remains available in the legacy documentation but should not define current calibration.

---

# 5.26 Front Ultrasonic Calibration

S1 is calibrated separately because it is not part of the lateral wall-following model.

Its variable is:

```text
D_FRONT
```

and its responsibility is:

```text
Frontal safety
```

The calibration question is:

> At what measured forward clearance should the current vehicle no longer continue ordinary forward movement without a safety response?

This must be determined on the complete robot.

---

# 5.27 Why the Front Limit Depends on Vehicle Dynamics

A useful frontal safety distance depends on more than sensor accuracy.

It can also depend on:

```text
Vehicle speed

Motor response

Stopping behavior

Robot length

Sensor position

Steering state
```

At greater speed:

```text
Robot travels farther
during response time
```

so a safe threshold may need to be more conservative.

Therefore:

```text
FRONT SAFETY CALIBRATION
      =
Sensor geometry
+
Vehicle dynamics
```

not simply one arbitrary distance.

---

# 5.28 Front Safety Threshold

The final software may use a value conceptually represented as:

```text
FRONT_SAFETY_LIMIT
```

A condition could be:

```python
if D_FRONT < FRONT_SAFETY_LIMIT:
    frontal_risk = True
```

This document intentionally does not assign a numerical threshold because a current final value has not been established here.

The threshold should be taken from the active final code once validated.

---

# 5.29 Front Confirmation

Because one isolated reading can be abnormal, a safety system may use confirmation logic.

Conceptually:

```text
Close front reading
      ↓
Confirm condition
      ↓
Safety response
```

However, confirmation must not create excessive delay.

The number of readings and exact implementation should reflect current software rather than an assumed value.

---

# 5.30 Color Sensor Calibration

S4 requires optical calibration instead of distance calibration.

The main surface classes are:

```text
BLUE

ORANGE

NORMAL FLOOR
```

The purpose is to identify sensor ranges that separate these physical surfaces reliably in the current mounted configuration.

---

# 5.31 Color Calibration Environment

Color calibration should use the complete installed system:

```text
Current S4 sensor

Current mounting position

Current casing

Current sensor-to-floor spacing

Representative track surface

Representative lighting
```

Removing the sensor from the robot and calibrating it separately could produce values that do not match competition operation.

---

# 5.32 Raw Color Data Collection

When RGB-style data is used, samples can be recorded as:

```text
(R, G, B)
```

for each surface.

The calibration dataset should conceptually contain:

```text
BLUE:
(R1, G1, B1)
(R2, G2, B2)
...


ORANGE:
(R1, G1, B1)
(R2, G2, B2)
...


FLOOR:
(R1, G1, B1)
(R2, G2, B2)
...
```

The purpose is to identify **ranges and relationships**, not one perfect RGB tuple.

---

# 5.33 Why Multiple Color Samples Are Required

If only one sample is recorded:

```text
BLUE = one RGB value
```

the software may incorrectly assume that every future blue reading must match that exact value.

Real measurements vary.

Therefore calibration should identify:

```text
Typical minimums

Typical maximums

Channel relationships

Separation from other surfaces
```

using multiple measurements.

---

# 5.34 Color Classification Regions

Conceptually, calibration aims to establish non-identical regions such as:

```text
BLUE DATA
██████████


          separation


                    █████████
                    ORANGE DATA
```

The larger the separation between measured classes, the easier classification becomes.

If the classes overlap:

```text
More ambiguity
```

exists and the team may need to improve:

```text
Mechanical light isolation

Sensor position

Classification logic
```

rather than simply widening every threshold.

---

# 5.35 Color Threshold Logic

A color classifier can use multiple conditions.

Conceptually:

```python
def is_blue(r, g, b):
    return (
        condition_1
        and condition_2
        and condition_3
    )
```

and similarly:

```python
def is_orange(r, g, b):
    return (
        condition_1
        and condition_2
        and condition_3
    )
```

The specific conditions should be derived from the current calibration dataset.

No universal RGB threshold is assumed.

---

# 5.36 Absolute vs. Relative Color Conditions

Color classification can use:

```text
Absolute channel ranges
```

such as:

```text
B > some calibrated value
```

and/or relative relationships such as:

```text
B > R
```

depending on measured data.

Relative relationships can sometimes remain useful when overall brightness changes, but they are not automatically sufficient.

The final classifier should be chosen from current empirical samples.

---

# 5.37 Normal-Floor Calibration

The ordinary track surface is just as important as Blue and Orange.

The classifier needs to know when the robot has:

```text
LEFT the colored marking
```

so that:

```text
Color lock can reset

Next event can be recognized
```

Therefore:

```text
NORMAL FLOOR
```

is an active calibration class rather than simply "everything else."

---

# 5.38 Color Event Calibration

Correct color classification alone does not guarantee correct course counting.

The event layer must also be calibrated for:

```text
Confirmation

Locking

Unlock condition

Transition recognition

Cooldown behavior
```

The goal is:

```text
ONE PHYSICAL MARKING
      ↓
ONE VALID EVENT
```

---

# 5.39 Confirmation Trade-Off for S4

If too little confirmation is required:

```text
Noise
     ↓
False color event
```

If too much confirmation is required:

```text
Robot crosses marking quickly
        ↓
Insufficient confirmed samples
        ↓
Missed event
```

Therefore the final confirmation behavior must be tested at real operating speed.

---

# 5.40 Color Lock Calibration

The lock should remain active while Piolín is still associated with the same physical marking.

Conceptually:

```text
Detect BLUE
      ↓
Register once
      ↓
LOCK
      ↓
Remain BLUE
      ↓
No extra count
```

The release condition should occur only when the sensor has sufficiently left that marking.

---

# 5.41 Cooldown Calibration

If cooldown is used, it should reject rapid duplicate triggers without suppressing the next legitimate course event.

Too short:

```text
Boundary fluctuation
      ↓
Duplicate count
```

Too long:

```text
Next valid marking
      ↓
Still inside cooldown
      ↓
Missed event
```

The correct duration depends on:

```text
Vehicle speed

Marking spacing

Sampling rate

Classification stability
```

and should therefore be derived from the current run behavior.

---

# 5.42 Direction Calibration

The direction mapping itself is fixed and should be verified:

```text
BLUE FIRST
    ↓
COUNTERCLOCKWISE
```

```text
ORANGE FIRST
     ↓
CLOCKWISE
```

After the first valid direction event:

```text
direction
```

should be locked so later floor markings do not redefine the course direction.

The corresponding ultrasonic mapping is:

```text
COUNTERCLOCKWISE

S3 LEFT = INNER
S2 RIGHT = OUTER
```

and:

```text
CLOCKWISE

S2 RIGHT = INNER
S3 LEFT = OUTER
```

---

# 5.43 Progress Calibration

The intended three-lap course progression includes:

```text
12 valid BLUE events

12 valid ORANGE events
```

The calibration objective is not to force these counts artificially.

It is to ensure that each real physical marking produces exactly one valid event.

Therefore, the useful relationship is:

```text
PHYSICAL COURSE EVENTS
        ↓
S4 DETECTION
        ↓
12 BLUE + 12 ORANGE
```

for the complete intended progression.

---

# 5.44 HuskyLens Calibration

HuskyLens calibration focuses on obstacle identity rather than metric wall distance.

The confirmed current mapping is:

```text
ID 1
=
GREEN PILLAR
```

and:

```text
ID 2
=
RED PILLAR
```

The navigation interpretation is:

```text
GREEN
   ↓
Pass LEFT
```

and:

```text
RED
  ↓
Pass RIGHT
```

These mappings are current system constants and should remain consistent throughout the vision pipeline.

---

# 5.45 Vision Mapping Verification

Calibration should verify the complete information chain:

```text
Physical GREEN pillar
        ↓
HuskyLens
        ↓
ID 1
        ↓
Nano
        ↓
EV3
        ↓
GREEN state
```

and:

```text
Physical RED pillar
        ↓
HuskyLens
        ↓
ID 2
        ↓
Nano
        ↓
EV3
        ↓
RED state
```

A correct camera ID is not sufficient if the EV3 interprets it incorrectly.

---

# 5.46 HuskyLens Training Consistency

The learned identifiers stored in the HuskyLens must remain consistent with the software mapping.

If a target is re-learned under a different ID:

```text
Camera recognition may still work
```

but:

```text
EV3 meaning may become wrong
```

This can produce:

```text
Correct visual recognition
        ↓
Wrong navigation behavior
```

Therefore, ID consistency is part of calibration.

---

# 5.47 Vision Visibility Calibration

HuskyLens must also be validated physically.

Useful questions include:

```text
When does a pillar enter view?

Can both colors be recognized from representative approaches?

Does the chassis block part of the image?

Does the pillar leave the view too early during avoidance?

Does a corner orientation temporarily create a blind region?
```

These are not purely software questions.

They depend on the current camera mount.

---

# 5.48 Camera Mount Calibration

The current HuskyLens is forward-facing.

Its usable perception depends on:

```text
Height

Pitch

Horizontal orientation

Forward position

Structural obstruction
```

No final numerical camera height or angle is claimed here because those measurements have not been confirmed as final specifications.

The mount should be treated as calibrated when it remains physically stable and supports reliable obstacle visibility for the current vehicle strategy.

---

# 5.49 Camera Calibration Is Coupled to Speed

A pillar may be detected correctly but still too late for a given vehicle speed.

Therefore:

```text
Detection
     +
Communication
     +
Steering response
     +
Vehicle speed
     ↓
Available avoidance margin
```

Vision calibration should therefore be validated while Piolín is moving at representative obstacle-round speed.

---

# 5.50 Vision Classification vs. Avoidance Calibration

Two different results should be separated.

### Vision classification

```text
Did HuskyLens identify
GREEN / RED correctly?
```

### Vehicle avoidance

```text
Did Piolín pass on
the correct side safely?
```

If:

```text
ID is correct
```

but:

```text
Piolín hits pillar
```

the camera calibration may be valid while steering or timing requires tuning.

This distinction prevents unnecessary retraining of the vision system.

---

# 5.51 Nano–EV3 Communication Validation

The Nano-to-EV3 connection is confirmed as USB.

Calibration of this interface means verifying that the meaning transmitted by the Nano is interpreted correctly by the EV3.

Conceptually:

```text
Nano reports ID 1
        ↓
EV3 receives expected representation
        ↓
EV3 interprets GREEN
```

and similarly:

```text
Nano reports ID 2
        ↓
EV3 interprets RED
```

The exact packet format should be documented from the current code, not inferred here.

---

# 5.52 Unknown and No-Detection States

The vision interface should preserve distinct meanings for:

```text
GREEN

RED

NO TARGET

UNKNOWN / INVALID
```

These should not collapse into the same state.

For example:

```text
No target
```

should not automatically be interpreted as:

```text
RED
```

or:

```text
GREEN
```

Calibration therefore includes verifying the **absence state**, not only successful detections.

---

# 5.53 Sensor Fusion Calibration

After individual sensors are calibrated, they must be validated together.

For example:

```text
GREEN detected
       ↓
LEFT pass requested
```

while simultaneously:

```text
S3 reports left-wall geometry

S2 reports right-wall geometry

S1 reports frontal clearance
```

The EV3 must interpret these together without creating contradictory vehicle commands.

---

# 5.54 Sensor Fusion Is Not Sensor Averaging

Sensor fusion does not mean averaging:

```text
Ultrasonic distance

Color value

Camera ID
```

These represent different physical quantities and cannot be meaningfully averaged together.

Instead:

```text
ULTRASONIC
      ↓
Spatial constraint


COLOR
      ↓
Course state


HUSKYLENS
      ↓
Obstacle identity
```

are combined logically.

This is **decision-level fusion**, not numerical averaging of unrelated measurements.

---

# 5.55 Calibration by Navigation State

The same sensor can require different interpretation depending on current robot state.

For example:

### Straight state

```text
D_INNER
↓
Wall-following error
```

### Corner state

```text
Large D_INNER
↓
Possible wall disappearance
```

### Obstacle recovery

```text
D_LEFT + D_RIGHT
↓
Recovery geometry
```

Therefore, calibration should validate measurements in the states where they are actually used.

---

# 5.56 Static Calibration vs. Dynamic Calibration

Static calibration is useful for determining initial sensor behavior.

```text
Robot stationary
      ↓
Known geometry
      ↓
Record sensor output
```

However, Piolín operates while moving.

Dynamic calibration checks what happens during:

```text
Acceleration

Steering

Cornering

Obstacle avoidance

Recovery
```

Both are necessary because motion changes the physical geometry seen by the sensors.

---

# 5.57 Why Dynamic Calibration Matters for Ultrasonics

During a turn:

```text
Chassis rotates
        ↓
Lateral sensor orientation
relative to wall changes
        ↓
Measured distance changes
```

Therefore, a sensor value measured with Piolín perfectly parallel to a wall cannot describe every possible turning state.

Static measurements establish the baseline.

Dynamic behavior determines how that baseline should be interpreted in navigation.

---

# 5.58 Why Dynamic Calibration Matters for Color

During motion:

```text
S4 crosses marking
        ↓
Only a limited number of samples are available
```

and during a curve:

```text
S4 follows an arc
```

Therefore, color classification that works while the robot is held stationary should also be validated during realistic movement.

---

# 5.59 Why Dynamic Calibration Matters for Vision

While stationary, a pillar may remain centered and easy to recognize.

During driving:

```text
Camera translates

Camera rotates

Pillar approaches

Pillar moves across image
```

so visibility changes continuously.

Vision calibration should therefore include realistic driving trajectories.

---

# 5.60 Calibration Data Logging

Useful calibration logs should preserve both raw and interpreted values.

A combined diagnostic record can conceptually include:

```text
TIME

STATE

D_FRONT

D_LEFT

D_RIGHT

D_INNER

D_OUTER

COLOR_RAW

COLOR_CLASS

BLUE_COUNT

ORANGE_COUNT

PILLAR_ID

VISION_STATE

STEERING_COMMAND

DRIVE_COMMAND
```

This allows one recorded run to be analyzed across multiple subsystems.

---

# 5.61 Why Raw Data Should Be Preserved

Suppose the robot makes a wrong steering correction.

If only:

```text
STEERING = LEFT
```

is logged, it is difficult to determine why.

If the record contains:

```text
D_LEFT
D_RIGHT
STATE
STEERING
```

the team can trace:

```text
Measurement
      ↓
Interpretation
      ↓
Action
```

This is far more useful for calibration.

---

# 5.62 Calibration Dataset Separation

Data should be kept conceptually separated by purpose.

```text
ULTRASONIC CALIBRATION
      ↓
Distance / geometry


COLOR CALIBRATION
      ↓
Optical classification


VISION CALIBRATION
      ↓
Pillar identity


CONTROL TUNING
      ↓
Steering / speed response
```

Combining all changes simultaneously makes it difficult to determine which adjustment improved or degraded the run.

---

# 5.63 One Variable at a Time

During calibration, the preferred process is:

```text
Baseline
   ↓
Change one calibration parameter
   ↓
Run same condition
   ↓
Record result
   ↓
Compare
```

For example:

```text
Change BLUE threshold
```

without simultaneously changing:

```text
Drive speed

Steering strength

Ultrasonic target
```

This improves cause-and-effect traceability.

---

# 5.64 Hysteresis

Some sensor classifications benefit from different thresholds for entering and leaving a state.

This is called hysteresis.

Conceptually:

```text
ENTER BLUE
at one calibrated condition
```

but:

```text
LEAVE BLUE
only after moving clearly
outside that condition
```

This can reduce rapid switching:

```text
BLUE
OTHER
BLUE
OTHER
```

near the edge of a threshold.

Whether hysteresis is used in the final implementation should be documented from the current code.

---

# 5.65 Threshold Margin

A threshold should ideally not lie directly on top of the normal variation of two classes.

For example:

```text
Class A values
████████

threshold
        │

          ████████
          Class B values
```

provides more margin than:

```text
Class A ███████████
           │ threshold
        ███████████ Class B
```

where the distributions overlap substantially.

The same principle applies to:

```text
Color classification

Wall-loss detection

Geometry validity
```

Calibration seeks useful separation between states.

---

# 5.66 Avoiding Over-Calibrated Thresholds

A calibration value can work perfectly in one specific position but fail under ordinary variation.

For example:

```text
BLUE accepted only
within extremely narrow RGB range
```

may work during stationary testing but fail under:

```text
Small lighting changes

Movement

Different part of same marking
```

Calibration should therefore represent the **usable operating range**, not one perfect sample.

---

# 5.67 Avoiding Overly Broad Thresholds

The opposite problem also exists.

If a threshold is too broad:

```text
Normal floor
```

may be classified as:

```text
BLUE
```

or:

```text
ORANGE
```

Likewise, an overly permissive ultrasonic condition may confuse:

```text
Normal distance variation
```

with:

```text
Corner transition
```

Calibration therefore balances:

```text
Sensitivity
```

and:

```text
Specificity
```

for each sensor role.

---

# 5.68 Calibration and Mechanical Changes

Any significant change to:

```text
Sensor mount

Wheel geometry

Chassis geometry

Color casing

Camera position
```

should trigger a review of affected calibration constants.

For example:

```text
Move S2
    ↓
Review D_RIGHT behavior
    ↓
Review D_TARGET / C_REF
```

or:

```text
Move HuskyLens
    ↓
Review obstacle visibility
```

Calibration belongs to a physical configuration, not only to software.

---

# 5.69 Calibration and Software Changes

Software changes can also require recalibration.

For example, changing:

```text
Sensor filtering
```

can alter the value seen by higher-level control.

Likewise, changing:

```text
Color confirmation count
```

changes detection timing even if the RGB classifier is unchanged.

Therefore, calibration records should be associated with the software version that used them.

---

# 5.70 Calibration and Vehicle Speed

Sensor thresholds can be physically correct while navigation still fails because speed changed.

Higher speed changes:

```text
Response distance

Number of color samples

Vision reaction time

Corner transition timing
```

Therefore, after increasing Motor A speed, the team should verify that:

```text
Color events remain detectable

Corner geometry remains timely

Front safety margin remains adequate

Vision avoidance still begins early enough
```

without assuming the existing dynamic calibration remains optimal.

---

# 5.71 Calibration and Steering

Steering can also change sensor geometry.

During strong steering:

```text
Vehicle rotates faster
        ↓
Lateral ultrasonic angles
relative to walls change faster
```

and:

```text
Camera field of view rotates faster
```

Therefore, changing steering strength can alter how sensor events appear over time.

This is why calibration and control tuning interact even though they are conceptually separate.

---

# 5.72 Current Confirmed Calibration Mappings

The following current mappings are confirmed:

| Item | Current Mapping |
| :--- | :--- |
| **S1** | Front Ultrasonic |
| **S2** | Right Ultrasonic |
| **S3** | Left Ultrasonic |
| **S4** | Downward Color Sensor |
| **Blue first** | Counterclockwise |
| **Orange first** | Clockwise |
| **CCW inner sensor** | S3 Left |
| **CCW outer sensor** | S2 Right |
| **CW inner sensor** | S2 Right |
| **CW outer sensor** | S3 Left |
| **Green pillar** | HuskyLens ID 1 |
| **Green passing side** | Left |
| **Red pillar** | HuskyLens ID 2 |
| **Red passing side** | Right |
| **Nano → EV3** | USB |
| **Gyroscope** | Not used |
| **PixyCam** | Legacy |

These mappings are architectural calibration facts rather than numerical thresholds.

---

# 5.73 Numerical Values Intentionally Not Invented

The following calibration values should be taken from the final code or current measured data before being presented numerically:

```text
D_TARGET

D_TARGET_MIN / MAX

DEADBAND

C_REF

G_TOL

Front safety limit

Front confirmation count

Lateral ultrasonic offsets

Current RGB Blue thresholds

Current RGB Orange thresholds

Normal-floor thresholds

Color confirmation count

Color cooldown

Color lock-release condition

HuskyLens detection confirmation

Camera detection distance

Camera mounting angle

Camera mounting height

Camera field-of-view angle
```

Older values may remain useful as development history, but they should not be labeled as final calibration.

---

# 5.74 Calibration Configuration Table

Once current software values are frozen, the calibration architecture can be summarized using variables such as:

| Variable | Meaning | Source |
| :--- | :--- | :--- |
| `D_TARGET` | Desired inner-wall measurement | Lateral US calibration |
| `DEADBAND` | Acceptable wall-error region | Lateral US calibration |
| `C_REF` | Normal lateral corridor sum | Dual-US calibration |
| `G_TOL` | Geometry-consistency tolerance | Dual-US calibration |
| `FRONT_SAFETY_LIMIT` | Frontal safety distance | S1 calibration |
| `BLUE_RANGE` | Valid Blue classification region | S4 calibration |
| `ORANGE_RANGE` | Valid Orange classification region | S4 calibration |
| `FLOOR_RANGE` | Normal floor classification | S4 calibration |
| `COLOR_CONFIRM` | Color-event confirmation behavior | Dynamic S4 calibration |
| `ID_GREEN` | Green pillar identifier | HuskyLens |
| `ID_RED` | Red pillar identifier | HuskyLens |

This table describes the logical structure without inventing unsupported numerical values.

---

# 5.75 Calibration Acceptance Criteria

A calibration should be considered useful only when it supports repeatable behavior.

For ultrasonic navigation:

```text
Stable straight-wall interpretation

Correct corner transition recognition

Useful wall recovery

No frequent false safety events
```

For color:

```text
Blue detected

Orange detected

Normal floor rejected correctly

One physical marking produces one event
```

For vision:

```text
Green maps to ID 1

Red maps to ID 2

No-target state remains distinct

EV3 receives correct identity
```

These are system behaviors rather than arbitrary numerical accuracy claims.

---

# 5.76 Calibration Failure Categories

| Failure | Likely Calibration Area |
| :--- | :--- |
| Robot continuously hugs one wall | `D_TARGET`, steering center, sensor geometry |
| Robot oscillates on straight | Deadband/filtering/control interaction |
| Corner not recognized | Wall-loss / geometry calibration |
| False corner appears | Filtering / geometry tolerance |
| Front safety activates unnecessarily | S1 threshold / measurement interpretation |
| Blue missed | S4 Blue classification or timing |
| Orange missed | S4 Orange classification or timing |
| One marking counted multiple times | Lock/cooldown/event logic |
| Wrong initial direction | Color mapping or event classification |
| Green causes right-side behavior | Vision ID mapping / software interpretation |
| Red causes left-side behavior | Vision ID mapping / software interpretation |
| Correct ID but pillar collision | Mobility/control timing rather than classification |
| Pillar recognized too late in motion | Vision geometry / speed interaction |

This table helps identify which calibration layer should be inspected first.

---

# 5.77 Calibration Diagnostic Hierarchy

When a sensor-related problem occurs:

```text
CHECK PHYSICAL MOUNT
        ↓
CHECK CONNECTION
        ↓
CHECK RAW DATA
        ↓
CHECK FILTERED DATA
        ↓
CHECK CLASSIFICATION
        ↓
CHECK STATE LOGIC
        ↓
CHECK CONTROL RESPONSE
```

The key principle is:

```text
Do not tune Motor B
to compensate for
incorrect sensor interpretation
```

unless the sensing layer has first been verified.

---

# 5.78 Current vs. Legacy Calibration

Piolín's development history contains calibration values associated with:

```text
Two-ultrasonic configurations

Gyroscope navigation

Different sensor positions

Different wall targets

Different color thresholds

PixyCam

Alternative control systems
```

Those values remain useful as evidence of engineering development.

They do not automatically describe the current robot.

The current rule is:

```text
CURRENT HARDWARE
      ↓
CURRENT MEASUREMENT
      ↓
CURRENT CALIBRATION
```

Historical systems are documented in:

[Legacy Documentation](../legacy/00_LEGACY_NOTICE.md)

[Legacy Gyroscope Configuration](../legacy/01_GConfig.md)

[Legacy PixyCam](../legacy/02_CameraPixy.md)

[Legacy Performance Testing](../legacy/03_PTesting&Analysis.md)

---

# 5.79 Calibration Traceability

Every important calibration constant should ultimately be traceable through:

```text
PHYSICAL REQUIREMENT
      ↓
MEASUREMENT
      ↓
SELECTED VALUE
      ↓
CODE CONSTANT
      ↓
TEST RESULT
```

For example:

```text
Desired wall position
      ↓
Measured S3 / S2 values
      ↓
D_TARGET
      ↓
Wall-following code
      ↓
Straight-run evidence
```

or:

```text
Physical Blue marking
      ↓
Recorded RGB samples
      ↓
Blue classifier
      ↓
S4 code
      ↓
Color-detection evidence
```

This traceability is one of the strongest ways to demonstrate that constants were engineered rather than guessed.

---

# 5.80 Calibration and Reproducibility

A second Piolín build should not require guessing sensor constants from scratch.

The repository should explain:

```text
What must be measured

Why it must be measured

What variable it produces

Where that variable is used
```

The exact execution steps belong in:

[How to Calibrate](../reproducibility/06_HowToCalibrate.md)

while this document explains the technical meaning behind those steps.

Together:

```text
05_Calibration.md
      ↓
WHY + WHAT


06_HowToCalibrate.md
      ↓
HOW
```

This separation improves repository organization.

---

# 5.81 Complete Calibration Pipeline

The complete current sensor-calibration architecture can be summarized as:

```text
                       PHYSICAL PIOLÍN
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
   ULTRASONICS               COLOR                VISION
        │                     │                     │
        ▼                     ▼                     ▼
 RAW DISTANCES            RAW OPTICAL            TARGET ID
        │                     │                     │
        ▼                     ▼                     ▼
   FILTERING             CLASSIFICATION       ID VALIDATION
        │                     │                     │
        ▼                     ▼                     ▼
 WALL / SAFETY           COLOR EVENT        OBSTACLE STATE
 INTERPRETATION           PROCESSING               │
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              ▼
                           LEGO EV3
                              │
                              ▼
                     NAVIGATION STATE
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
                 Motor A             Motor B
```

Calibration defines the transformation between each physical measurement and its usable navigation meaning.

---

# 5.82 Ultrasonic Calibration Summary

The current ultrasonic calibration structure is:

```text
S2 / S3
   ↓
D_LEFT / D_RIGHT
   ↓
Direction mapping
   ↓
D_INNER / D_OUTER
   ↓
Wall target + geometry reference
```

with:

```text
E_WALL =
D_TARGET - D_INNER
```

and:

```text
G =
ABS(
(D_INNER + D_OUTER)
-
C_REF
)
```

while:

```text
S1
 ↓
D_FRONT
 ↓
Independent frontal safety calibration
```

The front sensor remains separate from lateral geometry.

---

# 5.83 Color Calibration Summary

The color calibration structure is:

```text
S4
 ↓
Raw optical sample
 ↓
BLUE / ORANGE / FLOOR
 ↓
Confirmation
 ↓
Event lock
 ↓
Valid event
 ↓
Direction or progress
```

with confirmed mappings:

```text
BLUE first
=
COUNTERCLOCKWISE
```

and:

```text
ORANGE first
=
CLOCKWISE
```

The intended full three-lap progression contains:

```text
12 valid BLUE events

12 valid ORANGE events
```

rather than counting every raw sample.

---

# 5.84 Vision Calibration Summary

The current vision calibration structure is:

```text
HuskyLens
    ↓
Known pillar ID
    ↓
Arduino Nano
    ↓
USB
    ↓
EV3
```

with:

```text
ID 1 = GREEN = PASS LEFT

ID 2 = RED = PASS RIGHT
```

Calibration verifies both:

```text
Correct recognition
```

and:

```text
Correct end-to-end interpretation
```

without treating obstacle steering itself as part of camera classification.

---

# 5.85 Final Calibration Architecture

Piolín's calibration process is based on one central principle:

> **A calibration value belongs to the current physical robot, current sensor installation, current software interpretation, and current operating environment.**

The final sensor stack is:

```text
                    ENVIRONMENT
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
      WALLS            FLOOR            PILLARS
        │                │                │
        ▼                ▼                ▼
   S1 / S2 / S3          S4           HuskyLens
        │                │                │
        ▼                ▼                ▼
    DISTANCE         COLOR DATA         ID DATA
        │                │                │
        ▼                ▼                ▼
   CALIBRATION       CALIBRATION      CALIBRATION
        │                │                │
        └────────────────┼────────────────┘
                         ▼
                      LEGO EV3
                         │
                         ▼
                NAVIGATION DECISION
```

The current architecture does **not** rely on copied legacy constants or unverified theoretical numbers.

Instead:

```text
MEASURE
   ↓
CALIBRATE
   ↓
VALIDATE
   ↓
IMPLEMENT
   ↓
TEST
   ↓
RECALIBRATE IF HARDWARE CHANGES
```

This provides a traceable engineering relationship between Piolín's physical environment and its autonomous software.

---

## Power and Sensor Documentation

[Power and Sensor Configuration](01_PowerSensorconfig.md)

[Ultrasonic Sensor Data](02_USSensorD.md)

[Color Sensor](03_color_sensor.md)

[HuskyLens Vision System](04_huskylens.md)

---

## Reproducibility

[Wiring](../reproducibility/03_wiring.md)

[Electrical Schematic](../reproducibility/04_elecschem.md)

[Software Setup](../reproducibility/05_softwaresetup.md)

[How to Calibrate](../reproducibility/06_HowToCalibrate.md)

[Testing Protocol](../reproducibility/07_TestingProtocol.md)

[Troubleshooting](../reproducibility/08_Troubleshooting.md)

---

## Related Software Documentation

[Software Architecture](../software_obstacles_strategy/01_SWArchitecture.md)

[State Machine](../software_obstacles_strategy/02_statemachine.md)

[Wall Following](../software_obstacles_strategy/03_wallfollowing.md)

[Corner Handling](../software_obstacles_strategy/04_cornerhandling.md)

[Obstacle Detection](../software_obstacles_strategy/05_obstacledetec.md)

[Obstacle Strategy](../software_obstacles_strategy/06_obstaclestrateg.md)

[Software Tuning](../software_obstacles_strategy/07_softwaretuning.md)

[HuskyLens Vision](../software_obstacles_strategy/08_CameraHLVision.md)

[RGB Detection](../software_obstacles_strategy/09_RGBdetection.md)

---

## Historical Reference

[Legacy Documentation Notice](../legacy/00_LEGACY_NOTICE.md)

[Legacy Gyroscope Configuration](../legacy/01_GConfig.md)

[Legacy PixyCam](../legacy/02_CameraPixy.md)

[Legacy Performance Testing](../legacy/03_PTesting&Analysis.md)
