# StateDiagram: UML Statecharts, Automata & Transitions

`StateDiagram` models behavioral state transitions, Finite State Machines (FSM), and UML 2.0 Statecharts. It provides dedicated pseudo-states, internal action compartments (`entry`, `do`, `exit`), and curved arc transitions.

---

## 1. Overview & Action Compartments

```text
    (Initial)
        │
        ▼
   ┌─────────┐      event [guard] / action
   │  Idle   ├─────────────────────────────────►┌──────────────┐
   └────▲────┘                                  │  Processing  │
        │           failure (bend=0.3)          ├──────────────┤
        └───────────────────────────────────────┤ entry/timer  │
                                                │ do/calculate │
                                                └──────────────┘
```

- **UML Action Compartments**: A `State` card can display internal behavior triggers (`entry`, `do`, `exit`) below a divider line.
- **Pseudo-States**:
  - `InitialState`: Solid black circle indicating system start.
  - `FinalState`: Bullseye concentric circles indicating termination.
  - `ChoiceState`: Diamond shape for dynamic conditional branching.
  - `ForkJoinState`: Solid synchronization bar for concurrent state splits and joins.
- **Standard Transition Syntax**: Transition labels automatically format as `event [guard] / action`.
- **Bidirectional Arcs (`bend`)**: Setting `bend=0.3` creates smooth curved lines, allowing bidirectional transitions between the same pair of states without overlapping.

---

## 2. Constructor & Core Classes

```python
from drawlib.diagrams.state import (
    ChoiceState,
    FinalState,
    ForkJoinState,
    InitialState,
    State,
    StateDiagram,
)
from drawlib.styles import Styles

sd = StateDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark,
    title="Session Lifecycle State Machine",
)

# State with action compartments
active = sd.add(
    State("Active", shape="box", entry="start_heartbeat()", do="handle_requests()", exit="flush()", style=Styles.PrimaryNeutral),
    xy=(60.0, 40.0),
)

# Transition with guard and action
init = sd.add(InitialState(), xy=(10.0, 40.0))
sd.connect(init, active, event="login", guard="token_valid", action="init_session()")
```

---

## 3. Session Lifecycle State Machine

The following complete example showcases pseudo-states, choice diamonds, action compartments, a self-loop, and curved return transitions:

```drawlib 650px center file:state_user_session_lifecycle.png caption:"User Session Lifecycle State Machine"
from drawlib import canvas
from drawlib.diagrams.state import ChoiceState, FinalState, InitialState, State, StateDiagram
from drawlib.styles import Styles

canvas.clear()
canvas.setup(width=142, height=75)

sd = StateDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark,
    title="User Session Lifecycle State Machine",
)

# 1. Pseudo-states and state nodes
init = sd.add(InitialState(), xy=(12.0, 38.0))
idle = sd.add(
    State("Idle", shape="box", entry="reset()", do="listen()", width=22.0),
    xy=(38.0, 38.0),
)
valid_check = sd.add(ChoiceState(name="Valid?", style=Styles.SecondaryNeutral), xy=(72.0, 38.0))
active = sd.add(
    State(
        "Active",
        shape="box",
        entry="start()",
        do="handle()",
        exit="flush()",
        style=Styles.PrimaryNeutral,
        width=22.0,
    ),
    xy=(105.0, 38.0),
)
final = sd.add(FinalState(), xy=(132.0, 38.0))

# 2. Connect transitions
sd.connect(init, idle)
sd.connect(idle, valid_check, event="login")

# Choice branches (success vs failure)
sd.connect(valid_check, active, guard="valid")
sd.connect(
    valid_check,
    idle,
    guard="invalid",
    bend=-0.35,
    start_side="bottom",
    end_side="bottom",
    text_style=Styles.Dark.patch(text_valign="top"),
)

# Self-transition heartbeat loop
sd.connect(active, active, side="top", event="ping", action="extend()")

# Termination
sd.connect(active, final, event="logout")

sd.draw(xy=(0.0, 0.0))
```

---

## 4. Concurrent Task Synchronization (Fork & Join)

Use `ForkJoinState` to represent concurrent parallel threads:

```drawlib 650px center file:state_concurrent_task_sync.png caption:"Concurrent Task Synchronization with Fork and Join"
from drawlib import canvas
from drawlib.diagrams.state import FinalState, ForkJoinState, InitialState, State, StateDiagram
from drawlib.styles import Styles

canvas.clear()
canvas.setup(width=115, height=75)

sd = StateDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark,
    title="Concurrent Task Fork and Join",
)

init = sd.add(InitialState(), xy=(10.0, 37.5))
fork = sd.add(ForkJoinState(orientation="vertical", length=22.0), xy=(25.0, 37.5))
job_a = sd.add(State("Compute Analytics", shape="box", width=28.0, style=Styles.PrimaryNeutral), xy=(55.0, 50.0))
job_b = sd.add(State("Index Search", shape="box", width=28.0, style=Styles.SecondaryNeutral), xy=(55.0, 25.0))
join = sd.add(ForkJoinState(orientation="vertical", length=22.0), xy=(85.0, 37.5))
final = sd.add(FinalState(), xy=(105.0, 37.5))

sd.connect(init, fork)
sd.connect(fork, job_a)
sd.connect(fork, job_b)
sd.connect(job_a, join)
sd.connect(job_b, join)
sd.connect(join, final)

sd.draw(xy=(0.0, 0.0))
```

---

## 5. Best Practices & Guidelines

1. **Use `bend` for Opposing Transitions**: When two states transition back and forth (e.g. `Idle` ↔ `Active`), apply `bend=0.25` on one transition and `bend=-0.25` on the return so they do not overlap.
2. **Standard Label Formatting**: Prefer passing `event`, `guard`, and `action` parameters rather than writing `label="login [valid] / init"`. Drawlib guarantees standard UML typography and spacing.
3. **Choice Diamond Clarity**: Label exit branches from `ChoiceState` with explicit `guard` criteria (`guard="is_valid"` vs `guard="is_invalid"`).
