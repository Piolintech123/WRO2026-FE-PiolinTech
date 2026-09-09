# 10. Other Components and Supporting Hardware

<div align="center">

<img
  src="../../v-photos/v4/piolin_open_isometric.jpg"
  alt="Piolín complete Open Challenge hardware configuration"
  width="720"
/>

<br>

<sub><b>Figure 10.1.</b> Complete Piolín Open Challenge configuration. In addition to the major electronic components, the robot depends on a large number of structural, mechanical, mounting, and connection elements.</sub>

</div>

Piolín's main active components are documented individually throughout this section: the EV3 controller, propulsion and steering motors, ultrasonic sensors, Color Sensor, Pixy2.1 vision system, battery, and electrical architecture. However, these components cannot operate as an autonomous vehicle without the supporting mechanical and electrical hardware that connects them into one complete system.

These supporting components include the LEGO Technic chassis structure, wheels and tires, axles, gears, steering links, structural pins, cable routing elements, camera mounting hardware, the Color Sensor light-isolation casing, and the physical connection hardware used by the round-specific S1 architecture.

Although these parts are individually less complex than the main controller or sensors, their engineering importance is significant. A loose sensor mount can corrupt a measurement. A flexible steering support can change wheel geometry. A cable routed through the steering mechanism can stop an otherwise correct program. A poorly supported camera can change the visual coordinate system between runs.

Piolín therefore treats these components as part of the complete engineering system rather than as miscellaneous accessories.

---

## 10.1 Supporting-Hardware Architecture

The supporting components can be divided into several functional groups:

| Group | Main Function |
| :--- | :--- |
| LEGO Technic structure | Creates and reinforces the chassis |
| Wheels and tires | Transfer propulsion and steering forces to the track |
| Axles, gears, and drivetrain elements | Transfer Motor A rotation to the rear wheels |
| Steering links and pivots | Transfer Motor B rotation to the front wheels |
| Sensor mounts | Preserve sensor position and orientation |
| Pixy2.1 mounting hardware | Maintains the camera reference frame |
| Color Sensor casing | Reduces uncontrolled ambient light |
| EV3 cables | Connect motors and LEGO sensors |
| Pixy connection hardware | Connects the current vision system to S1 |
| Cable-management elements | Keep electrical connections away from moving mechanisms |
| Structural pins/connectors | Maintain chassis rigidity and modular assembly |

The overall relationship is:

```text
ACTIVE COMPONENT
      +
SUPPORTING HARDWARE
      ↓
REPEATABLE PHYSICAL INSTALLATION
      ↓
RELIABLE SENSOR / MOTOR BEHAVIOR
```

This relationship is important because software calibration assumes that the hardware remains physically repeatable.

---

## 10.2 LEGO Technic Structural System

Piolín is constructed primarily from LEGO Mindstorms EV3 and LEGO Technic structural elements.

These include combinations of:

```text
beams

frames

axles

pins

connectors

bushings

gears

wheel hubs

steering elements
```

that form the mechanical chassis.

<div align="center">

<img
  src="../../v-photos/v4/chassis_top.jpg"
  alt="Top view of Piolín LEGO Technic chassis"
  width="720"
/>

<br>

<sub><b>Figure 10.2.</b> Piolín's chassis viewed from above, showing the LEGO Technic structural network supporting its actuators, sensors, and controller.</sub>

</div>

The purpose of the chassis is not simply to hold the parts together. It must preserve the relative positions of the major subsystems.

In particular, it must keep stable relationships between:

```text
Motor A and rear drivetrain

Motor B and steering linkage

left and right ultrasonic sensors

Color Sensor and floor

Gyro and chassis orientation

Pixy2.1 and vehicle centerline
```

If the structure flexes enough to change one of these relationships, sensor calibration or steering behavior can change even when the software remains identical.

---

## 10.3 Chassis Rigidity

Structural rigidity is especially important in an autonomous vehicle because mechanical deformation appears to software as inconsistent behavior.

For example:

```text
sensor mount moves
      ↓
sensor measurement changes
      ↓
EV3 interprets environment differently
```

or:

```text
steering structure flexes
      ↓
same Motor B position
      ↓
different wheel angle
```

The purpose of reinforcement is therefore not to create the heaviest possible chassis.

The design goal is:

> **Use enough structure to maintain geometry while avoiding unnecessary complexity and mass.**

<div align="center">

<img
  src="../../v-photos/v4/chassis_bottom.jpg"
  alt="Bottom view of Piolín chassis structure"
  width="720"
/>

<br>

<sub><b>Figure 10.3.</b> Bottom view of the structural chassis used to maintain drivetrain, steering, and sensor alignment.</sub>

</div>

Structural changes should therefore be followed by mechanical and sensor verification before previously tuned software values are assumed to remain valid.

---

## 10.4 Modular Construction

LEGO Technic construction provides an important development advantage: major assemblies can be modified without manufacturing an entirely new chassis.

Piolín's design evolved repeatedly through changes to:

```text
sensor orientation

camera architecture

steering reinforcement

wheel support

cable routing

S1 hardware
```

The modular construction system made those iterations possible.

However, modularity also introduces mechanical joints.

Every additional connection can introduce:

```text
small play

small misalignment

structural flexibility
```

The final design therefore balances:

```text
ease of modification
```

against:

```text
mechanical rigidity
```

rather than maximizing either property independently.

---

# 10.5 Wheels and Tires

Piolín uses separate front and rear wheel roles.

The rear wheels are associated primarily with propulsion:

```text
Motor A
→ drivetrain
→ rear wheels
```

while the front wheels are associated primarily with steering:

```text
Motor B
→ Ackermann linkage
→ front wheels
```

<div align="center">

<img
  src="../../v-photos/v4/rear_wheels.jpg"
  alt="Piolín rear propulsion wheels"
  width="660"
/>

<br>

<sub><b>Figure 10.4.</b> Rear wheels used to transfer Motor A propulsion to the competition surface.</sub>

</div>

<div align="center">

<img
  src="../../v-photos/v4/front_wheels.jpg"
  alt="Piolín front steering wheels"
  width="660"
/>

<br>

<sub><b>Figure 10.5.</b> Front wheels integrated with the Ackermann-style steering system.</sub>

</div>

The wheels influence more than movement speed. Their diameter, tire deformation, traction, and alignment affect:

```text
theoretical encoder distance

cornering

steering load

vehicle speed

turning radius

odometry

parking displacement
```

For this reason, the current wheel diameters should be physically remeasured before final numerical specifications are published.

Older wheel dimensions from previous Piolín configurations should not automatically be treated as current V4 values.

---

## 10.6 Wheel Traction

Motor rotation only produces useful vehicle motion when the tire can transfer force to the track.

The complete relationship is:

```text
Motor rotation
      ↓
drivetrain
      ↓
wheel rotation
      ↓
tire / track interaction
      ↓
vehicle displacement
```

If slip occurs:

```text
wheel rotation
≠
equivalent vehicle displacement
```

This is one reason wheel encoders are useful but are not treated as perfect odometry.

Track cleanliness, tire condition, steering angle, and vehicle loading can all influence the effective traction available during a run.

---

## 10.7 Wheel Alignment

Wheel alignment affects both propulsion and steering.

A rear wheel that is not aligned correctly can introduce:

```text
rolling resistance

lateral drift

unequal drivetrain load
```

A front wheel that is misaligned can produce:

```text
constant steering bias

unequal turning behavior

increased tire scrub
```

Therefore straight-line drift should not automatically be corrected through software before wheel alignment and steering center are inspected.

Mechanical alignment is part of navigation calibration.

---

# 10.8 Axles and Rotational Support

LEGO axles transfer rotation through Piolín's drivetrain and steering mechanisms.

Their alignment is critical because an axle that is slightly forced sideways can increase friction.

This can create a misleading software symptom:

```text
Motor A command unchanged
      ↓
vehicle becomes slower
```

while the real cause is:

```text
mechanical resistance increased
```

Bushings and supports are therefore used to keep rotating parts in their intended positions while preventing unwanted axial movement.

The objective is to achieve:

```text
free rotation
+
controlled positioning
```

rather than simply adding as many axle supports as possible.

---

## 10.9 Drivetrain Components

The rear drivetrain transfers the Large Motor's output to the wheels.

<div align="center">

<img
  src="../../v-photos/v4/rear_drivetrain_top.jpg"
  alt="Top view of Piolín rear drivetrain"
  width="700"
/>

<br>

<sub><b>Figure 10.6.</b> Rear drivetrain showing the mechanical path between Motor A and the driven wheels.</sub>

</div>

The drivetrain can contain several mechanical functions:

```text
rotation transfer

axle support

gear transmission

wheel support
```

depending on the final V4 arrangement.

The exact current gear ratio should be documented only after the final drivetrain is physically verified.

This is important because an old ratio or wheel size can produce incorrect odometry calculations even if the equation itself is correct.

---

## 10.10 Drivetrain Friction

Mechanical efficiency matters because Motor A must overcome both the resistance of the vehicle and the internal resistance of the drivetrain.

Potential friction sources include:

```text
misaligned axles

tight bushings

gear contact

wheel rubbing

structural deformation
```

A useful drivetrain test is to rotate the system manually with power removed and verify that no unexpected binding exists.

This test should be performed after significant chassis changes before increasing motor commands to compensate for reduced motion.

---

# 10.11 Steering Linkage Components

The Ackermann-style steering system depends on several passive mechanical components in addition to Motor B.

These include:

```text
steering arms

links

pivots

axles

pins

wheel hubs

structural supports
```

<div align="center">

<img
  src="../../v-photos/v4/ackermann_top.jpg"
  alt="Piolín Ackermann steering linkage"
  width="700"
/>

<br>

<sub><b>Figure 10.7.</b> Complete steering assembly showing the passive linkage that transforms Motor B rotation into coordinated front-wheel movement.</sub>

</div>

These passive elements define the relationship between:

```text
Motor B rotation
```

and:

```text
left / right wheel angle
```

The steering motor therefore cannot be calibrated independently of the linkage.

Changing one steering-arm connection point can change the entire steering response even if the same Medium Motor remains installed.

---

## 10.12 Steering Pivots

The front wheels must rotate around stable steering pivots.

The pivot structure must simultaneously provide:

```text
low enough friction for Motor B to steer

enough rigidity to maintain geometry
```

A pivot that is too tight increases Motor B load.

A pivot with excessive play decreases wheel-angle repeatability.

This creates another mechanical trade-off:

```text
freedom of movement
```

versus:

```text
positional precision
```

The best configuration is the one that provides repeatable movement without binding.

---

## 10.13 Mechanical Play

Some mechanical clearance is unavoidable in LEGO assemblies.

This can appear in:

```text
axles

pins

steering pivots

linkage joints

gear interfaces
```

A small amount may have little practical effect.

Too much can cause a visible delay between:

```text
Motor B changes direction
```

and:

```text
front wheels respond
```

This is particularly important during obstacle avoidance, where the robot can move from:

```text
avoid
→ countersteer
```

in a short period.

The current documentation therefore does not claim zero backlash or perfectly rigid steering.

---

# 10.14 Sensor Mounting Hardware

Sensor mounting is part of sensor performance.

A sensor measurement is only meaningful if its position relative to the chassis remains known.

The current permanent sensors are:

```text
S2 Left Ultrasonic

S3 Right Ultrasonic

S4 Color Sensor
```

while S1 is round-specific:

```text
Open
→ Gyro


Obstacles
→ Pixy2.1
```

Each requires a different physical mounting strategy.

The ultrasonic sensors require stable lateral orientation.

The Color Sensor requires controlled height above the floor.

The gyro requires fixed orientation relative to the chassis.

Pixy requires repeatable camera alignment.

The sensor mounts are therefore functional components rather than passive decoration.

---

## 10.15 Ultrasonic Mounting

<div align="center">

<img
  src="../../v-photos/v4/PiolinUSlabeling.png"
  alt="Piolín left and right ultrasonic sensor labeling"
  width="720"
/>

<br>

<sub><b>Figure 10.8.</b> Physical identification of Piolín's lateral ultrasonic sensors: S2 LEFT and S3 RIGHT.</sub>

</div>

The current ultrasonic sensors are mounted laterally.

The mount must preserve:

```text
left/right orientation

sensor height

horizontal direction

rigidity
```

A loose ultrasonic mount can make a correct wall-following algorithm appear unstable.

Because the software assumes:

```text
S2 = LEFT
S3 = RIGHT
```

the physical mounting and electrical mapping must remain consistent.

---

# 10.16 Color Sensor Light-Isolation Casing

Piolín includes a custom casing around the downward-facing EV3 Color Sensor.

<div align="center">

<img
  src="../../v-photos/v4/color_sensor_casing.jpg"
  alt="Piolín Color Sensor light isolation casing"
  width="650"
/>

<br>

<sub><b>Figure 10.9.</b> Custom casing used to reduce uncontrolled environmental light around the S4 Color Sensor.</sub>

</div>

This component was introduced because color sensing is affected by the optical environment.

Instead of attempting to solve all lighting variation through increasingly broad software thresholds, the casing improves the physical measurement conditions before the data reaches the EV3.

The intended effect is:

```text
less uncontrolled light
        ↓
more repeatable sensor data
        ↓
cleaner Blue / Orange separation
```

The casing therefore demonstrates a broader engineering principle used in Piolín:

> **Improve the physical measurement system when possible before compensating entirely in software.**

---

## 10.17 Casing Clearance

The casing must remain close enough to the floor to reduce external light while maintaining sufficient physical clearance.

It must not:

```text
drag on the mat

contact floor markings

change the sensor angle

create additional friction
```

<div align="center">

<img
  src="../../v-photos/v4/color_sensor_casing_bottom.jpg"
  alt="Bottom view of Piolín Color Sensor casing"
  width="640"
/>

<br>

<sub><b>Figure 10.10.</b> Bottom view used to verify the casing opening and physical clearance above the competition surface.</sub>

</div>

The casing is therefore both an optical and mechanical component.

---

## 10.18 Additive-Manufactured Components

The Color Sensor casing is one example of how custom-manufactured components can complement the LEGO platform without replacing the main mechanical architecture.

The part allows Piolín to solve a specific sensing problem that standard structural elements do not address as effectively.

When custom parts are used, reproducibility requires documenting:

```text
part geometry

installation position

purpose

orientation
```

The current Color Sensor casing model is stored in the repository so that it can be reproduced consistently.

Where applicable, custom manufactured components should always have their source or printable model included alongside the documentation.

---

# 10.19 Pixy2.1 Mount

Pixy2.1 requires a mechanically stable forward-facing mount.

<div align="center">

<img
  src="../../v-photos/v4/pixy21_top.jpg"
  alt="Top view of Pixy2.1 mounted on Piolín"
  width="700"
/>

<br>

<sub><b>Figure 10.11.</b> Top view of the Pixy2.1 installation used to evaluate its alignment relative to Piolín's forward axis.</sub>

</div>

Unlike a lateral distance sensor, the camera produces measurements in image coordinates.

This makes its physical alignment especially important.

A change in camera orientation changes:

```text
where image center points

where a pillar appears in X

where a pillar appears in Y

which objects remain inside the field of view
```

The mount therefore acts as part of the visual calibration.

---

## 10.20 Pixy Mount Rigidity

A Pixy mount should remain stable during:

```text
acceleration

cornering

reverse movement

obstacle maneuvers

handling between runs
```

If the camera tilts after calibration:

```text
same physical pillar
        ↓
different image position
```

The software may then interpret the changed image as a changed target geometry.

For this reason, visual tuning should only begin after the camera mount is mechanically repeatable.

---

# 10.21 Pixy2.1 Connection Hardware

Pixy2.1 is the only major non-LEGO sensor in the current competition architecture.

Its connection hardware therefore deserves special documentation.

<div align="center">

<img
  src="../../v-photos/v4/pixy21_connection_cable.jpg"
  alt="Connection cable used between Pixy2.1 and Piolín EV3"
  width="650"
/>

<br>

<sub><b>Figure 10.12.</b> Physical connection cable used by the current Pixy2.1-to-EV3 S1 architecture.</sub>

</div>

The current obstacle configuration is:

```text
Pixy2.1
   ↓
S1 connection
   ↓
EV3
```

The exact physical cable must be documented because the visual appearance of a camera alone does not tell another team how to reproduce its EV3 integration.

This cable replaces the previous multi-device communication chain involving the HuskyLens and Arduino Nano.

---

## 10.22 EV3 Cables

The LEGO motors and LEGO sensors use EV3-compatible cables to connect to the controller.

These connections may seem simple, but incorrect routing or port assignment can create serious navigation failures.

Current mapping:

```text
A
→ Large Motor


B
→ Medium Motor


S2
→ Left Ultrasonic


S3
→ Right Ultrasonic


S4
→ Color Sensor
```

S1 is the only modular connection:

```text
Open
→ Gyro


Obstacles
→ Pixy2.1
```

Cable placement must therefore preserve both electrical correctness and mechanical freedom.

---

# 10.23 Cable Management

<div align="center">

<img
  src="../../v-photos/v4/cable_management.jpg"
  alt="Piolín cable routing and mechanical cable management"
  width="700"
/>

<br>

<sub><b>Figure 10.13.</b> Cable routing designed to keep electrical connections clear of wheels, drivetrain elements, and the moving steering mechanism.</sub>

</div>

Cables must be secured enough to prevent unwanted movement while retaining enough slack to avoid connector stress.

The two undesirable extremes are:

```text
TOO TIGHT

→ connector tension
→ possible disconnection
```

and:

```text
TOO LOOSE

→ steering interference
→ wheel interference
→ drivetrain interference
```

Cable management is therefore part of mechanical reliability.

---

## 10.24 Steering-Cable Clearance

The steering area deserves particular attention because Motor B moves a physical linkage through a changing range of positions.

A cable that is clear when the wheels are centered may enter the mechanism when the wheels turn.

Cable verification should therefore be performed at:

```text
LEFT steering position

CENTER

RIGHT steering position
```

rather than only while the robot is stationary at center.

This is another reason the complete steering range should be tested mechanically before autonomous navigation begins.

---

# 10.25 Structural Fasteners and Connectors

LEGO pins, axle connectors, bushings, and frame joints perform the same basic function as fasteners in a conventional mechanical assembly.

Their orientation and placement matter.

A partially seated connector can introduce:

```text
structural movement

misalignment

unexpected friction

sensor position changes
```

For critical structures such as:

```text
steering supports

motor mounts

sensor mounts

EV3 mounting

camera mounting
```

connections should be visually inspected before important competition runs.

---

## 10.26 EV3 Mounting

The EV3 is one of the largest and more massive individual components in Piolín.

Its mount therefore contributes to:

```text
overall rigidity

mass distribution

cable accessibility

battery accessibility
```

<div align="center">

<img
  src="../../v-photos/v4/ev3_installed.jpg"
  alt="EV3 mounted within the Piolín chassis"
  width="680"
/>

<br>

<sub><b>Figure 10.14.</b> EV3 mounting integrates the main controller and battery into the structural chassis.</sub>

</div>

The controller must be sufficiently secure to prevent movement while still allowing practical access to:

```text
power button

screen/buttons

ports

battery
```

during testing.

---

# 10.27 Round-Specific Mechanical Conversion

Piolín uses the same vehicle chassis for both competition rounds.

The main physical configuration change is the specialized S1 sensor.

```text
OPEN
→ Gyro installed


OBSTACLES
→ Pixy2.1 installed
```

<div align="center">

<img
  src="../../v-photos/v4/piolin_obstacle_isometric.jpg"
  alt="Piolín complete Obstacle Challenge configuration"
  width="720"
/>

<br>

<sub><b>Figure 10.15.</b> Obstacle configuration using the same base vehicle with Pixy2.1 replacing the Open Gyro sensing role.</sub>

</div>

This modular strategy avoids maintaining two mechanically different robots.

The following remain unchanged:

```text
chassis

Motor A

Motor B

drivetrain

steering

S2 Left Ultrasonic

S3 Right Ultrasonic

S4 Color Sensor

EV3

battery
```

This makes the robot easier to calibrate because most mechanical variables remain common between both rounds.

---

## 10.28 Why a Modular S1 Mount Is Useful

The S1 system must allow the specialized device to be changed without disturbing unrelated subsystems.

A good round conversion should not require rebuilding:

```text
steering

drivetrain

ultrasonic mounts

Color Sensor mount
```

The goal is:

```text
one controlled hardware change
```

rather than:

```text
complete robot reconstruction
```

This reduces the risk that switching competition rounds invalidates unrelated mechanical calibration.

---

# 10.29 Components Removed from the Current Architecture

Several components appeared in previous Piolín development stages but are **not part of the current competition robot**.

These include:

```text
HuskyLens

Arduino Nano

permanent front ultrasonic sensor

external battery

permanent buck converter

prototype jumper-wire assemblies
```

These components should remain in legacy documentation where they provide useful engineering history, but they should not appear in the current Bill of Materials, wiring instructions, or reproduction procedure.

This distinction is particularly important because older photographs or code may still show those devices.

---

## 10.30 Why the Arduino Nano Is Not a Current Component

The Arduino Nano previously acted as an interface between HuskyLens and the EV3.

Its former architecture was:

```text
HuskyLens
    ↓
Arduino Nano
    ↓
USB
    ↓
EV3
```

The current obstacle architecture is:

```text
Pixy2.1
    ↓
S1
    ↓
EV3
```

Because the intermediate processor is no longer required, retaining it would add:

```text
another controller

another firmware

more wiring

another communication layer
```

without providing a necessary current function.

It was therefore removed from the final active architecture.

---

## 10.31 Why the HuskyLens Is Not a Current Component

HuskyLens played an important role in Piolín's vision-development process, but the current obstacle architecture uses Pixy2.1.

The change should not be interpreted as evidence that HuskyLens is inherently unsuitable for robotics.

Instead, the final vision requirements favored:

```text
direct color signatures

block position

block width / height

simpler current EV3 integration
```

provided by the current Pixy approach.

HuskyLens therefore belongs in the repository's legacy engineering history rather than the current components section.

---

## 10.32 Why the Front Ultrasonic Is Not a Current Component

Earlier configurations used or experimented with a forward ultrasonic sensor.

The current architecture contains only:

```text
S2 Left Ultrasonic

S3 Right Ultrasonic
```

S1 is reserved for:

```text
Gyro during Open
```

or:

```text
Pixy2.1 during Obstacles
```

The front ultrasonic was therefore removed as a deliberate sensor-allocation trade-off.

This is documented more fully in the ultrasonic and electrical sections.

---

# 10.33 Hardware Common to Both Rounds

Most of Piolín's hardware is permanent.

| Component / Subsystem | Open | Obstacles |
| :--- | :---: | :---: |
| EV3 Brick | Yes | Yes |
| Battery 45501 | Yes | Yes |
| Large Motor A | Yes | Yes |
| Medium Motor B | Yes | Yes |
| Rear drivetrain | Yes | Yes |
| Ackermann steering | Yes | Yes |
| Left Ultrasonic S2 | Yes | Yes |
| Right Ultrasonic S3 | Yes | Yes |
| Color Sensor S4 | Yes | Yes |
| Color Sensor casing | Yes | Yes |
| LEGO Technic chassis | Yes | Yes |
| EV3 cables | Yes | Yes |
| Gyro | Yes | No |
| Pixy2.1 | No | Yes |
| Pixy connection hardware | No | Yes |

The table shows that the majority of Piolín is a common physical platform.

Only the specialized S1 sensing subsystem changes.

---

## 10.34 Why Common Hardware Matters

A common platform provides more than convenience.

If the drivetrain and steering remain identical between rounds, mechanical calibration performed in one configuration can remain relevant to the other.

For example:

```text
steering center

steering limits

drivetrain friction

wheel alignment
```

do not need to be rediscovered simply because S1 changes.

This is a major systems-engineering advantage of the current design.

---

# 10.35 Physical Dimensions

Piolín's final V4 dimensions should be documented from the current physical robot rather than inherited from earlier versions.

Older values exist from previous configurations, but the robot has changed through:

```text
sensor repositioning

camera changes

structural modifications

wheel changes

steering reinforcement
```

Therefore the following should be remeasured before being published as final:

```text
overall length

overall width

overall height

wheelbase

front track

rear track

ground clearance
```

<div align="center">

<img
  src="../../embed/chassis_dimensions.png"
  alt="Piolín chassis dimension reference drawing"
  width="850"
/>

<br>

<sub><b>Figure 10.16.</b> Dimension reference drawing. Numerical values should only be added after the current V4 robot is physically remeasured.</sub>

</div>

This figure should not contain estimated values presented as measurements.

---

## 10.36 Vehicle Mass

The final current mass should also be remeasured after all current hardware is installed.

The mass of the robot influences:

```text
acceleration

braking

motor load

wheel traction

steering load

battery consumption
```

A previously measured robot mass may no longer represent the present configuration after structural and vision changes.

Therefore this document intentionally does not claim a final V4 mass until it is reweighed.

---

# 10.37 Component Selection Philosophy

Piolín's supporting components follow the same philosophy as its main electronic architecture.

A component should exist because it solves a specific engineering problem.

Examples include:

```text
Color Sensor casing
→ reduces uncontrolled light


steering linkage
→ transforms Motor B motion


ultrasonic mounts
→ preserve lateral geometry


Pixy mount
→ preserves visual frame


cable supports
→ prevent mechanical interference
```

Components that no longer perform a necessary role are removed rather than kept simply because they were previously used.

This is why:

```text
Arduino Nano

HuskyLens

front ultrasonic

external power hardware
```

are not included in the current architecture.

---

## 10.38 Supporting Components and Reproducibility

A robot cannot be reproduced from a list containing only:

```text
EV3

motors

sensors
```

because the exact way those parts are mechanically integrated strongly influences behavior.

For this reason, Piolín's repository should document supporting hardware using:

```text
photographs

mechanical diagrams

3D-printable files

wiring diagrams

assembly details
```

A reconstruction should be able to identify not only **which component** was used but also:

```text
where it was installed

how it was oriented

what it was connected to

why it was placed there
```

This is especially important for the ultrasonic sensors, Color Sensor, steering linkage, and Pixy camera.

---

# 10.39 Inspection Before a Run

Supporting hardware should be included in the pre-run inspection.

A useful mechanical inspection is:

```text
Check EV3 mounting
      ↓
Check Motor A mount
      ↓
Check Motor B mount
      ↓
Check steering linkage
      ↓
Check wheel alignment
      ↓
Check ultrasonic mounts
      ↓
Check Color Sensor casing
      ↓
Check S1 device
      ↓
Check cable clearance
      ↓
Verify free wheel / steering motion
```

A loose passive component can cause the same level of navigation failure as an incorrect software parameter.

---

## 10.40 Typical Supporting-Hardware Failure Modes

| Observed Behavior | Possible Supporting-Hardware Cause |
| :--- | :--- |
| Robot drifts on a straight | Wheel alignment or steering-center structure |
| Steering becomes inconsistent | Linkage play, pivot friction, loose Motor B mount |
| Motor A appears weak | Drivetrain friction or axle misalignment |
| Ultrasonic values change unexpectedly | Sensor mount moved |
| Color detection becomes inconsistent | Casing shifted or sensor height changed |
| Pixy X values change after rebuild | Camera alignment changed |
| Pixy loses targets more often | Camera pitch/yaw mount changed |
| Random cable-related sensor loss | Connector tension or cable movement |
| Steering jams at one extreme | Cable or structure interfering with linkage |
| Same software produces different path | Mechanical geometry changed |

This table reinforces that not every apparent software problem originates in code.

---

# 10.41 Current Supporting-Hardware Definition

The current Piolín supporting hardware can be summarized as:

```text
LEGO TECHNIC STRUCTURE
        │
        ├── chassis beams / frames
        ├── pins / connectors
        ├── axles / bushings
        ├── drivetrain elements
        ├── steering linkage
        └── wheel supports


WHEELS
        │
        ├── front steering wheels
        └── rear propulsion wheels


SENSOR SUPPORT
        │
        ├── S2 Left US mount
        ├── S3 Right US mount
        ├── S4 Color Sensor mount
        ├── Color Sensor casing
        └── S1 modular mounting


ELECTRICAL SUPPORT
        │
        ├── EV3 motor/sensor cables
        ├── Pixy2.1 connection hardware
        └── cable-management elements
```

These components transform a collection of motors and sensors into a repeatable autonomous vehicle.

---

## 10.42 Final Engineering Assessment

Piolín's supporting components demonstrate that autonomous-robot performance depends on much more than processor speed or software sophistication.

A useful sensor must be mounted correctly.

A powerful motor must transfer its rotation through a low-friction drivetrain.

A steering algorithm requires a repeatable linkage.

A camera requires a stable optical reference.

A controller requires reliable wiring.

A Color Sensor classifier benefits from controlled lighting.

The complete relationship is therefore:

```text
MECHANICAL STRUCTURE
         +
MOUNTING
         +
WIRING
         +
ACTIVE ELECTRONICS
         +
SOFTWARE
         ↓
AUTONOMOUS VEHICLE
```

<div align="center">

<img
  src="../../v-photos/v4/piolin_obstacle_top.jpg"
  alt="Top view of Piolín complete hardware integration"
  width="720"
/>

<br>

<sub><b>Figure 10.17.</b> Complete Piolín hardware integration demonstrating how structural, electrical, sensing, and actuation components form one common vehicle platform.</sub>

</div>

The final supporting-hardware architecture was therefore selected according to the same systems-engineering principle used throughout the robot:

> **Every component should have a clear function, its physical implementation should support repeatable behavior, and unnecessary hardware should be removed when it no longer provides enough value to justify its complexity.**

This approach allows Piolín to maintain one mechanically consistent vehicle platform while adapting only the specialized S1 sensing subsystem between the Open and Obstacle Challenges.

---

<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
