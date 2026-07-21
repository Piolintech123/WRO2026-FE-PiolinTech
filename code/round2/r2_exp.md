# Code for Round 2 Overview & Explanation

The software architecture for the Round 2 obstacle challenge is engineered around a four-phase state machine that integrates real-time computer vision with low-level chassis telemetry. Compared to the basic wall-following requirements of the first round, this round forces the system to continuously balance wall distance metrics against dynamic obstacle avoidance vectors. This strict isolation of execution states prevents the vehicle from attempting conflicting maneuvers when an obstacle appears directly inside its preferred wall-tracking path.

The initial phase manages dynamic sensor calibration and vision matrix initialization. Prior to movement, the microcontroller resets all drive motor encoders, zeroes the steering rack, and initializes the camera sensor with pre-calibrated color threshold profiles. This step ensures that ambient arena lighting does not corrupt the vision processing pipeline, establishing a reliable color signature baseline for red and green obstacle detection before the vehicle begins its acceleration.

The second operational phase executes real-time vision processing and trajectory planning. As the vehicle moves along the track, the vision sensor scans for color signatures at sixty frames per second. Upon detecting a pillar, the algorithm calculates the bounding box area and centroid location to estimate relative distance and position. If a red signature is detected, the trajectory planner generates a right-hand bypass vector. If a green signature is identified, the planner calculates a left-hand bypass vector. This spatial filtering ensures the robot strictly adheres to competition regulations while keeping the vehicle within safe track boundaries.

The third phase manages hybrid wall-tracking and obstacle evasion. During clear stretches of the track, the robot relies on ultrasonic distance sensors to maintain a consistent offset along the wall. However, as soon as an obstacle passes a proximity threshold in the vision feed, the steering logic temporarily suppresses the wall-following loop. The controller smoothly blends the wall distance error with the camera-based evasion angle, executing an arc that clears the pillar without losing overall track orientation or causing erratic wheel slip.

The final phase controls spatial odometry, lap validation, and automated precision parking. Rather than relying on simple vision triggers that can be spoofed by background reflections, the architecture combines camera data with wheel encoder counts to verify lap progression. Once three full circuits are completed, the state machine transitions into the parking routine. The robot actively scans for the designated finish bay, utilizes ultrasonic distance sensors to measure enclosure depth, and executes a controlled deceleration sequence to come to a complete stop within the marked zone.

### Vision-Driven Steering & Bounding Box Filtering

The steering correction during an obstacle evasion maneuver is calculated using the relative offset of the detected bounding box centroid combined with the specific color signature rule.

```python
def calculate_obstacle_steering(block, frame_center_x=158, max_steering_limit=45):
    signature_bias = 1 if block.signature == 1 else -1
    required_clearance = (block.width // 2) + 35
    target_x = block.x + (signature_bias * required_clearance)
    
    error_x = target_x - frame_center_x
    steering_angle = clamp(error_x * 0.35, -max_steering_limit, max_steering_limit)
    
    return steering_angle

```

The calculate obstacle steering function translates visual metadata into a precise angular command for the steering motor. The signature bias variable inspects the detected color ID. For red obstacles, a positive multiplier shifts the target waypoint to the right side of the block. For green obstacles, a negative multiplier shifts the waypoint to the left side of the block.

The algorithm adds a safety margin to half of the detected bounding box width, creating a dynamic clearance offset that adapts as the obstacle grows larger in the camera frame. The raw horizontal error is multiplied by a proportional gain constant and passed through a clamping function. This clamping prevents the steering rack from over-rotating beyond its physical mechanical stops, ensuring smooth, predictable evasion curves even when obstacles appear near the edge of the lens field of view.

### Advanced Stability Analysis

To achieve maximum reliability and speed during the Round 2 obstacle challenge, developers should consider several key structural upgrades to the visual and mechanical control loops.

1. **Dynamic Velocity Profiling:** High vehicle speeds during evasive turns often cause lateral tire scrub and motion blur in the camera sensor. Implementing speed profiling allows the main controller to scale down motor power proportionally as the required steering angle increases. Slowing down slightly during sharp evasive maneuvers stabilizes the image feed, reduces mechanical strain on the steering linkage, and ensures maximum tire traction when re-entering the wall-tracking phase.
2. **State Machine Resilience via Optical Odometry Fusion:** Visual occlusion can occur when an obstacle briefly blocks the camera from seeing distant wall markers or upcoming turns. By fusing optical flow or wheel encoder data into a local position estimation matrix, the robot maintains a short-term memory of the track layout. If a frame drop or lighting flicker causes the camera to briefly lose sight of a pillar, the vehicle continues along its calculated arc rather than making sharp, erratic steering adjustments.
3. **Telemetry Logging for Vision Gain Tuning:** Fine-tuning the balance between the visual proportional gain and the ultrasonic wall-following gain requires empirical test data. Writing frame execution latency, bounding box dimensions, calculated steering angles, and raw ultrasonic readings to an onboard log file allows developers to identify system bottlenecks. Analyzing these logs reveals whether steering instability stems from camera latency, incorrect HSV color thresholds, or overly aggressive proportional gains in the control loop.

This integrated architectural framework provides a robust foundation for navigating complex obstacle layouts. By combining real-time visual categorization with physical clamping, spatial odometry, and adaptive trajectory planning, the robot achieves high-speed precision while remaining resilient against physical environmental variations.
