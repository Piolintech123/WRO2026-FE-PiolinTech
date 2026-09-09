# 5. Risks and Mitigation

<div align="center">

<img
  src="../../v-photos/v4/piolin_obstacle_isometric.jpg"
  alt="Piolín in its current Obstacle Challenge configuration"
  width="720"
/>

<br>

<sub><b>Figure 5.1.</b> Piolín is designed as an integrated system in which failures in sensing, mechanics, control, or software can propagate into navigation errors.</sub>

</div>

Autonomous performance depends not only on what Piolín can do when every subsystem behaves correctly, but also on how the system responds when information becomes uncertain, a mechanism behaves differently than expected, or two controllers request conflicting actions.

PiolínTech therefore treats risk management as part of the engineering process.

The basic risk cycle is:

```text
IDENTIFY POSSIBLE FAILURE
        ↓
UNDERSTAND ITS EFFECT
        ↓
DETECT IT AS EARLY AS POSSIBLE
        ↓
REDUCE ITS PROBABILITY
        ↓
LIMIT ITS CONSEQUENCES
        ↓
TEST THE MITIGATION
```

The main risk categories are:

```text
MECHANICAL

SENSING

PERCEPTION

CONTROL

STATE MANAGEMENT

COURSE PROGRESSION

PARKING

POWER / CONNECTIONS

SOFTWARE / CONFIGURATION

TESTING / REPRODUCIBILITY
```

A mitigation is considered stronger when it prevents a failure from propagating into several later subsystems.

For example:

```text
incorrect Pixy block
→ target validation
```

is preferable to allowing the incorrect block to reach:

```text
target selection
→ AVOID
→ steering
→ collision
```

---

## 5.1 Risk Evaluation Method

PiolínTech uses qualitative risk assessment while development measurements are still being collected.

Two properties are considered:

```text
LIKELIHOOD
→ How easily could this occur during realistic operation?
```

and:

```text
IMPACT
→ How severely could it affect the run?
```

The qualitative levels are:

```text
LOW

MEDIUM

HIGH
```

These labels are engineering priorities, not statistically measured probabilities.

A failure can receive high priority even if it is relatively uncommon when its consequence is severe.

For example:

```text
incorrect Red/Green passing side
```

has high impact because it directly violates the required obstacle behavior.

By contrast:

```text
small temporary ultrasonic noise
```

may have low impact if filtering and state logic prevent it from reaching the steering output.

---

## 5.2 Current Risk Register

| ID | Risk | Likelihood | Impact | Primary Mitigation | Status |
| :--- | :--- | :---: | :---: | :--- | :---: |
| `R-01` | Steering center changes or is incorrect | Medium | High | Center verification, Motor B feedback, bounded steering | ACTIVE |
| `R-02` | Mechanical steering play changes trajectory | Medium | High | Mechanical inspection, repeatable mounting, trajectory testing | ACTIVE |
| `R-03` | S2/S3 identity is reversed in software | Low | High | Fixed `S2 = LEFT`, `S3 = RIGHT` convention | MITIGATED |
| `R-04` | Ultrasonic spike creates wrong correction | Medium | Medium | Range validation, short filtering, bounded commands | MITIGATED / TUNING |
| `R-05` | Normal wall control fights pillar avoidance | Medium | High | State-dependent authority and arbitration | ACTIVE |
| `R-06` | Pixy detects wrong or irrelevant target | Medium | High | Signature validation, relevance selection, confirmation | ACTIVE |
| `R-07` | Target changes during active avoidance | Medium | High | Target lock until pass confirmation | ACTIVE |
| `R-08` | Pixy loses pillar during steering | Medium | High | Temporary target memory + lateral context | ACTIVE |
| `R-09` | Red/Green passing side becomes inverted | Low | High | Signature-only rule: Red RIGHT, Green LEFT | MITIGATED |
| `R-10` | Lighting changes vision behavior | Medium | High | Physical casing, signature calibration, repeated testing | ACTIVE |
| `R-11` | S4 counts one floor marking more than once | Medium | High | Confirmation, latch, release, encoder separation | MITIGATED / TUNING |
| `R-12` | Real floor event is missed at speed | Medium | High | Dynamic RGB testing, confirmation tuning | ACTIVE |
| `R-13` | Incorrect state transition activates wrong controller | Medium | High | Explicit states, transition guards, telemetry | ACTIVE |
| `R-14` | Recovery begins before pillar is passed | Medium | High | `PASS_CONFIRM` before `RECOVER` | ACTIVE |
| `R-15` | Recovery begins too late | Medium | High | Visual + ultrasonic pass evidence | ACTIVE |
| `R-16` | Corner geometry is interpreted as wall error | Medium | High | Dedicated `CORNER` state, reduced straight-wall authority | ACTIVE |
| `R-17` | Parking activates before course completion | Low/Medium | High | Course-progress gate before Pink target authority | MITIGATED |
| `R-18` | Parking final movement overshoots | Medium | Medium/High | Encoder progression, lower final speed, geometry check | ACTIVE |
| `R-19` | S1 round configuration does not match software | Low | High | Separate Open/Obstacle configurations and startup checks | ACTIVE |
| `R-20` | Software regression removes previously working behavior | Medium | High | Known-good baselines, isolated changes, Git version control | ACTIVE |

The status column describes the current engineering treatment:

```text
MITIGATED
→ architecture already contains a strong preventive measure

ACTIVE
→ still requires continued physical validation

TUNING
→ mitigation exists but numerical parameters are still being calibrated
```

---

# 5.3 Mechanical and Steering Risks

<div align="center">

<img
  src="../../v-photos/v4/steering_motor_mount.jpg"
  alt="Piolín Motor B steering installation"
  width="680"
/>

<br>

<sub><b>Figure 5.2.</b> Mechanical steering consistency is a prerequisite for meaningful software calibration.</sub>

</div>

Piolín's Ackermann architecture makes steering repeatability particularly important.

A software command may be correct while the physical result differs because of:

```text
mechanical play

linkage movement

Motor B center drift

wheel support movement

binding near steering limits
```

The risk chain is:

```text
MECHANICAL CHANGE
      ↓
actual wheel angle differs
      ↓
trajectory differs
      ↓
sensor geometry changes
      ↓
controller compensates incorrectly
```

This is dangerous because the visible symptom may appear to be a software problem.

### Mitigation

Before major tuning sessions:

```text
inspect steering linkage

verify Motor B mounting

verify steering center

verify left/right motion

check that the wheels return repeatably
```

Software also limits steering commands rather than allowing unlimited Motor B targets.

The actuator layer uses Motor B feedback so the controller can distinguish:

```text
requested steering
```

from:

```text
actual steering
```

A failure such as:

```text
FINAL CMD: RIGHT

REAL STEER: LEFT
```

can therefore be diagnosed downstream from the perception system.

---

# 5.4 Ultrasonic Sensing Risks

<div align="center">

<img
  src="../../v-photos/v4/PiolinUSlabeling.png"
  alt="Piolín ultrasonic sensor mapping"
  width="710"
/>

<br>

<sub><b>Figure 5.3.</b> Fixed physical sensor identities reduce the risk of software left/right inversion.</sub>

</div>

The permanent ultrasonic convention is:

```text
S2 = LEFT

S3 = RIGHT
```

One major risk is accidentally reversing these identities inside software.

That could transform:

```text
left wall close
```

into:

```text
software believes right wall close
```

and cause steering directly toward the danger.

### Mapping Mitigation

The physical names remain fixed across:

```text
wiring

code

telemetry

documentation

testing
```

Navigation direction may change logical roles such as:

```text
inner

outer
```

but it must never rename:

```text
LEFT

RIGHT
```

---

Ultrasonic sensors can also produce temporary unusual measurements.

One development controller therefore uses:

```text
range validation
```

followed by:

```text
short median filtering
```

before navigation uses the values.

The mitigation philosophy is:

```text
one strange measurement
≠
one extreme steering command
```

At the same time, filtering cannot become so strong that:

```text
real wall danger
```

is detected too late.

The remaining risk is therefore a trade-off between:

```text
noise rejection
```

and:

```text
reaction speed
```

which continues to require physical tuning.

---

# 5.5 Pixy2.1 Perception Risks

<div align="center">

<img
  src="../../v-photos/v4/pixy21_front.jpg"
  alt="Piolín Pixy2.1 forward vision sensor"
  width="680"
/>

<br>

<sub><b>Figure 5.4.</b> Pixy2.1 provides essential obstacle information, but camera observations require validation before being allowed to control a maneuver.</sub>

</div>

Pixy2.1 is the main forward-perception sensor during Obstacles.

Several risks must be managed:

```text
incorrect signature

small irrelevant color region

distant pillar selected too early

multiple pillars visible

target leaves field of view

lighting changes classification
```

The mitigation architecture therefore separates:

```text
DETECTION
```

from:

```text
TARGET SELECTION
```

from:

```text
STEERING
```

The planned process is:

```text
READ BLOCKS
      ↓
VALIDATE
      ↓
EVALUATE RELEVANCE
      ↓
CONFIRM
      ↓
LOCK
      ↓
AVOID
```

A raw camera block should never directly become a Motor B command.

---

## Multiple-Target Risk

Suppose Pixy sees:

```text
near Red

far Green
```

Using:

```text
first block returned
```

creates the risk of choosing the wrong physical obstacle.

The mitigation is relevance-based selection using information such as:

```text
signature

x

y

width

height

current state

previous target
```

The exact scoring formula remains under development.

---

## Target-Loss Risk

When Piolín turns:

```text
camera rotates
      ↓
pillar moves across image
      ↓
pillar may disappear
```

A missing frame therefore does not prove that the obstacle has been passed.

The mitigation is:

```text
temporary target memory
+
PASS_CONFIRM
+
S2/S3 physical context
```

rather than:

```text
no Pixy block
→ immediately release target
```

---

# 5.6 Risk of Red/Green Direction Inversion

One of the highest-impact obstacle failures is applying the wrong competition rule.

The required mapping is fixed:

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

A dangerous implementation would derive passing side from:

```text
pillar x-position
```

because the target can appear on either side of the image while Piolín approaches it.

The mitigation is architectural:

```text
SIGNATURE
→ required side
```

```text
IMAGE COORDINATES
→ target geometry
```

These roles are never exchanged.

The software should be able to print explicitly:

```text
SIG: 2
PASS: RIGHT
```

or:

```text
SIG: 3
PASS: LEFT
```

before steering is applied.

This allows the team to determine whether an inverted physical trajectory originates in:

```text
vision mapping
```

or later in:

```text
controller sign

arbitration

Motor B actuation
```

---

# 5.7 Controller-Conflict Risk

One of the most important system-level risks occurs when several individually reasonable controllers request different steering directions.

For example:

```text
RED pillar
→ obstacle controller requests RIGHT
```

while:

```text
normal wall control
→ requests LEFT
```

and:

```text
corner logic
→ requests another trajectory
```

If all commands are simply added:

```text
result can be weak or unstable
```

The mitigation is explicit controller arbitration.

The conceptual hierarchy is:

```text
CRITICAL SAFETY
      ↓
CURRENT COMMITTED MANEUVER
      ↓
NORMAL NAVIGATION
```

Therefore:

```text
NORMAL
→ wall geometry has authority
```

```text
AVOID
→ pillar controller has authority
```

```text
CORNER
→ corner controller has authority
```

```text
PARKING
→ parking controller has authority
```

while critical wall safety remains available where required.

This architecture reduces the risk that a correct obstacle decision appears physically inverted because another controller quietly cancelled it.

---

# 5.8 State-Transition Risks

A state machine reduces controller conflict, but it introduces another risk:

```text
correct controller
+
wrong state
=
wrong behavior
```

Examples include:

```text
RECOVER starts before pillar is passed

CORNER begins from false geometry

PARKING becomes active too early

NORMAL resumes before steering has stabilized
```

The mitigation is to require evidence for transitions.

For example:

```text
TARGET_ACQUIRE
→ confirmed target
→ AVOID
```

rather than:

```text
one detection
→ AVOID
```

and:

```text
AVOID
→ physical pass evidence
→ PASS_CONFIRM
→ RECOVER
```

rather than:

```text
camera loses target
→ RECOVER
```

Likewise:

```text
course progress complete
+
Pink confirmed
→ PARKING
```

rather than:

```text
Pink visible
→ PARKING
```

State transitions should also be exposed in telemetry so an incorrect transition can be identified directly.

---

# 5.9 Corner and Recovery Risks

Corners and post-pillar recovery are especially sensitive because the robot is intentionally leaving one stable geometry and trying to acquire another.

During a corner:

```text
S2/S3 straight-corridor assumptions degrade
```

If normal wall control remains fully active, it may interpret the expected corner geometry as:

```text
large lateral error
```

and steer against the turn.

The mitigation is:

```text
dedicated CORNER state
+
reduced straight-wall authority
+
critical safety still available
```

After a pillar, the opposite transition occurs.

Piolín must return from:

```text
intentional lateral avoidance
```

to:

```text
stable track geometry
```

Two high-impact recovery risks exist.

### Recovery too early

```text
pillar still beside robot
      ↓
countersteer
      ↓
vehicle moves back toward pillar
```

Mitigation:

```text
PASS_CONFIRM before RECOVER
```

### Recovery too late

```text
pillar already cleared
      ↓
avoidance continues
      ↓
outside wall approaches
```

Mitigation:

```text
use Pixy history + lateral ultrasonic evidence
to identify when the target is physically behind the active maneuver
```

The final thresholds remain active tuning parameters.

---

# 5.10 Floor Detection and Course-Counting Risks

<div align="center">

<img
  src="../../v-photos/v4/color_sensor_casing.jpg"
  alt="Piolín Color Sensor casing"
  width="650"
/>

<br>

<sub><b>Figure 5.5.</b> Physical light control and software event filtering work together to reduce floor-detection risk.</sub>

</div>

A course-progression failure can affect several later states.

For example:

```text
one Blue line counted twice
      ↓
course count becomes incorrect
      ↓
parking eligibility occurs early
```

or:

```text
one event missed
      ↓
count remains low
      ↓
parking never becomes eligible
```

Piolín therefore separates:

```text
RGB / color classification
```

from:

```text
event counting
```

Mitigation includes:

```text
candidate confirmation

event latch

neutral-floor release

minimum encoder separation
```

The goal is:

```text
one physical marking
→ one software event
```

The S4 casing also helps reduce uncontrolled ambient-light variation, although it does not eliminate the need for calibration.

A remaining risk is that excessive confirmation can reject a valid marking when the robot crosses it quickly.

This is why floor-event testing must be performed:

```text
while moving
```

and not only with the robot stationary.

---

# 5.11 Parking Risks

<div align="center">

<img
  src="../../v-photos/v4/parking_area.jpg"
  alt="Parking area used for Piolín final maneuver testing"
  width="700"
/>

<br>

<sub><b>Figure 5.6.</b> Parking is a terminal maneuver, so errors in progression, perception, geometry, or stopping logic can all affect the final result.</sub>

</div>

Parking inherits risks from several earlier subsystems.

Possible failures include:

```text
course count incorrect

Pink detected too early

Pink target not confirmed

entry begins from poor pose

entry arc too wide or too tight

alignment incomplete

final travel overshoots

STOP does not remain terminal
```

The mitigation is to divide parking into phases:

```text
ELIGIBILITY
      ↓
PINK CONFIRMATION
      ↓
APPROACH
      ↓
ENTRY
      ↓
ALIGNMENT
      ↓
FINAL POSITION
      ↓
STOP
```

Each phase can be tested independently.

The final movement also uses:

```text
Motor A encoder progression
```

rather than time alone.

However, encoder progression is not treated as perfect absolute localization.

Final parking can additionally use:

```text
S2/S3 geometry

Motor B position

parking state
```

before accepting the final condition.

The current prototype value:

```text
PARK_EXTRA_DEG = 300
```

remains a development value and is not considered a final risk mitigation until repeated physical testing validates the endpoint.

---

# 5.12 Power, Connection, and Configuration Risks

Piolín's current electrical system is intentionally simple.

The active power source is:

```text
LEGO Mindstorms EV3 Rechargeable DC Battery 45501
```

and the current robot does not require a permanent:

```text
external battery

Arduino power system

buck converter
```

This reduces the number of active electrical failure points.

However, configuration risk still exists because S1 changes by round.

The critical mapping is:

```text
OPEN
S1 = Gyro
```

```text
OBSTACLES
S1 = Pixy2.1
```

A dangerous mismatch would be:

```text
Obstacle hardware installed
+
Open software started
```

or the opposite.

Mitigation includes:

```text
separate source programs

clear wiring documentation

round-specific startup procedure

physical S1 photographs

descriptive filenames
```

The repository should never imply that Gyro and Pixy2.1 are simultaneously active.

Connection inspection should also occur before competition-style runs because a software algorithm cannot compensate for a physically disconnected sensor.

---

# 5.13 Software Regression and Reproducibility Risks

One of the less visible but important risks is losing a working behavior while trying to improve another one.

For example:

```text
change corner steering
→ accidentally changes post-corner pose
→ obstacle behavior becomes worse
→ parking entry also changes
```

A poor development workflow would continue editing the same code until the cause becomes unclear.

The mitigation is:

```text
KNOWN-GOOD BASELINE
      ↓
one primary change
      ↓
controlled test
      ↓
compare result
```

If the change improves behavior repeatedly:

```text
save / commit
```

If it makes behavior worse:

```text
restore known-good version
```

Regression testing should include major downstream functions when upstream behavior changes.

For example, after modifying:

```text
corner exit
```

the team should eventually check:

```text
next pillar acquisition

recovery

parking entry pose
```

because systems engineering considers propagation, not only the subsystem directly edited.

---

## 5.14 Risk Mitigation Through Telemetry

Many risks become harder to diagnose when only the final collision is observed.

Piolín's software therefore benefits from telemetry that exposes the internal decision chain.

Useful variables include:

```text
STATE

COURSE COUNT

S2 LEFT

S3 RIGHT

PIXY SIGNATURE

PIXY TARGET X

TARGET LOCK

REQUIRED PASS SIDE

WALL COMMAND

OBSTACLE COMMAND

SAFETY ACTIVE

FINAL COMMAND

MOTOR B TARGET

MOTOR B REAL
```

This allows failures to be localized.

For example:

```text
SIG: 2
PASS: RIGHT
OBS_CMD: RIGHT
FINAL: LEFT
```

indicates an arbitration problem.

While:

```text
SIG: 2
PASS: LEFT
```

indicates an interpretation problem.

And:

```text
FINAL: RIGHT
MOTOR B REAL: LEFT
```

moves investigation toward actuation.

The mitigation principle is:

> **The earlier the software can expose where the expected decision changed, the less likely the team is to modify the wrong subsystem.**

---

## 5.15 Fail-Safe Behavior and Defensive Programming

Not every uncertain condition should produce an aggressive reaction.

Several defensive patterns are used or planned across Piolín:

```text
clamp extreme controller values

filter short ultrasonic spikes

confirm visual targets

lock active targets

require release conditions

reduce speed during difficult maneuvers

use critical wall safety

retain current maneuver briefly after temporary camera loss

require course progress before parking

make STOP terminal
```

The general philosophy is:

```text
UNCERTAIN DATA
→ reduce confidence
```

rather than:

```text
UNCERTAIN DATA
→ maximum steering
```

For example:

```text
one Red-looking frame
```

should become:

```text
candidate
```

before:

```text
confirmed Red obstacle
```

Similarly:

```text
one missing Pixy frame
```

should not instantly reverse the active steering trajectory.

This creates more predictable behavior under temporary uncertainty.

---

## 5.16 Verification of Mitigations

A mitigation should be tested against the failure it is intended to prevent.

Examples include:

| Risk | Mitigation Test |
| :--- | :--- |
| S2/S3 reversed | Place object separately near each sensor |
| Duplicate floor count | Cross one line slowly and at normal speed |
| Far pillar selected | Present near and far targets together |
| Target switching | Make two signatures visible during active pass |
| Temporary target loss | Allow pillar to leave FOV during steering |
| Wall controller fighting AVOID | Compare obstacle command with final command |
| Recovery too early | Inspect pillar location when `RECOVER` begins |
| Recovery too late | Inspect wall approach after pillar clearance |
| Pink activates early | Expose Pink before required course progression |
| STOP resumes motion | Keep program running after final stop |
| Software regression | Repeat known-good representative test after change |

This prevents a mitigation from existing only on paper.

The engineering sequence should be:

```text
identify risk
      ↓
implement defense
      ↓
deliberately test relevant scenario
      ↓
observe whether failure propagation is reduced
```

---

## 5.17 System-Level Failure Containment

The strongest risk strategy is to prevent one subsystem failure from controlling the entire robot.

Piolín's architecture can be visualized as:

```text
                         SENSOR INPUT
                              │
                              ▼
                          VALIDATION
                              │
                    bad data rejected?
                         /         \
                       YES          NO
                       │             │
                       ▼             ▼
                    IGNORE       PERCEPTION
                                      │
                                      ▼
                                 CONFIRMATION
                                      │
                                      ▼
                                  STATE LOGIC
                                      │
                                      ▼
                                CONTROLLER
                                      │
                                      ▼
                               ARBITRATION
                                      │
                                      ▼
                                SAFETY CHECK
                                      │
                                      ▼
                                FINAL COMMAND
                                      │
                                      ▼
                                  MOTOR B
```

Several containment boundaries exist:

```text
sensor validation
→ contains measurement errors

target confirmation
→ contains unstable perception

state machine
→ contains inappropriate controller activation

arbitration
→ contains controller conflict

wall safety
→ contains dangerous trajectory requests

command limits
→ contain excessive actuator requests
```

No layer guarantees perfect behavior, but multiple independent defenses reduce the probability that one incorrect observation immediately becomes a severe physical failure.

---

## 5.18 Highest-Priority Remaining Risks

Several risks still require significant physical validation before the Obstacle Challenge controller can be considered mature.

### 1. Relevant pillar selection

The final multi-block relevance function is not yet fully calibrated.

### 2. Obstacle authority vs. wall control

The exact amount of wall influence that should remain during `AVOID` still requires testing.

### 3. Pillar pass confirmation

The final combination of Pixy and ultrasonic evidence for releasing the target remains under development.

### 4. Recovery timing

Recovery must begin neither too early nor too late.

### 5. Pillars near corners

The transition between `CORNER` and obstacle handling is still one of the more complex interaction cases.

### 6. Final RGB thresholds

Floor detection must be validated dynamically under the final optical installation.

### 7. Parking geometry

Final entry, alignment, encoder progression, and stopping tolerances require measured repeatability.

Documenting these as active risks is preferable to presenting unfinished behavior as solved.

---

## 5.19 Final Engineering Assessment

Piolín's risk-management strategy is based on preventing uncertain information or a local subsystem error from immediately becoming a severe vehicle-level failure.

The current architecture uses several layers of mitigation:

```text
physical inspection

fixed sensor conventions

measurement validation

short filtering

candidate confirmation

target locking

state-based behavior

controller arbitration

critical wall safety

bounded steering

state-dependent speed

course-progress gating

encoder-supported parking

terminal STOP logic

telemetry

known-good software baselines
```

Several important examples demonstrate the systems approach.

```text
Pixy may temporarily lose a pillar
→ preserve target state instead of reversing immediately
```

```text
normal wall control may oppose pillar avoidance
→ reduce its authority during AVOID
```

```text
one floor marking produces many samples
→ latch it as one physical event
```

```text
Pink may be visible early
→ require course completion before parking can activate
```

```text
encoder travel is not perfect localization
→ combine it with physical parking geometry
```

```text
a correct command may still produce the wrong physical steering
→ compare requested and actual Motor B state
```

Not every risk has been eliminated, and several high-priority behaviors remain under active testing.

The objective is instead to ensure that each major risk has:

```text
a known cause or failure mechanism

a defined detection method

a mitigation strategy

a test that can verify the mitigation
```

The central risk-management principle used by PiolínTech is:

> **A robust autonomous system should not assume that every sensor reading, state transition, or actuator response is correct. Piolín's software is structured so that important decisions are validated, dangerous commands can be limited or overridden, failures can be traced to the layer where they begin, and improvements can be verified through repeatable physical tests.**

This approach turns risk management from a list of possible failures into an active part of Piolín's mechanical design, control architecture, software organization, testing process, and competition strategy.

---

<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
