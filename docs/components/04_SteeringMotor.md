# 4. Steering Motor and Ackermann Actuation

<div align="center">

<img
  src="../../v-photos/v4/motor_b_medium_steering.jpg"
  alt="LEGO EV3 Medium Motor installed as Piolín's steering actuator"
  width="700"
/>

<br>

<sub><b>Figure 4.1.</b> LEGO EV3 Medium Motor connected to Port B and used as Piolín's dedicated steering actuator.</sub>

</div>

Piolín uses a **LEGO Mindstorms EV3 Medium Motor connected to Motor Port B** as the only active actuator in the front steering system. Unlike Motor A, which produces propulsion, Motor B does not directly move the vehicle forward or backward. Its responsibility is to reposition the front steering linkage so that the two front wheels create the curvature required by the autonomous controller.

The current steering architecture is:

```text
EV3
 ↓
Motor Port B
 ↓
EV3 Medium Motor
 ↓
Mechanical steering linkage
 ↓
Left + Right front wheel angles
 ↓
Vehicle curvature
```

This division of responsibilities is fundamental to Piolín's mechanical architecture:

```text
Motor A
→ propulsion


Motor B
→ steering
```

The vehicle therefore behaves as an Ackermann-style car rather than as a differential-drive robot.

The steering system is especially important because every wall correction, corner, obstacle maneuver, recentering action, and parking adjustment eventually becomes a physical Motor B movement.

---

## 4.1 Why a Dedicated Steering Motor Is Used

Piolín separates propulsion and steering mechanically.

A differential-drive robot normally turns by controlling the relative speeds of two drive motors. Piolín instead has one propulsion system and one steering system.

```text
REAR
Motor A
→ vehicle movement


FRONT
Motor B
→ direction of movement
```

This architecture was selected because WRO Future Engineers is fundamentally a vehicle-navigation challenge. A front-steered vehicle produces continuous curved trajectories rather than rotating around its center.

Using a dedicated steering actuator also allows the software to reason independently about:

```text
how fast Piolín should move
```

and:

```text
how strongly Piolín should steer
```

before those two decisions interact physically.

---

## 4.2 Why the EV3 Medium Motor Was Selected

The steering actuator has different mechanical requirements from the propulsion actuator.

Motor A must continuously move the complete vehicle.

Motor B instead performs relatively limited angular movements such as:

```text
left correction

right correction

return to center

corner steering

obstacle avoidance

countersteering
```

The EV3 Medium Motor fits this role because the steering system benefits from a compact actuator capable of controlled position changes.

The selection was therefore based on the physical role:

| Requirement | Motor A | Motor B |
| :--- | :---: | :---: |
| Move complete vehicle | Yes | No |
| Continuous propulsion | Yes | No |
| Angular positioning | Secondary | Primary |
| Rear drivetrain | Yes | No |
| Front steering linkage | No | Yes |
| EV3 Port | A | B |

Using a second Large Motor for steering would add size and mechanical capacity that the current front steering architecture does not require.

---

## 4.3 Ackermann-Style Steering

Motor B operates an **Ackermann-style front steering mechanism**.

<div align="center">

<img
  src="../../v-photos/v4/ackermann_top.jpg"
  alt="Top view of Piolín Ackermann-style steering mechanism"
  width="720"
/>

<br>

<sub><b>Figure 4.2.</b> Top view of Piolín's installed front steering mechanism.</sub>

</div>

During a turn, the left and right front wheels should not necessarily remain at identical angles.

The wheel closer to the center of the turn follows a smaller-radius path than the wheel farther away.

Conceptually:

```text
INNER WHEEL
→ smaller turning radius
→ larger steering angle


OUTER WHEEL
→ larger turning radius
→ smaller steering angle
```

This is the central idea behind Ackermann steering.

Piolín's system is described as **Ackermann-style** rather than claiming mathematically perfect Ackermann geometry. The actual relationship is determined by the LEGO linkage, pivot positions, wheel spacing, and steering-arm geometry installed on the physical robot.

---

## 4.4 Ackermann Geometry

<div align="center">

<img
  src="../../v-photos/v4/ackermann_geometry.png"
  alt="Ackermann steering geometry used to explain Piolín's turning mechanism"
  width="720"
/>

<br>

<sub><b>Figure 4.3.</b> Ackermann geometry showing why the inner and outer front wheels follow different turning radii.</sub>

</div>

The steering geometry can be understood through the relationship between:

```text
wheelbase

front track width

inner wheel angle

outer wheel angle

turning center
```

In an idealized Ackermann model, the extended wheel directions intersect near a common instantaneous center of rotation.

A common geometric relationship can be written as:

```text
cot(δ_outer) - cot(δ_inner)
=
T / L
```

where:

```text
δ_inner
→ inner front-wheel steering angle


δ_outer
→ outer front-wheel steering angle


T
→ front track width


L
→ wheelbase
```

This equation describes the idealized geometry.

Piolín's actual mechanism should still be evaluated experimentally because LEGO linkage clearances and real pivot positions can create differences from the theoretical model.

---

## 4.5 Inner and Outer Steering Angles

<div align="center">

<img
  src="../../v-photos/v4/ackermann_angles.png"
  alt="Inner and outer steering angles in Piolín Ackermann steering"
  width="720"
/>

<br>

<sub><b>Figure 4.4.</b> Relationship between the inner and outer front-wheel angles during an Ackermann-style turn.</sub>

</div>

During a turn:

```text
δ_inner > δ_outer
```

because the inner wheel must follow a tighter radius.

This distinction is important when documenting Piolín because one Motor B position ultimately creates **two different wheel-angle responses**.

Therefore the steering system cannot be described simply as:

```text
Motor B = 20°
therefore
both wheels = 20°
```

That would not correctly describe the installed linkage.

Instead:

```text
Motor B position
        ↓
linkage displacement
        ↓
left wheel angle
+
right wheel angle
```

and which wheel becomes the inner wheel depends on the direction of the turn.

---

## 4.6 Motor B Angle Is Not Wheel Angle

One of the most important steering relationships is:

```text
MOTOR B ENCODER ANGLE
≠
FRONT-WHEEL ANGLE
```

The EV3 measures Motor B rotation through the motor encoder.

That rotational position passes through a mechanical linkage before reaching the wheels.

```text
Motor B
   ↓
linkage input
   ↓
steering arms
   ↓
wheel pivots
   ↓
physical wheel angles
```

The conversion depends on:

```text
link length

connection points

pivot position

steering-arm geometry

mechanical clearance
```

and may not be perfectly linear throughout the steering range.

For this reason, a numerical Motor B command should never be presented as the physical front-wheel angle unless that relationship has been measured on Piolín.

---

## 4.7 Mechanical Center

The steering system requires a repeatable neutral reference.

```text
LEFT
  ←
CENTER
  →
RIGHT
```

The mechanical center is the position at which the front wheels are approximately aligned for straight vehicle motion.

The software can then represent steering relative to that reference.

Conceptually:

```text
STEERING_CENTER
        ↓
0 relative steering error
```

with commands on either side representing left or right steering.

A correct software center does not automatically guarantee straight driving if the physical mechanism is misaligned.

Therefore steering-center verification should include:

```text
Motor B reference

front wheel orientation

linkage symmetry

straight-line vehicle behavior
```

rather than relying only on the motor encoder.

---

## 4.8 Centering Repeatability

A useful steering system should repeatedly return to approximately the same physical wheel position when Motor B returns to its reference.

A basic mechanical test is:

```text
CENTER
  ↓
LEFT
  ↓
CENTER
  ↓
RIGHT
  ↓
CENTER
```

If the final center differs depending on which direction the mechanism approached from, possible causes include:

```text
mechanical backlash

joint clearance

linkage flex

motor-position error

steering friction
```

This matters because Piolín frequently changes steering direction during:

```text
wall correction

corner exit

pillar avoidance

countersteering

recentering
```

A repeatable center makes all of those behaviors easier to tune.

---

## 4.9 Mechanical Play and Backlash

Some clearance is unavoidable in a LEGO Technic steering system.

Potential sources include:

```text
pins

axles

pivot joints

linkage connections

gears
```

When Motor B reverses direction, part of its initial movement may first remove mechanical clearance before producing a visible change at the front wheels.

Conceptually:

```text
Motor B reverses
      ↓
linkage clearance changes side
      ↓
mechanical play is taken up
      ↓
wheel movement begins
```

This becomes particularly important during fast transitions such as:

```text
avoid
→ countersteer
```

because the software may change direction before the mechanical steering system has fully responded.

The current documentation therefore does not claim:

```text
zero backlash
```

or:

```text
perfect steering repeatability
```

The goal is instead to keep mechanical play low enough for repeatable autonomous control.

---

## 4.10 Mechanical Steering Range

Motor B cannot rotate indefinitely while connected to the steering mechanism.

The linkage has a physically useful range.

Beyond that range, additional Motor B movement may produce:

```text
little useful wheel-angle increase

mechanical binding

higher motor load

structural stress
```

The software should therefore define a **usable steering range** rather than attempting to drive the mechanism to its absolute mechanical stop.

Conceptually:

```text
LEFT LIMIT
     │
     │ usable range
     │
CENTER
     │
     │ usable range
     │
RIGHT LIMIT
```

The final numerical limits should only be published after the current V4 steering system is physically measured.

---

## 4.11 Why Maximum Steering Is Not Always Better

A larger steering command creates a tighter intended trajectory only up to the point where the mechanical and tire geometry remain useful.

Excessive steering can increase:

```text
tire scrub

rolling resistance

mechanical load

trajectory instability
```

It can also make recovery more difficult because Motor B must travel farther before reaching the opposite steering direction.

For example:

```text
large avoidance angle
        ↓
pillar cleared quickly
        ↓
but...
        ↓
large countersteering movement required
```

The best steering command is therefore not automatically the largest available command.

It is the smallest command that reliably produces the required trajectory with adequate clearance.

---

## 4.12 Steering Motion

<div align="center">

<img
  src="../../v-photos/v4/steering_motion.gif"
  alt="Physical movement of Piolín front steering system"
  width="680"
/>

<br>

<sub><b>Figure 4.5.</b> Physical movement of the current steering linkage through its operating range.</sub>

</div>

The animation provides useful physical evidence of how Motor B changes both front wheel orientations through the linkage.

It demonstrates:

```text
coordinated wheel motion

movement through center

direction reversal

real linkage behavior
```

The animation is more useful than a purely conceptual diagram because it shows the actual mechanism that Piolín's software controls.

It should not, however, be interpreted as proof of ideal theoretical Ackermann geometry.

---

## 4.13 Steering Requires Vehicle Motion

Unlike differential drive, Piolín cannot rotate meaningfully in place by simply changing the steering angle.

Ackermann steering produces a curved vehicle trajectory only when the vehicle also moves.

```text
Motor B changes wheel angle
        +
Motor A moves vehicle
        ↓
Piolín turns
```

This relationship is fundamental.

If Motor B turns while Motor A is stopped:

```text
wheel orientation changes
```

but:

```text
vehicle heading does not immediately change
```

The robot must translate forward or backward for the steering geometry to create a change in position and orientation.

This is why propulsion speed and steering response must be tuned together.

---

## 4.14 Steering and Speed Interaction

The same Motor B position can produce different practical behavior depending on how quickly Piolín is moving.

At greater forward speed:

```text
same steering geometry
+
more vehicle movement per unit time
```

can make the trajectory develop more quickly.

At lower speed:

```text
more time for sensing and correction
```

is available, but the vehicle also develops its Ackermann trajectory more slowly.

This creates a trade-off:

```text
TOO FAST
→ less reaction time
→ larger correction distance


TOO SLOW
→ slower trajectory development
→ inefficient maneuver
```

The objective is therefore not to independently find:

```text
best steering
```

and:

```text
best speed
```

but to find a useful combination of both.

---

## 4.15 Steering During Straight Navigation

During a stable straight section, Motor B should remain relatively close to the steering center.

The navigation system then makes smaller corrections based on the active sensor architecture.

During Open:

```text
S2/S3
→ lateral geometry


Gyro
→ heading information
```

The EV3 converts those measurements into a steering correction around the center reference.

Conceptually:

```text
STEERING =
CENTER
+
CORRECTION
```

The correction should be strong enough to prevent growing positional or heading error but not so aggressive that Piolín repeatedly crosses its desired trajectory.

---

## 4.16 Zig-Zag and Steering Overcorrection

A recurring prototype failure was zig-zag motion.

A common sequence was:

```text
error detected
      ↓
strong steering correction
      ↓
vehicle crosses desired path
      ↓
error changes sign
      ↓
strong opposite correction
      ↓
repeat
```

This can be caused by several factors:

```text
steering gain too high

vehicle speed too high

mechanical backlash

sensor noise

multiple controllers competing

late correction
```

Therefore zig-zag should not automatically be solved by changing Motor B limits.

The source of the oscillation must first be identified.

---

## 4.17 Steering During Open Corners

Open corners require a stronger and more deliberate steering state than normal straight-line correction.

Conceptually:

```text
STRAIGHT
   ↓
corner evidence detected
   ↓
CORNER STATE
   ↓
Motor B moves to larger steering request
   ↓
Motor A moves vehicle through arc
   ↓
turn progresses
   ↓
Motor B returns toward center
   ↓
straight geometry reacquired
```

The current Open architecture can use gyro information to support turn progress while the lateral ultrasonic sensors help verify when useful wall geometry returns.

This is more robust than assuming that one fixed Motor B position held for one fixed time will always generate exactly the same physical turn.

---

## 4.18 Why Timed Steering Alone Is Limited

A purely timed turn might behave as:

```text
Motor B = turn
Motor A = drive
wait X seconds
Motor B = center
```

This can work during controlled tests, but its physical result depends on:

```text
battery condition

vehicle speed

friction

entry position

entry heading

steering response
```

Therefore:

```text
same time
≠
guaranteed same orientation
```

The current Open architecture benefits from the Gyro Sensor because the software can observe actual vehicle rotation rather than relying only on elapsed time.

---

## 4.19 Steering During Obstacle Avoidance

During the Obstacle Challenge, Motor B remains the same actuator, but the information driving its command changes.

Pixy2.1 determines important visual characteristics of the target.

```text
RED
→ pass RIGHT


GREEN
→ pass LEFT
```

However:

```text
RED
```

does not mean:

```text
set Motor B permanently to maximum right
```

and Green does not imply one permanent maximum-left angle.

The desired steering can depend on:

```text
target X position

target apparent size

current wall geometry

vehicle speed

current obstacle state
```

The steering system therefore converts a perception objective into a controlled vehicle trajectory rather than a simple color-to-angle command.

---

## 4.20 Countersteering

Once Piolín has moved around a pillar, Motor B must usually transition toward an opposite steering direction or toward center.

This is **countersteering**.

```text
AVOID
   ↓
vehicle moves around pillar
   ↓
PASS
   ↓
countersteer
   ↓
recover heading / lateral position
```

Countersteering is important because the avoidance steering that created clearance from the pillar also leaves Piolín laterally displaced.

Without recovery, the robot may:

```text
approach a wall

enter next corner poorly

misalign the camera

reduce visibility of next pillar
```

The timing of countersteering is therefore closely tied to pass confirmation and recovery logic.

---

## 4.21 Why Early Countersteering Fails

If Motor B begins countersteering before Piolín has physically cleared the pillar:

```text
vehicle begins returning
      ↓
pillar still alongside
      ↓
clearance decreases again
      ↓
possible collision
```

This is one reason:

```text
camera target disappeared
```

cannot automatically mean:

```text
countersteer now
```

The pillar may have left the camera's field of view because Piolín itself rotated.

During obstacle development, lateral ultrasonic context became useful for determining whether the physical obstacle had actually been passed.

---

## 4.22 Why Late Countersteering Fails

The opposite problem occurs when recovery begins too late.

```text
pillar passed
      ↓
avoidance steering continues
      ↓
vehicle moves farther laterally
      ↓
wall becomes close
      ↓
strong recovery required
```

This can produce another oscillation.

The desired maneuver therefore balances:

```text
enough avoidance to clear pillar
```

with:

```text
early enough recovery to preserve track geometry
```

Motor B performance is consequently linked directly to obstacle-state timing.

---

## 4.23 Steering and Camera Geometry

During Obstacles, changing Piolín's steering also changes the orientation of the entire camera.

```text
Motor B steering
      ↓
vehicle begins rotating
      ↓
Pixy viewpoint rotates
      ↓
pillar X position changes
```

This means some apparent target movement in the camera is caused by Piolín itself.

A pillar can also leave the field of view before it has been physically passed.

The steering and vision systems therefore cannot be designed as completely independent subsystems.

Motor B changes both:

```text
vehicle trajectory
```

and:

```text
camera viewing direction
```

during the maneuver.

---

## 4.24 Steering and Ultrasonic Geometry

Motor B also affects the geometry measured by the lateral ultrasonic sensors.

While Piolín is aligned with a wall, a lateral sensor has a relatively direct geometric relationship with that wall.

When the chassis rotates:

```text
sensor direction rotates too
```

and the measured distance may change even before the vehicle has translated significantly.

Therefore a rapid ultrasonic change during a strong steering maneuver does not necessarily mean that Piolín instantly moved the same physical distance sideways.

This interaction is considered when designing wall recovery and corner logic.

---

## 4.25 Mechanical Friction

Motor B performance depends strongly on the mechanical resistance of the steering system.

Potential sources include:

```text
tight pivots

wheel friction

linkage misalignment

axle friction

structural contact

cables interfering with steering
```

If steering appears slow or weak, the first response should not automatically be:

```text
increase Motor B command
```

A stronger software command can hide a mechanical problem while increasing motor load.

The preferred diagnostic sequence is:

```text
inspect mechanism
      ↓
verify free movement
      ↓
verify Motor B response
      ↓
verify physical wheel response
      ↓
then tune control
```

---

## 4.26 Structural Rigidity

The steering system must also remain structurally stable.

If Motor B is firmly mounted but the surrounding Technic structure flexes:

```text
Motor B moves
      ↓
support structure moves
      ↓
part of actuator motion becomes chassis deformation
      ↓
wheel response changes
```

This reduces steering repeatability.

The steering motor mount, linkage supports, and front wheel pivots must therefore work as one mechanical assembly.

A control algorithm can only be calibrated reliably if this mechanical relationship remains stable between runs.

---

## 4.27 Left/Right Symmetry

Theoretical steering geometry may suggest symmetrical behavior between left and right turns.

The physical LEGO mechanism may not be perfectly symmetrical because of:

```text
linkage placement

mechanical play

component mounting

cable routing

friction
```

Therefore:

```text
same Motor B magnitude left
```

does not automatically guarantee:

```text
exact mirror of same magnitude right
```

The final steering calibration should verify both directions independently.

If real measurements show a consistent asymmetry, software can account for it after the mechanical structure has first been checked.

---

## 4.28 Steering Calibration Procedure

A practical calibration sequence for the current V4 steering system is:

```text
1. Verify linkage moves freely.

2. Find physical straight-wheel position.

3. Associate that position with STEERING_CENTER.

4. Move Motor B progressively left.

5. Determine useful left limit.

6. Return to center.

7. Move progressively right.

8. Determine useful right limit.

9. Repeat center-return tests.

10. Measure actual wheel angles if required.

11. Perform slow straight-driving test.

12. Perform controlled left/right curve tests.
```

The process should be performed on the actual competition configuration rather than relying on old V3 steering values.

---

## 4.29 Measuring Wheel Angles

The new steering-angle documentation allows Piolín to distinguish between:

```text
Motor B encoder position
```

and:

```text
actual wheel geometry
```

A useful measurement set can record:

| Motor B Position | Inner Wheel Angle | Outer Wheel Angle | Direction |
| :---: | :---: | :---: | :--- |
| — | — | — | Left |
| — | — | — | Left |
| Center | Approx. 0 | Approx. 0 | Straight |
| — | — | — | Right |
| — | — | — | Right |

The table should only be completed with physically measured V4 values.

Once those measurements exist, they can help establish:

```text
Motor B position
        ↓
actual steering geometry
        ↓
estimated vehicle curvature
```

without falsely assuming a one-to-one relationship.

---

## 4.30 Turning Radius

The steering geometry ultimately determines vehicle curvature.

For a simplified bicycle-model approximation:

```text
R ≈ L / tan(δ)
```

where:

```text
R
→ approximate turning radius


L
→ wheelbase


δ
→ equivalent steering angle
```

For a real Ackermann vehicle, the inner and outer wheels have different angles, so the complete geometry is more detailed.

The simplified expression is still useful for understanding the physical trend:

```text
larger steering angle
→ smaller turning radius


smaller steering angle
→ larger turning radius
```

The final Piolín turning radius should be measured physically rather than published from theoretical geometry alone.

---

## 4.31 Alternative Steering Architectures

Several other steering architectures could theoretically have been used.

| Architecture | Advantage | Limitation for Piolín |
| :--- | :--- | :--- |
| Differential drive | Simple turning control | Does not match selected vehicle architecture |
| Two-wheel skid steering | Can rotate sharply | Different WRO vehicle behavior and tire interaction |
| Hobby servo steering | Compact positional actuator | Requires additional non-EV3 integration |
| Large EV3 Motor steering | Higher torque | Larger than required for current mechanism |
| **EV3 Medium Motor + Ackermann-style linkage** | **Native EV3 integration and car-like steering** | **Requires mechanical linkage calibration** |

The selected system keeps Piolín inside the EV3 motor ecosystem while producing the vehicle-like front steering behavior required by the design.

---

## 4.32 Why a Hobby Servo Was Not Used

A conventional hobby servo can be very effective for vehicle steering.

However, using one would require an additional integration method between:

```text
EV3
```

and:

```text
servo electronics
```

The current Medium Motor already provides:

```text
EV3 compatibility

position feedback

software control

mechanical integration
```

without another motor controller or power interface.

The servo alternative could reduce actuator size, but it would also increase electrical and software integration complexity.

The current Medium Motor was therefore retained.

---

## 4.33 Why Differential Steering Was Not Used

Differential steering could simplify the mechanical front axle because the robot would not require a steering linkage.

However, it would fundamentally change Piolín's vehicle behavior.

A differential robot controls turning through:

```text
left-wheel speed
vs.
right-wheel speed
```

Piolín instead controls:

```text
rear propulsion
+
front steering
```

The Ackermann-style architecture provides a more car-like trajectory and aligns better with the mechanical concept chosen for Future Engineers.

The team therefore accepted the additional mechanical steering complexity in exchange for vehicle-like motion.

---

## 4.34 Values Intentionally Not Claimed as Final

The following steering values should not be published as final until they have been physically measured on the current V4 mechanism:

```text
Motor B mechanical center value

usable left Motor B limit

usable right Motor B limit

maximum inner-wheel angle

maximum outer-wheel angle

Motor B angle-to-wheel-angle relationship

front track width

exact wheelbase

minimum turning radius

left/right steering asymmetry

measured backlash

steering response time
```

Historical estimates or values from previous robot versions should not automatically become current specifications.

The current architecture is documented now, while the final numerical calibration can be added after measurement.

---

## 4.35 Final Steering Architecture

Piolín's steering system can be summarized as:

```text
                      LEGO EV3
                         │
                         ▼
                       PORT B
                         │
                         ▼
                EV3 MEDIUM MOTOR
                         │
                         ▼
                STEERING LINKAGE
                     ┌───┴───┐
                     │       │
                     ▼       ▼
                  LEFT     RIGHT
                  WHEEL     WHEEL
                     │       │
                     └───┬───┘
                         ▼
                  VEHICLE CURVATURE
```

The EV3 therefore does not directly control vehicle heading.

It controls Motor B.

Motor B controls the steering linkage.

The linkage controls the front wheels.

The front-wheel geometry combines with Motor A propulsion to create the physical trajectory.

This layered relationship explains why software, motor calibration, mechanical linkage design, and vehicle speed must all be considered together.

---

## 4.36 Final Engineering Assessment

The EV3 Medium Motor was retained as Piolín's steering actuator because it provides a simple and fully EV3-integrated method of controlling a car-like front steering system.

Its role is clearly separated from propulsion:

```text
Motor A
→ move vehicle


Motor B
→ shape vehicle trajectory
```

The steering mechanism also demonstrates an important distinction between actuator state and vehicle geometry:

```text
MOTOR POSITION
        ↓
MECHANICAL LINKAGE
        ↓
WHEEL ANGLES
        ↓
TRAJECTORY
```

This means that successful steering cannot be achieved through software values alone.

The mechanical center must be repeatable.

The linkage must move freely.

The structure must remain rigid.

The usable limits must be calibrated.

The inner and outer wheel angles must be understood separately.

The software must coordinate steering with vehicle speed.

The final design principle is therefore:

> **Piolín's steering system is treated as a complete electromechanical subsystem, not simply as Motor B. Reliable autonomous steering depends on the relationship between the EV3 command, Medium Motor position, Ackermann linkage, wheel geometry, and actual vehicle movement.**

---

<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
