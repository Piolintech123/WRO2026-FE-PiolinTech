# PiolínTech 3D Printing Process

This directory documents the **3D-printed components designed, manufactured, tested, and installed on Piolín** during the development of the WRO Future Engineers 2026 robot.

3D printing was used where the standard LEGO structure did not provide the exact geometry required for a sensor installation.

The current printed components are:

```text
ColorSensorCasing.stl

PIXY_Case1.stl

PIXY_Case2.stl
```

These components support two important sensing systems:

```text
S4 Color Sensor
→ ColorSensorCasing.stl
```

and:

```text
Pixy2.1
→ PIXY_Case1.stl
→ PIXY_Case2.stl
```

---

# Printing Equipment

PiolínTech manufactured the current printed components using an:

**Anet ET4X 3D Printer**

The printer provides sufficient build space for the custom sensor housings used on Piolín.

<div align="center">

<img
  src="https://github.com/user-attachments/assets/07d5d86e-c8d5-4aa6-9109-42227dfe5aa5"
  alt="Anet ET4X 3D printer used by PiolínTech"
  width="600"
/>

<br>

<sub><b>Figure 1.</b> Anet ET4X 3D printer used to manufacture Piolín's custom sensor components.</sub>

</div>

The available build volume for this printer model is:

```text
220 × 220 × 250 mm
```

This was sufficient for the sensor-casing components used on Piolín.

---

# Filament

The material used for the printed components was:

**OVERTURE High Speed PLA**

with:

```text
Filament diameter: 1.75 mm
Spool size:        1 kg
```

<div align="center">

<img
  src="https://github.com/user-attachments/assets/47db2b68-44a2-4477-9929-342703d8487d"
  alt="OVERTURE High Speed PLA filament used by PiolínTech"
  width="560"
/>

<br>

<sub><b>Figure 2.</b> OVERTURE High Speed PLA filament used to manufacture Piolín's custom 3D-printed components.</sub>

</div>

PLA was used to manufacture the custom sensor-support components installed on the robot.

---

# Printing Parameters

The printing configuration used by PiolínTech was:

| Parameter | Setting |
|---|---:|
| Printer | Anet ET4X |
| Filament | OVERTURE High Speed PLA |
| Filament diameter | 1.75 mm |
| Nozzle temperature | 200 °C |
| Heated bed temperature | 80 °C |
| Print speed setting | 100% |
| Available build volume | 220 × 220 × 250 mm |

The `100%` speed value refers to the **printer speed setting used during manufacturing**, rather than a measured linear printing speed in mm/s.

Parameters that were not formally recorded during the original manufacturing process are not presented as measured specifications in this repository.

---

# Manufacturing Workflow

The general manufacturing process used by PiolínTech was:

```text
3D MODEL
   ↓
EXPORT STL
   ↓
IMPORT INTO SLICER
   ↓
PREPARE MODEL
   ↓
SET PRINT PARAMETERS
   ↓
SLICE
   ↓
TRANSFER PRINT FILE
   ↓
PREHEAT PRINTER
   ↓
PRINT
   ↓
REMOVE PART
   ↓
INSPECT
   ↓
TEST FIT
   ↓
INSTALL ON PIOLÍN
   ↓
RECALIBRATE SENSOR
```

The objective of this process was not only to manufacture the part successfully, but also to ensure that the printed component worked correctly as part of Piolín's complete sensor system.

---

# 1. Prepare the STL

The required model is first selected from the `3dprint/` directory.

Current files:

```text
ColorSensorCasing.stl
PIXY_Case1.stl
PIXY_Case2.stl
```

The STL file is imported into the slicing software before printing.

At this stage, the model is prepared for fabrication on the Anet ET4X.

---

# 2. Prepare the Print

Before beginning the print, the model is positioned and prepared in the slicing software.

The temperature configuration used by PiolínTech was:

```text
NOZZLE
→ 200 °C
```

```text
HEATED BED
→ 80 °C
```

The printer speed setting used during these prints was:

```text
100%
```

The objective of documenting these settings is to make it possible to reproduce the manufacturing process if one of Piolín's printed components must be replaced.

---

# 3. Preheat the Printer

Before extrusion begins, the Anet ET4X is brought to the configured printing temperatures.

```text
BED
→ 80 °C
```

```text
NOZZLE
→ 200 °C
```

Printing begins after the printer reaches the required operating temperatures.

---

# 4. Print the Component

The sliced model is then printed using:

```text
PRINTER
Anet ET4X

FILAMENT
OVERTURE High Speed PLA
1.75 mm

NOZZLE
200 °C

BED
80 °C

PRINT SPEED SETTING
100%
```

During manufacturing, the print is monitored for obvious problems that could affect the final geometry or installation of the component.

Examples include:

```text
major deformation

incomplete sections

poor attachment to the print surface

unexpected movement of the part

geometry that could affect sensor fit
```

---

# 5. Remove and Inspect

After printing is complete, the part is removed from the printer and visually inspected.

The team checks whether the component contains problems that could prevent proper installation.

This includes checking for:

```text
major deformation

incomplete geometry

incorrect fit

blocked sensor openings

cable interference

interference with nearby LEGO structure
```

A component is therefore not considered successful only because the 3D printer completed the job.

It must also function correctly when installed on Piolín.

---

# Fit Testing

Each printed component is physically tested on the robot before being accepted.

The general verification process is:

```text
PRINT
   ↓
FIT ON ROBOT
   ↓
CHECK POSITION
   ↓
CHECK SENSOR
   ↓
CHECK CABLES
   ↓
CHECK CLEARANCE
   ↓
ACCEPT OR MODIFY
```

If the component does not provide the intended result:

```text
MODEL
   ↓
MODIFY
   ↓
REPRINT
   ↓
RETEST
```

This makes 3D printing part of PiolínTech's iterative engineering process rather than only a manufacturing step.

---

# Color Sensor Casing

The file:

```text
ColorSensorCasing.stl
```

is used for the custom casing surrounding Piolín's downward-facing **S4 EV3 Color Sensor**.

The casing was developed to create a more controlled physical environment around the sensor and reduce the influence of uncontrolled external light on floor readings.

This is especially relevant when distinguishing:

```text
Blue course markings

Orange course markings
```

The complete relationship is:

```text
EXTERNAL LIGHT
      ↓
COLOR SENSOR ENVIRONMENT
      ↓
S4 MEASUREMENTS
      ↓
RGB / REFLECTION VALUES
      ↓
COLOR CLASSIFICATION
```

By adding a physical casing around the sensor, PiolínTech can make the sensing environment more repeatable.

However, installing the casing can also change the sensor's actual readings.

Therefore:

```text
PRINT
→ INSTALL
→ TEST S4
→ RECALIBRATE IF REQUIRED
```

Detailed manufacturing and installation documentation is available in:

[Color Sensor Casing Print](ColorSensorCasing_Print.md)

---

# Pixy2.1 Case

The current Pixy2.1 casing is composed of:

```text
PIXY_Case1.stl

PIXY_Case2.stl
```

The printed pieces form part of the physical camera installation used during the **Obstacle Challenge**.

The casing contributes to:

```text
mechanical protection

camera support

repeatable installation

more consistent camera positioning

partial shielding from stray light,
depending on casing geometry
```

Because the casing changes the physical installation of Pixy2.1, it is treated as part of the complete vision system rather than as a purely cosmetic component.

The relationship is:

```text
3D-PRINTED CASE
      ↓
CAMERA POSITION
      ↓
CAMERA FIELD OF VIEW
      ↓
PIXY BLOCK GEOMETRY
      ↓
VISION PROCESSING
      ↓
NAVIGATION DECISION
```

After installation, PiolínTech verifies:

```text
camera opening remains unobstructed

Pixy cable remains unobstructed

camera orientation remains usable

Red pillar detection

Green pillar detection

Pink parking detection
```

Detailed manufacturing and installation documentation is available in:

[Pixy2.1 Case Print](PixyCase_Print.md)

---

# Post-Installation Calibration

A 3D-printed sensor component is not treated independently from the sensor's software calibration.

The complete process is:

```text
PRINT COMPONENT
      ↓
INSTALL
      ↓
VERIFY PHYSICAL FIT
      ↓
TEST SENSOR
      ↓
COLLECT REAL READINGS
      ↓
ADJUST CALIBRATION IF REQUIRED
      ↓
VALIDATE ON PIOLÍN
```

For the Color Sensor casing:

```text
physical casing
      ↓
optical environment changes
      ↓
S4 readings verified
      ↓
Blue / Orange detection retested
```

For the Pixy2.1 casing:

```text
physical camera installation
      ↓
camera geometry / field of view
      ↓
Pixy blocks verified
      ↓
Red / Green / Pink detection retested
```

This relationship between manufacturing and sensing is important because a physically successful print is only useful if the corresponding sensor remains reliable after installation.

---

# Current 3D-Printed Components

| File | System | Function |
|---|---|---|
| `ColorSensorCasing.stl` | S4 Color Sensor | Creates a more controlled physical and optical environment around the floor sensor |
| `PIXY_Case1.stl` | Pixy2.1 | Part of the custom camera casing |
| `PIXY_Case2.stl` | Pixy2.1 | Part of the custom camera casing |

---

# Reproducing the Prints

The currently documented manufacturing configuration is:

```text
3D PRINTER
Anet ET4X
```

```text
FILAMENT
OVERTURE High Speed PLA
Diameter: 1.75 mm
```

```text
NOZZLE TEMPERATURE
200 °C
```

```text
BED TEMPERATURE
80 °C
```

```text
PRINT SPEED SETTING
100%
```

The available STL files are:

```text
ColorSensorCasing.stl

PIXY_Case1.stl

PIXY_Case2.stl
```

After manufacturing:

```text
INSPECT
   ↓
TEST FIT
   ↓
INSTALL
   ↓
VERIFY SENSOR
   ↓
RECALIBRATE IF REQUIRED
```

---

# Engineering Relevance

The 3D-printed components solve problems that are directly connected to Piolín's autonomous performance.

```text
ColorSensorCasing.stl
      ↓
more controlled S4 environment
      ↓
more repeatable floor sensing
```

and:

```text
PIXY_Case1.stl
+
PIXY_Case2.stl
      ↓
repeatable Pixy2.1 installation
      ↓
more consistent vision geometry
```

The manufacturing process is therefore connected directly to:

```text
MECHANICAL DESIGN
      ↓
SENSOR INSTALLATION
      ↓
PERCEPTION
      ↓
SOFTWARE CALIBRATION
      ↓
AUTONOMOUS PERFORMANCE
```

The central manufacturing principle used by PiolínTech is:

> **A 3D-printed component is considered successful only when it can be manufactured, installed consistently, and verified as part of the sensing system it was designed to support.**
