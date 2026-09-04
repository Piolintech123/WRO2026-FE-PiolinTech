# 10. Other Components and Supporting Hardware

Piolín's final hardware architecture includes several supporting components that do not require an independent component document but are still essential to the operation, mechanical structure, integration, and reproducibility of the robot.

The EV3, motors, ultrasonic sensors, color sensor, HuskyLens, battery, and power architecture form the main active systems. However, those components cannot operate as a complete autonomous vehicle without the mechanical structures, interfaces, wheels, cables, connectors, and custom parts that connect them together.

These supporting components can be grouped into several categories:

```text
                    PIOLÍN
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
    ELECTRONICS     MECHANICS     INTEGRATION
        │             │             │
        ▼             ▼             ▼
 Arduino Nano      LEGO Technic    Wiring
 USB Interface     Structure       Connectors
                  Wheels / Axles   Mounts
                  Custom Casing    Fasteners
```

The purpose of this section is to document these secondary but necessary elements and explain how they support Piolín's main systems.

---

## 10.1 Supporting Component Summary

The main supporting components used in Piolín are:

| Component | Main Function |
| :--- | :--- |
| **Arduino Nano** | Communication bridge between the HuskyLens subsystem and EV3 |
| **USB connection** | Transfers vision information from Nano to EV3 |
| **LEGO Technic structure** | Forms chassis and component-support framework |
| **Technic axles and connectors** | Transfer motion and connect mechanical assemblies |
| **Front wheels** | Steering wheels |
| **Rear wheels** | Driven propulsion wheels |
| **Tires** | Provide floor contact and traction |
| **Color Sensor Casing** | Reduces uncontrolled ambient light around the floor sensor |
| **Sensor mounts** | Maintain sensor orientation relative to chassis |
| **Camera mounting structure** | Holds the HuskyLens in its forward-facing position |
| **Cable routing elements** | Keep electrical connections organized and clear of moving mechanisms |

Although these components perform different roles, all of them contribute to the reliability of the final robot.

---

# 10.2 Arduino Nano

Piolín uses an **Arduino Nano** as part of the vision subsystem.

Its role is deliberately limited.

The Nano does not replace the LEGO EV3 as Piolín's main controller and does not directly control the propulsion or steering motors.

Instead, it acts as an interface between the HuskyLens vision system and the EV3.

The final information architecture is:

```text
HUSKYLENS
     │
     ▼
ARDUINO NANO
     │
     │ USB
     ▼
LEGO EV3
     │
     ▼
Navigation Decision
```

The Arduino Nano therefore belongs to Piolín's **communication architecture**, rather than its primary motion-control architecture.

This separation allows the EV3 to remain responsible for:

```text
Motor control
Ultrasonic navigation
Color detection
Navigation state
Safety logic
Obstacle response
```

while the Nano concentrates on transferring useful vision information.

---

# 10.3 Why the Nano Is a Supporting Controller

Using more than one processor does not mean that Piolín uses several equal main controllers.

The final architecture follows a hierarchy:

```text
               MAIN CONTROLLER
                  LEGO EV3
                      ▲
                      │
                Vision Data
                      │
                ARDUINO NANO
                      ▲
                      │
                   HUSKYLENS
```

The EV3 remains at the center of the robot because it determines the final movement commands.

The Nano provides a specialized interface function.

This distinction is important for understanding Piolín's architecture:

> **The Nano communicates vision information. The EV3 controls the vehicle.**

---

# 10.4 USB Communication Connection

The Arduino Nano communicates with the LEGO EV3 through **USB**.

This allows the vision subsystem to reach the main controller without occupying one of the four EV3 sensor ports.

All four EV3 sensor ports are already assigned:

```text
S1 → Front Ultrasonic Sensor

S2 → Right Ultrasonic Sensor

S3 → Left Ultrasonic Sensor

S4 → Color Sensor
```

The vision system therefore follows another path:

```text
HuskyLens
    ↓
Arduino Nano
    ↓
USB
    ↓
EV3
```

This allows Piolín to retain all three ultrasonic sensors and the color sensor simultaneously while also integrating visual obstacle recognition.

The USB link shown here represents the confirmed Nano-to-EV3 communication connection. Detailed wiring is documented separately in the reproducibility section.

---

# 10.5 LEGO Technic Chassis Structure

Piolín's mechanical architecture is built primarily from **LEGO Technic structural elements**.

These components form the rigid framework that supports:

```text
EV3
Motors
Sensors
Vision Hardware
Battery
Wheels
Steering Mechanism
Drivetrain
```

The chassis is more than a platform for mounting electronics.

It establishes the relative position between all of the sensors and mechanical systems.

For example:

```text
Sensor Position
      ↓
Measured Geometry


Motor Position
      ↓
Mechanical Transmission


Wheel Position
      ↓
Vehicle Geometry
```

A change in the chassis can therefore affect sensing, steering, drivetrain behavior, and overall vehicle dimensions at the same time.

The LEGO Technic frame therefore acts as the common mechanical reference for the complete system.

---

# 10.6 Technic Beams and Connectors

LEGO Technic beams and connectors are used throughout Piolín to create the structural frame and connect different subsystems.

Their main function is to maintain the relative position of the robot's components.

Conceptually:

```text
         STRUCTURAL FRAME
                │
       ┌────────┼────────┐
       ▼        ▼        ▼
     EV3      Sensors   Motors
       │        │        │
       └────────┼────────┘
                ▼
            One Chassis
```

This structural consistency is particularly important for the lateral ultrasonic sensors and Ackermann steering mechanism.

If the structure holding those components changes orientation, the software may continue using the same values while the physical geometry of the robot has changed.

The LEGO Technic frame therefore acts as the mechanical reference shared by sensing and actuation.

---

# 10.7 Axles and Rotational Components

Technic axles are used in Piolín's drivetrain and steering assemblies to transmit rotational movement between components.

In the propulsion system:

```text
Drive Motor
    ↓
Mechanical Transmission
    ↓
Axle
    ↓
Rear Wheels
```

In the steering system:

```text
Steering Motor
      ↓
Mechanical Linkage
      ↓
Steering Components
      ↓
Front Wheel Direction
```

Axles therefore perform a different role from structural beams.

Beams primarily maintain geometry, while axles primarily transmit rotation.

Both are necessary for Piolín to behave as a vehicle rather than as a collection of independently mounted components.

---

# 10.8 Rear Wheels

Piolín's rear wheels form the primary propulsion interface with the competition surface.

Their measured diameter is approximately:

```text
2.4 in
```

which corresponds to:

```text
≈ 60.96 mm
```

or approximately:

```text
61.0 mm
```

The resulting radius is approximately:

```text
30.5 mm
```

and the geometric circumference is approximately:

```text
191.5 mm
```

Their role is:

```text
Motor A
   ↓
Rear Drivetrain
   ↓
Rear Wheels
   ↓
Floor Contact
   ↓
Vehicle Propulsion
```

These wheels therefore convert drivetrain rotation into forward or reverse movement of the complete robot.

---

# 10.9 Front Wheels

Piolín's front wheels have a measured diameter of:

```text
1.5 in
```

which corresponds to:

```text
38.1 mm
```

Their radius is therefore:

```text
19.05 mm
```

and their approximate circumference is:

```text
119.7 mm
```

Unlike the rear wheels, the front wheels are not Piolín's primary propulsion wheels.

Their main responsibility is directional control.

```text
Motor B
    ↓
Ackermann Linkage
    ↓
Front Wheels
    ↓
Vehicle Direction
```

The smaller front wheels therefore belong primarily to the steering system, while the larger rear wheels belong primarily to the propulsion system.

---

# 10.10 Different Front and Rear Wheel Sizes

Piolín operates with different wheel sizes at the front and rear because the two wheel groups perform different mechanical functions.

The final wheel configuration is:

| Wheel Position | Diameter | Primary Function |
| :--- | :---: | :--- |
| **Front** | **38.1 mm** | Steering |
| **Rear** | **~61.0 mm** | Propulsion |

The architecture can be represented as:

```text
                 FRONT

          O                 O
        38.1 mm          38.1 mm
           \               /
            \  STEERING   /
             \           /

              [ PIOLÍN ]

             PROPULSION

          O=================O
             ~61.0 mm

                  REAR
```

The front assembly prioritizes directional movement through the Ackermann mechanism, while the rear assembly converts Motor A rotation into vehicle displacement.

---

# 10.11 Tires

The tires form the physical contact point between Piolín and the competition surface.

Every motor command ultimately depends on this interface.

```text
Motor
  ↓
Wheel
  ↓
Tire
  ↓
Competition Surface
  ↓
Vehicle Movement
```

Tire behavior affects both propulsion and steering.

At the rear, traction is required to convert wheel rotation into forward movement.

At the front, tire interaction with the floor influences how effectively the Ackermann steering position changes the direction of the complete vehicle.

This means tire behavior is connected to:

```text
Acceleration
Braking
Cornering
Steering response
Wheel slip
```

The tires therefore form an important mechanical part of Piolín's control system even though they contain no electronics or software.

---

# 10.12 Color Sensor Casing

Piolín includes a dedicated casing around the downward-facing color sensor.

The purpose of the casing is to reduce uncontrolled ambient light entering the sensing region.

The optical relationship is:

```text
        External Light
      ↘      ↓      ↙

      ┌─────────────┐
      │   CASING    │
      │             │
      │ ColorSensor │
      └──────┬──────┘
             │
             ▼
      Competition Mat
```

The casing helps create a more consistent local optical environment.

This component represents a good example of solving a sensing problem mechanically rather than relying entirely on software.

---

# 10.13 Custom 3D-Printed Component

The repository includes the model for Piolín's color-sensor casing:

```text
models/
└── 3dprint/
    └── ColorSensorCasing.stl
```

This custom component connects CAD design directly with sensor reliability.

The relationship is:

```text
3D MODEL
    ↓
Physical Casing
    ↓
Controlled Sensor Environment
    ↓
Color Measurements
    ↓
EV3 Classification
```

A custom physical component that affects sensing behavior is therefore documented alongside the software and electronic configuration that depends on it.

This contributes directly to Piolín's reproducibility because the sensing environment can be reconstructed rather than being described only in text.

---

# 10.14 Sensor Mounting Components

All of Piolín's sensors depend on mechanical mounts that keep them oriented correctly relative to the chassis.

This is particularly important for:

```text
Front Ultrasonic
Right Ultrasonic
Left Ultrasonic
Color Sensor
HuskyLens
```

Each sensor observes a different region.

```text
                  HUSKYLENS
                      ↑
                Forward Vision

                FRONT US
                    ↑
               Front Distance


LEFT US ←       [ PIOLÍN ]       → RIGHT US


                COLOR SENSOR
                    ↓
                   Floor
```

The mounting components establish these sensing directions physically.

A correctly functioning sensor mounted at the wrong angle could still provide information that does not correspond correctly with the software model.

Sensor mounting is therefore part of Piolín's perception architecture.

---

# 10.15 Lateral Ultrasonic Mounting

Piolín's two lateral ultrasonic sensors are mounted facing toward opposite sides of the chassis.

Their measured mounting height is approximately:

```text
43 mm above the competition surface
```

The supports holding these sensors maintain their lateral orientation.

```text
LEFT WALL                         RIGHT WALL
    │                                 │
    │                                 │
    └──── S3 ← [ PIOLÍN ] → S2 ──────┘
```

This orientation supports the geometry used by Piolín's wall-navigation system.

The structural pieces holding the sensors are therefore part of the measurement system itself rather than merely decorative supports.

---

# 10.16 HuskyLens Mounting Structure

The HuskyLens is mounted on Piolín in a forward-facing position so that it can observe the traffic pillars used during the Obstacle Challenge.

<div align="center">
  <img
    width="358"
    height="358"
    alt="HuskyLens installed on Piolín"
    src="https://github.com/user-attachments/assets/b00dbb40-e32a-446d-83df-9d760912ccf6"
  />
  <br>
  <sub><b>Figure 10.1.</b> HuskyLens mounted on Piolín as part of the final vision subsystem.</sub>
</div>

The image above shows how the vision sensor is physically integrated into the robot rather than functioning as an external device.

The supporting structure maintains the camera position relative to the chassis and keeps its forward viewing region available.

```text
                 VISIBLE ENVIRONMENT
                         ▲
                        / \
                       /   \
                      /     \
                 [ HUSKYLENS ]
                       │
                       │
                 Mounting Frame
                       │
                       ▼
                    PIOLÍN
```

Because the HuskyLens is rigidly mounted to the robot, the camera rotates whenever the chassis rotates.

Therefore:

```text
ROBOT HEADING
      ↓
CAMERA HEADING
      ↓
VISIBLE REGION
```

The mechanical installation of the HuskyLens is consequently part of Piolín's vision geometry.

The mount must support the camera while avoiding unnecessary obstruction of its forward-facing observation region.

Detailed information about visual detection and the HuskyLens subsystem is documented in:

```text
docs/components/07_HuskyLens.md
```

---

# 10.17 Cable Routing

Piolín contains several cables connecting the EV3, motors, sensors, Arduino Nano, and vision subsystem.

Cable routing is important because the robot also contains moving mechanical assemblies.

The primary objective is to prevent cables from interfering with:

```text
Steering linkage
Front wheels
Rear wheels
Drivetrain
Sensor fields
```

The relationship can be represented as:

```text
ELECTRICAL CONNECTION
       ↓
Cable routing
       ↓
Secure path through chassis
       ↓
No interference with movement
```

Cable routing therefore belongs to both the electrical and mechanical design.

---

# 10.18 Why Cable Management Matters

A cable can be electrically correct but mechanically problematic.

For example:

```text
Loose cable
    ↓
Moves during steering
    ↓
Touches linkage or wheel
    ↓
Mechanical resistance
    ↓
Navigation changes
```

The resulting behavior may appear to be a software or motor-control issue even though the actual cause is mechanical interference.

Organizing the cables helps keep electrical connections stable and keeps moving mechanisms free.

This is especially important around Piolín's front steering assembly and the electronics mounted above the chassis.

---

# 10.19 Connectors

Connectors allow the major components to remain electrically modular.

The LEGO sensors and motors use the EV3 connection system, while the external vision subsystem uses its own electrical and communication connections.

The architecture can be separated into:

```text
LEGO DOMAIN

EV3
 ├── Motor A
 ├── Motor B
 ├── S1
 ├── S2
 ├── S3
 └── S4
```

and:

```text
VISION DOMAIN

HuskyLens
    ↓
Arduino Nano
    ↓
USB
    ↓
EV3
```

This modularity allows the responsibilities of individual components to remain clear within the complete vehicle architecture.

---

# 10.20 Mechanical Fastening

Piolín uses LEGO Technic connection elements and additional securing methods where necessary to hold hardware in place.

The objective of these components is:

```text
Component
    ↓
Secure attachment
    ↓
Stable orientation
    ↓
Repeatable system geometry
```

This is particularly important for sensing hardware.

A sensor whose mount changes orientation can begin observing a different region of the environment even though its electronic operation remains correct.

Mechanical fastening therefore supports sensor repeatability as well as structural integrity.

---

# 10.21 Component Placement

The location of each component influences more than the physical appearance of the robot.

For example:

```text
Battery / EV3 Position
        ↓
Mass Distribution


Sensor Position
        ↓
Perception Geometry


Motor Position
        ↓
Mechanical Transmission


Wheel Position
        ↓
Vehicle Geometry


Camera Position
        ↓
Field of View
```

The final Piolín architecture therefore treats component placement as an engineering decision rather than simply fitting parts wherever space is available.

The full robot measures approximately:

```text
Length = 210 mm

Width = 150 mm

Height = 230 mm
```

with a final measured mass of approximately:

```text
0.80476 kg
```

All supporting components must fit within and contribute to this complete vehicle architecture.

---

# 10.22 Supporting Components and Mass

Even relatively small components contribute to Piolín's total vehicle mass.

The final measured mass includes:

```text
EV3
Battery
Motors
Sensors
HuskyLens
Arduino Nano
Wheels
Tires
Technic Structure
Cables
Mounting Components
Custom Parts
```

The drivetrain must accelerate all of these components together.

Therefore, structural and supporting hardware influence the same propulsion system that moves the main electronic components.

This is one reason component placement and structural design are considered at the system level rather than individually.

---

# 10.23 Mechanical Integration

Supporting components connect Piolín's main subsystems into one physical vehicle.

Without mechanical integration, the robot would consist of separate functional modules:

```text
Controller

Motors

Sensors

Vision

Battery
```

The chassis and supporting components transform those modules into:

```text
                     PIOLÍN
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
     SENSING          CONTROL        ACTUATION
        │               │               │
        └───────────────┼───────────────┘
                        ▼
                  ONE VEHICLE
```

This integration allows information measured at one physical position on the chassis to result in predictable movement through an actuator mounted elsewhere on the robot.

---

# 10.24 Supporting Components and Reproducibility

Documenting only the EV3, motors, and sensors would not be enough for another team to understand how Piolín was constructed.

Reproducing the robot also requires information about:

```text
Wheel sizes
Sensor orientation
Structural arrangement
Custom casing
Controller placement
Vision subsystem
Connections
Cable routing
```

This is why supporting components are included in the repository rather than being treated as visually unimportant pieces.

The component files explain **what hardware is used**, while the reproducibility section explains **how those components are connected and assembled into the complete robot**.

---

# 10.25 Supporting Hardware Responsibility Matrix

The final supporting hardware can be summarized as:

| Component | Electrical Role | Mechanical Role | Software Role |
| :--- | :---: | :---: | :---: |
| **Arduino Nano** | Communication interface | Mounted to chassis | Transfers vision information |
| **USB Connection** | Data connection | Routed through chassis | Nano-EV3 communication |
| **Technic Beams** | None | Structural frame | None |
| **Technic Axles** | None | Transfer rotation | None |
| **Front Wheels** | None | Steering / rolling | Influences motion geometry |
| **Rear Wheels** | None | Propulsion / rolling | Related to encoder-distance model |
| **Tires** | None | Traction | Influences physical response |
| **Color Sensor Casing** | None | Optical isolation | Improves sensing environment |
| **Sensor Mounts** | None | Maintain orientation | Preserve sensor geometry |
| **HuskyLens Mount** | None | Maintains camera position | Preserves vision geometry |
| **Cable Routing Elements** | Supports connections | Prevent interference | None |

The table demonstrates that a component does not need to contain electronics to influence autonomous behavior.

---

# 10.26 Relationship With the Complete Piolín Architecture

The supporting components can be placed around the primary systems as follows:

```text
                         PIOLÍN
                            │
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
          CONTROL        PERCEPTION      ACTUATION
             │              │              │
            EV3         Ultrasonic       Motor A
                         Color           Motor B
                       HuskyLens
             │              │              │
             └──────────────┼──────────────┘
                            ▼
                    SUPPORTING HARDWARE
                            │
          ┌─────────────────┼─────────────────┐
          ▼                 ▼                 ▼
    Arduino Nano       LEGO Structure     Wheels / Tires
         USB           Sensor Mounts      Axles / Linkage
                            │
                            ▼
                    Custom Components
                            │
                            ▼
                 Color Sensor Casing
```

The supporting hardware therefore does not exist separately from the main robot architecture.

It enables the main subsystems to remain mechanically connected, electrically organized, and physically aligned.

---

# 10.27 Engineering Philosophy

Piolín's final hardware design follows a simple principle:

> **Every component should have a defined responsibility.**

For the primary hardware:

```text
EV3
    → Main control

Motor A
    → Propulsion

Motor B
    → Steering

Ultrasonic Sensors
    → Distance / geometry

Color Sensor
    → Course-state information

HuskyLens
    → Obstacle identity
```

For the supporting hardware:

```text
Arduino Nano
    → Vision communication

Technic Structure
    → Mechanical support

Wheels
    → Vehicle-floor interaction

Sensor Mounts
    → Perception geometry

HuskyLens Mount
    → Vision geometry

Color Sensor Casing
    → Optical isolation

Cables / Connectors
    → Electrical integration
```

This avoids adding parts without a clear reason and makes the final robot easier to understand as an engineering system.

---

# 10.28 Current vs. Legacy Supporting Hardware

Piolín's hardware architecture changed significantly during development.

Some components and configurations explored during earlier phases are no longer part of the final robot.

These previous systems are preserved separately in:

```text
docs/legacy/
```

This separation is important because older hardware may appear in development photographs, experiments, or source files without representing the current configuration.

The final supporting architecture described in this section reflects Piolín's current WRO Future Engineers 2026 configuration.

---

# 10.29 Component Documentation Structure

The complete current hardware documentation is organized as:

```text
docs/components/

01_Hardwareoverview.md
        ↓
Complete hardware architecture

02_EV3.md
        ↓
Main controller

03_Motors.md
        ↓
Actuation system

04_SteeringMotor.md
        ↓
Steering actuator and Ackermann interface

05_UltrasonicSensors.md
        ↓
Three-sensor distance architecture

06_ColorSensor.md
        ↓
Floor sensing and course-state detection

07_HuskyLens.md
        ↓
Vision subsystem

08_Battery.md
        ↓
Main energy source

09_PowerDistribution.md
        ↓
Electrical distribution architecture

10_OtherComponents.md
        ↓
Supporting electronics and mechanical hardware
```

Together, these files describe Piolín's complete current hardware configuration without mixing the final system with obsolete development components.

---

# 10.30 Final Supporting Hardware Summary

Piolín's autonomous behavior depends on more than its main electronic devices.

The final robot also relies on a collection of supporting components that connect the electrical, mechanical, sensing, and control systems into one vehicle.

The most important supporting elements include:

```text
ARDUINO NANO
      ↓
Vision communication


LEGO TECHNIC STRUCTURE
      ↓
Mechanical framework


AXLES + LINKAGES
      ↓
Motion transmission


FRONT + REAR WHEELS
      ↓
Vehicle movement


HUSKYLENS MOUNT
      ↓
Stable forward vision


COLOR SENSOR CASING
      ↓
Optical isolation


SENSOR MOUNTS
      ↓
Stable perception geometry


CABLES + CONNECTORS
      ↓
Electrical integration
```

Piolín's final wheel configuration uses approximately **61.0 mm rear propulsion wheels** and **38.1 mm front steering wheels**.

The Arduino Nano provides the communication bridge used by the HuskyLens vision subsystem, while the EV3 remains the main controller.

The LEGO Technic structure maintains the geometry between the drivetrain, steering system, sensors, camera, and electronic components.

The HuskyLens mounting structure shown in **Figure 10.1** demonstrates how a sensing component becomes part of the robot's mechanical geometry once it is physically integrated into the chassis.

The custom color-sensor casing similarly demonstrates how a relatively simple mechanical component can directly improve the environment in which a sensor operates.

The final engineering concept can therefore be summarized as:

> **The main components provide Piolín's core functions.**

> **The supporting components make those functions physically possible, mechanically stable, electrically connected, and reproducible.**

With this section, the `docs/components/` directory documents the complete current hardware architecture of Piolín before the repository moves into the more detailed mobility, sensing, software, systems-engineering, and reproducibility documentation.
