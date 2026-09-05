# 2. Chassis Design and Structural Integration

Piolín's chassis is the structural foundation of the entire WRO Future Engineers 2026 vehicle.

It is responsible for much more than simply holding the components together. The chassis establishes the relative position of the wheels, steering mechanism, motors, sensors, controller, and vision system. Because the autonomous software interprets sensor measurements according to this geometry, changes in the structure can directly affect navigation behavior.

The current Piolín chassis is primarily constructed from **LEGO Technic structural elements** and supports a car-like mechanical architecture with rear propulsion and front Ackermann-style steering.

The complete mechanical relationship can be summarized as:

```text
CHASSIS
   │
   ├── Supports drivetrain
   │
   ├── Supports steering system
   │
   ├── Aligns front and rear wheels
   │
   ├── Holds LEGO EV3
   │
   ├── Maintains ultrasonic sensor orientation
   │
   ├── Supports downward color sensor
   │
   ├── Supports HuskyLens
   │
   └── Organizes cables and secondary electronics
```

The chassis therefore acts as the common mechanical reference for every major Piolín subsystem.

For the general vehicle architecture, see:

[Mechanical Architecture](01_mecharchitecture.md)

---

## 2.1 Current Chassis Configuration

The current Piolín chassis supports the following primary systems:

| Chassis Region | Integrated System | Main Function |
| :--- | :--- | :--- |
| **Front** | Ackermann steering assembly | Direction control |
| **Front** | Front ultrasonic sensor | Frontal safety sensing |
| **Front / Upper Structure** | HuskyLens | Obstacle perception |
| **Left Side** | Left ultrasonic sensor | Left-wall measurement |
| **Right Side** | Right ultrasonic sensor | Right-wall measurement |
| **Lower Structure** | Color sensor | Floor-marking detection |
| **Central Structure** | LEGO EV3 | Main controller |
| **Rear Structure** | Drive system | Vehicle propulsion |
| **Internal / Upper Structure** | Arduino Nano and wiring | Vision communication support |

The chassis combines these systems into one vehicle rather than treating them as independent modules.

---

# 2.2 Confirmed Overall Dimensions

The final assembled Piolín configuration has the following confirmed dimensions:

| Parameter | Measured Value |
| :--- | :---: |
| **Length** | **210 mm** |
| **Width** | **150 mm** |
| **Height** | **230 mm** |
| **Mass** | **0.80476 kg** |

These measurements describe the complete robot rather than only the bare LEGO frame.

They include the installed mechanical, sensing, processing, and vision hardware used by the current Piolín architecture.

Conceptually:

```text
                  HEIGHT
                  230 mm
                     ↑
                     │
                     │
              ┌──────────────┐
              │              │
              │    PIOLÍN    │
              │              │
              └──────────────┘
               ← 150 mm →
                  WIDTH


       ←──────── 210 mm ────────→
                  LENGTH
```

The robot's external dimensions are relevant because Piolín must remain compact enough to maneuver within the WRO Future Engineers track while carrying all required systems.

---

# 2.3 Chassis Design Objectives

The current chassis was developed around several structural requirements.

It needed to:

```text
Maintain wheel alignment

Support Ackermann steering

Provide stable drivetrain mounting

Keep sensors in repeatable positions

Support the EV3 securely

Allow forward camera visibility

Protect cables from moving mechanisms

Remain compact

Maintain sufficient rigidity

Allow access to important components
```

These requirements can conflict with one another.

For example:

```text
More structural reinforcement
        ↓
Potentially greater rigidity

but also

More structural material
        ↓
Additional mass and occupied space
```

The final chassis therefore represents a balance between structural support, component integration, accessibility, and overall vehicle size.

---

# 2.4 LEGO Technic as the Structural Framework

Piolín uses LEGO Technic elements as the main chassis construction system.

The structural framework includes components such as:

```text
Beams

Pins

Axles

Connectors

Frames

Bracing elements

Wheel supports

Steering linkages
```

These elements allow the chassis to be assembled around the exact mechanical requirements of the vehicle.

One advantage of the Technic system during development was that structural geometry could be modified without manufacturing an entirely new chassis.

This supported an iterative process:

```text
Build
  ↓
Observe
  ↓
Modify geometry
  ↓
Reassemble
  ↓
Evaluate behavior
```

That flexibility was particularly useful while the steering, sensor arrangement, and electronics configuration were still evolving.

---

# 2.5 Structural Reference Frame

The chassis defines the physical reference frame used throughout the robot.

For navigation purposes, the main directions are:

```text
                         FRONT
                           ↑
                           │
                           │
LEFT  ←────────────── [ PIOLÍN ] ──────────────→ RIGHT
                           │
                           │
                           ↓
                          REAR
```

The sensors are mounted relative to this frame.

Therefore:

```text
Front ultrasonic
        ↓
Measures forward geometry


Left ultrasonic
        ↓
Measures left-side geometry


Right ultrasonic
        ↓
Measures right-side geometry


Color sensor
        ↓
Measures floor beneath robot


HuskyLens
        ↓
Observes forward visual region
```

If a sensor rotates relative to the chassis, the meaning of its measurement also changes.

For this reason, sensor mounting is part of the structural design.

---

# 2.6 Front Chassis Region

The front of Piolín contains several mechanically important systems.

These include:

```text
Front wheels

Steering pivots

Ackermann linkage

Motor B steering actuation

Front ultrasonic sensor

HuskyLens support structure
```

This makes the front assembly one of the most mechanically dense regions of the robot.

Conceptually:

```text
                         FRONT
                           ↑

                       HuskyLens

                    Front Ultrasonic

              Front L           Front R
                Wheel             Wheel
                   \             /
                    \           /
                  Steering Linkage
                         │
                         ▼
                      Motor B
```

The structure must hold these components without preventing the steering linkage from moving through its usable range.

---

# 2.7 Steering Structure Integration

Piolín's front chassis is designed around an Ackermann-style steering system.

The chassis must support:

```text
Left steering pivot

Right steering pivot

Steering linkage

Motor B

Front wheel mounts
```

while allowing controlled motion.

The structural relationship is:

```text
CHASSIS
   ↓
Fixed steering supports
   ↓
Rotating steering elements
   ↓
Front wheels
```

The fixed chassis establishes the geometry from which the movable steering components operate.

Any unwanted movement in the fixed support structure can alter the effective steering geometry.

---

# 2.8 Fixed Structure vs. Moving Structure

One important chassis-design distinction is between components that should remain stationary and components that must move.

### Fixed relative to the chassis

```text
EV3

Ultrasonic mounts

Color sensor mount

HuskyLens mount

Motor bodies

Main beams

Structural braces
```

### Intentionally moving

```text
Steering linkage

Front steering pivots

Front wheels

Drive wheels

Drivetrain transmission elements
```

A good chassis must provide rigidity to the fixed structure without restricting the intended motion of the mechanical systems.

---

# 2.9 Steering Clearance

The front wheels require physical clearance when steering.

When Motor B changes the steering position:

```text
Front wheel orientation changes
        ↓
Outer edge of wheel moves
        ↓
Required chassis clearance changes
```

Therefore, structural elements near the front wheels must not interfere with the steering path.

Conceptually:

```text
STRAIGHT

| FRONT WHEEL |


TURNED

\ FRONT WHEEL \
```

The second orientation occupies a different physical envelope.

The chassis design must leave space for this movement.

---

# 2.10 Structural Rigidity

The chassis must resist unnecessary deformation during:

```text
Acceleration

Braking

Cornering

Obstacle avoidance

Steering reversal

Manual handling
```

If the frame moves significantly relative to the steering system, the same motor command can produce different physical behavior.

For example:

```text
Motor B command
       ↓
Steering linkage moves
       ↓
Chassis support flexes
       ↓
Effective wheel angle changes
```

This creates inconsistency between software commands and actual trajectory.

Piolín's structure therefore uses interconnected LEGO Technic members to maintain the alignment of the important mechanical assemblies.

This does not imply that the structure is perfectly rigid. The objective is to reduce unwanted movement enough to maintain repeatable vehicle behavior.

---

# 2.11 Triangulation and Bracing

Long unsupported structural elements are generally more susceptible to movement than structures supported at multiple points.

Piolín's chassis therefore benefits from connecting major structural regions through multiple LEGO Technic members rather than relying on isolated single-beam connections.

Conceptually:

```text
Weak structural concept:

A────────────B


More constrained concept:

A────────────B
 \          /
  \        /
   \      /
      C
```

In a real LEGO chassis, the exact geometry differs, but the engineering objective is similar:

```text
More constrained joints
        ↓
Less unintended relative movement
```

Structural reinforcement is particularly important around:

```text
Steering supports

Motor mounts

Wheel supports

EV3 mounting points
```

---

# 2.12 Motor A Structural Integration

Motor A provides propulsion and must be mechanically supported by the chassis.

The structural path is:

```text
Motor A
   ↓
Motor mount
   ↓
Main chassis
   ↓
Drivetrain
   ↓
Rear propulsion
```

Motor torque creates reaction forces in the motor housing.

Therefore, the motor mount must resist those forces while keeping the drivetrain aligned.

If the motor mount moves significantly:

```text
Gear / axle alignment can change
        ↓
Mechanical resistance can increase
        ↓
Vehicle response can change
```

The drivetrain structure is documented in greater detail in:

[Drivetrain](05_drivetrain.md)

---

# 2.13 Motor B Structural Integration

Motor B actuates the steering system.

Its mounting must maintain a stable relationship with the steering linkage.

```text
Motor B
   ↓
Fixed chassis mount
   ↓
Motor output
   ↓
Steering mechanism
   ↓
Front wheels
```

If Motor B itself rotates or shifts relative to the frame, part of the commanded motion can be absorbed by structural movement instead of being transferred to the steering linkage.

For this reason, the steering motor is mechanically integrated into the fixed chassis structure.

Current motor documentation:

[Steering Motor](../components/04_SteeringMotor.md)

---

# 2.14 Rear Chassis Region

The rear region supports the propulsion system and rear wheels.

Its primary mechanical responsibilities are:

```text
Support Motor A

Maintain drivetrain alignment

Support rear wheel geometry

Transfer propulsion forces into chassis

Support rear portion of robot mass
```

The rear structure therefore receives both vertical load from the vehicle mass and longitudinal force during propulsion.

Conceptually:

```text
               Motor A
                  │
                  ▼
             Drivetrain
             /        \
            /          \
       Rear wheel   Rear wheel
```

The exact transmission arrangement is documented separately from the overall chassis structure.

---

# 2.15 Wheel Support and Alignment

Wheel alignment is fundamental to predictable vehicle movement.

Ideally, when Piolín is commanded to drive straight:

```text
Front wheels
       +
Rear propulsion direction
       ↓
Produce approximately the same
longitudinal vehicle direction
```

Misalignment can create:

```text
Continuous steering bias

Additional tire scrub

Higher mechanical resistance

Unexpected wall-distance changes
```

The chassis therefore acts as the reference structure that holds the wheel assemblies relative to one another.

---

# 2.16 Front and Rear Wheel Sizes

The current vehicle uses different front and rear wheel sizes.

| Position | Diameter | Primary Role |
| :--- | :---: | :--- |
| **Front** | **38.1 mm** | Steering |
| **Rear** | **~61.0 mm** | Propulsion |

The front radius is:

```text
R_FRONT = 19.05 mm
```

The rear radius is approximately:

```text
R_REAR ≈ 30.5 mm
```

The mechanical architecture therefore does not use four identical wheels for identical functions.

Instead:

```text
Front assembly
      ↓
Directional control


Rear assembly
      ↓
Primary propulsion
```

---

# 2.17 Central EV3 Integration

The LEGO EV3 is integrated into the main chassis rather than being treated as an external module.

This has both electronic and mechanical consequences.

Mechanically, the EV3 contributes:

```text
Mass

Volume

Structural mounting requirements
```

Electronically, it provides:

```text
Motor control

Sensor interfaces

Main processing
```

Its position must therefore balance accessibility with structural integration.

The EV3 also requires cable access to:

```text
Motor A

Motor B

S1

S2

S3

S4

USB connection
```

The chassis must provide enough physical space for these connections without allowing the cables to interfere with steering or wheel movement.

---

# 2.18 Mass Distribution

Piolín's total measured mass is:

```text
m = 0.80476 kg
```

The chassis determines where this mass is physically distributed.

Components contributing to the distribution include:

```text
EV3

Battery

Drive motor

Steering motor

Wheels

Sensors

HuskyLens

Arduino Nano

LEGO structure
```

The exact center-of-mass coordinates are not claimed in this document.

However, the design objective is to avoid placing unnecessary mass in positions that would create poor mechanical balance or interfere with vehicle motion.

---

# 2.19 Center of Mass and Vehicle Behavior

Even without a measured center-of-mass coordinate, its mechanical importance can be understood.

A vehicle's center of mass affects:

```text
Load on front wheels

Load on rear wheels

Available tire traction

Response during acceleration

Response during cornering
```

The total gravitational force acting on Piolín is approximately:

```text
P = m × g
```

using:

```text
m = 0.80476 kg

g = 9.81 m/s²
```

therefore:

```text
P ≈ 7.89 N
```

That force is distributed across the wheel contact points according to the physical mass distribution.

The chassis therefore influences not only component positioning but also wheel loading.

---

# 2.20 Lateral Ultrasonic Sensor Integration

The lateral ultrasonic sensors are physically mounted to the chassis and face their respective sides.

Current arrangement:

```text
LEFT US                     RIGHT US
  S3                           S2
   ←                           →
      ┌───────────────────┐
      │      PIOLÍN       │
      └───────────────────┘
```

Their approximate confirmed mounting height is:

```text
43.2 mm above the floor
```

Because these sensors form the primary lateral wall-navigation pair, their orientation should remain stable relative to the chassis.

The mechanical relationship is:

```text
Chassis orientation
        ↓
Sensor orientation
        ↓
Observed wall geometry
        ↓
Distance measurement
```

Current sensing documentation:

[Ultrasonic Sensors](../components/05_UltrasonicSensors.md)

---

# 2.21 Front Ultrasonic Integration

S1 is mounted facing forward.

Its main role is frontal safety.

```text
        Direction of travel
                ↑

           FRONT US S1
                │
           ┌─────────┐
           │ PIOLÍN  │
           └─────────┘
```

The front sensor must have an unobstructed forward acoustic path.

Structural elements directly in front of it could alter the usable sensing region.

Its position is therefore part of the chassis design.

The front ultrasonic is structurally integrated with the vehicle but logically separated from the lateral wall-navigation pair.

---

# 2.22 Color Sensor Integration

The color sensor is mounted underneath the chassis and faces the floor.

```text
        PIOLÍN CHASSIS
              │
              ▼
        COLOR SENSOR
              │
              ▼
          TRACK FLOOR
```

Its mounting structure must satisfy several conditions:

```text
Remain close enough to observe floor markings

Maintain consistent orientation

Avoid direct mechanical contact with track

Reduce exposure to unwanted ambient light
```

A dedicated casing around the sensor helps isolate the observation region from the surrounding environment.

A 3D-printable casing is also preserved in:

[Color Sensor Casing Model](../../models/3dprint/ColorSensorCasing.stl)

Current color-sensor documentation:

[Color Sensor](../components/06_ColorSensor.md)

---

# 2.23 HuskyLens Structural Integration

The HuskyLens is positioned toward the front of Piolín.

Its chassis mounting affects the visible region available to the obstacle-detection system.

```text
            FIELD OF VIEW
             \         /
              \       /
               \     /
              HuskyLens
                  │
                  ▼
             PIOLÍN CHASSIS
```

The mount must keep the camera facing consistently toward the region in front of the vehicle.

A change in camera orientation can change:

```text
Where pillars appear

When pillars enter view

When pillars leave view
```

The camera mount therefore forms part of the perception geometry.

Current documentation:

[HuskyLens](../components/07_HuskyLens.md)

---

# 2.24 Arduino Nano Integration

The Arduino Nano is a supporting component of the current vision architecture.

Its confirmed relationship with the EV3 is:

```text
HuskyLens
    ↓
Arduino Nano
    ↓
USB
    ↓
LEGO EV3
```

Mechanically, the Nano requires a protected mounting location and cable routing that does not interfere with:

```text
Steering movement

Wheel movement

Drivetrain

Sensor field of view
```

It does not replace the EV3 as the main vehicle controller.

---

# 2.25 Cable Management as a Mechanical Requirement

Cable routing is part of chassis engineering because electrical cables occupy physical space and can interfere with moving mechanisms.

The principal moving area that requires protection is the front steering assembly.

Poor routing could produce:

```text
Cable contacts steering linkage
        ↓
Mechanical resistance increases
        ↓
Steering response changes
```

or:

```text
Cable reaches wheel
        ↓
Cable moves or disconnects
```

For this reason, the chassis provides controlled cable paths between the EV3 and:

```text
Motor A

Motor B

Ultrasonic sensors

Color sensor

Arduino Nano
```

Mechanical cable management supports electrical reliability.

---

# 2.26 Chassis and Sensor Accuracy

Sensor accuracy is not determined only by the electronics.

Mechanical mounting also matters.

For example:

```text
Sensor rotates by small angle
        ↓
Observed wall position changes
        ↓
Reported distance changes
```

Even though the wall and vehicle center may not have moved significantly.

Similarly:

```text
Color sensor height changes
        ↓
Illuminated floor region changes
        ↓
Color reading can change
```

This demonstrates why chassis stability is part of the sensing system.

---

# 2.27 Chassis and Steering Accuracy

Steering control also depends on the chassis.

The complete chain is:

```text
Software command
        ↓
Motor B
        ↓
Motor mount
        ↓
Steering linkage
        ↓
Wheel supports
        ↓
Front-wheel orientation
```

Every structural connection in that chain contributes to the final wheel position.

If a joint has excessive unintended motion, the output becomes less repeatable.

For this reason, the steering support structure is one of the most important regions of Piolín's chassis.

---

# 2.28 Chassis and Drivetrain Efficiency

The propulsion system also depends on structural alignment.

Conceptually:

```text
Motor A
    ↓
Transmission
    ↓
Driven wheels
```

If drivetrain components are not properly aligned, part of the motor output can be lost through:

```text
Friction

Binding

Axle misalignment

Unnecessary structural deformation
```

The chassis therefore supports efficient power transfer by keeping the drivetrain geometry consistent.

---

# 2.29 Ground Clearance

Piolín must provide sufficient clearance between the fixed chassis structure and the track surface.

The underside includes the downward-facing color sensor and structural components.

The design must avoid unintended contact between the track and:

```text
LEGO beams

Sensor casing

Axles

Cables

Other fixed components
```

while still positioning the color sensor appropriately for floor observation.

No final numerical ground-clearance value is claimed here because it has not been confirmed as a final measured specification.

---

# 2.30 Chassis Width and Track Navigation

The confirmed total vehicle width is:

```text
150 mm
```

The chassis width directly affects:

```text
Available lateral clearance

Distance from sensors to walls

Obstacle bypass space

Turning envelope
```

This means software wall-distance targets cannot be interpreted independently from the physical vehicle width.

The robot does not navigate as a single mathematical point.

It occupies a real physical envelope:

```text
               150 mm
       ←──────────────────→

       ┌──────────────────┐
       │      PIOLÍN      │
       └──────────────────┘
```

The navigation software must therefore keep the entire chassis clear of boundaries and obstacles.

---

# 2.31 Chassis Length and Cornering

The confirmed total length is:

```text
210 mm
```

During a turn, the front and rear of the vehicle follow different paths.

Conceptually:

```text
        FRONT
          ↗

      ┌───────────┐
      │           │
      │  PIOLÍN   │
      │           │
      └───────────┘
           ↗
          REAR
```

The chassis therefore occupies a larger swept area during rotation than during straight-line motion.

This is important when Piolín:

```text
Turns around track corners

Passes pillars

Recovers after obstacle avoidance

Performs parking-related movement
```

---

# 2.32 Chassis Height

The current overall height is:

```text
230 mm
```

This includes the upper robot structure and installed components.

Vertical placement affects:

```text
Component packaging

Camera mounting

Cable routing

Mass distribution
```

The objective is not simply to minimize height, but to place each subsystem where it can perform its intended function while maintaining structural stability.

---

# 2.33 Modularity and Maintenance

Although Piolín operates as one integrated vehicle, the LEGO Technic construction makes major areas accessible for modification or maintenance.

Subsystems can be treated conceptually as modules:

```text
FRONT MODULE
Steering + front sensing


CENTER MODULE
EV3 + main structure


REAR MODULE
Propulsion


SENSOR MODULES
Left / right / bottom


VISION MODULE
HuskyLens + Nano support
```

This separation makes it easier to identify whether a problem originates from:

```text
Structure

Steering

Drivetrain

Sensor mount

Electrical connection
```

without rebuilding the entire robot.

---

# 2.34 Chassis Evolution

Piolín's current chassis should not be interpreted as the first version of the robot.

The mechanical architecture evolved together with:

```text
Steering design

Sensor arrangement

Camera system

Electrical architecture

Software strategy
```

Changes to one subsystem often required physical changes elsewhere.

For example:

```text
Sensor architecture changes
        ↓
Mounting structure changes


Camera changes
        ↓
Front / upper structure changes


Steering changes
        ↓
Front chassis geometry changes
```

This development history is preserved separately from the current configuration.

[Legacy Documentation](../legacy/00_LEGACY_NOTICE.md)

Additional visual evidence of Piolín's physical evolution is available in:

[Robot Version Photos](../../v-photos/README.md)

---

# 2.35 Current Chassis vs. Legacy Configurations

The current chassis should only be interpreted together with the current hardware architecture.

Current Piolín uses:

```text
LEGO EV3

Motor A propulsion

Motor B Ackermann steering

S1 front ultrasonic

S2 right ultrasonic

S3 left ultrasonic

S4 downward color sensor

HuskyLens

Arduino Nano
```

Historical configurations involving:

```text
Gyroscope

PixyCam

Alternative ultrasonic arrangements

Raspberry Pi prototypes

Arduino Mega controller experiments
```

belong to the legacy development history and should not be used to define the final chassis configuration.

---

# 2.36 Structural Interaction With Software

The relationship between software and chassis behavior can be represented as a closed loop:

```text
TRACK
  ↓
SENSORS
  ↓
EV3
  ↓
CONTROL COMMAND
  ↓
MOTORS
  ↓
CHASSIS MECHANICS
  ↓
VEHICLE MOVES
  ↓
SENSOR GEOMETRY CHANGES
  ↓
NEW SENSOR DATA
```

The chassis is therefore not passive.

It is the physical system through which every software decision becomes a change in the environment observed by the sensors.

---

# 2.37 Mechanical Problem Propagation

A structural issue can propagate through multiple subsystems.

Example:

```text
Loose sensor mount
       ↓
Sensor angle changes
       ↓
Distance measurement changes
       ↓
Navigation error changes
       ↓
Steering command changes
       ↓
Vehicle trajectory changes
```

Another example:

```text
Loose steering support
       ↓
Physical wheel angle differs
       ↓
Robot does not follow expected path
       ↓
Wall distance changes
       ↓
Controller applies larger correction
```

This is why mechanical consistency must be considered before interpreting every navigation problem as a software problem.

---

# 2.38 Chassis Responsibility Matrix

| Chassis Requirement | Why It Matters |
| :--- | :--- |
| **Wheel alignment** | Supports predictable straight movement |
| **Steering support** | Maintains Ackermann geometry |
| **Motor support** | Transfers motor torque into useful motion |
| **Sensor stability** | Preserves measurement geometry |
| **Camera stability** | Preserves field of view |
| **Controller support** | Integrates the EV3 structurally |
| **Cable management** | Prevents mechanical/electrical interference |
| **Clearance** | Prevents contact with track or moving components |
| **Compact dimensions** | Supports track maneuverability |
| **Structural rigidity** | Improves repeatability |

The chassis therefore connects nearly every engineering category of the robot.

---

# 2.39 Final Chassis Architecture

The current structural system can be summarized as:

```text
                           PIOLÍN CHASSIS
                                  │
             ┌────────────────────┼────────────────────┐
             │                    │                    │
             ▼                    ▼                    ▼
        FRONT STRUCTURE      CENTER STRUCTURE      REAR STRUCTURE
             │                    │                    │
             │                    │                    │
     Ackermann Steering        LEGO EV3           Propulsion
         Motor B                  │                 Motor A
             │                    │                    │
       Front Wheels          Sensor Wiring        Rear Drive
             │                    │                    │
     Front Ultrasonic       Arduino Nano              │
             │                    │                 Rear Wheels
         HuskyLens                 │
                                  │
                     Structural Integration
```

The confirmed current chassis specifications are:

```text
Length       = 210 mm

Width        = 150 mm

Height       = 230 mm

Mass         = 0.80476 kg

Front wheels = 38.1 mm diameter

Rear wheels  ≈ 61.0 mm diameter

Lateral ultrasonic
mounting height ≈ 43.2 mm
```

No unconfirmed wheelbase, track-width, ground-clearance, center-of-mass coordinate, or sensor-offset values are claimed in this document.

The final chassis provides the physical reference structure required for Piolín's autonomous systems to operate together:

```text
STRUCTURE
    ↓
Stable mechanical geometry

MECHANICS
    ↓
Predictable motion

SENSORS
    ↓
Meaningful measurements

SOFTWARE
    ↓
Useful corrections
```

This integration makes the chassis the physical foundation of Piolín's WRO Future Engineers 2026 navigation architecture.

---

## Continue Reading

[Robot Mobility](03_RMobility.md)

[Steering System](04_steering.md)

[Drivetrain](05_drivetrain.md)

[Mechanical Testing](06_testing.md)

Return to:

[Mechanical Architecture](01_mecharchitecture.md)

Related hardware:

[Hardware Overview](../components/01_Hardwareoverview.md)

[Motors](../components/03_Motors.md)

[Steering Motor](../components/04_SteeringMotor.md)

[Ultrasonic Sensors](../components/05_UltrasonicSensors.md)

[Color Sensor](../components/06_ColorSensor.md)

[HuskyLens](../components/07_HuskyLens.md)
