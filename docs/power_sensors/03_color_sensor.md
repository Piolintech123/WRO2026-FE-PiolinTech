# 3. Color Sensor Detection and Course-State Processing

Piolín uses a **LEGO Color Sensor connected to EV3 input S4** as the main floor-event sensor for the WRO Future Engineers course.

The sensor is mounted underneath the robot and faces downward toward the track surface.

Its current responsibilities are:

```text
Detect BLUE floor markings

Detect ORANGE floor markings

Determine initial travel direction

Track valid course events

Support corner / lap progression

Support the final run state
```

The color sensor does **not** directly control Motor B or determine the physical steering angle.

Instead, it provides information about **where Piolín is in the course sequence**.

The complete relationship is:

```text
TRACK FLOOR
     ↓
COLOR SENSOR S4
     ↓
COLOR MEASUREMENT
     ↓
EVENT CLASSIFICATION
     ↓
COURSE STATE
     ↓
LEGO EV3
     ↓
NAVIGATION BEHAVIOR
```

This makes the color sensor a **state sensor** rather than a direct wall-navigation sensor.

For the complete sensor architecture, see:

[Power and Sensor Configuration](01_PowerSensorconfig.md)

For component-level information, see:

[Color Sensor Hardware](../components/06_ColorSensor.md)

---

## 3.1 Current Color Sensor Configuration

The confirmed current configuration is:

| Parameter | Current Configuration |
| :--- | :--- |
| **EV3 Port** | S4 |
| **Sensor** | LEGO Color Sensor |
| **Orientation** | Downward-facing |
| **Observed Surface** | Competition track floor |
| **Primary colors used** | Blue and Orange |
| **Direction role** | Determines initial course direction |
| **Progress role** | Detects valid floor-marking events |
| **Direct steering role** | None |
| **Mechanical light control** | Dedicated surrounding casing |

The physical arrangement is approximately:

```text
              [ PIOLÍN ]
                  │
                  │
                 S4
                  ▼
             COLOR SENSOR
                  │
                  ▼
        ─────────────────────
              TRACK FLOOR
```

The sensor observes the region immediately beneath the robot.

---

# 3.2 Why the Sensor Faces Downward

The color sensor is intended to observe:

```text
TRACK MARKINGS
```

rather than:

```text
Walls

Pillars

Objects ahead
```

Its downward orientation separates its role from the other perception systems.

```text
ULTRASONICS
      ↓
Track geometry


HUSKYLENS
      ↓
Obstacle identity


COLOR SENSOR
      ↓
Floor / course state
```

This division gives each sensing technology a specific environmental reference.

---

# 3.3 Floor Markings as Navigation Events

A floor color is useful because it represents more than a visual color.

For Piolín, a valid marking is interpreted as a **course event**.

Conceptually:

```text
BLUE / ORANGE REGION
        ↓
S4 detects color
        ↓
EV3 recognizes valid event
        ↓
Course state changes
```

Therefore:

```text
COLOR VALUE
```

is converted into:

```text
NAVIGATION INFORMATION
```

before it influences robot behavior.

---

# 3.4 Initial Direction Detection

At the beginning of the run, Piolín uses the first relevant floor marking to determine travel direction.

The current rule is:

```text
BLUE FIRST
    ↓
COUNTERCLOCKWISE
```

and:

```text
ORANGE FIRST
     ↓
CLOCKWISE
```

This initial color decision affects the interpretation of the lateral ultrasonic sensors.

---

# 3.5 Blue-First Configuration

When the initial valid marking indicates blue:

```text
BLUE
  ↓
COUNTERCLOCKWISE
```

the navigation geometry becomes:

```text
S3 LEFT
=
INNER SENSOR
```

and:

```text
S2 RIGHT
=
OUTER SENSOR
```

The information flow is:

```text
BLUE detected
      ↓
direction = COUNTERCLOCKWISE
      ↓
LEFT = INNER
RIGHT = OUTER
      ↓
Wall-following interpretation established
```

The color sensor therefore indirectly configures the ultrasonic navigation system.

---

# 3.6 Orange-First Configuration

When the initial valid marking indicates orange:

```text
ORANGE
   ↓
CLOCKWISE
```

the sensor roles become:

```text
S2 RIGHT
=
INNER SENSOR
```

and:

```text
S3 LEFT
=
OUTER SENSOR
```

The corresponding information flow is:

```text
ORANGE detected
       ↓
direction = CLOCKWISE
       ↓
RIGHT = INNER
LEFT = OUTER
       ↓
Wall-following interpretation established
```

The physical ultrasonic sensors do not move.

Only their logical roles change.

---

# 3.7 Color Does Not Directly Steer Piolín

An important architectural distinction is:

```text
COLOR DETECTION
      ≠
STEERING COMMAND
```

The color sensor reports a course event.

The EV3 then uses the current state to decide what that event means.

The complete chain is:

```text
Floor marking
      ↓
S4
      ↓
Color event
      ↓
Navigation state
      ↓
EV3 logic
      ↓
Motor A / Motor B behavior
```

Therefore, statements such as:

```text
"Blue makes the robot turn left"
```

would oversimplify the actual system.

Blue primarily establishes or updates **course interpretation**.

---

# 3.8 Sensor Measurement vs. Color Classification

The color sensor first produces optical measurement data.

The software must then classify that information into a useful category.

Conceptually:

```text
RAW OPTICAL DATA
       ↓
COLOR CLASSIFICATION
       ↓
BLUE / ORANGE / OTHER
       ↓
EVENT PROCESSING
```

This separation is important.

A raw sensor measurement is not automatically a navigation event.

---

# 3.9 RGB Representation

When RGB-style measurements are used, a color sample can be represented as:

```text
R = red-channel response

G = green-channel response

B = blue-channel response
```

or:

```text
COLOR_SAMPLE =
(R, G, B)
```

Different floor colors produce different relationships between these channels.

Conceptually:

```text
BLUE SURFACE
      ↓
Different RGB pattern
than
ORANGE SURFACE
```

The exact current classification thresholds should come from the final calibrated software rather than from assumed generic RGB values.

---

# 3.10 Why Absolute RGB Values Are Not Universal

A color sensor does not necessarily produce the exact same numerical RGB readings under every condition.

Measurements can be affected by:

```text
Ambient lighting

Sensor height

Sensor orientation

Surface reflectivity

Sensor casing

Track material

Battery / electronics conditions

Movement speed
```

Therefore:

```text
BLUE = one universal RGB number
```

is not a safe assumption.

Instead, Piolín's thresholds should be based on measurements from the **actual mounted sensor and actual competition-style surface**.

---

# 3.11 Relative Channel Relationships

In addition to absolute channel values, color classification can consider relationships between channels.

Conceptually:

```text
BLUE candidate
    ↓
Blue channel relationship differs
from Red / Green channels
```

while:

```text
ORANGE candidate
     ↓
Red / Green relationship differs
from Blue
```

The exact mathematical rules belong to the current calibrated code.

The engineering principle is:

```text
RAW RGB
   ↓
PATTERN / THRESHOLD CHECK
   ↓
COLOR CLASS
```

rather than assuming one single unchanging sensor value.

---

# 3.12 Color Classification Output

A useful software abstraction is:

```text
COLOR_BLUE

COLOR_ORANGE

COLOR_OTHER
```

or similar state values.

For example:

```python
if is_blue(r, g, b):
    detected_color = BLUE

elif is_orange(r, g, b):
    detected_color = ORANGE

else:
    detected_color = OTHER
```

This keeps the color-detection layer separated from course-state logic.

The exact implementation may differ in the active competition code.

---

# 3.13 Classification and Navigation Should Be Separate

A robust architecture separates two questions.

### Perception question

```text
What color is currently beneath S4?
```

### Navigation question

```text
What does that color mean right now?
```

The relationship is:

```text
RGB / optical reading
        ↓
Color classifier
        ↓
BLUE / ORANGE
        ↓
Course-state processor
        ↓
Direction / progress event
```

This makes the software easier to debug.

If the color is classified correctly but the course counter changes incorrectly, the error is likely in event logic rather than sensing.

---

# 3.14 Physical Marking vs. Sensor Samples

While Piolín crosses one colored strip, the program may read the sensor many times.

For example:

```text
Physical BLUE strip
────────────────────

Sensor samples:

BLUE
BLUE
BLUE
BLUE
BLUE
```

These are:

```text
Five sensor readings
```

but only:

```text
One physical marking
```

The software must therefore distinguish repeated samples from independent course events.

---

# 3.15 Why Direct Counting Fails

A naive implementation could do:

```python
if detected_color == BLUE:
    blue_count += 1
```

on every program cycle.

If the robot remains over the same blue region for several cycles:

```text
ONE BLUE MARKING
       ↓
BLUE
BLUE
BLUE
BLUE
       ↓
COUNT = 4
```

This would produce false progress.

Therefore, course tracking requires **event detection**, not simply raw sample counting.

---

# 3.16 Color Event Lock

One solution is to introduce a lock while the sensor remains over the same marking.

Conceptually:

```text
Neutral floor
     ↓
BLUE detected
     ↓
Count BLUE event
     ↓
LOCK BLUE
     ↓
More BLUE samples ignored
     ↓
Leave marking
     ↓
Unlock
```

This converts:

```text
Many samples
```

into:

```text
One event
```

A conceptual implementation is:

```python
if detected_color == BLUE and not color_locked:
    register_blue_event()
    color_locked = True
```

The lock is released only after the marking is considered cleared according to the active detection logic.

---

# 3.17 Edge-Based Event Detection

Another way to describe the same principle is detecting a **transition**.

Instead of asking:

```text
Is the sensor blue?
```

every cycle, the system asks:

```text
Did the sensor transition
from non-blue to blue?
```

Conceptually:

```text
OTHER
  ↓
OTHER
  ↓
BLUE  ← event begins
  ↓
BLUE
  ↓
BLUE
  ↓
OTHER ← marking cleared
```

Only the first valid transition represents the new event.

This can be written conceptually as:

```python
if current_color == BLUE and previous_color != BLUE:
    register_blue_event()
```

A real implementation may also use confirmation or cooldown logic for additional robustness.

---

# 3.18 Cooldown Logic

A cooldown can provide additional protection against duplicate detections.

Conceptually:

```text
Valid color event
      ↓
Register event
      ↓
Start cooldown
      ↓
Ignore duplicate event triggers
      ↓
Cooldown expires
```

This is useful when sensor readings fluctuate at the boundary of a marking:

```text
BLUE
OTHER
BLUE
OTHER
BLUE
```

Without protection, one physical strip could be interpreted as several separate markings.

The exact current cooldown duration should come from the final competition code and is intentionally not assigned a value here.

---

# 3.19 Lock and Cooldown Are Different Concepts

These two mechanisms solve related but slightly different problems.

### Lock

Prevents:

```text
BLUE
BLUE
BLUE
BLUE
```

from generating multiple events while remaining on the same marking.

### Cooldown

Prevents short boundary fluctuations such as:

```text
BLUE
OTHER
BLUE
```

from generating immediate duplicate events.

Conceptually:

```text
COLOR CLASSIFICATION
       ↓
EVENT LOCK
       ↓
COOLDOWN / TRANSITION CONTROL
       ↓
VALID COURSE EVENT
```

The current code may implement one or both ideas depending on the final version.

---

# 3.20 Confirmation Samples

Another technique is requiring more than one consistent sample before accepting a color classification.

Conceptually:

```text
Sample 1 = BLUE
Sample 2 = BLUE
        ↓
Confirmed BLUE
```

rather than:

```text
One isolated BLUE reading
        ↓
Immediate course event
```

This can reduce false detections caused by brief optical disturbances.

However:

```text
More confirmations
       ↓
Greater robustness
```

can also produce:

```text
More detection delay
```

so confirmation count must be balanced against vehicle speed.

No final current confirmation count is claimed here.

---

# 3.21 Vehicle Speed and Color Detection

The faster Piolín moves, the less time the sensor remains over a colored region.

Conceptually:

```text
LOWER SPEED
      ↓
More samples over marking
```

while:

```text
HIGHER SPEED
      ↓
Fewer samples over marking
```

Therefore, color-detection reliability depends on the interaction between:

```text
Sensor sampling

Vehicle speed

Marking width

Confirmation logic

Cooldown logic
```

This is why color processing cannot be tuned completely independently from mobility.

---

# 3.22 Color Sensor Casing

Piolín uses a casing around the color sensor to reduce unwanted surrounding light reaching the observed floor region.

Conceptually:

```text
      AMBIENT LIGHT
       ↘       ↙

       ┌─────────┐
       │ CASING  │
       │   S4    │
       └────┬────┘
            │
            ▼
        TRACK FLOOR
```

The casing creates a more controlled local optical environment around the sensor.

This is an example of solving a sensing problem partly through **mechanical design** rather than only through software thresholds.

---

# 3.23 Why Ambient Light Matters

Optical sensors respond to light reflected from the surface.

If external illumination changes:

```text
Incident light changes
        ↓
Reflected light changes
        ↓
Sensor values may shift
```

This means identical floor material can produce somewhat different measurements under:

```text
Bright overhead lighting

Shadow

Directional light

Nearby reflections
```

The casing helps reduce this uncontrolled variation.

---

# 3.24 Mechanical Light Isolation

The design relationship is:

```text
External environment
       ↓
Mechanical casing
       ↓
Reduced direct ambient influence
       ↓
More controlled sensor region
```

The casing does not make the color sensor completely independent of lighting.

Instead, it helps improve consistency by limiting the amount of uncontrolled external light entering the measurement area.

The current model is available at:

[Color Sensor Casing STL](../../models/3dprint/ColorSensorCasing.stl)

---

# 3.25 Sensor Height

Color measurements also depend on the physical distance between the sensor and floor.

Conceptually:

```text
Sensor too high
      ↓
Larger / weaker observed region
      ↓
Greater environmental influence
```

while:

```text
Sensor too low
      ↓
Risk of physical floor contact
```

The chassis therefore needs to maintain a stable sensor position.

No final numerical S4-to-floor distance is claimed here because it has not been established as a confirmed current measurement.

---

# 3.26 Sensor Orientation

The sensor should remain directed toward the floor.

If it tilts:

```text
Observed region changes
        ↓
Reflected light distribution changes
        ↓
Color values can change
```

Therefore:

```text
Mechanical sensor stability
        ↓
Optical measurement stability
```

The color-sensor mount is consequently part of the sensing architecture.

---

# 3.27 Current Course Marking Structure

Piolín's current course-progress logic is designed around the blue and orange floor markings encountered around the course.

Across three laps, the intended course sequence includes:

```text
12 valid BLUE events

12 valid ORANGE events
```

corresponding to the repeated colored corner markings around the track.

This means the sensor may produce many raw blue/orange samples during the run, but the course-state system should only register the valid physical events.

The distinction is:

```text
RAW DETECTIONS
      ↓
Potentially many samples


VALID EVENTS
      ↓
12 BLUE + 12 ORANGE
across three laps
```

for the complete intended three-lap progression.

---

# 3.28 Why Both Colors Are Tracked

Tracking both colors provides more course-state information than counting only one color.

Conceptually:

```text
BLUE EVENTS
     +
ORANGE EVENTS
     ↓
Course progression evidence
```

The system can therefore verify that the expected sequence of track markings is being crossed as Piolín moves around the circuit.

This information is useful for:

```text
Corner progression

Lap progression

Final-run state
```

without using the color sensor as a steering-angle sensor.

---

# 3.29 Color Event Counters

A conceptual data structure can include:

```text
blue_count

orange_count
```

Each counter changes only after a **new valid event**.

For example:

```python
if new_blue_event:
    blue_count += 1

if new_orange_event:
    orange_count += 1
```

The event-validation layer should occur before the counters are updated.

Therefore:

```text
RAW COLOR
    ↓
VALIDATE EVENT
    ↓
UPDATE COUNTER
```

rather than:

```text
RAW COLOR
    ↓
UPDATE COUNTER
```

---

# 3.30 Corner Progress

Because the colored markings are associated with repeated locations around the course, the event counters can help determine how much of the run has been completed.

Conceptually:

```text
Valid color event
       ↓
Progress changes
       ↓
Current course phase updated
```

This information can be combined with:

```text
Ultrasonic corner geometry
```

rather than replacing it.

The two sensing systems answer different questions.

```text
ULTRASONICS
      ↓
What geometry is present?


COLOR SENSOR
      ↓
Which course event was crossed?
```

---

# 3.31 Color and Corner Geometry

A robust architecture should not assume:

```text
Color alone = physical steering geometry
```

The lateral ultrasonic sensors provide the actual wall transition information used for corner behavior.

The color sensor can provide:

```text
Course progress

Event confirmation

Direction information
```

The combined architecture is:

```text
COLOR EVENT
      +
WALL GEOMETRY
      ↓
Navigation state
```

This reduces dependence on one sensor modality.

---

# 3.32 Example Course-State Flow

A simplified course-state sequence can be represented as:

```text
START
  ↓
Read first valid color
  ↓
Determine direction
  ↓
Assign inner / outer ultrasonic roles
  ↓
Navigate straight
  ↓
Detect wall geometry change
  ↓
Execute corner
  ↓
Cross valid color marking
  ↓
Update progress
  ↓
Continue
```

The exact order of physical wall and color events can vary according to robot trajectory and sensor mounting, so the software should not treat every sensing event as occurring at exactly the same instant.

---

# 3.33 Color Sensor and Lap Counting

Course progression eventually needs to distinguish:

```text
Corner events
```

from:

```text
Complete laps
```

A lap consists of multiple repeated corner/marking events.

Conceptually:

```text
Valid corner events
      ↓
Progress accumulated
      ↓
One complete circuit
      ↓
Lap count changes
```

Across the intended Open Challenge run:

```text
3 complete laps
```

must be distinguished from intermediate course positions.

The color counters provide one source of progression information for this purpose.

---

# 3.34 Why Duplicate Counts Are Dangerous

A false extra color event can create a larger system error than a simple incorrect sensor reading.

For example:

```text
One physical marking
       ↓
Counted twice
       ↓
Progress counter becomes incorrect
       ↓
Robot believes it is farther into run
       ↓
Final-state behavior may occur early
```

Therefore:

```text
COURSE EVENT RELIABILITY
```

is more important than simply detecting color as quickly as possible.

This justifies lock, transition, confirmation, and cooldown logic.

---

# 3.35 Missing Events Are Also Dangerous

The opposite failure is:

```text
Physical marking crossed
       ↓
No valid event registered
       ↓
Course counter remains behind
```

The robot may then believe it has completed fewer corners or laps than it physically has.

This creates a trade-off:

```text
Detection too permissive
      ↓
False extra counts


Detection too strict
      ↓
Missed counts
```

Calibration must find a practical region between these two failure modes.

---

# 3.36 Event-Detection Balance

The desired processing behavior is:

```text
REAL MARKING
      ↓
Detected reliably


NO REAL MARKING
      ↓
No event


SAME MARKING
      ↓
Only one event
```

This can be summarized as three requirements:

```text
DETECT

REJECT

DE-DUPLICATE
```

A useful color-event system needs all three.

---

# 3.37 State Machine Representation

The color-event subsystem can be described using a simple state machine.

```text
             ┌─────────────┐
             │   FLOOR     │
             └──────┬──────┘
                    │
             Valid color detected
                    │
                    ▼
             ┌─────────────┐
             │ ON MARKING  │
             └──────┬──────┘
                    │
              Register once
                    │
                    ▼
             ┌─────────────┐
             │   LOCKED    │
             └──────┬──────┘
                    │
             Marking cleared
                    │
                    ▼
             ┌─────────────┐
             │   FLOOR     │
             └─────────────┘
```

This is a conceptual architecture rather than a requirement that the final source code use these exact state names.

---

# 3.38 Previous and Current Color

Another useful representation stores:

```text
previous_color

current_color
```

The transition can then be evaluated.

Conceptually:

```python
new_blue_event = (
    current_color == BLUE
    and previous_color != BLUE
)

new_orange_event = (
    current_color == ORANGE
    and previous_color != ORANGE
)
```

This naturally makes the system sensitive to **edges** rather than continuously counting a sustained color.

Additional confirmation may still be used if required.

---

# 3.39 Neutral / Other Surface

The system also needs to recognize when the sensor is not currently on a valid blue or orange marking.

This state can be represented conceptually as:

```text
OTHER

FLOOR

NEUTRAL
```

depending on the software naming convention.

The important function is:

```text
Valid marking cleared
        ↓
System becomes ready
for next event
```

The exact appearance of the normal floor should be calibrated from the actual competition surface.

---

# 3.40 Color Boundary Behavior

At the edge between ordinary floor and a colored marking, the sensor can temporarily observe a mixture of regions.

Conceptually:

```text
FLOOR | BLUE
        ↑
     sensor field
partially overlaps both
```

This can produce intermediate measurements.

Therefore, classification should tolerate the fact that transitions are not infinitely sharp.

This is another reason event logic should not depend on one single exact RGB tuple.

---

# 3.41 Sensor Sampling While Turning

The color sensor is attached to the chassis, so during a turn its path over the floor differs from the path of the vehicle center.

The physical sequence may be:

```text
Vehicle begins turning
       ↓
S4 follows curved floor path
       ↓
Colored marking enters sensor region
       ↓
Event occurs
```

Therefore, color timing depends partly on:

```text
Vehicle geometry

Sensor position

Steering path
```

The color event should be interpreted as a course observation, not as an exact vehicle-center coordinate.

---

# 3.42 Sensor Offset and Course Events

Because S4 is not necessarily located exactly at the vehicle's geometric center:

```text
Color sensor crosses marking
```

does not mean:

```text
Vehicle center is exactly above marking
```

The physical offset introduces a difference between:

```text
Sensor event location
```

and:

```text
Vehicle reference-point location
```

No final numerical sensor offset is claimed here because it has not been confirmed for the final robot.

---

# 3.43 Color Sensor and Vehicle Speed

At higher speed:

```text
Colored strip remains beneath sensor
for less time
```

which means:

```text
Fewer samples are available
```

At lower speed:

```text
More samples are available
```

but a naive counting system would also be more likely to count the same marking repeatedly.

Therefore:

```text
Higher speed
      ↓
Miss risk can increase


Lower speed
      ↓
Duplicate-sample exposure increases
```

Event processing is needed in both cases.

---

# 3.44 Color Sensor and Steering

Steering changes the physical path followed by the downward sensor.

During an ideal straight:

```text
S4 path
≈
longitudinal track path
```

During a turn:

```text
S4 follows an arc
```

This can change:

```text
Where the marking is crossed

How long the sensor remains over it

Which part of the marking is observed
```

Color calibration should therefore be validated under real movement rather than only with the stationary robot.

---

# 3.45 Course Direction Should Be Locked

Once the initial direction is correctly established, ordinary later color events should not repeatedly reverse the course interpretation.

Conceptually:

```text
START
  ↓
First valid direction color
  ↓
Set direction
  ↓
LOCK DIRECTION
```

After this:

```text
BLUE / ORANGE events
```

are primarily progress events rather than instructions to redefine the entire travel direction.

This prevents later markings from corrupting the established inner/outer ultrasonic mapping.

---

# 3.46 Direction Variable

A conceptual variable can be:

```text
direction
```

with states:

```text
UNKNOWN

CLOCKWISE

COUNTERCLOCKWISE
```

At startup:

```text
direction = UNKNOWN
```

Then:

```python
if direction == UNKNOWN:

    if new_blue_event:
        direction = COUNTERCLOCKWISE

    elif new_orange_event:
        direction = CLOCKWISE
```

After assignment, the lateral ultrasonic roles can be mapped accordingly.

The exact code structure may differ, but the state concept is useful.

---

# 3.47 Sensor Role After Direction Lock

After travel direction is known, the color subsystem continues operating but its role changes.

### Before direction is known

```text
Color
  ↓
Determine direction
```

### After direction is known

```text
Color
  ↓
Track course progression
```

This is a state-dependent sensor responsibility.

The same physical sensor provides different information at different points in the run.

---

# 3.48 Open Challenge Role

During the Open Challenge, S4 contributes:

```text
Initial direction

Progress events

Lap / corner progression

Final run-state support
```

while:

```text
S2 + S3
```

provide lateral wall navigation and:

```text
S1
```

provides frontal safety.

The Open sensing architecture is therefore:

```text
S1
↓
Safety


S2 + S3
↓
Geometry


S4
↓
Course state
```

No camera information is required for ordinary Open-round wall navigation.

---

# 3.49 Obstacle Challenge Role

The color sensor remains useful during the Obstacle Challenge.

The architecture becomes:

```text
S4
↓
Course state


HuskyLens
↓
Obstacle identity


S2 + S3
↓
Wall geometry


S1
↓
Frontal safety
```

The HuskyLens does not replace the color sensor because the two systems observe different environmental information.

---

# 3.50 Color and HuskyLens Must Not Be Confused

Both systems involve optical perception, but their responsibilities are different.

| System | Observes | Main Information |
| :--- | :--- | :--- |
| **Color Sensor S4** | Floor below robot | Course-state markings |
| **HuskyLens** | Region ahead of robot | Pillar identity |

Therefore:

```text
S4 BLUE
```

does not mean:

```text
HuskyLens obstacle ID
```

and:

```text
HuskyLens GREEN ID 1
```

does not correspond to a floor course event.

Keeping these classifications separate prevents software ambiguity.

---

# 3.51 Color and Ultrasonic Sensor Fusion

A course event becomes more useful when interpreted together with current geometry.

For example:

```text
Valid marking crossed
       +
Known navigation state
       +
Current wall geometry
       ↓
Course progress updated
```

The sensor architecture therefore follows:

```text
COLOR
      ↓
WHEN / WHERE IN COURSE?


ULTRASONIC
      ↓
WHAT GEOMETRY EXISTS NOW?
```

Combining both produces stronger state information than either one alone.

---

# 3.52 Why Color Alone Should Not Determine a Corner Turn

A color marking is an important event, but using it as the only physical trigger for steering could create several problems.

For example:

```text
Color detected slightly early
        ↓
Turn begins before correct geometry
```

or:

```text
Color detection delayed
        ↓
Turn begins too late
```

The current architecture therefore emphasizes actual wall geometry for vehicle motion while using color for course-state awareness.

Conceptually:

```text
COLOR
   ↓
Progress / state


WALLS
   ↓
Physical steering geometry
```

---

# 3.53 Color Event Reliability

A reliable course-state event should satisfy:

```text
Correct classification

Sufficient confirmation

No duplicate count

Correct state interpretation
```

Conceptually:

```text
RAW SAMPLE
    ↓
CLASSIFY
    ↓
CONFIRM
    ↓
CHECK LOCK
    ↓
CHECK COURSE STATE
    ↓
REGISTER EVENT
```

A failure at any of these stages can create a wrong progress count.

---

# 3.54 Data Logging

During development, useful color-sensor logging can include:

```text
R

G

B

Detected color

Previous color

Lock state

Blue count

Orange count

Direction

Current navigation state
```

A conceptual diagnostic output could be:

```text
RGB=(..., ..., ...)
COLOR=BLUE
LOCK=1
BLUE_COUNT=...
ORANGE_COUNT=...
DIR=CCW
STATE=...
```

Actual values should come from the active robot.

Logging both raw and interpreted data helps separate classification problems from event-processing problems.

---

# 3.55 Debugging Classification vs. Counting

Suppose the robot reports:

```text
BLUE
```

correctly but the count increases twice.

Then:

```text
Classification works
```

but:

```text
Event de-duplication failed
```

By contrast, if the raw reading appears correct but software reports:

```text
OTHER
```

the issue is more likely in:

```text
Classification thresholds
```

This separation makes debugging much faster.

---

# 3.56 Common Failure Modes

Color-sensor problems can be divided into several categories.

| Failure Mode | Possible Result |
| :--- | :--- |
| **Ambient-light variation** | RGB values shift |
| **Loose S4 mount** | Observed floor region changes |
| **Sensor too high** | Weaker / broader reading |
| **Casing contacts floor** | Mechanical disturbance |
| **Threshold too narrow** | Missed marking |
| **Threshold too broad** | False detection |
| **No event lock** | Duplicate counts |
| **Cooldown too restrictive** | Valid next event may be delayed |
| **Direction not locked** | Later colors could corrupt direction |
| **Incorrect counter logic** | Wrong lap/course state |
| **High speed** | Fewer samples across marking |

These failure modes should be isolated rather than solved by changing every parameter simultaneously.

---

# 3.57 Diagnostic Sequence

When course-color behavior becomes unreliable, a useful investigation order is:

```text
1. Verify S4 physical connection
        ↓
2. Verify sensor faces floor
        ↓
3. Verify casing and clearance
        ↓
4. Read raw sensor values
        ↓
5. Verify BLUE classification
        ↓
6. Verify ORANGE classification
        ↓
7. Verify neutral-floor classification
        ↓
8. Verify event lock
        ↓
9. Verify cooldown / transition handling
        ↓
10. Verify counters
        ↓
11. Verify course-state interpretation
```

This prevents a course-counting problem from being incorrectly treated as a sensor-hardware problem.

---

# 3.58 Calibration Philosophy

Color calibration should be performed on the **current final installation** because the complete optical system includes:

```text
Sensor

Mounting height

Sensor angle

Casing

Track material

Lighting environment
```

Changing one of these can change the measured values.

Therefore:

```text
Sensor calibration
      belongs to
complete mounted system
```

rather than the sensor alone.

Detailed calibration procedures are documented in:

[Sensor Calibration](05_Calibration.md)

[How to Calibrate](../reproducibility/06_HowToCalibrate.md)

---

# 3.59 Calibration Data Categories

For color calibration, the useful measurement categories are conceptually:

```text
BLUE samples

ORANGE samples

NORMAL FLOOR samples
```

These allow the team to compare:

```text
Within-color variation
```

and:

```text
Between-color separation
```

The final thresholds should be chosen from real measurements rather than generated theoretical values.

---

# 3.60 Classification Margin

A robust classifier should ideally leave separation between typical measurements of different surfaces.

Conceptually:

```text
BLUE RANGE

████████


            separation


                    ████████

                 ORANGE RANGE
```

If the measured distributions overlap heavily:

```text
Classification becomes less reliable
```

Possible responses include:

```text
Improve lighting isolation

Adjust sensor position

Use multiple channel conditions

Modify threshold logic
```

This is why the casing and software calibration are complementary solutions.

---

# 3.61 Mechanical Solution Before Software Complexity

One important lesson from Piolín's color sensing development is that not every sensor problem should be solved with more complicated code.

If ambient lighting causes large variation:

```text
Software thresholds become difficult
```

A mechanical casing can reduce the variation before the signal reaches software.

The engineering chain is:

```text
PHYSICAL CAUSE
      ↓
MECHANICAL MITIGATION
      ↓
MORE CONSISTENT DATA
      ↓
SIMPLER CLASSIFICATION
```

This is a good example of systems engineering between mechanical and sensing design.

---

# 3.62 Color Sensor and Reproducibility

For another team or judge to reproduce the sensor behavior, documentation should identify:

```text
S4 port

Downward orientation

Casing

Floor colors used

Direction mapping

Event-processing concept

Calibration procedure
```

Simply stating:

```text
"Use a color sensor"
```

would not be sufficient.

The reproducible architecture is:

```text
INSTALL
   ↓
CALIBRATE
   ↓
CLASSIFY
   ↓
DE-DUPLICATE
   ↓
INTERPRET COURSE STATE
```

---

# 3.63 Current vs. Legacy Color Logic

Earlier Piolín development versions used different:

```text
Detection thresholds

Confirmation counts

Cooldown durations

Corner logic

Sensor configurations
```

These historical parameters should not automatically be copied into the final system.

The current confirmed architecture is:

```text
S4
↓
Downward color sensing


BLUE FIRST
↓
COUNTERCLOCKWISE


ORANGE FIRST
↓
CLOCKWISE


VALID COLOR EVENTS
↓
Course progression
```

Current numerical thresholds should come from the active final calibration/code.

---

# 3.64 Confirmed Current Color-Sensor Information

The following information is confirmed for the current Piolín configuration:

| Parameter | Current Value |
| :--- | :--- |
| **EV3 input** | S4 |
| **Orientation** | Downward-facing |
| **Primary course colors** | Blue and Orange |
| **Blue first** | Counterclockwise |
| **Orange first** | Clockwise |
| **Direct steering control** | No |
| **Main state role** | Direction + progress |
| **Light isolation** | Physical casing |
| **Three-lap intended valid blue events** | 12 |
| **Three-lap intended valid orange events** | 12 |

The following are intentionally not assigned final values here:

```text
RGB thresholds

Reflected-light thresholds

Confirmation count

Cooldown duration

Color lock release timing

Exact S4-to-floor distance

Exact longitudinal/lateral sensor offset
```

These should only be documented numerically when confirmed from the current robot and code.

---

# 3.65 Sensor Responsibility Matrix

| Information | Source / Derived State | Purpose |
| :--- | :--- | :--- |
| **Raw optical sample** | S4 | Base measurement |
| **BLUE classification** | Color logic | Identify blue marking |
| **ORANGE classification** | Color logic | Identify orange marking |
| **OTHER / floor state** | Color logic | Identify marking clearance |
| **New color event** | Transition logic | Prevent repeated counting |
| **Direction** | First valid color event | Select CW / CCW |
| **Blue count** | Valid blue events | Course progress |
| **Orange count** | Valid orange events | Course progress |
| **Lap / course state** | Event history | Overall run progression |

The information chain is therefore:

```text
OPTICAL DATA
      ↓
COLOR
      ↓
EVENT
      ↓
COURSE STATE
```

---

# 3.66 Complete Color Data Pipeline

The current color subsystem can be summarized as:

```text
                     TRACK FLOOR
                         │
                         ▼
                    COLOR SENSOR
                         S4
                         │
                         ▼
                RAW OPTICAL VALUES
                         │
                         ▼
                 COLOR CLASSIFIER
                  /      |      \
                 /       |       \
                ▼        ▼        ▼
              BLUE    ORANGE    OTHER
                │        │        │
                └────┬───┴────────┘
                     ▼
               EVENT PROCESSING
                     │
             ┌───────┼────────┐
             ▼       ▼        ▼
         Transition  Lock   Confirmation /
                          Cooldown logic
                     │
                     ▼
                VALID EVENT
                     │
           ┌─────────┴─────────┐
           ▼                   ▼
      DIRECTION STATE      PROGRESS STATE
           │                   │
           └─────────┬─────────┘
                     ▼
                  LEGO EV3
                     │
                     ▼
             NAVIGATION LOGIC
```

This pipeline prevents raw sensor samples from being treated directly as course commands.

---

# 3.67 Open Challenge Integration

Within the Open Challenge, the complete perception architecture becomes:

```text
                       COURSE
                         │
       ┌─────────────────┼─────────────────┐
       ▼                 ▼                 ▼
    WALLS              FLOOR            FRONT
       │                 │                 │
       ▼                 ▼                 ▼
    S2 / S3              S4                S1
       │                 │                 │
       ▼                 ▼                 ▼
   GEOMETRY          COURSE STATE        SAFETY
       │                 │                 │
       └─────────────────┼─────────────────┘
                         ▼
                      LEGO EV3
                         │
                         ▼
                    VEHICLE CONTROL
```

The color sensor therefore complements, rather than replaces, ultrasonic navigation.

---

# 3.68 Obstacle Challenge Integration

During the Obstacle Challenge:

```text
                      ENVIRONMENT
                           │
      ┌─────────────┬──────┼──────┬─────────────┐
      ▼             ▼             ▼             ▼
    WALLS          FLOOR         FRONT         PILLAR
      │             │             │             │
      ▼             ▼             ▼             ▼
   S2 / S3          S4            S1        HuskyLens
      │             │             │             │
      │             │             │        Arduino Nano
      │             │             │             │
      └─────────────┴──────┬──────┴─────────────┘
                           ▼
                        LEGO EV3
                           │
                           ▼
                     VEHICLE CONTROL
```

S4 continues supplying course-state information while the HuskyLens adds obstacle identity.

---

# 3.69 Why the Color Sensor Is Important

Piolín's wall sensors can tell the robot about immediate geometry, but wall distances alone do not fully describe **course progression**.

For example, similar wall geometry can appear on different laps.

The color system provides an additional reference:

```text
GEOMETRY
    ↓
Where can I drive?


COLOR EVENTS
    ↓
How far through the course sequence am I?
```

This distinction becomes particularly important when the robot must eventually transition from repeated navigation into the final run state.

---

# 3.70 Engineering Significance

The color sensor is a relatively small physical component but has a significant logical role.

It connects:

```text
PHYSICAL TRACK MARKINGS
        ↓
OPTICAL MEASUREMENT
        ↓
SOFTWARE EVENT
        ↓
COURSE MEMORY
```

The sensor allows Piolín to make navigation decisions based not only on what surrounds the robot at the current instant, but also on **where the robot is within the complete competition sequence**.

The mechanical casing further demonstrates that sensing performance depends on integration between:

```text
MECHANICS
     +
ELECTRONICS
     +
SOFTWARE
```

rather than software classification alone.

---

# 3.71 Final Color-Sensor Architecture

Piolín's final color system can be summarized as:

```text
                    TRACK MARKING
                         ↓
                         S4
                         ↓
                  OPTICAL SAMPLE
                         ↓
                BLUE / ORANGE /
                     OTHER
                         ↓
                 EVENT FILTER
                         ↓
               NEW VALID EVENT
                         ↓
            ┌────────────┴────────────┐
            ▼                         ▼
     INITIAL DIRECTION          COURSE PROGRESS
            │                         │
            ▼                         ▼
      BLUE → CCW                BLUE COUNT
    ORANGE → CW                ORANGE COUNT
            │                         │
            └────────────┬────────────┘
                         ▼
                      LEGO EV3
                         │
                         ▼
                NAVIGATION STATE
```

The most important distinction is:

```text
RAW COLOR SAMPLE
      ≠
COURSE EVENT
```

The software must convert many rapidly sampled optical measurements into a smaller number of meaningful physical events.

The intended complete three-lap progression contains:

```text
12 valid BLUE events
+
12 valid ORANGE events
```

while repeated readings from the same physical marking must not create additional counts.

The current architecture therefore relies on:

```text
COLOR CLASSIFICATION

EVENT TRANSITIONS

DUPLICATE REJECTION

DIRECTION LOCK

COURSE-STATE TRACKING
```

together with a mechanically shielded downward sensor.

This makes S4 Piolín's primary connection between the physical floor markings and the robot's internal understanding of course progression.

---

## Continue Reading

[HuskyLens Vision System](04_huskylens.md)

[Sensor Calibration](05_Calibration.md)

---

## Related Sensor Documentation

[Power and Sensor Configuration](01_PowerSensorconfig.md)

[Ultrasonic Sensor Data](02_USSensorD.md)

[Color Sensor Hardware](../components/06_ColorSensor.md)

---

## Related Mechanical Documentation

[Chassis Design](../mobility_mechanical/02_chassis.md)

[Robot Mobility](../mobility_mechanical/03_RMobility.md)

[Mechanical Testing](../mobility_mechanical/06_testing.md)

---

## Related Software Documentation

[Software Architecture](../software_obstacles_strategy/01_SWArchitecture.md)

[State Machine](../software_obstacles_strategy/02_statemachine.md)

[Corner Handling](../software_obstacles_strategy/04_cornerhandling.md)

[RGB Detection](../software_obstacles_strategy/09_RGBdetection.md)

[Parking Overview](../software_obstacles_strategy/parking/01_ParkingOverview.md)

---

## Reproducibility

[Wiring](../reproducibility/03_wiring.md)

[Calibration Procedure](../reproducibility/06_HowToCalibrate.md)

[Testing Protocol](../reproducibility/07_TestingProtocol.md)

[Troubleshooting](../reproducibility/08_Troubleshooting.md)

---

## Historical Reference

[Legacy Documentation Notice](../legacy/00_LEGACY_NOTICE.md)
