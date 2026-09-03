
<div align="center">
  <img src="https://github.com/user-attachments/assets/839b917a-c2bc-4053-8b2a-f68e43b7efa0"
       alt="Piolin hardware evolution"
       style="max-width: 65%; height: auto;" />
</div>

# 2. Robot Hardware and Components

Piolín's final WRO Future Engineers 2026 hardware architecture is centered around the **LEGO Mindstorms EV3 Intelligent Brick**.

The current design is the result of several hardware iterations in which different processors, sensors, vision systems, and drivetrain configurations were tested. The final architecture was selected primarily for **reliability, simplicity, compatibility, and repeatable competition performance**.

Earlier systems such as the Raspberry Pi, PixyCam, Arduino Mega, additional ultrasonic sensors, and experimental motor-control electronics are part of Piolín's development history, but they are **not part of the final competition configuration**.

> [!IMPORTANT]
> The components described in Sections 2.1–2.6 represent the **final 2026 Piolín configuration**.  
> Previous or rejected hardware architectures are documented separately in the Hardware Evolution section.

---

## 2.1 Final Hardware Architecture

The final robot combines the EV3's native motor and sensor ecosystem with an independent computer-vision subsystem based on the HuskyLens and Arduino Nano.

| System | Final Component | Connection | Primary Function |
| :--- | :--- | :--- | :--- |
| **Main Controller** | LEGO Mindstorms EV3 Intelligent Brick | Central unit | Executes the robot's autonomous navigation and motor-control software. |
| **Drive System** | EV3 Drive Motor | Port A | Provides propulsion to the drivetrain. |
| **Steering System** | EV3 Steering Motor | Port B | Controls the front Ackermann steering mechanism. |
| **Right Distance Sensor** | LEGO Ultrasonic Sensor | Port S2 | Measures the distance between Piolín and the right-side track wall. |
| **Left Distance Sensor** | LEGO Ultrasonic Sensor | Port S3 | Measures the distance between Piolín and the left-side track wall. |
| **Floor Detection** | LEGO Color Sensor | Port S4 | Detects blue and orange floor markings for direction and lap tracking. |
| **Vision Sensor** | HuskyLens | Arduino Nano | Detects colored obstacles during the Obstacle Challenge. |
| **Vision Interface** | Arduino Nano | USB → EV3 | Transfers processed HuskyLens information to the EV3. |
| **Front Distance Sensor**| LEGO Ultrasonic Sensor | Port S1 | Measures the distance between Piolín and the front-side track |

This architecture deliberately keeps the **Open Challenge navigation system independent from the vision system**.

The Open Challenge can operate using:

- two lateral ultrasonic sensors,
- a front ultrasonic sensor,
- one color sensor,
- drive motor,
- steering motor,
- and the EV3 controller.

The HuskyLens and Arduino Nano become relevant primarily during the **Obstacle Challenge**.

---

## 2.2 LEGO Mindstorms EV3 Intelligent Brick

### Component: LEGO EV3 Brick

- **Quantity:** 1
- **Role:** Main robot controller
- **Motor Connections:** Ports A and B
- **Sensor Connections:** Ports S2, S3, and S4
- **Software Environment:** Python / Pybricks

<div align="center">
  <img src="https://github.com/user-attachments/assets/ab7c39a9-6f0e-4c9d-aee2-8d59c25d3adc"
       alt="LEGO EV3 Intelligent Brick"
       style="max-width: 30%; height: auto; border-radius: 8px; margin: 10px 0;" />
</div>

The **EV3 Intelligent Brick is the primary processing unit of Piolín**.

It is responsible for:

- reading both ultrasonic sensors,
- reading and validating floor-color detections,
- determining the driving direction,
- identifying the inner and outer track walls,
- executing straight-line navigation,
- detecting corner transitions,
- controlling the steering motor,
- controlling the drive motor,
- tracking progress through the course,
- and receiving obstacle information from the Arduino Nano when required.

A major advantage of keeping the EV3 as the main controller is that the motors and primary navigation sensors can communicate directly with the same hardware platform.

This reduces the number of intermediate electronic interfaces required for basic movement.

---

## 2.3 Ultrasonic Navigation Sensors

### Component: LEGO Ultrasonic Sensor

- **Quantity:** 2
- **Right Sensor:** EV3 Port S2
- **Left Sensor:** EV3 Port S3
- **Mounting Orientation:** Lateral
- **Measured Height Above Floor:** approximately **1.7 in / 43 mm**

<div align="center">
  <img src="https://github.com/user-attachments/assets/b8872f62-adb5-4fd1-98fb-18491c57de56"
       alt="Ultrasonic sensor"
       style="max-width: 30%; height: auto; border-radius: 8px; margin: 10px 0;" />
</div>

Unlike previous Piolín prototypes, the final robot does **not** use a front ultrasonic sensor.

Instead, two ultrasonic sensors are mounted laterally:

```text
           Direction of travel
                   ↑

        LEFT US ← [ PIOLÍN ] → RIGHT US
                     ↑
                  front
````

Each sensor observes one side of the track.

This arrangement allows the software to assign the sensors dynamically according to the robot's driving direction:

### Counterclockwise Navigation

* Left sensor → inner wall
* Right sensor → outer wall

### Clockwise Navigation

* Right sensor → inner wall
* Left sensor → outer wall

The role of each ultrasonic sensor also changes during a corner.

During a straight section, the **inner sensor provides the primary wall-following reference**, while the outer sensor contributes additional geometric and collision-safety information.

When the inner wall disappears at a corner, that large distance measurement is interpreted as a **change in track geometry**, not simply as a wall-following error.

During the turn, the outer wall becomes a more useful temporary reference until the inner wall becomes visible again.

This sensor interpretation forms the basis of Piolín's final Open Challenge navigation strategy.

---

## 2.4 LEGO Color Sensor

### Component: LEGO Color Sensor

* **Quantity:** 1
* **Connection:** EV3 Port S4
* **Orientation:** Downward-facing
* **Primary Detected Markings:** Blue and Orange

<div align="center">
  <img src="https://github.com/user-attachments/assets/5e59f3a1-5b7c-4992-9d57-07951f412e67"
       alt="LEGO Color Sensor"
       style="max-width: 30%; height: auto; border-radius: 8px; margin: 10px 0;" />
</div>

The color sensor does **not control Piolín's steering directly**.

Instead, it has two specific navigation responsibilities.

### 1. Determine Initial Direction

The first valid floor marking establishes the direction of travel:

| First Detected Color | Direction        |
| :------------------- | :--------------- |
| **Blue**             | Counterclockwise |
| **Orange**           | Clockwise        |

Once the direction has been established, the software can determine which ultrasonic sensor corresponds to the inner and outer walls.

### 2. Track Course Progress

Each corner contains both a blue and an orange floor marking.

With four corners per lap and three required laps:

**4 corners/laps x 3 laps = 12 corners**
Therefore, across three laps Piolín expects:

* **12 valid blue detections**
* **12 valid orange detections**

The software includes detection-locking logic to prevent the same physical strip from being counted repeatedly while the sensor remains above it.

---

## 2.5 HuskyLens Vision System

### Component: HuskyLens AI Vision Sensor

* **Quantity:** 1
* **Primary Challenge:** Obstacle Challenge
* **Interface:** Connected through the Arduino Nano
* **Role:** Colored obstacle recognition

<div align="center">
  <img src="https://github.com/user-attachments/assets/737bd86d-a82a-46fa-b683-06f18ec4721b"
       alt="HuskyLens vision sensor"
       style="max-width: 30%; height: auto; border-radius: 8px; margin: 10px 0;" />
</div>

The **HuskyLens is Piolín's final computer-vision sensor**.

It is used primarily during the Obstacle Challenge to identify colored traffic pillars and provide visual information that cannot be obtained from the ultrasonic sensors alone.

The HuskyLens performs its own image-processing operations internally. This reduces the amount of raw image processing that must be performed by the EV3.

The final architecture intentionally separates:

```text
DISTANCE / TRACK NAVIGATION
        ↓
2 Ultrasonic Sensors + EV3

FLOOR POSITION TRACKING
        ↓
Color Sensor + EV3

OBJECT RECOGNITION
        ↓
HuskyLens + Arduino Nano
```

This modular division makes it possible to test each sensing system independently.

---

## 2.6 Arduino Nano Vision Interface

### Component: Arduino Nano

* **Quantity:** 1
* **Primary Function:** HuskyLens communication interface
* **Connection to EV3:** USB
* **Role in Open Challenge:** Not required for wall navigation
* **Role in Obstacle Challenge:** Transfers vision information to the EV3

The Arduino Nano is **not Piolín's main controller**.

This distinction is important.

The EV3 remains responsible for:

* navigation,
* steering,
* propulsion,
* ultrasonic processing,
* color processing,
* and overall autonomous behavior.

The Nano performs a specialized role between the HuskyLens and the EV3:

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

The Nano receives the relevant visual detections and converts them into information that the EV3 navigation software can use.

This architecture allows Piolín to use the HuskyLens without replacing the EV3 as the primary vehicle controller.

---

## 2.7 Drive and Steering System

Piolín uses two independent EV3-controlled actuation functions.

### Drive Motor

* **Connection:** Port A
* **Function:** Vehicle propulsion

The drive motor provides the forward motion required for both competition challenges.

### Steering Motor

* **Connection:** Port B
* **Function:** Front steering control

The steering motor operates Piolín's **Ackermann-style steering mechanism**.

Unlike differential-drive robots, Piolín changes direction by physically changing the angle of its front wheels.

This produces vehicle-like cornering and allows the rear drivetrain to remain dedicated to propulsion.

The final wheel configuration uses:

| Wheel Position   |       Diameter      |
| :--------------- | :-----------------: |
| **Rear wheels**  | **2.4 in / ~61 mm** |
| **Front wheels** | **1.5 in / ~38 mm** |

Detailed mechanical steering geometry and Ackermann calculations are documented separately in the mobility section.

---

## 2.8 Final Hardware Connection Map

The complete active architecture can be summarized as:

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
│   Port S1 ───────────── Unused                      │
│   Port S2 ───────────── Right Ultrasonic            │
│   Port S3 ───────────── Left Ultrasonic             │
│   Port S4 ───────────── Color Sensor                │
│                                                     │
└─────────────────────────────────────────────────────┘
```

This diagram represents the **final Piolín 2026 competition hardware architecture**.

---

# 2.9 Hardware Evolution

Piolín's final configuration was reached through several experimental architectures.

Rather than hiding these unsuccessful or temporary designs, they are documented because they influenced important engineering decisions.

| Development Stage                                | Main Architecture                                        | Result / Engineering Lesson                                                                                                |
| :----------------------------------------------- | :------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------- |
| **Early EV3 Prototype**                          | EV3 + LEGO drivetrain                                    | Established the basic autonomous vehicle platform, but revealed chassis rigidity and steering consistency problems.        |
| **Structural Reinforcement**                     | EV3 + reinforced LEGO/SPIKE structure                    | Reduced chassis deformation and improved mechanical repeatability.                                                         |
| **PixyCam Experiments**                          | EV3 + PixyCam                                            | Demonstrated the usefulness of color-based computer vision, but was later replaced by the HuskyLens vision architecture.   |
| **Raspberry Pi Experiments**                     | Raspberry Pi-based processing                            | Increased processing flexibility but introduced additional power, integration, and reliability complexity.                 |
| **Arduino Mega / Hybrid Electronics Experiment** | Arduino-based controller + external motor electronics    | Tested a non-EV3 control architecture, but added hardware complexity and was not selected as the final competition system. |
| **Gyroscope Navigation Experiment**              | EV3 + Gyroscope + 2 US                                   | Tested heading-controlled 90° corner navigation, but the gyro was removed from the final sensor configuration.             |
| **Final 2026 Architecture**                      | **EV3 + 2 lateral US + Color Sensor + Nano + HuskyLens** | Selected for its balance of simplicity, compatibility, sensor coverage, and reliability.                                   |

---

## 2.10 Key Engineering Decision

The most important hardware decision in Piolín's development was to avoid replacing the EV3 simply because a more computationally powerful controller was available.

The final architecture instead assigns each processor a specific responsibility:

### EV3

**Vehicle control and navigation**

### Arduino Nano

**Vision communication interface**

### HuskyLens

**Dedicated visual recognition**

This avoids forcing one controller to perform every function while also avoiding unnecessary duplication of the robot's basic motor and sensor systems.

The resulting architecture is simpler than several earlier prototypes and corresponds directly to the hardware installed on the final Piolín robot.

> [!NOTE]
> Legacy components remain documented as engineering evidence, but they should never be interpreted as active parts of the final 2026 competition configuration.
