# 2. Legacy Prototype Testing and Analysis

> [!WARNING]
> This document describes **historical Piolín prototype testing, experimental control strategies, failed iterations, and engineering analysis** carried out during WRO Future Engineers 2026 development.
>
> The configurations, thresholds, sensor combinations, and software behaviors described here are not necessarily part of the current competition robot.
>
> Current hardware and software documentation always takes priority over this legacy analysis.

Piolín did not reach its current architecture through a single successful design. The robot evolved through repeated cycles of construction, programming, track testing, failure observation, modification, and retesting.

Many of the most useful engineering conclusions did not come from successful full-course runs. They came from situations where the robot behaved differently from what the software designer expected.

Examples included:

```text
correct color detected
but wrong physical passing side

correct steering command
but unstable vehicle trajectory

pillar visible to camera
but EV3 did not react

robot completed one corner
but software counted two

same code
but different behavior from a different starting position

camera lost target
before obstacle had actually been passed
```

These observations gradually changed the development process from:

```text
change code
→ run robot
→ visually judge result
```

toward a more structured approach:

```text
identify subsystem
      ↓
define expected behavior
      ↓
change one variable
      ↓
test
      ↓
observe
      ↓
classify failure
      ↓
retain or revert
```

The purpose of this document is to preserve that testing history and the engineering reasoning produced by it.

---

# 2.1 Why Prototype Testing Was Necessary

Piolín is an Ackermann-steered autonomous vehicle operating in a constrained track environment.

Its behavior depends on several interacting systems:

```text
mechanical steering

rear propulsion

sensor geometry

camera perception

wall sensing

floor-color detection

software state

vehicle speed

battery condition
```

A parameter that appears correct mathematically can still behave incorrectly once these systems interact physically.

For example:

```text
Motor B command
      ↓
steering linkage
      ↓
front-wheel angle
      ↓
vehicle moves forward
      ↓
actual turning radius
```

The software does not command the final trajectory directly.

It commands an actuator that operates through a mechanical system.

Testing was therefore required to determine whether the physical robot matched the assumptions used by the software.

---

# 2.2 The Core Testing Loop

A useful description of the development loop is:

```text
DESIGN
   ↓
IMPLEMENT
   ↓
TEST
   ↓
OBSERVE
   ↓
DIAGNOSE
   ↓
CHANGE
   ↓
RETEST
```

<div align="center">

<img
  src="../../embed/legacy_testing_cycle.png"
  alt="Piolín legacy engineering testing cycle"
  width="850"
/>

<br>

<sub><b>Figure L2.1.</b> Prototype development followed repeated design, implementation, testing, diagnosis, and refinement cycles.</sub>

</div>

The quality of the final decision depended heavily on the **diagnosis** step.

If a steering failure was incorrectly classified as a camera failure, camera parameters could be changed unnecessarily.

If an electrical connection problem was interpreted as a control problem, navigation code could become more complicated without solving the actual issue.

---

# 2.3 Failure Classification

Over time, Piolín failures could be grouped into several major categories.

| Category | Typical Examples |
| :--- | :--- |
| Perception | False camera detection, missed color, unstable target |
| Geometry | Wall distance, FOV, sensor orientation, starting position |
| State logic | Double counting, stale target lock, incorrect transition |
| Control | Zig-zag, overcorrection, weak steering, late response |
| Mechanical | Steering play, wheel alignment, drivetrain friction |
| Electrical / communication | Wrong port, missing sensor, Nano/USB communication |
| Integration | Two controllers requesting conflicting steering |
| Methodology | Too many changes between tests |

A visible failure could belong to more than one category.

For example:

```text
robot hits red pillar
```

could result from:

```text
red not detected

red detected too late

EV3 never received detection

steering sign inverted

wall controller overrode vision

steering mechanically weak

vehicle speed too high
```

This is why symptom-based diagnosis alone was insufficient.

---

# 2.4 Testing Perception Separately from Navigation

One of the most important lessons was that a camera should be tested independently before judging the full autonomous maneuver.

For the historical HuskyLens architecture, a complete chain existed:

```text
pillar
  ↓
HuskyLens
  ↓
Arduino Nano
  ↓
USB Serial
  ↓
EV3
  ↓
state logic
  ↓
steering
```

A test therefore needed to answer several separate questions.

```text
Does the camera see the object?

Does it identify the correct ID?

Does Nano receive the data?

Does Nano send the expected message?

Does EV3 receive the line?

Does EV3 parse it correctly?

Does obstacle logic choose correct side?

Does Motor B physically steer correct way?
```

<div align="center">

<img
  src="../../embed/legacy_layered_testing.png"
  alt="Layered testing of Piolín perception and navigation system"
  width="880"
/>

<br>

<sub><b>Figure L2.2.</b> Layered testing separated perception, communication, interpretation, actuation, and physical vehicle response.</sub>

</div>

This prevented a correct camera from being blamed for a downstream steering error.

---

# 2.5 Static Testing Was Not Enough

Several sensing systems behaved convincingly while the robot was stationary.

However, stationary testing removed many variables that exist during autonomous movement.

While driving:

```text
camera position changes

background changes

lighting changes

pillar moves across image

available reaction time decreases

ultrasonic geometry changes

steering changes sensor viewpoint
```

Therefore:

```text
works while stationary
```

did not imply:

```text
works reliably during a complete run
```

Dynamic testing was essential.

---

# 2.6 Historical HuskyLens Testing

The HuskyLens system demonstrated that Piolín could distinguish:

```text
ID 1 = GREEN

ID 2 = RED
```

but full-track testing revealed several problems that were difficult to reproduce using only stationary tests.

Observed issues included:

```text
false detections

intermittent Green detection

lighting sensitivity

objects outside track being recognized

target leaving FOV during steering

multiple visible blocks

target lock remaining active too long
```

These observations were particularly useful because they revealed that **recognition accuracy alone was not the complete problem**.

The vehicle needed contextual and temporal perception.

---

# 2.7 False Detection Testing

False detections were tested by observing the camera in representative track environments rather than only placing a clean pillar against an isolated background.

Potential confusing regions included:

```text
track material

shadows

reflections

colored objects outside track

background structures
```

The resulting engineering problem was a trade-off.

```text
loose filtering
→ more false positives


strict filtering
→ more valid targets rejected
```

<div align="center">

<img
  src="../../embed/legacy_false_positive_negative_test.png"
  alt="Legacy Piolín false positive and false negative vision trade-off"
  width="850"
/>

<br>

<sub><b>Figure L2.3.</b> Vision filtering had to balance false-positive rejection against the risk of rejecting real pillars.</sub>

</div>

This led to the conclusion that a single threshold could not always solve perception reliability.

---

# 2.8 Green vs. Red Detection

During HuskyLens testing, Green was observed to be less consistent than Red in several conditions.

Instead of assuming both colors behaved identically, testing had to evaluate them independently.

A useful test sequence was:

```text
RED
→ stationary
→ moving
→ different angle
→ different distance


GREEN
→ stationary
→ moving
→ different angle
→ different distance
```

The repeated Green issue demonstrated why individual target classes should be validated separately.

A single statement such as:

```text
camera detects colors
```

was too general to describe actual competition behavior.

---

# 2.9 Intermittent Detection

One difficult camera behavior was intermittent recognition.

A physical pillar could remain continuously visible to a human observer while software received a sequence more similar to:

```text
DETECTED

NOT DETECTED

DETECTED

NOT DETECTED
```

This created problems for controllers that responded directly to every current frame.

A frame-by-frame controller could repeatedly enter and exit obstacle mode.

The solution required some degree of temporal memory.

However, memory created the next problem:

```text
when should the detection be forgotten?
```

That question eventually became part of target-state management.

---

# 2.10 Field-of-View Tests

The camera's field of view was tested not only when Piolín was perfectly aligned, but also after turns.

This was important because a small post-corner heading error could move the next pillar outside the camera image.

The failure sequence was often:

```text
corner completed
      ↓
robot exits slightly rotated
      ↓
pillar outside FOV
      ↓
no detection
      ↓
vehicle continues
      ↓
pillar becomes visible late
```

<div align="center">

<img
  src="../../embed/legacy_fov_track_test.png"
  alt="Camera field of view test after Piolín corner exit"
  width="860"
/>

<br>

<sub><b>Figure L2.4.</b> Dynamic FOV testing evaluated whether the next obstacle remained visible after a realistic corner exit.</sub>

</div>

This showed that camera placement and post-corner vehicle alignment were part of the same perception problem.

---

# 2.11 Target-Loss Testing

One of the most useful tests compared:

```text
target disappears from camera
```

with:

```text
vehicle physically passes target
```

These are not equivalent events.

Piolín could begin steering around a pillar, rotate the camera away from it, and lose visual detection before sufficient clearance existed.

This produced an important experimental conclusion:

> **Camera disappearance cannot be used by itself as a pillar-passed condition.**

Later strategies therefore considered ultrasonic geometry as additional evidence.

---

# 2.12 Lateral Ultrasonic Pass Confirmation

The side ultrasonic sensors offered a physical method of observing the pillar passing beside the robot.

A typical qualitative sequence was:

```text
normal wall distance
      ↓
distance decreases
      ↓
pillar enters lateral sensor region
      ↓
minimum region
      ↓
distance increases again
```

This created a stronger physical interpretation:

```text
camera identifies target
+
lateral geometry changes
+
distance opens again
=
stronger evidence of physical pass
```

<div align="center">

<img
  src="../../embed/legacy_pass_confirmation_test.png"
  alt="Legacy pillar pass confirmation testing using lateral ultrasonic measurements"
  width="870"
/>

<br>

<sub><b>Figure L2.5.</b> Lateral ultrasonic behavior was explored as physical evidence that the vehicle had moved past an obstacle.</sub>

</div>

The exact thresholds were not universal and depended on geometry, but the principle remained useful.

---

# 2.13 Target-Lock Testing

Target locking was introduced to prevent unstable color switching.

Without lock:

```text
RED
→ loss
→ GREEN false detection
→ RED
```

could cause inconsistent steering.

With lock:

```text
RED confirmed
→ maintain RED maneuver
```

was more stable.

However, testing revealed the opposite extreme.

```text
first pillar locked
      ↓
pillar passed
      ↓
next pillar visible
      ↓
old lock remains
      ↓
next pillar ignored
```

This showed that target locking had two calibration dimensions:

```text
how easily target becomes locked

how reliably target becomes released
```

The release logic was just as important as acquisition.

---

# 2.14 Multiple-Block Testing

The perception system was also tested in situations where more than one candidate target appeared simultaneously.

A simplistic strategy:

```text
take first block
```

could fail because returned ordering did not guarantee physical relevance.

The first block could be:

```text
smaller

farther away

future obstacle

background detection
```

Testing therefore led toward a relevance concept involving:

```text
target identity

position

size

temporal persistence

current navigation state
```

This lesson later transferred directly into Pixy2.1 development.

---

# 2.15 Testing Reference Code from Other Teams

PiolínTech studied successful external WRO implementations to understand useful navigation concepts.

This was valuable for learning ideas such as:

```text
wall following

camera-based pillar selection

corner handling

state management
```

However, direct copying of numerical values repeatedly proved unreliable.

Another team's constants may depend on:

```text
different camera

different camera height

different wheelbase

different steering mechanism

different motor layout

different vehicle speed
```

For example, camera thresholds from another robot could only be interpreted as examples of **what type of variable matters**.

They were not Piolín calibration values.

The correct process became:

```text
study idea
      ↓
understand physical meaning
      ↓
adapt architecture
      ↓
measure Piolín
      ↓
calibrate Piolín values
```

---

# 2.16 Hardware-Mapping Validation

Several historical software problems were caused by code being written for a hardware mapping that did not match the physical robot.

Examples included different interpretations of:

```text
S2

S3

Motor A

Motor B
```

Piolín's current convention is:

```text
A = propulsion

B = steering

S2 = LEFT ultrasonic

S3 = RIGHT ultrasonic
```

Historical reference code sometimes used different assignments.

A software algorithm could therefore be logically correct and still produce an incorrect vehicle response simply because:

```text
software LEFT sensor
```

was physically:

```text
RIGHT sensor
```

or a steering motor was assumed to be a drive motor.

This produced one of the simplest but most important testing rules:

> **Verify hardware mapping before tuning control parameters.**

---

# 2.17 Steering-Sign Testing

Another repeated source of confusion was steering sign.

The software needed a consistent physical interpretation of:

```text
positive steering

negative steering
```

Before obstacle logic could be trusted, a basic actuator test needed to verify:

```text
command LEFT
→ front wheels physically move left


command RIGHT
→ front wheels physically move right
```

Without this verification:

```text
RED correctly detected
```

could still lead to:

```text
wrong-side pass
```

because perception and steering mapping were independent problems.

---

# 2.18 Why Wrong-Side Passing Did Not Always Mean Wrong Color Recognition

Suppose Piolín passes a Red pillar on the left.

At least several explanations are possible:

```text
camera classified Red as Green

EV3 parsed ID incorrectly

target lock contained Green

steering command sign inverted

avoidance side mapping inverted

another controller overrode obstacle steering
```

Therefore the visible result:

```text
wrong side
```

did not uniquely identify the failing subsystem.

This reinforced the need for logs containing intermediate state information.

Useful debugging output could include:

```text
target ID

target state

left US

right US

steering request

active controller
```

rather than only observing the final trajectory.

---

# 2.19 Conflicting Controllers

One of the most repeated causes of zig-zag behavior was multiple controllers requesting steering corrections at the same time.

For example:

```text
camera says LEFT

wall controller says RIGHT

recenter logic says LEFT

safety logic says RIGHT
```

If those requests alternated between control cycles:

```text
+8
-6
+5
-7
```

the physical result was:

```text
LEFT
RIGHT
LEFT
RIGHT
```

<div align="center">

<img
  src="../../embed/legacy_controller_conflict.png"
  alt="Legacy Piolín steering conflict between multiple controllers"
  width="870"
/>

<br>

<sub><b>Figure L2.6.</b> Zig-zag behavior often resulted from multiple control subsystems competing for Motor B authority.</sub>

</div>

The solution was architectural rather than simply numerical.

---

# 2.20 State-Dependent Steering Authority

Later development moved toward assigning steering responsibility according to robot state.

A conceptual structure was:

```text
NORMAL
→ wall navigation dominant


CORNER
→ corner controller dominant


PILLAR
→ vision objective dominant


PASSING
→ maintain obstacle trajectory


RECENTER
→ ultrasonic geometry dominant


SAFETY
→ emergency correction
```

This reduced the chance of several controllers continuously fighting each other.

The lesson carried forward was:

> **Control arbitration is often more important than adding another correction term.**

---

# 2.21 Over-Aggressive Correction Testing

Several controllers produced a familiar oscillation pattern.

```text
small error
      ↓
large correction
      ↓
robot crosses target
      ↓
error changes sign
      ↓
large opposite correction
```

The resulting vehicle path became a zig-zag.

This appeared in:

```text
wall correction

post-pillar recentering

camera steering

initial acquisition
```

Testing showed that a controller should be judged not only by:

```text
does it correct error?
```

but also by:

```text
does it settle without repeatedly crossing the target?
```

---

# 2.22 Correction Strength vs. Reaction Speed

Reducing gain can decrease oscillation but may also make the robot react too slowly.

The trade-off is:

```text
high correction
→ faster reaction
→ greater overshoot risk


low correction
→ smoother behavior
→ greater late-response risk
```

This is why tuning one numerical gain without considering vehicle speed was insufficient.

Control strength and forward velocity had to be tested together.

---

# 2.23 Vehicle Speed Testing

An intuitive response to instability is to reduce speed.

This helped in some situations because it increased reaction time.

However, reducing speed too much also created problems for Piolín's Ackermann geometry.

Ackermann steering requires longitudinal vehicle movement.

```text
front wheels turn
+
vehicle advances
=
curved path
```

If propulsion becomes extremely slow:

```text
steering changes
```

but:

```text
vehicle geometry develops very slowly
```

which can produce awkward corner and recovery behavior.

The objective was therefore not minimum speed.

It was a speed that provided:

```text
enough perception time

enough steering response

enough forward motion for Ackermann geometry
```

---

# 2.24 Corner-Strength Testing

Corner tuning repeatedly moved between two extremes.

```text
corner too weak
→ vehicle runs wide / reaches wall


increase steering or duration
        ↓

corner too strong
→ vehicle cuts excessively / over-rotates
```

This iterative cycle showed that a corner cannot be defined by steering magnitude alone.

Its physical result also depends on:

```text
forward speed

entry position

entry heading

steering mechanics

turn duration

available geometry
```

The later use of gyro during Open provided a more direct orientation reference for evaluating the amount of rotation achieved.

---

# 2.25 Corner Start Testing

Several failures came from initiating a corner too late.

A typical sequence was:

```text
robot approaches end of straight
      ↓
corner event not recognized
      ↓
robot continues forward
      ↓
steering begins late
      ↓
collision / wide turn
```

This demonstrated that corner logic requires both:

```text
reliable start condition
```

and:

```text
reliable completion condition
```

Possible physical evidence included:

```text
floor color event

wall geometry change

loss/opening of expected wall

gyro rotation once turn begins
```

No single historical implementation solved every case perfectly, but testing clarified the information needed by later Open development.

---

# 2.26 Corner Completion Testing

Timed turns can work under stable conditions, but they depend heavily on:

```text
speed

battery

friction

starting angle

steering response
```

A more robust corner completion condition uses physical feedback.

This is one reason the current Open architecture returned to using the Gyro Sensor.

Historical testing showed the limitation of treating:

```text
turn for N milliseconds
```

as equivalent to:

```text
vehicle rotated expected amount
```

Those two conditions are not always the same.

---

# 2.27 Color-Sensor Event Testing

Piolín used floor-color information as course-state evidence.

A major issue appeared when one physical marking remained under the sensor for several control cycles.

The sensor could report:

```text
BLUE

BLUE

BLUE

BLUE
```

while the robot had crossed only:

```text
ONE physical landmark
```

A naive counter could therefore produce:

```text
1
2
3
4
```

from one line.

This revealed the distinction between:

```text
sensor sample
```

and:

```text
physical event
```

---

# 2.28 Event Latching

The solution was to introduce an event-latching concept.

```text
valid color detected
      ↓
count once
      ↓
lock event
      ↓
ignore repeated same-line samples
      ↓
re-arm after sufficient physical separation
```

<div align="center">

<img
  src="../../embed/legacy_color_event_latch.png"
  alt="Legacy Piolín color event latching"
  width="850"
/>

<br>

<sub><b>Figure L2.7.</b> Event latching prevented multiple software counts from one physical floor marking.</sub>

</div>

Encoder movement or neutral-floor evidence could help determine when another color event should become valid.

This lesson remains useful in the current course-progress logic.

---

# 2.29 Color Sensor and Ambient Light

The downward Color Sensor also experienced environmental-light variation.

Instead of only expanding software thresholds, Piolín added a physical casing around the sensor.

The engineering sequence was:

```text
inconsistent optical environment
      ↓
color readings less repeatable
      ↓
physical light isolation added
      ↓
more controlled measurement environment
```

This was an important example of solving a sensing problem mechanically rather than exclusively through code.

---

# 2.30 Ultrasonic Orientation Testing

The ultrasonic sensors were tested in different physical orientations during development.

Historical arrangements included:

```text
diagonal sensors

lateral sensors

front sensor configurations
```

A sensor orientation changes the physical meaning of the reported distance.

For a lateral sensor approximately perpendicular to a wall:

```text
reading
≈ lateral separation
```

For a diagonal sensor:

```text
reading
=
geometry-dependent line-of-sight distance
```

Therefore the same controller cannot always be transferred between sensor orientations without modification.

The eventual preference for lateral sensors simplified interpretation.

---

# 2.31 Initial-Position Testing

Another repeated issue was starting Piolín from different lateral positions.

A controller tuned for a center start could behave badly when started near an outer wall.

A direct controller might see:

```text
large distance error
```

and immediately command:

```text
large steering correction
```

causing the robot to cross the track too aggressively.

This motivated a gradual acquisition concept.

---

# 2.32 Progressive Acquisition

Instead of instantly demanding the final wall target, a more stable approach was:

```text
measure current position
      ↓
start from current geometry
      ↓
move reference gradually
      ↓
approach desired operating position
```

<div align="center">

<img
  src="../../embed/legacy_progressive_acquire.png"
  alt="Piolín gradual acquisition from different starting positions"
  width="860"
/>

<br>

<sub><b>Figure L2.8.</b> Progressive acquisition reduced the large initial steering command produced when the robot began far from its desired wall position.</sub>

</div>

This was particularly important because competition starting geometry may not always reproduce a laboratory placement exactly.

---

# 2.33 Mechanical Testing Before Software Tuning

Software changes were sometimes used to compensate for mechanical problems.

This proved inefficient.

A more appropriate diagnostic order became:

```text
check steering freely moves

check wheels aligned

check drivetrain friction

check sensor mounts

then tune software
```

If Motor B command changes but the wheel angle does not respond consistently, changing a gain does not solve the mechanical cause.

---

# 2.34 Steering Play and Ackermann Geometry

Piolín's steering mechanism contains passive mechanical elements.

Therefore:

```text
Motor B encoder angle
```

is not identical to:

```text
front wheel steering angle
```

The relationship depends on:

```text
linkage geometry

mechanical play

connection points

pivot friction
```

This explained why theoretically reasonable motor angles sometimes produced slightly different physical turns.

It also reinforced the need for steering repeatability tests.

---

# 2.35 Wheel and Steering Reinforcement

Mechanical reinforcement of the front-wheel and steering structure was part of development because physical flexibility could change wheel response.

A stronger structure could improve repeatability without changing one line of software.

This demonstrated the relationship:

```text
mechanical consistency
      ↓
more repeatable actuator response
      ↓
more meaningful software calibration
```

The opposite is also true: a mechanically unstable platform makes software tuning much harder.

---

# 2.36 Drivetrain Testing

Motor A performance also required mechanical verification.

Unexpectedly slow motion could result from:

```text
battery condition

axle friction

wheel rubbing

misaligned drivetrain

software speed setting
```

Testing the drivetrain independently helped determine whether a navigation problem originated before or after the propulsion motor.

---

# 2.37 Reverse-Maneuver Testing

Reverse movement was explored several times during obstacle development.

Potential uses included:

```text
creating additional space

reacquiring pillar

recovering from too-close approach

repositioning before steering
```

However, reverse introduced additional state transitions.

```text
forward
→ reverse
→ steering change
→ forward
```

If each transition depended on time rather than physical state, variability could increase.

Reverse therefore became a recovery technique rather than a universal solution.

---

# 2.38 Parking Testing

Parking was repeatedly more difficult when introduced before the main lap behavior was stable.

A program trying to solve simultaneously:

```text
straight navigation

corners

three laps

color counting

obstacle handling

parking
```

contained many interacting states.

A stronger testing order became:

```text
stable movement
      ↓
stable cornering
      ↓
stable progress counting
      ↓
complete laps
      ↓
parking
```

This reduced the number of unresolved variables at each development stage.

---

# 2.39 Why Parking Was Delayed

Parking depends on the quality of everything that occurs before it.

If Piolín arrives at the final region with:

```text
wrong heading

wrong lateral position

wrong counter

wrong lap state
```

then even a well-designed parking routine may fail.

Therefore parking was treated as:

```text
final state of a successful navigation sequence
```

rather than an isolated maneuver.

This systems perspective remains relevant in current development.

---

# 2.40 Communication Testing

The historical HuskyLens–Nano system demonstrated the importance of preserving validated communication layers.

A proven serial interface used lines formatted conceptually as:

```text
ID,X,Y,W,H
```

and a working EV3-side method used:

```python
nano.readline()
```

Changing that acquisition method while simultaneously modifying obstacle logic introduced unnecessary uncertainty.

The testing lesson was:

> **Freeze known-good lower layers while tuning higher layers.**

---

# 2.41 Runtime and Hardware Errors

Not every failed run represented a navigation failure.

Development also encountered ordinary implementation errors such as:

```text
NameError

UnboundLocalError

OSError / missing device

TypeError

incorrect sensor initialization
```

These should be separated from autonomous-navigation analysis.

A useful validation sequence is:

```text
1. Program starts

2. Required hardware initializes

3. Raw sensors produce plausible values

4. Motors move in correct directions

5. State transitions operate

6. Full navigation is tested
```

<div align="center">

<img
  src="../../embed/legacy_test_validation_layers.png"
  alt="Piolín software and hardware validation layers before navigation testing"
  width="850"
/>

<br>

<sub><b>Figure L2.9.</b> Basic software execution and hardware validation should occur before autonomous-navigation performance is evaluated.</sub>

</div>

---

# 2.42 The Cost of Changing Too Many Variables

One of the most significant development-method problems was modifying several parameters at once.

A new iteration might change:

```text
speed

PID / correction gain

corner angle

reverse duration

camera filter

target lock

recentering

timeout
```

Then:

```text
new version is worse
```

but there is no clear answer to:

```text
which change caused the regression?
```

This made development slower and produced many code versions with difficult-to-trace behavior.

---

# 2.43 One-Variable Testing

A better method became:

```text
KNOWN-GOOD BASELINE
        ↓
ONE CHANGE
        ↓
TEST
        ↓
OBSERVE
        ↓
IMPROVED?
   ┌────┴────┐
   │         │
  YES       NO
   │         │
 KEEP      REVERT
```

<div align="center">

<img
  src="../../embed/legacy_one_change_method.png"
  alt="Piolín one-variable-at-a-time testing methodology"
  width="850"
/>

<br>

<sub><b>Figure L2.10.</b> Later testing preserved a known-good baseline and evaluated one meaningful modification at a time.</sub>

</div>

This approach made cause-and-effect relationships much easier to identify.

---

# 2.44 Rewriting Stable Code

Another development problem was replacing large sections of working control logic to solve one isolated failure.

The pattern could become:

```text
A works
B works
C fails
      ↓
rewrite A+B+C
      ↓
C changes
but A and B regress
```

This occurred particularly when navigation logic had already completed significant portions of the track.

The stronger approach was:

```text
preserve working behavior

identify failing subsystem

modify smallest justified region
```

This reduced regression risk.

---

# 2.45 Known-Good Baselines

A code version that completes a meaningful behavior should be treated as an engineering asset.

Examples include:

```text
stable straight driving

successful corner

three-lap completion

correct pillar pass
```

A known-good version provides:

```text
comparison point

regression reference

fallback implementation
```

Version control is therefore not merely repository organization.

It is part of the experimental method.

---

# 2.46 Logs and Diagnostics

Visual observation alone was often insufficient to explain failures.

A more useful test included software output such as:

```text
current state

detected color / ID

left ultrasonic

right ultrasonic

heading when applicable

steering command

counter

target lock
```

Then a physical failure could be compared with the program's internal interpretation.

For example:

```text
robot went left around Red
```

with log:

```text
TARGET = RED
STEER_REQUEST = LEFT
```

indicates a different problem from:

```text
TARGET = GREEN
STEER_REQUEST = LEFT
```

The first suggests maneuver mapping.

The second suggests perception/state interpretation.

---

# 2.47 Test Evidence Should Be Measured, Not Invented

The repository should distinguish between:

```text
observed qualitative behavior
```

and:

```text
measured quantitative result
```

Statements such as:

```text
Green was observed to be less consistent
```

can be preserved as historical qualitative observations.

However, claims such as:

```text
Green detection accuracy = 73%
```

should only appear if a documented dataset actually produced that value.

The same applies to:

```text
success rates

run times

camera latency

corner error

sensor noise
```

No graph should imply measurements that were never collected.

---

# 2.48 Recommended Historical Test Record

A useful prototype test record can use the following structure:

| Field | Example of Information |
| :--- | :--- |
| Test ID | Sequential identifier |
| Date | Test date |
| Code version | Exact file / commit |
| Hardware configuration | Sensors and port mapping |
| Starting position | Inner / center / outer |
| Main variable changed | One parameter or behavior |
| Expected result | What should happen |
| Actual result | What physically happened |
| Internal state | Important logs |
| Diagnosis | Most likely subsystem |
| Decision | Keep / revert / retest |

This format makes each run useful even when the robot fails.

---

# 2.49 Suggested Testing Sequence

A structured development sequence for an autonomous vehicle such as Piolín is:

```text
LEVEL 1
Hardware presence
        ↓
LEVEL 2
Raw sensor values
        ↓
LEVEL 3
Motor direction
        ↓
LEVEL 4
Single subsystem
        ↓
LEVEL 5
Two-subsystem interaction
        ↓
LEVEL 6
Single track feature
        ↓
LEVEL 7
Multiple features
        ↓
LEVEL 8
Complete run
        ↓
LEVEL 9
Parking / final state
```

This hierarchy avoids testing the entire system before its individual layers are understood.

---

# 2.50 Examples of Single-Subsystem Tests

Useful isolated tests include:

### Steering

```text
center
→ left
→ center
→ right
→ center
```

Observe repeatability.

### Ultrasonics

Place Piolín at known relative wall positions and compare readings.

### Color Sensor

Cross Blue and Orange landmarks independently.

### Camera

Present Red and Green targets at several positions without autonomous steering.

### Propulsion

Drive a fixed command on a simple straight section.

These tests isolate behavior before sensor fusion is introduced.

---

# 2.51 Integration Tests

Once individual systems behave correctly, paired integration can be tested.

Examples include:

```text
Ultrasonics + steering

Color + corner state

Camera + steering

Camera + ultrasonic safety

Gyro + steering
```

Only then should the robot move toward complete multi-state autonomous runs.

This testing order makes it much easier to identify which new interaction caused a regression.

---

# 2.52 The Most Repeated Global Failure Pattern

Across many Piolín versions, one pattern appeared repeatedly:

```text
sensor detects error
      ↓
controller reacts strongly
      ↓
vehicle crosses desired state
      ↓
another sensor/controller reacts
      ↓
opposite correction
      ↓
vehicle crosses again
      ↓
oscillation / zig-zag
```

<div align="center">

<img
  src="../../embed/legacy_global_failure_pattern.png"
  alt="Repeated Piolín overcorrection and controller-conflict failure pattern"
  width="870"
/>

<br>

<sub><b>Figure L2.11.</b> A recurring development failure involved strong corrections triggering opposing corrections from another sensor or controller.</sub>

</div>

The long-term solution was not simply:

```text
add another correction
```

but:

```text
simplify controller roles

reduce unnecessary authority overlap

use state-dependent priorities

improve physical calibration
```

---

# 2.53 Open Challenge Lessons

Historical Open testing eventually clarified useful sensor responsibilities.

The current architecture moved toward:

```text
ULTRASONICS
→ lateral geometry


GYRO
→ vehicle orientation


COLOR
→ course progress / direction


MOTOR ENCODER
→ motion reference
```

This separation is much cleaner than asking one sensor or one mathematical controller to solve every part of navigation.

The current Open use of a gyro also reflects historical testing showing that timed or purely geometric corner completion could be inconsistent.

---

# 2.54 Obstacle Challenge Lessons

Obstacle testing produced a similar separation of responsibilities.

The later architecture moved toward:

```text
VISION
→ identify relevant pillar and passing objective


ULTRASONICS
→ wall safety, physical context, pass confirmation, recovery


COLOR
→ course progress


ENCODER
→ relative vehicle movement
```

This was a direct response to earlier situations where:

```text
camera

wall controller

recenter logic

safety logic
```

all attempted to steer simultaneously.

---

# 2.55 Why the Current Architecture Became More Modular

A major result of prototype testing was that Piolín improved when subsystem roles became more explicit.

Instead of:

```text
every sensor influences steering at all times
```

the architecture moved toward:

```text
each state has a primary information source
```

For example:

```text
OPEN STRAIGHT
→ US + gyro


OPEN CORNER
→ corner state + gyro + geometry


OBSTACLE APPROACH
→ vision


OBSTACLE PASS
→ vision + physical context


RECOVERY
→ lateral US
```

This reduces ambiguity and makes debugging easier.

---

# 2.56 Why the HuskyLens Architecture Was Eventually Replaced

The HuskyLens stage should not be summarized as:

```text
camera failed
```

because that would ignore the useful results it produced.

The more accurate analysis is:

```text
Husky could identify colors
```

but dynamic track testing revealed a combined burden of:

```text
false detections

Green instability

lighting sensitivity

field-of-view limitations

target loss

multiple-target ambiguity

target-lock management

Nano bridge

USB communication

additional debugging layers
```

The transition to Pixy2.1 therefore represented both:

```text
perception redesign
```

and:

```text
architecture simplification
```

---

# 2.57 Why the Front Ultrasonic Was Eventually Removed

Earlier versions used or explored a frontal ultrasonic sensor.

Testing showed that every EV3 input had significant value.

The final architecture needed specialized information from:

```text
gyro during Open
```

and:

```text
Pixy during Obstacles
```

while still retaining:

```text
S2 left US

S3 right US

S4 Color
```

The front ultrasonic was therefore removed as part of a systems-level port-allocation decision.

This is an example of testing leading to **hardware removal rather than hardware addition**.

---

# 2.58 Why Testing Led Back to the Gyro

The gyro appeared in different stages of Piolín development and was also removed during some architectures.

Historical Open testing continued to show that the vehicle benefited from a direct orientation reference for:

```text
heading stabilization

turn progress

corner completion
```

The current Open architecture therefore reintroduced the gyro on S1.

This demonstrates that engineering evolution is not always linear.

A component can be:

```text
tested
→ removed
→ reconsidered
→ returned in a more appropriate architecture
```

---

# 2.59 Why Pixy2.1 Could Return After Earlier Pixy Experiments

The same principle applies to Pixy.

Earlier Pixy experiments do not represent the current architecture.

Later development clarified that the required vision information included:

```text
signature

X

Y

width

height
```

and that a shorter communication path would be valuable.

The current Pixy2.1 architecture therefore revisited a previously explored technology under different requirements and integration conditions.

---

# 2.60 Current vs. Historical Testing Context

The following distinctions are important when reading historical test notes.

| Historical Element | Current Status |
| :--- | :--- |
| HuskyLens | Legacy |
| Arduino Nano | Legacy |
| Husky → Nano → USB | Legacy |
| Front ultrasonic | Not current |
| Three-ultrasonic configurations | Legacy |
| Diagonal ultrasonic layouts | Legacy |
| S2/S3 reversed mappings | Not current |
| Gyro-free Open concepts | Historical |
| Current Open gyro | Current |
| Current Pixy2.1 direct S1 | Current Obstacles |
| S2 LEFT / S3 RIGHT | Current |
| Motor A drive / Motor B steering | Current |

This prevents historical observations from being confused with present hardware instructions.

---

# 2.61 Lessons About Engineering Method

The most valuable legacy testing lessons were methodological.

### Verify the physical robot before changing code

```text
hardware first
software second
```

### Test one layer at a time

```text
sensor
→ communication
→ interpretation
→ control
→ physical motion
```

### Preserve known-good versions

Do not destroy a stable baseline while fixing an unrelated problem.

### Change one meaningful variable at a time

Otherwise cause and effect become unclear.

### Use physical feedback

A timer is not the same as a measured physical state.

### Separate controller responsibilities

More simultaneous corrections can produce less control.

### Distinguish recognition from navigation

Seeing the correct target does not guarantee the correct trajectory.

### Record failures

A failed run is useful if its state, configuration, and cause can be analyzed.

---

# 2.62 Failure Analysis Matrix

A condensed historical diagnostic matrix is:

| Symptom | Possible Perception Cause | Possible Control Cause | Possible Hardware Cause |
| :--- | :--- | :--- | :--- |
| Wrong pillar side | Wrong ID / stale target | Sign/mapping error | — |
| No pillar response | Target not detected | State rejected detection | Camera/communication |
| Zig-zag | Intermittent target | Controllers fighting | Steering play |
| Late avoidance | Late target visibility | Excess confirmation | FOV/mount |
| Hits wall after pass | — | Recovery incorrect | US orientation |
| Double corner count | — | Event latch missing | Color positioning |
| Wide corner | — | Weak/late steering | Steering mechanics |
| Tight corner | — | Excess steering | Steering mechanics |
| Different start behavior | — | Initial error too large | Different placement |
| Sensor appears reversed | — | Port interpretation | S2/S3 wiring |
| Slow vehicle | — | Low command | Battery/drivetrain friction |

The matrix is not intended to automatically diagnose every failure.

It demonstrates why several subsystem hypotheses should be checked before changing code.

---

# 2.63 Legacy Evidence and Quantitative Claims

Many historical observations were qualitative because the development priority was achieving working competition behavior under significant time constraints.

The repository should preserve those observations honestly.

It should not retroactively invent:

```text
success percentages

precision values

latency values

mean error

standard deviation
```

for tests where those measurements were not collected.

If real logs or videos allow those values to be reconstructed later, they may be added with a clear methodology.

Until then:

```text
observed repeatedly
```

should remain distinct from:

```text
measured statistically
```

---

# 2.64 Recommended Future Testing Standard

The lessons from this legacy period suggest a stronger testing standard for the current robot.

A test should ideally record:

```text
date

hardware configuration

software version / commit

battery condition

track setup

starting position

parameter changed

expected behavior

actual behavior

important sensor logs

result

next action
```

The development sequence should then be:

```text
BASELINE
   ↓
HYPOTHESIS
   ↓
ONE CHANGE
   ↓
CONTROLLED TEST
   ↓
DATA
   ↓
DECISION
```

<div align="center">

<img
  src="../../embed/testing_workflow.png"
  alt="Current recommended Piolín engineering testing workflow"
  width="870"
/>

<br>

<sub><b>Figure L2.12.</b> Legacy experience informed a more controlled testing methodology for current Piolín development.</sub>

</div>

---

# 2.65 How Legacy Testing Shaped the Current Robot

The current Piolín architecture reflects many direct conclusions from these experiments.

### Two fixed lateral ultrasonics

```text
S2 = LEFT

S3 = RIGHT
```

because lateral geometry is easier to interpret consistently than several changing ultrasonic layouts.

### Modular S1

```text
OPEN
→ Gyro


OBSTACLES
→ Pixy2.1
```

because the most useful specialized sensor changes by round.

### No permanent front ultrasonic

EV3 port allocation favored more valuable round-specific information.

### No HuskyLens + Nano bridge

The current vision architecture uses a shorter communication path.

### Color Sensor casing

Physical control of lighting improved measurement conditions.

### State-dependent control

Different navigation phases assign clearer responsibilities to different sensors.

### Stronger version discipline

Known-good behavior is preserved while isolated changes are tested.

---

# 2.66 Final Engineering Analysis

The most important result of Piolín's prototype-testing period was not a single set of parameters.

It was a better model of how the robot should be engineered.

Early development often treated failures as isolated software problems:

```text
robot turns wrong
→ change steering


camera misses target
→ add filter


robot oscillates
→ add another correction
```

Repeated testing showed that these failures were frequently interactions between multiple layers.

A more accurate model became:

```text
PHYSICAL ENVIRONMENT
        ↓
SENSORS
        ↓
PERCEPTION / GEOMETRY
        ↓
STATE
        ↓
CONTROL PRIORITY
        ↓
MOTOR COMMAND
        ↓
MECHANICAL RESPONSE
        ↓
NEW PHYSICAL STATE
        └───────────────┐
                        │
                        └── feedback to sensors
```

<div align="center">

<img
  src="../../embed/legacy_system_feedback_loop.png"
  alt="Piolín complete sensing control mechanical feedback loop"
  width="900"
/>

<br>

<sub><b>Figure L2.13.</b> Piolín's behavior is produced by a closed interaction between environment, sensing, software state, control decisions, and mechanical response.</sub>

</div>

This explains several recurring development patterns.

A camera problem could become a steering problem.

A steering problem could become a camera FOV problem.

A mechanical alignment problem could appear to be a wall-controller problem.

A port-mapping error could appear to be a mathematical error.

A strong wall controller could prevent a correct obstacle controller from performing its maneuver.

The strongest engineering improvement was therefore not simply adding more code.

It was learning to simplify and separate responsibilities.

The final historical lesson can be summarized as:

> **Piolín became more reliable when testing moved from repeatedly changing symptoms to identifying the physical subsystem responsible for each behavior, preserving known-good baselines, modifying one variable at a time, and assigning clear control authority according to navigation state.**

The legacy prototypes remain in the repository because they demonstrate the experimental process through which these conclusions were discovered.

---

<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
