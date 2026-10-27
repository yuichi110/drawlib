# Drawlib StateDiagram Guidelines (`lib-diagrams-state`)

`drawlib.diagrams.state` models Finite State Machines (FSM) and UML 2.x Statecharts, featuring initial/final pseudo-states, conditional choice diamonds, fork/join concurrency bars, multi-compartment internal state behaviors (`entry /`, `do /`, `exit /`), self-transitions, and bidirectional curved transitions (`event [guard] / action`).

```text
                ┌──────────────────────┐
   (●)─────────►│      Connecting      │
  Initial       ├──────────────────────┤
                │ entry / initSocket() │
                │ do / handshake()     │
                └──────┬────────▲──────┘
       connected [ok]  │        │  retry [attempts < 3]
                       ▼        │
                ┌───────────────┴──────┐
                │      Connected       │────────►(◉) Final
                └──────────────────────┘
```

---

## 1. Public Exports & Imports

```python
from drawlib.diagrams.state import (
    ChoiceState,
    FinalState,
    ForkJoinState,
    InitialState,
    PaddingType,
    RoutingType,
    ShapeType,
    Side,
    State,
    StateAction,
    StateDiagram,
    StateNodeBase,
    StateTransition,
)
```

*(Note on naming conventions: In user specifications or conceptual discussions, `StateNodeBase`, `StateTransition`, and `StateAction` are sometimes referred to as `StateNode`, `Transition`, and state notes/actions. Always import the concrete symbol names `StateNodeBase`, `StateTransition`, and `StateAction` from `drawlib.diagrams.state`.)*

---

## 2. Core Classes, State Nodes & Constructor Parameters

### 2.1 `StateDiagram`

```python
sd = StateDiagram(
    *,
    node_style: Style,
    edge_style: Style,
    edge_text_style: Style,
    title: str = "",
    title_style: Style | None = None,
    style: Style | None = None,
    width: float | None = None,
    height: float | None = None,
    margin: float = 5.0,
)
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `node_style` | `Style` | *(Required)* | Mandatory base `Style` object for state nodes in the diagram. |
| `edge_style` | `Style` | *(Required)* | Mandatory base `Style` object for state transition lines and arrowheads. |
| `edge_text_style` | `Style` | *(Required)* | Mandatory base `Style` object for transition labels (`event [guard] / action`). |
| `title` | `str` | `""` | Optional diagram title rendered at the top center. |
| `title_style` | `Style \| None` | `None` | Optional typography style for the diagram title. |
| `style` | `Style \| None` | `None` | Optional outer background card style for the diagram container. |
| `width` / `height` | `float \| None` | `None` | Optional explicit diagram dimensions override. |
| `margin` | `float` | `5.0` | Outer margin padding surrounding all states. |

#### Diagram Registration & Sizing Methods:
- **`sd.add(item, xy=(0.0, 0.0), width=None, height=None, style=None, show=None) -> StateNodeBase`**:
  Registers a state or pseudo-state (`State`, `InitialState`, `FinalState`, `ChoiceState`, `ForkJoinState`) centered at `xy=(cx, cy)`.
- **`sd.connect(source, target, *, label="", event="", guard="", action="", side="top", bend=0.0, start_side="auto", end_side="auto", routing="curved", style=None, text_style=None, padding=0.0, loop_width=None, loop_height=None, loop_ratio=0.88, show=True) -> StateTransition`**:
  Creates and registers a `StateTransition` between `source` and `target`.
- **`sd.add_transition(trans) -> StateTransition`**:
  Registers a pre-constructed `StateTransition` instance.
- **`sd.get_bounds() -> tuple[float, float, float, float]`**:
  Returns `(min_x, min_y, max_x, max_y)` of the state diagram in local coordinates.
- **`sd.get_size() -> tuple[float, float]`**:
  Returns the total `(width, height)` of the state diagram in unscaled local units.
- **`sd.draw(xy=(0.0, 0.0), *, align="bottom_left", scale=1.0) -> None`**:
  Renders the state diagram onto the active canvas anchored at `xy` (`align: Literal["bottom_left", "center"] = "bottom_left"`, `scale: float = 1.0`).

---

### 2.2 State & Pseudo-State Classes (`StateNodeBase` Subclasses)

| Class | Constructor Signature | Visual Geometry & Purpose |
| :--- | :--- | :--- |
| **`State`** | `State(name, shape="box", entry="", do="", exit="", width=None, height=None, style=None, show=True)` | State node (`shape: Literal["box", "ellipse", "circle", "double_circle", "text_only"] = "box"`). When `entry`, `do`, `exit`, or `.add_action()` items are present on `"box"`, renders a horizontal divider line and an internal behavior compartment. Height auto-expands if `height=None`. |
| **`InitialState`** | `InitialState(name="", radius=1.75, style=None, show=True)` | Solid filled circle (`radius=1.75`) marking the FSM starting pseudo-state. |
| **`FinalState`** | `FinalState(name="", radius=2.2, style=None, show=True)` | Outer ring (`radius=2.2`) surrounding a solid inner circle marking state termination. |
| **`ChoiceState`** | `ChoiceState(name="", size=4.5, style=None, show=True)` | Diamond pseudo-state (`size=4.5`) for dynamic guard evaluation branching. |
| **`ForkJoinState`** | `ForkJoinState(name="", orientation="horizontal", length=16.0, thickness=1.8, style=None, show=True)` | Thick solid synchronization bar (`length=16.0`, `thickness=1.8`, `orientation: Literal["horizontal", "vertical"] = "horizontal"`) for splitting or joining concurrent orthogonal state regions. |

#### Internal State Compartments (`State` Methods):
- **`state.add_action(kind: str, action: str) -> State`**:
  Appends a custom behavior row (`StateAction(kind=kind, action=action)`, rendered as `"{kind} / {action}"`, e.g. `state.add_action("on_timeout", "closeSocket()")`) and returns `self` for chaining.

---

### 2.3 Transitions (`sd.connect()` & `StateTransition`)

```python
tr = sd.connect(
    source: StateNodeBase,
    target: StateNodeBase,
    *,
    label: str = "",
    event: str = "",
    guard: str = "",
    action: str = "",
    side: LoopSide = "top",
    bend: float = 0.0,
    start_side: Side = "auto",
    end_side: Side = "auto",
    routing: RoutingType = "curved",
    style: Style | None = None,
    text_style: Style | None = None,
    padding: PaddingType = 0.0,
    loop_width: float | None = None,
    loop_height: float | None = None,
    loop_ratio: float = 0.88,
    show: bool = True,
) -> StateTransition
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `source` / `target` | `StateNodeBase` | *(Required)* | Origin and destination state/pseudo-state nodes. |
| `label` | `str` | `""` | Explicit full transition label (overrides `event`/`guard`/`action` formatting if non-empty). |
| `event` | `str` | `""` | Trigger event name (formatted into UML `"event [guard] / action"` when `label=""`). |
| `guard` | `str` | `""` | Boolean guard condition (wrapped in `[guard]`). |
| `action` | `str` | `""` | Transition effect behavior (prefixed with `/ action`). |
| `routing` | `RoutingType` | `"curved"` | `"curved"` (smooth arc using `bend`), `"orthogonal"` (Manhattan right angles), or `"direct"` (straight line). |
| `bend` | `float` | `0.0` | Arc deflection for `"curved"` transitions (`-2.0 < bend < 2.0`, typically `0.2`–`0.4`). Positive values curve toward one side; use positive `bend` on both `A -> B` and `B -> A` (or opposite signs depending on port sides) to create non-overlapping bidirectional arcs. |
| `start_side` / `end_side` | `Side` | `"auto"` | Attachment side on `source` and `target` (`"auto"`, `"left"`, `"right"`, `"top"`, `"bottom"`). |
| `side` | `LoopSide` | `"top"` | Attachment side for **self-transitions** (`source is target`): `"top"`, `"bottom"`, `"left"`, or `"right"`. |
| `loop_width` / `loop_height` / `loop_ratio` | `float \| None` | `None` / `None` / `0.88` | Custom geometry controls for self-transition loops (`source is target`). |
| `style` | `Style \| None` | `None` | Stroke style override for the transition curve and arrowhead. |
| `text_style` | `Style \| None` | `None` | Typography style override for the transition label. |
| `padding` | `PaddingType` | `0.0` | Boundary offset gap (`float` or `(start_pad, end_pad)`). |
| `show` | `bool` | `True` | Visibility flag for this transition. |

- **`StateTransition` Fluent Methods**:
  - `tr.points(waypoints: list[tuple[float, float]]) -> Self`
  - `tr.via(*waypoints: tuple[float, float]) -> Self`
  - `tr.set_label(label: str) -> Self`
  - `tr.set_style(style: Style) -> Self`
  - `tr.set_text_style(text_style: Style) -> Self`
  - `tr.set_padding(padding: PaddingType) -> Self`

---

## 3. Production Examples

### Example 3.1: TCP Connection & Retry Lifecycle with Entry/Do/Exit Compartments
```drawlib align=center code=fold file=state_tcp_lifecycle.png caption="TCP Socket State Machine with Internal Compartments and Curved Transitions"
from drawlib import canvas
from drawlib.diagrams.state import ChoiceState, FinalState, InitialState, State, StateDiagram
from drawlib.styles import Styles

canvas.clear()
canvas.setup(width=152, height=84)

sd = StateDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=9.5),
    title="TCP Connection & Automatic Retry Lifecycle",
)

init = sd.add(InitialState(), xy=(10, 46))
closed = sd.add(State("Closed", entry="resetCounters()", width=26), xy=(32, 46))
connecting = sd.add(
    State("Connecting", entry="openSocket()", do="awaitSynAck()", width=30, style=Styles.PrimaryNeutral),
    xy=(74, 46),
)
choice = sd.add(ChoiceState(), xy=(74, 18))
established = sd.add(
    State("Established", entry="startHeartbeat()", do="streamFrames()", exit="flushBuffer()", width=32, style=Styles.SuccessNeutral),
    xy=(122, 46),
)
final = sd.add(FinalState(), xy=(122, 16))

# Transitions
sd.connect(init, closed, routing="direct", padding=1.0)
sd.connect(closed, connecting, event="connect()", start_side="right", end_side="left", routing="direct", padding=1.0)
sd.connect(
    connecting,
    established,
    event="synAck",
    guard="valid",
    start_side="right",
    end_side="left",
    routing="direct",
    padding=1.0,
)
sd.connect(
    connecting,
    choice,
    event="timeout",
    start_side="bottom",
    end_side="top",
    routing="direct",
    style=Styles.Warning,
    padding=1.0,
)
sd.connect(
    choice,
    connecting,
    guard="retries < 3",
    action="backoff()",
    start_side="right",
    end_side="bottom",
    bend=0.3,
    padding=1.0,
)
sd.connect(
    choice,
    closed,
    guard="retries >= 3",
    action="reportErr()",
    start_side="left",
    end_side="bottom",
    routing="orthogonal",
    style=Styles.Danger,
    text_style=Styles.Danger,
    padding=1.0,
)
sd.connect(established, established, event="ping()", action="sendPong()", side="top")
sd.connect(established, final, event="close()", start_side="bottom", end_side="top", routing="direct", padding=1.0)

sd.draw(xy=(4.0, 4.0))
canvas.save()
```

### Example 3.2: Concurrent Fork & Join Synchronization Bars (`ForkJoinState`)
```drawlib align=center code=fold file=state_fork_join.png caption="Concurrent Order Processing with Horizontal ForkJoinState Bars"
from drawlib import canvas
from drawlib.diagrams.state import FinalState, ForkJoinState, InitialState, State, StateDiagram
from drawlib.styles import Styles

canvas.clear()
canvas.setup(width=128, height=88)

sd = StateDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark,
    title="Concurrent Payment & Inventory Verification",
)

init = sd.add(InitialState(), xy=(64, 76))
fork_bar = sd.add(ForkJoinState(orientation="horizontal", length=16.0), xy=(64, 62))
charge = sd.add(State("Charge Card", do="captureStripe()", width=30, style=Styles.PrimaryNeutral), xy=(34, 42))
reserve = sd.add(State("Reserve Stock", do="lockSkuRows()", width=30, style=Styles.SecondaryNeutral), xy=(94, 42))
join_bar = sd.add(ForkJoinState(orientation="horizontal", length=16.0), xy=(64, 22))
final = sd.add(FinalState(), xy=(64, 8))

sd.connect(init, fork_bar, routing="direct", padding=0.8)
sd.connect(fork_bar, charge, routing="orthogonal", start_side="bottom", end_side="top", padding=0.8)
sd.connect(fork_bar, reserve, routing="orthogonal", start_side="bottom", end_side="top", padding=0.8)
sd.connect(charge, join_bar, routing="orthogonal", start_side="bottom", end_side="top", padding=0.8)
sd.connect(reserve, join_bar, routing="orthogonal", start_side="bottom", end_side="top", padding=0.8)
sd.connect(join_bar, final, event="fulfilled", routing="direct", padding=0.8)

sd.draw(xy=(4.0, 4.0))
canvas.save()
```
