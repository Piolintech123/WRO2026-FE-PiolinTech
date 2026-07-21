# Performance Testing and Analytics
---

## Vision Subsystem Statistical Validation

To calculate the tracking error rates of our primary visual tracking engines under varying environmental conditions, we ran continuous benchmark tracking loops across 5,000 operational frames.

### 10.1.1 Error Rate Mathematical Formulation
The raw frame tracking error rate ($E_{\text{vision}}$) is calculated using the following formula:

$$E_{\text{vision}} = \left( \frac{F_{\text{dropped}} + F_{\text{false-positive}}}{F_{\text{total}}} \right) \times 100$$

Where:
*   $F_{\text{dropped}}$: Frames where a valid track line or target obstacle was present but the sensor failed to output coordinate bounding boxes.
*   $F_{\text{false-positive}}$: Frames where background glare or track artifacts caused false target detections.
*   $F_{\text{total}}$: Total frame count in the test run ($5,000$ frames).

  
### Benchmark Data under Variable Conditions

The table below shows performance data across different testing environments, comparing our legacy configuration against our current machine-learning architecture:

| Environment Profile | Lux Level | Legacy PixyCam 2.1 Error Rate | Current Huskylens Error Rate |
| :--- | :--- | :--- | :--- |
| **Standard Ambient (Lab)** | 450 lx | 4.2% | 0.8% |
| **High Overhead Glare** | 1,200 lx | 14.8% | 2.1% |
| **Low-Contrast Shadowing** | 150 lx | 18.5% | 2.9% |
| **Composite Track Mean** | **-** | **12.5%** | **1.93%** |

---

## Spatial Sensing and Ranging Reliability

The triple-staggered ultrasonic array was benchmarked against calibrated hardware physical baselines to evaluate noise distribution and response curves.


```

              [Left Sensor]       [Center Sensor]      [Right Sensor]
                 (GPIO15)            (GPIO17)             (GPIO23)
                    ╲                   │                    ╱
                     ╲                  │                   ╱


180° Coverage Sweep:    ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

```

### Data Filtering and Noise Rejection
Raw distance pulses are subjected to an inline low-pass median filter running on a dedicated background execution thread. The filter discards any outlier data points ($D_n$) that deviate from the running array median ($M$) by a threshold variant:

$$\Delta D = |D_n - M| > 5\text{ cm}$$

Discarded data points are dropped from the navigation matrix to prevent sudden, erratic steering corrections.

### Ranging Accuracy Profile

| True Physical Distance | Raw Sensor Mean Output | Filtered Output Mean | Standard Deviation ($\sigma$) |
| :--- | :--- | :--- | :--- |
| **5.0 cm** | 5.2 cm | 5.02 cm | 0.08 cm |
| **15.0 cm** | 15.6 cm | 15.04 cm | 0.12 cm |
| **30.0 cm** | 31.2 cm | 30.11 cm | 0.24 cm |
| **50.0 cm** | 52.8 cm | 50.29 cm | 0.45 cm |

---

## Kinematic Control Loop Analysis (PID)

Steering actuation adjustments are managed via a dedicated proportional-integral-derivative (PID) tracking loop that targets the visual center line ($X_{\text{target}} = 160$) provided by the Huskylens I2C packet stream.

### Control Equation

$$u(t) = K_p e(t) + K_i \int_{0}^{t} e(\tau) d\tau + K_d \frac{de(t)}{dt}$$

Where the tracking error is defined as:

$$e(t) = X_{\text{target}} - X_{\text{measured}}$$

### Loop Optimization Impact
The migration of the steering servo signal away from software-based timing maps to the Raspberry Pi 5’s dedicated `PWM0` hardware clock channel (GPIO 15) represents a critical advancement in our system’s deterministic performance. By anchoring the signal directly to the internal hardware clock, we have successfully eliminated the overhead associated with software-defined timing, resulting in a dramatic reduction in data propagation latency from an initial $18\text{ ms}$ down to a refined $1.2\text{ ms}$.

This hardware-level assignment effectively decouples the steering actuation from the heavy multi-threaded CPU load inherent in our image processing pipeline. By removing the dependency on fluctuating software cycles, the steering loop maintains a level of precision that was previously unattainable, ensuring that the actuator receives consistent, high-fidelity signals regardless of the intensity of the concurrent computational tasks being performed by the central processor.

The cumulative result of these modifications is an exceptionally stable steering response that demonstrates superior damping characteristics. Our empirical testing shows that this architectural shift successfully suppresses transient overshoot, allowing the vehicle to damp all oscillation cycles to zero within $220\text{ ms}$ during aggressive lane recovery maneuvers. This ensures that the robot maintains its trajectory integrity even under the most demanding dynamic conditions on the competition track.

