# 3. Color Sensor

<div align="center">

<img
  src="../../v-photos/v4/color_sensor_s4_installed.jpg"
  alt="EV3 Color Sensor installed underneath Piolín on Sensor Port S4"
  width="680"
/>

<br>

<sub><b>Figure 3.1.</b> Piolín's downward-facing LEGO Mindstorms EV3 Color Sensor permanently connected to Sensor Port S4.</sub>

</div>

Piolín uses one **LEGO Mindstorms EV3 Color Sensor** mounted underneath the chassis and permanently connected to **Sensor Port S4**. Unlike the lateral ultrasonic sensors, which observe the geometry surrounding the robot, the Color Sensor observes the competition surface directly below the vehicle.

Its main role is to detect the colored floor references used by the WRO Future Engineers track.

The current important markings are:

```text
BLUE

ORANGE
```

These markings provide information about:

```text
initial course direction

course progression

corner / section progression

lap counting support

final run-state decisions
```

The Color Sensor remains installed in the same position during both the **Open Challenge** and the **Obstacle Challenge**.

Its electrical mapping never changes:

```text
S4 = Color Sensor
```

This makes S4 one of the stable sensing references shared by both competition configurations.

---

## 3.1 Sensor Role in Piolín

The Color Sensor performs a fundamentally different function from the other sensors.

During Open:

```text
Gyro
→ heading

Ultrasonics
→ lateral geometry

Color Sensor
→ course-state landmarks
```

During Obstacles:

```text
Pixy2.1
→ pillar identity and image position

Ultrasonics
→ lateral geometry

Color Sensor
→ course-state landmarks
```

The Color Sensor therefore does not try to determine:

```text
vehicle heading

wall distance

pillar color
```

Instead, it answers a different question:

> **What important floor reference has Piolín just crossed?**

This division of responsibilities simplifies the navigation architecture because each sensor is used for the type of physical information it measures most directly.

---

# 3.2 Permanent S4 Configuration

<div align="center">

<img
  src="../../v-photos/v4/ev3_sensor_ports.jpg"
  alt="EV3 sensor ports showing Piolín permanent S4 Color Sensor connection"
  width="660"
/>

<br>

<sub><b>Figure 3.2.</b> The Color Sensor remains assigned to S4 regardless of competition round.</sub>

</div>

Piolín's fixed sensor convention includes:

```text
S2 = LEFT Ultrasonic

S3 = RIGHT Ultrasonic

S4 = Color Sensor
```

Only S1 changes between rounds.

```text
OPEN
S1 = Gyro
```

```text
OBSTACLES
S1 = Pixy2.1
```

S4 does not need to change because floor-state information is useful in both navigation strategies.

Keeping the same sensor in the same port also reduces the risk of introducing wiring or software inconsistencies when Piolín is converted from one round to another.

---

# 3.3 Downward-Facing Installation

<div align="center">

<img
  src="../../v-photos/v4/color_sensor_bottom_view.jpg"
  alt="Bottom view of Piolín showing the downward-facing Color Sensor"
  width="680"
/>

<br>

<sub><b>Figure 3.3.</b> Bottom view showing the Color Sensor positioned to observe the track surface directly beneath the vehicle.</sub>

</div>

The sensor is mounted facing downward because the relevant information is located on the floor.

This geometry allows Piolín to detect a marking when the chassis physically crosses over it.

The sensing sequence is approximately:

```text
Piolín approaches marking
        ↓
marking enters sensor field
        ↓
S4 measurement changes
        ↓
EV3 classifies floor state
        ↓
event is confirmed
        ↓
navigation state is updated
```

The exact moment at which the robot recognizes the marking depends on the physical location of the sensor relative to the rest of the chassis.

Therefore Color Sensor placement is part of the navigation geometry.

---

# 3.4 Why Sensor Position Matters

The Color Sensor does not sit at the exact center of the vehicle.

As a result:

```text
sensor crosses line
```

and:

```text
vehicle center crosses line
```

do not occur at exactly the same physical moment.

This becomes important when a floor event is used near a corner.

The controller must understand that the detection represents:

```text
the sensor reaching the marking
```

rather than:

```text
the complete vehicle reaching exactly the same point
```

This physical offset can influence:

```text
corner timing

state transitions

parking logic

progress counting
```

and should be considered when tuning the final controller.

---

# 3.5 Color Sensor Light-Isolation Casing

<div align="center">

<img
  src="../../v-photos/v4/color_sensor_casing.jpg"
  alt="Piolín Color Sensor light isolation casing"
  width="660"
/>

<br>

<sub><b>Figure 3.4.</b> Physical casing surrounding the Color Sensor to reduce uncontrolled ambient illumination.</sub>

</div>

One of the most important modifications to Piolín's floor-sensing system is the light-isolation casing surrounding the Color Sensor.

A color measurement depends on the light reaching the sensing area.

Without physical isolation, readings can change because of:

```text
room lighting

sunlight

shadows

reflections

robot orientation

nearby objects
```

Instead of trying to solve all of these effects using increasingly broad software thresholds, Piolín also improves the physical measurement environment.

The design principle is:

```text
reduce uncontrolled light
        ↓
reduce measurement variation
        ↓
improve classification consistency
```

This is an example of using mechanical design to improve sensor quality before software processing begins.

---

# 3.6 Why Physical Isolation Is Useful

Suppose the same blue marking is measured under two different lighting conditions.

Without sufficient isolation:

```text
same physical blue
+
different environmental light
=
different sensor values
```

If the difference becomes large enough, the software may need very broad classification ranges.

Broad ranges create another problem:

```text
more tolerance
```

can also produce:

```text
more overlap between categories
```

The casing helps reduce this problem by making the local optical environment around the sensor more controlled.

This does not eliminate the need for calibration.

It improves the conditions under which calibration is performed.

---

# 3.7 Blue Course Reference

<div align="center">

<img
  src="../../v-photos/v4/color_sensor_blue_mark.jpg"
  alt="Piolín Color Sensor positioned over a blue course marking"
  width="660"
/>

<br>

<sub><b>Figure 3.5.</b> S4 observing a real blue floor reference used by the navigation system.</sub>

</div>

A valid **Blue** event has special importance during Open because the first recognized course color establishes the navigation direction.

The current rule used by Piolín is:

```text
BLUE first
→ COUNTERCLOCKWISE
```

This means Blue is not merely a visual label.

At the beginning of an Open run, it can initialize an important persistent software state.

Conceptually:

```text
direction = UNKNOWN
        ↓
BLUE detected first
        ↓
direction = COUNTERCLOCKWISE
```

Once this state has been established, later color events should not continuously reverse the navigation direction.

---

# 3.8 Orange Course Reference

<div align="center">

<img
  src="../../v-photos/v4/color_sensor_orange_mark.jpg"
  alt="Piolín Color Sensor positioned over an orange course marking"
  width="660"
/>

<br>

<sub><b>Figure 3.6.</b> S4 observing a real orange floor reference.</sub>

</div>

The opposite Open initialization rule is:

```text
ORANGE first
→ CLOCKWISE
```

Conceptually:

```text
direction = UNKNOWN
        ↓
ORANGE detected first
        ↓
direction = CLOCKWISE
```

Once direction has been established, Blue and Orange can continue to provide progress information without redefining which physical ultrasonic sensor is left or right.

The physical sensor mapping always remains:

```text
S2 = LEFT

S3 = RIGHT
```

Only the logical interpretation of:

```text
INNER

OUTER
```

changes according to the course direction.

---

# 3.9 Direction Is a Persistent State

The first valid course marking should initialize direction only once.

A weak implementation could behave like:

```text
see Blue
→ CCW

later see Orange
→ CW

later see Blue
→ CCW
```

That would continuously invert the interpretation of the track.

Instead, Piolín should conceptually use:

```text
IF direction is UNKNOWN:
    first valid Blue/Orange
    sets direction

ELSE:
    keep existing direction
```

Later floor detections then become **course-progress events** rather than direction-selection events.

This distinction is essential for stable multi-lap navigation.

---

# 3.10 Color as Course-State Information

Once course direction is established, the Color Sensor becomes a physical landmark detector.

Rather than trying to estimate progress entirely through:

```text
time

motor rotation

assumed distance
```

Piolín can use real features on the course.

This provides a state transition based on:

```text
robot physically crossed a known floor reference
```

which is often more meaningful than:

```text
approximately enough time has passed
```

The Color Sensor therefore helps connect internal software state to physical track progress.

---

# 3.11 Progress Counting

The WRO Open course requires Piolín to complete multiple corners and laps.

A color event can contribute to the progress counter.

Conceptually:

```text
valid marking crossed
        ↓
new course event
        ↓
progress counter updated
```

The exact relationship between individual Blue/Orange events and the final corner-count implementation depends on the active Open controller.

The important design principle is that the software should count **physical events**, not repeated sensor samples from the same physical marking.

---

# 3.12 Why One Marking Can Be Read Many Times

When Piolín drives over a colored region, the sensor may remain above that color for more than one program loop.

For example:

```text
LOOP 1 → BLUE
LOOP 2 → BLUE
LOOP 3 → BLUE
LOOP 4 → BLUE
```

If every loop increments the counter:

```text
one physical marking
→ four software events
```

This would corrupt lap and corner progression.

Therefore color recognition needs an event mechanism that distinguishes:

```text
currently seeing Blue
```

from:

```text
a NEW Blue crossing occurred
```

---

# 3.13 Event Lock

A useful conceptual solution is a detection lock.

```text
neutral floor
      ↓
Blue detected
      ↓
count one Blue event
      ↓
lock Blue event
      ↓
continue over marking
      ↓
do not count again
      ↓
leave marking
      ↓
unlock for next event
```

The same concept applies to Orange.

This prevents one physical region from being counted several times because of the sensor's sampling rate.

---

# 3.14 Debouncing and Confirmation

A color event should also avoid reacting to one uncertain sample if that sample is not representative.

A conceptual confirmation process is:

```text
possible Blue
      ↓
check classification consistency
      ↓
confirm event
```

However, confirmation creates a trade-off.

Too little confirmation can cause:

```text
false detections
```

Too much confirmation can cause:

```text
late detection
```

At vehicle speed, late detection corresponds to additional physical travel.

The best confirmation strategy is therefore not necessarily the longest one.

It should be sufficient to reject unstable samples without making the course-state event occur too late.

---

# 3.15 Neutral Floor and Re-Arming

One way to identify that Piolín has left a colored marking is to observe the normal floor again.

Conceptually:

```text
BLUE
→ locked
→ normal floor returns
→ Blue detector re-armed
```

The exact current implementation can vary because physical floor readings may not always produce one perfectly uniform neutral value.

The broader engineering requirement is:

> **A second event should only be accepted after there is convincing evidence that Piolín has left the previous physical marking.**

This reduces double counting.

---

# 3.16 Classification Pipeline

The conceptual Color Sensor pipeline is:

```text
PHYSICAL FLOOR
      ↓
LIGHT-ISOLATION CASING
      ↓
EV3 COLOR SENSOR
      ↓
RAW / COLOR MEASUREMENT
      ↓
CLASSIFICATION
      ↓
TEMPORAL CONFIRMATION
      ↓
EVENT LOCK
      ↓
COURSE-STATE UPDATE
```

Each stage solves a different problem.

```text
Casing
→ physical measurement stability

Classification
→ Blue / Orange / other

Confirmation
→ reject unstable events

Lock
→ avoid duplicate counting

State logic
→ decide what detection means
```

This separation makes the system easier to debug.

---

# 3.17 Raw Measurement vs. Navigation Event

It is useful to distinguish three levels.

### Measurement

```text
sensor reports optical information
```

### Classification

```text
software decides:
Blue / Orange / Other
```

### Event

```text
software decides:
a NEW meaningful marking was crossed
```

These are not the same thing.

For example:

```text
100 consecutive Blue measurements
```

may correspond to:

```text
one Blue event
```

This distinction is particularly important when debugging progression errors.

---

# 3.18 Classification Calibration

Color classification should be based on measurements from the actual V4 robot.

Calibration should use:

```text
current sensor

current sensor height

current casing

real competition-style Blue

real competition-style Orange

representative lighting
```

A calibration performed before changing the casing or sensor mounting may no longer represent the current system.

The repository should therefore avoid copying old threshold values automatically into the final documentation.

---

# 3.19 Recommended Calibration Samples

A useful calibration dataset should include repeated measurements of:

```text
Blue

Orange

normal floor
```

rather than only one reading from each.

A table can later be used:

| Surface | Trial | Sensor Reading | Classification Result |
| :--- | :---: | :--- | :--- |
| Blue | 1 | — | — |
| Blue | 2 | — | — |
| Blue | 3 | — | — |
| Orange | 1 | — | — |
| Orange | 2 | — | — |
| Orange | 3 | — | — |
| Normal floor | 1 | — | — |
| Normal floor | 2 | — | — |

Only real V4 measurements should populate this table.

The goal is to understand the **range of readings**, not merely one ideal value.

---

# 3.20 Why RGB or Raw Values Can Be Useful

A predefined color-name mode can be useful, but raw or RGB-style measurements can provide greater control when the physical colors do not match ideal sensor categories perfectly.

A custom classifier can conceptually compare:

```text
R

G

B
```

or other available sensor values.

This allows the team to create thresholds matched to:

```text
the actual mat

the actual casing

the actual mounting
```

rather than relying only on generic color definitions.

The final classification method should be the one that proves most repeatable under real testing.

---

# 3.21 Relative Color Relationships

A classifier does not always need to rely only on one absolute threshold.

For example, a color may be identified through relationships between channels rather than:

```text
R > one fixed number
```

alone.

This can sometimes make classification more tolerant of moderate brightness changes.

However, no final mathematical classification rule should be documented as validated until actual current sensor data supports it.

---

# 3.22 Lighting Variation

Even with the casing, lighting can still influence measurements.

Possible environmental changes include:

```text
different room

different overhead lights

sunlight entering room

shadows

reflections from nearby surfaces
```

Therefore calibration should not be evaluated using only one ideal stationary test.

The final classifier should also be tested during actual driving.

---

# 3.23 Static vs. Dynamic Detection

A stationary calibration test answers:

```text
Can the sensor distinguish the colors
while Piolín is not moving?
```

A dynamic test answers:

```text
Can the system detect the marking
while Piolín crosses it at real speed?
```

The second is essential.

During motion:

```text
sensor spends limited time above marking

sampling position changes

vehicle vibration exists

lighting can change slightly
```

A classifier that works perfectly while stationary can still miss markings during a real run.

---

# 3.24 Vehicle Speed and Detection Window

The faster Piolín travels, the less time the Color Sensor remains over a floor marking.

Conceptually:

```text
higher speed
→ shorter observation time
```

which means:

```text
fewer available sensor samples
```

before the robot leaves the colored region.

This creates another design trade-off.

```text
more confirmation
→ stronger noise rejection
→ but slower event recognition
```

At higher vehicle speed, an overly slow confirmation method may cause the event to occur after Piolín has already traveled too far.

Color logic should therefore be validated at representative operating speed.

---

# 3.25 Sensor Height

The physical distance between the sensor and the floor affects the optical measurement.

If the sensor height changes:

```text
illumination geometry changes

reflected light changes

field observed can change
```

This means a chassis modification that moves S4 vertically can invalidate previous calibration.

The Color Sensor mount should therefore remain mechanically stable after thresholds have been tuned.

---

# 3.26 Casing Clearance

The casing must reduce unwanted light without interfering with vehicle motion.

It should not:

```text
drag on the floor

catch on track features

push the sensor out of alignment
```

A useful physical design therefore balances:

```text
light isolation
```

with:

```text
safe ground clearance
```

The casing is both an optical and mechanical component.

---

# 3.27 Color Sensor During Open Challenge

During Open, S4 has two major responsibilities.

First:

```text
determine initial course direction
```

Second:

```text
provide physical progression landmarks
```

The complete Open sensing context is:

```text
S1 Gyro
→ orientation

S2/S3 Ultrasonics
→ wall geometry

S4 Color
→ track-state events
```

This allows Piolín to combine:

```text
continuous information
```

from the gyro and ultrasonics with:

```text
discrete landmarks
```

from the floor.

---

# 3.28 Continuous vs. Discrete Sensors

This distinction is useful.

The ultrasonic and gyro sensors provide values that can change continuously while Piolín moves.

The Color Sensor often produces navigation information as discrete events:

```text
Blue crossed

Orange crossed
```

The controller therefore combines two different forms of information.

```text
CONTINUOUS
→ where / how am I moving?


DISCRETE
→ what important course point did I cross?
```

This is one reason floor sensing is valuable even when the robot already has wall and heading sensors.

---

# 3.29 Color and Corner Handling

Floor markings can contribute to corner-state logic.

However, the Color Sensor should not be treated as the only source of corner geometry.

A strong Open corner decision can combine:

```text
course progress from S4

ultrasonic geometry

gyro heading / rotation
```

The Color Sensor can indicate:

```text
a relevant course landmark has been reached
```

while the other sensors help determine:

```text
how the vehicle should physically complete the turn
```

This prevents one sensor type from being responsible for the entire corner maneuver.

---

# 3.30 Color and Gyro Complementarity

During Open:

```text
Color
→ tells Piolín that a course event occurred
```

while:

```text
Gyro
→ tells Piolín how much the vehicle has rotated
```

These are different pieces of information.

For example, a floor event may begin a corner state, but the gyro can help determine whether the vehicle has actually rotated enough to begin exiting that state.

This produces a stronger relationship than either sensor alone.

---

# 3.31 Color and Ultrasonic Complementarity

Similarly:

```text
Color
→ progress landmark
```

and:

```text
Ultrasonics
→ wall geometry
```

A color event may indicate that Piolín has reached the region where a corner is expected, while S2/S3 help determine whether the surrounding geometry is consistent with that interpretation.

Combining them reduces dependence on one sensor reading.

---

# 3.32 Color Sensor During Obstacle Challenge

The Color Sensor remains on S4 during Obstacles.

The active configuration becomes:

```text
S1 = Pixy2.1

S2 = Left Ultrasonic

S3 = Right Ultrasonic

S4 = Color Sensor
```

Pixy is responsible for visual pillar information.

The Color Sensor remains responsible for the floor.

Therefore:

```text
Pixy Red
```

and:

```text
Color Sensor Orange
```

are completely different sensing events even though both involve color.

---

# 3.33 Color Sensor vs. Pixy2.1

The distinction is essential.

### EV3 Color Sensor

```text
looks downward

observes floor directly underneath Piolín

detects track markings
```

### Pixy2.1

```text
looks forward

observes objects ahead

detects visual signatures
```

The two devices solve different physical problems.

The Color Sensor should not be used to identify obstacle pillars because it cannot observe them ahead of the robot.

Pixy should not replace S4 for precise floor crossings because its visual geometry is entirely different.

---

# 3.34 Parking and Course Progress

The Color Sensor can also support parking by helping determine whether the robot has completed the required course progression before the final positioning sequence begins.

A safe parking condition should not be:

```text
see one relevant color
→ immediately stop
```

Instead, course state can contribute to a larger decision containing:

```text
expected progress reached

correct lap / corner count

parking condition active

vehicle positioned appropriately
```

The final parking implementation remains under development, so this document does not claim one finished event sequence.

---

# 3.35 Three-Lap Progression

For Open, Piolín's intended full run consists of:

```text
3 laps

12 corners
```

The Color Sensor provides physical events that can help the controller maintain awareness of this progression.

A useful state concept is:

```text
START
 ↓
direction established
 ↓
course events counted
 ↓
lap / corner progress updated
 ↓
12-corner condition reached
 ↓
parking sequence allowed
```

The exact implementation must prevent:

```text
duplicate counts

missed counts

false counts
```

because any of these can move the software state out of synchronization with the physical robot.

---

# 3.36 Missed Detection

A missed marking can occur when:

```text
sensor classification fails

robot crosses too quickly

marking is only partially observed

sensor position is poor

thresholds are too restrictive
```

If one event is missed, the internal course counter can fall behind the physical robot.

This can later appear as:

```text
parking too late

corner count wrong

lap state wrong
```

even though the original failure happened much earlier.

Color-state debugging should therefore identify the first incorrect event rather than only the final symptom.

---

# 3.37 Duplicate Detection

The opposite failure is counting one marking twice.

Possible causes include:

```text
event lock released too early

sensor briefly leaves and re-enters threshold

classification oscillates near boundary

no cooldown / re-arm logic
```

A duplicate event causes software progression to move ahead of the physical robot.

The two failure types can therefore be distinguished conceptually:

```text
MISSED EVENT
→ software behind physical progress
```

```text
DUPLICATE EVENT
→ software ahead of physical progress
```

This distinction is useful during debugging.

---

# 3.38 False Detection

A false detection occurs when the software classifies something as Blue or Orange even though Piolín did not cross the intended course marking.

Potential causes include:

```text
threshold overlap

lighting

surface variation

reflections

classification noise
```

The casing reduces part of the optical variability, while software confirmation reduces part of the remaining classification risk.

Neither method should be expected to solve every problem independently.

---

# 3.39 Color Sensor Diagnostic Order

When floor detection behaves incorrectly, a useful diagnostic sequence is:

```text
1. Verify S4 connection.

2. Inspect sensor mounting.

3. Inspect casing position.

4. Verify sensor faces floor correctly.

5. Read raw values over normal floor.

6. Read raw values over Blue.

7. Read raw values over Orange.

8. Compare with classification logic.

9. Test event lock.

10. Test dynamic crossing at low speed.

11. Test at representative speed.

12. Only then change course-state logic.
```

This order separates:

```text
physical sensing problem
```

from:

```text
classification problem
```

and:

```text
state-management problem
```

before the full navigation controller is changed.

---

# 3.40 Common Failure Modes

| Observed Behavior | Possible Cause |
| :--- | :--- |
| Blue never detected | Threshold, S4, height, casing, lighting |
| Orange never detected | Threshold, S4, height, casing, lighting |
| Blue classified as Orange | Classification ranges or sensor data |
| Orange classified as Blue | Classification ranges or sensor data |
| Same line counted multiple times | Event-lock / re-arm logic |
| Line detected while stationary but missed while driving | Speed, confirmation delay, sampling |
| Direction changes later in the run | Direction state is being overwritten |
| Corner count becomes too high | Duplicate events |
| Corner count becomes too low | Missed events |
| Detection changed after mechanical work | Sensor height or casing position changed |
| Random false detections | Threshold overlap, lighting, surface variation |
| Correct raw reading but wrong navigation behavior | State logic rather than sensor problem |

This table helps identify which layer should be investigated first.

---

# 3.41 Testing Blue

<div align="center">

<img
  src="../../v-photos/v4/color_sensor_blue_mark.jpg"
  alt="Blue floor reference used during Piolín Color Sensor testing"
  width="660"
/>

<br>

<sub><b>Figure 3.7.</b> Blue should be tested using the actual sensor installation rather than a detached sensor under unrelated conditions.</sub>

</div>

Blue testing should include:

```text
multiple stationary samples

multiple crossing speeds

slightly different vehicle positions

representative lighting
```

The objective is not only to identify a perfect center-of-marking reading.

The classifier should remain useful during the actual physical crossing performed by Piolín.

---

# 3.42 Testing Orange

<div align="center">

<img
  src="../../v-photos/v4/color_sensor_orange_mark.jpg"
  alt="Orange floor reference used during Piolín Color Sensor testing"
  width="660"
/>

<br>

<sub><b>Figure 3.8.</b> Orange should be characterized independently from Blue using real V4 measurements.</sub>

</div>

Blue and Orange should be measured independently.

The team should avoid assuming:

```text
if Blue works,
Orange automatically works
```

because the optical values and their separation from the normal floor can differ.

Both classes need sufficient margin from:

```text
each other
```

and:

```text
normal track surface
```

for reliable classification.

---

# 3.43 Dynamic Course Test

<div align="center">

<img
  src="../../v-photos/v4/full_track.jpg"
  alt="Full track used for Piolín dynamic Color Sensor testing"
  width="740"
/>

<br>

<sub><b>Figure 3.9.</b> Final Color Sensor validation must occur during real track motion because timing and vehicle speed affect floor-event detection.</sub>

</div>

After isolated classification is stable, the system should be tested as part of a full moving robot.

A useful test progression is:

```text
stationary color test
      ↓
slow single crossing
      ↓
normal-speed single crossing
      ↓
several consecutive markings
      ↓
one complete lap
      ↓
three-lap progression
```

This helps determine at which level a failure first appears.

---

# 3.44 Test Logging

Useful Color Sensor tests should record:

| Field | Information |
| :--- | :--- |
| Software version | Current test code / commit |
| Sensor mode | Raw / RGB / classification method |
| Casing | Current physical configuration |
| Surface | Blue / Orange / normal |
| Vehicle state | Stationary or moving |
| Speed | Current Motor A condition |
| Raw measurement | Actual sensor output |
| Classification | Resulting class |
| Event accepted? | Yes / No |
| Counter before | Course state |
| Counter after | Course state |
| Notes | Misclassification, delay, duplicate, etc. |

This makes it possible to distinguish a sensor improvement from an unrelated state-logic change.

---

# 3.45 Mechanical Changes Require Recalibration

The Color Sensor should be recalibrated or at least reverified after changes such as:

```text
sensor remounting

casing replacement

casing movement

chassis-height change

sensor angle change
```

Even if the software is unchanged, the optical environment may no longer be identical.

This reflects the broader Piolín engineering principle:

> **Sensor calibration belongs to the complete physical sensor installation, not only to the electronic component.**

---

# 3.46 Same Color Hardware in Both Rounds

One major advantage of S4 is that it remains physically unchanged when switching competition configurations.

```text
OPEN
S4 = Color
```

```text
OBSTACLES
S4 = Color
```

Unlike S1:

```text
Gyro ↔ Pixy
```

the Color Sensor does not need to be replaced or rewired.

This preserves:

```text
sensor position

sensor height

casing geometry

electrical port

calibration reference
```

between rounds.

---

# 3.47 Physical Integration

<div align="center">

<img
  src="../../v-photos/v4/piolin_bottom.jpg"
  alt="Bottom view of Piolín showing Color Sensor integration into the chassis"
  width="720"
/>

<br>

<sub><b>Figure 3.10.</b> S4 is integrated into the underside of the common Piolín vehicle platform.</sub>

</div>

The bottom installation places the sensor close enough to the competition surface to detect floor markings while keeping it mechanically integrated with the chassis.

Its location must also avoid interference with:

```text
wheels

drivetrain

steering

track surface
```

The sensor therefore forms part of both the sensing and mechanical architecture.

---

# 3.48 Current vs. Legacy Color Logic

The physical S4 concept has remained useful throughout Piolín's development, but classification and course-state logic have evolved.

Older programs may contain different:

```text
color windows

confirmation counts

cooldowns

thresholds

event-count logic
```

These historical values should not automatically be treated as current final calibration.

The current documentation should distinguish:

```text
sensor architecture
```

which is established, from:

```text
final software thresholds
```

which are still subject to testing.

---

# 3.49 Values Intentionally Not Claimed as Final

The following values should only be published after current V4 measurement and validation:

```text
final Blue RGB range

final Orange RGB range

final neutral-floor range

final brightness thresholds

final confirmation count

final debounce duration

final event-lock release condition

final minimum time between events

final sensor-to-floor distance

final sensor offset from vehicle reference point

measured classification accuracy

measured missed-event rate

measured duplicate-event rate

maximum validated crossing speed
```

Working code can contain current tuning values, but those values should not be described as universal or final until the tests support that claim.

---

# 3.50 Recommended Final Characterization

A complete V4 Color Sensor characterization should eventually contain four groups of measurements.

### Static optical characterization

Measure repeated:

```text
Blue

Orange

normal floor
```

samples while Piolín remains stationary.

### Lighting robustness

Repeat representative measurements under realistic lighting conditions.

### Dynamic crossing test

Cross each marking several times at representative vehicle speed and record:

```text
detected?

correct class?

event counted once?
```

### Full-course progression test

Verify that:

```text
initial direction

course count

lap count

final progression state
```

remain synchronized with the physical robot throughout the run.

This progression converts basic optical sensing into validated autonomous-course state.

---

# 3.51 Complete Color-Sensing Chain

The current system can be represented as:

```text
                 TRACK FLOOR
                     │
                     ▼
            BLUE / ORANGE MARK
                     │
                     ▼
            LIGHT-ISOLATION CASING
                     │
                     ▼
             COLOR SENSOR S4
                     │
                     ▼
                    EV3
                     │
             raw measurement
                     │
                     ▼
              classification
                     │
                     ▼
             event confirmation
                     │
                     ▼
                event lock
                     │
                     ▼
             course-state update
                     │
                     ▼
         navigation decision / progress
```

The important point is that the sensor measurement passes through several interpretation layers before it changes vehicle behavior.

This makes each layer independently testable.

---

# 3.52 Final Engineering Assessment

Piolín's EV3 Color Sensor provides a stable physical connection between the robot's internal software state and the real competition surface.

Its permanent mapping is:

```text
S4 = Color Sensor
```

in both Open and Obstacles.

The sensor is mounted downward and protected by a physical light-isolation casing to improve the optical conditions under which Blue and Orange floor references are measured.

During Open, the first valid color event establishes course direction:

```text
BLUE first
→ counterclockwise

ORANGE first
→ clockwise
```

After direction has been established, later floor detections contribute primarily to course progression rather than redefining the robot's direction.

This requires the software to distinguish between:

```text
raw measurements

color classifications

new physical events
```

so that one marking is not counted repeatedly across multiple control loops.

The Color Sensor also complements the other sensing systems rather than replacing them.

During Open:

```text
Color
→ course state

Gyro
→ heading

Ultrasonics
→ lateral geometry
```

During Obstacles:

```text
Color
→ course state

Pixy2.1
→ visual obstacle information

Ultrasonics
→ lateral geometry
```

The main engineering principle behind the subsystem is:

> **Use physical floor markings as discrete navigation landmarks, improve the measurement environment mechanically, and convert sensor readings into controlled state events rather than treating every sample as a new course event.**

This makes the Color Sensor more than a simple color detector. It becomes a persistent course-state reference used to connect Piolín's autonomous software with the physical structure of the WRO Future Engineers track.

---

<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
