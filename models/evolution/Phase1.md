
# 1. Evolution of the Robot Prototype Models

This document details the engineering evolution of our autonomous vehicle, **"Piolín"**, tracing its development from an educational LEGO-based testing platform to a custom-built, high-performance edge-computing robot designed for the World Robot Olympiad (WRO) Future Engineers competition.

---

## 1.1 Prototype Phase 1.0: The LEGO MINDSTORMS EV3 Genesis (Our First Model)

The initial design (shown below) served as a rapid prototyping platform to validate basic closed-loop control algorithms, sensor response times, and basic driving kinematics.

<div align="center">
  <img src="https://github.com/user-attachments/assets/94f45de2-0536-41ca-9f66-075bb64a17f1" alt="Prototype Phase 1.0" width="400"/> 

  <p><em>Prototype Phase 1.0 built entirely with LEGO Technic and the EV3 Intelligent Brick.</em></p>
</div>

### 1.1.1 Architectural Specifications
*   **Primary Controller:** LEGO MINDSTORMS EV3 Intelligent Brick (ARM99 @ 300 MHz, 64 MB RAM) running *ev3dev Linux* / Pybricks.
*   **Actuators:** LEGO EV3 Large and Medium Interactive Servo Motors.
*   **Sensing Array:** Single EV3 Ultrasonic Sensor mounted on a static front bracket.
*   **Chassis & Kinematics:** Standard LEGO Technic beams, pins, and plastic structural frames utilizing a basic differential drive setup.
*   **Power Source:** LEGO Lithium-Ion Rechargeable Battery Pack (7.4V, 2050 mAh).

### 1.1.2 Engineering Lessons & Performance Bottlenecks
While Phase 1.0 was crucial for testing our early Python scripts, we quickly ran into physical and processing limits that prevented competitive performance:

1.  **Computational Latency:** The 300 MHz single-core ARM9 processor on the EV3 brick could not handle multi-threaded sensor reading and real-time obstacle evasion logic without significant loop execution delays (>50 ms).
2.  **Structural Mechanical Play:** The standard LEGO Technic pin-and-beam connections introduced mechanical flex, leading to physical drift and inconsistent steering feedback during sudden accelerations.
3.  **Limited Vision Capabilities:** The EV3 architecture could not support high-speed camera modules or edge-AI vision processing, restricting obstacle recognition to simple, short-range distance checks.
4.  **I/O Port Saturation:** The EV3 brick’s physical design capped our maximum connectivity at 4 sensor inputs and 4 motor outputs, preventing us from expanding to a wider sensor array.

---

## 1.2 Transition to Phase 2.0: The Custom "Piolín" Platform

To overcome the performance limits of the EV3 prototype, we completely redesigned the robot. We shifted from a locked educational ecosystem to an open-hardware, custom-machined design.


```

┌────────────────────────────────────────────────────────────────────────┐
│                        ARCHITECTURAL EVOLUTION                         │
├───────────────────────────────────────┬────────────────────────────────┤
│          PHASE 1.0 (LEGACY)           │       PHASE 2.0 (CURRENT)      │
├───────────────────────────────────────┼────────────────────────────────┤
│ • LEGO MINDSTORMS EV3 (300 MHz ARM9)  │ • Raspberry Pi 5 (2.4 GHz A76) │
│ • Static EV3 Ultrasonic Sensor        │ • Triple Ultrasonic Array      │
│ • No Vision / Camera Capabilities     │ • Huskylens Edge-AI Camera     │
│ • Differential/Skid-Steering          │ • True Ackermann Steering      │
│ • Educational 7.4V LEGO Battery       │ • 225W High-Output Power Bank  │
└───────────────────────────────────────┴────────────────────────────────┘

```

### 1.2.1 Why We Upgraded the Hardware Core
*   **Processing Power:** Upgrading to the **Raspberry Pi 5** gave us a 2.4 GHz quad-core processor and up to 8GB of RAM. This extra power cut our navigation loop latency down to under **1.2 ms**.
*   **Edge-AI Vision:** Adding the **Huskylens** vision sensor offloaded all color and obstacle tracking to an internal RISC-V coprocessor, keeping our main CPU free to run the core steering and path planning code.
*   **Dynamic Actuation:** We replaced the slip-prone differential drive with a **true Ackermann steering geometry** controlled by a high-torque, metal-gear digital servo. This structural change eliminated steering slop and allowed high-speed, predictable lane alignment.
*   **Modular Sensing:** Moving to standard GPIO control allowed us to implement a triple-staggered ultrasonic sensor array (using HC-SR04 sensors on dedicated hardware channels), giving the robot complete 180° spatial awareness.

---

## 1.3 Key Evolutionary Comparison Matrix

| Design Parameter | Phase 1.0 (First Model) | Phase 2.0 (Piolín Current) | Engineering Impact |
| :--- | :--- | :--- | :--- |
| **Control Unit** | LEGO EV3 Brick | Raspberry Pi 5 | Up to 100x increase in computational bandwidth. |
| **Telemetry Bus** | Proprietary RJ12 (Analog/I2C) | Hardware I2C & Direct GPIO | High-frequency data transfers with zero dropouts. |
| **Steering Type** | Differential Skid-Steer | Ackermann Geometry | True car-like steering; eliminates wheel slip on turns. |
| **Vision Processor** | None | Huskylens AI Cam (K210) | Localized neural-net object tracking at 50 FPS. |
| **Logic Voltage** | 5.0V / 9.0V | 3.3V (Protected with Dividers) | Safe, standardized interfacing with high-speed components. |
| **Power Budget** | ~15W Max Limit | 225W Fast-Charge Delivery | Continuous peak performance without voltage sags. |

