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

This separation was selected because Piolín is not a differential-drive robot. The vehicle does not turn by changing the speeds of two independent drive motors. Instead, propulsion and steering are mechanically separated in the same way they are in a conventional car.

This has important consequences for the complete robot architecture. Motor A determines how quickly Piolín moves along its trajectory, while Motor B determines the shape of that trajectory. The EV3 software must therefore coordinate both actuators instead of treating them as two interchangeable motors.

---

## 3.1 Final Motor Architecture

The current motor configuration is intentionally simple.

| Function | Motor | EV3 Port | Mechanical Responsibility |
| :--- | :--- | :---: | :--- |
| Propulsion | LEGO EV3 Large Motor | A | Drives the rear drivetrain |
| Steering | LEGO EV3 Medium Motor | B | Actuates the front Ackermann steering linkage |

<div align="center">

<img
  src="../../embed/motor_role_architecture.png"
  alt="Piolín propulsion and steering motor architecture"
  width="820"
/>

<br>

<sub><b>Figure 3.2.</b> Separation of Piolín's actuation system into propulsion and steering responsibilities.</sub>

</div>

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

Using only two motors also reduces wiring, software complexity, mechanical mass, and the number of actuators that need to be calibrated before a run.

---

## 3.2 Motor A — LEGO EV3 Large Motor

The **LEGO Mindstorms EV3 Large Motor** is connected to **Motor Port A** and is Piolín's only propulsion motor.

<div align="center">

<img
  src="../../v-photos/v4/drive_motor_mount.jpg"
  alt="EV3 Large Motor mounting and drivetrain connection on Piolín"
  width="680"
/>

<br>

<sub><b>Figure 3.3.</b> Mechanical installation of Motor A showing its relationship with Piolín's rear drivetrain.</sub>

</div>

The Large Motor was selected for propulsion because this actuator must overcome the mechanical resistance of the complete vehicle. When Piolín accelerates, the propulsion motor is responsible for accelerating the robot's full mass. It must also maintain vehicle motion while the front wheels are turned, reverse when required, and continue producing useful wheel torque throughout the complete course.

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

<div align="center">

<img
  src="../../embed/drivetrain_power_flow.png"
  alt="Piolín propulsion power flow from Motor A to the rear wheels"
  width="820"
/>

<br>

<sub><b>Figure 3.4.</b> Mechanical propulsion path from the EV3 Large Motor to the rear wheels.</sub>

</div>

The EV3 determines the requested motor command, but the resulting vehicle motion depends on the complete mechanical system. Axle alignment, wheel traction, drivetrain friction, gearing, vehicle mass, battery condition, and steering angle all influence the physical result.

For this reason, a motor command should not be interpreted as an exact vehicle speed without measurement.

---

## 3.3 Why a Large Motor Was Selected for Propulsion

The propulsion motor experiences a different type of load than the steering motor.

Motor A must continuously transfer energy into vehicle motion. It needs sufficient mechanical capability to:

```text
accelerate the complete robot

maintain forward motion

reverse the vehicle

continue driving during steering

recover after obstacle maneuvers
```

The EV3 Large Motor is better suited to this role than the Medium Motor because Piolín's propulsion system benefits more from torque capacity and sustained drivetrain operation than from compact steering-oriented actuation.

Using the Medium Motor as the primary drive actuator would reduce the distinction between the actuator roles and could make the propulsion system more sensitive to changes in vehicle load or drivetrain resistance.

The final selection therefore follows the physical demand of each subsystem:

```text
Higher continuous vehicle load
        ↓
Large Motor
        ↓
Propulsion
```

while:

```text
Controlled angular positioning
        ↓
Medium Motor
        ↓
Steering
```

---

## 3.4 Rear-Wheel Propulsion

Piolín uses rear-wheel propulsion rather than front-wheel drive or differential drive.

<div align="center">

<img
  src="../../v-photos/v4/rear_drivetrain_top.jpg"
  alt="Piolín rear drivetrain viewed from above"
  width="700"
/>

<br>

<sub><b>Figure 3.5.</b> Rear drivetrain through which Motor A transfers propulsion to the vehicle.</sub>

</div>

This choice separates the two main mechanical functions of the vehicle.

The front wheels primarily determine direction, while the rear wheels primarily generate longitudinal motion.

```text
FRONT
↓
STEERING


REAR
↓
PROPULSION
```

This is useful because the steering linkage can be optimized for controlled wheel-angle movement without also having to transmit propulsion torque through the same moving steering joints.

The rear drive layout also allows the front assembly to remain mechanically focused on Ackermann steering geometry.

---

## 3.5 Motor A and Vehicle Speed

The software can change the command sent to Motor A, but the relationship between motor command and actual vehicle speed is not perfectly constant.

Vehicle speed depends on several factors:

```text
motor command

battery condition

drivetrain resistance

wheel traction

vehicle mass

steering angle

track surface
```

For example, Piolín may travel differently at the same nominal drive command when the front wheels are centered compared with when they are strongly turned.

During strong steering, the vehicle experiences additional rolling and lateral resistance. This means that the propulsion system and steering system cannot be treated as completely independent physical systems even though they use separate motors.

The software must therefore consider the interaction between:

```text
DRIVE SPEED
+
STEERING INTENSITY
```

especially during corners and obstacle avoidance.

---

## 3.6 Motor Encoder Feedback

The LEGO EV3 motors provide rotational feedback through their internal encoders. This allows the software to reason about motor rotation rather than controlling the actuator only through time.

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

This is particularly useful for movements such as:

```text
controlled forward displacement

reverse movement

parking approach

steering-centering procedures
```

However, encoder rotation should not automatically be interpreted as exact vehicle displacement.

For propulsion:

```text
Motor rotation
      ↓
Drivetrain rotation
      ↓
Wheel rotation
      ↓
Theoretical distance
```

but the physical robot may experience:

```text
tire slip

mechanical compliance

gear backlash

wheel deformation

turning losses
```

Therefore encoder-based movement is useful, but it is not equivalent to perfect odometry.

---

## 3.7 Motor Rotation and Theoretical Vehicle Distance

If the effective wheel circumference and drivetrain ratio are known, theoretical displacement can be estimated from motor rotation.

For a directly driven wheel:

```text
DISTANCE =
(MOTOR_ROTATION / 360)
×
WHEEL_CIRCUMFERENCE
```

If a gear ratio exists between the motor and wheel:

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

These equations are useful for understanding the drivetrain, but the final Piolín documentation should only substitute numerical wheel dimensions and gear ratios after the current V4 robot has been physically measured.

<div align="center">

<img
  src="../../embed/motor_encoder_distance.png"
  alt="Relationship between motor encoder rotation and theoretical vehicle distance"
  width="800"
/>

<br>

<sub><b>Figure 3.6.</b> Relationship between Motor A encoder rotation, drivetrain transmission, wheel rotation, and theoretical vehicle displacement.</sub>

</div>

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

<sub><b>Figure 3.7.</b> EV3 Medium Motor installed as Motor B and connected to Piolín's Ackermann steering mechanism.</sub>

</div>

Unlike Motor A, Motor B does not continuously propel the robot. Its main responsibility is controlled angular positioning.

The actuation path is:

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

The Medium Motor was selected because steering requires relatively fast and repeatable position changes within a limited motion range.

The steering motor must be able to:

```text
move left

move right

return toward center

hold an intermediate steering request

change direction during recovery
```

rather than rotate continuously through an unrestricted drivetrain.

---

## 3.9 Why a Medium Motor Was Selected for Steering

Using a Large Motor for steering would provide greater mechanical size and torque capability, but those characteristics are not necessarily advantageous in the front steering system.

The steering actuator benefits from:

```text
compact installation

controlled angular movement

lower moving-system mass

quick directional response
```

The Medium Motor fits the steering mechanism more naturally and allows the front section of the chassis to remain more compact.

The comparison between the two selected actuators is therefore functional rather than simply based on which motor is stronger.

| Characteristic | Large Motor — A | Medium Motor — B |
| :--- | :--- | :--- |
| Main role | Propulsion | Steering |
| Typical operation in Piolín | Continuous/variable rotation | Limited angular positioning |
| Mechanical load | Complete vehicle motion | Steering linkage |
| Connected mechanism | Rear drivetrain | Front Ackermann linkage |
| Software variable | Drive command | Steering command |
| Encoder use | Rotation/displacement reference | Steering-position reference |

This division prevents one actuator from being required to perform two very different mechanical tasks.

---

## 3.10 Steering Motor Position Is Not Wheel Angle

A critical detail in Piolín's steering system is that:

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

<sub><b>Figure 3.8.</b> Ackermann-style linkage through which Motor B rotation becomes physical front-wheel steering.</sub>

</div>

The relationship can be represented conceptually as:

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

The relationship is not necessarily linear across the complete range.

This is why the steering system must be calibrated mechanically rather than assuming that:

```text
10° motor rotation
=
10° wheel rotation
```

No such equality is assumed in the current documentation.

---

## 3.11 Mechanical Center

The most important steering reference is the **mechanical center**.

When Piolín is intended to travel straight, the front steering system should return to a physical alignment in which the wheels are approximately centered relative to the chassis.

<div align="center">

<img
  src="../../v-photos/v4/ackermann_center.jpg"
  alt="Piolín front wheels at steering center"
  width="680"
/>

<br>

<sub><b>Figure 3.9.</b> Front steering mechanism at its mechanical center reference.</sub>

</div>

Software can then use a steering-center reference:

```text
STEERING_CENTER
```

from which left and right commands are measured.

Conceptually:

```text
negative / one direction
←
CENTER
→
positive / opposite direction
```

The exact numerical convention depends on the current program.

The important engineering requirement is consistency between:

```text
software center
```

and:

```text
physical wheel center
```

If these do not match, a software command intended to drive straight can create a continuous curved trajectory.

---

## 3.12 Steering Limits

The steering mechanism has finite physical limits.

<div align="center">

<img
  src="../../v-photos/v4/ackermann_left_lock.jpg"
  alt="Piolín steering mechanism near its left physical limit"
  width="620"
/>

<br>

<sub><b>Figure 3.10.</b> Steering mechanism near the left side of its usable range.</sub>

</div>

<div align="center">

<img
  src="../../v-photos/v4/ackermann_right_lock.jpg"
  alt="Piolín steering mechanism near its right physical limit"
  width="620"
/>

<br>

<sub><b>Figure 3.11.</b> Steering mechanism near the right side of its usable range.</sub>

</div>

These limits exist because the mechanical linkage cannot rotate indefinitely.

Driving Motor B beyond the useful steering range can create:

```text
mechanical stress

linkage deformation

increased motor load

unpredictable wheel geometry
```

The software should therefore keep steering requests inside a validated usable range rather than treating the Medium Motor as an unrestricted actuator.

The final numerical limits should be documented after the V4 steering mechanism is measured and calibrated.

---

## 3.13 Ackermann Steering and Motor B

Motor B acts on an Ackermann-style steering mechanism rather than rotating both wheels to exactly the same angle.

During an ideal turn:

```text
INNER FRONT WHEEL
→ larger steering angle


OUTER FRONT WHEEL
→ smaller steering angle
```

because the inner wheel follows a smaller turning radius.

<div align="center">

<img
  src="../../embed/ackermann_linkage_annotated.png"
  alt="Annotated Piolín Ackermann steering linkage"
  width="820"
/>

<br>

<sub><b>Figure 3.12.</b> Annotated steering linkage showing how one Motor B input produces coordinated movement of both front wheels.</sub>

</div>

This improves vehicle-like turning compared with a front axle where both steering wheels are forced into identical angles.

The detailed Ackermann geometry is documented in the mechanical steering section, but Motor B is the actuator that makes that geometry usable by the autonomous controller.

---

## 3.14 Steering Movement Evidence

<div align="center">

<img
  src="../../v-photos/v4/steering_motion.gif"
  alt="Piolín steering movement from left through center to right"
  width="680"
/>

<br>

<sub><b>Figure 3.13.</b> Real movement of the current steering mechanism through its usable range.</sub>

</div>

The steering-motion GIF is valuable because it provides direct physical evidence that Motor B actuates both front wheels through the installed linkage.

It also helps document properties that are difficult to communicate through a static diagram, including:

```text
linkage motion

relative wheel movement

mechanical clearance

return toward center
```

The GIF should not be treated as proof that the geometry is mathematically perfect Ackermann. Instead, it demonstrates the actual installed mechanism that the software must control.

---

## 3.15 Coordinating Motor A and Motor B

Piolín's movement is produced by combining propulsion and steering.

```text
Motor A
→ how strongly the robot moves


Motor B
→ where that motion is directed
```

Neither actuator alone defines the complete trajectory.

For example, a strong steering command while the drive motor is moving quickly can create:

```text
larger lateral acceleration

greater tire scrub

larger swept path

more difficult recovery
```

The same steering request at a lower propulsion speed can produce a more controlled maneuver.

This means the EV3 software must consider vehicle speed when choosing steering behavior.

<div align="center">

<img
  src="../../embed/drive_steering_interaction.png"
  alt="Interaction between propulsion speed and steering command"
  width="820"
/>

<br>

<sub><b>Figure 3.14.</b> Vehicle motion results from the combined effect of Motor A propulsion and Motor B steering.</sub>

</div>

---

## 3.16 Motors During the Open Challenge

The motor hardware is identical in both competition rounds.

During Open, the EV3 uses information from:

```text
S1 Gyro

S2 Left Ultrasonic

S3 Right Ultrasonic

S4 Color
```

to determine the appropriate Motor A and Motor B commands.

The interaction is:

```text
wall geometry
+
gyro heading
+
course state
       ↓
EV3
       ↓
drive request
+
steering request
       ↓
Motor A + Motor B
```

Motor A provides the forward motion required to traverse the course, while Motor B reacts to wall position, heading error, and corner state.

The gyro does not physically steer the robot. It changes the information used by the EV3 to decide the Motor B command.

---

## 3.17 Motors During Cornering

Corners create one of the strongest interactions between the two motors.

During a straight, Motor B should remain relatively close to the steering center while Motor A provides forward propulsion.

Approaching a corner:

```text
corner detected
      ↓
steering request increases
      ↓
Motor B changes wheel angles
      ↓
vehicle begins curved trajectory
```

The propulsion motor continues moving the robot through this trajectory.

The software can reduce, maintain, or otherwise adjust Motor A depending on how aggressive the curve needs to be.

The physical result depends on both actuators simultaneously.

```text
Corner shape
≈
Steering geometry
+
Vehicle speed
+
Mechanical traction
```

This is why a corner that appears too wide is not automatically a Motor B problem. It can also result from excessive propulsion speed.

---

## 3.18 Motors During the Obstacle Challenge

During Obstacles, Motor A and Motor B remain physically unchanged.

What changes is the information used by the EV3.

```text
Pixy2.1
→ obstacle signature and position


Ultrasonics
→ wall geometry


Color
→ course state
```

The resulting avoidance maneuver requires coordinated actuation.

For a green pillar:

```text
GREEN
→ required LEFT passing side
```

For a red pillar:

```text
RED
→ required RIGHT passing side
```

However, the color does not directly determine one fixed steering-motor angle.

The EV3 must consider:

```text
pillar position

pillar size

wall distances

vehicle speed

previous steering state
```

before commanding Motor B.

Motor A must also move the vehicle through the maneuver at a speed that allows the steering system enough time to react.

---

## 3.19 Countersteering and Recovery

Obstacle avoidance does not end when Piolín moves to one side of a pillar.

After passing the obstacle, the vehicle must recover a useful trajectory.

This often requires **countersteering**.

Conceptually:

```text
avoid pillar
      ↓
vehicle displaced laterally
      ↓
pillar passed
      ↓
reverse steering tendency
      ↓
Motor B countersteers
      ↓
vehicle returns toward normal path
```

<div align="center">

<img
  src="../../embed/obstacle_steering_sequence.png"
  alt="Motor B obstacle avoidance and countersteering sequence"
  width="850"
/>

<br>

<sub><b>Figure 3.15.</b> Steering sequence during obstacle avoidance: initial avoidance, passing phase, countersteering, and recovery.</sub>

</div>

If the countersteering begins too early, the robot can move back toward the pillar.

If it begins too late, Piolín can remain too close to a wall or enter the next section with an incorrect trajectory.

This demonstrates why Motor B behavior is closely connected to obstacle-state logic.

---

## 3.20 Reverse Motion

Motor A is capable of reversing Piolín.

Reverse movement is useful when the robot needs to create additional space before reacting to:

```text
an obstacle

a wall

a failed approach

a parking maneuver
```

The mechanical architecture does not change during reverse motion. Motor B continues controlling the front steering geometry while Motor A drives the rear wheels in the opposite direction.

However, the relationship between steering and vehicle path changes from the driver's perspective because the robot is moving backward.

For this reason, reverse behavior should be tested as a vehicle maneuver rather than assumed to behave identically to forward steering.

---

## 3.21 Parking

Parking is one of the situations where encoder feedback, propulsion control, and steering control can all interact.

A parking sequence may require:

```text
progress detection

controlled approach

steering alignment

forward or reverse movement

final displacement
```

Motor A provides the vehicle movement while Motor B determines the orientation of the vehicle during that movement.

Because the final parking strategies for both rounds are still being tuned, this document does not present one fixed motor-angle or encoder-distance value as final.

The motor hardware itself is already defined, while the exact parking control sequence belongs to the software and calibration layers.

---

## 3.22 Mechanical Load and Motor Response

Motor response depends on mechanical load.

For Motor A, sources of load include:

```text
robot mass

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

wheel load
```

A motor that appears weak does not necessarily have an electrical problem.

The failure may be mechanical.

This is why motor diagnostics should distinguish:

```text
Motor command problem

Motor hardware problem

Mechanical transmission problem
```

rather than changing software values immediately.

---

## 3.23 Mechanical Alignment and Propulsion Efficiency

The rear drivetrain should rotate freely and remain properly aligned.

<div align="center">

<img
  src="../../v-photos/v4/rear_drivetrain_bottom.jpg"
  alt="Bottom view of Piolín rear drivetrain"
  width="700"
/>

<br>

<sub><b>Figure 3.16.</b> Bottom view of the rear drivetrain, useful for examining axle alignment and mechanical transmission.</sub>

</div>

If an axle is misaligned or a wheel rubs against the chassis, Motor A must overcome additional resistance.

This can produce symptoms such as:

```text
reduced speed

asymmetric movement

greater battery demand

inconsistent encoder displacement
```

The correct response is not necessarily to increase motor command.

Improving the drivetrain mechanically can provide a better solution.

---

## 3.24 Mechanical Alignment and Steering Load

The same principle applies to Motor B.

If the steering linkage is too tight or misaligned, the Medium Motor may:

```text
move slowly

fail to reach requested position

return inconsistently

produce different left/right behavior
```

The first diagnostic should therefore be mechanical.

```text
Disconnect / unload steering
        ↓
Check free linkage motion
        ↓
Check motor response
        ↓
Reconnect system
```

This prevents software from compensating for avoidable physical resistance.

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
exact wheel angle
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

<div align="center">

<img
  src="../../embed/motor_command_to_motion.png"
  alt="Transformation from EV3 motor command to physical vehicle motion"
  width="850"
/>

<br>

<sub><b>Figure 3.17.</b> A motor command becomes vehicle motion only after passing through the actuator, mechanical transmission, wheel geometry, and track interaction.</sub>

</div>

This is why Piolín's final parameters must be calibrated on the assembled vehicle.

---

## 3.26 Alternative Actuation Architectures

Several vehicle architectures could theoretically have been used.

| Architecture | Advantage | Limitation for Piolín |
| :--- | :--- | :--- |
| Differential drive | Mechanically simple turning control | Does not reproduce car-like steering geometry |
| Two independent drive motors + steering | Potential for additional propulsion control | Greater weight, wiring, power demand, and control complexity |
| One Large Motor for drive + one Large Motor for steering | Greater steering torque | Larger steering actuator and unnecessary mechanical capacity |
| One Medium Motor for drive + one Medium Motor for steering | Compact | Less appropriate propulsion role |
| **Large Motor drive + Medium Motor steering** | **Actuator role matches mechanical demand** | Requires coordinated car-like control |

The current configuration was selected because each motor is assigned according to the mechanical task it performs.

Piolín therefore does not maximize the number or size of motors. It uses the actuator that best matches each subsystem.

---

## 3.27 Why Two Motors Are Enough

Adding more motors does not automatically improve the vehicle.

Additional motors would introduce:

```text
more mass

more cables

more ports

greater electrical demand

more synchronization

more mechanical components
```

The current architecture already provides the two independently controllable quantities required for vehicle motion:

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

Adding another motor would only be justified if it provided a clearly necessary mechanical function.

No such additional actuator is required in the current Piolín design.

---

## 3.28 Motor Architecture Evolution

Earlier robot configurations explored different mobility and steering arrangements before the current architecture stabilized.

The most important development was moving toward a clear separation between:

```text
DRIVE
```

and:

```text
STEERING
```

rather than treating the robot like a conventional two-wheel educational EV3 platform.

<div align="center">

<img
  src="../../embed/evolution_motor_architecture.png"
  alt="Evolution of Piolín motor and mobility architecture"
  width="880"
/>

<br>

<sub><b>Figure 3.18.</b> Evolution toward the current Large-Motor propulsion and Medium-Motor Ackermann steering architecture.</sub>

</div>

The current actuation architecture better matches the physical requirements of WRO Future Engineers because the robot behaves as a small autonomous vehicle rather than as a point-turning mobile base.

---

## 3.29 Current Motor Configuration

The current final motor hardware is:

```text
MOTOR A
LEGO Mindstorms EV3 Large Motor

Role:
Rear propulsion


MOTOR B
LEGO Mindstorms EV3 Medium Motor

Role:
Front Ackermann steering
```

The architecture is identical in both rounds.

```text
OPEN
A = Large Drive
B = Medium Steering


OBSTACLES
A = Large Drive
B = Medium Steering
```

Only the sensing configuration changes between Open and Obstacles.

This means that motor behavior can be developed and mechanically validated on one common vehicle platform.

---

## 3.30 Values Intentionally Not Claimed as Final

The following values should only be documented numerically after they are measured on the current V4 robot:

```text
final drivetrain gear ratio

maximum vehicle speed

maximum useful drive command

current rear wheel diameter

current front wheel diameter

exact steering-motor limits

exact physical left-wheel angle

exact physical right-wheel angle

motor-angle to wheel-angle relationship

minimum turning radius

measured acceleration

measured stopping distance
```

Older measurements may remain useful in development history, but they should not automatically become final motor specifications.

This keeps the motor documentation tied to the physical robot that will actually compete.

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
