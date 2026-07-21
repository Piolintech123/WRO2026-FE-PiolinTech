<div align="center">
  <img src="https://github.com/user-attachments/assets/839b917a-c2bc-4053-8b2a-f68e43b7efa0" alt="Comparison" style="max-width: 65%; height: auto;" />
</div>

# 2. Robot Hardware and Components Evolution

Our design process has been a journey of overcoming hard technical limitations. We didn't build this current iteration of Piolín overnight; it is the direct result of testing what worked and discarding what failed under actual competition stress. 



| System | Component | Primary Feature / Technical Specification |
| :--- | :--- | :--- |
| **High-Level Processor** | **LEGO Mindstorms EV3** | ARM9-based processor. Handles multi-sensor fusion, PID motor control, and state machines. |
| **Computer Vision Engine** | **PixyCam (Pixy2)** | Color-based object detection. Communicates via I2C/SPI to the EV3; handles real-time lane and marker parsing. |
| **Distance Telemetry** | **Ultrasonic Sensor (x3)** | Active ultrasonic transducers (1 front, 2 side) to detect walls and track boundaries. |
| **Heading / Navigation** | **Gyro Sensor** | Provides angular velocity and heading data for steering stabilization and turn precision. |
| **Lane Tracking** | **Color Sensor** | Detects surface contrast and track markers; provides feedback for lane-keeping error corrections. |
| **Propulsion Power** | **LEGO Motors** | High-torque output for rapid acceleration and precise steering actuation. |

---

## 2.1 Robot Hardware and Components Evolution

Our design process has been a journey of overcoming hard technical limitations. We didn't build this current iteration of Piolín overnight; it is the direct result of testing what worked and discarding what failed under actual competition stress. 

### 2.2 Technical Analysis of Components

*   ### Component: LEGO EV3 Brick (Primary Controller)
    *   **Quantity:** 1
    *   **Voltage:** 9V
    *   **Description:** The EV3 Brick functions as the primary actuator controller. It executes commands from onboard programs, controls motors, reads sensor inputs, and coordinates all low-level robot actions.
    <div align="center">
      <img src="https://github.com/user-attachments/assets/ab7c39a9-6f0e-4c9d-aee2-8d59c25d3adc" alt="EV3 Brick" style="max-width: 30%; height: auto; border-radius: 8px; margin: 10px 0;" />
    </div>

*   ### Component: PixyCam (Pixy2)
    *   **Quantity:** 1
    *   **Interface:** I2C / SPI
    *   **Description:** Color-based vision sensor used for object tracking and track-line identification. It processes color signatures at 60 frames per second, sending coordinate data to the EV3 for steering corrections.
    <div align="center">
      <img src="https://github.com/user-attachments/assets/7affa9bf-dd5e-4f34-a890-4a50c6d409ad" alt="EV3 Brick" style="max-width: 30%; height: auto; border-radius: 8px; margin: 10px 0;" />
    </div>
*   ### Component: Ultrasonic Sensors
    *   **Quantity:** 3 (1 Front, 2 Side)
    *   **Voltage:** 4.5V – 7V
    *   **Description:** High-frequency ranging modules. The front sensor handles obstacle avoidance, while the side sensors (S2, S3) are used to maintain track alignment and assist in evasive maneuvers.
    <div align="center">
      <img src="https://github.com/user-attachments/assets/b8872f62-adb5-4fd1-98fb-18491c57de56" alt="Ultrasonic" style="max-width: 30%; height: auto; border-radius: 8px; margin: 10px 0;" />
    </div>

*   ### Component: LEGO Color Sensor
    *   **Quantity:** 1
    *   **Description:** Used for surface detection and track marker identification. It provides critical feedback on lane trajectories, allowing the robot to distinguish between track types and adjust PID error terms accordingly.
    <div align="center">
      <img src="https://github.com/user-attachments/assets/5e59f3a1-5b7c-4992-9d57-07951f412e67" alt="Color Sensor" style="max-width: 30%; height: auto; border-radius: 8px; margin: 10px 0;" />
    </div>

---

## 3. Evolutionary Timeline

### Version 1 (Phase 1.0: Prototype Chassis)
The initial prototype utilized a standard LEGO Technic chassis driven by the EV3 Brick. The primary limitation was structural compliance; plastic snap-pin connectors allowed for significant chassis twist under steering torque, causing erratic behavior on the track.

### Version 2 (Phase 1.5: LEGO SPIKE Stabilization)
To address the structural flex identified in Phase 1, the frame was rebuilt using cross-braced LEGO SPIKE Prime beams, creating a rigid overhead bridge structure. This successfully eliminated vertical chassis twist and established a stable, fully LEGO ecosystem.

### Version 3 (Current Integrated Configuration)
The current active configuration implements an integrated sensor fusion paradigm. We preserved the rigid SPIKE Prime box-frame structure for compliance and modularity, while leveraging the LEGO Mindstorms EV3 Intelligent Brick to process a sophisticated sensor array. By integrating the PixyCam for real-time computer vision, alongside the precision gyro, ultrasonic, and color sensors, we achieved high-fidelity telemetry, responsive obstacle detection, and accurate lane tracking.

---

## 4. Engineering Achievements & Control Logic

*   **Asynchronous Sensor Fusion:** We have optimized the Pybricks environment to run an asynchronous polling loop. This allows the EV3 to read the PixyCam vision data, gyro heading, and ultrasonic distances concurrently, minimizing latency between visual input and motor output.
*   **PID Control Loop:** Steering is governed by a PID loop that utilizes the gyro and color sensor data as primary feedback. This ensures that the robot maintains a stable heading even when the track geometry changes rapidly.
*   **Predictive Maneuvering:** By fusing the ultrasonic sensor data with vision inputs, the robot can anticipate upcoming track segments, allowing it to initiate evasive maneuvers or tighten steering arcs before an obstacle is even fully in view.

---

## 5. Power Consumption Analysis

| Component | Operating Voltage (V) | Avg. Current (A) | Peak Current (A) |
| :--- | :---: | :---: | :---: |
| LEGO EV3 Brick | 9.0 | 0.20 | 0.50 |
| PixyCam (Pixy2) | 5.0 | 0.10 | 0.15 |
| EV3 L-Motors (x2) | 9.0 | 0.60 | 1.50 |
| Sensors (Gyro, US, Color) | 5.0 | 0.05 | 0.10 |
| **Total** | -- | **0.95 A** | **2.25 A** |

## 6. Technical Analysis of Final System Configuration

The following hardware stack represents the finalized, competition-ready configuration of Piolín. This architecture was selected to maximize processing speed, sensor precision, and electrical stability, ensuring the robot can handle the rigorous demands of the WRO 2026 Future Engineers track. Each component listed below is integrated into our master control loop to enable autonomous navigation, high-speed evasion, and real-time decision-making.

*   ### Component: Huskylens AI Camera Module (Current Primary Vision)
    *   **Quantity:** 1
    *   **Voltage:** 3.3V - 5.0V
    *   **Current Consumption:** ~320 mA (with LCD screen active)
    *   **Interface:** I2C Bus / UART Serial Connection
    *   **Description:** Smart AI vision sensor capable of hardware-accelerated machine learning object tracking and color block matrix recognition. Used as the core track-line alignment and adaptive visual navigation system. 
    <div align="center">
      <img src="https://github.com/user-attachments/assets/737bd86d-a82a-46fa-b683-06f18ec4721b" alt="Component Image" style="max-width: 30%; height: auto; border-radius: 8px; margin: 10px 0;" />
    </div>

---

*   ### Component: Raspberry Pi 5 - 8GB RAM (Processing Core)
    *   **Quantity:** 1
    *   **Voltage:** 5.1V
    *   **Current Consumption:** Up to 5.0A (Peak workload output)
    *   **Interface:** GPIO / Native I2C / Hardware PWM / UART
    *   **Description:** High-performance 64-bit quad-core microcomputer hosting our multi-threaded control architecture. Manages asynchronous sensor data ingestion, executes real-time digital filtering, and computes the master steering PID control outputs. 
    <div align="center">
      <img src="https://github.com/user-attachments/assets/9fb3da92-7bec-4a39-8955-44342d2e165f" alt="Component Image" style="max-width: 30%; height: auto; border-radius: 8px; margin: 10px 0;" />
    </div>

---

*   ### Component: HC-SR04 Ultrasonic Distance Sensor
    *   **Quantity:** 3
    *   **Voltage:** 5.0V
    *   **Current Consumption:** ~15 mA per unit
    *   **Interface:** Digital GPIO (Dedicated Trigger / Echo Pins)
    *   **Description:** High-frequency ultrasonic ranging module providing real-time spatial telemetry from 2 cm to 400 cm. Staggered in a triple-sensor array (-30°, 0°, +30°) to drive our background obstacle evasion subroutines and parallel wall-alignment safety tracking loops.
    <div align="center">
      <img src="https://github.com/user-attachments/assets/f5ddc783-744e-44fe-a237-15ff04f8e7cc" alt="Component Image" style="max-width: 30%; height: auto; border-radius: 8px; margin: 10px 0;" />
    </div>

---

*   ### Component: TB6612FNG Dual Motor Driver IC
    *   **Quantity:** 1
    *   **Voltage:** Logic (VCC): 2.7V - 5.5V / Motor Power (VM): Up to 13.5V
    *   **Current Consumption:** 1.2A Continuous output current (3.2A peak spikes)
    *   **Interface:** Hardware PWM (Speed Control) & Digital GPIO (Direction Pins)
    *   **Description:** High-efficiency Dual H-Bridge integrated circuit used to route regulated current lines directly to the rear traction DC motor based on instructions parsed from the Raspberry Pi 5 control loop.
    <div align="center">
      <img src="https://github.com/user-attachments/assets/dedaad37-bdad-43fa-a155-460b2aa46a68" alt="Component Image" style="max-width: 30%; height: auto; border-radius: 8px; margin: 10px 0;" />
    </div>

---

*   ### Component: XL6019E1 DC-DC Automatic Buck-Boost Converter
    *   **Quantity:** 1
    *   **Voltage:** Input: 5V - 32V / Output: Configured to stable 7.4V Motor Rail
    *   **Current Consumption:** Handles up to 5.0A output current capacity
    *   **Interface:** Direct Hardwired Power Plane Routing
    *   **Description:** High-frequency power management regulator board deployed to electrically isolate inductive motor acceleration surges away from the delicate digital logic rails powering our main processor.
    <div align="center">
      <img src="https://github.com/user-attachments/assets/174f5059-9500-4f5d-90b7-229c98128c7a" alt="Component Image" style="max-width: 30%; height: auto; border-radius: 8px; margin: 10px 0;" />
    </div>

---

*   ### Component: High-Torque Micro Servo Motor
    *   **Quantity:** 1
    *   **Voltage:** 4.8V - 6.0V
    *   **Current Consumption:** ~250 mA (Idle) / 1.2A (Stall peak under load)
    *   **Interface:** Hardware PWM ($50\text{ Hz}$ frequency, $20\text{ ms}$ periodic window)
    *   **Description:** Metal-geared actuator linked directly to our physical front steering linkage blocks to translate spatial orientation adjustments into exact mechanical Ackermann angles.
    <div align="center">
      <img src="https://github.com/user-attachments/assets/8
