# 2. Engineering Decision Log

<div align="center">

<img
  src="../../v-photos/v4/piolin_obstacle_isometric.jpg"
  alt="Piolín in its current Obstacle Challenge configuration"
  width="720"
/>

<br>

<sub><b>Figure 2.1.</b> Piolín's current architecture is the result of multiple engineering decisions involving mechanics, sensors, perception, control, and software organization.</sub>

</div>

PiolínTech maintains an engineering decision log to document **why important design choices were made**, not only what the final robot contains.

A robot can change significantly during development.

For this reason, the repository distinguishes between:

```text
CURRENT
→ used in the present architecture

LEGACY
→ tested previously but replaced

ONGOING
→ architecture selected, but numerical or algorithmic tuning is still in progress
```

Each important decision is evaluated through a common structure:

```text
PROBLEM
   ↓
ALTERNATIVES
   ↓
TESTING / OBSERVATION
   ↓
DECISION
   ↓
TRADE-OFF
   ↓
CURRENT RESULT
```

The decision log is therefore intended to preserve the reasoning behind Piolín's architecture even after old prototypes are replaced.

---

## 2.1 Decision Summary

| ID | Engineering Decision | Selected Direction | Status |
| :--- | :--- | :--- | :---: |
| `D-01` | Propulsion architecture | Motor A for rear propulsion | CURRENT |
| `D-02` | Steering architecture | Motor B with front Ackermann-style steering | CURRENT |
| `D-03` | One universal sensor configuration vs. round-specific S1 | Use two round-specific S1 configurations | CURRENT |
| `D-04` | Open Challenge S1 sensor | EV3 Gyro Sensor | CURRENT |
| `D-05` | Obstacle Challenge S1 sensor | Pixy2.1 | CURRENT |
| `D-06` | Obstacle camera architecture | Direct Pixy2.1-to-EV3 integration | CURRENT |
| `D-07` | HuskyLens + Arduino Nano | Remove from current architecture | LEGACY |
| `D-08` | Ultrasonic layout | Two permanent lateral ultrasonic sensors | CURRENT |
| `D-09` | Ultrasonic identity | S2 LEFT, S3 RIGHT | CURRENT |
| `D-10` | Wall navigation method | Geometry-based control + independent wall safety | CURRENT / ONGOING |
| `D-11` | Software behavior organization | State-based control architecture | CURRENT / ONGOING |
| `D-12` | Red/Green passing-side decision | Signature determines passing side | CURRENT |
| `D-13` | Camera target selection | Relevance + confirmation + temporary lock | ONGOING |
| `D-14` | Controller interaction | Explicit arbitration instead of unrestricted command mixing | CURRENT / ONGOING |
| `D-15` | Floor-marking processing | Confirmed events instead of raw sample counting | CURRENT |
| `D-16` | Course progression | Physical floor events rather than time alone | CURRENT |
| `D-17` | Parking activation | Course progress must enable parking before Pink can control it | CURRENT / ONGOING |
| `D-18` | Final parking movement | Sensor fusion + encoder progression instead of timing alone | ONGOING |
| `D-19` | Software environment | Separate Open and Obstacle software stacks when appropriate | CURRENT |
| `D-20` | Legacy documentation | Preserve replaced systems instead of deleting their history | CURRENT |

The numerical tuning associated with several decisions remains under development, but the architectural decisions themselves are already established.

---

# 2.2 Mobility Decisions

## D-01 — One Drive Motor for Propulsion

### Problem

Piolín requires a propulsion system capable of moving the vehicle through:

```text
straights

corners

obstacle maneuvers

parking
```

while keeping the mechanical architecture compact enough for the WRO vehicle.

### Decision

The current robot uses:

```text
Motor A
→ LEGO EV3 Large Motor
→ rear propulsion
```

### Reasoning

Separating propulsion from steering creates a vehicle architecture similar to a small automobile:

```text
Motor A
→ controls longitudinal movement

Motor B
→ controls direction
```

This makes the responsibilities of both motors easy to understand and debug.

### Trade-off

With only one drive motor, Piolín does not gain differential-drive turning capability.

The vehicle must steer by changing the front-wheel geometry and continuing to move.

### Current Result

This architecture remains active in both:

```text
Open Challenge

Obstacle Challenge
```

and creates a common mechanical base for both rounds.

---

## D-02 — Ackermann-Style Front Steering

<div align="center">

<img
  src="../../v-photos/v4/ackermann_design.png"
  alt="Piolín Ackermann-style steering design"
  width="760"
/>

<br>

<sub><b>Figure 2.2.</b> Piolín uses a mechanically linked front steering system controlled by Motor B.</sub>

</div>

### Problem

Piolín requires predictable turns while behaving as a car-like vehicle rather than rotating in place.

### Alternatives Considered

Possible general approaches included:

```text
differential-style steering

skid steering

car-like front steering
```

### Decision

Piolín uses:

```text
Motor B
→ EV3 Medium Motor
→ front Ackermann-style steering
```

### Reasoning

The chosen mechanism provides:

```text
car-like trajectory

separate steering and propulsion control

predictable relationship between steering and turning radius
```

and fits the Future Engineers vehicle concept well.

### Trade-off

Ackermann steering increases the importance of:

```text
turning radius

steering-center calibration

vehicle speed

entry position
```

The robot cannot simply rotate to correct its heading instantly.

Parking and obstacle recovery therefore require actual curved trajectories.

### Current Result

The architecture remains current and is one of the main reasons software tuning must always be evaluated on the real mechanical robot.

---

# 2.3 Round-Specific Sensor Architecture

## D-03 — Do Not Force Every Sensor Onto the Robot Simultaneously

### Problem

Piolín has different sensing priorities in the two competition rounds.

Open strongly benefits from:

```text
heading information
```

while Obstacles requires:

```text
forward color-object perception
```

Using both the Gyro Sensor and Pixy2.1 simultaneously would require a different port/integration architecture.

### Decision

PiolínTech selected **round-specific S1 configurations**.

```text
OPEN
S1 → Gyro
```

```text
OBSTACLES
S1 → Pixy2.1
```

The two are never installed simultaneously in the current architecture.

### Reasoning

This decision prioritizes the most useful sensor for the problem being solved instead of increasing hardware complexity only to maintain one universal sensor arrangement.

### Trade-off

The robot requires a configuration change between rounds.

Software must also remain aware that:

```text
Open has direct gyro heading

Obstacles does not
```

### Current Result

This has become one of the defining architectural decisions of Piolín.

---

## D-04 — Gyro Sensor for Open

<div align="center">

<img
  src="../../v-photos/v4/s1_open_gyro.jpg"
  alt="EV3 Gyro Sensor installed on Piolín for Open"
  width="660"
/>

<br>

<sub><b>Figure 2.3.</b> Open Challenge configuration uses S1 for direct heading information.</sub>

</div>

### Problem

Open testing showed that lateral distance alone does not fully describe vehicle orientation.

A robot can have a reasonable wall distance while still being angled relative to the corridor.

### Decision

Use:

```text
S1 → EV3 Gyro Sensor
```

during Open.

### Reasoning

The Gyro Sensor gives the controller an independent measurement related to heading.

The current Open architecture can therefore separate:

```text
S2/S3
→ lateral position

Gyro
→ orientation
```

### Trade-off

S1 is no longer available for Pixy during that round.

### Current Result

Open uses gyro-assisted heading stabilization together with the two lateral ultrasonics.

---

## D-05 — Pixy2.1 for Obstacles

<div align="center">

<img
  src="../../v-photos/v4/s1_obstacle_pixy.jpg"
  alt="Pixy2.1 installed on S1 for the Obstacle Challenge"
  width="660"
/>

<br>

<sub><b>Figure 2.4.</b> During Obstacles, S1 is reassigned to Pixy2.1 because visual pillar information becomes more valuable than direct gyro heading.</sub>

</div>

### Problem

The Obstacle Challenge requires Piolín to identify:

```text
Red pillar

Green pillar

Pink parking reference
```

and react differently to each.

### Decision

Use:

```text
S1 → Pixy2.1
```

during Obstacles.

### Reasoning

Pixy2.1 can provide both:

```text
color signature
```

and:

```text
image geometry
```

such as:

```text
x

y

width

height
```

which directly supports obstacle perception.

### Trade-off

There is no direct Gyro Sensor heading measurement in Obstacles.

The software must infer maneuver progress through:

```text
camera state

lateral geometry

steering state

encoder progression

state history
```

### Current Result

Pixy2.1 is the current forward-perception sensor for the Obstacle Challenge.

---

# 2.4 Vision Architecture Decisions

## D-06 / D-07 — Replace HuskyLens + Nano with Direct Pixy2.1 Integration

### Earlier Architecture

An earlier obstacle-vision architecture used:

```text
HuskyLens
      ↓
Arduino Nano
      ↓
EV3
```

This allowed PiolínTech to explore:

```text
external vision

color-object identification

communication between devices

camera-based obstacle decisions
```

### Problem Observed

The architecture introduced additional integration layers.

More components meant more possible failure points involving:

```text
camera

Arduino program

communication bridge

EV3 parser

wiring
```

The team also continued evaluating camera reliability and obstacle-color detection.

### Decision

The current architecture uses:

```text
Pixy2.1
      ↓
EV3 S1
```

directly.

### Reasoning

Removing the intermediate controller simplifies the active perception chain.

Conceptually:

```text
OLD

camera
→ Nano
→ communication
→ EV3
```

became:

```text
CURRENT

Pixy2.1
→ EV3
```

### Trade-off

Pixy still requires its own:

```text
signature calibration

mounting calibration

lighting evaluation

software interface
```

so the change does not eliminate vision engineering.

It removes an unnecessary active integration layer.

### Current Result

HuskyLens and Arduino Nano are preserved as **legacy development**, while Pixy2.1 is current.

---

## D-13 — Do Not Use "First Block Wins"

### Problem

Pixy2.1 can potentially observe several colored blocks.

A naive controller could use:

```python
blocks[0]
```

as the current target.

However, camera return order does not necessarily mean:

```text
most physically relevant obstacle
```

### Decision

The current design direction is:

```text
detect candidates
      ↓
validate
      ↓
evaluate relevance
      ↓
confirm
      ↓
lock target
```

### Relevant Information

Target selection can consider:

```text
signature

x

y

width

height

current state

previous target
```

### Trade-off

This is more complex than selecting the first valid block.

### Current Result

The architecture has been selected, but the final numerical target-relevance function remains **ONGOING**.

---

# 2.5 Ultrasonic Architecture Decisions

## D-08 / D-09 — Two Permanent Lateral Ultrasonics

<div align="center">

<img
  src="../../v-photos/v4/PiolinUSlabeling.png"
  alt="Piolín current ultrasonic sensor labeling"
  width="720"
/>

<br>

<sub><b>Figure 2.5.</b> Current permanent ultrasonic convention: S2 is LEFT and S3 is RIGHT.</sub>

</div>

### Problem

Piolín needs physical information about course boundaries and vehicle position.

Earlier experimentation considered different sensor orientations and additional ultrasonic arrangements.

### Decision

The current permanent configuration is:

```text
S2 = LEFT lateral ultrasonic

S3 = RIGHT lateral ultrasonic
```

There is no permanent front ultrasonic in the current final architecture.

### Reasoning

Two lateral measurements are highly useful for:

```text
straight geometry

wall safety

recovery after obstacles

parking geometry
```

while keeping the sensor architecture consistent between both rounds.

### Trade-off

Piolín does not have a dedicated ultrasonic measurement directly forward.

Obstacle forward perception in the Obstacle Challenge is therefore primarily camera-based.

### Current Result

The S2/S3 identities are treated as **fixed physical conventions**.

They should never be reversed in software simply to compensate for a steering bug.

---

## D-10 — Geometry-Based Wall Navigation Instead of Threshold-Only Behavior

### Earlier Simplification

A simple wall strategy can be expressed as:

```text
wall close
→ steer away
```

### Problem

This does not fully describe:

```text
lateral vehicle position

sensor disagreement

corner geometry

oscillation

trajectory trend
```

and aggressive independent corrections can produce zig-zag.

### Decision

Piolín's development controller introduced a geometric approach using both sensors.

Conceptually:

```text
S2 + S3
      ↓
geometry estimate
      ↓
position error
      ↓
bounded steering correction
```

It also separates:

```text
NORMAL WALL CONTROL
```

from:

```text
CRITICAL WALL SAFETY
```

### Reasoning

This creates two different questions:

```text
Where should Piolín travel?
```

and:

```text
Is Piolín becoming physically unsafe?
```

These should not be answered by the same threshold.

### Trade-off

The geometry controller requires more calibration and state awareness.

### Current Result

The architecture is current, while its numerical gains and thresholds remain tunable.

---

# 2.6 Software Architecture Decisions

## D-11 — Move from Direct Reactions to States

### Problem

As Piolín gained more behaviors, several controllers could become active at once.

For example:

```text
wall following

pillar avoidance

corner handling

recovery

parking
```

A purely reactive program becomes difficult to reason about when every sensor can immediately influence steering.

### Decision

Use a high-level state architecture including:

```text
START

ACQUIRE

NORMAL

TARGET_ACQUIRE

AVOID

PASS_CONFIRM

RECOVER

CORNER

PARKING

STOP
```

### Reasoning

The state answers:

```text
What is Piolín currently trying to accomplish?
```

and therefore determines:

```text
which sensor matters most

which controller has authority

which transition is valid next
```

### Trade-off

State transitions must themselves be carefully designed and debugged.

A wrong transition can produce correct controllers at the wrong time.

### Current Result

State-based organization is the current software direction.

---

## D-14 — Explicit Controller Arbitration

### Problem

Testing showed that an obstacle controller can request one direction while normal wall control requests the opposite.

For example:

```text
Red obstacle
→ RIGHT
```

while:

```text
normal wall centering
→ LEFT
```

Combining both with equal authority can produce:

```text
weak steering

oscillation

late avoidance
```

### Decision

Piolín uses state-dependent control authority.

A conceptual priority is:

```text
CRITICAL SAFETY
        ↓
ACTIVE MANEUVER
        ↓
NORMAL NAVIGATION
```

### Examples

During:

```text
NORMAL
```

wall geometry can strongly control trajectory.

During:

```text
AVOID
```

pillar control receives greater authority.

During:

```text
CORNER
```

straight-line wall assumptions lose authority.

During:

```text
PARKING
```

the parking controller becomes the terminal navigation objective.

### Trade-off

Arbitration adds software architecture, but it prevents independent controllers from unknowingly fighting one another.

### Current Result

This has become a core design principle across the entire robot.

---

# 2.7 Perception and Event Decisions

## D-12 — Signature Determines the Required Pillar Side

The current Pixy mapping is:

```text
sig1 → Pink

sig2 → Red

sig3 → Green
```

The WRO rules require:

```text
RED
→ PASS RIGHT
```

```text
GREEN
→ PASS LEFT
```

### Decision

The passing side is determined only by:

```text
signature
```

not by:

```text
where the obstacle appears inside the image
```

Therefore:

```text
Red on left side of camera
→ still PASS RIGHT
```

and:

```text
Green on right side of camera
→ still PASS LEFT
```

### Reasoning

Camera position answers:

```text
Where is the pillar?
```

while signature answers:

```text
Which passing rule applies?
```

Mixing those two meanings was identified as a source of possible left/right inversion.

### Current Result

This is a fixed competition-logic decision, not a tuning parameter.

---

## D-15 — Convert Sensor Samples into Events

### Problem

One physical feature may remain visible for many loop cycles.

For S4:

```text
BLUE
BLUE
BLUE
BLUE
```

can represent one physical marking.

Likewise one pillar may generate many consecutive camera detections.

### Decision

Use:

```text
candidate
→ confirmation
→ latch / lock
→ release
```

instead of treating every raw observation as a new event.

For floor lines, development logic includes:

```text
confirmation

line lock

neutral-floor release

encoder separation
```

For obstacles, the same pattern becomes:

```text
candidate pillar

confirmed pillar

locked target

pass confirmation

target release
```

### Reasoning

This allows one successful software pattern to be reused across different perception systems.

### Current Result

Event lifecycle management is now part of Piolín's current architecture.

---

# 2.8 Course Progress and Parking Decisions

## D-16 — Use Physical Course Events Instead of Time Alone

### Problem

Elapsed run time varies because of:

```text
speed

corners

pillar placement

avoidance duration

recovery

safety corrections
```

A timer therefore provides weak evidence of actual track progression.

### Decision

Piolín uses confirmed S4 floor events as course-state evidence.

The current development model uses:

```text
12 accepted events
```

for the intended:

```text
3 laps / 12 corners
```

progression reference.

### Trade-off

Reliable progress now depends on:

```text
correct RGB/color detection

duplicate protection

event confirmation
```

### Current Result

Physical course events are the main progression mechanism.

---

## D-17 — Pink Alone Must Not Trigger Parking

### Problem

Pixy may be able to observe the Pink parking reference before parking is logically appropriate.

A controller based on:

```text
sig1 detected
→ park
```

could therefore activate too early.

### Decision

Parking requires:

```text
COURSE PROGRESSION COMPLETE
+
PINK TARGET CONFIRMED
```

before the parking state becomes authoritative.

Conceptually:

```python
if parking_eligible and pink_confirmed:
    state = PARKING
```

### Reasoning

This combines:

```text
logical evidence
+
physical evidence
```

instead of relying on one sensor alone.

### Current Result

This is the selected parking architecture, although final Pink confirmation and parking thresholds remain tunable.

---

## D-18 — Do Not Use Timing Alone for Final Parking Travel

### Problem

A final instruction such as:

```text
move for 0.5 seconds
```

measures command duration rather than actual physical progression.

### Decision

The parking architecture uses Motor A encoder progression as one source of final-movement evidence.

A current development prototype contains:

```text
PARK_EXTRA_DEG = 300
```

but this value remains experimental.

### Reasoning

Encoder change provides a stronger physical reference than elapsed time alone.

The final parking architecture can combine:

```text
encoder progression

S2/S3 geometry

Motor B state
```

before reaching:

```text
STOP
```

### Trade-off

Encoder rotation is still not perfect absolute position because:

```text
wheel slip

turning geometry

surface interaction
```

can affect real ground displacement.

### Current Result

Encoder-based progression is selected; the final numerical travel remains **ONGOING**.

---

# 2.9 Software Environment Decision

## D-19 — Separate Open and Obstacle Programs

### Problem

The two rounds do not use identical hardware.

Open uses:

```text
Gyro on S1
```

while Obstacles uses:

```text
Pixy2.1 on S1
```

The vision interface also has different software requirements from the Open control loop.

### Decision

Maintain separate high-level source programs, conceptually:

```text
src/
  open_challenge.py
  obstacle_challenge.py
```

The current Open work is based primarily around:

```text
Pybricks MicroPython
```

while the direct Pixy2.1 Obstacle integration is currently better matched to:

```text
ev3dev2 + SMBus/I2C
```

### Reasoning

Trying to force both rounds into one large source file would introduce:

```text
unused drivers

round-specific conditionals

sensor-port ambiguity

more difficult debugging
```

Separate programs can still share the same engineering concepts without pretending the hardware is identical.

### Trade-off

Some utility logic may exist in both programs unless later refactored into common modules.

### Current Result

The project treats Open and Obstacles as two software configurations for the same mechanical robot.

---

# 2.10 Decision to Preserve Legacy Engineering Work

## D-20 — Keep Replaced Approaches as Legacy Documentation

### Problem

Deleting every failed or superseded approach would make the final repository appear cleaner, but it would remove evidence of:

```text
experimentation

trade-offs

learning

architecture evolution
```

### Decision

Superseded systems are retained separately under legacy documentation.

Examples include:

```text
HuskyLens + Arduino Nano architecture

older Pixy approaches

earlier gyro strategies

prototype testing
```

They must be clearly labeled:

```text
LEGACY
```

and must never be confused with the current wiring or code.

### Reasoning

Engineering is not only the final design.

Understanding:

```text
why something was replaced
```

is evidence of systems thinking.

### Trade-off

The repository requires stronger organization so readers can immediately distinguish:

```text
historical
```

from:

```text
current
```

### Current Result

The project maintains legacy material intentionally while current documentation always uses the present architecture as the primary reference.

---

# 2.11 Decisions That Are Still Open

Not every engineering question has already been finalized.

Several decisions are structurally defined but still require numerical validation.

| Area | Architecture Already Chosen | Still to Determine |
| :--- | :--- | :--- |
| Pixy target selection | Relevance-based selection | Final scoring equation |
| Target confirmation | Confirm before lock | Final confirmation requirement |
| Target loss | Temporary lock maintained | Final loss tolerance |
| Red avoidance | Pass RIGHT | Final steering trajectory |
| Green avoidance | Pass LEFT | Final steering trajectory |
| Pass confirmation | Use visual + physical context | Final release criteria |
| Recovery | Separate state | Final steering/speed profile |
| Corner handling | Separate state | Final transition thresholds |
| RGB detection | Blue/Orange floor classification | Final calibrated thresholds |
| Parking entry | Dedicated maneuver | Final entry curvature |
| Parking alignment | Separate phase | Final alignment geometry |
| Parking final travel | Encoder-supported | Final calibrated encoder progression |
| Final parked geometry | Tolerance-based | Final S2/S3 target ranges |

Leaving these marked as ongoing is preferable to presenting untested values as finished engineering results.

A decision should become:

```text
FINAL / VALIDATED
```

only after sufficient physical evidence exists.

---

# 2.12 Decision-Making Principles

Several general principles now guide new PiolínTech decisions.

### Prefer Physical Meaning

A parameter should correspond to something understandable, such as:

```text
wall distance

camera relevance

steering authority

course progress

encoder travel
```

rather than existing only because one trial happened to work.

### Prefer Separation of Responsibilities

For example:

```text
Pixy
→ obstacle identity
```

```text
S2/S3
→ physical lateral geometry
```

```text
S4
→ floor progression
```

instead of forcing one sensor to solve every navigation problem.

### Prefer State Over Conflicting Reactions

The software should know:

```text
what maneuver is active
```

before selecting which controller receives authority.

### Prefer Repeatability Over One Successful Run

A change is only valuable when its improvement can be reproduced.

### Prefer Measured Values Over Assumptions

Physical dimensions, RGB ranges, camera geometry, parking clearances, and final movement values should be measured before being presented as validated specifications.

### Preserve Rejected Designs

A replaced approach can still explain why the current design is stronger.

---

# 2.13 Decision Traceability

The long-term goal is for each important decision to be traceable through:

```text
DECISION ID
      ↓
SOURCE CODE VERSION
      ↓
PHYSICAL CONFIGURATION
      ↓
TEST
      ↓
RESULT
      ↓
CURRENT STATUS
```

For example:

```text
D-14
Controller arbitration
      ↓
obstacle software version
      ↓
Red single-pillar test
      ↓
compare obstacle command vs final command
      ↓
determine whether wall controller was fighting AVOID
```

This creates an engineering record much stronger than:

```text
"We changed the code because it did not work."
```

The desired record explains:

```text
what failed

why the team believed it failed

what changed

what trade-off the change introduced

what the next test demonstrated
```

---

# 2.14 Current Architecture Result

The decisions in this log collectively produce the current Piolín architecture:

```text
                           PIOLÍN
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
      MECHANICS            SENSORS             SOFTWARE
          │                   │                   │
          │          ┌────────┼────────┐          │
          │          │        │        │          │
          ▼          ▼        ▼        ▼          ▼
   Ackermann       S2 L     S3 R      S4       State Machine
   + Motor A       US       US       Color          │
   + Motor B                            │            │
          │                             │            │
          │                 ┌───────────┴──────┐     │
          │                 │                  │     │
          │                 ▼                  ▼     │
          │               OPEN             OBSTACLES │
          │                 │                  │     │
          │              S1 Gyro           S1 Pixy  │
          │                 │                  │     │
          └─────────────────┴──────────┬───────┴─────┘
                                      ▼
                               SENSOR PROCESSING
                                      │
                                      ▼
                                  PERCEPTION
                                      │
                                      ▼
                                STATE / DECISION
                                      │
                                      ▼
                             CONTROL ARBITRATION
                                      │
                          ┌───────────┴───────────┐
                          │                       │
                          ▼                       ▼
                    safety override         active maneuver
                          │                       │
                          └───────────┬───────────┘
                                      ▼
                               FINAL COMMAND
                                      │
                         ┌────────────┴────────────┐
                         │                         │
                         ▼                         ▼
                      Motor A                   Motor B
                    propulsion                 steering
```

The architecture is therefore not a collection of independent parts.

It is the result of linked engineering decisions about:

```text
what should be sensed

when it should be trusted

which controller should act

how physical motion should be produced

how failures should be diagnosed
```

---

# 2.15 Final Engineering Assessment

PiolínTech's decision log shows that the current robot architecture was produced through **selection, rejection, and refinement**, rather than by keeping every early design choice.

Important examples include:

```text
HuskyLens + Nano
→ replaced by direct Pixy2.1 integration
```

```text
one universal S1 configuration
→ replaced by round-specific Gyro / Pixy configurations
```

```text
changing ultrasonic roles
→ replaced by fixed S2 LEFT / S3 RIGHT identities
```

```text
simple wall reactions
→ replaced by geometry control + independent safety
```

```text
direct sensor reactions
→ replaced by state-based control
```

```text
multiple competing corrections
→ replaced by explicit controller arbitration
```

```text
raw sensor samples
→ replaced by confirmed events and target lifecycles
```

```text
Pink detection alone
→ replaced by progression-gated parking
```

```text
timing-only movement
→ increasingly replaced by physical sensor and encoder evidence
```

Some numerical controller choices remain under active testing, and the repository intentionally labels them as such.

This distinction is important:

```text
ARCHITECTURE DECIDED
```

does not always mean:

```text
EVERY CALIBRATION VALUE FINALIZED
```

The central decision-making principle used by PiolínTech is:

> **A design decision is kept because it solves a clearly identified system problem with an acceptable trade-off and performs better under repeated physical testing—not simply because it is the most recent idea implemented.**

By preserving both current and replaced decisions, the repository documents not only what Piolín is, but also the reasoning that transformed earlier prototypes into the current competition architecture.

---

<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
