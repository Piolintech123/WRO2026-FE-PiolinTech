# 3.0 Overview of Pin Configuration


The following table summarizes the primary pin assignments for all the components on the Raspberry Pi 5:

| Device Element | Host Controller Interface | Core System Purpose |
| :--- | :--- | :--- |
| **PixyCam 2.1** | Sensor Port 1 (I2C) | Real-time color signature & lane tracking |
| **Ultrasonic Sensor (Front)** | Sensor Port 2 | Obstacle avoidance & distance telemetry |
| **Ultrasonic Sensors (Side x2)** | Sensor Port 3 | Wall alignment & path correction |
| **LEGO Color Sensor** | Sensor Port 4 | Surface detection & track marker identification |
| **Rear L-Motors (x2)** | Motor Port A | Propulsion & linear acceleration |
| **Front Steering Motor** | Motor Port B | Ackermann steering actuation |
| **Gyro Sensor** | Internal / Port 2 | Heading & angular stability |

---

This technical overview details the current configuration of Piolín. We have made the strategic decision to prioritize the reliability and deterministic performance of the LEGO Mindstorms EV3 platform for this competition cycle. While the Raspberry Pi 5 remains a key component of our future development roadmap, this documentation focuses on our current, battle-tested EV3 architecture, which provides the stability and hardware integration required for the WRO 2026 Future Engineers competition.

## 3.1. Engineering Philosophy and Current Architecture

The design philosophy behind Piolín is centered on robust autonomy. By utilizing the LEGO Mindstorms EV3 platform, we have opted for an integrated, hardware-optimized system that eliminates the overhead and potential stability variables associated with external computer boards. The EV3 brick provides a highly deterministic environment. It is specifically designed for robotics, meaning the internal bus timings and motor feedback loops are synchronized at the factory level. For WRO competitions, where environmental variables like lighting and track texture can fluctuate, the EV3 offers a stable foundation that allows us to focus entirely on PID tuning and sensor fusion rather than troubleshooting operating system latencies. This iteration of the robot serves as the Version 1.0 benchmark: a reliable, consistent platform that we can trust to complete the track consistently, setting the stage for future upgrades to high-compute architectures.

## 3.2. Structural Integrity and Chassis Dynamics

The chassis of Piolín represents a hybrid engineering approach, combining the rapid-prototyping versatility of LEGO Technic with custom-fabricated 3D-printed components. We have moved away from stock LEGO configurations in favor of a rigid, cross-braced frame that minimizes chassis flex. Structural compliance, or the twisting of the frame during high-speed cornering, is the enemy of accurate steering. When the chassis twists, the geometry of the steering linkage changes, causing the front wheels to scrub against the track rather than rolling cleanly. To combat this, we have 3D-printed specialized bevel gears and modified chassis connectors that lock the front steering linkage in place. This ensures that when the steering motor commands an Ackermann angle, the wheels execute that command with zero mechanical slop. The stability of this chassis is the foundation upon which our entire software control loop relies. Because the physical robot responds predictably, our control algorithms can be fine-tuned to absolute precision.

## 3.3. The Computing Core: The LEGO EV3 Brick

At the heart of Piolín sits the LEGO EV3 Intelligent Brick. While the industry is trending toward micro-controllers like the Raspberry Pi, the EV3 remains an exceptionally powerful tool for WRO Future Engineers. Its greatest strength is its seamless integration with the motor drivers and sensor ports. Unlike a general-purpose computer that requires complex external H-bridges and voltage level-shifting, the EV3 includes built-in, industrial-grade motor drivers and dedicated sensor ports with built-in protection. This allows us to maintain a clean, compact footprint without the spaghetti wiring often seen in prototype robots. The EV3 internal operating system handles the timing of sensor inputs at a high frequency, ensuring that every time our PID loop requests a distance measurement or a vision frame, the hardware is ready to deliver. This deterministic timing is vital for maintaining high-speed tracking without the jitters often caused by unmanaged background processes on standard PC hardware.

## 3.4. Visual Navigation and PixyCam 2.1 Integration

Our vision system utilizes the PixyCam 2.1, which remains one of the most effective sensors for line-tracking and object identification. Connecting the PixyCam to the EV3 via the I2C protocol allows us to offload the image processing work entirely. The PixyCam does not stream raw video to the EV3; instead, it performs color signature recognition on its internal processor and sends only the relevant X and Y coordinate data to the EV3 brick. This architecture is efficient and keeps the EV3 processor focused on steering and speed control.

However, visual navigation is only as good as the light that reaches the sensor. We have addressed the challenges of venue glare by constructing a modular shroud around the PixyCam. This housing acts as a physical aperture, limiting the incoming light to the track surface and preventing overhead stage lights from washing out the color signatures. We treat vision as our long-range sensor. It provides the global plan for where the robot needs to be, while our ultrasonic array handles the short-range tactical decisions required for obstacle evasion.

## 3.5. Ultrasonic Telemetry and Sensor Fusion

The HC-SR04 ultrasonic array is the primary safety net for Piolín. We have implemented a three-sensor configuration that provides a 180-degree spatial awareness bubble. By mounting one sensor forward and two at roughly 45-degree angles to the flanks, we have effectively eliminated the cornering blind spots that often trip up simpler robots.

The integration of these sensors with the EV3 is managed through dedicated sensor ports. We use a custom-coded filtering algorithm to process this data. Because ultrasonic sensors can sometimes receive ghost echoes, or reflections from the floor or track seams, our software implements a moving-average filter. This ensures that the robot only reacts to consistent, verified obstacle proximity. This is a form of sensor fusion: the robot combines the long-range data from the PixyCam with the immediate tactical data from the ultrasonics. If the vision system says turn right, but the ultrasonic sensors detect an obstacle on the right flank, the robot will intelligently override the turn command to avoid a collision. This logic is baked into the control flow, ensuring that even if the vision system fails, the robot remains physically safe from crashing into track boundaries.

## 3.6. Power Distribution and Electrical Reliability

The electrical architecture of Piolín is designed for sustained performance over long competition days. By relying on the EV3 native power management, we avoid the complex buck-boost converter setups required by more power-hungry processors. We utilize high-capacity rechargeable power packs, and we have implemented a strict wire-management protocol to ensure that no cables are exposed to the mechanical stress of the moving steering linkage.

One of the key lessons we learned in our previous testing cycles is that loose connections are the leading cause of ghost software errors. As a result, all connections on Piolín are secured with strain-relief points. The path from the sensors to the EV3 ports is short, shielded, and vibration-proofed. We also monitor our battery levels closely. The EV3 provides real-time telemetry on voltage, allowing our control software to adjust PID tuning constants dynamically as the battery drains, ensuring the steering response remains identical at 100 percent charge and 20 percent charge.

## 3.7. Control Logic: PID Tuning and Ackermann Steering

The control loop is the mathematical heart of Piolín. We utilize a Proportional-Integral-Derivative (PID) loop to calculate the steering angle.

* Proportional (P): Acts as the immediate correction force. The further the robot is from the track center, the harder the steering servo turns to bring it back.
* Integral (I): This term accumulates the error over time. It is particularly useful on tracks with consistent, wide curves where the robot needs to hold a steering angle for an extended period.
* Derivative (D): This is the damping factor. It predicts the error by looking at how fast the robot is moving toward or away from the center line. It prevents the robot from overshooting the center, which results in the dreaded zig-zag oscillation often seen in poorly tuned robots.

Our implementation of this loop is optimized for the EV3 internal clock. We have tuned our coefficients specifically to account for the physical weight of the chassis and the torque of the steering motor. The result is a robot that tracks the center line with a smooth, fluid motion that consumes less energy and generates less mechanical wear than a robot making jerky, aggressive corrections.

## 3.8. Strategic Competition Preparedness

Our move away from the Raspberry Pi 5 for this competition is not a step backward. It is a strategic decision for reliability. In the WRO Future Engineers category, the best robot is the one that is most predictable. By using the EV3 platform, we are operating within a well-understood, highly reliable ecosystem. We have spent the last weeks not just writing code, but refining the robot performance. We tested it on different surfaces, verified sensor accuracy in various lighting conditions, and practiced race-start procedures.

When we eventually decide to migrate to the Raspberry Pi 5 architecture in the future, we will do so with a solid foundation. We will take all the PID tuning data, the sensor filtering algorithms, and the chassis design lessons we have learned with the EV3 and port them over to the more powerful platform. For now, our goal is to master the track with the current hardware. Piolín is now a machine of precision, built for stability, and ready to navigate the WRO 2026 track with speed and confidence. Every line of code and every 3D-printed part has been validated, and we are prepared for the challenges of the competition environment.

