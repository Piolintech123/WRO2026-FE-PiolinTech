# Piolín Tech — Autonomous Vehicle Project

Welcome to the official repository of **Piolín Tech**. This open-source repository archives the complete mechatronic development, low-level software engineering, discrete control laws, and physical testing profiles of **Piolín**: our high-performance autonomous vehicle engineered explicitly to master the strict regulations of the **World Robot Olympiad (WRO) Future Engineers** competition. 

Our engineering framework prioritizes reproducibility, real-time execution, and high-velocity kinematic efficiency.

---

##  Deeper into our Project Overview & System Mission

The ultimate objective of the **Piolín** project is to design a fully self-driving, scale vehicle capable of parsing complex spatial environments and executing real-time trajectory adjustments under varying track dynamics. The platform bridges the gap between structured mechanical hardware and reactive, asynchronous code. Rather than relying on rigid, pre-programmed path sequences, Piolín perceives its environment dynamically and recalculates its actuation metrics while moving. Our main mission is to win :)

### Core Competition Objectives

The vehicle’s software architecture and mechanical hardware are engineered to excel across two distinct, highly demanding operational states:

1.  **The Open Challenge (Round 1 Trajectory Optimization):**
    The priority during this phase is the absolute minimization of lap times. The vehicle must break static inertia cleanly, establish continuous-time closed-loop lane tracking, and complete a precise 3-lap run. To maximize speed, the vehicle utilizes a discrete Proportional-Integral-Derivative (PID) control algorithm that continuously minimizes the spatial tracking error ($e_t$) relative to the track walls. This allows Piolín to calculate predictive racing lines, maintain high momentum through sharp corners, and execute a deterministic electromagnetic braking routine to stop instantly inside the designated regulatory spatial zone upon completing lap 3.
2.  **The Obstacle Challenge (Round 2 Dynamic Avoidance Matrix):**
    The complexity increases with the introduction of random, static obstacles along the track corridor. While the low-level PID line-tracking algorithm runs as the background process, it is instantly overridden by high-priority proximity interrupts. The vehicle must detect, classify, and safely bypass pillars based on color identification:
    * **Red Pillars (Pass-Left Constraint):** The software introduces a negative step offset into the baseline PID target reference, shifting the tracking center to the left margin of the lane.
    * **Green Pillars (Pass-Right Constraint):** The software executes the inverse routing matrix, shifting the control reference point to the right lane margin.
    The steering loop remains locked in these avoidance states until the lateral sensor arrays confirm that the vehicle's physical midpoint has cleared the obstacle coordinates, safely returning control to the primary lane-tracking loops.

---

## Key Technical Features & Mechatronic Breakdown

To achieve the reliability required for international judging, Piolín’s design was divided into four core mechatronic disciplines:

### 1. Hybrid Structural Architecture
The physical frame balances structural modularity with customized mechanical engineering. While the primary chassis, suspension mounts, and structural braces are built using high-grade LEGO Technic components to comply with modular rigidity requirements, commercial drivetrain components introduced unacceptable backlash. To solve this phase delay in our acceleration loops, we designed custom, mathematically matched **involute bevel gears** in Blender. Fabricated via FDM 3D printing using high-density PLA with a 60% gyroid infill pattern, this custom differential gearbox ensures a zero-slip, 1:1 torque-matching efficiency profile directly to the independent rear half-shafts.

### 2. True Ackermann Steering Geometry
To eliminate tire scrubbing, lateral sliding, and mechanical drag during transient cornering maneuvers, the front steering system incorporates a true **Ackermann Geometry Linkage**. The structural pivot joints ensure that when executing a turn of radius $R$, the inner steered wheel angles more sharply than the outer wheel. The kinematic relationship is defined by the classical equation:
$$\cot(\delta_{\text{outer}}) - \cot(\delta_{\text{inner}}) = \frac{w}{l}$$
Where $w$ represents the vehicle track width and $l$ represents the wheelbase length. This geometric alignment ensures a single, stable instantaneous center of rotation (ICR), maintaining predictable yaw rates and preserving kinetic energy through the track's sharpest curves.

### 3. Asynchronous Software State Machine
The vehicle's software environment is built inside a custom **Python MicroPython framework**, utilizing an asynchronous, non-blocking state machine model. This execution topology completely separates high-frequency sensor-polling tasks from primary motor actuation outputs. By isolating sensory acquisition threads from the core PID steering routines, we prevent code execution delays, flatten execution latency, and eliminate the risk of processor timing jitter affecting physical steering angles at high velocities.

### 4. Multi-Channel Sensory Allocation Matrix
Piolín interacts with its environment through an active, 3-channel distance mapping and computer vision matrix:
* **Dual Lateral Ultrasonic Transducers:** Mounted symmetrically on the front bumper profile at an offset angle of exactly $\theta = \pm 45^\circ$ relative to the longitudinal vector ($X$-axis). This specific orientation maximizes the spatial envelope mapping, eliminating blind spots along the vehicle's flanks and optimizing boundary-distance tracking ($d_{\text{lateral}}$).
* **Single Longitudinal Ultrasonic Transducer:** Positioned at the absolute geometric center of the front bumper along the $X$-axis. This sensor continuously monitors the forward distance vector ($d_{\text{forward}}$), feeding raw proximity telemetry directly into the state machine to trigger deterministic obstacle bypass routing matrices.
* **Elevated Vision Mast Subsystem:** An elevated camera structure mounted along the vehicle's central vertical axis, designed to capture clean color profiles of upcoming obstacle pillars without interference from chassis shadows or perspective distortion.

---
