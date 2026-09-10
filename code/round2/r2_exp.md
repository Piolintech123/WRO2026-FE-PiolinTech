# Round 2 EV3 V1 — Code Explanation

This document explains the logic implemented in [`ev3v1.py`](./ev3v1.py), an early obstacle-round software version developed for Piolín during the evolution of the WRO Future Engineers 2026 project.

Unlike the first Open Challenge program, this version introduces visual perception through the **Pixy2.1 camera** and combines it with the two lateral EV3 Ultrasonic Sensors. The objective of the program is to allow Piolín to navigate using basic lateral correction while identifying Red and Green pillars and selecting the passing side required by the WRO rules.

This program represents an important intermediate development stage. It already includes several ideas that later became fundamental to the current obstacle architecture, such as separating pillar identity from image position, validating detections before using them, preserving a detected target during short camera losses, and assigning priorities between obstacle avoidance and wall protection.

However, `ev3v1.py` should be considered a **development baseline**, not the current complete Round 2 controller. It does not yet contain the complete corner state machine, reliable three-lap progression, dedicated pass confirmation, full post-pillar recovery, or the final parking sequence.

---

## Hardware Configuration

This version uses the obstacle-round hardware configuration of Piolín.

| Port | Component | Function |
|---|---|---|
| A | EV3 Large Motor | Rear propulsion |
| B | EV3 Medium Motor | Ackermann steering |
| S1 | Pixy2.1 | Red, Green, and Pink visual perception |
| S2 | EV3 Ultrasonic Sensor | Left lateral sensing |
| S3 | EV3 Ultrasonic Sensor | Right lateral sensing |
| S4 | EV3 Color Sensor | Floor sensing and future course-event integration |

Motor A provides propulsion while Motor B controls the front Ackermann steering mechanism. As in the current Piolín architecture, propulsion and steering remain independent.

The two Ultrasonic Sensors retain fixed physical identities. S2 is always the **left** sensor and S3 is always the **right** sensor. Their physical assignments do not change depending on course direction.

During Round 2, Pixy2.1 occupies S1. The EV3 Gyro Sensor used during the Open Challenge is therefore not installed at the same time.

---

## Pixy2.1 Integration

The camera is initialized through the EV3 S1 connection using the `Pixy2` interface:

```python
PIXY = Pixy2(
    port=1,
    i2c_address=0x54
)
```

This version uses Pixy2.1's Color Connected Components capability to receive detected colored blocks. Instead of attempting to interpret the entire image, the program works with information already extracted by the camera, including the object's signature, horizontal position, vertical position, width, and height.

The three signatures used in the current Piolín convention are:

| Signature | Color | Purpose |
|---|---|---|
| `sig1` | Pink | Parking reference |
| `sig2` | Red | Pillar that must be passed on the right |
| `sig3` | Green | Pillar that must be passed on the left |

The program requests these three signatures using:

```python
PIXY_SIGNATURE_MASK = 0x07
```

although this V1 controller actively uses Red and Green for obstacle navigation. Pink is reserved for later parking integration.

---

## The Most Important Obstacle Rule

One of the most important ideas in this program is that the **pillar signature determines the passing side**.

For Piolín:

```python
SIG_RED = 2
SIG_GREEN = 3
```

and the WRO behavior is fixed as:

**Red pillar → pass RIGHT**

**Green pillar → pass LEFT**

The location of the object inside the Pixy image does not change this rule.

This is extremely important because early obstacle experiments showed that using the object's horizontal position to decide the passing side could cause the robot to invert Red and Green behavior depending on the angle from which the pillar entered the camera's field of view.

In this version, the image coordinates only influence how strongly Piolín reacts. They never redefine which side is legal.

---

## Steering Convention

The program establishes a consistent steering convention near the beginning of the file:

```python
STEER_LEFT = 1
STEER_RIGHT = -1
CENTER = 0
```

Positive Motor B targets therefore represent left steering and negative targets represent right steering.

This convention is used throughout the complete program so that every controller speaks the same steering language. Normal wall navigation, pillar avoidance, and wall safety all eventually produce a steering angle that follows this same sign convention.

Having one consistent convention is especially important when several control systems are active inside the same program.

---

## Vehicle Speed

The program uses different propulsion speeds depending on the current situation.

`SPEED_NORMAL` is used during ordinary lateral navigation. `SPEED_PILLAR` reduces the speed while Piolín is actively reacting to a detected obstacle, and `SPEED_WALL_DANGER` is used when the Ultrasonic Sensors indicate that the robot is dangerously close to a wall.

This means speed is not treated as one constant value throughout the run. The robot becomes more conservative when the navigation problem becomes more demanding.

The actual values in this file are development values and should not be interpreted as permanently calibrated competition parameters.

---

## Steering Limits

Piolín's steering actuator is controlled through Motor B, but the software prevents the requested angle from increasing without limit.

The main restriction is:

```python
MAX_STEER_ANGLE = 34
```

This represents a software steering boundary for this V1 program.

The normal wall controller is limited even further:

```python
MAX_NORMAL_STEER = 13
```

while obstacle avoidance is allowed to use a stronger range:

```python
MAX_PILLAR_STEER = 30
```

This distinction is intentional. Small wall-position errors should normally produce gentle corrections, while a pillar maneuver may require a substantially stronger trajectory change.

---

## Steering Rate Limiting

The function:

```python
def set_steering(target, immediate=False):
```

does more than simply send a new angle to Motor B.

The program limits how much
