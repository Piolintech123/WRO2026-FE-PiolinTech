# 3. Motors and Actuation System

<div align="center">

<img
  src="../../v-photos/v4/motor_a_large_drive.jpg"
  alt="LEGO EV3 Large Motor installed as Piolín's propulsion motor"
  width="700"
/>

<br>

<sub><b>Figure 3.1.</b> LEGO EV3 Large Motor installed as Piolín's rear-propulsion actuator and connected to EV3 Motor Port A.</sub>

</div>

Piolín uses two LEGO Mindstorms EV3 motors, but they perform fundamentally different mechanical tasks. One motor is responsible for moving the complete vehicle forward and backward, while the other is responsible only for changing the orientation of the front wheels.

The current actuation architecture is:

```text
Motor Port A
→ LEGO EV3 Large Motor
→ Rear propulsion


Motor Port B
→ LEGO EV3 Medium Motor
→ Ackermann steering
```

This separation was selected because Piolín is not a differential-drive robot. The vehicle does not turn by changing the speeds of two independent drive motors. Instead, propulsion and steering are mechanically separated in the same general way they are in a conventional car.

This has important consequences for the complete robot architecture. Motor A determines how Piolín moves along its trajectory, while Motor B determines the direction and curvature of that trajectory. The EV3 software must therefore coordinate both actuators instead of treating them as interchangeable motors.

---

## 3.1 Final Motor Architecture

The current motor configuration is intentionally simple.

| Function | Motor | EV3 Port | Mechanical Responsibility |
| :--- | :--- | :---: | :--- |
| Propulsion | LEGO EV3 Large Motor | A | Drives the rear propulsion system |
| Steering | LEGO EV3 Medium Motor | B | Actuates the front Ackermann-style steering linkage |

The system can be understood as:

```text
                    LEGO EV3
                       │
          ┌────────────┴────────────┐
          │                         │
          ▼                         ▼
        PORT A                    PORT B
          │                         │
          ▼                         ▼
     LARGE MOTOR               MEDIUM MOTOR
          │                         │
          ▼                         ▼
   REAR PROPULSION           FRONT STEERING
          │                         │
          └────────────┬────────────┘
                       ▼
                  VEHICLE MOTION
```

Using only two motors reduces wiring, actuator count, mechanical complexity, and the number of systems that need to be calibrated before a run.

---

## 3.2 Motor A — LEGO EV3 Large Motor

The **LEGO Mindstorms EV3 Large Motor** is connected to **Motor Port A** and is Piolín's only propulsion motor.

The propulsion chain is:

```text
EV3
 ↓
Motor Port A
 ↓
Large Motor
 ↓
Rear drivetrain
 ↓
Rear wheels
 ↓
Vehicle translation
```

The Large Motor was selected for propulsion because this actuator must overcome the mechanical resistance of the complete vehicle. When Piolín accelerates, the propulsion motor must move the robot's full mass. It must also maintain vehicle motion while the front wheels are turned, reverse when required, and continue producing useful drivetrain torque throughout the course.

The EV3 determines the requested motor command, but the resulting vehicle motion depends on the complete mechanical system. Axle alignment, wheel traction, drivetrain friction, gearing, vehicle mass, battery condition, and steering angle can all influence the physical result.

For this reason:

```text
Motor command
≠
exact vehicle speed
```

unless the complete vehicle response has been physically measured.

---

## 3.3 Why a Large Motor Was Selected for Propulsion

The propulsion motor experiences a fundamentally different type of load from the steering motor.

Motor A must continuously transfer energy into vehicle movement. It needs to:

```text
accelerate the complete robot

maintain forward motion

reverse the vehicle

continue driving during steering

recover after maneuvers
```

The EV3 Large Motor is therefore assigned to the mechanically heavier propulsion task, while the Medium Motor is reserved for controlled steering movement.

The selection follows the physical requirements of each subsystem:

```text
Vehicle propulsion
        ↓
larger continuous mechanical demand
        ↓
Large Motor
```

while:

```text
Steering
        ↓
controlled angular positioning
        ↓
Medium Motor
```

The choice was therefore based on actuator role rather than simply using identical motors throughout the robot.

---

## 3.4 Rear-Wheel Propulsion

Piolín uses rear-wheel propulsion rather than differential drive.

The architecture separates the two main mobility functions:

```text
FRONT
↓
STEERING


REAR
↓
PROPULSION
```

This allows the front assembly to focus on steering geometry while the rear section is responsible for generating longitudinal vehicle motion.

A more complex vehicle could use front-wheel drive, four-wheel drive, or multiple independent propulsion motors. Those alternatives can provide additional capabilities, but they also introduce more drivetrain elements, actuator synchronization, wiring, mass, and software complexity.

Piolín's current requirements can be satisfied with:

```text
1 propulsion motor
+
1 steering motor
```

so the simpler architecture was retained.

---

## 3.5 Motor A and Vehicle Speed

The software can change the command sent to Motor A, but the relationship between that command and actual vehicle speed is not perfectly constant.

Vehicle motion can be influenced by:

```text
motor command

battery condition

drivetrain resistance

wheel traction

vehicle mass

steering angle

track surface
```

Piolín may therefore travel differently at the same nominal drive command when the steering system is centered compared with when the front wheels are strongly turned.

During steering, additional rolling and lateral resistance can appear at the tires.

This means the propulsion and steering systems are mechanically separate but dynamically connected.

The software must therefore consider the interaction between:

```text
DRIVE SPEED
+
STEERING INTENSITY
```

especially during corners and obstacle maneuvers.

---

## 3.6 Motor Encoder Feedback

The LEGO EV3 motors include rotational feedback through their internal encoders. This allows Piolín to reason about motor rotation rather than controlling movement only through elapsed time.

Conceptually:

```text
Motor command
     ↓
Motor rotates
     ↓
Encoder measures rotation
     ↓
EV3 reads motor position
```

Motor A encoder information can be useful for:

```text
relative forward displacement

reverse movement

parking approach

movement verification
```

However:

```text
motor rotation
≠
perfect vehicle odometry
```

because the physical drivetrain can experience:

```text
tire slip

mechanical compliance

gear backlash

wheel deformation

turning losses
```

Encoder information is therefore treated as a useful motion reference rather than a perfect measurement of Piolín's real-world position.

---

## 3.7 Motor Rotation and Theoretical Distance

If wheel circumference and drivetrain ratio are known, theoretical displacement can be estimated from motor rotation.

For a directly driven wheel:

```text
DISTANCE =
(MOTOR_ROTATION / 360)
×
WHEEL_CIRCUMFERENCE
```

If a gear ratio exists:

```text
G =
MOTOR_ROTATION / WHEEL_ROTATION
```

then:

```text
WHEEL_ROTATION =
MOTOR_ROTATION / G
```

and:

```text
DISTANCE =
(MOTOR_ROTATION / (360 × G))
×
WHEEL_CIRCUMFERENCE
```

These equations describe the theoretical relationship between actuator motion and vehicle displacement.

The current V4 wheel diameter and final drivetrain ratio should be physically verified before numerical values are substituted into these equations as official Piolín specifications.

---

## 3.8 Motor B — LEGO EV3 Medium Motor

Motor B is a **LEGO Mindstorms EV3 Medium Motor** dedicated to steering.

<div align="center">

<img
  src="../../v-photos/v4/motor_b_medium_steering.jpg"
  alt="LEGO EV3 Medium Motor installed as Piolín's steering actuator"
  width="680"
/>

<br>

<sub><b>Figure 3.2.</b> EV3 Medium Motor installed as Motor B and connected to Piolín's Ackermann-style steering mechanism.</sub>

</div>

Unlike Motor A, Motor B does not continuously propel the robot. Its primary responsibility is controlled angular positioning.

The steering actuation path is:

```text
EV3
 ↓
Motor Port B
 ↓
Medium Motor
 ↓
Mechanical steering linkage
 ↓
Front-wheel angles
 ↓
Vehicle turning trajectory
```

The steering motor must be able to:

```text
move left

move right

return toward center

hold an intermediate steering request

change direction during recovery
```

rather than continuously rotate through a propulsion drivetrain.

---

## 3.9 Why a Medium Motor Was Selected for Steering

The steering actuator benefits from different characteristics than the propulsion actuator.

The front steering system needs:

```text
compact installation

controlled angular movement

quick direction changes

repeatable positioning
```

The Medium Motor fits this role while allowing the front section of the chassis to remain relatively compact.

The comparison between the motors is therefore functional.

| Characteristic | Large Motor — A | Medium Motor — B |
| :--- | :--- | :--- |
| Main role | Propulsion | Steering |
| Operation in Piolín | Continuous/variable rotation | Limited angular positioning |
| Mechanical responsibility | Complete vehicle movement | Steering linkage |
| Connected subsystem | Rear drivetrain | Front Ackermann mechanism |
| Encoder use | Rotation / displacement reference | Steering-position reference |

This division prevents one actuator from being required to perform two mechanically different tasks.

---

## 3.10 Steering Motor Position Is Not Wheel Angle

A critical detail in Piolín's steering system is:

```text
Motor B angle
≠
physical wheel angle
```

The Medium Motor rotates a mechanical linkage. That linkage then changes the orientation of the front wheels.

<div align="center">

<img
  src="../../v-photos/v4/ackermann_top.jpg"
  alt="Piolín steering linkage showing the connection between Motor B and front wheels"
  width="720"
/>

<br>

<sub><b>Figure 3.3.</b> Ackermann-style linkage through which Motor B rotation becomes coordinated physical movement of the front wheels.</sub>

</div>

The relationship is:

```text
Motor encoder angle
        ↓
Steering linkage geometry
        ↓
Steering-arm displacement
        ↓
Left wheel angle
+
Right wheel angle
```

The relationship is not assumed to be perfectly linear across the full steering range.

For this reason, Piolín's steering system must be calibrated from the actual installed mechanism rather than assuming:

```text
10° motor rotation
=
10° wheel rotation
```

No such equality is used in the current documentation.

---

## 3.11 Mechanical Center

The most important steering reference is the **mechanical center**.

When Piolín is intended to travel straight, the steering mechanism should return to a repeatable physical position in which the front wheels are approximately aligned with the chassis.

Software can define a reference such as:

```text
STEERING_CENTER
```

from which left and right steering requests are measured.

Conceptually:

```text
LEFT
←
CENTER
→
RIGHT
```

The exact numerical convention depends on the active program.

The important engineering requirement is consistency between:

```text
software center
```

and:

```text
physical wheel center
```

If those references do not match, a command intended to drive straight can create a continuous curved trajectory.

The exact V4 center and wheel angles belong to the detailed steering calibration rather than being assumed in this component overview.

---

## 3.12 Steering Limits

The steering mechanism has finite physical limits.

Driving Motor B beyond its useful mechanical range can create:

```text
mechanical stress

linkage binding

increased motor load

little additional useful wheel movement
```

The software should therefore constrain steering commands to a validated **usable range** rather than attempting to reach the absolute point where the mechanism can no longer move.

The final left and right steering limits should be measured on the current V4 mechanism before they are published numerically.

This is especially important because:

```text
motor limit
```

and:

```text
useful steering limit
```

are not necessarily the same thing.

---

## 3.13 Ackermann Steering and Motor B

Motor B acts on an Ackermann-style steering mechanism rather than forcing both front wheels to remain at exactly the same steering angle.

During a turn, the inner and outer front wheels follow different-radius paths.

Conceptually:

```text
INNER FRONT WHEEL
→ smaller turning radius
→ larger steering angle


OUTER FRONT WHEEL
→ larger turning radius
→ smaller steering angle
```

The detailed geometry, including the new `ackermann_geometry` and `ackermann_angles` evidence, is documented in the dedicated mobility/steering section rather than duplicated here.

For this component document, the important point is that one Motor B input is mechanically transformed into coordinated movement of both front wheels.

---

## 3.14 Steering Movement Evidence

<div align="center">

<img
  src="../../v-photos/v4/steering_motion.gif"
  alt="Piolín steering movement from one side through center toward the opposite side"
  width="680"
/>

<br>

<sub><b>Figure 3.4.</b> Real movement of Piolín's current front steering mechanism through its usable range.</sub>

</div>

The steering-motion GIF provides direct evidence of the installed mechanism.

It shows properties that are more difficult to communicate through a static description, including:

```text
linkage movement

relative wheel movement

mechanical clearance

return through center
```

The animation should not be interpreted as proof of mathematically perfect Ackermann geometry.

It demonstrates the **actual physical steering mechanism that Motor B must control**.

---

## 3.15 Coordinating Motor A and Motor B

Piolín's trajectory is produced by combining propulsion and steering.

```text
Motor A
→ longitudinal movement


Motor B
→ steering geometry
```

Neither actuator alone defines the complete vehicle path.

For example, a strong steering request while Motor A is driving rapidly can produce a different trajectory from the same steering request at a lower speed.

The relationship can be represented as:

```text
VEHICLE TRAJECTORY
=
f(
drive motion,
steering geometry,
traction,
vehicle state
)
```

This is why steering and propulsion should not be tuned as completely independent systems.

---

## 3.16 Motors During the Open Challenge

The motor hardware is identical in both competition rounds.

During Open, the EV3 uses:

```text
S1 Gyro

S2 Left Ultrasonic

S3 Right Ultrasonic

S4 Color
```

to determine the requested propulsion and steering behavior.

The relationship is:

```text
wall geometry
+
gyro orientation
+
course state
       ↓
EV3
       ↓
Motor A
+
Motor B
```

Motor A provides the forward movement required to traverse the course, while Motor B responds to the steering decision produced from the current wall, heading, and course state.

The gyro does not physically steer Piolín. It changes the information the EV3 uses to determine Motor B's command.

---

## 3.17 Motors During Cornering

Corners create one of the strongest interactions between Motor A and Motor B.

During a straight:

```text
Motor B
→ near steering center

Motor A
→ propulsion
```

When a corner is detected:

```text
corner state begins
      ↓
steering request increases
      ↓
Motor B changes front-wheel orientation
      ↓
Motor A continues moving vehicle
      ↓
curved trajectory develops
```

The physical shape of the corner depends on several variables:

```text
steering geometry

forward motion

entry position

entry orientation

traction
```

Therefore a corner that is too wide is not automatically caused by insufficient Motor B steering.

Vehicle speed and entry geometry can also contribute.

---

## 3.18 Motors During the Obstacle Challenge

During Obstacles, Motor A and Motor B remain physically unchanged.

What changes is the sensor information used by the EV3.

```text
Pixy2.1
→ visual obstacle information


Ultrasonics
→ track geometry


Color
→ course state
```

A green pillar requires a left-side pass:

```text
GREEN
→ PASS LEFT
```

while a red pillar requires a right-side pass:

```text
RED
→ PASS RIGHT
```

However, those rules do not correspond to one permanent Motor B angle.

The EV3 must determine a maneuver according to the current obstacle position, wall geometry, vehicle state, and steering history.

Motor A must simultaneously move Piolín through the maneuver at a speed compatible with the available steering response.

---

## 3.19 Countersteering and Recovery

Avoiding an obstacle does not end as soon as Piolín moves to one side of the pillar.

The vehicle must also recover a useful trajectory afterward.

A conceptual sequence is:

```text
avoid
   ↓
pass
   ↓
countersteer
   ↓
recover
   ↓
continue
```

Motor B therefore frequently changes from an avoidance steering request toward an opposite or reduced steering request during recovery.

If countersteering begins too early, Piolín can return toward the obstacle.

If it begins too late, the robot may remain displaced toward a wall or enter the next section with poor alignment.

This demonstrates why steering actuation is closely connected to the obstacle state machine rather than being a simple color-to-angle mapping.

---

## 3.20 Reverse Motion

Motor A can also reverse Piolín.

Reverse movement can be useful when the robot needs additional space for:

```text
recovery

obstacle approach adjustment

parking

repositioning
```

The mechanical system remains the same:

```text
Motor A
→ rear-wheel movement


Motor B
→ front-wheel steering
```

but vehicle trajectory while reversing must be treated as its own maneuver.

An Ackermann vehicle moving backward does not behave from the controller's perspective exactly like the same vehicle moving forward.

Reverse behavior therefore requires physical testing rather than assuming forward steering logic can be reused unchanged.

---

## 3.21 Parking

Parking is one of the clearest examples of Motor A and Motor B working together.

A parking sequence can involve:

```text
course progress detection

controlled approach

steering alignment

forward or reverse displacement

final stopping condition
```

Motor A produces the required movement while Motor B determines the vehicle orientation during that movement.

Because Piolín's final parking strategy is still being tuned, this document does not present a single motor angle, encoder displacement, or timed maneuver as the final solution.

The motor hardware is defined.

The exact parking behavior belongs to the software and calibration layers.

---

## 3.22 Mechanical Load and Motor Response

Motor response depends on mechanical load.

For Motor A, important sources include:

```text
vehicle mass

drivetrain friction

wheel traction

steering angle

track surface
```

For Motor B, load can increase because of:

```text
tire friction

steering linkage friction

mechanical misalignment

linkage binding

front-wheel loading
```

A motor that appears weak therefore does not automatically have an electrical or software problem.

The failure may be mechanical.

Motor diagnostics should distinguish between:

```text
command problem

actuator problem

mechanical transmission problem
```

before software values are changed.

---

## 3.23 Mechanical Alignment and Propulsion Efficiency

The rear drivetrain must rotate freely and remain properly aligned.

If an axle is misaligned or a wheel rubs against the chassis, Motor A must overcome additional resistance.

This can produce symptoms such as:

```text
reduced speed

greater motor load

different acceleration

inconsistent encoder-based movement
```

The correct response is not necessarily to increase the motor command.

Reducing unnecessary drivetrain resistance can provide a more reliable solution and makes later software calibration more meaningful.

---

## 3.24 Mechanical Alignment and Steering Load

The same principle applies to Motor B.

If the steering linkage is too tight or misaligned, the Medium Motor may:

```text
move slowly

fail to reach the requested position

return inconsistently

produce different left/right behavior
```

The first diagnostic should therefore examine the physical mechanism.

A useful sequence is:

```text
inspect linkage
      ↓
check free mechanical movement
      ↓
verify Motor B response
      ↓
verify physical wheel response
      ↓
then tune software
```

This prevents software from compensating for avoidable mechanical resistance.

---

## 3.25 Motor Commands vs. Physical Results

A recurring engineering distinction in Piolín is:

```text
software command
≠
guaranteed physical result
```

For example:

```text
Motor A command
≠
exact vehicle speed
```

and:

```text
Motor B command
≠
exact front-wheel angle
```

The physical result passes through several layers:

```text
COMMAND
   ↓
MOTOR
   ↓
MECHANICAL TRANSMISSION
   ↓
WHEELS
   ↓
TRACK INTERACTION
   ↓
VEHICLE MOTION
```

This is why final parameters must be calibrated on the assembled robot rather than inferred from motor commands alone.

---

## 3.26 Alternative Actuation Architectures

Several alternative vehicle architectures could theoretically have been used.

| Architecture | Advantage | Limitation for Piolín |
| :--- | :--- | :--- |
| Differential drive | Mechanically simple turning control | Does not reproduce the selected car-like steering model |
| Multiple independent drive motors | Additional propulsion control | More mass, wiring, synchronization, and complexity |
| Large Motor for both drive and steering | High steering torque | Larger steering actuator than currently required |
| Medium Motor for both drive and steering | Compact | Less appropriate division of actuator roles |
| **Large Motor drive + Medium Motor steering** | **Actuator role matches mechanical demand** | **Requires coordinated car-like control** |

The current configuration was selected because each motor is assigned according to the mechanical task it performs.

Piolín does not maximize the number or size of its motors. It uses two actuators with clearly separated responsibilities.

---

## 3.27 Why Two Motors Are Enough

Adding more motors does not automatically improve the vehicle.

Additional actuators would introduce:

```text
more mass

more cables

more ports

more electrical demand

more synchronization

more mechanical components
```

The current architecture already provides the two independently controllable quantities required for Piolín's mobility:

```text
longitudinal propulsion

steering direction
```

Therefore:

```text
2 motors
=
2 required actuation roles
```

An additional motor would only be justified if it solved a clearly identified mechanical requirement that the current architecture could not address.

---

## 3.28 Motor Architecture Evolution

Piolín's mobility architecture evolved toward a clear distinction between:

```text
DRIVE
```

and:

```text
STEERING
```

The final system behaves as a small vehicle rather than a conventional educational differential-drive platform.

This separation became especially useful when testing WRO-specific behaviors such as:

```text
smooth wall following

cornering

pillar avoidance

countersteering

parking
```

The current architecture was retained because its mechanical behavior matches the type of navigation required by Future Engineers.

---

## 3.29 Current Motor Configuration

The current motor hardware is:

```text
MOTOR A
LEGO Mindstorms EV3 Large Motor

Role:
Rear propulsion


MOTOR B
LEGO Mindstorms EV3 Medium Motor

Role:
Front Ackermann-style steering
```

The configuration remains identical between rounds.

```text
OPEN

A = Large Drive
B = Medium Steering
```

```text
OBSTACLES

A = Large Drive
B = Medium Steering
```

Only the sensing architecture changes.

This allows both motor systems to be mechanically validated on one common vehicle platform.

---

## 3.30 Values Intentionally Not Claimed as Final

The following values should only be published numerically after they are measured on the current V4 robot:

```text
final drivetrain gear ratio

maximum vehicle speed

maximum useful drive command

current rear wheel diameter

current front wheel diameter

exact steering-motor limits

exact physical inner-wheel angle

exact physical outer-wheel angle

Motor B angle to wheel-angle relationship

minimum turning radius

measured acceleration

measured stopping distance
```

Older measurements may remain useful in development history, but they should not automatically become current motor specifications.

---

## 3.31 Motor System Engineering Principle

Piolín's motor system follows one central principle:

> **Actuator selection should match the physical task instead of using identical motors for mechanically different responsibilities.**

The Large Motor is responsible for moving the complete vehicle.

The Medium Motor is responsible for positioning the steering mechanism.

```text
                  LEGO EV3
                     │
          ┌──────────┴──────────┐
          │                     │
          ▼                     ▼
       MOTOR A               MOTOR B
          │                     │
          ▼                     ▼
     LARGE MOTOR           MEDIUM MOTOR
          │                     │
          ▼                     ▼
   REAR PROPULSION       ACKERMANN STEERING
          │                     │
          └──────────┬──────────┘
                     ▼
               VEHICLE MOTION
```

The simplicity of this architecture is one of its strengths. Each motor has one clear responsibility, each physical effect can be diagnosed independently, and the EV3 can coordinate both actuators from the same autonomous control system.

---

<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
