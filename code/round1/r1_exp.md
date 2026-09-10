# Round 1 EV3 V1 — Current Open Challenge Code Explanation

This document explains the logic implemented in [`ev3v1.py`](./ev3v1.py), the **current Open Challenge program used by Piolín** for the WRO Future Engineers 2026 project.

The program follows a deliberately direct autonomous strategy: Piolín moves forward, detects the Blue and Orange floor markings with the EV3 Color Sensor, confirms each valid course event, executes the corresponding steering maneuver, counts the accepted markings, and stops after twelve accepted events.

The name `EV3 V1` identifies this published program version; it should **not** be interpreted as a legacy or inactive controller. This file represents the code currently used on the physical robot for the Open Challenge. Parameters may continue to be tuned during testing, but there is no separate unpublished “current Phase 4 controller” replacing this file.

---

## Hardware Used by the Current Open Program

`ev3v1.py` uses a deliberately small set of hardware inputs in its current Open Challenge implementation.

The EV3 Brick acts as the main controller. Motor A is responsible for propulsion, Motor B controls the front steering mechanism, and the EV3 Color Sensor connected to S4 observes the floor.

| Port | Component | Function |
|---|---|---|
| A | EV3 Large Motor | Rear propulsion |
| B | EV3 Medium Motor | Front steering |
| S4 | EV3 Color Sensor | Blue and Orange floor-mark detection |

In the exact program documented here, the navigation logic does **not read S2 or S3** and does **not read a Gyro Sensor on S1**. Therefore, even if additional sensors are physically available on Piolín, they do not influence the execution of this specific file.

The simplified architecture can therefore be understood as:

```text
S4 Color Sensor
      ↓
Color Classification
      ↓
Event Confirmation
      ↓
Blue / Orange Decision
      ↓
Motor B Steering
      ↓
Motor A Movement
```

The simplicity of this architecture is intentional: the current program bases its course progression primarily on floor events, steering actions, and the internal event counter.

---

## Program Initialization

The program begins by importing the Pybricks modules required to control the EV3 Brick, motors, buttons, and Color Sensor.

```python
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Stop, Button, Color
from pybricks.tools import wait
```

The EV3 hardware is then assigned to the correct ports:

```python
ev3 = EV3Brick()

drive = Motor(Port.A)
steering = Motor(Port.B)

color_sensor = ColorSensor(Port.S4)
```

This establishes the basic physical relationship used throughout the program. `drive` represents Motor A and controls longitudinal movement, while `steering` represents Motor B and controls the steering angle.

Before the autonomous run begins, the steering motor is reset so that its current physical position becomes the software reference for straight steering:

```python
steering.reset_angle(0)
```

For this reason, the front wheels should be physically centered before the program is started.

---

## Main Calibration Parameters

The program keeps its main behavior parameters near the beginning of the file so that testing does not require modifying the control logic itself.

For example:

```python
NORMAL_SPEED = -620
TURN_SPEED = -420

TURN_STEERING_ANGLE = 30
TURN_TIME_MS = 650

POST_TURN_STRAIGHT_MS = 180
STEERING_SPEED = 700
```

`NORMAL_SPEED` controls the propulsion motor during straight driving, while `TURN_SPEED` reduces the drive speed during a corner maneuver.

`TURN_STEERING_ANGLE` determines the target position given to Motor B when Piolín detects a floor marking. The steering value is maintained for `TURN_TIME_MS`, after which the steering mechanism returns to its center position.

These are the current tuning parameters stored in this program. They describe the behavior of the code presently used on Piolín and may still be adjusted during physical testing; they should not be interpreted as permanent universal values.

The program also defines:

```python
TOTAL_COUNTS = 12
```

which represents the twelve accepted course events used by the current Open Round program.

---

## Steering Center Function

The function:

```python
def center_steering():
```

returns Motor B to angle zero.

Its implementation is:

```python
steering.run_target(
    STEERING_SPEED,
    0,
    then=Stop.HOLD,
    wait=True
)
```

This is important because the program uses steering as a temporary maneuver. Piolín turns when a marking is detected and then deliberately returns the steering mechanism to its straight reference.

The sequence is therefore:

```text
Straight
→ Steering angle applied
→ Corner movement
→ Steering returns to zero
→ Straight movement resumes
```

In the current program, steering is intentionally handled as a discrete maneuver: Piolín applies a steering target for the turn, returns Motor B to center, and resumes straight movement.

---

## Floor Color Classification

The function:

```python
def read_track_color():
```

reads the EV3 Color Sensor and converts the sensor's built-in classification into one of three software results:

```text
BLUE
ORANGE
NONE
```

Blue is detected directly:

```python
if detected == Color.BLUE:
    return 'BLUE'
```

Orange is handled differently because an orange floor marking can sometimes be classified by the EV3 sensor as a nearby built-in color category. In the current implementation:

```python
if detected in (
    Color.RED,
    Color.YELLOW,
    Color.BROWN
):
    return 'ORANGE'
```

This is the practical classification strategy currently used by this program with the EV3 Color Sensor's named-color output.

If the floor does not match either course-marking group, the function returns:

```python
None
```

which represents neutral floor.

This program intentionally uses the simpler built-in named-color classifier rather than a separate RGB or reflection-based classification routine.

---

## Why Confirmation Is Necessary

The software does not immediately react to the first color reading.

Instead, it requires repeated observations of the same candidate color.

The relevant parameters are:

```python
COLOR_CONFIRMATIONS = 2
COLOR_RELEASE_CONFIRMATIONS = 3
```

When a color first appears, the program stores it as:

```python
candidate_color
```

and begins counting how many consecutive observations support that candidate.

If the next reading matches:

```python
candidate_count += 1
```

When enough matching readings have been observed, the program accepts the color as a real course event.

This provides basic protection against isolated or unstable sensor readings.

The principle is:

```text
One reading
→ Candidate

Repeated matching reading
→ Confirmed event
```

rather than allowing every individual S4 sample to immediately affect the robot.

---

## Blue and Orange Turning Logic

The function:

```python
def turn_for_color(detected_color):
```

contains the main corner behavior.

In the current program:

```text
BLUE
→ LEFT TURN
```

and:

```text
ORANGE
→ RIGHT TURN
```

For Blue:

```python
target = (
    -TURN_STEERING_ANGLE
    * STEER_DIRECTION
)
```

For Orange:

```python
target = (
    TURN_STEERING_ANGLE
    * STEER_DIRECTION
)
```

The variable:

```python
STEER_DIRECTION = 1
```

exists so that the steering polarity can be corrected if the physical steering mechanism is installed in the opposite orientation.

After selecting the target, Motor B moves to the requested steering position:

```python
steering.run_target(
    STEERING_SPEED,
    target,
    then=Stop.HOLD,
    wait=True
)
```

Motor A then moves Piolín through the corner at the reduced turning speed.

---

## Time-Based Corner Execution

One of the most important characteristics of the current Open program is that the corner is **time-based**.

After Motor B reaches the steering target:

```python
drive.run(TURN_SPEED)
wait(TURN_TIME_MS)
```

Piolín simply maintains the maneuver for the configured amount of time.

Once that period is complete, the steering returns to center:

```python
center_steering()
```

and normal forward movement resumes.

This approach is simple and currently practical for Piolín, but it also has an important limitation: elapsed time does not directly prove that the vehicle has completed the desired physical rotation.

Changes in speed, starting position, wheel behavior, battery condition, or mechanical alignment can change the resulting trajectory even when `TURN_TIME_MS` remains exactly the same.

This limitation is documented as a known property of the current program and is one of the areas that can be reconsidered if the team later decides that a more physically informed corner-completion method is necessary.

---

## Leaving the Floor Mark

After completing a corner, the program performs a short straight movement:

```python
drive.run(NORMAL_SPEED)
wait(POST_TURN_STRAIGHT_MS)
```

This helps Piolín continue away from the marking before normal detection resumes.

However, this alone is not the duplicate-count protection. The program also uses a dedicated line-lock mechanism.

That distinction is important because the Color Sensor may remain over the same physical marking for multiple control cycles.

---

## Event Counting and Line Lock

A single physical course marking can generate many sensor readings.

Without protection, one Blue strip could theoretically produce:

```text
BLUE
BLUE
BLUE
BLUE
```

and incorrectly increase the count four times.

`ev3v1.py` prevents this through:

```python
ready_for_new_color = True
```

After a confirmed event is accepted and counted:

```python
count += 1
```

the program changes:

```python
ready_for_new_color = False
```

This means that Piolín has already processed the current physical marking and cannot immediately count another event.

While the line is locked, additional Blue or Orange readings do not increase the course count.

This event lock is an important part of the current control logic because it converts many repeated sensor samples into one accepted physical course event.

---

## Neutral-Floor Release

The program must eventually allow another floor marking to be detected.

For that to happen, S4 must first return to neutral floor.

While the event detector is locked, the program counts consecutive neutral readings:

```python
if detected is None:
    release_count += 1
```

Once:

```python
release_count >= COLOR_RELEASE_CONFIRMATIONS
```

the event detector is re-armed:

```python
ready_for_new_color = True
```

This creates the event lifecycle:

```text
Detect color
→ Confirm
→ Count once
→ Lock
→ Leave physical marking
→ Confirm neutral floor
→ Re-arm
```

This mechanism is one of the most important parts of the current program. The guiding principle is that **one physical marking should create one software event**, even if the sensor reads that same marking during several consecutive control cycles.

---

## Course Counter

Each accepted Blue or Orange event increases:

```python
count
```

by one.

The EV3 screen displays the progress:

```python
'COUNT {}/{}'.format(
    count,
    TOTAL_COUNTS
)
```

For example:

```text
COUNT 4/12
```

indicates that four accepted floor events have been processed.

The program continues until:

```python
count >= TOTAL_COUNTS
```

with:

```python
TOTAL_COUNTS = 12
```

The current implementation therefore uses the accepted floor markings as its main representation of course progression.

In this file, course progress is intentionally represented by the accepted-event counter rather than by a larger navigation state machine.

---

## Starting the Robot

The program includes:

```python
def wait_for_start():
```

so that Piolín does not begin moving immediately after the script is launched.

The EV3 screen displays:

```text
PRESS CENTER
```

and waits until the EV3 center button is pressed.

The function also waits for the button to be released before the autonomous run begins.

This creates a deliberate start condition and prevents the robot from moving unexpectedly while the program is being prepared.

---

## Manual Emergency Stop

During the main loop, the program checks:

```python
if Button.DOWN in ev3.buttons.pressed():
    break
```

Pressing the EV3 Down button exits the autonomous loop.

This provides a simple manual interruption mechanism during testing.

Once the loop exits, the `finally` section ensures that Motor A is stopped and the steering mechanism is returned toward center.

---

## Finishing the Run

If the program reaches twelve accepted events, the function:

```python
stop_finished()
```

is executed.

The drive motor is held:

```python
drive.hold()
```

the steering returns to center, and the EV3 displays:

```text
FINISHED 12/12
```

A short beep is also attempted to indicate completion.

In the exact program documented here, Piolín **stops after the twelfth accepted event**. This file does not implement a separate physical parking sequence after that count.

Therefore, this behavior should be interpreted as:

```text
12 events reached
→ stop
```

rather than:

```text
12 events reached
→ physically locate parking area
→ approach
→ align
→ park
```

---

## Main Control Loop

The main loop brings all of the previous functions together.

Its general behavior is:

```python
while count < TOTAL_COUNTS:
```

Within each iteration, Piolín reads S4 and determines whether it is currently waiting for a new course event or waiting to leave an already accepted marking.

The logical sequence is:

```text
Read S4
→ Is detector ready?

If YES:
    Look for Blue / Orange
    Confirm candidate
    Execute turn
    Count event
    Lock detector

If NO:
    Wait for neutral floor
    Confirm release
    Re-arm detector
```

This creates a simple but understandable autonomous control loop.

---

## Software State Variables

Although this program does not use a large multi-state navigation machine, it maintains several variables that represent important internal software state.

| Variable | Purpose |
|---|---|
| `count` | Number of accepted course events |
| `candidate_color` | Current possible Blue or Orange event |
| `candidate_count` | Number of consecutive readings supporting that candidate |
| `ready_for_new_color` | Whether another event may be accepted |
| `release_count` | Number of neutral readings after an accepted line |

This is significant because the program already demonstrates the transition from purely reactive logic toward software that remembers what happened during previous control cycles.

For example, Piolín does not only ask:

> What color do I see right now?

It also asks:

> Have I already counted this physical marking?

That concept eventually evolved into much richer state-based behavior.

---

## Current Limitations and Known Trade-Offs

`ev3v1.py` is the **current Open Challenge controller used by Piolín**, but documenting the code accurately also means documenting what it does not currently do.

The main navigation input in this file is the floor Color Sensor on S4. Between accepted Blue and Orange events, the robot drives using its configured propulsion and steering behavior without continuously using lateral Ultrasonic Sensor feedback.

The corner maneuver is based on a fixed steering target and a fixed duration:

```python
drive.run(TURN_SPEED)
wait(TURN_TIME_MS)
```

This makes the behavior straightforward to tune, but it also means that the program does not independently measure whether a physical 90-degree rotation has been completed before ending the steering interval.

The exact program documented here also does not use gyro heading feedback. Therefore, straight-line drift and corner rotation are not corrected through an S1 gyro measurement inside this file.

Course progression is represented by the accepted floor-event count. When:

```python
count >= TOTAL_COUNTS
```

the program finishes the run.

In this exact version, reaching the twelfth accepted event leads to the finishing routine rather than to a separate parking state machine.

These points are **current implementation characteristics**, not evidence that a different hidden competition controller exists. If the team changes the competition code later, this explanation should be updated so the documentation continues to match the program actually running on Piolín.

---

## Why the Current Strategy Is Intentionally Simple

A more complicated controller is not automatically a better controller.

For the current Open program, the team chose a direct relationship between physical floor events and steering actions. That keeps the code understandable and makes it easier to identify whether a problem came from color detection, event confirmation, steering direction, steering duration, or course counting.

The software therefore concentrates on a small number of responsibilities:

```text
START
→ DRIVE
→ DETECT FLOOR EVENT
→ CONFIRM EVENT
→ TURN
→ RETURN STEERING TO CENTER
→ COUNT ONCE
→ RELEASE EVENT LOCK
→ REPEAT
→ STOP AFTER 12 EVENTS
```

This architecture has an important debugging advantage. If the robot reacts incorrectly, the team can inspect a relatively small chain of causes instead of several simultaneous controllers.

The strategy also reflects the actual code used on the robot. The purpose of this document is not to make the controller appear more complex than it is, but to explain clearly how the real competition program operates.

---

## Current Software State Variables

The program maintains a compact set of variables that gives it memory across control cycles.

| Variable | Purpose |
|---|---|
| `count` | Number of accepted course events |
| `candidate_color` | Current possible Blue or Orange event |
| `candidate_count` | Consecutive readings supporting the current candidate |
| `ready_for_new_color` | Whether a new physical event can be accepted |
| `release_count` | Consecutive neutral-floor readings used to re-arm detection |

These variables are important because the controller is not purely reactive.

For example, Piolín does not only ask:

> What color is below the sensor right now?

It also keeps track of:

> Is this a new physical marking, or am I still above the same marking that I already counted?

That distinction prevents duplicate counts and makes the course counter represent physical events more reliably.

---

## Engineering Value of the Current Controller

The current controller demonstrates that useful autonomous behavior does not require unnecessary software complexity.

Motor A and Motor B have clearly separated responsibilities. The Color Sensor is converted into confirmed physical events instead of being treated as a stream of unrelated samples. The line-lock mechanism prevents duplicate counts, and the start and emergency-stop logic provide deliberate control during testing.

The program also exposes its limitations clearly. Its corner behavior is time-based, it does not use continuous lateral wall feedback, and it does not use gyro heading feedback inside this file.

Documenting these limitations is part of the engineering process because it allows the team to decide whether a future modification actually solves a measured problem rather than adding complexity only because another architecture is possible.

If a future test shows that one of these limitations prevents reliable performance, the team can compare the current baseline against a modified controller and decide whether the additional sensing or state logic provides a real benefit.

---

## Relationship to Piolín's Broader Development

PiolínTech has experimented with additional sensing, vision systems, geometric navigation, and different control strategies throughout the project.

Those experiments remain valuable engineering evidence, but they should not be confused with the behavior implemented in this specific Open Challenge source file.

For `code/round1/ev3v1.py`, the authoritative implementation is the code itself:

```text
EV3 Brick
+
Motor A propulsion
+
Motor B steering
+
S4 Color Sensor
+
event confirmation
+
time-based turns
+
12-event course counter
```

If other documents in the repository describe experimental ultrasonic, gyro, or alternative Open-control ideas, those sections should be labeled according to their actual status so a reader can distinguish experimental architecture from the current competition program.

This keeps the repository internally consistent and allows a judge to move directly from the documentation to the source code and observe the same control logic.

---

## Current Competition Code Summary

`ev3v1.py` is Piolín's **current Round 1 Open Challenge program**.

It uses the EV3 Color Sensor on S4 to identify Blue and Orange floor markings, requires repeated observations before accepting a candidate, executes the corresponding time-based steering maneuver with Motor B, uses Motor A for propulsion, prevents repeated readings of the same physical marking from creating duplicate events, and tracks course progression through a twelve-event counter.

The current logic can be summarized as:

```text
PRESS CENTER
→ START

DRIVE FORWARD
→ READ S4

BLUE / ORANGE?
→ CONFIRM
→ TURN
→ COUNT ONCE
→ LOCK EVENT

NEUTRAL FLOOR?
→ CONFIRM RELEASE
→ RE-ARM

12 ACCEPTED EVENTS?
→ STOP
→ CENTER STEERING
→ FINISHED
```

The file is not a legacy placeholder and is not merely an early example preserved for historical purposes. It represents the program currently used on the physical Piolín robot for the Open Challenge.

Its parameters may continue to change as the team calibrates the robot, and future revisions may add or remove behaviors. When that happens, the documentation should evolve together with the source code so the repository always describes the robot that actually competes.

---

<div align="center">

### [View `ev3v1.py`](./ev3v1.py)

<br>

### [← Back to PiolínTech Main README](../../README.md)

</div>
