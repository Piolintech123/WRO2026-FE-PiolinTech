# 3. Robot Mobility

<div align="center">

<img
  src="../../v-photos/v4/piolin_open_isometric.jpg"
  alt="Piolín complete mobility platform in the Open Challenge configuration"
  width="720"
/>

<br>

<sub><b>Figure 3.1.</b> Piolín's current vehicle platform combines rear propulsion with front Ackermann-style steering.</sub>

</div>

Piolín is designed as a four-wheel autonomous vehicle in which **propulsion and steering are handled by separate actuators**. An EV3 Large Motor connected to Motor Port A generates the motion required to move the robot forward or backward, while an EV3 Medium Motor connected to Motor Port B controls the front steering system.

The fundamental mobility architecture is therefore:

```text
Motor A
→ propulsion

Motor B
→ steering
```

Rather than turning by driving the left and right sides at different speeds, Piolín behaves more like a small conventional vehicle. The rear section provides propulsion while the front wheels change their orientation to generate the required curvature.

This architecture is used for both the **Open Challenge** and the **Obstacle Challenge**. The mechanical mobility platform remains the same; what changes between rounds is primarily the sensing and navigation logic that decides what Motor A and Motor B should do.

---

## 3.1 Mobility as a Complete System

Vehicle movement is not produced by one component alone. It results from the interaction between the controller, motors, drivetrain, steering mechanism, wheels, structure, surface, and navigation software.

The complete relationship can be simplified as:

```text
EV3
 │
 ├── Motor A
 │      ↓
 │   drivetrain
 │      ↓
 │   rear wheels
 │      ↓
 │   longitudinal movement
 │
 └── Motor B
        ↓
     steering linkage
        ↓
     front wheels
        ↓
     vehicle curvature
```

The two paths remain mechanically distinct but interact dynamically.

For example, a steering position that produces a controlled maneuver at low vehicle speed can generate a very different trajectory when Motor A is driving faster. Likewise, increasing propulsion speed reduces the physical time available for the steering mechanism to react before Piolín reaches a corner or obstacle.

Piolín's mobility must therefore be understood as the combination of:

```text
propulsion
+
steering
+
mechanical geometry
+
traction
+
control timing
```

rather than as two isolated motor commands.

---

## 3.2 Rear-Wheel Propulsion

<div align="center">

<img
  src="../../v-photos/v4/motor_a_large_drive.jpg"
  alt="EV3 Large Motor A installed as Piolín's propulsion motor"
  width="660"
/>

<br>

<sub><b>Figure 3.2.</b> Motor A is the dedicated propulsion actuator in Piolín's current mobility architecture.</sub>

</div>

Piolín uses the **EV3 Large Motor on Port A** as its drive motor. Its purpose is to generate the rotational motion that ultimately moves the robot along the track.

The propulsion path is:

```text
EV3
 ↓
Motor A
 ↓
rear drivetrain
 ↓
rear wheels
 ↓
track surface
 ↓
vehicle displacement
```

The motor can operate in both rotational directions, allowing the vehicle to move forward and backward without requiring a mechanical reversing gearbox.

Forward movement is used for the majority of the autonomous run, while reverse movement can be used when a particular maneuver requires additional physical repositioning, recovery distance, or parking adjustment.

---

## 3.3 Rear Drivetrain

<div align="center">

<img
  src="../../v-photos/v4/rear_drivetrain_top.jpg"
  alt="Piolín rear drivetrain viewed from above"
  width="700"
/>

<br>

<sub><b>Figure 3.3.</b> Current rear drivetrain transferring Motor A rotation toward the driven wheels.</sub>

</div>

The rear drivetrain is the mechanical link between the Large Motor and the driven wheels.

Its purpose is not only to transmit rotation but also to preserve alignment and minimize unnecessary resistance while the vehicle is moving.

The physical chain is:

```text
Motor rotation
      ↓
drivetrain elements
      ↓
rear-wheel rotation
      ↓
tire-track interaction
      ↓
vehicle movement
```

A drivetrain that becomes misaligned or develops excessive friction can make the vehicle appear slower even when the software and Motor A command have not changed.

This is why mobility testing should distinguish between:

```text
software behavior
```

and:

```text
mechanical resistance
```

before changing motor-control values.

<div align="center">

<img
  src="../../v-photos/v4/rear_drivetrain_bottom.jpg"
  alt="Bottom view of Piolín rear drivetrain"
  width="700"
/>

<br>

<sub><b>Figure 3.4.</b> Bottom view of the drivetrain and rear mechanical support structure.</sub>

</div>

The exact drivetrain ratio should only be published after the final V4 configuration has been physically verified. Earlier mechanical values should not automatically be transferred to the current robot.

---

## 3.4 Rear Wheels and Traction

<div align="center">

<img
  src="../../v-photos/v4/rear_wheels.jpg"
  alt="Piolín rear propulsion wheels"
  width="660"
/>

<br>

<sub><b>Figure 3.5.</b> Rear wheels responsible for transferring propulsion force to the competition surface.</sub>

</div>

The rear wheels convert drivetrain rotation into longitudinal vehicle movement.

In an ideal model:

```text
wheel rotation
→ equivalent vehicle displacement
```

but a real vehicle can experience:

```text
wheel slip

tire deformation

track-surface variation

mechanical resistance

changes in vehicle load

cornering forces
```

Therefore motor or wheel rotation is a useful movement reference but should not automatically be interpreted as perfect physical displacement.

This becomes particularly important when encoder measurements are used during controlled forward motion, reverse movement, or parking.

---

## 3.5 Dedicated Front Steering

<div align="center">

<img
  src="../../v-photos/v4/motor_b_medium_steering.jpg"
  alt="EV3 Medium Motor B installed as Piolín's steering actuator"
  width="660"
/>

<br>

<sub><b>Figure 3.6.</b> Motor B provides the rotational input to the front steering mechanism.</sub>

</div>

Piolín uses an **EV3 Medium Motor on Port B** to control direction.

Motor B does not propel the vehicle. Instead, it changes the front-wheel orientation through a mechanical linkage.

The steering path is:

```text
EV3
 ↓
Motor B
 ↓
steering transmission
 ↓
linkage
 ↓
front wheel orientation
 ↓
vehicle curvature
```

This separation provides a clear division of responsibilities:

```text
Motor A
→ how Piolín moves longitudinally

Motor B
→ how Piolín changes direction
```

The actual trajectory is created by both working together.

---

## 3.6 Ackermann-Style Steering

<div align="center">

<img
  src="../../v-photos/v4/ackermann_top.jpg"
  alt="Top view of Piolín Ackermann-style steering system"
  width="700"
/>

<br>

<sub><b>Figure 3.7.</b> Top view of the current front steering mechanism.</sub>

</div>

Piolín uses an **Ackermann-style steering geometry** rather than differential or skid steering.

During a turn, the inner front wheel follows a smaller-radius path than the outer front wheel. The two wheels therefore should not remain at exactly the same steering angle.

The principle is:

```text
INNER WHEEL
→ tighter trajectory
→ larger steering angle

OUTER WHEEL
→ wider trajectory
→ smaller steering angle
```

<div align="center">

<img
  src="../../v-photos/v4/ackermann_design.png"
  alt="Piolín Ackermann steering design"
  width="780"
/>

<br>

<sub><b>Figure 3.8.</b> Ackermann steering design used to coordinate the different trajectories of the inner and outer front wheels.</sub>

</div>

This configuration reduces the need for the front tires to scrub laterally against the surface during normal turns.

It also allows Piolín to behave as a vehicle with a defined steering curvature instead of rotating primarily through opposite wheel speeds.

---

## 3.7 Steering Angles

<div align="center">

<img
  src="../../v-photos/v4/ackermann_angles.jpg"
  alt="Piolín Ackermann steering angle reference"
  width="720"
/>

<br>

<sub><b>Figure 3.9.</b> Steering-angle reference for the Ackermann-style front geometry.</sub>

</div>

One important distinction is that the EV3 controls the angular position of **Motor B**, but vehicle motion depends on the actual orientation of the **front wheels**.

Therefore:

```text
Motor B encoder angle
≠
physical wheel steering angle
```

unless the relationship has been physically measured.

The linkage converts one quantity into the other.

Its behavior depends on factors such as:

```text
connection points

link lengths

pivot geometry

mechanical clearance

structural alignment
```

For this reason, steering values in software should be treated as actuator commands rather than direct measurements of wheel angle.

---

## 3.8 Mechanical Steering Center

<div align="center">

<img
  src="../../v-photos/v4/ackermann_center.jpg"
  alt="Piolín front wheels in the centered steering position"
  width="680"
/>

<br>

<sub><b>Figure 3.10.</b> Current mechanical steering-center position.</sub>

</div>

Straight-line mobility depends on having a repeatable steering center.

Ideally:

```text
Motor B center
      ↓
linkage centered
      ↓
front wheels approximately straight
      ↓
minimal mechanical steering bias
```

If the front wheels are not mechanically centered, Piolín may continuously drift even when the software requests neutral steering.

For that reason, the preferred calibration order is:

```text
mechanical alignment
      ↓
steering-center verification
      ↓
low-speed straight test
      ↓
software fine adjustment
```

rather than using software immediately to compensate for a large mechanical offset.

---

## 3.9 Left and Right Steering Range

<div align="center">

<img
  src="../../v-photos/v4/ackermann_left_lock.jpg"
  alt="Piolín steering at the useful left limit"
  width="640"
/>

<br>

<sub><b>Figure 3.11.</b> Left steering limit of the current V4 mechanism.</sub>

</div>

<div align="center">

<img
  src="../../v-photos/v4/ackermann_right_lock.jpg"
  alt="Piolín steering at the useful right limit"
  width="640"
/>

<br>

<sub><b>Figure 3.12.</b> Right steering limit of the current V4 mechanism.</sub>

</div>

The useful steering range should remain inside the physical limits of the linkage.

A motor can sometimes continue attempting to rotate even after the mechanism has reached a practical mechanical stop. That condition is undesirable because it can increase motor load and stress the steering assembly without creating additional useful wheel angle.

The software limits should therefore be based on the **usable physical steering range**, not simply the maximum rotational capability of Motor B.

Left and right limits also should not be assumed to be perfectly symmetrical until measured.

---

## 3.10 Dynamic Steering Movement

<div align="center">

<img
  src="../../v-photos/v4/steering_motion.gif"
  alt="Piolín steering mechanism moving between left center and right"
  width="700"
/>

<br>

<sub><b>Figure 3.13.</b> Complete steering movement from one side through center to the opposite side.</sub>

</div>

The dynamic movement demonstrates that steering is not instantaneous.

The sequence is:

```text
EV3 changes command
      ↓
Motor B begins rotating
      ↓
linkage moves
      ↓
front-wheel angles change
      ↓
vehicle trajectory begins changing
```

During this time, Motor A may still be moving Piolín forward.

Therefore the physical delay between a software decision and the final wheel position directly affects:

```text
corner entry

obstacle reaction

countersteering

recovery

parking
```

---

## 3.11 Steering and Speed Are Coupled

One of the most important mobility relationships in Piolín is the interaction between propulsion speed and steering response.

Consider the same Motor B target position in two conditions.

```text
LOWER SPEED
→ Piolín travels less distance while steering develops
```

```text
HIGHER SPEED
→ Piolín travels more distance while steering develops
```

The same steering command can therefore produce different practical trajectories.

This means corner tuning cannot be reduced to:

```text
find one steering angle
```

The system must also consider:

```text
vehicle speed

steering response time

entry position

entry heading

duration of steering

release timing
```

---

## 3.12 Straight-Line Mobility

During a straight section, the desired mechanical state is approximately:

```text
Motor A
→ stable propulsion

Motor B
→ close to center
```

with steering corrections added only when the navigation system determines that they are necessary.

Repeated large left-right corrections produce a less efficient trajectory:

```text
left correction
      ↓
overshoot
      ↓
right correction
      ↓
overshoot
      ↓
zig-zag
```

A well-behaved mobility controller should therefore make corrections early enough and smoothly enough that the robot does not continuously cross its desired path.

<div align="center">

<img
  src="../../v-photos/v4/Piolin_open_front.jpeg"
  alt="Front view of Piolín in the Open Challenge configuration"
  width="680"
/>

<br>

<sub><b>Figure 3.14.</b> Front view of Piolín showing the relationship between the front steering geometry and the vehicle centerline.</sub>

</div>

Straight-line drift can originate from both mechanical and software causes.

Mechanical causes include:

```text
incorrect steering center

wheel alignment

drivetrain resistance

structural asymmetry
```

Software causes can include:

```text
excessive steering correction

incorrect control sign

sensor interpretation

delayed correction
```

The mechanical system should be checked before compensating for persistent drift entirely through software.

---

## 3.13 Vehicle Turning

A simplified vehicle model relates wheelbase and steering angle to turning radius:

```text
R ≈ L / tan(δ)
```

where:

```text
R
= approximate turning radius

L
= wheelbase

δ
= representative steering angle
```

The equation demonstrates the general relationship:

```text
smaller steering angle
→ wider turn

larger steering angle
→ tighter turn
```

However, Piolín uses a real four-wheel chassis with Ackermann geometry, mechanical linkage, finite track width, tire deformation, and non-ideal surfaces.

The equation is therefore useful for understanding the trend but should not replace physical turning-radius measurements.

---

## 3.14 Open Challenge Mobility

The Open Challenge uses the same mechanical mobility system shown throughout this document.

What changes is the sensing information used to determine the steering command.

The active sensing architecture is:

```text
S1
→ Gyro

S2
→ Left Ultrasonic

S3
→ Right Ultrasonic

S4
→ Color Sensor
```

During straight sections, the lateral ultrasonic sensors primarily describe track-relative position while the gyro provides vehicle-orientation information.

Motor B can then make relatively small corrections while Motor A maintains forward propulsion.

The Color Sensor provides course-state landmarks and determines the initial course direction.

The mobility system itself remains:

```text
rear propulsion
+
front steering
```

regardless of which sensor triggered the current correction.

---

## 3.15 Open Challenge Corners

Corners require a temporary transition from low-curvature straight driving to a stronger steering state.

A useful conceptual sequence is:

```text
stable straight
      ↓
corner evidence detected
      ↓
Motor B increases steering
      ↓
Piolín begins changing heading
      ↓
corner progresses
      ↓
steering begins returning
      ↓
new wall geometry acquired
      ↓
stable straight
```

A successful corner must accomplish more than approximately rotating the robot.

Piolín should also leave the corner in a useful position and orientation for the next straight.

A robot could complete the angular rotation but still exit:

```text
too close to the inner wall

too close to the outer wall

with excessive residual steering

at an unstable heading
```

Therefore corner **exit geometry** is just as important as corner entry.

---

## 3.16 Clockwise and Counterclockwise Mobility

The Open Challenge can begin in either navigation direction.

The first valid floor color establishes the course direction:

```text
BLUE first
→ counterclockwise

ORANGE first
→ clockwise
```

The drivetrain does not change.

The steering hardware does not change.

Instead, the interpretation of the lateral geometry changes.

For counterclockwise driving:

```text
S2 LEFT
→ inner side

S3 RIGHT
→ outer side
```

For clockwise driving:

```text
S3 RIGHT
→ inner side

S2 LEFT
→ outer side
```

This is a software interpretation of fixed hardware.

The physical sensor mapping always remains:

```text
S2 = LEFT

S3 = RIGHT
```

---

## 3.17 Obstacle Challenge Mobility

The mechanical vehicle is unchanged during the Obstacle Challenge.

The specialized sensing configuration changes to:

```text
S1
→ Pixy2.1

S2
→ Left Ultrasonic

S3
→ Right Ultrasonic

S4
→ Color Sensor
```

Pixy2.1 identifies the relevant obstacle and provides image-position information, while the lateral ultrasonic sensors continue describing the surrounding track geometry.

Motor A remains the propulsion actuator.

Motor B remains the steering actuator.

This is a significant engineering advantage because the team can develop a completely different navigation strategy without rebuilding the vehicle's mobility system.

---

## 3.18 Obstacle Avoidance as a Vehicle Trajectory

Obstacle avoidance is not simply:

```text
see color
→ turn
```

The vehicle must generate a complete trajectory around the pillar.

A more accurate sequence is:

```text
detect target
      ↓
approach
      ↓
create lateral displacement
      ↓
pass correct side
      ↓
clear pillar
      ↓
countersteer
      ↓
recover track geometry
```

The obstacle color determines the required passing side:

```text
RED
→ pass RIGHT

GREEN
→ pass LEFT
```

but the steering system must still determine how to create that trajectory physically.

---

## 3.19 Red Pillar Mobility

<div align="center">

<img
  src="../../v-photos/v4/obstacle_red_run.jpg"
  alt="Piolín performing a red pillar obstacle maneuver"
  width="700"
/>

<br>

<sub><b>Figure 3.15.</b> Piolín executing a red-pillar maneuver during Obstacle Challenge testing.</sub>

</div>

For a red pillar, the required objective is:

```text
pass on the RIGHT
```

This should not be interpreted as holding maximum right steering continuously.

A useful maneuver can contain:

```text
initial steering

controlled pass

pillar clearance

opposite steering

recovery
```

The exact steering magnitude and timing depend on the vehicle's current speed, approach position, obstacle position, and surrounding track geometry.

---

## 3.20 Green Pillar Mobility

<div align="center">

<img
  src="../../v-photos/v4/obstacle_green_run.jpg"
  alt="Piolín performing a green pillar obstacle maneuver"
  width="700"
/>

<br>

<sub><b>Figure 3.16.</b> Piolín executing a green-pillar maneuver during Obstacle Challenge testing.</sub>

</div>

For a green pillar:

```text
pass on the LEFT
```

The conceptual maneuver mirrors the red objective, but the final left and right control values should not automatically be assumed to be numerically identical.

A real mechanical system can contain small asymmetries in:

```text
steering linkage

pivot resistance

wheel alignment

approach geometry
```

Therefore both maneuver directions should be validated physically.

---

## 3.21 Countersteering and Recovery

After Piolín creates lateral displacement to pass an obstacle, it must reduce that lateral motion before reaching the track boundary or the next pillar.

This requires countersteering.

Conceptually:

```text
avoidance steering
      ↓
vehicle moves around pillar
      ↓
pillar clears
      ↓
steering reverses direction
      ↓
vehicle heading recovers
      ↓
Motor B approaches normal steering range
```

The countersteering phase is essential because successfully passing one obstacle is not enough.

Piolín must finish the maneuver in a state that allows it to continue navigating.

A vehicle that passes the current pillar but exits directly toward a wall has not completed a successful obstacle maneuver.

---

## 3.22 Why Recovery Matters

The state after a maneuver affects the next maneuver.

For example:

```text
poor obstacle exit
      ↓
poor next approach position
      ↓
larger next steering correction
      ↓
reduced margin
```

This creates a chain of errors even if the first obstacle was technically passed.

A more useful mobility objective is therefore:

```text
pass obstacle
+
recover
+
prepare for next section
```

rather than optimizing each obstacle independently.

---

## 3.23 Reverse Mobility

Because Motor A can rotate in both directions, Piolín can execute controlled reverse movement.

Reverse can support:

```text
repositioning

recovery

increased maneuvering space

parking
```

but it should not be treated as a universal solution for navigation errors.

Every reversal:

```text
takes time

changes track geometry

changes steering behavior

changes sensor observations
```

Therefore a reverse maneuver should have a defined purpose and a clear completion condition.

---

## 3.24 Encoder-Based Movement

The EV3 motor encoder provides a rotational reference that can be used to estimate vehicle displacement.

The theoretical relationship for a wheel-driven system is:

```text
distance =
(encoder rotation / 360°)
×
wheel circumference
```

or:

```text
distance =
(encoder rotation / 360°)
×
π × D
```

where:

```text
D
= effective driven-wheel diameter
```

This relationship can support:

```text
controlled forward movement

reverse displacement

parking

relative motion testing
```

However, it remains an estimate because:

```text
wheel slip

tire deformation

turning

surface variation
```

can create a difference between calculated wheel travel and actual vehicle displacement.

For this reason, Piolín does not treat simple encoder conversion as perfect global odometry.

---

## 3.25 Parking Mobility

<div align="center">

<img
  src="../../v-photos/v4/parking_area.jpg"
  alt="Parking area used for Piolín autonomous testing"
  width="700"
/>

<br>

<sub><b>Figure 3.17.</b> Parking area used to develop Piolín's final positioning behavior.</sub>

</div>

Parking combines several mobility requirements into one final maneuver.

Piolín must consider:

```text
course progression

approach position

vehicle heading

steering

propulsion displacement

final stopping point
```

The final parking strategy is still being developed and should therefore not be described as a fully validated solution yet.

The current engineering objective is to combine course-state information with vehicle displacement and environmental references so that parking becomes more repeatable than a purely time-based stop.

---

## 3.26 Starting Mobility

The beginning of an autonomous run is also a special mobility condition.

At the start:

```text
Piolín is stationary

course direction may not yet be established

normal wall geometry may not yet be acquired
```

The controller must transition from this initial state into stable course following.

An excessively aggressive first steering command can produce a collision even if the normal straight-line controller works correctly later.

The initial mobility phase should therefore acquire the track geometry progressively rather than assuming that the robot already begins in its ideal steady-state position.

---

## 3.27 Vehicle Geometry and Mobility

Several physical dimensions affect Piolín's behavior:

```text
wheelbase

front track

rear track

wheel diameter

overall width

steering linkage dimensions
```

These quantities influence:

```text
turning radius

corner clearance

Ackermann behavior

encoder conversion

parking geometry
```

Piolín has undergone several mechanical changes during development, so dimensions from earlier versions should not automatically be published as current V4 specifications.

Final values should come from measurements of the current physical robot.

<div align="center">

<img
  src="../../v-photos/v4/chassis_top.jpg"
  alt="Top view of Piolín current chassis and wheel geometry"
  width="720"
/>

<br>

<sub><b>Figure 3.18.</b> Top view of the current chassis used as the physical reference for final V4 mobility measurements.</sub>

</div>

---

## 3.28 Chassis and Mobility

The chassis maintains the relative position of the major mobility components.

<div align="center">

<img
  src="../../v-photos/v4/chassis_bottom.jpg"
  alt="Bottom view of Piolín chassis and mobility structure"
  width="720"
/>

<br>

<sub><b>Figure 3.19.</b> Bottom view showing the structural relationship between the drivetrain, steering system, and chassis.</sub>

</div>

If the chassis flexes or a critical mount moves, the mechanical relationships assumed by the controller can change.

For example:

```text
steering support shifts
→ wheel center changes
```

or:

```text
drive support becomes misaligned
→ drivetrain resistance increases
```

The chassis therefore contributes directly to mobility repeatability.

---

## 3.29 Mechanical Mobility Inspection

Before changing navigation software because the robot behaves differently, the mechanical system should be inspected.

A useful sequence is:

```text
rear wheels secure?
      ↓
rear drivetrain free?
      ↓
Motor A mount secure?
      ↓
front steering free?
      ↓
Motor B mount secure?
      ↓
steering center correct?
      ↓
left/right steering range free?
      ↓
chassis rigid?
```

<div align="center">

<img
  src="../../v-photos/v4/drive_motor_mount.jpg"
  alt="Piolín Motor A mounting"
  width="650"
/>

<br>

<sub><b>Figure 3.20.</b> Motor A mounting should remain mechanically stable so drivetrain geometry does not change between runs.</sub>

</div>

<div align="center">

<img
  src="../../v-photos/v4/steering_motor_mount.jpg"
  alt="Piolín Motor B steering mount"
  width="650"
/>

<br>

<sub><b>Figure 3.21.</b> Motor B mounting forms part of the steering reference and must remain stable during calibration and competition runs.</sub>

</div>

This process prevents software from being used to compensate for a mechanical failure.

---

## 3.30 Mechanical Play

Small amounts of clearance exist in LEGO mechanical assemblies.

These can appear in:

```text
axles

pins

steering pivots

linkages

motor connections
```

The effect may be especially noticeable when steering direction reverses.

For example:

```text
Motor B turns right
      ↓
controller requests left
      ↓
motor reverses
      ↓
mechanical clearance is crossed
      ↓
front wheels begin responding left
```

During that short interval, Motor A may continue moving the vehicle.

A small mechanical clearance at the linkage can therefore become a larger positional difference on the track.

---

## 3.31 Mobility and Sensors Form a Feedback Loop

Piolín's sensors do not observe the environment independently from vehicle motion.

When Piolín moves or turns:

```text
S2/S3 geometry changes

gyro heading changes in Open

Pixy viewpoint changes in Obstacles

S4 crosses different floor regions
```

The complete system is therefore a feedback loop:

```text
SENSORS
   ↓
EV3
   ↓
MOTOR COMMANDS
   ↓
MOBILITY SYSTEM
   ↓
ROBOT CHANGES POSITION
   ↓
SENSOR CONDITIONS CHANGE
   ↓
SENSORS
```

This is why mobility and perception cannot be tuned completely independently.

---

## 3.32 Mobility and Ultrasonic Geometry

Piolín's two ultrasonic sensors are mounted laterally:

```text
S2 = LEFT

S3 = RIGHT
```

<div align="center">

<img
  src="../../v-photos/v4/PiolinUSlabeling.png"
  alt="Piolín left and right ultrasonic sensor labeling"
  width="700"
/>

<br>

<sub><b>Figure 3.22.</b> Fixed physical ultrasonic mapping used by Piolín: S2 LEFT and S3 RIGHT.</sub>

</div>

When the robot is approximately parallel to a wall, the lateral measurements provide useful track-relative information.

During stronger steering or a corner, however, the robot's orientation changes and the sensor beams intersect the environment differently.

Therefore:

```text
distance change
```

does not always mean:

```text
pure lateral translation
```

Some of the variation can come from vehicle yaw.

This is one reason mobility state matters when interpreting sensor data.

---

## 3.33 Mobility and Pixy2.1

During the Obstacle Challenge, steering also changes the orientation of Pixy2.1.

```text
Motor B changes steering
      ↓
Piolín changes yaw
      ↓
camera viewpoint rotates
      ↓
pillar position in image changes
```

Therefore a pillar moving across the Pixy image does not necessarily indicate that the physical pillar itself changed position relative to the track.

Some of the visual motion is created by Piolín's own trajectory.

This is why target selection and obstacle steering must consider the current maneuver state.

---

## 3.34 Mobility and Battery Condition

Motor behavior depends on the complete electrical and mechanical system.

Changes in:

```text
battery condition

drivetrain friction

steering resistance

wheel traction
```

can alter physical response even when software commands remain unchanged.

For this reason, quantitative mobility comparisons should keep important test conditions reasonably consistent.

A steering controller should not be judged from one run performed under a significantly different mechanical or electrical condition from another.

---

## 3.35 Current Mobility Architecture vs. Alternatives

Several mobility designs could potentially complete a WRO Future Engineers course.

| Architecture | Advantage | Limitation for Piolín |
| :--- | :--- | :--- |
| Differential drive | Simple turning concept | Requires independent left/right propulsion and produces tire scrub |
| Four-wheel skid steer | Strong low-speed maneuverability | Increased drive and friction complexity |
| Multiple drive motors + front steering | More propulsion possibilities | More actuators and synchronization |
| External servo steering | Dedicated angular actuator | Adds non-EV3 electrical integration |
| **Single rear drive + Ackermann-style front steering** | **Separates propulsion and direction with only two EV3 motors** | **Requires accurate mechanical steering calibration** |

Piolín's selected architecture keeps the actuator count low while using mechanical geometry to create the required steering behavior.

---

## 3.36 Why Differential Steering Was Not Selected

Differential drive turns by using different wheel velocities:

```text
left speed
≠
right speed
```

Piolín instead uses:

```text
common propulsion
+
front steering
```

This makes the physical steering principle more similar to a conventional road vehicle.

The trade-off is that the front mechanical linkage becomes more important and requires careful calibration.

Rather than adding another propulsion actuator, Piolín uses the geometry of the front assembly to generate the difference between inner and outer turning paths.

---

## 3.37 Why Two Motors Are Sufficient

Piolín performs the primary mobility functions using only:

```text
1 × Large Motor
→ propulsion

1 × Medium Motor
→ steering
```

The design therefore does not require:

```text
four independent wheel motors

separate left/right drivetrain control

external steering servo

additional motor drivers
```

This demonstrates one of the central mechanical principles of Piolín:

> **Use mechanical geometry to provide vehicle behavior without adding unnecessary actuators.**

The cost of that simplification is that drivetrain condition and steering geometry must remain mechanically repeatable.

---

## 3.38 Same Mobility Platform in Both Competition Rounds

<div align="center">

<img
  src="../../v-photos/v4/piolin_obstacle_isometric.jpg"
  alt="Piolín Obstacle Challenge configuration using the same mobility platform"
  width="720"
/>

<br>

<sub><b>Figure 3.23.</b> The Obstacle Challenge uses the same drivetrain and steering system as the Open Challenge.</sub>

</div>

The mechanical mobility platform does not change between Open and Obstacles.

The following remain common:

```text
Motor A

Motor B

rear drivetrain

rear wheels

front steering linkage

front wheel geometry

chassis
```

The major round-specific change occurs in perception:

```text
OPEN
→ Gyro on S1

OBSTACLES
→ Pixy2.1 on S1
```

This allows the team to develop two navigation strategies while maintaining one physical vehicle platform.

---

## 3.39 Full Track Context

<div align="center">

<img
  src="../../v-photos/v4/full_track.jpg"
  alt="Full competition-style track used for Piolín testing"
  width="740"
/>

<br>

<sub><b>Figure 3.24.</b> Track environment in which Piolín's mobility system must combine straight driving, corners, obstacle maneuvers, and parking.</sub>

</div>

A complete run requires several mobility behaviors to work consecutively:

```text
start

straight driving

corner entry

corner exit

multiple laps

pillar avoidance in Obstacles

recovery

final positioning
```

The usefulness of the mobility design therefore cannot be evaluated only from one isolated steering test.

The system must preserve useful vehicle geometry from one maneuver to the next.

---

## 3.40 Values Not Yet Published as Final

The following parameters should be measured from the current V4 robot before being treated as final specifications:

```text
wheelbase

front track width

rear track width

front wheel diameter

rear wheel diameter

drivetrain ratio

effective wheel circumference

maximum useful wheel steering angles

Motor B-to-wheel-angle relationship

minimum turning radius

left/right turning-radius difference

straight-line encoder scale

maximum validated driving speed

final Open corner speed

final Obstacle speed

final reverse displacement

final parking displacement
```

Earlier Piolín values should not automatically be copied into the current documentation because the physical robot has changed during development.

---

## 3.41 Recommended Mobility Characterization

The current mechanical platform can later be characterized quantitatively using a small set of repeatable experiments.

### Straight-line test

Use:

```text
same start position

same Motor A command

same steering center

same travel distance
```

and compare the final position across several trials.

This can reveal persistent mechanical bias and repeatability.

### Encoder-distance test

Command a fixed Motor A encoder displacement and measure the actual physical travel distance.

This provides an experimental conversion between motor rotation and vehicle displacement.

### Turning test

Command a fixed Motor A speed and a repeatable Motor B position, then measure the actual vehicle turning radius.

The experiment should be repeated for both left and right steering.

### Steering-center repeatability

Move Motor B between different positions and repeatedly return to center, then inspect whether the front wheels return to approximately the same physical orientation.

### Reverse repeatability

Command the same reverse displacement several times and compare the final vehicle position.

These tests should be performed using the current V4 robot rather than values inherited from previous mechanical versions.

---

## 3.42 Mobility Failure Diagnosis

A mobility problem can originate from perception, software, actuation, or mechanics.

| Observed Behavior | Possible Causes |
| :--- | :--- |
| Piolín does not move | Motor A, Port A, software, drivetrain |
| Vehicle becomes slower | Battery condition, drivetrain friction, wheel resistance |
| Persistent drift | Steering center, alignment, software correction bias |
| Zig-zag motion | Excessive steering correction, delayed response, mechanical play |
| Left and right turns differ | Steering asymmetry, linkage geometry, software calibration |
| Corner starts too late | Detection timing, excessive speed, steering response |
| Corner becomes too tight | Excessive steering, release timing, low entry clearance |
| Obstacle is passed but wall is hit afterward | Countersteering or recovery failure |
| Reverse movement varies | Traction, timing, encoder strategy, mechanical condition |
| Parking position varies | Approach geometry, propulsion displacement, steering, traction |

The diagnostic process should identify the first stage that behaves incorrectly.

A useful sequence is:

```text
sensor information correct?
      ↓
EV3 decision correct?
      ↓
motor command correct?
      ↓
motor physically responds?
      ↓
mechanism responds?
      ↓
vehicle follows expected trajectory?
```

This prevents every physical failure from being treated automatically as a software problem.

---

## 3.43 Current Mechanical Definition

The current Piolín mobility system consists of:

| Component | Function |
| :--- | :--- |
| EV3 Large Motor A | Main propulsion actuator |
| Rear drivetrain | Transfers Motor A rotation |
| Rear wheels | Provide driven traction |
| EV3 Medium Motor B | Steering actuator |
| Ackermann-style linkage | Coordinates front-wheel steering |
| Front steering pivots | Allow wheel-angle changes |
| Motor encoders | Provide actuator rotation references |
| LEGO Technic chassis | Preserves the geometry of the mobility system |
| EV3 | Coordinates propulsion and steering commands |

This mechanical architecture is shared between both competition rounds.

---

## 3.44 Final Engineering Assessment

<div align="center">

<img
  src="../../v-photos/v4/piolin_bottom.jpg"
  alt="Bottom view of Piolín showing the complete mechanical mobility architecture"
  width="720"
/>

<br>

<sub><b>Figure 3.25.</b> Bottom view of Piolín showing the physical integration of the drivetrain, wheel layout, steering system, and chassis.</sub>

</div>

Piolín's mobility architecture is based on a deliberate separation between **propulsion** and **direction control**.

Motor A provides rear-wheel propulsion.

Motor B controls an Ackermann-style front steering mechanism.

The drivetrain, wheel geometry, steering linkage, tires, chassis, and control timing convert those two actuator commands into the final vehicle trajectory.

The design allows Piolín to perform:

```text
straight driving

clockwise and counterclockwise corners

forward movement

reverse movement

red-pillar avoidance

green-pillar avoidance

countersteering

post-obstacle recovery

parking maneuvers
```

without changing the mechanical platform between competition rounds.

The architecture also demonstrates that vehicle mobility is not purely a software problem. A navigation algorithm can only be repeatable if the physical steering center, drivetrain resistance, wheel alignment, mechanical rigidity, and sensor geometry remain sufficiently consistent.

Piolín therefore treats mobility as a **mechatronic system** in which mechanics, sensing, electrical actuation, and software continuously influence one another.

The main design principle can be summarized as:

> **Use a simple two-actuator vehicle architecture, preserve the mechanical geometry as consistently as possible, and let the EV3 coordinate propulsion and steering according to the current environment.**

---

<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
