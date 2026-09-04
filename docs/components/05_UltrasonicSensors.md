# 5. Ultrasonic Sensors

<div align="center">
  <img src="https://github.com/user-attachments/assets/b8872f62-adb5-4fd1-98fb-18491c57de56"
       alt="LEGO Ultrasonic Sensor used in Piolín"
       style="max-width: 30%; height: auto; border-radius: 8px; margin: 12px 0;" />
</div>

Piolín uses **three LEGO ultrasonic sensors** as its primary distance-sensing hardware. Although all three sensors measure distance using the same physical principle, they do not perform the same job inside the robot.

Two sensors are mounted on opposite sides of the chassis and provide the geometric information used to understand Piolín's position relative to the track walls. The third sensor faces forward and provides an independent safety measurement of the space directly ahead of the vehicle.

This separation is an important part of the final architecture. The lateral sensors are responsible for **navigation**, while the front sensor is responsible primarily for **frontal collision protection**.

The final ultrasonic configuration is:

| Sensor | EV3 Port | Orientation | Primary Responsibility |
| :--- | :---: | :--- | :--- |
| **Front Ultrasonic** | **S1** | Forward-facing | Emergency frontal safety |
| **Right Ultrasonic** | **S2** | Right lateral | Right-wall distance and navigation geometry |
| **Left Ultrasonic** | **S3** | Left lateral | Left-wall distance and navigation geometry |

> [!IMPORTANT]
> Piolín uses the **two lateral ultrasonic sensors to navigate the track**.  
> The front ultrasonic sensor is deliberately kept separate from the normal inner-wall and outer-wall navigation model.

---
<div align="center">
  <img
    alt="PiolinUSlabeling"
    src="https://github.com/user-attachments/assets/94a39e6c-5f78-49d3-835a-b5b09bd76189"
    style="max-width: 20%; height: auto;"
  />
</div>

## 5.1 Ultrasonic Sensing Principle

An ultrasonic sensor estimates distance using sound at a frequency above the normal range of human hearing.

The sensor emits an ultrasonic pulse toward the surrounding environment. When that pulse reaches a physical surface such as a track wall, part of the acoustic energy is reflected toward the sensor.

The basic process is:

```text
Sensor emits ultrasonic pulse
              │
              ▼
         Pulse travels
              │
              ▼
         Hits surface
              │
              ▼
         Echo returns
              │
              ▼
       Sensor measures
        travel time
              │
              ▼
       Distance estimate
```

Because the pulse must travel from the sensor to the wall and then return, the measured travel time represents a round trip.

Conceptually:

```text
DISTANCE =
(SPEED OF SOUND × ECHO TIME) / 2
```

Piolín does not need to calculate this equation manually during normal operation because the LEGO ultrasonic sensor provides a distance measurement directly to the EV3.

The EV3 software can therefore work with physical distance information instead of processing raw acoustic timing signals.

---

## 5.2 Why Ultrasonic Sensors Were Selected

The WRO Future Engineers track contains walls that provide strong geometric references around the robot. Ultrasonic sensing allows Piolín to use those physical boundaries directly as part of its autonomous navigation system.

Unlike a floor-following system that depends entirely on painted lines, the lateral ultrasonic sensors continuously describe the robot's relationship with the walls.

This produces a simple physical relationship:

```text
LEFT WALL
    │
    │  Distance measured by Left US
    ▼

       [ PIOLÍN ]

    ▲
    │  Distance measured by Right US
    │
RIGHT WALL
```

The sensors are particularly useful because the information they provide has a clear physical meaning. If one lateral distance decreases, Piolín is either moving toward that wall or changing its orientation relative to it. If the distance increases dramatically near a corner, the sensor may no longer be observing the same wall surface.

This makes ultrasonic sensing useful not only for basic wall following, but also for interpreting changes in track geometry.

---

# 5.3 Final Physical Arrangement

The final Piolín architecture uses one ultrasonic sensor facing forward and two facing laterally.

From above, the arrangement is:

```text
                        FRONT
                          ↑

                    [ FRONT US ]
                         S1
                          │
                          │

          LEFT US ←  [ PIOLÍN ]  → RIGHT US
             S3                         S2

                          │
                          ↓
                         REAR
```

The lateral sensors point directly toward opposite sides of the robot instead of being intentionally angled forward.

This orientation gives their measurements a more direct relationship with the lateral position of Piolín between the track boundaries.

The front sensor observes a different region entirely: the space directly ahead of the vehicle.

---

## 5.4 Lateral Sensor Mounting

The left and right ultrasonic sensors are mounted approximately laterally relative to Piolín's longitudinal axis.

Their measured mounting height is approximately:

```text
1.7 in
```

or:

```text
≈ 43 mm above the competition surface
```

This documented height applies to the **lateral sensor pair**.

The lateral mounting arrangement was selected because Piolín's navigation model is based on comparing the robot with the two track boundaries.

A direct lateral orientation can be represented as:

```text
               FRONT
                 ↑

                 │
                 │
LEFT WALL  ← [ PIOLÍN ] → RIGHT WALL
             ↑       ↑
            S3       S2
```

The measured distances can therefore be interpreted as left-wall and right-wall geometry without intentionally introducing a forward-angle component.

---

# 5.5 Front Ultrasonic Sensor

The third ultrasonic sensor is connected to **EV3 Sensor Port S1** and faces forward.

Its role differs significantly from the lateral pair.

The front sensor does not normally determine whether Piolín should follow the inner or outer wall. It does not participate in the lateral-position equations used for straight navigation, and it is not assigned dynamically according to clockwise or counterclockwise travel.

Instead, it answers a simpler safety question:

> **Is something dangerously close directly in front of Piolín?**

The physical sensing relationship is:

```text
              FRONT WALL / OBJECT
                     █████
                       ↑
                       │
                  Front distance
                       │
                       │
                  [ FRONT US ]
                       │
                   [ PIOLÍN ]
```

If the frontal distance becomes critically small, the EV3 can interrupt propulsion rather than allowing normal navigation to continue toward a direct collision.

This makes the front sensor an **independent safety layer** rather than another wall-following sensor.

---

## 5.6 Why the Front Sensor Is Separate From Wall Navigation

A sensor facing forward observes very different geometry from a sensor facing sideways.

During a normal corner, a forward-facing sensor may naturally see part of a wall ahead even though the robot is following the correct path.

If this measurement were continuously used to calculate steering, it could interfere with the lateral wall-navigation controller.

The final architecture therefore separates the two functions:

```text
LEFT + RIGHT ULTRASONIC
           │
           ▼
    Track Geometry
           │
           ▼
      Navigation


FRONT ULTRASONIC
           │
           ▼
    Frontal Distance
           │
           ▼
        Safety
```

This separation prevents the same measurement from being interpreted simultaneously as normal track geometry and as an emergency condition.

---

# 5.7 Right Ultrasonic Sensor — S2

The right ultrasonic sensor is connected directly to **EV3 Sensor Port S2**.

Its physical responsibility is to measure the distance between the right side of Piolín and the nearby track boundary.

Its software responsibility depends on the current direction of travel.

When Piolín is travelling clockwise, the right wall becomes the inner track boundary. In that situation, the right ultrasonic sensor becomes the main inner-wall reference during straight navigation.

When Piolín is travelling counterclockwise, the same physical sensor observes the outer wall instead.

Therefore, the sensor itself never changes position, but its **navigation meaning changes dynamically**.

```text
RIGHT US = S2

Clockwise
    ↓
INNER SENSOR


Counterclockwise
    ↓
OUTER SENSOR
```

This dynamic assignment allows one physical hardware configuration to support both competition directions.

---

# 5.8 Left Ultrasonic Sensor — S3

The left ultrasonic sensor is connected directly to **EV3 Sensor Port S3**.

It performs the same type of physical measurement as the right sensor but on the opposite side of the robot.

When Piolín travels counterclockwise, the left wall is the inner boundary, so S3 becomes the primary inner-wall sensor.

When Piolín travels clockwise, S3 becomes the outer-wall sensor.

```text
LEFT US = S3

Counterclockwise
      ↓
INNER SENSOR


Clockwise
      ↓
OUTER SENSOR
```

The left and right sensors therefore form a symmetrical sensing pair even though the software may assign them different responsibilities depending on the current direction.

---

# 5.9 Dynamic Inner and Outer Assignment

The initial course direction determines which lateral sensor represents the inner and outer walls.

| Direction | Inner Sensor | Outer Sensor |
| :--- | :---: | :---: |
| **Counterclockwise** | **Left US — S3** | **Right US — S2** |
| **Clockwise** | **Right US — S2** | **Left US — S3** |

This allows the navigation software to use generic concepts such as:

```text
INNER_DISTANCE
```

and:

```text
OUTER_DISTANCE
```

instead of creating completely separate navigation algorithms for clockwise and counterclockwise movement.

The physical sensor assignment changes, but the logic can remain conceptually the same.

```text
Determine direction
        │
        ▼
Assign S2 / S3
        │
        ├── INNER
        │
        └── OUTER
        │
        ▼
Use common navigation logic
```

This is one of the reasons the two lateral sensors are treated as a coordinated sensing system rather than as unrelated distance sensors.

---

# 5.10 Sensor Roles During a Straight Section

During normal straight navigation, the inner ultrasonic sensor acts as Piolín's primary wall reference.

The robot attempts to maintain a useful relationship with the inner wall while the outer sensor provides additional information about the surrounding corridor.

Conceptually:

```text
OUTER WALL
──────────────────────────────────

       ↑
    DOUTER

       [ PIOLÍN ]

    DINNER
       ↓

──────────────────────────────────
INNER WALL
```

The two values describe more than just whether a wall exists.

Together they provide information about how Piolín is positioned between the track boundaries.

This allows the robot to use wall geometry rather than relying on one isolated distance measurement.

---

# 5.11 Inner-Wall Disappearance at a Corner

One of the most important characteristics of Piolín's ultrasonic navigation is that a large distance does not always represent a navigation error.

During a straight section, the inner sensor observes a nearby wall.

```text
────────────────────────
INNER WALL

        ↑
     DINNER
        │
    [ PIOLÍN ]
```

At a corner, that physical wall ends.

```text
INNER WALL
──────────────────┐
                  │
                  │

           [PIOLÍN]
              ↗
```

The inner sensor may suddenly measure a much larger distance because it is now observing open space rather than the previous wall.

The hardware has not failed.

Instead:

```text
Large distance
      ↓
Wall may have ended
      ↓
Track geometry changed
```

This behavior became one of the main reasons Piolín's final navigation architecture treats ultrasonic measurements according to the robot's current navigation state.

---

# 5.12 Outer Sensor During Corner Navigation

As the inner wall disappears, the outer wall can remain visible for a larger part of the turn.

This gives the outer ultrasonic sensor a more useful physical reference during the corner.

```text
              OUTER WALL
             ╭────────────
            /
           /
          /  ← Outer US
         /
    [ PIOLÍN ]
         ↗
```

The sensor itself is unchanged. What changes is the software importance assigned to its measurement.

The navigation system therefore follows the general relationship:

```text
STRAIGHT
   ↓
Inner sensor primary


CORNER ENTRY
   ↓
Inner wall disappears


CORNER
   ↓
Outer sensor becomes more important


CORNER EXIT
   ↓
Inner wall reappears


NEXT STRAIGHT
   ↓
Inner sensor primary again
```

This is an example of the same hardware serving different roles depending on the geometry of the environment.

---

# 5.13 Reacquisition of the Inner Wall

As Piolín leaves a corner, the next section of the inner wall becomes visible to the lateral sensor.

The return of that measurement indicates that the robot is moving back toward a geometry similar to a straight section.

```text
Corner
   ↓
Inner wall absent
   ↓
Robot continues turning
   ↓
New inner wall appears
   ↓
Inner sensor becomes useful again
```

The sensor does not need to know that a corner has ended.

It simply measures distance.

The EV3 is responsible for interpreting the reappearance of a valid inner-wall measurement as part of the navigation state.

This distinction is important throughout Piolín's architecture:

> **Sensors measure the environment. The EV3 decides what those measurements mean.**

---

# 5.14 Two-Sensor Geometric Relationship

When both lateral sensors observe approximately parallel track walls, their measurements can be considered together.

The relationship is conceptually:

```text
LEFT WALL
│
│  LEFT DISTANCE
│        ↓
│     [ PIOLÍN ]
│        ↑
│  RIGHT DISTANCE
│
RIGHT WALL
```

Piolín's more detailed sensor documentation uses the two distances to estimate lateral position and evaluate whether the observed environment resembles normal straight-track geometry.

This is useful because a single distance tells the robot only about one side.

Two opposing distances provide a broader description of the robot's position inside the corridor.

The detailed mathematical model is documented separately in:

```text
docs/power_sensors/02_USSensorD.md
```

This component section focuses only on the hardware roles and physical interpretation of the sensors.

---

# 5.15 Why Direct Lateral Mounting Was Selected

Earlier Piolín concepts explored sensor orientations that were more diagonal or forward-facing.

A diagonal sensor can observe geometry before the robot reaches it, which initially appears useful for detecting upcoming track features.

However, the measured value becomes harder to interpret as a true lateral distance.

```text
DIRECT LATERAL

Wall │ ←──── Sensor
     │

Measured path ≈ lateral relationship
```

Compared with:

```text
DIAGONAL

Wall │
     │       /
     │      /
     │     / Sensor
```

With a diagonal arrangement, the reading depends more strongly on:

```text
Robot heading
Sensor angle
Wall orientation
Corner shape
```

Because Piolín's final navigation concept relies heavily on understanding the robot's relationship with the side walls, direct lateral orientation provides a clearer physical meaning for the measurements.

For this reason, the lateral sensors are mounted facing their respective sides rather than intentionally pointing toward the front of the vehicle.

---

# 5.16 Sensor Measurement and Robot Heading

Even with direct lateral mounting, ultrasonic measurements are influenced by the orientation of the complete robot.

If Piolín is approximately parallel to a wall:

```text
WALL
────────────────────────────

        [ PIOLÍN ]

────────────────────────────
WALL
```

the side measurements closely represent lateral separation.

If Piolín becomes rotated:

```text
WALL
────────────────────────────

          [ PIOLÍN ]
              /

────────────────────────────
WALL
```

the sensor is no longer perfectly perpendicular to the wall.

The measured acoustic path can therefore change even if the center of the robot has not moved laterally by the same amount.

This is one reason the ultrasonic system is interpreted as part of a **geometry-aware controller** rather than assuming that every change in measured distance represents pure sideways movement.

---

# 5.17 Measurement Noise and Reflections

Ultrasonic distance sensing depends on acoustic reflections from physical surfaces.

Real environments are not mathematically perfect reflectors.

A measurement can be influenced by:

```text
Wall angle
Rounded corners
Open spaces
Nearby structures
Robot orientation
Surface geometry
```

For example, when a sensor points toward the end of a wall, part of the ultrasonic pulse may no longer return from the same surface.

Similarly, during a corner, the wall angle relative to the sensor changes continuously.

The final Piolín architecture therefore does not assume that every individual ultrasonic reading is perfectly stable.

Instead, the software interprets the measurements in context and uses filtering and confirmation logic where appropriate.

Detailed signal-processing behavior is documented separately in the sensor-data section.

---

# 5.18 Lateral Sensor Filtering

The lateral ultrasonic sensors are used for continuous navigation, so their measurements need to remain stable enough to avoid unnecessary steering changes.

Piolín's software uses short filtering logic to reduce the effect of isolated abnormal readings while preserving enough responsiveness for corner detection.

The hardware relationship remains:

```text
LEFT US ───┐
           │
           ├──→ EV3 → Filtered navigation data
           │
RIGHT US ──┘
```

The sensors themselves provide the raw distance information. Filtering is performed by the navigation software running on the EV3.

This separation is important because the physical sensor and the mathematical interpretation of its reading are different parts of the system.

---

# 5.19 Front Sensor Validation

The front ultrasonic sensor solves a different problem from the lateral pair.

Its main responsibility is safety, so its reading is not processed in exactly the same way as continuous wall-navigation data.

Conceptually:

```text
FRONT US
    │
    ▼
Distance ahead
    │
    ▼
Safety interpretation
    │
    ├── Safe → normal navigation continues
    │
    └── Dangerous → propulsion interrupted
```

The front sensor does not continuously request left or right steering.

This prevents frontal distance from competing unnecessarily with the two lateral sensors that are responsible for track geometry.

---

# 5.20 Interaction With the Steering System

The ultrasonic sensors do not physically control the steering motor.

Instead, their measurements pass through the EV3 navigation software.

```text
ULTRASONIC SENSOR
        │
        ▼
   Distance Data
        │
        ▼
      LEGO EV3
        │
        ▼
Navigation Interpretation
        │
        ▼
Steering Target
        │
        ▼
      MOTOR B
```

This distinction is important because the same ultrasonic reading can result in different steering behavior depending on the current state.

A large inner distance during a straight section and a large inner distance during corner entry may produce completely different navigation decisions.

The sensor only measures distance; the EV3 provides the context.

---

# 5.21 Interaction With the Drive Motor

The ultrasonic system also affects propulsion.

The lateral sensors can influence how aggressively Piolín navigates close to walls, while the front sensor can interrupt forward motion when necessary.

The relationship is:

```text
LATERAL US
    │
    ▼
Navigation Geometry
    │
    ▼
Steering + Speed Decisions


FRONT US
    │
    ▼
Frontal Safety
    │
    ▼
Possible Motor A Stop
```

This allows the same sensing subsystem to support both navigation and safety without assigning every sensor the same authority.

---

# 5.22 Interaction With the Color Sensor

The ultrasonic sensors do not determine the initial clockwise or counterclockwise direction by themselves.

That information is established using the floor-color system.

Once direction is known, the EV3 can assign the left and right ultrasonic sensors correctly.

```text
COLOR SENSOR
     │
     ▼
Determine Direction
     │
     ▼
Clockwise / Counterclockwise
     │
     ▼
Assign S2 + S3 roles
     │
     ├── INNER
     └── OUTER
```

This demonstrates how two different sensing technologies work together.

The color sensor supplies **course-state information**, while the ultrasonic sensors supply **physical wall geometry**.

---

# 5.23 Interaction With the HuskyLens

During the Obstacle Challenge, the ultrasonic sensors remain active even when the HuskyLens is providing visual information about colored pillars.

The two systems solve different perception problems.

```text
HUSKYLENS
    │
    ▼
What obstacle is visible?


ULTRASONIC SENSORS
    │
    ▼
Where are the surrounding walls?
```

The EV3 then combines those information sources.

This is particularly useful because a camera-based avoidance maneuver should still respect the physical boundaries of the track.

The HuskyLens can provide information about a pillar, while the ultrasonic sensors continue describing the robot's relationship with the surrounding walls.

---

# 5.24 Ultrasonic Responsibility by Competition Challenge

The same three ultrasonic sensors remain physically installed in both competition challenges.

Their responsibilities can be summarized as:

| Sensor | Open Challenge | Obstacle Challenge |
| :--- | :--- | :--- |
| **Front US — S1** | Frontal safety | Frontal safety |
| **Right US — S2** | Wall navigation | Wall navigation and obstacle-path safety |
| **Left US — S3** | Wall navigation | Wall navigation and obstacle-path safety |

The Obstacle Challenge adds vision information but does not remove the need for ultrasonic geometry.

This allows Piolín to preserve the same fundamental navigation platform between both challenges.

---

# 5.25 Why Three Sensors Are Used Instead of One

A single ultrasonic sensor cannot observe all the geometric regions that are important to Piolín.

A sensor facing one side provides no direct information about the opposite side.

Similarly, the two lateral sensors cannot reliably observe every object directly ahead of the vehicle.

The final three-sensor arrangement therefore covers three different regions:

```text
                     FRONT REGION
                         S1
                          ↑
                          │

      LEFT REGION  ←   PIOLÍN   →  RIGHT REGION
           S3                         S2
```

This does not mean that Piolín attempts to combine all three distances into one large steering formula.

Instead, coverage is divided by purpose.

```text
S2 + S3
   ↓
Navigation geometry


S1
   ↓
Frontal safety
```

This is a more modular use of sensor redundancy.

---

# 5.26 Why More Sensors Were Not Automatically Better

During Piolín's development, an important engineering lesson was that adding more sensors does not necessarily create better navigation.

Every additional sensor introduces another measurement that must be mounted correctly, interpreted correctly, integrated into software, and prevented from conflicting with the other control systems.

The final architecture therefore focuses on **clear responsibility rather than maximum sensor quantity**.

The three ultrasonic sensors were retained because each one observes a region that is relevant to the vehicle:

```text
LEFT
RIGHT
FRONT
```

No sensor is included simply to increase the number of components.

This matches the broader design philosophy used throughout Piolín: each active component should solve a clearly defined problem.

---

# 5.27 Ultrasonic Failure Considerations

Ultrasonic sensors are useful, but their measurements should not be treated as infallible.

Several physical conditions can affect the data.

| Condition | Possible Sensor Effect | System Interpretation |
| :--- | :--- | :--- |
| **Wall ends at corner** | Distance increases dramatically | Possible geometry transition |
| **Robot rotates relative to wall** | Distance changes | Heading and lateral position both influence reading |
| **Isolated reflection** | Temporary abnormal value | Software filtering reduces influence |
| **Open space** | Very large distance | Sensor may no longer be observing a wall |
| **Outer wall becomes close** | Distance decreases | Possible lateral safety condition |
| **Object directly ahead** | Front distance decreases | Possible frontal safety condition |
| **Mounting movement** | Persistent bias | Sensor geometry no longer matches chassis geometry |

The final navigation system therefore interprets ultrasonic data together with the robot's current state instead of assuming that every measurement has one universal meaning.

---

# 5.28 Sensor Mounting and Mechanical Rigidity

The accuracy of a distance sensor depends not only on its electronics but also on its physical mounting.

If an ultrasonic sensor changes angle relative to the chassis, the direction of the acoustic measurement also changes.

```text
CORRECT MOUNT

[ SENSOR ] ─────────→ WALL


ROTATED MOUNT

[ SENSOR ]
      \
       \
        ───────────→ WALL
```

A flexible or loose mount can therefore create a persistent change in measured geometry even when the software has not changed.

For this reason, the ultrasonic sensors are treated as part of Piolín's mechanical reference frame.

The lateral sensors must remain consistently oriented relative to the chassis so that the wall-navigation model continues to describe the same physical geometry.

---

# 5.29 Ultrasonic Sensor Responsibility Matrix

The final responsibility of each sensor can be summarized as:

| Function | Front S1 | Right S2 | Left S3 |
| :--- | :---: | :---: | :---: |
| **Frontal Safety** | **Primary** | — | — |
| **Right-Wall Measurement** | — | **Primary** | — |
| **Left-Wall Measurement** | — | — | **Primary** |
| **Inner-Wall Navigation** | — | Dynamic | Dynamic |
| **Outer-Wall Reference** | — | Dynamic | Dynamic |
| **Straight Geometry** | — | **Used** | **Used** |
| **Corner Interpretation** | Safety only | **Used** | **Used** |
| **Obstacle-Wall Awareness** | Frontal safety | **Used** | **Used** |

This matrix shows that the sensor hardware remains fixed while software responsibility changes according to the navigation context.

---

# 5.30 Final Hardware Integration

The complete ultrasonic subsystem connects directly to the EV3:

```text
                         LEGO EV3
                            │
            ┌───────────────┼───────────────┐
            │               │               │
            ▼               ▼               ▼
           S1              S2              S3
            │               │               │
            ▼               ▼               ▼
       FRONT US         RIGHT US         LEFT US
            │               │               │
            ▼               └───────┬───────┘
     Frontal Safety                 │
                                    ▼
                            Track Geometry
                                    │
                         ┌──────────┴──────────┐
                         ▼                     ▼
                    Wall Following       Corner Handling
```

The final arrangement gives the EV3 direct access to all three distance measurements without requiring an intermediate microcontroller.

This keeps one of Piolín's most important navigation subsystems compact and directly integrated with the main controller.

---

# 5.31 Engineering Decision Summary

The final ultrasonic architecture is the result of several changes in how Piolín interprets the competition environment.

The key decisions were:

```text
Diagonal lateral sensing
          ↓
Harder geometric interpretation
          ↓
Direct lateral sensing selected
```

and:

```text
Two lateral sensors
          ↓
Strong side-wall awareness
          ↓
Limited direct frontal coverage
          ↓
Front ultrasonic added on S1
```

The important result is that the third sensor was **not added to complicate the wall-following algorithm**.

It was added to solve a separate missing problem: direct frontal safety.

This produced the final responsibility structure:

> **S2 + S3 → navigation geometry**

> **S1 → frontal safety**

The result is a sensor architecture in which each measurement has a clearly defined physical meaning and software responsibility.

---

# 5.32 Final Ultrasonic Architecture Summary

Piolín's final WRO Future Engineers 2026 configuration uses **three LEGO ultrasonic sensors connected directly to the EV3**.

```text
                         FRONT
                           ↑

                     FRONT US
                        S1
                           │
                           │

            LEFT US ← [ PIOLÍN ] → RIGHT US
               S3                      S2

                           │
                           ↓
                          REAR
```

The two lateral sensors form the primary wall-navigation system. Their roles change dynamically between inner and outer references depending on whether Piolín is travelling clockwise or counterclockwise.

The front sensor remains independent from this assignment and monitors the region directly ahead of the vehicle for frontal safety conditions.

The final engineering concept can therefore be summarized as:

> **Left and right ultrasonic sensors tell Piolín where it is relative to the track.**

> **The front ultrasonic sensor tells Piolín when continuing forward may no longer be safe.**

Together, the three sensors provide a compact distance-sensing architecture that supports wall following, corner interpretation, lateral safety, frontal safety, and obstacle-round navigation while keeping each sensor's responsibility clearly separated.

Detailed mathematical processing of the lateral measurements, filtering behavior, geometric consistency model, and corner interpretation are documented separately in:

```text
docs/power_sensors/02_USSensorD.md
```
