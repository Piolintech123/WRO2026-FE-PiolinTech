# 4. Engineering Trade-Offs

<div align="center">

<img
  src="../../v-photos/v4/piolin_obstacle_isometric.jpg"
  alt="Piolín in its current Obstacle Challenge configuration"
  width="720"
/>

<br>

<sub><b>Figure 4.1.</b> Piolín's architecture is the result of deliberate compromises between sensing capability, mechanical simplicity, control authority, software complexity, and competition performance.</sub>

</div>

Engineering design rarely produces a solution that is simultaneously:

```text
simplest

fastest

most accurate

most robust

easiest to reproduce
```

PiolínTech therefore evaluates major design choices as **trade-offs**.

A trade-off exists when improving one characteristic introduces a cost somewhere else.

For example:

```text
more sensors
→ more information
→ but more wiring, ports, software, and failure points
```

or:

```text
higher speed
→ faster lap
→ but less reaction time and harder steering control
```

The engineering objective is not to eliminate every compromise.

It is to select the combination of compromises that produces the most useful complete system for the WRO Future Engineers challenge.

The current Piolín architecture reflects trade-offs in five major areas:

```text
MECHANICS

SENSORS

PERCEPTION

CONTROL

SOFTWARE / REPRODUCIBILITY
```

---

## 4.1 Trade-Off Summary

| Design Choice | Main Benefit | Main Cost |
| :--- | :--- | :--- |
| Ackermann steering | Car-like predictable motion | Cannot rotate in place |
| One drive + one steering motor | Clear motor responsibilities | No differential steering |
| Round-specific S1 | Best sensor for each round | Hardware/software configuration changes |
| Gyro in Open | Direct heading information | No camera on S1 |
| Pixy2.1 in Obstacles | Forward obstacle identity | No gyro heading |
| Two lateral ultrasonics | Strong lateral geometry | No permanent forward ultrasonic |
| Direct Pixy2.1 integration | Simpler perception chain | Camera calibration still required |
| State machine | Reduced controller conflict | More transition logic |
| Target confirmation | More stable perception | Adds reaction delay |
| Target lock | Prevents target switching | Can retain stale target too long |
| Steering smoothing | Reduces oscillation/shock | Can delay avoidance |
| Reduced speed in maneuvers | More control time | Slower run |
| Event-based lap counting | Physical progression reference | Requires robust floor detection |
| Encoder-supported parking | Better than timing alone | Encoder is not absolute position |
| Separate Open/Obstacle programs | Cleaner hardware-specific code | Some duplicated concepts |

The rest of this document explains the most important compromises in greater detail.

---

## 4.2 Ackermann Steering vs. Easier Turning Methods

<div align="center">

<img
  src="../../v-photos/v4/ackermann_top.jpg"
  alt="Top view of Piolín Ackermann-style steering system"
  width="700"
/>

<br>

<sub><b>Figure 4.2.</b> Ackermann steering gives Piolín predictable car-like motion, but every heading change requires physical forward or reverse travel.</sub>

</div>

Piolín uses:

```text
Motor A
→ propulsion
```

and:

```text
Motor B
→ Ackermann-style steering
```

The main advantage is that vehicle motion is easy to interpret physically:

```text
steering angle
+
vehicle progression
→ curved path
```

This supports:

```text
smooth straights

controlled corners

car-like obstacle trajectories

structured parking arcs
```

However, the trade-off is significant.

Piolín cannot:

```text
rotate in place

translate sideways

instantly correct heading
```

A differential-drive vehicle could theoretically create sharper heading corrections by driving its sides differently.

Piolín instead requires actual trajectory space.

This affects:

```text
corner entry

pillar recovery

parking

wall escape
```

The team accepted this limitation because the resulting motion is consistent with the intended vehicle architecture and allows propulsion and steering to remain mechanically separate.

---

## 4.3 One Drive Motor vs. More Propulsion Authority

Using only one main propulsion motor keeps the drivetrain simple.

Benefits include:

```text
fewer motors

simpler control

clear Motor A responsibility

reduced software coordination
```

The drivetrain does not need to synchronize two independent traction motors.

The cost is that propulsion cannot contribute directly to steering.

With differential drive, software can create turning moments through:

```text
left motor speed
≠
right motor speed
```

Piolín cannot use that strategy.

Its path depends primarily on:

```text
Motor B steering
+
Motor A motion
```

This increases the importance of:

```text
steering calibration

Motor B response

entry position

vehicle speed
```

PiolínTech accepted the reduced actuation freedom in exchange for a simpler and more understandable car-like drivetrain.

---

## 4.4 One Universal Sensor Configuration vs. Round-Specific Sensors

One possible architecture would attempt to keep:

```text
Gyro

Pixy2.1

two ultrasonics

Color Sensor
```

active at the same time.

That would provide more simultaneous sensing.

However, it would also create additional problems involving:

```text
EV3 sensor-port availability

connection complexity

software drivers

power / communication interfaces

physical installation
```

The selected trade-off is:

```text
OPEN
S1 → Gyro
```

and:

```text
OBSTACLES
S1 → Pixy2.1
```

while keeping:

```text
S2 → LEFT US

S3 → RIGHT US

S4 → Color
```

constant.

<div align="center">

<img
  src="../../v-photos/v4/s1_open_gyro.jpg"
  alt="Piolín Open configuration using the Gyro Sensor on S1"
  width="650"
/>

<br>

<sub><b>Figure 4.3.</b> Open gives S1 to heading sensing.</sub>

</div>

<div align="center">

<img
  src="../../v-photos/v4/s1_obstacle_pixy.jpg"
  alt="Piolín Obstacle configuration using Pixy2.1 on S1"
  width="650"
/>

<br>

<sub><b>Figure 4.4.</b> Obstacles gives S1 to forward visual perception.</sub>

</div>

The benefit is:

```text
each round receives the sensor with the highest value
```

The cost is:

```text
hardware must be reconfigured

software must support two architectures

Obstacles loses direct gyro heading

Open loses camera perception
```

PiolínTech accepted this compromise because the two rounds do not require identical sensing priorities.

---

## 4.5 Gyro in Open vs. Pixy2.1 in Obstacles

The S1 decision creates a second trade-off: **observability changes between rounds**.

### Open

The Gyro Sensor provides direct information about:

```text
heading change

drift

turn progression
```

which combines well with the lateral ultrasonics.

A useful division is:

```text
S2/S3
→ lateral position
```

```text
Gyro
→ orientation
```

### Obstacles

Pixy2.1 instead provides:

```text
signature

x

y

width

height
```

which supports:

```text
pillar identity

target relevance

parking detection
```

The cost is that the obstacle software cannot directly ask:

```text
What is my gyro heading?
```

It must infer maneuver progression using:

```text
Pixy history

S2/S3 geometry

Motor A encoder

Motor B position

state history
```

The team accepts less direct orientation measurement because pillar identity is more important to the obstacle round.

---

## 4.6 Two Lateral Ultrasonics vs. a Front Ultrasonic

<div align="center">

<img
  src="../../v-photos/v4/ultrasonic_pair_top.jpg"
  alt="Piolín permanent lateral ultrasonic sensor pair"
  width="700"
/>

<br>

<sub><b>Figure 4.5.</b> Piolín prioritizes persistent left/right geometry instead of keeping a permanent front ultrasonic sensor.</sub>

</div>

The final ultrasonic configuration is:

```text
S2 = LEFT

S3 = RIGHT
```

The advantage is that these sensors provide continuous information for several different subsystems:

```text
wall following

wall safety

corner geometry

pillar-pass confirmation

recovery

parking
```

A permanent front ultrasonic could instead provide a direct answer to:

```text
Is something immediately ahead?
```

but would consume another sensing position/interface and would not identify whether that object is:

```text
Red

Green

wall
```

The selected strategy uses:

```text
Pixy2.1
→ forward object perception
```

and:

```text
S2/S3
→ lateral physical geometry
```

The trade-off is that Piolín has less direct forward distance sensing, but each active sensor has a clearer long-term responsibility.

---

## 4.7 Direct Pixy2.1 vs. HuskyLens + Arduino Nano

Earlier development explored a vision chain based on:

```text
HuskyLens
→ Arduino Nano
→ EV3
```

The advantage of an intermediate microcontroller is flexibility.

It can:

```text
process camera information

translate communication

implement custom preprocessing
```

However, every new processing layer also introduces:

```text
another program

another device

another communication link

another wiring path

another possible failure
```

The current solution instead uses:

```text
Pixy2.1
→ EV3 S1
```

directly.

The main benefit is architectural simplicity.

The trade-off is that vision still requires careful:

```text
signature calibration

camera mounting

lighting control

target-selection software
```

The system becomes simpler, but not automatically easier in every aspect.

PiolínTech selected the direct architecture because removing an unnecessary intermediate controller improved clarity and reproducibility.

---

## 4.8 Raw Camera Reaction vs. Target Confirmation

A vision system can respond immediately after one valid color detection.

This has one obvious benefit:

```text
minimum delay
```

But one frame can also represent:

```text
unstable color detection

small irrelevant region

temporary false target
```

Piolín therefore uses the design principle:

```text
CANDIDATE
→ CONFIRM
→ LOCK
```

The trade-off is:

### Faster reaction

```text
fewer confirmations
→ less delay
→ more sensitivity to unstable observations
```

### Greater stability

```text
more confirmations
→ more confidence
→ more distance traveled before reaction
```

The final confirmation level must therefore be tuned at the real driving speed.

The correct value is not simply:

```text
as many confirmations as possible
```

because excessive filtering can make a perfectly classified obstacle become a late obstacle.

---

## 4.9 Target Lock vs. Rapid Target Switching

When multiple pillars are visible, continuously selecting the currently strongest camera block might seem attractive.

It allows the controller to always respond to the latest information.

However, during an active maneuver this can create:

```text
Red selected

Green becomes visually larger

target switches

steering reverses

Red becomes larger again

target switches again
```

The alternative is temporary target locking:

```text
select

confirm

lock

pass

release
```

The benefit is maneuver consistency.

The cost is that:

```text
a bad target selection can persist
```

or:

```text
an old target may remain active too long
```

if the release logic is weak.

Therefore target lock requires a complementary mechanism:

```text
PASS_CONFIRM
```

The architecture accepts temporary commitment because changing the physical maneuver repeatedly is usually more dangerous than preserving one already confirmed target.

---

## 4.10 Strong Wall Following vs. Obstacle Authority

During normal driving, strong wall geometry control is useful.

It can keep Piolín near its intended corridor position.

However, during pillar avoidance the same behavior can become harmful.

Example:

```text
RED pillar
→ obstacle controller requests RIGHT
```

while:

```text
wall controller
→ requests LEFT to recenter
```

If both retain full authority:

```text
commands fight
```

The trade-off is therefore between:

```text
continuous centering
```

and:

```text
freedom to execute obstacle trajectory
```

Piolín solves this through state-dependent authority.

```text
NORMAL
→ wall control strong
```

```text
AVOID
→ normal wall control reduced
```

```text
critical wall safety
→ remains available
```

This intentionally allows Piolín to temporarily leave its preferred normal corridor in order to satisfy the required obstacle trajectory.

The cost is that recovery becomes a necessary additional maneuver.

---

## 4.11 Smooth Steering vs. Fast Reaction

Piolín's development controllers use target smoothing to reduce abrupt steering changes.

Conceptually:

```python
diff = target - current_target

diff = clamp(
    diff,
    -TARGET_STEP,
    TARGET_STEP
)
```

The benefit is:

```text
less oscillation

less mechanical shock

more predictable Motor B behavior

reduced command jitter
```

The trade-off is delay.

If smoothing is too strong:

```text
camera detects pillar

controller requests large turn

Motor B target increases slowly

Piolín reaches pillar before enough steering develops
```

If smoothing is too weak:

```text
steering jumps

camera view changes abruptly

controller can overshoot

vehicle can zig-zag
```

This parameter therefore represents a direct compromise between:

```text
STABILITY
```

and:

```text
RESPONSIVENESS
```

and must be tuned together with vehicle speed.

---

## 4.12 Speed vs. Control Margin

Higher drive speed improves potential run time.

However, every sensing and actuation delay becomes more physically significant.

At a higher speed:

```text
same camera processing delay
→ more distance traveled
```

```text
same Motor B response time
→ more distance traveled
```

```text
same state-transition delay
→ more distance traveled
```

This increases the risk of:

```text
late corners

late pillar avoidance

wall collisions

parking overshoot
```

Piolín therefore uses state-dependent speed.

Conceptually:

```text
NORMAL
→ faster
```

```text
AVOID
→ controlled
```

```text
RECOVER
→ controlled
```

```text
critical safety
→ slower
```

```text
final parking
→ potentially slower for precision
```

The trade-off is that maximum theoretical speed is sacrificed to gain control margin during difficult maneuvers.

---

## 4.13 Simple Color Categories vs. RGB-Based Floor Classification

S4 floor detection can use:

```text
built-in EV3 named colors
```

which is simple and easy to program.

The disadvantage is reduced control over borderline classification.

An Orange marking may sometimes be interpreted by the sensor as:

```text
RED

YELLOW

BROWN
```

depending on physical conditions.

The RGB-based approach instead reads:

```text
reflection

R

G

B
```

and applies explicit relationships.

Benefits include:

```text
more diagnostic information

custom thresholds

better visibility into classification failure
```

The cost is:

```text
more calibration

more parameters

greater dependence on measured data
```

PiolínTech has explored both approaches.

The final selection should favor the method that produces the most repeatable behavior on the actual track rather than the one with the most complex code.

---

## 4.14 Event Confirmation vs. Missing Fast Markings

Floor-event confirmation provides the same stability/reaction trade-off as camera confirmation.

A Blue or Orange region may remain under S4 for many control cycles.

The software therefore uses mechanisms such as:

```text
candidate confirmation

line latch

neutral release

encoder separation
```

These reduce duplicate counting.

However, if confirmation or release requirements are too strict:

```text
Piolín may pass the physical marking
before the software accepts it
```

especially at higher speed.

The design must balance:

```text
avoid duplicate events
```

against:

```text
do not miss real events
```

This is one reason floor-event parameters must be calibrated dynamically rather than only with Piolín stationary.

---

## 4.15 Physical Events vs. Time-Based Lap Tracking

Time-based progression would be simple:

```text
after N seconds
→ assume lap completed
```

The advantage is minimal sensing logic.

The disadvantage is that run duration changes with:

```text
pillar placement

corner speed

recovery

safety corrections

battery behavior
```

Piolín instead tracks physical floor events.

The benefit is stronger correspondence with the actual track.

The trade-off is increased dependence on:

```text
reliable S4 classification

event confirmation

duplicate rejection
```

PiolínTech accepts the additional sensing complexity because a physical landmark provides better course-state evidence than elapsed time alone.

---

## 4.16 Timed Parking vs. Sensor-Fused Parking

A simple parking system could use:

```text
turn

wait

straighten

wait

stop
```

Its main advantage is simplicity.

However, small differences in:

```text
entry pose

speed

steering response

wheel slip
```

can produce different endpoints.

The current architecture instead combines:

```text
course count

Pixy sig1

Pixy geometry

S2/S3

Motor A encoder

Motor B steering state
```

The benefit is a stronger relationship with the physical parking maneuver.

The cost is greater software complexity and calibration effort.

PiolínTech selected the sensor-fusion direction because parking is a terminal maneuver where endpoint repeatability is more important than keeping the code minimal.

---

## 4.17 Encoder Progression vs. Absolute Position

Motor A encoder information is useful because it measures a real actuator progression.

It is stronger than:

```text
drive for 500 ms
```

for representing physical movement.

However:

```text
encoder degrees
```

are not the same as:

```text
absolute course coordinates
```

because actual displacement can vary with:

```text
wheel slip

curved trajectory

surface interaction
```

The trade-off is therefore:

```text
encoder
→ more physical than timing
→ but less complete than absolute localization
```

Piolín uses encoders as one source of evidence rather than pretending they provide perfect odometry.

This is especially important during parking, where the same Motor A rotation can produce different x/y displacement depending on the steering angle.

---

## 4.18 Separate Open and Obstacle Programs vs. One Universal Program

One universal program could reduce file count.

However, it would need to contain:

```text
Gyro drivers

Pixy drivers

round detection / configuration logic

round-specific states

unused hardware branches
```

even though the two rounds use different S1 devices and different software interfaces.

The selected architecture favors:

```text
open_challenge.py

obstacle_challenge.py
```

or equivalent separate high-level programs.

Benefits include:

```text
clear sensor assumptions

simpler debugging

less inactive code

easier round-specific tuning
```

The cost is that some common concepts may appear in both programs.

PiolínTech accepts limited duplication when it keeps the current hardware state unambiguous.

Common utilities can later be factored out only where doing so actually improves clarity.

---

## 4.19 Complexity vs. Reproducibility

A more advanced controller can often produce better behavior.

However, every additional layer can also make the robot harder to understand.

For example:

```text
target relevance

target confirmation

target lock

state machine

control arbitration

recovery
```

is more complex than:

```text
if Red:
    steer right
```

The simpler program is easier to read.

The layered program is easier to **reason about when several objectives conflict**.

PiolínTech therefore accepts software complexity only when the new layer has a clear engineering responsibility.

The intended rule is:

```text
complexity should buy observability,
stability, safety, or control
```

not:

```text
complexity for its own sake
```

This is why debug telemetry and state naming are important parts of the architecture.

A complex system becomes reproducible only if another reader can determine:

```text
what state is active

what each sensor means

which controller owns the output

why a transition occurred
```

---

## 4.20 Trade-Offs That Remain Open

Some compromises cannot be finalized until more testing is completed.

| Area | More Aggressive Direction | More Conservative Direction |
| :--- | :--- | :--- |
| Drive speed | Faster run | More control margin |
| Steering smoothing | Faster reaction | Greater stability |
| Pixy confirmation | Faster target acquisition | Better noise rejection |
| Target lock duration | More maneuver consistency | Faster release to next target |
| Wall safety activation | Earlier protection | More freedom during avoidance |
| Obstacle steering | Greater pillar clearance response | Lower overshoot risk |
| Recovery strength | Faster recentering | Lower oscillation risk |
| Corner steering | Tighter turn | Lower over-rotation risk |
| RGB thresholds | Detect more candidate markings | Reduce false events |
| Parking tolerance | Easier STOP acceptance | More precise final pose |

These should remain calibration questions until physical testing shows which side of each compromise produces the most repeatable overall result.

---

## 4.21 System-Level Trade-Off Map

The main relationships can be represented as:

```text
                         PERFORMANCE
                              ▲
                              │
                 higher speed / stronger control
                              │
                              │
STABILITY ◄───────────────────┼──────────────────► RESPONSIVENESS
                              │
                              │
                    filtering / smoothing
                              │
                              ▼
                        CONTROL MARGIN
```

A second relationship exists between sensing and complexity:

```text
                       MORE INFORMATION
                              ▲
                              │
                       more sensors /
                       more processing
                              │
                              │
SIMPLICITY ◄──────────────────┼──────────────────► OBSERVABILITY
                              │
                              │
                    more interfaces /
                       more software
                              │
                              ▼
                       FAILURE POINTS
```

Piolín's design does not attempt to move entirely toward one side.

Instead, each subsystem is positioned where the team believes the overall vehicle gains the most useful capability for the least unnecessary complexity.

---

## 4.22 Final Engineering Assessment

Piolín's architecture contains several intentional compromises.

The team accepted:

```text
Ackermann motion constraints
```

in exchange for:

```text
predictable car-like steering
```

accepted:

```text
round-specific sensor changes
```

in exchange for:

```text
using the most valuable S1 sensor in each round
```

accepted:

```text
no direct gyro heading in Obstacles
```

in exchange for:

```text
Pixy2.1 obstacle perception
```

accepted:

```text
no permanent front ultrasonic
```

in exchange for:

```text
two permanent lateral geometry sensors
```

accepted:

```text
confirmation delay
```

in exchange for:

```text
more stable sensor events
```

accepted:

```text
reduced normal wall authority during AVOID
```

in exchange for:

```text
allowing the required pillar trajectory to dominate
```

accepted:

```text
lower speed during difficult states
```

in exchange for:

```text
greater steering and sensing margin
```

and accepted:

```text
more parking software complexity
```

in exchange for:

```text
a parking maneuver based on physical evidence rather than timing alone
```

These compromises are important because the goal of systems engineering is not to optimize one subsystem independently.

For example:

```text
maximum wall-centering accuracy
```

would not be useful if it prevents Piolín from moving far enough around a Red pillar.

Likewise:

```text
maximum vehicle speed
```

would not be useful if Motor B cannot reach the required steering angle before the vehicle reaches the obstacle.

The final design must therefore optimize the complete sequence:

```text
SENSE

→ INTERPRET

→ DECIDE

→ MOVE

→ RECOVER

→ CONTINUE
```

rather than maximizing one value in isolation.

The central trade-off principle used by PiolínTech is:

> **A subsystem is not selected because it is individually the most powerful solution. It is selected when the capability it adds is worth the mechanical, electrical, software, calibration, and reliability cost it introduces to the complete robot.**

This approach allows PiolínTech to document not only the strengths of the current design, but also the limitations that were deliberately accepted in order to build a simpler, more understandable, and more reproducible autonomous system.

---

<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
