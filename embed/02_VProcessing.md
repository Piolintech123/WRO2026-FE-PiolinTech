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
