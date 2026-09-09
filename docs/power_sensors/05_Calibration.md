# 5. Sensor Calibration

<div align="center">

<img
  src="../../v-photos/v4/piolin_open_top.jpg"
  alt="Top view of Piolín in the Open Challenge configuration"
  width="720"
/>

<br>

<sub><b>Figure 5.1.</b> Calibration is performed on the complete physical robot because sensor behavior depends on mounting, orientation, surrounding structure, and the current competition configuration.</sub>

</div>

Calibration is the process that connects Piolín's **raw sensor measurements** with meaningful physical information that the navigation software can use.

The purpose is not simply to find numbers that make one test work. A useful calibration should establish a repeatable relationship between:

```text
physical environment
        ↓
sensor installation
        ↓
sensor measurement
        ↓
software interpretation
        ↓
vehicle response
```

Piolín uses different specialized sensing configurations for the two WRO Future Engineers challenges, so calibration is also round-specific.

The current architectures are:

```text
OPEN CHALLENGE

S1 → Gyro
S2 → Left Ultrasonic
S3 → Right Ultrasonic
S4 → Color Sensor
```

and:

```text
OBSTACLE CHALLENGE

S1 → Pixy2.1
S2 → Left Ultrasonic
S3 → Right Ultrasonic
S4 → Color Sensor
```

The Gyro and Pixy2.1 are never active simultaneously.

Three sensor systems remain especially important to calibration:

```text
lateral ultrasonic geometry

floor-color recognition

round-specific S1 sensing
```

In the Open Challenge, S1 calibration concerns the Gyro Sensor.

In the Obstacle Challenge, S1 calibration concerns Pixy2.1 and its trained visual signatures.

---

## 5.1 Calibration Is a Physical Process

A software threshold is only valid for the physical sensor configuration under which it was measured.

If a sensor is moved, tilted, remounted, or surrounded by a different structure, its previous calibration may no longer represent the same physical conditions.

For Piolín, important calibration variables include:

```text
ultrasonic orientation

ultrasonic mounting position

Color Sensor height

Color Sensor casing

Gyro orientation

Pixy2.1 position

Pixy2.1 orientation

Pixy2.1 3D-printed casing

vehicle mechanical configuration
```

This leads to one of Piolín's main calibration principles:

> **Calibrate the complete installed sensor system, not the sensor as an isolated electronic component.**

The same EV3 sensor can behave differently after a mechanical change because the geometry around it has changed.

---

## 5.2 Calibration Before Software Tuning

Sensor calibration should occur before major navigation constants are tuned.

The preferred order is:

```text
VERIFY HARDWARE
      ↓
VERIFY SENSOR MOUNTING
      ↓
READ RAW VALUES
      ↓
CHARACTERIZE SENSOR
      ↓
DEFINE CLASSIFICATION / GEOMETRY
      ↓
TEST DYNAMICALLY
      ↓
TUNE CONTROLLER
```

Skipping the first stages creates a common problem:

```text
bad physical measurement
      ↓
software correction added
      ↓
hardware changes slightly
      ↓
software becomes wrong again
```

A stable calibration reduces the amount of software compensation required later.

---

# 5.3 Pre-Calibration Hardware Check

Before collecting values, Piolín should be checked mechanically.

The minimum inspection is:

```text
S2 physically LEFT?

S3 physically RIGHT?

Ultrasonic sensors aligned?

Color Sensor facing floor?

Color Sensor casing secure?

Gyro correctly oriented for Open?

Pixy2.1 correctly installed for Obstacles?

Pixy2.1 3D casing secure?

Sensor cables fully connected?

Correct S1 device installed for active round?
```

The sensor ports must match the documentation and source code.

The permanent convention is:

```text
S2 = LEFT

S3 = RIGHT

S4 = COLOR
```

Only S1 changes.

---

# 5.4 Ultrasonic Calibration

<div align="center">

<img
  src="../../v-photos/v4/ultrasonic_pair_top.jpg"
  alt="Piolín lateral ultrasonic sensor pair"
  width="700"
/>

<br>

<sub><b>Figure 5.2.</b> The two ultrasonic sensors are calibrated as installed lateral geometry sensors rather than as isolated rangefinders.</sub>

</div>

Piolín uses two permanent lateral EV3 Ultrasonic Sensors:

```text
S2 → LEFT

S3 → RIGHT
```

Their calibration should establish how the measured values relate to known physical track geometry.

The objective is not necessarily to force both sensors to return identical values.

Instead, the goal is to understand:

```text
what S2 reports at known left-wall positions

what S3 reports at known right-wall positions

how repeatable each measurement is

how orientation affects each measurement
```

The physical mounting of the two sensors is therefore part of the test.

---

## 5.5 Ultrasonic Mount Verification

<div align="center">

<img
  src="../../v-photos/v4/ultrasonic_lateral_alignment.jpg"
  alt="Piolín ultrasonic sensors aligned laterally"
  width="700"
/>

<br>

<sub><b>Figure 5.3.</b> Lateral alignment should be verified before distance values are treated as calibration data.</sub>

</div>

Before measuring distances, verify that the sensors remain:

```text
lateral

secure

approximately consistent with the intended chassis orientation
```

A sensor that rotates even slightly can begin observing a different part of the wall.

Then:

```text
same vehicle position
```

can produce:

```text
different ultrasonic value
```

without any change in the software.

This is why sensor alignment should be checked before modifying wall-control gains or target distances.

---

## 5.6 Static Ultrasonic Distance Test

A basic calibration can place Piolín at several known physical distances from a flat track boundary.

For each position, record the raw ultrasonic result.

A table can be used:

| Physical Reference | S2 Reading | S3 Reading | Notes |
| :---: | :---: | :---: | :--- |
| Position 1 | — | — | — |
| Position 2 | — | — | — |
| Position 3 | — | — | — |
| Position 4 | — | — | — |

Only measured V4 values should be entered.

The test should include several readings at each position rather than one sample.

This helps distinguish:

```text
normal measurement variation
```

from:

```text
consistent geometric offset
```

---

## 5.7 Ultrasonic Repeatability

At a fixed vehicle position, collect multiple measurements from each sensor.

For example:

```text
same wall

same vehicle position

same vehicle heading

several sensor readings
```

The useful question is not:

> Does the sensor always return exactly one number?

The useful question is:

> What range of values should be considered normal for this physical geometry?

This range later helps determine reasonable:

```text
control deadbands

safety thresholds

outlier rejection
```

without reacting strongly to insignificant sensor variation.

---

## 5.8 Ultrasonic Orientation Test

The lateral sensors are affected by vehicle yaw.

A useful experiment is to keep Piolín in approximately the same region while changing its heading slightly.

For example:

```text
parallel to wall

slightly rotated toward wall

slightly rotated away from wall
```

and record how S2/S3 respond.

This test demonstrates an important limitation:

```text
ultrasonic distance change
```

does not always represent:

```text
pure lateral vehicle movement
```

Part of the change can come from vehicle orientation.

This is especially relevant when interpreting measurements near corners.

---

# 5.9 Open Ultrasonic Calibration

During Open, the ultrasonic values primarily represent lateral geometry while the gyro provides heading information.

The useful separation is:

```text
S2 / S3
→ WHERE Piolín is laterally
```

```text
Gyro
→ HOW Piolín is oriented
```

The current Open controller may use a target inner-wall value as part of its working tuning, but any such value should be treated as:

```text
current software calibration
```

rather than:

```text
immutable physical specification
```

until it has been validated across representative track sections and repeated runs.

---

## 5.10 Inner and Outer Calibration

The physical sensors remain:

```text
S2 = LEFT

S3 = RIGHT
```

but the Open software assigns inner and outer roles based on direction.

For counterclockwise:

```text
S2 LEFT
→ INNER

S3 RIGHT
→ OUTER
```

For clockwise:

```text
S3 RIGHT
→ INNER

S2 LEFT
→ OUTER
```

Calibration data should therefore preserve the physical identities first.

It is safer to record:

```text
S2 reading

S3 reading
```

rather than only:

```text
inner reading

outer reading
```

because physical sensor identity remains constant while the logical role changes.

---

# 5.11 Color Sensor Calibration

<div align="center">

<img
  src="../../v-photos/v4/color_sensor_s4_installed.jpg"
  alt="Piolín EV3 Color Sensor installed on S4"
  width="660"
/>

<br>

<sub><b>Figure 5.4.</b> The Color Sensor is calibrated in its permanent downward-facing S4 installation.</sub>

</div>

The Color Sensor must distinguish the important floor categories used by Piolín:

```text
BLUE

ORANGE

NORMAL FLOOR
```

The useful calibration is not based on one sample from each category.

Instead, the team should measure a **range of observations** for each physical surface.

The calibration must use:

```text
current sensor

current casing

current mounting height

real track colors

representative lighting
```

because any of these can change the optical values.

---

# 5.12 Color Sensor Casing

<div align="center">

<img
  src="../../v-photos/v4/color_sensor_casing.jpg"
  alt="Piolín 3D-printed Color Sensor light isolation casing"
  width="660"
/>

<br>

<sub><b>Figure 5.5.</b> The Color Sensor casing improves control of the optical environment around the downward-facing sensor.</sub>

</div>

The casing reduces uncontrolled light reaching the floor-measurement region.

Its purpose is to improve the physical conditions before classification occurs.

Conceptually:

```text
ambient light variation
        ↓
casing reduces part of variation
        ↓
sensor measurement
        ↓
software classification
```

The casing does not eliminate the need for calibration.

Instead, it makes calibration more meaningful because the measurement environment is more controlled.

If the casing is changed or repositioned, color values should be reverified.

---

# 5.13 Blue Calibration

<div align="center">

<img
  src="../../v-photos/v4/color_sensor_blue_mark.jpg"
  alt="Piolín Color Sensor over a blue floor reference"
  width="660"
/>

<br>

<sub><b>Figure 5.6.</b> Blue calibration should use the real course marking and current sensor installation.</sub>

</div>

Blue should be measured repeatedly under the actual S4 installation.

A useful dataset includes:

```text
center of blue marking

different points across blue region

stationary readings

dynamic crossings
```

The objective is to determine a classification region wide enough to detect the actual marking while remaining sufficiently distinct from Orange and the normal floor.

During Open:

```text
BLUE first
→ counterclockwise
```

so incorrect Blue classification can affect the complete direction state of the run.

---

# 5.14 Orange Calibration

<div align="center">

<img
  src="../../v-photos/v4/color_sensor_orange_mark.jpg"
  alt="Piolín Color Sensor over an orange floor reference"
  width="660"
/>

<br>

<sub><b>Figure 5.7.</b> Orange must be characterized independently because its optical range can differ from Blue.</sub>

</div>

Orange should be measured using the same process.

During Open:

```text
ORANGE first
→ clockwise
```

The calibration should therefore provide enough separation that:

```text
Blue is not classified as Orange

Orange is not classified as Blue

normal floor is not classified as either
```

The final thresholds should come from the measured distribution of values rather than one ideal reading.

---

# 5.15 Color Calibration Dataset

A useful table can contain:

| Surface | Trial | Raw / RGB Measurement | Classified As |
| :--- | :---: | :--- | :--- |
| Blue | 1 | — | — |
| Blue | 2 | — | — |
| Blue | 3 | — | — |
| Orange | 1 | — | — |
| Orange | 2 | — | — |
| Orange | 3 | — | — |
| Normal floor | 1 | — | — |
| Normal floor | 2 | — | — |
| Normal floor | 3 | — | — |

The final dataset should contain real measurements only.

No theoretical RGB values should be substituted for measurements from the actual robot.

---

# 5.16 Dynamic Color Calibration

Static recognition is only the first stage.

Piolín detects course markings while moving.

Therefore the final calibration should test:

```text
slow crossing

normal driving-speed crossing

slightly different path across marking
```

At higher speed:

```text
less time above color
→ fewer samples
```

This affects:

```text
confirmation count

event lock

debounce

classification delay
```

A color threshold that works perfectly while stationary is not sufficient evidence of reliable dynamic detection.

---

# 5.17 Event Calibration

The Color Sensor must not only classify color correctly.

It must also convert a physical crossing into exactly one navigation event.

The desired behavior is:

```text
normal floor
      ↓
Blue enters sensor
      ↓
Blue confirmed
      ↓
ONE event
      ↓
sensor remains above Blue
      ↓
NO additional events
      ↓
marking leaves sensor
      ↓
detector re-armed
```

Calibration therefore includes:

```text
classification thresholds
+
temporal confirmation
+
event locking
+
re-arm condition
```

These values should be tuned together using real crossings.

---

# 5.18 Gyro Calibration — Open Challenge

<div align="center">

<img
  src="../../v-photos/v4/s1_open_gyro.jpg"
  alt="Piolín Gyro Sensor connected to S1 for Open Challenge"
  width="680"
/>

<br>

<sub><b>Figure 5.8.</b> Open Challenge calibration includes the round-specific EV3 Gyro Sensor on S1.</sub>

</div>

The Gyro Sensor is active only during Open.

Its purpose is to provide a heading and rotation reference.

At program startup, the current Open architecture establishes a local reference by resetting the gyro angle.

Conceptually:

```text
Piolín positioned at start
        ↓
gyro allowed to stabilize
        ↓
gyro reset
        ↓
initial heading = 0
```

The robot can then measure relative angular change from that reference.

---

## 5.19 Gyro Orientation

<div align="center">

<img
  src="../../v-photos/v4/gyro_orientation.jpg"
  alt="Physical orientation of Piolín EV3 Gyro Sensor"
  width="660"
/>

<br>

<sub><b>Figure 5.9.</b> Gyro calibration depends on preserving the sensor's orientation relative to the chassis.</sub>

</div>

The gyro must remain mechanically fixed because the software assumes its measured rotation corresponds to vehicle yaw.

If the sensor orientation changes relative to the chassis:

```text
gyro reference
```

no longer describes the vehicle in exactly the same way.

Therefore the physical gyro mount should be verified before Open heading constants are changed.

---

# 5.20 Gyro Zero Calibration

The most basic gyro calibration is the startup zero.

A practical sequence is:

```text
1. Place Piolín in the intended start orientation.

2. Keep the robot still.

3. Initialize the sensor.

4. Reset the gyro angle.

5. Confirm reading is near the expected reference.

6. Begin movement only after initialization is complete.
```

The robot should not reset the heading while it is already physically rotating unless that behavior is intentionally part of the controller.

---

# 5.21 Gyro Drift Test

The gyro can be tested while Piolín remains stationary.

The objective is to observe whether:

```text
reported heading
```

changes significantly even though:

```text
physical heading
```

does not.

A test table can use:

| Time | Gyro Angle | Robot Physically Moved? |
| :---: | :---: | :---: |
| Start | — | No |
| Sample 2 | — | No |
| Sample 3 | — | No |
| Sample 4 | — | No |

This should be populated only with actual measurements.

The purpose is to determine how stable the heading reference remains over the duration of a representative run.

---

# 5.22 Gyro Turn Calibration

A second experiment can physically rotate Piolín through a known track corner and compare the gyro change with the observed vehicle orientation.

The course corners are approximately right-angle turns, but the software should not assume one exact final gyro value without measurement.

A practical Ackermann vehicle can begin and release steering before or after the chassis reaches a theoretical geometric angle.

The useful calibration question is:

> **What gyro behavior corresponds to a reliable corner exit for the actual robot?**

This value should be established through repeated physical testing.

---

# 5.23 Gyro and Ultrasonic Cross-Checking

Open calibration becomes stronger when gyro and ultrasonic data are observed together.

For example:

```text
gyro indicates heading recovered
```

but:

```text
S2/S3 geometry still unstable
```

may indicate that the robot has rotated enough but has not yet reached a good lateral exit position.

Similarly:

```text
ultrasonic distance looks normal
```

while:

```text
gyro indicates significant yaw
```

can show that wall distance alone is insufficient to describe vehicle state.

This is why Open calibration should eventually test both data sources simultaneously.

---

# 5.24 Pixy2.1 Calibration — Obstacle Challenge

<div align="center">

<img
  src="../../v-photos/v4/pixy21_front.jpg"
  alt="Pixy2.1 installed on Piolín for Obstacle Challenge calibration"
  width="700"
/>

<br>

<sub><b>Figure 5.10.</b> Pixy2.1 is calibrated as part of the complete forward-facing Obstacle Challenge vision system.</sub>

</div>

Pixy2.1 replaces the Gyro Sensor on S1 during the Obstacle Challenge.

The current visual signature mapping is:

```text
sig1 → Pink → Parking

sig2 → Red → Pass RIGHT

sig3 → Green → Pass LEFT
```

Pixy calibration must establish more than whether the camera can detect a color.

It should characterize:

```text
signature reliability

block position

apparent size

target relevance

lighting response

target persistence
```

because all of these affect the final obstacle maneuver.

---

# 5.25 Pixy2.1 3D-Printed Casing

The current Pixy2.1 installation includes a **3D-printed casing around the camera**.

This casing is now part of Piolín's active Obstacle Challenge hardware and must therefore remain installed during final camera calibration.

Its main engineering roles are to provide a more controlled and repeatable physical environment around the vision module and to protect/support the camera as part of the front assembly.

Depending on the exact geometry of the casing, it can also reduce some unwanted side illumination reaching the camera.

However:

```text
Pixy casing
≠
replacement for visual calibration
```

The camera signatures still need to be trained and validated under representative track lighting.

The important rule is:

> **Pixy calibration performed with the casing installed should not automatically be reused after removing, modifying, or repositioning the casing.**

This is the same general principle applied to the Color Sensor casing: the mechanical enclosure becomes part of the optical system.

---

# 5.26 Why the Pixy Casing Matters

Pixy color recognition depends on the light reaching the camera.

Environmental changes can include:

```text
overhead lights

sunlight

shadows

reflections

bright objects beside the track
```

The casing can help make the camera installation more mechanically and optically repeatable.

The desired relationship is:

```text
stable camera mount
+
stable casing
+
representative lighting
        ↓
more repeatable visual blocks
```

It should not be assumed that the casing eliminates lighting sensitivity entirely.

Instead, it reduces one source of variability while Pixy's signature training and software logic handle the remaining visual uncertainty.

---

# 5.27 Pixy Signature Calibration

Each physical target should be tested independently.

The current mapping is:

| Signature | Target | Required Meaning |
| :---: | :--- | :--- |
| 1 | Pink | Parking |
| 2 | Red | Pass right |
| 3 | Green | Pass left |

The calibration must verify that the trained signature and the EV3 software agree.

A correct visual detection with an incorrect software mapping still produces the wrong maneuver.

The sequence is:

```text
physical color
      ↓
Pixy signature
      ↓
EV3 signature mapping
      ↓
navigation rule
```

Every stage must be correct.

---

# 5.28 Red Signature Test

<div align="center">

<img
  src="../../v-photos/v4/pixy21_red_detection.jpg"
  alt="Pixy2.1 red pillar detection"
  width="680"
/>

<br>

<sub><b>Figure 5.11.</b> Red detection calibration validates signature 2 and the corresponding pass-right rule.</sub>

</div>

Red testing should verify:

```text
Red produces sig2

sig2 is stable enough to be useful

Red is not confused with Pink

Red is not confused with Green

small unrelated red regions do not dominate navigation
```

The final navigation meaning is always:

```text
RED
→ pass RIGHT
```

The image position of Red may change.

The passing rule does not.

---

# 5.29 Green Signature Test

<div align="center">

<img
  src="../../v-photos/v4/pixy21_green_detection.jpg"
  alt="Pixy2.1 green pillar detection"
  width="680"
/>

<br>

<sub><b>Figure 5.12.</b> Green detection calibration validates signature 3 and the corresponding pass-left rule.</sub>

</div>

Green testing should independently verify:

```text
Green produces sig3

Green remains detectable at useful approach positions

background colors do not frequently create false sig3 blocks
```

The required navigation rule remains:

```text
GREEN
→ pass LEFT
```

Red and Green should not be assumed to have identical detection strength under the same lighting.

Each needs its own validation.

---

# 5.30 Parking Signature Test

<div align="center">

<img
  src="../../v-photos/v4/pixy21_parking_detection.jpg"
  alt="Pixy2.1 pink parking reference detection"
  width="680"
/>

<br>

<sub><b>Figure 5.13.</b> Signature 1 is calibrated independently as the visual parking reference.</sub>

</div>

The Pink signature should be distinguishable from the obstacle signatures.

The final parking controller should not rely only on:

```text
sig1 visible
```

because a valid visual block does not automatically prove that the complete course state is ready for parking.

Instead, Pink calibration establishes:

```text
can the visual reference be detected reliably?
```

while the navigation controller decides:

```text
is this the correct time to use it?
```

---

# 5.31 Pixy Horizontal Coordinate Calibration

The `x` value describes the horizontal position of a block inside the camera image.

A useful static calibration moves the same pillar through several positions:

```text
left of camera center

near center

right of camera center
```

and records the reported `x`.

This confirms the expected coordinate direction and provides a reference for steering logic.

One critical principle must remain fixed:

```text
x
→ target geometry
```

not:

```text
x
→ competition passing rule
```

A Red pillar remains a pass-right obstacle regardless of where it appears in the camera image.

---

# 5.32 Pixy Apparent-Size Calibration

Pixy also provides:

```text
width

height
```

which can be combined conceptually into:

```text
apparent area
≈ width × height
```

A useful test moves the same pillar through several distances and records how its apparent size changes.

The expected general tendency is:

```text
closer pillar
→ larger image block
```

but the relationship is not automatically an exact physical-distance equation.

Viewing angle, partial visibility, and lighting can change apparent dimensions.

The purpose of this calibration is therefore to support:

```text
target relevance
```

rather than claim exact centimeter ranging from the camera.

---

# 5.33 Multiple-Block Calibration

The Obstacle Challenge can produce situations where multiple valid blocks are visible.

The calibration should therefore test:

```text
Red + Green visible together

two blocks at different apparent sizes

one central + one peripheral block

near target + distant target
```

The goal is to determine whether the target-selection logic consistently chooses the most relevant current pillar.

Piolín should not rely permanently on:

```text
first block returned
```

because list order does not necessarily equal physical relevance.

---

# 5.34 Target-Lock Calibration

Once one pillar has been selected, Piolín may temporarily lock that target.

The lock prevents visual switching during an active maneuver.

Calibration should determine:

```text
how long the lock should persist

what evidence releases it

how brief target loss is handled
```

The target should not be released merely because it disappears for one camera update.

Likewise, it should not remain locked after the physical pillar has clearly been passed.

The final target-lock parameters remain under development.

---

# 5.35 Pixy Lighting Calibration

The camera should be tested under the lighting conditions expected during actual use.

Useful variations include:

```text
normal room lighting

slightly brighter illumination

slightly darker areas

representative track shadows
```

The test should ask:

```text
Does Red remain Red?

Does Green remain Green?

Does Pink remain distinguishable?

Do false blocks appear?
```

The new 3D-printed Pixy casing should remain installed during these tests because it is now part of the final optical installation.

---

# 5.36 Pixy Static vs. Dynamic Calibration

A stationary camera test is useful for signature training.

It is not enough for autonomous navigation.

During real movement:

```text
distance changes

camera yaw changes

pillar size changes

pillar x changes

lighting angle changes
```

Therefore calibration should progress from:

```text
stationary target
      ↓
slow vehicle approach
      ↓
normal-speed approach
      ↓
active steering
      ↓
complete pillar pass
```

This determines whether static camera performance remains useful while Piolín actually moves.

---

# 5.37 Obstacle Sensor Fusion Calibration

Pixy calibration should eventually be tested together with S2/S3.

The intended division is:

```text
Pixy
→ obstacle identity and visual relevance
```

```text
S2/S3
→ physical wall / lateral geometry
```

A representative test should record both sources during:

```text
pillar approach

avoidance

side pass

countersteering

recovery
```

This helps determine when obstacle control should dominate and when lateral wall recovery should regain greater authority.

---

# 5.38 Pillar-Pass Calibration

A key Obstacle Challenge calibration is deciding when the current pillar has actually been passed.

A visual-only condition such as:

```text
pillar disappeared
```

is weak because steering can move the camera away from the target before the vehicle has cleared it.

A stronger condition can combine:

```text
recent Pixy target

vehicle motion

lateral ultrasonic behavior

opening geometry after pillar
```

The exact final thresholds should come from recorded physical runs.

---

# 5.39 Calibration by Competition Round

The complete calibration workflow differs slightly between Open and Obstacles.

### Open

```text
verify mechanics
      ↓
verify S2/S3
      ↓
calibrate Color Sensor
      ↓
initialize / test Gyro
      ↓
test straight geometry
      ↓
test corner rotation
      ↓
test corner exit
      ↓
test multi-corner behavior
```

### Obstacles

```text
verify mechanics
      ↓
verify S2/S3
      ↓
verify Color Sensor
      ↓
install Pixy + 3D casing
      ↓
verify signatures
      ↓
test x / size
      ↓
test target selection
      ↓
test pillar pass
      ↓
test recovery
      ↓
test consecutive pillars
```

This keeps the calibration process aligned with the different information requirements of each round.

---

# 5.40 Battery Condition During Calibration

<div align="center">

<img
  src="../../v-photos/v4/ev3_battery_45501.jpg"
  alt="EV3 Rechargeable DC Battery 45501 used during Piolín calibration"
  width="650"
/>

<br>

<sub><b>Figure 5.14.</b> Battery condition should remain reasonably consistent when comparing dynamic calibration runs.</sub>

</div>

Sensor readings are not the only variable affecting dynamic calibration.

Motor response also matters.

When comparing:

```text
corner timing

obstacle reaction

reverse movement

parking
```

the battery condition should remain reasonably consistent.

Otherwise, the same sensor threshold can appear to behave differently simply because Piolín travels a different physical distance before the steering response develops.

---

# 5.41 One Variable at a Time

Calibration changes should be tested systematically.

Suppose the robot reacts too late to a Green pillar.

Potential causes include:

```text
Pixy detects late

block relevance threshold too strict

confirmation too long

Motor A too fast

Motor B response too slow
```

Changing all five at once does not reveal the cause.

A better process is:

```text
observe
      ↓
form hypothesis
      ↓
change one relevant parameter
      ↓
repeat same test
      ↓
compare
```

This transforms tuning into an engineering experiment.

---

# 5.42 Calibration Logging

A useful calibration record should contain:

| Field | Information to Record |
| :--- | :--- |
| Date | Test date |
| Challenge | Open / Obstacles |
| Software version | File or commit |
| Sensor | S1 / S2 / S3 / S4 |
| Mechanical configuration | Current mounting/casing |
| Battery condition | Test condition |
| Physical reference | Wall, floor, pillar, angle |
| Raw measurement | Actual sensor output |
| Processed state | Classification / target / geometry |
| Vehicle response | What Piolín did |
| Result | Expected / unexpected |
| Next change | One next calibration change |

For Pixy tests, the record should also note that the **3D-printed camera casing was installed**, because it is now part of the calibrated optical configuration.

---

# 5.43 When Calibration Must Be Rechecked

Calibration should be reverified after changes such as:

```text
ultrasonic remounting

ultrasonic orientation change

Color Sensor remounting

Color Sensor casing replacement

gyro remounting

Pixy remounting

Pixy casing modification

Pixy casing replacement

camera angle change

camera height change

major chassis change

wheel / steering changes that alter dynamic trajectories
```

Not every change necessarily requires a complete recalibration.

But the previous calibration should not be assumed automatically valid without at least a verification test.

---

# 5.44 Calibration Failure Diagnosis

| Symptom | First Calibration Area to Check |
| :--- | :--- |
| Open drifts despite normal wall distance | Gyro zero/orientation and steering |
| S2/S3 values suddenly changed | Ultrasonic mount / physical geometry |
| Inner/outer logic appears inverted | Direction mapping, not sensor remounting first |
| Blue missed | S4 thresholds, speed, casing |
| Orange missed | S4 thresholds, speed, casing |
| One line counted twice | Event-lock calibration |
| Gyro angle changes while stationary | Gyro stability / initialization |
| Open corner rotates incorrectly | Gyro turn calibration + geometry |
| Red weakly detected | Pixy Red signature / lighting |
| Green weakly detected | Pixy Green signature / lighting |
| Pixy behavior changes after casing work | Reverify optical calibration |
| Distant pillar affects steering too early | Target-relevance calibration |
| Pillar disappears and maneuver cancels | Target-loss / lock calibration |
| Pillar passed but robot stays in avoidance | Target-release / pass confirmation |
| Obstacle passed but wall hit | Recovery / ultrasonic arbitration |
| Parking reference appears too early | Parking-state logic rather than signature alone |

This encourages diagnosis at the correct layer before unrelated values are changed.

---

# 5.45 Values Not Yet Claimed as Final

The following calibration values should only be published as final after representative V4 testing:

```text
S2 static calibration curve

S3 static calibration curve

final inner-wall target

final wall safety thresholds

final ultrasonic filtering

measured ultrasonic repeatability

Blue classification range

Orange classification range

neutral-floor classification range

Color Sensor confirmation count

Color Sensor event-lock timing

Gyro drift

final gyro corner-release angle

Pixy camera height

Pixy camera pitch

Pixy camera yaw

Pixy image-center target

Red signature thresholds

Green signature thresholds

Pink signature thresholds

minimum useful block size

target relevance formula

target-lock duration

target-loss tolerance

pillar-pass confirmation threshold

maximum reliable obstacle reaction distance
```

Temporary code values are useful during development but should remain identified as **working calibration values** until validated.

---

# 5.46 Current Calibration Status

Piolín's hardware architecture is established, but several navigation calibration values are still being optimized.

Current work includes:

```text
Open initial acquisition

Open corner entry

Open corner exit

three-lap stability

Color Sensor progression counting

Pixy Red / Green reliability

multiple-block target selection

target locking

pillar-pass confirmation

post-pillar recovery

parking
```

This means the repository should distinguish clearly between:

```text
CURRENT HARDWARE
```

which can be documented definitively, and:

```text
FINAL PERFORMANCE CALIBRATION
```

which should be updated as measured evidence becomes available.

---

# 5.47 Complete Calibration Chain

The current calibration process can be summarized as:

```text
                    PHYSICAL ROBOT
                         │
                         ▼
                 VERIFY INSTALLATION
                         │
                         ▼
                  RAW SENSOR TEST
                         │
                         ▼
                STATIC CALIBRATION
                         │
                         ▼
                DYNAMIC CALIBRATION
                         │
                         ▼
                SENSOR INTERPRETATION
                         │
                         ▼
                  CONTROL RESPONSE
                         │
                         ▼
                   TRACK TESTING
                         │
                         ▼
                 MEASURE / OBSERVE
                         │
                         ▼
                 ADJUST ONE VARIABLE
                         │
                         └───────────────┐
                                         │
                                         ▼
                                      RETEST
```

The goal is not to search randomly for values that happen to complete one run.

The goal is to create a relationship between measurable physical conditions and predictable autonomous behavior.

---

# 5.48 Final Engineering Assessment

Calibration is the point at which Piolín's mechanical design, sensor installation, electronics, and software become one autonomous system.

The same raw measurement can have different meaning if the physical installation changes.

For this reason:

```text
ultrasonic mounting
```

is part of ultrasonic calibration,

```text
Color Sensor casing
```

is part of floor-color calibration,

```text
gyro orientation
```

is part of Open heading calibration,

and:

```text
Pixy2.1 mounting + 3D-printed casing
```

are part of Obstacle vision calibration.

Piolín therefore does not treat calibration as a list of isolated software constants.

Instead, calibration follows the complete chain:

```text
physical geometry
+
sensor installation
+
raw measurement
+
classification / interpretation
+
vehicle response
```

During Open, calibration combines:

```text
S2/S3 lateral geometry

S4 floor events

S1 gyro heading
```

During Obstacles, it combines:

```text
S2/S3 lateral geometry

S4 course state

S1 Pixy2.1 vision
```

The addition of the **3D-printed Pixy2.1 casing** strengthens this philosophy. Just as the Color Sensor casing is treated as part of its optical measurement system, the Pixy casing is now part of the physical camera installation and should remain consistent whenever final vision values are measured or compared.

The final calibration principle is:

> **Measure first, control the physical installation, validate dynamically, and only then treat a software value as meaningful.**

This approach allows Piolín's calibration values to represent the real V4 robot rather than assumptions inherited from earlier versions or isolated component tests.

---

<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
