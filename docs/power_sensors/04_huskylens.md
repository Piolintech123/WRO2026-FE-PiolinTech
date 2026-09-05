# 4. HuskyLens Vision System

Piolín uses a **HuskyLens vision sensor** as the primary obstacle-identification system for the WRO Future Engineers Obstacle Challenge.

The vision subsystem has one main responsibility:

```text
Identify the relevant pillar
        ↓
Determine its learned ID
        ↓
Provide obstacle information
to the LEGO EV3
```

The HuskyLens does **not** directly drive Motor A or Motor B.

Instead, the current architecture separates:

```text
VISION
   ↓
What obstacle is present?


ULTRASONICS
   ↓
What surrounding space is available?


LEGO EV3
   ↓
What should Piolín do?
```

The confirmed vision communication chain is:

```text
PILLAR
   ↓
HuskyLens
   ↓
Arduino Nano
   ↓
USB
   ↓
LEGO EV3
   ↓
Navigation Decision
   ↓
Motor A + Motor B
```

This preserves the EV3 as the main vehicle controller.

For the complete sensor configuration, see:

[Power and Sensor Configuration](01_PowerSensorconfig.md)

For component-level information, see:

[HuskyLens Hardware](../components/07_HuskyLens.md)

---

## 4.1 Current Vision Configuration

The current Piolín vision architecture is:

| Element | Current Role |
| :--- | :--- |
| **Vision Sensor** | HuskyLens |
| **Physical Position** | Forward-facing |
| **Supporting Controller** | Arduino Nano |
| **Nano → EV3 Connection** | USB |
| **Main Vehicle Controller** | LEGO EV3 |
| **Green Pillar** | ID 1 |
| **Red Pillar** | ID 2 |
| **Green Passing Side** | Left |
| **Red Passing Side** | Right |
| **Open Challenge Requirement** | Not required for normal wall navigation |
| **Obstacle Challenge Requirement** | Obstacle identification |

The system therefore converts:

```text
VISUAL OBJECT
      ↓
IDENTITY
      ↓
NAVIGATION REQUIREMENT
```

rather than attempting to control the complete vehicle from camera information alone.

---

# 4.2 Current Obstacle Mapping

The current trained mapping used by Piolín is:

```text
ID 1
=
GREEN PILLAR
```

which corresponds to:

```text
PASS ON LEFT
```

and:

```text
ID 2
=
RED PILLAR
```

which corresponds to:

```text
PASS ON RIGHT
```

The logical mapping is therefore:

```text
ID 1
  ↓
GREEN
  ↓
LEFT PASS
```

and:

```text
ID 2
  ↓
RED
  ↓
RIGHT PASS
```

This mapping should remain consistent between:

```text
HuskyLens training

Arduino Nano communication

EV3 interpretation

Obstacle strategy
```

A mismatch at any of these stages can produce the wrong avoidance direction even if the vision sensor itself detects the pillar correctly.

---

# 4.3 Vision Does Not Directly Control Steering

An important architectural distinction is:

```text
HUSKYLENS OUTPUT
       ≠
MOTOR COMMAND
```

The HuskyLens supplies perception information.

The EV3 makes the final motion decision.

The complete chain is:

```text
Pillar appears
     ↓
HuskyLens detects object
     ↓
Object ID obtained
     ↓
Nano communicates information
     ↓
EV3 receives obstacle state
     ↓
EV3 evaluates navigation conditions
     ↓
Final steering / drive command
```

Therefore, the camera does not directly command:

```text
LEFT STEERING
```

or:

```text
RIGHT STEERING
```

without the EV3 interpreting the complete navigation state.

---

# 4.4 Why the Arduino Nano Is Used

The Arduino Nano acts as a supporting interface in the vision architecture.

The current responsibility separation is:

```text
HUSKYLENS
   ↓
Visual perception


ARDUINO NANO
   ↓
Vision communication support


LEGO EV3
   ↓
Vehicle decision making
```

The Nano is not the primary Piolín controller.

It does not replace:

```text
EV3 motor control

EV3 wall navigation

EV3 course-state logic
```

The main controller remains the LEGO EV3.

---

# 4.5 Confirmed Communication Path

The confirmed communication path is:

```text
HuskyLens
    ↓
Arduino Nano
    ↓
USB
    ↓
LEGO EV3
```

The Nano-to-EV3 USB connection is part of the current architecture.

This document deliberately does **not** claim a specific electrical protocol between:

```text
HuskyLens
```

and:

```text
Arduino Nano
```

because that connection should only be documented once verified from the current physical wiring or current Nano code.

This distinction prevents an assumed protocol from becoming a false reproducibility instruction.

---

# 4.6 Perception vs. Control

Piolín separates perception from control.

### Perception

```text
"What object do I see?"
```

is handled by:

```text
HuskyLens
```

### Navigation decision

```text
"What should the vehicle do?"
```

is handled by:

```text
LEGO EV3
```

### Physical execution

```text
"How does the robot move?"
```

is handled by:

```text
Motor A + Motor B
```

The resulting hierarchy is:

```text
PERCEPTION
     ↓
DECISION
     ↓
ACTUATION
```

This makes the vision system easier to integrate with ultrasonic safety constraints.

---

# 4.7 What the HuskyLens Provides

The useful output from the vision subsystem is obstacle information associated with a learned identifier.

Conceptually:

```text
Visible object
      ↓
HuskyLens processing
      ↓
Recognized target
      ↓
ID
```

Piolín can then interpret the ID.

For example:

```text
ID = 1
```

means:

```text
GREEN pillar
```

while:

```text
ID = 2
```

means:

```text
RED pillar
```

The exact low-level data packet format should be documented from the current Nano/EV3 implementation rather than assumed here.

---

# 4.8 Object Identity vs. Vehicle Position

The HuskyLens answers primarily:

```text
WHAT target is visible?
```

It does not by itself provide the complete geometric state of Piolín relative to the course.

For example:

```text
GREEN detected
```

does not automatically tell the EV3:

```text
Exact distance to left wall

Exact vehicle heading

Exact steering angle required

Exact safe recovery path
```

Those decisions require additional vehicle and sensor context.

---

# 4.9 Vision and Ultrasonics Are Complementary

The vision and ultrasonic subsystems provide different information.

| System | Main Question |
| :--- | :--- |
| **HuskyLens** | What obstacle is present? |
| **S2 / S3 Ultrasonics** | Where are the lateral walls? |
| **S1 Ultrasonic** | Is forward clearance becoming unsafe? |
| **S4 Color Sensor** | What course event is occurring? |

The complete perception architecture therefore becomes:

```text
VISION
   ↓
Obstacle identity


ULTRASONICS
   ↓
Spatial constraints


COLOR
   ↓
Course state
```

These inputs are combined by the EV3.

---

# 4.10 Why Vision Alone Is Not Enough

Suppose the HuskyLens correctly identifies:

```text
GREEN
```

and therefore the desired requirement is:

```text
Pass on LEFT
```

The camera alone does not know whether the vehicle is already very close to the left track boundary.

Therefore:

```text
GREEN
   ↓
LEFT requested
```

must still be considered together with:

```text
LEFT WALL DISTANCE
```

The complete problem is:

```text
Desired passing side
        +
Available physical space
        ↓
Safe vehicle trajectory
```

This is why obstacle avoidance is a sensor-fusion problem rather than only a camera-classification problem.

---

# 4.11 Forward Camera Mounting

The HuskyLens is mounted toward the front of Piolín.

Conceptually:

```text
              CAMERA FIELD
               \         /
                \       /
                 \     /
                  \   /
               HuskyLens
                   │
              [ PIOLÍN ]
```

The forward location allows the robot to observe upcoming pillars before reaching them.

The camera mount is therefore part of the perception system.

---

# 4.12 HuskyLens Physical Evidence

<div align="center">
  <img
    src="https://github.com/user-attachments/assets/082c8e25-74b9-4d74-9c0c-cd44624037f8"
    alt="HuskyLens installed on Piolín"
    style="max-width: 80%; height: auto;"
  />
  <br>
  <sub><b>Figure 4.1.</b> HuskyLens integrated into the current Piolín vision system.</sub>
</div>

The physical installation determines:

```text
Camera height

Camera orientation

Visible forward region

Possible chassis occlusion

When pillars enter the image
```

The camera mount should therefore remain mechanically stable during operation.

---

# 4.13 Field of View

A camera only observes objects that fall within its field of view.

Conceptually:

```text
                 visible region
                \             /
                 \           /
                  \         /
                   \       /
                    CAMERA
                      │
                   PIOLÍN
```

A pillar outside this region can exist physically without being available to the vision algorithm.

Therefore:

```text
PILLAR EXISTS
```

does not automatically imply:

```text
PILLAR IS VISIBLE
```

This is one of the most important limitations of camera-based obstacle sensing.

---

# 4.14 Horizontal Field-of-View Limitation

During a curve, Piolín's chassis rotates.

Because the camera is rigidly attached to the chassis:

```text
Vehicle rotates
      ↓
Camera rotates
      ↓
Field of view rotates
```

A pillar that was previously ahead may move rapidly toward the edge of the image.

Similarly, a new pillar may remain outside the camera's field of view until Piolín has rotated far enough.

This creates a direct relationship between:

```text
Steering

Vehicle heading

Camera visibility
```

---

# 4.15 Camera Visibility Is Dynamic

The visible region changes continuously while Piolín moves.

Conceptually:

```text
TIME 1

       PILLAR

       \     /
        \   /
        CAMERA


TIME 2

PILLAR

              \     /
               \   /
               CAMERA
```

Even if the pillar itself does not move, its image position changes because the vehicle changes position and heading.

This makes camera perception inherently linked to mobility.

---

# 4.16 Detection Timing

The moment a pillar becomes visible is important because the robot still requires time and distance to react.

The full sequence is:

```text
Pillar enters field of view
        ↓
HuskyLens detects target
        ↓
Vision information communicated
        ↓
EV3 interprets target
        ↓
Motor B changes
        ↓
Vehicle trajectory changes
```

Therefore:

```text
DETECTION POINT
      ≠
PHYSICAL AVOIDANCE POINT
```

Piolín travels some distance during this process.

---

# 4.17 Vehicle Speed and Vision Reaction

At higher speed:

```text
Distance closes faster
```

which means:

```text
Less time between detection
and reaching the pillar
```

At lower speed:

```text
More reaction time
```

is available for:

```text
Detection

Communication

Steering response

Physical lateral displacement
```

Therefore, vision performance cannot be evaluated independently from drive speed.

---

# 4.18 Detection Distance Is Not Constant

The distance at which a pillar becomes reliably detectable can vary because of:

```text
Camera orientation

Pillar position

Lighting

Object size in image

Partial occlusion

Vehicle heading
```

Therefore, the architecture should not assume that every pillar will first be identified at one identical physical distance.

A robust avoidance strategy should tolerate some variation in the moment of initial detection.

---

# 4.19 Object Size in the Image

As Piolín approaches a pillar:

```text
Physical distance decreases
        ↓
Apparent image size generally increases
```

Conceptually:

```text
FAR

   [■]


NEAR

 [██████]
```

This means image information may change significantly during the approach.

However, apparent image size is influenced by camera geometry and should not automatically be interpreted as exact metric distance unless a dedicated calibrated model is used.

---

# 4.20 Image Position

A detected object can also have a horizontal image position.

Conceptually:

```text
LEFT SIDE          CENTER          RIGHT SIDE

0 ---------------------------------------- X_MAX
```

A pillar moving across this coordinate does not necessarily mean the pillar itself moved.

It may be caused by:

```text
Vehicle translation

Vehicle rotation

Steering

Approach geometry
```

Therefore:

```text
IMAGE X POSITION
       ≠
DIRECT PHYSICAL LATERAL POSITION
```

without additional calibration and geometry.

---

# 4.21 Why Image Coordinates Are Not Steering Angles

Suppose a pillar appears far to one side of the image.

This does not mean:

```text
Steering angle =
same numerical image offset
```

The actual chain is:

```text
Image position
      ↓
Navigation interpretation
      ↓
Desired vehicle behavior
      ↓
Motor B command
      ↓
Mechanical steering linkage
      ↓
Physical wheel angles
```

There are several transformations between image coordinates and actual wheel geometry.

---

# 4.22 Learned IDs

The HuskyLens system allows detected targets to be associated with learned identifiers.

Piolín uses these identifiers as a compact interface between vision and navigation.

```text
VISUAL APPEARANCE
       ↓
LEARNED TARGET
       ↓
ID
       ↓
EV3 MEANING
```

Current mapping:

```text
1 → GREEN

2 → RED
```

The EV3 therefore does not need to reproduce the complete image-classification process itself.

---

# 4.23 ID Mapping Must Be Deterministic

The navigation code must know exactly what each ID means.

For example:

```python
if pillar_id == 1:
    obstacle = GREEN

elif pillar_id == 2:
    obstacle = RED
```

Then:

```python
if obstacle == GREEN:
    required_side = LEFT

elif obstacle == RED:
    required_side = RIGHT
```

The exact variable names may differ in the current source code.

The important architecture is that:

```text
ID
  ↓
Known obstacle class
  ↓
Known passing requirement
```

---

# 4.24 Unknown ID Handling

The vision system may theoretically receive information that does not correspond to one of the expected obstacle IDs.

The safe architectural concept is:

```text
Known ID?
   │
 ┌─┴─┐
YES  NO
 │    │
 ▼    ▼
Use   Do not invent
known behavior
```

The software should not arbitrarily interpret an unknown identifier as green or red.

Exact fallback behavior belongs to the final obstacle software.

---

# 4.25 No Detection State

Another important state is:

```text
NO VALID PILLAR DETECTED
```

This should be distinct from:

```text
GREEN
```

and:

```text
RED
```

Conceptually:

```text
VISION STATE
   │
   ├── NONE
   ├── GREEN
   └── RED
```

This allows the EV3 to distinguish ordinary navigation from an active obstacle response.

---

# 4.26 Detection Persistence

One camera frame or reading should not necessarily determine the complete obstacle maneuver if the environment is uncertain.

A conceptual confirmation process can be:

```text
Possible ID
    ↓
Read again
    ↓
Same valid ID?
    ↓
Confirmed obstacle
```

However, excessive confirmation can also delay the response.

The current number of readings or confirmations should come from the active competition implementation rather than being invented here.

---

# 4.27 Confirmation Trade-Off

The vision system must balance:

```text
FAST REACTION
```

against:

```text
ROBUST CLASSIFICATION
```

More confirmation can provide:

```text
Reduced sensitivity to one abnormal reading
```

but can also produce:

```text
Later avoidance initiation
```

This relationship becomes especially important when the robot moves quickly toward a pillar.

---

# 4.28 Obstacle State

Once a valid obstacle is accepted, the EV3 can create a logical state such as:

```text
PILLAR_GREEN
```

or:

```text
PILLAR_RED
```

The navigation architecture then converts this state into an intended passing direction.

```text
PILLAR_GREEN
      ↓
LEFT PASS


PILLAR_RED
      ↓
RIGHT PASS
```

This keeps classification separate from physical steering behavior.

---

# 4.29 Passing Side vs. Steering Direction

The phrase:

```text
PASS ON LEFT
```

should not be interpreted as:

```text
Hold maximum left steering
until pillar disappears
```

Passing a pillar is a complete trajectory.

Conceptually:

```text
Normal path
      ↓
Move toward required passing side
      ↓
Create clearance
      ↓
Pass pillar
      ↓
Recover
      ↓
Return to normal navigation
```

Therefore:

```text
PASSING SIDE
      ≠
ONE FIXED STEERING ANGLE
```

---

# 4.30 Green Pillar Trajectory

For the current mapping:

```text
GREEN
ID 1
   ↓
PASS LEFT
```

The vision system supplies the requirement.

The EV3 must then consider:

```text
Current left-wall distance

Current right-wall distance

Current vehicle trajectory

Current forward clearance
```

before producing the final steering behavior.

The full green obstacle process is therefore:

```text
GREEN ID
     ↓
LEFT passing requirement
     ↓
Wall constraints
     ↓
EV3 control
     ↓
Physical left-side bypass
```

---

# 4.31 Red Pillar Trajectory

For:

```text
RED
ID 2
  ↓
PASS RIGHT
```

the same architecture applies in the opposite required passing direction.

```text
RED ID
    ↓
RIGHT passing requirement
    ↓
Wall constraints
    ↓
EV3 control
    ↓
Physical right-side bypass
```

The two maneuvers should use the same basic control architecture while respecting the different side requirement.

---

# 4.32 Vision Priority

Vision is important during obstacle avoidance, but it should not blindly override all other sensing.

A system-level priority concept is:

```text
FRONTAL COLLISION SAFETY
          ↓
LATERAL WALL SAFETY
          ↓
OBSTACLE / CORNER RESPONSE
          ↓
NORMAL WALL FOLLOWING
```

This means the camera can strongly influence the intended trajectory while the EV3 still protects the robot from surrounding boundaries.

---

# 4.33 Why Obstacle Steering Needs Wall Constraints

Consider:

```text
GREEN detected
      ↓
Pass left
```

but:

```text
Left wall already close
```

An unconstrained camera steering command could move Piolín into the wall.

Therefore:

```text
Vision request
      +
Left clearance
      +
Right clearance
      ↓
Constrained maneuver
```

This is a key principle of Piolín's obstacle strategy.

---

# 4.34 Vision and Front Safety

The S1 front ultrasonic remains available even when the HuskyLens sees a pillar.

These sensors answer different questions.

```text
HuskyLens
      ↓
Which obstacle is it?
```

while:

```text
S1
 ↓
How limited is forward clearance?
```

The front sensor can therefore provide a separate safety condition while vision controls the obstacle classification.

---

# 4.35 Camera Detection Loss

Eventually, a pillar can leave the HuskyLens field of view.

This may happen because:

```text
Piolín passes beside it

Piolín rotates

Pillar moves outside image boundary

Vehicle geometry occludes it
```

The loss of visual detection is an important state transition.

However:

```text
Pillar not visible
```

does not necessarily mean:

```text
Piolín is already safely recovered
```

The robot may still be laterally displaced.

---

# 4.36 Detection Loss vs. Maneuver Completion

These two events should be distinguished.

### Vision event

```text
Target no longer visible
```

### Vehicle event

```text
Robot has recovered a useful trajectory
```

They are not equivalent.

The sequence can be:

```text
Pillar disappears from camera
        ↓
Avoidance dominance reduced
        ↓
Ultrasonic geometry evaluated
        ↓
Recovery steering
        ↓
Normal wall following restored
```

This prevents the robot from remaining on the obstacle-avoidance trajectory after the pillar has been passed.

---

# 4.37 Post-Pillar Recovery

After an obstacle, the lateral ultrasonic sensors become the main recovery reference.

The robot may be:

```text
Closer to one wall

Angled relative to corridor

Still carrying lateral trajectory
```

The recovery architecture is:

```text
Vision target cleared
      ↓
S2 / S3 geometry evaluated
      ↓
Recovery steering
      ↓
Vehicle trajectory stabilizes
      ↓
Normal navigation
```

This demonstrates the handoff between:

```text
VISION-DRIVEN AVOIDANCE
```

and:

```text
ULTRASONIC-DRIVEN RECOVERY
```

---

# 4.38 Vision Handoff

A useful system model is:

```text
NORMAL NAVIGATION
        ↓
PILLAR DETECTED
        ↓
VISION BECOMES IMPORTANT
        ↓
AVOIDANCE
        ↓
PILLAR CLEARED
        ↓
VISION IMPORTANCE DECREASES
        ↓
WALL GEOMETRY RECOVERY
        ↓
NORMAL NAVIGATION
```

This prevents one control mode from dominating after its purpose has ended.

---

# 4.39 Vision and Cornering

Pillars may become visible near regions where the robot is also changing orientation for a corner.

This creates overlapping demands:

```text
CORNER LOGIC
      +
PILLAR LOGIC
```

The EV3 must avoid treating these as two completely independent steering controllers.

The vehicle has only one physical steering actuator:

```text
Motor B
```

Therefore:

```text
Multiple inputs
      ↓
One final steering objective
```

must be produced.

---

# 4.40 Why Camera Commands Can Conflict With Wall Following

Normal wall following may request:

```text
Small correction RIGHT
```

while the pillar requires:

```text
Strong movement LEFT
```

If both are independently applied:

```text
Control conflict
     ↓
Oscillation
or
weak obstacle reaction
```

A better architecture is:

```text
Obstacle requirement
       +
Wall correction
       ↓
Single combined / prioritized command
```

The exact blending method belongs to the current obstacle software.

---

# 4.41 Vision Authority Should Be Temporary

The obstacle system should strongly influence steering only while the obstacle maneuver is relevant.

Conceptually:

```text
No pillar
   ↓
Normal navigation authority


Pillar detected
   ↓
Obstacle authority increases


Pillar cleared
   ↓
Obstacle authority decreases


Recovered
   ↓
Normal navigation restored
```

This reduces the risk of steering remaining locked in the previous obstacle direction.

---

# 4.42 Why Fixed Steering Lock Is Risky

If the program simply does:

```text
GREEN detected
      ↓
STEER LEFT
```

and keeps that steering unchanged too long:

```text
Pillar may already be passed
        ↓
Robot continues curving
        ↓
Wall collision risk increases
```

Therefore obstacle control should respond to the changing physical situation rather than storing one permanent steering direction after detection.

---

# 4.43 Camera State Should Be Updated Continuously

During the active vision period:

```text
Pillar position changes

Object size changes

Visibility changes

Wall distances change
```

The EV3 should therefore interpret the current obstacle state as dynamic information.

The complete feedback process is:

```text
Vision observation
      ↓
EV3 response
      ↓
Vehicle moves
      ↓
New camera geometry
      ↓
New observation
```

This is another closed perception-control loop.

---

# 4.44 Camera Mount Stability

The camera's orientation is part of the calibration.

If the mount shifts:

```text
Camera points differently
       ↓
Field of view changes
       ↓
Pillar appears at different image location
       ↓
Detection timing changes
```

Therefore, vision debugging should not begin only with code.

The physical HuskyLens mounting should also be inspected.

---

# 4.45 Camera Height

Camera height influences the scene observed by the HuskyLens.

Different heights can change:

```text
Visible floor area

Apparent pillar position

Possible chassis obstruction

Relationship between pillar and background
```

No final numerical HuskyLens mounting height is claimed here because a confirmed current value has not been established in the project documentation.

---

# 4.46 Camera Angle

Similarly, camera pitch and horizontal orientation affect:

```text
How soon the pillar appears

Where it appears in the image

How long it remains visible
```

Therefore, the physical camera orientation should remain stable between calibration and competition runs.

No unconfirmed numerical camera angle is assigned here.

---

# 4.47 Camera Placement Trade-Off

Moving the camera forward or changing its orientation can improve one aspect of visibility while reducing another.

For example:

```text
Wider useful forward visibility
```

may improve early detection.

However, placement must also respect:

```text
Chassis clearance

Structural stability

Competition dimensions

Cable routing

Mechanical protection
```

The selected camera mounting is therefore part of the complete robot architecture.

---

# 4.48 Field-of-View Blind Regions

Any forward-facing camera can have regions that are temporarily difficult to observe.

Conceptually:

```text
       VISIBLE
      \       /
       \     /
        \   /
       CAMERA

 [possible side blind regions]
```

These regions are particularly relevant immediately after:

```text
Sharp corners

Large avoidance turns

Strong recovery corrections
```

when the robot's heading may temporarily point away from the next pillar.

This is one reason wall navigation should remain functional even when vision temporarily has no valid target.

---

# 4.49 Vision Failure Should Not Destroy Base Navigation

If no valid pillar is detected:

```text
NO VISION TARGET
```

the robot should still retain its base environmental sensing:

```text
S1
S2
S3
S4
```

Conceptually:

```text
No pillar information
        ↓
No obstacle classification
        ↓
Normal wall / course logic
remains available
```

This modularity prevents the entire vehicle architecture from depending on continuous camera detection.

---

# 4.50 Open Challenge Architecture

The HuskyLens is not required for ordinary wall-following navigation in the Open Challenge.

The base Open configuration is:

```text
S1
↓
Front safety


S2 + S3
↓
Wall geometry


S4
↓
Course state


EV3
↓
Vehicle control
```

The robot therefore maintains a complete non-vision navigation architecture for the Open round.

---

# 4.51 Obstacle Challenge Architecture

The Obstacle Challenge adds the vision path:

```text
                         ENVIRONMENT
                              │
       ┌──────────────┬───────┼────────┬─────────────┐
       ▼              ▼                ▼             ▼
    SIDE WALLS      FRONT            FLOOR         PILLAR
       │              │                │             │
       ▼              ▼                ▼             ▼
     S2/S3            S1               S4        HuskyLens
       │              │                │             │
       │              │                │       Arduino Nano
       │              │                │             │
       └──────────────┴───────┬────────┴─────────────┘
                              ▼
                           LEGO EV3
                              │
                              ▼
                      NAVIGATION DECISION
                              │
                      ┌───────┴───────┐
                      ▼               ▼
                   Motor A         Motor B
```

Vision therefore extends the base architecture rather than replacing it.

---

# 4.52 Vision Data Validation

Before an obstacle ID affects navigation, the software should distinguish:

```text
Valid known target
```

from:

```text
No detection

Unknown ID

Unusable / incomplete information
```

Conceptually:

```text
Vision data received
      ↓
Known ID?
 ┌────┴────┐
YES        NO
 │          │
 ▼          ▼
Interpret   Do not invent
obstacle    obstacle class
```

The exact validation conditions should correspond to the active Nano/EV3 software.

---

# 4.53 Data Logging

Useful obstacle diagnostics can include:

```text
PILLAR_ID

VISION_STATE

D_FRONT

D_LEFT

D_RIGHT

CURRENT_STEERING

CURRENT_DRIVE_COMMAND

NAVIGATION_STATE
```

A conceptual diagnostic line could be:

```text
ID=1
VISION=GREEN
L=...
R=...
F=...
STATE=AVOID
STEER=...
```

Actual measurements should come from current robot testing.

Logging sensor and control values together makes it easier to determine whether a failed maneuver originated from:

```text
Detection

Communication

Interpretation

Wall constraint

Steering response
```

---

# 4.54 Vision Failure Diagnosis

If Piolín reacts incorrectly to a pillar, the debugging process should follow the entire information chain.

```text
1. Is the pillar visible to HuskyLens?
        ↓
2. Is the correct ID detected?
        ↓
3. Is the Nano receiving vision information?
        ↓
4. Is the EV3 receiving the expected data?
        ↓
5. Is the ID mapped correctly?
        ↓
6. Is the required passing side correct?
        ↓
7. Are wall constraints modifying the command?
        ↓
8. Is Motor B physically responding?
```

This prevents immediately changing steering values when the original problem may be vision communication or ID mapping.

---

# 4.55 Incorrect Color Direction Failure

A particularly important failure mode is:

```text
Object correctly detected
      ↓
Wrong ID interpretation
      ↓
Wrong passing side
```

For example:

```text
GREEN physically present
      ↓
Software interprets as RED
      ↓
Robot attempts wrong side
```

Therefore, testing should separately verify:

```text
Green identification

Red identification

Green action

Red action
```

rather than treating obstacle avoidance as one indivisible test.

---

# 4.56 Detection vs. Avoidance

These are two separate engineering questions.

### Detection test

```text
Does HuskyLens correctly identify the pillar?
```

### Avoidance test

```text
Can Piolín physically pass the pillar correctly?
```

A failed avoidance does not automatically prove the camera failed.

For example:

```text
Correct GREEN detection
        ↓
Correct LEFT requirement
        ↓
Steering too weak
        ↓
Collision
```

In that case:

```text
Vision succeeded

Mobility failed
```

This distinction is essential for meaningful testing.

---

# 4.57 Vision Test Matrix

A useful current test table is:

| Trial | Physical Pillar | Reported ID | Classification Correct? | Required Side | Vehicle Result |
| :---: | :--- | :---: | :---: | :--- | :--- |
| 1 | Green |  |  | Left |  |
| 2 | Green |  |  | Left |  |
| 3 | Red |  |  | Right |  |
| 4 | Red |  |  | Right |  |

Only actual current results should be inserted.

This separates perception performance from vehicle-control performance.

---

# 4.58 Lighting Conditions

Vision performance can depend on the visual environment.

Possible influences include:

```text
Overhead lighting

Shadows

Reflections

Background contrast

Pillar orientation
```

Therefore, HuskyLens validation should include conditions representative of the competition environment.

No current numerical error rate or lux benchmark is claimed here unless supported by real current measurements.

Historical vision benchmarks belong only in:

[Legacy Performance Testing and Analysis](../legacy/03_PTesting&Analysis.md)

---

# 4.59 Why Legacy PixyCam Results Do Not Apply

Piolín previously experimented with PixyCam.

That architecture is not the current vision system.

Therefore:

```text
PixyCam detection result
      ≠
Current HuskyLens performance
```

and:

```text
PixyCam calibration
      ≠
Current HuskyLens calibration
```

Historical Pixy documentation is preserved in:

[Legacy PixyCam Vision System](../legacy/02_CameraPixy.md)

The current system should be evaluated independently.

---

# 4.60 Current vs. Legacy Vision

| Feature | Legacy | Current |
| :--- | :--- | :--- |
| **Primary camera** | PixyCam | HuskyLens |
| **Vehicle controller** | Multiple historical concepts | LEGO EV3 |
| **Vision support controller** | Historical arrangements | Arduino Nano |
| **Nano → EV3** | Not applicable to all legacy stages | USB |
| **Current green ID** | Not applicable | ID 1 |
| **Current red ID** | Not applicable | ID 2 |
| **Gyroscope requirement** | Present in some legacy architectures | None |
| **Main wall navigation** | Historical variations | S2 + S3 Ultrasonics |

This separation prevents legacy architecture from appearing to be part of the current robot.

---

# 4.61 Vision Calibration Philosophy

The HuskyLens should be calibrated and validated as part of the **installed robot**, not only as an isolated camera.

The useful perception system includes:

```text
HuskyLens

Physical mount

Camera orientation

Vehicle height

Lighting environment

Target appearance

Nano communication

EV3 interpretation
```

Changing one of these variables can affect the complete vision behavior.

This is why final calibration should be performed on the current Piolín configuration.

---

# 4.62 Mechanical and Vision Calibration Are Connected

For example:

```text
Camera mount moves
       ↓
Visual geometry changes
       ↓
Detection timing changes
       ↓
Avoidance starts at different position
```

The software thresholds may remain identical while the physical result changes.

Therefore:

```text
VISION CALIBRATION
      depends partly on
MECHANICAL CALIBRATION
```

This interaction is documented further in:

[Sensor Calibration](05_Calibration.md)

---

# 4.63 Vision and Vehicle Speed Calibration

The selected drive speed affects the usable vision reaction margin.

Therefore obstacle calibration should consider:

```text
Detection timing

Vehicle speed

Steering response

Available bypass distance
```

A configuration that works at one propulsion speed may become too late at a significantly higher speed.

This does not necessarily indicate worse vision classification.

It may indicate that the complete control system no longer has enough physical response distance.

---

# 4.64 Vision and Steering Strength

Similarly:

```text
Correct detection
```

does not guarantee:

```text
Sufficient lateral movement
```

If steering is too weak:

```text
Pillar detected early
      ↓
Correct passing direction chosen
      ↓
Vehicle does not move laterally enough
      ↓
Collision
```

The perception and mobility systems must therefore be tuned together while remaining diagnostically separate.

---

# 4.65 Vision and Over-Steering

The opposite failure is also possible.

```text
Pillar detected
      ↓
Correct direction
      ↓
Steering too aggressive
      ↓
Pillar cleared
      ↓
Robot approaches side wall
```

This produces:

```text
Successful obstacle classification
```

but:

```text
Poor vehicle trajectory
```

The lateral ultrasonic safety layer helps constrain this behavior.

---

# 4.66 Post-Pillar Centering

After avoidance, Piolín should recover toward a useful track-relative trajectory.

This is not primarily a HuskyLens task.

Once the pillar has been passed:

```text
Camera role decreases
```

and:

```text
Lateral wall geometry
```

becomes more important.

The handoff is:

```text
HuskyLens
      ↓
Select obstacle response


Ultrasonics
      ↓
Recover track position
```

This division prevents the camera from attempting to solve a problem better measured by the lateral distance sensors.

---

# 4.67 Sensor-Fusion Example

A conceptual obstacle state can contain:

```text
PILLAR_ID = 1

D_LEFT = ...

D_RIGHT = ...

D_FRONT = ...
```

The EV3 interprets:

```text
ID 1
   ↓
Need left-side pass
```

then asks:

```text
How much left clearance exists?

Is frontal clearance safe?

What is current wall geometry?
```

Only after considering these questions does the robot produce a final motion command.

This is the practical meaning of sensor fusion in Piolín.

---

# 4.68 Vision Responsibility Matrix

| Information / Action | Responsible System |
| :--- | :--- |
| **Observe forward scene** | HuskyLens |
| **Identify trained pillar** | HuskyLens |
| **Represent green pillar** | ID 1 |
| **Represent red pillar** | ID 2 |
| **Support communication** | Arduino Nano |
| **Nano → EV3 communication** | USB |
| **Interpret pillar ID** | EV3 |
| **Choose navigation response** | EV3 |
| **Check lateral clearance** | S2 / S3 |
| **Check frontal safety** | S1 |
| **Execute steering** | Motor B |
| **Provide propulsion** | Motor A |
| **Recover after obstacle** | EV3 + lateral ultrasonics |

This table shows that obstacle avoidance is distributed across several subsystems.

---

# 4.69 Confirmed Current Vision Information

The following information is confirmed for the current Piolín architecture:

| Parameter | Current Value |
| :--- | :--- |
| **Primary vision sensor** | HuskyLens |
| **Supporting controller** | Arduino Nano |
| **Nano → EV3** | USB |
| **Main vehicle controller** | LEGO EV3 |
| **Camera orientation** | Forward-facing |
| **Green pillar ID** | 1 |
| **Red pillar ID** | 2 |
| **Green required side** | Left |
| **Red required side** | Right |
| **PixyCam** | Legacy / not installed |
| **Gyroscope** | Not installed |
| **Raspberry Pi** | Not part of final system |

The following are intentionally not claimed here as final numerical or electrical specifications:

```text
HuskyLens-to-Nano protocol

Camera mounting height

Camera mounting angle

Exact field-of-view angle

Exact detection distance

Exact confirmation count

Exact frame rate

Exact image dimensions used by code

Exact vision latency

Current detection error percentage

Exact obstacle steering angle
```

These should only be added when verified from the final hardware, source code, or current testing.

---

# 4.70 Complete Vision Pipeline

The current Piolín vision pipeline can be summarized as:

```text
                      PILLAR
                        │
                        ▼
                    HuskyLens
                        │
                        ▼
                 TARGET / ID DATA
                        │
                        ▼
                  Arduino Nano
                        │
                       USB
                        │
                        ▼
                    LEGO EV3
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
         ID VALIDATION       SENSOR CONTEXT
              │                   │
              │             ┌─────┼─────┐
              │             ▼     ▼     ▼
              │            S1    S2    S3
              │             │     │     │
              └─────────────┴──┬──┴─────┘
                               ▼
                       NAVIGATION DECISION
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
                 Motor A               Motor B
                    │                     │
                    └──────────┬──────────┘
                               ▼
                      VEHICLE TRAJECTORY
                               │
                               ▼
                       NEW CAMERA VIEW
```

This forms a closed perception-control loop.

---

# 4.71 Obstacle State Pipeline

At the logical level:

```text
NO TARGET
   ↓
Normal navigation
```

then:

```text
VALID ID 1
   ↓
GREEN
   ↓
LEFT passing requirement
```

or:

```text
VALID ID 2
   ↓
RED
   ↓
RIGHT passing requirement
```

then:

```text
Pillar cleared
   ↓
Vision influence reduced
   ↓
Ultrasonic recovery
   ↓
Normal navigation
```

This state transition is more useful than treating the camera as a permanent steering controller.

---

# 4.72 Engineering Significance

The HuskyLens system gives Piolín information that the ultrasonic sensors cannot provide.

An ultrasonic sensor can report:

```text
There is an object / surface at a distance
```

but cannot inherently determine:

```text
This is the GREEN pillar
```

or:

```text
This is the RED pillar
```

The HuskyLens adds the missing semantic information:

```text
GEOMETRY
      +
IDENTITY
      ↓
CORRECT OBSTACLE STRATEGY
```

This is the primary reason the camera is valuable in the Obstacle Challenge.

---

# 4.73 Why the Final Architecture Uses Multiple Sensor Types

No single Piolín sensor provides every piece of information required for autonomous navigation.

```text
S1
↓
Forward safety


S2 + S3
↓
Lateral geometry


S4
↓
Course state


HuskyLens
↓
Pillar identity
```

The EV3 combines these independent observations.

The architecture therefore follows:

```text
SPECIALIZED SENSORS
        ↓
CENTRALIZED DECISION
        ↓
COORDINATED ACTUATION
```

rather than asking one camera to solve every navigation problem.

---

# 4.74 Final HuskyLens Architecture

Piolín's current obstacle vision system can be summarized as:

```text
                    VISUAL ENVIRONMENT
                           │
                           ▼
                       HuskyLens
                           │
               ┌───────────┴───────────┐
               ▼                       ▼
            ID = 1                  ID = 2
               │                       │
               ▼                       ▼
             GREEN                    RED
               │                       │
               ▼                       ▼
          PASS LEFT               PASS RIGHT
               │                       │
               └───────────┬───────────┘
                           ▼
                     Arduino Nano
                           │
                          USB
                           │
                           ▼
                       LEGO EV3
                           │
                ┌──────────┼──────────┐
                ▼          ▼          ▼
               S1        S2/S3       STATE
                │          │          │
                ▼          ▼          ▼
             FRONT       WALLS     NAVIGATION
             SAFETY     GEOMETRY      LOGIC
                └──────────┼──────────┘
                           ▼
                    FINAL VEHICLE
                       RESPONSE
                           │
                ┌──────────┴──────────┐
                ▼                     ▼
             Motor A               Motor B
              Drive                Steering
```

The key architectural principle is:

```text
CAMERA
does not drive the robot
```

Instead:

```text
CAMERA
   ↓
IDENTITY


ULTRASONICS
   ↓
SPACE


EV3
   ↓
DECISION


MOTORS
   ↓
MOTION
```

The HuskyLens therefore acts as Piolín's **semantic obstacle sensor**.

It identifies whether the relevant obstacle is green or red, while the EV3 combines that information with wall geometry and vehicle state to create a physically achievable avoidance trajectory.

The resulting obstacle strategy is not:

```text
SEE COLOR
   ↓
TURN FIXED ANGLE
```

but rather:

```text
IDENTIFY PILLAR
      ↓
SELECT REQUIRED SIDE
      ↓
CHECK AVAILABLE GEOMETRY
      ↓
EXECUTE AVOIDANCE
      ↓
CLEAR PILLAR
      ↓
RECOVER WITH WALL SENSORS
      ↓
RETURN TO NORMAL NAVIGATION
```

This division of responsibilities is the foundation of Piolín's current vision-assisted obstacle architecture.

---

## Continue Reading

[Sensor Calibration](05_Calibration.md)

---

## Related Sensor Documentation

[Power and Sensor Configuration](01_PowerSensorconfig.md)

[Ultrasonic Sensor Data](02_USSensorD.md)

[Color Sensor](03_color_sensor.md)

[HuskyLens Hardware](../components/07_HuskyLens.md)

---

## Related Software Documentation

[Software Architecture](../software_obstacles_strategy/01_SWArchitecture.md)

[State Machine](../software_obstacles_strategy/02_statemachine.md)

[Obstacle Detection](../software_obstacles_strategy/05_obstacledetec.md)

[Obstacle Strategy](../software_obstacles_strategy/06_obstaclestrateg.md)

[Software Tuning](../software_obstacles_strategy/07_softwaretuning.md)

[HuskyLens Vision](../software_obstacles_strategy/08_CameraHLVision.md)

---

## Related Mechanical Documentation

[Chassis Design](../mobility_mechanical/02_chassis.md)

[Robot Mobility](../mobility_mechanical/03_RMobility.md)

[Steering](../mobility_mechanical/04_steering.md)

[Mechanical Testing](../mobility_mechanical/06_testing.md)

---

## Reproducibility

[Wiring](../reproducibility/03_wiring.md)

[Electrical Schematic](../reproducibility/04_elecschem.md)

[How to Calibrate](../reproducibility/06_HowToCalibrate.md)

[Testing Protocol](../reproducibility/07_TestingProtocol.md)

[Troubleshooting](../reproducibility/08_Troubleshooting.md)

---

## Historical Reference

[Legacy Documentation Notice](../legacy/00_LEGACY_NOTICE.md)

[Legacy PixyCam](../legacy/02_CameraPixy.md)

[Legacy Performance Testing](../legacy/03_PTesting&Analysis.md)
