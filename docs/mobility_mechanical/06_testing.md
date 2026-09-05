# 6. Mechanical and Mobility Testing

Piolín's mechanical system is validated through structured testing rather than only by observing whether the robot completes the course.

The purpose of mechanical testing is to determine whether the physical vehicle behaves consistently enough for the autonomous software to rely on it.

The testing process focuses on the interaction between:

```text
CHASSIS
    +
DRIVETRAIN
    +
STEERING
    +
WHEELS
    +
SENSOR MOUNTING
    ↓
REPEATABLE VEHICLE MOTION
```

A navigation algorithm can only be tuned effectively if similar motor commands produce reasonably similar physical responses.

For this reason, Piolín's mobility testing separates mechanical behavior from higher-level navigation logic whenever possible.

The main mechanical subsystems evaluated are:

```text
Steering center

Steering repeatability

Steering range

Straight-line movement

Drivetrain consistency

Encoder-to-distance behavior

Wheel traction

Corner repeatability

Reverse movement

Structural stability

Sensor-mount stability

Full vehicle integration
```

This document describes the testing methodology used to evaluate those areas and the evidence that should be recorded for the final robot.

---

## 6.1 Testing Objectives

The purpose of the mechanical validation process is to answer six main questions:

```text
1. Does the chassis remain mechanically consistent?

2. Does Motor A produce repeatable propulsion?

3. Does Motor B return to a repeatable steering position?

4. Does the physical steering system respond consistently to commands?

5. Do drivetrain and steering behavior remain usable during real course maneuvers?

6. Do mechanical changes affect sensor measurements or autonomous behavior?
```

These questions connect directly to the WRO Future Engineers requirement for a vehicle that can repeatedly navigate the track rather than succeed only in isolated runs.

---

# 6.2 Current Mechanical Reference

The current Piolín configuration used for mechanical testing is:

| Parameter | Current Configuration |
| :--- | :--- |
| **Main controller** | LEGO EV3 |
| **Drive actuator** | Motor A |
| **Steering actuator** | Motor B |
| **Drive architecture** | Rear propulsion |
| **Steering architecture** | Ackermann-style front steering |
| **Front wheel diameter** | 38.1 mm |
| **Rear wheel diameter** | ~61.0 mm |
| **Robot length** | 210 mm |
| **Robot width** | 150 mm |
| **Robot height** | 230 mm |
| **Robot mass** | 0.80476 kg |

These values define the physical version of Piolín to which the tests in this document apply.

If the robot geometry changes significantly, results should not automatically be transferred to the new configuration.

---

# 6.3 Why Mechanical Testing Is Separated From Software Testing

A robot can fail a navigation test for several different reasons.

For example:

```text
Robot turns too far
```

could be caused by:

```text
Software steering command too large
```

or:

```text
Mechanical steering center incorrect
```

or:

```text
Linkage became loose
```

or:

```text
Vehicle speed changed
```

Similarly:

```text
Robot misses a corner
```

could originate from:

```text
Sensor interpretation

Drive speed

Steering delay

Mechanical binding

Incorrect sensor mounting
```

Mechanical testing therefore attempts to isolate the physical system before modifying software parameters.

The development principle is:

```text
VERIFY MECHANICS
       ↓
VERIFY SENSORS
       ↓
TUNE CONTROL
       ↓
VALIDATE COMPLETE SYSTEM
```

This reduces the risk of compensating for a mechanical problem with increasingly complex software.

---

# 6.4 Testing Conditions

Whenever possible, repeated mechanical tests should be performed under similar conditions.

Important variables include:

```text
Same robot configuration

Same wheel set

Same steering linkage

Same battery configuration

Same track surface

Same starting position

Same software version

Same motor command
```

If one of these variables changes, the test record should identify that change.

This makes comparisons between runs more meaningful.

---

# 6.5 Test Record Format

Each significant mechanical test should contain enough information to reproduce the condition.

A useful record format is:

| Field | Information |
| :--- | :--- |
| **Date** | When the test was performed |
| **Robot version** | Current physical configuration |
| **Code version** | Software used during test |
| **Test type** | Steering, drivetrain, corner, etc. |
| **Starting condition** | Initial robot placement |
| **Command** | Motor/steering instruction |
| **Expected behavior** | What should physically occur |
| **Observed behavior** | What actually occurred |
| **Result** | Pass / partial / fail |
| **Notes** | Mechanical observations |
| **Evidence** | Photo, GIF, video, log, or measurement |

The objective is to preserve not only whether a test succeeded but also **how the result was obtained**.

---

# 6.6 Visual Inspection Before Dynamic Testing

Before running motion tests, Piolín should first be inspected mechanically.

The inspection includes:

```text
Front wheels attached correctly

Rear wheels secured

Steering linkage connected

Motor B mounting stable

Motor A mounting stable

Rear drivetrain rotates freely

Sensor mounts secure

HuskyLens mount stable

Color sensor casing clear of track

Cables clear of steering linkage
```

This prevents a known physical fault from contaminating the results of a software or mobility test.

---

# 6.7 Chassis Integrity Check

The chassis should maintain the relative positions of its major components during handling and motion.

The areas of greatest importance are:

```text
Steering support structure

Rear drivetrain support

EV3 mounting

Ultrasonic sensor mounts

HuskyLens mount

Color sensor mount
```

The test does not attempt to prove that the LEGO chassis has zero deformation.

Instead, the objective is to identify visible or functionally significant unwanted movement.

A chassis problem is considered relevant when it changes:

```text
Wheel alignment

Steering response

Sensor orientation

Drivetrain resistance
```

---

# 6.8 Steering Center Test

One of the most important mechanical tests is verifying the steering center.

The purpose is to determine whether:

```text
Software center command
        ≈
Physical straight-wheel position
```

### Procedure

1. Place Piolín on a level surface.
2. Command Motor B to the current software steering-center position.
3. Observe both front wheels.
4. Check whether the wheels are approximately aligned with the longitudinal direction of the chassis.
5. Drive the robot forward for a controlled distance.
6. Observe whether a strong directional bias is present.

The test distinguishes between:

```text
MECHANICAL CENTER ERROR
```

and:

```text
WALL-FOLLOWING CONTROL ERROR
```

A robot should not require a large continuous software correction simply to compensate for an incorrectly centered mechanical steering mechanism.

---

# 6.9 Steering Center Evidence Table

| Trial | Center Command | Visible Wheel Alignment | Straight Bias | Notes |
| :---: | :---: | :--- | :--- | :--- |
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

This table should contain actual current measurements or observations rather than estimated values.

---

# 6.10 Steering Range Test

The steering mechanism has finite travel in both directions.

The objective of this test is to identify the usable range without mechanically forcing the linkage.

Conceptually:

```text
LEFT LIMIT
    │
    │<------- USABLE RANGE ------->│
                                   │
                              RIGHT LIMIT
```

The test should observe:

```text
Smooth movement

No structural collision

No wheel-chassis interference

No linkage binding

No excessive motor load
```

The mechanical limit should not be defined only by the maximum command that the software can generate.

It should correspond to the physical range that the mechanism can use repeatedly without being forced beyond its normal motion.

---

# 6.11 Steering Motion Evidence

The steering GIF documented in:

[Steering System](04_steering.md)

is useful evidence for this subsystem.

It visually demonstrates:

```text
Motor B actuation

Linkage movement

Left wheel response

Right wheel response

Return toward center
```

A GIF or short video is particularly valuable because steering is a dynamic mechanism and cannot be completely documented by a static photograph.

The visual evidence should be paired with measured or observed behavior rather than being treated as quantitative proof of the steering angle.

---

# 6.12 Steering Repeatability Test

The steering system should return to approximately the same physical position when the same command is repeated.

A useful sequence is:

```text
CENTER
  ↓
LEFT
  ↓
CENTER
  ↓
RIGHT
  ↓
CENTER
```

repeated several times.

The objective is to observe whether:

```text
Center remains consistent

Left position remains consistent

Right position remains consistent

Linkage movement remains smooth
```

This test is especially useful for detecting:

```text
Mechanical play

Loose pivots

Motor mounting movement

Linkage deformation
```

---

# 6.13 Steering Repeatability Record

| Cycle | Left Response | Return to Center | Right Response | Final Center | Notes |
| :---: | :--- | :--- | :--- | :--- | :--- |
| 1 |  |  |  |  |  |
| 2 |  |  |  |  |  |
| 3 |  |  |  |  |  |
| 4 |  |  |  |  |  |
| 5 |  |  |  |  |  |

The most important observation is whether repeated cycles produce visibly different wheel positions under the same conditions.

---

# 6.14 Steering Reversal Test

Autonomous wall following often changes steering direction rapidly.

For example:

```text
LEFT correction
      ↓
CENTER
      ↓
RIGHT correction
```

The steering reversal test evaluates the physical response when Motor B changes direction.

The test should observe:

```text
Delay before wheel movement

Mechanical play

Linkage noise

Binding

Difference between left-to-right
and right-to-left response
```

This is particularly relevant because excessive steering reversals can amplify mechanical backlash and contribute to zig-zag behavior.

---

# 6.15 Straight-Line Propulsion Test

The drivetrain should first be evaluated with steering near mechanical center.

The objective is to observe the natural vehicle tendency before wall-following corrections are applied.

### Procedure

```text
Place Piolín at known start
        ↓
Set steering to center
        ↓
Run Motor A at fixed command
        ↓
Travel controlled distance
        ↓
Observe final position
```

The test helps identify:

```text
Steering center bias

Wheel alignment issues

Drivetrain asymmetry

Unexpected mechanical resistance
```

A small deviation does not automatically indicate failure.

The objective is to identify whether the deviation is consistent enough that it must be considered during navigation calibration.

---

# 6.16 Straight-Line Repeatability Record

| Trial | Motor A Command | Distance Reference | Final Lateral Deviation | Direction of Bias | Notes |
| :---: | :---: | :---: | :---: | :--- | :--- |
| 1 |  |  |  |  |  |
| 2 |  |  |  |  |  |
| 3 |  |  |  |  |  |
| 4 |  |  |  |  |  |
| 5 |  |  |  |  |  |

If the robot repeatedly deviates toward the same side, the mechanical system should be checked before compensating entirely through software.

---

# 6.17 Rear Wheel Geometry Reference

The current rear wheel diameter is:

```text
D_REAR ≈ 61.0 mm
```

with theoretical circumference:

```text
C_REAR ≈ 191.5 mm
```

The ideal wheel-distance relationship is:

```text
DISTANCE =
(THETA_WHEEL / 360)
×
191.5 mm
```

This equation provides a theoretical reference for drivetrain testing.

---

# 6.18 Encoder-to-Distance Test

The purpose of this test is to compare theoretical wheel rotation with actual vehicle displacement.

For example:

```text
Command a known rotational amount
        ↓
Measure actual track displacement
        ↓
Compare with theoretical value
```

If the command corresponds to actual wheel rotation:

```text
THEORETICAL_DISTANCE =
(THETA / 360)
×
191.5 mm
```

The difference can be calculated as:

```text
DISTANCE_ERROR =
MEASURED_DISTANCE
-
THEORETICAL_DISTANCE
```

and percentage error as:

```text
ERROR_PERCENT =
ABS(DISTANCE_ERROR)
/
THEORETICAL_DISTANCE
×
100
```

If a transmission ratio exists between Motor A and the wheels, that ratio must also be included.

---

# 6.19 Encoder Distance Record

| Trial | Encoder / Wheel Rotation | Theoretical Distance | Measured Distance | Difference | Error % |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 1 |  |  |  |  |  |
| 2 |  |  |  |  |  |
| 3 |  |  |  |  |  |
| 4 |  |  |  |  |  |
| 5 |  |  |  |  |  |

This table should use measured current data.

The purpose is not to force the robot to match the ideal equation perfectly, but to quantify how physical motion differs from the theoretical model.

---

# 6.20 Repeatability vs. Accuracy

Two different drivetrain qualities should be distinguished.

### Accuracy

```text
How close is measured movement
to the theoretical or desired distance?
```

### Repeatability

```text
How similar are repeated runs
under the same conditions?
```

For autonomous control, repeatability can be particularly important.

For example:

```text
Desired distance = 500 mm

Measured repeatedly:
480
481
479
482
```

is systematically offset but highly repeatable.

By contrast:

```text
460
520
475
540
```

is much harder to compensate for because the behavior itself is inconsistent.

The real project data should be used to determine which condition applies to Piolín.

---

# 6.21 Drivetrain Rotation Test

Before full vehicle testing, the rear drivetrain can also be observed while the robot is safely lifted from the track.

The objective is to check:

```text
Rear wheels rotate freely

No visible drivetrain binding

Axles remain aligned

No structural component contacts rotating parts

Motor A remains securely mounted
```

This isolates the drivetrain from tire-track friction.

A system that already binds while unloaded should not be evaluated first through autonomous navigation.

---

# 6.22 Drivetrain Load Test

After unloaded inspection, the drivetrain should be evaluated with the complete vehicle on the track.

The test determines whether the mechanism behaves differently when supporting the robot's full:

```text
0.80476 kg
```

mass.

The test can reveal issues that do not appear when the wheels are free-spinning, including:

```text
Axle flex

Increased friction

Wheel rubbing

Structural movement

Traction problems
```

---

# 6.23 Wheel Slip Observation

Encoder rotation does not guarantee equal physical displacement.

Wheel slip can be identified when:

```text
Wheel rotation occurs
        ↓
Expected displacement does not
        ↓
Track contact is slipping
```

Potential evidence includes:

```text
Visible wheel spin

Encoder distance greater than actual distance

Sudden movement during acceleration

Inconsistent reverse behavior
```

No fixed slip percentage should be assumed without measurement.

---

# 6.24 Forward and Reverse Comparison

Because Piolín uses the same Motor A drivetrain in both directions, forward and reverse motion can be compared.

A useful test sequence is:

```text
Forward controlled distance
        ↓
Stop
        ↓
Reverse equivalent command
        ↓
Compare returned position
```

Perfect return to the original point is not expected because:

```text
Slip

Steering alignment

Mechanical backlash

Surface interaction
```

can create differences.

The purpose is to identify large or systematic asymmetry.

---

# 6.25 Forward/Reverse Record

| Trial | Forward Command | Forward Distance | Reverse Command | Reverse Distance | Position Difference |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 1 |  |  |  |  |  |
| 2 |  |  |  |  |  |
| 3 |  |  |  |  |  |
| 4 |  |  |  |  |  |
| 5 |  |  |  |  |  |

This test is relevant to both parking and recovery behavior.

---

# 6.26 Low-Speed Steering Test

Piolín should be evaluated at a lower propulsion speed while applying several steering positions.

The objective is to isolate steering geometry without large dynamic effects.

Example sequence:

```text
CENTER
      ↓
Small left
      ↓
Medium left
      ↓
Center
      ↓
Small right
      ↓
Medium right
```

The test should observe whether increased steering produces progressively tighter vehicle curvature.

The expected qualitative relationship is:

```text
More steering
      ↓
Smaller turning radius
```

within the usable mechanical range.

---

# 6.27 Turning-Radius Test

A turning-radius test can quantify the relationship between steering command and vehicle path.

### Procedure

1. Select one fixed steering command.
2. Maintain that steering position.
3. Drive Piolín at a controlled low speed.
4. Allow the robot to follow part of a circular trajectory.
5. Record the approximate radius.
6. Repeat for several steering commands.

The theoretical bicycle-model relationship is:

```text
R =
L / tan(DELTA)
```

but the real Piolín measurement should be treated separately because:

```text
DELTA
```

is the physical equivalent wheel angle, not simply the Motor B encoder command.

---

# 6.28 Turning-Radius Record

| Steering Command | Direction | Approx. Measured Radius | Speed Setting | Notes |
| :---: | :--- | :---: | :---: | :--- |
|  | Left |  |  |  |
|  | Left |  |  |  |
|  | Right |  |  |  |
|  | Right |  |  |  |

This table can later provide useful evidence for:

[Steering Geometry](04_steering.md)

and:

[Parking Geometry](../software_obstacles_strategy/parking/03_ParkingGeom.md)

---

# 6.29 Left vs. Right Steering Symmetry

Ackermann steering does not require the entire mechanism to be perfectly symmetric in measured behavior, but large left/right differences should be identified.

The comparison should consider:

```text
Equivalent steering command

Equivalent drive speed

Equivalent surface

Equivalent starting geometry
```

Observe:

```text
Turn radius left

Turn radius right

Steering response

Return to center
```

If one direction is consistently tighter than the other, that behavior should be documented rather than hidden.

---

# 6.30 Corner Test

The WRO track contains repeated corners, so corner performance must be validated dynamically.

The test should evaluate:

```text
Corner entry

Peak steering response

Clearance from inner boundary

Clearance from outer boundary

Corner exit

Post-corner stabilization
```

A corner should not be evaluated only by whether Piolín physically completes the turn.

The exit trajectory matters because a robot that completes the corner but immediately approaches a wall has not completed a stable maneuver.

---

# 6.31 Corner Test Sequence

The physical sequence is:

```text
Approach straight
      ↓
Corner condition detected
      ↓
Steering increases
      ↓
Vehicle rotates
      ↓
Outer geometry becomes useful
      ↓
Inner geometry returns
      ↓
Steering decreases
      ↓
Post-corner stabilization
```

Testing should determine whether this sequence is mechanically repeatable.

The software logic itself is documented in:

[Corner Handling](../software_obstacles_strategy/04_cornerhandling.md)

---

# 6.32 Corner Repeatability Record

| Trial | Direction | Entry Behavior | Wall Contact | Exit Stability | Result | Notes |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 |  |  |  |  |  |  |
| 2 |  |  |  |  |  |  |
| 3 |  |  |  |  |  |  |
| 4 |  |  |  |  |  |  |
| 5 |  |  |  |  |  |  |

A useful final record should include multiple attempts rather than only the best successful run.

---

# 6.33 Clockwise and Counterclockwise Testing

Piolín must be capable of operating in both course directions.

The mechanical system should therefore be evaluated in:

```text
CLOCKWISE
```

and:

```text
COUNTERCLOCKWISE
```

movement.

This is particularly important because:

```text
Clockwise
      ↓
Right side becomes inner reference
```

while:

```text
Counterclockwise
      ↓
Left side becomes inner reference
```

Any mechanical asymmetry can therefore affect the two travel directions differently.

---

# 6.34 Direction Comparison Table

| Test | Clockwise Result | Counterclockwise Result | Difference Observed |
| :--- | :--- | :--- | :--- |
| Straight stability |  |  |  |
| Corner entry |  |  |  |
| Corner radius |  |  |  |
| Corner exit |  |  |  |
| Wall recovery |  |  |  |

This table helps distinguish a general mobility problem from a direction-specific mechanical issue.

---

# 6.35 Wall-Following Mechanical Test

Although wall-following is primarily a sensing/control function, it is also a useful mobility test.

A stable run indicates that:

```text
Drive motion

Steering actuation

Sensor mounting

Chassis alignment
```

are cooperating sufficiently for continuous navigation.

The test should evaluate:

```text
Oscillation amplitude

Frequency of large steering reversals

Wall contact

Long straight stability

Recovery after small deviations
```

Software tuning should only be interpreted after checking the mechanical conditions described earlier in this document.

---

# 6.36 Zig-Zag Diagnostic Test

If Piolín zig-zags, the cause should be isolated systematically.

Potential mechanical causes:

```text
Incorrect steering center

Loose linkage

Uneven wheel alignment

Delayed steering reversal

Sensor mount movement
```

Potential control causes:

```text
Gain too high

Correction range too large

Correction applied too late

Drive speed too high
```

The diagnostic process should therefore be:

```text
Check steering mechanically
        ↓
Check sensor mounting
        ↓
Check straight-line behavior
        ↓
Then modify controller
```

This prevents software from masking a physical fault.

---

# 6.37 Speed Comparison Test

Because vehicle speed affects steering dynamics, the same course segment can be tested at several Motor A speed settings.

The objective is to observe how mobility changes with speed.

Possible observations include:

```text
Straight stability

Corner overshoot

Steering responsiveness

Wall correction distance

Post-corner recovery
```

The relationship:

```text
A_LATERAL =
V² / R
```

explains why the same geometric turn becomes dynamically more demanding as velocity increases.

---

# 6.38 Speed Test Record

| Speed Setting | Straight Stability | Corner Stability | Recovery Quality | Notes |
| :---: | :--- | :--- | :--- | :--- |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |

This table should use the actual speed commands tested by the team.

The goal is not automatically to choose the largest value.

The goal is to find a useful balance between:

```text
Speed
   +
Control
   +
Repeatability
```

---

# 6.39 Obstacle-Avoidance Mechanical Validation

The Obstacle Challenge adds a larger lateral trajectory change than ordinary wall following.

Mechanical testing should evaluate whether Piolín can physically:

```text
Begin avoidance

Create sufficient lateral movement

Clear the pillar

Reverse steering direction

Recover toward normal path
```

The camera classification itself belongs to vision testing.

This section focuses specifically on the **vehicle motion** produced after an obstacle maneuver is requested.

---

# 6.40 Green and Red Maneuver Testing

The current obstacle interpretation is:

```text
GREEN
ID 1
   ↓
Pass on LEFT
```

and:

```text
RED
ID 2
  ↓
Pass on RIGHT
```

Both directions should be evaluated because the physical steering mechanism may not behave identically left and right.

A useful record is:

| Trial | Pillar | Requested Side | Pillar Cleared | Wall Contact | Recovery | Result |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Green | Left |  |  |  |  |
| 2 | Green | Left |  |  |  |  |
| 3 | Red | Right |  |  |  |  |
| 4 | Red | Right |  |  |  |  |

No result should be filled in unless supported by an actual current run.

---

# 6.41 Post-Obstacle Recovery Test

Avoiding the pillar is only the first half of a successful maneuver.

The robot must also return to a usable trajectory.

The recovery test evaluates:

```text
Position immediately after pillar

Vehicle angle after avoidance

Steering reversal

Lateral wall clearance

Distance required to stabilize

Readiness for next obstacle
```

This is especially important because Piolín cannot move sideways directly.

Recovery requires:

```text
Steering
     +
Forward motion
     ↓
Gradual lateral repositioning
```

---

# 6.42 Front-Safety Mechanical Test

The front ultrasonic system belongs mainly to sensing and safety, but its effect on mobility should also be validated.

The physical test objective is to confirm that when the front safety behavior activates:

```text
Forward motion changes
```

without producing an unexpected mechanical response such as:

```text
Drivetrain binding

Uncontrolled steering

Wheel interference
```

The exact distance threshold belongs to the active software and calibration documentation and should not be invented here.

---

# 6.43 Reverse Mobility Test

Reverse movement should be tested independently because drivetrain and steering behavior can differ from forward movement.

The test should evaluate:

```text
Reverse start

Straight reverse motion

Reverse steering

Direction reversal

Stopping behavior
```

This is particularly useful for parking-related validation.

---

# 6.44 Parking Mobility Test

Parking combines several mechanical behaviors:

```text
Forward movement

Reverse movement

Steering changes

Stopping

Vehicle rotation

Final positioning
```

The parking mobility test should record whether the drivetrain and steering system can physically execute the commanded sequence consistently.

Detailed parking-specific testing belongs to:

[Parking Testing](../software_obstacles_strategy/parking/05_Parkingtesting.md)

This mechanical section only verifies that the vehicle platform can perform the required motion.

---

# 6.45 Sensor-Mount Stability Test

Mechanical sensor mounts should be checked before and after repeated movement.

The test should inspect:

```text
S1 front ultrasonic orientation

S2 right ultrasonic orientation

S3 left ultrasonic orientation

S4 color sensor height/orientation

HuskyLens orientation
```

A mount is mechanically important because:

```text
Sensor moves
     ↓
Measurement geometry changes
     ↓
Navigation behavior changes
```

A sensor can remain electrically functional while its mechanical orientation becomes incorrect.

---

# 6.46 Lateral Ultrasonic Mount Verification

The lateral sensors are mounted at approximately:

```text
43.2 mm
```

above the floor in the current configuration.

Testing should verify that both remain securely fixed and directed toward their intended side.

The purpose is not to force both sensors to report identical values.

Their function is to provide reliable measurements from their actual physical positions.

---

# 6.47 Color Sensor Clearance Test

The downward-facing color sensor and its casing should maintain sufficient clearance from the track.

The test should check that during:

```text
Straight movement

Cornering

Acceleration

Reverse movement
```

the casing does not unintentionally contact the floor.

Mechanical contact could:

```text
Alter chassis movement

Damage mounting

Change sensor distance from surface
```

The exact ground-clearance value should only be added once physically measured.

---

# 6.48 HuskyLens Mount Stability

The HuskyLens mounting should remain stable during:

```text
Acceleration

Cornering

Obstacle avoidance

Reverse movement
```

A camera mount that changes angle can alter:

```text
Field of view

Pillar position in image

Detection timing
```

Therefore, mechanical camera stability is relevant even though vision classification itself belongs to the sensing documentation.

---

# 6.49 Cable Clearance Test

The steering linkage should be moved through its usable left and right range while observing nearby wiring.

The test checks for:

```text
Cable stretching

Cable pinching

Cable contact with wheels

Cable contact with linkage

Connector movement
```

The objective is to ensure that electrical routing does not become a mechanical resistance or failure source.

---

# 6.50 Full-Lap Mechanical Validation

After subsystem tests, Piolín should be evaluated over a complete course sequence.

The purpose is to observe whether mechanical behavior remains consistent over repeated:

```text
Straight sections

Corners

Steering reversals

Acceleration changes
```

A full lap can reveal issues that short bench tests do not show, such as:

```text
Linkage loosening

Increasing drivetrain resistance

Sensor mount movement

Accumulated steering bias
```

---

# 6.51 Multi-Lap Validation

Because the Open Challenge requires multiple laps, mechanical validation should not stop after one successful circuit.

A useful sequence is:

```text
Lap 1
  ↓
Lap 2
  ↓
Lap 3
```

while observing whether the vehicle behavior changes over time.

Important comparisons include:

```text
First corner vs later corners

Early straight sections vs late straight sections

Steering center before vs after run

Drivetrain behavior before vs after run
```

This provides evidence of repeatability across the complete challenge duration.

---

# 6.52 Multi-Lap Record

| Run | Lap 1 | Lap 2 | Lap 3 | Contacts | Mechanical Change Observed | Final Result |
| :---: | :--- | :--- | :--- | :---: | :--- | :--- |
| 1 |  |  |  |  |  |  |
| 2 |  |  |  |  |  |  |
| 3 |  |  |  |  |  |  |

This table should reflect actual current testing rather than only successful demonstrations.

---

# 6.53 Repeatability Metric

A useful way to summarize repeated tests is:

```text
SUCCESS_RATE =
SUCCESSFUL_RUNS
/
TOTAL_RUNS
× 100
```

For example, if a particular maneuver is attempted `N` times:

```text
SUCCESS_RATE =
N_SUCCESS / N × 100
```

The exact success rate should only be reported after enough current trials have been recorded.

This metric is useful for:

```text
Corners

Obstacle avoidance

Parking

Full runs
```

but the definition of “successful” should be stated clearly for each test.

---

# 6.54 Mean Measurement

For repeated numerical measurements:

```text
X_1, X_2, ..., X_N
```

the arithmetic mean is:

```text
X_MEAN =
(X_1 + X_2 + ... + X_N) / N
```

This can be used for measurements such as:

```text
Travel distance

Turning radius

Lateral deviation

Recovery distance
```

when quantitative data is collected.

---

# 6.55 Measurement Spread

The average alone does not describe repeatability.

Two sets of results can have the same mean while having very different variation.

For example:

```text
SET A

100
101
99
100
```

and:

```text
SET B

80
120
90
110
```

can have similar averages but very different consistency.

Therefore, mechanical testing should preserve individual trial data rather than only the final average.

---

# 6.56 Standard Deviation

When enough quantitative trials are available, standard deviation can be used to describe variation.

For a set of measurements:

```text
X_1 ... X_N
```

the sample standard deviation can be represented as:

```text
s =
sqrt(
SUM((X_i - X_MEAN)^2)
/
(N - 1)
)
```

A smaller spread indicates more consistent measurements under the tested conditions.

This statistic should only be reported when based on real recorded measurements.

---

# 6.57 Failure Classification

Not every unsuccessful run has the same cause.

Mechanical test failures can be classified into categories:

| Category | Example |
| :--- | :--- |
| **Steering** | Linkage did not reach expected position |
| **Drivetrain** | Wheel movement inconsistent |
| **Structural** | Component shifted during run |
| **Traction** | Wheel slip changed displacement |
| **Sensor mounting** | Sensor orientation changed |
| **Integration** | Cable interfered with moving mechanism |
| **Unknown** | Cause not yet isolated |

This prevents all failures from being grouped into one vague category.

---

# 6.58 Root-Cause Process

When a mobility problem appears, the investigation should follow the physical system.

Example:

```text
Robot hits inner wall
        ↓
Was steering physically correct?
        ↓
Was steering center correct?
        ↓
Was lateral sensor still aligned?
        ↓
Was drivetrain speed consistent?
        ↓
Only then evaluate software command
```

The same approach can be represented as:

```text
OBSERVE FAILURE
      ↓
CHECK MECHANICS
      ↓
CHECK SENSOR GEOMETRY
      ↓
CHECK ACTUATION
      ↓
CHECK SOFTWARE
      ↓
MODIFY ONE VARIABLE
      ↓
RETEST
```

This makes the development process more traceable.

---

# 6.59 One-Variable-at-a-Time Testing

Changing many parameters simultaneously makes it difficult to determine which change caused the result.

For example:

```text
Steering angle changed
+
Drive speed changed
+
Sensor target changed
```

followed by improved behavior does not reveal which modification was responsible.

A stronger engineering process is:

```text
Baseline
   ↓
Change one parameter
   ↓
Test
   ↓
Record result
   ↓
Keep or revert
```

This principle applies especially to:

```text
Motor A speed

Motor B steering strength

Steering-center calibration

Mechanical linkage geometry
```

---

# 6.60 Before-and-After Evidence

When a mechanical change is significant, evidence should show both:

```text
BEFORE
```

and:

```text
AFTER
```

where available.

Examples include:

```text
Old steering mechanism
vs.
Current steering mechanism


Old sensor mount
vs.
Current sensor mount


Previous chassis
vs.
Final chassis
```

This helps demonstrate why the current mechanical design was selected.

Visual evolution evidence is available through:

[Robot Version Photos](../../v-photos/README.md)

---

# 6.61 Video Evidence

Videos provide valuable evidence for mobility behavior because many important properties are dynamic.

Useful recordings include:

```text
Straight-line test

Steering motion

Corner execution

Obstacle avoidance

Recovery

Reverse movement

Parking

Full lap
```

Repository video references can be organized through:

[Video Evidence](../../videos/links.md)

Each video should ideally identify:

```text
What is being tested

Robot configuration

Expected behavior

Relevant result
```

rather than being uploaded without context.

---

# 6.62 Evidence Hierarchy

Different evidence formats answer different questions.

```text
PHOTO
   ↓
Shows physical configuration


GIF
   ↓
Shows mechanism movement


VIDEO
   ↓
Shows complete dynamic behavior


MEASUREMENT TABLE
   ↓
Provides quantitative comparison


CODE / LOG
   ↓
Shows commanded behavior
```

The strongest mechanical documentation combines several forms rather than relying on only one.

---

# 6.63 Testing vs. Demonstration

A successful demonstration and a structured test are not the same thing.

A demonstration answers:

> Can Piolín perform this maneuver?

A test answers:

> How consistently can Piolín perform this maneuver under defined conditions?

For engineering documentation, both are useful.

However, repeatability requires:

```text
Multiple trials

Defined conditions

Recorded outcomes
```

rather than only one successful video.

---

# 6.64 Suggested Current Mechanical Test Matrix

The following matrix organizes the most important mechanical validations.

| Test | Primary Subsystem | Quantitative? | Recommended Evidence |
| :--- | :--- | :---: | :--- |
| Steering center | Steering | Partially | Photo + straight run |
| Steering range | Steering | Optional | GIF / video |
| Steering repeatability | Steering | Yes/observational | Table + video |
| Straight-line movement | Drivetrain | Yes | Measurement table |
| Encoder-distance relation | Drivetrain | Yes | Table |
| Forward/reverse symmetry | Drivetrain | Yes | Table + video |
| Turning radius | Steering + mobility | Yes | Measurement table |
| Left/right symmetry | Steering | Yes | Table |
| Corner repeatability | Full mobility | Yes | Video + run table |
| Clockwise vs. counterclockwise | Full mobility | Yes | Run table |
| Obstacle bypass | Steering + drive | Yes | Video + success table |
| Post-pillar recovery | Full mobility | Yes | Video |
| Sensor mount stability | Structure | Observational | Before/after photos |
| Multi-lap behavior | Full system | Yes | Video + run log |

The values should be filled only with current measured results.

---

# 6.65 Current Mechanical Acceptance Philosophy

A subsystem should not be considered validated merely because it moves.

For example:

```text
Motor B moves
```

does not automatically mean:

```text
Steering is reliable
```

Likewise:

```text
Motor A rotates wheels
```

does not automatically mean:

```text
Drivetrain is repeatable
```

Mechanical validation requires observing whether the behavior is:

```text
Controlled

Repeatable

Compatible with navigation

Mechanically safe

Suitable for complete runs
```

This distinction improves the quality of the engineering evidence.

---

# 6.66 Connection to Software Tuning

Mechanical testing should establish a stable baseline before software gains or steering constants are finalized.

The relationship is:

```text
Mechanical baseline
        ↓
Sensor baseline
        ↓
Control tuning
        ↓
Course testing
```

If the mechanism changes after software tuning:

```text
Mechanical response changes
        ↓
Previous software tuning
may no longer be optimal
```

This is why mechanical revisions and software revisions should be tracked together.

---

# 6.67 Connection to Reproducibility

Mechanical testing also supports reproducibility.

A second build of Piolín should be able to verify that its physical behavior is comparable to the documented robot before running full competition software.

Useful reconstruction checks include:

```text
Correct dimensions

Correct wheel sizes

Steering centers correctly

Drivetrain rotates freely

Sensors remain fixed

Vehicle can move straight

Vehicle can steer both directions
```

This creates a bridge between:

[Reproducibility Documentation](../reproducibility/)

and the mechanical system.

---

# 6.68 Confirmed Values vs. Test Results

This document separates two categories of information.

### Confirmed physical specifications

```text
Length = 210 mm

Width = 150 mm

Height = 230 mm

Mass = 0.80476 kg

Front wheel diameter = 38.1 mm

Rear wheel diameter ≈ 61.0 mm
```

These describe the current robot.

### Experimental performance results

Examples include:

```text
Turning radius

Straight-line deviation

Encoder distance error

Steering repeatability

Corner success rate

Obstacle success rate
```

These should only be included after actual current tests have been completed and recorded.

This prevents historical or estimated values from being presented as final performance data.

---

# 6.69 Legacy Results Are Not Current Test Results

Old Piolín development documents contain previous measurements from different architectures.

Those values may involve:

```text
Different sensor arrangements

Different camera systems

Different controller concepts

Different mechanical geometry

Different software
```

They should not be transferred into the current mechanical testing tables.

Historical data is preserved separately in:

[Legacy Performance Testing and Analysis](../legacy/03_PTesting&Analysis.md)

The rule is:

```text
Legacy measurement
      ≠
Current validation result
```

unless the measurement has been repeated and confirmed on the final robot.

---

# 6.70 Testing Workflow

The recommended mechanical validation workflow is:

```text
1. VISUAL INSPECTION
        ↓
2. CHASSIS CHECK
        ↓
3. DRIVETRAIN FREE-MOTION CHECK
        ↓
4. STEERING CENTER
        ↓
5. STEERING RANGE
        ↓
6. STEERING REPEATABILITY
        ↓
7. STRAIGHT-LINE TEST
        ↓
8. ENCODER / DISTANCE TEST
        ↓
9. TURNING TEST
        ↓
10. CORNER TEST
        ↓
11. REVERSE TEST
        ↓
12. OBSTACLE MANEUVER
        ↓
13. FULL LAP
        ↓
14. MULTI-LAP VALIDATION
```

This order moves from simple isolated mechanisms toward increasingly complex integrated behavior.

---

# 6.71 Mechanical Test Decision Tree

When a test fails:

```text
                     TEST FAILED
                          │
                          ▼
                 Visible mechanical issue?
                    /             \
                  YES              NO
                   │                │
                   ▼                ▼
             Repair mechanics    Check actuation
                                      │
                                      ▼
                              Motor response correct?
                                 /           \
                               NO             YES
                               │               │
                               ▼               ▼
                         Fix actuation     Check sensor geometry
                                               │
                                               ▼
                                       Sensor stable/correct?
                                          /          \
                                        NO            YES
                                        │              │
                                        ▼              ▼
                                   Fix mounting    Review software
```

This prevents immediately modifying software when the failure originates elsewhere.

---

# 6.72 Final Testing Evidence Package

For a strong final repository, the mechanical section should ideally contain evidence for:

```text
Current chassis

Current steering mechanism

Steering GIF

Straight mobility

Corner behavior

Obstacle maneuver

Reverse / parking movement

Repeated full-run behavior
```

along with numerical tables where measurements are available.

The goal is to create the traceability chain:

```text
DESIGN CLAIM
      ↓
PHYSICAL ROBOT
      ↓
TEST METHOD
      ↓
EVIDENCE
      ↓
RESULT
```

This allows another team or judge to understand not only what Piolín was designed to do, but how the team verified that behavior.

---

# 6.73 Relationship to Other Testing Documentation

This document focuses specifically on **mechanical and mobility validation**.

Other testing areas are documented separately.

For sensor calibration and sensor-specific procedures:

[Sensor Calibration](../power_sensors/05_Calibration.md)

For the complete reproducibility testing sequence:

[Testing Protocol](../reproducibility/07_TestingProtocol.md)

For parking-specific validation:

[Parking Testing](../software_obstacles_strategy/parking/05_Parkingtesting.md)

For software tuning:

[Software Tuning](../software_obstacles_strategy/07_softwaretuning.md)

This avoids placing every type of testing in a single document.

---

# 6.74 Mechanical Testing Summary

Piolín's mechanical testing process verifies whether the physical vehicle provides a sufficiently consistent platform for autonomous control.

The complete process evaluates:

```text
STRUCTURE
   ↓
Is the robot mechanically stable?


STEERING
   ↓
Does Motor B produce repeatable wheel motion?


DRIVETRAIN
   ↓
Does Motor A produce repeatable displacement?


MOBILITY
   ↓
Can propulsion and steering produce
controlled vehicle trajectories?


INTEGRATION
   ↓
Do mechanical systems remain stable
during complete autonomous runs?
```

The confirmed current physical baseline is:

```text
Length        = 210 mm

Width         = 150 mm

Height        = 230 mm

Mass          = 0.80476 kg

Front wheels  = 38.1 mm diameter

Rear wheels   ≈ 61.0 mm diameter

Drive         = Motor A

Steering      = Motor B

Steering type = Ackermann-style
```

The testing process deliberately does not invent final performance values.

Measurements such as:

```text
Turning radius

Encoder error

Straight-line deviation

Corner success rate

Obstacle success rate

Parking repeatability
```

should be reported only after they are measured on the current robot.

The central validation principle is:

```text
BUILD
  ↓
MEASURE
  ↓
OBSERVE
  ↓
COMPARE
  ↓
IDENTIFY CAUSE
  ↓
MODIFY
  ↓
RETEST
```

This process connects Piolín's mechanical design to real evidence and makes the mobility documentation reproducible rather than purely descriptive.

---

## Mechanical Documentation

[Mechanical Architecture](01_mecharchitecture.md)

[Chassis Design](02_chassis.md)

[Robot Mobility](03_RMobility.md)

[Steering System](04_steering.md)

[Drivetrain](05_drivetrain.md)

---

## Related Testing and Evidence

[Robot Version Photos](../../v-photos/README.md)

[Video Evidence](../../videos/links.md)

[Sensor Calibration](../power_sensors/05_Calibration.md)

[Testing Protocol](../reproducibility/07_TestingProtocol.md)

[Software Tuning](../software_obstacles_strategy/07_softwaretuning.md)

[Parking Testing](../software_obstacles_strategy/parking/05_Parkingtesting.md)

[Legacy Testing and Analysis](../legacy/03_PTesting&Analysis.md)
