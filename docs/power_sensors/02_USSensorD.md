# 2. Ultrasonic Distance Sensing

<div align="center">

<img
  src="../../v-photos/v4/ultrasonic_pair_top.jpg"
  alt="Top view of Piolín's two lateral EV3 Ultrasonic Sensors"
  width="720"
/>

<br>

<sub><b>Figure 2.1.</b> Piolín uses two permanently installed lateral EV3 Ultrasonic Sensors to observe the left and right boundaries of the track.</sub>

</div>

Piolín uses **two LEGO Mindstorms EV3 Ultrasonic Sensors** as permanent lateral distance sensors. Their primary purpose is to provide the EV3 with geometric information about the track boundaries surrounding the vehicle.

The current physical and electrical mapping is fixed:

```text
S2 = LEFT Ultrasonic Sensor

S3 = RIGHT Ultrasonic Sensor
```

This mapping remains unchanged in both the **Open Challenge** and the **Obstacle Challenge**.

The sensors are mounted laterally rather than facing forward or diagonally. Their role is therefore not simply to answer:

```text
"Is something directly in front of the robot?"
```

Instead, they help answer:

```text
How far is Piolín from the left boundary?

How far is Piolín from the right boundary?

Is the vehicle becoming too close to a wall?

Has the surrounding geometry changed?

Is the robot recovering toward a usable corridor after a maneuver?
```

The ultrasonic subsystem is one of the few sensing systems that remains completely unchanged between both competition rounds.

---

## 2.1 Permanent Left/Right Mapping

<div align="center">

<img
  src="../../v-photos/v4/PiolinUSlabeling.png"
  alt="Piolín ultrasonic sensor labeling showing S2 left and S3 right"
  width="720"
/>

<br>

<sub><b>Figure 2.2.</b> Permanent physical mapping of Piolín's ultrasonic sensors: S2 LEFT and S3 RIGHT.</sub>

</div>

The most important convention in Piolín's ultrasonic architecture is:

```text
S2
→ physical LEFT side


S3
→ physical RIGHT side
```

These identities do not change according to the direction of travel.

This is intentionally different from navigation concepts such as:

```text
INNER

OUTER
```

because those roles depend on course direction.

The hardware remains physically stable while the software changes only the logical interpretation.

---

# 2.2 Left Ultrasonic Sensor — S2

<div align="center">

<img
  src="../../v-photos/v4/ultrasonic_left_s2.jpg"
  alt="Piolín left EV3 Ultrasonic Sensor connected to S2"
  width="660"
/>

<br>

<sub><b>Figure 2.3.</b> Left lateral ultrasonic sensor permanently assigned to EV3 Sensor Port S2.</sub>

</div>

The S2 Ultrasonic Sensor observes the environment on the **left side of Piolín**.

Its information can contribute to:

```text
left-wall distance

left-side safety

corridor position

inner-wall control in counterclockwise Open driving

outer-wall context in clockwise Open driving

post-obstacle recovery
```

The sensor remains physically left even when its logical role changes.

This distinction helps keep:

```text
hardware

software

documentation

diagnostics
```

consistent.

---

# 2.3 Right Ultrasonic Sensor — S3

<div align="center">

<img
  src="../../v-photos/v4/ultrasonic_right_s3.jpg"
  alt="Piolín right EV3 Ultrasonic Sensor connected to S3"
  width="660"
/>

<br>

<sub><b>Figure 2.4.</b> Right lateral ultrasonic sensor permanently assigned to EV3 Sensor Port S3.</sub>

</div>

The S3 Ultrasonic Sensor observes the **right side of the vehicle**.

Its information can contribute to:

```text
right-wall distance

right-side safety

corridor position

inner-wall control in clockwise Open driving

outer-wall context in counterclockwise Open driving

post-obstacle recovery
```

The software should never redefine S3 as physically left because of course direction.

Only its navigation role changes.

---

# 2.4 Lateral Orientation

<div align="center">

<img
  src="../../v-photos/v4/ultrasonic_lateral_alignment.jpg"
  alt="Piolín ultrasonic sensors aligned laterally with the vehicle"
  width="700"
/>

<br>

<sub><b>Figure 2.5.</b> The current sensors are aligned laterally rather than facing forward or diagonally.</sub>

</div>

The current sensor arrangement was selected to make the two sensors useful as **track-geometry references**.

The intended observation is approximately:

```text
LEFT WALL
    │
    │  ← S2
 [ PIOLÍN ]
             S3 →
                   │
                   │
              RIGHT WALL
```

This configuration provides information from both sides of the corridor.

Earlier Piolín versions experimented with different ultrasonic arrangements, including configurations involving frontal or differently oriented sensors. Those are not part of the current V4 architecture.

---

# 2.5 Why Two Lateral Sensors Are Useful

A single lateral sensor can describe the distance to one boundary.

Two lateral sensors provide a richer geometric picture.

For example, consider two situations:

```text
CASE A

Left distance normal
Right distance normal
```

and:

```text
CASE B

Left distance small
Right distance large
```

The second pattern suggests a different vehicle position relative to the corridor.

The pair can therefore help the controller reason about:

```text
lateral position

clearance

wall proximity

recovery direction
```

more effectively than relying on only one side.

---

## 2.6 Two Sensors Do Not Directly Give Global Position

Although two side distances provide useful geometric information, they do not directly produce a complete global coordinate of the robot.

A measurement depends on:

```text
vehicle position

vehicle orientation

wall orientation

sensor orientation

surface geometry
```

Therefore:

```text
S2 + S3
```

should not automatically be interpreted as a perfect world-position system.

They are local geometric references.

This distinction is especially important during corners and obstacle maneuvers.

---

# 2.7 Ultrasonic Measurement Principle

An ultrasonic sensor estimates distance by transmitting an acoustic pulse and measuring the return from a surface.

Conceptually:

```text
sensor emits ultrasonic pulse
          ↓
pulse travels through air
          ↓
pulse reaches surface
          ↓
echo returns
          ↓
sensor estimates distance
```

The fundamental time-of-flight idea can be represented as:

```text
distance ≈
(speed of sound × round-trip time) / 2
```

The division by two accounts for the sound traveling:

```text
sensor → wall
```

and then:

```text
wall → sensor
```

Piolín does not calculate this acoustic timing manually in its navigation software; the EV3 Ultrasonic Sensor provides the resulting distance measurement.

---

# 2.8 Sensor Reading vs. Vehicle Distance

The value returned by an ultrasonic sensor corresponds to the distance measured from the sensor's own physical location.

It is not automatically the distance from:

```text
vehicle center
```

or:

```text
wheel centerline
```

For example:

```text
WALL
 │
 │<------ D_SENSOR ------>[SENSOR]--- offset ---[ROBOT CENTER]
```

If a controller needs a geometric distance from the vehicle centerline, the sensor's mounting offset must also be considered.

This is why physical sensor placement is part of calibration.

---

# 2.9 Sensor Mounting

<div align="center">

<img
  src="../../v-photos/v4/ultrasonic_mount_closeup.jpg"
  alt="Close-up of Piolín ultrasonic sensor mounting"
  width="660"
/>

<br>

<sub><b>Figure 2.6.</b> Mechanical mounting preserves the sensor orientation relative to the chassis.</sub>

</div>

The ultrasonic sensors must remain mechanically stable because a change in their orientation changes what surface the acoustic beam encounters.

The mount should preserve:

```text
sensor direction

sensor height

left/right identity

position relative to chassis
```

A sensor that rotates slightly can produce different measurements from the same vehicle position.

Therefore:

```text
changed ultrasonic behavior
```

should first trigger a check of:

```text
physical sensor mounting
```

before control values are changed.

---

# 2.10 Sensor Geometry and Vehicle Yaw

One of the most important limitations of side-facing ultrasonic sensing is that the reading depends on vehicle orientation.

Imagine Piolín approximately parallel to a wall.

```text
WALL
│
│
│      [ SENSOR → ]
│      [ PIOLÍN   ]
│
```

The lateral distance is relatively intuitive.

If Piolín rotates:

```text
WALL
│
│
│        / PIOLÍN
│       /
│
```

the sensor beam can interact with the wall differently.

Therefore:

```text
distance changed
```

does not always mean:

```text
Piolín translated sideways by the same amount
```

Part of the change may come from yaw.

This is one reason the Open Challenge combines ultrasonic geometry with a gyro.

---

# 2.11 Open Challenge Role

During the Open Challenge, the ultrasonic sensors provide the primary **lateral geometry** references.

The active sensor architecture is:

```text
S1
→ Gyro

S2
→ Left Ultrasonic

S3
→ Right Ultrasonic

S4
→ Color Sensor
```

The division of sensing responsibilities is:

```text
S2/S3
→ track-relative lateral geometry


Gyro
→ orientation / heading


Color
→ course-state landmarks
```

The ultrasonic sensors therefore do not need to solve heading estimation alone.

---

# 2.12 Heading vs. Lateral Position

The distinction between heading and lateral position is important.

Consider two cases.

### Case A

```text
Piolín has acceptable wall distance
but is rotated.
```

### Case B

```text
Piolín has correct heading
but is too close to a wall.
```

These states require different corrections.

Ultrasonics are especially useful for Case B.

The gyro is especially useful for Case A.

By combining the two, the EV3 has more information about the actual vehicle state.

---

# 2.13 Counterclockwise Inner/Outer Mapping

During counterclockwise Open driving:

```text
LEFT
→ inner side

RIGHT
→ outer side
```

therefore:

```text
S2 LEFT
→ INNER


S3 RIGHT
→ OUTER
```

The physical sensor ports remain unchanged.

The software simply assigns the logical roles after the initial course direction has been determined.

---

# 2.14 Clockwise Inner/Outer Mapping

During clockwise Open driving:

```text
RIGHT
→ inner side

LEFT
→ outer side
```

therefore:

```text
S3 RIGHT
→ INNER


S2 LEFT
→ OUTER
```

Again:

```text
S2 is still LEFT

S3 is still RIGHT
```

Only the navigation interpretation changes.

This design prevents hardware rewiring or mirrored port conventions from being required between directions.

---

# 2.15 Why Inner and Outer Distances Matter

The Open course contains a corridor-like geometry between inner and outer boundaries.

The robot can use that geometry to avoid two undesirable conditions:

```text
too close to inner wall
```

and:

```text
too close to outer wall
```

The controller can therefore maintain a useful operating region rather than following one boundary blindly.

The exact preferred distance is a calibration parameter and should not be treated as an immutable physical constant.

The current code may contain a working target, but final documentation should distinguish:

```text
current tuning value
```

from:

```text
final validated geometric specification
```

until testing is complete.

---

# 2.16 Wall Following Is Not Only One Distance Target

A simplistic wall controller could be:

```text
error =
target distance - measured distance
```

followed by one steering correction.

Piolín's actual geometric problem is more complex because it must also consider:

```text
vehicle orientation

opposite wall

corner geometry

safety limits

vehicle speed
```

Therefore the ultrasonic system should be understood as a source of geometric information rather than a single fixed wall-following variable.

---

# 2.17 Gentle Corrections

During stable straight driving, the preferred behavior is:

```text
small geometric error
→ small steering correction
```

rather than:

```text
small error
→ aggressive full steering
```

Strong corrections can produce:

```text
left correction
      ↓
overshoot
      ↓
right correction
      ↓
overshoot
      ↓
zig-zag
```

The sensors themselves may be providing correct information while the steering response is too aggressive.

This is why sensor evaluation and controller evaluation should remain separate.

---

# 2.18 Wall Safety

The ultrasonic measurements also provide a safety role.

If a wall becomes significantly closer than the normal operating range, the EV3 can apply a stronger protective response than it would for a small tracking error.

This creates two conceptual levels:

```text
NORMAL GEOMETRY CONTROL
→ gentle correction
```

and:

```text
WALL SAFETY
→ stronger intervention
```

The exact thresholds should come from measured testing rather than arbitrary values.

---

# 2.19 Why Safety and Normal Control Should Be Different

Suppose Piolín is only slightly closer to a wall than desired.

A strong emergency steering action would be unnecessary.

Conversely, if the vehicle is approaching a collision condition, a very weak proportional correction may be insufficient.

Therefore:

```text
normal deviation
```

and:

```text
collision-risk deviation
```

should not necessarily produce the same type of steering response.

The ultrasonic system provides the distance information needed to distinguish those states.

---

# 2.20 Corner Detection Through Geometry Change

Ultrasonic measurements can also help identify transitions between straights and corners.

During a stable straight:

```text
wall geometry
→ relatively consistent
```

As Piolín approaches or enters a corner:

```text
distance relationships can change rapidly
```

The important principle is that one isolated measurement should not automatically be interpreted as:

```text
corner detected
```

because temporary measurement variation can occur.

A stronger corner interpretation can combine:

```text
course progress

ultrasonic geometry change

gyro rotation
```

during Open.

---

# 2.21 Sensor Behavior During a Corner

During a turn, the lateral sensor assumptions change.

The robot rotates relative to the walls, so:

```text
sensor beam orientation
```

also changes relative to the track.

Therefore the same wall-following calculation used on a straight may not remain appropriate throughout the entire corner.

A useful architecture treats the corner as a separate vehicle state:

```text
STRAIGHT
      ↓
CORNER ENTRY
      ↓
TURNING
      ↓
CORNER EXIT
      ↓
STRAIGHT
```

During the turn, the gyro and vehicle state can have greater importance.

Afterward, the ultrasonic geometry can be reacquired.

---

# 2.22 Reacquiring the Wall After a Corner

A corner should not be considered complete only because the vehicle has rotated.

The lateral sensors should also return to a geometry that is useful for the next straight.

The process can be represented as:

```text
turn
  ↓
new heading reached
  ↓
lateral walls become measurable again
  ↓
S2/S3 geometry becomes valid
  ↓
normal correction resumes
```

This prevents the controller from immediately applying a large wall correction based on transitional corner measurements.

---

# 2.23 Obstacle Challenge Role

During Obstacles, the ultrasonic sensors remain:

```text
S2 LEFT

S3 RIGHT
```

but the specialized S1 device changes:

```text
S1
→ Pixy2.1
```

The ultrasonic sensors no longer work with the gyro because the gyro is not installed.

Instead, they complement visual perception.

```text
Pixy
→ what obstacle is visible?
→ where does it appear visually?


Ultrasonics
→ what lateral physical geometry surrounds Piolín?
```

This division is central to the current Obstacle Challenge strategy.

---

# 2.24 Why Pixy Cannot Replace Ultrasonic Distance Sensing

Pixy2.1 provides visual information such as:

```text
signature

x

y

width

height
```

These values are useful for identifying and locating a visual target inside the camera image.

They do not automatically provide the same information as:

```text
physical left-wall distance

physical right-wall distance
```

without a much more complex calibrated camera model.

The ultrasonic sensors therefore remain the simpler and more direct reference for lateral track boundaries.

---

# 2.25 Why Ultrasonics Cannot Replace Pixy

The opposite limitation also exists.

An ultrasonic sensor can detect that an object or wall is nearby.

It cannot reliably answer:

```text
Is this pillar RED?

Is this pillar GREEN?
```

The obstacle rule depends directly on that distinction.

Therefore:

```text
ultrasonics only
```

would not provide enough information for the full Obstacle Challenge strategy.

The two sensing systems are complementary.

---

# 2.26 Obstacle Maneuver Geometry

During a pillar pass, Piolín creates a temporary lateral trajectory.

For Red:

```text
RED
→ pass RIGHT
```

For Green:

```text
GREEN
→ pass LEFT
```

While that maneuver is occurring, the ultrasonic sensors can help monitor whether the robot is also approaching a track wall.

The EV3 therefore has to balance:

```text
pillar avoidance objective
```

with:

```text
boundary safety
```

The wall controller should assist the maneuver without overpowering the required obstacle direction.

---

# 2.27 Pillar Passing and Lateral Sensing

A lateral sensor can also observe a geometric change as Piolín moves beside and then beyond an obstacle.

Conceptually:

```text
approach pillar
      ↓
lateral geometry changes
      ↓
vehicle moves beside pillar
      ↓
geometry changes again
      ↓
space opens after pillar
```

This sequence can provide additional evidence that the obstacle has actually been passed.

It is more reliable than assuming:

```text
Pixy lost target
→ pillar passed
```

because the camera can lose a target simply because steering moved it outside the field of view.

---

# 2.28 Pass Confirmation

The intended obstacle-state logic can combine:

```text
Pixy target state
+
vehicle motion
+
ultrasonic geometry
```

before releasing the current obstacle.

A conceptual process is:

```text
pillar selected
      ↓
avoidance begins
      ↓
lateral sensor observes changing geometry
      ↓
vehicle continues past obstacle
      ↓
distance opens / wall geometry returns
      ↓
pillar considered cleared
```

The final numerical completion conditions remain under development.

---

# 2.29 Post-Obstacle Recovery

After an obstacle pass, the ultrasonic sensors become especially important.

The desired transition is:

```text
PIXY-INFLUENCED AVOIDANCE
          ↓
COUNTERSTEERING
          ↓
S2/S3 GEOMETRY RECOVERY
          ↓
NORMAL COURSE CONTROL
```

Once the pillar no longer requires the dominant steering objective, the lateral wall geometry can help Piolín return toward a useful path for the next obstacle or corner.

---

# 2.30 Why Immediate Recentering Can Be Dangerous

Recentering should not begin merely because the camera no longer sees the pillar.

If the pillar has only moved outside the camera field of view:

```text
immediate recenter
```

could steer Piolín back toward the obstacle.

A stronger recovery condition should therefore consider:

```text
visual target state

lateral geometry

vehicle motion history
```

before the normal corridor controller becomes dominant again.

---

# 2.31 Ultrasonic Beam Limitations

An ultrasonic sensor does not measure one infinitely thin ray.

It transmits acoustic energy across a region.

This means a return can be affected by:

```text
surface angle

nearby geometry

edges

corners

multiple surfaces

partial reflections
```

A wall that is not perpendicular to the effective beam may produce a different measurement from a flat surface in ideal alignment.

This is another reason Piolín avoids interpreting one isolated reading as perfect geometric truth.

---

# 2.32 Corners and Surface Edges

Corners are particularly challenging because the sensor can transition between:

```text
one wall surface

open space

another wall surface
```

over a short vehicle displacement.

This can create a rapid distance change even though the sensor is operating normally.

Such changes can be useful for detecting geometry transitions, but only if the controller understands the current course state.

---

# 2.33 Outliers

Distance measurements can occasionally differ significantly from surrounding readings.

A robust controller should therefore distinguish:

```text
persistent geometric change
```

from:

```text
single unexpected sample
```

Possible strategies include:

```text
short temporal confirmation

plausibility checks

limited correction magnitude

comparison with previous reading
```

The correct approach depends on the speed and reaction requirements.

Excessive filtering can make the controller react too slowly.

---

# 2.34 Filtering Trade-Off

Sensor filtering introduces an important trade-off.

More filtering can provide:

```text
smoother signal

less reaction to isolated noise
```

but also:

```text
greater delay
```

Less filtering provides:

```text
faster response
```

but also:

```text
greater sensitivity to measurement variation
```

At competition speed, delay corresponds to physical travel distance.

Therefore the best filter is not necessarily the smoothest one.

It is the one that preserves enough stability without making Piolín react too late.

---

# 2.35 Sensor Update and Vehicle Motion

Every sensor measurement occurs while the vehicle may be moving.

The complete control process is:

```text
read S2/S3
      ↓
EV3 interprets geometry
      ↓
EV3 calculates steering
      ↓
Motor B responds
      ↓
Motor A continues moving Piolín
      ↓
new measurement
```

At higher speed, the robot travels farther between equivalent control decisions.

This means:

```text
same sensor logic
+
higher speed
```

may produce different physical results.

Ultrasonic tuning must therefore be tested at representative driving speed.

---

# 2.36 Static Calibration vs. Dynamic Calibration

A static sensor test can verify whether the ultrasonic sensor returns plausible distances when Piolín is stationary.

However, the final navigation system operates while:

```text
moving

turning

accelerating

passing obstacles
```

A complete calibration should therefore include both:

```text
STATIC TESTS
```

and:

```text
DYNAMIC TESTS
```

Static testing helps characterize the sensor.

Dynamic testing validates whether the measurements are useful in the actual control loop.

---

# 2.37 Static Distance Test

A useful basic test places Piolín at several known wall distances and records the ultrasonic readings.

For example:

| Trial | Physical Reference Distance | S2 Reading | S3 Reading | Notes |
| :---: | :---: | :---: | :---: | :--- |
| 1 | — | — | — | — |
| 2 | — | — | — | — |
| 3 | — | — | — | — |
| 4 | — | — | — | — |

The values should be measured using the current V4 sensor mounts.

No calibration table should be populated with estimated numbers.

---

# 2.38 Repeatability Test

At one fixed physical position, the team can collect multiple readings.

The purpose is to evaluate:

```text
measurement spread

occasional outliers

sensor consistency
```

This helps determine whether a software threshold has enough margin.

A threshold located too close to normal measurement variation may produce unstable state changes.

---

# 2.39 Left/Right Comparison

The sensors can also be tested against equivalent wall geometries.

This helps determine whether:

```text
S2 and S3 behave similarly
```

or whether mounting and physical environment create meaningful differences.

The purpose is not to require identical readings.

The sensors occupy different physical locations on the robot.

Instead, the test identifies whether each sensor is internally repeatable and geometrically understandable.

---

# 2.40 Mounting Verification

<div align="center">

<img
  src="../../v-photos/v4/ultrasonic_pair_top.jpg"
  alt="Top view used to verify Piolín ultrasonic sensor mounting"
  width="700"
/>

<br>

<sub><b>Figure 2.7.</b> Top view provides a direct visual check of the two lateral sensor positions and orientations.</sub>

</div>

After:

```text
transport

mechanical work

sensor removal

chassis modification
```

the sensor arrangement should be visually verified before assuming previous calibration remains valid.

A small physical change can have a larger effect than a small software threshold adjustment.

---

# 2.41 Sensor Failure Diagnosis

| Observed Behavior | Possible Cause |
| :--- | :--- |
| S2 always reads unexpectedly | Left sensor mount, cable, port, wall geometry |
| S3 always reads unexpectedly | Right sensor mount, cable, port, wall geometry |
| Inner/outer control appears inverted | Direction logic may be wrong even if wiring is correct |
| Robot continuously moves toward one wall | Control sign, steering, sensor mapping, mechanical bias |
| Robot zig-zags | Excessive correction, delay, noisy geometry |
| Sensor suddenly reports much larger distance | Corner, open space, beam geometry, outlier |
| Reading changed after robot repair | Sensor orientation may have moved |
| Obstacle recovery starts too early | Pillar-pass interpretation may be weak |
| Robot ignores close wall | Safety threshold, reading validity, steering arbitration |
| Both sensors look wrong | Vehicle orientation, environment, software units/configuration |

The diagnostic process should identify whether the issue originates in:

```text
physical geometry

sensor measurement

software interpretation

steering response
```

before controller parameters are changed.

---

# 2.42 Diagnostic Order

A useful ultrasonic diagnostic sequence is:

```text
1. Verify physical S2 = LEFT.

2. Verify physical S3 = RIGHT.

3. Inspect sensor mounts.

4. Inspect cable connections.

5. Read raw S2 value.

6. Read raw S3 value.

7. Compare readings with known geometry.

8. Rotate/move robot and observe expected change.

9. Verify inner/outer software mapping.

10. Only then tune wall-control values.
```

This prevents a wiring or orientation problem from being misdiagnosed as a control-algorithm problem.

---

# 2.43 Why the Front Ultrasonic Was Removed

Earlier Piolín development included or considered an additional frontal ultrasonic sensor.

The current architecture uses only two ultrasonic sensors because S1 is more valuable as a specialized round-specific port.

The final allocation is:

```text
OPEN

S1 → Gyro
S2 → Left US
S3 → Right US
S4 → Color
```

and:

```text
OBSTACLES

S1 → Pixy2.1
S2 → Left US
S3 → Right US
S4 → Color
```

A permanent frontal sensor would require another interface or replacing one of these information sources.

The final strategy instead relies on:

```text
lateral wall geometry
+
round-specific S1 sensing
```

to solve the navigation problem.

---

# 2.44 Why the Sensors Are Not Diagonal Anymore

Earlier sensor-placement experiments considered different viewing directions.

The current sensors are lateral.

A diagonal arrangement can provide information that combines:

```text
forward geometry

lateral geometry
```

but that also makes interpretation more dependent on angle.

The current lateral mounting gives each sensor a clearer primary responsibility:

```text
S2
→ left-side geometry


S3
→ right-side geometry
```

This makes the physical meaning of each port easier to document and debug.

---

# 2.45 Current vs. Legacy Ultrasonic Architecture

The current ultrasonic definition is:

```text
2 sensors total

S2 = LEFT

S3 = RIGHT

both lateral
```

Historical Piolín versions may show:

```text
front ultrasonic

different port assignment

diagonal mounting

different sensor count
```

Those configurations should be treated as legacy or experimental architecture.

They should not be used as current reconstruction instructions.

---

# 2.46 Port Consistency

<div align="center">

<img
  src="../../v-photos/v4/ev3_sensor_ports.jpg"
  alt="Piolín EV3 sensor ports used by the ultrasonic sensors"
  width="660"
/>

<br>

<sub><b>Figure 2.8.</b> The current EV3 port convention permanently assigns S2 to the left ultrasonic and S3 to the right ultrasonic.</sub>

</div>

Port consistency is important because a software controller can behave correctly according to its own assumptions while still producing the wrong physical result if the sensors are swapped.

For example:

```text
software assumes:

S2 = LEFT
S3 = RIGHT
```

but hardware becomes:

```text
S2 = RIGHT
S3 = LEFT
```

then a correct wall-safety command can become physically inverted.

The port mapping therefore needs to remain consistent throughout:

```text
hardware

source code

documentation

testing
```

---

# 2.47 Same Ultrasonic Hardware in Both Rounds

One of the strengths of Piolín's current architecture is that the two lateral sensors remain unchanged during the round conversion.

When switching from Open to Obstacles:

```text
S1 changes

S2 does not

S3 does not

S4 does not
```

This means the physical lateral-geometry reference remains stable even though the specialized perception system changes completely.

That improves reproducibility and reduces the number of hardware variables that must be recalibrated between competition rounds.

---

# 2.48 Sensor Responsibilities by Round

| Function | Open | Obstacles |
| :--- | :---: | :---: |
| Left wall geometry | S2 | S2 |
| Right wall geometry | S3 | S3 |
| Inner/outer course geometry | S2/S3 | Context-dependent |
| Wall safety | S2/S3 | S2/S3 |
| Straight lateral correction | S2/S3 | S2/S3 |
| Corner geometry support | S2/S3 | S2/S3 |
| Post-maneuver recovery | S2/S3 | S2/S3 |
| Heading measurement | Gyro S1 | Not ultrasonic |
| Pillar color identification | Not ultrasonic | Pixy S1 |
| Course-state marking | Color S4 | Color S4 |

This table shows that the ultrasonic subsystem has a stable geometric role while other sensors supply information it cannot measure.

---

# 2.49 Values Intentionally Not Claimed as Final

The following should only be published after measurement and validation on the current V4 robot:

```text
final inner-wall target distance

final outer-wall thresholds

final safety distance

sensor mounting height

sensor offset from vehicle center

exact ultrasonic beam width

final filtering window

final outlier threshold

corner geometry thresholds

pillar-pass distance threshold

post-obstacle recovery threshold

measured sensor repeatability

measured static error

maximum reliable operating distance
```

Current software may contain working values, but those should be identified as tuning parameters rather than universal specifications until testing is finalized.

---

# 2.50 Recommended V4 Ultrasonic Characterization

A complete sensor characterization should include several real experiments.

### Static distance calibration

Place the vehicle at several measured distances from a flat boundary and record S2/S3.

### Repeatability

Keep the robot fixed and collect repeated readings.

### Orientation test

Keep the robot at approximately the same center position but rotate it slightly to observe how yaw affects the measured distance.

### Corner transition test

Record how S2/S3 behave while the vehicle approaches and enters a representative corner.

### Dynamic straight test

Record the measurements during stable straight driving.

### Obstacle pass test

Observe the lateral sensor response while Piolín moves alongside and then beyond a pillar.

These tests would convert the current qualitative understanding into quantitative V4 evidence.

---

# 2.51 Complete Ultrasonic Role

The complete subsystem can be summarized as:

```text
                 LEFT WALL
                    │
                    ▼
               S2 LEFT US
                    │
                    │
                    ▼
                   EV3
                    ▲
                    │
                    │
              S3 RIGHT US
                    ▲
                    │
                 RIGHT WALL
```

During Open, the EV3 combines that geometry with:

```text
Gyro heading
+
Color course state
```

During Obstacles, it combines the same geometry with:

```text
Pixy visual target
+
Color course state
```

The ultrasonic sensors therefore provide the stable geometric layer shared by both autonomous strategies.

---

# 2.52 Final Engineering Assessment

Piolín's current ultrasonic architecture uses two lateral EV3 Ultrasonic Sensors with a permanent and unambiguous physical mapping:

```text
S2 = LEFT

S3 = RIGHT
```

The decision to keep both sensors lateral provides the EV3 with continuous information about the two sides of the track while simplifying hardware interpretation.

During the Open Challenge, this information complements the Gyro Sensor:

```text
Ultrasonics
→ lateral geometry

Gyro
→ heading
```

During the Obstacle Challenge, it complements Pixy2.1:

```text
Ultrasonics
→ track geometry

Pixy
→ obstacle identity and image position
```

The ultrasonic sensors also support wall safety, corner transition awareness, post-obstacle recovery, and the geometric confirmation needed before Piolín returns to normal course control.

Their limitations are equally important. The measurements depend on sensor orientation, vehicle yaw, surface geometry, acoustic reflection, and the current driving state. For that reason, one ultrasonic value is not treated as a complete description of Piolín's position.

The final design principle is:

> **Use the ultrasonic sensors for the physical information they measure best—left and right local geometry—and combine that information with specialized sensing rather than forcing the ultrasonic subsystem to solve heading, vision, and course-state problems by itself.**

This division of responsibilities keeps Piolín's sensing architecture understandable, reproducible, and adaptable across both WRO Future Engineers challenges.

---

<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
