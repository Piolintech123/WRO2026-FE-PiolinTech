# 3. Robot Mobility

<div align="center">

<img
  src="../../v-photos/v4/piolin_open_isometric.jpg"
  alt="Piolín complete mobility architecture in Open Challenge configuration"
  width="720"
/>

<br>

<sub><b>Figure 3.1.</b> Piolín's complete vehicle platform combining rear-wheel propulsion with front Ackermann-style steering.</sub>

</div>

Piolín is designed as a four-wheel autonomous vehicle with **rear-wheel propulsion** and **front-wheel Ackermann-style steering**. Unlike a differential-drive robot, Piolín separates the two fundamental mobility functions between two independent actuators.

```text
Motor A
→ propulsion


Motor B
→ steering
```

The LEGO Mindstorms EV3 Large Motor on Port A produces the motion required to move the vehicle forward or backward, while the EV3 Medium Motor on Port B controls the angular position of the front steering mechanism.

The resulting architecture behaves more like a small conventional vehicle than a skid-steer robot:

```text
              FRONT

       steering wheels
          ↙       ↘
        O           O
        │           │
        │   CHASSIS │
        │           │
        O===========O
          rear drive

              REAR
```

This architecture was selected because WRO Future Engineers requires repeated straight sections, controlled corners, obstacle avoidance, recovery maneuvers, and parking. Separating propulsion from steering allows the software to modify vehicle speed and trajectory independently while preserving the same mechanical platform for both the Open and Obstacle Challenges.

---

## 3.1 Mobility Architecture

Piolín's mobility system can be divided into two principal mechanical paths:

```text
PROPULSION PATH

EV3
 ↓
Motor A
 ↓
rear drivetrain
 ↓
rear wheels
 ↓
longitudinal vehicle motion
```

and:

```text
STEERING PATH

EV3
 ↓
Motor B
 ↓
steering linkage
 ↓
front-wheel angles
 ↓
vehicle curvature
```

<div align="center">

<img
  src="../../embed/motor_role_architecture.png"
  alt="Piolín propulsion and steering motor role architecture"
  width="850"
/>

<br>

<sub><b>Figure 3.2.</b> Piolín separates propulsion and steering into two independently controlled mechanical subsystems.</sub>

</div>

The two systems are physically separate but dynamically coupled.

A steering angle has little effect when the robot is stationary, while the same steering angle can create a much larger trajectory change when Piolín is moving quickly.

Therefore vehicle mobility must be understood as:

```text
propulsion
+
steering
+
vehicle geometry
+
traction
+
control timing
```

rather than as two unrelated motor commands.

---

# 3.2 Rear-Wheel Propulsion

Piolín uses the EV3 Large Motor connected to **Port A** as its propulsion actuator.

<div align="center">

<img
  src="../../v-photos/v4/motor_a_large_drive.jpg"
  alt="EV3 Large Motor A used for Piolín propulsion"
  width="660"
/>

<br>

<sub><b>Figure 3.3.</b> Motor A provides the mechanical input for Piolín's rear-wheel propulsion system.</sub>

</div>

The propulsion path is:

```text
Motor A
   ↓
mechanical transmission
   ↓
rear axle / drivetrain
   ↓
rear wheels
   ↓
vehicle movement
```

The motor can be commanded in both rotational directions, allowing Piolín to move:

```text
forward
```

or:

```text
reverse
```

without requiring a separate transmission mechanism.

This ability is useful beyond ordinary driving. Reverse movement can also form part of recovery, obstacle positioning, and parking strategies when additional physical space is required.

---

## 3.3 Why Propulsion Is Separated from Steering

In a differential-drive vehicle, turning is produced by commanding the left and right drive wheels at different speeds.

Piolín instead uses one dedicated propulsion system and one dedicated steering system.

Conceptually:

```text
DIFFERENTIAL DRIVE

left wheel speed
+
right wheel speed
→ direction
```

Piolín uses:

```text
drive speed
+
front steering angle
→ direction
```

This separation offers an important control advantage for the current robot.

Motor A can be responsible primarily for:

```text
how quickly Piolín moves
```

while Motor B can be responsible primarily for:

```text
where Piolín moves
```

The two commands still interact physically, but the software architecture can reason about them as different control variables.

---

# 3.4 Rear Drivetrain

<div align="center">

<img
  src="../../v-photos/v4/rear_drivetrain_top.jpg"
  alt="Piolín rear drivetrain viewed from above"
  width="700"
/>

<br>

<sub><b>Figure 3.4.</b> Rear drivetrain transferring Motor A rotation toward Piolín's driven wheels.</sub>

</div>

The rear drivetrain performs the mechanical conversion between Motor A rotation and wheel rotation.

The complete energy path is:

```text
EV3 battery
     ↓
Motor A
     ↓
motor rotation
     ↓
drivetrain
     ↓
wheel rotation
     ↓
tire-track interaction
     ↓
vehicle displacement
```

<div align="center">

<img
  src="../../embed/drivetrain_power_flow.png"
  alt="Piolín propulsion power flow"
  width="850"
/>

<br>

<sub><b>Figure 3.5.</b> Electrical energy is converted into vehicle displacement through the complete propulsion chain.</sub>

</div>

The exact current drivetrain ratio should be published only after the final V4 drivetrain is physically verified. An earlier ratio should not be assumed to remain valid after mechanical revisions.

---

## 3.5 Rear-Wheel Traction

The rear wheels convert drivetrain rotation into longitudinal force against the competition surface.

<div align="center">

<img
  src="../../v-photos/v4/rear_wheels.jpg"
  alt="Piolín rear propulsion wheels"
  width="660"
/>

<br>

<sub><b>Figure 3.6.</b> Rear wheels provide the traction required to transform Motor A rotation into vehicle motion.</sub>

</div>

The ideal relationship is:

```text
wheel rotation
→ vehicle displacement
```

but the real relationship can be affected by:

```text
wheel slip

tire deformation

track surface

vehicle mass

cornering load

acceleration

mechanical friction
```

This distinction becomes important when wheel encoders are used to estimate traveled distance.

The encoder measures motor or axle rotation accurately, but the physical robot can still travel slightly more or less than the ideal calculated distance.

---

# 3.6 Front Steering

Piolín's front wheels are controlled by the EV3 Medium Motor on Port B.

<div align="center">

<img
  src="../../v-photos/v4/motor_b_medium_steering.jpg"
  alt="EV3 Medium Motor B controlling Piolín steering"
  width="660"
/>

<br>

<sub><b>Figure 3.7.</b> Motor B controls the front steering system independently from propulsion.</sub>

</div>

Motor B does not directly represent the vehicle's turning radius.

Instead, its rotation is transferred through a mechanical linkage:

```text
Motor B
   ↓
steering transmission
   ↓
linkage
   ↓
front wheel angles
   ↓
vehicle trajectory
```

This means:

```text
Motor B angle
≠
front-wheel angle
```

unless the mechanical relationship between them has been experimentally calibrated.

---

# 3.7 Ackermann-Style Steering

Piolín uses an **Ackermann-style steering geometry** so that the two front wheels can follow different turning radii during a corner.

<div align="center">

<img
  src="../../v-photos/v4/ackermann_top.jpg"
  alt="Piolín Ackermann-style steering viewed from above"
  width="700"
/>

<br>

<sub><b>Figure 3.8.</b> Top view of Piolín's front steering mechanism.</sub>

</div>

During a turn, the inner front wheel follows a tighter path than the outer front wheel.

Therefore the ideal steering relationship is approximately:

```text
inner wheel angle
>
outer wheel angle
```

rather than both wheels remaining perfectly parallel.

<div align="center">

<img
  src="../../embed/ackermann_geometry.png"
  alt="Ackermann steering geometry showing different inner and outer wheel angles"
  width="850"
/>

<br>

<sub><b>Figure 3.9.</b> Ackermann geometry allows the inner and outer front wheels to follow different radii around a common turning region.</sub>

</div>

This reduces unnecessary tire scrubbing compared with forcing both front wheels to use identical angles during a turn.

---

## 3.8 Geometric Turning Model

A simplified vehicle turning model relates steering geometry to vehicle curvature.

For a basic bicycle-model approximation:

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

The relationship shows an important mobility characteristic:

```text
small steering angle
→ large turning radius


large steering angle
→ smaller turning radius
```

However, Piolín uses two actual front wheels and an Ackermann linkage, so this equation is treated as a conceptual model rather than a complete description of the real vehicle.

The final turning radius should be measured experimentally on the current robot.

---

# 3.9 Steering Center

A reliable mobility system requires a repeatable neutral steering position.

Conceptually:

```text
Motor B center
      ↓
steering linkage center
      ↓
front wheels approximately straight
      ↓
vehicle capable of straight travel
```

<div align="center">

<img
  src="../../v-photos/v4/ackermann_center.jpg"
  alt="Piolín steering in its centered position"
  width="680"
/>

<br>

<sub><b>Figure 3.10.</b> Front steering assembly in its mechanical center position.</sub>

</div>

A software value of:

```text
steering = 0
```

is only useful if it corresponds consistently to the physical steering center.

If the linkage moves, the motor is reinstalled, or a front-wheel support changes, the relationship must be rechecked.

---

## 3.10 Steering Range

The steering system also has physical limits.

<div align="center">

<img
  src="../../v-photos/v4/ackermann_left_lock.jpg"
  alt="Piolín useful left steering limit"
  width="650"
/>

<br>

<sub><b>Figure 3.11.</b> Mechanical left steering limit used to evaluate available wheel-angle range.</sub>

</div>

<div align="center">

<img
  src="../../v-photos/v4/ackermann_right_lock.jpg"
  alt="Piolín useful right steering limit"
  width="650"
/>

<br>

<sub><b>Figure 3.12.</b> Mechanical right steering limit used to evaluate available wheel-angle range.</sub>

</div>

The software should avoid commanding the mechanism beyond its useful physical range.

Driving Motor B continuously against a mechanical stop can create:

```text
unnecessary motor load

linkage stress

steering inconsistency

slower response when reversing direction
```

The final software steering limits should therefore be established from the actual mechanical assembly.

---

# 3.11 Steering Motion

<div align="center">

<img
  src="../../v-photos/v4/steering_motion.gif"
  alt="Piolín Ackermann steering moving from left through center to right"
  width="700"
/>

<br>

<sub><b>Figure 3.13.</b> Complete steering movement demonstrating the transformation from Motor B rotation to front-wheel motion.</sub>

</div>

The steering animation provides useful evidence that the wheels do not simply pivot independently. They are mechanically connected through one coordinated linkage.

This also makes several non-ideal effects visible:

```text
backlash

mechanical play

different left/right geometry

linkage speed

physical limits
```

These factors should be considered when tuning rapid countersteering maneuvers.

---

# 3.12 Motor Angle vs. Wheel Angle

One important distinction in Piolín's mobility model is:

```text
Motor B encoder angle
```

is not the same physical quantity as:

```text
front-wheel steering angle
```

<div align="center">

<img
  src="../../embed/motor_to_wheel_angle.png"
  alt="Relationship between steering motor angle and physical wheel angle"
  width="850"
/>

<br>

<sub><b>Figure 3.14.</b> Motor B rotation is transformed through the steering linkage before becoming a physical wheel angle.</sub>

</div>

The relationship may be approximately linear over part of the steering range, but that should not be assumed without measurement.

A useful calibration can record:

```text
Motor B position
vs.
measured front-wheel angle
```

for several left, center, and right positions.

---

# 3.13 Propulsion and Steering Interaction

The vehicle trajectory depends on both Motor A and Motor B at the same time.

<div align="center">

<img
  src="../../embed/drive_steering_interaction.png"
  alt="Interaction between propulsion speed and steering angle"
  width="850"
/>

<br>

<sub><b>Figure 3.15.</b> The same steering position can produce different practical trajectories depending on propulsion speed and available response time.</sub>

</div>

For example:

```text
large steering angle
+
low speed
→ tight controlled maneuver
```

while:

```text
same steering angle
+
higher speed
→ larger physical displacement during steering response
```

This is why Piolín cannot tune steering independently from speed.

A corner that works correctly at one Motor A command may become too wide or too aggressive at another.

---

## 3.14 Why Speed Affects Cornering

Motor B requires physical time to move the steering linkage.

During that time, Motor A may continue moving the robot forward.

Therefore:

```text
higher speed
→ more distance traveled while steering changes
```

A delayed steering command can therefore become a large path error when propulsion speed increases.

The relevant chain is:

```text
corner condition detected
      ↓
EV3 calculates command
      ↓
Motor B begins moving
      ↓
Piolín continues traveling
      ↓
front wheels reach intended angle
```

The distance covered during this sequence forms part of practical corner behavior.

---

# 3.15 Straight-Line Mobility

During a straight section, the desired vehicle state is approximately:

```text
front wheels near neutral
+
stable propulsion
+
small steering corrections only when required
```

The robot should not continuously oscillate from left to right when the environmental geometry already indicates a stable trajectory.

Repeated large corrections create:

```text
zig-zag motion

additional path length

more steering activity

greater sensor variation

less predictable corner entry
```

A strong straight-line controller therefore aims to make corrections early enough that large emergency steering commands become less necessary.

---

## 3.16 Mechanical Straight-Line Bias

Straight-line drift can originate from several sources.

```text
front steering not centered

rear wheel misalignment

unequal wheel behavior

chassis geometry

drivetrain resistance

software correction bias
```

For this reason, the diagnostic sequence should begin mechanically.

```text
Check wheel alignment
      ↓
Check steering center
      ↓
Check drivetrain freedom
      ↓
Then evaluate software
```

Software should not be used to hide a mechanical problem that can be corrected physically.

---

# 3.17 Wheel Encoder Distance

Motor encoders provide a useful internal measurement of rotational movement.

A theoretical wheel-distance relationship can be written as:

```text
distance =
wheel revolutions × wheel circumference
```

or:

```text
distance =
(encoder angle / 360°) × π × D
```

where:

```text
D
= effective wheel diameter
```

<div align="center">

<img
  src="../../embed/motor_encoder_distance.png"
  alt="Conversion from encoder angle to theoretical wheel displacement"
  width="830"
/>

<br>

<sub><b>Figure 3.16.</b> Encoder rotation can be converted into an estimated travel distance when the effective wheel geometry is known.</sub>

</div>

The equation is useful for:

```text
controlled forward movement

reverse movement

parking

relative displacement

experimental odometry
```

but it remains an estimate of physical displacement.

---

## 3.18 Why Encoder Distance Is Not Perfect Odometry

The encoder measures rotational motion.

It does not directly measure the robot's position on the mat.

Errors can enter through:

```text
wheel slip

tire deformation

turning

mechanical backlash

effective wheel diameter

surface variation
```

During a curve, the wheels also travel different paths.

Therefore the simplest encoder-distance calculation is most reliable for approximately straight movement.

For complete vehicle localization, additional sensing and geometric assumptions would be required.

---

# 3.19 Open Challenge Mobility

The physical mobility system used during Open is:

```text
Motor A
→ propulsion


Motor B
→ steering


S2/S3
→ lateral geometry


Gyro
→ heading/orientation support


Color Sensor
→ course-state landmarks
```

The mechanical drivetrain and steering system do not change when the Open software changes.

This is important because the control problem can then be improved while preserving a stable vehicle platform.

---

## 3.20 Open Straight Sections

During Open, Piolín should use its mobility system to maintain a stable path without excessive steering.

The lateral ultrasonic sensors primarily describe the relationship between the robot and track boundaries, while the gyro helps characterize orientation.

The resulting mobility objective is:

```text
stable Motor A propulsion
+
small Motor B corrections
+
avoid wall proximity
+
prepare for corner entry
```

The mechanical architecture supports this because steering can change without directly changing the propulsion motor command.

---

# 3.21 Open Corner Mobility

Corners require a temporary transition from straight-line motion to high vehicle curvature.

A conceptual sequence is:

```text
STRAIGHT
   ↓
corner evidence
   ↓
steering increases
   ↓
vehicle yaws
   ↓
corner progresses
   ↓
steering returns toward center
   ↓
new straight geometry acquired
```

<div align="center">

<img
  src="../../v-photos/v4/open_corner_run.jpg"
  alt="Piolín physically executing an Open Challenge corner"
  width="700"
/>

<br>

<sub><b>Figure 3.17.</b> Piolín executing a real Open Challenge corner using the same rear-drive and front-steering mobility architecture.</sub>

</div>

The final corner trajectory depends on:

```text
entry position

entry heading

Motor A speed

Motor B steering command

steering response time

wheel geometry

track friction
```

This explains why a corner cannot be calibrated from steering angle alone.

---

## 3.22 Corner Exit

A successful corner is not complete when Piolín simply rotates approximately 90 degrees.

The vehicle must also exit into a useful geometry for the next straight.

A poor corner can have the correct overall heading but still leave Piolín:

```text
too close to the inner wall

too close to the outer wall

at a residual steering angle

with lateral motion still developing
```

The mobility system therefore treats:

```text
corner exit
```

as a distinct phase from:

```text
corner rotation
```

This distinction is important for achieving repeatable multi-lap navigation.

---

# 3.23 Obstacle Challenge Mobility

The mechanical mobility platform is unchanged during Obstacles.

The major difference is the source of steering information.

```text
OPEN

Gyro + ultrasonics + color
        ↓
mobility decisions
```

becomes:

```text
OBSTACLES

Pixy + ultrasonics + color
        ↓
mobility decisions
```

Motor A and Motor B retain exactly the same physical roles.

This allows obstacle software development to focus on perception and maneuver logic rather than requiring a separate drivetrain.

---

# 3.24 Pillar Avoidance as a Mobility Maneuver

A pillar avoidance maneuver requires more than steering toward one side.

The complete physical sequence is closer to:

```text
approach
   ↓
steer away from collision path
   ↓
establish side-pass trajectory
   ↓
move alongside pillar
   ↓
clear pillar
   ↓
countersteer
   ↓
recover stable course position
```

The mobility system must therefore support rapid changes in curvature.

Motor B creates the lateral trajectory while Motor A controls how quickly the maneuver develops in physical space.

---

## 3.25 Red Pillar Mobility

The competition rule requires:

```text
RED
→ pass RIGHT
```

This means Piolín must create a trajectory that places the vehicle on the required side of the pillar.

<div align="center">

<img
  src="../../v-photos/v4/obstacle_red_run.jpg"
  alt="Piolín passing a red pillar on the required right side"
  width="700"
/>

<br>

<sub><b>Figure 3.18.</b> Real red-pillar mobility maneuver in the Obstacle Challenge.</sub>

</div>

The maneuver may contain:

```text
initial steering

temporary hold

countersteer

recenter
```

rather than one constant wheel angle.

This reflects the fact that obstacle avoidance is a trajectory-generation problem, not simply a color-to-steering lookup.

---

## 3.26 Green Pillar Mobility

The corresponding Green rule is:

```text
GREEN
→ pass LEFT
```

<div align="center">

<img
  src="../../v-photos/v4/obstacle_green_run.jpg"
  alt="Piolín passing a green pillar on the required left side"
  width="700"
/>

<br>

<sub><b>Figure 3.19.</b> Real green-pillar maneuver showing the opposite required passing direction.</sub>

</div>

Although the two maneuvers are conceptually mirrored, their final software values do not have to be numerically identical.

Real mechanical systems can contain:

```text
small steering asymmetry

different wall geometry

different approach position

different target position
```

The final calibration should therefore be based on measured performance rather than assuming perfect symmetry.

---

# 3.27 Countersteering

Once Piolín has moved laterally around an obstacle, it must reverse part of the steering action to recover.

This is **countersteering** in the context of Piolín's obstacle maneuver.

For example:

```text
initial steer
→ creates lateral displacement


countersteer
→ reduces heading/lateral error
```

Without an effective recovery phase, the robot may successfully pass one pillar but continue toward a wall or enter the next obstacle with poor geometry.

The mobility objective is therefore not:

```text
avoid current obstacle
```

only.

It is:

```text
avoid current obstacle
+
finish in a useful state for the next event
```

---

# 3.28 Reverse Mobility

Piolín can reverse by commanding Motor A in the opposite direction.

Reverse movement can be useful when:

```text
additional reaction distance is needed

the robot must recover from an unsafe geometry

a parking maneuver requires backward displacement

a controlled repositioning maneuver is being tested
```

However, reverse motion should not be used as a universal correction for every navigation error.

Each reversal costs time and may change the robot's geometry relative to walls and obstacles.

A successful reverse maneuver therefore needs a clear objective.

---

## 3.29 Timed Reverse vs. Encoder Reverse

A reverse command can be defined using time:

```text
reverse for T seconds
```

or using encoder displacement:

```text
reverse for N motor degrees
```

The timed method is simple but depends more strongly on actual motor speed and battery/mechanical conditions.

Encoder-based movement provides a more direct rotational reference.

However:

```text
encoder displacement
≠
perfect physical distance
```

because tire slip and vehicle geometry still exist.

The appropriate method depends on the maneuver and the required precision.

---

# 3.30 Parking Mobility

Parking combines several aspects of Piolín's mobility architecture:

```text
course-state information

vehicle alignment

propulsion distance

steering

final position
```

<div align="center">

<img
  src="../../v-photos/v4/parking_area.jpg"
  alt="Parking area used for Piolín autonomous mobility testing"
  width="700"
/>

<br>

<sub><b>Figure 3.20.</b> Parking area used to develop the final autonomous positioning sequence.</sub>

</div>

The parking strategy is still under development, so this document does not claim one final parking trajectory.

The important mobility requirement is that Piolín must finish its autonomous run not only with the correct course progression but with a controlled final vehicle displacement.

---

# 3.31 Starting Position

Initial mobility is also a special case.

At the beginning of a run, the robot may not yet have the same geometric context available later in the course.

The vehicle must transition from:

```text
stationary starting position
```

to:

```text
stable course-following state
```

without immediately producing an excessive steering correction.

This transition can be difficult when Piolín begins closer to one track boundary than another.

The mechanical system must therefore support a gentle acquisition maneuver before normal navigation becomes fully active.

---

## 3.32 Why Starting Geometry Matters

The same controller can produce different initial paths if the robot starts:

```text
near inner wall

near center

near outer wall
```

because the initial lateral error is different.

The mobility controller must distinguish:

```text
large initial position error
```

from:

```text
emergency collision condition
```

Otherwise it may command an aggressive steering action that sends the vehicle across the corridor.

This is primarily a software decision, but the physical consequence is determined by the mobility system.

---

# 3.33 Vehicle Geometry

Several physical dimensions influence mobility:

```text
wheelbase

front track width

rear track width

wheel diameter

overall width

steering linkage dimensions
```

These values affect:

```text
turning radius

Ackermann geometry

encoder-distance conversion

corner clearance

parking behavior
```

The current V4 robot has undergone mechanical changes, so final numerical values should be taken from a fresh physical measurement rather than inherited from earlier Piolín versions.

---

## 3.34 Wheelbase

Wheelbase is the longitudinal distance between the front and rear axle reference lines.

In a simplified model:

```text
longer wheelbase
→ larger turning radius for same steering angle


shorter wheelbase
→ tighter turning capability
```

However, wheelbase also influences vehicle stability and the physical space required for components.

Piolín's final wheelbase should therefore be documented as a measured structural parameter once V4 measurements are finalized.

---

## 3.35 Track Width

Front and rear track widths affect lateral stability and turning geometry.

Track width should ideally be measured:

```text
wheel center
to
wheel center
```

rather than outside-edge to outside-edge, because center-to-center measurements are more useful for vehicle kinematics.

The current values should be physically remeasured before publishing them as final.

---

# 3.36 Turning Radius

Turning radius is one of the most useful complete-system measurements for Piolín.

It includes the combined effects of:

```text
wheelbase

steering geometry

Motor B range

wheel alignment

tire behavior
```

A practical turning-radius experiment can command a stable steering position and allow the robot to drive through a complete arc.

<div align="center">

<img
  src="../../embed/turning_radius_test.png"
  alt="Piolín measured turning-radius experiment"
  width="850"
/>

<br>

<sub><b>Figure 3.21.</b> Reserved evidence figure for the measured relationship between steering command and physical turning radius.</sub>

</div>

This graph should contain only real measurements from the current V4 robot.

---

# 3.37 Straight-Line Testing

A fixed-distance straight-line test can help evaluate:

```text
steering center

mechanical bias

distance repeatability

drivetrain behavior
```

<div align="center">

<img
  src="../../embed/straight_line_test.png"
  alt="Piolín measured straight-line mobility test"
  width="850"
/>

<br>

<sub><b>Figure 3.22.</b> Reserved evidence figure for measured straight-line deviation and repeatability.</sub>

</div>

A useful test can begin with:

```text
same start position

same Motor A command

Motor B centered

same test distance
```

and measure final lateral displacement.

Repeating the experiment helps distinguish a constant mechanical bias from random variation.

---

# 3.38 Mobility Repeatability

A successful autonomous vehicle must not only perform one correct maneuver.

It must reproduce that maneuver repeatedly.

Relevant mobility tests include:

```text
straight-line repeatability

left-turn repeatability

right-turn repeatability

reverse displacement

obstacle recovery

parking displacement
```

For each experiment, important controlled variables include:

```text
software version

battery condition

starting position

track condition

mechanical configuration
```

This transforms qualitative observations into engineering evidence.

---

# 3.39 Mobility and Mechanical Play

Small changes in mechanical geometry can become visible at the vehicle scale.

For example:

```text
small steering-linkage play
        ↓
small wheel-angle uncertainty
        ↓
larger lateral path difference
        ↓
different wall distance after several centimeters
```

This amplification is why steering backlash matters even when it appears small while the robot is stationary.

The complete vehicle must therefore be evaluated dynamically.

---

# 3.40 Mobility and Sensor Placement

Piolín's mobility system changes what the sensors observe.

When the robot moves laterally:

```text
ultrasonic distances change
```

When it rotates:

```text
gyro angle changes
```

When it passes over a floor landmark:

```text
Color Sensor state changes
```

When it steers during Obstacles:

```text
Pixy camera viewpoint changes
```

Therefore sensors do not observe a fixed world independently from movement.

The system forms a feedback loop:

```text
SENSORS
   ↓
EV3
   ↓
MOTORS
   ↓
ROBOT MOVES
   ↓
SENSOR GEOMETRY CHANGES
   ↓
SENSORS
```

This closed-loop relationship is fundamental to Piolín's navigation architecture.

---

# 3.41 Mobility and Camera Geometry

During Obstacles, steering changes not only the vehicle path but also the orientation of Pixy2.1.

This means:

```text
Motor B steering
      ↓
vehicle yaw
      ↓
camera yaw
      ↓
pillar X position changes
```

Some apparent target motion inside the camera image is therefore generated by Piolín itself.

This is one reason the obstacle controller should not interpret visual coordinates without considering the current maneuver state.

---

# 3.42 Mobility and Ultrasonic Geometry

The lateral ultrasonic sensors also depend on vehicle orientation.

When Piolín is parallel to a wall, a lateral sensor can produce a useful perpendicular-distance approximation.

During a corner or large steering maneuver:

```text
vehicle orientation changes
```

and the same sensor beam can intersect the wall differently.

Therefore ultrasonic values during a corner should not necessarily be interpreted with exactly the same assumptions as values during a stable straight.

Mechanical mobility and sensor geometry must be considered together.

---

# 3.43 Mobility and Battery Condition

Motor commands create physical motion through the electrical and mechanical system.

A change in battery condition, drivetrain friction, or steering resistance can therefore alter practical vehicle response even when the same software command is used.

For reproducible mobility tests, Piolín should maintain reasonably consistent electrical and mechanical conditions.

This is especially important when comparing:

```text
corner timing

reverse displacement

parking

full-run time
```

---

# 3.44 Mobility Failure Diagnosis

A mobility failure can originate from several different subsystems.

| Observed behavior | Possible causes |
| :--- | :--- |
| Robot does not move | Motor A, Port A, drivetrain, software |
| Robot moves slowly | Battery condition, Motor A, drivetrain friction |
| Robot drifts constantly | Steering center, alignment, controller bias |
| Robot zig-zags | Excessive correction, steering response, sensing noise |
| Left turn differs greatly from right | Mechanical asymmetry, calibration, software |
| Robot turns too late | Detection timing, Motor B response, excessive speed |
| Robot turns too sharply | Steering command, speed, corner duration |
| Robot cannot recover after pillar | Countersteer, speed, geometry, sensor arbitration |
| Reverse distance inconsistent | Timing, traction, battery, encoder strategy |
| Parking position varies | Approach geometry, propulsion displacement, steering, traction |

The correct diagnostic process should identify whether the first failure occurs in:

```text
perception

control command

motor response

mechanical transmission

vehicle motion
```

before changing software parameters.

---

# 3.45 Mechanical Mobility Inspection

Before an important run, Piolín's mobility hardware should be inspected in a consistent order:

```text
Check rear wheels
      ↓
Check front wheels
      ↓
Check Motor A mount
      ↓
Check drivetrain freedom
      ↓
Check Motor B mount
      ↓
Check steering center
      ↓
Check left/right steering motion
      ↓
Check linkage play
      ↓
Check cable clearance
      ↓
Check sensor mounts
```

A physical failure discovered before the run is much easier to correct than one diagnosed after several software changes.

---

# 3.46 Current Mobility Components

The current mobility system consists of:

| Component | Mobility Role |
| :--- | :--- |
| EV3 Large Motor A | Propulsion |
| Rear drivetrain | Transfers propulsion |
| Rear wheels | Generate longitudinal traction |
| EV3 Medium Motor B | Steering actuator |
| Ackermann linkage | Converts Motor B rotation to front-wheel angles |
| Front wheels | Produce vehicle curvature |
| Motor encoders | Measure actuator rotation |
| LEGO Technic chassis | Preserves vehicle geometry |
| EV3 controller | Coordinates propulsion and steering |

No separate left/right drive motors are used to create differential steering.

No hobby servo is used for steering.

The same mechanical mobility platform is used during both competition rounds.

---

# 3.47 Alternatives Considered

Several mobility architectures could theoretically be used for WRO Future Engineers.

| Mobility Architecture | Advantage | Limitation for Piolín |
| :--- | :--- | :--- |
| Differential drive | Mechanically simple steering | Turns through wheel-speed difference and tire scrub |
| Four-wheel skid steer | Strong maneuverability | Higher lateral tire scrub and more drive complexity |
| Servo steering + separate motor controller | Precise dedicated steering possibilities | Additional non-EV3 electronics and power integration |
| Two drive motors + front steering | Greater propulsion options | More motors, synchronization, mechanical complexity |
| **Single rear propulsion + Ackermann steering** | **Separates speed and direction using only two EV3 motors** | **Requires a carefully calibrated mechanical steering linkage** |

Piolín's current solution was selected because it achieves the required vehicle behavior while preserving a relatively simple EV3-centered architecture.

---

# 3.48 Why Two Motors Are Enough

Piolín performs all primary vehicle mobility with only:

```text
1 propulsion motor

1 steering motor
```

This keeps the actuator architecture compact.

The design does not require:

```text
four independent wheel motors

a separate steering servo

multiple motor drivers
```

The trade-off is that the mechanical transmission and steering geometry must do more of the work.

This represents one of the central mechanical decisions in Piolín:

> **Use mechanical geometry to reduce actuator complexity.**

---

# 3.49 Current vs. Legacy Mobility

The current V4 mobility architecture should be distinguished from previous mechanical configurations.

Historical robot versions may show:

```text
different wheel arrangement

different dimensions

different sensor positions

different steering reinforcement

different drivetrain details
```

Those systems remain useful engineering history but should not be used as the dimensional or mechanical specification of the current robot.

The final current architecture is defined by the actual V4 build and its current photographs, measurements, and tests.

---

# 3.50 Values Intentionally Not Claimed as Final

The following mobility parameters should be physically measured on the current V4 robot before they are published as final values:

```text
overall vehicle length

overall vehicle width

overall vehicle height

wheelbase

front track width

rear track width

front wheel diameter

rear wheel diameter

drivetrain gear ratio

maximum useful steering angle

left/right wheel steering angles

minimum turning radius

effective wheel circumference

straight-line encoder scale

measured reverse displacement

maximum validated competition speed

final Open corner speed

final Obstacle speed

final parking displacement
```

Earlier measurements should not automatically be copied into current documentation.

---

# 3.51 Recommended Mobility Measurements

A complete V4 mobility characterization can eventually contain:

### Straight-line test

```text
fixed Motor A command
fixed steering center
fixed travel distance
repeat several times
measure lateral deviation
```

### Steering calibration

```text
Motor B encoder position
vs.
physical wheel angle
```

### Turning-radius test

```text
fixed speed
fixed steering position
measure actual path radius
```

### Encoder-distance test

```text
command known encoder displacement
measure actual physical displacement
```

### Reverse repeatability

```text
same reverse command
repeat several trials
measure final displacement
```

### Left/right comparison

```text
same magnitude steering command
compare physical left and right trajectories
```

These tests would provide quantitative evidence for the mechanical decisions already documented qualitatively.

---

# 3.52 Complete Mobility System

Piolín's full mobility chain can be represented as:

```text
                      EV3
                       │
          ┌────────────┴────────────┐
          │                         │
          ▼                         ▼
       MOTOR A                   MOTOR B
          │                         │
          ▼                         ▼
    REAR DRIVETRAIN          STEERING LINKAGE
          │                         │
          ▼                         ▼
     REAR WHEELS              FRONT WHEELS
          │                         │
          └────────────┬────────────┘
                       ▼
                 VEHICLE MOTION
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
      TRANSLATION     YAW       CURVATURE
                       │
                       ▼
              NEW SENSOR GEOMETRY
                       │
                       ▼
                      EV3
```

<div align="center">

<img
  src="../../v-photos/v4/piolin_bottom.jpg"
  alt="Bottom view of Piolín showing the complete mechanical mobility system"
  width="720"
/>

<br>

<sub><b>Figure 3.23.</b> Bottom view of Piolín showing how propulsion, wheel placement, steering, and chassis structure form one integrated mobility platform.</sub>

</div>

This relationship demonstrates that mobility is not an isolated mechanical function.

It directly determines:

```text
what the sensors observe

how quickly the controller must react

how corners are executed

how obstacles are passed

how recovery occurs

where Piolín finally parks
```

---

# 3.53 Final Engineering Assessment

Piolín's mobility architecture was designed around a clear separation of functions:

```text
Motor A
→ controls longitudinal motion


Motor B
→ controls vehicle curvature
```

The rear drivetrain transforms Motor A rotation into wheel traction, while the Ackermann-style front linkage transforms Motor B movement into coordinated front-wheel steering.

The result is a vehicle platform capable of:

```text
straight driving

controlled corners

forward motion

reverse motion

pillar avoidance

countersteering

recentering

parking
```

using only two actuators.

The same mechanical platform is retained for both the Open and Obstacle Challenges. What changes between rounds is primarily the perception and control logic, not the underlying mobility mechanism.

This is important because it allows Piolín's engineering development to build on one stable mechanical foundation instead of solving the motion problem twice.

The final design philosophy can therefore be summarized as:

> **Piolín uses a simple two-actuator vehicle architecture in which mechanical geometry provides the steering behavior and software coordinates propulsion and direction according to the current environment.**

The effectiveness of this design depends not only on motor commands but also on steering geometry, wheel alignment, traction, drivetrain friction, vehicle speed, mechanical repeatability, and sensor feedback.

For that reason, Piolín's mobility system is treated as a complete **mechatronic subsystem** rather than as a pair of motors.

---

<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
