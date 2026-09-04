# 4. Steering Motor and Ackermann Actuation

Piolín uses a dedicated **LEGO EV3 motor connected to Motor Port B** to control the direction of the front wheels. Unlike the drive motor, which is responsible for propulsion, the steering motor does not move the robot forward. Its only responsibility is to position the front steering mechanism and therefore determine the direction in which the vehicle travels.

This separation between propulsion and steering is one of the defining characteristics of Piolín's mechanical architecture. Instead of changing direction by varying the speed of left and right drive wheels, Piolín uses a car-like system in which the rear drivetrain generates movement while the front wheels are physically rotated by an Ackermann steering mechanism.

The complete relationship is:

```text
                     LEGO EV3
                         │
                         │ Port B
                         ▼
                  STEERING MOTOR
                         │
                         ▼
                Mechanical Linkage
                         │
                         ▼
               Ackermann Mechanism
                         │
                         ▼
                  Front Wheels
                         │
                         ▼
                Vehicle Direction
```

> [!IMPORTANT]
> The steering motor controls the **mechanical position of the front wheels**.  
> It is completely separate from Motor A, which provides vehicle propulsion.

---

## 4.1 Final Steering Configuration

The final steering system uses the following architecture:

| Parameter | Final Configuration |
| :--- | :--- |
| **Primary Function** | Vehicle directional control |
| **Controller** | LEGO Mindstorms EV3 |
| **EV3 Connection** | **Motor Port B** |
| **Steering Type** | **Ackermann-style front steering** |
| **Steered Wheels** | Front wheels |
| **Front Wheel Diameter** | **1.5 in / 38.1 mm** |
| **Propulsion Responsibility** | None |
| **Position Feedback** | Internal motor encoder |
| **Neutral Reference** | Mechanically centered front-wheel position |

The steering motor operates independently from the drive motor. This allows Piolín to maintain one steering position while changing propulsion speed, or to modify steering without requiring separate left and right drivetrain commands.

---

## 4.2 Why a Dedicated Steering Motor Is Used

A conventional differential-drive robot changes direction by creating a difference between left-wheel and right-wheel speeds.

Piolín uses a different approach.

```text
DIFFERENTIAL DRIVE

Left Motor  ──┐
              ├── Vehicle direction
Right Motor ──┘
```

Piolín instead separates the two functions:

```text
PIOLÍN

Motor A ───────→ Propulsion

Motor B ───────→ Steering
```

This means that the steering system can be considered independently from the drivetrain.

The advantage is particularly important for Piolín's wall-based navigation system. The ultrasonic sensors estimate the robot's relationship with the surrounding walls, and the EV3 converts those measurements into a steering correction. Motor B can then physically change the front-wheel direction without requiring the drive system itself to create the turn.

---

## 4.3 Ackermann Steering Principle

Piolín's front steering mechanism follows the basic principle of **Ackermann steering geometry**.

When a vehicle turns, the inner front wheel travels along a smaller-radius path than the outer front wheel. Because these paths are different, the two wheels should not ideally use exactly the same steering angle.

During a left turn:

```text
                   TURN CENTER
                       ●
                      /|
                     / |
                    /  |
                   /   |
                  /    |
           INNER O     O OUTER
                /       \
               /         \
              O-----------O
                REAR AXLE
```

The inner front wheel turns more strongly because it follows a tighter circular path.

The desired relationship is therefore:

```text
INNER WHEEL ANGLE
        >
OUTER WHEEL ANGLE
```

During a right turn, the opposite front wheel becomes the inner wheel.

```text
LEFT TURN
Left front  = Inner wheel
Right front = Outer wheel


RIGHT TURN
Right front = Inner wheel
Left front  = Outer wheel
```

The steering motor does not control the two front wheels independently. Instead, its movement is transferred through the mechanical steering linkage, which establishes the relationship between the two wheel angles.

---

## 4.4 Steering Motor to Wheel Motion

The EV3 motor does not rotate the front wheels directly around their steering pivots.

Its movement passes through a mechanical linkage.

```text
STEERING MOTOR
      │
      ▼
Motor Rotation
      │
      ▼
Mechanical Linkage
      │
      ▼
Left + Right Steering Arms
      │
      ▼
Front Wheel Angles
```

This distinction is extremely important when interpreting the motor encoder.

If the steering motor moves by:

```text
20°
```

that does **not** automatically mean that the physical front wheels have also moved by:

```text
20°
```

The steering linkage transforms the motor rotation into another mechanical displacement.

Therefore:

```text
MOTOR ENCODER ANGLE
        ≠
PHYSICAL WHEEL ANGLE
```

The encoder value is primarily used as a repeatable software reference for the steering mechanism.

---

## 4.5 Steering Encoder Feedback

The steering motor includes an encoder that allows the EV3 to track its rotational position.

This gives Piolín a reference for where the steering mechanism is currently commanded.

The relationship is:

```text
Motor rotates
     ↓
Encoder position changes
     ↓
EV3 reads steering position
     ↓
Software compares it with target
     ↓
Motor moves toward target
```

Without encoder feedback, the software would know that it had powered the steering motor, but it would not have the same direct rotational reference for the steering mechanism.

Encoder feedback therefore allows the EV3 to use steering positions consistently throughout a run.

---

## 4.6 Steering Center

One of the most important positions in the steering system is the **mechanical center**.

When the front wheels are aligned approximately parallel with the longitudinal axis of Piolín, the steering mechanism is considered centered.

```text
                     FRONT

                 O           O
                 │           │
                 │           │
                 │  PIOLÍN   │
                 │           │
                 O===========O

              STEERING CENTER
```

This centered position becomes the reference from which left and right steering commands are generated.

Conceptually:

```text
RIGHT STEERING
      ←
      |
CENTER
      |
      →
LEFT STEERING
```

The exact sign used by the software depends on the physical orientation of the motor and linkage. What matters is that the same convention is used consistently throughout the final navigation program.

---

## 4.7 Why Steering Center Matters

If the motor encoder indicates that the steering mechanism is centered while the physical wheels are actually slightly rotated, Piolín will not travel perfectly straight even when the requested steering correction is zero.

The resulting behavior would be:

```text
Software command:
STEERING = CENTER

        ↓

Physical wheels:
slightly turned

        ↓

Robot gradually drifts
```

This can easily appear to be a wall-following or sensor problem even though the source is mechanical.

For that reason, Piolín treats steering center as the relationship between the encoder reference and the **physical front-wheel alignment**, not merely as an arbitrary numerical value.

---

## 4.8 Steering Direction Convention

The navigation software produces steering targets relative to the center position.

A simplified convention can be represented as:

```text
             LEFT
              ↑
              │
Negative / Center / Positive
              │
              ↓
             RIGHT
```

or the opposite arrangement depending on how the steering motor is physically installed.

The physical motor orientation determines which encoder direction produces left or right steering. Because this can change if a motor or linkage is installed in the opposite orientation, the documentation does not treat positive motor rotation as a universal definition of left steering.

Instead, Piolín's software uses one consistent final sign convention.

The important relationship is:

```text
STEERING TARGET
       ↓
Motor B rotates
       ↓
Front wheels change direction
       ↓
Vehicle trajectory changes
```

---

## 4.9 Steering Range

The steering mechanism has a finite physical range.

The front wheels cannot rotate indefinitely because the mechanical linkage, steering pivots, and chassis geometry impose limits.

The control relationship is therefore:

```text
FULL LEFT
    │
    │
CENTER
    │
    │
FULL RIGHT
```

Software steering commands are kept within the usable mechanical region rather than continuously attempting to rotate the mechanism beyond its physical limits.

This protects the steering assembly and prevents the motor from remaining loaded against a mechanical stop.

The useful steering range is therefore defined by the complete mechanical system, not by the maximum rotation that the motor itself could theoretically produce when disconnected from the robot.

---

## 4.10 Why Maximum Steering Is Not Always Best

A larger steering command creates a tighter directional change, but the strongest possible steering angle is not automatically the best command for every situation.

During normal wall following, large steering changes can make Piolín oscillate between the two track boundaries.

```text
Large correction left
        ↓
Robot crosses desired path
        ↓
Large correction right
        ↓
Robot crosses again
        ↓
Zig-zag movement
```

The steering mechanism therefore supports a range of corrections.

Small deviations can use relatively small steering adjustments, while larger trajectory errors or corner maneuvers can require stronger wheel angles.

The software determines how much steering is appropriate, while Motor B provides the physical movement required to reach that steering target.

---

## 4.11 Progressive Steering Behavior

Piolín's navigation architecture benefits from steering commands that change progressively rather than continuously jumping between opposite extreme positions.

Conceptually:

```text
CURRENT POSITION
      ↓
New target calculated
      ↓
Controlled change
      ↓
New steering position
```

This reduces sudden mechanical changes and makes the vehicle trajectory easier to predict.

The need for progressive steering is especially important because the ultrasonic sensors are mounted on the same chassis that is being rotated by the steering system. A very aggressive correction changes not only Piolín's trajectory but also the orientation of the sensors relative to the walls.

This creates a direct connection between mechanical steering and sensor interpretation.

---

## 4.12 Steering and Ultrasonic Geometry

Piolín's lateral ultrasonic sensors measure the distance between the robot and the track walls.

When Piolín is approximately parallel to the walls, these measurements are easier to interpret.

```text
WALL
────────────────────────────

        [ PIOLÍN ]
            ↑
        approximately
          parallel

────────────────────────────
WALL
```

When the steering system rotates the vehicle relative to the track, the sensors are no longer perfectly perpendicular to the walls.

```text
WALL
────────────────────────────

          [ PIOLÍN ]
             /

────────────────────────────
WALL
```

The measured distances can therefore change because of both:

```text
Lateral displacement

AND

Vehicle heading
```

This is one reason Piolín avoids unnecessary steering oscillation. Mechanical steering behavior directly influences the quality of the geometric information received by the ultrasonic sensors.

---

## 4.13 Steering During Straight Navigation

During a straight section, Motor B normally performs relatively small corrections.

The inner ultrasonic sensor provides the primary wall reference while the outer sensor contributes additional geometric information.

The control relationship is:

```text
Lateral Ultrasonic Measurements
              │
              ▼
           LEGO EV3
              │
        Wall Error / Geometry
              │
              ▼
      Steering Target
              │
              ▼
           MOTOR B
              │
              ▼
     Small Wheel Correction
```

The goal is not to keep Motor B perfectly motionless during a straight section. Instead, it provides only the steering movement required to keep Piolín on a stable trajectory.

---

## 4.14 Steering During Corner Entry

Corner entry requires a different mechanical behavior from normal straight-line correction.

When the inner wall disappears, the navigation logic interprets the change as a transition in track geometry.

Motor B then receives a stronger directional command appropriate for the turn.

```text
Inner wall disappears
         ↓
Corner confirmed
         ↓
Steering demand increases
         ↓
Motor B changes position
         ↓
Front wheels enter turn
```

The steering motor therefore acts as the mechanical executor of the corner decision made by the EV3.

It does not decide that a corner exists. That decision comes from the sensing and navigation logic.

---

## 4.15 Steering During the Corner

During the corner, the outer ultrasonic sensor can temporarily become the more useful wall reference.

Motor B maintains the directional change required to follow the curved trajectory while the EV3 continues observing the changing wall geometry.

```text
              OUTER WALL
                 ╭──────────
                /
               /
          [ PIOLÍN ]
              ↗
```

As the robot rotates through the turn, the required steering behavior depends on the actual trajectory and the new sensor information received during the maneuver.

The steering motor therefore operates continuously as part of a closed feedback loop rather than moving once to a fixed angle and remaining there regardless of the environment.

---

## 4.16 Steering During Corner Exit

As the next inner wall becomes visible again, Piolín begins transitioning from corner behavior back toward straight navigation.

The steering command is progressively reduced toward the center position.

```text
Inner wall reacquired
        ↓
Corner ending
        ↓
Reduce steering
        ↓
Front wheels approach center
        ↓
Stabilize trajectory
        ↓
Resume normal wall following
```

A controlled return is important because an abrupt movement from a strong corner angle directly to the opposite direction could cause overshoot.

Motor B therefore plays an important role not only in entering a corner but also in recovering from it.

---

## 4.17 Steering During Obstacle Avoidance

During the Obstacle Challenge, Motor B must also respond to pillar information from the HuskyLens vision subsystem.

The control path becomes:

```text
HUSKYLENS
     ↓
ARDUINO NANO
     ↓
LEGO EV3
     ↓
Obstacle direction
     ↓
Steering target
     ↓
MOTOR B
     ↓
Front wheel direction
```

The camera determines relevant visual information, but the steering motor does not communicate with the camera directly.

The EV3 remains between perception and actuation.

This means that obstacle steering can still be influenced by other safety information. If the requested avoidance direction would move Piolín dangerously close to a track wall, the EV3 can modify the final steering command before sending it to Motor B.

---

## 4.18 Steering and Wall Safety

The steering motor is capable of following commands from several navigation behaviors, but the EV3 applies a priority structure before the final target reaches Motor B.

A simplified hierarchy is:

```text
        HIGH PRIORITY

       Frontal Safety
             │
             ▼
       Wall Protection
             │
             ▼
     Obstacle Avoidance
             │
             ▼
      Corner Handling
             │
             ▼
    Normal Wall Following

        LOWER PRIORITY
```

Motor B therefore receives the **final resolved steering command**, rather than receiving independent commands from every sensor subsystem simultaneously.

This prevents several control behaviors from directly fighting over the mechanical steering position.

---

## 4.19 Steering and Propulsion Interaction

Motor B determines wheel direction, but the resulting trajectory also depends on the speed generated by Motor A.

The physical result is:

```text
STEERING ANGLE
      +
DRIVE SPEED
      ↓
ACTUAL TRAJECTORY
```

The same steering position can produce different behavior depending on how quickly Piolín is moving.

At higher speed, inertia can carry the robot farther before its heading changes sufficiently.

At lower speed, the same wheel angle produces a more controlled directional transition.

For this reason, Piolín's steering and propulsion systems are mechanically separate but functionally interconnected.

---

## 4.20 Front Wheel Geometry

Piolín's final front wheels have a measured diameter of approximately:

```text
FRONT_DIAMETER = 1.5 in
```

Using:

```text
1 in = 25.4 mm
```

the diameter is:

```text
FRONT_DIAMETER = 1.5 × 25.4
```

```text
FRONT_DIAMETER = 38.1 mm
```

The corresponding radius is:

```text
FRONT_RADIUS = 19.05 mm
```

and the approximate circumference is:

```text
FRONT_CIRCUMFERENCE = PI × 38.1
```

```text
FRONT_CIRCUMFERENCE ≈ 119.7 mm
```

| Front Wheel Parameter | Final Value |
| :--- | :---: |
| **Diameter** | **38.1 mm / 1.5 in** |
| **Radius** | **19.05 mm** |
| **Circumference** | **~119.7 mm** |
| **Primary Function** | Steering / free rolling |

The front wheels are smaller than the approximately 61 mm rear propulsion wheels.

Because the front wheels are not the main source of propulsion, their principal mechanical responsibility is to roll freely while maintaining the directional geometry commanded by the steering linkage.

---

## 4.21 Inner and Outer Wheel Behavior

When Piolín turns, the front wheels travel along paths of different radii.

For a left turn:

```text
                 TURN CENTER
                     ●

         INNER PATH    OUTER PATH
             ↘           ↘

          O                 O
           \               /
            \             /
             \           /
              O=========O
```

The left front wheel is the inner wheel and therefore follows the smaller-radius path.

For a right turn, the roles are reversed.

This means that the steering linkage must allow the front wheels to adopt different angles rather than forcing perfectly parallel steering during a tight turn.

That relationship is the basis of Piolín's Ackermann-style mechanism.

---

## 4.22 Ackermann Mathematical Relationship

The ideal Ackermann relationship can be represented by:

```text
cot(THETA_OUTER) - cot(THETA_INNER) = W / L
```

where:

```text
W = front track width
L = wheelbase

THETA_INNER = inner front-wheel steering angle
THETA_OUTER = outer front-wheel steering angle
```

An alternative representation using turning radius is:

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
R = turning radius measured from the vehicle center
```

Because:

```text
R - W/2
```

is smaller than:

```text
R + W/2
```

the inner wheel must use the larger steering angle.

The equations explain the geometry of the mechanism without assigning unverified final values to Piolín's wheelbase or track width.

Those older dimensions changed during the robot's mechanical evolution and are therefore not reused as final measurements in this component documentation.

---

## 4.23 Real Ackermann vs. Ideal Ackermann

The equations above describe an ideal geometric model.

Piolín is a physical robot and therefore does not behave as a mathematically perfect Ackermann vehicle.

Real steering behavior is influenced by:

```text
Linkage geometry
Joint clearance
Tire deformation
Mechanical flex
Surface friction
Wheel alignment
```

For that reason, the final documentation describes Piolín as using an **Ackermann-style steering mechanism** rather than claiming perfect theoretical Ackermann geometry.

The purpose of the design is to make the inner and outer wheel paths more appropriate for car-like turning and reduce unnecessary tire scrub compared with skid steering.

It does not imply that the physical wheels satisfy the theoretical equations with zero error at every steering position.

---

## 4.24 Mechanical Play

Any steering mechanism contains some amount of mechanical clearance between its moving elements.

If that clearance becomes too large, a small movement of Motor B may initially move the linkage without producing the same immediate movement at the wheels.

Conceptually:

```text
Motor movement
      ↓
Mechanical clearance
      ↓
Reduced initial wheel movement
```

This can appear in autonomous behavior as steering delay.

The important distinction is that a delayed response is not always caused by software.

```text
Late steering response
        │
        ├── Software command?
        ├── Motor response?
        ├── Mechanical linkage?
        └── Wheel alignment?
```

Piolín's final steering architecture therefore treats mechanical condition as part of navigation reliability.

The documentation does not claim that the mechanism has zero mechanical play. Instead, the design objective is to maintain sufficiently low and repeatable clearance for predictable steering behavior.

---

## 4.25 Mechanical Steering Resistance

Motor B must overcome the mechanical resistance of the steering system.

This resistance comes from several sources, including the linkage joints, steering pivots, tire contact with the competition surface, and the load placed on the front axle.

When Piolín is moving, the wheels can roll while changing direction.

When the robot is stationary, the tires must rotate against the surface without the same rolling movement, which can increase steering resistance.

The steering actuator is therefore part of a loaded mechanical system rather than a motor rotating freely.

This is one reason the software avoids intentionally holding the motor continuously against a physical steering stop.

---

## 4.26 Steering Failure Modes

Several physical conditions can affect steering accuracy.

| Condition | Mechanical Effect | Possible Navigation Effect |
| :--- | :--- | :--- |
| **Incorrect steering center** | Wheels are not straight at the neutral reference | Continuous drift |
| **Loose linkage** | Motor movement is not transferred consistently | Delayed steering |
| **Excessive joint friction** | Increased motor resistance | Slower response |
| **Mechanical limit reached** | Wheels cannot turn farther | No additional trajectory change |
| **Unequal left/right linkage geometry** | Turning behavior differs by direction | Asymmetric cornering |
| **Wheel alignment error** | Front wheels do not follow intended geometry | Tire scrub and path error |
| **Structural movement** | Steering geometry changes under load | Inconsistent autonomous behavior |

These effects illustrate why steering is considered both a software-control problem and a mechanical-design problem.

---

## 4.27 Relationship With the Complete Navigation System

Motor B is the final mechanical actuator of Piolín's directional control loop.

```text
                   ENVIRONMENT
                        │
          ┌─────────────┼─────────────┐
          │             │             │
          ▼             ▼             ▼
     ULTRASONICS      COLOR       HUSKYLENS
          │             │             │
          │             │         ARDUINO
          │             │             │
          └─────────────┴──────┬──────┘
                               ▼
                            LEGO EV3
                               │
                    Navigation / Safety
                               │
                               ▼
                       Steering Target
                               │
                               ▼
                            MOTOR B
                               │
                               ▼
                    Ackermann Linkage
                               │
                               ▼
                       Front Wheels
                               │
                               ▼
                     Vehicle Direction
```

This closes the relationship between perception and mechanical steering.

The sensors do not directly move the wheels. They provide information. The EV3 determines what that information means, and Motor B converts the resulting decision into a physical steering position.

---

## 4.28 Separation of Responsibilities

The final motor architecture gives Piolín a very clear division between propulsion and directional control.

| System | Component | Responsibility |
| :--- | :--- | :--- |
| **Propulsion** | Motor A | Moves Piolín forward or backward |
| **Directional Control** | **Motor B** | Changes front-wheel direction |
| **Wall Perception** | S2 + S3 Ultrasonic Sensors | Provides lateral geometry |
| **Frontal Safety** | S1 Ultrasonic Sensor | Detects dangerous frontal proximity |
| **Course Tracking** | S4 Color Sensor | Provides floor-marking information |
| **Obstacle Perception** | HuskyLens + Nano | Identifies obstacle information |
| **Decision Layer** | EV3 | Resolves final steering command |

This modular structure prevents the steering motor from having to determine why a turn is required.

Motor B only needs to accurately execute the directional target selected by the EV3.

---

## 4.29 Steering System Engineering Trade-Offs

Piolín's steering architecture introduces both advantages and mechanical limitations.

| Design Choice | Advantage | Engineering Consideration |
| :--- | :--- | :--- |
| **Dedicated steering motor** | Independent directional control | Requires additional actuator |
| **Ackermann-style steering** | More car-like turning | More mechanically complex than differential steering |
| **Front-wheel steering** | Separates direction from propulsion | Introduces steering linkage |
| **Encoder reference** | Repeatable motor-position control | Motor angle is not identical to wheel angle |
| **Mechanical center** | Provides consistent neutral reference | Depends on correct physical alignment |
| **Steering limits** | Protects linkage and motor | Restricts minimum possible turning radius |
| **Progressive corrections** | Reduces abrupt trajectory changes | Requires coordinated software control |
| **Small front wheels** | Compact steering assembly | Different rotational behavior from rear wheels |

These trade-offs are accepted because the final design prioritizes predictable car-like movement over the ability to rotate in place.

---

## 4.30 Final Steering Architecture

Piolín's steering system can be summarized as:

```text
                       LEGO EV3
                          │
                        PORT B
                          │
                          ▼
                   STEERING MOTOR
                          │
                          ▼
                  Encoder Reference
                          │
                          ▼
                Mechanical Steering
                       Linkage
                          │
                 ┌────────┴────────┐
                 ▼                 ▼
          LEFT FRONT WHEEL   RIGHT FRONT WHEEL
                 │                 │
                 └────────┬────────┘
                          ▼
                 ACKERMANN-STYLE
                     GEOMETRY
                          │
                          ▼
                  VEHICLE DIRECTION
```

The steering motor does not decide where Piolín should travel. Its purpose is to **translate the EV3's navigation decision into a physical change in front-wheel direction**.

Its encoder provides a repeatable reference, while the mechanical linkage converts motor rotation into the different wheel angles required for Ackermann-style turning.

The final steering architecture therefore establishes a clear relationship:

> **Sensors determine what Piolín sees.**

> **The EV3 determines where Piolín should go.**

> **Motor B physically points Piolín in that direction.**

This separation between perception, decision-making, propulsion, and steering is one of the fundamental design principles of Piolín's final WRO Future Engineers 2026 architecture.
