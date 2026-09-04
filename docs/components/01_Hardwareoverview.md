
<div align="center">
  <img src="https://github.com/user-attachments/assets/839b917a-c2bc-4053-8b2a-f68e43b7efa0"
       alt="Piolín hardware evolution"
       style="max-width: 65%; height: auto;" />
</div>

# 1. Hardware Overview

Piolín’s final WRO Future Engineers 2026 hardware architecture was designed around one main objective: building a robot that could navigate the track reliably, repeatedly, and with as little unnecessary complexity as possible. Although many earlier prototypes explored different processors, sensors, camera systems, and navigation approaches, the final version of Piolín uses a much more focused architecture. Every active hardware component in the current robot has a clearly defined responsibility inside the complete system.

The robot is centered around the **LEGO Mindstorms EV3 Intelligent Brick**, which acts as the main controller. The EV3 is responsible for propulsion, steering, ultrasonic navigation, color-based track detection, state transitions, and the overall execution of the autonomous program. Instead of replacing the EV3 completely, the final design keeps it as the core of the robot and adds an external vision subsystem only where it is genuinely useful. This decision allowed the team to preserve the reliability and simplicity of the EV3 ecosystem while still integrating obstacle-detection capabilities through the HuskyLens and Arduino Nano.

Piolín’s final architecture also reflects an important engineering decision: the Open Challenge and the Obstacle Challenge do not need exactly the same sensing logic. For that reason, the robot was designed so that its basic wall navigation and lap-tracking systems can function independently from the vision system. In practice, this means that Piolín can follow the track in the Open Challenge using only its ultrasonic sensors, color sensor, steering system, and EV3 control logic, while the HuskyLens and Arduino Nano become especially relevant during the Obstacle Challenge.

> [!IMPORTANT]
> The hardware described in this section corresponds to the **final active competition configuration of Piolín**. Older hardware architectures such as PixyCam-based vision, gyro-based navigation, Raspberry Pi experiments, and other rejected subsystems are part of the development history, but they are **not part of the final robot**.

---

## 1.1 Final Hardware Architecture

The final robot combines a LEGO-based mobility and sensing platform with a lightweight external vision interface. The EV3 remains the center of the system, while the Arduino Nano acts as a communication bridge between the HuskyLens and the EV3. This creates a modular architecture in which each component solves a specific part of the robot’s behavior rather than forcing a single controller to do everything.

| System | Final Component | Connection | Primary Function |
| :--- | :--- | :--- | :--- |
| **Main Controller** | LEGO Mindstorms EV3 Intelligent Brick | Central unit | Executes the robot’s navigation, sensing, and motion-control logic |
| **Drive System** | EV3 Drive Motor | Port A | Provides propulsion |
| **Steering System** | EV3 Steering Motor | Port B | Controls the front Ackermann steering mechanism |
| **Front Distance Sensor** | LEGO Ultrasonic Sensor | Port S1 | Detects dangerously close frontal obstacles or walls for emergency stopping |
| **Right Distance Sensor** | LEGO Ultrasonic Sensor | Port S2 | Measures the distance to the right-side wall |
| **Left Distance Sensor** | LEGO Ultrasonic Sensor | Port S3 | Measures the distance to the left-side wall |
| **Floor Detection Sensor** | LEGO Color Sensor | Port S4 | Detects blue and orange floor markings for direction and lap/corner tracking |
| **Vision Sensor** | HuskyLens | Connected to Arduino Nano | Detects colored pillars during the Obstacle Challenge |
| **Vision Interface** | Arduino Nano | USB to EV3 | Transfers HuskyLens detection information to the EV3 |

This final architecture was selected because it divides the robot into three major functional layers. The first is **motion control**, which includes propulsion and steering. The second is **track perception**, which includes ultrasonic sensing and color detection. The third is **obstacle perception**, which is handled by the HuskyLens and passed to the EV3 through the Arduino Nano. Because each layer has a defined role, the system is easier to debug, easier to explain, and easier to reproduce than some of the earlier experimental designs.

---

## 1.2 Main Controller: LEGO Mindstorms EV3

<div align="center">
  <img src="https://github.com/user-attachments/assets/ab7c39a9-6f0e-4c9d-aee2-8d59c25d3adc"
       alt="LEGO EV3 Intelligent Brick"
       style="max-width: 30%; height: auto; border-radius: 8px; margin: 10px 0;" />
</div>

The **LEGO EV3 Intelligent Brick** is the main computational core of Piolín. It was kept as the central controller because it provides direct and reliable integration with the LEGO motors and sensors that form the basis of the robot’s mobility and wall-navigation logic. In the final design, the EV3 is not just a hub that receives data; it is the device that actually decides how Piolín moves.

The EV3 reads all three ultrasonic sensors, reads the color sensor, controls the propulsion motor on Port A, controls the steering motor on Port B, and runs the main state-based navigation logic. It also receives obstacle information from the Arduino Nano whenever the HuskyLens detects a relevant visual target during the Obstacle Challenge. In other words, even though Piolín includes an external vision subsystem, the EV3 remains fully responsible for the robot’s overall autonomous behavior.

A major advantage of this decision is that the EV3 can directly manage the robot’s most time-critical functions without depending on a more complex external computing stack. The drive motor, steering motor, ultrasonic sensors, and color sensor are all connected directly to the same controller, which reduces integration complexity and minimizes the number of potential failure points during competition.

---

## 1.3 Distance and Track Sensing System

<div align="center">
  <img src="https://github.com/user-attachments/assets/b8872f62-adb5-4fd1-98fb-18491c57de56"
       alt="Ultrasonic sensor"
       style="max-width: 30%; height: auto; border-radius: 8px; margin: 10px 0;" />
</div>

Piolín uses **three LEGO ultrasonic sensors** in the final competition architecture. Two of them are mounted laterally and are used as the main source of track-geometry information, while the third is mounted at the front and acts as an additional safety layer. This is an important distinction because the three sensors do not all play the same role in the software.

The **left ultrasonic sensor**, connected to **Port S3**, measures the distance to the left side of the track. The **right ultrasonic sensor**, connected to **Port S2**, measures the distance to the right side. These two lateral sensors are the foundation of Piolín’s Open Challenge navigation strategy. They allow the software to determine which wall is the inner wall, which wall is the outer wall, and how the robot should behave when it approaches a corner. During straight sections, the inner wall normally acts as the primary reference. When the inner wall disappears at a corner, the software interprets that change as a change in track geometry and temporarily transfers more importance to the outer wall until the next straight section begins.

The **front ultrasonic sensor**, connected to **Port S1**, has a different role. It is not part of the normal inner-wall and outer-wall geometric calculations. Instead, it is used to detect whether Piolín is approaching something dangerously close in front of the robot. If that happens, the front sensor gives the system an emergency safety layer capable of stopping the robot before a frontal collision occurs. This improves robustness without complicating the lateral wall-following mathematics.

The final ultrasonic arrangement can be represented as follows:

```text
                        FRONT
                          ↑
                    [ FRONT US ]
                          │
                          │

          LEFT US ←  [ PIOLÍN ]  → RIGHT US

                          │
                          ↓
                         REAR
````

This architecture gives Piolín both **lateral geometric awareness** and **frontal safety awareness**. The two side sensors support navigation, while the front sensor provides an independent safety function.

---

## 1.4 Color Sensor and Floor Marking Detection

<div align="center">
  <img src="https://github.com/user-attachments/assets/5e59f3a1-5b7c-4992-9d57-07951f412e67"
       alt="LEGO Color Sensor"
       style="max-width: 30%; height: auto; border-radius: 8px; margin: 10px 0;" />
</div>

Piolín uses one **LEGO Color Sensor** connected to **Port S4**. The sensor is mounted facing downward so that it can read the floor markings placed on the mat. In the final system, the color sensor does not directly steer the robot. Instead, it provides information that helps the EV3 interpret where the robot is within the course.

Its first responsibility is to determine the initial direction of travel. The first valid floor marking establishes whether Piolín should navigate clockwise or counterclockwise. If the first detected marking is **blue**, the robot interprets that as one direction; if it is **orange**, it interprets it as the other. Once that direction has been determined, the software can assign the ultrasonic sensors correctly as inner-wall or outer-wall references.

Its second responsibility is to track progress around the course. Because the competition format requires multiple laps and because the floor markings appear at the corners, the color sensor acts as a compact progress-tracking tool. Rather than using it as a steering sensor, Piolín uses it as a **course-state sensor**. This division of responsibility keeps the control logic cleaner: ultrasonic sensors handle wall geometry, while the color sensor helps the EV3 understand direction and progress.

The final design also recognizes that color detection can be affected by lighting conditions and repeated readings over the same physical strip. For that reason, the software uses confirmation and locking logic so that one strip is not counted multiple times while the sensor remains above it.

---

## 1.5 Vision System: HuskyLens and Arduino Nano

<div align="center">
  <img src="https://github.com/user-attachments/assets/737bd86d-a82a-46fa-b683-06f18ec4721b"
       alt="HuskyLens vision sensor"
       style="max-width: 30%; height: auto; border-radius: 8px; margin: 10px 0;" />
</div>

The **HuskyLens** is Piolín’s final vision sensor and is used primarily during the **Obstacle Challenge**. Unlike the ultrasonic sensors, which provide distance information relative to walls, the HuskyLens provides visual recognition of the colored traffic pillars used in the obstacle round. This is important because pillar color determines which side of the obstacle the robot must pass.

The HuskyLens is not connected directly to the EV3 sensor ports. Instead, it communicates first with an **Arduino Nano**, which acts as an interface between the vision system and the EV3. The Nano receives the relevant visual detections and passes simplified information to the EV3 through a USB connection. This makes the vision subsystem more manageable and prevents the EV3 from having to process raw camera data directly.

The final architecture deliberately separates **track navigation** from **object recognition**. The EV3 and its directly connected sensors are sufficient to handle wall-following, corner interpretation, steering, propulsion, and course progress. The HuskyLens and Nano are added specifically to solve the visual-recognition problem of the Obstacle Challenge. This modular separation makes the complete robot easier to explain and easier to maintain.

The communication structure is:

```text
HuskyLens
    │
    ▼
Arduino Nano
    │
    │ USB
    ▼
LEGO EV3
```

This setup allows Piolín to benefit from dedicated visual detection without replacing the EV3 as the main robot controller.

---

## 1.6 Mobility Hardware Overview

Piolín uses two EV3-controlled actuation functions: one for propulsion and one for steering. The **drive motor**, connected to **Port A**, provides forward motion. The **steering motor**, connected to **Port B**, controls the front Ackermann steering mechanism. This separation is a defining part of Piolín’s mechanical identity because the robot does not turn like a differential-drive robot. Instead, it behaves more like a small car.

The steering motor physically changes the angle of the front wheels, while the rear drive system remains dedicated to propulsion. This results in more predictable vehicle-like turning behavior and aligns better with the geometry-based ultrasonic navigation strategy used in the Open Challenge. The decision to use Ackermann-style steering is not only a mechanical decision but also a sensing decision, because more predictable physical turning makes the wall-distance data easier to interpret.

The final wheel configuration uses larger rear wheels for propulsion and smaller front wheels for steering.

| Wheel Position   |       Diameter      |
| :--------------- | :-----------------: |
| **Rear Wheels**  | **2.4 in / ~61 mm** |
| **Front Wheels** | **1.5 in / ~38 mm** |

The detailed reasoning behind Ackermann geometry, steering-center calibration, wheel kinematics, and drivetrain analysis is documented in the mobility and mechanical sections. In this overview, the important point is that Piolín’s actuation system is split clearly into **go forward** and **change direction**, which simplifies both mechanical design and software control.

---

## 1.7 Challenge-Specific Hardware Roles

One reason the final architecture works well is that not every component is equally important in every phase of the competition. The Open Challenge and the Obstacle Challenge share the same base robot, but different hardware subsystems take the lead depending on the task.

During the **Open Challenge**, Piolín relies mainly on the EV3, the two lateral ultrasonic sensors, the front ultrasonic sensor, the color sensor, the drive motor, and the steering motor. In this mode, the robot does not require visual object recognition to navigate the track. It follows the walls, interprets corner transitions, determines direction from floor markings, and tracks progress through the course using its onboard sensors.

During the **Obstacle Challenge**, that same navigation base remains active, but the HuskyLens and Arduino Nano become essential because the robot must now recognize colored pillars and choose the correct passing behavior. The hardware architecture therefore supports both challenges without requiring a different robot or a complete rewiring of the system.

This separation is one of the main strengths of the final Piolín design. The robot does not depend on the camera for everything, and it does not depend on wall sensors for everything either. Instead, each sensing system is used where it is most effective.

---

## 1.8 Final Hardware Connection Map

The complete active hardware architecture can be summarized as follows:

```text
                         ┌─────────────────┐
                         │   HUSKYLENS     │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │  ARDUINO NANO   │
                         └────────┬────────┘
                                  │ USB
                                  ▼
┌─────────────────────────────────────────────────────┐
│                    LEGO EV3                         │
│                                                     │
│   Port A  ───────────── Drive Motor                 │
│   Port B  ───────────── Steering Motor              │
│                                                     │
│   Port S1 ───────────── Front Ultrasonic Sensor     │
│   Port S2 ───────────── Right Ultrasonic Sensor     │
│   Port S3 ───────────── Left Ultrasonic Sensor      │
│   Port S4 ───────────── Color Sensor                │
│                                                     │
└─────────────────────────────────────────────────────┘
```

This diagram represents the **final active Piolín 2026 competition hardware configuration**. It should be interpreted as the official system map for the current robot, not as a historical diagram of older prototypes.

---

## 1.9 Hardware Evolution Summary

Piolín’s final hardware configuration was not the first version of the robot. It emerged through several hardware iterations, each of which revealed something about what worked and what did not. These earlier versions are important because they explain why the final architecture looks the way it does.

At different stages, the team explored PixyCam-based vision, gyroscope-assisted navigation, additional experimental sensing layouts, and non-final processing architectures. Some of these approaches were useful as experiments, but they increased complexity, created integration difficulties, or did not improve real competition reliability enough to justify their continued use.

The final hardware architecture was selected because it achieved a better balance between sensing capability, simplicity, compatibility, and repeatability. Instead of trying to maximize the number of components, the final design focuses on using a smaller set of hardware more effectively.

| Development Stage                    | Main Architecture                                                        | Engineering Lesson                                                                                   |
| :----------------------------------- | :----------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------- |
| **Early EV3 Prototype**              | EV3 with basic LEGO mobility                                             | Established the platform but revealed steering and structural issues                                 |
| **PixyCam Vision Experiment**        | EV3 with PixyCam                                                         | Showed the usefulness of camera-based perception but was not kept as the final system                |
| **Gyro-Based Navigation Experiment** | EV3 with gyroscope and wall sensors                                      | Demonstrated heading-based turning ideas, but gyro dependence was not kept in the final architecture |
| **Sensor-Geometry Development**      | EV3 with lateral ultrasonic sensing                                      | Showed that wall-based geometric navigation could be effective and reproducible                      |
| **Vision Integration Stage**         | HuskyLens with Arduino Nano and EV3                                      | Provided a practical way to integrate obstacle recognition without replacing the EV3                 |
| **Final 2026 Architecture**          | **EV3 + 3 Ultrasonic Sensors + Color Sensor + HuskyLens + Arduino Nano** | Selected for reliability, clarity of roles, and competition suitability                              |

The important point is not simply that the robot changed, but that each change contributed to a more disciplined final design.

---

## 1.10 Key Hardware Design Decision

The most important hardware decision in Piolín’s development was **not** choosing the most powerful possible processor. Instead, it was choosing an architecture in which each active component had a specific and justified role.

The EV3 was kept as the main controller because it provides direct access to the motors and primary sensors that define the robot’s movement. The HuskyLens was added because it solves a visual-recognition problem that ultrasonic sensors cannot solve. The Arduino Nano was added not as a replacement for the EV3, but as a lightweight communication interface between the vision sensor and the main robot controller.

The same design philosophy appears in the sensor architecture. The lateral ultrasonic sensors are used for navigation geometry. The front ultrasonic sensor is used for frontal safety. The color sensor is used for direction and track progress. The vision subsystem is used for obstacle recognition. Because the final architecture avoids unnecessary overlap between components, the robot is easier to test and more understandable from an engineering perspective.

This is what gives Piolín’s hardware architecture its strength. It is not merely a collection of parts; it is a system in which every active component has a defined purpose inside the complete autonomous robot.

> [!NOTE]
> Detailed explanations of each individual subsystem are provided in the following component and subsystem sections. This overview is intended to present the complete hardware architecture and explain how the major elements of the robot fit together as one final competition system.

