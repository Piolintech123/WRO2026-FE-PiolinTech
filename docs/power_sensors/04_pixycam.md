# 4. Pixy2.1 Vision Sensor

<div align="center">

<img
  src="../../v-photos/v4/pixy21_front.jpg"
  alt="Pixy2.1 installed on Piolín for the Obstacle Challenge"
  width="700"
/>

<br>

<sub><b>Figure 4.1.</b> Pixy2.1 is Piolín's forward-facing vision sensor for the WRO Future Engineers Obstacle Challenge.</sub>

</div>

Piolín uses a **Pixy2.1 camera as its specialized vision sensor during the Obstacle Challenge**. The camera is connected directly to the LEGO Mindstorms EV3 through **Sensor Port S1** and provides information about the colored objects located ahead of the robot.

The Pixy2.1 is not installed during the Open Challenge.

Piolín's S1 architecture is intentionally round-specific:

```text
OPEN CHALLENGE
S1 → EV3 Gyro Sensor
```

```text
OBSTACLE CHALLENGE
S1 → Pixy2.1
```

Therefore:

```text
Gyro + Pixy simultaneously
→ NOT part of the current architecture
```

During Obstacles, the complete sensor arrangement is:

```text
S1 → Pixy2.1

S2 → Left Ultrasonic Sensor

S3 → Right Ultrasonic Sensor

S4 → Color Sensor
```

Pixy2.1 provides the information that Piolín cannot obtain from its ultrasonic or floor Color Sensor systems: **the visual identity and image location of the colored pillars ahead of the vehicle**.

---

## 4.1 Role in the Obstacle Challenge

The WRO Future Engineers Obstacle Challenge requires Piolín to distinguish between red and green pillars because each color defines a different required passing side.

The current rule implemented in Piolín's navigation strategy is:

```text
RED
→ pass RIGHT
```

```text
GREEN
→ pass LEFT
```

Pixy2.1 therefore provides two fundamental pieces of information:

```text
WHAT object is visible?
```

and:

```text
WHERE is that object in the image?
```

These two questions correspond to different parts of the camera output.

The detected color signature determines the obstacle type, while image coordinates and block dimensions provide geometric information that can help determine how relevant the object currently is.

The camera does **not** directly command Motor B.

Instead:

```text
Pixy2.1
     ↓
visual measurement
     ↓
EV3
     ↓
target selection
     ↓
obstacle-state logic
     ↓
steering decision
     ↓
Motor B
```

This separation is important because vision is only one part of the final navigation decision.

---

# 4.2 Physical Installation

<div align="center">

<img
  src="../../v-photos/v4/pixy21_top.jpg"
  alt="Top view of Pixy2.1 installed on Piolín"
  width="700"
/>

<br>

<sub><b>Figure 4.2.</b> Top view of the Pixy2.1 installation showing its relationship with Piolín's forward vehicle axis.</sub>

</div>

Pixy2.1 is positioned toward the front of Piolín so that it can observe pillars before the vehicle reaches them.

Unlike the downward Color Sensor or the lateral ultrasonic sensors, Pixy observes the environment in front of the robot.

Its physical orientation therefore establishes the visual reference frame used by the software.

Conceptually:

```text
          FORWARD

             ↑
             │
          [ PIXY ]
             │
       ┌─────────────┐
       │   PIOLÍN    │
       │             │
       └─────────────┘
```

The camera should remain sufficiently stable that the same physical pillar appears in a similar region of the image under comparable vehicle geometry.

This makes the camera mount part of the vision calibration.

---

## 4.3 Why Camera Alignment Matters

<div align="center">

<img
  src="../../v-photos/v4/pixy21_side.jpg"
  alt="Side view of Pixy2.1 mounted on Piolín"
  width="680"
/>

<br>

<sub><b>Figure 4.3.</b> Side view used to document the physical orientation of the camera relative to the chassis.</sub>

</div>

A visual coordinate such as:

```text
x = some image position
```

only has consistent physical meaning if the camera remains in approximately the same orientation.

Changes in:

```text
camera yaw

camera pitch

camera height

camera lateral position
```

can change where a pillar appears even if the course itself has not changed.

For example:

```text
camera rotates slightly left
       ↓
same physical pillar
       ↓
appears farther right in the image
```

A software problem should therefore not be assumed immediately when visual steering behavior changes after mechanical work.

The camera mount should first be inspected.

---

# 4.4 Direct EV3 Connection

<div align="center">

<img
  src="../../v-photos/v4/pixy21_s1_connection.jpg"
  alt="Pixy2.1 connected directly to EV3 Sensor Port S1"
  width="680"
/>

<br>

<sub><b>Figure 4.4.</b> Current Obstacle Challenge architecture connects Pixy2.1 directly to Sensor Port S1.</sub>

</div>

The current Piolín architecture uses a direct connection between Pixy2.1 and the EV3.

The high-level communication path is:

```text
Pixy2.1
   ↓
S1
   ↓
EV3
```

The current Obstacle Challenge software accesses Pixy2.1 through an **I2C/SMBus-style communication path** in the EV3 environment.

This architecture replaces an earlier vision system that used additional intermediate electronics.

The current competition configuration does not require:

```text
Arduino Nano

HuskyLens

USB-to-Arduino vision bridge
```

for Pixy operation.

---

# 4.5 Connection Hardware

<div align="center">

<img
  src="../../v-photos/v4/pixy21_connection_cable.jpg"
  alt="Cable used to connect Pixy2.1 to Piolín EV3"
  width="680"
/>

<br>

<sub><b>Figure 4.5.</b> Physical cable used in Piolín's current Pixy2.1-to-EV3 integration.</sub>

</div>

The physical connection is important for reproducibility because Pixy2.1 is the primary non-LEGO sensing device in the current competition robot.

The repository should therefore show the real connection rather than relying only on a textual statement such as:

```text
connect camera to S1
```

The current architecture uses S1 as the physical interface for both communication and the installed camera connection during Obstacles.

The exact physical cable shown in the repository is therefore part of the current hardware definition.

---

# 4.6 S1 Modularity

<div align="center">

<img
  src="../../v-photos/v4/s1_obstacle_pixy.jpg"
  alt="Piolín S1 configured with Pixy2.1 for the Obstacle Challenge"
  width="680"
/>

<br>

<sub><b>Figure 4.6.</b> S1 becomes the vision interface when Piolín is configured for the Obstacle Challenge.</sub>

</div>

The S1 port is Piolín's specialized sensing port.

The robot does not attempt to permanently install every sensor used across both challenges.

Instead:

```text
OPEN
→ install Gyro on S1
```

and:

```text
OBSTACLES
→ install Pixy2.1 on S1
```

The remaining ports stay unchanged:

```text
S2 = LEFT Ultrasonic

S3 = RIGHT Ultrasonic

S4 = Color Sensor
```

This reduces the number of hardware changes required between rounds while allowing each challenge to use the specialized sensor that provides the most valuable information.

---

# 4.7 Color Connected Components

Piolín uses Pixy2.1 primarily for **color-based object detection**, rather than using the camera as a conventional video stream.

The important output is a set of detected visual blocks.

A block can provide information such as:

```text
signature

x

y

width

height
```

These values can be interpreted as:

| Value | Meaning in Piolín |
| :--- | :--- |
| `signature` | Which trained color category was recognized |
| `x` | Horizontal image position |
| `y` | Vertical image position |
| `width` | Apparent block width |
| `height` | Apparent block height |

The EV3 can use these values without processing a complete camera image itself.

This is useful because the camera performs the low-level visual segmentation and sends compact object information to the controller.

---

# 4.8 Current Signature Mapping

Piolín currently uses three important Pixy signatures:

| Signature | Physical Target | Navigation Meaning |
| :---: | :--- | :--- |
| `sig1` | Pink parking reference | Parking-related visual state |
| `sig2` | Red pillar | Pass on the right |
| `sig3` | Green pillar | Pass on the left |

Therefore:

```text
sig2
→ RED
→ RIGHT
```

and:

```text
sig3
→ GREEN
→ LEFT
```

The mapping must remain consistent between:

```text
Pixy training

EV3 software

documentation

testing
```

If the camera signatures are retrained or reassigned but the EV3 code is not updated, the robot can execute the correct software logic for the wrong physical color.

---

# 4.9 Red Pillar Detection

<div align="center">

<img
  src="../../v-photos/v4/pixy21_red_detection.jpg"
  alt="Pixy2.1 detecting a red WRO pillar"
  width="700"
/>

<br>

<sub><b>Figure 4.7.</b> Red pillar detection provides the visual identity required for a pass-right maneuver.</sub>

</div>

When Pixy identifies the red signature, the high-level navigation objective becomes:

```text
PASS RIGHT
```

However, this does not mean:

```text
red detected
→ maximum right steering
```

The final steering behavior depends on additional information.

The EV3 can consider:

```text
block position

apparent block size

current maneuver state

left/right ultrasonic geometry

vehicle motion

previous target state
```

before deciding how strongly Motor B should react.

The red signature therefore establishes the **passing-side objective**, not the complete steering trajectory.

---

# 4.10 Green Pillar Detection

<div align="center">

<img
  src="../../v-photos/v4/pixy21_green_detection.jpg"
  alt="Pixy2.1 detecting a green WRO pillar"
  width="700"
/>

<br>

<sub><b>Figure 4.8.</b> Green pillar detection establishes a pass-left navigation objective.</sub>

</div>

For Green:

```text
GREEN
→ PASS LEFT
```

The same principle applies.

A complete maneuver can involve:

```text
approach

initial avoidance

side pass

pillar clearance

countersteering

recovery
```

rather than one continuous steering direction.

The current obstacle controller is still being developed, so final steering magnitudes and transition thresholds should not be presented as fully validated values yet.

---

# 4.11 Horizontal Position — `x`

The `x` coordinate describes where the visual block appears horizontally in Pixy's image.

Conceptually:

```text
LEFT SIDE        IMAGE CENTER        RIGHT SIDE

    |----------------|----------------|
```

A pillar's image position can help determine how much steering correction is useful.

However, one critical distinction must be maintained:

```text
signature
→ determines required passing side
```

while:

```text
x
→ contributes to steering magnitude / target geometry
```

The obstacle rule must not accidentally change just because a pillar moves from one side of the image to the other.

For example:

```text
RED
```

must still represent:

```text
PASS RIGHT
```

regardless of whether the red pillar initially appears somewhat left or right of image center.

This prevents image perspective from redefining the competition rule.

---

# 4.12 Why Image Left/Right Is Not the Passing Rule

One of the important lessons from Piolín's obstacle development is that several different concepts of "left" and "right" exist.

These include:

```text
left side of camera image

right side of camera image

left side of robot

right side of robot

required side of pillar
```

These concepts must not be confused.

The rule is defined relative to the **required passing side of the pillar**:

```text
GREEN
→ Piolín passes LEFT of pillar

RED
→ Piolín passes RIGHT of pillar
```

The current `x` coordinate describes only the target's visual location.

It should influence the geometry of the maneuver without changing the required side.

---

# 4.13 Block Width and Height

Pixy also reports apparent block dimensions.

These values can help estimate whether an object is becoming more visually significant.

Conceptually:

```text
small apparent block
→ possibly farther / less relevant
```

```text
larger apparent block
→ possibly closer / more relevant
```

However:

```text
width × height
```

is an **apparent image area**, not a direct physical distance measurement.

The relationship can also be affected by:

```text
viewing angle

partial visibility

lighting

pillar position

camera orientation
```

Therefore block size can contribute to relevance selection but should not be described as an exact centimeter measurement unless an appropriate calibration is performed.

---

# 4.14 Why Very Distant Pillars Should Not Dominate Steering

Pixy can sometimes see a pillar before it becomes the obstacle Piolín should actively maneuver around.

If every visible block immediately receives full steering authority:

```text
distant pillar detected
        ↓
strong steering begins too early
        ↓
vehicle leaves stable course geometry
```

A stronger strategy considers whether the target is sufficiently relevant.

Possible relevance evidence includes:

```text
valid signature

image position

apparent size

current course state

previous target
```

The goal is to react early enough to avoid the pillar without allowing very distant detections to continuously disturb straight driving.

---

# 4.15 Multiple Visible Blocks

The camera may detect more than one valid object at the same time.

A weak implementation could simply choose:

```text
first block returned by Pixy
```

but the first returned block is not guaranteed to be the obstacle that matters most for the current trajectory.

Piolín's intended target-selection logic therefore considers **relevance**, not only list order.

A candidate can be evaluated using information such as:

```text
signature validity

apparent size

horizontal position

current vehicle state

previous target
```

The selected object should represent the pillar that currently requires navigation attention.

The exact final scoring method remains under development.

---

# 4.16 Target Lock

Once Piolín commits to passing one pillar, immediately switching to another detected block can destabilize steering.

For example:

```text
red selected
      ↓
right-side maneuver begins
      ↓
another green becomes visible
      ↓
controller instantly changes target
      ↓
steering reverses
```

This can destroy the current avoidance trajectory.

A temporary target lock can therefore be useful.

Conceptually:

```text
select relevant pillar
      ↓
lock current target
      ↓
execute avoidance
      ↓
confirm pillar has been passed
      ↓
release target
```

The lock is temporary.

It should not permanently ignore the next obstacle.

---

# 4.17 Target Loss

The camera can temporarily lose a pillar while Piolín is already avoiding it.

This can happen because:

```text
vehicle steering changes camera angle

pillar moves outside field of view

partial occlusion occurs

lighting changes
```

A weak controller could interpret:

```text
target disappeared
```

as:

```text
immediately cancel maneuver
```

That is unsafe because the physical pillar may still be beside the vehicle.

A more robust approach uses the recent maneuver state and ultrasonic geometry to continue the maneuver long enough to determine whether the obstacle was actually cleared.

---

# 4.18 Pixy Field of View and Vehicle Motion

Piolín's camera is physically attached to the chassis.

Therefore steering the vehicle also steers the camera.

The sequence is:

```text
Motor B changes wheel angle
        ↓
Piolín changes yaw
        ↓
camera orientation changes
        ↓
pillar x/y position changes
```

A target can therefore leave the camera view because Piolín itself turned, not because the obstacle suddenly stopped being relevant.

Vision must be interpreted in the context of the current vehicle motion.

---

# 4.19 Pixy + Ultrasonic Fusion

<div align="center">

<img
  src="../../v-photos/v4/ultrasonic_pair_top.jpg"
  alt="Piolín lateral ultrasonic sensors used alongside Pixy2.1"
  width="700"
/>

<br>

<sub><b>Figure 4.9.</b> Pixy2.1 supplies visual obstacle information while the two lateral ultrasonic sensors preserve physical track-boundary context.</sub>

</div>

Pixy and the ultrasonic sensors measure different things.

```text
PIXY
→ object identity
→ image location
→ apparent object size
```

```text
S2 / S3
→ physical left/right geometry
→ wall proximity
→ post-maneuver recovery context
```

Neither subsystem completely replaces the other.

This creates a sensor-fusion architecture in which:

```text
Pixy
→ defines obstacle objective
```

while:

```text
Ultrasonics
→ constrain the maneuver using physical geometry
```

The EV3 combines both sources before producing the final steering behavior.

---

# 4.20 Why Wall Control Must Not Fight Obstacle Avoidance

During normal driving, ultrasonic information can influence steering toward a stable corridor position.

During a pillar maneuver, however, Piolín intentionally moves away from its normal path.

If normal wall-centering logic is allowed to dominate:

```text
Pixy requests pillar avoidance
```

while:

```text
wall controller requests recentering
```

and the commands can oppose each other.

The intended control hierarchy should therefore recognize that different states require different priorities.

Conceptually:

```text
NORMAL DRIVING
→ wall geometry has strong influence
```

```text
ACTIVE PILLAR AVOIDANCE
→ pillar objective receives greater steering authority
→ wall sensing remains safety/context
```

```text
PILLAR CLEARED
→ ultrasonic recovery becomes stronger again
```

This avoids having two controllers continuously fight for Motor B.

---

# 4.21 Pillar-Pass Confirmation

A pillar should not be considered cleared only because Pixy stops reporting it.

Instead, Piolín can use additional geometric evidence from the lateral ultrasonic sensors.

A conceptual process is:

```text
Pixy detects target
      ↓
avoidance begins
      ↓
vehicle moves alongside pillar
      ↓
lateral geometry changes
      ↓
vehicle continues
      ↓
space opens again
      ↓
pillar considered passed
```

This allows the robot to distinguish:

```text
target lost from camera
```

from:

```text
target physically passed
```

The final numerical pass-confirmation conditions are still under development.

---

# 4.22 Recovery After a Pillar

After clearing the pillar, Piolín must return to a usable state.

The desired transition is:

```text
PIXY TARGETING
      ↓
AVOIDANCE
      ↓
PASS CONFIRMATION
      ↓
COUNTERSTEERING
      ↓
ULTRASONIC RECOVERY
      ↓
NORMAL COURSE CONTROL
```

This is important because successful obstacle navigation is not only:

```text
do not hit current pillar
```

It is:

```text
pass correct side
+
avoid walls
+
recover
+
prepare for next obstacle
```

The camera is therefore most dominant during target identification and avoidance, while the ultrasonic system becomes increasingly important as Piolín returns to normal track geometry.

---

# 4.23 Parking Signature

<div align="center">

<img
  src="../../v-photos/v4/pixy21_parking_detection.jpg"
  alt="Pixy2.1 detecting the pink parking reference"
  width="700"
/>

<br>

<sub><b>Figure 4.10.</b> Signature 1 is currently assigned to Piolín's pink parking reference.</sub>

</div>

The current mapping reserves:

```text
sig1
→ PINK
→ PARKING
```

However, the detection of the parking reference should not automatically stop the robot during any point of the run.

A stronger final parking condition can require:

```text
correct course progression

parking state enabled

valid pink detection

vehicle position / motion context
```

before the final maneuver begins.

This prevents an isolated or premature visual detection from triggering parking at the wrong time.

The final parking sequence remains a work in progress.

---

# 4.24 Camera Detection vs. Floor Color Detection

Piolín contains two systems involving color, but they should not be confused.

### Pixy2.1

```text
forward-facing

detects objects ahead

Red pillar

Green pillar

Pink parking reference
```

### EV3 Color Sensor

```text
downward-facing

detects floor directly beneath vehicle

Blue floor reference

Orange floor reference
```

The two sensors therefore operate on different physical regions and serve different state variables.

Pixy answers:

```text
What visual object is ahead?
```

S4 answers:

```text
What floor landmark did Piolín cross?
```

---

# 4.25 Lighting Conditions

Color-based vision depends strongly on lighting.

Possible effects include:

```text
shadows

different room illumination

reflections

brightness changes

background objects

color saturation changes
```

A trained signature that works under one lighting condition may become weaker under another.

Therefore Pixy testing should be performed under representative competition conditions.

The final signature configuration should provide enough distinction between:

```text
red

green

pink

background
```

without becoming so broad that unrelated objects are accepted.

---

# 4.26 Why Detection Confidence Must Be Built from More Than One Factor

A visual detection can technically match a signature while still being a poor navigation target.

For example:

```text
very small red object far away

partial reflection

background color region

edge of another pillar
```

can produce a candidate that should not necessarily dominate steering.

A stronger interpretation can consider:

```text
correct signature
+
reasonable block size
+
useful image position
+
consistency over time
+
current navigation context
```

rather than:

```text
one matching sample
→ full maneuver
```

This reduces the effect of weak or irrelevant detections.

---

# 4.27 Temporal Confirmation

One way to improve visual stability is to require a detection to remain plausible across more than one observation.

Conceptually:

```text
possible target
      ↓
seen again
      ↓
consistent signature / geometry
      ↓
accept target
```

However, temporal confirmation creates the same trade-off present in other real-time sensors:

```text
more confirmation
→ more stability
→ more delay
```

At vehicle speed, delay means:

```text
Piolín travels farther
before steering begins
```

The confirmation strategy must therefore remain short enough for obstacle reaction.

---

# 4.28 Vision Reaction Distance

The obstacle controller should react early enough that Motor B has time to alter the physical trajectory.

The complete delay chain is:

```text
pillar enters useful camera region
      ↓
Pixy detects block
      ↓
EV3 reads block
      ↓
target is selected
      ↓
steering command calculated
      ↓
Motor B moves
      ↓
front wheels change angle
      ↓
vehicle path begins changing
```

Motor A can continue moving Piolín throughout this sequence.

Therefore:

```text
higher vehicle speed
→ greater distance traveled before avoidance develops
```

This is why camera tuning, steering tuning, and propulsion speed must be tested together.

---

# 4.29 Why Maximum Steering Is Not Always the Best Reaction

A stronger steering command can reduce collision risk when reaction occurs late.

However, excessive steering can create:

```text
wall collision

loss of camera target

large recovery requirement

zig-zag

poor approach to next pillar
```

The desired behavior is therefore not:

```text
pillar visible
→ maximum steering
```

but:

```text
pillar relevance increases
→ appropriate avoidance steering increases
```

with safety limits and current geometry still considered.

---

# 4.30 Full Obstacle Sensor Configuration

<div align="center">

<img
  src="../../v-photos/v4/wiring_obstacle.jpg"
  alt="Piolín complete Obstacle Challenge wiring configuration"
  width="720"
/>

<br>

<sub><b>Figure 4.11.</b> Current Obstacle Challenge wiring with Pixy2.1 on S1, lateral ultrasonics on S2/S3, and Color Sensor on S4.</sub>

</div>

The current obstacle hardware mapping is:

```text
MOTORS

A
→ Large Motor
→ propulsion

B
→ Medium Motor
→ steering
```

```text
SENSORS

S1
→ Pixy2.1

S2
→ LEFT Ultrasonic

S3
→ RIGHT Ultrasonic

S4
→ Color Sensor
```

No gyro is installed during this configuration.

No Arduino Nano is required.

No HuskyLens is part of the current system.

---

# 4.31 Current Obstacle Software Environment

The current direct Pixy development path uses:

```text
ev3dev2
+
SMBus / I2C
```

on the EV3.

The intended software architecture should keep Pixy communication separate from the Open Challenge Pybricks implementation.

Conceptually:

```text
src/
├── open_challenge.py
│   └── Pybricks + Gyro
│
└── obstacle_challenge.py
    └── ev3dev2 + Pixy2.1
```

This separation reflects the physical architecture:

```text
Open S1 device
≠
Obstacle S1 device
```

and prevents one large program from containing unnecessary drivers for hardware that is not installed during the active round.

---

# 4.32 Vision Diagnostic Process

When Piolín reacts incorrectly to a pillar, the problem should be traced through the full sensing chain.

A useful diagnostic sequence is:

```text
1. Is Pixy powered / communicating?

2. Is the correct signature detected?

3. Is the reported block actually the pillar?

4. Are x, y, width, and height plausible?

5. Was the correct target selected?

6. Was the correct passing rule applied?

7. Did Motor B receive the intended steering command?

8. Did the physical steering respond correctly?

9. Did ultrasonic safety interfere?

10. Was the target released at the correct time?
```

This prevents a steering problem from being blamed on the camera automatically—or a vision-selection error from being corrected by reversing Motor B polarity.

---

# 4.33 Common Failure Modes

| Observed Behavior | Possible Cause |
| :--- | :--- |
| Pixy detects nothing | S1 connection, signature training, lighting, target visibility |
| Red not recognized | Signature calibration or lighting |
| Green not recognized | Signature calibration or lighting |
| Pink not recognized | Parking-signature calibration |
| Red causes pass-left behavior | Software passing-side mapping |
| Green causes pass-right behavior | Software passing-side mapping |
| Pillar is detected but robot reacts too late | Relevance threshold, confirmation delay, vehicle speed |
| Robot reacts to very distant pillars | Target relevance too permissive |
| Robot changes target mid-maneuver | Target lock too weak |
| Robot stays locked after passing pillar | Target-release logic too weak |
| Target disappears during steering | Field of view changed with vehicle yaw |
| Robot avoids pillar but hits wall | Wall safety/recovery arbitration |
| Robot passes pillar but does not recenter | Countersteering or ultrasonic recovery |
| Different behavior after camera remount | Camera orientation changed |
| Correct signature but wrong block selected | Multiple-target selection logic |

A failure should be classified before parameters are changed.

---

# 4.34 Camera Testing

A complete camera test should progress through several levels.

### Signature test

Present one target at a time:

```text
Red

Green

Pink
```

and verify the reported signature.

### Position test

Move the same pillar across the camera view and verify that `x` changes in the expected direction.

### Apparent-size test

Move the target through different useful distances and observe how:

```text
width

height
```

change.

### Multiple-block test

Place more than one valid target in view and verify which one the EV3 selects.

### Dynamic driving test

Allow Piolín to approach a pillar under realistic motion.

This introduces:

```text
vehicle speed

camera yaw

steering response

changing apparent size
```

which cannot be tested with the robot stationary.

---

# 4.35 Red and Green Must Be Tested Independently

<div align="center">

<img
  src="../../v-photos/v4/piolin_obstacle_isometric.jpg"
  alt="Piolín complete Obstacle Challenge configuration"
  width="720"
/>

<br>

<sub><b>Figure 4.12.</b> Complete vehicle configuration used for dynamic vision and obstacle-navigation testing.</sub>

</div>

A successful Green test does not prove Red is calibrated correctly.

Likewise, successful Red behavior does not prove Green.

The two cases differ in:

```text
signature

required side

image geometry

steering direction

wall relationship
```

Each should therefore be tested separately before evaluating alternating pillar sequences.

---

# 4.36 Multiple-Pillar Testing

Once isolated Red and Green maneuvers are stable, Piolín should be tested with sequences such as:

```text
RED → RED

GREEN → GREEN

RED → GREEN

GREEN → RED
```

These tests are valuable because they expose state-management problems that single-pillar tests cannot.

For example:

```text
first Red correctly avoided
      ↓
target not released
      ↓
next Green ignored
```

or:

```text
first target released too early
      ↓
second target becomes active
before current pass is complete
```

Vision testing must therefore evaluate both object recognition and temporal target management.

---

# 4.37 Current vs. Legacy Vision Architecture

Piolín's current vision architecture is:

```text
Pixy2.1
   ↓
S1
   ↓
EV3
```

Previous development included a different architecture involving:

```text
HuskyLens

Arduino Nano

USB communication
```

Those components played an important role in development, but they are not part of the current competition hardware.

The change reduced the number of active layers between visual detection and the EV3 controller.

Legacy material should remain documented separately as engineering history rather than mixed with current wiring and reproduction instructions.

---

# 4.38 Why the Previous Vision Architecture Was Replaced

The previous vision system demonstrated several useful concepts but introduced additional interfaces.

The chain required:

```text
vision sensor
      ↓
intermediate controller
      ↓
communication bridge
      ↓
EV3
```

The current architecture is shorter:

```text
Pixy2.1
      ↓
EV3
```

This reduces:

```text
hardware count

additional firmware

communication dependencies

wiring complexity
```

while retaining the visual information needed for color-based obstacle navigation.

The engineering decision was therefore not simply:

```text
new camera is better
```

but:

> **The direct Pixy2.1 architecture better matches the current Piolín system by simplifying the communication chain while still supplying the obstacle information required by the controller.**

---

# 4.39 Values Intentionally Not Claimed as Final

The following parameters should only be published after current V4 testing and calibration:

```text
final Pixy mounting height

final camera pitch

final camera yaw

final camera lateral offset

final image-center target

final Red threshold configuration

final Green threshold configuration

final Pink threshold configuration

minimum accepted block width

minimum accepted block height

minimum accepted block area

maximum useful detection distance

final target relevance formula

final target-lock duration

final target-loss tolerance

final detection confirmation count

final pillar-pass confirmation threshold

final steering mapping from x

final reaction distance

measured detection success rate

measured Red-pass success rate

measured Green-pass success rate

parking-signature success rate
```

Working code may contain temporary values, but they should be documented as tuning values rather than validated final specifications until supported by representative testing.

---

# 4.40 Final Vision Architecture

<div align="center">

<img
  src="../../v-photos/v4/piolin_obstacle_top.jpg"
  alt="Top view of Piolín complete Obstacle Challenge architecture"
  width="720"
/>

<br>

<sub><b>Figure 4.13.</b> Piolín's current Obstacle Challenge configuration integrates forward vision with permanent lateral and floor sensing.</sub>

</div>

The complete visual-control chain is:

```text
                  PHYSICAL PILLAR
                        │
                        ▼
                    PIXY2.1
                        │
          ┌─────────────┼─────────────┐
          │             │             │
          ▼             ▼             ▼
      signature         x/y       width/height
          │             │             │
          └─────────────┼─────────────┘
                        ▼
                       EV3
                        │
                 TARGET SELECTION
                        │
                        ▼
                 MANEUVER STATE
                        │
          ┌─────────────┴─────────────┐
          ▼                           ▼
     PIXY OBJECTIVE              S2/S3 CONTEXT
          │                           │
          └─────────────┬─────────────┘
                        ▼
                 STEERING DECISION
                        │
                        ▼
                    MOTOR B
                        │
                        ▼
                 VEHICLE MOTION
                        │
                        ▼
                NEW CAMERA VIEW
```

This is a feedback loop.

Piolín's movement changes what Pixy sees, and the new visual information changes the next steering decision.

---

# 4.41 Final Engineering Assessment

Pixy2.1 provides Piolín with the specialized forward visual perception required by the WRO Future Engineers Obstacle Challenge.

Its current architecture is intentionally simple:

```text
Pixy2.1
→ S1
→ EV3
```

and is active only during Obstacles.

The camera currently distinguishes:

```text
sig1 → Pink → parking reference

sig2 → Red → pass right

sig3 → Green → pass left
```

while also providing block position and apparent size information that can help the EV3 determine which obstacle is currently most relevant.

The camera is not treated as an independent steering controller.

Instead:

```text
Pixy
→ defines obstacle identity and visual geometry

Ultrasonics
→ provide physical boundary context

Color Sensor
→ provides course-state information

EV3
→ combines the information

Motor B
→ produces the physical steering response
```

This architecture also avoids one of the most important possible interpretation errors: **the side on which a pillar appears in the camera does not redefine the side on which Piolín must pass it**.

The passing rule remains fixed:

```text
RED
→ RIGHT

GREEN
→ LEFT
```

while `x`, `y`, `width`, and `height` describe the current visual geometry.

Target selection, temporary locking, pass confirmation, ultrasonic recovery, and obstacle-state management are therefore required to transform a camera detection into a complete vehicle maneuver.

The main engineering principle behind the subsystem is:

> **Use vision to identify the obstacle and describe its visual relevance, but let the complete vehicle controller determine the trajectory using both camera information and physical track geometry.**

This makes Pixy2.1 not merely a color detector, but the visual perception layer of Piolín's Obstacle Challenge navigation system.

---

<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
