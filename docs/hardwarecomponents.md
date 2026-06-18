# Hardware Components Overview

## Introduction
Our robot's hardware architecture combines precision actuation, high-quality sensing, and advanced computation to navigate a predefined track, detect obstacles, and execute complex maneuvers. This section provides a detailed overview of all hardware components, including the Nexigo camera, LEGO EV3 Brick, motors, ultrasonic sensors, and the color sensor. Each component is described in terms of quantity, voltage requirements, functionality, and key features, ensuring a complete understanding of the robot’s physical architecture.

---

## LEGO Color Sensor
- **Quantity:** 1  
- **Voltage:** 4.3–5V (powered via EV3 Brick port)  
- **Description:** The LEGO Color Sensor detects the color of surfaces or objects directly in front of it. It can be used for obstacle recognition, simple visual cues, or track detection if programmed. The sensor communicates directly with the EV3 Brick, which processes the data for autonomous decision-making.  
- **Features:** Measures reflected and ambient light, detects colors (only red and green in our case), compatible with EV3 programming environments (LEGO Mindstorms Python, Pybricks).
<img width="300" height="300" alt="lego-color-senso" src="https://github.com/user-attachments/assets/5e59f3a1-5b7c-4992-9d57-07951f412e67" />

---

## LEGO EV3 Brick
- **Quantity:** 1  
- **Voltage:** 10V 
- **Description:** The EV3 Brick functions as the primary actuator controller of the robot. It executes commands from onboard programs or the Raspberry Pi, controls motors, reads sensor inputs, and coordinates all low-level robot actions.  
- **Features:** ARM9 processor, 64KB RAM, 16MB flash memory, 6 sensor input ports, 4 motor output ports, Bluetooth and USB connectivity, supports programming in MicroPython, EV3-G, and other languages.
<img width="300" height="300" alt="ev3" src="https://github.com/user-attachments/assets/ab7c39a9-6f0e-4c9d-aee2-8d59c25d3adc"/>

---

## DC Motors
### Rear Motor (A)
- **Quantity:** 1  
- **Voltage:** 7.2V nominal (powered by EV3)  
- **Description:** Drives the rear wheels, providing the main propulsion for the robot. Controlled by the EV3 Brick, it allows precise speed and direction adjustments.  
- **Features:** Built-in rotation sensors (encoders) for distance measurement, supports controlled acceleration and braking.

### Front Motor (B)
- **Quantity:** 1  
- **Voltage:** 7.2V nominal (powered by EV3)  
- **Description:** Controls front-wheel steering, enabling accurate turning maneuvers and path adjustments.  
- **Features:** Encoder feedback for precise angular positioning, reversible rotation for left/right turns.
<img width="300" height="300" alt="motor" src="https://github.com/user-attachments/assets/9177962f-3d0e-4574-9b86-d18fa9171280" />

---

## Ultrasonic Sensors
### Front Ultrasonic Sensor (S1)
- **Quantity:** 1  
- **Voltage:** 4.5–7V (EV3 powered)  
- **Description:** Detects obstacles or walls directly ahead of the robot. Provides distance measurements to prevent collisions and enable safe navigation.  
- **Features:** Range 0–250 cm, high sampling rate, adjustable detection thresholds, supports both continuous and triggered measurement modes.
<img width="500" height="500" alt="motor" src="https://github.com/user-attachments/assets/b8872f62-adb5-4fd1-98fb-18491c57de56"/>

### Right Ultrasonic Sensor (S2) & Left Ultrasonic Sensor (S3)
- **Quantity:** 2  
- **Voltage:** 4.5–7V (EV3 powered)  
- **Description:** Mounted on the sides, these sensors help maintain alignment with walls or track boundaries and assist in path correction during turns or evasive maneuvers.  
- **Features:** Same as front ultrasonic, supports simultaneous readings for improved side-to-side positioning.
<img width="500" height="500" alt="motor" src="https://github.com/user-attachments/assets/b8872f62-adb5-4fd1-98fb-18491c57de56"/>


---

## Conclusion
Overall, Our robot achieves to integrate multiple hardware components in a unified system, and this helps us allow autonomous navigation, obstacle avoidance, and accurate path following. The combination of high-performance computation, **visual sensing (Nexigo Camera)**, and **robust actuation and sensing (EV3 Brick, motors, and sensors)** ensures reliability and precision in the Open and Obstacle Challenges of the WRO. Each component contributes to the overall efficiency, safety, and adaptability of the robot, forming a versatile platform capable of tackling complex tasks in competitive robotics environments.
