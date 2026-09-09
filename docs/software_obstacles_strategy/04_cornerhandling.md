# 4. Corner Handling

<div align="center">

<img
  src="../../v-photos/v4/full_track.jpg"
  alt="Track geometry used for Piolín corner-handling development"
  width="740"
/>

<br>

<sub><b>Figure 4.1.</b> Corner handling must transition Piolín from one straight corridor to the next while preserving enough control authority to detect obstacles, avoid walls, and recover stable geometry.</sub>

</div>

Corner handling is one of the most important transitions in Piolín's autonomous software.

A corner is not treated simply as:

```text
steer strongly for a fixed amount of time
```

because entering a turn changes several things simultaneously:

```text
ultrasonic geometry changes

the preferred wall relationship changes

the Ackermann steering system rotates the chassis

Pixy2.1 viewing direction changes

visible pillars can move rapidly inside or outside the camera frame

normal straight-line wall assumptions become temporarily invalid
```

For this reason, the current Obstacle Challenge architecture is moving toward a dedicated **corner state** rather than allowing normal wall following to interpret every unusual ultrasonic reading as lateral error.

The intended high-level sequence is:

```text
NORMAL
   ↓
CORNER EVIDENCE
   ↓
CORNER ENTRY
   ↓
CORNER
   ↓
CORNER EXIT
   ↓
REACQUIRE GEOMETRY
   ↓
NORMAL
```

This document describes the design direction based on the control principles already tested in Piolín's prototype programs. The final corner thresholds, steering values, and transition conditions are still being calibrated.

---

## 4.1 What the Current Prototypes Already Show

The current Piolín programs contain two useful corner-handling approaches.

One early prototype uses a very direct sequence:

```python
def turn_for_color(detected_color):

    if detected_color == 'BLUE':
        target = -TURN_STEERING_ANGLE * STEER_DIRECTION

    else:
        target = TURN_STEERING_ANGLE * STEER_DIRECTION

    steering.run_target(
        STEERING_SPEED,
        target,
        then=Stop.HOLD,
        wait=True
    )

    drive.run(TURN_SPEED)
    wait(TURN_TIME_MS)

    center_steering()

    drive.run(NORMAL_SPEED)
    wait(POST_TURN_STRAIGHT_MS)
```

This prototype demonstrates an important basic state sequence:

```text
detect event
      ↓
enter turn
      ↓
hold steering
      ↓
move through corner
      ↓
center steering
      ↓
continue straight
```

It is useful because it proves the complete maneuver can be separated from normal driving.

However, the final Obstacle controller should not depend only on a fixed time because:

```text
entry position can vary

vehicle speed can vary

mechanical steering response can vary

course geometry can vary slightly

pillar avoidance may change the corner approach
```

The more advanced geometry prototype contributes another important idea: the software can recognize when the measurements no longer resemble a normal straight corridor.

---

# 4.2 Detecting When Straight Geometry Is No Longer Valid

During a normal straight, Piolín expects a relationship between the two lateral ultrasonic measurements.

The development controller calculates:

```python
geometry_error = abs(
    (Di + Do)
    - EXPECTED_SUM_MM
)
```

A confidence-like value is then calculated:

```python
weight = 1.0 - (
    geometry_error
    / GEOMETRY_TRANSITION_MM
)

weight = clamp(
    weight,
    0.0,
    1.0
)
```

Conceptually:

```text
weight near 1
→ measurements resemble expected straight geometry
```

while:

```text
weight decreases
→ measurements no longer resemble a clean straight corridor
```

This is useful during corner handling because a turn naturally changes what both ultrasonic sensors observe.

Instead of concluding:

```text
large geometry error
→ robot must be badly positioned
```

the state machine can ask:

```text
large geometry change
+
course event / expected corner
→ corner may be starting
```

This distinction prevents the normal wall controller from producing an unnecessarily large correction exactly when the vehicle should begin turning.

---

# 4.3 Corner Detection Should Use More Than One Clue

The planned Obstacle Challenge controller should avoid depending on one raw sensor sample to determine that a corner has begun.

Useful evidence can include:

```text
S4 floor landmark

course progression state

change in S2/S3 geometry

loss of normal corridor coherence

current vehicle trajectory
```

The intended logic is closer to:

```text
possible corner evidence
      ↓
confirm that course state allows a corner
      ↓
geometry also changes consistently
      ↓
enter CORNER
```

rather than:

```text
one strange ultrasonic value
→ immediately turn
```

Likewise:

```text
one color sample
→ immediately turn
```

is weaker than a confirmed event.

The color-event prototype already demonstrates how Piolín confirms a sensor event before acting:

```python
if detected == candidate_color:
    candidate_count += 1
else:
    candidate_color = detected
    candidate_count = 1
```

followed by:

```python
if candidate_count >= COLOR_CONFIRMATIONS:
```

The final corner detector can use the same architectural principle:

```text
DETECT
→ CONFIRM
→ TRANSITION
```

even if the exact final evidence differs.

---

# 4.4 Entering the CORNER State

Once a corner is confirmed, Piolín should temporarily stop treating the robot as if it were driving through a normal straight.

Conceptually:

```python
if corner_confirmed:
    state = CORNER
```

Entering `CORNER` changes controller priorities.

During `NORMAL`:

```text
wall geometry
→ major steering influence
```

During `CORNER`:

```text
corner trajectory
→ major steering influence
```

while:

```text
wall safety
→ remains available
```

This prevents the following conflict:

```text
corner controller
→ steer strongly into turn

normal wall controller
→ unusual geometry detected
→ steer opposite direction
```

Without state-dependent authority, the two commands can weaken one another and produce:

```text
wide corners

late turning

zig-zag

wall collisions
```

The state machine therefore determines when normal wall following should temporarily reduce its influence.

---

# 4.5 Steering Through the Corner

<div align="center">

<img
  src="../../v-photos/v4/ackermann_top.jpg"
  alt="Piolín Ackermann-style steering system"
  width="700"
/>

<br>

<sub><b>Figure 4.2.</b> Corner software commands Motor B, while the physical Ackermann-style linkage determines the resulting front-wheel angles and turning path.</sub>

</div>

Piolín uses:

```text
Motor B
→ front Ackermann-style steering
```

which means the software does not rotate the vehicle in place.

The complete physical sequence is:

```text
Motor B changes steering
      ↓
front wheel angles change
      ↓
Motor A continues propulsion
      ↓
vehicle follows curved path
      ↓
chassis orientation changes
```

This makes corner shape dependent on both:

```text
steering angle
```

and:

```text
drive speed
```

A steering value cannot therefore be calibrated independently from Motor A speed.

The current simple prototype already reflects this by using a dedicated turn speed:

```python
drive.run(TURN_SPEED)
```

instead of normal straight speed.

The final Obstacle controller is expected to preserve the same principle even if the maneuver is no longer purely time-based.

---

# 4.6 Steering Smoothing During Corner Entry

The more advanced controller already limits how quickly the desired steering target can change:

```python
def smooth_target(target):
    global current_target

    diff = target - current_target
    diff = clamp(
        diff,
        -TARGET_STEP,
        TARGET_STEP
    )

    current_target += diff
    return current_target
```

This is useful during a corner because Motor B is a physical mechanism.

A command such as:

```text
0
→ maximum turn
```

in one control cycle can create:

```text
mechanical shock

overshoot

inconsistent corner entry

rapid chassis yaw
```

A controlled target progression instead creates:

```text
STRAIGHT
   ↓
increasing steering
   ↓
corner steering
```

The smoothing amount must still be fast enough that the turn does not begin too late.

Therefore corner tuning involves a trade-off:

```text
too abrupt
→ unstable / aggressive
```

```text
too smooth
→ late / wide corner
```

The final value should come from repeated physical tests.

---

# 4.7 Speed Management Through a Corner

The current prototype already uses speed as part of the controller:

```python
if wall_active:
    drive.run(wall_speed)

elif acquire_progress < 1.0:
    drive.run(ACQUIRE_SPEED)

elif abs(combined_offset) >= TURN_STEER_THRESHOLD:
    drive.run(TURN_SPEED)

else:
    drive.run(DRIVE_SPEED)
```

This principle is especially important during corner handling.

When steering demand becomes large:

```text
lower speed
→ more time for Motor B to reach target
→ shorter distance traveled during reaction
```

while:

```text
high speed
→ more distance traveled before steering takes effect
```

The corner controller can therefore select a specific speed state.

Conceptually:

```text
NORMAL
→ normal speed
```

```text
CORNER ENTRY
→ controlled speed
```

```text
CORNER
→ turn speed
```

```text
CORNER EXIT
→ progressively return to normal speed
```

The final speed values remain calibration parameters.

---

# 4.8 Ultrasonic Behavior Inside a Corner

<div align="center">

<img
  src="../../v-photos/v4/ultrasonic_lateral_alignment.jpg"
  alt="Piolín lateral ultrasonic sensor alignment"
  width="700"
/>

<br>

<sub><b>Figure 4.3.</b> The two ultrasonic sensors remain physically lateral, so their interpretation changes as the chassis rotates through a corner.</sub>

</div>

During a straight, the lateral ultrasonics observe approximately perpendicular wall geometry.

During a corner:

```text
vehicle rotates
      ↓
sensor beam orientation changes relative to walls
      ↓
distance readings change rapidly
```

This is why normal straight-line formulas should lose authority during the turn.

The current geometry controller already reduces confidence in the two-sensor straight estimate when:

```text
Di + Do
```

moves away from the expected corridor relationship.

The fused estimate is:

```python
x_est = (
    weight * x_two_us
    + (1.0 - weight) * x_inner
)
```

As `weight` decreases, the controller becomes less dependent on the assumption that both sensors describe the same straight corridor.

This is useful for corner entry and exit because the algorithm transitions progressively rather than treating geometry as either:

```text
completely valid
```

or:

```text
completely invalid
```

---

# 4.9 Corner Exit Is as Important as Corner Entry

A corner is not complete when Piolín has simply rotated enough to face approximately toward the next corridor.

A successful corner requires:

```text
turn completed
+
steering begins returning
+
new lateral geometry becomes usable
+
vehicle stabilizes
```

The intended sequence is:

```text
CORNER
   ↓
rotation / geometry reaches exit condition
   ↓
CORNER_EXIT
   ↓
reduce steering
   ↓
S2/S3 begin observing new corridor
   ↓
REACQUIRE
   ↓
NORMAL
```

This addresses one of the most common autonomous-navigation failures:

```text
turn itself succeeds
but bad exit causes the next collision
```

If Piolín completes a corner but immediately heads toward a wall, the engineering problem may be:

```text
CORNER EXIT
```

rather than:

```text
TURN STRENGTH
```

The two should be tuned separately.

---

# 4.10 Reacquiring Wall Geometry

After steering begins to return toward center, the ultrasonic measurements should gradually become useful for normal track-relative navigation again.

The controller can conceptually check:

```text
left distance plausible?

right distance plausible?

geometry coherence increasing?

steering demand reducing?
```

Once these conditions become sufficiently stable:

```text
CORNER_EXIT
      ↓
NORMAL
```

or, in a more explicit implementation:

```text
CORNER
      ↓
REACQUIRE
      ↓
NORMAL
```

The purpose of the reacquisition stage is to avoid switching immediately from:

```text
strong corner steering
```

to:

```text
strong wall-centering
```

because that abrupt change can create the same zig-zag behavior observed after other strong maneuvers.

---

# 4.11 Corners and Pixy2.1

<div align="center">

<img
  src="../../v-photos/v4/pixy21_front.jpg"
  alt="Piolín Pixy2.1 forward camera"
  width="680"
/>

<br>

<sub><b>Figure 4.4.</b> Pixy2.1 rotates with the vehicle, so visible pillar coordinates can change rapidly during a corner.</sub>

</div>

The Obstacle Challenge adds an important complication: the camera continues operating while the chassis turns.

During a corner:

```text
vehicle yaw changes
      ↓
camera yaw changes
      ↓
pillar x-position can change rapidly
      ↓
pillar may enter or leave the field of view
```

Therefore a large change in Pixy `x` during `CORNER` does not necessarily mean the pillar itself moved relative to the track.

It may simply reflect camera rotation.

The software should therefore interpret Pixy information in the context of the active navigation state.

During `NORMAL`:

```text
Pixy x
→ useful forward obstacle geometry
```

During `CORNER`:

```text
Pixy x
→ still useful
but affected strongly by vehicle rotation
```

This is another reason the state machine must exist.

The same camera observation can require a different interpretation depending on whether Piolín is:

```text
driving straight

turning

actively avoiding

recovering
```

---

# 4.12 Pillar Near a Corner

One of the more difficult situations occurs when Piolín detects a pillar close to a corner transition.

Possible objectives may include:

```text
complete corner

avoid pillar

avoid wall

reacquire corridor
```

The final arbitration is still being developed, but the software architecture should prevent:

```text
CORNER controller

PILLAR controller

NORMAL wall controller
```

from all commanding Motor B with full authority simultaneously.

A useful conceptual hierarchy is:

```text
CRITICAL WALL SAFETY
        ↓
ACTIVE COMMITTED MANEUVER
        ↓
next navigation objective
        ↓
normal wall correction
```

For example, if Piolín has already committed to a corner:

```text
CORNER
→ should remain coherent long enough
  to avoid random steering reversals
```

while Pixy can continue collecting information for the next target.

Once the corner exit becomes stable:

```text
Pixy target relevance can increase again
```

If a pillar is physically close enough that it cannot safely wait, the final controller may need a combined corner/avoidance strategy.

That interaction remains an active development area and should not yet be presented as a finalized algorithm.

---

# 4.13 Target Lock Through Corners

A pillar that was selected shortly before a corner should not automatically be forgotten because the camera temporarily loses it during chassis rotation.

The state machine can preserve:

```text
active_target

last known signature

last known visual geometry

recent target state
```

through a short transition.

This follows the same philosophy used elsewhere in Piolín:

```text
temporary sensor loss
≠
automatic state reset
```

The controller should distinguish:

```text
target temporarily lost because camera rotated
```

from:

```text
target physically passed
```

and from:

```text
target no longer relevant
```

The exact memory duration is a future calibration parameter.

---

# 4.14 Corner Direction and Course State

The early color prototype directly maps:

```text
BLUE
→ one turn direction
```

and:

```text
ORANGE
→ opposite turn direction
```

This was useful for testing a complete:

```text
detect → turn → center
```

sequence.

However, the final Obstacle architecture should keep a persistent course context rather than treating every color sample as an independent command.

The stronger architecture is:

```text
floor event
      ↓
course-state update
      ↓
corner expected?
      ↓
select required turn direction
      ↓
CORNER
```

rather than allowing the raw Color Sensor to control Motor B directly.

This keeps:

```text
S4
→ course information
```

separate from:

```text
Motor B
→ physical steering execution
```

---

# 4.15 Safety During a Corner

Wall safety remains active even when normal wall following is reduced.

The current prototype already implements a safety controller separately:

```python
wall_active, wall_cmd, wall_speed = side_wall_guard(
    left,
    right
)
```

and allows it to override the normal steering request:

```python
if wall_active:
    combined_offset = wall_cmd
```

The same principle applies during cornering.

A corner controller may request:

```text
continue left
```

but if a physical boundary becomes critically unsafe:

```text
wall safety
→ can temporarily limit or override the maneuver
```

The distinction is:

```text
NORMAL WALL FOLLOWING
→ trajectory preference
```

versus:

```text
WALL SAFETY
→ physical protection
```

Normal wall following should not fight the corner.

Critical wall safety should remain available.

---

# 4.16 Corner Debugging

A useful corner debug line should expose both perception and control state.

Possible information includes:

```text
STATE

COURSE DIRECTION

CORNER COUNT

S2

S3

GEOMETRY COHERENCE

PIXY TARGET

STEERING REQUEST

FINAL STEERING

MOTOR B ANGLE
```

For example:

```text
STATE: CORNER
TURN: 5
S2: ...
S3: ...
GEOM: ...
SIG: 2
CMD: LEFT
REAL: ...
```

This makes it possible to determine whether a failed corner originated from:

```text
wrong event detection

wrong state transition

wrong turn direction

weak steering

late steering

incorrect exit condition

wall-controller conflict

physical Motor B response
```

Video should ideally be matched with the same debug output.

---

# 4.17 Diagnosing Corner Failures

Corner problems should be separated into three categories.

### Entry

Symptoms:

```text
turn starts too late

turn starts too early

robot enters from poor lateral position
```

Check:

```text
course event timing

geometry change

vehicle speed

previous recovery state
```

---

### Turn

Symptoms:

```text
corner too wide

corner too tight

steering direction wrong

vehicle hits inside or outside boundary
```

Check:

```text
Motor B direction

steering target

turn speed

steering smoothing

safety override

mechanical steering response
```

---

### Exit

Symptoms:

```text
turn looks correct but next straight fails

vehicle exits angled

robot zig-zags after turn

wall correction becomes extreme
```

Check:

```text
steering release

reacquisition timing

S2/S3 geometry

transition back to NORMAL
```

The first incorrect stage should be corrected rather than compensating later.

---

# 4.18 Prototype Code vs. Final Corner Controller

The current programs provide real evidence for the architecture, but they are not the final Obstacle Challenge corner code.

The prototypes already demonstrate:

| Existing Pattern | Corner-Handling Use |
| :--- | :--- |
| Color confirmation | Confirm possible course event |
| `turn_for_color()` | Explicit maneuver phase |
| Dedicated `TURN_SPEED` | State-dependent corner speed |
| `center_steering()` | Controlled steering release |
| `smooth_target()` | Progressive corner entry/exit |
| Geometry `weight` | Detect reduced straight-corridor confidence |
| Wall safety override | Physical protection inside corner |
| Debug telemetry | Corner-state diagnosis |

The final implementation is expected to replace some purely timed behavior with additional physical evidence.

Parameters still under development include:

```text
final corner-entry condition

final steering magnitude

corner speed

turn duration or progression metric

corner-exit condition

ultrasonic reacquisition threshold

pillar/corner arbitration

post-corner target handling
```

These values should not be described as validated until repeated track testing supports them.

---

# 4.19 Intended Corner-Control Flow

The planned corner flow can be summarized as:

```text
                         NORMAL
                            │
                            ▼
                    COURSE EVENT?
                            │
                           YES
                            │
                            ▼
                  GEOMETRY CHANGING?
                            │
                           YES
                            │
                            ▼
                     CORNER ENTRY
                            │
                            ▼
             reduce normal wall authority
                            │
                            ▼
                  set corner steering
                            │
                            ▼
                  select corner speed
                            │
                            ▼
                         CORNER
                            │
             ┌──────────────┴──────────────┐
             │                             │
             ▼                             ▼
      critical wall?              exit evidence?
             │                             │
            YES                           YES
             │                             │
             ▼                             ▼
       SAFETY OVERRIDE               CORNER EXIT
                                           │
                                           ▼
                                  reduce steering
                                           │
                                           ▼
                                 S2/S3 reacquire
                                           │
                                           ▼
                                    geometry valid
                                           │
                                           ▼
                                        NORMAL
```

Throughout the sequence:

```text
Pixy2.1
→ continues observing
```

but its interpretation depends on the active state.

---

# 4.20 Final Engineering Assessment

Piolín's corner-handling strategy is evolving from a simple event-triggered timed turn into a **state-based physical transition between two track geometries**.

The early prototype proves the basic sequence:

```text
detect color
→ steer
→ drive through turn
→ center steering
→ continue
```

while the more advanced geometry controller introduces additional concepts:

```text
detect when straight geometry becomes less coherent

reduce confidence in normal two-wall assumptions

smooth steering commands

change speed according to steering demand

retain independent wall safety
```

The final Obstacle Challenge architecture combines these ideas.

A corner should therefore be understood as:

```text
CORNER ENTRY
+
CONTROLLED ROTATION
+
CORNER EXIT
+
GEOMETRY REACQUISITION
```

rather than simply:

```text
turn for N milliseconds
```

During `CORNER`, normal wall following should temporarily lose authority because the lateral ultrasonic measurements no longer represent the same straight-corridor geometry.

However:

```text
critical wall safety
```

remains available.

Pixy2.1 also remains active, but its image coordinates must be interpreted carefully because the camera rotates with the vehicle. A target moving rapidly through the image during a corner does not necessarily represent an equivalent physical movement of the pillar.

The interaction between:

```text
CORNER

PILLAR AVOIDANCE

TARGET LOCK

RECOVERY
```

is still one of the areas under active development and should remain explicitly documented as such until repeated obstacle-track testing validates the final transition logic.

The core corner-handling principle is:

> **Piolín should not treat a corner as a large straight-line error. The software should recognize that the track geometry itself is changing, temporarily change controller authority, execute the turn, and only return to normal wall following once the new corridor has been reacquired.**

This allows corner tuning to remain separate from normal wall control and obstacle avoidance, making the complete autonomous system easier to test, diagnose, and improve.

---

<div align="center">

### [← Back to PiolínTech Main README](../../README.md)

</div>
