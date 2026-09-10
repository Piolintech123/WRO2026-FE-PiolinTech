# Round 2 EV3 V1 — Current Pixy2.1 Detection Code Explanation

This document explains the logic implemented in [`ev3v1.py`](./ev3v1.py), the Round 2 program currently published in the PiolínTech repository for testing and validating the **Pixy2.1 vision subsystem** used during the WRO Future Engineers 2026 Obstacle Challenge.

The most important point is that this file should be documented according to what it actually does. It is **not** a complete autonomous Obstacle Challenge controller. The current file initializes Pixy2.1 on EV3 sensor port S1, waits for a deliberate start input, reads detected color blocks, chooses the largest returned block, reports its signature and geometry, and displays the required passing side for recognized Red or Green targets.

This makes the program a current and useful Round 2 vision-validation program. It proves that the EV3 can communicate directly with Pixy2.1 and that the software can obtain the block information required for later obstacle navigation.

It should not be described as a four-phase autonomous driving state machine, ultrasonic wall-following controller, odometry system, or parking controller because those behaviors are not implemented in this exact source file.

---

## Purpose of This Program

The purpose of `ev3v1.py` is to validate the communication path:

```text
Pixy2.1
   ↓
EV3 Sensor Port S1
   ↓
Pybricks program
   ↓
Block detection data
   ↓
Signature interpretation
   ↓
EV3 screen + sound feedback
```

Before a vision sensor can be trusted inside an autonomous driving controller, the team first needs to know that the EV3 can create the Pixy object, request blocks, receive valid data, identify the detected signature, and expose useful image-space information.

This program isolates that problem from propulsion and steering.

That isolation is useful during engineering development because a failed camera test cannot be confused with a drivetrain, steering, wall-control, or parking failure.

---

## Hardware Used by This Program

The exact file directly initializes only the EV3 Brick and Pixy2.1.

| Connection | Component | Function in This File |
|---|---|---|
| EV3 | LEGO MINDSTORMS EV3 Brick | Runs the program and displays diagnostics |
| S1 | Pixy2.1 | Detects trained color signatures and reports blocks |

The file does **not** initialize Motor A, Motor B, S2, S3, or S4.

Therefore, those systems do not participate in the execution of this exact program.

This distinction is important when reading the broader PiolínTech documentation. The physical Obstacle Challenge robot may include propulsion, steering, lateral ultrasonic sensing, and floor sensing, but this particular source file is dedicated to validating Pixy2.1 communication and block interpretation.

---

## Software Environment

The program runs with Pybricks MicroPython and imports:

```python
from pybricks.hubs import EV3Brick
from pybricks.parameters import Button
from pybricks.tools import wait

from pixycamev3.pixy2 import Pixy2
```

The Pybricks modules provide access to the EV3 Brick, buttons, timing, screen, light, and speaker.

The `pixycamev3.pixy2` library provides the `Pixy2` class used to communicate with the camera.

The program then creates the EV3 object:

```python
EV3 = EV3Brick()
```

This EV3 object is used for all user-visible diagnostic feedback.

---

## Pixy2.1 Port Configuration

Pixy2.1 is connected to the EV3 through sensor port S1.

The file defines:

```python
PIXY_PORT = 1
```

and:

```python
PIXY_I2C_ADDRESS = 0x54
```

The camera is then created with:

```python
PIXY = Pixy2(
    port=PIXY_PORT,
    i2c_address=PIXY_I2C_ADDRESS
)
```

This initialization step is one of the most important parts of the program because it verifies that the EV3 can create the Pixy interface before attempting to read any blocks.

---

## Current Signature Mapping Inside This File

The code currently contains:

```python
# Signature 1 = rojo
# Signature 2 = verde

SIG_RED = 1
SIG_GREEN = 2
```

Therefore, **inside this exact source file** the interpretation is:

```text
Signature 1
→ RED
→ PASS RIGHT
```

and:

```text
Signature 2
→ GREEN
→ PASS LEFT
```

This documentation intentionally follows the source code exactly.

> [!IMPORTANT]
> Other PiolínTech documents may describe a newer or intended Pixy configuration in which Pink parking, Red, and Green use a different signature numbering scheme. If PixyMon has since been retrained to a different signature map, the constants in `ev3v1.py` and this document should be updated together. The GitHub documentation should never claim one signature mapping while the running program uses another.

The passing rule itself remains clear in this program:

```text
RED
→ PASS RIGHT

GREEN
→ PASS LEFT
```

---

## Program Startup

When the script begins, it clears the EV3 screen and displays:

```text
PIXY TEST
IMPORT OK
```

This confirms that the program reached the initialization stage and successfully imported the required modules.

The program then waits briefly:

```python
wait(700)
```

before attempting to create the Pixy2.1 object.

This makes startup easier to observe on the EV3 screen.

---

## Pixy Creation Test

The camera initialization is placed inside a `try` block.

```python
try:

    PIXY = Pixy2(
        port=PIXY_PORT,
        i2c_address=PIXY_I2C_ADDRESS
    )
```

If successful, the EV3 displays:

```text
PIXY CREATED
PRESS RIGHT
```

and produces a confirmation beep.

This gives the team a simple physical indication that the camera interface was created successfully.

The program does not begin continuous block reading immediately. It requires a deliberate button press first.

---

## Initialization Error Handling

If Pixy2.1 cannot be created, the program catches the exception:

```python
except Exception as error:
```

The EV3 then displays:

```text
CREATE ERROR
```

along with the exception type and part of the error message.

The program also prints more complete diagnostic information to the console:

```python
print("CREATE ERROR")
print("TYPE:", type(error))
print("DETAIL:", repr(error))
```

A lower-frequency beep indicates that the initialization failed.

The program then enters:

```python
freeze()
```

which keeps the script alive rather than allowing it to exit immediately.

This is useful during debugging because the failure message remains available for inspection.

---

## The `freeze()` Function

The helper function is:

```python
def freeze():

    while True:
        wait(1000)
```

Its purpose is not navigation.

It simply prevents the program from ending after a critical initialization error.

This allows the diagnostic state to remain visible on the EV3.

---

## Deliberate Start Using the Right Button

After Pixy2.1 is created successfully, the program waits for the EV3 Right button.

```python
while Button.RIGHT not in EV3.buttons.pressed():
    wait(20)
```

It then waits until the button is released:

```python
while Button.RIGHT in EV3.buttons.pressed():
    wait(20)
```

This creates a deliberate start sequence.

The camera-reading loop therefore begins only after the operator confirms that Piolín is ready for the vision test.

The screen then displays:

```text
READING PIXY
```

before the continuous read loop begins.

---

## Continuous Pixy2.1 Reading Loop

The main operation of the file occurs inside:

```python
while True:
```

This loop continuously requests blocks from Pixy2.1.

The important call is:

```python
block_count, blocks = PIXY.get_blocks(
    3,
    5
)
```

The first argument is a signature mask used by the current program to request the configured Red and Green signatures.

The second argument limits the number of returned blocks to five.

The program then displays:

```text
READ OK
BLOCKS: <count>
```

so the team can immediately see whether Pixy2.1 is returning visible objects.

---

## Why the Program Requests Multiple Blocks

Pixy2.1 can return more than one detected color block.

This matters because a camera frame may contain several regions that match trained signatures.

The current file therefore does not assume that the first returned block is automatically the most important one.

Instead, it evaluates the returned block list.

This is a useful first step toward obstacle-target selection.

---

## Largest-Block Selection

When at least one block exists, the program begins with:

```python
largest_block = blocks[0]
largest_area = 0
```

It then loops through the detected blocks:

```python
for block in blocks:
```

and calculates:

```python
area = (
    block.width
    * block.height
)
```

If the current block has a larger area than the previous best candidate, it becomes the new selected block.

```python
if area > largest_area:

    largest_area = area
    largest_block = block
```

The result is that the program selects the **largest block returned by Pixy2.1**.

This is not a complete physical-distance calculation, but block area is useful as a simple image-space relevance indicator.

A larger visible block often represents a target that occupies more of the camera frame.

The program does not convert this area into centimeters or claim that area alone is a calibrated physical distance.

---

## Information Extracted from the Selected Block

Once the largest block has been selected, the program extracts:

```python
signature = largest_block.sig
x = largest_block.x_center
y = largest_block.y_center
width = largest_block.width
height = largest_block.height
```

It also retains:

```python
largest_area
```

which was calculated from width multiplied by height.

The complete useful output is therefore:

```text
signature
x center
y center
width
height
area
```

This is important because obstacle perception requires more information than only a color name.

---

## Signature

The signature identifies which trained Pixy color class produced the selected block.

In the exact current file:

```text
1 = Red
2 = Green
```

The signature is used to decide which competition passing rule applies.

The program does not use x-position to decide whether Red should be passed right or Green should be passed left.

The color identity determines that rule.

---

## Horizontal Position — `x`

The value:

```python
x = largest_block.x_center
```

describes the horizontal center of the selected block inside the Pixy image.

A block appearing on the left side of the camera frame will have a different x-coordinate from one appearing near the center or right side.

This coordinate can later be useful for trajectory planning, target relevance, or obstacle-position analysis.

In the current file, however, x is **reported for diagnostics** and is not yet converted into a steering command.

---

## Vertical Position — `y`

The value:

```python
y = largest_block.y_center
```

describes the vertical center of the block inside the image.

Like x, this is image-space information.

The current program displays and prints the value, but does not use it to control the robot.

---

## Width and Height

The code reads:

```python
width = largest_block.width
height = largest_block.height
```

These values describe the bounding-box dimensions reported by Pixy2.1.

They are also used indirectly because:

```python
area = width * height
```

determines which block is selected as the largest candidate.

Width and height can become useful in later obstacle logic because the apparent size of a pillar changes as the robot approaches it.

However, the current file does not contain a calibrated width-to-distance or height-to-distance conversion.

---

## Area

The program calculates:

```python
largest_area
```

as:

```text
width × height
```

This provides a compact measure of how much image space the selected block occupies.

The area is printed to the console for testing and analysis.

The current program uses area only for selecting the largest returned block.

It does not use an area threshold to trigger an autonomous steering maneuver.

---

## Red Detection Behavior

If:

```python
signature == SIG_RED
```

the EV3 displays:

```text
RED
PASS RIGHT
```

and produces a short low-frequency beep.

This is the correct competition-side interpretation implemented by the file:

```text
RED
→ PASS RIGHT
```

The program communicates the desired passing side to the operator but does not command Motor B because no steering motor is initialized in this file.

---

## Green Detection Behavior

If:

```python
signature == SIG_GREEN
```

the EV3 displays:

```text
GREEN
PASS LEFT
```

and produces a higher-frequency beep.

The implemented rule is:

```text
GREEN
→ PASS LEFT
```

Again, the program identifies the correct required side but does not physically steer the robot.

---

## Other Signatures

The code includes:

```python
else:

    EV3.screen.print("OTHER COLOR")
```

This means that a returned signature that is neither the configured Red nor Green class is not interpreted as a competition pillar by this file.

The current source does not contain Pink parking logic.

If Pink parking is added to the actual PixyMon configuration and program, that behavior should be documented only after it exists in the source code.

---

## Console Diagnostic Output

For each selected block, the program prints:

```python
print(
    "SIG:", signature,
    "X:", x,
    "Y:", y,
    "WIDTH:", width,
    "HEIGHT:", height,
    "AREA:", largest_area
)
```

This diagnostic output is valuable because it exposes the raw perception information used during camera testing.

A test can therefore compare what the robot physically sees with what the software reports.

For example:

```text
SIG: 1
X: 155
Y: 130
WIDTH: 32
HEIGHT: 85
AREA: 2720
```

would indicate one selected block with the corresponding image geometry.

The numeric example above is only illustrative. Actual testing data should come from the physical camera output.

---

## No-Object Condition

If:

```python
block_count <= 0
```

the EV3 displays:

```text
NO OBJECT
```

and the program also prints:

```text
NO OBJECT
```

to the console.

This gives a clear distinction between:

```text
camera communication working
+
no valid visible blocks
```

and:

```text
camera communication failure
```

The two conditions should not be treated as the same problem during debugging.

---

## Block-Read Error Handling

The continuous read loop has its own exception handler.

If a Pixy read operation fails, the program displays:

```text
BLOCK ERROR
```

followed by the exception type and part of the error message.

It also prints more complete information to the console.

A short low-frequency beep provides audible feedback.

The program then waits:

```python
wait(1000)
```

before attempting another read.

This means a temporary read error does not automatically terminate the entire program.

---

## Main Program Flow

The complete current logic can be summarized as:

```text
START SCRIPT
      ↓
IMPORT LIBRARIES
      ↓
CREATE EV3
      ↓
CREATE PIXY2.1 ON S1
      ↓
CREATION SUCCESSFUL?
   ┌───────┴────────┐
   │                │
  NO               YES
   │                │
SHOW ERROR      PRESS RIGHT
   │                │
FREEZE              ↓
              READ PIXY BLOCKS
                    ↓
              ANY BLOCKS?
              ┌─────┴─────┐
              │           │
             NO          YES
              │           │
        SHOW NO OBJECT    ↓
                    CHOOSE LARGEST
                          ↓
               READ SIG / X / Y / W / H
                          ↓
                  INTERPRET SIGNATURE
                  ┌───────┴────────┐
                  │                │
                RED              GREEN
                  │                │
             PASS RIGHT        PASS LEFT
                  │                │
                  └───────┬────────┘
                          ↓
                    PRINT DATA
                          ↓
                       REPEAT
```

---

## What This Program Currently Does

The exact current file provides several important functions.

It verifies the Pixy2.1 import and library connection.

It attempts to create the Pixy2.1 object on S1.

It provides visible and audible feedback if camera creation fails.

It waits for a deliberate Right-button start.

It continuously requests blocks from the camera.

It can receive several blocks in one request.

It chooses the largest block by image area.

It extracts signature, x, y, width, and height.

It calculates block area.

It identifies Red and Green according to the constants stored in the file.

It reports:

```text
RED → PASS RIGHT
GREEN → PASS LEFT
```

and it prints diagnostic information that can be used during camera testing.

---

## What This Program Does Not Currently Do

Accurate documentation is especially important here.

The current `ev3v1.py` does **not** initialize or control Motor A.

It does **not** initialize or control Motor B.

It does **not** read S2 or S3 Ultrasonic Sensors.

It does **not** read the S4 Color Sensor.

It does **not** contain wall following.

It does **not** contain a propulsion controller.

It does **not** contain steering control.

It does **not** implement a pillar-avoidance trajectory.

It does **not** implement target memory.

It does **not** implement pass confirmation.

It does **not** implement post-pillar recovery.

It does **not** implement corner handling.

It does **not** count laps or floor markings.

It does **not** implement parking.

It does **not** calculate physical odometry.

It does **not** contain the four-phase autonomous state machine previously described in the old `r2_exp.md`.

These are not criticisms of the file. They define its real scope.

The current file is a focused **Pixy2.1 perception and diagnostic program**.

---

## Why This Scope Is Still Valuable

A full obstacle controller depends on reliable perception.

If the camera cannot be initialized consistently or the EV3 cannot correctly read signature and block geometry, then adding steering and wall control only makes the source of a failure harder to isolate.

This program therefore validates an important subsystem independently:

```text
Does Pixy initialize?
      ↓
Does Pixy return blocks?
      ↓
Which signature is detected?
      ↓
Where is the block?
      ↓
How large is it?
      ↓
Does the EV3 interpret its color rule correctly?
```

Only after these questions are understood does it make sense to connect the perception output to a physical avoidance maneuver.

This reflects a useful systems-engineering principle:

> **Validate a subsystem independently before allowing it to control the complete robot.**

---

## Largest Block as the Current Selection Rule

The current target-selection rule is simple:

```text
all returned blocks
      ↓
calculate width × height
      ↓
choose largest area
```

This is a valid development strategy because it avoids blindly taking the first block returned by the camera.

However, it is still a simplified relevance rule.

The largest block is not guaranteed to be the physically correct target in every possible multi-object arrangement.

A more advanced controller could later consider:

```text
signature validity
+
area
+
x position
+
y position
+
previous target
+
physical course state
```

but those additional behaviors should only be described as implemented after they appear in the actual source code.

---

## Relationship Between Signature and Passing Side

One of the strongest ideas already present in the program is that **color identity determines the required passing side**.

The current file explicitly maps:

```text
RED
→ RIGHT
```

and:

```text
GREEN
→ LEFT
```

This is important because image position and passing rule are different concepts.

A Red pillar can appear at different x-coordinates as the vehicle moves.

That does not change the fact that the required side is right.

Likewise, a Green pillar can move across the camera frame without changing its required left-side pass.

The current program correctly separates:

```text
signature
→ rule identity
```

from:

```text
x / y / width / height
→ image geometry
```

even though the image geometry is currently diagnostic rather than connected to steering.

---

## Relationship to the Physical Obstacle Robot

The broader Obstacle Challenge robot uses the same EV3 as its main controller and uses Pixy2.1 as the round-specific S1 sensing device.

The complete physical configuration can include:

```text
Motor A
→ rear propulsion

Motor B
→ Ackermann steering

S1
→ Pixy2.1

S2
→ left Ultrasonic Sensor

S3
→ right Ultrasonic Sensor

S4
→ Color Sensor
```

However, this `ev3v1.py` file does not initialize all of those devices.

Therefore, the hardware table at the top of this explanation intentionally distinguishes between:

```text
physical robot hardware
```

and:

```text
hardware actively used by this exact file
```

That distinction keeps the documentation honest and reproducible.

---

## Important Signature-Configuration Check

Before using this program, the PixyMon signature configuration must match the constants in the source file.

The current file expects:

```python
SIG_RED = 1
SIG_GREEN = 2
```

If the physical camera is instead trained as:

```text
Signature 1 = Pink
Signature 2 = Red
Signature 3 = Green
```

then the current constants are no longer consistent with the camera.

That would create an interpretation error even if the camera itself detected the colors correctly.

The correct engineering response is not to hide the discrepancy.

The camera configuration, constants, and documentation should all use the same mapping.

---

## Engineering Test Uses

This program is particularly useful for testing the following questions.

### Camera Initialization

Does Pixy2.1 initialize consistently when connected to S1?

### Signature Recognition

Does the camera return the expected signature for the visible pillar?

### Red / Green Separation

Can the camera distinguish the two competition pillar colors under the actual lighting conditions?

### Block Position

How do x and y change as the pillar moves through the field of view?

### Block Size

How do width, height, and area change as the pillar approaches or moves away?

### Multiple Blocks

When several blocks are visible, does selecting the largest region correspond to the most relevant physical target?

### Error Recovery

Does the program continue attempting reads after a temporary camera exception?

These tests can be performed without introducing drivetrain and steering behavior into the experiment.

---

## Suggested Diagnostic Record

When using the current file for testing, a useful record is:

| Field | Example |
|---|---|
| Physical target | Red / Green |
| Camera signature | Actual returned value |
| X center | Actual output |
| Y center | Actual output |
| Width | Actual output |
| Height | Actual output |
| Area | Width × Height |
| Lighting condition | Description |
| Position | Left / center / right |
| Approximate distance | Measured physical reference |
| Correct classification? | Yes / No |

The table should be filled only with real measured test data.

No detection accuracy percentage should be published unless enough trials were actually recorded to calculate it.

---

## Comparison With the Previous `r2_exp.md`

The previous explanation described features that are not present in `ev3v1.py`, including a four-phase obstacle-driving state machine, ultrasonic wall tracking, blended steering, wheel odometry, three-lap validation, and automated parking.

Those descriptions made the documentation appear more advanced than the source code and created a direct reproducibility problem.

The corrected explanation follows the implementation instead.

The relationship is now:

```text
DOCUMENTATION
      ↓
describes the same behavior as
      ↓
SOURCE CODE
      ↓
which can be checked on
      ↓
PHYSICAL PIXY2.1 + EV3
```

That consistency is more valuable than claiming features that are not implemented in the file.

---

## Current Development Status

`ev3v1.py` should be understood as the **current Round 2 Pixy2.1 detection and diagnostic program published by PiolínTech**.

It is current in the sense that it represents the code presently stored and used for this Round 2 vision-validation task.

It is not a complete autonomous Round 2 driving solution.

If PiolínTech later replaces this file with a controller that also drives Motor A, commands Motor B, reads the lateral Ultrasonic Sensors, processes course markings, performs obstacle maneuvers, or parks, this explanation must be updated to match that new implementation.

This avoids creating another mismatch between documentation and source code.

---

## Round 2 EV3 V1 Summary

The current Round 2 `ev3v1.py` is a focused Pixy2.1 perception program.

It initializes the EV3 and Pixy2.1, verifies camera creation, waits for the EV3 Right button, requests visible blocks, selects the largest block by bounding-box area, extracts signature and geometry information, displays the selected block, and reports the correct passing objective for the configured Red and Green signatures.

Its core behavior can be summarized as:

```text
PIXY2.1 ON S1
      ↓
CREATE CAMERA
      ↓
PRESS RIGHT
      ↓
READ BLOCKS
      ↓
SELECT LARGEST
      ↓
GET:
SIG + X + Y + WIDTH + HEIGHT + AREA
      ↓
RED?
→ PASS RIGHT

GREEN?
→ PASS LEFT
      ↓
DISPLAY + PRINT
      ↓
REPEAT
```

The file provides direct evidence that Piolín's EV3 can receive and interpret Pixy2.1 block data.

It should therefore be presented as a current and useful **vision-subsystem validation program**, while the documentation should avoid attributing autonomous driving functions to it that are not present in the source.

---

<div align="center">

### [View `ev3v1.py`](./ev3v1.py)

<br>

### [← Back to PiolínTech Main README](../../README.md)

</div>
