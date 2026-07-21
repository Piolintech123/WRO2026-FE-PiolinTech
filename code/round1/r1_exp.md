
# Code for Round 1 Overview & Explanation

The system is organized into four distinct operational phases, each optimized for specific track conditions. This modularity prevents the CPU from performing conflicting calculations and ensures that steering logic remains predictable.

* **Initialization and Calibration:** The script begins by normalizing the motor encoders to establish a zero-point for the steering rack. This is critical for maintaining consistency in the Proportional control loop.
* **Dynamic Centering:** The robot utilizes a non-linear alignment algorithm during the initial launch. By applying a square root transformation to the ultrasonic distance data, the robot achieves a smooth, logarithmic response curve. This prevents the violent steering jerks typically observed in robots that use simple linear subtraction, allowing the vehicle to accelerate at full power without breaking traction.
* **Asymmetric Proportional Cruising:** Upon identifying the track direction via color markers, the robot switches to a single-wall tracking mode. By focusing exclusively on the internal wall at a fixed distance, the robot traces a mathematically optimized racing line, effectively ignoring the sensor noise and varying track widths common in competition environments.
* **Spatial Odometry:** Rather than relying on unreliable time-based delays to count laps, the architecture employs spatial debouncing. The system monitors drive motor encoder values, requiring a specific distance of travel before acknowledging a new line. This renders the lap-counting logic immune to battery voltage drops or mechanical friction.

### Proportional Control Implementation

The steering logic is governed by a Proportional controller, which calculates the error between the current distance to the wall and the target offset.

```python
def amotor(degrese, cl=50):
    diff = degrese - motor_a.position
    diff = clamp(diff, -cl, cl)
    motor_a.on(diff)

```

The amotor function acts as the bridge between software logic and hardware movement. It calculates the error and translates it into a motor command. The clamp function acts as a critical safety barrier, restricting steering output to the mechanical limits of the chassis. This prevents motor stall and potential hardware damage in edge cases where sensor data might be erratic.

### Advanced Stability Analysis

For teams looking to optimize this architecture, the integration of a Derivative term, moving toward a PD control model, is the recommended path for higher performance.

1. **Dampening Oscillation:** A Derivative component measures the rate of change in distance to the wall. If the robot approaches the wall too rapidly, the derivative component applies a preemptive counter-steer, effectively braking the steering input to prevent the robot from overshooting the racing line.
2. **Robustness via Sensor Fusion:** By transitioning from single-sensor wall tracking to a center-weighted model, developers can create redundant navigation paths. If one ultrasonic sensor returns noise, the system can dynamically balance the error calculation across both sensors, ensuring the robot maintains its heading even under suboptimal environmental conditions.
3. **Performance Logging:** The implementation of data logging, writing sensor and error values to a file during test runs, allows for empirical tuning of the Proportional Gain. Analyzing these logs reveals if the robot is hunting for the center, meaning the gain is too high, or failing to correct aggressively enough, meaning the gain is too low.

This architectural framework provides a highly deterministic foundation for competitive robotics. By prioritizing modular state management, spatial accuracy, and hardware-aware control loops, the system achieves a level of precision that is resilient to the external variables typically encountered on a racing circuit.

