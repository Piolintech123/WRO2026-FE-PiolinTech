# Electrical Schematics & Circuit Diagrams

*   **[EV3Kicad.png](./EV3Kicad.png)**
    This schematic captures the primary PCB design for our EV3 interface. It documents the exact signal path mapping between the EV3 output ports and our custom sensor array. By visualizing the layout in KiCad, we ensure that every connection from the motor drivers to the ultrasonic sensors is verified for signal integrity. This blueprint is essential for troubleshooting electrical noise issues and confirms that our wiring logic perfectly matches the programmatic pin mapping used in our Pybricks environment.

*   **[PTScheme.png](./PTScheme.png)**
    This technical document illustrates the overarching electrical architecture of the PiolínTech system. It provides a clear visual hierarchy of the power distribution rails and the communication bus lines connecting our EV3 brain to peripheral hardware. This high-level schematic is critical for understanding the complete signal flow, ensuring that power rails remain isolated and that digital signals are routed cleanly across the robot chassis to prevent data corruption during high-speed operations.

*   **[PTechcircuit_image.png](./PTechcircuit_image.png)**
    This visual documentation displays the physical implementation of our circuit design as integrated onto the PiolínTech chassis. It bridges the gap between theoretical schematic design and real-world hardware assembly. By documenting the exact cable routing, soldering points, and component positioning, we ensure that our assembly process is fully reproducible. It serves as a vital visual reference for maintenance, allowing us to quickly identify and repair any physical wiring faults encountered during testing.
