# 1. Legacy HuskyLens Vision System

> [!WARNING]
> This document describes a **historical Piolín vision architecture** developed and tested during WRO Future Engineers 2026 preparation.
>
> HuskyLens and the Arduino Nano are **not part of the current competition robot**.
>
> The current Obstacle Challenge uses:
>
> ```text
> Pixy2.1
>    ↓
> EV3 S1
> ```
>
> instead of the historical:
>
> ```text
> HuskyLens
>    ↓ I2C
> Arduino Nano
>    ↓ USB Serial
> EV3
> ```

The HuskyLens vision system represented one of the most important experimental stages in Piolín's Obstacle Challenge development. It was introduced because the LEGO sensors already installed on the vehicle could provide useful information about walls, floor markings, and vehicle motion, but they could not identify the color of the traffic pillars that determine the required passing side.

The obstacle rule required Piolín to distinguish:

```text
GREEN
→ pass on the LEFT


RED
→ pass on the RIGHT
```

During this development stage, the HuskyLens identification mapping was:

```text
ID 1
→ GREEN


ID 2
→ RED
```

The HuskyLens successfully demonstrated that forward visual perception could provide the obstacle identity required by the robot. However, track testing also exposed several limitations that were much less obvious during stationary camera tests. These included false detections, inconsistent Green recognition, lighting sensitivity, field-of-view limitations, target loss during steering, ambiguity when multiple blocks were visible, excessive target locking, and the complexity introduced by the HuskyLens–Nano–USB communication chain.

The system was therefore not abandoned because it was incapable of recognizing colors. **It could recognize the competition targets.** The larger problem was achieving sufficiently consistent visual perception and state management while Piolín was moving through the course.

---

# 1.1 Why Vision Was Required

The ultrasonic sensors could provide environmental measurements such as:

```text
left-side distance

right-side distance

wall proximity

track geometry
```

but they could not determine whether a pillar was Red or Green.

Two pillars could occupy similar geometric positions while requiring opposite maneuvers.

```text
SAME APPROXIMATE GEOMETRY

        │
        ├── RED
        │      ↓
        │   PASS RIGHT
        │
        └── GREEN
               ↓
            PASS LEFT
```

The downward-facing EV3 Color Sensor could not solve this problem either because its role was to observe floor markings rather than forward obstacles.

HuskyLens was therefore introduced to provide a new type of information:

> **Visual obstacle identity.**

This established an important sensor-role separation that remained relevant even after the camera itself was replaced.

```text
VISION
→ What obstacle is present?


ULTRASONICS
→ What geometry surrounds the robot?


EV3
→ What maneuver should be executed?
```

---

# 1.2 Historical Hardware Architecture

The HuskyLens was not connected directly to the EV3 in the architecture that became the main HuskyLens development platform.

Instead, an **Arduino Nano** acted as an intermediate interface.

```text
COMPETITION TARGET
        ↓
    HUSKYLENS
        ↓ I2C
   ARDUINO NANO
        ↓
    USB SERIAL
        ↓
       EV3
        ↓
OBSTACLE STATE LOGIC
        ↓
 MOTOR A + MOTOR B
```

<div align="center">

<img
  src="../../embed/legacy_huskylens_nano_architecture.png"
  alt="Legacy Piolín HuskyLens Arduino Nano EV3 architecture"
  width="880"
/>

<br>

<sub><b>Figure L1.1.</b> Historical perception architecture using HuskyLens, Arduino Nano, USB communication, and the EV3 as the final navigation controller.</sub>

</div>

The EV3 remained Piolín's main controller. The Arduino Nano did not decide how the vehicle should navigate around a pillar.

Its role was to transfer useful vision information from HuskyLens to the EV3.

---

# 1.3 Role of the Arduino Nano

The Nano acted as a bridge between the vision sensor and Piolín's main navigation program.

The information path was:

```text
HuskyLens
→ visual detection


Arduino Nano
→ receives detection


USB Serial
→ transports formatted data


EV3
→ interprets obstacle


Motor B
→ executes steering response
```

This architecture made the HuskyLens usable with Piolín without replacing the EV3 controller.

However, it also introduced an important systems-engineering consequence:

```text
HuskyLens seeing a pillar
```

did **not** automatically mean:

```text
EV3 had received the pillar information
```

There were several intermediate stages between those two events.

---

# 1.4 Historical Detection Mapping

The HuskyLens identification system used the following mapping:

| HuskyLens ID | Competition Target | Required Behavior |
| :---: | :--- | :--- |
| **1** | Green pillar | Pass on the left |
| **2** | Red pillar | Pass on the right |

The complete interpretation chain therefore became:

```text
PHYSICAL TARGET
      ↓
HUSKYLENS ID
      ↓
NANO DATA
      ↓
USB SERIAL
      ↓
EV3 PARSER
      ↓
OBSTACLE CLASS
      ↓
PASSING SIDE
```

A failure at any stage could produce incorrect physical behavior even if the camera itself had recognized the correct color.

---

# 1.5 Historical Communication Format

One tested communication approach transmitted HuskyLens detections in a simple serial format:

```text
ID,X,Y,W,H
```

where the values represented:

```text
ID
→ learned HuskyLens target identity


X
→ horizontal image position


Y
→ vertical image position


W
→ detected target width


H
→ detected target height
```

On the EV3 side, a communication method that had been demonstrated to work reliably during this stage used:

```python
nano.readline()
```

to receive one complete formatted line.

Conceptually:

```text
HuskyLens
      ↓
ID, X, Y, W, H
      ↓
Nano
      ↓
"1,152,117,45,73\n"
      ↓
USB Serial
      ↓
nano.readline()
      ↓
EV3 parser
```

The exact numbers above are only an illustrative message format, not recorded calibration data.

---

# 1.6 A Software-Layer Lesson: Do Not Replace a Proven Interface Without a Reason

Once line-based communication using:

```python
nano.readline()
```

was operating successfully, some later software iterations experimented with more complicated chunked or non-blocking buffer parsing.

This created unnecessary uncertainty.

The development pattern became:

```text
known communication method works
        ↓
reader implementation changed
        ↓
new problems appear
        ↓
unclear whether failure is:
camera?
Nano?
serial?
parser?
navigation?
```

This became an important methodological lesson.

> **When one layer of a multi-layer system has already been validated, it should remain stable while another layer is being tuned unless there is a demonstrated reason to change it.**

Changing the communication system at the same time as camera filtering and obstacle behavior made failures much harder to isolate.

---

# 1.7 Recognition Was Not the Same as Successful Navigation

One of the most important conclusions from the HuskyLens stage was:

```text
CORRECT DETECTION
≠
SUCCESSFUL MANEUVER
```

The camera could correctly detect:

```text
RED
```

or:

```text
GREEN
```

while Piolín still failed because of:

```text
late steering

insufficient steering

excessive steering

vehicle speed

wall-controller interference

target loss

incorrect target lock

incorrect recovery timing
```

The complete obstacle-navigation problem was therefore:

```text
PERCEPTION
     +
TARGET SELECTION
     +
STATE MANAGEMENT
     +
STEERING
     +
SPEED
     +
WALL GEOMETRY
```

rather than simply:

```text
detect color
→ turn
```

This distinction strongly influenced the later Pixy2.1 architecture.

---

# 1.8 False Detections

One of the most repeated HuskyLens problems was detecting colored regions that were not the intended competition pillar.

The camera could respond to:

```text
track regions

reflections

shadows

objects outside the course

similarly colored backgrounds

illumination changes
```

A simplified failure sequence was:

```text
Husky reports GREEN
        ↓
detected region is not actual pillar
        ↓
EV3 accepts detection
        ↓
Piolín begins avoidance
        ↓
vehicle leaves intended trajectory
```

This exposed an important limitation of using only:

```python
if ID == 1:
    green
```

or:

```python
if ID == 2:
    red
```

A valid ID meant that the visual region matched the learned target sufficiently for the camera to classify it. It did not independently prove that the region was the **relevant competition pillar in Piolín's path**.

---

# 1.9 False Positives vs. False Negatives

To reduce false detections, the obstacle software progressively added additional validation criteria such as:

```text
X position

Y position

block size

multiple confirmations

minimum detection persistence
```

This reduced some false positives but introduced an opposite problem.

```text
TOO PERMISSIVE
      ↓
false detections accepted


MORE FILTERING
      ↓
fewer false detections


TOO RESTRICTIVE
      ↓
real pillar visible
but software rejects it
```

<div align="center">

<img
  src="../../embed/legacy_huskylens_filter_tradeoff.png"
  alt="Legacy HuskyLens filtering trade-off between false detections and rejected valid targets"
  width="850"
/>

<br>

<sub><b>Figure L1.2.</b> Increasing target-filter strictness reduced some false detections but could also reject real competition pillars.</sub>

</div>

This was a genuine perception trade-off rather than a problem that could always be solved by simply adding more thresholds.

---

# 1.10 Green Recognition Was Less Consistent

During multiple development tests, Green recognition was observed to be less consistent than Red recognition.

The reliability of Green changed with factors including:

```text
illumination

camera angle

distance

brightness

background

training conditions
```

A pillar could physically remain in front of Piolín while the camera output behaved more like:

```text
GREEN detected
      ↓
lost
      ↓
GREEN detected
      ↓
lost
      ↓
GREEN detected
```

To a human observing the HuskyLens screen, the target could appear essentially visible throughout the sequence.

To the software, however, these were separate short detection pulses.

<div align="center">

<img
  src="../../embed/legacy_huskylens_intermittent_detection.png"
  alt="Intermittent HuskyLens detection of a continuously visible pillar"
  width="850"
/>

<br>

<sub><b>Figure L1.3.</b> A visually continuous target could produce intermittent detection events from the perspective of the EV3 control program.</sub>

</div>

This mattered because obstacle state logic requires continuity across time.

---

# 1.11 Why Intermittent Detection Was Difficult

A simple obstacle program might assume:

```text
target visible
→ avoid


target not visible
→ stop avoiding
```

With an intermittent vision signal, this becomes unstable:

```text
GREEN
→ steer left


NO DETECTION
→ release steering


GREEN
→ steer left again


NO DETECTION
→ release again
```

The resulting steering can oscillate or begin too late.

This encouraged the use of temporary memory and target locking.

However, solving detection loss with memory introduced another problem: **deciding when that memory should be released.**

---

# 1.12 Field-of-View Limitation

Another major limitation was the usable field of view.

After completing a corner, Piolín could remain slightly rotated relative to the upcoming straight.

Even a relatively small orientation error could place the next pillar outside the camera's useful visual region.

The failure sequence could become:

```text
corner completed
      ↓
Piolín still points slightly sideways
      ↓
next pillar outside HuskyLens FOV
      ↓
no useful target
      ↓
Piolín continues forward
      ↓
pillar finally enters image
      ↓
available avoidance distance is now small
```

<div align="center">

<img
  src="../../embed/legacy_huskylens_fov.png"
  alt="HuskyLens field of view after Piolín exits a corner"
  width="850"
/>

<br>

<sub><b>Figure L1.4.</b> Small post-corner heading errors could place the next pillar outside the camera's usable field of view until Piolín was much closer.</sub>

</div>

This led to experiments involving:

```text
camera placement

post-corner centering

slower approaches

reverse movement

post-pillar recentering
```

Some of those additions helped individual situations but increased overall state complexity.

---

# 1.13 Target Loss During Avoidance

Even when the camera detected the correct pillar initially, the target could disappear during the avoidance maneuver.

This was partly a geometric consequence of mounting the camera rigidly to the robot.

```text
Piolín steers
      ↓
chassis rotates
      ↓
camera rotates
      ↓
pillar moves across image
      ↓
pillar exits field of view
```

The pillar had not necessarily been passed.

The camera had simply stopped seeing it.

This led to one of the most important lessons from the HuskyLens development stage:

> [!IMPORTANT]
> **TARGET LOST does not mean TARGET PASSED.**

---

# 1.14 The Incorrect Early Assumption

An early simplified state interpretation could behave conceptually like:

```text
pillar detected
      ↓
start avoidance
      ↓
pillar disappears
      ↓
assume avoidance complete
      ↓
straighten
```

But the real geometry could instead be:

```text
pillar detected
      ↓
Piolín steers slightly
      ↓
pillar leaves FOV
      ↓
pillar is still physically beside/in front of robot
      ↓
software straightens
      ↓
collision
```

<div align="center">

<img
  src="../../embed/legacy_target_lost_vs_passed.png"
  alt="Difference between a camera target leaving the field of view and the vehicle physically passing it"
  width="880"
/>

<br>

<sub><b>Figure L1.5.</b> Target disappearance from the image is not sufficient evidence that the physical obstacle has been cleared.</sub>

</div>

This discovery changed how later obstacle states were designed.

---

# 1.15 Using Ultrasonics to Confirm the Pass

A stronger concept was to combine the visual target state with physical side geometry.

As Piolín moves beside a pillar, the relevant lateral ultrasonic sensor may observe a characteristic sequence:

```text
normal side distance
      ↓
distance decreases
      ↓
pillar is alongside robot
      ↓
distance begins increasing again
      ↓
pillar is moving behind sensor region
```

Conceptually:

```text
CAMERA
→ identifies which pillar is being avoided


LATERAL US
→ helps determine whether Piolín physically moved past it
```

<div align="center">

<img
  src="../../embed/legacy_huskylens_us_pass_confirmation.png"
  alt="Legacy concept of combining HuskyLens target identity with ultrasonic pillar pass confirmation"
  width="880"
/>

<br>

<sub><b>Figure L1.6.</b> Later obstacle logic attempted to use lateral ultrasonic geometry as stronger evidence that a pillar had physically been passed.</sub>

</div>

This sensor-fusion principle survived beyond the HuskyLens architecture and became useful in later vision development.

---

# 1.16 Target Locking

Because Husky detections could be intermittent, the obstacle controller introduced the concept of locking the current target.

For example:

```text
camera confirms RED
      ↓
LOCK = RED
      ↓
temporary detection loss
      ↓
continue RED maneuver
```

This helped prevent a brief visual fluctuation from changing the obstacle identity in the middle of a maneuver.

Without any lock:

```text
RED
→ no detection
→ GREEN false detection
→ RED
```

could create unstable behavior.

Target memory was therefore useful.

The problem was determining how long that memory should remain active.

---

# 1.17 Persistent Lock Problem

One of the more important late-stage problems was that the target lock could remain active after the physical pillar had already been passed.

A failure could occur as:

```text
first pillar detected
      ↓
LOCK RED
      ↓
first pillar passed
      ↓
second pillar becomes visible
      ↓
LOCK still RED
      ↓
new pillar ignored or misinterpreted
```

The camera itself could be seeing the next target correctly while the robot's internal state still represented the previous one.

This was not strictly a HuskyLens recognition failure.

It was a **target-state-management failure**.

---

# 1.18 Target Lifecycle

The lock problem demonstrated that obstacle perception needs a lifecycle.

A more complete target state is:

```text
SEARCH
   ↓
ACQUIRE
   ↓
VALIDATE
   ↓
LOCK CURRENT TARGET
   ↓
AVOID
   ↓
PASS CONFIRMED
   ↓
RELEASE TARGET
   ↓
SEARCH NEXT
```

<div align="center">

<img
  src="../../embed/legacy_huskylens_target_lifecycle.png"
  alt="Legacy HuskyLens obstacle target lifecycle"
  width="860"
/>

<br>

<sub><b>Figure L1.7.</b> A robust obstacle controller must distinguish acquisition, active avoidance, pass confirmation, release, and the search for the next pillar.</sub>

</div>

The development team learned that the following are different concepts:

```text
current target

target currently visible

target remembered

target already passed

next target
```

Treating them as one variable was insufficient.

---

# 1.19 Multiple Visible Blocks

Another important problem appeared when more than one candidate block was visible.

A simple strategy could effectively behave as:

```text
first valid block returned
→ current target
```

This rule is attractive because it is easy to implement.

However, the first valid detection may be:

```text
far away

small

a future pillar

a background false detection

less relevant than another visible block
```

Therefore:

```text
FIRST BLOCK
≠
MOST RELEVANT BLOCK
```

This became an important lesson that directly influenced later Pixy target-selection development.

---

# 1.20 Target Relevance

A stronger target-selection system should consider multiple properties.

Conceptually:

```text
VALID ID
    +
BLOCK SIZE
    +
X POSITION
    +
Y POSITION
    +
TEMPORAL CONTINUITY
    +
CURRENT STATE
        ↓
TARGET RELEVANCE
```

<div align="center">

<img
  src="../../embed/legacy_huskylens_target_selection.png"
  alt="Legacy HuskyLens multi-factor target relevance concept"
  width="860"
/>

<br>

<sub><b>Figure L1.8.</b> Selecting the relevant obstacle requires more information than the order in which detections are returned.</sub>

</div>

This does not mean that every possible variable must always be combined into one complicated formula.

The lesson was that target selection needs a meaningful relationship with the robot's immediate driving situation.

---

# 1.21 X and Y Were Image Coordinates, Not Physical Distance

Another conceptual error encountered during development was treating image-space coordinates as if they were automatically real-world metric measurements.

For example:

```text
larger Y
→ target probably appears closer
```

may be a useful relative trend in a fixed camera installation.

However:

```text
Y = some value
```

does **not** automatically mean:

```text
target = exact distance in centimeters
```

The relationship depends on:

```text
camera height

camera inclination

lens geometry

target dimensions

vehicle orientation

target orientation
```

The same limitation applies to apparent width and height.

---

# 1.22 Image Geometry Required Calibration

A valid way to use image position would have been to calibrate the complete installed camera geometry experimentally.

For example:

```text
known physical distance
      ↓
record X, Y, W, H
      ↓
repeat across several distances
      ↓
build empirical relationship
```

Without that calibration, coordinates should be treated as:

```text
relative visual features
```

rather than:

```text
absolute physical measurements
```

This distinction later became particularly important when adapting ideas from other teams.

---

# 1.23 Reference-Code Thresholds Could Not Be Copied Directly

During development, Piolín studied successful external implementations, including strategies used by ShahroodRC.

That was useful for understanding concepts such as:

```text
target filtering

position-aware steering

pillar relevance

camera-guided avoidance
```

However, specific numerical values from another robot could not be transferred directly.

Reference code included values conceptually similar to:

```python
Yignor = 50
green = 245
red = 75
```

Those numbers were calibrated for:

```text
another camera

another mounting position

another chassis

another coordinate system
```

They were not physical constants.

The engineering lesson was:

> **Copy the strategy when it is useful; recalibrate the numerical thresholds for the actual robot.**

This principle remains important in the current Pixy2.1 system.

---

# 1.24 Lighting Sensitivity

The HuskyLens was strongly influenced by the visual environment.

Recognition could change with:

```text
shadows

reflections

ambient brightness

camera angle

pillar illumination

background colors
```

Green was particularly affected during some development tests.

A pillar that appeared stable while Piolín was aligned on a straight could appear differently after the chassis rotated because the lighting angle and visible background changed.

<div align="center">

<img
  src="../../embed/legacy_huskylens_lighting.png"
  alt="Lighting effects observed during legacy HuskyLens testing"
  width="850"
/>

<br>

<sub><b>Figure L1.9.</b> Lighting, shadow, viewing angle, and background could alter the visual appearance of the same competition target.</sub>

</div>

This created a difficult interaction:

```text
vehicle motion
→ changes camera angle
→ changes target appearance
→ changes detection reliability
```

The camera therefore had to be tested while the robot was actually moving.

---

# 1.25 Objects Outside the Track

The forward-facing camera could observe much more than the intended competition lane.

Its image could contain:

```text
track

pillars

people

walls

colored objects outside course

reflections

shadows
```

This was one reason false detections outside the track became significant.

A camera classification alone had no inherent understanding of:

```text
inside course
```

versus:

```text
irrelevant external object
```

The navigation system therefore needed contextual filtering.

This further increased the complexity surrounding otherwise simple color recognition.

---

# 1.26 Static Detection vs. Dynamic Detection

HuskyLens could perform convincingly during stationary tests.

However, a moving vehicle introduces additional variables:

```text
shorter observation time

rapid X/Y movement

changing background

changing lighting

camera yaw

vehicle vibration

pillar entering/leaving FOV
```

Therefore:

```text
camera recognizes object while stationary
```

did not prove:

```text
camera + controller can navigate the obstacle reliably at speed
```

The useful validation environment was the complete moving Piolín system.

---

# 1.27 Detection Timing and Vehicle Speed

Vehicle speed determines how much distance Piolín travels while perception and control are processing the obstacle.

The sequence is:

```text
pillar enters FOV
      ↓
Husky recognizes
      ↓
Nano receives
      ↓
Nano sends
      ↓
EV3 reads
      ↓
EV3 validates
      ↓
Motor B responds
      ↓
vehicle trajectory changes
```

At greater speed, more physical distance is covered during the same perception-and-control delay.

At very low speed, however, Piolín's Ackermann geometry also became less useful because steering requires longitudinal motion to develop a curved path.

The solution therefore was not simply:

```text
drive as slowly as possible
```

but rather to balance:

```text
vision reaction time

steering response

Ackermann motion

available obstacle distance
```

---

# 1.28 Camera and Ultrasonic Control Could Fight Each Other

Another major issue was not exclusive to the HuskyLens itself.

The camera could request one trajectory while normal wall control requested another.

For example:

```text
Husky
→ GREEN
→ move LEFT
```

while:

```text
wall controller
→ correct RIGHT
```

If both corrections were applied aggressively in consecutive loops, the result could become:

```text
LEFT
RIGHT
LEFT
RIGHT
```

and physically:

```text
zig-zag
```

This led to a much more important control-architecture lesson:

> Different controllers should not all have equal steering authority at every moment.

---

# 1.29 State-Dependent Control Priority

A more mature architecture separated responsibilities by state.

Conceptually:

```text
NORMAL
→ normal wall controller


PILLAR
→ vision determines avoidance objective
→ ultrasonics mainly constrain wall safety


PASSING
→ maintain obstacle maneuver


RECENTER
→ ultrasonic geometry becomes dominant again
```

<div align="center">

<img
  src="../../embed/legacy_obstacle_control_priority.png"
  alt="State-dependent control priority developed during HuskyLens obstacle testing"
  width="880"
/>

<br>

<sub><b>Figure L1.10.</b> Later development separated steering authority by state instead of allowing camera and wall controllers to continuously compete.</sub>

</div>

This systems-level lesson was more important than any single HuskyLens threshold.

---

# 1.30 Post-Pillar Recentering

Avoiding a pillar did not automatically leave Piolín in a useful position for the next obstacle.

After avoidance, the vehicle could be:

```text
laterally displaced

rotated

close to a wall

poorly aligned for next pillar
```

This made **recovery** a distinct phase of obstacle navigation.

```text
AVOID
   ↓
PASS
   ↓
COUNTERSTEER
   ↓
RECENTER
   ↓
SEARCH NEXT
```

The lateral ultrasonic sensors were useful during this phase because they provided environmental geometry independent of camera visibility.

This also helped compensate for the HuskyLens field-of-view limitation after a maneuver.

---

# 1.31 Reversing as a Perception-Recovery Experiment

During development, reverse movement was also explored as a way to create additional time or distance for the camera to reacquire a pillar.

The concept was:

```text
uncertain / too-close approach
        ↓
reverse slightly
        ↓
pillar returns to more useful visual position
        ↓
camera has additional reaction opportunity
```

This could help in some situations but also added:

```text
more states

more timing

more steering transitions

more opportunities for inconsistency
```

Therefore reverse was not a fundamental solution to unreliable perception by itself.

It was a recovery tool whose usefulness depended on the complete state logic.

---

# 1.32 Why Adding More Logic Did Not Automatically Fix the Camera

An important pattern emerged during HuskyLens development:

```text
detection unstable
      ↓
add filter
      ↓
new edge case
      ↓
add state
      ↓
new lock
      ↓
add timeout
      ↓
new interaction
```

Each individual addition could solve one observed failure.

However, the total system became increasingly difficult to reason about.

```text
more logic
≠
automatically more reliability
```

When perception itself was inconsistent, compensating for every failure in the high-level controller could create a fragile network of special cases.

This observation strongly influenced the later decision to simplify the vision architecture.

---

# 1.33 Multi-Layer Debugging Problem

The historical system required troubleshooting across several layers.

```text
PHYSICAL TARGET
      ↓
HUSKYLENS
      ↓
HUSKYLENS ID
      ↓
I2C
      ↓
ARDUINO NANO
      ↓
FORMATTED SERIAL MESSAGE
      ↓
USB
      ↓
EV3 READER
      ↓
EV3 PARSER
      ↓
FSM
      ↓
STEERING REQUEST
      ↓
MOTOR B
      ↓
VEHICLE TRAJECTORY
```

<div align="center">

<img
  src="../../embed/legacy_huskylens_debug_chain.png"
  alt="Legacy HuskyLens multi-layer debugging chain"
  width="900"
/>

<br>

<sub><b>Figure L1.11.</b> A wrong physical maneuver could originate from perception, communication, parsing, state management, steering logic, or mechanics.</sub>

</div>

This was a major practical disadvantage compared with a shorter perception path.

---

# 1.34 The HuskyLens Screen Was Not Enough to Diagnose the System

A particularly important debugging mistake was assuming:

```text
I can see the bounding box on HuskyLens
```

therefore:

```text
the EV3 received the detection correctly
```

The actual system required confirmation at each stage.

```text
Does Husky see the target?
        ↓
Does Husky report the correct ID?
        ↓
Does Nano receive it?
        ↓
Does Nano send it?
        ↓
Does EV3 receive the line?
        ↓
Does EV3 parse it?
        ↓
Does FSM accept the target?
        ↓
Does steering map correctly?
```

Only then could the complete perception chain be considered functional.

---

# 1.35 Historical Debugging Procedure

A reliable test process therefore separated the system into layers.

### Camera layer

Verify:

```text
Green → ID 1

Red → ID 2
```

### Nano layer

Verify that the correct camera data reaches the microcontroller.

### Serial layer

Verify that complete messages such as:

```text
ID,X,Y,W,H
```

are transmitted.

### EV3 acquisition layer

Verify that:

```python
nano.readline()
```

receives the expected line.

### Parsing layer

Verify that:

```text
ID
X
Y
W
H
```

have the expected meaning.

### State layer

Verify that the intended pillar becomes the active target.

### Actuation layer

Verify:

```text
GREEN
→ required left-side maneuver


RED
→ required right-side maneuver
```

This layered diagnostic approach helped distinguish vision failures from navigation failures.

---

# 1.36 Steering-Sign Errors Could Look Like Camera Errors

Another important source of confusion was the relationship between detected pillar color and the physical sign of Motor B steering.

A camera could correctly identify:

```text
RED
```

while the software could map the requested steering direction incorrectly.

The resulting behavior would look like:

```text
RED detected
→ Piolín goes wrong side
```

which could be misinterpreted as:

```text
camera classified incorrectly
```

when the real problem was:

```text
steering sign / maneuver mapping
```

This demonstrated again why perception and actuation needed to be diagnosed independently.

---

# 1.37 Target Selection and Target State Were Different Problems

Two different problems emerged during development:

### Which target should Piolín select?

This is a **perception relevance** problem.

```text
multiple blocks
      ↓
choose correct obstacle
```

### When should Piolín stop considering that target active?

This is a **state-management** problem.

```text
current target
      ↓
avoid
      ↓
pass
      ↓
release
```

Combining those two questions into one variable made the controller difficult to stabilize.

The later architecture benefited from treating them separately.

---

# 1.38 Main HuskyLens Failure Categories

The historical HuskyLens problems can be grouped into four categories.

| Category | Examples |
| :--- | :--- |
| **Perception** | False detections, Green instability, lighting sensitivity |
| **Geometry** | Limited FOV, target leaving image during steering |
| **Target Management** | Persistent lock, multiple blocks, stale target |
| **Integration** | Nano, USB serial, EV3 reader/parser chain |

This classification is useful because the decision to replace HuskyLens was based on the **combined system burden**, not one isolated defect.

---

# 1.39 Problems That Were Not Exclusively HuskyLens Problems

It is equally important not to blame the camera for every failure during this period.

Several recurring problems came from the broader Piolín architecture or development process.

These included:

```text
incorrect steering sign

conflicting wall and camera controllers

aggressive corrections

vehicle speed

late corner handling

mechanical steering play

changing multiple parameters simultaneously

rewriting stable code while solving another subsystem
```

For example, the HuskyLens could report Green correctly while a reversed steering convention still caused Piolín to travel on the wrong side.

Preserving this distinction makes the legacy analysis more technically accurate.

---

# 1.40 Methodological Lesson: Change One Variable at a Time

During some development periods, new versions simultaneously changed:

```text
camera filtering

vehicle speed

wall correction

reverse logic

target lock

recenter logic

timeouts
```

If the new version performed worse, there was no clean way to determine which change caused the regression.

A stronger development process became:

```text
stable baseline
      ↓
change ONE behavior
      ↓
test
      ↓
record result
      ↓
keep or revert
```

This lesson applies far beyond the HuskyLens subsystem.

---

# 1.41 Why HuskyLens Was Still Valuable

Despite the problems documented above, the HuskyLens stage was extremely useful.

It demonstrated that Piolín needed:

```text
forward visual obstacle identity
```

and showed that a successful perception system needed more than simple color recognition.

The team learned about:

```text
target relevance

field of view

lighting

visual persistence

state memory

pillar-pass confirmation

camera/wall arbitration

communication diagnostics

post-obstacle recovery
```

These are not failures without value.

They are requirements discovered through experimentation.

---

# 1.42 Why the System Was Replaced

The final reason for leaving HuskyLens was not:

```text
"HuskyLens cannot detect colors."
```

That statement would be inaccurate.

A more accurate conclusion is:

> **HuskyLens could detect the competition colors, but Piolín's moving obstacle-navigation system accumulated too many consistency and integration problems around that detection.**

The complete burden included:

```text
false detections

Green instability

lighting sensitivity

limited effective FOV

target loss during turns

multiple-target ambiguity

persistent target locks

filtering trade-offs

Nano interface

USB serial communication

additional parsing/debugging layers
```

At the same time, Piolín increasingly needed convenient access to:

```text
target signature

X position

Y position

width

height
```

for more position-aware obstacle handling.

The later Pixy2.1 architecture provided a better fit for those requirements while reducing the communication chain.

---

# 1.43 Transition to Pixy2.1

The perception architecture changed from:

```text
LEGACY

HuskyLens
    ↓ I2C
Arduino Nano
    ↓ USB Serial
EV3
```

to:

```text
CURRENT OBSTACLES

Pixy2.1
    ↓
EV3 S1
```

<div align="center">

<img
  src="../../embed/vision_architecture_comparison.png"
  alt="Comparison between legacy HuskyLens Nano and current Pixy2.1 vision architecture"
  width="900"
/>

<br>

<sub><b>Figure L1.12.</b> The current Pixy2.1 architecture reduces the number of devices and communication stages between visual perception and the EV3.</sub>

</div>

The change retained the useful concept:

```text
camera
→ obstacle identity and position
```

while simplifying the physical and software interface.

---

# 1.44 HuskyLens vs. Current Pixy2.1

| Characteristic | Legacy HuskyLens | Current Pixy2.1 |
| :--- | :--- | :--- |
| Current competition status | Legacy | Current Obstacles |
| Main controller | EV3 | EV3 |
| Intermediate controller | Arduino Nano | None |
| Communication chain | Husky → Nano → USB → EV3 | Pixy → S1 → EV3 |
| Green identity | ID 1 | Signature 3 |
| Red identity | ID 2 | Signature 2 |
| Pink parking identity | Not part of current final Husky architecture | Signature 1 |
| Visual position available | X/Y information was transmitted in development | X/Y block information |
| Visual size information | W/H information was transmitted | Width/height block information |
| Major development issue | Detection consistency + integration complexity | Current system still requires tuning |
| Current reconstruction use | No | Yes |

The identification systems must never be mixed.

---

# 1.45 Critical ID Difference

> [!CAUTION]
> The historical HuskyLens ID map and the current Pixy2.1 signature map are different.

### Legacy HuskyLens

```text
ID 1
→ GREEN


ID 2
→ RED
```

### Current Pixy2.1

```text
SIG 1
→ PINK / PARKING


SIG 2
→ RED


SIG 3
→ GREEN
```

Copying the legacy HuskyLens mapping directly into Pixy code would invert the interpretation of important targets.

---

# 1.46 Current Architecture Should Not Be Inferred from This File

This document describes a historical development stage.

The current Piolín competition hardware is different.

### Current Open

```text
S1 = Gyro

S2 = LEFT Ultrasonic

S3 = RIGHT Ultrasonic

S4 = Color Sensor
```

### Current Obstacles

```text
S1 = Pixy2.1

S2 = LEFT Ultrasonic

S3 = RIGHT Ultrasonic

S4 = Color Sensor
```

The current robot does not use:

```text
HuskyLens

Arduino Nano

front ultrasonic sensor
```

as part of the final competition architecture.

Any old HuskyLens code or wiring map should therefore be interpreted only in the context of the historical robot configuration for which it was developed.

---

# 1.47 Engineering Lessons Carried into the Current Vision System

Several principles discovered during HuskyLens development remain important in the current Pixy2.1 architecture.

### Detection must be contextual

```text
valid color
≠
automatically relevant obstacle
```

### Lost target does not mean passed target

```text
camera loss
≠
physical completion
```

### Target state requires a lifecycle

```text
search
→ acquire
→ validate
→ lock
→ avoid
→ confirm pass
→ release
```

### Multiple blocks need selection

```text
first detection
≠
necessarily best target
```

### Camera coordinates are not automatically metric distance

```text
X/Y/W/H
→ image-space information
```

unless calibrated against real-world geometry.

### Wall control and vision need explicit priorities

```text
camera
→ obstacle objective


ultrasonics
→ geometry / safety / recovery
```

### Stable subsystems should remain stable during tuning

A proven communication layer should not be rewritten while testing an unrelated steering problem without a specific reason.

---

# 1.48 Historical System Overview

The complete legacy perception system can be summarized as:

```text
                     PHYSICAL PILLAR
                           │
                           ▼
                       HUSKYLENS
                           │
                ID / X / Y / W / H
                           │
                           ▼
                      ARDUINO NANO
                           │
                       USB SERIAL
                           │
                           ▼
                           EV3
                    ┌──────┼──────┐
                    │      │      │
                    ▼      ▼      ▼
                 VISION    US   STATE LOGIC
                    │      │      │
                    └──────┼──────┘
                           ▼
                    STEERING DECISION
                           │
                  ┌────────┴────────┐
                  ▼                 ▼
               Motor A           Motor B
                  │                 │
                  └────────┬────────┘
                           ▼
                     VEHICLE MOTION
```

<div align="center">

<img
  src="../../embed/legacy_huskylens_system_overview.png"
  alt="Complete legacy Piolín HuskyLens obstacle system"
  width="900"
/>

<br>

<sub><b>Figure L1.13.</b> Historical HuskyLens subsystem within the complete EV3-controlled vehicle architecture.</sub>

</div>

The system was functional enough to reveal the true requirements of dynamic obstacle perception, but it was also complex enough to make consistent competition behavior difficult.

---

# 1.49 Vision-System Evolution

The vision system did not evolve through a simple sequence of:

```text
bad camera
→ good camera
```

Instead, each stage answered different engineering questions.

```text
EARLY VISION EXPERIMENTS
        ↓
Can camera perception help?


HUSKYLENS DEVELOPMENT
        ↓
Can Piolín identify pillar color?


HUSKYLENS + NANO
        ↓
Can external vision be integrated with EV3?


DYNAMIC TRACK TESTING
        ↓
What happens to detection while moving?


FALSE DETECTIONS / FOV / LOCK / LIGHTING
        ↓
What information and state handling are actually needed?


PIXY2.1
        ↓
Can those requirements be handled through a simpler
and more direct vision architecture?
```

<div align="center">

<img
  src="../../embed/evolution_vision_system.png"
  alt="Evolution of Piolín vision architecture"
  width="900"
/>

<br>

<sub><b>Figure L1.14.</b> Piolín's current vision architecture resulted from lessons learned across several perception and integration stages.</sub>

</div>

---

# 1.50 Final Historical Assessment

The HuskyLens–Arduino Nano stage was an important part of Piolín's engineering development.

It successfully demonstrated that visual identification could provide the distinction required between:

```text
GREEN
→ LEFT PASS
```

and:

```text
RED
→ RIGHT PASS
```

However, actual moving-track operation revealed that obstacle vision required much more than color classification.

The system had to solve:

```text
Is this detection real?

Is it actually inside the relevant track region?

Is Green being detected consistently?

Which visible block matters?

Is this still the current pillar?

Has the current pillar physically been passed?

When should the target lock be released?

Did the EV3 actually receive the camera information?

Should vision or wall geometry control steering right now?
```

The final limitation was therefore not one camera feature.

It was the accumulated complexity of perception reliability, target management, physical camera geometry, and communication integration.

The architectural transition can be summarized as:

```text
HUSKYLENS STAGE

color detection
+
target filtering
+
target memory
+
Nano bridge
+
USB communication
+
EV3 parsing
```

compared with the direction selected later:

```text
CURRENT PIXY2.1 STAGE

direct signatures
+
block geometry
+
direct EV3 S1 integration
+
state-aware obstacle handling
```

The most important conclusion from this historical stage is therefore:

> **HuskyLens was capable of recognizing the competition colors, but reliable autonomous obstacle avoidance required more than recognition. The HuskyLens stage revealed the importance of target relevance, field of view, lighting robustness, target lifecycle, physical pass confirmation, controller priority, and communication simplicity. Those lessons directly shaped Piolín's later Pixy2.1 architecture.**

The HuskyLens prototype was therefore not wasted development.

It was the experiment that helped define what Piolín's final vision system needed to do better.

---

<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
