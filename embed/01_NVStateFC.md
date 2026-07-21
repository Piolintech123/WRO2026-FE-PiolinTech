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
