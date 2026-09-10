# Round 1 EV3 V1 — Code Explanation

This document explains the logic implemented in [`ev3v1.py`](./ev3v1.py), an early Open Challenge software version developed for Piolín during the evolution of the WRO Future Engineers 2026 project.

The purpose of this version was to test a simple autonomous strategy in which Piolín moved forward, detected the Blue and Orange floor markings with the EV3 Color Sensor, executed a predefined steering maneuver, counted the accepted markings, and stopped after completing twelve course events.

This program is preserved as part of PiolínTech's software evolution. It does **not** represent the current Phase 4 Open Challenge controller, which later introduced lateral ultrasonic geometry, gyro heading information, more advanced corner handling, and stronger event-based navigation.

---

## Hardware Used by This Version

`ev3v1.py` uses a deliberately small hardware configuration.

The EV3 Brick acts as the main controller. Motor A is responsible for propulsion, Motor B controls the front steering mechanism, and the EV3 Color Sensor connected to S4 observes the floor.

| Port | Component | Function |
|---|---|---|
| A | EV3 Large Motor | Rear propulsion |
| B | EV3 Medium Motor | Front steering |
| S4 | EV3 Color Sensor | Blue and Orange floor-mark detection |

This version does not use the current S2 and S3 lateral ultrasonic sensors for navigation and does not use the Gyro Sensor on S1.

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

The simplicity of this architecture made it useful for testing the earliest relationship between floor markings, steering, and course progression.

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

These values are development parameters. They describe the behavior of this particular early program and should not be interpreted as universal or final values for the current robot.

The program also defines:

```python
TOTAL_COUNTS = 12
```

which represents the twelve accepted course events used by this early Open Round model.

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

This is much simpler than the later Phase 4 Open controller, where steering can be continuously adjusted using geometry and heading information.

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

Orange is handled differently because an orange floor marking can sometimes be classified by the EV3 sensor as a nearby built-in color category. In this early implementation:

```python
if detected in (
    Color.RED,
    Color.YELLOW,
    Color.BROWN
):
    return 'ORANGE'
```

This was a practical early solution for working with the EV3 Color Sensor's named-color output.

If the floor does not match either course-marking group, the function returns:

```python
None
```

which represents neutral floor.

Later Piolín versions developed more detailed floor classification using sensor measurements such as RGB and reflection values, but this V1 program intentionally uses the simpler built-in classifier.

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

In this early version:

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

One of the most important characteristics of this early version is that the corner is **time-based**.

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

This approach is easy to understand and was useful during early development, but it also has an important limitation: elapsed time does not directly prove that the vehicle has completed the desired physical rotation.

Changes in speed, starting position, wheel behavior, battery condition, or mechanical alignment can change the resulting trajectory even when `TURN_TIME_MS` remains exactly the same.

This limitation became one of the reasons later versions moved toward more physically informed corner handling using ultrasonic geometry and gyro information.

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

This is an early form of the event-processing architecture that became much more important in later Piolín software.

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

This mechanism is one of the most important ideas preserved from this early program.

Although the current software architecture is more advanced, the principle that **one physical marking should create one software event** remains relevant.

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

This early implementation therefore uses the floor markings themselves as its main representation of course progression.

It does not yet contain the richer context later developed for distinguishing course events, corner states, and parking conditions.

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

The important limitation is that this version **stops after the twelfth accepted event**. It does not contain the more advanced parking sequence developed later.

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

Even though this program does not yet use the later full navigation state machine, it already maintains several variables representing internal software state.

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

## Main Limitations of EV3 V1

`ev3v1.py` was useful as a development milestone, but its limitations explain why the Open Round software continued to evolve.

The largest limitation is that navigation is driven primarily by the floor markings. Between color events, the robot simply moves forward and does not use S2 and S3 to continuously estimate its position relative to the walls.

The corner maneuver is also based on a fixed steering angle and fixed duration. Because it does not measure the physical completion of the corner, identical commands can produce different final poses if the initial conditions change.

The program also has no independent heading information. There is no gyro correction for straight-line drift and no gyro measurement to help verify the angular progression of a corner.

Finally, reaching twelve events immediately ends the run rather than activating a dedicated physical parking sequence.

These limitations became direct development targets for later software.

---

## Evolution Toward the Current Open Controller

The software progression from this V1 architecture can be summarized as a change in the amount and quality of information available to the controller.

In `ev3v1.py`, the main question is:

> **Which floor marking did S4 detect?**

The current Open architecture asks several questions simultaneously:

> **Where is Piolín relative to the walls?**

> **Which direction is the chassis pointing?**

> **Which physical course event has been reached?**

> **Is Piolín currently driving straight, entering a corner, leaving a corner, or preparing to park?**

This required the later addition of:

- S2 left lateral ultrasonic sensing;
- S3 right lateral ultrasonic sensing;
- S1 gyro heading information;
- stronger geometric navigation;
- physically informed corner handling;
- improved course-event processing;
- more deliberate parking logic.

The underlying EV3 platform and Motor A/Motor B architecture remained, but the software surrounding them became significantly more capable.

---

## Engineering Importance of This Version

`ev3v1.py` remains valuable because it captures an early stage of Piolín's software architecture in a form that is easy to understand.

It demonstrates several ideas that survived into later versions: a clear separation between propulsion and steering, deliberate start control, color confirmation, duplicate-event protection, physical course-event counting, and safe motor shutdown.

At the same time, it documents the limitations that motivated later improvements. Instead of removing this program after a more advanced controller was developed, PiolínTech preserves it as evidence of the software engineering process.

This makes it possible to trace the evolution from a simple architecture based primarily on:

```text
COLOR
→ TURN
→ COUNT
```

toward the current architecture based on:

```text
SENSING
→ PERCEPTION
→ COURSE CONTEXT
→ STATE
→ CONTROL
→ ACTUATION
```

---

## EV3 V1 Summary

`ev3v1.py` represents an early but important Open Challenge development stage. It uses the EV3 Color Sensor on S4 to identify Blue and Orange floor markings, confirms each marking before reacting, executes a time-based steering maneuver using Motor B, uses Motor A to move through the course, protects the counter against repeated detections of the same physical line, and stops after twelve accepted events.

Its simplicity made it useful for validating the relationship between floor detection, steering, and course progression. Its limitations also made the next engineering requirements clear: Piolín needed continuous knowledge of its lateral position, independent heading information, stronger corner-state awareness, and a more physical approach to final parking.

For that reason, this program should be interpreted as a **legacy software milestone**, not as the current Open Challenge controller.

---

<div align="center">

### [View `ev3v1.py`](./ev3v1.py)

<br>

### [← Back to PiolínTech Main README](../../README.md)

</div>
