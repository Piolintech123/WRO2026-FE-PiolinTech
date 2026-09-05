# 5. Drivetrain

Piolín uses a **rear-propulsion drivetrain** actuated by **Motor A**.

The drivetrain is responsible for transforming rotational motion from the drive motor into longitudinal movement of the complete robot.

Its fundamental mechanical chain is:

```text
LEGO EV3
    ↓
Motor A
    ↓
Mechanical Drivetrain
    ↓
Rear Driven Wheels
    ↓
Tire–Track Interaction
    ↓
Vehicle Motion
```

The drivetrain does not determine Piolín's steering direction.

That responsibility belongs to Motor B and the front Ackermann steering system.

The final vehicle architecture therefore separates:

```text
PROPULSION
     ↓
Motor A


STEERING
     ↓
Motor B
```

and combines both at the vehicle level:

```text
PROPULSION
     +
STEERING
     ↓
VEHICLE TRAJECTORY
```

This separation is one of the main characteristics of Piolín's car-like mobility architecture.

For the complete vehicle motion model, see:

[Robot Mobility](03_RMobility.md)

[Steering System](04_steering.md)

---

## 5.1 Current Drivetrain Configuration

The confirmed current propulsion architecture is:

| Element | Current Configuration | Function |
| :--- | :--- | :--- |
| **Main controller** | LEGO EV3 | Commands propulsion |
| **Drive actuator** | Motor A | Generates drivetrain rotation |
| **Driven region** | Rear drivetrain | Transfers propulsion |
| **Rear wheels** | ~61.0 mm diameter | Convert drivetrain rotation into track motion |
| **Front wheels** | 38.1 mm diameter | Primarily directional steering |
| **Steering actuator** | Motor B | Controls front-wheel direction |

The architecture can be represented as:

```text
                           FRONT
                             ↑

                  Front Steering Wheels
                       /           \
                      /             \
                 Ackermann Steering
                        Motor B


                    [ LEGO EV3 ]


                        Motor A
                           │
                           ▼
                    Rear Drivetrain
                      /          \
                     /            \
              Rear Wheel       Rear Wheel

                             ↓
                            REAR
```

This diagram represents subsystem relationships rather than an exact mechanical scale.

---

# 5.2 Role of Motor A

Motor A is dedicated to vehicle propulsion.

Its job is to generate rotational mechanical output that the drivetrain transfers toward the rear driven wheel system.

Conceptually:

```text
Electrical command
       ↓
Motor A
       ↓
Rotational mechanical output
       ↓
Drivetrain
       ↓
Rear-wheel motion
```

Motor A can be commanded to rotate in either direction.

Therefore, the drivetrain supports:

```text
Forward propulsion
```

and:

```text
Reverse propulsion
```

using the same mechanical architecture.

---

# 5.3 Propulsion and Steering Are Independent Functions

The rear drivetrain does not mechanically steer the vehicle.

Similarly, the front steering mechanism is not responsible for generating Piolín's primary propulsion.

The responsibility split is:

```text
Motor A
=
How Piolín moves longitudinally


Motor B
=
Where Piolín is directed
```

The actual path appears only when these two actions are combined.

For example:

```text
Motor A forward
+
Motor B centered
        ↓
Approximately straight forward motion
```

while:

```text
Motor A forward
+
Motor B turned
        ↓
Forward curved motion
```

and:

```text
Motor A reverse
+
Motor B turned
        ↓
Reverse curved motion
```

The drivetrain therefore provides the longitudinal component of every vehicle maneuver.

---

# 5.4 Rear Propulsion Architecture

Piolín uses the rear section of the vehicle for propulsion.

The basic mechanical path is:

```text
Motor A
   ↓
Transmission elements
   ↓
Rear driven assembly
   ↓
Rear wheels
```

This provides a car-like arrangement where:

```text
FRONT
   ↓
Directional steering


REAR
   ↓
Propulsion
```

The exact individual gears or transmission ratio are not numerically specified in this document because a final confirmed drivetrain ratio has not been established in the current documentation.

This avoids treating development-stage mechanical values as final measurements.

---

# 5.5 Rear Wheel Geometry

The current rear wheel diameter is approximately:

```text
D_REAR ≈ 61.0 mm
```

The radius is therefore:

```text
R_REAR =
D_REAR / 2
```

```text
R_REAR ≈ 30.5 mm
```

or:

```text
R_REAR ≈ 0.0305 m
```

The theoretical circumference is:

```text
C_REAR =
PI × D_REAR
```

therefore:

```text
C_REAR ≈
PI × 61.0 mm
```

```text
C_REAR ≈ 191.5 mm
```

This value provides the basis for relating wheel rotation to theoretical linear travel.

---

# 5.6 Wheel Rotation to Linear Motion

For a wheel rolling without slip:

```text
1 complete rotation
        ↓
1 wheel circumference
```

For Piolín:

```text
360° rear-wheel rotation
        ↓
≈ 191.5 mm theoretical travel
```

The general relationship is:

```text
DISTANCE =
(THETA_WHEEL / 360) × C_REAR
```

Therefore:

```text
DISTANCE ≈
(THETA_WHEEL / 360) × 191.5 mm
```

where:

```text
THETA_WHEEL
=
Rear-wheel angular rotation
```

This equation represents an **ideal kinematic relationship**.

---

# 5.7 Example Wheel Displacements

Using:

```text
C_REAR ≈ 191.5 mm
```

the following ideal relationships can be obtained:

| Rear-Wheel Rotation | Theoretical Linear Travel |
| :---: | :---: |
| **90°** | **~47.9 mm** |
| **180°** | **~95.8 mm** |
| **360°** | **~191.5 mm** |
| **720°** | **~383.0 mm** |
| **1080°** | **~574.5 mm** |

These values assume that the listed angle refers to actual **wheel rotation**.

If Motor A and the driven wheel do not rotate at a 1:1 relationship, the drivetrain ratio must also be considered.

---

# 5.8 Motor Encoder Rotation vs. Wheel Rotation

An important distinction is:

```text
MOTOR ROTATION
      ≠
Automatically
WHEEL ROTATION
```

if mechanical gearing exists between Motor A and the rear wheels.

A general drivetrain ratio can be defined as:

```text
G =
THETA_MOTOR / THETA_WHEEL
```

Therefore:

```text
THETA_WHEEL =
THETA_MOTOR / G
```

and the theoretical linear displacement becomes:

```text
DISTANCE =
(THETA_MOTOR / (360 × G))
×
C_REAR
```

or:

```text
DISTANCE ≈
(THETA_MOTOR / (360 × G))
×
191.5 mm
```

If:

```text
G = 1
```

then motor and wheel rotation are equal.

If a different transmission ratio is used, the corresponding ratio must be included.

No final numerical value of `G` is claimed here because it has not been confirmed as a final drivetrain measurement.

---

# 5.9 Why Encoder Distance Is Not Exact Odometry

Even if the transmission ratio is known, encoder-based travel remains an estimate of real track displacement.

The encoder measures:

```text
Motor / wheel rotation
```

not:

```text
Actual robot position on the track
```

Differences can appear because of:

```text
Wheel slip

Tire deformation

Turning motion

Surface irregularities

Mechanical losses

Collisions

Wheel unloading
```

Therefore:

```text
ENCODER DISTANCE
      ≈
THEORETICAL MOTION REFERENCE
```

rather than:

```text
ENCODER DISTANCE
      =
GUARANTEED PHYSICAL POSITION
```

This distinction is especially important during curves and obstacle maneuvers.

---

# 5.10 Straight-Line Drivetrain Motion

During approximately straight movement:

```text
Motor B ≈ steering center
```

while:

```text
Motor A → forward propulsion
```

The rear wheels then attempt to move the chassis longitudinally.

Conceptually:

```text
                 FRONT
                   ↑
                   │
                   │
              [ PIOLÍN ]
                   │
                   │
             Rear Wheels
               ↻     ↺
                   │
                   ↑
                Traction
```

If steering alignment and wheel geometry are correct, the resulting vehicle motion is approximately straight.

However, the drivetrain alone does not guarantee straight movement.

---

# 5.11 Why Propulsion Alone Does Not Guarantee Straight Travel

Even with identical Motor A commands, Piolín can deviate because of:

```text
Front steering misalignment

Wheel alignment

Mechanical resistance

Surface differences

Uneven tire interaction

Chassis geometry
```

Therefore, the complete straight-line system is:

```text
Motor A propulsion
        +
Motor B steering correction
        +
Ultrasonic feedback
        ↓
Controlled straight navigation
```

This is why propulsion and navigation cannot be considered independently.

---

# 5.12 Rotational Speed

The rear-wheel angular velocity can be represented as:

```text
OMEGA =
DELTA_THETA / DELTA_T
```

where:

```text
OMEGA
=
Angular velocity


DELTA_THETA
=
Angular displacement


DELTA_T
=
Elapsed time
```

When expressed in radians per second, the ideal tangential wheel speed is:

```text
V =
OMEGA × R_REAR
```

with:

```text
R_REAR ≈ 0.0305 m
```

Therefore:

```text
V ≈
OMEGA × 0.0305
```

This provides the ideal relationship between wheel angular speed and longitudinal vehicle velocity.

---

# 5.13 Rotations Per Second

If the wheel rotates at:

```text
N revolutions per second
```

then ideal longitudinal speed can also be calculated as:

```text
V =
N × C_REAR
```

For Piolín:

```text
V ≈
N × 0.1915 m/s
```

For example, theoretically:

```text
1 wheel revolution / second
        ↓
≈ 0.1915 m/s
```

assuming rolling without slip.

This example explains the relationship between wheel speed and vehicle speed but is not presented as a measured final Piolín velocity.

---

# 5.14 Motor Speed vs. Vehicle Speed

The EV3 can command a motor speed, but:

```text
MOTOR SPEED
      ≠
Automatically
VEHICLE SPEED
```

Vehicle speed also depends on:

```text
Transmission ratio

Wheel diameter

Track interaction

Mechanical losses

Current steering angle

Vehicle load
```

The drivetrain converts rotational motion into translation through several physical stages.

Therefore:

```text
Motor command
      ↓
Motor rotation
      ↓
Transmission
      ↓
Wheel rotation
      ↓
Track interaction
      ↓
Vehicle speed
```

---

# 5.15 Drive Torque

Motor A generates torque.

Torque describes rotational effort:

```text
TAU
=
Rotational force effect
```

The drivetrain transfers this rotational effort toward the driven wheels.

At the wheel, ideal tangential force is related to wheel torque by:

```text
F =
TAU_WHEEL / R_WHEEL
```

For Piolín's rear wheel:

```text
F ≈
TAU_WHEEL / 0.0305
```

where:

```text
TAU_WHEEL
=
Torque available at driven wheel


F
=
Ideal tangential force
```

This is a theoretical mechanical relationship.

---

# 5.16 Effect of Wheel Radius on Force

For the same wheel torque:

```text
F =
TAU / R
```

therefore:

```text
Smaller radius
      ↓
Greater tangential force
```

and:

```text
Larger radius
      ↓
Lower tangential force
but greater distance per rotation
```

This illustrates an important drivetrain trade-off:

```text
Wheel radius
      affects both
Force and Distance
```

Piolín's rear wheel radius is approximately:

```text
30.5 mm
```

and its circumference is approximately:

```text
191.5 mm
```

so the selected rear wheel geometry influences both propulsion force and motion per revolution.

---

# 5.17 Transmission Ratio

A drivetrain can trade rotational speed for torque through its transmission.

Using the general ratio:

```text
G =
OMEGA_MOTOR / OMEGA_WHEEL
```

an ideal reduction can increase wheel torque while reducing wheel speed.

Conceptually:

```text
Higher speed at motor
        ↓
Mechanical reduction
        ↓
Lower wheel speed
        +
Higher wheel torque
```

The opposite relationship can favor wheel speed at the expense of torque.

This is a fundamental drivetrain design trade-off.

Because Piolín's final numerical gear ratio is not confirmed here, no specific reduction or multiplication ratio is claimed.

---

# 5.18 Mechanical Power

Mechanical rotational power can be expressed as:

```text
P =
TAU × OMEGA
```

where:

```text
P
=
Mechanical power


TAU
=
Torque


OMEGA
=
Angular velocity
```

At the vehicle level, ideal linear mechanical power can also be represented as:

```text
P =
F × V
```

These relationships connect drivetrain torque and speed with vehicle force and velocity.

In a real system:

```text
Input mechanical power
      >
Useful track power
```

because some energy is lost through mechanical inefficiencies.

---

# 5.19 Drivetrain Losses

No drivetrain is perfectly efficient.

Possible losses include:

```text
Axle friction

Gear friction

Bearing friction

Tire deformation

Structural misalignment

Wheel slip
```

The mechanical energy path is:

```text
Motor output
     ↓
Drivetrain transmission
     ↓
Losses occur
     ↓
Wheel output
     ↓
Track motion
```

Therefore, theoretical torque, speed, and distance equations provide useful engineering models but not exact real-world outputs.

---

# 5.20 Drivetrain Alignment

Mechanical alignment is critical to efficient propulsion.

The drivetrain relies on the chassis to keep:

```text
Motor A

Transmission components

Axles

Rear wheel supports
```

correctly positioned relative to one another.

Misalignment can cause:

```text
Additional friction

Binding

Reduced wheel speed

Higher motor load

Uneven motion
```

The relationship is:

```text
Good structural alignment
        ↓
Lower unnecessary resistance
        ↓
More consistent propulsion
```

This is one reason drivetrain design and chassis design are closely connected.

---

# 5.21 Axle Support

Rotating drivetrain elements require stable structural support.

An axle should rotate while its support geometry remains fixed.

Conceptually:

```text
FIXED CHASSIS
      ↓
Axle support
      ↓
ROTATING AXLE
      ↓
Wheel
```

If the axle support moves significantly:

```text
Alignment changes
      ↓
Mechanical resistance changes
      ↓
Propulsion behavior changes
```

The chassis therefore provides the reference structure for drivetrain rotation.

---

# 5.22 Friction in the Drivetrain

Some friction is unavoidable.

The objective is not:

```text
ZERO FRICTION
```

which is physically unrealistic.

Instead, the design aims to avoid unnecessary resistance.

Sources of internal drivetrain resistance can include:

```text
Axle contact

Gear contact

Misaligned elements

Components pressed too tightly together

Structural deformation
```

Excessive internal friction reduces the amount of Motor A output available for useful propulsion.

---

# 5.23 Tire–Track Interaction

The drivetrain only produces useful vehicle motion if the driven wheels can transfer force to the track surface.

The complete chain is:

```text
Motor A
   ↓
Wheel torque
   ↓
Rear tire
   ↓
Track contact
   ↓
Tangential reaction force
   ↓
Vehicle acceleration
```

Without sufficient tire-track interaction:

```text
Wheel rotates
      ↓
Slip occurs
      ↓
Actual displacement is reduced
```

This is why theoretical encoder distance and actual movement can differ.

---

# 5.24 Traction Limit

The maximum useful propulsion force is limited by available traction.

A simplified friction limit can be represented as:

```text
F_TRACTION_MAX
≈
MU × N
```

where:

```text
MU
=
Effective coefficient of friction


N
=
Normal force on driven wheels
```

No numerical value of `MU` is assumed here because the track/tire friction coefficient has not been established as a confirmed current measurement.

Similarly, the exact rear-axle normal load is not claimed because the current center-of-mass position has not been numerically established.

---

# 5.25 Robot Weight

Piolín's confirmed mass is:

```text
m = 0.80476 kg
```

Using:

```text
g = 9.81 m/s²
```

the total approximate gravitational force is:

```text
P =
m × g
```

```text
P =
0.80476 × 9.81
```

```text
P ≈ 7.89 N
```

On a level surface, the total wheel normal reactions together are approximately equal in magnitude to this weight under static conditions.

However, this total load is not necessarily distributed equally between the front and rear wheels.

---

# 5.26 Weight Distribution and Rear Traction

Because Piolín is rear-driven, the amount of normal load supported by the rear wheels influences available traction.

Conceptually:

```text
More useful rear normal load
        ↓
Potential for greater rear traction
```

but vehicle balance also affects steering response.

Therefore, mass placement cannot be optimized only for propulsion.

The complete robot requires a balance between:

```text
Rear-wheel traction

Front steering effectiveness

Structural stability

Sensor positioning
```

The exact current front/rear load distribution has not been measured as a final documented value.

---

# 5.27 Longitudinal Force and Acceleration

From Newton's second law:

```text
F_NET =
m × a
```

so:

```text
a =
F_NET / m
```

Using Piolín's measured mass:

```text
a =
F_NET / 0.80476
```

The available longitudinal acceleration therefore depends on the net propulsion force after considering opposing effects such as:

```text
Mechanical resistance

Rolling resistance

Tire slip
```

This relationship explains why drivetrain efficiency influences how quickly Piolín changes speed.

---

# 5.28 Acceleration Is Not Instantaneous

A motor command change does not instantly create the final vehicle velocity.

The progression is:

```text
EV3 changes Motor A command
        ↓
Motor torque changes
        ↓
Wheel torque changes
        ↓
Net longitudinal force changes
        ↓
Vehicle accelerates
        ↓
Velocity changes over time
```

This is why:

```text
Commanded speed
      ≠
Immediate physical speed
```

Vehicle inertia must always be considered.

---

# 5.29 Momentum

Piolín's linear momentum is:

```text
p =
m × v
```

with:

```text
m = 0.80476 kg
```

As vehicle speed increases:

```text
Momentum increases
```

which affects how quickly the robot can:

```text
Stop

Change trajectory

Reverse direction

Recover after a maneuver
```

The drivetrain therefore influences not only top speed but also the dynamic behavior of the entire robot.

---

# 5.30 Stopping Behavior

Stopping a motor does not necessarily make the physical robot stop at exactly the same instant.

The sequence is:

```text
Drive command reduced
        ↓
Motor output changes
        ↓
Wheel propulsion decreases
        ↓
Vehicle still has momentum
        ↓
Robot decelerates
        ↓
Physical stop
```

The resulting stopping distance depends on:

```text
Vehicle velocity

Vehicle mass

Motor behavior

Track friction

Wheel traction
```

No final stopping-distance value is claimed here because it belongs to empirical testing rather than the drivetrain architecture itself.

---

# 5.31 Forward Mobility

During normal forward movement:

```text
Motor A
    ↓
Forward wheel rotation
    ↓
Rear tire forces
    ↓
Vehicle moves forward
```

At the same time, Motor B may make small steering changes.

Therefore:

```text
FORWARD
```

does not necessarily mean:

```text
PERFECTLY STRAIGHT
```

Piolín can move forward while continuously adjusting its heading through shallow steering changes.

---

# 5.32 Reverse Mobility

Motor A also supports reverse movement.

The drivetrain remains mechanically the same:

```text
Motor A reverses
      ↓
Rear wheels reverse
      ↓
Vehicle velocity changes direction
```

This capability is useful for:

```text
Repositioning

Frontal recovery

Parking maneuvers

Controlled backing movement
```

The steering system remains active during reverse motion, so Piolín continues behaving as a car-like vehicle.

---

# 5.33 Direction Reversal and Inertia

Changing directly from forward propulsion to reverse propulsion requires the drivetrain to reverse rotational direction.

The physical progression is:

```text
Forward velocity
       ↓
Motor command changes
       ↓
Vehicle decelerates
       ↓
Velocity approaches zero
       ↓
Reverse force dominates
       ↓
Vehicle moves backward
```

The robot cannot instantaneously change physical velocity from positive to negative.

This is another consequence of inertia.

---

# 5.34 Reverse Motion and Steering

The front steering geometry does not change fundamentally when the drivetrain reverses.

However, the direction of vehicle velocity changes.

Therefore:

```text
Same wheel steering angle
      +
Forward motion
```

and:

```text
Same wheel steering angle
      +
Reverse motion
```

produce different vehicle trajectories.

This property allows Piolín to perform parking-style repositioning using the same Motor B steering mechanism.

---

# 5.35 Drivetrain During Wall Following

During normal wall following, Motor A provides relatively continuous propulsion while Motor B performs steering corrections.

Conceptually:

```text
Motor A
   ↓
Maintains vehicle movement

+

Motor B
   ↓
Corrects trajectory

+

Ultrasonics
   ↓
Provide wall feedback
```

The drivetrain must therefore provide sufficiently consistent movement for the steering controller to have time to react to changes in wall geometry.

---

# 5.36 Why Drive Speed Affects Wall Following

At higher speed:

```text
Robot travels farther
between sensor updates
```

and:

```text
Less physical distance remains
for corrections
```

Therefore:

```text
Higher drive speed
        ↓
Greater steering demand
        ↓
Potentially more oscillation
```

if the controller is not adjusted accordingly.

The drivetrain speed is therefore part of wall-following behavior even though Motor A does not directly calculate steering.

---

# 5.37 Drivetrain During Corner Entry

A corner combines propulsion and steering.

The mechanical sequence is:

```text
Motor A continues propulsion
        ↓
Corner condition detected
        ↓
Motor B increases steering
        ↓
Vehicle curvature increases
        ↓
Piolín enters corner
```

The drive speed influences how quickly the robot advances while the steering mechanism reaches the required position.

Therefore, corner entry depends on coordination between both motors.

---

# 5.38 Drivetrain During Cornering

During a curve, the rear drivetrain continues pushing the vehicle along the path defined by the front steering geometry.

Conceptually:

```text
Rear wheels
    ↓
Generate forward force

Front wheels
    ↓
Define directional geometry

Combined
    ↓
Curved trajectory
```

The rear wheels do not need to independently steer.

They follow the chassis trajectory created by the steering geometry.

---

# 5.39 Inner and Outer Rear Wheel Paths

During a turn, the left and right rear wheels follow different path radii.

```text
TURN CENTER
     ●


Rear inner wheel
      ↓
Smaller-radius path


Rear outer wheel
      ↓
Larger-radius path
```

This is part of normal car-like motion.

The specific way the rear drivetrain accommodates the different wheel paths depends on the physical transmission arrangement.

Because the final internal rear-drive distribution has not been fully documented numerically here, no unconfirmed differential behavior is claimed.

---

# 5.40 Drivetrain During Corner Exit

At corner exit:

```text
Motor B reduces steering
        ↓
Turning radius increases
        ↓
Motor A continues propulsion
        ↓
Vehicle transitions toward straight motion
```

If propulsion is too aggressive while the steering system is still recovering:

```text
Robot can travel too far
before stabilization
```

This is another reason drive and steering behavior must be tuned together.

---

# 5.41 Drivetrain During Obstacle Avoidance

During obstacle avoidance, the drivetrain provides the forward motion needed for Piolín to move around a pillar.

The sequence is:

```text
Pillar detected
      ↓
Passing side selected
      ↓
Motor B changes steering
      ↓
Motor A continues controlled propulsion
      ↓
Vehicle follows avoidance trajectory
```

The camera alone cannot produce a bypass.

Without drivetrain movement:

```text
Steering angle changes
      ↓
Vehicle remains approximately in place
```

Therefore:

```text
Obstacle trajectory
=
Propulsion + steering
```

---

# 5.42 Drive Speed and Obstacle Reaction Time

Drive speed strongly influences obstacle avoidance.

At greater speed:

```text
Pillar enters view
      ↓
Less time before arrival
      ↓
Less available distance
for steering response
```

At a lower speed:

```text
More physical time
is available
for detection and maneuver
```

This creates a trade-off between:

```text
Competition speed
```

and:

```text
Available reaction distance
```

The drivetrain therefore influences vision-system effectiveness indirectly.

---

# 5.43 Post-Obstacle Recovery

After Piolín has passed a pillar, Motor A continues moving the vehicle while Motor B produces a recovery curve.

```text
Pillar cleared
      ↓
Recovery steering
      +
Forward propulsion
      ↓
Vehicle gradually returns
toward useful track position
```

The recovery cannot occur if the robot simply centers the steering wheels without continuing to move.

Because Piolín is non-holonomic:

```text
Position correction
      requires
Vehicle travel
```

The drivetrain supplies that travel.

---

# 5.44 Frontal Safety Interaction

The S1 front ultrasonic sensor can influence whether normal forward propulsion should continue.

Conceptually:

```text
Motor A forward request
        ↓
Front safety condition checked
        ↓
Safe?
   ┌────┴────┐
   │         │
  YES        NO
   │         │
   ▼         ▼
Continue   Modify /
           interrupt propulsion
```

The front ultrasonic sensor does not mechanically control the drivetrain.

It provides information to the EV3, which can then alter the Motor A command.

---

# 5.45 Lateral Wall Safety and Propulsion

Lateral ultrasonic information also affects how aggressively Piolín should continue a maneuver.

For example:

```text
Obstacle steering
      ↓
Robot moves toward side wall
      ↓
Lateral distance decreases
```

The EV3 can adjust the motion strategy before the trajectory becomes unsafe.

This demonstrates the interaction:

```text
DISTANCE SENSING
      ↓
CONTROL DECISION
      ↓
DRIVE + STEERING
```

rather than treating the drivetrain as an isolated open-loop subsystem.

---

# 5.46 Color Sensor and Drivetrain State

The color sensor does not directly power the drivetrain.

Instead:

```text
Floor marking
      ↓
Color sensor
      ↓
Course event
      ↓
EV3 navigation state
      ↓
Motor A behavior may change
```

Examples include:

```text
Determining initial direction

Tracking course progression

Triggering later run states

Supporting final parking behavior
```

Therefore, the color sensor influences **when and why** the drivetrain changes behavior without being part of the drivetrain mechanically.

---

# 5.47 Parking and the Drivetrain

Parking requires precise use of both forward and reverse propulsion.

A conceptual sequence is:

```text
Approach parking region
        ↓
Control forward motion
        ↓
Change steering
        ↓
Reverse propulsion
        ↓
Reposition chassis
        ↓
Final correction
        ↓
Stop
```

Because Piolín uses Ackermann steering:

```text
Parking
=
Coordinated drive direction
+
Steering position
```

rather than an in-place rotation.

Detailed parking logic is documented in:

[Parking Overview](../software_obstacles_strategy/parking/01_ParkingOverview.md)

---

# 5.48 Drivetrain and Course Progress

Motor A physically moves the color sensor across the floor markings.

Therefore:

```text
Drivetrain displacement
        ↓
Color sensor reaches new marking
        ↓
Course event detected
```

The relationship is cyclical:

```text
Navigation state
     ↓
Motor A moves robot
     ↓
Robot reaches course event
     ↓
Sensor updates navigation state
```

This is another example of mechanics and software interacting through physical motion.

---

# 5.49 Drivetrain and Sensor Timing

Increasing drivetrain speed changes how quickly physical features move relative to the sensors.

For example:

```text
Higher velocity
      ↓
Wall transition occurs faster

Floor marking passes faster

Pillar distance closes faster
```

This means propulsion speed affects:

```text
Sensor reaction time

Color detection duration

Corner transition timing

Obstacle response distance
```

The drivetrain therefore affects nearly every autonomous subsystem through vehicle speed.

---

# 5.50 Mechanical Load During Steering

When Piolín turns, the drivetrain may experience greater resistance than during straight movement.

Possible contributors include:

```text
Tire scrub

Different wheel path radii

Lateral tire forces

Steering geometry

Surface friction
```

Therefore:

```text
Same Motor A command
```

may not produce exactly the same physical velocity during:

```text
Straight motion
```

and:

```text
Sharp turning
```

This is expected in a real mechanical vehicle.

---

# 5.51 Mechanical Load During Obstacle Maneuvers

Obstacle maneuvers can involve:

```text
Large steering angles

Rapid steering transitions

Position recovery
```

which can increase drivetrain demand.

The complete mechanical system must simultaneously provide:

```text
Longitudinal force
        +
Lateral trajectory change
```

through tire-track interaction.

This is another reason obstacle performance depends on both propulsion and steering.

---

# 5.52 Drivetrain and Battery State

Motor A receives its electrical energy through the EV3 vehicle-control power system.

The mechanical output of the motor ultimately depends on available electrical conditions.

Conceptually:

```text
EV3 battery
     ↓
EV3
     ↓
Motor A
     ↓
Mechanical output
```

The battery architecture is documented separately in:

[Battery](../components/08_Battery.md)

[Power Distribution](../components/09_PowerDistribution.md)

No current-specific numerical voltage-drop or drivetrain-current claims are made in this mechanical document.

---

# 5.53 Drivetrain and Structural Load

Motor torque produces an equal and opposite reaction on the motor mounting structure.

Therefore:

```text
Motor A rotates drivetrain
        ↓
Drivetrain resists
        ↓
Reaction load reaches chassis
```

This means the drivetrain depends on strong structural integration.

If the motor or axle supports move under load:

```text
Transmission alignment changes
        ↓
Mechanical efficiency changes
```

The drivetrain and chassis are therefore mechanically interdependent.

---

# 5.54 Mechanical Consistency

Autonomous navigation benefits when similar propulsion commands produce similar physical results.

The desired relationship is:

```text
Similar Motor A command
        +
Similar conditions
        ↓
Similar vehicle response
```

Variability can be introduced by:

```text
Loose axle support

Wheel movement

Drivetrain resistance

Tire contamination

Mechanical binding
```

Mechanical consistency therefore contributes directly to repeatable software behavior.

---

# 5.55 Drivetrain Faults Can Appear as Software Problems

A propulsion problem can change sensor behavior even when the sensors and software are working correctly.

Example:

```text
Increased drivetrain friction
        ↓
Robot moves slower than expected
        ↓
Corner timing changes
        ↓
Sensor transitions occur differently
        ↓
Software appears mistuned
```

Another example:

```text
Wheel slip
        ↓
Encoder rotates normally
        ↓
Robot travels less distance
        ↓
Encoder-based movement appears incorrect
```

The drivetrain should therefore be considered whenever movement behavior becomes inconsistent.

---

# 5.56 Drivetrain Fault Propagation

A mechanical drivetrain issue can propagate through several systems:

```text
Mechanical resistance
        ↓
Reduced vehicle speed
        ↓
Different sensor timing
        ↓
Navigation response changes
        ↓
Different trajectory
```

or:

```text
Wheel slip
        ↓
Reduced real displacement
        ↓
Course position differs
        ↓
Color / corner events occur later
```

This illustrates why system-level troubleshooting is necessary.

---

# 5.57 Rear Wheel Circumference as a Motion Reference

The confirmed rear wheel circumference:

```text
C_REAR ≈ 191.5 mm
```

is useful because it creates a physical scale for drivetrain motion.

The basic relationship:

```text
Wheel rotations
      ↓
Approximate displacement
```

provides a bridge between:

```text
Software encoder values
```

and:

```text
Physical robot movement
```

Even when real displacement differs slightly, the theoretical model is valuable for understanding the system.

---

# 5.58 Distance per Degree of Wheel Rotation

Using:

```text
C_REAR ≈ 191.5 mm
```

the theoretical distance per degree of rear-wheel rotation is:

```text
DISTANCE_PER_DEGREE =
191.5 / 360
```

```text
DISTANCE_PER_DEGREE ≈ 0.532 mm/°
```

Therefore:

```text
1° wheel rotation
≈
0.532 mm ideal travel
```

and:

```text
10°
≈
5.32 mm
```

provided that the angle refers to actual rear-wheel rotation and slip is neglected.

---

# 5.59 Wheel Rotation Required for a Desired Distance

The inverse relationship is:

```text
THETA_WHEEL =
(DISTANCE / C_REAR) × 360
```

Using Piolín's rear wheel circumference:

```text
THETA_WHEEL ≈
(DISTANCE / 191.5) × 360
```

For example, an ideal theoretical travel of:

```text
100 mm
```

would correspond to:

```text
THETA_WHEEL ≈
(100 / 191.5) × 360
```

```text
THETA_WHEEL ≈ 188°
```

approximately.

Again, this represents a theoretical wheel-rotation reference rather than guaranteed track displacement.

---

# 5.60 General Motor Encoder Distance Equation

If the drive transmission ratio is represented by `G`:

```text
G =
THETA_MOTOR / THETA_WHEEL
```

then:

```text
THETA_WHEEL =
THETA_MOTOR / G
```

and:

```text
DISTANCE =
(THETA_MOTOR / G)
×
(C_REAR / 360)
```

For Piolín:

```text
DISTANCE ≈
(THETA_MOTOR / G)
×
0.532 mm
```

This formula remains valid for any confirmed transmission ratio once `G` is known.

It prevents the documentation from incorrectly assuming a 1:1 transmission when that value has not been confirmed.

---

# 5.61 Drivetrain Trade-Offs

A drivetrain must balance several competing requirements:

```text
Speed

Torque

Mechanical simplicity

Mass

Efficiency

Reliability

Available space
```

For example:

```text
More torque
```

can be obtained through mechanical reduction, but this can also reduce:

```text
Wheel rotational speed
```

Similarly:

```text
Larger wheels
```

increase travel distance per rotation but reduce ideal tangential force for the same wheel torque.

The drivetrain therefore represents an engineering compromise rather than a single-variable optimization.

---

# 5.62 Why Maximum Speed Is Not the Only Objective

The fastest possible drivetrain is not necessarily the best drivetrain for autonomous navigation.

Higher vehicle speed can reduce:

```text
Reaction time

Cornering margin

Obstacle avoidance time

Stopping margin
```

while increasing:

```text
Momentum

Lateral acceleration

Dynamic sensitivity
```

Therefore, useful competition performance depends on:

```text
CONTROLLED SPEED
      +
REPEATABLE PROPULSION
      +
RELIABLE STEERING
```

rather than maximum Motor A speed alone.

---

# 5.63 Drivetrain and WRO Track Demands

The WRO Future Engineers course requires the drivetrain to support multiple types of movement:

```text
Long straight sections

Repeated cornering

Obstacle bypasses

Recovery trajectories

Reverse repositioning

Parking
```

A useful drivetrain must therefore operate across:

```text
Different speeds

Different steering conditions

Different movement directions
```

without requiring a different mechanical propulsion system for each stage.

Piolín uses the same Motor A rear-drive architecture throughout the run.

---

# 5.64 Current Drivetrain vs. Legacy Architectures

The current Piolín propulsion architecture should not be confused with earlier development-stage systems.

The final architecture is:

```text
LEGO EV3
    ↓
Motor A
    ↓
Rear drivetrain
    ↓
Rear propulsion
```

The current robot does **not** use:

```text
Two independent drive motors

Raspberry Pi motor control

Arduino Mega as the primary vehicle controller

External DC drive architecture
```

as part of its final documented system.

Historical configurations belong to:

[Legacy Documentation](../legacy/00_LEGACY_NOTICE.md)

---

# 5.65 Confirmed Drivetrain Specifications

The currently confirmed drivetrain-related values are:

| Parameter | Confirmed Value |
| :--- | :---: |
| **Drive actuator** | **Motor A** |
| **Propulsion location** | **Rear** |
| **Rear wheel diameter** | **~61.0 mm** |
| **Rear wheel radius** | **~30.5 mm** |
| **Rear wheel circumference** | **~191.5 mm** |
| **Ideal distance per wheel degree** | **~0.532 mm/°** |
| **Robot mass** | **0.80476 kg** |
| **Approximate robot weight** | **~7.89 N** |
| **Main controller** | **LEGO EV3** |
| **Steering actuator** | **Motor B** |

The following are intentionally **not claimed as final values** in this document:

```text
Final gear ratio

Motor-to-wheel ratio

Maximum drivetrain speed

Measured maximum acceleration

Measured wheel torque

Measured tractive force

Front/rear weight distribution

Coefficient of friction

Measured drivetrain efficiency

Measured stopping distance
```

These values should only be introduced if supported by confirmed current measurements.

---

# 5.66 Drivetrain Responsibility Matrix

| Requirement | Primary Element |
| :--- | :--- |
| **Generate rotational propulsion** | Motor A |
| **Transfer rotation** | Rear drivetrain |
| **Apply force to track** | Rear wheels |
| **Control movement direction** | Motor A direction |
| **Determine steering direction** | Motor B, not drivetrain |
| **Provide approximate displacement reference** | Wheel/encoder rotation |
| **Forward movement** | Motor A + rear wheels |
| **Reverse movement** | Motor A + rear wheels |
| **Corner propulsion** | Motor A while Motor B steers |
| **Obstacle movement** | Motor A + steering coordination |
| **Recovery movement** | Motor A + wall-guided steering |
| **Parking propulsion** | Forward/reverse Motor A commands |

---

# 5.67 Drivetrain as Part of the Closed Control Loop

Piolín's drivetrain participates in a continuous autonomous feedback loop.

```text
                 TRACK ENVIRONMENT
                        ↓
                      SENSORS
                        ↓
                     LEGO EV3
                        ↓
                Navigation Decision
                        ↓
              ┌─────────┴─────────┐
              ▼                   ▼
           Motor A             Motor B
              ↓                   ↓
        DRIVETRAIN            STEERING
              ↓                   ↓
              └─────────┬─────────┘
                        ↓
                VEHICLE MOTION
                        ↓
                 New Position
                        ↓
                 New Sensor Data
                        ↓
                       ...
```

The drivetrain is the part of this loop responsible for creating the translational movement that changes Piolín's physical position.

---

# 5.68 Mechanical Energy Flow

The propulsion system can also be represented as an energy-conversion chain:

```text
Battery Energy
      ↓
EV3 Electrical System
      ↓
Motor A
      ↓
Rotational Mechanical Energy
      ↓
Drivetrain
      ↓
Rear-Wheel Mechanical Energy
      ↓
Tire–Track Interaction
      ↓
Vehicle Kinetic Energy
```

Losses may occur at several stages.

This makes drivetrain performance a combination of:

```text
Electrical input

Motor behavior

Mechanical transmission

Wheel geometry

Track interaction
```

rather than a property of Motor A alone.

---

# 5.69 Engineering Significance

The drivetrain is one of Piolín's core mechanical systems because every autonomous maneuver requires controlled physical displacement.

Without propulsion:

```text
Sensors can observe

EV3 can calculate

Steering can rotate
```

but:

```text
Piolín does not navigate the track
```

The drivetrain converts the robot's decisions into movement through the environment.

It also determines how quickly new environmental information reaches the sensors.

Therefore:

```text
DRIVETRAIN
      affects
MOTION
      affects
SENSOR TIMING
      affects
CONTROL
      affects
NEXT DRIVETRAIN COMMAND
```

This makes propulsion an integral part of the autonomous control system.

---

# 5.70 Final Drivetrain Architecture

Piolín's final drivetrain can be summarized as:

```text
                     LEGO EV3
                         │
                         ▼
                       Motor A
                         │
                         ▼
                 Rear Drivetrain
                         │
                         ▼
                 Rear Driven Wheels
                         │
                         ▼
                Tire–Track Interaction
                         │
                         ▼
               LONGITUDINAL MOTION
                         │
                         │
                         ├──────────────┐
                         │              │
                         ▼              ▼
                    Motor B         Sensor Feedback
                         │              │
                         ▼              │
                    Steering           │
                         │              │
                         └──────┬───────┘
                                ▼
                        VEHICLE TRAJECTORY
```

The drivetrain provides:

```text
Forward propulsion

Reverse propulsion

Corner movement

Obstacle bypass motion

Post-obstacle recovery

Parking movement
```

while Motor B independently controls front-wheel steering.

The confirmed rear wheel geometry provides the principal theoretical motion relationship:

```text
D_REAR ≈ 61.0 mm

R_REAR ≈ 30.5 mm

C_REAR ≈ 191.5 mm
```

and therefore:

```text
Ideal distance per wheel degree
≈
0.532 mm/°
```

The drivetrain should ultimately be understood as the physical link between:

```text
MOTOR ROTATION
       ↓
WHEEL ROTATION
       ↓
TRACK FORCE
       ↓
VEHICLE DISPLACEMENT
```

Its effectiveness depends not only on Motor A, but also on drivetrain alignment, wheel geometry, traction, vehicle mass, steering state, and the mechanical integrity of the chassis.

Together with Piolín's Ackermann steering system, the rear drivetrain forms the complete mobility platform used throughout the WRO Future Engineers 2026 course.

---

## Continue Reading

[Mechanical Testing](06_testing.md)

Return to:

[Mechanical Architecture](01_mecharchitecture.md)

[Chassis Design](02_chassis.md)

[Robot Mobility](03_RMobility.md)

[Steering System](04_steering.md)

Related documentation:

[Motors](../components/03_Motors.md)

[Battery](../components/08_Battery.md)

[Power Distribution](../components/09_PowerDistribution.md)

[Wall Following](../software_obstacles_strategy/03_wallfollowing.md)

[Corner Handling](../software_obstacles_strategy/04_cornerhandling.md)

[Obstacle Strategy](../software_obstacles_strategy/06_obstaclestrateg.md)

[Parking Overview](../software_obstacles_strategy/parking/01_ParkingOverview.md)
