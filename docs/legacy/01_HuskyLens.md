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

The HuskyLens vision system represented one of the most important experimental stages in Piolín's Obstacle Challenge development. It was introduced because the LEGO sensors already installed on the vehicle could provide information about walls and floor markings, but they could not identify the color of the traffic pillars that determine the required passing side.

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

The HuskyLens demonstrated that forward visual perception could provide the obstacle identity required by the robot. However, moving-track testing exposed limitations that were much less obvious during stationary camera tests.

These included:

```text
false detections

inconsistent Green recognition

lighting sensitivity

limited useful field of view

target loss during steering

multiple visible blocks

target-lock management

communication complexity
```

The system was therefore not abandoned because it could not recognize the competition colors.

**It could recognize them.**

The larger problem was obtaining sufficiently consistent autonomous behavior while perception, communication, steering, and vehicle motion were all interacting.

---

# 1.1 Why Vision Was Required

The ultrasonic sensors could provide information such as:

```text
left-side distance

right-side distance

wall proximity

track geometry
```

but they could not determine whether a pillar was Red or Green.

Two pillars could occupy approximately the same position while requiring opposite maneuvers.

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

This established an important separation of sensor roles:

```text
VISION
→ What obstacle is present?


ULTRASONICS
→ What geometry surrounds the robot?


EV3
→ What maneuver should be executed?
```

This principle remained relevant even after HuskyLens itself was replaced.

---

# 1.2 Historical Hardware Architecture

The main historical HuskyLens configuration used an **Arduino Nano** as an intermediate communication bridge.

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

The EV3 remained Piolín's main controller.

The Nano did **not** decide how Piolín should drive around a pillar. Its role was to transfer useful vision information from HuskyLens to the EV3.

This architecture allowed the team to experiment with external vision without replacing the LEGO controller already responsible for propulsion and steering.

---

# 1.3 Role of the Arduino Nano

The information path was:

```text
HuskyLens
→ visual detection


Arduino Nano
→ receives camera information


USB Serial
→ transports formatted data


EV3
→ interprets obstacle


Motor B
→ executes steering response
```

This architecture created an important systems-engineering consequence:

```text
HuskyLens sees pillar
```

did **not** automatically mean:

```text
EV3 received correct pillar information
```

Several communication and software stages existed between those two events.

---

# 1.4 Historical Detection Mapping

The historical identification convention was:

| HuskyLens ID | Competition Target | Required Behavior |
| :---: | :--- | :--- |
| **1** | Green pillar | Pass on the left |
| **2** | Red pillar | Pass on the right |

The complete interpretation chain became:

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

A failure at any stage could produce incorrect vehicle behavior even if the camera had classified the color correctly.

---

# 1.5 Historical Communication Format

One tested communication approach transmitted detections in the format:

```text
ID,X,Y,W,H
```

where:

```text
ID
→ learned HuskyLens identity


X
→ horizontal image position


Y
→ vertical image position


W
→ detected block width


H
→ detected block height
```

On the EV3 side, one communication method that had already been demonstrated to work during this development stage used:

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
formatted line
      ↓
USB Serial
      ↓
nano.readline()
      ↓
EV3 parser
```

The important point was not the formatting itself.

It was that the perception system depended on a complete communication chain before the EV3 could use the detection.

---

# 1.6 A Communication-Layer Lesson

Once:

```python
nano.readline()
```

was operating reliably, later experiments with more complicated reading methods introduced another variable into a system that already contained several uncertain layers.

The development pattern could become:

```text
known reader works
      ↓
reader changed
      ↓
new problem appears
      ↓
unclear source
```

The possible source could then be:

```text
camera

Nano

serial transmission

parser

navigation

steering
```

This produced an important methodological lesson:

> **When one subsystem has already been validated, keep it stable while another subsystem is being tuned unless there is a demonstrated reason to modify it.**

---

# 1.7 Detection Was Not Successful Navigation

One of the strongest conclusions from the HuskyLens stage was:

```text
CORRECT DETECTION
≠
SUCCESSFUL MANEUVER
```

The camera could correctly identify Red or Green while Piolín still failed because of:

```text
late steering

weak steering

excessive steering

vehicle speed

wall-controller interference

target loss

incorrect target lock

poor recovery timing
```

The real obstacle-navigation problem was:

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

This distinction became one of the most useful outcomes of the entire HuskyLens experiment.

---

# 1.8 False Detections

One recurring problem was detecting regions that were not the intended competition pillar.

Possible sources included:

```text
track regions

reflections

shadows

objects outside the course

similar colors

lighting changes
```

A simplified failure could occur as:

```text
Husky reports GREEN
        ↓
region is not actual pillar
        ↓
EV3 accepts detection
        ↓
avoidance begins
        ↓
vehicle leaves useful trajectory
```

This demonstrated that:

```text
valid camera ID
```

was not automatically equivalent to:

```text
relevant competition obstacle
```

The controller needed some form of contextual validation.

---

# 1.9 Filtering Trade-Off

Additional criteria were tested to reduce false detections.

Examples included:

```text
X position

Y position

block size

multiple confirmations

detection persistence
```

This created a trade-off:

| Filtering | Result |
| :--- | :--- |
| Too permissive | False targets can be accepted |
| Moderate | Better rejection of irrelevant detections |
| Too restrictive | Real pillars can be rejected |

Therefore:

```text
more filtering
```

did not automatically mean:

```text
better obstacle perception
```

The objective was to distinguish useful targets without preventing Piolín from reacting to a real obstacle.

---

# 1.10 Green Recognition

During development, Green was often observed to be less consistent than Red.

Recognition changed with factors such as:

```text
lighting

camera angle

distance

brightness

background

training conditions
```

A physically visible pillar could produce a software sequence such as:

```text
GREEN
  ↓
lost
  ↓
GREEN
  ↓
lost
  ↓
GREEN
```

To a person watching the scene, the pillar could appear continuously visible.

To the controller, those were separate detection events.

This made obstacle-state continuity difficult.

---

# 1.11 Intermittent Detection and Target Memory

A simple controller might behave as:

```text
target visible
→ avoid


target not visible
→ stop avoiding
```

With an intermittent camera signal, this could become:

```text
GREEN
→ steer left


NO TARGET
→ release


GREEN
→ steer left


NO TARGET
→ release
```

The resulting steering could oscillate.

This encouraged the introduction of **temporary target memory**.

For example:

```text
GREEN confirmed
      ↓
remember GREEN
      ↓
brief camera loss
      ↓
continue current maneuver
```

Target memory solved one problem but immediately created another:

> **When should the remembered target be released?**

---

# 1.12 Field-of-View Limitation

Camera field of view became particularly important after corners.

A typical failure sequence could be:

```text
corner completed
      ↓
Piolín remains slightly misaligned
      ↓
camera points away from next pillar
      ↓
pillar outside useful FOV
      ↓
no detection
      ↓
Piolín continues forward
      ↓
pillar finally becomes visible
      ↓
available reaction distance is smaller
```

This showed that camera reliability depended partly on the physical trajectory of the complete vehicle.

A camera can only process what enters its field of view.

Therefore post-corner alignment became part of the perception problem.

---

# 1.13 Steering Changes the Camera View

The camera was fixed to Piolín's chassis.

When the robot steered:

```text
Motor B changes wheel angles
        ↓
vehicle begins turning
        ↓
chassis rotates
        ↓
camera rotates
        ↓
pillar moves across image
```

This created an important effect:

```text
pillar leaves image
```

even though:

```text
pillar has not yet been physically passed
```

This led to one of the most important historical lessons:

> [!IMPORTANT]
> **TARGET LOST does not mean TARGET PASSED.**

---

# 1.14 Target Lost vs. Target Passed

An incorrect simplified model could behave as:

```text
detect pillar
      ↓
avoid
      ↓
pillar disappears
      ↓
straighten
```

But the real situation could instead be:

```text
detect pillar
      ↓
Piolín rotates
      ↓
pillar exits FOV
      ↓
pillar still beside vehicle
      ↓
Piolín straightens
      ↓
collision
```

This distinction forced the obstacle logic to consider evidence beyond camera visibility.

---

# 1.15 Ultrasonic Pass Confirmation

One stronger idea was to use the lateral ultrasonic sensors as physical context.

As Piolín moved beside a pillar, the relevant side sensor could observe a qualitative sequence like:

```text
normal side distance
      ↓
distance decreases
      ↓
pillar alongside vehicle
      ↓
distance increases
      ↓
pillar moving behind sensor region
```

The sensor roles could therefore become:

```text
CAMERA
→ identify pillar


LATERAL ULTRASONIC
→ help confirm physical passing
```

The exact thresholds were never universal because they depended on vehicle geometry and testing conditions.

The important contribution was the principle of **physical pass confirmation**.

---

# 1.16 Target Locking

Because visual detections could be intermittent, the controller experimented with locking the active target.

For example:

```text
RED confirmed
      ↓
LOCK = RED
      ↓
temporary visual loss
      ↓
continue RED maneuver
```

This prevented brief camera fluctuations from immediately changing the required passing side.

Target locking was useful.

Permanent locking was not.

---

# 1.17 Persistent Lock Failure

A lock could remain active after the physical obstacle was already gone.

```text
pillar 1 detected
      ↓
LOCK RED
      ↓
pillar 1 passed
      ↓
pillar 2 visible
      ↓
old lock remains active
      ↓
new pillar ignored
```

This demonstrated that the problem was no longer only:

```text
recognize target
```

It was also:

```text
manage target state
```

---

# 1.18 Target Lifecycle

A more mature interpretation separated obstacle handling into stages.

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

The development team learned that these were different concepts:

```text
visible target

selected target

remembered target

passed target

next target
```

Treating all of them as one variable created unstable behavior.

---

# 1.19 Multiple Visible Blocks

Another challenge appeared when the camera reported several candidate targets.

A rule such as:

```text
take first valid block
```

was simple, but it did not guarantee that the chosen block was the one Piolín should actually avoid.

The first block could be:

```text
farther away

smaller

near image edge

future pillar

false region
```

Therefore:

```text
FIRST BLOCK
≠
MOST RELEVANT BLOCK
```

This lesson carried directly into later Pixy2.1 target-selection work.

---

# 1.20 Target Relevance

A stronger selection concept could consider several properties:

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

This does not mean every value must always appear in one complex equation.

The important lesson was that obstacle selection should have a meaningful relationship with Piolín's current driving situation.

---

# 1.21 Camera Coordinates Were Not Physical Distance

Another important conceptual lesson was that:

```text
X

Y

W

H
```

are image-space values.

They are not automatically physical measurements.

For example:

```text
larger apparent target
```

may often suggest:

```text
target is more visually prominent / possibly closer
```

but:

```text
W = value
```

does not automatically correspond to:

```text
distance = exact centimeters
```

without calibration.

The same limitation applies to Y.

The relationship depends on:

```text
camera height

camera angle

lens geometry

pillar dimensions

vehicle orientation
```

Image coordinates should therefore be treated as relative visual information unless an empirical calibration has been performed.

---

# 1.22 External Reference Code

Piolín studied strategies from other WRO Future Engineers teams during development.

This was useful for understanding ideas such as:

```text
target filtering

position-aware steering

pillar relevance

camera-based avoidance
```

However, numerical thresholds from another robot could not simply be copied.

Reference values were tied to:

```text
another camera

another camera position

another chassis

another steering geometry

another coordinate system
```

The correct engineering principle became:

> **Reuse useful strategy concepts, but recalibrate numerical parameters for the actual Piolín system.**

---

# 1.23 Lighting Sensitivity

HuskyLens performance was influenced by the visual environment.

Important variables included:

```text
ambient brightness

shadows

reflections

camera angle

pillar illumination

background
```

This created a physical feedback relationship:

```text
vehicle turns
      ↓
camera angle changes
      ↓
background / illumination changes
      ↓
target appearance changes
      ↓
recognition may change
```

For this reason, stationary camera success was not sufficient evidence of competition reliability.

---

# 1.24 Objects Outside the Track

A forward-facing camera observes more than only competition pillars.

Its image can include:

```text
course

walls

people

colored external objects

reflections

shadows
```

HuskyLens classification alone did not inherently know:

```text
relevant object inside course
```

versus:

```text
irrelevant object elsewhere
```

This increased the importance of contextual filtering and target selection.

---

# 1.25 Static vs. Dynamic Vision Testing

Static testing helped verify that HuskyLens could classify Green and Red.

However:

```text
stationary recognition
```

was not equivalent to:

```text
dynamic obstacle navigation
```

During motion, additional variables appeared:

```text
changing viewing angle

vehicle vibration

shorter observation time

pillar movement through FOV

changing background

changing lighting
```

The correct validation environment was therefore the complete moving vehicle.

---

# 1.26 Perception Timing and Vehicle Speed

A complete reaction required several stages:

```text
pillar enters view
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
Motor B changes
      ↓
vehicle trajectory responds
```

At greater speed, Piolín travels more physical distance while those stages occur.

However, reducing speed indefinitely was also not ideal because Ackermann steering requires longitudinal motion to develop a curved trajectory.

The objective became balancing:

```text
perception time

steering response

vehicle speed

available obstacle distance
```

---

# 1.27 Camera and Wall Controllers Could Conflict

Another major issue was not exclusive to the HuskyLens itself.

The camera could request one trajectory while the wall controller requested another.

For example:

```text
GREEN
→ pass LEFT
```

while:

```text
wall correction
→ steer RIGHT
```

If both controllers had strong authority at the same time:

```text
LEFT
RIGHT
LEFT
RIGHT
```

could become:

```text
zig-zag
```

This led to an important control-system lesson:

> **Different controllers should not have equal steering authority in every navigation state.**

---

# 1.28 State-Dependent Control Priority

A stronger architecture separated control responsibility according to state.

```text
NORMAL
→ wall navigation dominant


PILLAR
→ vision establishes avoidance objective
→ ultrasonic sensing protects unsafe geometry


PASSING
→ preserve maneuver


RECENTER
→ wall geometry becomes stronger again
```

This systems-level concept was more important than any single camera threshold.

---

# 1.29 Post-Pillar Recovery

Avoiding a pillar successfully did not guarantee that Piolín was ready for the next section.

After avoidance, the robot could remain:

```text
laterally displaced

rotated

close to wall

poorly aligned for next pillar
```

This made recovery its own navigation phase.

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

The lateral ultrasonic sensors were especially useful during this phase because they provided environmental information even when the camera no longer saw the previous target.

---

# 1.30 Reverse as a Recovery Experiment

Reverse movement was also tested as a way to create more distance or time for perception.

Conceptually:

```text
approach uncertain / too close
        ↓
reverse
        ↓
target returns to useful image region
        ↓
additional reaction opportunity
```

This could help in individual cases.

However, it also introduced:

```text
more states

more timing

more steering transitions

more edge cases
```

Reverse was therefore a recovery tool, not a fundamental solution to perception instability.

---

# 1.31 More Logic Did Not Always Mean More Reliability

A repeated development pattern became:

```text
unstable detection
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
```

Each addition could fix one observed problem while making the entire system harder to reason about.

This produced another important lesson:

```text
more logic
≠
automatically more reliable
```

If the underlying perception or state model is unclear, continually adding special cases can make the controller more fragile.

---

# 1.32 Multi-Layer Debugging

The historical architecture contained a long failure chain:

```text
PHYSICAL TARGET
      ↓
HUSKYLENS
      ↓
ID / IMAGE DATA
      ↓
I2C
      ↓
ARDUINO NANO
      ↓
SERIAL MESSAGE
      ↓
USB
      ↓
EV3 READER
      ↓
EV3 PARSER
      ↓
STATE MACHINE
      ↓
STEERING REQUEST
      ↓
MOTOR B
      ↓
VEHICLE TRAJECTORY
```

A wrong physical maneuver could originate almost anywhere in this chain.

This became one of the strongest practical arguments for simplifying the later vision architecture.

---

# 1.33 The HuskyLens Screen Was Not Enough

Seeing a correct box on the HuskyLens screen did not prove that Piolín's complete vision system worked.

The correct debugging sequence was closer to:

```text
Does Husky see pillar?
        ↓
Is correct ID produced?
        ↓
Does Nano receive it?
        ↓
Does Nano transmit it?
        ↓
Does EV3 receive message?
        ↓
Does parser interpret it?
        ↓
Does state machine accept target?
        ↓
Is passing side mapped correctly?
        ↓
Does Motor B move correctly?
```

Each layer required independent verification.

---

# 1.34 Steering Errors Could Look Like Vision Errors

Suppose HuskyLens correctly identified:

```text
RED
```

but Piolín passed on the wrong side.

Possible causes included:

```text
wrong RED/RIGHT mapping

steering sign reversed

state error

controller conflict

mechanical steering problem
```

The visible behavior:

```text
camera saw Red
but robot went wrong direction
```

could easily be misdiagnosed as a camera problem.

This reinforced the need to test perception and actuation separately.

---

# 1.35 Target Selection vs. Target State

Two related but different problems emerged.

### Target selection

```text
Which visible block should Piolín use?
```

### Target state management

```text
When has the current target been completed and released?
```

The first is mainly a perception-relevance problem.

The second is mainly a state-machine problem.

Separating them made the later obstacle architecture easier to reason about.

---

# 1.36 Main Failure Categories

The historical issues can be grouped into four broad categories.

| Category | Examples |
| :--- | :--- |
| **Perception** | False detections, Green instability, lighting sensitivity |
| **Geometry** | FOV limitations, target leaving image during steering |
| **Target management** | Persistent locks, multiple targets, stale target |
| **Integration** | Nano, USB serial, EV3 reader and parser |

This is important because the decision to replace the HuskyLens architecture was based on the **combined system burden**, not one isolated problem.

---

# 1.37 Problems Not Caused Only by HuskyLens

Not every obstacle failure during this period was caused by the camera.

Other contributors included:

```text
steering sign mistakes

camera/wall controller conflict

aggressive corrections

vehicle speed

poor corner exits

mechanical steering play

changing several parameters simultaneously
```

For example:

```text
GREEN correctly identified
```

could still produce:

```text
wrong physical maneuver
```

if the steering convention itself was inverted.

Preserving this distinction makes the engineering history more accurate.

---

# 1.38 Development Methodology

During some development periods, several behaviors were changed at the same time:

```text
camera filtering

vehicle speed

wall correction

reverse logic

target locking

recenter logic

timeouts
```

If the new version failed, it became difficult to identify which modification caused the regression.

The stronger process became:

```text
stable baseline
      ↓
change ONE behavior
      ↓
test
      ↓
observe
      ↓
keep or revert
```

This lesson became useful throughout the entire Piolín project, not only in vision development.

---

# 1.39 Why the HuskyLens Stage Was Valuable

Despite its limitations, the HuskyLens stage established several requirements that later became fundamental.

It showed that Piolín needed:

```text
forward obstacle identity

target relevance

field-of-view awareness

temporary target memory

physical pass confirmation

camera/wall control arbitration

post-obstacle recovery

layered communication diagnostics
```

These discoveries were valuable precisely because they occurred through real track testing.

The prototype revealed requirements that were not obvious when the project began.

---

# 1.40 Why the Architecture Was Replaced

The final reason for replacing the HuskyLens system was not:

```text
HuskyLens cannot detect colors
```

That would be inaccurate.

A more accurate conclusion is:

> **HuskyLens could recognize the competition targets, but the complete Piolín obstacle system accumulated too much perception and integration complexity around that recognition.**

The combined burden included:

```text
false detections

Green inconsistency

lighting sensitivity

limited effective FOV

target loss during steering

multiple-target ambiguity

target-lock management

filtering trade-offs

Nano communication

USB serial

additional parsing layers
```

At the same time, Piolín increasingly needed easy access to:

```text
target identity

X

Y

width

height
```

for position-aware obstacle handling.

Pixy2.1 provided a better fit for the next development stage.

---

# 1.41 Transition to Pixy2.1

The vision architecture changed from:

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
  src="../../v-photos/v4/pixy21_front.jpg"
  alt="Current Pixy2.1 vision sensor installed on Piolín"
  width="680"
/>

<br>

<sub><b>Figure L1.1.</b> Current Pixy2.1 vision sensor that replaced the historical HuskyLens–Arduino Nano perception chain.</sub>

</div>

The change retained the useful vision role:

```text
camera
→ obstacle identity and image position
```

while reducing the number of intermediate components.

---

# 1.42 HuskyLens vs. Current Pixy2.1

| Characteristic | Legacy HuskyLens | Current Pixy2.1 |
| :--- | :--- | :--- |
| Competition status | Legacy | Current Obstacles |
| Main controller | EV3 | EV3 |
| Intermediate controller | Arduino Nano | None |
| Communication chain | Husky → Nano → USB → EV3 | Pixy → S1 → EV3 |
| Green identity | ID 1 | Signature 3 |
| Red identity | ID 2 | Signature 2 |
| Pink parking identity | Not current Husky mapping | Signature 1 |
| Image position | X/Y transmitted during development | X/Y block information |
| Image size | W/H transmitted during development | Width/height block information |
| Main historical problem | Detection consistency + integration complexity | Current system still being tuned |
| Current reconstruction use | No | Yes |

The identification conventions must never be mixed.

---

# 1.43 Critical ID Difference

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

Legacy HuskyLens identifiers must therefore not be copied directly into current Pixy logic.

---

# 1.44 Current Architecture

This file describes a historical configuration.

The current robot uses:

### Open Challenge

```text
S1 = Gyro

S2 = LEFT Ultrasonic

S3 = RIGHT Ultrasonic

S4 = Color Sensor
```

### Obstacle Challenge

```text
S1 = Pixy2.1

S2 = LEFT Ultrasonic

S3 = RIGHT Ultrasonic

S4 = Color Sensor
```

The current competition architecture does **not** use:

```text
HuskyLens

Arduino Nano

permanent front Ultrasonic Sensor
```

Any historical code or wiring described in this file should therefore remain clearly separated from current reconstruction instructions.

---

# 1.45 Lessons Carried into the Current Vision System

Several concepts discovered during HuskyLens development remain relevant.

### Detection needs context

```text
valid color
≠
automatically relevant obstacle
```

### Lost target is not passed target

```text
camera loss
≠
physical obstacle completion
```

### Target handling needs states

```text
search
→ acquire
→ validate
→ avoid
→ confirm pass
→ release
```

### Multiple blocks need selection

```text
first detection
≠
necessarily relevant detection
```

### Camera coordinates are image-space values

```text
X / Y / W / H
```

should not be interpreted as exact physical distance without calibration.

### Vision and wall control need defined authority

```text
vision
→ obstacle objective


ultrasonics
→ geometry and safety context
```

### Stable subsystems should remain stable during testing

A proven communication layer should not be rewritten while solving an unrelated steering issue without a clear reason.

---

# 1.46 Final Historical Assessment

The HuskyLens–Arduino Nano stage was an important part of Piolín's engineering development.

It demonstrated that visual identification could provide the distinction required between:

```text
GREEN
→ LEFT PASS
```

and:

```text
RED
→ RIGHT PASS
```

but moving-track operation revealed that autonomous obstacle perception required much more than color recognition.

The system also had to answer:

```text
Is this detection relevant?

Is it stable?

Which block matters?

Is this still the current pillar?

Has the pillar physically been passed?

When should target memory be released?

Did the EV3 receive the correct information?

Should vision or wall geometry control steering now?
```

The final limitation was therefore not one camera feature.

It was the accumulated interaction between:

```text
perception reliability

camera geometry

target management

communication

vehicle state

steering
```

The historical architecture can be summarized as:

```text
HUSKYLENS STAGE

target
  ↓
HuskyLens
  ↓
Arduino Nano
  ↓
USB
  ↓
EV3
  ↓
state logic
  ↓
Motor B
  ↓
vehicle
```

The current obstacle architecture reduces the perception path to:

```text
PIXY2.1 STAGE

target
  ↓
Pixy2.1
  ↓
EV3
  ↓
state logic
  ↓
Motor B
  ↓
vehicle
```

The most important conclusion is:

> **HuskyLens was capable of recognizing the competition colors, but reliable autonomous obstacle avoidance required target relevance, field-of-view awareness, robust target state, physical pass confirmation, controller priority, and simpler communication. Those lessons directly influenced Piolín's current Pixy2.1 architecture.**

The HuskyLens prototype was therefore not wasted development.

It helped define what the final vision system needed to do better.

---

<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
