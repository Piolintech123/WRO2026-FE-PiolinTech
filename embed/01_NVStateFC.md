# Piolín Navigation State Flowchart

This flowchart summarizes the high-level navigation logic used for Piolín's **Obstacle Challenge** architecture.

```mermaid
flowchart TD

    START([START])

    INIT["Initialize Robot<br/>• Reset state variables<br/>• Center steering<br/>• Read sensors<br/>• Initialize Pixy2.1"]
    
    ACQUIRE["ACQUIRE<br/>Establish safe initial course geometry"]
    
    NORMAL["NORMAL<br/>Wall geometry control<br/>Course progression monitoring<br/>Pixy target search"]
    
    TARGET{"Relevant pillar<br/>candidate detected?"}
    
    TARGET_ACQUIRE["TARGET_ACQUIRE<br/>Validate signature<br/>Evaluate relevance<br/>Confirm candidate"]
    
    CONFIRMED{"Target<br/>confirmed?"}
    
    AVOID["AVOID<br/>Execute required pillar trajectory<br/><br/>Red → PASS RIGHT<br/>Green → PASS LEFT"]
    
    PASSED{"Pillar physically<br/>passed?"}
    
    PASS_CONFIRM["PASS_CONFIRM<br/>Use Pixy history + S2/S3<br/>to verify clearance"]
    
    PASS_OK{"Pass<br/>confirmed?"}
    
    RECOVER["RECOVER<br/>Countersteer<br/>Reacquire safe lateral geometry"]
    
    RECOVERED{"Geometry<br/>recovered?"}
    
    CORNER_Q{"Corner evidence<br/>detected?"}
    
    CORNER["CORNER<br/>Reduce straight-wall assumptions<br/>Execute corner trajectory"]
    
    CORNER_EXIT{"New corridor<br/>acquired?"}
    
    COURSE_DONE{"Required course<br/>progress complete?"}
    
    PARK_SEARCH["PARKING ELIGIBLE<br/>Continue navigation while<br/>searching for Pink sig1"]
    
    PINK{"Pink parking target<br/>confirmed?"}
    
    PARKING["PARKING<br/>APPROACH → ENTRY → ALIGN → FINAL"]
    
    PARK_DONE{"Final parking<br/>condition valid?"}
    
    STOP([STOP<br/>Terminal State])

    SAFETY{"Critical wall<br/>danger?"}
    
    SAFETY_ACTION["WALL SAFETY OVERRIDE<br/>Limit steering / speed<br/>protect physical clearance"]


    START --> INIT
    INIT --> ACQUIRE
    ACQUIRE --> NORMAL

    NORMAL --> SAFETY

    SAFETY -- "YES" --> SAFETY_ACTION
    SAFETY_ACTION --> NORMAL

    SAFETY -- "NO" --> COURSE_DONE

    COURSE_DONE -- "YES" --> PARK_SEARCH
    COURSE_DONE -- "NO" --> CORNER_Q

    PARK_SEARCH --> PINK
    PINK -- "YES" --> PARKING
    PINK -- "NO" --> NORMAL

    PARKING --> PARK_DONE
    PARK_DONE -- "YES" --> STOP
    PARK_DONE -- "NO" --> PARKING

    CORNER_Q -- "YES" --> CORNER
    CORNER_Q -- "NO" --> TARGET

    CORNER --> CORNER_EXIT
    CORNER_EXIT -- "YES" --> NORMAL
    CORNER_EXIT -- "NO" --> CORNER

    TARGET -- "YES" --> TARGET_ACQUIRE
    TARGET -- "NO" --> NORMAL

    TARGET_ACQUIRE --> CONFIRMED
    CONFIRMED -- "YES" --> AVOID
    CONFIRMED -- "NO" --> NORMAL

    AVOID --> PASSED
    PASSED -- "NO" --> AVOID
    PASSED -- "POSSIBLE" --> PASS_CONFIRM

    PASS_CONFIRM --> PASS_OK
    PASS_OK -- "NO" --> AVOID
    PASS_OK -- "YES" --> RECOVER

    RECOVER --> RECOVERED
    RECOVERED -- "NO" --> RECOVER
    RECOVERED -- "YES" --> NORMAL
```

---

## State Meaning

| State | Main Responsibility |
| :--- | :--- |
| `START` | Program entry point |
| `ACQUIRE` | Establish usable initial course geometry |
| `NORMAL` | Normal navigation, wall geometry, target search, and course monitoring |
| `TARGET_ACQUIRE` | Validate and confirm a relevant Pixy obstacle |
| `AVOID` | Execute the required Red/Green passing trajectory |
| `PASS_CONFIRM` | Verify that the active pillar has physically been cleared |
| `RECOVER` | Restore stable track geometry after avoidance |
| `CORNER` | Handle course geometry where straight-wall assumptions are temporarily invalid |
| `PARKING ELIGIBLE` | Course progression is complete and Pink parking detection may now become authoritative |
| `PARKING` | Perform approach, entry, alignment, and final positioning |
| `STOP` | Terminal state; autonomous navigation does not resume |

---

## Fixed Obstacle Rules

```text
Pixy sig2
→ RED
→ PASS RIGHT
```

```text
Pixy sig3
→ GREEN
→ PASS LEFT
```

The pillar's horizontal image position does **not** change the required passing side.

```text
signature
→ determines competition rule

x / y / width / height
→ describe target geometry and relevance
```

---

## Controller Priority

The state machine determines which navigation controller has primary authority.

```text
CRITICAL WALL SAFETY
        ↓
ACTIVE STATE CONTROLLER
        ↓
NORMAL NAVIGATION
```

Examples:

```text
NORMAL
→ wall geometry control
```

```text
AVOID
→ obstacle trajectory
```

```text
CORNER
→ corner handling
```

```text
RECOVER
→ post-pillar recentering
```

```text
PARKING
→ terminal parking controller
```

Critical wall safety remains independent so that a committed maneuver cannot freely continue into an unsafe physical boundary.

---

## Navigation Sequence

The main obstacle-navigation cycle is:

```text
NORMAL
   ↓
TARGET_ACQUIRE
   ↓
AVOID
   ↓
PASS_CONFIRM
   ↓
RECOVER
   ↓
NORMAL
```

Corner handling forms a second loop:

```text
NORMAL
   ↓
CORNER
   ↓
NORMAL
```

Once course progression is complete:

```text
NORMAL
   ↓
PARKING ELIGIBLE
   ↓
Pink sig1 confirmed
   ↓
PARKING
   ↓
STOP
```

`STOP` is terminal and does not transition back to normal navigation.
