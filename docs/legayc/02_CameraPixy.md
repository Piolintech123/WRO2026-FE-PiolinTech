# 5. PixyCam 2.1 Vision Engine
## 5.1  Technical Analysis

The PixyCam 2.1 functions as a dedicated vision coprocessor rather than a traditional camera, which is a critical distinction for high performance robotics. By utilizing an onboard NXP LPC4330 processor, it offloads computationally expensive image processing tasks from the primary EV3 controller. This architecture is essential for maintaining the real time responsiveness required for competition grade robotics, as it ensures the primary processor is not overwhelmed by video data.

The PixyCam operates using a Color Connected Components (CCC) algorithm, which prioritizes object detection speed over raw image fidelity. The sensor converts raw RGB values into the HSV color space, which decouples color information from lighting intensity. This makes the system significantly more robust against the variable lighting conditions typically found in competition venues. The algorithm groups adjacent pixels of the same signature into clusters, assigning a bounding box to each. Instead of streaming raw video, the PixyCam transmits only the coordinates of these boxes to the EV3, ensuring that the main control loop remains lightweight and high frequency.

We selected this sensor because it enables semantic navigation. Unlike basic line followers that rely on binary transitions, the PixyCam allows Piolín to distinguish between different colored track markers and features. This allows the robot to perform complex maneuvers based on the identity of an object, not just its location. The sensor is calibrated to output the center coordinates of detected blocks, which are then used to calculate the steering error. If $X_{target}$ is the horizontal center of the camera frame and $X_{detected}$ is the center of the largest detected signature, the horizontal steering error $e(t)$ is calculated as $e(t) = X_{target} - X_{detected}$. This error signal is the foundation of our entire navigational strategy.

<img width="399" height="367" alt="image" src="https://github.com/user-attachments/assets/fbc13369-75e1-466d-a10b-e170476c5e9d" />

## 5.2 Structural Integrity and Chassis Dynamics

The chassis of Piolín is a hybrid construction that merges the versatility of LEGO Technic components with custom 3D printed structural reinforcements. We have prioritized a rigid frame design to minimize chassis flex. When the robot turns at high velocity, structural compliance can cause the front wheels to lose their intended Ackermann geometry, leading to speed loss and path deviation. We addressed specific component identification errors in previous iterations. We verified that a critical structural piece possesses three holes, specifically two horizontal and one vertical, which is essential for maintaining the rigidity of our chassis.

By moving toward custom 3D printed bevel gears and modified chassis components, we have successfully minimized chassis flex, which was a primary cause of steering inaccuracy in early prototypes. The front steering assembly relies on a precise linkage system that ensures correct Ackermann geometry, minimizing tire scrub and improving traction during high speed maneuvers. This structural stability is the foundation upon which our entire software control loop relies, as the physical robot must respond predictably for the control algorithms to be fine-tuned to absolute precision.

## 5.3 The Computing Core and Electrical Architecture

The Piolín robot utilizes the LEGO EV3 Intelligent Brick, which provides a highly deterministic environment for robotics control. This is a strategic choice for the WRO 2026 Future Engineers category, as it eliminates the potential inconsistencies found in less integrated or non-dedicated hardware environments.

It is vital to note that for the current competition configuration, no SD card is connected to the EV3, and we rely on the internal brick memory for operational stability. We have established a precise motor configuration, and we have corrected previous errors regarding motor pin mapping. The motors operate using $ain1$ and $ain2$ pins, rather than the previously tested $bin1$ and $bin2$ configuration, to ensure correct directionality and torque delivery.

We avoid ground loops by routing all component grounds to a centralized point, ensuring signal integrity across the entire sensor array. The electrical architecture is designed for sustained performance over long competition days. We utilize high capacity rechargeable batteries, and we have implemented a strict wire management protocol to ensure that no cables are exposed to the mechanical stress of the moving steering linkage. All electrical connections are secured using strain relief points to prevent accidental disconnections caused by mechanical vibration.

## 5.4 Control Logic and Mathematical Models

The steering behavior is governed by a Proportional-Integral-Derivative (PID) algorithm implemented on the EV3. The PID controller is the mathematical engine that turns steering error into steering action. The steering actuation $u(t)$ is calculated as $u(t) = K_p e(t) + K_i \int_{0}^{t} e(\tau) d\tau + K_d \frac{de(t)}{dt}$. In this formula, the proportional gain $K_p$ provides the immediate corrective force to return the robot to the center, the integral gain $K_i$ corrects accumulated error over time, particularly useful on tracks with consistent curves, and the derivative gain $K_d$ acts as a damping factor to prevent oscillation.

The robot must also calculate the appropriate steering angle $\delta$ for a given turn radius $R$ and wheelbase $L$ to ensure smooth cornering. This is calculated using the formula $\delta = \arctan\left(\frac{L}{R}\right)$. This geometric calculation ensures that the steering servo angle is proportional to the required turn, maintaining the vehicle on the intended path.

We also integrate data from an ultrasonic array to supplement our vision system. The distance $d$ for these sensors is derived from the time of flight $t$ and the speed of sound $v$ using the formula $d = \frac{t \cdot v}{2}$. This sensor fusion allows the robot to perform evasive maneuvers without needing to see the track line constantly, providing a safety net in cases where the visual system might fail or be temporarily obscured.

## 5.5 Strategic Competition Preparedness

The Piolín platform is engineered for predictability and reliability, which are the cornerstones of success in the WRO Future Engineers category. The robot is validated through multiple test runs on varying surfaces to ensure sensor consistency, and all mechanical and electrical subsystems are subjected to a pre-run checklist to ensure no loose connections or structural misalignments exist.

While our current architecture utilizes the EV3 platform, we maintain a development roadmap for migrating to more advanced computing architectures in the future. This roadmap ensures that our codebase, including PID tuning data and sensor filtering algorithms, remains modular and portable. We have documented our historical failures, including previous camera and hardware misidentifications, to ensure that the current system is optimized for stability and speed. Every component, from the specific 3 hole Technic pieces to the sophisticated PID control algorithms, has been analyzed and integrated to form a cohesive, high performance machine prepared to navigate the competition track with precision and resilience.

