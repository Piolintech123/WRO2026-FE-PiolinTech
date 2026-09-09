# 6. Color Sensor and Course-State Detection

<div align="center">

<img
  src="../../v-photos/v4/color_sensor_s4_installed.jpg"
  alt="LEGO EV3 Color Sensor installed underneath Piolín"
  width="680"
/>

<br>

<sub><b>Figure 6.1.</b> LEGO Mindstorms EV3 Color Sensor installed underneath Piolín and connected permanently to Sensor Port S4.</sub>

</div>

Piolín uses one **LEGO Mindstorms EV3 Color Sensor** connected permanently to **Sensor Port S4**. The sensor is mounted facing downward toward the competition mat and remains part of the robot in both the Open Challenge and the Obstacle Challenge.

Unlike the ultrasonic sensors, the Color Sensor does not primarily describe the robot's geometric position relative to the track. Unlike the Gyro Sensor, it does not directly measure vehicle rotation. Unlike Pixy2.1, it does not identify traffic pillars in front of the robot.

Its responsibility is different.

The Color Sensor provides **course-state information** by detecting the colored floor markings placed on the track. These markings act as physical landmarks that allow the EV3 to determine the initial travel direction and track progression through the course.

The sensor therefore answers a different question from the rest of Piolín's sensing system:

```text
Ultrasonics:
Where am I relative to the walls?


Gyro:
How is my orientation changing?


Pixy2.1:
Which obstacle is in front of me?


Color Sensor:
Which course landmark have I reached?
```

This separation of responsibilities is one of the reasons the Color Sensor remains a permanent component even though Piolín uses different specialized sensors on S1 for each competition round.

---

## 6.1 Final Color-Sensor Architecture

The current physical connection is fixed:

```text
EV3 Sensor Port S4
        ↓
LEGO EV3 Color Sensor
        ↓
Competition floor
```

<div align="center">

<img
  src="../../embed/color_sensor_architecture.png"
  alt="Piolín color sensor architecture"
  width="800"
/>

<br>

<sub><b>Figure 6.2.</b> The S4 Color Sensor converts physical floor markings into course-state information used by the EV3.</sub>

</div>

The sensor remains connected to S4 in both configurations:

| Configuration | S4 Component | Main Role |
| :--- | :--- | :--- |
| **Open Challenge** | EV3 Color Sensor | Initial direction and course progression |
| **Obstacle Challenge** | EV3 Color Sensor | Initial direction and course progression |

This permanent assignment avoids unnecessary rewiring and gives both programs access to the same external course landmarks.

---

## 6.2 Physical Placement

The Color Sensor is mounted beneath Piolín and faces downward.

<div align="center">

<img
  src="../../v-photos/v4/color_sensor_bottom_view.jpg"
  alt="Bottom view of Piolín showing the downward-facing Color Sensor"
  width="680"
/>

<br>

<sub><b>Figure 6.3.</b> Bottom view showing the Color Sensor positioned close to the competition surface.</sub>

</div>

This orientation is important because the sensor must observe the reflected light from the floor rather than objects in front of or beside the robot.

The physical mounting affects the quality of the measurement. Relevant factors include:

```text
sensor-to-floor distance

sensor angle

surrounding illumination

casing geometry

floor material

vehicle movement
```

A software threshold that works with one physical mounting position may not work identically if the sensor height or casing changes.

For this reason, Color Sensor calibration belongs to the complete installed robot rather than to the sensor alone.

---

## 6.3 Why the Color Sensor Is Used for Course State

Piolín could theoretically estimate its progression using:

```text
wheel encoders

gyro rotation

elapsed time

camera observations
```

However, each of these methods accumulates uncertainty.

Wheel encoders estimate rotation of the drivetrain, but wheel slip and turning can create differences between encoder motion and actual track displacement.

The gyro measures rotation, but it does not directly identify which physical corner or lap the robot has reached.

Elapsed time changes with battery condition, vehicle speed, steering corrections, and obstacle maneuvers.

Pixy2.1 is useful for obstacle recognition, but it is only installed during the Obstacle Challenge and is not needed for Open navigation.

The floor markings provide something different:

> **A physical external reference fixed to the competition course.**

The EV3 can therefore use the Color Sensor to correct uncertainty accumulated by internal movement estimates.

<div align="center">

<img
  src="../../embed/course_state_reference_comparison.png"
  alt="Comparison of internal odometry and physical floor landmarks"
  width="850"
/>

<br>

<sub><b>Figure 6.4.</b> Physical floor landmarks provide an external course reference that does not depend entirely on accumulated encoder, gyro, or time estimates.</sub>

</div>

---

## 6.4 Initial Direction Detection

One of the first important responsibilities of S4 is determining the direction in which Piolín should navigate the course.

The current convention is:

```text
BLUE first
→ COUNTERCLOCKWISE
```

and:

```text
ORANGE first
→ CLOCKWISE
```

<div align="center">

<img
  src="../../embed/color_direction_logic.png"
  alt="Blue and orange initial direction logic"
  width="820"
/>

<br>

<sub><b>Figure 6.5.</b> The first valid floor-color event determines the initial course direction.</sub>

</div>

This information is important because direction determines how several other sensors are interpreted.

For counterclockwise travel:

```text
S2 LEFT
→ INNER

S3 RIGHT
→ OUTER
```

For clockwise travel:

```text
S2 LEFT
→ OUTER

S3 RIGHT
→ INNER
```

The Color Sensor therefore does not directly steer Piolín, but its first valid event changes the meaning of the wall-navigation system.

---

## 6.5 Direction Is a State, Not a Continuous Color Command

Once the initial direction has been determined, later floor detections should not continuously redefine the robot's travel direction.

Conceptually:

```text
START
  ↓
No direction known
  ↓
First valid BLUE or ORANGE event
  ↓
Direction selected
  ↓
Direction locked
```

After this point, later floor markings represent **course progression**, not a new direction decision.

This distinction is important because the robot encounters additional colored floor regions while moving through the course.

The software should therefore separate:

```text
INITIAL COLOR EVENT
```

from:

```text
PROGRESS COLOR EVENT
```

even though both originate from the same physical sensor.

---

## 6.6 Color Sensor as a Course Landmark Detector

Once direction has been established, the Color Sensor becomes a progress-tracking sensor.

The basic concept is:

```text
Physical floor mark
        ↓
S4 detects color
        ↓
EV3 validates event
        ↓
course counter updates
        ↓
navigation state advances
```

<div align="center">

<img
  src="../../embed/color_course_state_logic.png"
  alt="Color Sensor course-state processing"
  width="850"
/>

<br>

<sub><b>Figure 6.6.</b> A physical floor marking becomes a navigation event only after the EV3 validates the sensor detection.</sub>

</div>

Piolín's intended three-lap navigation requires recognizing course progression through the repeated corners of the track.

The current architecture uses valid floor events as external landmarks rather than depending only on estimated traveled distance.

This provides a clearer relationship between:

```text
physical track event
```

and:

```text
software course state
```

---

## 6.7 Physical Marking vs. Raw Sensor Samples

One of the most important software distinctions is:

```text
ONE PHYSICAL MARKING
≠
ONE RAW SENSOR SAMPLE
```

While Piolín moves across one colored strip, the EV3 can read the sensor many times.

For example:

```text
BLUE
BLUE
BLUE
BLUE
BLUE
```

may all belong to one physical strip.

If every reading were counted independently, the course counter could increase several times while the robot had physically crossed only one landmark.

The correct goal is:

```text
ONE PHYSICAL MARKING
        ↓
ONE VALID EVENT
```

rather than:

```text
ONE SENSOR SAMPLE
        ↓
ONE EVENT
```

This is why the Color Sensor requires an **event-processing layer** in addition to basic color classification.

---

## 6.8 Event Locking

One method for preventing repeated counts is to use an event lock.

Conceptually:

```text
NORMAL FLOOR
     ↓
BLUE detected
     ↓
Register BLUE event
     ↓
LOCK BLUE
     ↓
Sensor remains above BLUE
     ↓
Do not count again
     ↓
Return to normal floor
     ↓
Release lock
```

<div align="center">

<img
  src="../../embed/color_event_lock.png"
  alt="Color event locking sequence"
  width="830"
/>

<br>

<sub><b>Figure 6.7.</b> Event locking prevents one physical floor marking from being counted repeatedly while the sensor remains over the same colored region.</sub>

</div>

The same concept applies to Orange.

The exact implementation can use:

```text
state transition

neutral-floor confirmation

cooldown

sample confirmation

or a combination
```

depending on the final current code.

---

## 6.9 Why Normal Floor Is Also Important

The ordinary competition surface is not simply an irrelevant third color.

It provides important transition information.

Conceptually:

```text
NORMAL FLOOR
→ BLUE
→ NORMAL FLOOR
```

is a complete event.

The return to ordinary floor helps the software determine that Piolín has physically left the previous marking.

Therefore the classifier should conceptually distinguish:

```text
BLUE

ORANGE

NORMAL / OTHER FLOOR
```

rather than only asking:

```text
Is this Blue?
```

or:

```text
Is this Orange?
```

This makes event release and rearming more reliable.

---

## 6.10 Color Classification

Depending on the active software implementation, the EV3 Color Sensor can be interpreted through built-in color identification or through measured optical values such as RGB/reflected-light data.

The important architectural concept is the same:

```text
RAW SENSOR INFORMATION
        ↓
CLASSIFICATION
        ↓
BLUE / ORANGE / FLOOR
```

<div align="center">

<img
  src="../../embed/color_classification_pipeline.png"
  alt="Color Sensor classification pipeline"
  width="820"
/>

<br>

<sub><b>Figure 6.8.</b> Raw optical measurements must be classified before they become course-state information.</sub>

</div>

The final current numerical thresholds should come from calibration performed with the sensor installed on Piolín.

This document intentionally does not invent final RGB thresholds or reflected-light limits.

---

## 6.11 Detecting Orange

Orange is especially important because the physical floor color does not always correspond perfectly to one simple predefined EV3 color label under every lighting condition.

Depending on illumination, reflectivity, sensor height, and software mode, an orange region may produce measurements closer to nearby red/brown classifications.

For this reason, Piolín should not rely on the assumption that:

```text
physical ORANGE
=
one universal EV3 value
```

The useful question is instead:

> What optical measurements does the actual competition orange produce with the current S4 mounting and casing?

The current classifier should be derived from those measurements.

This is one of the reasons the sensor casing became an important part of the subsystem.

---

## 6.12 Ambient Light as a Hardware Problem

During development, the team observed that external lighting could affect color detection.

Instead of attempting to solve the entire problem by continually widening software thresholds, Piolín uses a physical casing around the Color Sensor.

<div align="center">

<img
  src="../../v-photos/v4/color_sensor_casing.jpg"
  alt="Piolín color sensor light-isolation casing"
  width="640"
/>

<br>

<sub><b>Figure 6.9.</b> Custom light-isolation casing surrounding the EV3 Color Sensor.</sub>

</div>

The casing reduces the amount of uncontrolled light reaching the sensing region.

The goal is:

```text
less environmental variation
        ↓
more repeatable optical measurement
        ↓
cleaner classification
        ↓
more reliable course events
```

This follows an important engineering principle:

> **If measurement quality can be improved physically, that should be considered before compensating entirely through software.**

---

## 6.13 Why a Custom Casing Was Selected

Software thresholds can compensate for some variation, but increasingly broad thresholds create a new problem.

If the Blue or Orange acceptance region becomes too broad, ordinary floor measurements can begin overlapping with those classifications.

Conceptually:

```text
NARROW THRESHOLD

good separation
but may miss valid variation
```

versus:

```text
VERY BROAD THRESHOLD

captures more variation
but increases false positives
```

Improving the optical environment makes the classification problem easier before threshold tuning even begins.

<div align="center">

<img
  src="../../embed/color_casing_effect.png"
  alt="Conceptual effect of light isolation on color measurement distributions"
  width="840"
/>

<br>

<sub><b>Figure 6.10.</b> Reducing uncontrolled illumination can decrease measurement spread and improve separation between floor-color classes.</sub>

</div>

The casing therefore belongs to both the mechanical and sensing architecture.

The printable model is stored as:

[`ColorSensorCasing.stl`](../../models/3dprint/ColorSensorCasing.stl)

---

## 6.14 Casing Mechanical Requirements

The casing should reduce external light without creating new physical problems.

It should not:

```text
touch the competition mat

drag during motion

block the sensor's intended view

rotate the Color Sensor

interfere with steering

change height unpredictably
```

<div align="center">

<img
  src="../../v-photos/v4/color_sensor_casing_bottom.jpg"
  alt="Bottom view of Piolín Color Sensor casing"
  width="650"
/>

<br>

<sub><b>Figure 6.11.</b> Bottom view showing the Color Sensor casing and its clearance from the competition surface.</sub>

</div>

A good casing therefore needs both:

```text
optical isolation
```

and:

```text
mechanical clearance
```

Improving one while damaging the other would not improve the complete robot.

---

## 6.15 Sensor Height

Color measurement depends strongly on the distance between the sensor and the floor.

If the sensor is mounted too high:

```text
less controlled reflected light

larger external-light influence
```

may occur.

If it is too low:

```text
casing may touch the floor

surface irregularities become dangerous

mechanical clearance decreases
```

The target is therefore not necessarily the smallest possible sensor-to-floor distance.

It is a **repeatable mounting height that provides useful optical separation while preserving safe clearance**.

The exact current V4 height should be physically measured before being published as a final specification.

---

## 6.16 Static vs. Dynamic Color Detection

A color may be easy to identify while the robot is stationary.

Competition operation is different.

While moving:

```text
sensor approaches marking
        ↓
enters colored region
        ↓
crosses region
        ↓
leaves region
```

The number of samples collected during that interval depends on:

```text
vehicle speed

marking width

software loop frequency

confirmation logic
```

<div align="center">

<img
  src="../../embed/color_dynamic_detection.png"
  alt="Static versus moving color detection"
  width="850"
/>

<br>

<sub><b>Figure 6.12.</b> Dynamic color detection provides only a limited measurement window while the sensor moves across a floor marking.</sub>

</div>

This means a classifier that works perfectly while Piolín is held above a mark should still be validated while the robot is moving at representative competition speed.

---

## 6.17 Confirmation Trade-Off

Color detection can use multiple readings to confirm that a classification is real.

This reduces false triggers from one isolated measurement.

However, confirmation introduces a trade-off.

Too little confirmation:

```text
noise
→ false event
```

Too much confirmation:

```text
robot crosses mark
before enough valid samples occur
→ missed event
```

The final confirmation requirement should therefore be calibrated together with the actual operating speed.

This is another example of how sensing and mobility interact.

---

## 6.18 Cooldown

A cooldown can also be used to prevent one recently detected mark from being immediately counted again.

Conceptually:

```text
Valid mark detected
       ↓
Event registered
       ↓
Temporary cooldown
       ↓
New detections ignored
       ↓
Cooldown ends
```

However, a cooldown should not be selected arbitrarily.

If it is too short:

```text
same physical strip
may produce duplicate event
```

If it is too long:

```text
next legitimate course mark
may be ignored
```

The correct value therefore depends on actual:

```text
speed

track spacing

event-lock behavior

sensor sampling
```

The current final value should come from the active code and current testing.

---

## 6.19 Locking vs. Cooldown

Locking and cooldown solve related but different problems.

**Locking** is associated with the physical state of remaining on the same colored region.

**Cooldown** is associated with time after an event.

A robust event system can use one or both.

```text
LOCKING
→ "I am still physically on this mark."


COOLDOWN
→ "I recently accepted an event."
```

This distinction matters because a purely time-based system may rearm while Piolín is still physically crossing a wide mark.

A state-based system can instead wait for evidence that the colored region has actually ended.

---

## 6.20 Color Sensor During Open Challenge

During Open, the complete sensing architecture is:

```text
S1 Gyro
→ orientation


S2 / S3 Ultrasonics
→ wall geometry


S4 Color Sensor
→ course state
```

<div align="center">

<img
  src="../../embed/open_color_sensor_role.png"
  alt="Color Sensor role inside Piolín Open Challenge architecture"
  width="850"
/>

<br>

<sub><b>Figure 6.13.</b> During Open, the Color Sensor provides course-state landmarks while gyro and ultrasonic sensors handle orientation and wall geometry.</sub>

</div>

The Color Sensor does not replace the gyro during corners.

The gyro measures rotation.

Similarly, the Color Sensor does not replace the ultrasonic sensors during wall following.

It simply provides an external course event that those sensors cannot identify by themselves.

---

## 6.21 Why Color Does Not Directly Control Steering

An earlier/simple control strategy could theoretically say:

```text
BLUE detected
→ turn one direction


ORANGE detected
→ turn another direction
```

but this would combine course-state information with physical steering geometry too aggressively.

A floor mark indicates:

```text
a landmark has been reached
```

but it does not necessarily describe:

```text
exact wheel angle required right now
```

The actual steering response should still depend on:

```text
wall geometry

gyro orientation during Open

current corner state

vehicle speed
```

The current architecture therefore treats S4 as a **state trigger**, not as the primary steering controller.

---

## 6.22 Color Sensor During Obstacle Challenge

The Color Sensor remains connected to S4 during Obstacles.

The sensing architecture becomes:

```text
S1 Pixy2.1
→ obstacle identity / image position


S2 / S3
→ wall geometry


S4
→ course state
```

<div align="center">

<img
  src="../../embed/obstacle_color_sensor_role.png"
  alt="Color Sensor role in Piolín Obstacle Challenge"
  width="850"
/>

<br>

<sub><b>Figure 6.14.</b> During Obstacles, Pixy2.1 handles visual targets while S4 continues providing floor-based course landmarks.</sub>

</div>

This separation allows Pixy to focus on:

```text
RED pillar

GREEN pillar

PINK parking target
```

while the downward Color Sensor focuses on the competition mat.

The two optical sensors therefore do not perform the same task.

---

## 6.23 Color Sensor vs. Pixy2.1

Both devices detect color-related information, but they observe completely different parts of the environment.

| Sensor | Observes | Main Purpose |
| :--- | :--- | :--- |
| EV3 Color Sensor | Floor directly beneath Piolín | Course landmarks |
| Pixy2.1 | Forward camera image | Pillars and parking target |

Pixy sees:

```text
ahead
```

while S4 sees:

```text
below
```

<div align="center">

<img
  src="../../embed/color_vs_pixy_perception.png"
  alt="Comparison between downward Color Sensor and forward Pixy2.1"
  width="850"
/>

<br>

<sub><b>Figure 6.15.</b> S4 and Pixy2.1 both process color-related information but observe different physical regions and solve different navigation problems.</sub>

</div>

Keeping both therefore does not create unnecessary sensing duplication.

---

## 6.24 Color Sensor vs. Gyro

The Gyro Sensor can help the EV3 estimate:

```text
how much the robot has rotated
```

but it cannot identify:

```text
which physical floor marking has been reached
```

For example, after four nominal 90-degree turns, gyro accumulation could suggest that one lap has approximately occurred.

However, turning error, drift, recovery corrections, and real track trajectories make purely accumulated angular estimation less direct than observing physical floor landmarks.

The Color Sensor therefore provides an independent external reference that complements gyro information.

---

## 6.25 Color Sensor vs. Wheel Encoders

Wheel encoders can estimate theoretical traveled distance.

However:

```text
wheel rotation
≠
perfect vehicle displacement
```

because of:

```text
wheel slip

turning

tire deformation

mechanical backlash

different path lengths during curves
```

A floor mark exists at a known physical course location independent of how much the wheel has rotated.

The Color Sensor therefore reduces dependence on accumulated odometry.

This is especially useful over several laps, where small displacement errors can accumulate.

---

## 6.26 Why Line Tracking Was Not the Main Open Strategy

Color sensors are commonly used for line tracking.

Piolín does not use S4 primarily as a continuous line-following sensor.

The Open Challenge navigation strategy is instead based on:

```text
wall geometry
+
gyro orientation
+
floor landmarks
```

The reason is that Piolín's main environmental references are the track boundaries rather than one continuous floor line that defines the complete vehicle trajectory.

Using S4 as a course-state detector allows the sensor to solve the problem it is best positioned to solve without forcing it to become the primary steering reference.

---

## 6.27 Color Classification Data Collection

A strong calibration process should collect several readings for each relevant floor state.

Conceptually:

```text
BLUE samples

B1
B2
B3
...
BN
```

```text
ORANGE samples

O1
O2
O3
...
ON
```

and:

```text
NORMAL FLOOR samples

F1
F2
F3
...
FN
```

If RGB values are used, each observation can be recorded as:

```text
(R, G, B)
```

The objective is not to find one perfect value.

The objective is to understand the **distribution** produced by each surface.

<div align="center">

<img
  src="../../embed/color_rgb_calibration.png"
  alt="Piolín Color Sensor RGB calibration graph"
  width="850"
/>

<br>

<sub><b>Figure 6.16.</b> Color calibration should compare multiple measurements from Blue, Orange, and normal floor rather than relying on one isolated RGB sample.</sub>

</div>

This figure should be generated only after current V4 measurements are recorded.

---

## 6.28 Classification Margin

Good classification should provide separation between the measured classes.

Conceptually:

```text
BLUE VALUES
██████████


        separation


                    █████████
                    ORANGE VALUES
```

If distributions strongly overlap, simply choosing a threshold between them may not produce robust detection.

Possible improvements include:

```text
improving casing

adjusting sensor height

changing classification method

using multiple RGB relationships
```

This is preferable to pretending that overlapping measurements can always be solved with one arbitrary threshold.

---

## 6.29 Relative and Absolute Color Features

A classifier can use absolute ranges:

```text
R within range

G within range

B within range
```

or relative relationships:

```text
B greater than R

R greater than B

channel ratios
```

depending on the measured dataset.

Relative relationships can sometimes tolerate brightness changes better than one fixed absolute intensity, but they are not automatically superior.

The current classifier should therefore be derived from real sensor data rather than selected only from theoretical expectations of what Blue or Orange "should" look like.

---

## 6.30 Color Detection and Vehicle Speed

Vehicle speed directly affects how long S4 remains above a physical marking.

At higher speed:

```text
less time above mark
→ fewer sensor samples
```

At lower speed:

```text
more time above mark
→ more samples
```

This interaction affects:

```text
confirmation count

event locking

cooldown

classification confidence
```

Therefore, a Color Sensor configuration should be validated at the actual operating speeds used in competition.

The sensor and Motor A cannot be calibrated completely independently.

---

## 6.31 Color Sensor During Corners

Because the floor markings are associated with course transitions, S4 can provide useful information near corners.

However, the physical steering maneuver should still be determined from the complete navigation state.

Conceptually:

```text
COLOR EVENT
        ↓
course progression confirmed
        ↓
corner state becomes plausible
```

while:

```text
ultrasonic geometry
+
gyro angle
```

during Open provide physical evidence about how the vehicle should execute and complete the turn.

This creates stronger sensor fusion than relying on only one event source.

---

## 6.32 Progress Counting

The current Open objective remains:

```text
3 laps

12 corners
```

The Color Sensor contributes to identifying the physical events associated with that progression.

Conceptually:

```text
valid floor event
      ↓
corner/progress count
      ↓
...
      ↓
12 corner events
      ↓
three-lap objective reached
```

<div align="center">

<img
  src="../../embed/color_three_lap_progress.png"
  alt="Piolín color-based three-lap progress logic"
  width="860"
/>

<br>

<sub><b>Figure 6.17.</b> Valid floor events provide external landmarks that support progress tracking through the three-lap course.</sub>

</div>

The software should count **validated physical events**, not every raw sensor reading.

---

## 6.33 Color Sensor and Parking

The Color Sensor can also contribute to determining when Piolín has reached the correct stage of the course for parking.

This should be distinguished from detecting the parking target itself during Obstacles.

During the Obstacle Challenge:

```text
S4
→ course progress
```

while:

```text
Pixy Signature 1
→ pink parking target
```

The EV3 can therefore require:

```text
correct course state
+
parking visual evidence
```

before beginning the final parking maneuver.

This reduces the chance of interpreting an unrelated pink detection too early in the run as a parking command.

---

## 6.34 Sensor Priority

S4 does not need to dominate steering simply because a floor color is detected.

A useful decision hierarchy can instead be state-dependent.

For example, during Open:

```text
Color
→ identifies event/state


Gyro + Ultrasonics
→ control physical trajectory
```

During Obstacles:

```text
Color
→ course progression


Pixy + Ultrasonics
→ obstacle trajectory
```

This preserves the Color Sensor as a reliable **state sensor** rather than allowing one brief floor detection to override more relevant geometric information.

---

## 6.35 Color-Sensor Failure Modes

Several observable problems can originate from the Color Sensor subsystem.

| Observed Behavior | Possible Cause |
| :--- | :--- |
| Blue not detected | Classification threshold, sensor height, lighting, speed |
| Orange not detected | Orange classification or illumination |
| Normal floor detected as color | Threshold region too broad |
| One mark counted several times | Missing/weak event lock |
| Next mark ignored | Cooldown or release condition too long |
| Direction selected incorrectly | Initial classification error |
| Detection changes after casing removal | Ambient-light influence |
| Detection changes after chassis rebuild | Sensor height/orientation changed |
| Works while stationary but fails while moving | Confirmation too strict or speed too high |
| Random color events | Optical noise, threshold overlap, floor reflections |

The correct diagnostic response depends on which layer is failing.

---

## 6.36 Diagnostic Order

When color detection becomes unreliable, the recommended order is:

```text
1. Check S4 connection
        ↓
2. Inspect sensor orientation
        ↓
3. Inspect casing
        ↓
4. Check sensor-to-floor clearance
        ↓
5. Observe raw readings
        ↓
6. Compare BLUE / ORANGE / FLOOR data
        ↓
7. Check classification
        ↓
8. Check confirmation
        ↓
9. Check event lock / release
        ↓
10. Check cooldown
        ↓
11. Test at real vehicle speed
```

This prevents software thresholds from being changed before obvious physical causes are eliminated.

---

## 6.37 Why Hardware Should Be Checked Before Thresholds

Suppose Blue detection becomes inconsistent.

It may be tempting to immediately widen:

```text
BLUE threshold
```

However, if the actual problem is:

```text
Color Sensor mount became loose
```

then threshold expansion would compensate for a mechanical defect rather than solve it.

The same applies if:

```text
casing shifted

sensor height changed

light entered from one side
```

The engineering process should therefore follow:

```text
PHYSICAL SYSTEM
      ↓
RAW DATA
      ↓
CLASSIFICATION
      ↓
EVENT LOGIC
```

rather than starting at the last stage.

---

## 6.38 Comparison with Alternative Progress-Tracking Methods

| Method | Advantage | Limitation for Piolín |
| :--- | :--- | :--- |
| Motor encoders | Already available | Accumulated distance error |
| Gyro turn count | Useful during Open | Not available in Obstacles and does not identify physical landmark directly |
| Time-based progress | Very simple | Strongly dependent on speed and run conditions |
| Pixy landmarks | Rich visual information | Only installed in Obstacles and depends on camera view |
| **S4 floor landmarks** | **Direct physical course reference available in both rounds** | **Requires optical calibration and event filtering** |

The Color Sensor was therefore retained because it provides a unique external reference that is available regardless of which device occupies S1.

---

## 6.39 Why the Color Sensor Was Not Removed

The return of the gyro and the introduction of Pixy2.1 could make the Color Sensor appear redundant.

It is not.

The gyro describes:

```text
orientation
```

Pixy describes:

```text
visual objects ahead
```

the ultrasonics describe:

```text
walls
```

and the Color Sensor describes:

```text
fixed floor landmarks
```

These measurements are complementary.

Removing S4 would force another sensor to infer course progression indirectly.

Keeping S4 allows Piolín to maintain one direct physical course-state reference in both rounds.

---

## 6.40 Current Color-Sensor Architecture Compared with Earlier Development

The Color Sensor has remained useful through several Piolín versions even while the other sensing systems changed.

Development focused less on replacing the sensor and more on improving how it was used.

The progression can be summarized as:

```text
simple color detection
        ↓
lighting problems observed
        ↓
physical light isolation added
        ↓
classification improved
        ↓
event lock / confirmation logic
        ↓
course-state sensor
```

<div align="center">

<img
  src="../../embed/evolution_color_sensor.png"
  alt="Evolution of Piolín Color Sensor subsystem"
  width="880"
/>

<br>

<sub><b>Figure 6.18.</b> Evolution of the Color Sensor from simple floor detection toward a physically isolated and state-aware course-landmark subsystem.</sub>

</div>

This evolution demonstrates that improving a sensing system does not always require replacing the sensor itself.

Sometimes the stronger engineering solution is to improve:

```text
mounting

environment

classification

state processing
```

around an already appropriate sensor.

---

## 6.41 Current Responsibilities

The current S4 responsibilities are:

| Responsibility | Open | Obstacles |
| :--- | :---: | :---: |
| Detect Blue floor marking | Yes | Yes |
| Detect Orange floor marking | Yes | Yes |
| Determine initial direction | Yes | Yes |
| Provide course landmarks | Yes | Yes |
| Support corner/progress counting | Yes | Yes |
| Directly control steering | No | No |
| Detect traffic pillars | No | No |
| Measure heading | No | No |
| Measure wall distance | No | No |

The table makes the sensor boundary explicit.

S4 is a **course-state sensor**, not a general-purpose navigation sensor.

---

## 6.42 Values Intentionally Not Claimed as Final

The following values should only be included numerically after calibration of the current V4 installation:

```text
sensor-to-floor distance

BLUE RGB thresholds

ORANGE RGB thresholds

normal-floor thresholds

reflected-light thresholds

confirmation count

event-lock release condition

cooldown duration

minimum event duration

maximum reliable detection speed

measured classification error

ambient-light variation
```

Historical values can remain in development documentation, but they should not automatically be reused after changes to:

```text
sensor mount

casing

track

lighting

software mode
```

---

## 6.43 Final Engineering Assessment

The LEGO EV3 Color Sensor remains part of Piolín because it solves a problem that the other sensors do not solve as directly: identifying **fixed physical landmarks on the competition floor**.

Its role can be summarized as:

```text
                         COURSE FLOOR
                              │
                              ▼
                       EV3 COLOR SENSOR
                              │
                              ▼
                         CLASSIFICATION
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
                  BLUE               ORANGE
                    │                   │
                    └─────────┬─────────┘
                              ▼
                         VALID EVENT
                              │
                              ▼
                         COURSE STATE
                              │
                              ▼
                            EV3
```

<div align="center">

<img
  src="../../v-photos/v4/color_sensor_bottom_view.jpg"
  alt="Piolín final downward Color Sensor installation"
  width="680"
/>

<br>

<sub><b>Figure 6.19.</b> Current S4 installation providing a permanent floor-reference subsystem for both competition rounds.</sub>

</div>

The final design also demonstrates that reliable sensing is not only a software problem. The custom light-isolation casing, mounting position, classification logic, event locking, and dynamic validation all contribute to the final result.

Piolín therefore treats the Color Sensor as a complete optical subsystem rather than simply as a device that returns a color name.

---

<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
