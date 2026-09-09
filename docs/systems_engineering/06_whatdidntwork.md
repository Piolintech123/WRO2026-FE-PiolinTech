# 6. What Did Not Work — Failed Approaches and Engineering Lessons

<div align="center">

<img
  src="../../v-photos/v4/piolin_obstacle_isometric.jpg"
  alt="Piolín in its current Obstacle Challenge configuration after several design iterations"
  width="720"
/>

<br>

<sub><b>Figure 6.1.</b> Piolín's current architecture was reached through multiple prototypes, rejected approaches, partial successes, and redesigns.</sub>

</div>

Piolín was not developed through a straight sequence in which every new idea immediately improved the robot.

Several approaches:

```text
worked only in controlled situations

introduced new problems

became too difficult to maintain

were replaced by simpler architectures

or revealed that the original problem had been diagnosed incorrectly
```

These unsuccessful or superseded approaches are important engineering evidence.

A failed test can reveal:

```text
which assumption was wrong

which subsystem actually caused the problem

which information the robot was missing

which architecture was unnecessarily complex
```

For this reason, PiolínTech does not erase unsuccessful development from the engineering record.

The project distinguishes between:

```text
FAILED APPROACH
→ did not provide the required behavior

PARTIAL APPROACH
→ demonstrated a useful idea but had important limitations

LEGACY APPROACH
→ previously useful but replaced by the current architecture
```

The objective of documenting these cases is not to present failure as success.

It is to show how each problem contributed to the current Piolín design.

---

## 6.1 Earlier Vision Architecture: HuskyLens + Arduino Nano

One of the largest architecture changes occurred in obstacle perception.

An earlier configuration used:

```text
HuskyLens
      ↓
Arduino Nano
      ↓
EV3
```

The architecture was useful because it allowed PiolínTech to experiment with:

```text
colored-object detection

external vision sensors

communication between processors

Red / Green obstacle logic
```

However, it introduced several layers that all had to work correctly.

The complete chain was effectively:

```text
CAMERA DETECTION
      ↓
HUSKYLENS OUTPUT
      ↓
ARDUINO PROCESSING
      ↓
COMMUNICATION LINK
      ↓
EV3 PARSING
      ↓
NAVIGATION
```

This increased the number of locations where a perception failure could originate.

A problem visible at the vehicle level could come from:

```text
camera classification

camera field of view

Arduino code

communication

EV3 interpretation

steering logic
```

The additional hardware also complicated reproducibility.

### Engineering lesson

More components do not automatically produce a more capable system.

Each additional device introduces:

```text
another electrical interface

another software layer

another communication protocol

another possible failure point
```

### Current decision

The active Obstacle Challenge architecture now uses:

```text
Pixy2.1
→ EV3 S1
```

directly.

The HuskyLens + Nano system remains valuable as **legacy engineering history**, but it is no longer part of the current competition architecture.

---

## 6.2 Trying to Keep Too Many Sensors Active

During development, several configurations attempted to obtain more information by combining or exchanging:

```text
camera

gyro

lateral ultrasonics

front ultrasonic

Color Sensor
```

The idea was understandable:

```text
more sensors
→ more information
→ better navigation
```

but in practice, additional sensors also required:

```text
available ports

mounting space

software drivers

data fusion

clear controller responsibility
```

This became particularly important around S1.

Piolín eventually needed two different types of information:

```text
OPEN
→ heading information
```

and:

```text
OBSTACLES
→ forward visual perception
```

Trying to maintain every possible sensor simultaneously created unnecessary architectural pressure.

### Engineering lesson

Sensor value should be evaluated by:

```text
How useful is this information for the current round?
```

rather than:

```text
Can we physically add another sensor?
```

### Current decision

Piolín now uses two deliberate configurations:

```text
OPEN

S1 → Gyro
S2 → LEFT US
S3 → RIGHT US
S4 → Color
```

and:

```text
OBSTACLES

S1 → Pixy2.1
S2 → LEFT US
S3 → RIGHT US
S4 → Color
```

The Gyro Sensor and Pixy2.1 are never treated as simultaneously active in the current architecture.

<div align="center">

<img
  src="../../v-photos/v4/s1_open_gyro.jpg"
  alt="Current Piolín Open configuration using the Gyro Sensor on S1"
  width="640"
/>

<br>

<sub><b>Figure 6.2.</b> Open now dedicates S1 to heading sensing rather than attempting to maintain the Obstacle vision configuration simultaneously.</sub>

</div>

<div align="center">

<img
  src="../../v-photos/v4/s1_obstacle_pixy.jpg"
  alt="Current Piolín Obstacle configuration using Pixy2.1 on S1"
  width="640"
/>

<br>

<sub><b>Figure 6.3.</b> Obstacles deliberately replaces the Gyro Sensor with Pixy2.1 because obstacle identity becomes the more valuable measurement.</sub>

</div>

---

## 6.3 Changing Left and Right Sensor Meaning in Software

Another dangerous development problem was inconsistent left/right interpretation.

An early prototype contained ultrasonic variable naming that did not match the physical convention eventually adopted by the robot.

This demonstrated a serious systems problem:

```text
correct sensor measurement
+
incorrect physical identity
=
incorrect steering
```

A controller can be mathematically correct and still send Piolín toward the wrong wall if:

```text
LEFT
```

and:

```text
RIGHT
```

are interpreted inconsistently.

The same risk becomes even larger when navigation concepts such as:

```text
inner

outer
```

change according to course direction.

### What did not work

Allowing physical sensor identity and logical navigation role to become mixed together.

### Engineering lesson

Physical identity must remain immutable.

```text
LEFT
```

should always mean the physical left side of Piolín.

```text
RIGHT
```

should always mean the physical right side.

Only logical roles such as:

```text
inner

outer
```

should change.

### Current decision

The permanent convention is:

```text
S2 = LEFT

S3 = RIGHT
```

across:

```text
hardware

software

telemetry

documentation

testing
```

<div align="center">

<img
  src="../../v-photos/v4/PiolinUSlabeling.png"
  alt="Current Piolín S2 left and S3 right ultrasonic convention"
  width="700"
/>

<br>

<sub><b>Figure 6.4.</b> The current fixed sensor convention removes ambiguity between physical sensor location and direction-dependent navigation roles.</sub>

</div>

---

## 6.4 Simple Wall Reactions and Excessive Zig-Zag

An early wall-control idea can be represented as:

```text
too close to wall
→ steer away

too far from wall
→ steer toward wall
```

This is attractive because it is simple.

However, a moving Ackermann vehicle is not described completely by one instantaneous wall distance.

Piolín can be:

```text
at the correct distance but angled toward the wall

temporarily displaced but already correcting

inside a corner where the normal wall relationship has changed
```

A highly reactive threshold controller can therefore produce:

```text
LEFT correction
      ↓
overshoot
      ↓
RIGHT correction
      ↓
overshoot
      ↓
LEFT correction
```

which appears physically as:

```text
zig-zag
```

### What did not work

Treating every ultrasonic error as an immediate independent steering request.

### Engineering lesson

The wall system needs to distinguish:

```text
position

trajectory trend

geometry validity

physical danger
```

rather than reducing all four to one threshold.

### Current direction

The newer controller uses concepts such as:

```text
short ultrasonic filtering

two-sensor geometry

deadband

nonlinear correction

geometry confidence

steering smoothing
```

and separates:

```text
NORMAL WALL CONTROL
```

from:

```text
CRITICAL WALL SAFETY
```

The result is a more structured controller in which ordinary centering and emergency escape no longer represent the same behavior.

---

## 6.5 Allowing Normal Wall Control to Fight Pillar Avoidance

One of the most important obstacle-control lessons came from behavior that initially looked like incorrect Red/Green steering.

Consider:

```text
RED
→ required PASS RIGHT
```

If the obstacle controller correctly requests:

```text
RIGHT
```

but normal wall control simultaneously requests:

```text
LEFT
```

then combining both can produce:

```text
RIGHT + LEFT
→ weak command
```

or even unstable steering.

From outside the robot, this can look like:

```text
the camera got Red wrong
```

when the actual camera classification was already correct.

### What did not work

Allowing several navigation controllers to retain full steering authority simultaneously.

### Engineering lesson

A correct subsystem can still fail at the vehicle level when another correct subsystem is solving a different problem at the same time.

This is a **systems interaction failure**, not necessarily a sensor failure.

### Current decision

Piolín uses state-dependent authority.

```text
NORMAL
→ wall geometry has strong authority
```

```text
AVOID
→ pillar trajectory has strong authority
```

```text
CORNER
→ corner trajectory has strong authority
```

while:

```text
critical wall safety
```

can remain available independently.

This led directly to the current controller-arbitration architecture.

---

## 6.6 Direct Camera-to-Steering Logic

A tempting early obstacle strategy is:

```text
camera sees Green
→ steer left

camera sees Red
→ steer right
```

or even:

```text
pillar appears left in image
→ steer left
```

These rules are too direct for the complete maneuver.

The robot does not need to drive toward the colored block.

It must:

```text
identify obstacle

select required passing side

approach

move around it

confirm that it has been passed

recover
```

The camera also moves with Piolín.

During steering:

```text
chassis rotates
      ↓
camera rotates
      ↓
pillar x changes
```

even though the pillar remains stationary on the course.

### What did not work

Treating camera coordinates as direct Motor B commands without enough state or target context.

### Engineering lesson

Vision should answer:

```text
What do I see?

Where do I see it?
```

The navigation system should answer:

```text
What should I do about it?
```

### Current decision

The architecture now separates:

```text
PIXY DETECTION
      ↓
TARGET SELECTION
      ↓
STATE MACHINE
      ↓
OBSTACLE CONTROLLER
      ↓
ARBITRATION
      ↓
MOTOR B
```

The camera belongs to perception, not directly to actuation.

---

## 6.7 Using Image Position to Decide Red/Green Passing Side

Another dangerous interpretation is:

```text
pillar appears left
→ pass left
```

and:

```text
pillar appears right
→ pass right
```

This does not correspond to the competition rule.

The same Red pillar may appear:

```text
left of camera center

centered

right of camera center
```

depending on Piolín's current trajectory.

Its required side never changes.

### What did not work

Allowing camera perspective to determine competition behavior.

### Engineering lesson

Two different pieces of camera information must remain separate:

```text
SIGNATURE
→ object identity
```

and:

```text
X / Y
→ image geometry
```

### Current decision

The mapping is fixed:

```text
sig2
→ RED
→ PASS RIGHT
```

```text
sig3
→ GREEN
→ PASS LEFT
```

Image geometry may affect:

```text
reaction strength

target relevance

maneuver progression
```

but never reverses the required passing side.

---

## 6.8 Selecting the First Camera Block

Another simple implementation is:

```python
target = blocks[0]
```

This can work when:

```text
only one pillar is visible
```

but becomes unreliable when:

```text
a near pillar

and a distant pillar
```

appear simultaneously.

Camera return order is not necessarily the same as physical relevance.

A distant Green block could otherwise replace a nearby Red obstacle simply because it appears first in a returned list.

### What did not work

Using camera list order as navigation priority.

### Engineering lesson

```text
VISIBLE
```

does not mean:

```text
CURRENT TARGET
```

The system needs a selection layer.

### Current direction

The intended process is:

```text
READ BLOCKS
      ↓
VALIDATE
      ↓
BUILD CANDIDATES
      ↓
EVALUATE RELEVANCE
      ↓
CONFIRM
      ↓
LOCK
```

Possible relevance information includes:

```text
signature

x

y

width

height

current state

previous target
```

The final numerical relevance equation is still being calibrated, but the original:

```text
first block wins
```

strategy is no longer considered sufficient.

---

## 6.9 Releasing a Pillar as Soon as the Camera Loses It

During obstacle avoidance, Piolín rotates.

As it turns:

```text
camera orientation changes
```

and the pillar can leave the field of view before the vehicle has physically passed it.

A strategy such as:

```text
target disappeared
→ obstacle finished
```

can therefore cause:

```text
avoidance begins

camera loses pillar

recovery begins immediately

Piolín turns back toward the pillar
```

### What did not work

Using one missing camera observation as proof of physical clearance.

### Engineering lesson

```text
NOT VISIBLE
```

is not the same event as:

```text
PASSED
```

### Current decision

The architecture introduces:

```text
TARGET LOCK

PASS_CONFIRM

RECOVER
```

as separate phases.

Temporary visual loss can be combined with:

```text
recent Pixy history

S2/S3 physical geometry

current maneuver side

vehicle progression
```

before the obstacle is released.

This creates a more physically meaningful transition from avoidance to recovery.

---

## 6.10 Direct Single-Sample Floor Detection

The same event problem appeared with the S4 Color Sensor.

One physical marking may produce:

```text
BLUE
BLUE
BLUE
BLUE
```

across several control cycles.

Counting each reading would produce:

```text
4 events
```

instead of:

```text
1 physical event
```

A second problem occurs near the edge of a marking:

```text
BLUE
NONE
BLUE
```

which can incorrectly appear to be two separate lines.

### What did not work

Treating every classified color reading as a new course event.

### Engineering lesson

A continuous sensor signal must be converted into a discrete event lifecycle.

### Current decision

Piolín's prototypes developed mechanisms including:

```text
candidate confirmation

event lock

neutral-floor release

minimum Motor A encoder separation
```

so that the intended relationship becomes:

```text
one physical marking
→ one confirmed course event
```

This lesson later influenced Pixy target handling as well.

The same general pattern:

```text
CANDIDATE
→ CONFIRM
→ LOCK
→ RELEASE
```

is now reused across multiple perception systems.

---

## 6.11 Purely Timed Turns and Parking Movements

Timed movement was useful during early prototypes because it provided an easy way to test whether Piolín could physically execute a maneuver.

Examples include:

```text
steer

drive for fixed time

center
```

or:

```text
parking enabled

advance for fixed time

stop
```

These tests were useful as proofs of concept.

However, time does not directly represent:

```text
vehicle position

vehicle orientation

distance traveled
```

Two runs can differ because of:

```text
drive speed

battery behavior

entry pose

surface interaction

steering response
```

while using the same timer.

### What did not work well enough

Using elapsed time as the primary representation of physical maneuver completion.

### Engineering lesson

Whenever practical, the controller should use information related to the physical state.

### Current direction

Piolín increasingly uses:

```text
sensor events

Motor A encoder progression

S2/S3 geometry

Motor B position

Pixy target state
```

rather than time alone.

Timed actions can remain useful for:

```text
timeouts

small experimental maneuvers

safety limits
```

but are no longer treated as the strongest source of localization or maneuver completion.

---

## 6.12 Tuning Too Many Parameters at Once

One of the most damaging development patterns is changing several things after one failed run.

For example:

```text
increase steering

decrease speed

change wall gain

change target threshold

change recovery
```

in the same version.

If the next run improves:

```text
which change caused it?
```

becomes impossible to answer.

If the next run becomes worse:

```text
which change should be reverted?
```

is equally unclear.

### What did not work

Large groups of simultaneous tuning changes without an isolated hypothesis.

### Engineering lesson

Tuning is an experiment.

A useful experiment needs:

```text
controlled starting condition

one primary variable

repeatable test

observable result
```

### Current process

PiolínTech now prefers:

```text
KNOWN-GOOD BASELINE
        ↓
change one primary cause
        ↓
repeat same test
        ↓
compare
        ↓
keep or revert
```

This also reduces the chance of losing a previously successful behavior while trying to improve another one.

---

## 6.13 Full-Course Testing Too Early

A full autonomous run appears to be the most realistic test.

However, it is often a poor first test of a new controller.

Suppose Piolín fails after a Red pillar during a complete run.

The failure could originate in:

```text
target detection

target selection

pass-side mapping

avoidance strength

wall arbitration

pass confirmation

recovery

next corner
```

The complete run tells the team:

```text
something failed
```

but not necessarily:

```text
what failed first
```

### What did not work efficiently

Using the full track as the primary debugging environment for every new change.

### Engineering lesson

Complex behaviors should be decomposed before they are integrated.

### Current testing strategy

Development progresses through:

```text
sensor test

motor test

straight test

single corner

single Red pillar

single Green pillar

recovery

consecutive pillars

parking phases

complete parking

full course
```

<div align="center">

<img
  src="../../v-photos/v4/full_track.jpg"
  alt="Full track used only after subsystem behaviors are tested"
  width="740"
/>

<br>

<sub><b>Figure 6.5.</b> Full-course runs remain essential, but they are most informative after the individual behaviors involved in the run have already been isolated and tested.</sub>

</div>

The full course is now treated primarily as an **integration test**, not the first debugging tool.

---

## 6.14 Outdated Measurements and Architecture Descriptions

Piolín changed physically throughout development.

As a result, older values and descriptions can become incorrect even if they were accurate for an earlier version.

Examples of information that can become stale include:

```text
overall dimensions

mass

wheel dimensions

sensor positions

camera position

port mapping
```

A repository risk appears when an old value is copied into a current document simply because it already exists.

### What did not work

Treating previous measurements as permanently valid after the robot changed.

### Engineering lesson

Documentation must distinguish:

```text
CURRENT

LEGACY

NEEDS REMEASUREMENT
```

just as software distinguishes active and legacy code.

### Current decision

PiolínTech does not publish old dimensional values as current specifications without remeasurement.

Likewise, the current hardware architecture always uses:

```text
S2 = LEFT

S3 = RIGHT
```

and the round-specific S1 configuration.

Legacy hardware descriptions are preserved separately rather than mixed into the current wiring documentation.

---

## 6.15 What the Failed Approaches Changed

The most important result of unsuccessful testing is the architecture that followed from it.

| Earlier / Problematic Approach | Limitation Observed | Current Engineering Response |
| :--- | :--- | :--- |
| HuskyLens + Nano active architecture | Additional hardware and communication complexity | Direct Pixy2.1 → EV3 |
| Trying to support every sensor simultaneously | Port and integration complexity | Round-specific S1 |
| Ambiguous US left/right roles | Controller inversion risk | Fixed `S2 LEFT`, `S3 RIGHT` |
| Threshold-only wall reactions | Zig-zag / weak geometric understanding | Geometric wall controller |
| Wall controller always strong | Fought obstacle trajectory | State-dependent authority |
| Direct camera-to-steering | Camera motion affected trajectory decisions | Perception separated from control |
| Image x determines pass side | Perspective could reverse rule | Signature determines Red/Green rule |
| First Pixy block selected | Wrong target could dominate | Relevance-based target selection |
| Release target on camera loss | Recovery could begin before pass | `PASS_CONFIRM` |
| Count every S4 sample | Duplicate course events | Confirmation + latch + release |
| Time-based maneuver completion | Weak physical relationship | Sensor/encoder-based evidence |
| Many tuning changes together | Cause of improvement unclear | One-variable controlled iteration |
| Full course as first test | Difficult failure isolation | Subsystem tests before integration |
| Reusing old measurements | Documentation drift | Remeasure current robot |

These changes demonstrate that unsuccessful approaches were not isolated mistakes.

They produced design requirements that now appear throughout Piolín's current system.

---

## 6.16 From Failure to Architecture

The complete learning process can be represented as:

```text
                    OBSERVED FAILURE
                           │
                           ▼
                    FIRST ASSUMPTION
                           │
                           ▼
                     CONTROLLED TEST
                           │
                           ▼
                ASSUMPTION CORRECT?
                    /             \
                  YES              NO
                   │                │
                   ▼                ▼
            modify subsystem   inspect earlier layer
                   │                │
                   └────────┬───────┘
                            ▼
                      NEW HYPOTHESIS
                            │
                            ▼
                        TEST AGAIN
                            │
                            ▼
                     REPEATABLE RESULT?
                       /           \
                     NO             YES
                     │               │
                     ▼               ▼
                  iterate        keep change
                                     │
                                     ▼
                              document decision
                                     │
                                     ▼
                             integrate with system
```

Several major Piolín improvements followed this pattern.

The visible symptom was often not the actual root cause.

For example:

```text
"Red goes to the wrong side"
```

could originate from:

```text
signature interpretation

controller arbitration

steering sign

Motor B response
```

rather than from the camera itself.

Likewise:

```text
"Piolín hits the wall after a pillar"
```

could result from:

```text
late pass confirmation

weak recovery
```

rather than from obstacle avoidance being too strong.

This root-cause approach became increasingly important as the software architecture grew.

---

## 6.17 Final Engineering Assessment

Piolín's unsuccessful approaches are part of the engineering result, not material that should be removed from the project's history.

They reveal several recurring lessons.

### More hardware is not automatically better

The earlier multi-device vision architecture showed that additional processors and communication layers can increase uncertainty as quickly as they increase capability.

### More controller strength is not always the solution

Several trajectory problems resulted from controllers fighting each other rather than one controller being too weak.

### Missing information and wrong interpretation are different failures

The camera can correctly identify Red while a later software layer still produces a left trajectory.

### A sensor observation is not automatically a physical event

This applies to:

```text
floor lines

camera targets

pillar loss

parking references
```

and led to confirmation, locking, and release logic.

### Timers are useful but limited

They can create simple prototypes, but physical sensors and encoder progression usually provide stronger evidence of maneuver completion.

### Full-course testing is an integration tool

Subsystem failures are easier to diagnose when each behavior is isolated first.

### Documentation can also become technically wrong

Legacy values and architectures must be preserved as history without being presented as the current robot.

The evolution can therefore be summarized as:

```text
simple reactions
        ↓
unexpected interactions
        ↓
failure isolation
        ↓
clearer subsystem responsibilities
        ↓
state-based behavior
        ↓
controller arbitration
        ↓
sensor fusion
        ↓
repeatable testing
```

The central lesson from PiolínTech's unsuccessful development paths is:

> **An approach is valuable even when it is replaced if it reveals a limitation, disproves an assumption, or leads to a clearer architecture. The objective is not to avoid failed experiments; it is to ensure that each failed experiment changes what the team understands about the system.**

Piolín's current architecture is therefore not simply the collection of ideas that worked immediately.

It is the result of identifying which ideas were:

```text
too reactive

too ambiguous

too complex

too dependent on timing

too difficult to reproduce

or solving the wrong layer of the problem
```

and replacing them with designs whose responsibilities can be explained, tested, and traced more clearly.

---

<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
