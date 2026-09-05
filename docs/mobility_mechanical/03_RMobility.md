# 3. Robot Mobility

Piolín is designed as a **car-like autonomous vehicle** rather than a differential-drive robot.

Its mobility is produced by two independent mechanical actions:

```text
LONGITUDINAL MOTION
        ↓
Motor A
        ↓
Rear propulsion


DIRECTIONAL CONTROL
        ↓
Motor B
        ↓
Front Ackermann steering
```

This architecture allows the robot to control propulsion and steering separately while still combining both actions into a single vehicle trajectory.

The resulting movement can be represented as:

```text
DRIVE COMMAND
      +
STEERING COMMAND
      ↓
Physical wheel motion
      ↓
Vehicle trajectory
```

Piolín's mobility system is designed around the requirements of the WRO Future Engineers track, where the robot must repeatedly perform:

```text
Straight-line navigation

Controlled cornering

Wall-relative positioning

Obstacle avoidance

Post-obstacle recovery

Parking-related movement
```

The robot therefore cannot be understood only as a motorized chassis. Its movement is the result of interactions between mechanical geometry, wheel rotation, vehicle speed, steering position, sensor feedback, and software decisions.

For the structural foundation of this system, see:

[Mechanical Architecture](01_mecharchitecture.md)

[Chassis Design](02_chassis.md)

---

## 3.1 Current Mobility Architecture

The current Piolín vehicle uses:

| Mobility Element | Current Configuration | Function |
| :--- | :--- | :--- |
| **Drive Motor** | Motor A | Generates propulsion |
| **Steering Motor** | Motor B | Changes steering position |
| **Rear Wheels** | ~61.0 mm diameter | Primary driven wheels |
| **Front Wheels** | 38.1 mm diameter | Directional steering wheels |
| **Steering Geometry** | Ackermann-style | Produces car-like turns |
| **Main Controller** | LEGO EV3 | Coordinates drive and steering |
| **Navigation Sensors** | Ultrasonic + Color | Determine movement corrections |
| **Obstacle Perception** | HuskyLens + Arduino Nano | Provides obstacle information |

The basic physical chain is:

```text
                         LEGO EV3
                            │
             ┌──────────────┴──────────────┐
             ▼                             ▼
          Motor A                       Motor B
             │                             │
             ▼                             ▼
      Rear propulsion               Steering linkage
             │                             │
             ▼                             ▼
        Rear wheels                   Front wheels
             │                             │
             └──────────────┬──────────────┘
                            ▼
                     VEHICLE TRAJECTORY
```

Motor A determines how strongly Piolín moves forward or backward.

Motor B determines the direction in which the front wheels are oriented.

Neither motor alone defines the complete path.

---

# 3.2 Vehicle Motion Model

Piolín's mobility can be separated into two basic components:

```text
TRANSLATION
```

and:

```text
ROTATION
```

Translation describes movement of the robot through the track.

Rotation describes changes in vehicle heading.

During approximately straight motion:

```text
STEERING ≈ CENTER
        ↓
Small heading change
        ↓
Predominantly longitudinal movement
```

During a turn:

```text
STEERING ≠ CENTER
        ↓
Front wheels define curved path
        ↓
Vehicle heading changes
```

The complete movement of Piolín is therefore a combination of:

```text
Linear displacement
        +
Angular displacement
```

---

# 3.3 Coordinate Reference

For mobility analysis, Piolín can be described using a vehicle-centered reference frame.

```text
                         FORWARD
                            ↑
                            │
                            │
               LEFT  ← [ PIOLÍN ] →  RIGHT
                            │
                            │
                            ↓
                           REAR
```

The principal movement variables are:

```text
X
=
Longitudinal displacement


Y
=
Lateral displacement


PSI
=
Vehicle heading
```

Piolín does not directly command an independent lateral translation.

Instead, lateral displacement appears as a consequence of forward motion combined with steering.

This is a key difference from a robot that can rotate in place or independently drive its left and right sides.

---

# 3.4 Non-Holonomic Vehicle Behavior

Because Piolín uses car-like steering, it is a **non-holonomic vehicle**.

In practical terms, this means:

> Piolín cannot simply move sideways without first changing its orientation and following a curved path.

For example, if the robot needs to move toward the left side of the track:

```text
Desired lateral movement
        ↓
Steer left
        ↓
Drive forward
        ↓
Vehicle follows curve
        ↓
Position shifts left
```

It cannot execute:

```text
Move directly left
```

while keeping every wheel orientation unchanged.

This mechanical constraint strongly influences:

```text
Obstacle avoidance

Corner recovery

Parking

Wall-centering behavior
```

The software must therefore generate feasible **vehicle trajectories**, not simply desired positions.

---

# 3.5 Propulsion Motion

Motor A provides the main drive force.

The drivetrain converts motor rotation into rear-wheel rotation:

```text
Motor A rotation
       ↓
Drivetrain
       ↓
Rear-wheel rotation
       ↓
Tire-track interaction
       ↓
Vehicle translation
```

If the rear wheels rotate forward and maintain traction:

```text
Piolín moves forward
```

If they rotate in reverse:

```text
Piolín moves backward
```

This reversible propulsion is particularly useful for:

```text
Position recovery

Front-wall response

Parking maneuvers

Repositioning
```

---

# 3.6 Rear Wheel Circumference

The current rear wheel diameter is approximately:

```text
D_REAR ≈ 61.0 mm
```

Therefore:

```text
R_REAR ≈ 30.5 mm
```

The theoretical wheel circumference is:

```text
C_REAR = PI × D_REAR
```

so:

```text
C_REAR ≈ PI × 61.0
```

```text
C_REAR ≈ 191.5 mm
```

This means one complete ideal rear-wheel rotation corresponds to approximately:

```text
191.5 mm
```

of forward travel when:

```text
Wheel slip is neglected

Tire deformation is neglected

The robot follows a straight path
```

Actual track displacement can differ from this theoretical value.

---

# 3.7 Encoder Rotation to Linear Distance

Motor encoder information can be related to theoretical travel distance.

For a wheel rotation of:

```text
THETA degrees
```

the ideal distance is:

```text
DISTANCE =
(THETA / 360) × C_REAR
```

Using Piolín's current rear wheel:

```text
DISTANCE ≈
(THETA / 360) × 191.5 mm
```

For example, theoretically:

```text
360°
↓
≈ 191.5 mm
```

and:

```text
180°
↓
≈ 95.8 mm
```

These calculations provide a useful **motion reference**.

They should not be interpreted as exact odometry because physical movement can be affected by:

```text
Slip

Steering

Surface friction

Drivetrain losses

Wheel deformation
```

---

# 3.8 Why Encoder Distance Is an Estimate

An encoder measures motor or drivetrain rotation.

It does not directly measure the physical position of the robot on the track.

Therefore:

```text
ENCODER ROTATION
      ≠
GUARANTEED TRACK DISPLACEMENT
```

For example, the wheels can rotate while:

```text
Sliding

Turning

Recovering from a collision

Experiencing drivetrain resistance
```

This means the encoder is useful for:

```text
Relative motion

Repeatable movement segments

Approximate distance control
```

but external sensor information remains important for navigation.

---

# 3.9 Straight-Line Mobility

When the front wheels are close to the mechanical steering center, Piolín is intended to travel approximately straight.

The relationship is:

```text
Motor A
   ↓
Forward propulsion


Motor B
   ↓
Near mechanical center


COMBINED
   ↓
Approximately straight trajectory
```

However, real straight movement can still be affected by:

```text
Steering-center error

Wheel alignment

Mechanical play

Uneven tire interaction

Track surface

Mass distribution
```

For this reason, Piolín does not depend only on a fixed centered steering command to remain correctly positioned.

The lateral ultrasonic sensors provide feedback that allows the software to adjust the trajectory relative to the track walls.

---

# 3.10 Steering and Curved Motion

When Motor B moves away from center, the front wheels rotate.

The vehicle then follows a curved path.

Conceptually:

```text
Steering angle increases
        ↓
Turning radius generally decreases
        ↓
Vehicle follows tighter curve
```

and:

```text
Steering angle decreases
        ↓
Turning radius generally increases
        ↓
Vehicle follows broader curve
```

The relationship is not perfectly linear because Piolín uses a mechanical steering linkage.

Therefore:

```text
Motor B command
        ↓
Linkage displacement
        ↓
Front-wheel angles
        ↓
Turning radius
```

The actual path is determined by the complete mechanical geometry.

---

# 3.11 Ideal Bicycle Model

A simplified car-like vehicle can be represented using the **bicycle model**.

Instead of modeling four individual wheels, the model treats the front pair as one equivalent steering wheel and the rear pair as one equivalent rear wheel.

```text
             Equivalent Front Wheel
                       /
                      /
                     /
                    ●

                    │
                    │ L
                    │

                    ●
             Equivalent Rear Wheel
```

For a simplified steering angle `DELTA`, the approximate relationship between wheelbase `L` and turning radius `R` is:

```text
R =
L / tan(DELTA)
```

or equivalently:

```text
DELTA =
atan(L / R)
```

This relationship illustrates an important mobility principle:

```text
Greater steering angle
        ↓
Smaller turn radius
```

No final numerical value of `L` is claimed here because the current final wheelbase has not been documented as a confirmed measurement.

---

# 3.12 Ackermann Mobility

The bicycle model simplifies the front wheels into one equivalent wheel.

The real Piolín steering system uses two front wheels.

During a turn:

```text
INNER FRONT WHEEL
        ↓
Smaller path radius


OUTER FRONT WHEEL
        ↓
Larger path radius
```

An ideal Ackermann relationship can be written as:

```text
THETA_INNER =
atan(L / (R - W/2))
```

and:

```text
THETA_OUTER =
atan(L / (R + W/2))
```

where:

```text
L = wheelbase

W = front track width

R = vehicle turning radius
```

The purpose of the linkage is to allow the two front wheels to better match their different circular paths.

Detailed discussion is available in:

[Steering System](04_steering.md)

---

# 3.13 Turning Center

During an ideal steady turn, the wheel paths can be interpreted relative to an instantaneous center of rotation.

```text
                       TURN CENTER
                            ●


                       R


          FRONT INNER         FRONT OUTER
               \                   \
                \                   \
                 \                   \

          REAR INNER          REAR OUTER
```

The robot does not rotate about its physical center in the same way as a differential-drive robot performing an in-place turn.

Instead, the complete chassis follows a curved path around an external turning center.

This is important when interpreting track clearance.

---

# 3.14 Swept Path

Piolín has a real physical size:

```text
Length = 210 mm

Width  = 150 mm
```

Therefore, the center trajectory alone is not enough to determine whether the robot can clear an obstacle or wall.

During a turn:

```text
Vehicle center
      ↓
Follows one path


Front outside corner
      ↓
Follows wider path


Rear inside region
      ↓
Follows different path
```

The complete area occupied by the moving vehicle is called the **swept path**.

Conceptually:

```text
Straight vehicle footprint:

┌───────────────┐
│               │
│    PIOLÍN     │
│               │
└───────────────┘


During a turn:

         /──────────────
       /
     /
   /   Vehicle envelope
  /
```

This is particularly important during:

```text
Track corners

Obstacle avoidance

Parking
```

---

# 3.15 Why Robot Width Matters

Piolín's confirmed overall width is:

```text
150 mm
```

The navigation software may reason using sensor distances, but the robot itself occupies this full width.

For example:

```text
Sensor detects wall
        ↓
Distance belongs to sensor position
        ↓
Not necessarily vehicle center
```

This means:

```text
Sensor distance
        ≠
Centerline distance
```

unless the physical sensor offset is also considered.

Because the current final lateral sensor offsets are not claimed as confirmed values in this document, no final centerline conversion is presented here.

The important mobility principle is that vehicle geometry and sensor geometry are connected.

---

# 3.16 Velocity

Vehicle velocity describes how quickly Piolín changes position.

The basic relation is:

```text
V =
DELTA_X / DELTA_T
```

where:

```text
DELTA_X
=
Distance traveled


DELTA_T
=
Elapsed time
```

For rotational wheel motion:

```text
V ≈ OMEGA × R
```

where:

```text
OMEGA
=
Wheel angular velocity


R
=
Wheel radius
```

For the rear wheels:

```text
R_REAR ≈ 0.0305 m
```

Therefore, wheel rotational speed directly affects theoretical longitudinal vehicle speed.

---

# 3.17 Why Higher Speed Changes Mobility

Increasing drive speed does more than reduce lap time.

It changes the entire dynamic behavior of the robot.

At higher speed:

```text
Less time to react to sensor changes

Greater momentum

Greater lateral acceleration in turns

Greater stopping distance

Greater sensitivity to steering commands
```

This means:

```text
Speed tuning
      cannot be separated from
Steering tuning
```

A steering command that produces a controlled curve at a lower speed may become too aggressive or unstable at a higher speed.

---

# 3.18 Linear Momentum

Piolín's linear momentum can be represented as:

```text
p =
m × v
```

where:

```text
m = 0.80476 kg
```

and:

```text
v = vehicle velocity
```

As velocity increases:

```text
Momentum increases
```

meaning a larger change in motion is required to modify the robot's trajectory quickly.

This becomes relevant when:

```text
Entering a corner

Stopping near a wall

Changing direction around a pillar

Beginning a reverse maneuver
```

---

# 3.19 Longitudinal Acceleration

Acceleration can be represented as:

```text
a =
DELTA_V / DELTA_T
```

and from Newton's second law:

```text
F_NET =
m × a
```

therefore:

```text
a =
F_NET / m
```

Using Piolín's measured mass:

```text
a =
F_NET / 0.80476
```

This shows that the same available propulsion force produces a particular acceleration according to the robot's mass.

The real acceleration also depends on:

```text
Traction

Motor response

Drivetrain efficiency

Battery condition

Track surface
```

---

# 3.20 Lateral Acceleration

During curved motion, the robot experiences lateral acceleration.

The ideal relationship is:

```text
A_LATERAL =
V² / R
```

where:

```text
V
=
Vehicle speed


R
=
Turn radius
```

This relationship is particularly important because velocity is squared.

For the same curve:

```text
2 × speed
        ↓
4 × lateral acceleration
```

approximately.

This explains why high-speed cornering is significantly more demanding than low-speed cornering.

---

# 3.21 Steering, Speed, and Turn Radius

Three major variables interact during a turn:

```text
STEERING
    +
SPEED
    +
VEHICLE GEOMETRY
    ↓
TURNING BEHAVIOR
```

Increasing steering generally decreases turning radius.

Increasing speed does not directly change the geometric steering radius in the ideal model, but it increases dynamic forces and can change the real path because of:

```text
Tire slip

Mechanical compliance

Delayed response

Momentum
```

Therefore, Piolín's real trajectory is not determined by steering geometry alone.

---

# 3.22 Tire-Track Interaction

The wheels can only transmit useful forces through contact with the track.

For propulsion:

```text
Motor torque
    ↓
Wheel torque
    ↓
Tangential tire force
    ↓
Forward motion
```

For steering:

```text
Wheel orientation
    ↓
Lateral tire force
    ↓
Curved trajectory
```

If available traction is exceeded:

```text
Wheel slip increases
        ↓
Actual trajectory differs from ideal geometry
```

No fixed coefficient of friction is assumed in this documentation because it has not been measured as a confirmed final parameter.

---

# 3.23 Wheel Torque and Linear Force

For an ideal wheel:

```text
F =
TAU / R
```

where:

```text
TAU
=
Wheel torque


R
=
Wheel radius
```

Using the approximate current rear radius:

```text
R_REAR ≈ 0.0305 m
```

the ideal relationship becomes:

```text
F ≈
TAU / 0.0305
```

This does not mean that all calculated force becomes useful vehicle acceleration.

Real losses can include:

```text
Bearing and axle friction

Gear losses

Tire deformation

Wheel slip

Structural resistance
```

---

# 3.24 Mechanical Mobility Efficiency

The complete propulsion path contains several mechanical stages:

```text
Motor electrical input
        ↓
Motor mechanical output
        ↓
Drivetrain
        ↓
Wheel torque
        ↓
Tire-track interaction
        ↓
Vehicle motion
```

Efficiency losses can occur at each stage.

This is why theoretical encoder displacement or force calculations are useful reference models but should not be treated as exact descriptions of real movement.

---

# 3.25 Mobility Feedback

Piolín does not rely only on open-loop motor commands.

Its mobility is continuously influenced by environmental information.

The general control loop is:

```text
Vehicle moves
     ↓
Sensors observe environment
     ↓
EV3 interprets state
     ↓
Drive / steering command changes
     ↓
Vehicle trajectory changes
     ↓
Sensors observe new state
```

This forms a closed-loop navigation system.

The mechanical mobility system is therefore constantly responding to updated sensor information.

---

# 3.26 Lateral Wall Feedback

The main wall-navigation pair consists of:

```text
S2 → Right Ultrasonic

S3 → Left Ultrasonic
```

These sensors allow the EV3 to estimate Piolín's relationship with the side walls.

During normal navigation:

```text
Wall distance
     ↓
Navigation error
     ↓
Steering correction
     ↓
Vehicle changes trajectory
     ↓
Wall distance changes
```

The vehicle does not directly translate laterally.

Instead, the steering system creates a curved path that gradually modifies the lateral position.

---

# 3.27 Dynamic Inner and Outer Wall Roles

The physical sensors remain fixed:

```text
S3 = LEFT

S2 = RIGHT
```

but their navigation roles change with travel direction.

Counterclockwise:

```text
BLUE first
    ↓
S3 LEFT  = INNER

S2 RIGHT = OUTER
```

Clockwise:

```text
ORANGE first
     ↓
S2 RIGHT = INNER

S3 LEFT  = OUTER
```

This allows the same vehicle mobility architecture to operate in either direction around the course.

---

# 3.28 Normal Wall-Following Mobility

During a straight track section, the general mobility process is:

```text
Inner wall detected
        ↓
Distance compared with navigation reference
        ↓
Small steering correction
        ↓
Robot follows controlled curved segment
        ↓
Distance error decreases
        ↓
Steering returns toward center
```

This means wall following is not necessarily a perfectly straight motion.

At a smaller scale, the robot continually performs:

```text
Observe
  ↓
Correct
  ↓
Stabilize
  ↓
Observe again
```

The objective is controlled track-relative motion rather than maintaining an abstract mathematical heading.

---

# 3.29 Why Excessive Corrections Cause Zig-Zag

If steering corrections are too aggressive:

```text
Robot too close to wall
        ↓
Strong correction away
        ↓
Robot crosses desired position
        ↓
Strong correction back
        ↓
Robot crosses again
```

The result is oscillation:

```text
LEFT → RIGHT → LEFT → RIGHT
```

or visually:

```text
~~~~~~
```

instead of:

```text
────────
```

This is why Piolín's mobility depends on balancing:

```text
Correction magnitude

Vehicle speed

Sensor update rate

Steering response
```

---

# 3.30 Corner Mobility

Cornering requires a significantly different movement state from normal wall following.

The current Open Challenge concept follows approximately:

```text
Follow inner wall
        ↓
Inner wall disappears
        ↓
Corner confirmed
        ↓
Steering increases
        ↓
Vehicle begins curved trajectory
        ↓
Outer wall becomes temporary useful reference
        ↓
Vehicle rotates through corner
        ↓
Inner wall reappears
        ↓
Corner exit confirmed
        ↓
Steering reduced
        ↓
Straight-wall navigation resumes
```

This sequence is possible because the mechanical system produces a continuous car-like turn rather than an in-place rotation.

---

# 3.31 Why the Inner Wall Disappears During a Corner

The disappearance of the inner wall is partly a property of track geometry.

As Piolín reaches a corner:

```text
Straight wall surface
        ↓
Ends
        ↓
Side ultrasonic no longer observes
same nearby surface
        ↓
Measured distance increases
```

At the same time:

```text
Steering begins
        ↓
Chassis heading changes
        ↓
Sensor orientation relative to walls changes
```

Therefore, the measurement transition contains both:

```text
Track geometry information
```

and:

```text
Vehicle-motion information
```

This is why corner detection and mobility are tightly connected.

---

# 3.32 Outer Wall During Cornering

During a corner, the outer wall can become more useful as a temporary spatial reference.

Conceptually:

```text
Before corner:

INNER WALL → primary reference


During corner:

INNER wall temporarily disappears
        ↓
OUTER geometry becomes useful


After corner:

INNER wall reappears
        ↓
Primary wall following restored
```

This allows the robot to use environmental geometry rather than requiring a gyroscope.

The previous gyro-based architecture is preserved only in:

[Legacy Gyroscope Configuration](../legacy/01_GConfig.md)

---

# 3.33 Corner Exit Mobility

Completing the geometric turn is not the same as completing a stable corner exit.

Immediately after a turn, the robot may still have:

```text
Non-zero steering

Lateral displacement

Angular misalignment

Residual momentum
```

Therefore, corner recovery requires:

```text
Reduce steering
        ↓
Reacquire useful wall geometry
        ↓
Correct lateral position
        ↓
Stabilize
        ↓
Resume normal wall following
```

This transition prevents the corner maneuver from continuing longer than necessary.

---

# 3.34 Mobility Without a Gyroscope

The current Piolín architecture does not use a gyroscope.

Therefore, the robot does not depend on an absolute or accumulated gyro heading to determine movement around the course.

Current mobility instead relies on:

```text
Physical steering geometry

Lateral ultrasonic measurements

Front ultrasonic safety

Color-based course state

Encoder information where useful

Vision information during obstacles
```

The resulting philosophy is:

```text
Navigate relative to
the actual environment
```

rather than:

```text
Maintain a separately measured
gyro heading
```

This is a major difference between the current robot and the legacy navigation architecture.

---

# 3.35 Front-Wall Safety and Mobility

The front ultrasonic sensor on S1 provides a different type of mobility information.

It does not tell the robot how to follow the side wall.

Instead:

```text
S1
 ↓
Forward distance
 ↓
Potential frontal collision state
```

This information can interrupt or alter normal movement when necessary.

Conceptually:

```text
Normal navigation command
        ↓
Front safety check
        ↓
Safe?
   ┌────┴────┐
   │         │
  YES        NO
   │         │
   ▼         ▼
Continue   Safety response
```

The exact response belongs to the software implementation, but mechanically the purpose is clear: prevent ordinary forward mobility from continuing blindly into a frontal obstacle.

---

# 3.36 Obstacle Challenge Mobility

During the Obstacle Challenge, Piolín must alter its normal trajectory when a colored pillar is detected.

The movement sequence is generally:

```text
Normal navigation
       ↓
Pillar detected
       ↓
Required passing side determined
       ↓
Steering command changes
       ↓
Vehicle moves laterally through curved path
       ↓
Pillar is passed
       ↓
Wall geometry becomes primary again
       ↓
Recovery movement
       ↓
Normal navigation
```

The physical avoidance maneuver must respect the non-holonomic nature of the robot.

Piolín cannot simply shift sideways around a pillar.

It must create a sequence of curved movements.

---

# 3.37 Current Obstacle Passing Direction

In the current HuskyLens configuration:

```text
ID 1
=
GREEN
```

and the required behavior is:

```text
GREEN
   ↓
Pass on the LEFT
```

while:

```text
ID 2
=
RED
```

corresponds to:

```text
RED
  ↓
Pass on the RIGHT
```

The vision system determines **what maneuver is required**.

The mechanical mobility system determines **how that maneuver is physically executed**.

---

# 3.38 Vision Does Not Directly Move the Vehicle

The complete obstacle mobility chain is:

```text
Pillar
  ↓
HuskyLens
  ↓
Obstacle identity
  ↓
Arduino Nano
  ↓
USB
  ↓
EV3
  ↓
Navigation decision
  ↓
Motor B steering
  +
Motor A propulsion
  ↓
Physical avoidance trajectory
```

This distinction is important.

The camera does not control the wheels directly.

It provides information to the EV3.

---

# 3.39 Obstacle Avoidance and Wall Safety

A pillar avoidance maneuver cannot ignore the track walls.

For example:

```text
Pillar requires left bypass
        ↓
Robot steers left
```

but if the left wall is already close:

```text
Available space is reduced
```

Therefore:

```text
Obstacle direction
       +
Wall geometry
       ↓
Feasible physical trajectory
```

The mobility system must satisfy both requirements simultaneously.

This is why obstacle avoidance is a **vehicle-control problem**, not only a vision problem.

---

# 3.40 Post-Obstacle Recovery

After passing a pillar, Piolín must return from the temporary avoidance trajectory to normal navigation.

The recovery sequence can be represented as:

```text
Pillar cleared
     ↓
Obstacle steering no longer required
     ↓
Lateral wall geometry evaluated
     ↓
Steering changes toward recovery
     ↓
Robot moves back toward useful track position
     ↓
Normal wall-following resumes
```

This stage is particularly important because leaving the obstacle correctly but remaining at an unfavorable angle can create a wall collision later.

The obstacle maneuver is therefore not complete until the robot has recovered a usable track-relative trajectory.

---

# 3.41 Recovery Is a Trajectory, Not a Single Steering Command

Because Piolín cannot move sideways directly, centering after an obstacle requires motion over time.

A simplified recovery may look like:

```text
Initial displaced position

      [PIOLÍN]
           \
            \
             \
              ↓

        gradual correction

             ↓

          [PIOLÍN]
             │
             │
             ↓

       recovered path
```

The actual recovery depends on:

```text
Current heading

Wall distances

Vehicle speed

Steering position
```

This is why recovery cannot always be represented by simply commanding steering center immediately.

---

# 3.42 Reverse Mobility

Piolín's drive architecture also supports reverse motion.

Reverse movement changes the relationship between steering and vehicle trajectory.

Conceptually:

```text
FORWARD + LEFT STEERING
        ↓
Front of robot moves left through curve
```

while in reverse:

```text
REVERSE + SAME WHEEL ORIENTATION
        ↓
Rear trajectory changes in opposite geometric relationship
```

This behavior can be useful for:

```text
Repositioning

Front-wall recovery

Parking
```

but requires careful interpretation because the robot still behaves as a car-like system.

---

# 3.43 Reverse Steering Geometry

When reversing, the same steering mechanism remains physically unchanged.

What changes is the direction of vehicle velocity.

The bicycle model can still describe the vehicle, but:

```text
V < 0
```

instead of:

```text
V > 0
```

This reverses the direction in which the heading evolves for a given steering position.

The practical result is familiar from automobile reversing:

> Steering the front wheels one way while reversing causes the rear of the vehicle to move toward the opposite side of the forward turning behavior.

This property is particularly useful for parking-style repositioning.

---

# 3.44 Parking Mobility

Parking requires combining:

```text
Forward movement

Reverse movement

Steering changes

Distance references
```

rather than simply stopping after the final lap.

Because Piolín has Ackermann-style steering, a parking maneuver must account for the swept path of the entire chassis.

Conceptually:

```text
Approach
   ↓
Position vehicle
   ↓
Steer
   ↓
Reverse / forward movement
   ↓
Correct orientation
   ↓
Final position
```

Detailed parking logic is documented separately in:

[Parking Documentation](../software_obstacles_strategy/parking/01_ParkingOverview.md)

---

# 3.45 Mobility and Color Detection

The downward color sensor does not physically steer Piolín.

Its role is to identify course events that affect mobility state.

The relationship is:

```text
Color marking
    ↓
S4 Color Sensor
    ↓
EV3 identifies event
    ↓
Navigation state changes
    ↓
Mobility command may change
```

For example, initial color detection determines travel direction:

```text
BLUE first
    ↓
Counterclockwise
```

```text
ORANGE first
     ↓
Clockwise
```

The color sensor therefore changes the **interpretation of the course**, while Motor A and Motor B physically move the vehicle.

---

# 3.46 Mobility and Course Progress

Color events also provide progress information.

The WRO course contains repeated colored floor markings around the track.

Piolín can use valid color transitions to distinguish:

```text
Current progression
```

from:

```text
Repeated sensor readings
of the same physical marking
```

This becomes relevant for:

```text
Corner counting

Lap progression

Final parking logic
```

The mobility system therefore changes the sensor's physical location over the floor, while the sensor events help the EV3 determine how far the run has progressed logically.

---

# 3.47 Mobility State Transitions

Piolín's movement can be understood as a set of mobility states.

A simplified Open Challenge sequence is:

```text
START
  ↓
DETERMINE DIRECTION
  ↓
STRAIGHT WALL FOLLOWING
  ↓
CORNER ENTRY
  ↓
CORNERING
  ↓
CORNER EXIT
  ↓
STABILIZATION
  ↓
STRAIGHT WALL FOLLOWING
```

The Obstacle Challenge adds states such as:

```text
PILLAR DETECTION

AVOIDANCE

POST-PILLAR RECOVERY
```

These are software states, but each corresponds to a distinct physical mobility behavior.

---

# 3.48 Mobility Priority

Piolín may receive several possible movement influences at the same time.

For example:

```text
Normal wall following requests slight left
```

while:

```text
Obstacle logic requests right
```

or:

```text
Front safety indicates danger ahead
```

These cannot all control the vehicle independently.

A useful system-level priority concept is:

```text
FRONT COLLISION SAFETY
        ↓
LATERAL WALL SAFETY
        ↓
OBSTACLE / CORNER BEHAVIOR
        ↓
NORMAL WALL FOLLOWING
```

This represents the engineering hierarchy between mobility objectives.

The exact software implementation is documented separately.

---

# 3.49 Why Mobility Commands Must Be Blended Carefully

If two controllers simultaneously request large opposing steering changes:

```text
Controller A → LEFT

Controller B → RIGHT
```

the resulting motion can become:

```text
Oscillatory

Delayed

Unpredictable
```

Therefore, the final steering command should represent one coherent physical objective at each moment.

Piolín's mobility system works best when navigation layers cooperate rather than independently forcing the steering actuator.

---

# 3.50 Motor Command vs. Vehicle Response

The command sent to a motor is not the same as the resulting physical movement.

For propulsion:

```text
Motor command
     ↓
Motor torque / speed
     ↓
Drivetrain response
     ↓
Wheel motion
     ↓
Vehicle displacement
```

For steering:

```text
Motor B command
     ↓
Motor encoder position
     ↓
Mechanical linkage
     ↓
Front wheel orientation
     ↓
Vehicle curvature
```

This distinction is fundamental when tuning autonomous movement.

---

# 3.51 Mobility Delay

There is always some delay between sensing a problem and physically changing the vehicle trajectory.

The sequence is:

```text
Environment changes
        ↓
Sensor measurement
        ↓
EV3 processing
        ↓
Motor command
        ↓
Motor movement
        ↓
Mechanical response
        ↓
Vehicle trajectory changes
```

Therefore:

```text
Detection point
      ≠
Physical response point
```

At higher vehicle speed, the robot travels farther during this response interval.

This is one reason early detection and controlled speed are important for obstacle and corner handling.

---

# 3.52 Mobility and Mechanical Repeatability

Navigation algorithms assume that similar commands produce reasonably similar motion.

For example:

```text
Same steering request
        +
Similar speed
        ↓
Similar curved response
```

If mechanical conditions change because of:

```text
Loose linkage

Wheel misalignment

Sensor movement

Increased drivetrain resistance
```

the same software command may produce a different result.

Mobility repeatability therefore depends on the mechanical consistency documented in:

[Chassis Design](02_chassis.md)

---

# 3.53 Vehicle Weight

The current measured Piolín mass is:

```text
0.80476 kg
```

The gravitational force is approximately:

```text
P =
m × g
```

using:

```text
g = 9.81 m/s²
```

therefore:

```text
P ≈ 7.89 N
```

This load is supported by the wheel-track contact points.

Mass affects mobility because it influences:

```text
Acceleration

Momentum

Normal force

Traction demand

Dynamic response
```

---

# 3.54 Mass Does Not Define Mobility Alone

Two robots with identical mass can behave very differently if they have different:

```text
Wheel sizes

Motor torque

Steering geometry

Mass distribution

Tires

Control algorithms
```

Therefore, Piolín's mobility cannot be summarized by one physical parameter.

It is a system property created by:

```text
MASS
  +
GEOMETRY
  +
ACTUATION
  +
TRACTION
  +
CONTROL
```

---

# 3.55 Wheel Size and Mobility

The current wheel configuration is:

```text
FRONT
38.1 mm diameter


REAR
≈ 61.0 mm diameter
```

The larger rear wheel circumference means each full rear-wheel revolution corresponds to more theoretical linear distance.

The front wheel diameter affects:

```text
Ground contact geometry

Steering assembly size

Front ride height
```

while the rear wheel diameter affects:

```text
Drive distance per revolution

Effective force at contact patch

Drivetrain geometry
```

The two wheel sets therefore contribute differently to mobility.

---

# 3.56 Mechanical Center and Straight Mobility

When Motor B is at the calibrated steering center:

```text
STEERING COMMAND = CENTER
```

the front wheels should be approximately aligned with the vehicle's longitudinal direction.

If mechanical center and software center disagree:

```text
Software requests straight
        ↓
Physical wheels remain angled
        ↓
Robot follows curve
```

The wall-following controller may then continuously compensate for what is actually a mechanical calibration problem.

This demonstrates the dependency:

```text
Correct mobility
      requires
Correct steering center
```

---

# 3.57 Minimum and Maximum Steering

The steering mechanism has finite physical limits.

Within those limits:

```text
Small steering command
        ↓
Large-radius trajectory
```

and:

```text
Large steering command
        ↓
Smaller-radius trajectory
```

until mechanical geometry reaches its allowable range.

Commands beyond that physical range cannot produce unlimited additional turning.

Instead, they can result in:

```text
Mechanical binding

Higher motor load

Delayed response

Structural stress
```

The mobility controller must therefore respect the steering system's usable range.

---

# 3.58 Turning Radius Is Not Constant

Piolín does not have one fixed turning radius.

The actual radius depends primarily on:

```text
Steering angle
```

but also in real movement on:

```text
Vehicle speed

Traction

Mechanical alignment

Surface conditions
```

Therefore:

```text
TURNING RADIUS = VARIABLE
```

This is why different mobility states can use different steering levels.

---

# 3.59 Mobility and Track Centering

Centering between walls is not achieved by directly moving Piolín sideways.

Instead:

```text
Position error detected
        ↓
Small steering change
        ↓
Forward movement creates lateral shift
        ↓
Robot approaches desired region
        ↓
Steering reduces toward center
```

This is a dynamic trajectory.

If the robot is centered but still strongly angled:

```text
Position may be correct temporarily
```

while:

```text
Future trajectory is incorrect
```

Therefore, useful centering involves both:

```text
Lateral position
```

and:

```text
Vehicle orientation
```

even without explicitly measuring heading with a gyro.

---

# 3.60 Mobility and Sensor Interpretation

Sensor readings must always be interpreted in the context of vehicle movement.

For example:

```text
Left distance decreases
```

could mean:

```text
Robot translated left
```

or:

```text
Robot rotated toward left wall
```

or:

```text
Wall geometry changed
```

Therefore, no single distance measurement completely describes vehicle motion.

The EV3 uses navigation context to distinguish between:

```text
Straight corrections

Corner transitions

Obstacle maneuvers

Safety conditions
```

---

# 3.61 Current Mobility Without Legacy Hardware

The current vehicle mobility does not depend on:

```text
Gyroscope

PixyCam

Raspberry Pi

Arduino Mega as main controller
```

Those systems belong to previous development stages.

The current mobility architecture is:

```text
                     LEGO EV3
                         │
           ┌─────────────┴─────────────┐
           ▼                           ▼
        Motor A                     Motor B
           │                           │
           ▼                           ▼
    Rear propulsion             Front steering
           │                           │
           └─────────────┬─────────────┘
                         ▼
                  Vehicle movement

                         ▲
                         │
               Environmental feedback
                         │
           ┌─────────────┼─────────────┐
           ▼             ▼             ▼
      Ultrasonics      Color       HuskyLens
```

Historical navigation systems are documented separately in:

[Legacy Documentation](../legacy/00_LEGACY_NOTICE.md)

---

# 3.62 Mobility Responsibility Matrix

| Mobility Function | Primary System |
| :--- | :--- |
| **Forward motion** | Motor A + rear drivetrain |
| **Reverse motion** | Motor A + rear drivetrain |
| **Steering** | Motor B + Ackermann linkage |
| **Straight stabilization** | Lateral ultrasonic feedback + steering |
| **Cornering** | Steering + wall geometry |
| **Frontal protection** | S1 front ultrasonic |
| **Course direction** | S4 color sensor |
| **Course progression** | S4 color sensor |
| **Obstacle identity** | HuskyLens |
| **Obstacle maneuver** | EV3 + Motor A + Motor B |
| **Post-obstacle recovery** | Ultrasonic feedback + steering |
| **Parking movement** | Drive + steering + course state |

The table demonstrates that mobility is distributed across mechanical and sensing subsystems rather than controlled by one component.

---

# 3.63 Open Challenge Mobility Summary

The current Open Challenge movement can be summarized as:

```text
START
  ↓
Read floor marking
  ↓
Determine travel direction
  ↓
Assign inner / outer sensor
  ↓
Follow inner wall
  ↓
Detect corner geometry
  ↓
Execute car-like turn
  ↓
Use outer wall temporarily
  ↓
Reacquire inner wall
  ↓
Stabilize
  ↓
Repeat
  ↓
Track course progress
  ↓
Parking sequence
```

This entire strategy depends on the interaction between:

```text
Rear propulsion
        +
Ackermann steering
        +
Ultrasonic wall geometry
        +
Color-based course state
```

No gyro heading reference is required.

---

# 3.64 Obstacle Challenge Mobility Summary

The Obstacle Challenge adds vision-based trajectory changes:

```text
NORMAL NAVIGATION
        ↓
PILLAR DETECTED
        ↓
IDENTIFY GREEN / RED
        ↓
SELECT PASSING SIDE
        ↓
TEMPORARY AVOIDANCE CURVE
        ↓
WALL SAFETY REMAINS ACTIVE
        ↓
PILLAR CLEARED
        ↓
POSITION RECOVERY
        ↓
NORMAL NAVIGATION
```

The important mechanical principle is:

> Piolín must convert a desired passing side into a physically achievable curved path.

The vision system alone cannot produce that movement.

---

# 3.65 Confirmed Mobility Specifications

The currently confirmed physical values relevant to mobility are:

| Parameter | Confirmed Value |
| :--- | :---: |
| **Robot length** | **210 mm** |
| **Robot width** | **150 mm** |
| **Robot height** | **230 mm** |
| **Robot mass** | **0.80476 kg** |
| **Rear wheel diameter** | **~61.0 mm** |
| **Rear wheel radius** | **~30.5 mm** |
| **Rear wheel circumference** | **~191.5 mm** |
| **Front wheel diameter** | **38.1 mm** |
| **Front wheel radius** | **19.05 mm** |
| **Front wheel circumference** | **~119.7 mm** |
| **Drive actuator** | **Motor A** |
| **Steering actuator** | **Motor B** |
| **Steering type** | **Ackermann-style** |

No final numerical values are claimed here for:

```text
Wheelbase

Front track width

Rear track width

Maximum physical wheel angle

Minimum turning radius

Maximum vehicle speed

Acceleration

Center-of-mass location
```

because these have not been established as confirmed final measurements in the current documentation.

---

# 3.66 Mobility as a Complete System

Piolín's movement should ultimately be understood as a closed physical-control system:

```text
                   TRACK ENVIRONMENT
                          ↓
                        SENSORS
                          ↓
                       LEGO EV3
                          ↓
                Navigation Decision
                          ↓
            ┌─────────────┴─────────────┐
            ▼                           ▼
         Motor A                     Motor B
            ↓                           ↓
      Rear propulsion             Front steering
            └─────────────┬─────────────┘
                          ↓
                  VEHICLE TRAJECTORY
                          ↓
               New physical position
                          ↓
                    New sensor data
                          ↓
                         ...
```

Each movement changes the environment seen by the sensors.

Each new sensor reading changes the next movement command.

This continuous relationship between:

```text
PERCEPTION
     ↓
DECISION
     ↓
ACTUATION
     ↓
MOTION
     ↓
NEW PERCEPTION
```

is the foundation of Piolín's autonomous mobility.

---

# 3.67 Final Mobility Summary

Piolín's final WRO Future Engineers 2026 mobility architecture combines **rear propulsion with front Ackermann steering**.

Motor A provides the longitudinal drive force.

Motor B controls the front-wheel steering mechanism.

The vehicle therefore behaves as a small car rather than a differential-drive robot.

Its mobility is governed by:

```text
Rear wheel rotation

Front wheel orientation

Vehicle mass

Mechanical geometry

Vehicle speed

Track interaction

Sensor feedback
```

The confirmed rear wheel circumference of approximately:

```text
191.5 mm
```

provides a theoretical relationship between encoder rotation and longitudinal displacement.

The Ackermann steering mechanism provides a variable-radius curved trajectory rather than an in-place rotation.

These mechanics allow Piolín to perform:

```text
Wall following

Controlled cornering

Obstacle avoidance

Position recovery

Reverse repositioning

Parking
```

while the EV3 continuously modifies drive and steering according to the surrounding environment.

The central mobility relationship is therefore:

```text
SENSOR INFORMATION
        ↓
EV3 DECISION
        ↓
DRIVE + STEERING
        ↓
PHYSICAL TRAJECTORY
        ↓
NEW SENSOR INFORMATION
```

Piolín's autonomous navigation is not created by software alone.

It emerges from the interaction between the software controller and a physical vehicle whose geometry, wheels, steering system, mass, and traction determine how every command becomes real motion.

---

## Continue Reading

[Steering System](04_steering.md)

[Drivetrain](05_drivetrain.md)

[Mechanical Testing](06_testing.md)

Return to:

[Mechanical Architecture](01_mecharchitecture.md)

[Chassis Design](02_chassis.md)

Related documentation:

[Motors](../components/03_Motors.md)

[Steering Motor](../components/04_SteeringMotor.md)

[Ultrasonic Sensors](../components/05_UltrasonicSensors.md)

[Color Sensor](../components/06_ColorSensor.md)

[HuskyLens](../components/07_HuskyLens.md)

[Wall Following](../software_obstacles_strategy/03_wallfollowing.md)

[Corner Handling](../software_obstacles_strategy/04_cornerhandling.md)

[Obstacle Strategy](../software_obstacles_strategy/06_obstaclestrateg.md)
