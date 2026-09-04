# 9. Power Distribution Architecture

Piolín uses a **centralized EV3-based power architecture** for the hardware that controls the vehicle directly. The LEGO Mindstorms EV3 battery supplies the Intelligent Brick, and the EV3 then provides the electrical interface for the two motors and the four sensors connected to its native ports.

This arrangement keeps the fundamental navigation system concentrated around one controller. Propulsion, steering, ultrasonic sensing, and floor-color detection therefore belong to the same electrical platform as the software that interprets those devices.

The final vehicle-control power path can be summarized as:

<img width="989" height="736" alt="image" src="https://github.com/user-attachments/assets/6b5467aa-abf6-440e-b530-ba0f2027e3e5" />

The external vision subsystem is connected to the EV3 through the Arduino Nano. Its communication architecture is documented separately from the EV3's native motor and sensor distribution so that electrical power routing is not confused with data communication.

> [!IMPORTANT]
> Piolín's primary propulsion, steering, wall sensing, frontal safety, and floor sensing systems are all integrated directly with the **LEGO EV3 electrical platform**.

---

## 9.1 Final Power Distribution Overview

The final Piolín hardware can be divided into two main electrical domains.

The first is the **EV3 vehicle-control domain**, containing the EV3 itself, both motors, the three ultrasonic sensors, and the color sensor.

The second is the **vision subsystem**, containing the HuskyLens and Arduino Nano interface.

```text
                    PIOLÍN POWER ARCHITECTURE

                         MAIN VEHICLE
                             │
                        EV3 BATTERY
                             │
                             ▼
                          LEGO EV3
                             │
             ┌───────────────┼───────────────┐
             │               │               │
             ▼               ▼               ▼
           MOTORS          SENSORS        PROCESSING
           A + B           S1–S4             EV3


                       VISION SUBSYSTEM
                             │
                        HUSKYLENS
                             │
                        ARDUINO NANO
                             │
                            USB
                             │
                             ▼
                          LEGO EV3
                       Data Interface
```

The USB connection shown above represents the confirmed communication path between the Nano and the EV3. Detailed wiring inside the vision subsystem is documented separately so that communication and power paths are not incorrectly treated as the same thing.

---

# 9.2 EV3 as the Main Electrical Hub

The LEGO EV3 performs two functions simultaneously inside Piolín.

It is the main computational controller, but it is also the electrical interface for the LEGO motors and sensors.

```text
                       EV3 BATTERY
                            │
                            ▼
                     ┌──────────────┐
                     │   LEGO EV3   │
                     │              │
                     │ Controller   │
                     │      +       │
                     │ Electrical   │
                     │ Interface    │
                     └──────┬───────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
           Motors         Sensors       Software
```

This reduces the number of external interfaces required for the robot's fundamental movement.

Piolín does not require a separate external motor driver between the EV3 and the final LEGO propulsion or steering motors.

Similarly, the LEGO ultrasonic and color sensors connect directly to the EV3 sensor ports.

---

# 9.3 Motor Power Distribution

The final actuation architecture uses two EV3 motor outputs.

```text
                         LEGO EV3
                            │
                 ┌──────────┴──────────┐
                 ▼                     ▼
              PORT A                 PORT B
                 │                     │
                 ▼                     ▼
           DRIVE MOTOR           STEERING MOTOR
                 │                     │
                 ▼                     ▼
           Propulsion            Ackermann Steering
```

**Motor A** receives power and control through the EV3 and provides propulsion through the rear drivetrain.

**Motor B** receives power and control through the same EV3 platform and operates the front steering linkage.

Because the motors can operate simultaneously, the power system must support propulsion and steering as concurrent loads rather than as isolated components.

A typical navigation situation can involve:

```text
Drive Motor active
        +
Steering Motor active
        +
Sensors active
        +
EV3 processing active
```

This is the normal operating condition of the complete robot.

---

# 9.4 Sensor Power Distribution

Piolín's four LEGO navigation sensors are connected directly to the EV3.

```text
                         LEGO EV3
                            │
           ┌────────────────┼────────────────┐
           │                │                │
           ▼                ▼                ▼
          S1               S2               S3
           │                │                │
           ▼                ▼                ▼
      Front US         Right US          Left US

                            │
                            ▼
                           S4
                            │
                            ▼
                     Color Sensor
```

The sensor ports provide both the electrical interface and the communication connection required by the LEGO sensors.

This means the three ultrasonic sensors and the color sensor do not require separate external batteries or external signal-conditioning electronics in the final architecture.

---

# 9.5 Complete EV3 Port and Power Map

The final EV3 interface is:

| EV3 Interface | Connected Hardware | Main Function |
| :--- | :--- | :--- |
| **Motor Port A** | Drive Motor | Rear propulsion |
| **Motor Port B** | Steering Motor | Ackermann steering |
| **Sensor Port S1** | Front Ultrasonic Sensor | Frontal emergency safety |
| **Sensor Port S2** | Right Ultrasonic Sensor | Right-wall geometry |
| **Sensor Port S3** | Left Ultrasonic Sensor | Left-wall geometry |
| **Sensor Port S4** | LEGO Color Sensor | Floor marking detection |
| **USB** | Arduino Nano | Vision-data communication |

The same architecture can be represented visually as:

```text
                    LEGO MINDSTORMS EV3
        ┌─────────────────────────────────────┐
        │                                     │
        │   MOTOR OUTPUTS                     │
        │                                     │
        │   A  ───────→ Drive Motor           │
        │   B  ───────→ Steering Motor        │
        │                                     │
        │   SENSOR INPUTS                     │
        │                                     │
        │   S1 ───────→ Front Ultrasonic      │
        │   S2 ───────→ Right Ultrasonic      │
        │   S3 ───────→ Left Ultrasonic       │
        │   S4 ───────→ Color Sensor          │
        │                                     │
        │   USB ←─────→ Arduino Nano          │
        │                                     │
        └─────────────────────────────────────┘
```

This map represents both the physical port assignment and the logical division of responsibilities in Piolín.

---

# 9.6 Why the EV3 Motors Do Not Need an External Motor Driver

Some mobile-robot architectures use a microcontroller connected to an external H-bridge or motor driver.

Piolín's final LEGO drive and steering motors do not require that architecture.

The EV3 already provides the required motor interface.

Therefore, the final propulsion path is:

```text
EV3 Battery
     ↓
LEGO EV3
     ↓
Port A
     ↓
Drive Motor
```

rather than:

```text
Battery
   ↓
Microcontroller
   ↓
External Motor Driver
   ↓
Motor
```

The same applies to the steering actuator on Port B.

This eliminates additional motor-control electronics from the final vehicle architecture and reduces the number of electrical connections required for normal mobility.

---

# 9.7 Separation Between Power and Data

One important distinction in Piolín's electrical architecture is that **a communication connection should not automatically be interpreted as the complete power-distribution diagram**.

For example, the confirmed vision communication path is:

```text
HuskyLens
    ↓
Arduino Nano
    ↓
USB
    ↓
EV3
```

This describes how information reaches the main controller.

The detailed electrical supply connections of the HuskyLens/Nano subsystem belong in the dedicated wiring and electrical-schematic documentation.

Keeping the two concepts separate prevents diagrams such as:

```text
DATA CONNECTION
```

from being incorrectly interpreted as:

```text
POWER CONNECTION
```

The repository therefore distinguishes between:

```text
COMMUNICATION ARCHITECTURE
```

and:

```text
POWER DISTRIBUTION ARCHITECTURE
```

even when both involve the same physical devices.

---

# 9.8 Vision Subsystem Integration

The HuskyLens and Arduino Nano form Piolín's external vision subsystem.

From a functional perspective:

```text
HUSKYLENS
     ↓
Visual Recognition
     ↓
ARDUINO NANO
     ↓
Communication Interface
     ↓
USB
     ↓
LEGO EV3
```

The EV3 does not need to dedicate one of its four sensor ports to the vision subsystem.

This is particularly important because all four native sensor ports are already occupied:

```text
S1 = Front Ultrasonic
S2 = Right Ultrasonic
S3 = Left Ultrasonic
S4 = Color Sensor
```

Using USB for the Nano communication therefore allows the final sensor configuration to remain intact.

---

# 9.9 Why the Vision Subsystem Is Electrically Documented Separately

Piolín's vehicle-control hardware is almost entirely LEGO EV3-based, while the HuskyLens and Nano belong to a separate electronics ecosystem.

Treating both systems as identical would hide an important architectural distinction.

The final documentation therefore separates:

```text
EV3 DOMAIN

Battery
  ↓
EV3
  ↓
LEGO Motors + Sensors
```

from:

```text
VISION DOMAIN

HuskyLens
    ↕
Arduino Nano
    ↕
EV3 communication
```

The exact vision wiring is documented in:

```text
docs/reproducibility/03_wiring.md
```

and the electrical schematic is documented in:

```text
docs/reproducibility/04_elecschem.md
```

This keeps the component-level power overview accurate without inventing electrical details that belong to the final wiring diagram.

---

# 9.10 Power Flow During Open Challenge

During the Open Challenge, Piolín's essential navigation hardware is centered completely around the EV3 system.

```text
                       EV3 BATTERY
                            │
                            ▼
                          EV3
                            │
          ┌─────────────────┼─────────────────┐
          ▼                 ▼                 ▼
      MOTOR A           MOTOR B           SENSORS
       Drive            Steering          S1–S4
          │                 │                 │
          └─────────────────┴─────────┬───────┘
                                      ▼
                               Open Navigation
```

The lateral ultrasonic sensors provide track geometry, the front sensor provides frontal safety, and the color sensor provides course-state information.

The Open Challenge navigation logic therefore does not depend on the camera subsystem to perform its fundamental wall-following behavior.

This is both a sensing and electrical simplification.

---

# 9.11 Power Flow During Obstacle Challenge

The Obstacle Challenge uses the same EV3 vehicle-control hardware but adds information from the vision subsystem.

```text
                         HUSKYLENS
                             │
                             ▼
                       ARDUINO NANO
                             │
                            USB
                             │
                             ▼
                       ┌───────────┐
                       │ LEGO EV3  │
                       └─────┬─────┘
                             │
          ┌──────────────────┼──────────────────┐
          ▼                  ▼                  ▼
       MOTOR A            MOTOR B            S1–S4
        Drive             Steering           Sensors
```

The key difference is informational rather than mechanical.

Motor A and Motor B remain controlled by the EV3.

The ultrasonic sensors remain connected to S1–S3.

The color sensor remains on S4.

The vision subsystem simply provides an additional perception input.

---

# 9.12 Dynamic Electrical Load

Piolín does not create one constant electrical load throughout the entire course.

Different navigation states require different levels of actuator activity.

During a straight section:

```text
Motor A → continuous propulsion
Motor B → small corrections
Sensors → continuously active
EV3 → continuously processing
```

During a corner:

```text
Motor A → controlled propulsion
Motor B → stronger steering activity
Sensors → active
EV3 → active
```

During obstacle avoidance:

```text
Motor A → controlled propulsion
Motor B → stronger directional change
Vision subsystem → relevant
Ultrasonics → active
EV3 → active
```

This means the power system supports a continuously changing combination of loads.

---

# 9.13 High Mechanical Load and Electrical Demand

Motor electrical demand is related to mechanical load.

When a motor must produce more mechanical torque, it generally requires more electrical effort from the power system.

For Motor A, increased load can come from:

```text
Acceleration
Drivetrain resistance
Wheel friction
Vehicle mass
```

For Motor B, increased load can come from:

```text
Steering linkage resistance
Tire contact
Large steering corrections
Mechanical limits
```

This creates an important relationship:

```text
Mechanical System
      ↕
Electrical System
```

A mechanical problem can therefore appear as an electrical-load problem.

For example, excessive steering friction increases the work required from Motor B even if the software command has not changed.

---

# 9.14 Why Mechanical Efficiency Matters to Power Distribution

Power distribution should not be treated only as wires and connectors.

The electrical system ultimately exists to produce useful mechanical behavior.

If unnecessary friction consumes motor effort, electrical energy is being used without creating the desired amount of vehicle motion.

```text
Electrical Energy
       ↓
Motor
       ↓
Mechanical Output
       │
       ├── Useful Motion
       │
       └── Mechanical Losses
```

Reducing drivetrain friction, steering resistance, and unnecessary wheel slip therefore benefits the complete power architecture.

Piolín's mechanical and electrical systems are directly interconnected.

---

# 9.15 Software Also Influences Electrical Demand

The software does not generate electrical energy, but it determines how the actuators use it.

For example, continuous large steering oscillations require more motor movement than a stable control strategy.

```text
Unstable control
      ↓
Left correction
      ↓
Right correction
      ↓
Left correction
      ↓
Repeated motor activity
```

A smoother controller instead produces:

```text
Measured error
      ↓
Appropriate correction
      ↓
Stable trajectory
```

This means good software tuning can reduce unnecessary actuator activity while improving navigation.

Power efficiency is therefore influenced by control strategy as well as hardware.

---

# 9.16 Front Emergency Stop and Power Control

The front ultrasonic sensor provides a direct link between perception and the propulsion power state.

Under normal conditions:

```text
EV3
 ↓
Motor A
 ↓
Propulsion
```

If a dangerous frontal condition is detected:

```text
Front US
   ↓
EV3 Safety Logic
   ↓
Normal propulsion interrupted
   ↓
Motor A brake / stop
```

The sensor itself does not physically disconnect the battery.

Instead, it changes the motor-control decision made by the EV3.

This distinction is important because Piolín's safety architecture is software-controlled rather than based on a separate hardware emergency relay.

---

# 9.17 Steering Limits as Electrical Protection

Piolín's software steering limits also reduce unnecessary electrical stress.

The steering motor has a useful mechanical range.

If the linkage has already reached that range, commanding additional movement would not produce a larger steering angle.

```text
Useful steering range
        ↓
Mechanical limit
        ↓
No additional wheel movement
```

Continuing to command the motor against that limit would increase load without improving navigation.

For this reason, software steering limits serve two purposes:

```text
Navigation control
        +
Mechanical / electrical protection
```

The controller avoids intentionally using actuator effort where the mechanism cannot produce useful additional movement.

---

# 9.18 Electrical Architecture and Failure Isolation

A centralized but modular system also helps identify where a failure occurs.

For example:

```text
Drive problem
    ↓
Port A / Drive Motor / Drivetrain


Steering problem
    ↓
Port B / Steering Motor / Linkage


Front-distance problem
    ↓
S1 / Front Ultrasonic


Right-distance problem
    ↓
S2 / Right Ultrasonic


Left-distance problem
    ↓
S3 / Left Ultrasonic


Floor-detection problem
    ↓
S4 / Color Sensor


Vision communication problem
    ↓
HuskyLens / Nano / USB
```

Because the port map is fixed and documented, each subsystem has a clear electrical location.

This simplifies both documentation and troubleshooting.

---

# 9.19 Why the Final Architecture Avoids Unnecessary Converters

Earlier Piolín concepts explored more complex electronic systems involving additional control electronics.

The final EV3-centered architecture avoids adding power-conversion or motor-control components where the LEGO hardware can already perform the required task directly.

The design principle is:

```text
Add hardware
ONLY
when it solves a real missing function
```

For the final LEGO motor and sensor system:

```text
EV3 already provides interface
        ↓
No additional motor driver required
        ↓
No additional sensor interface required
```

The vision subsystem remains separate because it solves a perception problem that the EV3-native sensors do not solve.

---

# 9.20 Cable and Connection Organization

Power and signal reliability depend on physical wiring as well as electronic design.

Piolín contains moving mechanical components, particularly the steering system, so cables must be routed without interfering with wheel movement or the steering linkage.

Conceptually:

```text
GOOD ROUTING

Cable
  │
  └────────→ Secure path
                │
                └── Away from linkage
```

rather than:

```text
POOR ROUTING

Cable
   ↓
Steering linkage
   ↓
Mechanical interference
```

Cable organization is therefore part of both electrical and mechanical reliability.

The detailed wiring layout is documented in the reproducibility section.

---

# 9.21 Why the EV3 Port Map Is Kept Fixed

Keeping a consistent port assignment reduces ambiguity between hardware documentation and software.

The final mapping is:

```text
A  → Drive
B  → Steering

S1 → Front US
S2 → Right US
S3 → Left US
S4 → Color
```

This same arrangement can appear directly in the source code:

```python
drive = Motor(Port.A)
steer = Motor(Port.B)

us_front = UltrasonicSensor(Port.S1)
us_right = UltrasonicSensor(Port.S2)
us_left = UltrasonicSensor(Port.S3)

color_sensor = ColorSensor(Port.S4)
```

The relationship therefore becomes:

```text
PHYSICAL PORT
      =
SOFTWARE PORT
      =
DOCUMENTED FUNCTION
```

Maintaining this consistency improves reproducibility.

---

# 9.22 Power Distribution and Reproducibility

Another team attempting to reconstruct Piolín must know not only which components are used, but where they connect.

The essential EV3 power and interface architecture can be reproduced from the following table:

| Component | Connection |
| :--- | :--- |
| **Drive Motor** | EV3 Port A |
| **Steering Motor** | EV3 Port B |
| **Front Ultrasonic** | EV3 Port S1 |
| **Right Ultrasonic** | EV3 Port S2 |
| **Left Ultrasonic** | EV3 Port S3 |
| **Color Sensor** | EV3 Port S4 |
| **Arduino Nano** | EV3 USB communication |

This architecture should remain identical between the component documentation, wiring guide, electrical schematic, and final software.

---

# 9.23 Electrical Documentation Hierarchy

Piolín's repository separates electrical documentation into several levels so that one file does not attempt to explain everything.

```text
components/08_Battery.md
        ↓
Main energy source


components/09_PowerDistribution.md
        ↓
How the main hardware receives energy and interfaces


reproducibility/03_wiring.md
        ↓
Physical cable connections


reproducibility/04_elecschem.md
        ↓
Electrical schematic


power_sensors/01_PowerSensorconfig.md
        ↓
System-level sensor and power reasoning
```

This separation keeps each document focused while allowing the complete electrical architecture to remain traceable.

---

# 9.24 Confirmed vs. Unverified Electrical Values

Piolín's documentation distinguishes between architecture that is physically confirmed and electrical values that would require direct measurement.

The confirmed architecture includes:

```text
EV3 battery as main vehicle energy source

EV3-controlled Motor A

EV3-controlled Motor B

Three EV3 ultrasonic sensors

One EV3 color sensor

Nano communication with EV3 through USB
```

The documentation does not present estimated current consumption, voltage drop, power draw, or runtime as if those values were measured directly from the final robot.

This distinction protects the technical accuracy of the repository.

The objective of this section is to document **how power is distributed**, not to invent numerical electrical performance.

---

# 9.25 Power Distribution Responsibility Matrix

The main electrical responsibilities can be summarized as:

| System | Power / Interface Responsibility |
| :--- | :--- |
| **EV3 Battery** | Main stored-energy source for vehicle-control system |
| **LEGO EV3** | Main controller and LEGO hardware interface |
| **Motor A** | Converts electrical energy into propulsion |
| **Motor B** | Converts electrical energy into steering movement |
| **S1 Front US** | Distance sensing through EV3 sensor interface |
| **S2 Right US** | Distance sensing through EV3 sensor interface |
| **S3 Left US** | Distance sensing through EV3 sensor interface |
| **S4 Color Sensor** | Optical floor sensing through EV3 interface |
| **Arduino Nano** | Vision communication interface |
| **HuskyLens** | Visual perception subsystem |

The table shows that energy distribution, sensing, communication, and control are related but distinct responsibilities.

---

# 9.26 Complete System Architecture

Piolín's overall hardware architecture can be represented as:

```text
                            EV3 BATTERY
                                 │
                                 ▼
                           ┌───────────┐
                           │ LEGO EV3  │
                           └─────┬─────┘
                                 │
           ┌─────────────────────┼─────────────────────┐
           │                     │                     │
           ▼                     ▼                     ▼
         MOTORS                SENSORS              PROCESSING
           │                     │                     │
    ┌──────┴──────┐     ┌────────┼────────┐            │
    ▼             ▼     ▼        ▼        ▼            │
 Drive         Steering Front   Right    Left           │
Motor A        Motor B    US      US       US           │
                         S1      S2       S3            │
                                  │                     │
                                  ▼                     │
                              Color S4                  │
                                                        │
                             USB Communication          │
                                    ▲                   │
                                    │                   │
                              Arduino Nano              │
                                    ▲                   │
                                    │                   │
                                HuskyLens               │
```

This diagram separates the EV3-native electrical system from the external vision communication path while showing how both ultimately contribute to the same autonomous controller.

---

# 9.27 Engineering Decision Summary

The final power-distribution architecture reflects Piolín's broader engineering philosophy: **keep the fundamental vehicle system as simple as possible while adding specialized hardware only where necessary**.

The EV3 already provides the required interface for the motors and LEGO sensors.

Therefore:

```text
EV3 Battery
     ↓
EV3
     ↓
Motors + Sensors
```

remains the foundation of the robot.

The HuskyLens and Arduino Nano are added because vision requires capabilities outside the four native EV3 sensor connections, but they are kept as a specialized subsystem rather than replacing the primary control architecture.

The resulting system avoids unnecessary duplication of:

```text
Motor drivers
Sensor interfaces
Main controllers
Power stages
```

within the core navigation platform.

---

# 9.28 Final Power Distribution Summary

Piolín's final WRO Future Engineers 2026 power architecture is centered around the **LEGO EV3 battery and Intelligent Brick**.

The EV3 battery provides the main energy source for the vehicle-control system. The EV3 then interfaces directly with:

```text
Port A  → Drive Motor

Port B  → Steering Motor

Port S1 → Front Ultrasonic

Port S2 → Right Ultrasonic

Port S3 → Left Ultrasonic

Port S4 → Color Sensor
```

The HuskyLens and Arduino Nano form a specialized external vision subsystem whose information reaches the EV3 through USB communication.

The final architecture can therefore be summarized as:

```text
                    MAIN VEHICLE POWER

                       EV3 BATTERY
                            ↓
                         LEGO EV3
                            ↓
             Motors + Navigation Sensors


                   SPECIALIZED VISION

                        HUSKYLENS
                            ↓
                     ARDUINO NANO
                            ↓
                           USB
                            ↓
                         LEGO EV3
```

The central engineering principle is:

> **The EV3 power system supports the hardware responsible for moving and sensing the track.**

> **The external vision subsystem adds obstacle perception without replacing the main EV3 architecture.**

> **Power, communication, sensing, and control are documented as separate responsibilities so that the complete robot architecture remains technically clear and reproducible.**

Detailed physical wiring is documented in:

```text
docs/reproducibility/03_wiring.md
```

while the final electrical schematic is documented in:

```text
docs/reproducibility/04_elecschem.md
```
