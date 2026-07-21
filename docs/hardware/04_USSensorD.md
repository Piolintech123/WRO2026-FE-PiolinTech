
# 4. Ultrasonic Sensor Array Design and Placement

This document details the spatial layout, mathematical positioning, and physical mounting configuration of the ultrasonic range-finding array on **"Piolín"**.

---

## 4.1 Sensor Layout and Mounting Architecture

To achieve complete spatial awareness without adding dead zones, the robot uses a custom **dual-inclined side sensor array** combined with a front-facing sensor. This layout ensures the robot can scan the walls of the track and detect obstacles simultaneously.


<img width="1600" height="900" alt="image" src="https://github.com/user-attachments/assets/ce15c2f7-eebd-47b4-b352-60b27ea47d67" />


### 4.1.1 Spatial Orientation and Angle Selection
Unlike flat-mounted sensors that point directly to the left and right (at $90^\circ$ angles), the side sensors on "Piolín" are mounted on custom 3D-printed brackets **inclined forward at exactly $30^\circ$** relative to the longitudinal driving axis ($120^\circ$ and $60^\circ$ sweeps respectively).

This precise physical layout offers several mechanical advantages:
*   **Predictive Wall Detection:** By pointing slightly forward, the side sensors detect approaching corners and track walls *before* the robot physically reaches them. This allows the PID steering controller to calculate smoother turning curves.
*   **Blind Spot Elimination:** The $30^\circ$ incline bridges the sensing gap between the central forward sensor and the sides of the chassis. This ensures that diagonal obstacles are always captured in the active field of view.
*   **Acoustic Cross-Talk Prevention:** Angling the sensors away from each other prevents the ultrasonic pulses emitted by one transducer from bouncing back into the receiver of another, eliminating telemetry noise and spike readings.

    <div align="center">
  <img src="https://github.com/user-attachments/assets/a0955d23-b504-4ae6-9411-2c82d0c5c52f" width="400" alt="Robot Configuration" />
</div>

---

## 4.2 Electrical Specifications and Pinout

The ultrasonic array uses three standard **HC-SR04** (or equivalent) transducers powered directly from the primary power rail.

Because the Raspberry Pi 5 logic operates strictly at **$3.3\text{V}$** while the HC-SR04 sensors output a **$5\text{V}$** signal on their Echo pins, we integrated **custom voltage dividers** (using $1\text{ k}\Omega$ and $2\text{ k}\Omega$ resistors) on each Echo line. This safely drops the signal voltage to protect the Pi's GPIO pins.

### 4.2.1 Technical GPIO Mapping

| Sensor Position | Trigger Pin (Output) | Echo Pin (Input) | Operating Voltage | Voltage Divider Required? |
| :--- | :--- | :--- | :--- | :--- |
| **Left ($30^\circ$ Inclined)** | GPIO 23 | GPIO 24 | $5\text{V}$ | Yes ($5\text{V} \rightarrow 3.3\text{V}$) |
| **Center (Front-Facing)** | GPIO 17 | GPIO 27 | $5\text{V}$ | Yes ($5\text{V} \rightarrow 3.3\text{V}$) |
| **Right ($30^\circ$ Inclined)** | GPIO 5 | GPIO 6 | $5\text{V}$ | Yes ($5\text{V} \rightarrow 3.3\text{V}$) |

---

## 4.3 Algorithmic Integration & Obstacle Evasion

The distances calculated from the three sensor channels are parsed concurrently by a high-frequency Python polling thread.


```


   [Left Distance]        [Center Distance]       [Right Distance]
          │                       │                      │
          └───────────────────────┼──────────────────────┘
                                  ▼
                    [Priority Routing Matrix]
                                  │
           ┌──────────────────────┴──────────────────────┐
           ▼                                             ▼
 [Distance < 25 cm]                             [Distance >= 25 cm]
           │                                             │
           ▼                                             ▼


[Trigger Obstacle Evasion]                     [Maintain PID Lane Keeping]

```

1.  **Primary Wall Following:** The left and right sensors monitor the distance to the track boundaries. The steering software calculates the difference ($e(t) = D_{\text{left}} - D_{\text{right}}$) and passes it directly to the proportional-integral-derivative (PID) algorithm to keep the robot centered in the lane.
2.  **Proximity Interrupts:** If the center sensor detects an object closer than $25\text{ cm}$, it triggers a high-priority software interrupt. The robot immediately stops running the standard lane-keeping PID and queries the Huskylens camera to decide whether to pass the obstacle on the left or the right.


