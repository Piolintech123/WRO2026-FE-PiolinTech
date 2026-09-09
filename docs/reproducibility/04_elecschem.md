# 4. Electrical Schematic and System Architecture

<div align="center">

<img
  src="../../v-photos/v4/ev3_installed.jpg"
  alt="LEGO Mindstorms EV3 Brick installed as Piolín's central electrical controller"
  width="700"
/>

<br>

<sub><b>Figure 4.1.</b> The EV3 Brick is the central electrical node of Piolín, distributing battery power and providing the interfaces used by the motors and sensors.</sub>

</div>

Piolín's electrical architecture is centered around a single **LEGO Mindstorms EV3 Brick** powered by the official **EV3 Rechargeable DC Battery 45501**. The EV3 acts simultaneously as the main controller, motor interface, sensor interface, and power-distribution point for the current competition robot.

The architecture was deliberately simplified so that Piolín does not require a separate motor controller, external propulsion battery, Arduino-based communication layer, or permanent external power converter.

At the highest level:

```text
                 EV3 BATTERY 45501
                        │
                        ▼
                 ┌─────────────┐
                 │  EV3 BRICK  │
                 └──────┬──────┘
                        │
          ┌─────────────┴─────────────┐
          │                           │
          ▼                           ▼
     MOTOR OUTPUTS               SENSOR PORTS
          │                           │
       A / B                      S1–S4
```

The same central electrical platform is used in both WRO Future Engineers challenges. Only the device connected to **Sensor Port S1** changes.

---

## 4.1 Electrical Architecture at a Glance

Piolín has two competition configurations built around one common electrical base.

| Interface | Open Challenge | Obstacle Challenge |
| :---: | :--- | :--- |
| Battery | EV3 Rechargeable Battery 45501 | EV3 Rechargeable Battery 45501 |
| Controller | EV3 Brick | EV3 Brick |
| Motor A | EV3 Large Motor | EV3 Large Motor |
| Motor B | EV3 Medium Motor | EV3 Medium Motor |
| S1 | EV3 Gyro Sensor | Pixy2.1 |
| S2 | Left EV3 Ultrasonic Sensor | Left EV3 Ultrasonic Sensor |
| S3 | Right EV3 Ultrasonic Sensor | Right EV3 Ultrasonic Sensor |
| S4 | EV3 Color Sensor | EV3 Color Sensor |
| Motor C | Unused | Unused |
| Motor D | Unused | Unused |

The permanent electrical convention is:

```text
A  = propulsion

B  = steering

S2 = left ultrasonic

S3 = right ultrasonic

S4 = Color Sensor
```

and the only round-specific electrical connection is:

```text
OPEN
S1 = Gyro
```

```text
OBSTACLES
S1 = Pixy2.1
```

The Gyro Sensor and Pixy2.1 are not connected simultaneously in the current architecture.

---

## 4.2 Main Power Source

<div align="center">

<img
  src="../../v-photos/v4/ev3_battery_45501.jpg"
  alt="LEGO Mindstorms EV3 Rechargeable DC Battery 45501 used by Piolín"
  width="640"
/>

<br>

<sub><b>Figure 4.2.</b> Piolín's main electrical power source is the LEGO Mindstorms EV3 Rechargeable DC Battery 45501.</sub>

</div>

The battery is installed directly into the EV3 Brick. From there, the EV3 supplies the electrical interfaces used by the rest of the active robot.

The current power architecture can be represented as:

```text
             EV3 BATTERY 45501
                    │
                    ▼
               EV3 BRICK
                    │
       ┌────────────┼────────────┐
       │            │            │
       ▼            ▼            ▼
    Motor A      Motor B      Sensors
```

Piolín does not currently use a separate propulsion battery or a dedicated battery for the camera.

There is also no permanent current architecture involving:

```text
external buck converter

Arduino Nano power rail

external motor driver

separate camera battery
```

This reduces the number of power connections and potential electrical failure points.

---

## 4.3 EV3 as the Central Distribution Point

<div align="center">

<img
  src="../../v-photos/v4/ev3_motor_ports.jpg"
  alt="Piolín EV3 motor output ports"
  width="660"
/>

<br>

<sub><b>Figure 4.3.</b> Motor Ports A and B provide the electrical interfaces for propulsion and steering.</sub>

</div>

<div align="center">

<img
  src="../../v-photos/v4/ev3_sensor_ports.jpg"
  alt="Piolín EV3 sensor input ports"
  width="660"
/>

<br>

<sub><b>Figure 4.4.</b> Sensor Ports S1–S4 form Piolín's complete active sensing interface.</sub>

</div>

The EV3 separates its external connections into two functional groups.

```text
MOTOR PORTS
A B C D
```

are used for actuators, while:

```text
SENSOR PORTS
S1 S2 S3 S4
```

are used for perception.

Piolín only requires:

```text
Motor A

Motor B

S1

S2

S3

S4
```

Ports C and D remain unused.

This gives the electrical system a clear one-to-one relationship between hardware responsibility and EV3 interface.

---

## 4.4 Motor Output Circuit

The actuator side of the electrical architecture does not change between rounds.

```text
                        EV3
                         │
                ┌────────┴────────┐
                │                 │
                ▼                 ▼
             PORT A            PORT B
                │                 │
                ▼                 ▼
         EV3 Large Motor   EV3 Medium Motor
                │                 │
                ▼                 ▼
          PROPULSION          STEERING
```

### Motor A

<div align="center">

<img
  src="../../v-photos/v4/motor_a_large_drive.jpg"
  alt="EV3 Large Motor used as Piolín Motor A"
  width="620"
/>

<br>

<sub><b>Figure 4.5.</b> Motor A receives its command and electrical supply through EV3 Motor Port A.</sub>

</div>

Motor A drives the rear propulsion system.

Its electrical connection supports bidirectional motor operation so that the software can command:

```text
forward

stop

reverse
```

without additional external motor-control electronics.

### Motor B

<div align="center">

<img
  src="../../v-photos/v4/motor_b_medium_steering.jpg"
  alt="EV3 Medium Motor used as Piolín Motor B"
  width="620"
/>

<br>

<sub><b>Figure 4.6.</b> Motor B receives its steering commands through EV3 Motor Port B.</sub>

</div>

Motor B controls the front Ackermann-style steering mechanism.

The electrical interface remains the same even though the requested steering position changes continuously during navigation.

---

## 4.5 Permanent Sensor Circuit

Three sensor connections remain identical in both competition rounds:

```text
                    EV3
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
       S2           S3           S4
        │            │            │
        ▼            ▼            ▼
     LEFT US      RIGHT US      COLOR
```

The mapping is physically fixed:

```text
S2 → LEFT Ultrasonic Sensor

S3 → RIGHT Ultrasonic Sensor

S4 → Color Sensor
```

<div align="center">

<img
  src="../../v-photos/v4/PiolinUSlabeling.png"
  alt="Piolín S2 left and S3 right ultrasonic sensor mapping"
  width="690"
/>

<br>

<sub><b>Figure 4.7.</b> The ultrasonic sensors retain a permanent physical left/right electrical identity.</sub>

</div>

This means clockwise and counterclockwise driving do not require any electrical rewiring.

Only the software interpretation of:

```text
inner side

outer side
```

changes.

---

## 4.6 Open Challenge Electrical Schematic

<div align="center">

<img
  src="../../v-photos/v4/wiring_open.jpg"
  alt="Piolín Open Challenge electrical wiring"
  width="740"
/>

<br>

<sub><b>Figure 4.8.</b> Physical wiring reference for the current Open Challenge configuration.</sub>

</div>

The Open electrical architecture is:

```text
                       EV3 BATTERY 45501
                              │
                              ▼
                         ┌─────────┐
                         │   EV3   │
                         └────┬────┘
                              │
       ┌──────────────────────┼────────────────────────┐
       │                      │                        │
       ▼                      ▼                        ▼
  MOTOR PORTS             SENSOR PORTS            EV3 CONTROL
       │                      │
   ┌───┴───┐        ┌─────────┼─────────┬─────────┐
   │       │        │         │         │         │
   ▼       ▼        ▼         ▼         ▼         ▼
   A       B        S1        S2        S3        S4
   │       │        │         │         │         │
   ▼       ▼        ▼         ▼         ▼         ▼
 Large   Medium    Gyro      Left      Right     Color
 Motor   Motor               US         US      Sensor
   │       │
   ▼       ▼
 Drive   Steering
```

The Open configuration therefore contains:

```text
A  → Large Motor

B  → Medium Motor

S1 → Gyro

S2 → Left Ultrasonic

S3 → Right Ultrasonic

S4 → Color Sensor
```

All active sensors in this round are LEGO Mindstorms EV3 devices.

---

## 4.7 Gyro Electrical Role in Open

<div align="center">

<img
  src="../../v-photos/v4/s1_open_gyro.jpg"
  alt="Piolín Gyro Sensor connected to S1 during Open"
  width="650"
/>

<br>

<sub><b>Figure 4.9.</b> The EV3 Gyro Sensor is the round-specific S1 device during the Open Challenge.</sub>

</div>

Electrically, the Gyro Sensor connects directly to S1 through the normal EV3 sensor interface.

The sensor supplies orientation information to the EV3 while the EV3 software uses that information to influence Motor B.

The complete control path is:

```text
vehicle rotation
      ↓
Gyro S1
      ↓
EV3
      ↓
steering calculation
      ↓
Motor B
```

The gyro does not require a separate power source or intermediate controller in the current Open configuration.

---

## 4.8 Obstacle Challenge Electrical Schematic

<div align="center">

<img
  src="../../v-photos/v4/wiring_obstacle.jpg"
  alt="Piolín Obstacle Challenge electrical wiring"
  width="740"
/>

<br>

<sub><b>Figure 4.10.</b> Physical wiring reference for the current Obstacle Challenge configuration.</sub>

</div>

During the Obstacle Challenge, the complete electrical structure becomes:

```text
                       EV3 BATTERY 45501
                              │
                              ▼
                         ┌─────────┐
                         │   EV3   │
                         └────┬────┘
                              │
       ┌──────────────────────┼────────────────────────┐
       │                      │                        │
       ▼                      ▼                        ▼
  MOTOR PORTS             SENSOR PORTS            EV3 CONTROL
       │                      │
   ┌───┴───┐        ┌─────────┼─────────┬─────────┐
   │       │        │         │         │         │
   ▼       ▼        ▼         ▼         ▼         ▼
   A       B        S1        S2        S3        S4
   │       │        │         │         │         │
   ▼       ▼        ▼         ▼         ▼         ▼
 Large   Medium   Pixy2.1    Left      Right     Color
 Motor   Motor               US         US      Sensor
   │       │
   ▼       ▼
 Drive   Steering
```

The only electrical sensor change from Open is:

```text
S1

Gyro
  ↓
replaced by
  ↓
Pixy2.1
```

The motor wiring and S2/S3/S4 connections remain unchanged.

---

## 4.9 Pixy2.1 Electrical Interface

<div align="center">

<img
  src="../../v-photos/v4/pixy21_s1_connection.jpg"
  alt="Pixy2.1 connected to EV3 Sensor Port S1"
  width="680"
/>

<br>

<sub><b>Figure 4.11.</b> Pixy2.1 connects directly to Piolín's EV3 through the current S1 interface.</sub>

</div>

Piolín's current camera architecture removes the intermediate Arduino-based communication layer used during earlier experiments.

The current path is:

```text
Pixy2.1
    │
    │  data + active device connection
    ▼
Sensor Port S1
    │
    ▼
EV3
```

The current obstacle software accesses Pixy2.1 using an **I2C/SMBus communication path**.

The same physical S1 connection is part of the current camera interface and provides the active connection used by the vision system.

<div align="center">

<img
  src="../../v-photos/v4/pixy21_connection_cable.jpg"
  alt="Current Pixy2.1 connection cable used by Piolín"
  width="670"
/>

<br>

<sub><b>Figure 4.12.</b> Actual cable used for Piolín's current direct Pixy2.1 integration.</sub>

</div>

This document deliberately does **not** provide an invented conductor-by-conductor pinout for this cable.

A true pin-level electrical diagram should only be added after the exact current cable and connector mapping are verified.

The reproducible fact currently supported by the vehicle is:

```text
Pixy2.1
→ current connection cable
→ EV3 S1
→ I2C/SMBus communication
```

---

## 4.10 Pixy2.1 Casing and Electrical Integration

The current Pixy2.1 installation includes a **3D-printed casing**.

The casing has no separate electrical circuit and requires no independent power connection.

Its relationship to the electrical subsystem is indirect but important:

```text
3D casing
    ↓
stabilizes / protects camera installation
    ↓
camera orientation remains more repeatable
    ↓
electrical sensor data retains consistent physical meaning
```

The casing should therefore be treated as part of the current Pixy installation even though it is not represented as a separate branch in the electrical schematic.

The camera should remain connected and calibrated in the same physical casing configuration used during testing.

---

## 4.11 Signal and Power Responsibilities

At system level, it is useful to distinguish between **power flow**, **sensor information**, and **actuator commands**.

### Power flow

```text
EV3 Battery 45501
      ↓
EV3
      ↓
active motors and sensors
```

### Sensor information

```text
SENSORS
   ↓
EV3
```

### Actuator commands

```text
EV3
 ↓
Motor A / Motor B
```

The complete closed-loop relationship is:

```text
             PHYSICAL ENVIRONMENT
                      │
                      ▼
                   SENSORS
                      │
                      ▼
                     EV3
                      │
            ┌─────────┴─────────┐
            ▼                   ▼
         Motor A             Motor B
            │                   │
            ▼                   ▼
        PROPULSION           STEERING
            │                   │
            └─────────┬─────────┘
                      ▼
               VEHICLE MOVEMENT
                      │
                      ▼
             PHYSICAL ENVIRONMENT
```

The electrical system therefore supports the complete autonomous feedback loop.

---

## 4.12 Why the Current Electrical Architecture Is Simpler

Earlier Piolín vision development involved additional hardware and communication layers.

A previous architecture could be represented conceptually as:

```text
Vision Sensor
     ↓
Arduino Nano
     ↓
communication link
     ↓
EV3
```

The current Obstacle architecture is:

```text
Pixy2.1
     ↓
EV3 S1
```

Removing the intermediate controller reduces:

```text
extra wiring

extra firmware

extra power dependencies

communication failure points

hardware integration complexity
```

Likewise, the final current robot does not keep a permanent front ultrasonic sensor.

The available sensor interfaces are instead dedicated to:

```text
S1 → specialized round sensor

S2 → left geometry

S3 → right geometry

S4 → floor state
```

This creates a clearer electrical architecture in which every active connection has a defined responsibility.

---

## 4.13 No Separate External Power Subsystem

The current competition robot does not depend on an additional regulated external electrical system.

Specifically, the current architecture does not require:

```text
external drive battery

separate camera battery

permanent buck converter

Arduino Nano power rail

external motor controller
```

This is important for reproducibility because an engineer reconstructing current Piolín should not add legacy electrical hardware simply because it appears in historical development files.

The central power concept remains:

```text
ONE EV3 BATTERY
       ↓
ONE EV3 BRICK
       ↓
CURRENT ROBOT
```

---

## 4.14 Round Conversion at the Electrical Level

The electrical conversion between rounds should occur while Piolín is powered down.

### Open → Obstacles

```text
POWER OFF
   ↓
disconnect Gyro from S1
   ↓
install Pixy2.1 assembly
   ↓
connect Pixy2.1 to S1
   ↓
verify S2 / S3 / S4 unchanged
   ↓
POWER ON
   ↓
run Obstacle software
```

### Obstacles → Open

```text
POWER OFF
   ↓
disconnect Pixy2.1 from S1
   ↓
install Gyro
   ↓
connect Gyro to S1
   ↓
verify S2 / S3 / S4 unchanged
   ↓
POWER ON
   ↓
run Open software
```

The conversion should not require changes to Motor Ports A or B.

That stability is intentional and reduces the number of possible wiring errors introduced between competition rounds.

---

## 4.15 Electrical Verification Procedure

Before autonomous testing, the electrical architecture should be checked from the center outward.

```text
BATTERY
  ↓
EV3 powers correctly?
  ↓
MOTOR A detected / responsive?
  ↓
MOTOR B detected / responsive?
  ↓
correct S1 device?
  ↓
S2 left ultrasonic?
  ↓
S3 right ultrasonic?
  ↓
S4 Color Sensor?
```

For Open, confirm:

```text
S1 = Gyro

Pixy not connected
```

For Obstacles, confirm:

```text
S1 = Pixy2.1

Gyro not connected
```

A raw sensor communication test should be performed before full autonomous movement.

This prevents an electrical configuration error from being mistaken for a navigation-algorithm failure.

---

## 4.16 Electrical Failure Isolation

| Symptom | Electrical Layer to Check First |
| :--- | :--- |
| EV3 does not power correctly | Battery installation / EV3 |
| Motor A unavailable | Port A cable / Large Motor |
| Motor B unavailable | Port B cable / Medium Motor |
| Left distance unavailable | S2 connection |
| Right distance unavailable | S3 connection |
| Floor sensor unavailable | S4 connection |
| Gyro unavailable in Open | S1 connection / correct round hardware |
| Pixy unavailable in Obstacles | S1 connection / Pixy cable / software interface |
| Open software finds wrong S1 device | Pixy may still be installed |
| Obstacle software cannot access vision | Gyro may still occupy S1 |
| Intermittent camera behavior | S1 connection and cable seating |
| Sensor changes after mechanical work | Check mount before assuming electrical failure |
| Correct raw sensor values but wrong driving | Move diagnosis to software/control layer |

The useful troubleshooting sequence is:

```text
POWER
  ↓
CONNECTION
  ↓
DEVICE
  ↓
RAW SIGNAL
  ↓
SOFTWARE INTERPRETATION
  ↓
CONTROL
```

This prevents unrelated controller constants from being changed to solve an electrical problem.

---

## 4.17 What This Schematic Does Not Claim

This document is intentionally a **system-level electrical schematic**, not a fabricated PCB-level circuit diagram.

The current repository can accurately document:

```text
power source

EV3 controller

motor-port assignments

sensor-port assignments

round-specific S1 device

Pixy communication method

physical connection architecture
```

but it should not invent unverified details such as:

```text
exact internal EV3 rail voltages

exact current consumption of the complete V4 robot

custom Pixy conductor pinout

unverified cable wire colors

unverified internal adapter circuitry
```

If those details are needed later, they should be obtained from verified technical documentation or measured directly before being presented as part of Piolín's engineering record.

This distinction keeps the electrical documentation reproducible without creating false precision.

---

## 4.18 Current Electrical Architecture vs. Legacy

The authoritative current configurations are:

```text
OPEN

Battery 45501
   ↓
EV3

A  → Large Motor
B  → Medium Motor

S1 → Gyro
S2 → Left US
S3 → Right US
S4 → Color
```

and:

```text
OBSTACLES

Battery 45501
   ↓
EV3

A  → Large Motor
B  → Medium Motor

S1 → Pixy2.1
S2 → Left US
S3 → Right US
S4 → Color
```

The following are not part of the current competition electrical schematic:

```text
HuskyLens

Arduino Nano

front ultrasonic

external battery

permanent buck converter

legacy camera bridge
```

Those systems belong in the legacy documentation because they represent earlier engineering experiments rather than current reconstruction requirements.

---

## 4.19 Complete Current Electrical Schematic

The final system-level representation is:

```text
                              ┌──────────────────┐
                              │ EV3 BATTERY 45501│
                              └────────┬─────────┘
                                       │
                                       ▼
                              ┌──────────────────┐
                              │     EV3 BRICK    │
                              │                  │
                              │ CONTROL + POWER  │
                              └────────┬─────────┘
                                       │
                ┌──────────────────────┼──────────────────────┐
                │                                             │
                ▼                                             ▼
         MOTOR INTERFACES                              SENSOR INTERFACES
                │                                             │
         ┌──────┴──────┐                       ┌──────────────┼─────────────┐
         │             │                       │              │             │
         ▼             ▼                       ▼              ▼             ▼
      PORT A         PORT B                    S2             S3            S4
         │             │                       │              │             │
         ▼             ▼                       ▼              ▼             ▼
     Large Motor   Medium Motor             Left US        Right US       Color
         │             │
         ▼             ▼
      REAR DRIVE   FRONT STEERING


                                S1 — MODULAR
                                     │
                       ┌─────────────┴─────────────┐
                       │                           │
                       ▼                           ▼
                      OPEN                      OBSTACLES
                       │                           │
                       ▼                           ▼
                  EV3 Gyro                     Pixy2.1
                                                   │
                                             I2C / SMBus
                                             through current
                                             S1 interface
```

<div align="center">

<img
  src="../../v-photos/v4/piolin_obstacle_top.jpg"
  alt="Top view of Piolín showing the integrated current electrical and sensor architecture"
  width="720"
/>

<br>

<sub><b>Figure 4.13.</b> The current vehicle integrates all active electrical devices around one EV3 controller and one central battery system.</sub>

</div>

---

## 4.20 Final Engineering Assessment

Piolín's electrical architecture is designed around **centralization and controlled modularity**.

The EV3 Rechargeable Battery 45501 provides the main power source, while the EV3 Brick becomes the central interface between perception and actuation.

The permanent electrical structure is:

```text
A
→ rear propulsion

B
→ front steering

S2
→ left lateral sensing

S3
→ right lateral sensing

S4
→ floor sensing
```

Only S1 changes according to the information requirements of the active competition round:

```text
OPEN
→ Gyro orientation sensing
```

```text
OBSTACLES
→ Pixy2.1 visual perception
```

This decision avoids the need to power and communicate with every experimental sensor simultaneously. It also eliminates the current need for the Arduino Nano, HuskyLens, front ultrasonic sensor, external battery, and additional permanent power-conversion electronics used or considered during earlier development.

The Pixy2.1 camera uses Piolín's current direct S1 connection and is physically integrated with its 3D-printed casing. The casing does not add another electrical branch, but it remains part of the calibrated camera assembly.

The central design principle is:

> **Keep the electrical path as short and understandable as possible: one central battery, one main controller, two actuators, three permanent sensors, and one round-specific sensing interface.**

This architecture makes the current Piolín easier to reconstruct, verify, troubleshoot, and convert between WRO Future Engineers competition rounds without changing the fundamental vehicle electronics.

---

<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
