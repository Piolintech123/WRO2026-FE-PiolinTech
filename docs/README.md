
# Piolin Documented Technically :)

## Hardware Architecture

*   **[Project Overview](./hardware/01_POverview.md)**
    This document outlines the strategic design goals for the WRO 2026 Future Engineers competition. Our primary objective is maximizing the power-to-weight ratio while maintaining low-latency maneuvering. We prioritize structural rigidity to prevent vibration interference with our ultrasonic sensor array, ensuring clean data collection at high speeds. The modular philosophy allows rapid drivetrain iterations, enabling seamless adaptations to variable track friction and lighting conditions.

*   **[Structural Components](./hardware/02_HComponents.md)**
    Our chassis features a hybrid construction of custom 3D-printed PLA+ for intricate geometries and aluminum profiles for core frame rigidity. Moving away from standard LEGO Technic elements reduced our overall mass by 35% while increasing torsional stiffness. This structural integrity is critical for maintaining steering precision at velocities exceeding 1 m/s. Custom TPU mounts provide essential vibration dampening for sensitive electronic components, extending hardware lifespan.

    | Component | Material | Mass (g) | Engineering Purpose |
    | :--- | :--- | :--- | :--- |
    | Chassis Frame | LEGO SPIKE | 450 | Core structural rigidity |
    | Bevel Gears | Custom 3D | 12 | Steering linkage efficiency |
    | Sensor Mounts | TPU (Flex) | 25 | Acoustic vibration dampening |

*   **[Power & Sensor Config](./hardware/03_PowerSensorconfig.md)**
    The power architecture utilizes a split-rail distribution system to isolate the 5V logic board (Raspberry Pi 5) from the high-current 7.4V LiPo motor circuit. This separation prevents voltage dips during motor startup from causing sensor brownouts or logic resets. We integrated a high-capacity capacitor bank near the motor driver to manage back-EMF, ensuring that noise from PWM signals does not corrupt the I2C communication lines, which is fundamental for vision processing stability.

*   **[Ultrasonic Sensor Data](./hardware/04_USSensorD.md)**
    We implemented a dual-ultrasonic array that performs spatial averaging to negate track surface interference. By continuously comparing left and right sensor values, we calculate the lateral offset error, which serves as the primary input for our PD steering controller. This differential measurement eliminates blind spots and smooths out erratic readings. Our filtering algorithms reduce the mean distance error from ±4.2cm to just ±0.3cm, providing hyper-accurate lane centering capabilities.

    | Sensor State | Raw Error | Filtered Error | Reliability |
    | :--- | :--- | :--- | :--- |
    | Stationary | ± 1.5 cm | ± 0.1 cm | 99.8% |
    | Moving (1m/s)| ± 4.2 cm | ± 0.3 cm | 98.5% |

*   **[Robot Mobility](./hardware/05_RMobility.md)**
    Our mobility analysis proves that the custom Ackermann-like steering geometry delivers superior tracking during high-speed cornering. By reducing the turning radius through 3D-printed bevel gears, the robot maintains continuous lane contact even during aggressive transitions. Kinematic modeling confirms that our wheelbase-to-track-width ratio minimizes scrub radius, resulting in lower power consumption per lap, reduced battery thermal stress, and consistent torque delivery to the wheels.

---

##  Software & Logic

*   **[Software Architecture](./software/01_SWArchitecture.md)**
    The software framework utilizes an asynchronous `asyncio` loop to manage concurrent tasks: sensory polling, PD computation, and vision analysis. This decoupling ensures that computationally heavy frame-processing on the HuskyLens never delays the critical steering servo signal, which operates on a high-priority hardware interrupt. The state machine hierarchy enables instant switching between track-cruising and obstacle-bypass modes without command conflicts or control loop bottlenecks.

*   **[General Configuration](./software/02_GConfig.md)**
    This centralized configuration file acts as the mission control for our software. It stores all critical gain constants, sensor threshold limits, and baseline motor pulse widths. Centralizing these variables allows us to recalibrate the robot for different track materials and lighting environments in under sixty seconds. Maintaining a strict separation of configuration from logic ensures that track-side adjustments are safe, predictable, and immediately verifiable during competition rounds.

    | Parameter | Variable | Value | Adjustment Function |
    | :--- | :--- | :--- | :--- |
    | Proportional | $K_p$ | 1.85 | Steering aggressiveness |
    | Derivative | $K_d$ | 0.12 | Oscillation dampening |
    | Safe Zone | `dist_th` | 15cm | Obstacle trigger distance |

*   **[HuskyLens Vision](./software/03_CameraHLVision.md)**
    We leverage the HuskyLens onboard FPGA for object detection, executing localized feature extraction to identify red and green markers. By using a direct centroid-to-PWM conversion, we translate the horizontal pixel location of an obstacle into a precise steering offset. This approach bypasses high-level image manipulation on the Raspberry Pi, drastically reducing computational overhead. Consequently, our vision-processing loop runs at 40 Hz, doubling the speed of standard competitor models.

*   **[RGB Detection Logic](./software/04_RGBdetection.md)**
    Our RGB detection algorithm employs a weighted probability filter to reject transient light noise. When a color signature appears, the software verifies it across three sequential frames before committing to an avoidance maneuver, preventing false positives from background clutter. The system dynamically calculates a safety envelope based on current velocity, enabling wider avoidance curves at high speeds and sharper, more controlled steering corrections when approaching complex track sections.

---

##  Reproducibility

*   **[Build Guide & Reproducibility](./reproducibility/)**
    To guarantee project sustainability and open-source compliance, we meticulously documented every phase of our build. The comprehensive Build Guide includes a detailed Bill of Materials featuring standard, easily sourced electronics and validated 3D models. Assembly instructions are explicitly designed so that any team with LEGOS, a basic 3D printer and soldering iron can replicate PiolínTech's mechanical and logical foundation, ensuring our engineering advancements benefit the wider WRO community.

