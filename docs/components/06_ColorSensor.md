# 6. LEGO Color Sensor

Piolín uses one **LEGO Color Sensor connected to EV3 Sensor Port S4**. The sensor is mounted facing downward toward the competition surface and provides Piolín with information about the colored floor markings encountered while travelling around the track.

<div align="center">
  <img
    width="208"
    height="213"
    alt="Piolín Color Sensor"
    src="https://github.com/user-attachments/assets/59a381ff-3383-4951-9bea-b83d9a1151fd"
  />
  <br>
  <sub><b>Figure 6.1.</b> LEGO Color Sensor installed on Piolín in its final downward-facing position.</sub>
</div>

The sensor is positioned close to the competition surface so that its observation area remains concentrated on the floor directly beneath Piolín. Its physical mounting is therefore part of the sensing system itself, since changes in height, orientation, or surrounding illumination can modify the optical information received by the sensor.

Unlike the ultrasonic sensors, which describe the physical geometry surrounding the robot, the color sensor does not continuously determine where Piolín should steer. Its primary purpose is to provide **course-state information**.

The sensor helps Piolín determine its initial driving direction and track its progress around the course. The steering decisions themselves remain primarily dependent on the ultrasonic navigation system and the current software state.

The final responsibility can be summarized as:

```text
COLOR SENSOR
     │
     ▼
Floor Markings
     │
     ├───────────────┐
     ▼               ▼
Initial Direction   Course Progress
     │               │
     └───────┬───────┘
             ▼
          LEGO EV3
```

> [!IMPORTANT]
> The color sensor does **not directly steer Piolín**.  
> It provides information that allows the EV3 to understand the course state, while the ultrasonic sensors remain responsible for wall geometry and normal navigation.

---

## 6.1 Final Color Sensor Configuration

The final Piolín configuration uses one downward-facing LEGO Color Sensor.

| Parameter | Final Configuration |
| :--- | :--- |
| **Sensor** | LEGO Color Sensor |
| **Quantity** | **1** |
| **EV3 Connection** | **Sensor Port S4** |
| **Orientation** | Downward-facing |
| **Primary Markings** | Blue and Orange |
| **Primary Role 1** | Determine initial driving direction |
| **Primary Role 2** | Track progress around the course |
| **Steering Authority** | None directly |
| **Main Controller** | LEGO Mindstorms EV3 |

The physical relationship is:

```text
                    PIOLÍN
              ┌───────────────┐
              │               │
              │     EV3       │
              │               │
              └───────┬───────┘
                      │
                      │ S4
                      ▼
               [ COLOR SENSOR ]
                      │
                      ▼
               Competition Mat
```

Because the sensor faces downward, its field of observation is intentionally restricted to a small area directly beneath the robot.

---

## 6.2 Why a Downward-Facing Sensor Is Used

The color sensor is mounted downward because Piolín needs to identify markings located on the floor rather than objects in front of the vehicle.

A forward-facing sensor would observe the surrounding environment and could be affected by walls, obstacles, or objects that are not relevant to the course-marking logic.

The downward orientation creates a simpler sensing relationship:

```text
        ROBOT
          │
          ▼
    COLOR SENSOR
          │
          ▼
    FLOOR MARKING
```

The sensor only needs to determine what type of surface is directly underneath it.

This makes the color sensor complementary to the other sensing systems:

```text
Ultrasonic Sensors
        ↓
Measure surrounding walls


HuskyLens
        ↓
Recognizes visible obstacles


Color Sensor
        ↓
Reads floor markings
```

Each sensor therefore observes a different region of the environment.

---

## 6.3 Role in Determining Driving Direction

One of the most important responsibilities of the color sensor is determining Piolín's initial direction around the course.

The first valid colored floor marking detected by the robot establishes the direction that the navigation system should use.

Piolín's current direction mapping is:

| First Valid Color | Piolín Direction |
| :--- | :--- |
| **Blue** | **Counterclockwise** |
| **Orange** | **Clockwise** |

The logic can be represented as:

```text
          START
            │
            ▼
     Read Color Sensor
            │
      ┌─────┴─────┐
      │           │
      ▼           ▼
    BLUE        ORANGE
      │           │
      ▼           ▼
Counterclockwise Clockwise
      │           │
      └─────┬─────┘
            ▼
   Assign Inner / Outer
     Ultrasonic Sensors
```

This is an important connection between the color sensor and the ultrasonic navigation system.

The color sensor does not tell Piolín how far it is from a wall. Instead, it tells the EV3 which physical side of the robot should be interpreted as the **inner wall** and which should be interpreted as the **outer wall**.

---

## 6.4 Relationship With the Ultrasonic Sensors

Piolín's left and right ultrasonic sensors are physically fixed on the chassis.

However, their software responsibilities depend on the driving direction.

Once the color sensor establishes direction, the EV3 can assign the lateral ultrasonic sensors correctly.

For counterclockwise navigation:

```text
BLUE detected first
        ↓
COUNTERCLOCKWISE
        ↓

LEFT US  S3 = INNER
RIGHT US S2 = OUTER
```

For clockwise navigation:

```text
ORANGE detected first
         ↓
CLOCKWISE
         ↓

RIGHT US S2 = INNER
LEFT US  S3 = OUTER
```

This demonstrates that the color sensor and ultrasonic sensors solve different parts of the same navigation problem.

The color sensor establishes **course orientation**, while the ultrasonic sensors provide **physical geometry**.

---

## 6.5 Course Progress Tracking

After the initial driving direction has been established, the color sensor remains useful throughout the run.

Piolín uses the colored floor markings as repeatable events that indicate progress around the course.

The basic relationship is:

```text
Robot moves
    ↓
Color strip reached
    ↓
Sensor detects valid color
    ↓
EV3 records event
    ↓
Robot continues
```

This allows the program to maintain a course-progress count without depending entirely on elapsed time or wheel rotation.

The color sensor therefore acts as a physical reference tied directly to the competition mat.

---

## 6.6 Piolín's Blue and Orange Counting Logic

Piolín's course-tracking logic distinguishes between valid blue and orange detections.

With four corner regions per lap and three laps, Piolín's implementation expects the repeated appearance of the floor markings throughout the run.

The course relationship used by Piolín is:

```text
4 corners per lap
        ×
3 laps
        =
12 corner events
```

Across the complete three-lap course, Piolín's progress logic can therefore track:

```text
12 valid BLUE detections

and

12 valid ORANGE detections
```

The two counters provide the software with a way to confirm that the robot is continuing to encounter the expected floor markings throughout the required laps.

This information can later be used by the navigation state machine to determine whether the vehicle is approaching the end of the required course.

---

## 6.7 Why the Color Sensor Is Not Used for Steering

A floor color detection provides very different information from an ultrasonic wall measurement.

A color sensor can determine that Piolín is currently above a colored strip, but that does not directly indicate how far the robot is from the inner wall, how far it is from the outer wall, or how strongly the wheels should turn.

For this reason, the final architecture avoids using the color sensor as the main steering reference.

Instead:

```text
COLOR SENSOR
     ↓
Course Event


ULTRASONIC SENSORS
     ↓
Navigation Geometry
```

The EV3 then combines those roles inside the state machine.

This separation prevents a brief floor detection from unnecessarily overriding the continuous geometric information provided by the lateral ultrasonic sensors.

---

## 6.8 Color Sensor Physical Mounting

As shown in **Figure 6.1**, the color sensor is mounted on the lower section of Piolín and faces directly toward the competition surface.

Its physical position is intentionally different from the ultrasonic sensors and HuskyLens. While those systems observe the environment around or ahead of the robot, the color sensor observes only the small floor region immediately beneath the chassis.

The mechanical relationship is:

```text
       PIOLÍN CHASSIS
             │
             ▼
      COLOR SENSOR
             │
             ▼
       Optical Gap
             │
             ▼
     COMPETITION MAT
```

Maintaining a stable sensor position helps keep the optical geometry consistent.

Changes in mounting height or sensor angle can change the amount of reflected light that reaches the detector, even when the physical floor color remains the same.

---

## 6.9 Light Isolation Casing

During Piolín's development, color detection was affected by environmental illumination.

The amount and direction of surrounding light can influence the light reflected from the competition surface and therefore alter the sensor values observed by the EV3.

To reduce this effect, Piolín uses a **physical casing around the color sensor**.

The casing creates a more controlled local environment around the sensing area.

```text
Ambient Light
   ↘   ↓   ↙

 ┌─────────────┐
 │   CASING    │
 │      │      │
 │ ColorSensor │
 └──────┬──────┘
        │
        ▼
       MAT
```

The purpose of the casing is not to make lighting irrelevant.

Instead, it reduces the amount of uncontrolled external light reaching the sensor from the sides.

This improves the consistency of the optical environment and makes the software classification more dependent on the actual floor marking beneath Piolín.

---

## 6.10 Why Physical Light Isolation Matters

Color sensing is an optical measurement.

The EV3 color sensor observes light reflected from the surface beneath it.

Therefore, the measurement depends not only on the physical color of the mat, but also on the light reaching and reflecting from that surface.

Conceptually:

```text
Ambient / Sensor Light
          ↓
      Floor Surface
          ↓
      Reflected Light
          ↓
      Color Sensor
```

If the surrounding illumination changes dramatically, the reflected signal can also change.

The casing helps reduce that environmental variable.

This represents an important design principle in Piolín:

> **Software filtering is not always the only solution to a sensing problem. Mechanical design can improve the quality of the sensor data before the software receives it.**

The color-sensor casing is therefore both a mechanical and sensing component.

---

## 6.11 3D-Printed Color Sensor Casing

Piolín's repository includes a dedicated 3D model for the color-sensor casing:

```text
models/
└── 3dprint/
    └── ColorSensorCasing.stl
```

This custom component reflects the integration between hardware design and sensor reliability.

Instead of changing the entire color-detection algorithm every time environmental light influenced the readings, the mechanical design was improved to provide the sensor with a more controlled observation region.

The component can be represented as:

```text
       Piolín Chassis
             │
             ▼
    ┌────────────────┐
    │  Sensor Casing │
    │                │
    │  Color Sensor  │
    └───────┬────────┘
            │
            ▼
       Floor Marking
```

The casing therefore supports the optical sensing system without changing the fundamental purpose of the LEGO Color Sensor itself.

---

## 6.12 Sensor Input and Output

The color sensor can be understood as a conversion stage between the physical competition environment and the digital information used by the EV3.

The **input** to the sensor is optical. Light reaches the competition surface, interacts with the material and color of the floor, and part of that light is reflected back toward the sensor.

The **output** is numerical information that the EV3 software can process.

The complete relationship is:

```text
PHYSICAL ENVIRONMENT
        ↓
Floor Color
        ↓
Reflected Light
        ↓
LEGO Color Sensor
        ↓
Numerical Sensor Data
        ↓
EV3 Software
        ↓
Color Classification
        ↓
Navigation Event
```

<div align="center">
  <img
    width="800"
    height="450"
    alt="Color Sensor Input and Output Explanation"
    src="https://github.com/user-attachments/assets/3d5a986e-d0e8-44ca-a664-70d23bd7b0fe"
  />
  <br>
  <sub><b>Figure 6.2.</b> Simplified representation of the color sensor input/output process used by Piolín.</sub>
</div>

The diagram above shows the basic relationship between the physical environment and the information used by the navigation program.

The **input** to the sensor is the light reflected from the competition surface. When Piolín passes over a blue, orange, or neutral section of the mat, the optical characteristics of that surface affect the signal observed by the sensor.

The **output** is numerical optical information that can be read by the EV3.

Piolín's software then interprets those values and classifies the observed surface into a useful navigation category.

```text
PHYSICAL INPUT
Floor color and reflected light
            │
            ▼
     LEGO COLOR SENSOR
            │
            ▼
NUMERICAL SENSOR OUTPUT
            │
            ▼
     EV3 CLASSIFICATION
            │
      ┌─────┼─────┐
      ▼     ▼     ▼
    BLUE  ORANGE  OTHER
      │     │
      └──┬──┘
         ▼
  Navigation Event
```

This distinction between **sensor input** and **software interpretation** is important.

The LEGO Color Sensor does not directly tell Piolín to turn, count a lap, or select a driving direction.

It provides optical measurements.

The EV3 software is responsible for converting those measurements into meaningful course information.

---

## 6.13 RGB-Based Color Information

The LEGO Color Sensor can provide reflected-color information that the EV3 software can interpret.

In Piolín, the sensor data is used to distinguish the relevant floor markings rather than relying only on a generic predefined color category.

Conceptually:

```text
Sensor observes floor
        ↓
RGB-related measurement
        ↓
EV3 receives values
        ↓
Classification logic
        ↓
BLUE / ORANGE / OTHER
```

This allows Piolín's software to define detection behavior according to the actual floor colors present in the competition environment.

The detailed RGB classification logic and software decisions are documented separately in:

```text
docs/software_obstacles_strategy/09_RGBdetection.md
```

This component section focuses on the physical sensor and its role inside the hardware architecture.

---

## 6.14 Software Integration

The color sensor is connected directly to S4 and can be initialized from the EV3 software environment.

A simplified Pybricks representation is:

```python
from pybricks.ev3devices import ColorSensor
from pybricks.parameters import Port

color_sensor = ColorSensor(Port.S4)
```

The program can then request optical information from the sensor and pass it to the color-classification logic.

Conceptually:

```text
Color Sensor S4
      ↓
Raw optical information
      ↓
Classification
      ↓
Valid color event?
      ↓
Course-state update
```

This direct connection means that Piolín does not require the Arduino Nano or HuskyLens subsystem to identify the blue and orange floor markings.

---

## 6.15 Independence From the Vision System

The color sensor and HuskyLens are both optical devices, but their roles are completely different.

The color sensor looks downward at a very small area of the competition mat.

The HuskyLens looks outward into the environment and identifies visible obstacles.

```text
                HUSKYLENS
                    │
                    ▼
             Forward Environment
                    │
                    ▼
             Obstacle Recognition


             COLOR SENSOR
                    │
                    ▼
                 Floor
                    │
                    ▼
          Course Marking Detection
```

The two sensors should therefore not be considered redundant.

The HuskyLens answers:

> **What obstacle is visible ahead?**

The color sensor answers:

> **What course marking is directly underneath Piolín?**

---

## 6.16 Detection Locking

A physical color strip occupies an area rather than a single mathematical point.

As Piolín drives across a strip, the color sensor may observe the same marking across several consecutive software loops.

Without additional logic, one strip could therefore be counted multiple times.

```text
Robot movement →

████████████ BLUE STRIP ████████████

Reading 1 → BLUE
Reading 2 → BLUE
Reading 3 → BLUE
Reading 4 → BLUE
```

All four readings may correspond to the **same physical strip**.

Piolín therefore uses a detection-locking concept.

```text
First valid detection
        ↓
Record event
        ↓
LOCK detection
        ↓
Ignore repeated readings
        ↓
Sensor leaves strip
        ↓
UNLOCK
```

This allows a continuous stream of sensor readings to be converted into discrete course events.

---

## 6.17 Why Detection Locking Is Necessary

The purpose of the color counter is to count physical course markings, not software execution cycles.

These are fundamentally different quantities.

Without locking:

```text
One strip
   ↓
Several software loops
   ↓
Several counts
```

With locking:

```text
One strip
   ↓
Several software loops
   ↓
One valid event
```

This distinction is especially important because the EV3 program can execute many sensor-reading cycles while the robot is physically passing over a single colored area.

The locking mechanism therefore belongs to the interpretation layer between physical sensing and course-state counting.

---

## 6.18 Leaving the Color Marking

After a valid strip has been recorded, the sensor must eventually observe a region that is no longer classified as that same marking.

This allows the software to recognize that Piolín has physically moved away from the previous strip.

The conceptual sequence is:

```text
Neutral floor
     ↓
Colored marking begins
     ↓
Valid color detected
     ↓
Event recorded
     ↓
Color remains visible
     ↓
No additional count
     ↓
Neutral / different floor returns
     ↓
Detection released
```

This prevents the physical width of a marking from artificially increasing the lap or corner count.

---

## 6.19 Color Sensor and Navigation States

A color event can also be useful as part of the state machine because it represents a known physical feature of the competition mat.

The sensor itself does not manage the state machine.

Instead:

```text
COLOR SENSOR
      ↓
Detection
      ↓
EV3 classification
      ↓
Course event
      ↓
State machine receives information
```

The state machine can then decide whether the event is relevant to direction initialization, progress counting, corner sequencing, or the end of the required run.

This keeps the hardware layer simple.

The sensor provides optical data. The EV3 determines how that data affects navigation.

---

## 6.20 Relationship With Corner Navigation

The color sensor and ultrasonic sensors can both provide information near corner regions, but they describe different physical properties.

The ultrasonic system observes:

```text
Wall disappears
Wall geometry changes
Outer wall becomes reference
Inner wall reappears
```

The color sensor observes:

```text
Colored floor marking encountered
```

The final navigation architecture therefore does not require the floor color alone to prove that a corner is physically safe to execute.

Instead, color provides **course progress**, while ultrasonic geometry provides **vehicle positioning and wall interpretation**.

This reduces the risk of using one sensor type for a problem that another sensor measures more directly.

---

## 6.21 Relationship With Parking

Course-progress information from the color sensor can help the EV3 understand when Piolín is approaching the end of the required three-lap sequence.

Parking is not controlled by color detection alone.

Instead, the lap and marking counts form part of the information available to the software before the parking state is entered.

Conceptually:

```text
Color events
     ↓
Course count
     ↓
Required sequence completed
     ↓
Parking state becomes relevant
```

The actual parking geometry and movement are handled by the dedicated parking subsystem.

Detailed parking documentation is located in:

```text
docs/software_obstacles_strategy/parking/
```

---

## 6.22 Why the Color Sensor Is Connected Directly to the EV3

The color sensor performs a fundamental course-navigation role in both normal track interpretation and lap counting.

For this reason, it is connected directly to the EV3 rather than passing through the Arduino Nano.

The architecture is:

```text
COLOR SENSOR
     │
     │ S4
     ▼
   LEGO EV3
```

rather than:

```text
Color Sensor
     ↓
Arduino
     ↓
EV3
```

This reduces unnecessary communication layers.

The Nano is reserved primarily for the HuskyLens vision interface, while the EV3 directly controls the LEGO sensors that are fundamental to normal navigation.

---

## 6.23 Sensor Priority

The color sensor provides important information, but it does not have the highest safety authority.

Piolín's control architecture distinguishes between course information and immediate physical safety.

A simplified priority relationship is:

```text
        Frontal Safety
              ↓
        Lateral Safety
              ↓
       Navigation State
              ↓
      Course Progress Data
```

A valid floor marking should not force Piolín to continue moving if the front ultrasonic sensor simultaneously detects a dangerous frontal condition.

Similarly, course-counting information does not replace wall geometry during a corner.

This hierarchy prevents the color sensor from being assigned responsibilities beyond what it physically measures.

---

## 6.24 Optical Failure Considerations

Like every optical sensor, the color sensor can be influenced by environmental and mechanical conditions.

| Condition | Possible Effect | Piolín Design Response |
| :--- | :--- | :--- |
| **Ambient light variation** | Changes reflected-light values | Physical light-isolation casing |
| **Sensor position variation** | Changes observed reflection | Fixed chassis mounting |
| **Sensor angle variation** | Changes observed floor area | Downward mechanical orientation |
| **Repeated readings over same strip** | Multiple detections | Detection locking |
| **Temporary ambiguous value** | Incorrect classification possibility | Software validation |
| **Dirty sensor window** | Reduced optical clarity | Accessible sensor placement |
| **Different floor appearance** | Different reflected signal | Classification based on competition colors |

The design therefore combines mechanical control of the sensing environment with software interpretation.

---

## 6.25 Why Mechanical and Software Solutions Are Combined

The final color-sensing architecture illustrates an important engineering principle.

A software-only solution would attempt to compensate for every possible lighting change using increasingly complicated thresholds or filters.

A hardware-only solution would attempt to physically isolate the sensor perfectly, which is also unrealistic.

Piolín combines both approaches:

```text
MECHANICAL
Light-isolation casing
        +
Stable downward mounting

        ↓

SOFTWARE
Color classification
        +
Detection validation
        +
Event locking
```

This distributes the problem across hardware and software instead of forcing one subsystem to solve everything.

---

## 6.26 Color Sensor Responsibility Matrix

The final responsibility of the S4 color sensor can be summarized as:

| Function | Color Sensor Role |
| :--- | :---: |
| **Detect blue floor markings** | **Primary** |
| **Detect orange floor markings** | **Primary** |
| **Determine initial direction** | **Primary input** |
| **Track course progress** | **Primary input** |
| **Count physical marking events** | **Used** |
| **Determine inner/outer wall assignment** | Indirect through direction |
| **Continuous steering control** | **No** |
| **Wall-distance measurement** | **No** |
| **Pillar recognition** | **No** |
| **Frontal collision safety** | **No** |

This clear division prevents overlap with Piolín's ultrasonic and vision systems.

---

## 6.27 Integration With the Complete Robot

The color sensor is one part of a larger perception architecture.

```text
                         ENVIRONMENT
                             │
           ┌─────────────────┼─────────────────┐
           │                 │                 │
           ▼                 ▼                 ▼
     TRACK WALLS         FLOOR MARKS        OBSTACLES
           │                 │                 │
           ▼                 ▼                 ▼
      ULTRASONICS       COLOR SENSOR       HUSKYLENS
      S1 / S2 / S3           S4                 │
           │                 │            Arduino Nano
           │                 │                 │
           └─────────────────┴────────┬────────┘
                                     ▼
                                  LEGO EV3
                                     │
                              Navigation Logic
                                     │
                          ┌──────────┴──────────┐
                          ▼                     ▼
                       MOTOR A               MOTOR B
                        Drive                Steering
```

The color sensor therefore contributes one specific type of environmental information to the same EV3 that controls the rest of Piolín's autonomous behavior.

---

## 6.28 Why One Color Sensor Is Sufficient

Piolín's final architecture uses only one floor-facing color sensor.

The purpose of the sensor is not to reconstruct a complete image of the floor or perform full-width visual line tracking.

It only needs to identify when a relevant marking passes underneath the designated sensing location.

The required sensing region is therefore localized:

```text
Robot moves forward
        ↓
One known sensor position
        ↓
Colored marking passes below
        ↓
Event detected
```

Adding multiple color sensors would increase hardware complexity without necessarily improving this specific course-state function.

The final design therefore uses one sensor with a clearly controlled mounting position and optical environment.

---

## 6.29 Final Color Sensor Architecture

Piolín's final color-sensing architecture can be summarized as:

```text
                   COMPETITION MAT
                         │
                         ▼
                  BLUE / ORANGE
                      MARKINGS
                         │
                         ▼
                  COLOR SENSOR
                       S4
                         │
                         ▼
                     LEGO EV3
                         │
               ┌─────────┴─────────┐
               ▼                   ▼
       Initial Direction      Course Progress
               │                   │
               └─────────┬─────────┘
                         ▼
                Navigation State
```

The sensor's function is intentionally narrow and clearly defined.

It does not attempt to replace ultrasonic wall navigation, HuskyLens obstacle recognition, or front collision protection.

Instead, it provides Piolín with a physical reference tied directly to the floor of the competition course.

---

## 6.30 Engineering Decision Summary

The final color-sensor design combines several important decisions.

First, the sensor is mounted **downward**, because its responsibility is floor detection rather than forward vision.

Second, the sensor is used for **direction and course progress rather than continuous steering**, which separates floor-state information from wall geometry.

Third, Piolín uses a **physical light-isolation casing** to reduce the influence of uncontrolled ambient illumination before the optical information reaches the software.

Finally, the software converts continuous sensor measurements into discrete course events through classification and detection-locking logic.

The complete concept can be represented as:

```text
STABLE PHYSICAL MOUNT
        +
LIGHT ISOLATION
        +
RGB CLASSIFICATION
        +
DETECTION LOCKING
        ↓
COURSE INFORMATION
```

This demonstrates that Piolín's color-sensing system is not simply a sensor attached to S4.

It is a complete subsystem involving mechanical placement, optical behavior, software classification, and navigation-state interpretation.

---

## 6.31 Final Summary

Piolín uses one **LEGO Color Sensor connected directly to EV3 Sensor Port S4**.

Its two primary responsibilities are:

```text
1. Determine the initial course direction

2. Track progress through the colored floor markings
```

The first valid blue or orange detection establishes the direction used by the navigation system:

```text
BLUE
  ↓
COUNTERCLOCKWISE


ORANGE
  ↓
CLOCKWISE
```

This direction then determines which lateral ultrasonic sensor is interpreted as the inner-wall reference and which becomes the outer-wall reference.

After initialization, the color sensor continues to provide discrete floor-marking events used for course tracking.

Detection locking prevents one physical strip from being interpreted as several independent events while Piolín passes across it.

The color sensor is mechanically supported by a dedicated light-isolation casing that reduces the influence of uncontrolled ambient illumination.

Its complete input/output relationship is:

```text
FLOOR COLOR
    ↓
REFLECTED LIGHT
    ↓
COLOR SENSOR
    ↓
NUMERICAL DATA
    ↓
EV3 CLASSIFICATION
    ↓
BLUE / ORANGE / OTHER
    ↓
COURSE EVENT
```

The final engineering role of the sensor can therefore be summarized as:

> **The ultrasonic sensors tell Piolín where it is relative to the walls.**

> **The HuskyLens tells Piolín what obstacle it sees.**

> **The color sensor tells Piolín where it is within the course sequence.**

Detailed sensor-processing behavior is documented separately in:

```text
docs/power_sensors/03_color_sensor.md
```

while RGB classification and event-detection logic are documented in:

```text
docs/software_obstacles_strategy/09_RGBdetection.md
```
