# 8. Troubleshooting

<div align="center">

<img
  src="../../v-photos/v4/piolin_open_isometric.jpg"
  alt="Piolín autonomous vehicle used for troubleshooting and validation"
  width="740"
/>

<br>

<sub><b>Figure 8.1.</b> Troubleshooting Piolín requires diagnosing the complete mechatronic system rather than assuming every failure originates in software.</sub>

</div>

Troubleshooting Piolín follows a simple engineering rule:

> **Find the first layer that behaves incorrectly before changing the next one.**

Autonomous failures often appear at the end of a long chain.

For example:

```text
sensor mounted incorrectly
        ↓
distance measurement becomes wrong
        ↓
controller calculates wrong steering
        ↓
Piolín exits corner badly
        ↓
next straight begins incorrectly
        ↓
later collision occurs
```

The collision is the visible symptom, but it is not necessarily the original failure.

For this reason, PiolínTech diagnoses problems in the following order:

```text
MECHANICS
    ↓
WIRING
    ↓
RAW SENSOR DATA
    ↓
SOFTWARE INTERPRETATION
    ↓
NAVIGATION STATE
    ↓
MOTOR COMMAND
    ↓
PHYSICAL RESPONSE
```

The objective is to avoid compensating for a physical or sensing problem by adding increasingly complex software corrections.

---

## 8.1 First Diagnostic Rule

Before changing any control constant, answer these questions:

```text
Is the robot mechanically intact?

Is the correct round configuration installed?

Are the ports correct?

Do raw sensor values make sense?

Does the software interpret those values correctly?

Is the correct navigation state active?

Is the intended motor command being produced?

Does the physical robot respond to that command correctly?
```

If one answer is already wrong, stop there.

There is little value in tuning a controller if its input assumptions are incorrect.

The current fixed hardware conventions are:

```text
Motor A = propulsion

Motor B = steering

S2 = LEFT Ultrasonic

S3 = RIGHT Ultrasonic

S4 = Color Sensor
```

Only S1 changes:

```text
OPEN
S1 = Gyro
```

```text
OBSTACLES
S1 = Pixy2.1
```

The Gyro and Pixy2.1 are never part of the same active configuration.

---

# 8.2 Quick Troubleshooting Table

Use this table to decide where to begin.

| Symptom | First Area to Check |
| :--- | :--- |
| Robot does not move | Motor A / Port A / drivetrain |
| Robot drives backward unexpectedly | Motor A polarity / software command |
| Steering does not move | Motor B / Port B |
| Steering moves opposite direction | Steering sign / linkage orientation |
| Robot never drives straight | Steering center / gyro / wall control |
| Robot zig-zags | Controller strength, steering center, delay |
| Robot constantly goes toward one wall | S2/S3 mapping, correction sign |
| Open starts directly into wall | Initial acquisition / steering / sensor geometry |
| Blue selects wrong direction | Color-state mapping |
| Orange selects wrong direction | Color-state mapping |
| Direction changes during run | Direction state overwritten |
| One line counted twice | Color event lock / re-arm |
| Corner starts too late | Detection, speed, state logic |
| Corner rotates wrong direction | Gyro sign / steering sign |
| Corner completes but next straight is bad | Corner exit / geometry reacquisition |
| Pixy sees nothing | S1, communication, signatures, lighting |
| Red causes left pass | Signature mapping / obstacle rule |
| Green causes right pass | Signature mapping / obstacle rule |
| Pixy detects pillar but robot ignores it | Target relevance / state transition |
| Robot reacts to distant pillar | Relevance threshold too permissive |
| Robot switches pillars mid-pass | Target lock |
| Pillar disappears and steering reverses | Target-loss handling |
| Robot passes pillar but hits wall | Recovery / control arbitration |
| Pillar avoidance feels inverted after a corner | State or controller interaction |
| Parking triggers too early | Progress-state logic |
| Parking position varies | Approach geometry / encoder / steering center |
| Same code behaves differently after rebuild | Mechanical or sensor recalibration |

This table identifies the **first diagnostic area**, not necessarily the final cause.

---

# 8.3 Mechanical Problems First

<div align="center">

<img
  src="../../v-photos/v4/piolin_bottom.jpg"
  alt="Bottom view of Piolín showing drivetrain, steering and sensor integration"
  width="720"
/>

<br>

<sub><b>Figure 8.2.</b> Mechanical problems can change sensor readings and motor response even when the software is unchanged.</sub>

</div>

Before debugging software, inspect the physical vehicle.

### Steering

Check:

```text
Motor B securely mounted?

steering linkage connected?

front wheels approximately centered?

left and right movement free?

no part touching chassis?

no axle partially disconnected?
```

A mechanical steering problem often appears in software as:

```text
weak correction

different left/right response

corner inconsistency

failure to return to center
```

If Motor B is commanded correctly but the physical wheels do not move as expected, do not compensate with larger control gains.

Fix the mechanism first.

<div align="center">

<img
  src="../../v-photos/v4/ackermann_center.jpg"
  alt="Piolín steering mechanism at center"
  width="670"
/>

<br>

<sub><b>Figure 8.3.</b> Steering center should be mechanically repeatable before navigation tuning begins.</sub>

</div>

### Drivetrain

Inspect:

```text
rear wheels secure?

axles aligned?

Motor A mount secure?

no wheel rubbing?

drivetrain moving freely?
```

<div align="center">

<img
  src="../../v-photos/v4/rear_drivetrain_bottom.jpg"
  alt="Piolín rear drivetrain inspection"
  width="690"
/>

<br>

<sub><b>Figure 8.4.</b> Unexpected drivetrain resistance can change physical travel distance and invalidate previously working timing or encoder values.</sub>

</div>

If the drivetrain changed physically, previously calibrated:

```text
speed

encoder distance

reverse displacement

parking movement
```

may require verification.

---

# 8.4 Wiring and Port Errors

The next layer is electrical configuration.

The permanent mapping is:

```text
A  → Large Motor

B  → Medium Motor

S2 → LEFT Ultrasonic

S3 → RIGHT Ultrasonic

S4 → Color Sensor
```

The most common high-impact wiring mistake would be swapping S2 and S3.

<div align="center">

<img
  src="../../v-photos/v4/PiolinUSlabeling.png"
  alt="Piolín ultrasonic mapping showing S2 left and S3 right"
  width="700"
/>

<br>

<sub><b>Figure 8.5.</b> Permanent ultrasonic identity: S2 is LEFT and S3 is RIGHT.</sub>

</div>

If the software assumes:

```text
S2 = LEFT
```

but the physical robot has:

```text
S2 = RIGHT
```

then a correct wall correction can become physically inverted.

Always verify wiring before reversing steering polarity in software.

### Open wiring

<div align="center">

<img
  src="../../v-photos/v4/wiring_open.jpg"
  alt="Piolín Open Challenge wiring"
  width="720"
/>

<br>

<sub><b>Figure 8.6.</b> Open configuration requires the Gyro Sensor on S1.</sub>

</div>

```text
S1 = Gyro
```

### Obstacle wiring

<div align="center">

<img
  src="../../v-photos/v4/wiring_obstacle.jpg"
  alt="Piolín Obstacle Challenge wiring"
  width="720"
/>

<br>

<sub><b>Figure 8.7.</b> Obstacle configuration requires Pixy2.1 on S1.</sub>

</div>

```text
S1 = Pixy2.1
```

Running the wrong program with the wrong S1 device is a configuration failure, not a navigation failure.

---

# 8.5 Raw Sensor Diagnosis

Once hardware and wiring are correct, inspect raw sensor data before looking at steering behavior.

The diagnostic principle is:

```text
RAW SENSOR WRONG
→ fix sensing first
```

```text
RAW SENSOR RIGHT
+
BEHAVIOR WRONG
→ investigate interpretation / control
```

### Ultrasonics

Move Piolín physically closer to the left wall.

Expected:

```text
S2 changes accordingly
```

Move Piolín closer to the right wall.

Expected:

```text
S3 changes accordingly
```

If the wrong variable changes, the physical or software mapping is incorrect.

If the correct variable changes but steering reacts the wrong way, the problem is later in the control chain.

### Color Sensor

Test:

```text
normal floor

Blue

Orange
```

with the current casing installed.

<div align="center">

<img
  src="../../v-photos/v4/color_sensor_casing.jpg"
  alt="Piolín Color Sensor casing"
  width="640"
/>

<br>

<sub><b>Figure 8.8.</b> Color troubleshooting must use the same casing and physical installation used during calibration.</sub>

</div>

### Gyro

Rotate Piolín manually and observe:

```text
angle magnitude

angle sign

return toward original heading
```

### Pixy2.1

Place one known target ahead and inspect:

```text
signature

x

y

width

height
```

Do not begin by debugging obstacle steering if the camera itself reports the wrong target.

---

# 8.6 Open Challenge Troubleshooting

Open combines three main information sources:

```text
Gyro
→ heading

S2/S3
→ lateral geometry

S4
→ course progression
```

When a failure occurs, determine which information became incorrect first.

### Robot leaves start and immediately crashes

Check in this order:

```text
1. Steering center.

2. Motor B direction.

3. S2/S3 mapping.

4. Initial wall geometry.

5. Gyro zero.

6. Initial acquisition logic.
```

Do not immediately increase steering strength.

If Piolín begins from an outside position and drives directly toward the inner wall, the key question is:

```text
Did software understand where the robot started?
```

before asking:

```text
Was steering strong enough?
```

### Robot starts in a circle

Possible causes:

```text
Motor B not centered

steering center calibration wrong

gyro heading correction sign wrong

wall-control sign wrong

sensor mapping reversed
```

A constant circle usually suggests a persistent steering bias rather than random sensor noise.

---

## 8.7 Open Direction Problems

Current direction selection is:

```text
BLUE first
→ COUNTERCLOCKWISE
```

```text
ORANGE first
→ CLOCKWISE
```

If Blue produces clockwise behavior, inspect the direction mapping directly.

Do not swap S2 and S3 to compensate.

After direction is established:

```text
CCW
S2 = inner
S3 = outer
```

```text
CW
S3 = inner
S2 = outer
```

The physical ports never change.

If the first corner works but later corners suddenly appear mirrored, inspect whether the software has accidentally changed:

```text
direction

inner_sensor

outer_sensor

steering polarity
```

during a state transition.

Direction should normally be established once and remain persistent for the run.

---

# 8.8 Open Straight-Line Problems

A stable straight depends on both heading and lateral geometry.

If Piolín zig-zags:

```text
check steering center first
      ↓
check raw S2/S3 stability
      ↓
check gyro behavior
      ↓
then examine correction strength
```

Possible control causes include:

```text
correction too strong

correction applied too frequently

insufficient deadband

delayed response

gyro and wall correction fighting each other
```

The desired relationship is:

```text
Ultrasonic
→ lateral correction
```

```text
Gyro
→ heading correction
```

If the robot has correct heading but is consistently too close to one wall, changing gyro gains is unlikely to solve the underlying lateral error.

If lateral distance looks correct but the chassis is visibly rotated, wall control alone is not enough.

---

# 8.9 Open Corner Problems

Corner failures should be divided into:

```text
ENTRY

TURN

EXIT
```

### Entry failure

Symptoms:

```text
starts too late

starts too early

starts from wrong lateral position
```

Investigate:

```text
color event

geometry transition

vehicle speed

current course state
```

### Turn failure

Symptoms:

```text
rotates too much

rotates too little

turns wrong direction
```

Investigate:

```text
steering sign

gyro sign

steering strength

turn-release logic
```

### Exit failure

Symptoms:

```text
correct rotation but hits wall after turn

zig-zags after turn

does not return to normal straight control
```

Investigate:

```text
gyro release

steering return

S2/S3 reacquisition

state transition back to straight
```

A corner should not be debugged as one indivisible event.

The first incorrect stage is the important one.

---

# 8.10 Double-Counting Course Events

If Piolín physically crosses one marking but the software counts two:

```text
physical event = 1

software events > 1
```

the likely problem is not color classification itself.

Inspect:

```text
event lock

re-arm condition

cooldown

state transition
```

The desired logic is:

```text
neutral
  ↓
color detected
  ↓
count ONCE
  ↓
lock
  ↓
leave marking
  ↓
re-arm
```

If neutral floor is unreliable, the release condition may need to use another robust state transition rather than simply removing protection against duplicates.

---

# 8.11 Gyro Troubleshooting

<div align="center">

<img
  src="../../v-photos/v4/gyro_orientation.jpg"
  alt="Piolín Gyro Sensor orientation"
  width="650"
/>

<br>

<sub><b>Figure 8.9.</b> Gyro troubleshooting begins with physical orientation and sign verification before control gains are modified.</sub>

</div>

### Gyro starts with unexpected angle

Check:

```text
robot stationary during reset?

reset actually executed?

sensor orientation unchanged?
```

### Gyro sign seems reversed

Rotate Piolín manually.

If clockwise physical rotation produces the opposite sign from what the code expects, correct the interpretation centrally.

Do not compensate by reversing unrelated corner logic in multiple places.

### Gyro appears correct but robot oscillates

The problem may be:

```text
gain strength

derivative response

steering delay

mechanical center

wall correction interaction
```

A correct sensor can still be used incorrectly by the controller.

---

# 8.12 Pixy2.1 Troubleshooting

<div align="center">

<img
  src="../../v-photos/v4/pixy21_front.jpg"
  alt="Piolín Pixy2.1 vision sensor"
  width="680"
/>

<br>

<sub><b>Figure 8.10.</b> Pixy troubleshooting should distinguish communication, detection, target selection, and steering problems.</sub>

</div>

The current camera configuration uses:

```text
S1 = Pixy2.1
```

with:

```text
sig1 = Pink

sig2 = Red

sig3 = Green
```

The current Pixy2.1 also includes a **3D-printed casing**.

The casing is part of the calibrated installation, so camera behavior should be rechecked if:

```text
casing moves

camera moves inside casing

camera angle changes

front assembly changes
```

### Pixy sees nothing

Check:

```text
S1 connection

correct Obstacle software

I2C/SMBus communication

camera power/connection

signature training

lighting

target inside field of view
```

<div align="center">

<img
  src="../../v-photos/v4/pixy21_s1_connection.jpg"
  alt="Pixy2.1 S1 connection"
  width="660"
/>

<br>

<sub><b>Figure 8.11.</b> Verify the current direct S1 connection before changing vision parameters.</sub>

</div>

### Pixy detects wrong color

Check signature training first.

Expected:

```text
Red → sig2

Green → sig3

Pink → sig1
```

The software and camera training must agree.

---

# 8.13 Red/Green Passing Direction Is Wrong

This is one of the most important obstacle diagnostic rules.

The competition logic is fixed:

```text
RED
→ PASS RIGHT
```

```text
GREEN
→ PASS LEFT
```

This rule is based on the pillar color, not on where the pillar appears inside the image.

Therefore:

```text
Red appears left of image center
```

still means:

```text
PASS RIGHT
```

and:

```text
Green appears right of image center
```

still means:

```text
PASS LEFT
```

If Piolín does the opposite, inspect:

```text
1. Was the signature correct?

2. Was the target selected correctly?

3. Did the software map the signature to the correct side?

4. Did the intended steering command have the correct sign?

5. Did another controller override the command?
```

Do not reverse the complete steering system before identifying which stage is actually inverted.

---

# 8.14 When Pixy Detects Correctly but the Robot Goes the Wrong Way

This symptom is especially useful because it narrows the diagnosis.

Suppose debug output says:

```text
RED detected
PASS RIGHT requested
```

but Piolín physically goes left.

Then camera classification is probably not the first failure.

Investigate:

```text
steering-command sign

Motor B polarity

steering conversion

wall-control override

corner-control override

recovery state accidentally active
```

The chain is:

```text
RED
  ↓
RIGHT objective
  ↓
steering command
  ↓
Motor B
  ↓
physical wheel angle
```

Find the first stage where "right" becomes "left."

---

# 8.15 Controller Conflict During Obstacle Avoidance

A common obstacle failure is when Pixy requests one trajectory while normal wall control requests another.

For example:

```text
Pixy:
move right of Red
```

while:

```text
wall controller:
return toward center
```

If both are applied with similar authority:

```text
commands fight
      ↓
weak obstacle response
      ↓
zig-zag
      ↓
wrong passing side
```

The intended priority is state-dependent.

```text
NORMAL
→ geometry control dominant
```

```text
ACTIVE PILLAR
→ pillar objective dominant
→ wall safety still active
```

```text
PILLAR CLEARED
→ recovery regains authority
```

If pillar avoidance feels randomly weak or appears inverted even though the color rule is correct, inspect controller arbitration before reversing the Pixy rule.

---

# 8.16 Distant Pillars Affect Steering

If Piolín begins steering strongly toward a pillar that is still far away, target relevance may be too permissive.

Check:

```text
block size

image position

current state

target-selection condition
```

The desired relationship is:

```text
visible
≠
automatically dominant
```

A target should become strongly influential only when it is relevant to the current vehicle trajectory.

Very small or distant visual blocks may be useful for awareness without requiring immediate maximum steering.

---

# 8.17 Multiple Pillars and Wrong Target Selection

If Red and Green are visible simultaneously, the first block returned by Pixy should not automatically be considered the correct obstacle.

Investigate target-selection logic.

Useful evidence can include:

```text
signature

x

y

width

height

current maneuver state

previous target
```

Typical failure:

```text
near Red ahead

far Green visible

software chooses Green
      ↓
wrong avoidance trajectory
```

The problem is then:

```text
TARGET SELECTION
```

not:

```text
COLOR RULE
```

These are separate layers and should remain separate in troubleshooting.

---

# 8.18 Target Lock Problems

### Robot changes from one pillar to another mid-pass

Target lock may be too weak.

Expected:

```text
select pillar
      ↓
temporarily commit
      ↓
complete pass
      ↓
release
```

### Robot ignores the next pillar

Target lock may be too strong or release logic may be incomplete.

A lock should be:

```text
temporary
```

not:

```text
permanent until program ends
```

Check debug state after the first obstacle.

The important question is:

```text
Did software return from PILLAR_ACTIVE to a state that can acquire another target?
```

---

# 8.19 Target Loss Problems

A target disappearing from Pixy's field of view does not automatically mean it has been passed.

Piolín's own steering changes camera orientation.

Therefore:

```text
pillar leaves frame
```

can mean:

```text
camera turned away
```

rather than:

```text
vehicle cleared pillar
```

If the robot immediately reverses steering when detection disappears, inspect target-loss handling.

A more robust sequence is:

```text
recent target retained briefly
      ↓
current maneuver continues
      ↓
S2/S3 geometry evaluated
      ↓
pillar clearance confirmed
      ↓
target released
```

Target loss and target clearance should be treated as different states.

---

# 8.20 Pillar Is Passed but Robot Still Crashes

<div align="center">

<img
  src="../../v-photos/v4/obstacle_red_run.jpg"
  alt="Piolín red obstacle maneuver"
  width="700"
/>

<br>

<sub><b>Figure 8.12.</b> Avoiding the pillar is only one part of the maneuver; recovery must also restore a useful track trajectory.</sub>

</div>

If Piolín passes the obstacle correctly but then hits a wall, the avoidance itself may already be successful.

Investigate:

```text
target release

countersteering

recovery timing

S2/S3 wall geometry

normal-control reactivation
```

The full maneuver is:

```text
DETECT
  ↓
AVOID
  ↓
PASS
  ↓
RELEASE
  ↓
COUNTERSTEER
  ↓
RECOVER
```

Do not weaken the initial avoidance merely because the recovery afterward is incorrect.

That can turn:

```text
successful pass + bad recovery
```

into:

```text
pillar collision
```

without solving the actual problem.

---

# 8.21 Why Obstacle Steering Can Appear Inverted After a Corner

If Red and Green behave correctly before a corner but appear inverted after it, do not assume Pixy has suddenly reversed its coordinate system.

Check:

```text
current navigation state

left/right steering sign

last active maneuver

target lock

corner controller still active?

wall controller influence

software direction variables
```

The physical rule remains:

```text
Red → RIGHT

Green → LEFT
```

throughout the course.

A failure that appears only after a state transition often indicates a **state-management or controller-interaction problem**, not a camera-color problem.

---

# 8.22 Color Sensor Troubleshooting

<div align="center">

<img
  src="../../v-photos/v4/color_sensor_bottom_view.jpg"
  alt="Bottom view of Piolín Color Sensor"
  width="650"
/>

<br>

<sub><b>Figure 8.13.</b> Floor detection should be diagnosed at the sensor, classification, and event-state levels separately.</sub>

</div>

### Color not detected

Check:

```text
S4 connection

sensor position

sensor height

casing

raw reading

classification range
```

### Correct color detected but wrong direction

Then the problem is not optical classification.

Check:

```text
Blue/Orange state mapping
```

### Color detected several times

Check:

```text
event lock

re-arm condition

cooldown
```

### Works stationary but fails while moving

Check:

```text
vehicle speed

confirmation count

sampling delay

sensor crossing time
```

Avoid widening thresholds immediately unless raw dynamic data shows classification itself is failing.

---

# 8.23 Parking Troubleshooting

<div align="center">

<img
  src="../../v-photos/v4/parking_area.jpg"
  alt="Piolín parking area"
  width="700"
/>

<br>

<sub><b>Figure 8.14.</b> Parking errors should be separated into state, approach, steering, and final-displacement problems.</sub>

</div>

Parking depends on the entire run state.

Possible failure categories include:

### Parking begins too early

Check:

```text
course counter

lap state

parking-enable condition

duplicate Color Sensor event
```

### Parking begins too late

Check:

```text
missed course event

parking trigger

final approach condition
```

### Parking starts correctly but stops in wrong place

Check:

```text
Motor A displacement

approach heading

steering center

wall geometry

physical drivetrain repeatability
```

### Pixy Pink appears but parking should not start

During Obstacles:

```text
sig1 = Pink
```

is a visual parking reference.

It should not automatically override course progression.

The desired logic is closer to:

```text
correct progress
+
parking state active
+
Pink reference valid
+
physical approach valid
```

before the final sequence begins.

---

# 8.24 Software Runtime Problems

Not every failure occurs after the robot begins moving.

### Open program does not start

Check:

```text
Pybricks runtime

file location

syntax/import errors

correct hardware objects
```

### Obstacle program does not start

Check:

```text
Python 3

ev3dev2 availability

SMBus/I2C availability

Pixy interface
```

### IDE reports missing EV3 libraries

Desktop editors may report that packages such as:

```text
ev3dev2
```

cannot be resolved locally.

This does not automatically mean the package is unavailable on the EV3.

Separate:

```text
editor language-server warning
```

from:

```text
actual EV3 runtime failure
```

The authoritative test is whether the program imports and runs in the intended EV3 environment.

---

# 8.25 Debug Output

Debug output should help identify the first incorrect state.

### Useful Open values

```text
direction

navigation state

corner count

S2

S3

gyro angle

steering command
```

A compact conceptual line is:

```text
DIR: CCW | STATE: STRAIGHT | TURN: 3 | S2: ... | S3: ... | G: ... | STEER: ...
```

### Useful Obstacle values

```text
state

selected signature

x

y

width

height

S2

S3

steering command
```

For example:

```text
STATE: AVOID | SIG: 2 | X: ... | W: ... | S2: ... | S3: ... | STEER: RIGHT
```

When the robot does something unexpected, compare:

```text
what the robot physically did
```

with:

```text
what the software believed it was doing
```

This distinction can immediately reveal whether the failure is perception, interpretation, or actuation.

---

# 8.26 Use Video as Diagnostic Evidence

Video is especially useful when a maneuver occurs too quickly to understand during the run.

A useful recording should show as much as practical of:

```text
starting position

track geometry

front steering

pillar position

corner entry

wall clearance

recovery
```

When possible, synchronize the video with software debug output or record the corresponding test ID.

Useful questions while reviewing a run include:

```text
Where was Piolín when steering first changed?

Was that change physically appropriate?

When did the camera lose the pillar?

When did recovery begin?

Did the front wheels actually follow the command?

Did the failure begin before the visible collision?
```

The purpose of video is not only presentation.

It is measurement evidence for timing and state transitions.

---

# 8.27 Return to a Known-Good Version

When an experimental modification creates several new problems, do not continue stacking fixes indefinitely.

Use Git to return to the most recent known-good version.

The process is:

```text
KNOWN-GOOD
    ↓
one experimental change
    ↓
test
```

If significantly worse:

```text
reject change
    ↓
return to baseline
```

If better:

```text
record result
    ↓
commit improvement
```

This prevents Piolín from accumulating many interacting changes until the original working behavior can no longer be recovered.

---

# 8.28 Recalibration After Physical Changes

The same software should not be assumed to behave identically after mechanical work.

Recheck the relevant subsystem after:

```text
steering rebuild

Motor B remounting

Motor A remounting

wheel change

drivetrain repair

ultrasonic movement

Color Sensor movement

Color Sensor casing change

Gyro movement

Pixy movement

Pixy 3D-casing change

camera orientation change
```

For example:

```text
Pixy behavior changed after casing work
```

should first trigger:

```text
camera position / orientation verification
```

rather than:

```text
rewrite target-selection algorithm
```

Likewise:

```text
Open suddenly drifts after steering repair
```

should first trigger:

```text
steering center verification
```

rather than immediately retuning gyro gains.

---

# 8.29 Recommended Diagnostic Workflow

When the cause is unclear, use this complete sequence.

```text
1. Stop Piolín.

2. Record the failed test.

3. Inspect mechanical condition.

4. Verify wiring.

5. Verify correct round configuration.

6. Test motors individually.

7. Read raw sensors.

8. Verify sensor mapping.

9. Verify software state.

10. Verify calculated steering command.

11. Compare command with physical wheel response.

12. Identify first incorrect layer.

13. Change one relevant variable.

14. Repeat the same test.

15. Compare against the previous result.
```

Do not skip directly from:

```text
"robot crashed"
```

to:

```text
"change PID"
```

without identifying whether PID was actually responsible.

---

# 8.30 Troubleshooting by Layer

The complete diagnostic structure can be summarized as:

```text
                    FAILURE OBSERVED
                           │
                           ▼
                     MECHANICAL?
                    /          \
                  YES          NO
                   │            │
                  FIX           ▼
                            ELECTRICAL?
                            /       \
                          YES       NO
                           │         │
                          FIX        ▼
                              RAW SENSOR?
                              /       \
                            WRONG     RIGHT
                              │         │
                             FIX        ▼
                                INTERPRETATION?
                                  /       \
                                WRONG     RIGHT
                                  │         │
                                 FIX        ▼
                                      STATE LOGIC?
                                       /      \
                                     WRONG    RIGHT
                                       │        │
                                      FIX       ▼
                                           CONTROL?
                                            /    \
                                          WRONG  RIGHT
                                            │      │
                                           FIX     ▼
                                              PHYSICAL
                                               RESPONSE
```

This structure makes troubleshooting repeatable.

---

# 8.31 Current Known Development Areas

Some Piolín behaviors are still under active development and should therefore receive extra attention during diagnosis.

### Open

```text
initial acquisition from different starting positions

corner consistency

corner exit geometry

multi-lap stability

final parking
```

### Obstacles

```text
Pixy target relevance

multiple-block selection

target lock

target-loss handling

Red/Green steering consistency

controller arbitration

pillar-pass confirmation

post-pillar recovery

parking
```

A failure in one of these areas does not mean the architecture itself is invalid.

It means the current implementation still requires testing and tuning.

The repository should distinguish clearly between:

```text
known architecture
```

and:

```text
unfinished performance tuning
```

---

# 8.32 Final Troubleshooting Checklist

Before modifying navigation code, verify:

| Check | Required |
| :--- | :--- |
| Mechanical structure intact | Yes |
| Steering center verified | Yes |
| Drivetrain free | Yes |
| Correct round hardware installed | Yes |
| Motor A on A | Yes |
| Motor B on B | Yes |
| S2 physically LEFT | Yes |
| S3 physically RIGHT | Yes |
| S4 working | Yes |
| Correct S1 device | Yes |
| Raw sensor values plausible | Yes |
| Software mapping matches hardware | Yes |
| Navigation state correct | Yes |
| Steering command known | Yes |
| Physical steering response matches command | Yes |

For Obstacles also verify:

| Pixy Check | Required |
| :--- | :--- |
| 3D-printed casing secure | Yes |
| S1 connection secure | Yes |
| `sig1 = Pink` | Yes |
| `sig2 = Red` | Yes |
| `sig3 = Green` | Yes |
| Red rule = RIGHT | Yes |
| Green rule = LEFT | Yes |
| Correct target selected | Yes |
| Target lock state known | Yes |

---

# 8.33 Final Engineering Assessment

Troubleshooting Piolín is most effective when the robot is treated as a chain of connected physical and software systems rather than as a program that occasionally makes mistakes.

The diagnostic sequence is:

```text
MECHANICS
→ WIRING
→ RAW SENSING
→ INTERPRETATION
→ STATE
→ CONTROL
→ ACTUATION
```

A failure should be corrected at the earliest layer where the expected behavior becomes incorrect.

This distinction is especially important in the two current competition configurations.

During Open:

```text
S2/S3
→ lateral geometry

Gyro
→ heading

Color Sensor
→ course progression
```

During Obstacles:

```text
Pixy2.1
→ obstacle identity and visual geometry

S2/S3
→ physical boundary context

Color Sensor
→ course progression
```

The current Pixy2.1 must be evaluated with its **3D-printed casing installed**, because the casing is part of the calibrated camera assembly. Likewise, the Color Sensor should remain in its current cased installation when floor-detection problems are diagnosed.

One of the most important obstacle troubleshooting rules is that the competition mapping never changes:

```text
RED
→ PASS RIGHT

GREEN
→ PASS LEFT
```

If the vehicle physically does the opposite, the team should determine whether the failure occurred in:

```text
signature identification

target selection

rule mapping

controller arbitration

steering sign

physical steering response
```

instead of immediately reversing the full system.

Similarly, an Open collision should not automatically lead to stronger steering. The original problem may have been an incorrect start state, direction mapping, gyro reference, or corner exit several seconds earlier.

The final troubleshooting principle is:

> **Do not fix the last visible symptom. Find the first incorrect assumption in the system and correct it there.**

Using this method allows PiolínTech to preserve known-good behavior, reduce unnecessary code changes, and turn failures into useful engineering evidence rather than repeated trial-and-error.

---

<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
