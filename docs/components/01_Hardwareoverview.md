# 1. Hardware Overview

<div align="center">

<img
  src="../../v-photos/v4/piolin_open_isometric.jpg"
  alt="Piolín in its Open Challenge configuration"
  width="720"
/>

<br>

<sub><b>Figure 1.1.</b> Piolín in its Open Challenge configuration. The robot uses a LEGO Mindstorms EV3 platform with rear propulsion, front Ackermann steering, two lateral ultrasonic sensors, a downward-facing color sensor, and a Gyro Sensor connected to S1.</sub>

</div>

Piolín is the autonomous vehicle developed by **PiolínTech** for the **WRO Future Engineers 2026** competition. Its current hardware architecture is based almost completely on the LEGO Mindstorms EV3 ecosystem because the team found that keeping the primary motion, sensing, and control systems inside one compatible platform reduced integration complexity and made the robot easier to debug, calibrate, and reproduce.

The robot is controlled by a **LEGO Mindstorms EV3 Intelligent Brick**, which remains the central decision-making unit in both competition rounds. Propulsion is provided by one **LEGO EV3 Large Motor** connected to Motor Port A, while steering is controlled by one **LEGO EV3 Medium Motor** connected to Motor Port B. The vehicle uses rear-wheel propulsion and front Ackermann-style steering, creating a car-like motion model rather than differential steering.

Piolín uses two permanent lateral ultrasonic sensors and one permanent downward-facing color sensor. The left ultrasonic sensor is connected to S2, the right ultrasonic sensor is connected to S3, and the color sensor is connected to S4. The remaining sensor input, **S1**, is intentionally modular and changes depending on the competition round.

During the **Open Challenge**, S1 is occupied by the LEGO EV3 Gyro Sensor. During the **Obstacle Challenge**, the Gyro Sensor is removed and S1 is instead occupied by the **Pixy2.1 vision sensor**.

This round-specific configuration is one of the most important hardware decisions in the final Piolín architecture. Rather than forcing every possible sensor to remain connected simultaneously, the robot uses the same mechanical platform and changes only the device needed for the specific sensing problem of each challenge.

> [!IMPORTANT]
> Piolín does **not** use the Gyro Sensor and Pixy2.1 simultaneously in the current architecture.
>
> **Open Challenge:** S1 = EV3 Gyro Sensor  
> **Obstacle Challenge:** S1 = Pixy2.1

---

## 1.1 Final Hardware Architecture

The current robot is organized around a permanent vehicle platform and one challenge-specific sensing port.

| System | Current Component | Connection | Main Function |
| :--- | :--- | :---: | :--- |
| Main Controller | LEGO Mindstorms EV3 Intelligent Brick | Central controller | Executes sensing, navigation, state logic, and motor commands |
| Propulsion | LEGO EV3 Large Motor | A | Drives the rear propulsion system |
| Steering | LEGO EV3 Medium Motor | B | Actuates the front Ackermann steering linkage |
| Challenge Sensor — Open | LEGO EV3 Gyro Sensor | S1 | Measures robot rotation and supports heading/turn control |
| Challenge Sensor — Obstacles | Pixy2.1 | S1 | Detects colored pillars and parking target |
| Left Distance Sensor | LEGO EV3 Ultrasonic Sensor | S2 | Measures left-side track geometry |
| Right Distance Sensor | LEGO EV3 Ultrasonic Sensor | S3 | Measures right-side track geometry |
| Floor Sensor | LEGO EV3 Color Sensor | S4 | Detects course markings and progression |
| Main Power Source | LEGO EV3 Rechargeable DC Battery 45501 | EV3 | Powers the EV3-based vehicle system |

The structure can be simplified into two layers. The first is the **permanent platform**, which includes the EV3, motors, steering, drivetrain, lateral ultrasonic sensors, and color sensor. The second is the **challenge-specific perception layer**, located on S1.

```text
                       PERMANENT PLATFORM
                              │
                     LEGO Mindstorms EV3
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
     Motor A              Motor B              Sensors
       Drive              Steering            S2 / S3 / S4
                                                  │
                                                  ▼
                                    Wall geometry + floor state

                              S1
                              │
                  ┌───────────┴───────────┐
                  │                       │
                  ▼                       ▼
                OPEN                  OBSTACLES
                  │                       │
                  ▼                       ▼
             EV3 Gyro                  Pixy2.1
```

<div align="center">

<img
  src="../../embed/s1_modular_architecture.png"
  alt="Piolín modular S1 architecture"
  width="760"
/>

<br>

<sub><b>Figure 1.2.</b> Piolín's modular S1 architecture. The permanent vehicle remains unchanged while the S1 sensor is selected according to the competition round.</sub>

</div>

This arrangement was selected because the two challenges require fundamentally different information. In Open, the robot benefits from measuring its own rotation and maintaining a repeatable heading through straight sections and corners. In Obstacles, visual identification is much more valuable because the robot must distinguish red, green, and parking targets. Using one configurable port allows Piolín to solve both problems without adding an unnecessary secondary controller or overcomplicating the wiring.

---

## 1.2 LEGO Mindstorms EV3 as the Main Controller

<div align="center">

<img
  src="../../v-photos/v4/ev3_installed.jpg"
  alt="LEGO Mindstorms EV3 Intelligent Brick installed on Piolín"
  width="650"
/>

<br>

<sub><b>Figure 1.3.</b> LEGO Mindstorms EV3 Intelligent Brick installed as the central controller of Piolín.</sub>

</div>

The **LEGO Mindstorms EV3 Intelligent Brick** is the computational center of the robot. It receives sensor measurements, interprets the current navigation state, determines the required steering and propulsion response, and commands the two motors.

Keeping the EV3 as the central controller was a deliberate engineering choice. Earlier development explored architectures involving additional processors and interfaces, including Arduino-based camera integration and other external processing ideas. Those approaches demonstrated that additional hardware could expand the available sensing options, but they also created more communication layers, more wiring, and more potential failure points.

For the current version, Piolín returns to a simpler architecture in which the EV3 directly interacts with almost every active competition component. The only current non-LEGO device is the Pixy2.1 used during the Obstacle Challenge.

This provides several practical advantages. Motor and sensor interfaces remain centralized, there is no need to synchronize multiple main processors, debugging can begin directly from the EV3, and competition preparation requires fewer electronic subsystems.

The EV3 therefore serves three roles simultaneously: **sensor interface, navigation computer, and motion controller**.

<div align="center">

<img
  src="../../embed/ev3_control_architecture.png"
  alt="Piolín EV3 central control architecture"
  width="820"
/>

<br>

<sub><b>Figure 1.4.</b> Centralized control structure. Sensor information enters the EV3, which determines the resulting propulsion and steering commands.</sub>

</div>

---

## 1.3 Motor and Mobility Architecture

Piolín uses only two motors. This was preferred over a more complex multi-motor drive system because the mechanical architecture does not require differential drive.

The **EV3 Large Motor connected to Port A** provides propulsion to the rear drivetrain. The **EV3 Medium Motor connected to Port B** controls the front steering linkage.

<div align="center">

<img
  src="../../v-photos/v4/motor_a_large_drive.jpg"
  alt="EV3 Large Motor used for Piolín propulsion"
  width="620"
/>

<br>

<sub><b>Figure 1.5.</b> EV3 Large Motor connected to Port A and mechanically integrated with the rear propulsion system.</sub>

</div>

The Large Motor was selected for propulsion because propulsion places the greatest continuous mechanical demand on the robot. It must accelerate the entire vehicle, maintain motion through straight sections, reverse when required, and provide sufficient torque while the front wheels are steering.

The Medium Motor is more appropriate for steering because it does not need to propel the complete robot. Its task is to move the Ackermann linkage through a controlled angular range and return the mechanism toward its mechanical center.

<div align="center">

<img
  src="../../v-photos/v4/motor_b_medium_steering.jpg"
  alt="EV3 Medium Motor used for Piolín steering"
  width="620"
/>

<br>

<sub><b>Figure 1.6.</b> EV3 Medium Motor connected to Port B and dedicated exclusively to steering.</sub>

</div>

Separating propulsion and steering simplifies both the mechanical and software architecture:

```text
Motor A
   ↓
Vehicle longitudinal motion

Motor B
   ↓
Vehicle directional control
```

This is fundamentally different from a differential-drive robot, where two propulsion motors create turns by changing left and right wheel speeds. Piolín instead follows a vehicle-like trajectory.

---

## 1.4 Ackermann Steering System

<div align="center">

<img
  src="../../v-photos/v4/ackermann_top.jpg"
  alt="Piolín Ackermann steering mechanism"
  width="720"
/>

<br>

<sub><b>Figure 1.7.</b> Top view of Piolín's front Ackermann-style steering mechanism.</sub>

</div>

The front wheels are connected through an **Ackermann-style steering linkage**. This mechanism allows the two front wheels to follow different turning radii during a curve. The inner wheel must turn more sharply than the outer wheel because it travels along a smaller radius.

Ackermann steering was selected because WRO Future Engineers requires the robot to behave more like an autonomous vehicle than a conventional differential-drive robot. It also matches Piolín's wall-based navigation strategy more naturally. Instead of rotating approximately around its center, the robot follows a continuous curved trajectory, allowing the ultrasonic geometry and gyro heading to correspond more closely to actual vehicle motion.

The steering system also introduces important engineering constraints. The Medium Motor encoder angle is not the same as the physical wheel angle, because the mechanical linkage transforms motor rotation into steering movement. Mechanical center, steering limits, linkage play, and chassis rigidity therefore affect the final response.

For this reason, the steering mechanism is treated as both a mechanical and control-system component rather than simply as a motor attached to wheels.

<div align="center">

<img
  src="../../v-photos/v4/steering_motion.gif"
  alt="Piolín Ackermann steering mechanism moving through its range"
  width="650"
/>

<br>

<sub><b>Figure 1.8.</b> Physical steering movement generated by Motor B. The animation provides direct evidence of the installed linkage but is not by itself proof of mathematically perfect Ackermann geometry.</sub>

</div>

A more detailed analysis of wheel geometry, mechanical center, steering limits, and ideal Ackermann relationships is available in the dedicated [Ackermann Steering documentation](../mobility_mechanical/04_steering.md).

---

## 1.5 Lateral Ultrasonic Navigation

Piolín currently uses **two LEGO EV3 Ultrasonic Sensors**, not three. They are installed laterally and remain connected in both competition configurations.

```text
S2 = LEFT Ultrasonic Sensor

S3 = RIGHT Ultrasonic Sensor
```

<div align="center">

<img
  src="../../v-photos/v4/ultrasonic_pair_top.jpg"
  alt="Piolín two lateral ultrasonic sensors"
  width="720"
/>

<br>

<sub><b>Figure 1.9.</b> Left and right ultrasonic sensors installed laterally on Piolín.</sub>

</div>

The decision to use two lateral sensors is closely related to how Piolín interprets the track. Rather than relying exclusively on an absolute heading or following a painted line, the robot continuously observes the geometry created by the track walls.

Each sensor has a permanent physical identity:

```text
S2 = LEFT

S3 = RIGHT
```

but its navigation role changes according to travel direction.

If the robot travels counterclockwise, the left wall becomes the inner wall. If the robot travels clockwise, the right wall becomes the inner wall.

```text
COUNTERCLOCKWISE

S2 LEFT  → INNER
S3 RIGHT → OUTER


CLOCKWISE

S2 LEFT  → OUTER
S3 RIGHT → INNER
```

<div align="center">

<img
  src="../../embed/ultrasonic_inner_outer_mapping.png"
  alt="Dynamic inner and outer ultrasonic mapping"
  width="800"
/>

<br>

<sub><b>Figure 1.10.</b> Dynamic assignment of the permanent left and right ultrasonic sensors to the logical inner and outer wall roles.</sub>

</div>

Using physical left/right assignments in hardware and converting them into logical inner/outer variables in software is preferable to wiring the robot around a specific course direction. It allows the same hardware to support both clockwise and counterclockwise navigation.

Earlier development also experimented with a frontal ultrasonic sensor. The current architecture no longer requires that sensor because S1 is now reserved for the round-specific Gyro Sensor or Pixy2.1. Removing the front ultrasonic also simplified the port architecture and forced the navigation system to use the lateral sensors more effectively.

This is an example of a broader design principle used throughout Piolín: a component is retained only if the additional information it provides justifies the integration complexity it creates.

---

## 1.6 Floor Detection with the EV3 Color Sensor

<div align="center">

<img
  src="../../v-photos/v4/color_sensor_s4_installed.jpg"
  alt="Piolín EV3 Color Sensor mounted downward"
  width="620"
/>

<br>

<sub><b>Figure 1.11.</b> Downward-facing LEGO EV3 Color Sensor connected to S4.</sub>

</div>

The LEGO EV3 Color Sensor is connected to **S4** and remains installed for both competition rounds. Unlike the ultrasonic sensors, the color sensor does not primarily describe the robot's geometric position. Its main role is to provide information about **course state**.

The first valid floor color determines the direction of travel:

```text
BLUE first
→ Counterclockwise


ORANGE first
→ Clockwise
```

Once direction has been determined, the software can correctly interpret the two ultrasonic sensors as inner or outer wall references.

The same sensor is also used to track progress through the course. Instead of requiring the gyro or wheel encoders to estimate an entire three-lap trajectory independently, physical floor markings provide repeatable external landmarks.

This division of responsibilities is important. The ultrasonic sensors answer:

> Where am I relative to the walls?

The gyro answers during Open:

> How has my orientation changed?

The color sensor answers:

> What course event have I reached?

Separating these questions prevents a single sensor from being forced to solve several unrelated navigation problems.

---

## 1.7 Color Sensor Light Isolation

The accuracy of a color sensor is affected not only by software thresholds but also by the physical optical environment around it. Piolín therefore uses a custom casing around the sensor to reduce uncontrolled external illumination.

<div align="center">

<img
  src="../../v-photos/v4/color_sensor_casing.jpg"
  alt="Piolín color sensor light isolation casing"
  width="620"
/>

<br>

<sub><b>Figure 1.12.</b> Custom casing surrounding the S4 color sensor to reduce variation caused by ambient light.</sub>

</div>

The casing was introduced because lighting changes can alter reflected-light or RGB measurements even when the physical track color has not changed. Improving the physical measurement environment is preferable to continually widening software thresholds to compensate for unstable readings.

This reflects an important systems-engineering principle:

```text
Improve the measurement physically
before compensating entirely in software.
```

The printable model is stored in:

[Color Sensor Casing STL](../../models/3dprint/ColorSensorCasing.stl)

---

## 1.8 Open Challenge Configuration: Gyro-Assisted Navigation

During the Open Challenge, the device connected to S1 is the **LEGO EV3 Gyro Sensor**.

<div align="center">

<img
  src="../../v-photos/v4/s1_open_gyro.jpg"
  alt="EV3 Gyro Sensor installed on Piolín S1 for Open Challenge"
  width="650"
/>

<br>

<sub><b>Figure 1.13.</b> EV3 Gyro Sensor installed in the Open Challenge configuration.</sub>

</div>

The gyro was reintroduced because the lateral ultrasonic sensors and gyro solve different problems and can therefore complement one another.

The ultrasonic sensors provide information about lateral track position. However, a robot can have approximately correct wall distance while still being slightly rotated relative to the straight. That angular error can eventually lead to oscillation or poor corner entry.

The gyro adds a direct rotational reference. It can support straight-line heading stabilization, measure accumulated rotation during corners, and help determine whether a turn has approached the expected orientation.

The resulting Open architecture is therefore based on **sensor fusion rather than sensor replacement**:

```text
Ultrasonic sensors
        ↓
Lateral geometry


Gyro
        ↓
Angular orientation


Color sensor
        ↓
Course state


Combined by EV3
        ↓
Navigation decision
```

<div align="center">

<img
  src="../../embed/open_hardware_architecture.png"
  alt="Piolín Open Challenge sensor architecture"
  width="850"
/>

<br>

<sub><b>Figure 1.14.</b> Open Challenge hardware architecture combining lateral ultrasonic geometry, gyro orientation, and color-based course state.</sub>

</div>

Earlier gyro-based approaches sometimes placed excessive importance on heading alone. The current philosophy is different. The gyro is not expected to tell Piolín where it is laterally within the track. Instead, it complements the walls.

This is why the current Open strategy can be summarized as:

```text
Ultrasonics → WHERE relative to walls

Gyro → WHICH ORIENTATION

Color → WHICH COURSE EVENT
```

That division produces a more structured sensing architecture.

---

## 1.9 Why the Gyro Was Reintroduced

The decision to return to the gyro was the result of iteration rather than simply returning to an older design.

A gyro-free Open architecture had an important advantage: it reduced dependence on heading drift and attempted to infer the complete track structure from wall geometry. This demonstrated that lateral sensing was powerful enough to navigate significant portions of the course.

However, using only wall geometry also meant that orientation had to be inferred indirectly. When the robot exited a corner at a slightly incorrect angle, the lateral controller had to correct both position and orientation using the same measurements. This could contribute to oscillation, delayed stabilization, or inconsistent trajectories depending on the starting position.

The current design keeps the useful part of the gyro-free approach—the two-wall geometry—but adds the gyro back specifically for the information it measures better.

The comparison is therefore:

| Architecture | Strength | Limitation |
| :--- | :--- | :--- |
| Gyro-dominant navigation | Direct angle measurement | Does not directly describe lateral track position |
| Ultrasonic-only navigation | Strong environmental geometry reference | Orientation must be inferred indirectly |
| **Current combined architecture** | **Gyro orientation + ultrasonic lateral geometry** | Requires calibration and coordination between both measurement types |

The final strategy was selected because these sensors provide complementary information instead of redundant measurements.

---

## 1.10 Obstacle Challenge Configuration: Pixy2.1

During the Obstacle Challenge, the Gyro Sensor is removed from S1 and replaced by the **Pixy2.1 vision sensor**.

<div align="center">

<img
  src="../../v-photos/v4/piolin_obstacle_isometric.jpg"
  alt="Piolín in Obstacle Challenge configuration"
  width="720"
/>

<br>

<sub><b>Figure 1.15.</b> Piolín configured for the Obstacle Challenge with Pixy2.1 replacing the Gyro Sensor on S1.</sub>

</div>

The Obstacle Challenge requires a type of information that neither ultrasonic sensors nor the gyro can provide: **visual color identity of traffic pillars**.

A red and green pillar can occupy similar physical positions, but the required passing side is different. Distance information alone cannot determine the correct response.

The current mapping is:

```text
Signature 2
RED
→ pass RIGHT


Signature 3
GREEN
→ pass LEFT
```

A third signature is reserved for the parking target:

```text
Signature 1
PINK
→ parking reference
```

<div align="center">

<img
  src="../../v-photos/v4/pixy21_front.jpg"
  alt="Pixy2.1 mounted on the front of Piolín"
  width="650"
/>

<br>

<sub><b>Figure 1.16.</b> Forward-facing Pixy2.1 used for colored-pillar and parking-target detection.</sub>

</div>

Pixy2.1 can provide more than the signature itself. The software can obtain information about the detected block such as its horizontal position, vertical position, width, and height. This allows vision to become part of the avoidance trajectory rather than acting as a simple red/green switch.

For example, the signature can determine **which side to pass**, while horizontal position can help determine **how much steering correction is appropriate**.

---

## 1.11 Why Pixy2.1 Was Selected

Piolín previously experimented with a **HuskyLens + Arduino Nano + USB-to-EV3 architecture**. That approach had the advantage of providing a dedicated vision processor and allowed the team to experiment with learned visual IDs.

However, it also introduced an additional communication chain:

```text
HuskyLens
    ↓
Arduino Nano
    ↓
USB
    ↓
EV3
```

This meant that a detection problem could originate from several different places: visual recognition, HuskyLens configuration, Nano interpretation, serial communication, EV3 reception, or navigation logic.

The current Pixy2.1 architecture removes the intermediate controller and connects the vision sensor directly through the EV3 S1 interface during the Obstacle Challenge.

```text
Pixy2.1
   ↓
S1
   ↓
EV3
```

<div align="center">

<img
  src="../../embed/vision_architecture_comparison.png"
  alt="Comparison between legacy HuskyLens Nano architecture and current Pixy2.1 architecture"
  width="850"
/>

<br>

<sub><b>Figure 1.17.</b> Comparison between the previous multi-stage HuskyLens/Nano vision architecture and the current direct Pixy2.1-to-EV3 configuration.</sub>

</div>

The change was not made because the HuskyLens was inherently unusable. It was made because the Pixy architecture better matched Piolín's current priorities: direct color signatures, block-position data, fewer intermediate devices, and simpler integration with the existing EV3-based robot.

This also reduces the number of non-LEGO components in the competition vehicle. In the current Obstacle configuration, **Pixy2.1 is the only major active non-LEGO sensing component**.

---

## 1.12 Pixy2.1 and the Two Ultrasonic Sensors

The Pixy does not replace the ultrasonic sensors.

Instead, the sensors describe different properties of the same situation.

```text
Pixy2.1
    ↓
Which pillar?
Where is the visual block?


Ultrasonic Sensors
    ↓
Where are the surrounding walls?
How much lateral space is available?
```

This distinction is important during obstacle avoidance.

A red pillar may require a right-side pass, but that does not mean the robot should command an unrestricted right turn. The wall geometry still defines the safe movement envelope.

The intended architecture therefore combines:

```text
Pillar identity
+
Pillar image position
+
Left wall
+
Right wall
+
Vehicle steering state
```

before the EV3 determines the final Motor B command.

<div align="center">

<img
  src="../../embed/obstacle_pixy_us_fusion.png"
  alt="Pixy2.1 and ultrasonic sensor fusion during obstacle navigation"
  width="850"
/>

<br>

<sub><b>Figure 1.18.</b> Decision-level fusion between Pixy2.1 obstacle information and lateral ultrasonic wall geometry.</sub>

</div>

This is one reason the Obstacle Challenge does not require the gyro in the current design. S1 is more valuable as a vision input because pillar identity is essential, while the two ultrasonic sensors continue to provide environmental geometry.

---

## 1.13 Permanent vs. Round-Specific Hardware

The two competition configurations share almost the entire robot.

<div align="center">

<img
  src="../../embed/open_obstacle_hardware_comparison.png"
  alt="Comparison of Piolín Open and Obstacle hardware configurations"
  width="900"
/>

<br>

<sub><b>Figure 1.19.</b> Hardware comparison showing that only the S1 perception device changes between the Open and Obstacle Challenges.</sub>

</div>

The permanent components are:

```text
LEGO EV3 Intelligent Brick

LEGO EV3 Rechargeable Battery 45501

EV3 Large Motor on A

EV3 Medium Motor on B

Left Ultrasonic on S2

Right Ultrasonic on S3

Color Sensor on S4

Rear drivetrain

Ackermann steering

LEGO Technic chassis
```

The challenge-specific device is:

```text
OPEN
S1 = EV3 Gyro Sensor


OBSTACLE
S1 = Pixy2.1
```

This architecture avoids building two different robots for the two challenges. Mechanical behavior, drivetrain geometry, steering, most sensors, and the controller remain unchanged.

The modularity is therefore achieved with minimal physical reconfiguration.

---

## 1.14 Power Architecture

Piolín's main power source is the **LEGO Mindstorms EV3 Rechargeable DC Battery, part 45501**.

<div align="center">

<img
  src="../../v-photos/v4/ev3_battery_45501.jpg"
  alt="LEGO Mindstorms EV3 Rechargeable DC Battery 45501 used by Piolín"
  width="600"
/>

<br>

<sub><b>Figure 1.20.</b> EV3 Rechargeable DC Battery 45501 used as the main vehicle power source.</sub>

</div>

The use of the standard EV3 power system was preferred over adding a separate vehicle battery because the drivetrain motors, steering motor, controller, gyro, ultrasonic sensors, and color sensor are already designed to operate within the same ecosystem.

This keeps the electrical architecture compact and reduces additional regulators, converters, power rails, and wiring.

During the Obstacle Challenge, the Pixy2.1 is integrated through the S1 vision connection. The detailed power and communication arrangement is documented separately in the power-distribution and electrical-schematic sections.

---

## 1.15 Complete Open Challenge Hardware Map

The complete Open configuration is:

```text
                    LEGO EV3 BATTERY 45501
                             │
                             ▼
                       LEGO EV3 BRICK
                             │
      ┌───────────┬──────────┼──────────┬───────────┐
      │           │          │          │           │
      ▼           ▼          ▼          ▼           ▼
      A           B          S1         S2          S3
      │           │          │          │           │
      ▼           ▼          ▼          ▼           ▼
 Large Motor  Medium Motor  Gyro     Left US     Right US
      │           │
      ▼           ▼
 Rear Drive   Ackermann
              Steering

                             S4
                              │
                              ▼
                         Color Sensor
```

<div align="center">

<img
  src="../../embed/ev3_portmap_open.png"
  alt="Piolín Open Challenge port map"
  width="850"
/>

<br>

<sub><b>Figure 1.21.</b> Current EV3 port map for the Open Challenge.</sub>

</div>

---

## 1.16 Complete Obstacle Challenge Hardware Map

The Obstacle configuration keeps all permanent systems but replaces the S1 sensor.

```text
                    LEGO EV3 BATTERY 45501
                             │
                             ▼
                       LEGO EV3 BRICK
                             │
      ┌───────────┬──────────┼──────────┬───────────┐
      │           │          │          │           │
      ▼           ▼          ▼          ▼           ▼
      A           B          S1         S2          S3
      │           │          │          │           │
      ▼           ▼          ▼          ▼           ▼
 Large Motor  Medium Motor Pixy2.1   Left US     Right US
      │           │
      ▼           ▼
 Rear Drive   Ackermann
              Steering

                             S4
                              │
                              ▼
                         Color Sensor
```

<div align="center">

<img
  src="../../embed/ev3_portmap_obstacle.png"
  alt="Piolín Obstacle Challenge port map"
  width="850"
/>

<br>

<sub><b>Figure 1.22.</b> Current EV3 port map for the Obstacle Challenge.</sub>

</div>

The comparison makes the modular design especially clear:

```text
OPEN                 OBSTACLE

A  Drive             A  Drive
B  Steering          B  Steering

S1 Gyro              S1 Pixy2.1
S2 Left US           S2 Left US
S3 Right US          S3 Right US
S4 Color             S4 Color
```

---

## 1.17 Hardware Evolution and Engineering Decisions

Piolín's current configuration is the result of multiple hardware iterations rather than a single initial design.

Earlier development explored different combinations of ultrasonic sensors, gyro navigation, Pixy vision, HuskyLens, Arduino Nano communication, and different navigation strategies. These experiments were useful because each one isolated a specific engineering problem.

A gyro-heavy approach demonstrated the value of direct angular measurement but also showed that heading alone does not describe lateral track position. A gyro-free approach demonstrated that two side ultrasonic sensors could provide strong environmental geometry, but orientation recovery after some curves remained difficult. The current Open architecture therefore combines both measurement types.

Similarly, the HuskyLens/Nano vision stage proved that external vision could be integrated into an EV3 vehicle, but the multi-device communication chain increased complexity. The return to Pixy2.1 reduced that chain and provided direct color-signature and block-position information that better matched the obstacle-navigation problem.

<div align="center">

<img
  src="../../embed/evolution_sensor_architecture.png"
  alt="Piolín sensing architecture evolution"
  width="900"
/>

<br>

<sub><b>Figure 1.23.</b> Evolution of Piolín's sensing architecture from earlier experimental systems toward the current round-specific configuration.</sub>

</div>

The important engineering lesson is that components were not kept simply because they had once been installed. Hardware was repeatedly evaluated according to whether the information it provided justified its mechanical, electrical, and software complexity.

This led to the current principle:

> **Use each sensor for the physical quantity it measures best, and avoid adding hardware whose function can already be provided reliably by the existing system.**

---

## 1.18 Current Architecture Compared with Previous Designs

| Architecture | Main Advantage | Main Limitation | Final Role |
| :--- | :--- | :--- | :--- |
| EV3 + gyro navigation | Direct heading information | Heading alone does not determine lateral track position | Gyro retained as an Open support sensor |
| Two lateral ultrasonics without gyro | Strong track-relative geometry | Orientation had to be inferred indirectly | Lateral geometry retained |
| Three-ultrasonic architecture | Added frontal sensing | Consumed S1 and competed with more useful round-specific sensing | Front US removed |
| HuskyLens + Arduino Nano | Dedicated vision recognition | Additional processing and communication layer | Moved to legacy |
| Pixy2.1 | Direct color signatures and block position | Requires careful visual calibration and target selection | Current Obstacle sensor |
| **Current modular S1 architecture** | **Allows optimized sensing for each round while retaining one common robot** | **Requires changing S1 configuration between rounds** | **Current design** |

This comparison shows that the current hardware is not simply the configuration with the greatest number of components. It is the configuration that provides the strongest information with the smallest unnecessary integration burden.

---

## 1.19 Why the Final Architecture Was Selected

The final hardware architecture was selected because it creates a clear division of responsibility.

During Open:

```text
S2 + S3
→ track geometry

S1 Gyro
→ angular orientation

S4 Color
→ course progression

Motor A
→ propulsion

Motor B
→ steering
```

During Obstacles:

```text
S2 + S3
→ track geometry

S1 Pixy2.1
→ obstacle identity and image position

S4 Color
→ course progression

Motor A
→ propulsion

Motor B
→ steering
```

No sensor is expected to solve the entire navigation problem by itself.

This makes the architecture easier to reason about because each measurement can be traced through:

```text
Physical phenomenon
        ↓
Sensor
        ↓
Software interpretation
        ↓
Navigation decision
        ↓
Motor response
```

That traceability is important not only for competition reliability but also for debugging and reproducibility.

---

## 1.20 Current Hardware Scope

The current competition architecture contains:

```text
1 × LEGO Mindstorms EV3 Intelligent Brick

1 × LEGO EV3 Rechargeable DC Battery 45501

1 × LEGO EV3 Large Motor

1 × LEGO EV3 Medium Motor

2 × LEGO EV3 Ultrasonic Sensors

1 × LEGO EV3 Color Sensor

1 × LEGO EV3 Gyro Sensor
    used in Open

1 × Pixy2.1
    used in Obstacles

LEGO Technic chassis

Rear drivetrain

Front Ackermann steering
```

The current competition architecture does **not** include:

```text
Arduino Nano

HuskyLens

Front ultrasonic sensor

Raspberry Pi

Arduino Mega

Gyro during Obstacles

Pixy during Open
```

Those systems may remain in the repository as part of Piolín's engineering history, but they should not appear in current reconstruction instructions.

---

## 1.21 Current Hardware Evidence

<div align="center">

<img
  src="../../v-photos/v4/piolin_open_top.jpg"
  alt="Top view of Piolín Open configuration"
  width="720"
/>

<br>

<sub><b>Figure 1.24.</b> Top view of the Open configuration showing the permanent vehicle platform and Gyro Sensor configuration.</sub>

</div>

<div align="center">

<img
  src="../../v-photos/v4/piolin_obstacle_top.jpg"
  alt="Top view of Piolín Obstacle configuration"
  width="720"
/>

<br>

<sub><b>Figure 1.25.</b> Top view of the Obstacle configuration showing Pixy2.1 replacing the gyro while the remainder of the platform remains unchanged.</sub>

</div>

These two configurations should be used as the physical reference for all current documentation.

Mechanical measurements, calibration constants, sensor positions, wiring diagrams, and software assumptions should correspond to one of these two current states rather than to an older development version.

---

## 1.22 Hardware Documentation Structure

The remaining component documentation describes each part of this architecture in greater depth.

[EV3 Controller](02_EV3.md) explains why the EV3 remains the main controller and documents its responsibilities and port use.

[Motors](03_Motors.md) documents the Large Motor propulsion system and Medium Motor steering system.

[Steering Motor](04_SteeringMotor.md) focuses specifically on Motor B, mechanical center, steering actuation, and its relationship with Ackermann geometry.

[Ultrasonic Sensors](05_UltrasonicSensors.md) explains S2/S3 placement, wall geometry, inner/outer assignment, and why the final architecture uses two lateral sensors.

[Color Sensor](06_ColorSensor.md) documents S4, floor detection, direction selection, course progression, and light isolation.

[Pixy2.1 Vision Sensor](07_Pixy21.md) documents the current Obstacle Challenge camera, its signatures, block information, direct EV3 integration, and the reasons it replaced the HuskyLens/Nano architecture.

[Battery](08_Battery.md) documents the LEGO EV3 Rechargeable DC Battery 45501 and the robot's primary power source.

[Power Distribution](09_PowerDistribution.md) explains how energy and signals are distributed through the two round-specific configurations.

[Other Components](10_OtherComponents.md) documents structural LEGO Technic components, mounts, custom parts, cables, and other supporting hardware.

---

## 1.23 Final Hardware Design Principle

Piolín's current hardware design can be summarized by one principle:

> **The robot should use the simplest architecture that still provides the information required to make reliable autonomous decisions.**

This is why Piolín does not permanently carry every sensor tested during development. The current design preserves the components that provide distinct, useful information and removes those whose additional complexity is not justified by the current strategy.

The result is one common mechanical vehicle with two optimized sensing configurations:

```text
                         PIOLÍN
                            │
                   COMMON EV3 PLATFORM
                            │
          ┌─────────────────┴─────────────────┐
          │                                   │
          ▼                                   ▼
        OPEN                              OBSTACLES
          │                                   │
          ▼                                   ▼
        GYRO                                PIXY2.1
          │                                   │
          ▼                                   ▼
 Orientation reference               Visual obstacle identity
          │                                   │
          └─────────────────┬─────────────────┘
                            ▼
                     SAME EV3 VEHICLE
```

This architecture is the current hardware baseline for PiolínTech's WRO Future Engineers 2026 documentation.

---


<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
