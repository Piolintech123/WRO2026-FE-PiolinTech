# 5. Software Setup

<div align="center">

<img
  src="../../v-photos/v4/ev3_installed.jpg"
  alt="LEGO Mindstorms EV3 installed as Piolín's central controller"
  width="700"
/>

<br>

<sub><b>Figure 5.1.</b> Piolín uses the EV3 Brick as the execution platform for both competition programs, while the active software environment changes with the S1 device installed for each round.</sub>

</div>

Piolín uses **two round-specific software configurations** because the Open Challenge and Obstacle Challenge use different hardware on Sensor Port S1 and require different sensor interfaces.

The software architecture follows the same principle as the hardware architecture:

```text
ONE VEHICLE
+
TWO ROUND-SPECIFIC PROGRAMS
```

The current configuration is:

| Challenge | S1 Hardware | Main Software Environment |
| :--- | :--- | :--- |
| Open Challenge | EV3 Gyro Sensor | Pybricks MicroPython |
| Obstacle Challenge | Pixy2.1 | Python 3 + ev3dev2 + SMBus/I2C |

The permanent hardware remains:

```text
Motor A
→ propulsion

Motor B
→ steering

S2
→ LEFT Ultrasonic

S3
→ RIGHT Ultrasonic

S4
→ Color Sensor
```

The software selected for a run must always match the physical device installed on S1.

```text
OPEN SOFTWARE
↔
GYRO ON S1
```

```text
OBSTACLE SOFTWARE
↔
PIXY2.1 ON S1
```

Running the correct code with the wrong S1 hardware should be treated as a **configuration error**, not as a controller-tuning problem.

---

## 5.1 Software Architecture

Piolín deliberately avoids combining every experimental driver and competition mode into one large program.

The preferred project structure separates the two challenge entry points:

```text
src/
│
├── open_challenge.py
│
└── obstacle_challenge.py
```

Conceptually:

```text
OPEN CHALLENGE
      │
      ▼
Pybricks MicroPython
      │
      ├── Motor A
      ├── Motor B
      ├── Gyro S1
      ├── Left US S2
      ├── Right US S3
      └── Color S4
```

while:

```text
OBSTACLE CHALLENGE
      │
      ▼
Python 3 / ev3dev2
      │
      ├── Motor A
      ├── Motor B
      ├── Pixy2.1 S1
      ├── Left US S2
      ├── Right US S3
      └── Color S4
```

This separation mirrors the real hardware and makes each program easier to understand, test, and reproduce.

During development, filenames may differ from the final repository entry points. A known Open development version, for example, may retain a longer experimental filename. Before competition or final repository publication, the known-good program should be copied or promoted into a clearly identified round-specific entry point without losing its Git history.

---

## 5.2 Common EV3 Requirements

Both competition programs run on the LEGO Mindstorms EV3 Brick.

The EV3 environment must be capable of:

```text
running Python-based programs

accessing EV3 motor ports

accessing EV3 sensor ports

reading motor encoders

executing files from the robot filesystem
```

The Obstacle environment additionally needs access to the I2C/SMBus interface used for Pixy2.1 communication.

Before working on either competition program, verify that the EV3 itself is operational:

```text
EV3 powers correctly

battery is installed

filesystem is accessible

program files can be transferred

Python environment launches

motor and sensor devices are visible
```

Software debugging should not begin until these basic platform requirements are working.

---

# 5.3 Hardware Must Match the Software

Before selecting the software environment, identify the active round.

### Open hardware

```text
A  → Large Motor

B  → Medium Motor

S1 → Gyro

S2 → LEFT Ultrasonic

S3 → RIGHT Ultrasonic

S4 → Color Sensor
```

### Obstacle hardware

```text
A  → Large Motor

B  → Medium Motor

S1 → Pixy2.1

S2 → LEFT Ultrasonic

S3 → RIGHT Ultrasonic

S4 → Color Sensor
```

<div align="center">

<img
  src="../../v-photos/v4/wiring_open.jpg"
  alt="Piolín Open Challenge wiring configuration"
  width="720"
/>

<br>

<sub><b>Figure 5.2.</b> Open software must be used with the Gyro Sensor installed on S1.</sub>

</div>

<div align="center">

<img
  src="../../v-photos/v4/wiring_obstacle.jpg"
  alt="Piolín Obstacle Challenge wiring configuration"
  width="720"
/>

<br>

<sub><b>Figure 5.3.</b> Obstacle software must be used with Pixy2.1 installed on S1.</sub>

</div>

The following combinations are incorrect:

```text
Open program
+
Pixy on S1
```

```text
Obstacle program
+
Gyro on S1
```

The software should never compensate for an incorrect hardware configuration.

---

# 5.4 Open Challenge Environment

The current Open development path uses **Pybricks MicroPython**.

This environment is responsible for controlling the EV3 hardware used during Open:

```text
Large Motor A

Medium Motor B

Gyro Sensor

two Ultrasonic Sensors

Color Sensor
```

The Open controller uses the sensors for different purposes:

```text
Gyro
→ heading and rotational reference

S2 / S3
→ lateral track geometry

S4
→ course-direction and progression events
```

The known control architecture includes:

```text
gyro initialization

straight heading stabilization

wall-relative correction

color-event processing

corner-state logic

progress counting

parking logic
```

The software should initialize all required hardware before Motor A begins propulsion.

---

## 5.5 Open Startup Sequence

<div align="center">

<img
  src="../../v-photos/v4/s1_open_gyro.jpg"
  alt="Piolín EV3 Gyro Sensor installed on S1"
  width="660"
/>

<br>

<sub><b>Figure 5.4.</b> The Gyro Sensor must be installed and initialized before the Open controller begins autonomous movement.</sub>

</div>

A reproducible Open startup sequence is:

```text
1. Install the Gyro Sensor on S1.

2. Verify S2 = LEFT Ultrasonic.

3. Verify S3 = RIGHT Ultrasonic.

4. Verify S4 = Color Sensor.

5. Verify Motor A = propulsion.

6. Verify Motor B = steering.

7. Power on the EV3.

8. Load the Open program.

9. Keep Piolín stationary.

10. Initialize sensors.

11. Reset the gyro heading reference.

12. Verify steering center.

13. Place Piolín at the intended starting position.

14. Start the autonomous run.
```

The gyro reference should be established while Piolín is stationary.

The current software concept uses:

```python
gyro.reset_angle(0)
```

or the equivalent operation supported by the active Open implementation.

The important requirement is not the exact syntax alone. It is that the vehicle begins with a known relative heading reference.

---

# 5.6 Running the Open Program

When using an EV3 environment configured for Pybricks MicroPython, a development program may be launched from the EV3 shell using the appropriate Pybricks runner.

A typical development command has the form:

```bash
brickrun -r -- pybricks-micropython <open_program>.py
```

For example, after the final entry point is organized as:

```text
src/open_challenge.py
```

the corresponding command can follow the same pattern using that filename.

The exact working directory depends on where the repository is stored on the EV3.

A program should not be considered correctly installed merely because it starts.

Before track testing, verify that it can read the expected hardware.

---

# 5.7 Open Hardware Test Before Driving

A minimal Open diagnostic should verify:

```text
Motor A responds

Motor B responds

Gyro angle changes when Piolín rotates

S2 reports left-side distance

S3 reports right-side distance

S4 changes when placed over course colors
```

The most important mapping check is:

```text
S2 = LEFT

S3 = RIGHT
```

If these values are reversed in software, the controller can produce physically inverted wall corrections even though the motors and sensors are all functioning.

---

# 5.8 Open Direction State

The current course-direction convention is:

```text
BLUE first
→ COUNTERCLOCKWISE
```

```text
ORANGE first
→ CLOCKWISE
```

The software should initially treat direction as unknown:

```text
direction = UNKNOWN
```

and establish it only after the first valid course-color event.

Once selected:

```text
direction should remain persistent
```

for the run.

The program must not repeatedly invert direction every time another Blue or Orange region is detected.

This direction state determines how the permanent sensors are logically interpreted.

### Counterclockwise

```text
S2 LEFT
→ inner

S3 RIGHT
→ outer
```

### Clockwise

```text
S3 RIGHT
→ inner

S2 LEFT
→ outer
```

The physical sensor mapping remains unchanged.

---

# 5.9 Open Gyro Control

The current Open controller combines gyro information with ultrasonic geometry.

A conceptual control structure is:

```text
wall geometry
      ↓
lateral correction
```

plus:

```text
gyro heading error
      ↓
heading correction
```

followed by:

```text
combined steering request
      ↓
Motor B
```

Current development code has used gyro PD-style stabilization rather than relying on the gyro as a complete navigation system by itself.

Working values inside the current code should be treated as **calibration constants**, not permanent hardware specifications.

The reproducibility requirement is therefore:

```text
copy current known-good values
      ↓
verify hardware geometry
      ↓
recalibrate if mechanical configuration changes
```

rather than assuming a gain value will behave identically on every rebuild.

---

# 5.10 Obstacle Challenge Environment

The Obstacle Challenge requires a different software path because S1 is occupied by Pixy2.1 rather than the EV3 Gyro Sensor.

The current development architecture uses:

```text
Python 3

ev3dev2

SMBus / I2C
```

The EV3 remains responsible for:

```text
drive motor control

steering motor control

ultrasonic sensing

Color Sensor input

state management
```

while the Pixy2.1 interface supplies forward visual block information.

The high-level software structure is:

```text
EV3 PROGRAM
    │
    ├── Motor A
    ├── Motor B
    ├── S2 Left US
    ├── S3 Right US
    ├── S4 Color
    │
    └── Pixy interface
           ↓
        I2C / SMBus
           ↓
        Pixy2.1 S1
```

---

# 5.11 Pixy2.1 Software Interface

<div align="center">

<img
  src="../../v-photos/v4/pixy21_s1_connection.jpg"
  alt="Pixy2.1 directly connected to Piolín EV3 Sensor Port S1"
  width="680"
/>

<br>

<sub><b>Figure 5.5.</b> The current Obstacle software communicates with Pixy2.1 through the direct S1 connection.</sub>

</div>

The current architecture no longer uses:

```text
HuskyLens

Arduino Nano

USB-to-Nano bridge
```

for active obstacle vision.

Instead:

```text
Pixy2.1
    ↓
S1
    ↓
EV3
```

The software accesses visual information through the current I2C/SMBus communication path.

The application should obtain block data such as:

```text
signature

x

y

width

height
```

and pass that information into the obstacle-navigation logic.

The vision interface should remain conceptually separate from the steering controller:

```text
read camera
      ↓
select target
      ↓
determine obstacle state
      ↓
calculate steering
```

rather than allowing one raw Pixy value to command Motor B directly.

---

# 5.12 Pixy2.1 Physical Configuration

<div align="center">

<img
  src="../../v-photos/v4/pixy21_front.jpg"
  alt="Pixy2.1 installed as Piolín forward vision sensor"
  width="680"
/>

<br>

<sub><b>Figure 5.6.</b> Pixy2.1 software calibration is valid only for the corresponding physical camera installation.</sub>

</div>

The current Pixy2.1 assembly includes a **3D-printed casing**.

The casing is part of the active Obstacle Challenge installation and should remain installed while final signatures and visual parameters are calibrated.

It does not require a software driver of its own, but changing the casing or camera orientation can change:

```text
lighting conditions

camera field of view

target coordinates

apparent target geometry
```

Therefore software calibration should always be associated with the current physical camera installation.

---

# 5.13 Pixy Signature Setup

The current visual mapping is:

| Pixy Signature | Target | Software Meaning |
| :---: | :--- | :--- |
| `1` | Pink | Parking reference |
| `2` | Red | Pass RIGHT |
| `3` | Green | Pass LEFT |

The camera training and the EV3 program must use the same mapping.

The required obstacle rules are:

```text
signature 2
→ RED
→ PASS RIGHT
```

```text
signature 3
→ GREEN
→ PASS LEFT
```

A common configuration failure would be:

```text
Pixy trained:
sig2 = Green
```

while:

```text
EV3 code assumes:
sig2 = Red
```

The software could then be internally correct while producing the wrong physical maneuver.

Signature mapping should therefore be verified before steering calibration.

---

# 5.14 Running the Obstacle Program

The Obstacle program uses the standard Python environment associated with its ev3dev2 implementation.

A typical shell execution pattern is:

```bash
python3 <obstacle_program>.py
```

or the equivalent launch method configured on the EV3.

If the final repository entry point is:

```text
src/obstacle_challenge.py
```

that file should be the clearly documented program used for the current Obstacle configuration.

Before full execution, verify that the software can:

```text
initialize ev3dev2 motors

read S2

read S3

read S4

open the Pixy I2C/SMBus interface

receive valid Pixy data
```

A failure in Pixy communication should be solved before obstacle-navigation parameters are modified.

---

# 5.15 Obstacle Startup Sequence

A reproducible startup process is:

```text
1. Power down Piolín before changing S1.

2. Remove the Gyro Sensor.

3. Install the Pixy2.1 assembly.

4. Verify the Pixy 3D-printed casing is secure.

5. Connect Pixy2.1 to S1.

6. Verify S2 = LEFT Ultrasonic.

7. Verify S3 = RIGHT Ultrasonic.

8. Verify S4 = Color Sensor.

9. Verify Motors A and B.

10. Power on the EV3.

11. Launch the Obstacle software environment.

12. Verify Pixy communication.

13. Verify Red / Green / Pink signature mapping.

14. Test raw ultrasonic readings.

15. Test steering direction.

16. Begin low-speed obstacle testing.
```

The robot should not proceed directly to a full-speed run after changing the S1 device.

A short hardware/software verification catches many configuration errors immediately.

---

# 5.16 Obstacle Target Processing

The software should not assume that the first block returned by Pixy is always the obstacle Piolín should follow.

A more robust pipeline is:

```text
read blocks
    ↓
reject invalid signatures
    ↓
evaluate candidate relevance
    ↓
select active pillar
    ↓
temporarily lock target
    ↓
execute maneuver
    ↓
confirm pass
    ↓
release target
```

Target relevance can use information such as:

```text
signature

x

y

width

height

current state

previous target
```

The final scoring or selection formula is still under development and should therefore not be documented as a fully validated final algorithm until testing supports it.

---

# 5.17 Vision Coordinates and Passing Direction

The software must keep two concepts separate.

```text
PIXY x
→ where the target appears in the image
```

and:

```text
signature
→ which side Piolín is required to pass
```

The rule is always:

```text
RED
→ RIGHT
```

```text
GREEN
→ LEFT
```

regardless of whether the target appears:

```text
left of image center

centered

right of image center
```

The coordinate can influence **how strongly** or **how early** the robot reacts.

It must not invert the competition rule.

---

# 5.18 Obstacle Control Arbitration

The Obstacle program contains multiple possible steering influences.

These can include:

```text
normal wall correction

wall safety

pillar avoidance

countersteering

post-pillar recovery

corner control
```

The software should not simply add all of them with equal authority.

A state-dependent priority is more understandable.

Conceptually:

```text
NORMAL
→ geometry control
```

```text
PILLAR ACTIVE
→ obstacle objective dominates
→ wall safety remains active
```

```text
PILLAR PASSED
→ countersteer
→ ultrasonic recovery
```

```text
RECOVERED
→ normal control resumes
```

This is especially important because allowing wall following to fight obstacle avoidance can make correct Pixy detections appear to produce the wrong steering behavior.

---

# 5.19 Shared Software Conventions

Even though the two programs use different software environments, some conventions should remain identical.

### Motor mapping

```text
A = propulsion

B = steering
```

### Ultrasonic mapping

```text
S2 = LEFT

S3 = RIGHT
```

### Floor sensor

```text
S4 = Color Sensor
```

### Obstacle rules

```text
RED = pass RIGHT

GREEN = pass LEFT
```

These conventions should not be redefined independently in different source files.

A shared engineering vocabulary reduces errors when switching between round-specific programs.

---

# 5.20 Recommended Source-Code Organization

A clean final repository can organize software by responsibility.

For example:

```text
src/
│
├── open_challenge.py
│
├── obstacle_challenge.py
│
└── README.md
```

If helper modules are later separated, the structure could expand conceptually to:

```text
src/
│
├── open_challenge.py
├── obstacle_challenge.py
│
├── control/
│   ├── steering
│   └── drive
│
├── sensors/
│   ├── ultrasonic
│   ├── color
│   ├── gyro
│   └── pixy
│
└── utilities/
```

The exact module structure should reflect the actual code rather than creating empty architecture only for appearance.

The important reproducibility requirement is that another reader can identify:

```text
which file starts Open

which file starts Obstacles
```

without searching through experimental programs.

---

# 5.21 Development Files vs. Current Entry Points

Piolín development naturally produces files such as:

```text
test versions

calibration programs

experimental steering programs

camera tests

old controller iterations
```

These are valuable engineering records, but they should not all appear to have equal status.

A useful distinction is:

```text
CURRENT ENTRY POINT
→ program intended for present round testing
```

```text
EXPERIMENTAL
→ active development / subsystem testing
```

```text
LEGACY
→ architecture no longer used
```

For example, old HuskyLens/Nano code should not sit beside the current Pixy program without clear legacy labeling.

This prevents another builder from reproducing the wrong architecture.

---

# 5.22 Calibration Files

Small diagnostic programs are useful during setup.

Examples include programs that only:

```text
print S2/S3 distance

print Color Sensor values

print gyro angle

read Pixy blocks

move Motor B to center

test Motor A forward/reverse
```

These programs can be easier to debug than the complete autonomous controller.

The setup philosophy is:

```text
TEST EACH INTERFACE
        ↓
THEN RUN COMPLETE CONTROLLER
```

A full autonomous program is a poor first diagnostic for a newly rebuilt system because too many variables are active simultaneously.

---

# 5.23 Suggested Software Verification Sequence

After transferring the software to the EV3, verify it in this order:

```text
1. Program starts without import/runtime errors.

2. Motor A object initializes.

3. Motor B object initializes.

4. S2 can be read.

5. S3 can be read.

6. S4 can be read.

7. Correct S1 device can be read.

8. Motor A direction is correct.

9. Motor B left/right direction is correct.

10. Steering center is correct.

11. Sensor values are physically plausible.

12. Low-speed test succeeds.

13. Only then run autonomous navigation.
```

This order isolates configuration problems before they become track collisions.

---

# 5.24 Software Setup After a Round Change

Changing from Open to Obstacles is not only a hardware action.

The active runtime also changes.

### Open → Obstacles

```text
power down
      ↓
replace Gyro with Pixy
      ↓
verify wiring
      ↓
boot EV3
      ↓
select Python 3 / ev3dev2 Obstacle program
      ↓
verify SMBus/I2C camera communication
      ↓
test signatures
      ↓
run Obstacles
```

### Obstacles → Open

```text
power down
      ↓
replace Pixy with Gyro
      ↓
verify wiring
      ↓
boot EV3
      ↓
select Pybricks Open program
      ↓
initialize gyro
      ↓
reset heading
      ↓
run Open
```

A round conversion is not complete until both the **hardware and software environment** correspond to the same challenge.

---

# 5.25 Git and Version Control

Reproducibility requires knowing which source code produced a particular result.

A useful workflow is:

```text
modify code
    ↓
test
    ↓
record observation
    ↓
keep or reject change
    ↓
commit meaningful version
```

Important known-good versions should be identifiable through Git rather than only through filenames such as:

```text
final2.py

finalfinal.py

newnewworking.py
```

Development filenames are understandable during rapid testing, but the final repository should use Git history and descriptive entry points to preserve traceability.

---

# 5.26 Configuration Constants

Controller values should be grouped clearly rather than scattered throughout the program.

Examples include:

```text
drive speed

steering limits

wall target

wall safety threshold

gyro gains

color thresholds

corner parameters

Pixy signature IDs

visual relevance limits

target-lock parameters

parking parameters
```

A reader should be able to distinguish:

```text
CALIBRATION VALUES
```

from:

```text
CONTROL LOGIC
```

This makes reproduction and retuning significantly easier.

Working values should be described as current tuning values until repeated testing supports them as final calibrated parameters.

---

# 5.27 Units

Software should use consistent units and make them obvious.

Examples include:

```text
millimeters

degrees

motor degrees

milliseconds

pixels
```

Variables should avoid ambiguous names such as:

```text
distance
```

when the actual quantity could be:

```text
distance_mm
```

or:

```text
motor_deg
```

Likewise, Pixy coordinates should remain visibly separate from physical distances.

```text
pixy_x
```

is an image coordinate.

It is not automatically a centimeter measurement.

Clear units reduce software errors and improve reproducibility.

---

# 5.28 Startup Safety

A software failure during initialization should preferably occur **before propulsion begins**.

The controller should verify critical devices before Motor A starts a normal run.

Examples include:

```text
required S1 device available?

S2 available?

S3 available?

S4 available?

Motor B initialized?
```

If a critical sensor cannot be initialized, continuing immediately at competition speed can create an avoidable collision.

The exact failure-handling implementation can evolve, but the architectural principle is:

> **Validate the control system before enabling normal motion.**

---

# 5.29 Debug Output

Diagnostic output is useful during development.

A compact line might include values such as:

```text
direction

state

corner count

S2

S3

gyro angle
```

during Open, or:

```text
state

target signature

x

y

width

height

S2

S3
```

during Obstacles.

Debug output should be concise enough that it does not make the control loop unnecessarily difficult to observe or maintain.

For competition code, unnecessary development logging can be reduced once the controller is validated.

---

# 5.30 Common Open Setup Errors

| Symptom | First Software Check |
| :--- | :--- |
| Program does not start | Pybricks runtime / syntax / file location |
| Gyro unavailable | S1 mapping and Open hardware |
| Heading starts incorrectly | Gyro initialization / reset |
| Robot corrects toward wrong wall | S2/S3 mapping or steering sign |
| Blue sets wrong direction | Color-direction mapping |
| Orange sets wrong direction | Color-direction mapping |
| Direction changes later | Persistent state implementation |
| Corner counted twice | Color-event / state logic |
| Straight driving oscillates | Control tuning after hardware verification |
| Same program changed behavior after rebuild | Recalibrate mechanics/sensors before rewriting logic |

---

# 5.31 Common Obstacle Setup Errors

| Symptom | First Software Check |
| :--- | :--- |
| `ev3dev2` import fails | Python environment / package installation |
| SMBus interface unavailable | Obstacle software environment |
| Pixy returns no blocks | S1 communication, signatures, lighting |
| Red becomes left maneuver | Signature/rule mapping |
| Green becomes right maneuver | Signature/rule mapping |
| Distant pillar changes steering | Relevance logic |
| Target changes during pass | Target-lock state |
| Camera loses target and robot reverses decision | Target-loss handling |
| Correct pillar chosen but steering seems opposed | Control arbitration / steering sign |
| Pillar passed but robot remains locked | Pass-confirmation / release state |
| Robot avoids pillar then hits wall | Recovery logic / ultrasonic arbitration |

This distinction helps prevent installation problems from being treated as vision-model or steering problems.

---

# 5.32 Legacy Software

The current software setup should not require legacy vision components.

Older Piolín development may contain software for:

```text
HuskyLens

Arduino Nano

USB serial bridge

front ultrasonic

older Pixy configurations
```

These programs should remain separated from current competition software.

The correct current distinction is:

```text
CURRENT OPEN
→ Gyro + Pybricks
```

```text
CURRENT OBSTACLES
→ Pixy2.1 + ev3dev2/SMBus
```

Legacy code is useful to explain the engineering evolution but should not be included in the current installation procedure.

---

# 5.33 Setup Checklist — Open Challenge

Before Open testing, verify:

| Check | Required State |
| :--- | :--- |
| Runtime | Pybricks MicroPython |
| Program | Current Open entry point |
| Motor A | Available and correct direction |
| Motor B | Available and centered |
| S1 | Gyro |
| S2 | LEFT Ultrasonic |
| S3 | RIGHT Ultrasonic |
| S4 | Color Sensor |
| Pixy2.1 | Not active |
| Gyro initialization | Completed while stationary |
| Direction state | Initially unknown |
| Blue mapping | Counterclockwise |
| Orange mapping | Clockwise |
| Low-speed hardware test | Completed |

Only after these checks should a complete Open run begin.

---

# 5.34 Setup Checklist — Obstacle Challenge

Before Obstacle testing, verify:

| Check | Required State |
| :--- | :--- |
| Runtime | Python 3 / ev3dev2 |
| Vision interface | SMBus/I2C available |
| Program | Current Obstacle entry point |
| Motor A | Available and correct direction |
| Motor B | Available and centered |
| S1 | Pixy2.1 |
| S2 | LEFT Ultrasonic |
| S3 | RIGHT Ultrasonic |
| S4 | Color Sensor |
| Gyro | Not active |
| Pixy casing | Installed and secure |
| `sig1` | Pink |
| `sig2` | Red |
| `sig3` | Green |
| Red rule | Pass RIGHT |
| Green rule | Pass LEFT |
| Raw camera test | Successful |
| Low-speed maneuver test | Completed |

---

# 5.35 Complete Software Deployment Flow

The reproducible software workflow can be summarized as:

```text
                    SELECT ROUND
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
            OPEN                OBSTACLES
              │                     │
              ▼                     ▼
         Gyro on S1           Pixy2.1 on S1
              │                     │
              ▼                     ▼
        Pybricks runtime      Python 3 / ev3dev2
              │                + SMBus/I2C
              │                     │
              ▼                     ▼
        load Open code       load Obstacle code
              │                     │
              ▼                     ▼
         verify sensors       verify sensors
              │                     │
              ▼                     ▼
        calibrate heading     verify signatures
              │                     │
              └──────────┬──────────┘
                         ▼
                 LOW-SPEED TEST
                         │
                         ▼
                 MANEUVER TEST
                         │
                         ▼
                    FULL RUN
                         │
                         ▼
                  RECORD RESULT
```

The central rule is simple:

```text
hardware configuration
+
runtime
+
source code
+
calibration
```

must all describe the same version of Piolín.

---

# 5.36 Final Engineering Assessment

Piolín's software architecture reflects the same modular philosophy used in its hardware.

Most of the robot remains constant:

```text
Motor A

Motor B

S2

S3

S4
```

while the specialized S1 device changes according to the challenge.

The software follows that distinction rather than hiding it.

### Open

```text
Pybricks MicroPython
+
Gyro
+
Ultrasonics
+
Color Sensor
```

### Obstacles

```text
Python 3
+
ev3dev2
+
SMBus/I2C
+
Pixy2.1
+
Ultrasonics
+
Color Sensor
```

This separation reduces unnecessary dependencies and keeps each controller aligned with the hardware that is actually installed.

The current Pixy2.1 assembly, including its **3D-printed casing**, should remain physically unchanged when final visual calibration values are recorded. Likewise, the Color Sensor casing is part of the current S4 calibration.

The software setup process therefore does not end when a Python file successfully executes.

A reproducible Piolín software installation requires:

```text
correct hardware

correct runtime

correct port mapping

correct source-code version

correct sensor calibration

correct startup procedure
```

The final principle is:

> **The program running on the EV3 must describe the same physical robot that is actually connected to it.**

Keeping the Open and Obstacle software paths clearly separated makes Piolín easier to deploy, debug, reproduce, and improve without mixing assumptions from two different competition configurations.

---

<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
