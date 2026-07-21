# Flowcharts and Resources

## 1. [Navigation State Flowchart](./01_NVStateFC.md)

The Navigation State Flowchart visualizes our core control loop. Upon system boot and sensor calibration, the robot enters a high speed PID state to track the lane. We utilize an interrupt driven architecture where the main execution pauses only when proximity sensors detect an obstacle. This triggers the RGB parsing routine to identify color coded markers. The logic then executes a pre defined evasion maneuver based on the color identification, either turning left for red or right for green. The robot constantly scans to reacquire the primary lane, defaulting to emergency braking if visual confirmation fails. This state machine approach ensures that our robot maintains stability during complex maneuvers without losing its orientation on the track.

```mermaid
graph TD
    %% Define States
    A[Power On / Boot] --> B[Sensor Calibration]
    B --> C{Initialization Success?}
    C -- No --> D[Error Diagnostic Halt]
    C -- Yes --> E[PID Lane Tracking State]
    
    %% Main Loop & Interrupts
    E --> F{Proximity Sensor Interrupt?}
    F -- No / Clear Path --> E
    F -- Yes / Obstacle Detected --> G[RGB Color Signature Parse]
    
    %% Obstacle Routing Matrix
    G --> H{Color ID Identified?}
    H -- Red Marker --> I[Execute Left Evasion Routing]
    H -- Green Marker --> J[Execute Right Evasion Routing]
    H -- Unknown/Shadow --> K[Emergency Static Braking]
    
    %% Re-alignment
    I --> L[Scan for Primary Color Lane]
    J --> L
    K --> L
    L --> M{Lane Re-acquired?}
    M -- Yes --> E
    M -- No --> K
    
    %% Styles with explicitly forced black text (color:#000)
    classDef default fill:#f9f9f9,stroke:#333,stroke-width:1px,color:#000;
    classDef state fill:#d5e8d4,stroke:#82b366,stroke-width:2px,font-weight:bold,color:#000;
    classDef dec fill:#fff2cc,stroke:#d6b656,stroke-width:2px,color:#000;
    classDef err fill:#f8cecc,stroke:#b85450,stroke-width:2px,color:#000;
    
    class A,B,E,G,I,J,L state;
    class C,F,H,M dec;
    class D,K err;

```

---

## 2. [Vision Processing Logic](./02_VProcessing.md)

This diagram outlines the computer vision pipeline that powers our autonomous obstacle detection system. We employ the K210 dual core RISC V processor, which acts as a dedicated AI accelerator. It ingests raw visual frames from the OV2640 sensor. The onboard KPU model then executes real time feature extraction to identify red and green color signatures. Once detected, it generates precise bounding boxes for these objects. This coordinate data is formatted into clean serial packages containing X and Y offsets, ID tags, and dimensions. These packages are transmitted to the host Raspberry Pi 5 via hardware I2C protocols. This offloading strategy is critical for performance, allowing the main processor to focus on steering.

```mermaid
graph TD
    %% Define Nodes
    A[Raw Visual Frame Ingestion <br> Sensor: OV2640] --> B[K210 Dual-Core RISC-V Processor <br> Executes Onboard KPU Models]
    B --> C[Internal Color & Coordinate <br> Bounding Box Generation]
    C --> D[Clean Serial Packages <br> X/Y, ID, Width, Height]
    D --> E[Host Controller <br> Raspberry Pi 5 via Hardware I2C]

    %% Styles forcing black text (color:#000)
    classDef default fill:#ecf0f1,stroke:#2c3e50,stroke-width:1.5px,color:#000000,font-family:sans-serif;
    classDef highlight fill:#d5e8d4,stroke:#82b366,stroke-width:2px,color:#000000,font-weight:bold;
    
    class B,E highlight;

```

---

## 3. [Torque Calculation](./03_TorqueCalc.png)

This document details the mechanical analysis used to select the optimal drive motor for our chassis. We calculated the total tractive force required by summing the force of acceleration and the rolling resistance. With a vehicle mass of 0.72 kg and an acceleration of 0.50 m/s squared, our calculations resulted in a required force of 0.50 N. We then derived the required torque by multiplying this force by the radius of the rear wheels. The resulting value confirmed that our assembly maintains a torque capacity approximately 18 times greater than the threshold required to overcome static inertia. This significant safety margin ensures our robot can handle rapid accelerations and track surface changes without motor stalling.

![Torque Calculation Analysis](/embed/03_TorqueCalc.png)

