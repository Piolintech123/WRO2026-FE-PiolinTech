## Current Hardware I/O Register & Electrical Interface

<table border="0">
  <tr>
    <td width="35%" valign="top">
      <h3>Left Lateral Sensor (S1)</h3>
      <p>Symmetrically allocated ultrasonic transducer operating within a 4.5V–7V DC envelope. It broadcasts acoustic ping sequences to map instantaneous lateral distance variables ($d_{\text{left}}$) relative to the left boundary wall, feeding the core lane-centering matrix.</p>
    </td>
    <td width="30%" align="center" valign="middle">
      <br>
      <h3>Central Controller (LEGO EV3)</h3>
      <p>The primary CPU and deterministic thread scheduler. It ingests high-frequency sensory telemetry from ports S1–S4 and processes the discrete PID control laws.</p>
    </td>
    <td width="35%" valign="top">
      <h3>Primary Propulsion (Ports A & B)</h3>
      <p>Dual high-torque LEGO Large Core Motors configured in a parallel arrangement driving the rear propulsion axle. They receive synchronized PWM voltage signals to maintain linear velocity matching through our custom 3D-printed involute differential gearbox.</p>
    </td>
  </tr>

  <tr>
    <td width="35%" valign="middle">
      <h3>Right Lateral Sensor (S2)</h3>
      <p>Matches the left transducer configuration, monitoring the right flank distance ($d_{\text{right}}$). A software-level noise filtration register filters out secondary reflections and cross-talk echoes to prevent steering instability at peak velocities.</p>
    </td>
    <td width="30%" align="center" valign="middle">
      <img src="https://github.com/user-attachments/assets/fcc56fdc-522b-426d-bd81-ac708e1cd2cc" alt="EV3 Block Wiring Architecture" width="100%"/>
    </td>
    <td width="35%" valign="middle">
      <h3>Ackermann Steering Servo (Port C)</h3>
      <p>A single LEGO Medium Core Motor vertically integrated into the front sub-chassis to manipulate the mechanical Ackermann linkage layout. Operating as a closed-loop digital position servo, its minimal rotor inertia ensures immediate transient response times for micro-corrections.</p>
    </td>
  </tr>

  <tr>
    <td width="35%" valign="bottom">
      <h3>Front US Sensor (S3)</h3>
      <p>Positioned at the absolute geometric center of the front bumper matrix along the longitudinal axis. It continuously monitors the forward vector ($d_{\text{forward}}$) and functions as the primary hardware-interrupt trigger to instantly jump into the Round 2 obstacle-bypass routine.</p>
    </td>
    <td width="30%" align="center" valign="top">
      <p><b>Signal & Power Rails:</b> Inputs S1–S4 run on safe logic rails, while output channels A–C push digital PWM duty cycles under active current protection.</p>
    </td>
    <td width="35%" valign="bottom">
      <h3>Solid-State Gyroscope (S4)</h3>
      <p>An onboard single-axis solid-state digital gyroscope that tracks the vehicle's angular velocity and absolute heading drift along the yaw axis with a 1-degree resolution. Delivers an un-aliased heading reference during aggressive cornering when walls fade out of sensor range.</p>
    </td>
  </tr>
</table>
