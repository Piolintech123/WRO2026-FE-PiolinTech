# 8. Battery and Primary Power Source

<div align="center">

<img
  src="../../v-photos/v4/ev3_battery_45501.jpg"
  alt="LEGO Mindstorms EV3 Rechargeable DC Battery 45501 used by Piolín"
  width="680"
/>

<br>

<sub><b>Figure 8.1.</b> LEGO Mindstorms EV3 Rechargeable DC Battery 45501 used as Piolín's primary competition power source.</sub>

</div>

Piolín uses the **LEGO Mindstorms EV3 Rechargeable DC Battery, part 45501**, as its primary power source.

The battery is installed directly in the LEGO Mindstorms EV3 Intelligent Brick and powers the central EV3-based architecture used in both WRO Future Engineers 2026 competition configurations.

The current system was intentionally designed around one main power platform rather than introducing separate batteries for different subsystems.

Conceptually:

```text
EV3 RECHARGEABLE BATTERY 45501
              ↓
         LEGO EV3 BRICK
              ↓
     vehicle electronics
              ↓
     sensing + actuation
````

Most of Piolín's active competition hardware belongs to the LEGO Mindstorms EV3 ecosystem. This makes the standard rechargeable battery a natural choice because propulsion, steering, sensing, and computation are integrated around the same controller.

---

## 8.1 Current Power Architecture

Piolín uses the same battery in both competition rounds.

### Open Challenge

```text
EV3 Battery 45501
        ↓
       EV3
        │
        ├── Motor A
        │   → Large Motor
        │   → propulsion
        │
        ├── Motor B
        │   → Medium Motor
        │   → steering
        │
        ├── S1
        │   → Gyro
        │
        ├── S2
        │   → Left Ultrasonic
        │
        ├── S3
        │   → Right Ultrasonic
        │
        └── S4
            → Color Sensor
```

### Obstacle Challenge

```text
EV3 Battery 45501
        ↓
       EV3
        │
        ├── Motor A
        │   → Large Motor
        │   → propulsion
        │
        ├── Motor B
        │   → Medium Motor
        │   → steering
        │
        ├── S1
        │   → Pixy2.1
        │
        ├── S2
        │   → Left Ultrasonic
        │
        ├── S3
        │   → Right Ultrasonic
        │
        └── S4
            → Color Sensor
```

The battery itself does not change between the two configurations.

Only the round-specific device on S1 changes.

---

## 8.2 Why the EV3 Rechargeable Battery Was Selected

The battery was selected because it integrates directly with Piolín's main controller.

The current vehicle already uses:

```text
LEGO EV3 Brick

LEGO EV3 Large Motor

LEGO EV3 Medium Motor

LEGO EV3 Ultrasonic Sensors

LEGO EV3 Color Sensor

LEGO EV3 Gyro Sensor
```

Using the standard EV3 battery avoids introducing a separate primary power architecture for hardware that was already designed around the EV3 platform.

The selected solution therefore reduces the need for:

```text
external battery packs

additional motor drivers

separate power switches

extra regulators

additional charging systems

independent power wiring
```

The engineering objective was not to maximize electrical complexity.

It was to provide a reliable power source for the existing vehicle architecture with as few unnecessary subsystems as possible.

---

## 8.3 One Main Vehicle Power Source

Piolín's current architecture is based on one main rechargeable battery rather than multiple independent vehicle power systems.

This simplifies several areas:

```text
charging

pre-run preparation

fault isolation

wiring

mechanical packaging

reproducibility
```

For example, if Piolín used separate batteries for:

```text
controller

motors

camera

additional electronics
```

the team would also need to verify the state and connections of each supply before every run.

Using the EV3 battery keeps the primary competition platform much simpler.

---

## 8.4 Battery Integration with the EV3

<div align="center">

<img
src="../../v-photos/v4/ev3_installed.jpg"
alt="LEGO EV3 Brick installed in Piolín with the rechargeable battery integrated into the controller"
width="700"
/>

<br>

<sub><b>Figure 8.2.</b> EV3 installed as Piolín's central controller and battery platform.</sub>

</div>

The rechargeable battery is mechanically integrated with the EV3 Brick.

This is important because the controller and battery together form one of the larger concentrated assemblies in the vehicle.

Their installation affects:

```text
mechanical packaging

vehicle balance

cable routing

accessibility

serviceability
```

The EV3 must remain secure during:

```text
acceleration

cornering

reverse movement

obstacle avoidance

handling between runs
```

because physical movement of the controller assembly could affect both chassis consistency and wiring reliability.

---

## 8.5 Battery Placement and Vehicle Balance

A battery is not only an electrical component.

It is also part of the vehicle's mechanical mass distribution.

The location of the EV3 and battery assembly can influence:

```text
front/rear loading

rear-wheel traction

front steering load

overall chassis balance
```

Piolín therefore treats controller placement as part of the mechanical architecture.

However, the current V4 center of mass has not yet been measured precisely.

This documentation therefore does not claim an exact center-of-mass position or exact front/rear weight distribution.

Those values should only be added after direct measurement.

---

## 8.6 Battery Condition and Motor Performance

Battery state can influence the practical behavior of an autonomous vehicle.

Motor A is responsible for propulsion, while Motor B controls steering.

If available electrical performance changes, the physical response of the motors can also change.

This is important because Piolín's trajectory depends on the interaction between:

```text
propulsion

steering

vehicle speed

mechanical load
```

For example, a corner tuned under one set of operating conditions may behave slightly differently if vehicle speed changes.

This does not mean every navigation error is a battery problem.

It means battery condition is one variable that should remain reasonably controlled during calibration and testing.

---

## 8.7 Why Battery State Matters During Calibration

A calibration result is most useful when the test conditions are repeatable.

Suppose Piolín is tuning:

```text
corner strength

drive speed

reverse distance

parking movement
```

If the battery condition changes significantly between tests, the team may observe a different physical response even when the software value remains unchanged.

Therefore a stronger experimental process is:

```text
similar battery condition
        +
same hardware
        +
same software baseline
        ↓
more meaningful comparison
```

This makes battery preparation part of the testing methodology rather than something considered only when the robot stops working.

---

## 8.8 Motors Are the Main Dynamic Load

The propulsion and steering motors create the most obvious changing electrical demand in Piolín.

Motor A must:

```text
accelerate vehicle

maintain forward motion

reverse vehicle

continue driving through turns
```

Motor B must:

```text
move steering linkage

hold steering positions

reverse steering direction

countersteer
```

Mechanical resistance increases the work required from these actuators.

For example:

```text
drivetrain friction
→ Motor A works harder
```

and:

```text
steering linkage binding
→ Motor B works harder
```

This creates an important diagnostic principle:

> A system that appears to have a power problem may actually have unnecessary mechanical resistance.

The mechanical system should therefore be inspected before increasing motor commands.

---

## 8.9 Mechanical Efficiency and Battery Use

Improving mechanical efficiency reduces unnecessary actuator load.

Relevant mechanical checks include:

```text
rear axle alignment

wheel rubbing

drivetrain friction

steering-linkage friction

tight pivots

cable interference
```

A freely moving drivetrain allows more of Motor A's output to become useful vehicle motion.

A freely moving steering mechanism allows Motor B to reach the requested position without fighting avoidable mechanical resistance.

Power-system performance and mechanical design are therefore connected.

---

## 8.10 Open Challenge Power Requirements

During Open, Piolín uses:

```text
Motor A
→ propulsion

Motor B
→ steering

S1
→ Gyro

S2
→ Left Ultrasonic

S3
→ Right Ultrasonic

S4
→ Color Sensor
```

The battery supports a largely LEGO-native electrical architecture.

There is no Pixy2.1 installed in this configuration.

There is also no Arduino Nano, HuskyLens, or permanent front ultrasonic sensor in the current Open vehicle.

This keeps the Open electrical configuration relatively simple.

---

## 8.11 Obstacle Challenge Power Requirements

During Obstacles, the Gyro Sensor is removed and Pixy2.1 occupies S1.

```text
Motor A
→ propulsion

Motor B
→ steering

S1
→ Pixy2.1

S2
→ Left Ultrasonic

S3
→ Right Ultrasonic

S4
→ Color Sensor
```

The current Pixy connection provides the obstacle-vision interface through the EV3 S1 configuration.

Piolín does not currently use a separate external competition battery for Pixy2.1.

This preserves the principle of one primary vehicle power architecture.

Detailed wiring and signal distribution are documented separately in `09_PowerDistribution.md`.

---

## 8.12 Why a Separate Pixy Battery Was Not Added

A separate camera battery would introduce another independent subsystem.

That would require additional consideration of:

```text
charging

switching

mounting

cable routing

electrical compatibility

battery condition
```

The current architecture does not require that additional complexity.

The camera is therefore integrated through the current S1 obstacle configuration rather than being treated as a separately powered vehicle subsystem.

This improves reproducibility because a second team does not need to recreate an additional battery installation.

---

## 8.13 Why an External Motor Battery Was Not Added

Piolín also does not use a separate external battery dedicated to the drive motor.

Such a system could theoretically provide a different power architecture, but it would also require:

```text
additional electrical interface

additional wiring

additional mechanical mounting

additional charging

potentially separate motor-control electronics
```

The current EV3 Large Motor and Medium Motor already belong to the EV3 ecosystem.

Keeping them inside the same system therefore provides a cleaner architecture.

---

## 8.14 Why a Buck Converter Is Not Part of the Current Architecture

Earlier experimental electronics can create situations where voltage conversion becomes necessary.

The current final competition architecture does not depend on a dedicated external buck-converter system.

This reflects the broader simplification that occurred when the current robot moved away from the historical:

```text
HuskyLens
+
Arduino Nano
+
USB bridge
```

configuration.

Reducing external electronics also reduced the number of custom power interfaces required by the vehicle.

---

## 8.15 Current vs. Legacy Power Complexity

Earlier vision experiments introduced more electrical dependencies.

Conceptually:

```text
LEGACY VISION

EV3 system
+
HuskyLens
+
Arduino Nano
+
USB communication
+
additional wiring
```

The current obstacle architecture is simpler:

```text
CURRENT

EV3 system
+
Pixy2.1 on S1
```

The reduction in components improved not only communication architecture but also power-system simplicity.

This demonstrates that hardware simplification can improve several subsystems simultaneously.

---

## 8.16 Power and Communication Should Be Distinguished

A cable can carry:

```text
power
```

and/or:

```text
data
```

but those are different engineering functions.

For example, during obstacle operation, Pixy2.1 must:

```text
operate electrically
```

and:

```text
communicate block information
```

with the EV3.

Documentation should therefore distinguish:

```text
POWER PATH
```

from:

```text
SIGNAL PATH
```

The exact electrical and communication connection belongs in the dedicated power-distribution documentation rather than being duplicated here.

---

## 8.17 Battery Preparation Before Testing

A simple pre-test battery routine improves consistency.

```text
1. Verify battery is installed securely.

2. Confirm EV3 powers on normally.

3. Confirm sufficient charge for the intended test session.

4. Verify motors initialize normally.

5. Verify required sensors initialize.

6. Run basic movement test.

7. Begin calibration or course test.
```

The goal is not to create an unnecessarily complicated battery procedure.

It is to prevent a test from being interpreted incorrectly because the power system was not in a reasonable operating condition.

---

## 8.18 Why Testing With Similar Battery Conditions Matters

Consider two steering tests.

### Test A

```text
same code
same robot
battery condition A
```

### Test B

```text
same code
same robot
different battery condition
```

If physical vehicle speed differs, the turning trajectory can also differ.

That creates an additional uncontrolled variable.

A stronger experiment tries to keep:

```text
hardware

software

battery preparation

track conditions
```

similar while changing only the parameter under investigation.

This is consistent with PiolínTech's broader one-change-at-a-time testing methodology.

---

## 8.19 Battery and Corner Calibration

Piolín uses Ackermann-style steering.

The physical corner depends on:

```text
Motor B steering

Motor A movement

entry geometry

traction
```

If propulsion behavior changes, the resulting curve can also change.

Therefore the team should not calibrate a corner only once under unusual power conditions and assume that it represents every run.

Repeated testing under normal competition preparation conditions provides stronger evidence.

---

## 8.20 Battery and Encoder-Based Motion

Motor encoders measure motor rotation.

They do not directly measure battery performance.

However, battery state can still affect how quickly a requested movement occurs.

For an encoder-terminated movement:

```text
move until encoder reaches target
```

the final rotational target may remain similar while the **time required to reach it** changes.

For a time-based movement:

```text
drive for X seconds
```

a change in vehicle response can directly change the physical distance covered.

This is one reason encoder-based physical conditions can sometimes be more repeatable than purely timed movement.

---

## 8.21 Why Timed Motions Are More Sensitive to Vehicle Conditions

Suppose a program performs:

```text
drive for 1 second
```

The result depends on how far the vehicle physically moves during that second.

That can be influenced by:

```text
motor response

mechanical friction

surface interaction

battery condition
```

By comparison:

```text
move until encoder displacement
```

uses motor motion itself as a stopping reference.

Neither method creates perfect physical odometry, but encoder-based termination can reduce dependence on elapsed time alone.

This distinction is relevant for recovery and parking development.

---

## 8.22 Battery and Troubleshooting

If Piolín behaves unusually, battery condition should be one item in the diagnostic sequence.

However, it should not automatically be blamed.

For example:

```text
vehicle suddenly slower
```

could be caused by:

```text
battery condition

drivetrain friction

wheel rubbing

software speed command

motor problem
```

Similarly:

```text
steering weak
```

could result from:

```text
mechanical binding

Motor B issue

software limit

power condition
```

A useful diagnostic process checks the complete subsystem rather than replacing one explanation with another without evidence.

---

## 8.23 Battery and Repeatability

The purpose of battery management in Piolín is not merely:

```text
keep robot turned on
```

It also contributes to repeatable autonomous testing.

A competition run depends on the interaction between:

```text
software

motors

mechanics

sensors

power
```

Stable preparation makes it easier to determine whether a software change actually improved the robot.

This is particularly important when tuning small differences in:

```text
corner behavior

obstacle reaction

recovery

parking
```

---

## 8.24 Charging and Handling

The EV3 rechargeable battery should be charged and handled according to the normal requirements of the LEGO EV3 battery system.

The repository does not need to reproduce general battery-safety instructions that are already provided by the manufacturer.

For Piolín, the engineering documentation is focused on:

```text
why this battery was selected

how it integrates with the robot

how power condition affects testing

how the architecture avoids unnecessary extra power systems
```

rather than rewriting the complete manufacturer manual.

---

## 8.25 Reproducibility

For another team reproducing Piolín's current architecture, the primary battery requirement is straightforward:

```text
1 × LEGO Mindstorms EV3 Rechargeable DC Battery
Part 45501
```

installed with:

```text
1 × LEGO Mindstorms EV3 Intelligent Brick
```

The current competition vehicle does not require reconstruction of:

```text
external propulsion battery

separate camera battery

Nano power system

HuskyLens power system

external buck-converter rail
```

This significantly reduces the number of electrical subsystems that must be reproduced.

---

## 8.26 Battery Architecture Trade-Offs

| Decision                  | Advantage                          | Trade-Off                                  |
| :------------------------ | :--------------------------------- | :----------------------------------------- |
| EV3 Rechargeable Battery  | Native integration with EV3 system | Vehicle power remains tied to EV3 platform |
| One primary power source  | Simpler charging and wiring        | Less independent subsystem separation      |
| No external motor battery | Reduced electrical complexity      | No dedicated propulsion supply             |
| No separate Pixy battery  | Cleaner obstacle configuration     | Camera depends on current EV3 integration  |
| Rechargeable system       | Reusable during repeated testing   | Requires consistent charging discipline    |

The current solution was selected because its simplicity matches the rest of Piolín's architecture.

---

## 8.27 Values Intentionally Not Claimed as Final

This document intentionally does not invent or infer measurements that have not been verified for Piolín.

The following should only be added if they are measured or taken directly from authoritative manufacturer documentation:

```text
measured battery voltage during a run

measured current draw

measured motor current

measured Pixy current

measured runtime

battery discharge curve

power consumption by subsystem

battery-related speed variation
```

Likewise, no graph such as:

```text
battery_performance_test.png
```

should be added unless actual test data has been collected.

This keeps the repository evidence-based.

---

## 8.28 Battery Test Data That Could Be Added Later

If PiolínTech decides to collect quantitative battery data later, a useful experiment could compare:

```text
battery condition

run duration

Motor A response

straight-line travel

corner behavior
```

across repeated controlled tests.

A proper record would include:

```text
date

software version

battery condition

test configuration

measured result
```

Only after collecting such measurements would it make sense to produce a battery-performance graph.

Until then, qualitative engineering observations should remain clearly identified as qualitative.

---

## 8.29 Current Battery Responsibility Matrix

| Responsibility                                      |  EV3 Battery 45501 |
| :-------------------------------------------------- | :----------------: |
| Primary EV3 power                                   |         Yes        |
| Supports propulsion system through EV3 architecture |         Yes        |
| Supports steering system through EV3 architecture   |         Yes        |
| Used in Open                                        |         Yes        |
| Used in Obstacles                                   |         Yes        |
| Separate external propulsion supply                 |         No         |
| Separate camera battery                             |         No         |
| Requires Arduino Nano supply                        | No, Nano is legacy |
| Main competition power source                       |         Yes        |

The same battery architecture is therefore preserved between both competition rounds.

---

## 8.30 Current Power Philosophy

Piolín's current power philosophy is intentionally simple:

```text
ONE MAIN BATTERY
       ↓
      EV3
       ↓
COMMON VEHICLE PLATFORM
```

The challenge-specific sensing architecture changes:

```text
OPEN
→ Gyro


OBSTACLES
→ Pixy2.1
```

but the main battery platform remains unchanged.

This allows the team to change sensing configuration without redesigning the vehicle's complete energy system.

---

## 8.31 Final Engineering Assessment

The LEGO Mindstorms EV3 Rechargeable DC Battery 45501 was retained because it matches the architecture of the robot rather than forcing the robot to be redesigned around a more complicated power system.

Piolín's current design already centers around the EV3.

The motors are EV3 motors.

The permanent sensors are EV3 sensors.

The Open Gyro Sensor is an EV3 sensor.

The controller itself is the EV3 Brick.

The battery therefore completes a largely unified system.

The current power chain can be summarized as:

```text
EV3 RECHARGEABLE BATTERY 45501
             ↓
          EV3 BRICK
             ↓
 ┌───────────┼────────────┐
 │           │            │
 ▼           ▼            ▼
MOTORS     SENSORS     CONTROL
 │           │            │
 └───────────┴──────┬─────┘
                    ▼
              AUTONOMOUS VEHICLE
```

The design principle is:

> **Piolín uses one primary EV3 power platform because the simplest reliable power architecture is preferable to adding independent supplies that do not provide a necessary competition advantage.**

This also supports reproducibility: another team can reconstruct the primary electrical platform with the EV3 Brick and its standard rechargeable battery rather than recreating several independent power systems.

---

<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
