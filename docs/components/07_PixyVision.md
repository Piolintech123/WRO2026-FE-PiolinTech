# 7. Pixy2.1 Vision System

<div align="center">

<img
  src="../../v-photos/v4/pixy21_front.jpg"
  alt="Pixy2.1 installed on Piolín for the Obstacle Challenge"
  width="700"
/>

<br>

<sub><b>Figure 7.1.</b> Pixy2.1 installed as Piolín's forward-facing vision sensor for the Obstacle Challenge.</sub>

</div>

Piolín uses a **Pixy2.1 vision sensor connected to EV3 Sensor Port S1** during the WRO Future Engineers Obstacle Challenge.

The camera provides information that the LEGO ultrasonic sensors cannot obtain: **visual identity and image position of colored competition targets**.

The current obstacle configuration is:

```text
S1 = Pixy2.1

S2 = LEFT Ultrasonic Sensor

S3 = RIGHT Ultrasonic Sensor

S4 = Color Sensor
````

The Gyro Sensor is **not installed during the Obstacle Challenge**.

During Open, the opposite configuration is used:

```text
S1 = Gyro

Pixy2.1 = not installed
```

This makes Pixy2.1 part of Piolín's modular S1 architecture rather than a permanent sensor used in both rounds.

---

## 7.1 Why Vision Is Required

The Obstacle Challenge contains colored traffic pillars whose required passing side depends on their color.

The current competition behavior is:

```text
GREEN
→ pass LEFT


RED
→ pass RIGHT
```

Distance sensors cannot solve this problem alone.

A red pillar and a green pillar can occupy almost identical geometric positions:

```text
same distance

same size

same location
```

but require opposite maneuvers.

Therefore Piolín needs a sensor capable of answering:

```text
What target am I seeing?
```

rather than only:

```text
How far away is an object?
```

Pixy2.1 provides that visual classification layer.

---

## 7.2 Current Signature Mapping

Piolín currently uses three Pixy color signatures.

| Pixy Signature | Target | Navigation Meaning |
| :------------: | :----- | :----------------- |
|       `1`      | Pink   | Parking reference  |
|       `2`      | Red    | Pass on the RIGHT  |
|       `3`      | Green  | Pass on the LEFT   |

The mapping must remain explicit because it is different from Piolín's historical HuskyLens configuration.

The legacy HuskyLens mapping was:

```text
ID 1 = GREEN

ID 2 = RED
```

The current Pixy2.1 mapping is:

```text
SIG 1 = PINK

SIG 2 = RED

SIG 3 = GREEN
```

These two systems must never be confused in current software.

---

# 7.3 Color Connected Components

Pixy2.1 is used primarily through its **Color Connected Components** functionality.

The objective is not line tracking.

Piolín uses trained color signatures so that Pixy can identify connected regions corresponding to the relevant colored targets.

Conceptually:

```text
camera image
      ↓
color signature processing
      ↓
connected visual block
      ↓
block information
      ↓
EV3
```

The resulting block contains more information than a simple:

```text
RED
```

or:

```text
GREEN
```

classification.

The EV3 can also receive information describing where the block appears within the camera image.

---

# 7.4 Block Information

For a detected Pixy block, useful information includes:

```text
signature

x

y

width

height
```

These variables describe different properties.

```text
signature
→ what target class was detected


x
→ horizontal image position


y
→ vertical image position


width
→ detected block width


height
→ detected block height
```

This gives Piolín both:

```text
IDENTITY
+
IMAGE GEOMETRY
```

rather than only color identity.

---

# 7.5 Horizontal Position — X

The `x` value is particularly useful for steering.

Conceptually:

```text
pillar appears left in image
→ low horizontal image position


pillar appears near image center
→ central horizontal position


pillar appears right in image
→ high horizontal image position
```

The exact numerical center depends on the Pixy image coordinate system and current software interface.

For Piolín, the important engineering concept is:

```text
X
→ where the target appears horizontally
```

This allows steering behavior to depend on actual target position rather than using only:

```text
RED = fixed right command

GREEN = fixed left command
```

---

# 7.6 Signature Determines Passing Objective

The signature provides the required passing side.

For Green:

```text
SIG 3
   ↓
GREEN
   ↓
PASS LEFT
```

For Red:

```text
SIG 2
   ↓
RED
   ↓
PASS RIGHT
```

The signature determines the **objective**.

It should not necessarily determine one permanent steering angle.

A more useful interpretation is:

```text
SIGNATURE
→ which side should Piolín pass?


X / SIZE / STATE
→ how should Piolín approach that maneuver?
```

This distinction is important because pillar position changes from run to run.

---

# 7.7 Red Detection

<div align="center">

<img
src="../../v-photos/v4/pixy21_red_detection.jpg"
alt="Pixy2.1 detecting a red WRO obstacle pillar"
width="680"
/>

<br>

<sub><b>Figure 7.2.</b> Real Pixy2.1 detection of a red target used by Piolín's obstacle-perception system.</sub>

</div>

A valid Red target corresponds to:

```text
Signature 2
```

and the competition navigation objective is:

```text
RED
→ PASS RIGHT
```

However, successful Red recognition alone does not prove that the robot will physically pass on the correct side.

The complete chain is:

```text
RED PILLAR
     ↓
Pixy detection
     ↓
Signature 2
     ↓
EV3 interpretation
     ↓
target state
     ↓
RIGHT passing objective
     ↓
Motor B command
     ↓
physical vehicle motion
```

A failure at any later layer can produce the wrong physical trajectory even when Pixy identified Red correctly.

---

# 7.8 Green Detection

<div align="center">

<img
src="../../v-photos/v4/pixy21_green_detection.jpg"
alt="Pixy2.1 detecting a green WRO obstacle pillar"
width="680"
/>

<br>

<sub><b>Figure 7.3.</b> Real Pixy2.1 detection of a green target used by Piolín's obstacle-perception system.</sub>

</div>

A valid Green target corresponds to:

```text
Signature 3
```

and requires:

```text
GREEN
→ PASS LEFT
```

Red and Green should be tested separately.

A camera being able to detect one color reliably does not automatically prove equivalent performance for the other.

Useful testing conditions include:

```text
different distance

different horizontal position

different lighting

different approach angle

stationary robot

moving robot
```

This ensures the perception system is evaluated under conditions closer to the actual course.

---

# 7.9 Parking Signature

<div align="center">

<img
src="../../v-photos/v4/pixy21_parking_detection.jpg"
alt="Pixy2.1 detecting Piolín's pink parking reference"
width="680"
/>

<br>

<sub><b>Figure 7.4.</b> Pixy2.1 recognition of the pink target currently assigned to Signature 1 for parking-related perception.</sub>

</div>

The current mapping reserves:

```text
Signature 1
→ PINK
→ parking reference
```

The parking strategy is still under development.

Therefore this documentation does not claim that detecting Signature 1 alone is sufficient to initiate or complete parking.

A more complete parking state may eventually combine:

```text
course progression

pink visual reference

vehicle alignment

encoder movement

lateral geometry
```

before stopping the vehicle.

Pixy provides the visual reference, but parking remains a complete navigation problem.

---

# 7.10 Direct EV3 Integration

<div align="center">

<img
src="../../v-photos/v4/pixy21_s1_connection.jpg"
alt="Pixy2.1 connected to Piolín's EV3 through Sensor Port S1"
width="680"
/>

<br>

<sub><b>Figure 7.5.</b> Current Pixy2.1-to-EV3 connection used in the Obstacle Challenge configuration.</sub>

</div>

The current architecture connects Pixy2.1 directly to the EV3 through the S1 vision interface.

Conceptually:

```text
Pixy2.1
   ↓
S1
   ↓
EV3
```

The current software path uses:

```text
ev3dev2

SMBus / I2C
```

for communication with the Pixy.

This direct architecture is significantly simpler than Piolín's previous HuskyLens system.

---

# 7.11 Legacy Vision Architecture

The historical architecture used:

```text
HuskyLens
    ↓ I2C
Arduino Nano
    ↓ USB Serial
EV3
```

The Nano acted as a bridge rather than as the main navigation controller.

That architecture successfully demonstrated that visual information could reach the EV3, but it introduced additional communication layers.

A perception failure could originate from:

```text
camera recognition

HuskyLens ID

camera-to-Nano communication

Nano firmware

serial formatting

USB communication

EV3 reader

EV3 parser

navigation state
```

The Pixy2.1 architecture reduces this chain to:

```text
Pixy
 ↓
EV3
```

The detailed historical analysis is preserved separately in the Legacy documentation.

---

# 7.12 Why Pixy2.1 Replaced the HuskyLens Architecture

The HuskyLens was not removed because it could never detect the competition colors.

It did detect them.

The difficulty was achieving consistent autonomous behavior while also managing:

```text
false detections

lighting variation

Green inconsistency

field-of-view limitations

intermittent detections

multiple blocks

target locking

Nano communication

USB communication

EV3 parsing
```

Pixy2.1 offered a simpler vision architecture centered around direct color signatures and block geometry.

The change therefore addressed two different engineering goals:

```text
improve perception workflow
```

and:

```text
reduce integration complexity
```

---

# 7.13 Pixy2.1 Is a Sensor, Not the Navigation Controller

Pixy does not decide how Piolín moves.

The responsibility remains with the EV3.

```text
Pixy
→ perception


EV3
→ decision


Motor B
→ steering
```

For example, Pixy may report:

```text
Signature 3
X = target position
W = target width
H = target height
```

The EV3 must decide how that information should affect the current vehicle state.

This distinction allows the camera and navigation logic to be tested independently.

---

# 7.14 Static Camera Testing

The first level of Pixy testing can be performed while Piolín is stationary.

Useful checks include:

```text
Does Red produce Signature 2?

Does Green produce Signature 3?

Does Pink produce Signature 1?

Does X change when target moves horizontally?

Do width and height change as apparent target size changes?
```

These tests confirm the basic perception pipeline.

However:

```text
stationary detection
≠
complete autonomous reliability
```

Dynamic testing is still required.

---

# 7.15 Dynamic Vision Testing

When Piolín moves, several additional variables appear.

```text
vehicle vibration

changing viewing angle

target movement within image

steering-induced camera rotation

changing distance

changing background

reduced reaction time
```

Therefore a target that is stable while Piolín is stationary may be more difficult to track during autonomous driving.

Dynamic tests should evaluate:

```text
straight approach

approach after corner

off-center approach

target avoidance

target leaving field of view
```

before perception is considered fully integrated with navigation.

---

# 7.16 Camera Field of View

Pixy2.1 can only detect objects that are visible within its current field of view.

This creates an important relationship between:

```text
vehicle orientation
```

and:

```text
visual availability
```

Suppose Piolín exits a corner slightly misaligned.

```text
corner exit error
      ↓
camera points away from next pillar
      ↓
pillar outside FOV
      ↓
no visual detection
      ↓
pillar may become visible only later
```

This means a camera problem can sometimes originate from vehicle alignment rather than from color recognition.

---

# 7.17 Steering Changes the Camera View

Pixy2.1 is mounted to Piolín's chassis.

When Motor B creates a vehicle turn:

```text
vehicle heading changes
        ↓
camera heading changes
        ↓
pillar image position changes
```

This has an important consequence:

> **Target movement inside the Pixy image is produced by both relative vehicle motion and steering-induced camera rotation.**

The camera and steering systems therefore interact physically.

A target can leave the camera image before Piolín has actually passed it.

---

# 7.18 Target Lost Does Not Mean Target Passed

This was one of the strongest lessons from earlier vision development.

```text
TARGET LOST
```

and:

```text
TARGET PASSED
```

are different events.

During avoidance:

```text
Piolín begins steering
      ↓
camera rotates with chassis
      ↓
pillar moves toward image edge
      ↓
pillar disappears
```

but the physical pillar may still be beside or ahead of part of the vehicle.

Therefore the system should not automatically do:

```text
no Pixy block
→ immediately center steering
```

The obstacle state needs some persistence or additional physical context.

---

# 7.19 Target Memory

Short-term target memory can help Piolín continue a maneuver when a detection temporarily disappears.

Conceptually:

```text
SEARCH
   ↓
detect valid pillar
   ↓
ACQUIRE
   ↓
remember target
   ↓
AVOID
```

If the camera briefly loses detection:

```text
temporary loss
≠
immediate target deletion
```

However, memory should also not persist indefinitely.

Otherwise the previous pillar can incorrectly influence the next section.

This creates the need for a clear target lifecycle.

---

# 7.20 Target Lifecycle

A useful conceptual obstacle lifecycle is:

```text
SEARCH
   ↓
ACQUIRE
   ↓
VALIDATE
   ↓
LOCK
   ↓
AVOID
   ↓
PASS CONFIRMED
   ↓
RELEASE
   ↓
SEARCH NEXT
```

The exact implementation is still being tuned.

The important architectural idea is that Piolín should distinguish between:

```text
a block that is visible

a target that is currently selected

a target that was temporarily lost

a target that has physically been passed

a target that should now be forgotten
```

This prevents one camera reading from controlling the entire obstacle sequence indefinitely.

---

# 7.21 Multiple Visible Blocks

Pixy may sometimes report more than one block.

This creates a target-selection problem.

A simple rule such as:

```text
take first block returned
```

does not guarantee that the selected object is the most relevant one.

A candidate may be:

```text
farther away

smaller

near image edge

future pillar

false visual region
```

Piolín therefore needs a relevance decision rather than relying only on returned order.

---

# 7.22 Target Selection

<div align="center">

<img
src="../../embed/pixy21_block_selection.png"
alt="Piolín Pixy2.1 relevant block selection concept"
width="820"
/>

<br>

<sub><b>Figure 7.6.</b> Target-selection concept using signature validity, image position, apparent size, temporal continuity, and navigation state rather than selecting a block only by returned order.</sub>

</div>

Useful target-selection information can include:

```text
valid signature

x position

y position

width

height

apparent area

temporal continuity

current vehicle state
```

A simple apparent area can be calculated as:

```text
A = width × height
```

A larger apparent block may often correspond to a more visually prominent target, but apparent area is not a calibrated metric distance.

It should therefore be treated as a relevance signal rather than as an exact range measurement.

---

# 7.23 Image Size Is Not Physical Distance

Pixy provides:

```text
width

height
```

in image coordinates.

These values can change as a pillar appears larger or smaller.

However:

```text
image size
≠
direct physical distance
```

unless a camera calibration model has been established.

Apparent size also depends on:

```text
target orientation

camera angle

target visibility

partial occlusion
```

Therefore the current software can use size as a qualitative relevance indicator without falsely claiming an exact distance in centimeters.

---

# 7.24 Y Is Not Automatically Distance

The same caution applies to vertical image position.

A `y` value may correlate with target geometry for a fixed camera mount, but it depends on:

```text
camera height

camera pitch

lens geometry

target dimensions

vehicle orientation
```

Therefore:

```text
Y
≠
distance
```

by itself.

If Piolín later establishes a measured calibration relating image geometry to physical distance, that model can be documented separately.

Until then, Y remains an image-space measurement.

---

# 7.25 Camera Mounting Stability

The physical Pixy mount is part of the vision calibration.

If the camera changes:

```text
height

pitch

yaw

lateral offset
```

then the meaning of image coordinates can change even when the software is identical.

Therefore:

```text
same pillar
+
different camera mount
=
different image position
```

The Pixy mount must remain mechanically stable between calibration and competition runs.

The exact current V4 camera height, angle, and offset should be physically measured before they are published as final numerical specifications.

---

# 7.26 Forward Camera Position

<div align="center">

<img
src="../../v-photos/v4/piolin_obstacle_isometric.jpg"
alt="Piolín obstacle configuration showing the forward Pixy2.1 installation"
width="720"
/>

<br>

<sub><b>Figure 7.7.</b> Complete Obstacle Challenge configuration showing Pixy2.1 mounted forward while the permanent EV3 platform remains unchanged.</sub>

</div>

The forward placement is intended to make traffic pillars visible before the vehicle reaches them.

The camera should provide enough preview for:

```text
detection

target validation

steering reaction

physical avoidance
```

while still remaining mechanically protected and integrated into the chassis.

The best camera position is therefore a compromise between:

```text
visibility

reaction distance

mounting stability

vehicle dimensions
```

rather than simply placing the camera as high as possible.

---

# 7.27 Lighting

Pixy color recognition depends on the visual appearance of the target.

This can be influenced by:

```text
ambient lighting

shadows

reflections

pillar brightness

camera angle

background color
```

Therefore signature training should be tested under representative track conditions.

The objective is not merely:

```text
Pixy sees Red in one room
```

but:

```text
Pixy continues identifying Red and Green
under the lighting conditions expected during competition
```

No final detection percentages are claimed until repeated measured trials are recorded.

---

# 7.28 Color Signature Calibration

The Pixy signatures should be trained and validated using the actual competition-style targets.

A useful process is:

```text
1. Mount Pixy in final position.

2. Present Red pillar.

3. Train / verify Signature 2.

4. Present Green pillar.

5. Train / verify Signature 3.

6. Present Pink parking reference.

7. Train / verify Signature 1.

8. Test at multiple image positions.

9. Test at multiple distances.

10. Test while Piolín is moving.
```

Changing camera position after this process can alter visual performance and may require recalibration.

---

# 7.29 Vision and Ultrasonic Sensors

Pixy2.1 and the lateral ultrasonic sensors provide different information.

```text
PIXY
→ target identity
→ image geometry


ULTRASONICS
→ lateral physical geometry
```

This produces a useful division:

```text
VISION
→ what should I avoid and on which side?


ULTRASONICS
→ what physical space surrounds the vehicle?
```

The two systems complement rather than replace one another.

---

# 7.30 Control Priority During Pillar Avoidance

One historical failure mode occurred when the wall controller and vision controller attempted to steer strongly in opposite directions.

For example:

```text
GREEN
→ pass LEFT


wall correction
→ steer RIGHT
```

If both commands are allowed to dominate simultaneously, Piolín can zig-zag or fail to commit to the pillar maneuver.

A more useful state-dependent concept is:

```text
NORMAL
→ wall navigation dominant


PILLAR
→ vision establishes avoidance objective
→ ultrasonic mainly protects unsafe geometry


PASSING
→ maintain obstacle maneuver


RECENTER
→ ultrasonic geometry becomes stronger again
```

The exact current weighting remains under development, but controller priority is an important architectural principle.

---

# 7.31 Pillar Pass Confirmation

Vision alone does not always provide strong evidence that a pillar has been physically passed.

A lateral ultrasonic sensor may observe a sequence similar to:

```text
normal distance
      ↓
pillar enters side region
      ↓
distance decreases
      ↓
pillar moves behind vehicle
      ↓
distance increases
```

This can provide additional evidence for:

```text
PASS CONFIRMED
```

before target memory is released.

The exact numerical thresholds are still being calibrated and are therefore not presented as final values here.

---

# 7.32 Recovery After a Pillar

After a pillar maneuver, Piolín may be laterally displaced.

The robot therefore needs a recovery state.

```text
AVOID
   ↓
PASS
   ↓
RECENTER
   ↓
NORMAL
```

During recentering:

```text
Pixy target influence decreases

ultrasonic geometry becomes more important

Motor B countersteers or approaches center

vehicle prepares for next target
```

Without this stage, a successful obstacle pass can still place Piolín in a poor position for the next corner or pillar.

---

# 7.33 Why a Permanent Target Lock Is Dangerous

Target locking can stabilize noisy detections.

However, a lock that never releases can create:

```text
pillar 1 selected
      ↓
pillar 1 passed
      ↓
pillar 2 appears
      ↓
old target still active
      ↓
pillar 2 ignored
```

The solution is not simply:

```text
remove all target memory
```

because that can make detection unstable again.

The stronger approach is:

```text
controlled acquisition
+
controlled release
```

with clear state transitions.

---

# 7.34 Pixy and Motor B

Pixy does not directly command Motor B.

The control chain is:

```text
PILLAR
   ↓
Pixy2.1
   ↓
block data
   ↓
EV3
   ↓
target selection
   ↓
navigation state
   ↓
steering objective
   ↓
Motor B
   ↓
Ackermann movement
```

This distinction is useful for debugging.

If Pixy reports the correct signature but Piolín passes on the wrong side, the problem may exist after perception.

Possible causes include:

```text
incorrect passing-side mapping

steering-sign inversion

state error

controller conflict

mechanical steering problem
```

The camera should not automatically be blamed.

---

# 7.35 Independent Vision Diagnostics

A diagnostic program can print values such as:

```text
signature

x

y

width

height
```

without enabling autonomous steering.

This allows the team to verify:

```text
camera
→ communication
→ EV3 parsing
```

before testing:

```text
state
→ steering
→ vehicle
```

This layered testing approach reduces the number of unknown variables during debugging.

---

# 7.36 Why Direct Communication Helps Debugging

With the current architecture:

```text
Pixy
 ↓
EV3
```

there are fewer communication layers than in the historical:

```text
HuskyLens
 ↓
Nano
 ↓
USB
 ↓
EV3
```

This does not guarantee perfect perception.

It does reduce the number of places where information can be lost or incorrectly reformatted before reaching navigation logic.

For competition debugging, reducing unnecessary intermediate layers is valuable.

---

# 7.37 Current Software Separation

Pixy2.1 is used only by the Obstacle Challenge software.

The Open Challenge does not initialize or depend on Pixy.

Conceptually:

```text
OPEN

S1 = Gyro
→ Open software
```

and:

```text
OBSTACLES

S1 = Pixy2.1
→ obstacle software
```

Keeping these configurations separate avoids unnecessary conditional code for hardware that is physically absent from the current round.

---

# 7.38 Current Pixy Responsibility Matrix

| Function                              |           Pixy2.1           |
| :------------------------------------ | :-------------------------: |
| Red pillar identification             |             Yes             |
| Green pillar identification           |             Yes             |
| Pink parking-reference identification |             Yes             |
| Horizontal image position             |             Yes             |
| Vertical image position               |             Yes             |
| Block width / height                  |             Yes             |
| Exact physical distance               | No, not without calibration |
| Wall distance                         |              No             |
| Vehicle heading                       |              No             |
| Floor Blue/Orange detection           |              No             |
| Final steering decision               |              No             |
| Target relevance input                |             Yes             |
| Obstacle-state input                  |             Yes             |

The table highlights an important principle:

> Pixy provides perception information. It does not replace the rest of the autonomous navigation system.

---

# 7.39 Values Intentionally Not Claimed as Final

The following values should only be published after they are measured or finalized on the current V4 robot:

```text
Pixy mounting height

Pixy pitch angle

Pixy yaw alignment

Pixy lateral offset

final X thresholds

final Y thresholds

final width thresholds

final height thresholds

minimum valid apparent area

target-lock duration

target-release conditions

final multi-block scoring formula

measured detection reliability

measured reaction distance

lighting performance statistics
```

The obstacle software is still actively being tuned.

Documenting these values before they stabilize would make the repository less reproducible rather than more reproducible.

---

# 7.40 Current Vision Architecture

The current obstacle perception system can be summarized as:

```text
                WRO TARGET
                    │
                    ▼
                 PIXY2.1
                    │
                    ▼
         SIGNATURE + BLOCK DATA
                    │
                    ▼
                  EV3
                    │
          ┌─────────┴─────────┐
          │                   │
          ▼                   ▼
   TARGET SELECTION      CURRENT STATE
          │                   │
          └─────────┬─────────┘
                    ▼
            PASSING OBJECTIVE
                    │
                    ▼
                 MOTOR B
                    │
                    ▼
          ACKERMANN STEERING
                    │
                    ▼
             VEHICLE MOTION
```

The two lateral ultrasonic sensors provide additional physical context around this process.

This keeps the architecture modular:

```text
VISION
→ identify and locate


ULTRASONICS
→ physical side geometry


EV3
→ decide


MOTOR B
→ execute
```

---

# 7.41 Final Engineering Assessment

Pixy2.1 was selected because the Obstacle Challenge requires perception information that the LEGO distance and orientation sensors cannot provide.

Its principal contribution is:

```text
TARGET IDENTITY
+
IMAGE POSITION
```

The current mapping is:

```text
SIG 1
→ PINK
→ parking reference


SIG 2
→ RED
→ pass RIGHT


SIG 3
→ GREEN
→ pass LEFT
```

However, the most important engineering decision is not the signature mapping itself.

It is the separation between:

```text
PERCEPTION
```

and:

```text
NAVIGATION
```

Pixy identifies visual blocks.

The EV3 decides which block matters.

The obstacle state determines what maneuver is active.

The ultrasonic sensors provide surrounding physical geometry.

Motor B creates the physical trajectory.

The complete system is therefore:

```text
VISUAL TARGET
      ↓
PIXY DETECTION
      ↓
BLOCK INTERPRETATION
      ↓
TARGET SELECTION
      ↓
STATE
      ↓
STEERING OBJECTIVE
      ↓
ACKERMANN MOTION
```

This architecture also reflects the lessons learned from the earlier HuskyLens/Nano system.

Rather than maximizing the number of processing layers, Piolín now favors a shorter communication path and clearer division of responsibility.

The central design principle is:

> **Pixy2.1 tells Piolín what it can see and where it appears in the image. The EV3 remains responsible for deciding what that perception means for the physical vehicle.**

---

<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
