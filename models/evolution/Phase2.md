## 1.2 Prototype Phase 1.5: The 1st Regional Competitor (Our Second Model)

Developed and optimized specifically for our first regional competition, this intermediate iteration represented a focused effort to push the limits of the LEGO Technic and MINDSTORMS EV3 ecosystem. This model was engineered to increase physical rigidity, introduce multi-sensor data input, and resolve critical telemetry dropouts under actual live tournament track conditions.

<div align="center">
  <img src="https://github.com/user-attachments/assets/1c69496e-6b70-4709-8284-e27ac4f175b2" alt="Prototype Phase 1.5" width="450"/>
  <p><em>Prototype Phase 1.5 featuring reinforced dual-layer structural bracing, a multi-sensor front bumper, and manually secured cable connections.</em></p>
</div>

### 1.2.1 Architectural Specifications and Upgrades

*   **Primary Controller & Operating System:** The core remained the LEGO MINDSTORMS EV3 Intelligent Brick running a custom *ev3dev Linux* kernel. Programs were executed using Python and MicroPython scripts to handle non-blocking sensor polling loops.
*   **Chassis Reinforcement & Mechanical Bracing:** We completely redesigned the upper horizontal frame. Replacing the colored, multi-jointed LEGO Technic pieces from Phase 1.0, we utilized high-density white and grey structural beams to build a dual-layer, cross-braced overhead bridge. This significantly reduced lateral twisting of the high-rise motor mounts.
*   **Sensor Array Expansion:** To begin testing dual-input path-finding and boundary detection, we constructed an expanded front-bumper assembly. We integrated an EV3 Color/Light Sensor alongside the primary dual-receiver ultrasonic transducer, allowing the robot to actively detect floor markers while simultaneously scanning for physical obstacles.
*   **Physical Connection Hardening:** High-frequency track vibration during initial trials frequently loosened the standard RJ12 connector clips inside the EV3 ports. To prevent runtime failures, we implemented manual tape-reinforcement on critical ports (specifically Port 4) to physically secure the telemetry lines to the brick.
*   **Power & Drive System:** The platform utilized a heavy rear-mounted EV3 motor configuration paired with high-grip rubber tires, attempting to maximize mechanical traction over the track surface while distributing the weight of the central EV3 brick.

---

### 1.2.2 Engineering Lessons & Regional Tournament Bottlenecks

While this model successfully completed its runs and proved to be far more durable than its predecessor during the regional tournament, the stress of competition highlighted severe limits inherent to the educational hardware platform:

1.  **Pin-Joint Backlash and Mechanical Play:** Despite the reinforced dual-beam white bridge, the entire chassis relied on friction-based plastic snap-pins. Under rapid steering corrections and acceleration, these pin-joints experienced microscopic shifting (backlash). This structural flex resulted in a persistent, cumulative steering drift of up to $\pm 5\text{ cm}$ per meter, which could not be corrected via software.
2.  **Telemetry and Port Vulnerability:** The necessity of physically taping the sensor cables demonstrated that standard consumer-grade RJ12 telephone-style clips are fundamentally unsuited for high-vibration robotic environments. A single loose clip could trigger an instantaneous system crash or loop freeze, steering us toward the absolute requirement of locking headers (like DuPont or JST) and direct-soldered wire joints in future models.
3.  **Severe Processing Jitter and Thread Lag:** Adding the color sensor to the execution loop pushed the EV3's ARM9 300 MHz processor to its computational limit. The overhead of reading both the analog color registers and parsing the ultrasonic distance pulses in Python caused the main program loop to experience timing jitter. This control lag meant the vehicle would occasionally "overshoot" its turning points on the track because the processor was busy executing previous sensor calculations.
4.  **Inefficient Weight Distribution (High CoG):** Stacking the heavy EV3 Intelligent Brick vertically above the drive wheels created an elevated Center of Gravity (CoG). During sharp, regional-level speed turns, this caused significant body roll, reducing tire contact pressure on the inner wheels and causing slipping that corrupted our wheel encoder calculations.

