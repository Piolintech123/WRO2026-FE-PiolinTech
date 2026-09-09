# 7. HuskyLens Vision Sensor

Piolín uses one **HuskyLens vision sensor** as the main visual perception device for the WRO Future Engineers Obstacle Challenge. While the ultrasonic sensors measure physical distance to the surrounding walls and the color sensor reads floor markings, the HuskyLens provides information about **colored traffic pillars located in front of the robot**.

The HuskyLens is not Piolín's main controller and does not command the motors directly. Its responsibility is perception: it detects and identifies relevant colored obstacles. That information is then transferred through an **Arduino Nano** to the LEGO Mindstorms EV3, where it becomes one of the inputs used by the navigation software.

This creates a clear separation between seeing an obstacle and deciding how the robot should react to it.

```text
HUSKYLENS
    ↓
Detects / identifies obstacle
    ↓
ARDUINO NANO
    ↓
Transfers useful information
    ↓
LEGO EV3
    ↓
Navigation decision
    ↓
Drive + Steering
```

> [!IMPORTANT]
> The HuskyLens provides **visual perception only**.  
> The LEGO EV3 remains responsible for deciding Piolín's final steering, speed, wall-safety behavior, and obstacle-avoidance maneuver.

---

## 7.1 HuskyLens Installed on Piolín

The HuskyLens is physically mounted on Piolín so that it observes the area ahead of the robot during the Obstacle Challenge.

<div align="center">
  <img
    width="237"
    height="223"
    alt="HuskyLens installed on Piolín"
    src="https://github.com/user-attachments/assets/082c8e25-74b9-4d74-9c0c-cd44624037f8"
  />
  <br>
  <sub><b>Figure 7.1.</b> HuskyLens vision sensor installed on Piolín.</sub>
</div>

Its forward-facing position allows the vision subsystem to identify traffic pillars before Piolín physically reaches them.

The camera is therefore observing a completely different region from the other sensors:

```text
                    HUSKYLENS
                        ↓
                 Forward Scene
                        ↓
              Colored Traffic Pillars


LEFT US ←          [ PIOLÍN ]          → RIGHT US
   ↓                                         ↓
Left Wall                               Right Wall


                    COLOR SENSOR
                        ↓
                       Floor
```

This distribution gives each sensing technology a specific physical area to observe.

---

## 7.2 Final Vision Architecture

The final Piolín vision architecture uses three main elements:

| Element | Final Role |
| :--- | :--- |
| **HuskyLens** | Detects and identifies colored pillars |
| **Arduino Nano** | Interfaces the vision sensor with the EV3 |
| **LEGO EV3** | Interprets vision information and decides the vehicle response |

The complete relationship is:

```text
                  ENVIRONMENT
                      │
                      ▼
                COLORED PILLAR
                      │
                      ▼
                  HUSKYLENS
                      │
                      ▼
                ARDUINO NANO
                      │
                     USB
                      │
                      ▼
                  LEGO EV3
                      │
             Navigation Logic
                      │
            ┌─────────┴─────────┐
            ▼                   ▼
         MOTOR A             MOTOR B
          Drive              Steering
```

The HuskyLens and Nano therefore form a **vision subsystem**, while the EV3 remains the main vehicle-control subsystem.

---

## 7.3 HuskyLens and Arduino Nano Interface

Piolín does not connect the HuskyLens directly to an EV3 sensor port.

Instead, the HuskyLens communicates through an Arduino Nano, and the Nano transfers the relevant vision information to the EV3 through USB.

<div align="center">
  <img
    width="589"
    height="458"
    alt="Piolín HuskyLens and Arduino Nano architecture diagram"
    src="https://github.com/user-attachments/assets/2251375a-0c88-4d5c-b805-2ed615658d84"
  />
  <br>
  <sub><b>Figure 7.2.</b> Piolín's final HuskyLens, Arduino Nano, and EV3 vision architecture.</sub>
</div>

This architecture gives the Nano a specialized role.

The Nano does not replace the EV3 and does not independently control Piolín's motors. Instead, it acts as the communication layer between the vision sensor and the main robot controller.

The information path is therefore:

```text
VISUAL INPUT
     ↓
HuskyLens Detection
     ↓
Arduino Nano Interface
     ↓
USB Communication
     ↓
EV3 Navigation Program
```

This division keeps the vision subsystem modular and prevents the main wall-navigation hardware from depending on the camera interface for basic operation.

---

## 7.4 Why an Arduino Nano Is Used

The Arduino Nano serves as an intermediate interface because the HuskyLens and EV3 belong to different hardware ecosystems.

Piolín's main controller already has all four EV3 sensor ports assigned:

```text
S1 → Front Ultrasonic

S2 → Right Ultrasonic

S3 → Left Ultrasonic

S4 → Color Sensor
```

The vision system therefore uses a separate communication path:

```text
HuskyLens
    ↓
Arduino Nano
    ↓
USB
    ↓
EV3
```

This preserves the complete EV3 sensor-port configuration while still allowing Piolín to receive camera information.

The Nano is therefore not an additional navigation computer. It has a much narrower responsibility: **deliver usable vision information to the EV3**.

---

## 7.5 What the HuskyLens Detects

During the Obstacle Challenge, Piolín must distinguish between the colored traffic pillars placed on the field.

The HuskyLens is configured so that the relevant detections have known identifiers.

Piolín's current identification mapping is:

| Obstacle | HuskyLens ID |
| :--- | :---: |
| **Green Pillar** | **ID 1** |
| **Red Pillar** | **ID 2** |

Conceptually:

```text
Camera sees obstacle
        ↓
HuskyLens detection
        ↓
      ID?
      │
 ┌────┴────┐
 ▼         ▼
ID 1      ID 2
GREEN      RED
```

This means that the EV3 does not need to receive an entire camera image and determine the pillar color itself.

The visual classification has already been performed by the vision subsystem before the navigation program makes its movement decision.

---

## 7.6 Green and Red Pillar Meaning

The visual identification is important because the two pillar colors represent different avoidance requirements.

Piolín uses the following obstacle interpretation:

```text
GREEN
  ↓
ID 1
  ↓
Pass on the LEFT side
```

and:

```text
RED
  ↓
ID 2
  ↓
Pass on the RIGHT side
```

The HuskyLens itself does not physically execute these maneuvers.

Its job ends at providing the relevant visual information.

The complete relationship is:

```text
HuskyLens detects GREEN
          ↓
         ID 1
          ↓
Nano transfers detection
          ↓
EV3 interprets obstacle
          ↓
Request LEFT-side passing maneuver
```

or:

```text
HuskyLens detects RED
          ↓
         ID 2
          ↓
Nano transfers detection
          ↓
EV3 interprets obstacle
          ↓
Request RIGHT-side passing maneuver
```

The actual obstacle strategy is documented separately in:

```text
docs/software_obstacles_strategy/05_obstacledetec.md

docs/software_obstacles_strategy/06_obstaclestrateg.md
```

---

## 7.7 Perception Is Separate From Navigation

One of the most important concepts in Piolín's final architecture is the difference between **detecting an obstacle** and **deciding how to move around it**.

The HuskyLens performs the first task.

The EV3 performs the second.

```text
        PERCEPTION

HuskyLens sees pillar
        ↓
Identifies pillar
        ↓
Reports detection


         CONTROL

EV3 receives detection
        ↓
Checks wall geometry
        ↓
Checks safety conditions
        ↓
Determines steering
        ↓
Determines propulsion
```

This separation is important because simply seeing a green or red pillar does not describe the entire situation around the robot.

Piolín may simultaneously be close to a track wall, entering a corner, recovering from a previous avoidance maneuver, or approaching a frontal safety condition.

The EV3 must therefore combine the visual detection with the rest of the robot's sensor information before generating the final motor commands.

---

## 7.8 HuskyLens vs. Ultrasonic Sensors

The HuskyLens and ultrasonic sensors provide fundamentally different types of environmental information.

The HuskyLens answers:

> **What colored obstacle is visible ahead?**

The ultrasonic sensors answer:

> **Where are the surrounding track walls and is something dangerously close?**

Their roles can be compared as follows:

| System | Information Provided | Main Purpose |
| :--- | :--- | :--- |
| **HuskyLens** | Visual obstacle identity | Pillar recognition |
| **Left US — S3** | Left-side distance | Wall geometry |
| **Right US — S2** | Right-side distance | Wall geometry |
| **Front US — S1** | Frontal distance | Emergency frontal safety |

The systems therefore complement rather than replace each other.

```text
             HUSKYLENS
                 ↓
         Obstacle Identity
                 │
                 │
                 ▼
              LEGO EV3
                 ▲
                 │
                 │
      Ultrasonic Distances
                 ↑
       S1      S2      S3
```

The EV3 receives both **what is ahead** and **where the physical boundaries are**.

---

## 7.9 Vision and Wall Safety

A camera detection should not automatically override every other sensor.

For example, the HuskyLens may indicate that Piolín should move toward one side of a pillar, but an ultrasonic sensor may simultaneously indicate that the requested trajectory would move the robot dangerously close to a wall.

The architecture therefore separates an **avoidance request** from the **final steering command**.

```text
HuskyLens
     ↓
Suggested obstacle direction
     │
     ▼
    EV3
     ▲
     │
Ultrasonic wall information
     │
     ▼
Final safe steering command
```

This prevents the camera subsystem from becoming the sole authority over steering.

The vision information contributes to the navigation decision, but wall geometry and safety remain active.

---

## 7.10 Front Ultrasonic Safety Remains Independent

The front ultrasonic sensor on S1 also remains active during vision-based navigation.

The HuskyLens may recognize a pillar visually, but the front ultrasonic sensor solves a separate problem: identifying dangerously close frontal proximity.

The control relationship can therefore be understood as:

```text
HUSKYLENS
    ↓
What obstacle is it?


FRONT US
    ↓
Is something dangerously close?


LATERAL US
    ↓
Where are the track walls?
```

All three questions are useful, but they are not interchangeable.

This is why Piolín uses multiple types of sensors instead of attempting to make the camera responsible for all environmental perception.

---

## 7.11 HuskyLens Field of View

Unlike the ultrasonic sensors, the HuskyLens observes the environment through a camera field of view.

Only objects that appear within that visible region can be recognized.

Conceptually:

```text
                 CAMERA VIEW
                    \     /
                     \   /
                      \ /
                  [ HUSKYLENS ]
                       │
                       │
                    [PIOLÍN]
```

A pillar outside the visible camera region cannot provide useful visual information until it enters the HuskyLens view.

This is an important physical characteristic of camera-based perception.

It also explains why the ultrasonic sensors remain active even when vision is being used. The camera provides rich visual information inside its view, while the ultrasonic sensors continue providing geometric distance information around the robot.

---

## 7.12 Why Camera Position Matters

Because the HuskyLens has a limited viewing region, its mechanical mounting directly affects what Piolín can see.

A camera mounted too low may have part of its view blocked by the robot structure.

A camera positioned poorly relative to the chassis may lose sight of pillars during steering maneuvers.

The relationship is:

```text
CAMERA POSITION
      ↓
VISIBLE REGION
      ↓
WHEN PILLAR ENTERS VIEW
      ↓
WHEN DETECTION BECOMES AVAILABLE
```

For this reason, the HuskyLens should be considered both an electronic component and part of Piolín's mechanical perception geometry.

The installation shown in **Figure 7.1** integrates the camera into the front-facing perception system of the robot.

---

## 7.13 Camera Information During a Turn

The appearance of a pillar in the camera can change substantially while Piolín is turning.

As the vehicle rotates, the camera rotates with the chassis.

```text
Before turn:

          PILLAR
             ●
             │
             │
        [ PIOLÍN ]


During turn:

     PILLAR
        ●
          \
           \
        [ PIOLÍN ]
             ↗
```

The pillar may move across the visible image or leave the camera view entirely even though it still exists physically beside the robot.

This is another reason the final system does not interpret loss of camera detection as proof that the surrounding environment is completely clear.

The ultrasonic sensors and navigation state continue providing context after the visual target leaves the field of view.

---

## 7.14 Object Detection and Robot Reaction Are Different Events

The instant when a pillar is first detected is not necessarily the same instant when the robot completes its avoidance maneuver.

The sequence is more accurately represented as:

```text
Pillar enters camera view
        ↓
HuskyLens detects pillar
        ↓
Detection reaches EV3
        ↓
EV3 requests avoidance
        ↓
Steering changes
        ↓
Robot trajectory changes
        ↓
Pillar leaves relevant region
        ↓
Navigation recovers
```

This distinction helps explain why vision, steering, propulsion, and wall sensing must work together.

The camera can provide early information, but the physical vehicle still needs time and distance to respond.

---

## 7.15 HuskyLens Input and Output

The HuskyLens can be viewed as an information-processing stage between the physical environment and Piolín's navigation software.

The physical input is the visible scene in front of the robot.

The useful output is a simplified obstacle identification that can be communicated to the EV3.

```text
PHYSICAL INPUT
Visible traffic pillar
        ↓
HUSKYLENS
        ↓
Visual recognition
        ↓
Detected object / ID
        ↓
ARDUINO NANO
        ↓
Communication data
        ↓
LEGO EV3
```

This is fundamentally different from the ultrasonic sensor system.

The ultrasonic sensors primarily provide numerical distances.

The HuskyLens provides information related to **visual object identity**.

---

## 7.16 Why Raw Camera Processing Is Not Performed by the EV3

The EV3 is already responsible for:

```text
Ultrasonic navigation
Color detection
State management
Motor control
Steering
Safety logic
Course progress
```

The final architecture does not require it to also process a complete raw camera stream.

Instead, visual recognition is handled before the relevant information reaches the EV3.

```text
RAW VISUAL ENVIRONMENT
          ↓
      HUSKYLENS
          ↓
Useful detection
          ↓
         NANO
          ↓
         EV3
```

This reduces the amount of visual-processing responsibility placed on the main vehicle controller.

The EV3 can therefore focus on what it does after the object has been identified: deciding how Piolín should move.

---

## 7.17 Why HuskyLens Replaced PixyCam

Piolín previously experimented with a **PixyCam-based vision system**.

That system demonstrated that camera-based color information could be useful for the Obstacle Challenge, but it was not retained as the final architecture.

The final robot instead uses the HuskyLens with the Arduino Nano interface.

The important engineering evolution was:

```text
PIXyCam EXPERIMENT
        ↓
Vision proved useful
        ↓
Vision architecture reconsidered
        ↓
HUSKYLENS + ARDUINO NANO
        ↓
Final vision subsystem
```

The PixyCam documentation remains preserved as part of Piolín's engineering history in:

```text
docs/legacy/02_CameraPixy.md
```

Keeping that previous architecture in the legacy section makes it possible to document the evolution of the vision system without confusing it with the final robot configuration.

---

## 7.18 Why the HuskyLens Does Not Replace the Color Sensor

Both devices use optical information, but their functions are different.

The HuskyLens is oriented toward the environment ahead of the robot.

The LEGO Color Sensor is oriented downward toward the competition mat.

```text
HUSKYLENS
    ↓
Forward vision
    ↓
Pillar detection


COLOR SENSOR
    ↓
Floor observation
    ↓
Blue / Orange course markings
```

The HuskyLens therefore cannot simply replace the floor-facing sensor.

Similarly, the downward color sensor cannot identify pillars located several centimeters or more in front of Piolín.

Their sensing directions and navigation responsibilities are fundamentally different.

---

## 7.19 Why the HuskyLens Does Not Replace Ultrasonic Navigation

Visual recognition provides obstacle identity, but it does not provide Piolín with the same wall geometry supplied by the lateral ultrasonic sensors.

The Open Challenge can therefore operate without relying on HuskyLens obstacle recognition.

The architecture is intentionally modular:

```text
OPEN CHALLENGE

Ultrasonic Sensors
      +
Color Sensor
      +
EV3
      ↓
Track Navigation
```

while:

```text
OBSTACLE CHALLENGE

Ultrasonic Navigation
      +
Color Sensor
      +
HuskyLens / Nano
      ↓
Track + Obstacle Navigation
```

The vision subsystem extends Piolín's perception rather than replacing the navigation system that already exists.

---

## 7.20 Vision Data and Steering

The HuskyLens never communicates directly with Motor B.

Instead:

```text
HuskyLens
    ↓
Arduino Nano
    ↓
EV3
    ↓
Navigation logic
    ↓
Steering target
    ↓
Motor B
```

This means that the visual detection can influence the desired steering direction while still allowing the EV3 to apply wall-protection limits and other safety behavior.

The camera therefore provides a **navigation input**, not a direct actuator command.

---

## 7.21 Vision Data and Propulsion

The same principle applies to Motor A.

A detected pillar can cause the EV3 to modify propulsion behavior during the avoidance maneuver, but the HuskyLens does not directly control drive speed.

```text
Obstacle detected
      ↓
EV3 receives visual information
      ↓
Obstacle state selected
      ↓
Drive speed determined
      ↓
Motor A command
```

This allows speed and steering to be coordinated according to the complete navigation situation.

---

## 7.22 Sensor Responsibility During Obstacle Navigation

The main sensors remain active together during the Obstacle Challenge.

| Sensor / System | Primary Information |
| :--- | :--- |
| **HuskyLens** | Colored pillar identity |
| **Arduino Nano** | Vision communication |
| **Front US — S1** | Frontal safety |
| **Right US — S2** | Right-wall geometry |
| **Left US — S3** | Left-wall geometry |
| **Color Sensor — S4** | Course direction and progress |
| **EV3** | Final navigation decision |

The resulting perception model is:

```text
                   VISUAL IDENTITY
                       HUSKYLENS
                           │
                           ▼
                        NANO
                           │
                           ▼
                      ┌─────────┐
WALL GEOMETRY ───────→│   EV3   │←────── COURSE STATE
 Ultrasonics           └────┬────┘        Color Sensor
                            │
                            ▼
                    Movement Decision
```

This is the fundamental sensor-fusion structure of Piolín's obstacle architecture.

---

## 7.23 Loss of Visual Detection

A detected pillar can eventually leave the camera field of view as Piolín moves around it.

That does not necessarily mean the obstacle has vanished physically.

```text
Pillar visible
     ↓
Avoidance begins
     ↓
Robot changes heading
     ↓
Pillar moves outside camera view
```

The navigation system therefore must distinguish between:

```text
No pillar currently visible
```

and:

```text
No obstacle interaction exists
```

These are not always the same condition.

Piolín's wall sensors and navigation state continue operating even when a pillar is no longer visible to the camera.

This helps the robot return from obstacle avoidance toward normal track navigation.

---

## 7.24 Camera Limitations

The HuskyLens provides valuable visual information, but the system has physical limitations.

| Limitation | Effect on Piolín |
| :--- | :--- |
| **Finite field of view** | Pillars outside the visible region cannot be identified |
| **Robot rotation** | Pillar position in the image changes during turns |
| **Mechanical obstruction** | Chassis components can reduce visible area if poorly positioned |
| **Distance to object** | Apparent pillar size changes |
| **Lighting conditions** | Visual appearance of colors can change |
| **Loss of target from view** | Camera information may disappear during an active maneuver |

These limitations are why Piolín does not depend on vision alone for autonomous navigation.

The HuskyLens is used where visual identification is necessary, while other sensors continue solving geometry and safety problems.

---

## 7.25 Vision System Modularity

The vision subsystem is intentionally isolated from Piolín's most basic motion-control architecture.

If represented by subsystem:

```text
                 PIOLÍN

        ┌─────────────────────┐
        │     NAVIGATION      │
        │ EV3 + Ultrasonics   │
        │ + Color Sensor      │
        └──────────┬──────────┘
                   │
                   │
        ┌──────────▼──────────┐
        │       VISION        │
        │ HuskyLens + Nano    │
        └─────────────────────┘
```

The modules exchange information, but the navigation subsystem does not need the HuskyLens to perform every fundamental movement.

This makes the architecture easier to understand and prevents one camera-related issue from automatically redefining every other sensing responsibility.

---

## 7.26 HuskyLens Responsibility Matrix

The final responsibilities of the HuskyLens can be summarized as:

| Function | HuskyLens Role |
| :--- | :---: |
| **Detect green pillar** | **Primary** |
| **Detect red pillar** | **Primary** |
| **Provide obstacle ID** | **Primary** |
| **Determine wall distance** | No |
| **Determine floor color** | No |
| **Determine initial driving direction** | No |
| **Control Motor A directly** | No |
| **Control Motor B directly** | No |
| **Make final safety decision** | No |
| **Provide visual input to EV3** | **Yes** |

This narrow responsibility is intentional.

The HuskyLens is a perception device, while the EV3 remains the decision-making device.

---

## 7.27 Final Vision Data Flow

The complete Piolín vision data flow can be summarized as:

```text
                      TRAFFIC PILLAR
                            │
                            ▼
                       HUSKYLENS
                            │
                     Visual Detection
                            │
                            ▼
                      ARDUINO NANO
                            │
                           USB
                            │
                            ▼
                        LEGO EV3
                            │
                   Obstacle Strategy
                            │
            ┌───────────────┴───────────────┐
            ▼                               ▼
        DRIVE MOTOR                    STEERING MOTOR
          Port A                           Port B
            │                               │
            └───────────────┬───────────────┘
                            ▼
                     VEHICLE RESPONSE
```

At no point does the camera directly command the actuators.

This keeps sensing, communication, decision-making, and actuation as distinct parts of the architecture.

---

## 7.28 Engineering Decision Summary

The HuskyLens subsystem demonstrates Piolín's broader hardware philosophy: add specialized hardware only when it solves a problem that the existing sensors cannot solve effectively.

The ultrasonic sensors are well suited for measuring wall distance but cannot determine whether a visible traffic pillar is red or green.

The downward color sensor can distinguish course markings beneath the robot but cannot identify obstacles ahead.

The HuskyLens fills that missing perception role.

```text
ULTRASONIC
   ↓
DISTANCE


COLOR SENSOR
   ↓
FLOOR MARKING


HUSKYLENS
   ↓
VISUAL OBJECT IDENTITY
```

The Arduino Nano allows this specialized visual information to reach the EV3 without replacing the main controller.

This produced a final architecture in which every major sensing device answers a different question.

---

## 7.29 Final Summary

Piolín uses one **HuskyLens vision sensor** as the primary obstacle-recognition device for the WRO Future Engineers Obstacle Challenge.

The camera is mounted facing forward and identifies the colored traffic pillars encountered by the robot.

Piolín's final obstacle IDs are:

```text
ID 1 = GREEN PILLAR

ID 2 = RED PILLAR
```

These detections are transferred through the Arduino Nano to the EV3.

The complete architecture is:

```text
HUSKYLENS
    ↓
Obstacle Identification
    ↓
ARDUINO NANO
    ↓
USB
    ↓
LEGO EV3
    ↓
Combine with Ultrasonic + Course Information
    ↓
Navigation Decision
    ↓
Drive + Steering
```

The final engineering role of the HuskyLens can therefore be summarized as:

> **The ultrasonic sensors tell Piolín where the surrounding walls are.**

> **The color sensor tells Piolín where it is within the course sequence.**

> **The HuskyLens tells Piolín which colored obstacle it can see.**

> **The EV3 decides what Piolín should do with all of that information.**

The HuskyLens therefore extends Piolín's perception without replacing the EV3, ultrasonic navigation, or color-sensing systems.

Detailed HuskyLens data handling is documented separately in:

```text
docs/power_sensors/04_huskylens.md
```

while visual detection and obstacle behavior are documented in:

```text
docs/software_obstacles_strategy/05_obstacledetec.md

docs/software_obstacles_strategy/06_obstaclestrateg.md

docs/software_obstacles_strategy/08_CameraHLVision.md
```
