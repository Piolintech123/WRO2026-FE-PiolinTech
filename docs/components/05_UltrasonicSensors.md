# 5. Ultrasonic Sensors

<div align="center">

<img
  src="../../v-photos/v4/ultrasonic_pair_top.jpg"
  alt="Piolín left and right LEGO EV3 Ultrasonic Sensors"
  width="720"
/>

<br>

<sub><b>Figure 5.1.</b> Piolín's two permanent lateral ultrasonic sensors. S2 is mounted on the left side and S3 on the right side of the vehicle.</sub>

</div>

Piolín uses **two LEGO Mindstorms EV3 Ultrasonic Sensors** as its primary source of lateral track-geometry information. Unlike several earlier versions of the robot, the current architecture does not use a permanent frontal ultrasonic sensor. Instead, both ultrasonic sensors are dedicated to observing the walls on the left and right sides of the vehicle.

Their physical assignments are fixed:

```text
S2 = LEFT Ultrasonic Sensor

S3 = RIGHT Ultrasonic Sensor
```

These two sensors remain installed in both competition configurations. During the Open Challenge, they work together with the EV3 Gyro Sensor and Color Sensor. During the Obstacle Challenge, they remain in the same ports while Pixy2.1 replaces the gyro on S1.

The decision to keep two lateral ultrasonic sensors was based on the type of information Piolín needs most consistently. A frontal sensor can indicate that something is close directly ahead, but it does not describe the robot's lateral position within the track. The two side sensors continuously provide information about the geometry surrounding the vehicle and are therefore useful during straight navigation, corner transitions, obstacle recovery, and wall protection.

---

## 5.1 Final Ultrasonic Architecture

The permanent ultrasonic architecture is simple:

```text
                         FRONT
                           ↑


      LEFT WALL                          RIGHT WALL
          │                                  │
          │                                  │
          ▼                                  ▼
       S2 LEFT          [ PIOLÍN ]        S3 RIGHT
          │                                  │
          └──────────────┬───────────────────┘
                         │
                         ▼
                     LEGO EV3
```

<div align="center">

<img
  src="../../embed/ultrasonic_sensor_architecture.png"
  alt="Piolín final two-sensor ultrasonic architecture"
  width="820"
/>

<br>

<sub><b>Figure 5.2.</b> Current ultrasonic architecture. Both sensors are mounted laterally and provide independent left and right wall measurements to the EV3.</sub>

</div>

The software first treats the sensors according to their physical sides:

```text
D_LEFT

D_RIGHT
```

Only after the course direction is known are those measurements converted into the logical roles:

```text
D_INNER

D_OUTER
```

This separation between physical identity and logical meaning is one of the most important design choices in Piolín's wall-navigation system.

---

## 5.2 Left Ultrasonic Sensor — S2

The left ultrasonic sensor is permanently connected to **EV3 Sensor Port S2**.

<div align="center">

<img
  src="../../v-photos/v4/ultrasonic_left_s2.jpg"
  alt="Piolín left LEGO EV3 Ultrasonic Sensor connected to S2"
  width="620"
/>

<br>

<sub><b>Figure 5.3.</b> Left lateral ultrasonic sensor. Its physical software identity remains LEFT regardless of the direction Piolín travels around the course.</sub>

</div>

Its direct physical measurement can be represented as:

```text
D_LEFT
```

The sensor measures the distance between its mounting position and the surface that reflects the ultrasonic signal on the left side of the robot.

The EV3 does not permanently interpret S2 as the inner-wall sensor. That would only work for one direction of travel. Instead, S2 always remains **LEFT**, while the navigation software determines whether the left wall is currently the inner or outer boundary.

This produces a cleaner software architecture because the hardware definition never changes:

```text
S2
=
LEFT
```

while navigation state decides its meaning.

---

## 5.3 Right Ultrasonic Sensor — S3

The right ultrasonic sensor is permanently connected to **EV3 Sensor Port S3**.

<div align="center">

<img
  src="../../v-photos/v4/ultrasonic_right_s3.jpg"
  alt="Piolín right LEGO EV3 Ultrasonic Sensor connected to S3"
  width="620"
/>

<br>

<sub><b>Figure 5.4.</b> Right lateral ultrasonic sensor connected to S3 and aligned with the right side of the vehicle.</sub>

</div>

Its physical measurement is represented as:

```text
D_RIGHT
```

Like S2, the right sensor maintains one permanent physical identity while its logical role changes according to course direction.

Keeping the sensor-port mapping constant is especially useful during debugging. If a program reports an unexpected `D_RIGHT` value, the team knows that the problem should be investigated through S3, its cable, its physical mount, or its software acquisition path. The meaning is not hidden behind a direction-dependent wiring convention.

---

## 5.4 Why Physical LEFT and RIGHT Are Kept Separate from INNER and OUTER

The WRO track can be driven clockwise or counterclockwise. This means that the wall considered "inner" changes with direction.

The current direction convention is:

```text
BLUE first
→ COUNTERCLOCKWISE


ORANGE first
→ CLOCKWISE
```

For counterclockwise movement:

```text
S2 LEFT
→ INNER


S3 RIGHT
→ OUTER
```

For clockwise movement:

```text
S2 LEFT
→ OUTER


S3 RIGHT
→ INNER
```

<div align="center">

<img
  src="../../embed/ultrasonic_inner_outer_mapping.png"
  alt="Dynamic inner and outer wall mapping for Piolín ultrasonic sensors"
  width="820"
/>

<br>

<sub><b>Figure 5.5.</b> Physical S2/S3 identities remain constant while the EV3 assigns the logical INNER and OUTER roles according to course direction.</sub>

</div>

Conceptually, the software performs:

```text
IF COUNTERCLOCKWISE:

D_INNER = D_LEFT
D_OUTER = D_RIGHT
```

and:

```text
IF CLOCKWISE:

D_INNER = D_RIGHT
D_OUTER = D_LEFT
```

This is much more robust than physically or logically pretending that one EV3 port is always "inner."

---

## 5.5 Why Two Lateral Sensors Were Selected

A single side sensor can be used to follow one wall, but it provides only one geometric measurement.

With one sensor:

```text
one wall distance
```

is known.

With two lateral sensors:

```text
left geometry
+
right geometry
```

are available simultaneously.

This additional information is useful because a robot can be at an acceptable distance from one wall while still being poorly positioned or rotated relative to the complete track.

<div align="center">

<img
  src="../../embed/one_vs_two_ultrasonic_sensors.png"
  alt="Comparison between one-sided and two-sided ultrasonic navigation"
  width="850"
/>

<br>

<sub><b>Figure 5.6.</b> Comparison between one-wall sensing and the two-sided geometry available from Piolín's current ultrasonic configuration.</sub>

</div>

Two sensors also provide a second environmental reference when one wall disappears at a corner. The system does not become completely blind to lateral geometry simply because the primary inner-wall reference has ended.

This was one of the main reasons for preserving both lateral sensors throughout Piolín's development.

---

## 5.6 Why the Sensors Are Mounted Laterally

Earlier experiments considered different ultrasonic orientations, including arrangements in which sensors were not perfectly lateral.

The final design keeps both ultrasonic sensors directed toward their respective sides because the navigation system is primarily concerned with **lateral wall geometry**.

<div align="center">

<img
  src="../../v-photos/v4/ultrasonic_lateral_alignment.jpg"
  alt="Lateral alignment of Piolín ultrasonic sensors"
  width="700"
/>

<br>

<sub><b>Figure 5.7.</b> Lateral orientation of the current ultrasonic sensors relative to the vehicle chassis.</sub>

</div>

A strongly diagonal sensor can detect walls earlier in some situations, but its measurement combines more forward and lateral geometry. This can make the numerical distance harder to interpret as a direct side clearance.

The final lateral arrangement favors a clearer physical meaning:

```text
LEFT sensor
→ left-side clearance


RIGHT sensor
→ right-side clearance
```

This makes both calibration and debugging easier.

---

## 5.7 Ultrasonic Measurement Principle

An ultrasonic sensor measures distance by transmitting a sound pulse and detecting the returning echo.

Conceptually:

```text
Sensor
  ↓
Transmit pulse
  ↓
Sound reaches wall
  ↓
Echo returns
  ↓
Elapsed time measured
  ↓
Distance estimated
```

The underlying physical relationship can be written as:

```text
D =
V_SOUND × T / 2
```

where:

```text
D = distance

V_SOUND = speed of sound

T = round-trip travel time
```

The division by two is required because the sound travels from the sensor to the surface and then back to the sensor.

In Piolín, the EV3 sensor interface provides the distance measurement directly to software, so the main navigation program does not need to manually calculate ultrasonic time-of-flight.

---

## 5.8 What the Ultrasonic Measurement Actually Represents

A sensor reading is the distance from the **sensor**, not automatically from the geometric center of the robot.

This distinction matters.

```text
WALL
 │
 │<------ sensor distance ------>[ SENSOR ][ ROBOT ]
```

If navigation mathematics requires the position of the chassis center, the sensor's mounting offset must be considered.

Conceptually:

```text
CENTER-REFERENCED DISTANCE
=
SENSOR READING
+
SENSOR OFFSET
```

depending on the selected coordinate convention.

<div align="center">

<img
  src="../../embed/ultrasonic_sensor_offset.png"
  alt="Difference between ultrasonic sensor distance and vehicle-center wall distance"
  width="820"
/>

<br>

<sub><b>Figure 5.8.</b> An ultrasonic reading originates at the sensor face rather than the geometric center of Piolín.</sub>

</div>

The final V4 sensor offsets should only be introduced numerically after they are physically measured. Older offsets from previous robot versions should not automatically be reused.

---

## 5.9 Sensor Height and Mounting Stability

The ultrasonic sensor mount is part of the measurement system.

A sensor whose software and electronics operate correctly can still produce poor navigation information if its physical orientation changes.

Important mounting properties include:

```text
height

horizontal orientation

lateral angle

rigidity

distance from chassis center
```

<div align="center">

<img
  src="../../v-photos/v4/ultrasonic_mount_closeup.jpg"
  alt="Piolín ultrasonic sensor mounting structure"
  width="650"
/>

<br>

<sub><b>Figure 5.9.</b> Close-up of an ultrasonic mount showing how the sensor is structurally supported by the chassis.</sub>

</div>

Loose mounting can create changing distance measurements even when the robot follows the same trajectory.

For example:

```text
sensor rotates slightly
        ↓
echo reaches different part of wall
        ↓
distance changes
        ↓
EV3 interprets false position change
        ↓
steering correction
```

For this reason, mounting rigidity is part of ultrasonic accuracy.

---

## 5.10 Normal Straight-Section Navigation

During a straight section, the inner wall usually provides the primary lateral reference.

The controller can define a desired inner-wall measurement:

```text
D_TARGET
```

and calculate a wall error:

```text
E_WALL =
D_TARGET - D_INNER
```

If:

```text
E_WALL ≈ 0
```

the robot is approximately at its intended wall reference.

If the magnitude of the error increases, Motor B can apply a corrective steering request.

<div align="center">

<img
  src="../../embed/ultrasonic_wall_following.png"
  alt="Piolín inner-wall ultrasonic control concept"
  width="850"
/>

<br>

<sub><b>Figure 5.10.</b> Inner-wall distance provides a lateral reference during normal straight-section navigation.</sub>

</div>

The exact current numerical value of `D_TARGET` belongs to calibration and software tuning. It should not be treated as a permanent physical constant because sensor position, chassis geometry, and desired trajectory can all change the correct value.

---

## 5.11 Why the Outer Sensor Is Still Important

If Piolín primarily follows the inner wall during a straight, it may appear that the outer sensor is unnecessary.

However, the outer sensor provides valuable additional information.

It can help the EV3 evaluate:

```text
overall corridor geometry

distance from the opposite wall

corner transitions

abnormal lateral position

post-maneuver recovery
```

The outer sensor therefore acts as more than a backup.

The two measurements can form a corridor relationship such as:

```text
D_INNER + D_OUTER
```

which is expected to behave differently in a normal corridor than when the surrounding geometry changes.

This allows Piolín to reason about the **shape of the environment**, not only one distance.

---

## 5.12 Dual-Sensor Corridor Geometry

A useful conceptual variable is:

```text
C_CURRENT =
D_INNER + D_OUTER
```

A reference corridor value can be represented as:

```text
C_REF
```

and geometry consistency as:

```text
G =
ABS(
C_CURRENT - C_REF
)
```

When:

```text
G is small
```

the environment may still resemble the calibrated straight corridor.

When:

```text
G becomes large
```

the geometry may have changed.

Possible reasons include:

```text
corner opening

vehicle rotation

sensor outlier

obstacle interference

unusual wall geometry
```

<div align="center">

<img
  src="../../embed/ultrasonic_corridor_geometry.png"
  alt="Piolín two-sensor corridor geometry"
  width="850"
/>

<br>

<sub><b>Figure 5.11.</b> The combination of both lateral sensor readings provides information about the current corridor geometry.</sub>

</div>

The EV3 should therefore interpret `G` together with navigation state rather than assuming that every large value automatically means one specific event.

---

## 5.13 Corner Detection

Corners create one of the most important geometric changes observed by the ultrasonic sensors.

During a normal straight:

```text
inner wall present
+
outer wall present
```

At a corner, the inner wall can end.

```text
INNER WALL
───────────────┐
               │
               │
        corner opening
```

As Piolín approaches the opening, `D_INNER` can increase rapidly.

<div align="center">

<img
  src="../../embed/ultrasonic_corner_detection.png"
  alt="Ultrasonic geometry change at a WRO corner"
  width="850"
/>

<br>

<sub><b>Figure 5.12.</b> Inner-wall disappearance produces a characteristic geometry change that can contribute to corner detection.</sub>

</div>

A large inner reading should not simply be interpreted as:

```text
robot is extremely far from wall
```

because in the correct state it may mean:

```text
the wall physically ended
```

This is why ultrasonic interpretation must be **state-aware**.

---

## 5.14 Wall Loss vs. Sensor Error

One challenge with ultrasonic navigation is distinguishing a real opening from a poor reading.

Consider two situations.

### Situation A — genuine corner

```text
wall ends
→ sensor sees open space
→ distance becomes large
```

### Situation B — measurement anomaly

```text
wall still present
→ unusual echo
→ distance becomes large
```

The numerical reading alone can look similar.

Piolín therefore benefits from considering additional evidence such as:

```text
previous readings

other ultrasonic sensor

course state

gyro during Open

color-event information
```

This reduces dependence on one isolated sample.

---

## 5.15 Outer-Wall Role During a Corner

When the inner wall disappears, the outer wall becomes temporarily more valuable.

The navigation sequence can be described as:

```text
STRAIGHT
↓
inner wall primary


CORNER APPROACH
↓
inner wall begins disappearing


TURN
↓
outer wall provides temporary geometry


CORNER EXIT
↓
new inner wall appears


STRAIGHT
↓
inner wall becomes primary again
```

<div align="center">

<img
  src="../../embed/ultrasonic_corner_sequence.png"
  alt="Piolín ultrasonic wall-reference sequence through a corner"
  width="880"
/>

<br>

<sub><b>Figure 5.13.</b> The relative importance of inner and outer ultrasonic measurements changes throughout a corner.</sub>

</div>

This strategy uses both sensors for different phases of the same maneuver rather than assigning one sensor as permanently important and the other as permanently secondary.

---

## 5.16 Inner-Wall Reacquisition

A turn should not be considered complete simply because Piolín has steered for a fixed amount of time.

After the corner, the robot should recover a recognizable lateral geometry.

One useful indicator is the reappearance of a stable inner-wall reading.

```text
TURN
 ↓
new wall enters lateral sensor view
 ↓
D_INNER returns to plausible range
 ↓
geometry stabilizes
 ↓
normal wall following resumes
```

During Open, gyro rotation can provide additional evidence that the robot has approached the expected new heading.

This creates a stronger corner-exit condition than relying only on time.

---

## 5.17 Ultrasonics and the Gyro During Open

During Open, ultrasonic sensors and the gyro measure different physical quantities.

```text
ULTRASONICS
→ lateral environmental geometry


GYRO
→ vehicle rotation / orientation
```

<div align="center">

<img
  src="../../embed/open_gyro_wall_fusion.png"
  alt="Fusion between gyro heading and ultrasonic wall geometry during Open"
  width="850"
/>

<br>

<sub><b>Figure 5.14.</b> Open navigation combines lateral geometry from S2/S3 with angular information from the Gyro Sensor on S1.</sub>

</div>

This combination was selected because neither measurement completely replaces the other.

A robot can have a reasonable wall distance while still being rotated.

Similarly, a robot can have the correct gyro heading while being laterally too close to one wall.

Conceptually:

```text
GOOD HEADING
≠
GOOD LATERAL POSITION
```

and:

```text
GOOD WALL DISTANCE
≠
GOOD HEADING
```

The current Open architecture uses both types of information to reduce this ambiguity.

---

## 5.18 Why Ultrasonic Sensors Still Matter After the Gyro Returned

Reintroducing the gyro did not make the ultrasonic sensors less important.

A gyro can measure:

```text
how much Piolín rotated
```

but it cannot directly measure:

```text
how far Piolín is from the left wall

how far Piolín is from the right wall

whether an inner wall has ended

whether the vehicle is displaced laterally
```

The gyro therefore improves orientation control but cannot replace environmental geometry.

The two ultrasonic sensors remain the primary link between Piolín and the physical track boundaries.

---

## 5.19 Ultrasonic Sensors During the Obstacle Challenge

During Obstacles, S1 is occupied by Pixy2.1 and the gyro is absent.

The two ultrasonic sensors remain connected exactly as before:

```text
S2 = LEFT

S3 = RIGHT
```

Their role changes slightly because vision becomes the main source of obstacle identity.

```text
Pixy2.1
→ what pillar is present
→ where the visual block appears


S2 / S3
→ where the surrounding walls are
```

<div align="center">

<img
  src="../../embed/obstacle_pixy_us_fusion.png"
  alt="Pixy2.1 and ultrasonic sensor fusion during obstacle navigation"
  width="860"
/>

<br>

<sub><b>Figure 5.15.</b> During Obstacles, Pixy2.1 provides visual target information while the ultrasonic pair constrains the vehicle relative to the track walls.</sub>

</div>

The sensors therefore complement each other instead of competing for the same role.

---

## 5.20 Why the Ultrasonics Should Not Override Pixy Blindly

Suppose Pixy identifies:

```text
GREEN
→ pass LEFT
```

while the left ultrasonic indicates that Piolín is already dangerously close to the left track boundary.

A vision-only controller might continue commanding a stronger leftward trajectory.

A wall-only controller might ignore the green pillar and steer away from the wall directly into the obstacle.

The desired architecture is neither extreme.

Instead:

```text
PIXY
→ desired passing strategy


ULTRASONICS
→ environmental constraints
```

and:

```text
EV3
→ final steering decision
```

This is **decision-level sensor fusion**.

---

## 5.21 Post-Obstacle Recovery

The two ultrasonic sensors become especially important after Piolín has passed a pillar.

During avoidance, the robot can become laterally displaced.

Once the obstacle is no longer the main concern:

```text
Pixy influence decreases
        ↓
wall geometry becomes more important
        ↓
Motor B countersteers
        ↓
Piolín returns toward stable path
```

<div align="center">

<img
  src="../../embed/obstacle_recenter.png"
  alt="Ultrasonic-assisted recentering after obstacle avoidance"
  width="850"
/>

<br>

<sub><b>Figure 5.16.</b> Post-pillar recovery uses left/right wall geometry to help Piolín return toward a stable course trajectory.</sub>

</div>

This makes the lateral ultrasonic pair useful throughout the entire Obstacle Challenge rather than only between pillars.

---

## 5.22 Detecting That a Pillar Has Been Passed

Vision loss alone does not prove that a pillar has been fully passed.

A block may disappear because:

```text
robot turned

camera field of view shifted

pillar became occluded

pillar moved outside image
```

One development strategy is therefore to use changes in lateral ultrasonic geometry as additional evidence that the vehicle has moved alongside and then beyond the obstacle.

Conceptually:

```text
pillar approached
      ↓
lateral geometry changes
      ↓
vehicle passes obstacle
      ↓
geometry opens / changes again
      ↓
pillar considered passed
```

The exact final pass-confirmation logic belongs to the obstacle software, but the ultrasonic sensors provide a physical source of information that can support this decision.

---

## 5.23 Why the Front Ultrasonic Sensor Was Removed

Earlier Piolín versions used a third ultrasonic sensor facing forward.

That architecture had an obvious advantage: it provided direct frontal clearance information.

However, the EV3 has only four sensor ports.

The final robot requires:

```text
S2
→ left wall


S3
→ right wall


S4
→ floor color
```

leaving only:

```text
S1
```

for a round-specific sensor.

The design decision therefore became:

```text
permanent front distance
```

versus:

```text
gyro orientation in Open
+
Pixy vision in Obstacles
```

<div align="center">

<img
  src="../../embed/three_us_vs_modular_s1.png"
  alt="Comparison between three-ultrasonic architecture and modular S1 architecture"
  width="880"
/>

<br>

<sub><b>Figure 5.17.</b> The permanent front ultrasonic was removed so S1 could provide higher-value round-specific information.</sub>

</div>

The front sensor was useful, but the gyro and Pixy provide types of information that cannot be reproduced effectively by the two side ultrasonic sensors.

The final architecture therefore prioritizes those specialized inputs.

---

## 5.24 Two Sensors vs. Three Sensors

The comparison is not simply:

```text
three sensors are better than two
```

because every additional sensor also occupies hardware resources and creates another data stream the software must interpret.

| Architecture | Advantage | Limitation |
| :--- | :--- | :--- |
| One lateral ultrasonic | Minimal hardware | Only one side of track directly observed |
| Two lateral ultrasonics | Strong two-sided geometry | No direct frontal range |
| Three ultrasonics | Adds frontal safety information | Uses S1 permanently |
| **Two lateral + modular S1** | **Preserves wall geometry while allowing Gyro or Pixy** | **Front distance must be handled without dedicated frontal US** |

The final configuration was selected because the S1 information changes the robot's capabilities more substantially than the permanent frontal distance measurement.

---

## 5.25 Why Ultrasonic Sensors Were Kept Instead of Using Only Vision

During the Obstacle Challenge, Piolín already has Pixy2.1.

It might therefore appear possible to use the camera for wall navigation as well.

That would create several disadvantages.

Camera measurements depend on:

```text
lighting

visible features

field of view

image interpretation

camera orientation
```

The ultrasonic sensors provide direct geometric range information without needing to recognize the visual appearance of the walls.

Similarly, the Open Challenge does not require a camera at all.

The ultrasonic sensors therefore remain a simpler and more direct tool for track-wall geometry.

This follows the same design principle used throughout Piolín:

> Use each sensor for the physical quantity it measures most directly.

---

## 5.26 Why Ultrasonic Sensors Were Kept Instead of Using Only the Gyro

A gyro can stabilize orientation, but orientation is not position.

Consider two robots:

```text
Robot A:
correct heading
close to inner wall


Robot B:
correct heading
close to outer wall
```

The gyro could report approximately the same orientation for both.

The ultrasonic pair distinguishes them immediately.

<div align="center">

<img
  src="../../embed/heading_vs_lateral_position.png"
  alt="Difference between heading and lateral position"
  width="850"
/>

<br>

<sub><b>Figure 5.18.</b> Identical or similar gyro heading does not imply identical lateral position within the track.</sub>

</div>

This is why the gyro and lateral sensors are complementary rather than interchangeable.

---

## 5.27 Ultrasonic Beam Geometry

An ultrasonic sensor does not measure distance along an infinitely thin mathematical ray.

The emitted sound occupies a finite region.

Conceptually:

```text
        \       /
         \     /
          \   /
           \ /
        [ SENSOR ]
```

This means the detected echo may come from a surface located within the sensor's effective beam rather than exactly along the centerline.

<div align="center">

<img
  src="../../embed/ultrasonic_beam_geometry.png"
  alt="Conceptual ultrasonic beam geometry"
  width="800"
/>

<br>

<sub><b>Figure 5.19.</b> Ultrasonic sensing covers a finite region, so observed geometry depends on both distance and surface orientation.</sub>

</div>

This becomes important near:

```text
corners

angled walls

pillar edges

openings
```

because the returned echo can change abruptly even when the chassis moves only slightly.

---

## 5.28 Effect of Robot Angle on Ultrasonic Readings

A lateral sensor provides the clearest wall-distance interpretation when the robot is approximately aligned with the wall.

When Piolín rotates:

```text
sensor orientation relative to wall changes
```

and the measured distance can change before the vehicle has significantly translated laterally.

<div align="center">

<img
  src="../../embed/steering_ultrasonic_geometry.png"
  alt="Effect of Piolín yaw angle on lateral ultrasonic measurements"
  width="850"
/>

<br>

<sub><b>Figure 5.20.</b> Steering and vehicle rotation change the geometry observed by the lateral sensors.</sub>

</div>

This means that:

```text
distance change
```

does not always equal:

```text
pure lateral displacement
```

During Open, gyro information helps distinguish orientation from lateral positioning.

During Obstacles, navigation state and the opposite sensor provide additional context.

---

## 5.29 Sensor Noise and Isolated Outliers

Ultrasonic readings can occasionally contain values that do not represent the normal local geometry.

For example:

```text
248 mm
251 mm
693 mm
```

If the physical situation is known to be stable, the third reading may be an isolated outlier.

A short median filter can reduce the effect of such a sample.

Sorting:

```text
248
251
693
```

gives:

```text
MEDIAN = 251 mm
```

A median is useful because one extreme value has less influence than it would have on an arithmetic mean.

This numerical example is illustrative and is not presented as a recorded V4 calibration dataset.

---

## 5.30 Filtering Trade-Off

Filtering improves stability but introduces a trade-off.

More filtering can provide:

```text
smoother measurements

better outlier rejection
```

but can also produce:

```text
slower reaction
```

This is especially important at corners, where a rapidly changing distance may be a real geometric event rather than noise.

Therefore:

```text
large sudden change
```

should not automatically be filtered away.

A good navigation system distinguishes:

```text
unexpected isolated sample
```

from:

```text
persistent geometry transition
```

using both measurement history and current state.

---

## 5.31 Temporal Confirmation

One way to distinguish isolated readings from real changes is to require confirmation across more than one sample.

Conceptually:

```text
possible wall loss
      ↓
next measurement
      ↓
still indicates opening?
      ↓
YES
      ↓
stronger evidence of corner
```

However, excessive confirmation can delay steering.

At vehicle speed, every additional sensor cycle corresponds to additional physical travel.

Therefore the confirmation strategy must balance:

```text
false detection rejection
```

against:

```text
reaction delay
```

The final number of samples should come from the current controller implementation rather than being assumed universally.

---

## 5.32 Ultrasonic Sensors and Vehicle Speed

Sensor usefulness depends on how far the robot travels between control updates.

At greater speed:

```text
more distance is covered
before the next correction
```

A wall-following controller that performs well slowly may begin oscillating or reacting too late when Motor A speed increases.

This interaction can be represented conceptually as:

```text
SENSOR SAMPLE
      ↓
EV3 CALCULATION
      ↓
MOTOR B RESPONSE
      ↓
VEHICLE MOVES
      ↓
NEXT SAMPLE
```

<div align="center">

<img
  src="../../embed/ultrasonic_control_timing.png"
  alt="Relationship between ultrasonic sampling, control response, and vehicle motion"
  width="850"
/>

<br>

<sub><b>Figure 5.21.</b> Vehicle speed affects how much physical movement occurs between sensing and corrective steering actions.</sub>

</div>

Therefore, ultrasonic tuning and drive-speed tuning cannot be completely separated.

---

## 5.33 Wall Following and Zig-Zag

If the ultrasonic controller responds too strongly to small changes, the robot can enter an oscillating path.

```text
too close
→ steer away strongly

then

too far
→ steer back strongly

then repeat
```

This produces zig-zag.

Possible causes include:

```text
steering gain too strong

measurement noise

vehicle speed too high

steering center error

insufficient deadband

mechanical steering delay
```

The presence of two ultrasonic sensors can help diagnose this behavior by showing whether the complete corridor geometry is actually moving as expected.

A zig-zag problem should therefore not automatically be treated as an ultrasonic hardware failure.

---

## 5.34 Wall Safety

The lateral sensors can also support protection against approaching a wall too closely.

Normal wall following attempts to maintain a target trajectory.

Wall safety has a different purpose:

```text
normal control
→ maintain desired path


safety control
→ avoid physically dangerous clearance
```

If one sensor indicates a much smaller-than-expected wall distance, the EV3 can apply a stronger correction or reduce propulsion according to the active software strategy.

This layer is especially important during obstacle avoidance because Pixy-based steering may temporarily request movement toward one side of the track.

The ultrasonic sensors therefore act both as navigation references and as geometric constraints.

---

## 5.35 Sensor Priority Is State-Dependent

There is no single universal priority between:

```text
left ultrasonic

right ultrasonic

gyro

Pixy

color sensor
```

The useful sensor depends on the current state.

During an Open straight:

```text
inner wall
+
gyro
```

are highly important.

During an Open corner:

```text
wall transition
+
gyro rotation
+
outer geometry
```

gain importance.

During obstacle approach:

```text
Pixy target
+
wall safety
```

become important.

After the pillar:

```text
left/right ultrasonic geometry
```

becomes increasingly important for recovery.

This state-dependent interpretation is more flexible than assigning one sensor permanent authority over Motor B.

---

## 5.36 Ultrasonic Sensor Failure Modes

Several failure modes can affect ultrasonic navigation.

| Observed Behavior | Possible Cause |
| :--- | :--- |
| Reading remains constant | Sensor/cable/software acquisition issue |
| Left/right values reversed | S2/S3 mapping incorrect |
| Reading suddenly becomes very large at corner | Possibly valid wall disappearance |
| Large value on normal straight | Echo/outlier/mounting issue |
| Robot consistently hugs one wall | Target calibration or steering-center error |
| Robot oscillates | Gain, noise, speed, deadband, or mechanical response |
| Different values after chassis rebuild | Sensor mounting position changed |
| Poor obstacle recovery | Wall geometry not reacquired correctly |
| Both values appear unusual simultaneously | Vehicle orientation or non-standard geometry |
| One side varies when cable moves | Loose connection or unstable mount |

The important diagnostic principle is that the numerical reading should always be interpreted together with the physical situation.

---

## 5.37 Diagnostic Order

When an ultrasonic-related problem occurs, the preferred diagnostic sequence is:

```text
1. Verify S2 = LEFT
        ↓
2. Verify S3 = RIGHT
        ↓
3. Inspect physical mounts
        ↓
4. Observe raw readings
        ↓
5. Compare readings with real wall movement
        ↓
6. Inspect filtering
        ↓
7. Inspect INNER / OUTER assignment
        ↓
8. Inspect current navigation state
        ↓
9. Inspect steering response
        ↓
10. Tune control parameters
```

This avoids changing controller gains to compensate for incorrect wiring or unstable hardware.

---

## 5.38 Comparison with Alternative Track-Sensing Methods

Several sensing approaches could theoretically provide information about the course.

| Sensing Method | Strength | Limitation for Piolín |
| :--- | :--- | :--- |
| Single ultrasonic | Simple | Only one wall directly observed |
| Three ultrasonics | Adds frontal distance | Occupies S1 permanently |
| Gyro only | Strong orientation reference | Does not measure lateral position |
| Camera-based wall detection | Rich visual information | More processing and lighting dependence |
| Line tracking | Strong if a continuous line exists | Does not directly describe wall geometry |
| **Two lateral ultrasonics** | **Direct left/right environmental geometry with low integration complexity** | **No dedicated frontal distance** |

The selected architecture provides the type of measurement most consistently useful across both competition rounds while leaving S1 free for the sensor that each round specifically requires.

---

## 5.39 Current Ultrasonic Architecture Compared with Earlier Piolín Versions

Piolín's ultrasonic architecture changed several times during development.

Earlier versions included:

```text
different S2/S3 assignments

diagonal sensor experiments

frontal ultrasonic sensing

gyro-free navigation

three-ultrasonic layouts
```

The current version simplifies the physical sensing map to:

```text
S2
=
LEFT


S3
=
RIGHT
```

<div align="center">

<img
  src="../../embed/evolution_ultrasonic_architecture.png"
  alt="Evolution of Piolín ultrasonic sensor architecture"
  width="880"
/>

<br>

<sub><b>Figure 5.22.</b> Evolution from experimental sensor arrangements toward the current permanent two-lateral-sensor configuration.</sub>

</div>

This structure was selected because it is easier to reproduce, easier to interpret in software, and compatible with the modular S1 strategy.

---

## 5.40 Current Values Intentionally Not Claimed as Final

Several numerical properties should only be documented after they are measured on the current V4 physical robot.

These include:

```text
final lateral sensor height

left sensor lateral offset

right sensor lateral offset

final D_TARGET

final C_REF

geometry tolerance

wall safety threshold

corner wall-loss threshold

inner-wall reacquisition threshold

median/filter length

confirmation count

maximum reliable range in current mounting

measured sensor error
```

Earlier development values may remain useful as historical evidence, but they should not automatically be treated as current calibration constants.

This is especially important because changing the chassis or sensor mount can change the numerical value required to follow the same physical trajectory.

---

## 5.41 Current Ultrasonic Responsibility Matrix

| Function | S2 Left | S3 Right |
| :--- | :---: | :---: |
| Permanent physical identity | LEFT | RIGHT |
| Counterclockwise inner wall | Yes | No |
| Counterclockwise outer wall | No | Yes |
| Clockwise inner wall | No | Yes |
| Clockwise outer wall | Yes | No |
| Straight wall geometry | Yes | Yes |
| Corner context | Yes | Yes |
| Wall protection | Yes | Yes |
| Obstacle recovery | Yes | Yes |
| Open Challenge | Yes | Yes |
| Obstacle Challenge | Yes | Yes |

The ultrasonic pair is therefore one of the few sensing subsystems that remains active and physically unchanged across both rounds.

---

## 5.42 Final Engineering Assessment

Piolín's ultrasonic system was selected because it provides direct, low-complexity information about the geometry surrounding the vehicle.

The sensors do not attempt to determine everything about navigation.

They answer a specific physical question:

> **How is Piolín positioned relative to the track boundaries on its left and right sides?**

During Open, that information is combined with gyro orientation and color-based course state.

During Obstacles, it is combined with Pixy visual information and color-based course state.

```text
                         S2 LEFT
                            │
                            ▼
                       LEFT GEOMETRY
                            │
                            │
                            ▼
                           EV3
                            ▲
                            │
                            │
                       RIGHT GEOMETRY
                            ▲
                            │
                         S3 RIGHT
```

<div align="center">

<img
  src="../../v-photos/v4/ultrasonic_pair_top.jpg"
  alt="Piolín final two-sensor ultrasonic configuration"
  width="720"
/>

<br>

<sub><b>Figure 5.23.</b> Current ultrasonic subsystem. The simple permanent S2-left / S3-right arrangement supports both competition challenges.</sub>

</div>

The final design demonstrates an important engineering principle: **more sensors do not automatically create a better robot**. The value of a sensor depends on whether the information it provides is distinct, useful, reliable, and worth the hardware and software resources it consumes.

For Piolín, two permanent lateral ultrasonic sensors provide the strongest balance between environmental awareness, port availability, control simplicity, and compatibility with the round-specific Gyro/Pixy architecture.

---

<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
