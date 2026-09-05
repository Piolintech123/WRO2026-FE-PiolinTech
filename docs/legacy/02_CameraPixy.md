# 2. Legacy PixyCam Vision System

> [!WARNING]
> **This document describes a previous Piolín vision architecture.**
>
> The PixyCam system documented here is **not part of the current WRO Future Engineers 2026 robot configuration**.
>
> Piolín currently uses a **HuskyLens + Arduino Nano** vision subsystem, with the Nano communicating with the LEGO EV3 through USB.
>
> Current documentation:
>
> [HuskyLens Vision System](../components/07_HuskyLens.md)  
> [Hardware Overview](../components/01_Hardwareoverview.md)  
> [Legacy Documentation Notice](00_LEGACY_NOTICE.md)

---

## 2.1 Purpose of This Document

During an earlier stage of Piolín's development, a **PixyCam 2.1** was explored as the robot's primary visual-perception device for the WRO Future Engineers Obstacle Challenge.

The objective of this architecture was to give Piolín information that the ultrasonic sensors could not provide.

The ultrasonic sensors could answer:

```text
How far is the robot from a wall?
```

but they could not answer:

```text
What color is the obstacle ahead?
```

The PixyCam was introduced to solve that missing perception problem.

The historical architecture therefore separated two different types of environmental information:

```text
ULTRASONIC SENSORS
        ↓
Distance and wall geometry


PIXyCAM
        ↓
Colored-object recognition
```

The EV3 could then use both forms of information when determining the robot's movement.

This architecture was later replaced by the current HuskyLens and Arduino Nano system.

---

# 2.2 Historical Vision Architecture

The PixyCam acted as a dedicated vision device rather than requiring the EV3 to process complete camera images directly.

Conceptually, the system worked as:

```text
VISIBLE ENVIRONMENT
        ↓
PIXyCAM
        ↓
Color/Object Detection
        ↓
Detection Information
        ↓
LEGO EV3
        ↓
Navigation Decision
        ↓
Drive + Steering
```

This was important because the EV3 remained responsible for the actual vehicle behavior.

The camera supplied visual information.

The EV3 interpreted that information and determined how Piolín should respond.

The PixyCam therefore belonged to the **perception layer**, not the final actuation layer.

---

# 2.3 Why a Dedicated Vision Processor Was Considered

Processing raw camera images directly on the main controller would add substantial computational responsibility to the EV3.

The PixyCam reduced that requirement by performing object detection internally and returning simplified information about detected objects.

Instead of the EV3 needing to process:

```text
Complete Image
    ↓
Thousands of Pixels
    ↓
Color Segmentation
    ↓
Object Detection
```

the intended architecture was closer to:

```text
Complete Image
    ↓
PixyCam Processing
    ↓
Detected Object Data
    ↓
EV3
```

This made the camera attractive for Piolín's early obstacle-recognition experiments.

The vision subsystem could identify relevant colored regions while allowing the EV3 to continue concentrating on navigation and motor control.

---

# 2.4 Color Connected Components

The PixyCam vision system used **Color Connected Components**, commonly referred to as CCC, to detect trained color signatures.

The basic principle was:

```text
Camera captures scene
        ↓
Pixels are analyzed by color
        ↓
Pixels belonging to a trained signature
are grouped
        ↓
Connected region identified
        ↓
Bounding box generated
```

A detected object could then be represented using information such as:

```text
Object signature

Horizontal position

Vertical position

Bounding-box width

Bounding-box height
```

This was much more useful for navigation than transferring an entire raw image to the EV3.

The camera therefore converted a complex visual scene into a smaller set of structured object measurements.

---

# 2.5 Bounding-Box Representation

When a trained color region was detected, the PixyCam could represent it as a rectangular region around the object.

Conceptually:

```text
        CAMERA IMAGE

┌─────────────────────────────┐
│                             │
│          ┌───────┐          │
│          │       │          │
│          │OBJECT │          │
│          │       │          │
│          └───────┘          │
│                             │
└─────────────────────────────┘
```

From this region, the software could obtain a horizontal center position.

If:

```text
X_LEFT  = left side of bounding box

WIDTH   = bounding-box width
```

then the approximate object center could be written as:

```text
X_DETECTED =
X_LEFT + WIDTH / 2
```

The EV3 could then compare that object position with a chosen reference position in the camera frame.

---

# 2.6 Horizontal Position Error

One of the main navigation concepts explored with the PixyCam was using the horizontal position of the detected object to calculate a steering-related error.

The basic relationship was:

```text
ERROR =
X_TARGET - X_DETECTED
```

where:

```text
X_TARGET
=
Desired horizontal reference in the image


X_DETECTED
=
Detected object center
```

If the object appeared approximately at the chosen target location:

```text
ERROR ≈ 0
```

If the object appeared farther to one side:

```text
|ERROR| increases
```

This gave the software a numerical description of where the object appeared relative to the desired image position.

However, this image-space error did not directly represent a physical steering angle.

It still had to be interpreted by the EV3 navigation logic.

---

# 2.7 Historical PixyCam Image

<div align="center">
  <img
    width="399"
    height="367"
    alt="Legacy Piolín PixyCam vision system"
    src="https://github.com/user-attachments/assets/fbc13369-75e1-466d-a10b-e170476c5e9d"
  />
  <br>
  <sub><b>Figure 2.1.</b> PixyCam used during an earlier stage of Piolín's vision-system development.</sub>
</div>

The image above belongs to the previous PixyCam architecture documented in this file.

It should not be interpreted as Piolín's current obstacle-recognition hardware.

---

# 2.8 Visual Detection vs. Steering

An important distinction in the historical architecture was that the PixyCam did **not** directly steer the robot.

The camera only provided visual information.

The complete control relationship was:

```text
PIXyCAM
    ↓
Object Detection
    ↓
Object Position
    ↓
LEGO EV3
    ↓
Navigation Interpretation
    ↓
Steering Command
    ↓
Motor B
    ↓
Ackermann Steering
```

This separation remains conceptually important in the current robot as well.

A perception sensor can provide information about an obstacle, but the main controller must still decide whether that information should cause a steering change.

---

# 2.9 Proportional Steering Concept

The historical software explored proportional steering based on the visual error.

A simplified relationship was:

```text
STEERING_COMMAND =
Kp × ERROR
```

where:

```text
ERROR =
X_TARGET - X_DETECTED
```

A larger visual displacement could therefore request a larger steering correction.

Conceptually:

```text
Object close to target
        ↓
Small visual error
        ↓
Small correction


Object far from target
        ↓
Large visual error
        ↓
Larger correction
```

This approach was useful because it avoided treating every object position as a binary left/right event.

However, the resulting steering behavior still depended on:

```text
Vehicle speed

Camera position

Field of view

Steering geometry

Mechanical response

Distance to obstacle
```

A camera-space error alone could therefore not define the complete vehicle trajectory.

---

# 2.10 PID Concepts Explored During Development

Some Piolín development work also explored PID-style control relationships.

The general controller can be represented as:

```text
u(t) =
Kp × e(t)
+
Ki × integral(e(t))
+
Kd × derivative(e(t))
```

where:

```text
e(t) = current control error
```

The proportional term responds to the current error.

The integral term responds to accumulated error.

The derivative term responds to how quickly the error is changing.

However, the presence of a PID equation in historical documentation should not be interpreted as proof that every PixyCam behavior used a complete PID controller in the final implementation of that stage.

The PixyCam experiments primarily demonstrated how visual position information could be converted into useful control variables.

Current software strategy should be read from the current software documentation rather than inferred from this legacy file.

---

# 2.11 Why Camera Error Was Not Enough by Itself

A detected object's horizontal location describes where it appears in the camera image.

It does not directly describe:

```text
Distance to the left wall

Distance to the right wall

Exact physical distance to the pillar

Vehicle heading

Available clearance
```

For example, the same horizontal camera coordinate can occur when:

```text
The pillar is far away

or

The pillar is much closer
```

The required physical maneuver can be very different in those two situations.

This demonstrated the need to combine visual information with other sensors rather than treating the camera as the only navigation reference.

---

# 2.12 Integration With Ultrasonic Sensors

The PixyCam was therefore combined conceptually with Piolín's ultrasonic navigation system.

The two systems provided different information:

```text
PIXyCAM
   ↓
Obstacle identity / visual position


ULTRASONICS
   ↓
Wall-distance information
```

The EV3 could then combine both sources:

```text
              PIXyCAM
                 │
                 ▼
            Object Data
                 │
                 │
                 ▼
              LEGO EV3
                 ▲
                 │
                 │
          Wall Distances
                 ▲
                 │
           ULTRASONICS
```

This represented an early form of sensor fusion in Piolín's architecture.

The camera described an obstacle.

The ultrasonic sensors described the surrounding physical boundaries.

---

# 2.13 Why Wall Information Remained Necessary

A visually correct obstacle-avoidance direction could still produce a collision if the track wall was ignored.

For example:

```text
Camera requests movement left
        ↓
Robot steers left
        ↓
Left wall is already close
        ↓
Collision risk
```

The visual system therefore needed to coexist with wall-safety logic.

A more complete navigation relationship was:

```text
Obstacle Detection
        +
Wall Geometry
        ↓
EV3 Decision
        ↓
Final Steering Command
```

This lesson remained important even after the PixyCam itself was replaced.

---

# 2.14 Camera Field of View

A major characteristic of any camera-based navigation system is its limited **field of view**.

The PixyCam could only detect an obstacle when that obstacle appeared inside the visible camera region.

Conceptually:

```text
              CAMERA VIEW
                 \     /
                  \   /
                   \ /
               [ PIXYCAM ]
                    │
                 [PIOLÍN]
```

An object outside this region could not provide useful visual information.

This introduced a physical dependency between:

```text
Camera position
      ↓
Visible region
      ↓
Detection timing
      ↓
Available reaction distance
```

The camera mounting therefore became an important part of the obstacle-navigation system.

---

# 2.15 Effect of Vehicle Rotation

Because the camera was attached to Piolín's chassis, the visible scene changed whenever the robot turned.

For example:

```text
Before steering:

             PILLAR
                ●
                │
           [ PIOLÍN ]


During steering:

       PILLAR
          ●

               [ PIOLÍN ]
                    ↗
```

The pillar could move rapidly across the image or leave the field of view during an active maneuver.

Loss of visual detection therefore did not automatically mean that the obstacle had disappeared physically.

This became an important limitation of camera-only steering concepts.

---

# 2.16 Lighting Dependence

Color-based visual detection also depends on the appearance of the object under the available lighting.

Factors such as:

```text
Ambient illumination

Object brightness

Shadows

Reflections

Camera exposure

Viewing angle
```

can change how a colored region appears to the sensor.

Color-signature training helped the camera distinguish selected colors, but it did not make the system completely independent from environmental lighting.

The vision system therefore required both software configuration and appropriate physical camera placement.

---

# 2.17 Object Size and Distance

The apparent size of an obstacle in the camera image changes with its distance from the robot.

Conceptually:

```text
FAR OBJECT
    ↓
Small bounding box


CLOSER OBJECT
    ↓
Larger bounding box
```

This meant that bounding-box dimensions could potentially provide additional context beyond horizontal position.

However, image size is influenced by perspective and camera geometry and should not automatically be interpreted as an exact physical-distance measurement.

Piolín's ultrasonic sensors remained more appropriate for direct wall-distance information.

---

# 2.18 Camera Detection and Vehicle Response Are Different Events

The moment when the PixyCam detected an object and the moment when the physical robot completed a steering maneuver were separated by several stages.

```text
Object enters camera view
        ↓
PixyCam identifies object
        ↓
Detection reaches EV3
        ↓
EV3 interprets information
        ↓
Steering command changes
        ↓
Motor B moves linkage
        ↓
Front wheels change angle
        ↓
Vehicle trajectory changes
```

This distinction became important during obstacle avoidance.

Earlier detection could provide more physical distance for the robot to react, while late detection could require more aggressive steering.

---

# 2.19 Interaction With Ackermann Steering

Piolín uses car-like front-wheel steering rather than differential steering.

Therefore, visual steering commands eventually had to be converted into a position for the Ackermann steering mechanism.

The relationship was:

```text
Camera Position Error
        ↓
Control Calculation
        ↓
Steering Target
        ↓
Motor B
        ↓
Mechanical Linkage
        ↓
Front Wheel Angles
        ↓
Vehicle Path
```

This means:

```text
CAMERA ERROR
    ≠
FRONT WHEEL ANGLE
```

and:

```text
MOTOR ENCODER POSITION
    ≠
PHYSICAL WHEEL ANGLE
```

The complete physical steering system had to be considered when converting vision information into movement.

---

# 2.20 Steering Geometry

The Ackermann mechanism allows the inner and outer front wheels to follow different turning radii.

For an idealized vehicle model:

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

W = track width

R = turning radius
```

These equations describe the geometric principle behind Ackermann steering.

They should not be interpreted as evidence that the PixyCam directly calculated the physical wheel angles.

The camera provided perception information, while the steering architecture remained a separate mechanical and control subsystem.

---

# 2.21 Ultrasonic Distance Principle

The ultrasonic sensors used alongside the vision system operated using time-of-flight distance measurement.

The basic physical relationship is:

```text
DISTANCE =
(SPEED_OF_SOUND × ECHO_TIME) / 2
```

The division by two is required because the ultrasonic pulse travels:

```text
Sensor
   ↓
Wall
   ↓
Sensor
```

The LEGO ultrasonic sensors provide the resulting distance information to the EV3 without requiring the navigation program to manually process the acoustic timing.

This information complemented the camera's visual data.

---

# 2.22 Historical Sensor-Fusion Concept

The previous Piolín obstacle architecture can therefore be summarized as:

```text
                   ENVIRONMENT
                        │
           ┌────────────┴────────────┐
           ▼                         ▼
     COLORED OBJECTS               WALLS
           │                         │
           ▼                         ▼
       PIXyCAM                  ULTRASONICS
           │                         │
           ▼                         ▼
      Visual Data                Distances
           │                         │
           └────────────┬────────────┘
                        ▼
                     LEGO EV3
                        │
                Navigation Decision
                        │
             ┌──────────┴──────────┐
             ▼                     ▼
          MOTOR A               MOTOR B
           Drive               Steering
```

The concept was valuable because it separated environmental perception into specialized sensing methods.

---

# 2.23 Limitations Identified With the PixyCam Architecture

The PixyCam provided useful visual information, but the development process also revealed important limitations.

| Limitation | Effect on Navigation |
| :--- | :--- |
| **Finite field of view** | Obstacles outside the visible region could not be detected |
| **Camera rotation with chassis** | Objects could quickly leave the image during turns |
| **Lighting dependence** | Color appearance could change with environment |
| **Image position is not physical position** | Additional geometry was required |
| **Loss of visual target** | Navigation still needed another environmental reference |
| **Camera mounting dependency** | Physical position directly affected detection timing |
| **Additional integration complexity** | Vision had to coexist with EV3 navigation |
| **Obstacle detection alone was insufficient** | Wall safety still required ultrasonic sensing |

These limitations did not mean that camera vision was unnecessary.

Instead, they helped define what the vision system should and should not be responsible for.

---

# 2.24 Why the PixyCam Was Replaced

Piolín's vision architecture changed as the robot evolved.

The final system no longer uses the PixyCam.

Instead, Piolín currently uses:

```text
HUSKYLENS
     ↓
ARDUINO NANO
     ↓
USB
     ↓
LEGO EV3
```

The change should be interpreted as a **system-level redesign**, not simply as replacing one camera with another.

The current architecture establishes a clearer separation between:

```text
VISUAL PERCEPTION
     ↓
HuskyLens


VISION INTERFACE
     ↓
Arduino Nano


MAIN CONTROL
     ↓
LEGO EV3
```

The PixyCam experiments contributed directly to understanding what information the obstacle-navigation system required.

---

# 2.25 Legacy vs. Current Vision Architecture

The progression can be represented as:

```text
LEGACY

Environment
    ↓
PixyCam
    ↓
Visual Detection
    ↓
EV3
    ↓
Obstacle Logic
```

compared with:

```text
CURRENT

Environment
    ↓
HuskyLens
    ↓
Arduino Nano
    ↓
USB
    ↓
EV3
    ↓
Obstacle Logic
```

The current system should always be used when reconstructing Piolín.

---

# 2.26 Current HuskyLens Identification

The current Piolín obstacle architecture uses known HuskyLens identifiers:

```text
ID 1 = GREEN PILLAR

ID 2 = RED PILLAR
```

Their current interpretation is:

```text
GREEN
  ↓
Pass on the LEFT
```

and:

```text
RED
  ↓
Pass on the RIGHT
```

These IDs belong to the **current HuskyLens system**, not the PixyCam architecture documented in this file.

They are included here only to clearly distinguish the previous and current vision approaches.

For current implementation details, use:

[HuskyLens Vision System](../components/07_HuskyLens.md)

---

# 2.27 What Remained Useful From the PixyCam Experiment

Although the camera itself was replaced, several engineering concepts remained valuable.

The PixyCam experiments demonstrated that:

```text
Obstacle identity
        ≠
Obstacle distance
```

and:

```text
Visual perception
        ≠
Final steering command
```

They also demonstrated the importance of:

```text
Field of view

Camera placement

Detection timing

Wall safety

Sensor fusion

Separating perception from control
```

These principles remained relevant when Piolín transitioned to the HuskyLens architecture.

---

# 2.28 Why This File Is Preserved

This file remains in `docs/legacy/` because it documents an important stage in Piolín's obstacle-navigation development.

The engineering progression was:

```text
Need obstacle recognition
        ↓
PixyCam selected
        ↓
Color-based object detection explored
        ↓
Image position used as navigation input
        ↓
Integration with ultrasonic sensing
        ↓
Physical and software limitations observed
        ↓
Vision architecture reconsidered
        ↓
HuskyLens + Arduino Nano adopted
```

Deleting the PixyCam documentation would remove the evidence explaining why the current architecture developed as it did.

---

# 2.29 Do Not Use the PixyCam Configuration for the Current Robot

The following architecture is **legacy**:

```text
PixyCam
   ↓
Previous Piolín vision implementation
```

It should not be combined with the current hardware configuration.

The current robot uses:

```text
                         LEGO EV3
                            │
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
         Motor A         Motor B           S1–S4
          Drive          Steering          Sensors

                            ▲
                            │ USB
                            │
                      Arduino Nano
                            ▲
                            │
                        HuskyLens
```

For reconstruction of the final robot, use:

[Current Hardware](../components/)  
[Current HuskyLens](../components/07_HuskyLens.md)  
[Current Wiring](../reproducibility/03_wiring.md)  
[Current Electrical Schematic](../reproducibility/04_elecschem.md)

---

# 2.30 Final Legacy Summary

The **PixyCam 2.1** was part of an earlier Piolín vision architecture developed to provide color-based obstacle information to the EV3.

Its historical role was to transform the visual scene into simplified detected-object information such as:

```text
Color signature

Object position

Bounding-box dimensions
```

This information could then be used by the EV3 to create navigation decisions.

The historical perception chain was:

```text
COLORED OBJECT
      ↓
PIXyCAM
      ↓
OBJECT DETECTION
      ↓
VISUAL POSITION
      ↓
LEGO EV3
      ↓
STEERING / DRIVE DECISION
```

The experiments also demonstrated important limitations associated with camera navigation, including field of view, lighting, target loss during steering, and the difference between image position and physical track geometry.

These observations reinforced the need to combine vision with other sensors.

Piolín eventually moved to the current architecture:

```text
HUSKYLENS
     ↓
ARDUINO NANO
     ↓
USB
     ↓
LEGO EV3
```

The PixyCam documentation is therefore preserved as:

> **A historical vision-system implementation that contributed to Piolín's current obstacle-perception architecture, not as the current competition camera configuration.**

Return to:

[Legacy Documentation Notice](00_LEGACY_NOTICE.md)

Current documentation:

[Hardware Overview](../components/01_Hardwareoverview.md)  
[Ultrasonic Sensors](../components/05_UltrasonicSensors.md)  
[HuskyLens](../components/07_HuskyLens.md)  
[Power Distribution](../components/09_PowerDistribution.md)
