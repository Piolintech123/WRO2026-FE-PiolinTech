# 8. Pixy2.1 Camera Vision

<div align="center">

<img
  src="../../v-photos/v4/pixy21_front.jpg"
  alt="Pixy2.1 installed as Piolín's forward vision sensor"
  width="700"
/>

<br>

<sub><b>Figure 8.1.</b> Pixy2.1 is Piolín's primary forward-perception sensor during the Obstacle Challenge.</sub>

</div>

Piolín uses **Pixy2.1** as its dedicated vision sensor for the WRO Future Engineers Obstacle Challenge.

The camera does not replace the EV3 as the main controller and does not directly command the steering motor. Instead, Pixy2.1 performs color-based visual detection and provides compact object information that the EV3 can use as part of the autonomous decision process.

The intended information path is:

```text
COLORED PILLAR
      ↓
PIXY2.1
      ↓
COLOR SIGNATURE DETECTION
      ↓
BLOCK GEOMETRY
      ↓
EV3
      ↓
TARGET SELECTION
      ↓
STATE MACHINE
      ↓
OBSTACLE CONTROLLER
      ↓
MOTOR B
```

The camera therefore belongs to Piolín's **perception layer**, while the EV3 remains responsible for interpreting the detection and deciding how the vehicle should move.

The current vision system is still being tuned, so this document describes the active architecture and design principles without presenting temporary thresholds or target-ranking equations as final competition values.

---

## 8.1 Current Obstacle Vision Hardware

During the Obstacle Challenge, Piolín uses the following sensor configuration:

```text
S1 → Pixy2.1

S2 → LEFT Ultrasonic Sensor

S3 → RIGHT Ultrasonic Sensor

S4 → Color Sensor
```

The EV3 Gyro Sensor is **not installed** in this configuration.

<div align="center">

<img
  src="../../v-photos/v4/s1_obstacle_pixy.jpg"
  alt="Pixy2.1 occupying Piolín EV3 Sensor Port S1"
  width="680"
/>

<br>

<sub><b>Figure 8.2.</b> During Obstacles, Pixy2.1 replaces the Open Challenge Gyro Sensor on S1.</sub>

</div>

This architecture keeps the vision path simple:

```text
Pixy2.1
    ↓
current connection cable
    ↓
EV3 S1
```

The previous:

```text
HuskyLens
→ Arduino Nano
→ EV3
```

architecture is legacy and is not part of the current competition vision system.

---

## 8.2 Direct S1 Integration

<div align="center">

<img
  src="../../v-photos/v4/pixy21_s1_connection.jpg"
  alt="Current Pixy2.1 connection to EV3 S1"
  width="680"
/>

<br>

<sub><b>Figure 8.3.</b> Pixy2.1 communicates directly with the EV3 through the current S1 connection.</sub>

</div>

The current Obstacle software architecture accesses Pixy2.1 using an **I2C/SMBus communication path** through Sensor Port S1.

The physical connection also provides the active camera connection used by the current robot.

<div align="center">

<img
  src="../../v-photos/v4/pixy21_connection_cable.jpg"
  alt="Current cable used to connect Pixy2.1 to Piolín"
  width="660"
/>

<br>

<sub><b>Figure 8.4.</b> Actual cable used in Piolín's current Pixy2.1 integration.</sub>

</div>

The repository intentionally does not invent an internal conductor-by-conductor cable pinout.

The reproducible architecture supported by the current robot is:

```text
Pixy2.1
→ current cable
→ EV3 S1
→ I2C / SMBus software interface
```

A detailed electrical pinout should only be added after the actual connection is independently verified.

---

## 8.3 Current Pixy2.1 3D-Printed Casing

Piolín's current Pixy2.1 assembly includes a **3D-printed casing**.

The casing is not a legacy prototype. It is part of the active Obstacle Challenge camera installation.

Its functions include supporting the camera mechanically, protecting the sensor assembly, and helping maintain a more repeatable physical installation.

Depending on the direction of external illumination, its geometry can also partially reduce unwanted stray light reaching the camera.

The casing should therefore remain installed during:

```text
signature calibration

camera-position calibration

target testing

Obstacle Challenge runs
```

because changing the physical enclosure can also change the optical conditions under which Pixy2.1 operates.

The repository does not currently contain a separate filename dedicated exclusively to the Pixy casing, so no nonexistent casing image is referenced here.

The important engineering principle is:

> **The camera and its physical enclosure must be calibrated as one installed sensing system.**

---

## 8.4 Color Connected Components Mode

Piolín uses Pixy2.1 primarily for **color-signature object detection**.

The vision strategy is based on identifying colored blocks representing:

```text
Red pillar

Green pillar

Pink parking reference
```

This means the relevant Pixy functionality is its color-object detection capability rather than using the camera as a line-following sensor.

The current signatures are:

| Pixy Signature | Color | Current Meaning |
| :---: | :--- | :--- |
| `sig1` | Pink | Parking reference |
| `sig2` | Red | Obstacle — pass RIGHT |
| `sig3` | Green | Obstacle — pass LEFT |

The camera and EV3 software must use the same signature mapping.

A mismatch such as:

```text
Pixy:
sig2 = Green
```

while the EV3 assumes:

```text
sig2 = Red
```

would create a logically inverted obstacle response even if the rest of the program were correct.

---

## 8.5 Fixed Obstacle Rules

<div align="center">

<img
  src="../../v-photos/v4/pixy21_red_detection.jpg"
  alt="Pixy2.1 detecting Piolín's red obstacle signature"
  width="680"
/>

<br>

<sub><b>Figure 8.5.</b> Red classification represents a pass-right obstacle.</sub>

</div>

The competition rule for Red is:

```text
RED
→ PASS RIGHT
```

<div align="center">

<img
  src="../../v-photos/v4/pixy21_green_detection.jpg"
  alt="Pixy2.1 detecting Piolín's green obstacle signature"
  width="680"
/>

<br>

<sub><b>Figure 8.6.</b> Green classification represents a pass-left obstacle.</sub>

</div>

The competition rule for Green is:

```text
GREEN
→ PASS LEFT
```

These rules remain fixed regardless of where the pillar appears inside the image.

For example:

```text
Red appears on left side of camera
```

still means:

```text
PASS RIGHT
```

and:

```text
Green appears on right side of camera
```

still means:

```text
PASS LEFT
```

This distinction is fundamental to Piolín's vision strategy.

```text
SIGNATURE
→ decides passing side
```

while:

```text
IMAGE POSITION
→ describes target geometry
```

The two concepts must never be confused.

---

## 8.6 What the Camera Reports

Pixy2.1 can provide compact block information instead of requiring the EV3 to process complete raw images.

The current software architecture is designed around information such as:

```text
signature

x

y

width

height
```

These values have different meanings.

| Value | Interpretation |
| :--- | :--- |
| `signature` | Detected color category |
| `x` | Horizontal image position |
| `y` | Vertical image position |
| `width` | Apparent block width |
| `height` | Apparent block height |

The software can represent one target conceptually as:

```python
target = {
    "signature": signature,
    "x": x,
    "y": y,
    "width": width,
    "height": height
}
```

This is an architectural representation rather than the final Pixy communication implementation.

The camera interface should ideally convert the raw Pixy response into one clean software representation before passing it to higher-level navigation.

---

## 8.7 Image Coordinates

The value:

```text
x
```

represents where the obstacle appears horizontally in Pixy's camera frame.

Conceptually:

```text
LEFT SIDE        IMAGE CENTER        RIGHT SIDE
    │                 │                  │
    └─────────────────┼──────────────────┘
                      ↑
                    target x
```

This information can help determine:

```text
whether the pillar is becoming centered

whether Piolín is moving relative to it

how quickly the target is crossing the view

how much steering correction may be useful
```

However:

```text
x
```

does not tell Piolín which side the rules require.

For example, the software should not do:

```python
if target.x < camera_center:
    pass_side = "LEFT"
else:
    pass_side = "RIGHT"
```

because that would allow image position to redefine the competition rule.

Instead:

```python
def required_pass_side(signature):
    if signature == 2:
        return "RIGHT"

    if signature == 3:
        return "LEFT"

    return None
```

The image geometry can then influence **how the maneuver is executed**, while the signature determines **which maneuver is required**.

---

## 8.8 Apparent Target Size

The values:

```text
width

height
```

represent apparent image size.

Under comparable viewing conditions:

```text
distant pillar
→ generally smaller block
```

while:

```text
closer pillar
→ generally larger block
```

This gives Piolín another useful cue for determining whether a visible target is relevant.

The software can conceptually distinguish:

```text
VISIBLE
```

from:

```text
RELEVANT
```

and finally:

```text
CLOSE / ACTIVE
```

A pillar should not automatically receive maximum steering authority simply because it appears somewhere in the camera frame.

This helps prevent a distant pillar from pulling Piolín away from its current trajectory too early.

However:

> **Pixy block size is not treated as an exact physical distance measurement unless that relationship has been separately calibrated.**

Piolín's lateral ultrasonic sensors remain the more direct physical-distance references for nearby geometry.

---

## 8.9 From Blocks to an Active Target

Pixy2.1 may detect more than one block at the same time.

A robust controller should therefore avoid:

```text
blocks[0]
→ automatically becomes target
```

The intended process is:

```text
READ BLOCKS
      ↓
VALIDATE SIGNATURES
      ↓
BUILD CANDIDATES
      ↓
EVALUATE RELEVANCE
      ↓
SELECT BEST TARGET
      ↓
CONFIRM
      ↓
LOCK
```

A conceptual validation function can be:

```python
RED_SIG = 2
GREEN_SIG = 3

def valid_obstacle_signature(signature):
    return signature in (RED_SIG, GREEN_SIG)
```

A block can then be rejected before it enters target selection:

```python
def valid_obstacle_block(block):
    if block is None:
        return False

    if not valid_obstacle_signature(block["signature"]):
        return False

    if block["width"] <= 0:
        return False

    if block["height"] <= 0:
        return False

    return True
```

This is illustrative architecture.

The final data structure may differ depending on the finished Pixy interface.

---

## 8.10 Relevance and Multiple Targets

Consider:

```text
near Red pillar
+
far Green pillar
```

Both may be valid detections.

Piolín should normally select the obstacle that is most relevant to the current trajectory rather than simply the block that Pixy happens to return first.

Potential relevance information includes:

```text
apparent width

apparent height

x-position

y-position

current navigation state

previous active target
```

A future selector may conceptually resemble:

```python
def select_target(blocks):
    best_target = None
    best_score = None

    for block in blocks:

        if not valid_obstacle_block(block):
            continue

        score = target_relevance(block)

        if best_target is None or score > best_score:
            best_target = block
            best_score = score

    return best_target
```

The exact `target_relevance()` equation is intentionally not defined here because it remains under active track testing.

The engineering objective is not to create the most complicated possible scoring function.

It is to create the **simplest selection rule that repeatedly chooses the physically relevant pillar**.

---

## 8.11 Confirmation and Target Lock

Piolín already uses confirmation and release logic in other sensor processing.

The same architectural idea is useful for camera targets.

A single frame can create:

```text
candidate
```

while repeated consistent information can create:

```text
confirmed target
```

Conceptually:

```python
if candidate_signature == last_candidate_signature:
    target_confirmations += 1
else:
    last_candidate_signature = candidate_signature
    target_confirmations = 1
```

Then:

```python
if target_confirmations >= TARGET_CONFIRMATIONS:
    active_target = candidate
```

The final number of confirmations is not fixed yet.

The trade-off is:

```text
fewer confirmations
→ faster reaction
→ greater sensitivity to unstable detections
```

versus:

```text
more confirmations
→ greater stability
→ later physical reaction
```

Once accepted, the target becomes temporarily locked:

```text
candidate
      ↓
confirmed
      ↓
ACTIVE TARGET
      ↓
AVOID
```

During that maneuver, another newly visible pillar should not freely replace it.

---

## 8.12 Temporary Target Loss

One of the most important camera limitations is that Pixy2.1 is mounted on the vehicle.

When Piolín steers:

```text
vehicle rotates
      ↓
camera rotates
      ↓
target x changes rapidly
      ↓
target can leave the field of view
```

Therefore:

```text
Pixy cannot see target now
```

does not necessarily mean:

```text
pillar has been passed
```

The state machine should retain short-term target memory.

Conceptually:

```python
if target_visible:
    last_target = current_target
    missing_cycles = 0

else:
    missing_cycles += 1
```

A short loss can then mean:

```text
continue the committed maneuver
```

rather than:

```text
immediately select a different pillar
```

The final target-loss tolerance remains a tunable value.

If it is too short:

```text
avoidance can reverse prematurely
```

If it is too long:

```text
an old pillar can remain active after it is irrelevant
```

---

## 8.13 Camera Vision and Ultrasonic Sensor Fusion

<div align="center">

<img
  src="../../v-photos/v4/piolin_obstacle_top.jpg"
  alt="Top view of Piolín showing Pixy2.1 and lateral ultrasonic sensing"
  width="720"
/>

<br>

<sub><b>Figure 8.7.</b> Piolín combines forward visual perception with physical lateral geometry rather than expecting one sensor type to solve the complete navigation problem.</sub>

</div>

Pixy2.1 and the ultrasonic sensors answer fundamentally different questions.

```text
PIXY2.1

What pillar is ahead?

What color is it?

Where does it appear?

How visually relevant is it?
```

The permanent lateral sensors answer:

```text
S2 LEFT

How close is physical geometry on the left?
```

```text
S3 RIGHT

How close is physical geometry on the right?
```

The intended sensor fusion is:

```text
PIXY
→ obstacle identity and forward geometry
```

```text
ULTRASONICS
→ physical lateral context and wall safety
```

This prevents either sensor system from being forced to solve a problem it is poorly suited for.

The ultrasonics should not decide whether a pillar is Red or Green.

Pixy should not be treated as a precise lateral wall-distance sensor.

---

## 8.14 Camera Behavior During Avoidance and Corners

Vision data must always be interpreted in the context of Piolín's current state.

During:

```text
NORMAL
```

a pillar's image coordinates largely describe a forward target.

During:

```text
AVOID
```

the camera itself is rotating as the vehicle moves around the target.

During:

```text
CORNER
```

the camera can rotate rapidly relative to the entire course.

Therefore the same change in `x` can mean different things depending on the state.

For example:

```text
large x change during NORMAL
```

may indicate meaningful target-relative movement.

But:

```text
large x change during CORNER
```

may be primarily caused by chassis rotation.

The intended interpretation is therefore:

```text
PIXY DATA
+
CURRENT STATE
→ MEANING
```

rather than:

```text
PIXY DATA
→ same steering formula everywhere
```

This is one reason the camera is integrated into the state machine rather than controlling Motor B independently.

---

## 8.15 Pink Parking Detection

<div align="center">

<img
  src="../../v-photos/v4/pixy21_parking_detection.jpg"
  alt="Pixy2.1 detecting Piolín's pink parking signature"
  width="680"
/>

<br>

<sub><b>Figure 8.8.</b> Signature 1 is reserved for the parking reference and is kept separate from Red/Green obstacle selection.</sub>

</div>

The current mapping reserves:

```text
sig1
→ Pink
→ parking reference
```

Pink should therefore be excluded from ordinary obstacle target selection.

Conceptually:

```python
def is_obstacle(signature):
    return signature in (2, 3)

def is_parking_reference(signature):
    return signature == 1
```

This prevents a Pink region from accidentally becoming:

```text
Red/Green obstacle avoidance
```

Likewise, seeing Pink should not immediately command the robot to stop or park.

The stronger logic is:

```text
course progression complete
+
parking state enabled
+
Pink reference valid
      ↓
parking controller
```

This keeps visual recognition separate from high-level course state.

---

## 8.16 Vision Calibration and Lighting

Pixy2.1 detects color, so lighting remains an important environmental variable.

Calibration should be performed using:

```text
current camera position

current camera orientation

current 3D-printed casing

representative Red pillar

representative Green pillar

representative Pink reference

representative track lighting
```

A signature that works in one lighting condition should not automatically be assumed reliable in every venue condition.

Useful validation should include:

```text
pillar centered

pillar left in frame

pillar right in frame

near target

far target

different representative illumination
```

The goal is not to make Pixy detect every possible colored object in the environment.

The goal is to make the competition targets distinguishable and repeatable within Piolín's actual camera geometry.

The 3D-printed casing can help control part of the optical environment, but it should not be described as completely eliminating lighting variation.

---

## 8.17 Field of View and Camera Mounting

<div align="center">

<img
  src="../../v-photos/v4/pixy21_side.jpg"
  alt="Side view of Piolín Pixy2.1 installation"
  width="680"
/>

<br>

<sub><b>Figure 8.9.</b> Pixy2.1 mounting geometry determines what portion of the course remains inside the camera's field of view.</sub>

</div>

<div align="center">

<img
  src="../../v-photos/v4/pixy21_top.jpg"
  alt="Top view of Piolín Pixy2.1 installation"
  width="680"
/>

<br>

<sub><b>Figure 8.10.</b> Camera lateral position and orientation are part of the vision calibration.</sub>

</div>

Vision performance depends on physical installation.

Relevant variables include:

```text
camera height

camera lateral position

camera pitch

camera yaw

mount rigidity

casing position
```

The final exact measurements have not yet been published as verified V4 specifications.

Therefore the repository should use the actual installation photographs as the physical reference until those dimensions are measured.

If the camera is moved, final visual parameters should be rechecked.

This includes:

```text
signature behavior

target x-position

apparent block size

relevance thresholds

target-loss behavior
```

because software coordinates only have physical meaning relative to the camera installation used during calibration.

---

## 8.18 Diagnostic Vision Output

Vision debugging should expose enough information to distinguish detection problems from downstream control problems.

Useful values include:

```text
STATE

NUMBER OF BLOCKS

CANDIDATE SIGNATURES

ACTIVE TARGET

X

Y

WIDTH

HEIGHT

TARGET CONFIRMATIONS

TARGET LOCKED?

TARGET MISSING?

REQUIRED PASS SIDE
```

A development output could conceptually resemble:

```text
STATE: TARGET_ACQUIRE
BLOCKS: 2
BEST_SIG: 2
X: ...
Y: ...
W: ...
H: ...
CONF: 2
LOCK: False
```

and later:

```text
STATE: AVOID
TARGET: RED
PASS: RIGHT
X: ...
W: ...
LOCK: True
```

This is extremely useful for troubleshooting.

If the terminal shows:

```text
TARGET: RED
PASS: RIGHT
```

but Piolín physically goes left, then:

```text
Pixy recognition
```

is probably not the first failure.

Investigation should continue into:

```text
control arbitration

steering sign

Motor B control

physical steering response
```

---

## 8.19 Current Limitations and Development Areas

The current vision architecture is established, but several algorithmic details are still being tuned.

These include:

```text
final target relevance equation

multiple-block ranking

minimum useful apparent size

candidate confirmation count

temporary target-memory duration

target-loss behavior

pillar-pass confirmation

camera behavior around corners

Red/Green trajectory integration

parking-reference conditions
```

These should remain documented as active development areas rather than being presented as completed final algorithms.

The hardware architecture itself is clearer:

```text
S1 = Pixy2.1

direct EV3 connection

current 3D-printed casing

sig1 = Pink

sig2 = Red

sig3 = Green
```

The distinction between:

```text
CURRENT HARDWARE
```

and:

```text
FINAL SOFTWARE TUNING
```

is important for accurate engineering documentation.

---

## 8.20 Complete Vision Pipeline

The intended Pixy2.1 software flow can be summarized as:

```text
                         PHYSICAL TARGET
                               │
                               ▼
                           PIXY2.1
                               │
                               ▼
                     COLOR SIGNATURE BLOCKS
                               │
                               ▼
                         READ THROUGH S1
                               │
                               ▼
                        VALIDATE BLOCKS
                               │
                  ┌────────────┴────────────┐
                  │                         │
                  ▼                         ▼
             sig2 / sig3                  sig1
              obstacles                  parking
                  │                         │
                  ▼                         │
          BUILD TARGET CANDIDATES            │
                  │                         │
                  ▼                         │
            EVALUATE RELEVANCE               │
                  │                         │
                  ▼                         │
             SELECT TARGET                   │
                  │                         │
                  ▼                         │
             CONFIRM TARGET                  │
                  │                         │
                  ▼                         │
               LOCK TARGET                  │
                  │                         │
                  ▼                         │
             STATE MACHINE                   │
                  │                         │
             ┌────┴────┐                    │
             │         │                    │
             ▼         ▼                    │
           AVOID   PASS_CONFIRM              │
             │         │                    │
             └────┬────┘                    │
                  ▼                         │
               RECOVER                      │
                  │                         │
                  └─────────────┬───────────┘
                                ▼
                         NEXT NAVIGATION STATE
```

The camera remains a perception device throughout this process.

The EV3 retains authority over every final motor command.

---

## 8.21 Final Engineering Assessment

Piolín's Pixy2.1 vision system is designed around **interpretation rather than direct camera steering**.

The current camera provides:

```text
signature

x

y

width

height
```

which the EV3 converts into increasingly meaningful information:

```text
RAW BLOCK

→ VALID BLOCK

→ CANDIDATE

→ RELEVANT TARGET

→ CONFIRMED TARGET

→ LOCKED TARGET
```

Only then does the obstacle state machine allow the target to influence the vehicle trajectory.

The fixed mapping is:

```text
sig1
→ Pink
→ parking reference
```

```text
sig2
→ Red
→ PASS RIGHT
```

```text
sig3
→ Green
→ PASS LEFT
```

The passing side is therefore determined by:

```text
SIGNATURE
```

and never by:

```text
left/right position inside the image
```

Camera coordinates and apparent size instead provide information about:

```text
target geometry

target relevance

maneuver progression
```

Piolín also does not depend on vision alone.

The complete perception architecture combines:

```text
PIXY2.1
→ forward obstacle perception
```

with:

```text
S2 / S3
→ lateral physical geometry
```

and:

```text
S4
→ course-state landmarks
```

The current Pixy2.1's **3D-printed casing** is considered part of its calibrated physical installation, so camera tuning should be performed with the casing installed and the mounting geometry unchanged.

Patterns already tested elsewhere in Piolín's software—such as bounded values, sensor confirmation, event locking, and controlled release—provide a useful basis for target confirmation and target locking, even though the final Pixy-specific implementation is still evolving.

The central vision principle is:

> **Pixy2.1 should tell Piolín what it sees and where it sees it; the EV3 must decide whether that object matters, what the competition rule requires, and when the resulting maneuver should begin or end.**

This separation makes the vision system easier to calibrate, debug, and improve without coupling every camera observation directly to Motor B behavior.

---

<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
