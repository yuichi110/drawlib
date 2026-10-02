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
from drawlib.diagrams.state_diagram import (
    ChoiceState,
    FinalState,
    ForkJoinState,
    InitialState,
    State,
    StateDiagram,
)
from drawlib.styles import Styles

sd = StateDiagram(
    node_style=Styles.PrimaryFlat,
    edge_style=Styles.Primary,
    title="Session Lifecycle State Machine",
)

# State with action compartments
active = sd.add(
    State("Active", shape="box", entry="start_heartbeat()", do="handle_requests()", exit="flush()"),
    xy=(60.0, 40.0),
)

# Transition with guard and action
init = sd.add(InitialState(), xy=(10.0, 40.0))
init.to(active, event="login", guard="token_valid", action="init_session()")
```

---

## 3. Session Lifecycle State Machine

The following complete example showcases pseudo-states, choice diamonds, action compartments, a self-loop, and curved return transitions:

```drawlib 650px center file:state_user_session_lifecycle.png caption:"User Session Lifecycle State Machine"
from drawlib import canvas
from drawlib.diagrams.state_diagram import ChoiceState, FinalState, InitialState, State, StateDiagram
from drawlib.styles import Styles

canvas.clear()
canvas.setup(width=135, height=75)

sd = StateDiagram(
    node_style=Styles.PrimaryFlat,
    edge_style=Styles.Primary,
    title="User Session Lifecycle State Machine",
)

# 1. Pseudo-states and state nodes
init = sd.add(InitialState(), xy=(12.0, 38.0))
idle = sd.add(
    State("Idle", shape="box", entry="reset_timeout()", do="listen_events()"),
    xy=(35.0, 38.0),
)
valid_check = sd.add(ChoiceState(name="Valid?"), xy=(70.0, 38.0))
active = sd.add(
    State("Active", shape="box", entry="start_heartbeat()", do="handle_requests()", exit="flush()"),
    xy=(102.0, 38.0),
)
final = sd.add(FinalState(), xy=(126.0, 38.0))

# 2. Connect transitions
init.to(idle)
idle.to(valid_check, event="login", guard="token_present")

# Choice branches (success vs failure with curved arc)
valid_check.to(active, guard="token_valid")
valid_check.to(idle, guard="token_invalid", bend=0.3)

# Self-transition heartbeat loop
active.loop(side="top", event="ping", action="extend_lease()")

# Termination
active.to(final, event="logout")

sd.draw(xy=(0.0, 0.0))
```

---

## 4. Concurrent Task Synchronization (Fork & Join)

Use `ForkJoinState` to represent concurrent parallel threads:

```drawlib 650px center file:state_concurrent_task_sync.png caption:"Concurrent Task Synchronization with Fork and Join"
from drawlib import canvas
from drawlib.diagrams.state_diagram import FinalState, ForkJoinState, InitialState, State, StateDiagram
from drawlib.styles import Styles

canvas.clear()
canvas.setup(width=115, height=75)

sd = StateDiagram(
    node_style=Styles.PrimaryFlat,
    edge_style=Styles.Primary,
    title="Concurrent Task Fork and Join",
)

init = sd.add(InitialState(), xy=(10.0, 37.5))
fork = sd.add(ForkJoinState(orientation="vertical", length=22.0), xy=(25.0, 37.5))
job_a = sd.add(State("Compute Analytics", shape="box"), xy=(55.0, 50.0))
job_b = sd.add(State("Index Search", shape="box"), xy=(55.0, 25.0))
join = sd.add(ForkJoinState(orientation="vertical", length=22.0), xy=(85.0, 37.5))
final = sd.add(FinalState(), xy=(105.0, 37.5))

init.to(fork)
fork.to(job_a)
fork.to(job_b)
job_a.to(join)
job_b.to(join)
join.to(final)

sd.draw(xy=(0.0, 0.0))
```

---

## 5. Best Practices & Guidelines

1. **Use `bend` for Opposing Transitions**: When two states transition back and forth (e.g. `Idle` ↔ `Active`), apply `bend=0.25` on one transition and `bend=-0.25` on the return so they do not overlap.
2. **Standard Label Formatting**: Prefer passing `event`, `guard`, and `action` parameters rather than writing `label="login [valid] / init"`. Drawlib guarantees standard UML typography and spacing.
3. **Choice Diamond Clarity**: Label exit branches from `ChoiceState` with explicit `guard` criteria (`guard="is_valid"` vs `guard="is_invalid"`).
