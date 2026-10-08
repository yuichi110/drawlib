::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils

utils.draw_page_number()
```
:::

::: block (80, 40) (1760, 60)
# Finite State Machines & Lifecycles (`StateDiagram`)
:::

::: block (80, 140) (640, 840) compact
## UML 2.0 Statecharts & Concurrent Forks

`StateDiagram` models finite state automata, protocol lifecycles, and distributed job orchestrators:

### Rich State & Pseudo-State Palette
- **`State(name, shape="box", entry=..., do=..., exit=...)`**:
  - Supports 5 shapes (`"box"`, `"oval"`, `"circle"`, `"double_circle"`, `"text_only"`) and internal action compartments (`entry / ...`, `do / ...`, `exit / ...`).
- **UML Pseudo-States**:
  - `InitialState()`: Solid black entry circle.
  - `ChoiceState(name="...")`: Dynamic conditional diamond branch.
  - `ForkJoinState(orientation="vertical" | "horizontal", length=...)`: Solid synchronization bar for concurrent splits and joins.
  - `FinalState()`: Bullseye termination target.

### Formal Transition Formatting (`sd.connect`)
- `sd.connect(src, dst, event="...", guard="...", action="...", bend=0.25)` automatically formats `event [guard] / action` labels and supports curved arcs (`bend`) and self-loops (`side="top"`).
:::

::: block (760, 140) (1080, 840)
```drawlib file:state_lifecycle.svg
from drawlib.canvas import clear, save, setup
from drawlib.diagrams.state import (
    ChoiceState,
    FinalState,
    ForkJoinState,
    InitialState,
    State,
    StateDiagram,
)
from drawlib.styles import Styles

clear()
setup(width=108, height=84)

sd = StateDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=6.8),
    title="Distributed Batch Job Execution Lifecycle (StateDiagram)",
    title_style=Styles.DarkBold.patch(text_size=9.5),
)

# 1. Initial -> Queued -> Quota ChoiceState
init = sd.add(InitialState(), xy=(7.0, 42.0))
queued = sd.add(
    State(
        "Queued",
        shape="box",
        entry="enqueue()",
        do="await_slot()",
        width=20.0,
        style=Styles.Neutral,
    ),
    xy=(23.0, 42.0),
)
quota_check = sd.add(
    ChoiceState(name="Quota?", style=Styles.SecondaryNeutral),
    xy=(44.0, 42.0),
)

# 2. Fork into Concurrent Map & Shuffle Workers -> Join -> Final
fork_bar = sd.add(
    ForkJoinState(orientation="vertical", length=28.0),
    xy=(58.0, 42.0),
)
shard_a = sd.add(
    State(
        "Map Shards",
        shape="box",
        entry="alloc_gpu()",
        do="exec_map()",
        width=21.0,
        style=Styles.PrimaryNeutral,
    ),
    xy=(75.0, 56.0),
)
shard_b = sd.add(
    State(
        "Stream Checkpoints",
        shape="box",
        entry="open_wal()",
        do="sync_s3()",
        width=21.0,
        style=Styles.BlueNeutral,
    ),
    xy=(75.0, 26.0),
)
join_bar = sd.add(
    ForkJoinState(orientation="vertical", length=28.0),
    xy=(92.0, 42.0),
)
final = sd.add(FinalState(), xy=(102.0, 42.0))

# 3. Connect State Transitions
sd.connect(init, queued)
sd.connect(queued, quota_check, event="schedule")
sd.connect(quota_check, fork_bar, guard="ok")

# Curved backoff loop when quota is throttled
sd.connect(
    quota_check,
    queued,
    guard="throttled",
    action="backoff()",
    bend=-0.38,
    start_side="bottom",
    end_side="bottom",
    text_style=Styles.Dark.patch(text_size=6.8, text_valign="top"),
)

# Concurrent fork/join branches
sd.connect(fork_bar, shard_a)
sd.connect(fork_bar, shard_b)
sd.connect(shard_a, join_bar)
sd.connect(shard_b, join_bar)
sd.connect(join_bar, final, event="commit")

sd.draw(xy=(0.0, 0.0))

save()
```
:::

::: note
- Slide 9 showcases `StateDiagram` modeling a distributed batch job execution lifecycle.
- Every major UML statechart element is represented in this single flow:
  1. `InitialState()` transitions into `Queued` (a `"box"` state with `entry / enqueue()` and `do / await_slot()` compartments).
  2. `ChoiceState(name="Quota?")` evaluates cluster capacity: if `[throttled] / backoff()`, a negative curved arc (`bend=-0.38`) loops back underneath to `Queued`.
  3. If `[ok]`, execution hits a vertical `ForkJoinState` bar that splits into two concurrent active states (`Map Shards` and `Stream Checkpoints`), synchronizes at a second `ForkJoinState` bar, and finishes at `FinalState()`.
:::
