# 5. Mobility, Kinematics, and Mechanical Analysis

Piolín's mobility system was designed around a **car-like Ackermann steering architecture** rather than differential steering. The final robot uses one LEGO EV3 motor for propulsion and a separate EV3 motor for steering, allowing speed and wheel direction to be controlled independently.

The mechanical architecture evolved through several prototypes. Earlier approaches prioritized simplicity, but testing showed that Piolín needed a steering system capable of producing predictable curves without relying on differential wheel speeds. The final Ackermann configuration was therefore selected because it better matches the movement required by the WRO Future Engineers track.

Piolín's final measured dimensions are **210 mm long, 150 mm wide, and 230 mm high**, with a total mass of approximately **0.80476 kg**. The rear wheels have a measured diameter of approximately **2.4 in / 61.0 mm**, while the front steering wheels have a diameter of approximately **1.5 in / 38.1 mm**.

The final mobility architecture can be summarized as:

```text
                         FRONT
                           ↑

                  O                 O
                   \               /
                    \  ACKERMANN  /
                     \ STEERING  /

                    Steering Motor
                       Port B


                    [   PIOLÍN   ]


                  O===============O
                       REAR DRIVE

                      Drive Motor
                        Port A
```

The front wheels determine the direction of travel, while propulsion is provided through the rear drivetrain.

---

## 5.1 Final Mobility Configuration

Piolín separates propulsion and steering into two independent mechanical systems. Motor Port A controls forward motion, while Motor Port B controls the Ackermann steering mechanism.

| Parameter | Final Configuration |
| :--- | :--- |
| **Main Controller** | LEGO Mindstorms EV3 |
| **Drive Motor** | LEGO EV3 Motor |
| **Drive Port** | **A** |
| **Steering Motor** | LEGO EV3 Motor |
| **Steering Port** | **B** |
| **Steering Geometry** | **Ackermann** |
| **Primary Drive Location** | Rear drivetrain |
| **Front Wheel Function** | Steering |
| **Rear Wheel Function** | Propulsion |
| **Robot Mass** | **0.80476 kg** |
| **Robot Length** | **210 mm** |
| **Robot Width** | **150 mm** |
| **Robot Height** | **230 mm** |

The final design deliberately avoids using independent left and right motor speeds to turn the robot. Steering is instead produced mechanically by changing the orientation of the front wheels.

---

## 5.2 Why Ackermann Steering Was Selected

A differential or skid-steer vehicle turns by creating a speed difference between the wheels on opposite sides. This architecture is mechanically simple, but it requires the tires to slide laterally across the surface during many turns.

That lateral tire scrub can create additional friction and makes the exact trajectory dependent on tire grip, robot mass, surface material, and wheel deformation. For an autonomous vehicle that relies on ultrasonic measurements relative to fixed walls, unpredictable lateral movement can make the sensor data more difficult to interpret.

Ackermann steering approaches the problem differently. Instead of forcing the vehicle to rotate by dragging the wheels, the front wheels are mechanically pointed toward the desired turn.

The inner front wheel must turn slightly more than the outer front wheel because it travels around a smaller-radius path.

```text
TURNING LEFT

                     ICR
                      ●
                     /|
                    / |
                   /  |
                  /   |
             O---/----O
            /         /
           /         /
          O---------O
```

The objective is for the wheel paths to approximately share the same instantaneous center of rotation.

This does not mean that real tires experience absolutely zero slip. LEGO joints, tire deformation, linkage play, surface friction, and imperfect geometry still introduce small errors. However, the Ackermann arrangement significantly reduces the tire scrub associated with skid steering and produces a more predictable car-like trajectory.

---

## 5.3 Ackermann Kinematic Model

For ideal Ackermann geometry, the inner and outer front wheels must use different steering angles.

The relationship can be expressed as:

```text
cot(THETA_OUTER) - cot(THETA_INNER) = W / L
```

where:

```text
W = front track width
L = wheelbase
THETA_INNER = physical angle of the inner front wheel
THETA_OUTER = physical angle of the outer front wheel
```

The same geometry can be expressed using the desired turning radius `R`:

```text
THETA_INNER = atan(L / (R - W/2))

THETA_OUTER = atan(L / (R + W/2))
```

Because:

```text
R - W/2 < R + W/2
```

the resulting relationship is:

```text
THETA_INNER > THETA_OUTER
```

This is the fundamental principle behind Piolín's steering linkage.

The final wheelbase and track width are intentionally not assigned numerical values in this document until they are measured directly from the final competition chassis. This avoids mixing dimensions from older prototypes with the geometry of the current robot.

---

## 5.4 Steering Motor Angle vs. Wheel Angle

An important distinction in Piolín's steering system is that the EV3 steering motor angle is **not automatically equal to the physical steering angle of the wheels**.

The motor rotates a mechanical linkage. The linkage then moves the steering arms connected to the front wheels.

Therefore:

```text
STEERING MOTOR ANGLE
        ↓
Mechanical Linkage
        ↓
Steering Arm Motion
        ↓
Actual Wheel Angle
```

The relationship depends on the length and position of the steering links.

This means that a command such as:

```text
Steering motor = 20 degrees
```

does not necessarily mean:

```text
Front wheels = 20 degrees
```

The steering motor encoder is therefore treated as a **repeatable control reference**, while actual wheel steering geometry must be verified physically.

Before starting a navigation run, the front wheels are aligned approximately straight and the steering system uses this position as its neutral reference.

```text
STEER CENTER = 0

Positive steering command → Left
Negative steering command → Right
```

This creates a consistent coordinate system for the navigation software.

---

## 5.5 Mechanical Steering Center

A reliable neutral position is extremely important for Piolín because even a small mechanical steering offset can produce continuous drift during long straight sections.

If the physical wheels are slightly rotated while the software assumes they are centered, Piolín can gradually move toward one track wall even when the requested steering value is zero.

The starting procedure therefore uses a physically centered steering position as the reference for the motor encoder.

```text
Physical wheels straight
        ↓
Set steering reference
        ↓
STEER CENTER = 0
        ↓
Navigation begins
```

This also makes left and right steering commands easier to compare during testing.

Mechanical centering must therefore be checked whenever the steering linkage is modified, loosened, or rebuilt.

---

## 5.6 Wheel Geometry

Piolín uses different wheel sizes at the front and rear.

The measured rear wheel diameter is approximately:

```text
REAR DIAMETER = 2.4 in
```

Converting to millimeters:

```text
2.4 × 25.4 = 60.96 mm
```

Therefore:

```text
REAR DIAMETER ≈ 61.0 mm
REAR RADIUS ≈ 30.5 mm
```

The rear wheel circumference is:

```text
C = PI × D
```

```text
C = PI × 60.96
```

```text
REAR CIRCUMFERENCE ≈ 191.5 mm
```

The front wheel diameter is approximately:

```text
FRONT DIAMETER = 1.5 in
```

which gives:

```text
1.5 × 25.4 = 38.1 mm
```

Therefore:

```text
FRONT DIAMETER = 38.1 mm
FRONT RADIUS = 19.05 mm
```

and:

```text
FRONT CIRCUMFERENCE ≈ 119.7 mm
```

| Wheel Parameter | Front | Rear |
| :--- | ---: | ---: |
| **Measured Diameter** | **1.5 in** | **2.4 in** |
| **Metric Diameter** | **38.1 mm** | **~61.0 mm** |
| **Radius** | **19.05 mm** | **~30.5 mm** |
| **Circumference** | **~119.7 mm** | **~191.5 mm** |
| **Primary Function** | Steering | Propulsion |

The larger rear rolling circumference means that one full rear-wheel rotation corresponds to approximately **191.5 mm of theoretical travel**, assuming no tire slip and a direct one-to-one relationship between wheel rotation and ground movement.

---

## 5.7 Linear Motion Model

The relationship between rear wheel rotation and theoretical vehicle displacement can be written as:

```text
DISTANCE = ROTATIONS × REAR_CIRCUMFERENCE
```

Using Piolín's rear wheels:

```text
DISTANCE = ROTATIONS × 191.5 mm
```

For one full wheel rotation:

```text
DISTANCE ≈ 191.5 mm
```

For five full wheel rotations:

```text
DISTANCE ≈ 957.5 mm
```

which is approximately:

```text
0.96 m
```

This is a theoretical relationship. Real distance can differ slightly because of tire compression, wheel slip, drivetrain play, and the fact that Piolín rarely moves under perfectly ideal conditions.

The relationship is still useful for understanding how wheel rotation translates into physical movement.

---

## 5.8 Speed Relationship

Piolín's theoretical linear speed is related to the rotational speed of the rear wheel.

If the rear wheel rotates at `RPM` revolutions per minute:

```text
V = (RPM × C) / 60
```

where:

```text
V = linear velocity
C = rear wheel circumference
```

Using:

```text
C = 0.1915 m
```

the relationship becomes:

```text
V = (RPM × 0.1915) / 60
```

This formula is more useful for Piolín than claiming one fixed theoretical maximum speed because the actual robot speed depends on motor command, battery condition, drivetrain resistance, mechanical load, and the navigation state.

During competition, maximum speed is also not always the optimal speed. Piolín must leave enough time for the ultrasonic sensors, color sensor, steering mechanism, and obstacle-avoidance system to react before the robot reaches a wall or pillar.

For this reason, speed is treated as a control parameter rather than simply being maximized.

---

## 5.9 Mass and Static Load

Piolín's final measured mass is approximately:

```text
MASS = 0.80476 kg
```

The corresponding gravitational force is:

```text
WEIGHT = MASS × G
```

Using:

```text
G = 9.81 m/s²
```

gives:

```text
WEIGHT = 0.80476 × 9.81
```

```text
WEIGHT ≈ 7.89 N
```

Therefore, the robot applies approximately:

```text
7.9 N
```

of total gravitational force to the ground.

The exact force supported by each wheel depends on the real center-of-mass position and is not assumed to be equally distributed. This is important because claiming an equal 25% load on every wheel without measuring the actual mass distribution would create an inaccurate mechanical model.

---

## 5.10 Drive Force and Torque Relationship

The rear drivetrain must generate enough tangential force at the wheels to accelerate the robot and overcome rolling resistance.

The basic relationship is:

```text
FORCE = MASS × ACCELERATION
```

and wheel torque is related to that force by:

```text
TORQUE = FORCE × WHEEL_RADIUS
```

For Piolín:

```text
MASS = 0.80476 kg
REAR_RADIUS ≈ 0.0305 m
```

Therefore, ignoring rolling resistance for the basic inertial model:

```text
FORCE = 0.80476 × ACCELERATION
```

and:

```text
TORQUE = (0.80476 × ACCELERATION) × 0.0305
```

which simplifies to approximately:

```text
TORQUE ≈ 0.0245 × ACCELERATION
```

where torque is expressed in `N·m` when acceleration is expressed in `m/s²`.

For example, this means that higher requested acceleration directly increases the required wheel torque.

In the physical robot, additional torque is also required to overcome drivetrain friction, bearing resistance, tire deformation, and rolling resistance. Those forces have not been assigned invented coefficients in the final report because they have not yet been independently measured on Piolín.

Instead, the adequacy of the drive system is ultimately verified through loaded driving tests on the actual competition surface.

---

## 5.11 Why Motor Torque Is Not Evaluated Using Stall Torque Alone

A common mistake in drivetrain analysis is to compare the required driving torque directly with a motor's stall torque and conclude that the system has a large safety margin.

Stall torque occurs when the motor is not rotating. It therefore does not represent the torque continuously available during normal driving.

Piolín's design instead treats drivetrain performance as a balance between torque and speed.

```text
More load
   ↓
Motor speed decreases
   ↓
Available torque increases
```

while:

```text
Less load
   ↓
Motor can rotate faster
```

For competition, the important requirement is not simply that the drive motor can move Piolín. It must move the robot at a useful speed while still leaving enough control margin for steering and sensor response.

This is why Piolín's final navigation software uses different speeds for different situations instead of operating the motor permanently at its maximum possible output.

---

## 5.12 Steering Mechanical Load

The steering motor must overcome friction in the front tires and resistance inside the Ackermann linkage.

The steering load is highest when the robot is stationary because the front tires must rotate against the track surface without rolling forward.

Once Piolín is moving, steering generally requires less static tire deformation because the contact patch can move while the wheels change direction.

This led to an important operating principle:

> **Piolín should avoid holding the steering system against its mechanical limit for unnecessary periods.**

Doing so increases motor load, stresses the linkage, consumes additional electrical power, and does not provide additional steering once the physical mechanism has reached its maximum position.

Software steering limits are therefore also a form of mechanical protection.

---

## 5.13 Steering Smoothness and Mechanical Response

The steering motor is physically capable of changing direction rapidly, but commanding an instantaneous jump from a large left angle to a large right angle can create several problems.

The linkage must absorb the sudden motion, the tires experience a rapid change in lateral force, and the robot can begin oscillating between corrections.

Piolín therefore benefits from progressively changing the steering target rather than repeatedly commanding opposite maximum angles.

```text
Current steering
      ↓
Small target change
      ↓
New steering position
      ↓
Next correction
```

This approach reduces mechanical shock while still allowing the steering system to react quickly enough to track geometry.

It also complements the ultrasonic strategy described previously. Small wall errors should normally create small mechanical corrections, while stronger steering should be reserved for situations where the robot actually requires a larger trajectory change.

---

## 5.14 Turning Radius

Ackermann steering does not allow a true zero-radius turn. The minimum turning radius depends mainly on the wheelbase, track width, and maximum physical steering angle.

For a simplified bicycle model, turning radius can be approximated by:

```text
R = L / tan(THETA)
```

where:

```text
R = turning radius
L = wheelbase
THETA = equivalent steering angle
```

As the steering angle increases:

```text
THETA increases
        ↓
tan(THETA) increases
        ↓
R decreases
```

Therefore, stronger steering creates a tighter turn.

However, increasing steering indefinitely is not useful. The mechanical linkage has a physical limit, and very large steering angles can increase tire scrub and steering resistance.

The practical steering limit is therefore chosen according to actual track performance rather than simply maximizing wheel angle.

---

## 5.15 Physical Turning-Radius Calibration

The actual turning radius can be measured without relying entirely on theoretical dimensions.

Piolín can be placed on a large sheet or marked test surface with a constant steering command. The robot is then driven forward slowly while maintaining that fixed steering position.

The path of the rear axle or vehicle center can be marked and the approximate radius of the resulting circle measured.

The same test can be repeated for several steering commands.

A calibration table can then be produced:

| Steering Motor Command | Physical Wheel Direction | Measured Turning Radius |
| :---: | :--- | :---: |
| **0°** | Straight | — |
| **Small Left** | Left | To be measured |
| **Medium Left** | Left | To be measured |
| **Maximum Left** | Left | To be measured |
| **Small Right** | Right | To be measured |
| **Medium Right** | Right | To be measured |
| **Maximum Right** | Right | To be measured |

This test is more useful than assuming that motor encoder angle directly represents vehicle turning radius.

---

## 5.16 Ackermann Alignment

Correct Ackermann geometry depends not only on the steering motor but also on the physical position of the linkage joints.

If the steering rods are incorrectly positioned, both front wheels may rotate by nearly the same angle. This creates a more parallel-steering behavior and increases tire scrub in tight turns.

The desired relationship is:

```text
INNER WHEEL
larger steering angle

OUTER WHEEL
smaller steering angle
```

During mechanical inspection, both steering directions should be checked.

```text
LEFT TURN

Inner wheel  = Left front
Outer wheel  = Right front
```

```text
RIGHT TURN

Inner wheel  = Right front
Outer wheel  = Left front
```

The mechanism must also return consistently to the same straight position after both left and right steering commands.

---

## 5.17 Mechanical Play and Steering Repeatability

A steering mechanism can have correct theoretical geometry but still behave poorly if there is excessive mechanical play.

Any clearance between gears, pins, steering links, wheel hubs, or joints can create a region where the steering motor moves but the wheel angle changes very little.

This is particularly important when the software makes small corrections.

```text
Small motor correction
        ↓
Mechanical play absorbs movement
        ↓
Wheel barely changes
        ↓
Controller requests larger correction
        ↓
Play is suddenly overcome
        ↓
Wheel changes too much
```

This can appear in software testing as delayed steering or oscillation even when the real cause is mechanical.

For this reason, Piolín's mechanical inspections focus on keeping the steering linkage secure while still allowing the joints to move freely.

The goal is not to claim that the mechanism has mathematically zero play. The engineering objective is to reduce play enough that steering commands remain repeatable.

---

## 5.18 Different Front and Rear Wheel Sizes

Piolín uses approximately **38.1 mm front wheels** and **61.0 mm rear wheels**.

The smaller front wheels allow the steering assembly to remain relatively compact, while the larger rear wheels provide a larger rolling circumference for the driven axle.

The important mechanical consequence is that the front and rear wheels rotate at different angular speeds even when the robot is travelling at the same linear velocity.

For a vehicle speed `V`:

```text
FRONT_RPM = (V / FRONT_CIRCUMFERENCE) × 60
```

and:

```text
REAR_RPM = (V / REAR_CIRCUMFERENCE) × 60
```

Because:

```text
FRONT_CIRCUMFERENCE < REAR_CIRCUMFERENCE
```

the front wheels rotate more times per second than the rear wheels at the same vehicle speed.

This is normal because the front wheels are free-rolling steering wheels rather than the primary driven wheels.

---

## 5.19 Mechanical Stability

Piolín's final dimensions are:

```text
Length = 210 mm
Width  = 150 mm
Height = 230 mm
Mass   = 0.80476 kg
```

The chassis must remain rigid enough that sensor position and steering geometry do not change significantly during driving.

This matters because Piolín's software assumes that the ultrasonic sensors maintain a known orientation relative to the chassis. A flexible frame could change the direction of the sensors or alter the steering linkage during acceleration and cornering.

Mechanical rigidity therefore directly affects sensor reliability.

The structure is inspected for movement around the steering assembly, wheel supports, motor mounts, and sensor brackets before competition testing.

---

## 5.20 Center of Mass Considerations

A lower center of mass generally improves vehicle stability because lateral acceleration during a turn produces a smaller roll moment when heavy components are positioned closer to the ground.

Piolín's relatively tall overall height of **230 mm** means that component placement is important. Heavy components such as the EV3 brick should therefore be positioned as securely and as low as the mechanical design reasonably allows without interfering with steering, sensors, or ground clearance.

The final report does not claim a numerical center-of-mass height because it has not been experimentally measured.

Instead, the design objective is to maintain stable contact between all wheels and avoid unnecessary high-mounted mass.

---

## 5.21 Mechanical Interaction With Sensor Navigation

Piolín's mobility system and ultrasonic navigation system cannot be treated as independent systems.

When the steering mechanism changes the robot's heading, the orientation of the lateral ultrasonic sensors relative to the track walls also changes.

This means that a steering correction changes both the vehicle trajectory and the geometry observed by the sensors.

```text
Ultrasonic reading
        ↓
Navigation decision
        ↓
Steering mechanism
        ↓
Robot heading changes
        ↓
Sensor-wall geometry changes
        ↓
New ultrasonic reading
```

This feedback relationship explains why overly aggressive steering can make wall-following unstable even when the sensor measurements themselves are accurate.

The final strategy therefore attempts to correct the robot without creating unnecessary large changes in orientation.

---

## 5.22 Mobility and Front Safety Sensor

The front ultrasonic sensor introduced in the final architecture also interacts with the mobility system.

Unlike the lateral ultrasonic sensors, the front sensor does not normally request a steering angle. Its role is to interrupt propulsion when the measured frontal distance indicates an immediate collision risk.

The mobility hierarchy therefore becomes:

```text
FRONT EMERGENCY CONDITION?
          │
      YES │ NO
          │
          ▼
       BRAKE       → Continue navigation
```

Stopping the drive motor using the EV3 braking mode provides an additional safety layer if the steering trajectory becomes unsafe.

The exact stopping distance must be calibrated according to real vehicle speed because a faster-moving Piolín requires more distance to stop safely.

---

## 5.23 Mechanical Development Evolution

Piolín's mobility architecture was developed through multiple physical configurations.

| Development Stage | Main Configuration | Engineering Lesson |
| :--- | :--- | :--- |
| **Early Mobility Prototype** | Simpler LEGO-based mobility concepts | Easy to modify but less representative of the final vehicle geometry |
| **Ackermann Development** | Mechanical front-wheel steering introduced | Produced more car-like and predictable turning behavior |
| **Steering Refinement** | Linkage geometry and steering limits repeatedly adjusted | Demonstrated the importance of mechanical centering and repeatability |
| **Sensor-Integrated Chassis** | Steering geometry tested together with lateral ultrasonic sensing | Showed that mechanical trajectory directly affects sensor interpretation |
| **Final Architecture** | Rear propulsion + front Ackermann steering | Clear separation between propulsion, steering, navigation, and safety |

The most important change was the transition toward Ackermann steering.

Earlier mobility concepts could change direction, but the final design required the steering mechanism itself to produce a predictable vehicle trajectory that could be understood by the navigation software.

The development process also demonstrated that many apparent software problems can have mechanical causes. Steering delay, asymmetric left/right turns, oscillation, or repeated wall corrections can result from linkage play, poor wheel alignment, or incorrect steering-center calibration.

For this reason, software and mechanical testing are performed together.

---

## 5.24 Skid Steering vs. Ackermann

The main trade-off between the earlier steering concept and the final Ackermann architecture can be summarized as:

| Characteristic | Skid / Differential Steering | Ackermann Steering |
| :--- | :--- | :--- |
| **Mechanical Complexity** | Lower | Higher |
| **Zero-Radius Turn** | Possible | Not possible |
| **Tire Scrub During Turns** | High | Reduced |
| **Car-Like Trajectory** | Limited | Strong |
| **Separate Steering Mechanism** | Not required | Required |
| **Predictability for Wall Sensors** | Lower | Higher |
| **Minimum Turning Radius** | Very small | Mechanically limited |
| **Suitability for Piolín Final Design** | Development concept | **Selected architecture** |

Ackermann steering introduces more mechanical components, but Piolín benefits from the increased predictability of a dedicated steering geometry.

---

## 5.25 Mechanical Failure Mode Analysis

| Failure Mode | Mechanical Effect | Navigation Consequence | Engineering Response |
| :--- | :--- | :--- | :--- |
| **Steering center offset** | Wheels are not straight at command zero | Continuous drift | Re-center mechanically before run |
| **Loose steering linkage** | Motor motion does not immediately move wheels | Delayed or inconsistent correction | Inspect and tighten joints |
| **Excessive linkage friction** | Steering motor responds slowly | Late corner response | Inspect pivot freedom |
| **Mechanical steering limit reached** | Motor cannot create more wheel angle | Increased motor load | Software steering limit |
| **Unequal left/right geometry** | One direction turns tighter | Direction-dependent behavior | Compare both steering directions |
| **Rear wheel slip** | Wheel rotation exceeds ground movement | Position/speed inconsistency | Reduce excessive acceleration |
| **Flexible sensor mount** | Ultrasonic orientation changes | Incorrect distance interpretation | Reinforce sensor mounting |
| **Loose drive transmission** | Motor turns without consistent wheel motion | Reduced propulsion | Inspect drivetrain |
| **High-speed corner instability** | Chassis rolls or loses grip | Path deviation | Reduce corner speed |
| **Front obstacle too close** | Steering alone may not avoid impact | Frontal collision | Front US emergency brake |

The purpose of this analysis is not to claim that mechanical failures have been completely eliminated. It documents which physical problems can influence autonomous performance and how the design attempts to detect or reduce them.

---

## 5.26 Mechanical Testing Procedure

Mobility tests are performed separately from full autonomous runs so that mechanical behavior can be evaluated without confusing software and hardware errors.

Straight-line testing checks whether Piolín maintains approximately the same heading when the steering target is centered. Repeated left and right steering tests check whether the steering linkage returns to the same center position.

Constant-steering tests are used to compare turning radius and left/right symmetry. Low-speed corner tests allow the linkage to be observed while loaded, while higher-speed tests reveal instability that may not appear when the robot is moving slowly.

The drivetrain is also tested under the final robot mass rather than with an unloaded motor because mechanical resistance changes substantially once the complete vehicle is assembled.

The front emergency ultrasonic sensor is evaluated separately by measuring whether the drivetrain can stop Piolín before contacting a controlled test obstacle.

This separation of tests makes it easier to identify whether a problem originates from propulsion, steering, sensor interpretation, or navigation software.

---

## 5.27 Reproducibility Summary

The final mobility architecture can be reproduced from the following verified information:

| Parameter | Final Piolín Configuration |
| :--- | :--- |
| **Vehicle Architecture** | Car-like autonomous vehicle |
| **Steering Type** | **Ackermann** |
| **Drive Motor Port** | **A** |
| **Steering Motor Port** | **B** |
| **Rear Wheel Diameter** | **~61.0 mm / 2.4 in** |
| **Front Wheel Diameter** | **38.1 mm / 1.5 in** |
| **Robot Length** | **210 mm** |
| **Robot Width** | **150 mm** |
| **Robot Height** | **230 mm** |
| **Robot Mass** | **0.80476 kg** |
| **Rear Wheel Circumference** | **~191.5 mm** |
| **Front Wheel Circumference** | **~119.7 mm** |
| **Front Wheel Role** | Steering |
| **Rear Wheel Role** | Propulsion |
| **Final Wheelbase** | Not yet independently re-measured |
| **Final Track Width** | Not yet independently re-measured |

The mechanical control architecture is:

```text
LEGO EV3
│
├── Port A
│      ↓
│   Drive Motor
│      ↓
│   Rear Wheels
│
└── Port B
       ↓
   Steering Motor
       ↓
 Ackermann Linkage
       ↓
   Front Wheels
```

This clearly separates propulsion from directional control.

---

## 5.28 Engineering Conclusion

Piolín's final mobility system is based on a **rear-propelled, front-steered Ackermann architecture** controlled by the LEGO EV3.

The mechanical design was selected because Future Engineers navigation requires more than simply moving the robot forward. Piolín must produce repeatable curves while maintaining sensor geometry that the navigation software can interpret.

Ackermann steering provides a more appropriate car-like motion than skid steering because the inner and outer wheels are allowed to follow different turning paths. Although the mechanism is mechanically more complex and cannot produce a zero-radius turn, the resulting trajectory is more predictable and better suited to Piolín's wall-based autonomous navigation strategy.

The wheel geometry also forms an important part of the mobility design. Piolín uses approximately **61 mm rear drive wheels** and **38.1 mm front steering wheels**, with theoretical circumferences of approximately **191.5 mm** and **119.7 mm** respectively. Combined with a measured robot mass of **0.80476 kg**, these values provide a real physical basis for analyzing propulsion rather than relying on dimensions from older prototypes.

The development process also demonstrated that mobility problems cannot automatically be classified as software problems. Steering-center error, mechanical play, friction, wheel slip, structural movement, and asymmetric linkage geometry can all produce behavior that appears similar to incorrect navigation code.

For this reason, Piolín's final engineering approach treats the mechanical system, sensor system, and software controller as one interconnected vehicle.

> **Reliable autonomous navigation requires the software to understand the sensors, but it also requires the mechanical platform to respond predictably to every steering and propulsion command.**
