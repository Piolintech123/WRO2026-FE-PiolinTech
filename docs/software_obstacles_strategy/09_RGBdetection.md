# 9. RGB Floor Detection

<div align="center">

<img
  src="../../v-photos/v4/color_sensor_s4_installed.jpg"
  alt="Piolín downward-facing EV3 Color Sensor installed on S4"
  width="680"
/>

<br>

<sub><b>Figure 9.1.</b> Piolín's S4 Color Sensor observes the floor and provides course-state information independently from Pixy2.1 obstacle vision.</sub>

</div>

Piolín uses the LEGO Mindstorms EV3 Color Sensor on **Sensor Port S4** to detect colored floor markings used as physical course landmarks.

This sensing system must remain clearly separated from the Obstacle Challenge camera system.

```text
S4 COLOR SENSOR
→ floor beneath Piolín
→ Blue / Orange course markings
→ direction / progression events
```

while:

```text
PIXY2.1
→ objects ahead
→ Red / Green pillars
→ Pink parking reference
```

The Color Sensor therefore does **not** identify Red and Green traffic pillars, and Pixy2.1 does not replace S4's floor-state role.

Piolín's software development has tested both:

```text
built-in color classification
```

and:

```text
raw RGB + reflection classification
```

for detecting the competition floor markings.

The current engineering direction favors treating a floor color as a **confirmed software event**, not simply reacting to one instantaneous sensor sample.

---

## 9.1 Why RGB Detection Is Useful

A simple implementation can ask the EV3 Color Sensor to return a named color.

For example, one Piolín prototype uses:

```python
detected = color_sensor.color()

if detected == Color.BLUE:
    return 'BLUE'

if detected in (
    Color.RED,
    Color.YELLOW,
    Color.BROWN
):
    return 'ORANGE'
```

This approach is useful because it is:

```text
simple

easy to debug

easy to understand
```

However, the physical Orange course marking may not always be classified by the EV3 as one identical named color under every condition.

Depending on:

```text
lighting

sensor height

surface reflectivity

sensor casing

course material
```

the same Orange region may appear closer to:

```text
RED

YELLOW

BROWN
```

in built-in classification.

For this reason, Piolín has also tested a more explicit method using the individual RGB channels.

---

# 9.2 Current Sensor Installation

<div align="center">

<img
  src="../../v-photos/v4/color_sensor_bottom_view.jpg"
  alt="Bottom view of Piolín's downward-facing Color Sensor"
  width="660"
/>

<br>

<sub><b>Figure 9.2.</b> S4 is mounted downward so that floor measurements correspond to the physical area immediately beneath Piolín.</sub>

</div>

The current permanent sensor mapping is:

```text
S4
→ EV3 Color Sensor
```

The sensor remains installed in both competition configurations.

Its role is independent from the round-specific S1 device:

```text
OPEN
S1 → Gyro
S4 → Color
```

```text
OBSTACLES
S1 → Pixy2.1
S4 → Color
```

The physical sensor height and orientation should remain as consistent as practical because RGB and reflection values depend strongly on the optical geometry between:

```text
sensor

floor

ambient light
```

---

# 9.3 Color Sensor Casing

<div align="center">

<img
  src="../../v-photos/v4/color_sensor_casing.jpg"
  alt="Piolín Color Sensor casing used to reduce ambient illumination"
  width="650"
/>

<br>

<sub><b>Figure 9.3.</b> The current Color Sensor casing is part of the calibrated optical installation.</sub>

</div>

Piolín uses a physical casing around the downward-facing Color Sensor.

The purpose of the casing is to make the sensor environment more controlled by reducing some uncontrolled ambient illumination reaching the measurement area.

This does not mean lighting effects are completely eliminated.

Instead, the design principle is:

```text
improve physical optical conditions
        ↓
measure RGB values
        ↓
classify in software
```

rather than relying entirely on software to compensate for an unstable physical sensor environment.

For this reason, RGB calibration should always be performed with the **current casing installed**.

---

# 9.4 Reading Reflection and RGB

One of Piolín's development programs reads both reflected-light intensity and the individual color channels:

```python
reflection = color.reflection()
red, green, blue = color.rgb()
```

This gives two different types of information.

```text
reflection
→ overall reflected-light behavior
```

while:

```text
red
green
blue
→ relative color composition
```

The software can therefore make decisions based on both:

```text
brightness
+
channel relationships
```

instead of relying on a single named-color result.

The high-level process is:

```text
FLOOR
  ↓
S4 SENSOR
  ↓
reflection + R/G/B
  ↓
classification rules
  ↓
BLUE / ORANGE / NONE
```

---

# 9.5 Prototype Orange Classification

The RGB-based prototype contains a dedicated Orange classifier.

Its development logic is:

```python
orange = (
    red >= ORANGE_MIN_RED
    and green >= ORANGE_MIN_GREEN
    and red >= green * ORANGE_RED_OVER_GREEN
    and red > blue * ORANGE_RED_OVER_BLUE
    and green > blue * ORANGE_GREEN_OVER_BLUE
    and red - blue >= ORANGE_MIN_DIFFERENCE
)
```

This is more informative than checking only:

```text
red > blue
```

because the classifier considers several relationships simultaneously.

Conceptually, Orange is expected to contain:

```text
meaningful Red

meaningful Green

less Blue

Red sufficiently dominant
```

The software therefore asks:

```text
Is Red high enough?

Is Green high enough?

Is Red sufficiently stronger than Blue?

Is Green sufficiently stronger than Blue?

Is Red sufficiently related to Green?
```

before accepting the surface as Orange.

This reduces dependence on one exact RGB triplet.

---

# 9.6 Why Ratios Are Useful

Absolute sensor values can change when overall lighting changes.

For example, two measurements may look like:

```text
R = higher
G = higher
B = higher
```

under stronger illumination while preserving a similar color relationship.

Ratio-style logic can therefore be more useful than requiring:

```text
R == exact number

G == exact number

B == exact number
```

The development classifier uses relationships such as:

```python
red > blue * ORANGE_RED_OVER_BLUE
```

and:

```python
green > blue * ORANGE_GREEN_OVER_BLUE
```

This expresses:

```text
Red should be sufficiently stronger than Blue
```

rather than:

```text
Red must always equal one fixed reading
```

The final numerical ratios still require calibration on the current physical robot.

The important architecture is the use of **channel relationships**, not the exact temporary numbers.

---

# 9.7 Prototype Blue Classification

<div align="center">

<img
  src="../../v-photos/v4/color_sensor_blue_mark.jpg"
  alt="Piolín Color Sensor positioned over the Blue floor marking"
  width="650"
/>

<br>

<sub><b>Figure 9.4.</b> Blue detection can combine reflected intensity with relative channel dominance.</sub>

</div>

The same prototype identifies Blue using:

```python
blue_line = (
    reflection <= BLUE_REFLECTION_THRESHOLD
    and blue >= red
    and blue >= green
)
```

Conceptually, the classifier requires:

```text
suitable reflection level
+
Blue channel >= Red
+
Blue channel >= Green
```

This provides more context than simply checking:

```text
blue is the largest channel
```

because a surface with weak or unusual optical behavior can otherwise produce misleading relative values.

The development code then applies a clear priority:

```python
if orange:
    return "ORANGE"

if blue_line:
    return "BLUE"

return None
```

The result is one of three software states:

```text
ORANGE

BLUE

NONE
```

---

# 9.8 Prototype Values Are Not Final Calibration

The RGB prototype currently contains working constants such as:

```python
BLUE_REFLECTION_THRESHOLD = 50

ORANGE_RED_OVER_BLUE = 1.15
ORANGE_GREEN_OVER_BLUE = 0.95
ORANGE_RED_OVER_GREEN = 0.95

ORANGE_MIN_RED = 8
ORANGE_MIN_GREEN = 4
ORANGE_MIN_DIFFERENCE = 3
```

These values are useful engineering evidence because they show how Piolín's RGB classifier has been structured.

However, they should be interpreted as:

```text
PROTOTYPE / WORKING PARAMETERS
```

rather than:

```text
FINAL V4 COLOR SPECIFICATION
```

The final values should be determined from repeated measurements of the actual:

```text
Blue marking

Orange marking

normal floor
```

with:

```text
current S4 position

current casing

representative track

representative lighting
```

A final raw RGB calibration table has not yet been established, so the repository should not claim that these temporary values are universally validated.

---

# 9.9 Recommended Calibration Dataset

Before finalizing the RGB classifier, PiolínTech should collect repeated measurements under the actual installed configuration.

A useful table is:

| Surface | Reflection | Red | Green | Blue |
| :--- | :---: | :---: | :---: | :---: |
| Blue — Sample 1 | — | — | — | — |
| Blue — Sample 2 | — | — | — | — |
| Blue — Sample 3 | — | — | — | — |
| Blue — Sample 4 | — | — | — | — |
| Blue — Sample 5 | — | — | — | — |
| Orange — Sample 1 | — | — | — | — |
| Orange — Sample 2 | — | — | — | — |
| Orange — Sample 3 | — | — | — | — |
| Orange — Sample 4 | — | — | — | — |
| Orange — Sample 5 | — | — | — | — |
| Normal — Sample 1 | — | — | — | — |
| Normal — Sample 2 | — | — | — | — |
| Normal — Sample 3 | — | — | — | — |
| Normal — Sample 4 | — | — | — | — |
| Normal — Sample 5 | — | — | — | — |

The objective is not to calculate one average and discard the rest.

The dataset should reveal:

```text
normal variation

minimum values

maximum values

overlap between surfaces

lighting sensitivity
```

so that thresholds can be placed between real measured ranges.

---

# 9.10 Static Detection Is Not Enough

A classifier can work perfectly while Piolín is stationary and still fail during a run.

When the robot moves:

```text
sensor approaches marking
      ↓
only part of sensing area sees color
      ↓
full marking passes underneath
      ↓
sensor begins leaving marking
```

The RGB values therefore change continuously.

Dynamic testing should include:

```text
slow crossing

normal driving speed

representative competition speed
```

The question is not only:

```text
Can S4 identify Blue?
```

but:

```text
Can S4 identify Blue while Piolín crosses it quickly enough
for the state machine to use the event?
```

This makes sampling and event management just as important as the RGB classifier itself.

---

# 9.11 RGB Classification and Event Detection Are Separate

A crucial software distinction is:

```text
COLOR CLASSIFICATION
```

versus:

```text
COURSE EVENT
```

The classifier answers:

```text
What surface does S4 currently see?
```

The event layer answers:

```text
Has Piolín just crossed a NEW physical marking?
```

These are not the same thing.

One physical strip can remain beneath the sensor for many program cycles:

```text
BLUE
BLUE
BLUE
BLUE
BLUE
```

but should normally produce:

```text
ONE BLUE EVENT
```

not:

```text
FIVE EVENTS
```

The software therefore requires state memory.

---

# 9.12 Line Locking in Piolín's Prototype

The RGB prototype already implements a line-lock mechanism.

When a line is registered:

```python
line_locked = True
neutral_reads = 0
last_line_angle = drive.angle()
```

While locked, additional readings of the same colored region do not create another event.

The update logic waits for neutral readings:

```python
if detected is None:
    neutral_reads += 1

    if neutral_reads >= 2:
        line_locked = False
        neutral_reads = 0
```

Conceptually:

```text
NORMAL FLOOR
      ↓
BLUE / ORANGE detected
      ↓
REGISTER EVENT
      ↓
LOCK
      ↓
remain over marking
      ↓
do NOT register again
      ↓
neutral floor confirmed
      ↓
RE-ARM
```

This is one of the strongest parts of the current floor-detection architecture.

---

# 9.13 Encoder Separation as Additional Protection

The same RGB prototype also checks vehicle displacement before accepting another physical line:

```python
if (
    blue_count + orange_count == 0
    or motor_distance(last_line_angle)
       >= MIN_DEG_BETWEEN_LINES
):
    register_line(detected)
```

This creates two layers of duplicate protection:

```text
SENSOR RELEASE
+
MINIMUM VEHICLE PROGRESSION
```

The reason is practical.

Suppose the Color Sensor briefly reports:

```text
Blue
→ None
→ Blue
```

while Piolín is still physically near the same marking.

A pure release-only system may accidentally count:

```text
two lines
```

The encoder condition adds the question:

```text
Has Piolín physically moved far enough
for this to plausibly be another landmark?
```

The exact required encoder distance remains a calibration parameter.

---

# 9.14 Initial Direction vs. Later Progress

Piolín uses the first valid floor color differently from later color events.

The development code shows:

```python
if direction is None:
    if name == "BLUE":
        direction = "ANTIHORARIO"
    else:
        direction = "HORARIO"
```

Therefore:

```text
FIRST BLUE
→ COUNTERCLOCKWISE
```

```text
FIRST ORANGE
→ CLOCKWISE
```

Once direction is established, later floor detections primarily provide:

```text
course progression

landmark counting

state information
```

The first event therefore contains two pieces of information:

```text
COLOR
+
INITIAL DIRECTION
```

while later events mainly contribute:

```text
PROGRESS
```

The direction should not be continuously recalculated every time a new marking is detected.

---

# 9.15 Role During the Obstacle Challenge

Even though the RGB classifier was developed heavily through Open Challenge testing, the S4 architecture remains relevant during Obstacles.

The obstacle system should maintain a separation of responsibilities:

```text
PIXY2.1
→ Red / Green pillar perception
```

```text
S2/S3
→ lateral physical geometry
```

```text
S4 RGB
→ floor/course landmarks
```

The Color Sensor can therefore support:

```text
course progression

corner context

lap state

parking eligibility
```

without directly deciding:

```text
pillar passing side
```

This is important because Red has two completely different meanings depending on which sensor is involved.

For Pixy:

```text
Red visual pillar
→ obstacle
→ PASS RIGHT
```

For S4:

```text
Red-like RGB response
```

may simply be part of the classifier used to recognize:

```text
ORANGE FLOOR
```

The software should keep these sensing domains separate.

---

# 9.16 Avoiding Ambiguous Variable Names

Because both systems involve colors, descriptive variable names are important.

Poor naming would be:

```python
red_detected
```

because that could mean:

```text
Pixy Red pillar
```

or:

```text
S4 Red RGB channel / Orange classification
```

A clearer architecture uses names such as:

```python
floor_color
pixy_signature

floor_orange
pillar_red

rgb_red
rgb_green
rgb_blue
```

This reduces the chance that:

```text
floor color logic
```

accidentally influences:

```text
pillar logic
```

or vice versa.

---

# 9.17 Recommended Software Structure

The RGB subsystem can be divided conceptually into three functions.

### 1. Read optical data

```python
def read_floor_rgb():
    reflection = color.reflection()
    red, green, blue = color.rgb()

    return reflection, red, green, blue
```

### 2. Classify the current surface

```python
def classify_floor(
    reflection,
    red,
    green,
    blue
):
    # Apply calibrated Blue / Orange rules.
    ...
```

### 3. Convert classification into a course event

```python
def update_floor_event():
    detected = classify_floor(...)

    # Apply lock, release and progression rules.
    ...
```

This creates:

```text
HARDWARE
   ↓
RGB READING
   ↓
CLASSIFICATION
   ↓
EVENT FILTER
   ↓
COURSE STATE
```

Separating these responsibilities makes later tuning much easier.

---

# 9.18 Why RGB Thresholds Should Be Centralized

RGB constants should remain in one calibration section rather than being scattered through the program.

For example:

```python
# Floor RGB calibration

BLUE_REFLECTION_THRESHOLD = ...

ORANGE_RED_OVER_BLUE = ...
ORANGE_GREEN_OVER_BLUE = ...
ORANGE_RED_OVER_GREEN = ...

ORANGE_MIN_RED = ...
ORANGE_MIN_GREEN = ...
ORANGE_MIN_DIFFERENCE = ...
```

Then classification functions reference those values.

This makes it possible to change:

```text
sensor calibration
```

without modifying:

```text
navigation architecture
```

It also makes Git comparisons much clearer.

A reviewer can see:

```text
only RGB calibration changed
```

rather than searching through many unrelated controller changes.

---

# 9.19 Failure Diagnosis

RGB problems should be diagnosed according to layer.

| Symptom | First Layer to Check |
| :--- | :--- |
| No values from S4 | Wiring / sensor interface |
| RGB values change unpredictably | Mounting, casing, lighting |
| Blue raw data looks correct but returns `None` | Blue classifier |
| Orange appears as normal floor | Orange ratios / thresholds |
| Normal floor becomes Orange | Classifier too permissive |
| Correct classification but event counted twice | Lock / release logic |
| Event completely missed at high speed | Sampling / confirmation / speed |
| First Blue chooses wrong direction | Direction-state mapping |
| RGB works but pillar maneuver wrong | Not S4; inspect Pixy/controller |
| Red pillar confused with Orange floor in software | Variable/domain separation |

The diagnostic sequence should be:

```text
RAW RGB
  ↓
CLASSIFICATION
  ↓
EVENT
  ↓
COURSE STATE
```

Do not modify the RGB thresholds if:

```text
raw + classification are already correct
```

and the actual failure occurs later in:

```text
event counting

state transition

navigation
```

---

# 9.20 Development Telemetry

During calibration, the RGB subsystem should print enough information to compare the physical surface with the software decision.

A useful output format is:

```text
REF: ...
R: ...
G: ...
B: ...
CLASS: BLUE
LOCK: True
B_COUNT: ...
O_COUNT: ...
```

For example:

```python
print(
    "REF:", reflection,
    "R:", red,
    "G:", green,
    "B:", blue,
    "FLOOR:", detected
)
```

Once the classifier works reliably, verbose RGB logging can be reduced for competition runs.

During development, however, raw telemetry is essential because it shows **why** the classifier produced a particular result.

---

# 9.21 Current Prototype vs. Final RGB Detector

Piolín has already tested two useful approaches.

### Built-in classification prototype

```python
if detected == Color.BLUE:
    return "BLUE"

if detected in (
    Color.RED,
    Color.YELLOW,
    Color.BROWN
):
    return "ORANGE"
```

Advantages:

```text
simple

compact

fast to implement
```

### RGB + reflection prototype

```python
reflection = color.reflection()
red, green, blue = color.rgb()
```

followed by explicit relational rules.

Advantages:

```text
greater visibility into raw sensor behavior

thresholds can be calibrated directly

Orange can be identified from channel relationships

easier to diagnose borderline classifications
```

The final selection should be based on repeatable track testing.

The existence of both prototypes demonstrates an iterative development process rather than two contradictory final architectures.

---

# 9.22 Complete RGB Detection Pipeline

The intended floor-detection process can be summarized as:

```text
                       TRACK FLOOR
                            │
                            ▼
                      COLOR SENSOR S4
                            │
                  ┌─────────┴─────────┐
                  │                   │
                  ▼                   ▼
            REFLECTION             RGB VALUES
                                  R / G / B
                  │                   │
                  └─────────┬─────────┘
                            ▼
                     FLOOR CLASSIFIER
                            │
                ┌───────────┼───────────┐
                │           │           │
                ▼           ▼           ▼
              BLUE       ORANGE       NONE
                │           │           │
                └─────┬─────┘           │
                      ▼                 │
               EVENT LOCK CHECK         │
                      │                 │
                      ▼                 │
              ENCODER SEPARATION?       │
                      │                 │
                     YES                │
                      │                 │
                      ▼                 │
                REGISTER EVENT          │
                      │                 │
                      ▼                 │
                    LOCK                │
                      │                 │
                      └────────┐        │
                               ▼        ▼
                         NEUTRAL FLOOR
                               │
                               ▼
                             RE-ARM
                               │
                               ▼
                      READY FOR NEXT LINE
```

The RGB classifier and event detector therefore form two distinct layers.

---

# 9.23 Final Engineering Assessment

Piolín's RGB detection system turns the EV3 Color Sensor from a simple named-color detector into a more controlled **course-landmark perception subsystem**.

The current development has explored both:

```text
built-in EV3 color classification
```

and:

```text
raw reflection + RGB relationships
```

The RGB-based prototype demonstrates a stronger engineering structure because it allows the team to inspect and tune the relationships between:

```text
Red

Green

Blue

overall reflection
```

directly.

Orange detection uses relative channel relationships rather than one exact RGB value, while Blue detection combines channel dominance with reflected-light information.

However, the current numeric thresholds remain **prototype calibration values**. A final RGB table for the current physical robot should be collected before those values are presented as validated specifications.

The optical installation also matters.

The S4 sensor should be calibrated with:

```text
its current downward orientation

its current height

its current casing

the actual track surface

representative lighting
```

Detection itself is only the first layer.

Piolín additionally uses:

```text
event locking

neutral-floor release

vehicle-progression checks
```

to convert many consecutive sensor samples into one physical course event.

Finally, RGB floor detection must remain conceptually separate from Pixy2.1 obstacle recognition:

```text
S4 RGB
→ Blue / Orange floor state
```

```text
Pixy2.1
→ Red / Green pillars
→ Pink parking reference
```

The central principle is:

> **Piolín should first measure the floor, classify the optical pattern, confirm that it represents a new physical landmark, and only then update course state. A raw RGB reading should never directly become a steering command.**

This architecture makes floor detection easier to calibrate, test, and modify without coupling optical thresholds directly to obstacle avoidance or Motor B behavior.

---

<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
