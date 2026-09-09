# 10. Other Structural and Supporting Components

<div align="center">

<img
  src="../../v-photos/v4/chassis_top.jpg"
  alt="Top view of Piolín's LEGO Technic chassis"
  width="720"
/>

<br>

<sub><b>Figure 10.1.</b> Top view of Piolín's current LEGO Technic chassis and the structural integration of its main subsystems.</sub>

</div>

Piolín's autonomous system depends on more than its controller, motors, and sensors. A large part of the robot's reliability comes from the **structural and supporting components** that hold those systems in repeatable positions.

The current vehicle is built primarily from **LEGO Technic structural elements**, including beams, axles, pins, connectors, wheel assemblies, and mounting structures.

These components perform several important functions:

```text
support the EV3

support the battery

hold Motor A

hold Motor B

maintain Ackermann steering geometry

support the wheel assemblies

hold the ultrasonic sensors

hold the Color Sensor

support the round-specific S1 device

route cables away from moving mechanisms
```

Although these pieces do not directly execute autonomous decisions, they strongly influence whether the sensors and actuators behave consistently.

A good software controller cannot fully compensate for a chassis that changes geometry between runs.

---

## 10.1 LEGO Technic Chassis

The current Piolín platform uses a LEGO Technic frame to connect the vehicle's main systems into one rigid mechanical structure.

The chassis must support:

```text
EV3 Brick

Rechargeable Battery

Large Motor

Medium Motor

rear drivetrain

front steering system

ultrasonic sensors

Color Sensor

Gyro or Pixy2.1
```

while keeping these components in predictable positions.

The chassis therefore serves as the mechanical reference frame for almost every calibration performed on the robot.

For example:

```text
gyro orientation
```

is meaningful relative to the chassis.

```text
ultrasonic direction
```

is meaningful relative to the chassis.

```text
camera orientation
```

is meaningful relative to the chassis.

```text
steering center
```

is also defined relative to the chassis.

This makes structural consistency part of the sensing and control system.

---

## 10.2 Chassis Rigidity

<div align="center">

<img
  src="../../v-photos/v4/chassis_bottom.jpg"
  alt="Bottom view of Piolín's current chassis"
  width="720"
/>

<br>

<sub><b>Figure 10.2.</b> Bottom view of the current chassis, showing the structural relationships between the drivetrain, front steering assembly, and central frame.</sub>

</div>

A chassis does not need to be perfectly rigid, but excessive flex can reduce repeatability.

Suppose the front structure moves slightly under steering load.

```text
Motor B rotates
      ↓
steering structure flexes
      ↓
part of motor motion becomes chassis deformation
      ↓
wheel angle differs from expected value
```

The same problem can occur around sensor mounts.

```text
sensor mount flexes
      ↓
sensor orientation changes
      ↓
measurement geometry changes
```

For this reason, Piolín's structural design aims to reduce unnecessary movement around:

```text
steering pivots

motor mounts

sensor mounts

axles

EV3 mounting points
```

before software calibration is performed.

---

## 10.3 Why Structural Repeatability Matters

Many autonomous-navigation parameters assume that the physical robot remains approximately unchanged.

For example, Open navigation assumes that:

```text
S2 remains LEFT

S3 remains RIGHT

Gyro orientation remains fixed

Color Sensor remains at the same floor position
```

Obstacle navigation assumes that:

```text
Pixy remains at the same viewing orientation

ultrasonic mounts remain stable

steering geometry remains repeatable
```

If the physical structure changes, previously tuned software values may no longer describe the same vehicle.

Therefore:

> **Mechanical repeatability is a prerequisite for meaningful software calibration.**

---

# 10.4 Motor A Mounting

<div align="center">

<img
  src="../../v-photos/v4/drive_motor_mount.jpg"
  alt="Piolín Motor A mounting structure"
  width="680"
/>

<br>

<sub><b>Figure 10.3.</b> Mounting structure used to secure the EV3 Large Motor that powers Piolín's rear drivetrain.</sub>

</div>

Motor A produces the force required to move the complete robot.

Its mounting structure must therefore prevent unnecessary motion between:

```text
Large Motor

drivetrain

chassis
```

If the motor shifts relative to the drivetrain:

```text
gear / axle alignment may change

friction may increase

mechanical efficiency may decrease

encoder movement may become less repeatable
```

The motor mount is therefore part of the propulsion system rather than simply a structural accessory.

---

# 10.5 Motor B Mounting

<div align="center">

<img
  src="../../v-photos/v4/steering_motor_mount.jpg"
  alt="Piolín Motor B steering-motor mounting structure"
  width="680"
/>

<br>

<sub><b>Figure 10.4.</b> Structural mounting of the EV3 Medium Motor used to actuate Piolín's front steering system.</sub>

</div>

Motor B requires an especially stable mount because its output is interpreted as a steering-position reference.

If the motor housing moves while the output shaft rotates:

```text
encoder position changes
```

but not all of that movement becomes:

```text
wheel steering
```

The mounting structure should therefore resist:

```text
rotation

flex

movement under steering load
```

so that Motor B position corresponds as consistently as possible to the installed linkage position.

The detailed steering geometry is documented separately in [Steering Motor and Ackermann Actuation](04_SteeringMotor.md).

---

# 10.6 Axles and Rotational Support

LEGO axles transmit motion through both the drivetrain and steering systems.

Their alignment influences:

```text
friction

wheel rotation

drivetrain efficiency

steering response
```

An axle that is slightly forced out of alignment can create unnecessary resistance.

For propulsion:

```text
motor torque
      ↓
axle / drivetrain
      ↓
rear wheel motion
```

For steering:

```text
Motor B
      ↓
steering linkage
      ↓
wheel pivot motion
```

The mechanical system should therefore be checked for free movement before increasing software motor commands.

---

# 10.7 Pins and Connectors

LEGO Technic pins and connectors form the structural joints of Piolín.

They provide a modular construction system, but each connection also introduces some mechanical clearance.

Possible consequences include:

```text
small chassis flex

steering backlash

mounting movement

sensor-angle variation
```

The objective is not to claim that LEGO connections have zero play.

Instead, the chassis is arranged so that important assemblies are supported by enough structure to remain consistent under normal competition movement.

---

# 10.8 Wheel Assemblies

Piolín uses separate front and rear wheel roles.

```text
FRONT WHEELS
→ steering


REAR WHEELS
→ propulsion
```

The wheel assemblies influence:

```text
traction

turning radius

vehicle speed

encoder-to-distance relationship

ground clearance

mechanical load
```

The exact current V4 wheel diameters should be physically remeasured before being published as final specifications.

Older measurements from previous robot versions should not automatically be reused.

---

# 10.9 Rear Wheels

The rear wheels receive propulsion through Motor A and the drivetrain.

Their mechanical condition can influence:

```text
vehicle acceleration

straight-line behavior

traction

encoder-based displacement
```

Differences in wheel mounting or friction between the two sides can create an apparent navigation problem even when Motor A receives the correct software command.

Before tuning drive behavior, both rear wheels should therefore be checked for:

```text
free rotation

secure mounting

similar alignment

no chassis rubbing
```

---

# 10.10 Front Wheels

The front wheels belong to the Ackermann-style steering system.

Their mounting influences:

```text
steering geometry

mechanical center

turning radius

left/right symmetry
```

They must rotate freely while also pivoting through the steering mechanism.

A wheel that rubs against the structure during stronger steering can change the trajectory and increase Motor B load.

Therefore steering tests should check the mechanism at:

```text
center

left steering

right steering
```

rather than only when the wheels are straight.

---

# 10.11 Wheel and Axle Inspection

A simple mechanical check before major testing is:

```text
1. Lift the vehicle slightly.

2. Rotate rear wheels manually.

3. Check for rubbing or unusual resistance.

4. Move steering toward the left.

5. Check front-wheel clearance.

6. Return to center.

7. Move steering toward the right.

8. Check front-wheel clearance again.

9. Verify no axle or wheel is visibly loose.
```

This prevents software tuning from compensating for a mechanical condition that can be corrected directly.

---

# 10.12 Ultrasonic Sensor Mounts

The two lateral ultrasonic sensors remain permanently installed.

```text
S2 = LEFT

S3 = RIGHT
```

Their mounting geometry is especially important because the navigation system interprets their readings as track-relative distance information.

A small sensor rotation changes the direction in which distance is measured.

Therefore the mounts should preserve:

```text
lateral orientation

height

position relative to chassis

left/right identity
```

The detailed ultrasonic geometry is documented in [Ultrasonic Sensors](05_UltrasonicSensors.md).

---

# 10.13 Color Sensor Mount

The Color Sensor is permanently connected to S4 and faces the course surface.

Its mounting determines:

```text
sensor-to-floor distance

location at which a marking is detected

optical geometry

timing of course events
```

A loose vertical mount can change the sensor's optical response.

A loose longitudinal mount can change when the robot detects a floor marking relative to the rest of the chassis.

For this reason, the Color Sensor is treated as a fixed mechanical reference rather than as a freely repositioned accessory.

---

# 10.14 Custom Color Sensor Casing

<div align="center">

<img
  src="../../v-photos/v4/color_sensor_casing.jpg"
  alt="Piolín custom light-isolation casing around the EV3 Color Sensor"
  width="650"
/>

<br>

<sub><b>Figure 10.5.</b> Custom Color Sensor casing used to reduce uncontrolled ambient-light variation at the floor measurement area.</sub>

</div>

Piolín uses a custom casing around the downward-facing Color Sensor.

Its purpose is primarily optical rather than structural.

Without isolation:

```text
ambient light

side reflections

shadows
```

can contribute to the measurement environment.

The casing helps create a more controlled region around the sensor.

This illustrates an important engineering principle:

```text
sensor performance
=
sensor hardware
+
mechanical mounting
+
measurement environment
+
software
```

Improving the physical measurement environment can reduce the burden placed on software classification.

---

# 10.15 3D-Printed Components

The Color Sensor casing is one of the custom supporting components developed for Piolín.

The repository contains its printable model:

[Color Sensor Casing STL](../../models/3dprint/ColorSensorCasing.stl)

Providing the model improves reproducibility because another team can reproduce the same general light-isolation concept rather than reconstructing it only from photographs.

However, printing method and material can affect the final physical dimensions slightly.

The printed part should therefore still be checked on the assembled sensor.

---

# 10.16 Round-Specific S1 Mounting

Piolín's S1 device changes between rounds.

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

This means the supporting structure must allow the vehicle to use different sensing hardware while preserving the same main platform.

The modularity is primarily electrical and sensing-related rather than requiring a complete chassis rebuild.

---

# 10.17 Gyro Mounting Requirements

During Open, the Gyro Sensor must remain mechanically fixed relative to the chassis.

If the sensor rotates physically:

```text
same vehicle heading
```

can correspond to:

```text
different sensor orientation
```

which reduces the usefulness of gyro calibration.

The gyro mount should therefore maintain a repeatable orientation throughout the run.

The exact orientation is documented by the current V4 hardware evidence rather than inferred from older configurations.

---

# 10.18 Pixy2.1 Mounting Requirements

During Obstacles, Pixy2.1 must remain stable relative to the vehicle.

Camera geometry depends on:

```text
height

pitch

yaw

lateral offset
```

If the camera moves between tests, a pillar can appear at different image coordinates even when the physical scene is similar.

Therefore the Pixy mounting system is part of vision calibration.

The camera should also remain clear of:

```text
steering mechanism

moving cables

structural obstruction
```

that could reduce its useful field of view.

---

# 10.19 Cable and Connector Components

Piolín uses LEGO EV3 cables for its LEGO motors and sensors, while the Pixy2.1 uses its current S1 connection in the Obstacle configuration.

Cables perform an electrical role, but their physical routing is also a mechanical design issue.

Poor routing can create:

```text
steering interference

wheel interference

connector strain

moving cable loops

intermittent disconnection
```

Therefore cable placement must be checked under actual movement.

---

# 10.20 Cable Clearance Around Steering

Motor B moves the front steering mechanism through a usable range.

A cable may appear safe when the wheels are centered but interfere when they turn.

Cable clearance should therefore be checked at:

```text
LEFT
CENTER
RIGHT
```

If a cable becomes tensioned at one steering extreme, it can:

```text
resist Motor B

move a sensor

pull on a connector

change steering response
```

Cable routing is therefore part of mechanical reliability.

---

# 10.21 Cable Clearance Around the Drivetrain

The rear drivetrain also contains rotating components.

Cables should remain away from:

```text
axles

wheels

rotating drivetrain elements
```

A cable touching a moving drivetrain can cause:

```text
mechanical drag

cable damage

intermittent motion

unexpected load
```

The safest routing keeps wiring mechanically separated from the vehicle's moving transmission.

---

# 10.22 Fasteners and Structural Checks

Because Piolín is repeatedly:

```text
carried

tested

reconfigured

transported
```

structural connections can gradually loosen.

A simple inspection should check:

```text
motor mounts

sensor mounts

steering pivots

wheel mounts

EV3 support

camera / gyro support
```

before important runs.

This type of inspection is often faster and more effective than attempting to compensate for a shifted component through software.

---

# 10.23 Serviceability

A competition robot needs to be adjustable without requiring a complete rebuild.

Piolín's supporting structure should therefore allow access to:

```text
EV3

battery

motor connections

sensor connections

S1 device

Color Sensor

steering system
```

for inspection and maintenance.

Serviceability is an engineering trade-off.

A completely enclosed structure might protect components well, but can make:

```text
charging

port inspection

sensor replacement

mechanical adjustment
```

more difficult.

The current design prioritizes reasonable access to the components that are most likely to be checked between tests.

---

# 10.24 Modularity

Piolín uses one common vehicle platform for both competition challenges.

The permanent mechanical systems are:

```text
chassis

rear drivetrain

front steering

Motor A

Motor B

S2 Left Ultrasonic

S3 Right Ultrasonic

S4 Color Sensor
```

The challenge-specific sensor is:

```text
S1
```

This reduces the amount of mechanical reconfiguration necessary between Open and Obstacles.

The robot remains fundamentally the same vehicle.

---

# 10.25 Why One Common Chassis Is Preferable

Building separate vehicles for each challenge could allow greater specialization.

However, it would also require maintaining:

```text
two drivetrains

two steering systems

two chassis calibrations

two wiring systems

two mechanical baselines
```

Using one common platform allows mechanical improvements to benefit both rounds.

For example:

```text
better steering alignment
```

helps both Open and Obstacles.

```text
lower drivetrain friction
```

also helps both rounds.

```text
stronger chassis rigidity
```

improves all sensor calibrations.

This makes the common platform more efficient to develop.

---

# 10.26 Weight and Mass Distribution

Every supporting component adds mass.

Structural design therefore involves a trade-off between:

```text
rigidity
```

and:

```text
unnecessary weight
```

More beams and reinforcement can improve stiffness, but additional mass also increases the work required from Motor A.

Similarly, component placement affects weight distribution.

The EV3 and battery are among the larger concentrated masses in the vehicle.

The final current V4 mass should be reweighed before being published as an official specification.

No previous mass value should automatically be reused.

---

# 10.27 Dimensions

The current robot's final competition dimensions should also be physically remeasured.

Values that should be verified include:

```text
overall length

overall width

overall height

wheelbase

front track width

rear track width

ground clearance
```

Earlier Piolín measurements can remain in development history, but they should not be presented as final V4 specifications unless confirmed on the current physical robot.

The documentation should prefer:

```text
unknown pending measurement
```

over:

```text
precise but outdated number
```

---

# 10.28 Why Exact Measurements Matter

Physical dimensions affect more than appearance.

For example:

```text
wheelbase
→ steering geometry


track width
→ Ackermann relationship


sensor offset
→ measurement interpretation


camera height
→ image geometry


robot width
→ obstacle clearance
```

Therefore final dimensions should be measured specifically for the current assembled configuration.

These values can later support more detailed calculations in:

```text
mobility documentation

steering documentation

vision calibration

reproducibility
```

---

# 10.29 Components Intentionally Not Included

The current competition robot does not include:

```text
Arduino Nano

HuskyLens

permanent front Ultrasonic Sensor

Raspberry Pi

Arduino Mega

external motor driver

external competition battery

dedicated buck converter
```

These should not appear in current reconstruction instructions.

Some of them remain relevant to Piolín's engineering history and are documented separately under `docs/legacy/`.

---

# 10.30 Historical Supporting Hardware

Earlier prototypes used additional supporting hardware because the sensor architecture was different.

For example, the HuskyLens stage required:

```text
HuskyLens

Arduino Nano

USB communication

additional wiring
```

Removing that system simplified not only software and communication but also the physical robot.

Fewer supporting electronics meant fewer:

```text
mounts

cables

connections

power dependencies
```

This is an example of how one systems-level decision can simplify several engineering layers simultaneously.

---

# 10.31 Reproducibility

Another team reproducing Piolín should understand that the supporting structure must preserve the relationships between the main components.

The most important requirements are not exact cosmetic duplication.

They are:

```text
rigid central chassis

Motor A securely connected to rear drivetrain

Motor B securely connected to steering linkage

S2 mounted on LEFT side

S3 mounted on RIGHT side

S4 facing downward toward floor

S1 device mounted according to active round

wheels moving freely

cables clear of moving mechanisms
```

These relationships define the functional structure of the robot.

---

# 10.32 Mechanical Pre-Run Inspection

A practical pre-run mechanical check can be:

```text
1. Check chassis for loose connections.

2. Check EV3 mounting.

3. Check Motor A mounting.

4. Check Motor B mounting.

5. Rotate rear wheels manually.

6. Verify steering moves freely.

7. Verify S2 mount is secure.

8. Verify S3 mount is secure.

9. Verify Color Sensor and casing are secure.

10. Verify current S1 sensor is secure.

11. Check wheel clearance.

12. Check cable clearance.

13. Verify no component contacts the ground unexpectedly.

14. Begin sensor verification.
```

This procedure isolates physical issues before navigation tuning begins.

---

# 10.33 Mechanical Failure vs. Software Failure

A recurring systems lesson is:

```text
unexpected vehicle behavior
```

does not automatically mean:

```text
software error
```

For example:

| Symptom | Possible Mechanical Cause |
| :--- | :--- |
| Robot curves during straight driving | Steering center shifted |
| Left/right behavior differs | Linkage asymmetry or friction |
| Motor A seems weak | Drivetrain resistance |
| Motor B responds slowly | Steering binding |
| Ultrasonic readings changed | Sensor mount shifted |
| Pixy coordinates changed | Camera mount shifted |
| Color detection became inconsistent | Sensor/casing position changed |

The mechanical system should therefore be inspected before control parameters are changed.

---

# 10.34 Current Supporting-Component Responsibility Matrix

| Supporting Component | Main Responsibility |
| :--- | :--- |
| LEGO Technic chassis | Holds complete vehicle geometry |
| Beams and connectors | Provide structural support |
| Pins and axles | Form joints and rotational transmission |
| Rear wheel assemblies | Transfer propulsion to track |
| Front wheel assemblies | Produce steered vehicle trajectory |
| Motor A mount | Stabilizes propulsion actuator |
| Motor B mount | Stabilizes steering actuator |
| Ultrasonic mounts | Preserve lateral sensing geometry |
| Color Sensor mount | Preserves floor-sensing geometry |
| Color Sensor casing | Reduces ambient-light influence |
| S1 mounting structure | Supports Gyro or Pixy2.1 |
| EV3 cables | Connect LEGO motors and sensors |
| Pixy connection | Integrates obstacle vision with EV3 |

Each part supports another subsystem rather than functioning as an independent navigation device.

---

# 10.35 Values Intentionally Not Claimed as Final

The following should only be published after measurement on the current V4 robot:

```text
final robot mass

overall length

overall width

overall height

wheelbase

front track width

rear track width

front wheel diameter

rear wheel diameter

ground clearance

Color Sensor height

ultrasonic sensor height

sensor offsets

Pixy mounting height

Pixy mounting angle
```

The repository should not reuse stale physical dimensions simply because older versions contained measured values.

Current hardware must be measured directly.

---

# 10.36 Final Structural Architecture

Piolín's supporting mechanical system can be summarized as:

```text
                   LEGO TECHNIC CHASSIS
                           │
       ┌───────────────────┼───────────────────┐
       │                   │                   │
       ▼                   ▼                   ▼
   PROPULSION          STEERING            SENSING
       │                   │                   │
   Motor A             Motor B          S2 / S3 / S4
       │                   │                   │
 rear drivetrain       Ackermann          fixed mounts
       │                   │
       ▼                   ▼
 rear wheels          front wheels


                           +
                           │
                           ▼
                  ROUND-SPECIFIC S1
                    Gyro / Pixy2.1
```

The chassis establishes the physical relationships that allow all these systems to work together.

---

# 10.37 Final Engineering Assessment

Piolín's supporting components demonstrate that autonomous-vehicle performance depends on more than sensors and software.

A sensor must be held in the correct position.

A motor must be connected to a stable mechanism.

A wheel must rotate freely.

A cable must remain clear of moving parts.

A controller must remain securely mounted.

The complete relationship is:

```text
STRUCTURE
    ↓
COMPONENT POSITION
    ↓
MEASUREMENT / ACTUATION
    ↓
SOFTWARE INTERPRETATION
    ↓
VEHICLE BEHAVIOR
```

This is why Piolín's LEGO Technic chassis and supporting components are treated as part of the engineering system rather than as passive construction material.

The final design principle is:

> **Every supporting component should preserve the geometry, alignment, and accessibility required by the subsystem it supports without introducing unnecessary mass or complexity.**

The result is one common mechanical platform capable of supporting both competition configurations while keeping the propulsion, steering, sensing, and electrical architectures consistent and reproducible.

---

<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
