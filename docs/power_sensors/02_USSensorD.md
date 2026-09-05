# 2. Ultrasonic Sensor Data and Geometry

Piolín uses **three LEGO ultrasonic sensors** to obtain spatial information about the WRO Future Engineers track.

The current configuration is:

```text
S1 → Front Ultrasonic Sensor

S2 → Right Ultrasonic Sensor

S3 → Left Ultrasonic Sensor
```

These sensors do not all perform the same task.

The two lateral sensors form the main geometric navigation pair:

```text
S2 + S3
   ↓
Lateral track geometry
```

while the front sensor is kept logically separate:

```text
S1
 ↓
Frontal safety
```

This distinction is fundamental to the current Piolín architecture.

The lateral sensors are used to understand where the vehicle is relative to the track boundaries and how that geometry changes when entering or leaving a corner.

The front sensor is used to identify limited clearance directly ahead and is not part of the normal inner-wall / outer-wall calculations.

The complete ultrasonic relationship is:

```text
                         FRONT
                           ↑

                     S1 FRONT US
                           │


             S3 LEFT       │       S2 RIGHT
                ←      [ PIOLÍN ]      →
```

For the complete sensor configuration, see:

[Power and Sensor Configuration](01_PowerSensorconfig.md)

[Ultrasonic Sensor Hardware](../components/05_UltrasonicSensors.md)

---

## 2.1 Current Ultrasonic Roles

| Sensor | Physical Position | Logical Responsibility |
| :--- | :--- | :--- |
| **S1** | Front | Frontal safety |
| **S2** | Right side | Right-wall geometry |
| **S3** | Left side | Left-wall geometry |

The current system deliberately separates:

```text
NAVIGATION GEOMETRY
```

from:

```text
FRONTAL SAFETY
```

Therefore:

```text
S1
```

must not be inserted into formulas intended for:

```text
D_INNER

D_OUTER
```

The two systems answer different questions.

---

# 2.2 Physical and Logical Sensor Names

Two naming systems are useful in software.

The physical names are fixed:

```text
D_LEFT
=
S3 reading


D_RIGHT
=
S2 reading


D_FRONT
=
S1 reading
```

These describe where each sensor is physically mounted.

The navigation names are dynamic:

```text
D_INNER

D_OUTER
```

These describe the sensor's role relative to the course direction.

This distinction allows the same navigation equations to be used in clockwise and counterclockwise operation.

---

# 2.3 Dynamic Inner and Outer Assignment

Piolín uses the first valid floor-color event to determine the course direction.

```text
BLUE FIRST
    ↓
COUNTERCLOCKWISE
```

For counterclockwise travel:

```text
D_INNER = D_LEFT

D_OUTER = D_RIGHT
```

because:

```text
S3 LEFT  = INNER

S2 RIGHT = OUTER
```

For clockwise travel:

```text
ORANGE FIRST
     ↓
CLOCKWISE
```

and:

```text
D_INNER = D_RIGHT

D_OUTER = D_LEFT
```

because:

```text
S2 RIGHT = INNER

S3 LEFT  = OUTER
```

The physical sensors do not move.

Only their **logical interpretation** changes.

---

# 2.4 Direction Mapping

The mapping can be represented as:

```python
if direction == COUNTERCLOCKWISE:
    D_INNER = D_LEFT
    D_OUTER = D_RIGHT

elif direction == CLOCKWISE:
    D_INNER = D_RIGHT
    D_OUTER = D_LEFT
```

This abstraction is useful because later navigation code can operate using:

```text
D_INNER
```

and:

```text
D_OUTER
```

without needing a completely different steering algorithm for each travel direction.

---

# 2.5 Current Lateral Sensor Mounting

The two lateral ultrasonic sensors are mounted directly toward their respective sides.

Their confirmed approximate mounting height is:

```text
43.2 mm
```

above the track surface.

Conceptually:

```text
LEFT WALL                               RIGHT WALL
    │                                       │
    │                                       │
    ▼                                       ▼
   S3  ←──────────── [ PIOLÍN ] ─────────→ S2
```

The sensor height matters because the ultrasonic beam must intersect the intended vertical wall surfaces rather than floor-level geometry.

Their lateral orientation is also important because the software interprets their values as side-wall measurements.

---

# 2.6 What an Ultrasonic Reading Represents

An ultrasonic sensor reports distance from the sensor toward the reflecting surface detected within its acoustic field.

Therefore:

```text
ULTRASONIC READING
        =
Distance from sensor
to detected surface
```

It does **not** directly represent:

```text
Robot center position

Vehicle heading

Distance from wheel to wall

Distance from chassis edge to wall
```

unless the physical offsets between those reference points are also included.

This distinction is essential when building a geometric navigation model.

---

# 2.7 Ultrasonic Time-of-Flight Principle

Ultrasonic ranging is based on the travel time of an acoustic pulse.

The physical sequence is:

```text
Sensor emits pulse
        ↓
Pulse travels to wall
        ↓
Wall reflects pulse
        ↓
Echo returns to sensor
        ↓
Travel time measured
```

The ideal physical relationship is:

```text
d =
(v × t) / 2
```

where:

```text
d = distance to reflecting surface

v = speed of sound

t = round-trip acoustic travel time
```

The division by two is required because the sound travels:

```text
Sensor → Surface
```

and then:

```text
Surface → Sensor
```

The LEGO sensor interface provides usable distance data to the EV3, so Piolín's navigation code works with the resulting distance measurement rather than manually timing the acoustic pulse.

---

# 2.8 Unit Consistency

All ultrasonic calculations should use one consistent unit system.

For example:

```text
millimeters
```

or:

```text
centimeters
```

but different units should not be mixed inside the same geometric expression.

A conversion between the two is:

```text
1 cm = 10 mm
```

and:

```text
D_CM =
D_MM / 10
```

For example:

```text
245 mm
=
24.5 cm
```

A consistent unit convention prevents calibration constants from being interpreted incorrectly.

---

# 2.9 Raw Distance Variables

A clear software representation is:

```text
D_FRONT
=
Current S1 measurement


D_RIGHT
=
Current S2 measurement


D_LEFT
=
Current S3 measurement
```

After travel direction is known:

```text
D_INNER
=
Selected lateral inner-wall value


D_OUTER
=
Selected lateral outer-wall value
```

The resulting information path is:

```text
S2 + S3
   ↓
Physical readings
   ↓
Direction mapping
   ↓
D_INNER + D_OUTER
   ↓
Navigation geometry
```

---

# 2.10 Why the Front Sensor Is Excluded From Lateral Geometry

S1 observes a different spatial direction.

```text
                    S1
                    ↑
                    │

         S3 ← [ PIOLÍN ] → S2
```

Therefore:

```text
D_FRONT
```

cannot be combined directly with:

```text
D_INNER + D_OUTER
```

to estimate the lateral corridor geometry.

The lateral pair answers:

> Where is Piolín relative to the side boundaries?

The front sensor answers:

> Is the available space directly ahead becoming unsafe?

These are independent spatial questions.

---

# 2.11 Side-Wall Navigation

During a normal straight section, Piolín primarily follows the inner wall.

Conceptually:

```text
Desired inner-wall relationship
              ↓
          Compare with
              ↓
           D_INNER
              ↓
        Navigation error
              ↓
       Steering correction
```

The basic wall error can be represented as:

```text
E_WALL =
D_TARGET - D_INNER
```

where:

```text
D_TARGET
=
Calibrated inner-wall reference
```

and:

```text
D_INNER
=
Current inner-wall measurement
```

The exact final value of `D_TARGET` belongs to current calibration and competition software and is not assigned an unconfirmed number in this document.

---

# 2.12 Wall Error Sign

Suppose:

```text
E_WALL =
D_TARGET - D_INNER
```

If:

```text
D_INNER < D_TARGET
```

then Piolín is closer to the inner wall than the target relationship.

If:

```text
D_INNER > D_TARGET
```

then Piolín is farther from the inner wall.

The steering controller converts the magnitude and sign of this error into the appropriate physical correction according to the current direction of travel.

The exact steering sign depends on the software coordinate convention.

---

# 2.13 Deadband

Very small sensor variations should not necessarily produce constant steering movement.

A deadband can conceptually be defined as:

```text
if ABS(E_WALL) <= DEADBAND:
    correction = 0
```

This creates a small acceptable region around the target:

```text
Too close      Acceptable       Too far
    │              │               │
────┼──────────────┼───────────────┼────
```

The purpose is to prevent the steering motor from reacting continuously to insignificant distance variation.

The current numerical deadband should be taken from the active code or calibration documentation rather than assumed here.

---

# 2.14 Why One Lateral Sensor Is Not Enough for Every State

During ordinary straight navigation, the inner sensor can provide a strong primary reference.

However, at a corner:

```text
Inner wall ends
        ↓
D_INNER changes sharply
```

If the robot continued treating that new value as an ordinary wall-following error:

```text
Large apparent error
        ↓
Incorrect steering response
```

Therefore the software must distinguish:

```text
WALL DISTANCE ERROR
```

from:

```text
WALL NO LONGER PRESENT
```

This is why Piolín also uses the outer sensor and navigation state.

---

# 2.15 Inner-Wall Disappearance

The WRO track geometry creates a characteristic transition at a corner.

Before the corner:

```text
INNER WALL
    │
    │
    │
    │
```

The inner sensor observes a nearby continuous surface.

At the corner:

```text
INNER WALL
    │
    │
    └──────── opening
```

the previous wall surface ends.

The sensor can therefore report a much larger distance or a different geometry.

Conceptually:

```text
D_INNER
stable
   ↓
D_INNER increases
   ↓
Potential corner entry
```

This transition is not interpreted simply as "Piolín is too far from the wall."

It can indicate that the wall itself has ended.

---

# 2.16 Corner Confirmation

A single unusual ultrasonic reading should not automatically be treated as a confirmed corner.

The navigation architecture can combine:

```text
Inner distance behavior

Outer distance behavior

Previous navigation state

Vehicle motion

Color/course information where relevant
```

to determine whether the geometry corresponds to a real corner.

Conceptually:

```text
Unusual D_INNER
      ↓
Is geometry consistent with corner?
      ↓
YES → Corner state
NO  → Continue / reject abnormal reading
```

This reduces sensitivity to isolated ultrasonic anomalies.

---

# 2.17 Outer Sensor During a Corner

During normal straight driving:

```text
D_INNER
```

is often the strongest navigation reference.

During a corner:

```text
D_INNER
```

may lose its normal wall.

At this point:

```text
D_OUTER
```

can become more useful.

The conceptual transition is:

```text
STRAIGHT
   ↓
Inner-wall reference


CORNER
   ↓
Outer geometry becomes temporarily important


EXIT
   ↓
Inner wall reacquired
```

This allows Piolín to navigate corners without relying on a gyroscope.

---

# 2.18 Inner-Wall Reacquisition

As Piolín finishes the turn, the next inner wall enters the lateral sensor's useful region.

Conceptually:

```text
Corner turning
      ↓
New straight approaches
      ↓
Inner wall becomes visible
      ↓
D_INNER returns to expected range
      ↓
Corner exit can be confirmed
```

The software can then reduce the corner steering command and transition back toward normal wall following.

This relationship is central to the current no-gyro Open Challenge architecture.

---

# 2.19 Geometry State Sequence

The complete lateral geometry sequence can be summarized as:

```text
INNER WALL PRESENT
        ↓
NORMAL WALL FOLLOWING
        ↓
INNER WALL DISAPPEARS
        ↓
CORNER ENTRY
        ↓
OUTER GEOMETRY USED
        ↓
VEHICLE ROTATES
        ↓
INNER WALL REAPPEARS
        ↓
CORNER EXIT
        ↓
STABILIZATION
        ↓
NORMAL WALL FOLLOWING
```

This makes the ultrasonic pair part of both:

```text
Continuous control
```

and:

```text
Discrete state detection
```

---

# 2.20 Corridor Geometry Model

When both side walls are visible and the readings have been converted to a common geometric reference, Piolín can reason about its lateral position inside the corridor.

Let:

```text
W
=
Distance between the two reference walls


D_INNER_C
=
Inner-wall distance corrected to a common
robot reference point


D_OUTER_C
=
Outer-wall distance corrected to the same
reference point
```

Then:

```text
D_INNER_C + D_OUTER_C ≈ W
```

during a suitable straight-wall condition.

This provides a useful consistency relationship.

---

# 2.21 Estimating Lateral Position

If:

```text
X
```

represents the vehicle reference position measured from the inner wall, then:

```text
D_INNER_C ≈ X
```

and:

```text
D_OUTER_C ≈ W - X
```

Subtracting:

```text
D_INNER_C - D_OUTER_C
=
2X - W
```

therefore:

```text
X =
(W + D_INNER_C - D_OUTER_C) / 2
```

This is the general lateral-position relationship:

```text
X_EST =
(W + D_INNER_C - D_OUTER_C) / 2
```

It can be useful when both walls are available and the sensor measurements are expressed relative to a consistent geometric reference.

---

# 2.22 Why Raw Sensor Values Need Offset Awareness

The actual ultrasonic sensors are not located at the exact geometric center of Piolín.

Therefore raw measurements represent:

```text
Sensor face → wall
```

rather than:

```text
Robot center → wall
```

To obtain a center-referenced model, lateral sensor offsets would need to be considered.

Conceptually:

```text
D_LEFT_CENTER
=
D_LEFT_RAW + O_LEFT
```

and:

```text
D_RIGHT_CENTER
=
D_RIGHT_RAW + O_RIGHT
```

where:

```text
O_LEFT

O_RIGHT
```

represent the relevant physical sensor offsets.

No final numerical offset values are claimed in this document because the current final offsets have not been established as confirmed measurements.

This prevents development-stage dimensions from being presented as final geometry.

---

# 2.23 Raw-Sum Consistency

Even without converting every reading into an exact robot-center position, the lateral pair can provide a useful geometric consistency check.

Let:

```text
C_REF
```

represent the expected sum of the two lateral readings for a valid straight-wall condition under the chosen sensor geometry.

Then:

```text
C_CURRENT =
D_INNER + D_OUTER
```

and a geometric consistency error can be defined as:

```text
G =
ABS(C_CURRENT - C_REF)
```

or:

```text
G =
ABS(
(D_INNER + D_OUTER)
-
C_REF
)
```

A small `G` suggests that both readings are reasonably compatible with the expected corridor geometry.

A large `G` can indicate that the usual straight-wall model is no longer valid.

---

# 2.24 Meaning of the Geometry Error `G`

The consistency variable:

```text
G
```

does not directly tell Piolín which way to steer.

Instead, it answers a different question:

> Do the two lateral readings still resemble the expected straight-corridor geometry?

Conceptually:

```text
Small G
   ↓
Both walls likely consistent
with normal corridor geometry
```

while:

```text
Large G
   ↓
Possible corner
Possible opening
Possible unusual reflection
Possible invalid reading
```

This makes `G` useful as a **state-quality indicator**.

---

# 2.25 Geometry Gating

A geometry gate can conceptually be implemented as:

```python
geometry_error = abs(
    (D_INNER + D_OUTER) - C_REF
)

if geometry_error <= GEOMETRY_TOLERANCE:
    corridor_valid = True
else:
    corridor_valid = False
```

No numerical `C_REF` or `GEOMETRY_TOLERANCE` is assigned here because those values depend on the final physical robot and course calibration.

The architecture is more important than an old experimental constant.

---

# 2.26 Why `D_INNER + D_OUTER` Changes at Corners

During a straight section:

```text
LEFT WALL                RIGHT WALL
    │                        │
    │       PIOLÍN           │
    │                        │
```

both sensors observe surfaces belonging to the same corridor.

Therefore the total lateral geometry is relatively constrained.

At a corner:

```text
one expected wall ends
```

and one sensor may observe:

```text
A distant surface

An opening

A different wall orientation
```

Therefore:

```text
D_INNER + D_OUTER
```

can differ significantly from its normal straight-section reference.

This is why the sum can help distinguish:

```text
Ordinary lateral position error
```

from:

```text
Track geometry transition
```

---

# 2.27 Position Error vs. Geometry Error

Two different errors can therefore exist.

### Position error

```text
E_WALL =
D_TARGET - D_INNER
```

This answers:

> Am I at the desired distance from the inner wall?

### Geometry error

```text
G =
ABS(
(D_INNER + D_OUTER)
-
C_REF
)
```

This answers:

> Does the current lateral scene still look like the expected corridor?

These values have different responsibilities.

```text
E_WALL
      ↓
Steering correction


G
      ↓
Geometry / state confidence
```

This separation improves the interpretation of the ultrasonic data.

---

# 2.28 Example Straight Geometry

Consider a generic example where both side walls are visible.

```text
INNER WALL                   OUTER WALL
    │                            │
    │     ← D_INNER →            │
    │          [PIOLÍN]          │
    │                ←D_OUTER→   │
    │                            │
```

If the robot moves slightly toward the inner wall:

```text
D_INNER decreases
```

while:

```text
D_OUTER increases
```

The two values therefore change in opposite directions.

This is characteristic of lateral displacement inside a fixed corridor.

---

# 2.29 Example Heading Change

Now suppose Piolín rotates while remaining near approximately the same lateral region.

Because the ultrasonic sensors are attached to the chassis:

```text
Robot heading changes
        ↓
Sensor beam angles relative to walls change
        ↓
Measured distances can change
```

Therefore:

```text
D_INNER changed
```

does not automatically mean:

```text
Piolín translated laterally
```

The vehicle state and previous sensor history must also be considered.

---

# 2.30 Sensor Beam Geometry

An ultrasonic sensor does not measure along an infinitely thin mathematical line.

It emits sound over a finite acoustic region.

Conceptually:

```text
              WALL
               │
               │

          \    │    /
           \   │   /
            \  │  /
             \ │ /
            SENSOR
```

The returned measurement depends on which surface produces a usable reflection within that region.

This is one reason measurements can change when:

```text
Wall orientation changes

Robot rotates

A corner opens

Another object enters the acoustic region
```

The software should therefore avoid treating every reading as perfect point geometry.

---

# 2.31 Perpendicular vs. Angled Observation

When a lateral sensor approximately faces a wall perpendicularly:

```text
SENSOR → │ WALL
```

the reading corresponds closely to the lateral separation between the sensor and the wall.

If the chassis rotates:

```text
SENSOR ↗ │ WALL
```

the acoustic path and reflected surface geometry change.

The resulting reading can increase even if the vehicle has not translated the same amount.

This explains why ultrasonic measurements and steering angle are physically coupled.

---

# 2.32 Short-Window Filtering

Autonomous steering should not react excessively to one isolated abnormal ultrasonic reading.

A short-window filter can reduce the influence of outliers.

A useful robust approach is a median calculation:

```text
D1
D2
D3
 ↓
MEDIAN
 ↓
Filtered distance
```

For example:

```text
245 mm
247 mm
710 mm
```

produces:

```text
MEDIAN = 247 mm
```

The isolated large reading does not dominate the resulting navigation value.

---

# 2.33 Median-of-Three Concept

For three readings:

```text
A, B, C
```

the median is the middle value after sorting:

```text
SORT(A, B, C)
        ↓
MIDDLE VALUE
```

A conceptual implementation is:

```python
def median3(a, b, c):
    return sorted([a, b, c])[1]
```

The advantage is that one isolated extreme sample can be rejected naturally.

This is particularly useful for distance sensors operating in a geometry containing:

```text
Edges

Openings

Angled walls

Nearby obstacles
```

---

# 2.34 Filtering Trade-Off

Filtering improves stability but also introduces a trade-off.

A larger sample window can provide:

```text
More noise rejection
```

but also:

```text
More delay
```

The relationship is:

```text
More filtering
      ↓
Smoother measurement
      ↓
Potentially slower response
```

For a moving vehicle, excessive delay can cause the software to respond to geometry that Piolín has already passed.

Therefore, short filtering windows are generally more appropriate for fast navigation than very long averaging windows.

---

# 2.35 Median vs. Mean

Consider:

```text
240
242
900
```

The arithmetic mean is:

```text
(240 + 242 + 900) / 3
=
460.7
```

which does not resemble the two consistent measurements.

The median is:

```text
242
```

For isolated extreme readings, the median can therefore better preserve the dominant local measurement.

This does not mean median filtering solves every ultrasonic problem.

Persistent incorrect readings can still pass through the filter.

---

# 2.36 Temporal Confirmation

Some important state transitions can also require confirmation over more than one sensor cycle.

Conceptually:

```text
Possible corner reading
        ↓
Read again
        ↓
Geometry still indicates corner?
        ↓
YES
        ↓
Confirm transition
```

This prevents one unusual sample from immediately changing the complete navigation state.

The number of confirmations belongs to the current software implementation and should not be inferred from older experiments.

---

# 2.37 Invalid and Extreme Readings

An ultrasonic sensor may occasionally return a reading that is:

```text
Unexpectedly large

Unexpectedly small

Inconsistent with recent geometry
```

Such a value should be interpreted in context.

An unusually large reading may represent:

```text
A real opening
```

rather than:

```text
Sensor failure
```

This is particularly important at corners.

Therefore, simple rules such as:

```text
Large reading = invalid
```

would be unsafe.

The navigation state must determine whether the value is physically plausible.

---

# 2.38 State-Dependent Interpretation

The same distance value can mean different things depending on the current state.

For example:

```text
Large D_INNER
```

during normal straight navigation may indicate:

```text
Robot too far from wall
```

but immediately at a corner it may indicate:

```text
Inner wall has ended
```

Therefore:

```text
SENSOR VALUE
      +
NAVIGATION STATE
      ↓
MEANING
```

rather than:

```text
SENSOR VALUE
      ↓
FIXED MEANING
```

This is one of the central principles of Piolín's ultrasonic architecture.

---

# 2.39 Front Safety Data

The front sensor produces:

```text
D_FRONT
```

which represents forward clearance.

A conceptual frontal safety condition can be written as:

```python
if D_FRONT < FRONT_SAFETY_LIMIT:
    frontal_risk = True
```

The exact value of:

```text
FRONT_SAFETY_LIMIT
```

must come from the current final code or calibration.

No unconfirmed threshold is assigned in this document.

The important architecture is:

```text
D_FRONT
   ↓
Safety evaluation
   ↓
Possible interruption of ordinary forward motion
```

---

# 2.40 Front Sensor Priority

Suppose the lateral controller indicates:

```text
Continue forward with small correction
```

while S1 indicates:

```text
Insufficient frontal clearance
```

The normal wall-following request should not blindly continue.

The system-level hierarchy is:

```text
FRONTAL SAFETY
      ↓
LATERAL SAFETY
      ↓
CORNER / OBSTACLE LOGIC
      ↓
NORMAL WALL FOLLOWING
```

The front sensor therefore provides an independent safety layer above ordinary track-following behavior.

---

# 2.41 Why Front Distance Is Not Used for Centering

Centering is a lateral geometry problem.

```text
LEFT WALL
     ↔
PIOLÍN
     ↔
RIGHT WALL
```

The front ultrasonic measures:

```text
PIOLÍN
   ↕
FORWARD SURFACE
```

Therefore:

```text
D_FRONT
```

does not provide the same information as:

```text
D_LEFT - D_RIGHT
```

or:

```text
D_INNER / D_OUTER
```

Using the front value inside lateral centering equations would mix independent spatial directions.

---

# 2.42 Lateral Balance Indicator

When both side walls form a suitable corridor, a simple lateral-balance indicator can be defined as:

```text
B =
D_LEFT - D_RIGHT
```

or in direction-independent form:

```text
B_IO =
D_INNER - D_OUTER
```

The sign indicates which side currently has the larger measured clearance.

However:

```text
B = 0
```

does not automatically mean the chassis center is geometrically centered because the sensor positions relative to the chassis center may differ.

Sensor offsets must be considered for exact geometric centering.

---

# 2.43 Corrected Centering Model

If final sensor offsets are available, corrected distances can be defined.

For example:

```text
D_LEFT_C =
D_LEFT + O_LEFT
```

and:

```text
D_RIGHT_C =
D_RIGHT + O_RIGHT
```

where the offsets transform sensor-face measurements toward a common reference point.

Then a corrected balance can be written as:

```text
B_C =
D_LEFT_C - D_RIGHT_C
```

and:

```text
B_C ≈ 0
```

would represent equal distance from the chosen reference point to both walls in a symmetric corridor.

Because the final offsets are not currently confirmed here, this remains a symbolic geometric model.

---

# 2.44 Center Position Estimate

Using corrected inner and outer distances:

```text
X_EST =
(W + D_INNER_C - D_OUTER_C) / 2
```

This can be derived from:

```text
D_INNER_C ≈ X
```

and:

```text
D_OUTER_C ≈ W - X
```

The estimate is most meaningful when:

```text
Both side walls are visible

Walls are approximately suitable references

Sensor geometry is known

Robot is not in an open corner transition
```

It should not be applied blindly to every navigation state.

---

# 2.45 Why Geometry Validity Matters

Suppose one wall disappears at a corner.

The equations may still produce a numerical `X_EST`.

However, that does not mean the result describes the actual vehicle position.

```text
Bad geometric assumptions
        +
Valid arithmetic
        =
Misleading result
```

Therefore, geometry-based position estimation should first ask:

```text
Is the corridor model currently valid?
```

This is one purpose of the consistency variable:

```text
G
```

---

# 2.46 Geometry Confidence

A conceptual decision structure is:

```text
Read D_INNER + D_OUTER
        ↓
Calculate G
        ↓
G compatible with corridor?
    ┌─────────┴─────────┐
   YES                  NO
    │                    │
    ▼                    ▼
Use normal          Treat as
wall geometry       transition /
                    corner /
                    special state
```

This prevents a straight-wall equation from being used after the physical geometry has changed.

---

# 2.47 Ultrasonic Data During the Open Challenge

The Open Challenge uses the ultrasonic system primarily as:

```text
S2 + S3
    ↓
Wall-following geometry


S1
    ↓
Frontal safety
```

The basic flow is:

```text
Read lateral sensors
        ↓
Assign D_INNER / D_OUTER
        ↓
Interpret current geometry
        ↓
Normal straight?
Corner entry?
Corner exit?
        ↓
Calculate steering behavior
```

while independently:

```text
Read D_FRONT
        ↓
Check frontal safety
```

---

# 2.48 Open Challenge Corner Sequence

The ultrasonic sequence can be summarized as:

```text
D_INNER valid
      ↓
Follow inner wall
      ↓
D_INNER changes as wall ends
      ↓
Corner confirmed
      ↓
Turn begins
      ↓
D_OUTER becomes useful
      ↓
Vehicle rotates
      ↓
D_INNER reacquired
      ↓
Turn ends
      ↓
Normal wall following resumes
```

This is the core reason the current Open strategy does not require a gyroscope.

---

# 2.49 Ultrasonic Data During the Obstacle Challenge

The same three ultrasonic sensors remain relevant during the Obstacle Challenge.

The HuskyLens adds:

```text
Obstacle identity
```

but does not replace:

```text
Wall geometry
```

The architecture becomes:

```text
HuskyLens
    ↓
Which side should the pillar be passed?


S2 + S3
    ↓
How much lateral clearance is available?


S1
    ↓
Is forward clearance becoming unsafe?
```

The EV3 combines these constraints into one movement decision.

---

# 2.50 Pillar Avoidance and Side Distance

Suppose the camera determines:

```text
GREEN
   ↓
Pass on LEFT
```

The requested avoidance direction still has to respect:

```text
D_LEFT
```

because steering toward the left side of the track changes wall clearance.

Similarly:

```text
RED
  ↓
Pass on RIGHT
```

must coexist with:

```text
D_RIGHT
```

This creates the relationship:

```text
PILLAR REQUIREMENT
       +
SIDE-WALL GEOMETRY
       ↓
FEASIBLE STEERING RESPONSE
```

---

# 2.51 Post-Pillar Recovery

After an obstacle is passed, the lateral ultrasonic pair becomes particularly important.

The robot may be:

```text
Laterally displaced

Angled relative to walls

Closer to one boundary
```

The recovery process can use:

```text
D_LEFT

D_RIGHT
```

to re-establish a useful normal trajectory.

Conceptually:

```text
Pillar cleared
      ↓
Vision steering reduced
      ↓
Lateral geometry evaluated
      ↓
Recovery steering
      ↓
Normal wall following restored
```

---

# 2.52 Position vs. Heading After an Obstacle

After an obstacle, equal side distances alone do not prove that Piolín is correctly oriented.

For example:

```text
LEFT distance ≈ RIGHT distance
```

can occur momentarily while the chassis is still angled.

The next measurements may then diverge quickly.

Therefore, recovery should consider:

```text
Current distances

Change in distances over time

Vehicle movement

Navigation state
```

rather than relying on one static equality condition.

---

# 2.53 Distance Derivative Concept

The change in a distance measurement over time can provide additional information.

For one sensor:

```text
DELTA_D =
D_CURRENT - D_PREVIOUS
```

and approximately:

```text
RATE_D =
DELTA_D / DELTA_T
```

If:

```text
D_LEFT
```

is decreasing rapidly, Piolín may be approaching the left wall.

If it changes only slightly, the geometry may be relatively stable.

This derivative concept can support diagnostics or advanced control, although the active implementation should be verified from current software before claiming a specific derivative controller.

---

# 2.54 Two-Sensor Trend Interpretation

The two lateral distances can also be compared over time.

For example:

```text
D_LEFT decreases

D_RIGHT increases
```

is consistent with movement toward the left side in a stable corridor.

If both:

```text
D_LEFT increases

D_RIGHT increases
```

significantly, the vehicle may be entering:

```text
An opening

A corner

A geometry transition
```

depending on track orientation.

This illustrates why using both lateral sensors provides richer information than a single distance reading.

---

# 2.55 Ultrasonic Data and Vehicle Rotation

If Piolín rotates inside a corridor:

```text
Front of robot changes orientation
        ↓
Left and right acoustic paths change
```

The readings can therefore show a pattern different from simple lateral translation.

The software does not attempt to turn the ultrasonic pair into a perfect gyroscope.

Instead, the readings are interpreted relative to:

```text
Known track state

Previous readings

Steering state

Expected geometry
```

This maintains the current environment-relative navigation philosophy.

---

# 2.56 No Gyroscope in Current Geometry

The current Piolín ultrasonic strategy does not use:

```text
GYRO HEADING
```

to validate every corner.

Instead:

```text
Physical track geometry
        ↓
Ultrasonic transitions
        ↓
Navigation state
```

provides the primary spatial reference.

The previous gyroscope architecture is documented only as historical development:

[Legacy Gyroscope Navigation](../legacy/01_GConfig.md)

---

# 2.57 Sensor Height and Geometry

The confirmed lateral mounting height is approximately:

```text
43.2 mm
```

This height defines the horizontal region of the wall observed by the lateral sensors.

If the sensors were mounted significantly lower or higher, they could interact differently with:

```text
Track structures

Wall edges

Nearby objects
```

The mounting dimension is therefore part of the sensing geometry, not merely a mechanical detail.

---

# 2.58 Sensor Orientation Stability

A physically loose ultrasonic sensor can create an apparent data problem.

For example:

```text
Sensor rotates slightly
        ↓
Acoustic beam observes
different region of wall
        ↓
Distance changes
        ↓
Controller reacts
```

even though the vehicle center has not changed significantly.

This produces the failure chain:

```text
MECHANICAL MOUNT ERROR
        ↓
SENSOR DATA ERROR
        ↓
CONTROL ERROR
```

For this reason, sensor-mount integrity is checked as part of mechanical testing.

[Mechanical Testing](../mobility_mechanical/06_testing.md)

---

# 2.59 Data Plausibility

A useful sensor-processing architecture distinguishes between:

```text
Possible measurement
```

and:

```text
Plausible measurement for the current state
```

For example, a large inner reading may be physically valid at a corner but unexpected in the middle of a long straight.

A plausibility layer can therefore consider:

```text
Current state

Previous value

Opposite sensor

Vehicle motion
```

before treating a reading as a steering error.

---

# 2.60 Avoiding Hard Rejection of Real Geometry

An important design risk is rejecting unusual values too aggressively.

Suppose the code assumes:

```text
Any large distance = sensor error
```

At a real corner:

```text
Wall disappears
        ↓
Large distance is physically correct
```

Rejecting it could prevent the robot from recognizing the corner.

Therefore, filtering should primarily reject:

```text
Isolated inconsistent samples
```

rather than suppressing every measurement outside the normal straight-wall range.

---

# 2.61 Filter Then Interpret

The intended processing order is conceptually:

```text
RAW SENSOR DATA
       ↓
SHORT FILTERING
       ↓
PHYSICAL SENSOR VALUES
       ↓
DIRECTION MAPPING
       ↓
D_INNER / D_OUTER
       ↓
GEOMETRY INTERPRETATION
       ↓
NAVIGATION STATE
       ↓
STEERING DECISION
```

Frontal safety remains parallel:

```text
D_FRONT
   ↓
Safety interpretation
```

This keeps filtering separate from high-level navigation meaning.

---

# 2.62 Recommended Variable Structure

A clear internal data model can use:

```python
D_FRONT = ...
D_LEFT = ...
D_RIGHT = ...

if direction == COUNTERCLOCKWISE:
    D_INNER = D_LEFT
    D_OUTER = D_RIGHT

elif direction == CLOCKWISE:
    D_INNER = D_RIGHT
    D_OUTER = D_LEFT
```

Then:

```python
wall_error = D_TARGET - D_INNER

geometry_error = abs(
    (D_INNER + D_OUTER) - C_REF
)
```

This structure separates:

```text
Physical sensor acquisition

Direction assignment

Navigation calculations
```

which improves readability and debugging.

The actual competition code may use different variable names, but the engineering architecture remains the same.

---

# 2.63 Data Logging

During development, ultrasonic data is most useful when recorded together with context.

A meaningful diagnostic line might conceptually contain:

```text
STATE
D_FRONT
D_LEFT
D_RIGHT
D_INNER
D_OUTER
STEERING
DIRECTION
```

For example:

```text
STRAIGHT  F:420  L:250  R:600  IN:250  OUT:600
```

The numerical example above is illustrative only.

The important principle is that one distance value without context is much harder to interpret than a complete navigation snapshot.

---

# 2.64 Why Both Raw and Logical Values Are Useful

During debugging:

```text
D_LEFT

D_RIGHT
```

show whether the physical sensors are functioning as expected.

Meanwhile:

```text
D_INNER

D_OUTER
```

show whether the direction mapping is correct.

If:

```text
Physical readings correct
```

but:

```text
Inner / outer interpretation incorrect
```

the problem is likely software mapping rather than sensor hardware.

This makes the dual naming structure valuable for diagnostics.

---

# 2.65 Direction-Mapping Failure Example

Suppose Piolín is moving clockwise.

Correct mapping:

```text
RIGHT = INNER

LEFT = OUTER
```

If the program accidentally assigns:

```text
LEFT = INNER
```

then a perfectly correct left ultrasonic measurement could generate the wrong steering behavior.

The failure chain becomes:

```text
Sensor works correctly
        ↓
Software labels it incorrectly
        ↓
Wrong wall error
        ↓
Wrong steering
```

This is why direction mapping should be explicit and easy to inspect.

---

# 2.66 Sensor Data and Steering

The lateral ultrasonic sensors do not physically steer Piolín.

The complete chain is:

```text
WALL
 ↓
ULTRASONIC SENSOR
 ↓
DISTANCE DATA
 ↓
LEGO EV3
 ↓
CONTROL CALCULATION
 ↓
Motor B
 ↓
ACKERMANN STEERING
```

This distinction separates:

```text
PERCEPTION
```

from:

```text
ACTUATION
```

The same sensor data could theoretically support different steering strategies without modifying the physical sensor hardware.

---

# 2.67 Sensor Data and Drive Speed

Drive speed changes how quickly the sensor geometry evolves.

At higher speed:

```text
Piolín travels farther
between equivalent processing intervals
```

therefore:

```text
Wall changes arrive faster

Corners approach faster

Safety distance closes faster
```

The sensing system and drivetrain are therefore dynamically linked.

```text
HIGHER SPEED
      ↓
LESS AVAILABLE RESPONSE TIME
```

This is one reason sensor tuning cannot be evaluated independently from vehicle speed.

---

# 2.68 Sensor Data During Reverse Motion

When Piolín reverses, the lateral sensors remain physically directed left and right.

Therefore:

```text
D_LEFT

D_RIGHT
```

remain valid side measurements.

However, the relationship between:

```text
steering direction
```

and:

```text
future vehicle trajectory
```

changes because velocity is reversed.

The sensor hardware does not change.

The navigation interpretation must account for the current movement state.

---

# 2.69 Failure Modes

Common ultrasonic data problems can be grouped into several categories.

| Failure Type | Possible Effect |
| :--- | :--- |
| **Isolated outlier** | Sudden false steering correction |
| **Wall opening** | Large reading that is actually valid |
| **Angled observation** | Distance differs from simple lateral separation |
| **Loose mount** | Persistent geometry error |
| **Direction mapping error** | Inner and outer roles reversed |
| **Excessive filtering** | Delayed corner response |
| **No filtering** | Sensitivity to isolated noise |
| **Incorrect units** | Wrong thresholds and control values |
| **Using S1 in lateral equations** | Invalid geometry model |

The correct response depends on the cause.

---

# 2.70 Diagnostic Hierarchy

If ultrasonic-based navigation behaves incorrectly, the investigation should proceed in order:

```text
1. Verify physical ports
        ↓
2. Verify sensor orientation
        ↓
3. Read raw S1/S2/S3 values
        ↓
4. Verify units
        ↓
5. Verify LEFT / RIGHT assignment
        ↓
6. Verify INNER / OUTER mapping
        ↓
7. Verify filtering
        ↓
8. Verify geometry state
        ↓
9. Verify steering calculation
```

This prevents immediately changing steering gains when the real issue is a sensor or mapping problem.

---

# 2.71 Current vs. Legacy Ultrasonic Data

Previous Piolín versions used different ultrasonic layouts and development geometry.

Historical documentation may contain:

```text
Different sensor orientations

Only two ultrasonic sensors

Gyroscope on S1

Development wall references

Previous sensor offsets

Alternative geometry constants
```

Those values should not be transferred automatically into the final system.

The current configuration is:

```text
S1 → Front Ultrasonic

S2 → Right Ultrasonic

S3 → Left Ultrasonic
```

with:

```text
S2 + S3
=
Lateral navigation
```

and:

```text
S1
=
Independent frontal safety
```

Historical systems are preserved in:

[Legacy Documentation](../legacy/00_LEGACY_NOTICE.md)

---

# 2.72 Confirmed Current Ultrasonic Information

The following information is confirmed for the current Piolín architecture:

| Parameter | Current Value |
| :--- | :--- |
| **Number of ultrasonic sensors** | 3 |
| **S1** | Front Ultrasonic |
| **S2** | Right Ultrasonic |
| **S3** | Left Ultrasonic |
| **Lateral sensor orientation** | Direct lateral |
| **Lateral sensor mounting height** | ~43.2 mm |
| **Primary wall-navigation sensors** | S2 + S3 |
| **Frontal safety sensor** | S1 |
| **Gyroscope** | Not installed |

The following values are intentionally not assigned as final numerical specifications here:

```text
Current D_TARGET

Current C_REF

Geometry tolerance

Front safety threshold

Final lateral sensor offsets

Final corridor width model

Final confirmation count

Final filter window implementation
```

These values should come from the current software or calibration process when confirmed.

---

# 2.73 Data Responsibility Matrix

| Variable / Information | Source | Primary Use |
| :--- | :--- | :--- |
| **D_FRONT** | S1 | Frontal safety |
| **D_RIGHT** | S2 | Physical right-wall distance |
| **D_LEFT** | S3 | Physical left-wall distance |
| **D_INNER** | S2 or S3 | Primary wall-following reference |
| **D_OUTER** | S2 or S3 | Secondary geometry / corner reference |
| **E_WALL** | Derived | Normal steering error |
| **G** | Derived | Corridor-geometry consistency |
| **X_EST** | Derived from corrected geometry | Lateral-position estimate when geometry is valid |

This hierarchy shows the transformation from:

```text
RAW MEASUREMENT
```

to:

```text
NAVIGATION INFORMATION
```

---

# 2.74 Complete Ultrasonic Data Pipeline

The current design can be summarized as:

```text
                         TRACK
                           │
            ┌──────────────┼──────────────┐
            ▼              ▼              ▼
         FRONT           LEFT           RIGHT
            │              │              │
            ▼              ▼              ▼
           S1             S3             S2
            │              │              │
            ▼              ▼              ▼
        D_FRONT         D_LEFT         D_RIGHT
            │              │              │
            │              └──────┬───────┘
            │                     ▼
            │              DIRECTION MAPPING
            │                     ↓
            │            D_INNER + D_OUTER
            │                     ↓
            │         FILTER / GEOMETRY CHECK
            │                     ↓
            │       ┌─────────────┴─────────────┐
            │       ▼                           ▼
            │   WALL ERROR                 STATE CHANGE
            │       │                           │
            │       └─────────────┬─────────────┘
            │                     ▼
            │                  LEGO EV3
            │                     ▲
            └──── SAFETY ─────────┘
                                  │
                                  ▼
                           FINAL CONTROL
                                  │
                          ┌───────┴───────┐
                          ▼               ▼
                       Motor A         Motor B
```

This pipeline preserves the separation between:

```text
FRONTAL SAFETY
```

and:

```text
LATERAL NAVIGATION
```

while allowing both systems to influence the final vehicle behavior.

---

# 2.75 Engineering Significance

The three-ultrasonic architecture gives Piolín a compact but useful spatial model.

It does not attempt to reconstruct the complete environment in three dimensions.

Instead, it measures the three directions most relevant to the vehicle:

```text
LEFT

FRONT

RIGHT
```

The lateral pair provides enough information to reason about:

```text
Wall distance

Lateral displacement

Corner openings

Wall reacquisition

Post-obstacle recovery
```

while the front sensor adds:

```text
Independent frontal clearance
```

The architecture is therefore based on **specialized sensor roles rather than one universal distance calculation**.

---

# 2.76 Final Ultrasonic Geometry Summary

Piolín's current ultrasonic system is:

```text
                         S1
                         ↑
                         │
                         │

                S3 ← [ PIOLÍN ] → S2
```

with:

```text
S1
=
Front safety


S2
=
Physical right sensor


S3
=
Physical left sensor
```

After course direction is established:

```text
CLOCKWISE

D_INNER = D_RIGHT
D_OUTER = D_LEFT
```

and:

```text
COUNTERCLOCKWISE

D_INNER = D_LEFT
D_OUTER = D_RIGHT
```

Normal wall following uses:

```text
E_WALL =
D_TARGET - D_INNER
```

while lateral geometry consistency can be represented by:

```text
G =
ABS(
(D_INNER + D_OUTER)
-
C_REF
)
```

and, when both measurements have been corrected to a common vehicle reference and the corridor model is valid:

```text
X_EST =
(W + D_INNER_C - D_OUTER_C) / 2
```

These equations represent different levels of information:

```text
D_INNER
     ↓
Primary wall relationship


D_OUTER
     ↓
Secondary geometry


E_WALL
     ↓
Steering error


G
     ↓
Geometry confidence


X_EST
     ↓
Possible center-referenced position estimate
```

The front sensor remains independent:

```text
D_FRONT
     ↓
Frontal safety
```

The resulting architecture allows Piolín to navigate using the physical geometry of the WRO track without requiring a gyroscope:

```text
STRAIGHT WALL
      ↓
FOLLOW


INNER WALL LOST
      ↓
CORNER


OUTER GEOMETRY
      ↓
TURN SUPPORT


INNER WALL REACQUIRED
      ↓
EXIT


SIDE DISTANCES AFTER PILLAR
      ↓
RECOVERY


FRONT DISTANCE
      ↓
SAFETY
```

This combination of lateral geometry, state-dependent interpretation, short-window noise rejection, and independent frontal ranging forms the core of Piolín's current ultrasonic navigation system.

---

## Continue Reading

[Color Sensor Configuration](03_color_sensor.md)

[HuskyLens Vision System](04_huskylens.md)

[Sensor Calibration](05_Calibration.md)

---

## Related Hardware Documentation

[Ultrasonic Sensors](../components/05_UltrasonicSensors.md)

[Hardware Overview](../components/01_Hardwareoverview.md)

---

## Related Mechanical Documentation

[Chassis Design](../mobility_mechanical/02_chassis.md)

[Robot Mobility](../mobility_mechanical/03_RMobility.md)

[Steering System](../mobility_mechanical/04_steering.md)

[Mechanical Testing](../mobility_mechanical/06_testing.md)

---

## Related Navigation Documentation

[Software Architecture](../software_obstacles_strategy/01_SWArchitecture.md)

[Wall Following](../software_obstacles_strategy/03_wallfollowing.md)

[Corner Handling](../software_obstacles_strategy/04_cornerhandling.md)

[Obstacle Strategy](../software_obstacles_strategy/06_obstaclestrateg.md)

---

## Reproducibility

[Wiring](../reproducibility/03_wiring.md)

[Calibration Procedure](../reproducibility/06_HowToCalibrate.md)

[Testing Protocol](../reproducibility/07_TestingProtocol.md)

[Troubleshooting](../reproducibility/08_Troubleshooting.md)

---

## Historical Reference

[Legacy Documentation Notice](../legacy/00_LEGACY_NOTICE.md)

[Legacy Gyroscope Configuration](../legacy/01_GConfig.md)

[Legacy Performance Testing and Analysis](../legacy/03_PTesting&Analysis.md)
