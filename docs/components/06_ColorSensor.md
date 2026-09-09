# 6. Color Sensor and Course-State Detection

<div align="center">

<img
  src="../../v-photos/v4/color_sensor_s4_installed.jpg"
  alt="LEGO EV3 Color Sensor installed underneath Piolín"
  width="680"
/>

<br>

<sub><b>Figure 6.1.</b> LEGO EV3 Color Sensor permanently connected to S4 and mounted downward to observe the course surface.</sub>

</div>

Piolín uses one **LEGO Mindstorms EV3 Color Sensor connected to Sensor Port S4** as its permanent floor-perception sensor.

Unlike the lateral ultrasonic sensors, which primarily describe the geometry around the vehicle, the Color Sensor provides information about **course state**.

Its current responsibilities include:

```text
detecting BLUE floor markings

detecting ORANGE floor markings

determining the initial travel direction

identifying physical course events

supporting progression through the three-lap round
```

The Color Sensor remains installed during both competition configurations.

```text
OPEN
S4 = Color Sensor


OBSTACLES
S4 = Color Sensor
```

This makes it one of the permanent sensors in Piolín's architecture.

---

## 6.1 Current Hardware Assignment

The hardware mapping is fixed:

```text
S4
=
LEGO EV3 Color Sensor
```

The sensor is mounted facing downward so that its optical system observes the course surface rather than walls or obstacles.

<div align="center">

<img
  src="../../v-photos/v4/color_sensor_bottom_view.jpg"
  alt="Bottom view of Piolín showing the downward-facing Color Sensor"
  width="680"
/>

<br>

<sub><b>Figure 6.2.</b> Bottom view showing the Color Sensor's orientation relative to the track surface.</sub>

</div>

The physical position of the sensor matters because the software assumes that a valid color event corresponds to Piolín physically crossing a course marking.

The sensor therefore needs a repeatable relationship with:

```text
track surface

vehicle centerline

front/rear position

sensor height
```

If the mount moves, the timing of color detection can also change.

---

# 6.2 Why the Color Sensor Is Used

Piolín already has several sensors, but none of the others provide the same information.

The lateral ultrasonic sensors answer:

```text
Where am I relative to the walls?
```

The Gyro Sensor during Open answers:

```text
How has my orientation changed?
```

Pixy2.1 during Obstacles answers:

```text
Which visual target is in front of me?
```

The Color Sensor answers a different question:

```text
Which physical course marking have I reached?
```

This distinction is important because the color markings are fixed features of the competition track.

They provide an **external physical reference** that does not depend entirely on:

```text
elapsed time

motor rotation

gyro integration

wall-following distance
```

The Color Sensor can therefore help Piolín determine where it is within the sequence of the course.

---

# 6.3 Initial Direction Detection

One of the most important uses of the Color Sensor is determining the initial direction of travel.

Piolín uses the first valid Blue or Orange floor event.

The current convention is:

```text
BLUE FIRST
→ COUNTERCLOCKWISE


ORANGE FIRST
→ CLOCKWISE
```

<div align="center">

<img
  src="../../embed/color_direction_logic.png"
  alt="Piolín direction selection based on the first Blue or Orange course marking"
  width="800"
/>

<br>

<sub><b>Figure 6.3.</b> The first valid Blue or Orange floor event establishes the direction used by the navigation system.</sub>

</div>

This single decision influences several later parts of the software.

Once direction is known, Piolín can correctly interpret:

```text
which ultrasonic is INNER

which ultrasonic is OUTER

which corner direction should be expected

how course progression should be interpreted
```

The Color Sensor therefore affects navigation indirectly even though it does not control steering itself.

---

# 6.4 Blue Means Counterclockwise

When Blue is the first valid course color:

```text
BLUE
  ↓
COUNTERCLOCKWISE
```

the current ultrasonic interpretation becomes:

```text
S2 LEFT
→ INNER


S3 RIGHT
→ OUTER
```

<div align="center">

<img
  src="../../v-photos/v4/color_sensor_blue_mark.jpg"
  alt="Piolín Color Sensor positioned over a Blue course marking"
  width="680"
/>

<br>

<sub><b>Figure 6.4.</b> Color Sensor observing a Blue course marking used as a valid physical course event.</sub>

</div>

The Color Sensor does not itself perform this inner/outer conversion.

Instead:

```text
Color Sensor
     ↓
direction state
     ↓
EV3 navigation logic
     ↓
ultrasonic role mapping
```

This is another example of separating sensor measurement from software interpretation.

---

# 6.5 Orange Means Clockwise

When Orange is the first valid course color:

```text
ORANGE
  ↓
CLOCKWISE
```

the ultrasonic interpretation becomes:

```text
S2 LEFT
→ OUTER


S3 RIGHT
→ INNER
```

<div align="center">

<img
  src="../../v-photos/v4/color_sensor_orange_mark.jpg"
  alt="Piolín Color Sensor positioned over an Orange course marking"
  width="680"
/>

<br>

<sub><b>Figure 6.5.</b> Color Sensor observing an Orange course marking used by the course-state logic.</sub>

</div>

The physical sensor wiring never changes.

Only the logical meaning of the measurements changes.

This keeps:

```text
S2 = LEFT

S3 = RIGHT

S4 = COLOR
```

constant in both directions.

---

# 6.6 Physical Color vs. Course Event

A major software distinction is:

```text
COLOR SAMPLE
≠
COURSE EVENT
```

The EV3 can read the Color Sensor many times while Piolín is physically crossing one colored region.

For example:

```text
BLUE

BLUE

BLUE

BLUE

BLUE
```

may correspond to only:

```text
ONE physical Blue marking
```

If every sample were counted independently, one real course feature could generate several false progression events.

The software must therefore transform repeated sensor samples into discrete physical events.

---

# 6.7 Event Latching

Piolín uses the concept of an **event latch** to prevent one physical marking from being counted repeatedly.

<div align="center">

<img
  src="../../embed/color_event_lock.png"
  alt="Piolín Color Sensor event-latching logic"
  width="800"
/>

<br>

<sub><b>Figure 6.6.</b> One physical color region may produce several sensor samples, but the event-latching logic allows it to create only one progression event.</sub>

</div>

Conceptually:

```text
valid color detected
        ↓
register one event
        ↓
lock
        ↓
ignore repeated samples from same region
        ↓
robot moves away
        ↓
re-arm detector
```

The objective is:

```text
1 physical marking
=
1 software event
```

rather than:

```text
1 sensor reading
=
1 event
```

This distinction is essential for reliable corner and lap counting.

---

# 6.8 Why a Cooldown Alone Is Not Always Ideal

A simple implementation could use only time:

```text
detect color
      ↓
wait fixed time
      ↓
allow next color
```

This can reduce double counting, but the physical distance travelled during that time depends on vehicle speed.

For example:

```text
same cooldown
+
different speed
=
different physical lock distance
```

A more physically meaningful system can consider whether Piolín has actually moved sufficiently away from the previous marking.

Possible evidence can include:

```text
encoder movement

return to non-target floor

physical progression state
```

The exact current implementation can continue to evolve, but the engineering objective remains the same: **prevent repeated counting without suppressing the next legitimate event**.

---

# 6.9 Why Neutral Floor Can Be Useful

Between colored regions, the sensor normally observes ordinary track surface.

That provides a conceptual sequence such as:

```text
NORMAL FLOOR
      ↓
BLUE / ORANGE
      ↓
EVENT
      ↓
NORMAL FLOOR
      ↓
ready for next event
```

Returning to ordinary floor can therefore help confirm that Piolín has left the previous marking.

However, navigation should not depend blindly on one perfect neutral-floor sample.

Lighting, sensor height, and the physical edge of the marking can produce transitional readings.

The event logic should therefore be robust enough to distinguish:

```text
still crossing same region
```

from:

```text
entered a new physical course region
```

without requiring ideal laboratory readings.

---

# 6.10 Course Progression

Once the initial direction has been determined, later color events can help Piolín track its progression around the course.

For the WRO Future Engineers Open round, the intended complete navigation contains:

```text
3 laps

12 corners
```

Color markings provide external landmarks that can support this progress count.

Conceptually:

```text
color event
     ↓
validate
     ↓
update progression state
     ↓
continue navigation
```

This is preferable to estimating the entire round only through:

```text
time

motor encoder distance

gyro angle accumulation
```

because the course itself supplies observable physical events.

---

# 6.11 Color Events and Corner Logic

A floor-color event can provide useful evidence that Piolín is approaching or entering a meaningful course section.

However, the Color Sensor should not necessarily be treated as the only evidence for a turn.

A more robust navigation model can combine:

```text
floor event

wall geometry

current corner count

gyro information during Open
```

For example:

```text
color progression evidence
        +
geometry consistent with corner
        ↓
corner state becomes valid
```

The exact weighting belongs to the Open navigation strategy, but the Color Sensor's role is to provide an external landmark rather than replacing all geometric sensing.

---

# 6.12 Why the Sensor Is Downward-Facing

The Color Sensor is mounted toward the floor because the information of interest exists on the track surface.

This orientation isolates its role from the other sensors.

```text
ULTRASONICS
→ side walls


GYRO
→ chassis rotation


PIXY
→ forward visual targets


COLOR
→ floor
```

Each sensor is therefore physically oriented toward the environmental feature it is intended to measure.

This makes the architecture easier to interpret and debug.

---

# 6.13 Optical Measurement Environment

A color sensor does not measure an abstract color label directly.

Its optical response can be influenced by:

```text
ambient light

surface reflectivity

sensor height

sensor angle

shadows

track material
```

Therefore the physical environment around the sensor affects the measurement before software processing begins.

During Piolín development, variations in environmental light made floor-color detection less repeatable.

Instead of responding only by making software thresholds broader, the team introduced a **physical light-isolation casing**.

---

# 6.14 Color Sensor Casing

<div align="center">

<img
  src="../../v-photos/v4/color_sensor_casing.jpg"
  alt="Piolín custom casing surrounding the EV3 Color Sensor"
  width="680"
/>

<br>

<sub><b>Figure 6.7.</b> Physical light-isolation casing used around Piolín's downward-facing Color Sensor.</sub>

</div>

The purpose of the casing is to reduce uncontrolled external light reaching the measurement region.

Conceptually:

```text
WITHOUT ISOLATION

course surface
+
room lighting
+
side reflections
+
shadows
      ↓
greater measurement variation
```

With physical isolation:

```text
course surface
+
more controlled optical environment
      ↓
more repeatable reading conditions
```

The casing does not guarantee perfect detection.

Its purpose is to improve the physical conditions under which the sensor operates.

---

# 6.15 Why a Mechanical Solution Was Preferred

A common software response to changing color measurements is to continually widen acceptable thresholds.

That can create another problem.

```text
wide threshold
→ easier detection
→ greater possibility of classifying unrelated floor values as target color
```

Improving the sensor's physical environment instead attacks one source of variation before classification occurs.

This led to an important engineering principle:

> **If a measurement is unstable because of the physical environment, improve the physical measurement conditions before compensating entirely in software.**

The Color Sensor casing is a direct example of this principle.

---

# 6.16 RGB / Reflected-Light Calibration

Color detection should be calibrated on the actual competition surface.

Depending on the software mode used, useful raw information can include components such as:

```text
R

G

B
```

or reflected-light behavior.

The correct classification values should be determined experimentally from Piolín's current sensor position and casing.

A basic calibration process can collect measurements for:

```text
Blue region

Orange region

normal floor
```

under representative lighting.

The current documentation intentionally does not publish invented final RGB thresholds.

Those values should come from measured data.

---

# 6.17 Calibration Should Use Ranges, Not One Sample

One sensor sample does not describe a complete color class.

For example, several Blue measurements might vary slightly:

```text
Blue sample 1

Blue sample 2

Blue sample 3

...
```

The objective is to understand a **distribution or useful range**, not memorize one reading.

The same applies to Orange and normal floor.

Calibration should therefore consider:

```text
multiple samples

different positions on marking

representative lighting

real installed sensor height
```

This produces more useful classification boundaries than selecting one ideal laboratory value.

---

# 6.18 Static vs. Dynamic Color Testing

Static calibration is useful for understanding raw measurements.

However:

```text
sensor held over color
```

is not identical to:

```text
robot driving across color
```

During movement, several additional effects appear:

```text
shorter observation time

transition across edge

vehicle vibration

changing illumination

control-loop timing
```

Dynamic testing is therefore necessary before a color classifier can be considered reliable for competition use.

A classification that works while Piolín is stationary may still miss a marking when the robot crosses it at speed.

---

# 6.19 Detection Persistence

One possible way to reject noise is to require multiple consistent samples.

For example:

```text
BLUE
BLUE
→ valid Blue
```

instead of reacting to one isolated measurement.

However, excessive confirmation creates a different risk.

```text
more confirmations
→ greater confidence
→ slower reaction
```

If Piolín crosses a color marking quickly, requiring too many samples can cause the robot to leave the region before validation completes.

The appropriate persistence therefore depends on:

```text
vehicle speed

control-loop frequency

marking size

sensor position
```

and should be calibrated experimentally.

---

# 6.20 False Positives vs. Missed Events

Color classification contains a familiar engineering trade-off.

```text
threshold too permissive
→ false color events


threshold too restrictive
→ real color events missed
```

The goal is not to classify every uncertain sample.

The goal is to reliably identify the physical events needed for navigation.

This is another reason the casing is useful: reducing optical variation can make the classification problem easier without expanding the software acceptance region excessively.

---

# 6.21 Sensor Height

Distance between the Color Sensor and the floor can affect the measurement.

If the sensor is moved vertically:

```text
illumination geometry changes

observed area changes

reflected signal changes
```

For reproducibility, the sensor should therefore remain mechanically fixed at the same operating height.

The exact current V4 sensor-to-floor distance should be measured before it is published as a final specification.

Until then, the important requirement is:

```text
fixed mounting
+
repeatable geometry
```

rather than an unverified numerical value.

---

# 6.22 Sensor Position and Event Timing

The Color Sensor is not located at the exact geometric center of the vehicle.

Therefore:

```text
sensor crosses marking
```

occurs before or after other parts of the chassis reach the same location.

This matters when color detection is used to trigger or support:

```text
corner preparation

state changes

progress counting

parking logic
```

The software should therefore interpret the event according to the **actual sensor position**, not as though the complete robot crossed the marking simultaneously.

This is another reason physical sensor placement belongs in the navigation model.

---

# 6.23 Interaction with Ackermann Motion

During a straight section, the Color Sensor crosses a marking with relatively predictable orientation.

During a turn, the sensor follows an arc with the chassis.

Its physical path is therefore affected by:

```text
steering angle

wheelbase

sensor offset

vehicle trajectory
```

This can alter:

```text
where the sensor intersects the marking

how long it remains above the marking
```

Color-event testing should therefore include realistic corner behavior rather than only perfectly straight crossings.

---

# 6.24 Color Sensor During Open

During the Open Challenge, the relevant sensor architecture is:

```text
S1 = Gyro

S2 = Left Ultrasonic

S3 = Right Ultrasonic

S4 = Color
```

The roles are separated:

```text
GYRO
→ orientation


ULTRASONICS
→ wall geometry


COLOR
→ direction and course progression
```

The Color Sensor therefore acts as a state reference rather than as the primary steering sensor.

The EV3 can combine the event with the current wall and heading information before deciding how Motor B should respond.

---

# 6.25 Color Sensor During Obstacles

The Color Sensor remains installed during the Obstacle Challenge.

The sensing architecture becomes:

```text
S1 = Pixy2.1

S2 = Left Ultrasonic

S3 = Right Ultrasonic

S4 = Color
```

Again, the roles remain distinct:

```text
PIXY2.1
→ visual target identity


ULTRASONICS
→ lateral physical context


COLOR
→ floor course state
```

The Color Sensor does not replace Pixy2.1.

A red or green pillar is a forward visual target, while Blue and Orange course markings are physical floor features.

These are different perception problems and are intentionally handled by different sensors.

---

# 6.26 Color Sensor vs. Pixy2.1

Although both devices perceive color, their roles should not be confused.

| Feature | EV3 Color Sensor | Pixy2.1 |
| :--- | :--- | :--- |
| Orientation | Downward | Forward |
| Main target | Course surface | Pillars / parking visual target |
| Current port | S4 | S1 during Obstacles |
| Direction detection | Yes | No |
| Course floor events | Yes | No |
| Red/Green pillar identity | No | Yes |
| Image coordinates | No | Yes |
| Permanent between rounds | Yes | No |

The similarity is only that both use optical information.

Their physical measurement problems are fundamentally different.

---

# 6.27 Why Vision Does Not Replace the Floor Sensor

It would be theoretically possible to attempt to recognize additional track features with the forward camera.

However, that would introduce several unnecessary dependencies:

```text
camera field of view

camera orientation

lighting ahead of vehicle

visual target selection

perspective
```

The downward-facing Color Sensor has a much simpler physical relationship with the floor markings.

The sensor is therefore retained because:

```text
simple dedicated measurement
```

is preferable to:

```text
forcing a more complex sensor
to solve an additional problem
```

when the dedicated device already works with the EV3 architecture.

---

# 6.28 Why Encoders Do Not Replace the Color Sensor

Motor encoders can estimate relative vehicle movement.

However:

```text
encoder movement
```

can differ from:

```text
actual track displacement
```

because of:

```text
wheel slip

turning

mechanical variation
```

Encoder error can also accumulate across a long run.

A floor color is different.

It is an **external course landmark**.

Therefore:

```text
ENCODER
→ relative vehicle motion


COLOR MARKING
→ physical course event
```

The two sources can complement one another, but they are not equivalent.

---

# 6.29 Why the Gyro Does Not Replace the Color Sensor

The Gyro Sensor measures rotation.

It can help determine:

```text
heading

turn progress

angular change
```

but it cannot identify a Blue or Orange region on the track.

A robot could theoretically accumulate approximately 90° of rotation without knowing which physical course marking it had crossed.

The Color Sensor provides that external state reference.

The Open architecture therefore assigns each sensor according to what it physically measures best.

---

# 6.30 Course Counting and Three-Lap Completion

The complete Open round requires Piolín to progress through the course repeatedly.

The Color Sensor can support the progression model by providing discrete physical events.

A conceptual state may include:

```text
direction

color-event count

corner count

lap progression
```

The objective is eventually to establish:

```text
known start
      ↓
validated course events
      ↓
12 corners
      ↓
3 laps
      ↓
parking state
```

The exact parking trigger remains part of active software development.

For that reason, this component document explains the sensor's contribution without presenting an unfinished parking algorithm as a final solution.

---

# 6.31 Avoiding Double Corner Counts

One important historical problem occurred when software detected multiple samples while physically crossing one course region.

Without a latch:

```text
one marking
↓
sample 1 → count

sample 2 → count

sample 3 → count
```

which creates a false progression state.

The intended behavior is:

```text
one marking
↓
many sensor samples
↓
one validated event
↓
one count
```

This is one of the strongest reasons the software separates:

```text
raw color detection
```

from:

```text
course-event counting
```

---

# 6.32 Why Course State Matters

A sensor reading becomes much more useful when interpreted together with navigation state.

For example:

```text
BLUE detected at startup
```

may mean:

```text
set direction COUNTERCLOCKWISE
```

while a later Blue detection may mean:

```text
update progression
```

The physical color is the same.

The meaning changes because the robot is in a different state.

This can be represented as:

```text
COLOR
+
CURRENT STATE
=
COURSE MEANING
```

The Color Sensor therefore participates in a state machine rather than functioning as a simple one-line `if color == blue` controller.

---

# 6.33 Color Sensor Diagnostics

Before testing complete navigation, the sensor can be verified independently.

A useful diagnostic test should confirm:

```text
normal floor
→ plausible normal reading


Blue marking
→ classified as Blue


Orange marking
→ classified as Orange
```

Then the robot should be moved across the marking to confirm that:

```text
one physical region
→ one software event
```

This separates several possible failure types:

```text
optical problem

classification problem

event-latch problem

course-state problem
```

before full steering behavior is evaluated.

---

# 6.34 Pre-Run Verification

A simple pre-run process is:

```text
1. Check sensor mount.

2. Check casing position.

3. Confirm sensor faces floor.

4. Confirm S4 connection.

5. Read normal floor.

6. Test Blue.

7. Test Orange.

8. Verify direction mapping.

9. Verify one marking produces one event.

10. Begin track test.
```

This sequence is much faster than discovering during a complete run that the Color Sensor was misaligned or incorrectly classified.

---

# 6.35 Values Intentionally Not Claimed as Final

The following values should only be published after they are measured on the current V4 robot:

```text
sensor-to-floor height

exact sensor longitudinal position

exact sensor lateral offset

final RGB ranges

final reflected-light thresholds

number of confirmation samples

event release distance

final cooldown time if used

dynamic detection reliability

Blue/Orange classification accuracy
```

Older values from previous Piolín versions should not automatically become current calibration values.

Any future graph such as:

```text
color_rgb_calibration.png
```

should only be created after real measurements have been recorded.

---

# 6.36 Current Color Sensor Responsibility Matrix

| Function | Open Challenge | Obstacle Challenge |
| :--- | :---: | :---: |
| Blue floor detection | Yes | Yes |
| Orange floor detection | Yes | Yes |
| Initial direction selection | Yes | Yes |
| Course progression | Yes | Yes |
| Wall distance | No | No |
| Vehicle heading | No | No |
| Red pillar detection | No | No |
| Green pillar detection | No | No |
| Pixy visual coordinates | No | No |
| Physical floor landmark | Yes | Yes |

This illustrates why the Color Sensor remains installed in both round configurations.

Its information is useful regardless of which device occupies S1.

---

# 6.37 Current Color Sensor Architecture

The complete role of S4 can be summarized as:

```text
                    COURSE FLOOR
                         │
                         ▼
                EV3 COLOR SENSOR
                         │
                         ▼
                        S4
                         │
                         ▼
                   LEGO EV3
                         │
              ┌──────────┴──────────┐
              │                     │
              ▼                     ▼
      INITIAL DIRECTION       COURSE EVENTS
              │                     │
        ┌─────┴─────┐               ▼
        │           │          PROGRESSION
        ▼           ▼
      BLUE        ORANGE
        │           │
        ▼           ▼
      CCW           CW
```

The Color Sensor provides a physical connection between Piolín's software state and fixed features of the competition course.

That is its primary value.

---

# 6.38 Final Engineering Assessment

Piolín's Color Sensor architecture is based on a simple but important principle:

> **The Color Sensor does not control where the robot should steer. It tells the navigation system which physical course event Piolín has reached.**

Its permanent assignment is:

```text
S4
→ downward-facing EV3 Color Sensor
```

Its primary roles are:

```text
Blue / Orange recognition

initial direction selection

course-event detection

progress tracking
```

The sensor also demonstrates how mechanical and software design interact.

The casing improves the optical environment physically.

Classification interprets the resulting sensor measurement.

Event latching converts repeated samples into one physical event.

The state machine assigns that event its navigation meaning.

The complete chain is therefore:

```text
COURSE MARKING
      ↓
PHYSICAL LIGHT ENVIRONMENT
      ↓
COLOR SENSOR
      ↓
CLASSIFICATION
      ↓
EVENT VALIDATION
      ↓
COURSE STATE
      ↓
NAVIGATION LOGIC
```

This layered approach is more reliable than treating every raw color sample as an immediate steering command.

Piolín therefore uses the Color Sensor as a dedicated **course-state reference**, complementing the geometric, rotational, and visual sensors used elsewhere in the robot.

---

<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
