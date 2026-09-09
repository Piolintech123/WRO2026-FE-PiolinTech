# 9. Power Distribution and Electrical Integration

<div align="center">

<img
  src="../../v-photos/v4/wiring_open.jpg"
  alt="Piolín wiring in the Open Challenge configuration"
  width="720"
/>

<br>

<sub><b>Figure 9.1.</b> Current Piolín wiring in the Open Challenge configuration, where S1 is assigned to the EV3 Gyro Sensor.</sub>

</div>

Piolín uses a deliberately simple electrical architecture centered around the **LEGO Mindstorms EV3 Intelligent Brick** and its **LEGO EV3 Rechargeable DC Battery 45501**.

The EV3 acts as both:

```text
main controller
```

and:

```text
central electrical interface
```

for the current competition vehicle.

The current architecture avoids unnecessary external power electronics, secondary motor controllers, external vehicle batteries, or additional microcontrollers.

Instead, Piolín uses one common EV3 platform whose S1 device changes according to the competition round.

```text
OPEN
S1 = EV3 Gyro Sensor


OBSTACLES
S1 = Pixy2.1
```

The rest of the principal electrical architecture remains unchanged.

---

## 9.1 Electrical Architecture Overview

The current common platform contains:

```text
EV3 Rechargeable Battery 45501
            ↓
      EV3 Intelligent Brick
            │
    ┌───────┼───────┐
    │       │       │
    ▼       ▼       ▼
 MOTORS   SENSORS   CONTROL
```

The permanent motor assignments are:

```text
A
→ EV3 Large Motor
→ rear propulsion


B
→ EV3 Medium Motor
→ front steering
```

The permanent sensor assignments are:

```text
S2
→ LEFT Ultrasonic Sensor


S3
→ RIGHT Ultrasonic Sensor


S4
→ Color Sensor
```

S1 is modular:

```text
S1
├── Open      → Gyro Sensor
└── Obstacles → Pixy2.1
```

This gives Piolín one common electrical base with minimal reconfiguration between competition rounds.

---

# 9.2 Primary Power Source

Piolín's primary power source is:

```text
LEGO Mindstorms EV3 Rechargeable DC Battery
Part 45501
```

<div align="center">

<img
  src="../../v-photos/v4/ev3_battery_45501.jpg"
  alt="LEGO Mindstorms EV3 Rechargeable DC Battery 45501 used by Piolín"
  width="650"
/>

<br>

<sub><b>Figure 9.2.</b> EV3 Rechargeable DC Battery 45501 used as the primary power source for Piolín's current competition platform.</sub>

</div>

The battery is integrated directly into the EV3 Brick.

This simplifies the vehicle because the primary LEGO electronics are already designed around the same controller ecosystem.

The current robot does not require:

```text
external propulsion battery

separate steering battery

separate camera battery

external motor driver

custom power distribution board
```

for its competition architecture.

---

# 9.3 Why Power Is Centralized Through the EV3

Most of Piolín's active components are LEGO Mindstorms EV3 hardware.

These include:

```text
Large Motor

Medium Motor

two Ultrasonic Sensors

Color Sensor

Gyro Sensor during Open
```

Keeping these components on their native EV3 interfaces eliminates the need to build additional conversion electronics for the main vehicle systems.

The electrical philosophy is therefore:

```text
native EV3 component
→ use native EV3 interface
```

whenever practical.

This improves:

```text
simplicity

fault isolation

cable management

competition preparation

reproducibility
```

---

# 9.4 Power Path vs. Signal Path

Power and communication are related but should not be treated as the same concept.

A useful distinction is:

```text
POWER PATH
→ provides electrical energy


SIGNAL PATH
→ transfers information or control commands
```

For example, Motor A needs electrical power to operate, but it also receives control commands from the EV3.

Similarly, a sensor requires power to operate while also returning measurements to the controller.

The current documentation therefore distinguishes:

```text
component is powered
```

from:

```text
component communicates with EV3
```

even when both functions occur through the same physical connection.

---

# 9.5 Motor Power and Control

Piolín uses two EV3 motor outputs.

### Port A

```text
EV3
 ↓
PORT A
 ↓
Large Motor
 ↓
Rear propulsion
```

### Port B

```text
EV3
 ↓
PORT B
 ↓
Medium Motor
 ↓
Ackermann steering
```

The EV3 provides both the electrical interface and the software control path for these motors.

The current architecture does not use an external motor driver between the EV3 and either actuator.

This allows:

```text
navigation decision
      ↓
EV3 motor command
      ↓
motor response
```

without another controller in the chain.

---

# 9.6 Motor Electrical Demand and Mechanical Load

Electrical demand and mechanical load are connected.

For Motor A:

```text
greater drivetrain resistance
→ greater mechanical effort
```

Potential causes include:

```text
axle friction

wheel rubbing

drivetrain misalignment

strong steering resistance
```

For Motor B:

```text
greater steering resistance
→ greater actuator effort
```

Potential causes include:

```text
tight pivots

linkage binding

wheel friction

mechanical misalignment
```

Therefore a motor that appears to be experiencing a power problem may actually be operating against unnecessary mechanical resistance.

The electrical system should not be used to compensate for a mechanically inefficient subsystem.

---

# 9.7 Permanent Sensor Power Architecture

Three sensors remain connected in both rounds:

```text
S2 = LEFT Ultrasonic

S3 = RIGHT Ultrasonic

S4 = Color Sensor
```

These devices form Piolín's permanent sensing layer.

Conceptually:

```text
              EV3
               │
      ┌────────┼────────┐
      │        │        │
      ▼        ▼        ▼
     S2       S3       S4
      │        │        │
      ▼        ▼        ▼
 LEFT US   RIGHT US   COLOR
```

This part of the wiring does not need to be changed when switching between Open and Obstacles.

Keeping the permanent sensors electrically unchanged reduces the possibility of introducing wiring errors between rounds.

---

# 9.8 Modular S1 Electrical Architecture

S1 is the only current sensor port intentionally changed between competition configurations.

```text
                 S1
                 │
         ┌───────┴───────┐
         │               │
         ▼               ▼
       OPEN          OBSTACLES
         │               │
         ▼               ▼
       GYRO            PIXY2.1
```

This design was selected because the two challenges require different information.

During Open:

```text
rotation information
```

is valuable.

During Obstacles:

```text
visual identity
+
visual position
```

is essential.

Using S1 as a modular port avoids adding a secondary controller solely to keep both devices connected simultaneously.

---

# 9.9 Open Challenge Electrical Configuration

The complete current Open configuration is:

```text
                EV3 BATTERY 45501
                       │
                       ▼
                     EV3
                       │
       ┌───────────────┼───────────────┐
       │               │               │
       ▼               ▼               ▼
    MOTORS           SENSORS         CONTROL
       │               │
   ┌───┴───┐      ┌────┼────┬────┐
   │       │      │    │    │    │
   ▼       ▼      ▼    ▼    ▼    ▼
   A       B      S1   S2   S3   S4
   │       │      │    │    │    │
   ▼       ▼      ▼    ▼    ▼    ▼
 Large   Medium  Gyro Left Right Color
 Motor   Motor        US    US  Sensor
```

The corresponding assignments are:

| Port | Open Component |
| :---: | :--- |
| A | EV3 Large Motor — propulsion |
| B | EV3 Medium Motor — steering |
| S1 | EV3 Gyro Sensor |
| S2 | Left Ultrasonic Sensor |
| S3 | Right Ultrasonic Sensor |
| S4 | Color Sensor |

No Pixy2.1 is installed in this configuration.

No Arduino Nano is required.

No HuskyLens is required.

No permanent front ultrasonic sensor is used.

---

# 9.10 Why the Open Wiring Is Simple

The Open Challenge configuration is almost completely LEGO-native.

Its active electrical devices are:

```text
EV3 Brick

EV3 Battery

EV3 Large Motor

EV3 Medium Motor

EV3 Gyro Sensor

2 × EV3 Ultrasonic Sensors

EV3 Color Sensor
```

This creates a short electrical and control path.

For example:

```text
Gyro
 ↓
EV3
 ↓
Motor B
```

The heading measurement does not pass through an additional processor.

Likewise:

```text
Ultrasonic
 ↓
EV3
 ↓
navigation
```

This reduces the number of interfaces that must be checked when debugging the Open Challenge.

---

# 9.11 Obstacle Challenge Electrical Configuration

The Obstacle Challenge uses the same EV3, battery, motors, ultrasonic sensors, and Color Sensor.

Only S1 changes.

<div align="center">

<img
  src="../../v-photos/v4/wiring_obstacle.jpg"
  alt="Piolín wiring in the Obstacle Challenge configuration"
  width="720"
/>

<br>

<sub><b>Figure 9.3.</b> Current Piolín wiring in the Obstacle Challenge configuration, where Pixy2.1 replaces the Gyro Sensor on S1.</sub>

</div>

The configuration becomes:

```text
                EV3 BATTERY 45501
                       │
                       ▼
                     EV3
                       │
       ┌───────────────┼───────────────┐
       │               │               │
       ▼               ▼               ▼
    MOTORS           SENSORS         CONTROL
       │               │
   ┌───┴───┐      ┌────┼────┬────┐
   │       │      │    │    │    │
   ▼       ▼      ▼    ▼    ▼    ▼
   A       B      S1   S2   S3   S4
   │       │      │    │    │    │
   ▼       ▼      ▼    ▼    ▼    ▼
 Large   Medium Pixy  Left Right Color
 Motor   Motor   2.1   US    US  Sensor
```

The assignments are:

| Port | Obstacle Component |
| :---: | :--- |
| A | EV3 Large Motor — propulsion |
| B | EV3 Medium Motor — steering |
| S1 | Pixy2.1 |
| S2 | Left Ultrasonic Sensor |
| S3 | Right Ultrasonic Sensor |
| S4 | Color Sensor |

The Gyro Sensor is not installed during this round.

---

# 9.12 Pixy2.1 Electrical Integration

Pixy2.1 is the only major active current sensing component outside the LEGO Mindstorms EV3 ecosystem.

<div align="center">

<img
  src="../../v-photos/v4/pixy21_connection_cable.jpg"
  alt="Connection cable used between Pixy2.1 and Piolín's EV3"
  width="680"
/>

<br>

<sub><b>Figure 9.4.</b> Current connection used to integrate Pixy2.1 into the EV3-based Obstacle Challenge architecture.</sub>

</div>

The current system uses:

```text
Pixy2.1
   ↓
S1 interface
   ↓
EV3
```

for the Obstacle Challenge.

The current integration provides the communication path used by the EV3 to obtain Pixy block information and supports the camera through the installed S1 connection.

The exact connector pinout and electrical details should be documented only from the actual installed interface or authoritative hardware documentation.

This repository therefore does **not** guess:

```text
individual pin voltage

custom pin mapping

unverified current draw

unverified regulator topology
```

from appearance alone.

---

# 9.13 Pixy Signal Path

During Obstacles, the software obtains visual information through the Pixy interface.

Conceptually:

```text
PILLAR
   ↓
PIXY2.1
   ↓
S1 COMMUNICATION
   ↓
EV3 SOFTWARE
   ↓
TARGET INTERPRETATION
   ↓
MOTOR COMMAND
```

The current obstacle software path uses:

```text
ev3dev2
+
SMBus / I2C
```

for Pixy communication.

This communication architecture belongs to the same EV3 that controls Motor A and Motor B.

There is no second main navigation processor.

---

# 9.14 Power and Data for Pixy Should Not Be Confused

The camera must both:

```text
operate electrically
```

and:

```text
communicate visual information
```

with the EV3.

These functions are related but conceptually separate.

```text
Pixy operating power
        +
Pixy data communication
        ↓
usable vision system
```

When debugging Pixy, the team should therefore distinguish between:

```text
camera does not power correctly
```

and:

```text
camera powers but EV3 receives no valid data
```

because those indicate different failure layers.

---

# 9.15 Why the Arduino Nano Is No Longer Required

Piolín's historical HuskyLens architecture used:

```text
HuskyLens
    ↓ I2C
Arduino Nano
    ↓ USB Serial
EV3
```

The Arduino Nano acted as an interface bridge.

This added:

```text
another electronic board

another communication protocol

another software layer

additional wiring

another debugging stage
```

The current Pixy architecture is shorter:

```text
Pixy2.1
   ↓
EV3
```

The Nano is therefore not part of the current power or wiring architecture.

It remains relevant only in Piolín's legacy engineering history.

---

# 9.16 Why the HuskyLens Is No Longer Powered

The current obstacle robot does not contain HuskyLens.

Therefore the present competition wiring does not need to provide power, communication, or physical mounting for:

```text
HuskyLens

Arduino Nano
```

This distinction is important for reproducibility.

A team reconstructing current Piolín should not reproduce electrical subsystems that belonged only to earlier experiments.

---

# 9.17 No Permanent Front Ultrasonic

Earlier robot configurations also used or explored a frontal ultrasonic sensor.

The current architecture does not.

The final sensor port allocation is:

```text
S1
→ round-specific sensor


S2
→ Left Ultrasonic


S3
→ Right Ultrasonic


S4
→ Color
```

Therefore no additional front ultrasonic connection should appear in the current wiring.

This keeps the electrical documentation consistent with the actual competition configuration.

---

# 9.18 No External Motor Driver

The current LEGO EV3 motors are connected directly through EV3 Motor Ports A and B.

Piolín does not currently require an external motor driver.

The actuation path is:

```text
EV3
 ↓
motor port
 ↓
EV3 motor
```

rather than:

```text
EV3
 ↓
external controller
 ↓
motor driver
 ↓
motor
```

This simplifies:

```text
power distribution

software control

fault diagnosis

reproduction
```

---

# 9.19 No External Competition Battery

The current Piolín platform does not use an additional battery for:

```text
propulsion

steering

vision
```

The primary vehicle energy source remains the EV3 Rechargeable Battery 45501.

This means another team reproducing Piolín does not need to design:

```text
multiple battery rails

battery isolation

multiple charging systems

multiple power switches
```

for the current architecture.

---

# 9.20 No Current External Buck Converter

A dedicated external buck converter is not part of the current final architecture.

This is important because older experimental electronic systems could have required more custom power management.

The final architecture instead moved toward:

```text
fewer external electronics
```

which reduced:

```text
power-conversion requirements

wiring complexity

electronic failure points
```

The repository should therefore not include a buck converter in the current Bill of Materials unless the physical competition robot later changes.

---

# 9.21 Why Electrical Simplification Matters

Every additional electronic component creates dependencies.

For example:

```text
additional processor
→ requires power
→ requires communication
→ requires initialization
→ requires software
→ creates another failure point
```

A systems-engineering question should therefore be:

> Does this component provide information or capability that justifies the complexity it introduces?

This principle directly influenced Piolín's movement from the historical HuskyLens/Nano system toward the current modular EV3 architecture.

---

# 9.22 Cable Routing

Electrical design also interacts with mechanical design.

Cables must remain clear of:

```text
steering linkage

front wheels

rear drivetrain

moving axles
```

A cable that is electrically correct can still create a mechanical failure if it interferes with a moving subsystem.

This is especially important around Motor B.

The steering mechanism moves through a significant range, so cable clearance should be checked at:

```text
left steering

center

right steering
```

rather than inspecting wiring only while the wheels are centered.

---

# 9.23 Why Wiring Must Be Mechanically Secured

Competition movement includes:

```text
acceleration

cornering

reverse movement

wall corrections

obstacle avoidance
```

A loose connector or cable can move during these maneuvers.

The result may appear as an intermittent software failure:

```text
sensor works
→ sensor disconnects
→ sensor works again
```

even though the code has not changed.

Wiring therefore needs:

```text
secure connection

reasonable strain relief

clear routing

mechanical clearance
```

in addition to correct electrical assignment.

---

# 9.24 Electrical Faults Can Look Like Software Faults

Suppose a sensor stops returning useful information.

The visible result could be:

```text
robot drives incorrectly
```

but the cause might be:

```text
software error

wrong port

loose connector

failed initialization

communication issue
```

A useful diagnostic sequence is:

```text
PHYSICAL CONNECTION
        ↓
PORT ASSIGNMENT
        ↓
DEVICE INITIALIZATION
        ↓
RAW DATA
        ↓
PROCESSED DATA
        ↓
NAVIGATION
```

This prevents the navigation controller from being modified unnecessarily when the actual problem exists at the electrical interface.

---

# 9.25 Open Pre-Run Electrical Check

Before an Open Challenge test:

```text
1. Battery installed and sufficiently charged.

2. EV3 powers on correctly.

3. Motor A connected to A.

4. Motor B connected to B.

5. Gyro installed on S1.

6. LEFT Ultrasonic installed on S2.

7. RIGHT Ultrasonic installed on S3.

8. Color Sensor installed on S4.

9. No Pixy installed.

10. No cable interferes with steering or drivetrain.
```

Then verify sensor response before full navigation begins.

---

# 9.26 Obstacle Pre-Run Electrical Check

Before an Obstacle Challenge test:

```text
1. Battery installed and sufficiently charged.

2. EV3 powers on correctly.

3. Motor A connected to A.

4. Motor B connected to B.

5. Pixy2.1 installed on S1.

6. LEFT Ultrasonic installed on S2.

7. RIGHT Ultrasonic installed on S3.

8. Color Sensor installed on S4.

9. Gyro removed.

10. Pixy communication verified.

11. No cable interferes with steering or drivetrain.
```

This sequence prevents the most basic configuration errors from being mistaken for autonomous-navigation problems.

---

# 9.27 Round Change Procedure

Switching Piolín between the two current competition configurations should require only a limited electrical change.

### Open → Obstacles

```text
power down EV3
      ↓
remove Gyro from S1
      ↓
install Pixy2.1 S1 connection
      ↓
verify Pixy mount
      ↓
start obstacle software
```

### Obstacles → Open

```text
power down EV3
      ↓
remove Pixy2.1 from S1
      ↓
install Gyro on S1
      ↓
verify Gyro orientation
      ↓
start Open software
```

S2, S3, S4, Motor A, and Motor B remain unchanged.

This minimizes reconfiguration risk.

---

# 9.28 Why the EV3 Should Be Powered Down During Reconfiguration

Changing the active S1 device is a hardware reconfiguration.

A safe and reproducible procedure is to make the physical change with the EV3 powered down.

This ensures that:

```text
device change
```

and:

```text
software initialization
```

occur in a clearly defined sequence.

Once the correct device is installed, the appropriate round software can initialize the expected hardware.

This also reduces ambiguity during debugging.

---

# 9.29 Software Must Match the Electrical Configuration

Hardware and software must agree.

The Open program expects:

```text
S1 = Gyro
```

while the Obstacle program expects:

```text
S1 = Pixy2.1
```

Running the wrong software with the wrong hardware can produce:

```text
initialization failure

invalid sensor values

missing device errors

unexpected behavior
```

Therefore the round selection is not only a physical wiring decision.

It is a combined:

```text
HARDWARE CONFIGURATION
+
SOFTWARE CONFIGURATION
```

decision.

---

# 9.30 Current Electrical Reproducibility Map

A team reconstructing Piolín should be able to reproduce the electrical architecture from the following assignments.

### Common

```text
Battery
→ EV3 Rechargeable Battery 45501


A
→ EV3 Large Motor


B
→ EV3 Medium Motor


S2
→ LEFT EV3 Ultrasonic Sensor


S3
→ RIGHT EV3 Ultrasonic Sensor


S4
→ EV3 Color Sensor
```

### Open

```text
S1
→ EV3 Gyro Sensor
```

### Obstacles

```text
S1
→ Pixy2.1
```

No current reconstruction requires:

```text
Arduino Nano

HuskyLens

front ultrasonic

external motor driver

external battery

buck converter
```

---

# 9.31 Current vs. Legacy Electrical Architecture

| Component / System | Current | Legacy / Removed |
| :--- | :---: | :---: |
| EV3 Brick | Yes | — |
| EV3 Battery 45501 | Yes | — |
| Motor A Large Motor | Yes | — |
| Motor B Medium Motor | Yes | — |
| S2 Left Ultrasonic | Yes | — |
| S3 Right Ultrasonic | Yes | — |
| S4 Color Sensor | Yes | — |
| S1 Gyro in Open | Yes | — |
| S1 Pixy2.1 in Obstacles | Yes | — |
| Gyro in Obstacles | No | Previous concepts only |
| Pixy in Open | No | Previous experiments only |
| Front ultrasonic | No | Earlier prototype |
| HuskyLens | No | Legacy |
| Arduino Nano | No | Legacy |
| Nano-to-EV3 USB bridge | No | Legacy |
| External motor driver | No | Not required |
| External vehicle battery | No | Not current |
| External buck converter | No | Not current |

This table is intended to prevent historical wiring from being mistaken for current competition architecture.

---

# 9.32 Why Current Photos Are Important

The actual wiring photographs provide stronger reconstruction evidence than a purely conceptual electrical illustration.

They show:

```text
real installed components

real cable routing

real sensor configuration

real controller placement
```

For this reason, the current Open and Obstacle wiring photographs are treated as the primary visual electrical references.

Conceptual diagrams should only be added later if they explain something that cannot be understood from the real hardware or port tables.

---

# 9.33 Values Intentionally Not Claimed as Final

The current documentation does not invent electrical measurements that have not been recorded.

The following should only be added with real measurement or authoritative device documentation:

```text
total current draw

Motor A current

Motor B current

Pixy current draw

individual sensor current

measured battery voltage during operation

measured voltage drop

power consumption per round

measured runtime under competition load

measured electrical efficiency
```

No power-consumption chart should be created without actual measurements.

Likewise, the Pixy connector should not be assigned a detailed custom pinout unless the installed cable/interface is physically verified or documented from an authoritative source.

---

# 9.34 Troubleshooting Electrical Problems

A useful electrical troubleshooting order is:

```text
1. Battery

2. EV3 power

3. Physical connection

4. Correct port

5. Correct round configuration

6. Device initialization

7. Raw sensor / camera data

8. Software interpretation

9. Motor response
```

This order moves from the lowest-level dependency toward autonomous behavior.

For example:

```text
Pixy not detected
```

should be investigated through:

```text
physical connection
→ S1
→ software interface
→ I2C communication
→ block data
```

before changing obstacle steering logic.

---

# 9.35 Electrical Architecture Trade-Offs

| Decision | Advantage | Trade-Off |
| :--- | :--- | :--- |
| EV3-centered power architecture | Native integration with LEGO systems | Limited EV3 port resources |
| One primary battery | Simple charging and preparation | Shared power platform |
| S1 modularity | Specialized sensing for each round | Requires physical sensor change |
| Direct Pixy integration | Fewer intermediate electronics | Requires non-LEGO S1 interface |
| No Nano in current system | Shorter communication/power chain | Removes flexible intermediate microcontroller |
| No front ultrasonic | Frees S1 for higher-value sensing | No dedicated frontal range measurement |
| No external motor driver | Simpler electrical architecture | Motors remain within EV3 ecosystem |
| No external battery | Easier reproduction | No separate propulsion power system |

The final architecture reflects the information requirements of the robot rather than maximizing the number of electrical subsystems.

---

# 9.36 Final Electrical Architecture

The complete current system can be summarized as:

```text
                 EV3 BATTERY 45501
                        │
                        ▼
                  EV3 CONTROLLER
                        │
          ┌─────────────┼─────────────┐
          │             │             │
          ▼             ▼             ▼
       MOTORS        PERMANENT      MODULAR
                      SENSORS          S1
          │             │             │
     ┌────┴────┐    ┌───┼───┐    ┌───┴────┐
     │         │    │   │   │    │        │
     ▼         ▼    ▼   ▼   ▼    ▼        ▼
     A         B    S2  S3  S4  GYRO     PIXY
     │         │    │   │   │   OPEN   OBSTACLES
     ▼         ▼    ▼   ▼   ▼
   DRIVE    STEER  LEFT RIGHT COLOR
```

The architecture is deliberately compact.

The EV3 remains the central point at which:

```text
power

sensing

software

actuation
```

come together.

---

# 9.37 Final Engineering Assessment

Piolín's power-distribution architecture reflects the same design philosophy used throughout the robot:

> **Keep the electrical system as simple as possible while preserving every sensing and actuation function required by the competition.**

The current robot uses:

```text
one EV3 Brick

one EV3 Rechargeable Battery

two EV3 motors

two permanent lateral ultrasonic sensors

one permanent Color Sensor

one round-specific S1 device
```

The Open Challenge uses:

```text
S1 = Gyro
```

The Obstacle Challenge uses:

```text
S1 = Pixy2.1
```

The historical HuskyLens, Arduino Nano, front ultrasonic sensor, and multi-stage USB vision bridge are no longer required by the current competition architecture.

This reduced:

```text
component count

power dependencies

communication layers

cable complexity

debugging complexity
```

while preserving the required vehicle capabilities.

The final power and electrical philosophy can therefore be represented as:

```text
PRIMARY BATTERY
      ↓
     EV3
      ↓
CLEAR PORT ASSIGNMENTS
      ↓
MINIMAL EXTERNAL ELECTRONICS
      ↓
REPRODUCIBLE VEHICLE
```

The electrical architecture is not designed to contain the largest possible number of devices.

It is designed so that every installed device has a clear purpose, a known connection, and a justified role in the autonomous system.

---

<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
