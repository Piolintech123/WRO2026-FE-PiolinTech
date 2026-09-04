# 8. Battery and Main Energy Source

Piolín uses the **LEGO Mindstorms EV3 power system as the main energy source for the robot**. The battery installed in the EV3 supplies the energy required by the Intelligent Brick and, through it, the directly connected motors and LEGO sensors.

The battery is therefore not an isolated component. It sits at the beginning of Piolín's complete electrical and mechanical chain. Every steering correction, propulsion command, ultrasonic measurement, color-sensor reading, and EV3 computation ultimately depends on a stable source of electrical energy.

The basic relationship is:

```text
                     EV3 BATTERY
                          │
                          ▼
                     LEGO EV3
                          │
          ┌───────────────┼───────────────┐
          │               │               │
          ▼               ▼               ▼
        MOTORS          SENSORS        PROCESSING
        A + B          S1–S4             EV3
          │               │               │
          └───────────────┴───────┬───────┘
                                  ▼
                         AUTONOMOUS ROBOT
````

The final Piolín architecture intentionally keeps the primary navigation hardware within the EV3 electrical ecosystem. This reduces the need for additional motor drivers, separate high-current power rails, or multiple independent battery systems for the basic vehicle.

> [!IMPORTANT]
> The EV3 battery is the **main power source of Piolín's vehicle-control system**.
> It powers the EV3 and supports the LEGO motors and sensors connected directly to it.

---

## 8.1 Role of the Battery in Piolín

The battery provides the electrical energy that allows Piolín to convert software decisions into physical movement.

A sensor measurement by itself requires relatively little mechanical energy. However, once the EV3 interprets that measurement and commands a steering correction or acceleration, electrical energy from the battery must be converted into mechanical work by the motors.

The complete relationship can be represented as:

```text
CHEMICAL ENERGY
    Battery
       │
       ▼
ELECTRICAL ENERGY
       │
       ▼
     LEGO EV3
       │
       ├──────────→ Sensors
       │
       ├──────────→ Processing
       │
       └──────────→ Motors
                       │
                       ▼
                MECHANICAL ENERGY
                       │
                       ▼
                 ROBOT MOVEMENT
```

The battery therefore supports both **perception** and **actuation**, but the largest changes in instantaneous electrical demand normally occur when the motors are required to perform mechanical work.

---

# 8.2 Centralized EV3 Power Architecture

One of Piolín's final hardware decisions was to maintain a centralized power architecture for the LEGO vehicle-control components.

The EV3 acts as both the main computational controller and the distribution point for its directly connected LEGO hardware.

```text
EV3 BATTERY
     │
     ▼
┌──────────────────────────┐
│        LEGO EV3          │
│                          │
│ A  → Drive Motor         │
│ B  → Steering Motor      │
│                          │
│ S1 → Front Ultrasonic    │
│ S2 → Right Ultrasonic    │
│ S3 → Left Ultrasonic     │
│ S4 → Color Sensor        │
└──────────────────────────┘
```

This arrangement means that Piolín's primary navigation system does not require separate electrical regulators or external motor-control electronics between the EV3 and the LEGO components.

The architecture is simpler than earlier experimental concepts that involved additional controllers and external motor electronics.

---

# 8.3 Power Consumers

The electrical loads connected to the EV3 can be separated into three main groups.

```text
                     EV3 BATTERY
                          │
             ┌────────────┼────────────┐
             ▼            ▼            ▼
          CONTROL       SENSING      ACTUATION
             │            │            │
             ▼            ▼            ▼
            EV3        S1–S4        MOTOR A
                                   + MOTOR B
```

The **control load** consists primarily of the EV3 itself and its processing electronics.

The **sensing load** consists of the three ultrasonic sensors and the color sensor.

The **actuation load** consists of the drive and steering motors.

These loads behave differently. Sensors and processing electronics normally require power continuously while the robot is active, whereas motor demand changes significantly according to the mechanical state of the vehicle.

---

## 8.4 Drive Motor Energy Demand

The drive motor connected to **Port A** converts electrical energy into propulsion.

During normal straight movement, the motor must overcome drivetrain resistance and maintain the desired vehicle speed.

When Piolín accelerates, the motor must additionally increase the kinetic energy of the complete robot.

The relationship is:

```text
Battery
   ↓
EV3
   ↓
Motor A
   ↓
Rear Drivetrain
   ↓
Rear Wheels
   ↓
Vehicle Motion
```

Piolín's final measured mass is approximately:

```text
MASS = 0.80476 kg
```

Because the entire mass must be accelerated by the propulsion system, the mechanical load on Motor A changes according to the requested motion.

A stronger acceleration generally requires greater motor effort than maintaining a stable speed.

This is one reason propulsion behavior and electrical demand cannot be considered completely independent.

---

# 8.5 Steering Motor Energy Demand

The steering motor on **Port B** also receives its energy through the EV3 power system.

Its electrical demand is linked to the resistance of the Ackermann steering mechanism.

```text
Battery
   ↓
EV3
   ↓
Motor B
   ↓
Steering Linkage
   ↓
Front Wheels
```

A small steering correction under low mechanical resistance requires less effort than forcing the steering mechanism rapidly toward a large angle or holding it against a physical limit.

For this reason, Piolín's software avoids treating the steering motor as a simple position device with unlimited mechanical authority.

Mechanical steering limits also protect the electrical system by avoiding unnecessary motor load once the linkage has reached its useful range.

---

# 8.6 Simultaneous Motor Load

Motor A and Motor B can operate at the same time.

This occurs frequently during autonomous navigation.

For example:

```text
Corner detected
      ↓
Motor A continues propulsion
      +
Motor B increases steering
      ↓
Both motors operating
```

The same situation appears during obstacle avoidance:

```text
Obstacle detected
      ↓
Motor A controls approach speed
      +
Motor B produces avoidance steering
```

The battery must therefore support the complete vehicle behavior rather than only one motor operating independently.

This shared-power architecture is one of the reasons battery condition can influence the physical response of the robot.

---

# 8.7 Sensor Power

The three ultrasonic sensors and the color sensor are connected directly to the EV3 sensor ports.

Their power is therefore supplied through the EV3 rather than through separate batteries.

```text
EV3 BATTERY
     ↓
   LEGO EV3
     │
     ├── S1 → Front Ultrasonic
     ├── S2 → Right Ultrasonic
     ├── S3 → Left Ultrasonic
     └── S4 → Color Sensor
```

This creates a clean relationship between sensing and control.

The same device that provides the electrical interface to the sensors also receives their measurements and interprets them in software.

No independent power source is required for the four directly connected navigation sensors.

---

# 8.8 EV3 Processing Power

The EV3 itself also consumes energy while executing Piolín's navigation software.

The brick continuously performs tasks such as:

```text
Read ultrasonic sensors
        ↓
Read color sensor
        ↓
Update navigation state
        ↓
Interpret wall geometry
        ↓
Process safety conditions
        ↓
Calculate motor commands
        ↓
Communicate with external subsystem
```

This computational load is different from the mechanical load produced by the motors.

The processor does not physically move Piolín, but the robot cannot operate autonomously without the EV3 remaining powered and executing the control program.

The battery therefore supports both the **decision layer** and the **actuation layer** of the robot.

---

# 8.9 Battery Condition and Robot Behavior

The physical behavior of an electric motor depends partly on the electrical energy available to it.

For this reason, battery condition can influence how Piolín responds even when the software command remains unchanged.

Conceptually:

```text
Software command
       ↓
      EV3
       ↓
Electrical output
       ↓
Motor response
       ↓
Physical movement
```

The software command is only one element of this chain.

Motor load, drivetrain resistance, steering resistance, and battery condition also influence the resulting physical motion.

This is particularly relevant for Piolín because autonomous navigation depends on repeatable timing between sensing and movement.

If the physical response of the drivetrain changes significantly, the robot may reach a corner or obstacle with a slightly different trajectory even though the program itself has not changed.

---

# 8.10 Why Battery State Matters for Navigation

Piolín's navigation system continuously reacts to the environment.

The vehicle is therefore part of a feedback loop:

```text
Sensor measurement
      ↓
Navigation decision
      ↓
Motor command
      ↓
Physical movement
      ↓
New sensor measurement
```

Battery condition can influence the **motor-command-to-physical-movement** stage.

For example, a steering command may still request the same encoder target, but the speed at which the mechanism responds can be influenced by mechanical and electrical load.

Similarly, the drive motor may receive the same software command while the physical acceleration differs slightly under different operating conditions.

This demonstrates why the battery is part of Piolín's control system even though it does not participate directly in navigation logic.

---

# 8.11 Battery and Emergency Braking

The front ultrasonic sensor can cause the EV3 to interrupt propulsion when a dangerous frontal condition is detected.

The electrical relationship is:

```text
Front US
   ↓
EV3 detects danger
   ↓
Normal Motor A command cancelled
   ↓
Motor braking behavior
   ↓
Piolín decelerates
```

The battery remains the energy source during this event, but the EV3 changes how the propulsion motor is controlled.

The physical robot does not stop instantaneously because Piolín still has momentum.

Therefore, emergency braking is a combination of:

```text
Sensing
+
Software decision
+
Motor control
+
Vehicle mechanics
```

rather than a property of the battery alone.

---

# 8.12 Battery and Steering Stability

The steering system is mechanically loaded by the front wheels, linkage, and tire contact with the competition surface.

Motor B must overcome that resistance using electrical energy supplied through the EV3.

The complete relationship is:

```text
EV3 Battery
     ↓
EV3
     ↓
Motor B
     ↓
Mechanical Torque
     ↓
Steering Linkage
     ↓
Front Wheel Direction
```

This is another reason Piolín avoids unnecessary aggressive steering commands.

Repeatedly commanding large opposite steering angles creates more mechanical activity than maintaining a stable trajectory with smaller corrections.

A smoother controller therefore benefits not only navigation stability but also overall actuator efficiency.

---

# 8.13 Energy Use During Different Navigation States

Piolín does not use its actuators identically throughout the entire course.

Different states create different mechanical demands.

| Navigation State       | Drive Motor Behavior             | Steering Motor Behavior       |
| :--------------------- | :------------------------------- | :---------------------------- |
| **Straight**           | Continuous propulsion            | Small corrections             |
| **Corner Entry**       | Controlled propulsion            | Increasing steering           |
| **Corner**             | Controlled movement              | Stronger directional control  |
| **Corner Exit**        | Returns toward straight behavior | Moves toward center           |
| **Obstacle Approach**  | Controlled approach              | Prepares avoidance            |
| **Obstacle Avoidance** | Active propulsion                | Strong directional maneuver   |
| **Recovery**           | Continued propulsion             | Re-centering                  |
| **Frontal Emergency**  | Brake / Stop                     | Normal navigation interrupted |

This means electrical demand varies naturally according to what the robot is doing.

The battery therefore supports a **dynamic load**, not one constant operating condition.

---

# 8.14 Power Path to the Navigation Sensors

The main LEGO sensing system follows a direct electrical path:

```text
                        EV3 BATTERY
                             │
                             ▼
                         LEGO EV3
                             │
             ┌───────────────┼───────────────┐
             │               │               │
             ▼               ▼               ▼
            S1              S2              S3
        Front US        Right US         Left US

                             │
                             ▼
                            S4
                       Color Sensor
```

This direct connection reduces the number of interfaces between the power source and the navigation sensors.

It also means that the LEGO sensing subsystem and vehicle controller share one integrated power architecture.

---

# 8.15 Relationship With the Vision Subsystem

The HuskyLens and Arduino Nano form a separate functional subsystem from the EV3's native motor and sensor connections.

Their **communication path** is:

```text
HuskyLens
    ↓
Arduino Nano
    ↓
USB
    ↓
EV3
```

The battery section intentionally distinguishes communication from electrical distribution.

The fact that information travels through USB does not by itself define every electrical connection inside the vision subsystem.

The detailed routing of power between the EV3, Arduino Nano, and HuskyLens is therefore documented in the dedicated **Power Distribution** and wiring sections rather than being mixed with the main battery description.

This keeps the hardware documentation consistent with the physical wiring architecture.

---

# 8.16 Why Piolín Uses a Central Vehicle Battery Architecture

Earlier experimental hardware concepts included more complex electronic systems and additional control hardware.

The final robot returned to a simpler EV3-centered vehicle architecture.

One important advantage is that the main propulsion, steering, processing, and LEGO sensing system can operate from one integrated platform.

```text
             ONE MAIN VEHICLE PLATFORM

                   EV3 Battery
                        ↓
                       EV3
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
     Motors           Sensors        Processing
```

This reduces the number of separate energy systems that must remain synchronized during the fundamental navigation task.

The objective was not simply to minimize component count. It was to reduce unnecessary electrical complexity while preserving all of the sensing and actuation capabilities Piolín actually needs.

---

# 8.17 Power-System Modularity

Although the EV3 battery is the main vehicle energy source, Piolín's architecture remains modular from a functional perspective.

```text
POWER
  ↓
EV3 battery system


NAVIGATION
  ↓
EV3 + Ultrasonics + Color


VISION
  ↓
HuskyLens + Nano


ACTUATION
  ↓
Motor A + Motor B
```

Separating these responsibilities makes the architecture easier to understand.

The battery provides energy.

The EV3 distributes and manages the directly connected LEGO hardware.

The sensors provide information.

The motors convert electrical energy into mechanical movement.

The vision subsystem provides additional obstacle information.

No single component is documented as performing responsibilities that belong to another subsystem.

---

# 8.18 Battery and Mechanical Efficiency

Electrical energy consumed by the drive motor does not become useful vehicle motion with perfect efficiency.

Some energy is lost through:

```text
Motor internal losses
Drivetrain friction
Axle resistance
Tire deformation
Wheel slip
```

The same principle applies to steering.

Some electrical energy is used to overcome friction in the linkage and tire contact rather than directly changing the ideal vehicle trajectory.

This creates the relationship:

```text
Battery Energy
      ↓
Electrical Motor Input
      ↓
Mechanical Motor Output
      ↓
Drivetrain / Steering Losses
      ↓
Useful Vehicle Movement
```

Reducing unnecessary mechanical friction therefore benefits both mobility and energy use.

This is another example of how Piolín's electrical and mechanical systems are interconnected.

---

# 8.19 Why Unnecessary Motor Load Is Avoided

When a motor reaches a mechanical limit but the controller continues commanding additional movement, the motor cannot convert the extra effort into useful steering or propulsion.

In the steering system:

```text
Motor command
     ↓
Mechanical limit reached
     ↓
No additional wheel angle
     ↓
Unnecessary motor load
```

For this reason, Piolín uses software steering limits that correspond to the useful mechanical range of the linkage.

A similar principle applies to propulsion. Excessively aggressive acceleration can increase wheel slip without producing the same proportional increase in useful vehicle movement.

The final architecture therefore aims to convert battery energy into controlled movement rather than maximizing actuator effort at every moment.

---

# 8.20 Battery as Part of System Reliability

The battery is a fundamental reliability component because every active subsystem ultimately depends on electrical power.

A simplified dependency map is:

```text
                         BATTERY
                            │
                            ▼
                           EV3
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
      Sensors             Motors            Software
        │                   │                   │
        └───────────────────┴──────────┬────────┘
                                       ▼
                              Autonomous Behavior
```

A navigation algorithm can be logically correct, but it cannot produce predictable physical behavior if the actuators do not receive sufficient energy to execute the requested motion.

The power system therefore belongs to the same engineering chain as software, sensors, and mechanics.

---

# 8.21 Battery Safety and Mechanical Placement

The battery is carried inside the vehicle and therefore contributes to Piolín's total mass and mass distribution.

Piolín's final measured total robot mass is approximately:

```text
0.80476 kg
```

The battery is part of that complete vehicle mass.

Like other relatively heavy components, its physical position can influence the robot's center of mass and mechanical stability.

The battery must also remain mechanically secure so that it does not shift relative to the chassis during acceleration, braking, or cornering.

Conceptually:

```text
SECURE BATTERY
      ↓
Stable mass distribution
      ↓
Consistent vehicle dynamics
```

The battery is therefore both an electrical component and part of the mechanical packaging of the robot.

---

# 8.22 Why Battery Position Matters

The position of mass affects how a vehicle responds during acceleration and turning.

If a relatively heavy component shifts during movement, the distribution of forces across the wheels can also change.

For an Ackermann-steered vehicle such as Piolín, stable mechanical packaging supports predictable turning behavior.

```text
Fixed Component Position
        ↓
Stable Mass Distribution
        ↓
Predictable Wheel Loading
        ↓
More Consistent Vehicle Behavior
```

The battery is therefore installed as part of the chassis architecture rather than treated as a loose external power source.

---

# 8.23 Battery and the Final Robot Mass

Piolín's complete mass of approximately **0.80476 kg** includes the controller, battery, motors, sensors, wheels, chassis structure, wiring, vision hardware, and mechanical assemblies.

This means the propulsion motor must accelerate the complete electrical system along with the mechanical chassis.

The vehicle-level relationship is:

```text
Battery
   │
   ├── Provides electrical energy
   │
   └── Contributes physical mass
            ↓
       Complete Robot
            ↓
        0.80476 kg
```

This dual role is common in mobile robotics: the energy source enables movement while simultaneously increasing the mass that the drivetrain must move.

Battery selection and vehicle architecture are therefore mechanically connected.

---

# 8.24 Why Exact Electrical Claims Are Kept Separate

Piolín's component documentation distinguishes between confirmed robot configuration and assumptions about electrical behavior.

Values such as instantaneous current consumption, exact runtime, internal voltage drop, and total power consumption depend on the real operating state of the robot.

For that reason, this component section does not present estimated electrical values as if they were direct measurements from Piolín.

The distinction is:

```text
CONFIRMED
    ↓
Physical battery architecture
Connected hardware
Power responsibilities


OPERATING ELECTRICAL VALUES
    ↓
Depend on actual system load
```

This keeps the repository technically consistent and prevents theoretical estimates from being mistaken for measured competition data.

Detailed system-level power distribution is documented separately in:

```text
docs/components/09_PowerDistribution.md
```

and:

```text
docs/power_sensors/01_PowerSensorconfig.md
```

---

# 8.25 Battery Responsibility Matrix

The role of the main EV3 battery system can be summarized as:

| Function                         |       Battery Role      |
| :------------------------------- | :---------------------: |
| **Power EV3 controller**         |       **Primary**       |
| **Support Motor A propulsion**   |       **Primary**       |
| **Support Motor B steering**     |       **Primary**       |
| **Support S1 ultrasonic**        | **Primary through EV3** |
| **Support S2 ultrasonic**        | **Primary through EV3** |
| **Support S3 ultrasonic**        | **Primary through EV3** |
| **Support S4 color sensor**      | **Primary through EV3** |
| **Determine navigation logic**   |            No           |
| **Determine steering direction** |            No           |
| **Measure environment**          |            No           |
| **Provide stored energy**        |       **Primary**       |

The battery does not make autonomous decisions.

Its role is to provide the energy that allows every other active vehicle subsystem to perform its assigned function.

---

# 8.26 Integration With the Complete Robot

The main energy path can be combined with Piolín's complete functional architecture:

```text
                            BATTERY
                               │
                               ▼
                           LEGO EV3
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
          ▼                    ▼                    ▼
       SENSORS              PROCESSING            MOTORS
          │                    │                    │
          │              Navigation Logic          │
          │                    │                    │
          └────────────────────┼────────────────────┘
                               │
                               ▼
                       AUTONOMOUS RESPONSE
```

The EV3 battery is therefore one of the few components that indirectly participates in every major vehicle function.

Without sensing, Piolín cannot understand the environment.

Without processing, it cannot decide what to do.

Without motors, it cannot move.

Without electrical energy, none of those systems can operate.

---

# 8.27 Engineering Decision Summary

The final Piolín architecture favors an **EV3-centered power system** for the fundamental vehicle hardware.

This decision keeps the main controller, drive motor, steering motor, three ultrasonic sensors, and color sensor within the same integrated electrical platform.

The development philosophy can be summarized as:

```text
MORE COMPLEX POWER ARCHITECTURES
             ↓
More interfaces and dependencies
             ↓
Architecture simplified
             ↓
EV3-centered vehicle power
             ↓
Clearer hardware responsibilities
```

The goal was not to create the most electrically complex robot.

It was to create a power architecture appropriate for the hardware actually required by Piolín.

The result is a system in which the EV3 battery supplies the vehicle-control platform while specialized external hardware remains clearly separated by function.

---

# 8.28 Final Battery Architecture Summary

Piolín's battery is the main stored-energy source behind the LEGO EV3 vehicle-control system.

Its fundamental architecture is:

```text
                         EV3 BATTERY
                              │
                              ▼
                          LEGO EV3
                              │
           ┌──────────────────┼──────────────────┐
           │                  │                  │
           ▼                  ▼                  ▼
        MOTOR A            MOTOR B          SENSORS S1–S4
          Drive             Steering             │
           │                  │                  │
           └──────────────────┴──────────┬───────┘
                                         ▼
                                  ROBOT OPERATION
```

The battery supports propulsion, steering, sensing, and computation through the EV3 platform.

Its importance extends beyond simply "turning the robot on." Battery condition influences the electrical environment in which the motors and controller operate, while the battery's physical mass also contributes to the vehicle's mechanical behavior.

The final engineering relationship can therefore be summarized as:

> **The battery stores the energy.**

> **The EV3 distributes and controls how that energy is used by the LEGO hardware.**

> **The motors convert it into movement.**

> **The sensors and controller use it to perceive and interpret the environment.**

This centralized energy architecture supports Piolín's broader design goal of keeping the fundamental navigation system integrated, understandable, and free from unnecessary electrical complexity.

Detailed power routing and subsystem distribution are documented next in:

```text
docs/components/09_PowerDistribution.md
```

```
