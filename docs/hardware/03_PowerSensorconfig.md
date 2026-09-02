# 3. Power & Sensor Architecture

Piolín's final WRO Future Engineers 2026 electrical architecture was designed around a simple engineering principle:

> **Keep all systems required for basic autonomous navigation directly controlled by the EV3, while using a separate vision subsystem only when computer vision is required.**

The final robot therefore uses the **LEGO Mindstorms EV3 Intelligent Brick** as its main controller.

For normal track navigation, the EV3 directly controls:

- the drive motor,
- the steering motor,
- two lateral ultrasonic sensors,
- and one downward-facing color sensor.

For the Obstacle Challenge, Piolín adds a **HuskyLens vision sensor connected through an Arduino Nano**, with the Nano communicating with the EV3 through USB.

This architecture was selected after testing several previous hardware configurations. The final version prioritizes:

- reliability,
- simple wiring,
- direct EV3 motor control,
- clear sensor responsibilities,
- independent subsystem testing,
- and reduced electrical and software complexity.

> [!IMPORTANT]
> The final 2026 Piolín configuration does **not** use a gyroscope, PixyCam, Raspberry Pi, Arduino Mega, front ultrasonic sensor, external motor driver, or external steering servo as part of its active competition hardware.

---

# 3.1 Final Port Configuration

The following table represents the final electrical connection map of Piolín.

| Port / Interface | Connected Device | Primary Function |
| :--- | :--- | :--- |
| **Motor Port A** | Drive Motor | Provides propulsion |
| **Motor Port B** | Steering Motor | Controls Ackermann steering |
| **Sensor Port S1** | Unused | Available in final configuration |
| **Sensor Port S2** | Right Ultrasonic Sensor | Measures right-side wall distance |
| **Sensor Port S3** | Left Ultrasonic Sensor | Measures left-side wall distance |
| **Sensor Port S4** | LEGO Color Sensor | Detects blue/orange floor markings |
| **EV3 USB** | Arduino Nano | Communication with vision subsystem |
| **Arduino Nano** | HuskyLens | Receives visual obstacle detections |

The EV3 remains the **main vehicle controller** at all times.

The Arduino Nano is not responsible for propulsion or steering. Its role is limited to interfacing the HuskyLens vision subsystem with the EV3.

---

# 3.2 Complete System Architecture

```mermaid
flowchart TB

    POWER[EV3 Power System]

    EV3[LEGO EV3<br>Main Controller]

    DRIVE[Drive Motor<br>Port A]
    STEER[Steering Motor<br>Port B]

    USR[Right Ultrasonic<br>Port S2]
    USL[Left Ultrasonic<br>Port S3]

    COLOR[Color Sensor<br>Port S4]

    NANO[Arduino Nano]
    HUSKY[HuskyLens]

    POWER --> EV3

    EV3 --> DRIVE
    EV3 --> STEER

    USR --> EV3
    USL --> EV3
    COLOR --> EV3

    EV3 <-->|USB| NANO
    NANO <-->|Vision Data| HUSKY
````

The architecture can be separated into three functional sensing layers:

| Sensing Layer           | Hardware                        | Main Responsibility                                            |
| :---------------------- | :------------------------------ | :------------------------------------------------------------- |
| **Track Geometry**      | Left + Right Ultrasonic Sensors | Wall following, corner interpretation and collision prevention |
| **Track Progress**      | LEGO Color Sensor               | Direction selection and lap/corner counting                    |
| **Obstacle Perception** | HuskyLens + Arduino Nano        | Recognition of colored traffic pillars                         |

Each sensing system therefore has a clearly defined responsibility.

---

# 3.3 Power Architecture

## 3.3.1 Main EV3 Power Domain

The LEGO EV3 provides the main electrical power domain used for Piolín's basic navigation system.

It directly powers and controls:

* Drive Motor — Port A
* Steering Motor — Port B
* Right Ultrasonic Sensor — S2
* Left Ultrasonic Sensor — S3
* Color Sensor — S4

This removes the need for external H-bridge motor drivers or separate motor power converters for the basic drivetrain.

```text
EV3 POWER / CONTROL DOMAIN
│
├── Port A ── Drive Motor
├── Port B ── Steering Motor
│
├── S2 ────── Right Ultrasonic
├── S3 ────── Left Ultrasonic
└── S4 ────── Color Sensor
```

Using native EV3 motors and sensors reduces:

* wiring complexity,
* external electrical components,
* connector count,
* possible voltage-level incompatibilities,
* and potential failure points caused by loose connections.

---

## 3.3.2 Vision Subsystem

Computer vision is treated as a secondary subsystem.

```text
HuskyLens
    │
    ▼
Arduino Nano
    │
    │ USB
    ▼
LEGO EV3
```

The Arduino Nano acts as a **communication bridge**.

The EV3 still decides:

* vehicle speed,
* steering direction,
* wall corrections,
* obstacle-avoidance response,
* and overall autonomous behavior.

This separation is particularly useful because the Open Challenge does not depend on vision.

If the camera subsystem is not required, Piolín can still navigate using:

> **EV3 + two ultrasonic sensors + color sensor + motors**

---

# 3.4 Power Budget and Electrical Behavior

Piolín's electrical load changes depending on which actuators and sensors are active.

The largest dynamic loads are expected when:

* the drive motor accelerates,
* the steering motor makes a strong correction,
* propulsion and steering operate simultaneously,
* and the vision subsystem is active during the Obstacle Challenge.

Because final voltage measurements have not yet been performed with external measurement equipment, the following values are used as **preliminary engineering estimates**.

| Operating Condition                | Estimated Supply Voltage | Electrical Condition                     |
| :--------------------------------- | :----------------------: | :--------------------------------------- |
| **EV3 Idle / Sensors Active**      |        **~7.9 V**        | Baseline system load                     |
| **Straight Driving**               |        **~7.6 V**        | Drive motor active                       |
| **Drive + Steering**               |        **~7.3 V**        | Both motors operating                    |
| **Full System + Nano + HuskyLens** |        **~7.2 V**        | Highest expected normal competition load |

The estimated difference between the lightest and heaviest operating conditions is:

$$
\Delta V = V_{idle}-V_{load}
$$

$$
\Delta V = 7.9-7.2
$$

$$
\boxed{\Delta V\approx0.7V}
$$

The estimated relative voltage reduction is:

$$
\frac{0.7}{7.9}\times100
\approx8.9\%
$$

This represents a preliminary electrical design estimate rather than a direct multimeter measurement.

> [!NOTE]
> These voltage values are engineering estimates. They can later be replaced by measured experimental values without changing the architecture or reasoning described in this section.

---

## 3.4.1 Reducing Electrical Stress

The software and mechanical design also influence electrical reliability.

The final navigation strategy avoids unnecessary actuator load by minimizing:

* continuous maximum steering,
* repeated left-right steering oscillations,
* steering against a mechanical limit,
* unnecessary rapid corrections,
* and prolonged high-load maneuvers.

This is important because a navigation algorithm that continuously oscillates the steering does not only reduce trajectory stability; it also increases mechanical wear and electrical demand.

---

# 3.5 Ultrasonic Sensor Architecture

Piolín uses **two lateral LEGO ultrasonic sensors**.

There is no dedicated front ultrasonic sensor in the final configuration.

| Sensor               | EV3 Port | Orientation |
| :------------------- | :------: | :---------- |
| **Right Ultrasonic** |  **S2**  | Faces right |
| **Left Ultrasonic**  |  **S3**  | Faces left  |

The ultrasonic sensors are positioned approximately:

$$
1.7\text{ in}\approx43\text{ mm}
$$

above the floor.

---

## 3.5.1 Physical Orientation

Top view:

```text
                     FRONT
                       ↑

       LEFT US  ←  [ PIOLÍN ]  →  RIGHT US

                       ↓
                     REAR
```

The two sensors observe opposite track walls.

This allows the same physical sensor configuration to operate in both possible competition directions.

---

# 3.6 Dynamic Inner and Outer Wall Assignment

Piolín does not permanently define the left or right sensor as the most important sensor.

Instead, the role depends on the direction determined from the floor markings.

### Counterclockwise

```text
LEFT US  = Inner Wall
RIGHT US = Outer Wall
```

### Clockwise

```text
RIGHT US = Inner Wall
LEFT US  = Outer Wall
```

This produces the following mapping:

| Direction            | Inner Wall Sensor | Outer Wall Sensor |
| :------------------- | :---------------- | :---------------- |
| **Counterclockwise** | Left US           | Right US          |
| **Clockwise**        | Right US          | Left US           |

This allows one navigation algorithm to operate in either direction without physically changing the sensor layout.

---

# 3.7 Ultrasonic Geometry During Straight Sections

During a straight section, both ultrasonic sensors observe approximately parallel track walls.

The nominal corridor width used during Piolín's navigation development is approximately:

$$
W=1000\text{ mm}
$$

The current target distance from the inner ultrasonic sensor is approximately:

$$
D_{inner,target}=270\text{ mm}
$$

During a normal straight:

```text
OUTER WALL
────────────────────────────────────

        ← Douter

        [ PIOLÍN ]

        Dinner →

────────────────────────────────────
INNER WALL
```

The inner ultrasonic sensor provides the primary wall-following reference.

The outer ultrasonic sensor provides:

* additional geometric information,
* detection of extreme lateral displacement,
* and protection against approaching the outer wall too closely.

---

# 3.8 Why Ultrasonic Meaning Changes at a Corner

A major lesson from Piolín's testing was that an ultrasonic reading cannot always be interpreted only as lateral distance.

During a straight:

> A large inner distance may mean that Piolín moved away from the wall.

During a corner:

> A large inner distance may mean that the wall physically ended.

Consider the following geometry:

```text
INNER WALL
──────────────────────────┐
                          │
                          │
                  PIOLÍN  │
                     ↗    │
                          │
```

As Piolín reaches the corner, the inner ultrasonic sensor begins to point into open space.

The measured distance increases significantly.

If the controller treated this only as:

> "Piolín is too far from the inner wall"

the robot could incorrectly command an aggressive steering correction.

Instead, the final strategy interprets this change as a possible **corner transition**.

---

# 3.9 Final Corner Sensor Strategy

Piolín's final Open Challenge strategy combines lessons learned from previous ultrasonic and gyro-based experiments.

The sequence is:

```text
STRAIGHT
   ↓
Follow inner wall
   ↓
Monitor outer wall
   ↓
Inner wall disappears
   ↓
Confirm corner
   ↓
Begin steering into corner
   ↓
Outer wall becomes temporary reference
   ↓
Inner wall reappears
   ↓
Reduce corner steering
   ↓
Re-center
   ↓
Return to inner-wall following
```

This allows the meaning of each ultrasonic sensor to change according to the geometry currently observed.

---

## 3.9.1 Straight Section

Primary reference:

> **Inner Ultrasonic**

Secondary reference:

> **Outer Ultrasonic**

---

## 3.9.2 Corner Entry

The inner wall begins to disappear.

The controller does not immediately interpret the large reading as a normal wall-following error.

Instead, additional readings are used to determine whether the robot is actually reaching a corner.

---

## 3.9.3 Corner

Once the corner has been confirmed:

> **Outer Ultrasonic becomes the primary temporary wall reference.**

The inner ultrasonic may currently be pointing toward open space and therefore becomes less useful for normal distance control.

---

## 3.9.4 Corner Exit

As Piolín progresses around the corner, the inner wall eventually becomes visible again.

This indicates the transition toward the next straight section.

The robot then:

1. reduces the corner steering command,
2. restores the inner sensor as the main reference,
3. stabilizes its lateral position,
4. and returns to straight navigation.

The transition is gradual to avoid an abrupt steering reversal.

---

# 3.10 Ultrasonic Filtering

Ultrasonic measurements can contain occasional abnormal readings caused by:

* reflection angle,
* wall geometry,
* floor reflections,
* nearby objects,
* track openings,
* or isolated echo errors.

A navigation system should therefore avoid making a major steering decision from one isolated measurement.

One tested approach uses a short **median-of-three filter**.

For three consecutive readings:

$$
D_1,\ D_2,\ D_3
$$

the filtered measurement is:

$$
D_{filtered}=median(D_1,D_2,D_3)
$$

For example:

$$
268,\ 271,\ 940\text{ mm}
$$

results in:

$$
median(268,271,940)=271\text{ mm}
$$

The isolated 940 mm measurement therefore does not immediately cause an extreme response.

This method has an important advantage over a long moving-average filter:

> it rejects isolated spikes while maintaining relatively fast sensor response.

---

# 3.11 Ultrasonic Calibration Procedure

Each ultrasonic sensor should be characterized independently before navigation thresholds are finalized.

Piolín's ultrasonic calibration procedure consists of:

1. positioning the robot parallel to a flat wall,
2. placing the sensor at a known physical distance,
3. recording multiple ultrasonic readings,
4. comparing measured and physical distance,
5. repeating the test at several distances,
6. observing measurement variation and isolated spikes,
7. repeating the process for both sensors,
8. testing both sensors simultaneously between the track walls,
9. and observing how readings change when entering a corner.

The objective is not to force the two sensors to produce identical values.

Instead, calibration establishes:

* normal operating range,
* repeatability,
* useful wall-following distances,
* spike behavior,
* and corner-transition behavior.

---

# 3.12 Color Sensor Architecture

The LEGO Color Sensor is connected directly to:

> **EV3 Port S4**

and faces the competition floor.

The color sensor does not directly steer Piolín.

Instead, it has two specific responsibilities:

1. determining initial driving direction,
2. tracking course progress.

---

# 3.13 Initial Direction Detection

The first valid color detection determines Piolín's driving direction.

| First Valid Color | Direction        |
| :---------------- | :--------------- |
| **Blue**          | Counterclockwise |
| **Orange**        | Clockwise        |

Once the direction is known, the software also knows which ultrasonic sensor corresponds to the inner wall.

For example:

```text
BLUE
 ↓
COUNTERCLOCKWISE
 ↓
LEFT = INNER WALL
RIGHT = OUTER WALL
```

or:

```text
ORANGE
 ↓
CLOCKWISE
 ↓
RIGHT = INNER WALL
LEFT = OUTER WALL
```

This creates a direct relationship between the color and ultrasonic subsystems.

---

# 3.14 Lap and Corner Counting

The WRO track contains four corners per lap.

Piolín must complete three laps:

$$
4\text{ corners/lap}\times3\text{ laps}
=
12\text{ corners}
$$

Each corner contains two colored floor markings:

* one blue,
* one orange.

Therefore, over three complete laps Piolín expects:

$$
12\text{ blue detections}
$$

and:

$$
12\text{ orange detections}
$$

This means the complete track-progress target becomes:

```text
BLUE  = 12
ORANGE = 12
```

The first detection is still counted even though it also determines direction.

---

# 3.15 Preventing Duplicate Color Counts

A physical color strip remains underneath the sensor for more than one software cycle.

Without protection, one line could be counted many times.

Piolín therefore treats a colored line as an **event**, rather than as a continuous state.

```text
Neutral floor
     ↓
Valid color detected
     ↓
Register line ONCE
     ↓
Lock detector
     ↓
Robot leaves line
     ↓
Neutral floor confirmed
     ↓
Unlock detector
```

This detection lock prevents repeated counts while the sensor remains on the same strip.

Additional protection can be provided through a minimum traveled distance before another line is accepted.

---

# 3.16 Color Sensor Calibration

Color sensing is strongly influenced by illumination.

The apparent RGB and reflected-light values of the track can change because of:

* sunlight,
* indoor competition lighting,
* shadows,
* reflections,
* sensor height,
* and sensor angle.

For this reason, Piolín does not rely only on one theoretical LEGO color classification.

Calibration should compare actual sensor readings over:

* neutral floor,
* blue line,
* orange line.

The useful objective is to establish **ranges and relationships**, not one perfect RGB value.

For example, identification can consider:

* relative red, green and blue intensity,
* reflected-light level,
* and differences between color channels.

---

# 3.17 Ambient-Light Mitigation

Software thresholds alone cannot completely eliminate lighting variation.

Piolín therefore also applies a mechanical solution by positioning the color sensor close to the floor and reducing the amount of uncontrolled external light reaching the sensing area.

This reflects an important engineering principle:

> **Improve the physical input signal before attempting to solve every sensing problem in software.**

Mechanical shielding and software calibration therefore work together.

---

# 3.18 HuskyLens Vision Architecture

The HuskyLens is Piolín's final computer-vision sensor for the Obstacle Challenge.

Its role is different from the ultrasonic sensors.

The ultrasonic sensors answer:

> **How far are the walls from the robot?**

The HuskyLens answers:

> **Which colored obstacle is visible and where is it located in the camera's field of view?**

This distinction is important.

The HuskyLens does not replace the ultrasonic sensors.

Instead, the two sensing systems provide complementary information.

---

# 3.19 Vision Processing Flow

```text
Physical obstacle
      ↓
HuskyLens
      ↓
Color / object identification
      ↓
Arduino Nano
      ↓
USB communication
      ↓
LEGO EV3
      ↓
Navigation decision
```

The HuskyLens performs image recognition internally.

The EV3 therefore does not need to process a full raw video stream.

It receives only the information required for autonomous navigation.

---

# 3.20 Why Arduino Nano Is Used

The Arduino Nano has one specialized purpose:

> **interface the HuskyLens vision system with the EV3.**

It is not Piolín's main controller.

```text
           VEHICLE CONTROL
                EV3
                 ▲
                 │
                USB
                 │
            Arduino Nano
                 ▲
                 │
             HuskyLens
```

Keeping the EV3 as the primary controller preserves:

* native EV3 motor control,
* native ultrasonic integration,
* native color sensor integration,
* and the existing navigation software.

The vision subsystem can therefore be added without redesigning Piolín's complete control architecture.

---

# 3.21 Challenge-Specific Sensor Usage

The final hardware does not require every sensor to have the same importance in both competition challenges.

| Hardware             |          Open Challenge          | Obstacle Challenge |
| :------------------- | :------------------------------: | :----------------: |
| **EV3**              |                 ✅                |          ✅         |
| **Drive Motor**      |                 ✅                |          ✅         |
| **Steering Motor**   |                 ✅                |          ✅         |
| **Left Ultrasonic**  |                 ✅                |          ✅         |
| **Right Ultrasonic** |                 ✅                |          ✅         |
| **Color Sensor**     |                 ✅                |          ✅         |
| **Arduino Nano**     | Not required for Open navigation |          ✅         |
| **HuskyLens**        | Not required for Open navigation |          ✅         |
| **Gyroscope**        |                 ❌                |          ❌         |

The important advantage is that Open Challenge navigation remains independent from computer vision.

---

# 3.22 Sensor Responsibility Matrix

To avoid control conflicts, every sensor is assigned a specific responsibility.

| Driving Situation        |      Inner US      |           Outer US          |  Color Sensor  | HuskyLens |
| :----------------------- | :----------------: | :-------------------------: | :------------: | :-------: |
| **Straight Navigation**  |       Primary      |          Secondary          |     Monitor    |     —     |
| **Corner Detection**     |  Primary indicator |         Confirmation        |     Monitor    |     —     |
| **Corner Navigation**    |    Reacquisition   | Primary temporary reference |     Monitor    |     —     |
| **Corner Exit**          | Returns to primary |          Secondary          |     Monitor    |     —     |
| **Direction Detection**  |          —         |              —              |     Primary    |     —     |
| **Lap Tracking**         |          —         |              —              |     Primary    |     —     |
| **Obstacle Recognition** |     Wall safety    |         Wall safety         | Track progress |  Primary  |

This structure prevents unrelated sensors from continuously fighting for steering control.

---

# 3.23 Failure-Point Analysis

Reliability does not mean assuming that sensors never fail.

Instead, Piolín's design identifies likely failure modes and attempts to reduce their effect.

| Failure Mode                             | Possible Effect                  | Engineering Response                                 |
| :--------------------------------------- | :------------------------------- | :--------------------------------------------------- |
| **Single ultrasonic spike**              | False steering correction        | Short filtering and confirmation                     |
| **Inner US observes open corner**        | Distance appears extremely large | Interpret reading according to track geometry        |
| **Repeated color readings**              | One strip counted multiple times | Detection lock + neutral confirmation                |
| **Lighting variation**                   | Incorrect color classification   | Mechanical shielding + calibration                   |
| **Outer wall becomes too close**         | Collision risk                   | Outer US remains available for safety                |
| **HuskyLens temporarily loses a pillar** | Vision information disappears    | Wall-safety sensing remains independent              |
| **Vision subsystem disconnected**        | Obstacle recognition unavailable | Open Challenge navigation remains functional         |
| **Steering reaches mechanical limit**    | Increased motor load             | Software steering limits                             |
| **Excessive steering oscillation**       | Mechanical/electrical stress     | Reduced unnecessary corrections                      |
| **Battery voltage decreases**            | Reduced motor performance        | Controlled battery condition before competition runs |

The goal is not to claim that failure is impossible.

The goal is to understand:

> **what can fail, what effect it would have, and how the system reduces that effect.**

---

# 3.24 Evolution of the Sensor Architecture

Piolín's current architecture was not the first system tested.

Several earlier approaches contributed directly to the final design.

---

## 3.24.1 Two-Ultrasonic Mathematical Controller

One experimental navigation system continuously combined the two ultrasonic sensors to estimate Piolín's lateral position.

During straight sections this provided useful information because both sensors observed approximately parallel walls.

However, testing revealed an important limitation:

> **The same geometric relationship cannot be assumed when entering a corner.**

As the inner wall disappears, one ultrasonic sensor no longer measures a normal lateral wall distance.

This experiment led to the decision to make sensor interpretation dependent on track geometry.

---

## 3.24.2 Gyroscope-Assisted Navigation Experiment

Another experimental controller introduced a gyroscope.

In that architecture:

* ultrasonic sensors helped during straight sections,
* the gyro provided heading stabilization,
* and corners were executed as approximately 90° heading changes.

This provided an absolute angular reference, but also introduced another sensor dependency and changed the navigation architecture substantially.

The gyroscope was eventually removed from the final competition configuration.

Sensor Port S1 therefore remains unused.

---

## 3.24.3 Earlier Vision Architectures

Piolín also experimented with other vision and processing architectures before arriving at the final system.

Previous development included alternatives such as:

* Pixy-based vision,
* external processing architectures,
* and more complex controller configurations.

These experiments demonstrated that increasing processing capability does not automatically increase competition reliability.

The final architecture instead retains the EV3 for vehicle control and uses the HuskyLens/Nano combination only for the specialized vision task.

---

# 3.25 Final Sensor Strategy

The final sensor architecture combines lessons from the previous experiments:

```text
STRAIGHT
   │
   ├── Inner US = main trajectory reference
   └── Outer US = secondary reference
              ↓
      INNER WALL DISAPPEARS
              ↓
        CONFIRM CORNER
              ↓
     BEGIN CORNER STEERING
              ↓
 Outer US = temporary main reference
              ↓
      INNER WALL REAPPEARS
              ↓
       REDUCE STEERING
              ↓
          RE-CENTER
              ↓
           STRAIGHT
```

The final strategy therefore does not require a gyroscope to identify the shape of the track.

Instead, it uses the geometry already observed by the two lateral ultrasonic sensors.

---

# 3.26 Engineering Trade-Offs

Every hardware decision introduces both advantages and disadvantages.

Piolín's final architecture deliberately accepts several trade-offs.

| Design Decision                        | Advantage                                             | Trade-Off                                          |
| :------------------------------------- | :---------------------------------------------------- | :------------------------------------------------- |
| **Two lateral US instead of three US** | Lower wiring complexity and direct wall geometry      | No dedicated forward distance sensor               |
| **No gyroscope**                       | Fewer sensor dependencies and free S1                 | Turns must be inferred from wall geometry          |
| **EV3 as main controller**             | Native sensor/motor integration                       | Less processing power than modern SBCs             |
| **Nano + HuskyLens**                   | Adds vision without replacing EV3                     | Adds one additional communication subsystem        |
| **Color-based progress tracking**      | Uses physical track markings directly                 | Requires lighting calibration                      |
| **Short filtering**                    | Rejects isolated errors with low delay                | Cannot eliminate every incorrect reading           |
| **Outer-wall corner reference**        | Maintains useful geometry while inner wall disappears | Requires reliable transition logic                 |
| **Separate Open and Vision systems**   | Open navigation remains independent                   | More than one sensing subsystem must be maintained |

The final configuration prioritizes **predictability and understandability** over maximum hardware complexity.

---

# 3.27 Reproducibility

Another team should be able to reconstruct the electrical and sensor architecture from the following connection map.

```text
LEGO EV3
│
├── Motor Port A
│      └── Drive Motor
│
├── Motor Port B
│      └── Steering Motor
│
├── Sensor Port S1
│      └── Unused
│
├── Sensor Port S2
│      └── Right Ultrasonic
│
├── Sensor Port S3
│      └── Left Ultrasonic
│
├── Sensor Port S4
│      └── Color Sensor
│
└── USB
       │
       ▼
   Arduino Nano
       │
       ▼
    HuskyLens
```

---

## 3.27.1 Physical Sensor Placement

```text
TOP VIEW

                      FRONT
                        ↑

                 [ HuskyLens ]


LEFT ULTRASONIC  ←  ┌───────────────┐  → RIGHT ULTRASONIC
                    │               │
                    │    PIOLÍN     │
                    │               │
                    └───────────────┘


                    Color Sensor
                         ↓
                       FLOOR
```

The ultrasonic sensors are mounted laterally, approximately **43 mm above the competition surface**.

The color sensor is mounted facing downward toward the colored floor markings.

---

# 3.28 Final Engineering Summary

Piolín's final Power & Sensor Architecture is intentionally simpler than several previous prototypes.

The final system assigns each subsystem one clearly defined responsibility:

### LEGO EV3

Main navigation and vehicle control.

### Two Lateral Ultrasonic Sensors

Track-wall geometry, wall following, corner interpretation and collision prevention.

### LEGO Color Sensor

Direction selection and track-progress counting.

### Arduino Nano

Communication interface between the vision system and the EV3.

### HuskyLens

Colored-obstacle recognition during the Obstacle Challenge.

The most important engineering lesson learned during development was:

> **More sensors and more processing power do not automatically produce a more reliable autonomous vehicle.**

Reliability improved when each sensor was given a clearly defined responsibility and when its limitations were considered explicitly.

The final Piolín architecture is therefore based on three principles:

> **Measure only information that is useful.**

> **Interpret sensor readings according to the geometry of the track.**

> **Keep fundamental navigation independent from non-essential subsystems.**

This produces a sensor architecture that is easier to test, easier to reproduce, and easier to diagnose when unexpected behavior occurs.


