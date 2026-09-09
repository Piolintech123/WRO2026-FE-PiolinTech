## Project History & Timeline

PiolínTech's development journey began in **June 2025**. From the beginning, the project was shaped by continuous experimentation, mechanical redesigns, hardware setbacks, competition constraints, and repeated testing. The robot that exists today was not the result of one successful build, but of many prototypes that exposed different weaknesses and forced us to reconsider how the mechanical, electrical, sensing, and software systems should work together.

Throughout the development process, several designs were replaced because they were mechanically unstable, too slow, unreliable, difficult to integrate, or simply incompatible with the competition requirements. Rather than hiding those unsuccessful attempts, we consider them an important part of the project because each one contributed information that directly influenced the next version of the robot.

---

### June 2025 — The Beginning

Our journey began in June 2025 with the first experimental vehicle that would eventually lead to Piolín. At this stage, our objective was not yet to create a complete WRO Future Engineers robot. We were primarily trying to understand basic autonomous vehicle behavior: how the chassis responded to acceleration, how steering commands translated into physical motion, how much structural rigidity was necessary, and how sensors could be incorporated into the robot without interfering with its mechanical movement.

The first prototype allowed us to begin connecting software decisions with real physical consequences. We quickly learned that a command that appears simple in code does not necessarily produce a repeatable trajectory. Wheel alignment, structural flex, motor placement, weight distribution, and the starting position of the vehicle all affected how the robot behaved. This first stage established one of the most important ideas that would remain throughout the project: mechanical design and autonomous control could not be developed independently.

<p align="center">
  <img src="https://github.com/user-attachments/assets/e8f6a7bf-9663-4bfb-8b8d-1fb598d62b1d" width="200">
</p>

Although this early robot was far from the architecture used today, it provided the first useful platform for understanding the problems involved in building an autonomous vehicle for WRO Future Engineers.

---

### July 2025 — The Yahboom Hardware Failure

In July 2025, the project experienced one of its most serious early setbacks when the Yahboom kit we were using suffered a major hardware failure and caught fire. Development immediately stopped because the platform could no longer be used safely, and the incident forced us to reconsider the reliability of the hardware on which the robot depended.

<p align="center">
  <img src="https://github.com/user-attachments/assets/c2c7ec54-d42e-4f9c-9a4a-a2b69047f0b2" width="200">
</p>

Until that moment, most of our attention had been focused on whether a component could perform the task we wanted. After the failure, we began evaluating hardware differently. Reliability, electrical stability, wiring complexity, replacement availability, and the number of possible failure points became important engineering criteria alongside performance.

This event also changed our attitude toward unnecessary hardware complexity. A component could offer additional capability, but if it introduced fragile wiring, difficult communication interfaces, or additional power requirements, those disadvantages also had to be considered. The July failure therefore became an important influence on our later preference for a more integrated and easier-to-debug architecture.

---

### August 2025 — The “Against Rules” Prototype

After losing the previous platform, we needed a simple robot that would allow us to continue testing movement and control ideas. During August, we developed an experimental vehicle using one motor, two wheels, and a spherical support. Mechanically, the prototype was useful and allowed us to continue experimenting with autonomous motion, but the configuration did not comply with the WRO Future Engineers regulations.

<p align="center">
  <img src="https://github.com/user-attachments/assets/c0980ce3-dff4-45dd-8280-052b609c39e0" width="200">
</p>

This prototype taught us a lesson that was just as important as any mechanical or software improvement: a robot can function very well from a technical perspective and still be the wrong solution for the competition. From this stage onward, the competition rules became engineering constraints that had to be considered from the beginning of the design process rather than checked only after the robot was finished.

The experience forced us to evaluate future concepts not only by asking whether they worked, but also whether they respected the required vehicle architecture, whether they could pass inspection, and whether the design could remain legal after later modifications. The prototype itself did not continue into the competition architecture, but the lesson about designing within constraints became permanent.

---

### Late 2025 — The “Forbidden” V1

Later in 2025, we developed a considerably more complete and mechanically stronger design that we internally called the **“Forbidden” V1**. Compared with the previous prototypes, it represented a major improvement in structural stability and vehicle behavior. However, testing exposed a different limitation: the robot was simply too slow.

<p align="center">
  <img src="https://github.com/user-attachments/assets/b472c9dc-02f2-445b-b1bf-cff487a16ce0" width="200">
</p>

This version showed us that reliability alone was not enough. A robot can be stable and predictable but still be unsuitable for competition if its navigation strategy leaves too little performance margin. At the same time, simply increasing the speed was not a sufficient solution because higher velocity changed the entire control problem. Faster movement gave the robot less time to correct errors, increased the distance traveled between control updates, and made poor steering decisions much more difficult to recover from.

As a result, we started paying much more attention to the relationship between speed, steering geometry, correction timing, sensor placement, and the physical trajectory of the vehicle. Rather than thinking of speed as an independent parameter, we began treating it as part of the complete navigation system.

---

### End of 2025 — Nationals and Americas

By the end of 2025, repeated redesigns and testing had allowed us to progress far enough to compete at the **WRO Nationals and the Americas stage**. These events became an important turning point because they exposed our robot to conditions that could not be reproduced perfectly during normal development.

<p align="center">
  <img src="https://github.com/user-attachments/assets/b02d076a-0c1f-44d6-8297-e713f1c7f70d" width="200">
</p>

Competition introduced differences in lighting, track conditions, starting position, time pressure, mechanical wear, and calibration opportunities. More importantly, it taught us that a robot completing one successful run was not enough. Competitive reliability required the same behavior to be reproduced repeatedly despite small changes in the environment.

This changed the questions we asked during testing. Instead of stopping after a successful attempt, we began asking why the attempt had worked, whether the result could be repeated, what happened when the robot started slightly differently, and which subsystem was the first to become incorrect when a run failed. This was an important transition from simply building prototypes toward treating Piolín as a complete engineering system.

---

## 2026 — Development of Piolín

Entering 2026, our objective was to take the lessons from the previous year and consolidate them into a more coherent WRO Future Engineers platform. The LEGO MINDSTORMS EV3 remained the central controller of the project, while the mechanical design, steering system, sensor arrangement, perception strategy, and software architecture continued to evolve around it.

<p align="center">
  <img src="https://github.com/user-attachments/assets/812b7146-2706-4745-93e5-c2bc14222051" width="200">
</p>

The focus during 2026 shifted from simply adding capabilities toward assigning every component a clear responsibility. This became especially important after earlier experiments demonstrated that more sensors and more control logic did not automatically produce a more reliable robot. The challenge was to make the complete system easier to understand, calibrate, reproduce, and debug.

---

### Mechanical Development

The mechanical architecture evolved toward the current car-like configuration based on **rear propulsion and Ackermann-style front steering**. Motor A became responsible for propulsion, while Motor B became responsible for steering. Separating these roles allowed us to treat vehicle progression and steering curvature as two different control problems.

The chassis also went through repeated reinforcement and sensor-position changes. Instead of treating each LEGO assembly as an isolated structure, we increasingly considered how the complete geometry of the vehicle affected navigation. Steering linkage behavior, wheel alignment, sensor placement, cable routing, and the physical distribution of components all became part of the same design problem.

Custom 3D-printed components were later introduced where a LEGO-only structure could not provide the exact sensor environment we required. These included the Color Sensor casing and the Pixy2.1 casing, both of which became part of the current sensor installation rather than purely decorative additions.

---

### Sensor Architecture

One of the most important developments during 2026 was the simplification of the sensing architecture. Throughout earlier experimentation, we tested different sensor positions and combinations, but the final direction became much clearer once each sensor was assigned a specific role.

The current common architecture uses the **left ultrasonic sensor on S2**, the **right ultrasonic sensor on S3**, and the **downward-facing Color Sensor on S4**. These assignments remain physically constant regardless of the direction in which the vehicle travels.

S1 became round-specific. During the Open Challenge, S1 is used by the EV3 Gyro Sensor to provide information about heading and vehicle rotation. During the Obstacle Challenge, S1 is instead occupied by Pixy2.1, which provides visual information about colored pillars and the parking reference. The Gyro Sensor and Pixy2.1 are therefore not installed simultaneously in the current architecture.

This decision allowed us to avoid forcing every available sensor into one universal configuration. Instead, the robot uses the sensor that provides the most useful missing information for each competition round.

---

### Open Challenge Development

For the Open Challenge, the current sensor configuration separates lateral position, orientation, and course progress into different sources of information. The two ultrasonic sensors describe Piolín's lateral relationship with the track, while the gyro provides information about the direction in which the chassis is pointing and how much the robot has rotated.

The Color Sensor adds a third type of information by detecting the Blue and Orange floor markings. The first confirmed Blue marking indicates counterclockwise navigation, while the first confirmed Orange marking indicates clockwise navigation. Later detections are used as physical course landmarks rather than repeatedly redefining the direction.

This separation became particularly useful during corner development. Ultrasonic readings naturally change when the vehicle rotates because the sensors begin observing different wall geometry. The gyro provides independent rotational information that helps distinguish a normal lateral error from an actual corner maneuver.

---

### Obstacle Challenge Development

The Obstacle Challenge introduced a more difficult perception problem because Piolín needed to distinguish between Red and Green pillars rather than simply detecting that an object existed. Earlier experiments included HuskyLens and an Arduino Nano communication bridge, but those configurations introduced additional wiring, communication, and debugging complexity.

The current architecture uses **Pixy2.1 directly through S1** during the Obstacle Challenge. The camera is configured so that Pink corresponds to the parking reference, Red corresponds to a pillar that must be passed on the right, and Green corresponds to a pillar that must be passed on the left.

A major software improvement came from separating object identity from image position. The detected signature determines which WRO passing rule applies, while the object's x, y, width, and height values describe its geometry and relevance inside the camera image. This prevents the position of the pillar in the frame from incorrectly redefining whether the robot should pass left or right.

---

### Software Architecture

As Piolín became more complex, the software also moved away from direct sensor-to-motor reactions. Earlier versions could react immediately when a sensor detected a condition, but this became unreliable when several systems were active at the same time.

The current architecture separates sensing, perception, decision-making, and control. Sensor readings are first validated and interpreted before the navigation state determines what Piolín is currently trying to achieve. The active controller then generates the required maneuver, and control arbitration determines which steering command ultimately reaches Motor B.

This led to the development of states such as `NORMAL`, `TARGET_ACQUIRE`, `AVOID`, `PASS_CONFIRM`, `RECOVER`, `CORNER`, `PARKING`, and `STOP`. Each state represents a different physical objective, which makes the robot's behavior much easier to diagnose than a large collection of simultaneous reactions.

---

### Obstacle Avoidance and Recovery

Another important lesson was that detecting a pillar is only the beginning of obstacle avoidance. The robot must determine whether the target is valid, confirm which pillar should be followed, preserve the correct passing side during the maneuver, determine whether the pillar has actually been cleared, and then restore a useful trajectory for the next part of the course.

This was especially important because the camera may temporarily lose sight of a pillar while the chassis rotates. A missing target does not automatically mean that the pillar has been passed. The current architecture therefore preserves maneuver context and uses additional physical information before releasing the obstacle state.

Recovery also became a dedicated part of the maneuver. After passing a pillar, Piolín may be displaced from its normal corridor or angled toward a wall. Returning directly to ordinary wall navigation can create an aggressive correction, so the robot instead uses a dedicated recovery stage before normal navigation regains full authority.

---

### Control Arbitration

As more navigation behaviors were introduced, another important problem became visible: several controllers could request different steering directions at the same time. For example, obstacle avoidance might require a rightward trajectory while normal wall navigation simultaneously requests a correction to the left.

Because Piolín has only one steering actuator, Motor B cannot obey multiple independent controllers at once. The current software therefore uses an explicit hierarchy in which critical physical safety has the highest priority, followed by the active maneuver, while normal navigation receives authority when no higher-priority action is required.

This decision is one of the most important changes between the early reactive prototypes and the current Piolín architecture. It ensures that the robot's final steering behavior depends on the current physical objective rather than on several control outputs competing with one another.

---

### Color Event Processing

The Color Sensor also became more structured as the project evolved. During early experiments, a physical Blue or Orange marking could remain under the sensor for several control loops, creating the risk that one line would be counted several times.

The current approach treats a floor marking as a discrete course event. A candidate detection must be confirmed, accepted once, locked while the sensor remains over the same physical region, and released only after Piolín returns to neutral floor. This allows the Color Sensor to contribute reliable information about direction, course progression, corner context, and parking eligibility.

This change reflects a broader principle that developed throughout the project: raw sensor readings are not automatically meaningful navigation events. They must first be interpreted within the context of the robot's movement.

---

### 3D-Printed Sensor Components

The 2026 architecture also introduced custom 3D-printed components to improve sensor installation. The Color Sensor casing was developed to provide a more controlled optical environment around the downward-facing S4 sensor, reducing the influence of uncontrolled ambient light on the area immediately surrounding the measurement.

A two-part Pixy2.1 casing was also produced to support and protect the camera and make its physical installation more repeatable. Because camera orientation affects the apparent x, y, width, and height of detected blocks, the casing became part of the calibrated vision system rather than simply a protective shell.

Both components are documented together with their printing process and post-installation verification because changes to the mechanical sensor installation can also require changes to software calibration.

---

### Parking Development

Parking became another area where the project moved away from simple timed behavior. Earlier approaches could attempt to drive for a fixed period and stop, but that strategy did not provide enough information about the final physical position of the robot.

The current parking architecture is being developed as a sequence of controlled stages that includes approach, entry, alignment, final positioning, and stop. The objective is to use available information such as encoder progression, lateral geometry, steering position, course progress, and the Pink parking reference rather than depending entirely on elapsed time.

Parking remains an active calibration area in the current Phase 4 architecture, so the repository distinguishes between the established architecture and parameters that are still being refined through physical testing.

---

## What the Timeline Taught Us

The most important result of the project history is that each setback changed the way we approached the next design. The Yahboom failure made hardware reliability and safety part of our engineering decisions. The non-compliant August prototype taught us to treat WRO rules as design constraints. The slow “Forbidden” prototype showed us that stability and speed must be developed together. Nationals and Americas demonstrated the difference between a robot that succeeds once and one that can reproduce its behavior under competition conditions.

During 2026, these lessons gradually produced a much more structured robot. Piolín remained based on LEGO MINDSTORMS EV3, but the system around the controller became increasingly organized. Mechanics, sensing, perception, state logic, control arbitration, event processing, and parking were no longer treated as independent features, but as interacting parts of the same autonomous vehicle.

---

## Current Status

Piolín is currently in **Phase 4**, which represents the architecture being used for WRO Future Engineers 2026. The hardware configuration and major software responsibilities are established, while several behaviors continue to be tuned and validated through real track testing.

The current Open development continues to focus on areas such as corner consistency, starting conditions, course-event reliability, and final parking behavior. Obstacle Challenge development continues to refine target selection, pillar avoidance, pass confirmation, recovery, controller interaction, and parking.

For this reason, PiolínTech considers Phase 4 the **current competition architecture**, rather than claiming that every calibration value or maneuver has reached a permanent final state.

---

## Conclusion

Piolín's history is not simply a sequence of increasingly newer robots. It is the record of how our engineering decisions changed as we encountered new problems. Each prototype revealed limitations that could not always be predicted in software or during assembly, and every competition or track test provided information that influenced the next design.

The current Piolín is therefore the result of accumulated mechanical, electrical, sensing, and software lessons collected since June 2025. Instead of replacing the entire project whenever something failed, PiolínTech progressively refined the original concept until the robot became a more structured and understandable autonomous system designed specifically around the challenges of WRO Future Engineers.
