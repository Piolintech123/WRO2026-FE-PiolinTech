
# 5. Mobility, Kinematics, and Mechanical Analysis

This document details the mechanical design of Piolín, focusing on its kinematic framework, steering geometry, powertrain analysis, and the physical testing iterations that shaped our final mobile platform.

---

## 5.1 Mobility Framework & Steering Geometry

This section details the kinematic evolution of the robot from a differential or skid-steer drive system to a true **Ackermann** steering geometry, specifically designed to enhance precision during high-speed cornering. In the previous configuration (Phase 1.0), the constant lateral slipping of the tires compromised sensor accuracy and caused significant energy loss due to friction when turning. By implementing Ackermann geometry in Phase 2.0, the design ensures that the front wheels follow paths with concentric centers of rotation, completely eliminating the dragging or skidding of the inner and outer wheels by mathematically calculating their respective angles through the trigonometric relationship between the track width ($W = 14.0\text{ cm}$) and the wheelbase ($L = 16.5\text{ cm}$). Although this architectural shift required the construction of a much more complex mechanical linkage system and inherently restricted the vehicle's minimum turning radius, the trade-off yielded optimal structural stability, a highly predictable navigation trajectory, and the complete elimination of unforeseen physical drift during competitive runs.

```
   Front Axle (Steering)
      ┌───[ Servo ]───┐
   ===█               █=== 
      │  ╲         ╱  │ 
      │    ╲     ╱    │ 
      │      ▀▀▀      │  L (Wheelbase: 16.5 cm)
      │               │ 
      │               │ 
   ===█===============█===
     Rear Axle (Fixed Propulsion)
        ◄───── W ─────► (Track Width: 14.0 cm)

```

### 5.1.1 Ackermann Kinematic Modeling
Unlike differential steering—which causes wheels to slip laterally during high-speed turns—Ackermann geometry ensures that all wheels trace concentric circles around a single, shared instantaneous center of rotation (ICR). This is mathematically defined as:

$$\cot(\theta_{\text{outer}}) - \cot(\theta_{\text{inner}}) = \frac{W}{L}$$

Where:
*   $W$: Track width ($14.0\text{ cm}$ or $0.14\text{ m}$)
*   $L$: Wheelbase ($16.5\text{ cm}$ or $0.165\text{ m}$)
*   $\theta_{\text{inner}}$: Steering angle of the inside wheel
*   $\theta_{\text{outer}}$: Steering angle of the outside wheel

### 5.1.2 Design Tradeoffs: Skid-Steer vs. Ackermann

*   **Skid-Steering (Phase 1.0):** Extremely simple to build and allowed a zero-turning radius. However, it caused massive tire slip, dragged down battery voltage during tight turns, and introduced random physical drift that ruined our sensor path calculations.
*   **Ackermann Steering (Phase 2.0):** Required complex mechanical linkages and restricted our minimum turning radius. However, it eliminated lateral tire slip entirely, stabilized our trajectory tracking, and ensured predictable, highly repeatable steering maneuvers.

---

## 5.2 Mechanical Powertrain & Actuator Torque Analysis

To guarantee that "Piolín" can handle continuous high-speed runs and sharp steering corrections, we performed static and dynamic physical analyses.

### 5.2.1 Drive Motor Torque & Speed Reasoning
Our drive system must provide a balance of high acceleration (to quickly recover speed after obstacle avoidance maneuvers) and a high top speed on straightaways.

*   **Total Robot Mass ($m$):** $1.4\text{ kg}$
*   **Wheel Radius ($r$):** $0.03\text{ m}$ ($3\text{ cm}$)
*   **Target Acceleration ($a$):** $2.0\text{ m/s}^2$
*   **Coefficient of Rolling Friction ($\mu$):** $0.05$ (Rubber on track surface)
*   **Number of Drive Motors ($N$):** $2$

First, we calculate the total force ($F_{\text{total}}$) required to overcome both inertia and rolling resistance:

$$F_{\text{total}} = F_{\text{inertia}} + F_{\text{friction}}$$

$$F_{\text{total}} = (m \cdot a) + (m \cdot g \cdot \mu)$$

$$F_{\text{total}} = (1.4\text{ kg} \cdot 2.0\text{ m/s}^2) + (1.4\text{ kg} \cdot 9.81\text{ m/s}^2 \cdot 0.05) \approx 3.49\text{ N}$$

Distributed across both drive motors, the required force per wheel ($F_{\text{wheel}}$) is:

$$F_{\text{wheel}} = \frac{3.49\text{ N}}{2} = 1.745\text{ N}$$

The minimum required dynamic stall torque ($T_{\text{drive}}$) per motor is:

$$T_{\text{drive}} = F_{\text{wheel}} \cdot r$$

$$T_{\text{drive}} = 1.745\text{ N} \cdot 0.03\text{ m} \approx 0.052\text{ N}\cdot\text{m} \quad (5.3\text{ N}\cdot\text{cm})$$

*   **Motor Choice & Speed Margin:** We chose metal-geared DC motors providing up to $0.15\text{ N}\cdot\text{m}$ of stall torque (giving us a **2.88x safety margin**). With a rated speed of $320\text{ RPM}$ at $6\text{V}$, the theoretical maximum linear velocity ($v_{\text{max}}$) is:
    
    $$v_{\text{max}} = \omega \cdot r = \left(320 \cdot \frac{2\pi}{60}\right) \cdot 0.03\text{ m} \approx 1.005\text{ m/s}$$
    
    This speed allows the robot to complete competition laps efficiently while staying well within the stable boundaries of our $50\text{ Hz}$ vision tracking loop.

---

### 5.2.2 Steering Servo Torque Analysis (Static Turn Resistance)
To verify that our steering servo can actuate the wheels while stationary (worst-case friction scenario), we calculate the static steering resistance torque ($T_{\text{steering}}$):

*   **Weight on Front Axle ($W_{\text{front}}$):** $0.7\text{ kg}$ ($6.87\text{ N}$)
*   **Tire Width/Contact Patch ($b$):** $0.02\text{ m}$
*   **Steering Pivot Arm Radius ($d_{\text{arm}}$):** $0.015\text{ m}$ ($1.5\text{ cm}$)
*   **Static Friction Coefficient ($\mu_s$):** $0.8$ (High-grip rubber)

The torque required to spin the tire contact patch in a stationary position is:

$$T_{\text{pivot}} = \frac{1}{3} \cdot \mu_s \cdot W_{\text{front}} \cdot b$$

$$T_{\text{pivot}} = \frac{1}{3} \cdot 0.8 \cdot 6.87\text{ N} \cdot 0.02\text{ m} \approx 0.0366\text{ N}\cdot\text{m}$$

Converting this rotation to the servo's mechanical linkage via our steering pivot arm ($d_{\text{arm}}$), the minimum torque required at the servo horn is:

$$T_{\text{servo}} = T_{\text{pivot}} \cdot \left(\frac{1}{d_{\text{arm}}}\right)$$

$$T_{\text{servo}} = 0.0366\text{ N}\cdot\text{m} \cdot \left(\frac{1}{0.015\text{ m}}\right) \approx 2.44\text{ N}\cdot\text{m} \quad (24.9\text{ kg}\cdot\text{cm})$$

*   **Actuator Selection:** We selected a metal-geared high-torque digital servo rated for $3.2\text{ N}\cdot\text{m}$ ($32.6\text{ kg}\cdot\text{cm}$) at $5\text{V}$. This exceeds our minimum static requirements, preventing gear stripping and steering lag during aggressive maneuvers.

---

## 5.3 Mechanical Iterations & Performance Gains


```

[Phase 1.0 (LEGO)]        [Phase 2.0 (Early 3D)]       [Phase 2.1 (Current)]

* High Mechanical Flex    - Lower Flex                 - Zero Play Carbon Rods
* Direct Gear Slippage    - Weak 3D Print Linkages     - Machined Brass Bushings
* No Adjustability        - High SLA Material Snap     - Adjustable Ball Joints

```

Our chassis went through three major physical design iterations based on testing data:

### Iteration 1: The LEGO Technic Base (Phase 1.0)
*   **Issue:** The structural beams flexed under load, causing the front steering wheels to physically toe-out during acceleration. This introduced a drift error of up to $\pm 8\text{ cm}$ per meter traveled.
*   **Fix:** Scrapped the LEGO chassis and designed a rigid, 3D-printed custom frame plate to anchor all structural points.

### Iteration 2: SLA/3D Printed Ackermann Linkages
*   **Issue:** While the 3D-printed chassis was rigid, the printed steering linkages suffered from high friction at the pivot points. This restricted the servo's responsiveness and caused the steering to bind up under maximum turning angles.
*   **Fix:** Redesigned the linkage pivot points with machined brass press-fit bushings and replaced the 3D-printed rods with adjustable carbon fiber turnbuckles containing mini steel ball-joints.

### Iteration 3: Low-Center-of-Gravity (LoCoG) Redesign
*   **Issue:** During high-speed testing ($>0.8\text{ m/s}$), the high mounting position of the heavy battery bank caused body roll, slightly lifting the inner rear wheel on sharp corners and causing loss of traction.
*   **Fix:** Lowered the battery mounting cradle by $2.2\text{ cm}$, dropping the overall Center of Gravity (CoG). This stabilized wheel contact pressure and reduced our cornering lap times by **14%** with zero wheel lift.


