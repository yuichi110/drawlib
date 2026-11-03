# drawlib.diagrams.state

Finite State Machine (FSM) and UML 2.x statechart diagrams featuring entry/do/exit compartments, initial/final/choice/fork-join pseudo-states, self-loops, and curved guard transitions. Canonical import: `from drawlib.diagrams.state import ChoiceState, FinalState, InitialState, State, StateDiagram`.

```drawlib align=center code=fold file=24_diagrams_state_hero.png caption="Connection State Machine with Internal Compartments, Choice Diamond, and Curved Retry Arc"
from drawlib.canvas import save, setup
from drawlib.diagrams.state import ChoiceState, FinalState, InitialState, State, StateDiagram
from drawlib.styles import Colors, Styles

setup(width=120, height=54)

sd = StateDiagram(
    node_style=Styles.Neutral.patch(text_size=10.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=10.0),
    margin=4.0,
)

init = sd.add(InitialState(), xy=(6.0, 34.0))
idle = sd.add(State("Idle", width=17, height=11), xy=(21.0, 34.0))
connecting = sd.add(
    State(
        "Connecting",
        entry="openSocket()",
        do="handshake()",
        width=29,
        style=Styles.PrimaryNeutral.patch(text_size=10.5),
    ),
    xy=(54.0, 34.0),
)
choice = sd.add(ChoiceState(style=Styles.SecondaryNeutral), xy=(80.0, 34.0))
connected = sd.add(
    State(
        "Connected",
        width=21,
        height=11,
        style=Styles.PrimaryFlat.patch(text_color=Colors.White, text_size=10.5),
    ),
    xy=(103.5, 34.0),
)
final = sd.add(FinalState(), xy=(103.5, 11.0))

sd.connect(init, idle, routing="direct", padding=0.8)
sd.connect(idle, connecting, event="connect", start_side="right", end_side="left", routing="direct", padding=0.8)
sd.connect(connecting, choice, event="done", start_side="right", end_side="left", routing="direct", padding=0.8)
sd.connect(choice, connected, guard="ok", start_side="right", end_side="left", routing="direct", padding=0.8)
sd.connect(choice, idle, guard="retry", start_side="bottom", end_side="bottom", bend=-0.26, padding=0.8)
sd.connect(
    connected,
    final,
    event="close",
    start_side="bottom",
    end_side="top",
    routing="direct",
    padding=0.8,
    text_style=Styles.Dark.patch(text_size=10.0, halign="left"),
)

sd.draw(xy=(60.0, 27.0), align="center")
save()
```

---

## `class` ChoiceState

UML 2.x dynamic conditional branch pseudo-state rendered as a diamond. Subclass of [`StateNodeBase`](#statenodebase).

```python
ChoiceState(
    name: str = "",
    size: float = 4.5,
    style: Style | None = None,
    show: bool = True,
) -> None
```

- **Coordinate Anchor**: **Center `(cx, cy)`** when registered via `sd.add(choice, xy=(cx, cy))`.

### Constructor Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `name` | `str` | `""` | Optional identifier for the choice node. |
| `size` | `float` | `4.5` | Diamond width and height in local diagram units. |
| `style` | `Style \| None` | `None` | Optional fill and border style override (falls back to `sd.node_style`). |
| `show` | `bool` | `True` | Visibility flag (`False` hides the diamond and incident transitions). |

### Public Methods & Properties

| Member | Kind | Signature | Description |
| :--- | :--- | :--- | :--- |
| `center` | `property` | `-> tuple[float, float]` | Relative center coordinate `(cx, cy)` of the choice diamond. |
| `effective_height` | `property` | `-> float` | Actual rendered height (`size`). |
| `effective_width` | `property` | `-> float` | Actual rendered width (`size`). |
| `get_anchor` | `method` | `(self, side: Side) -> tuple[float, float]` | Return diamond vertex/boundary anchor coordinate on `side`. |
| `get_bounds` | `method` | `(self) -> tuple[float, float, float, float]` | Return local bounding box `(-size/2, -size/2, size/2, size/2)` relative to `(0, 0)`. |
| `xy` | `property` | `-> tuple[float, float]` | Alias returning the relative center coordinate `(cx, cy)`. |

---

## `class` FinalState

UML 2.x final state node rendered as a bullseye (outer ring enclosing a solid inner circle). Subclass of [`StateNodeBase`](#statenodebase).

```python
FinalState(
    name: str = "",
    radius: float = 2.2,
    style: Style | None = None,
    show: bool = True,
) -> None
```

- **Coordinate Anchor**: **Center `(cx, cy)`** when registered via `sd.add(final, xy=(cx, cy))`.

### Constructor Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `name` | `str` | `""` | Optional identifier for the final state. |
| `radius` | `float` | `2.2` | Outer ring radius in local diagram units (total diameter `2 * radius`). |
| `style` | `Style \| None` | `None` | Optional stroke/fill color override for the ring and inner dot. |
| `show` | `bool` | `True` | Visibility flag (`False` hides this node and incident transitions). |

### Public Methods & Properties

| Member | Kind | Signature | Description |
| :--- | :--- | :--- | :--- |
| `center` | `property` | `-> tuple[float, float]` | Relative center coordinate `(cx, cy)` of the bullseye. |
| `effective_height` | `property` | `-> float` | Actual rendered diameter (`2 * radius`). |
| `effective_width` | `property` | `-> float` | Actual rendered diameter (`2 * radius`). |
| `get_anchor` | `method` | `(self, side: Side) -> tuple[float, float]` | Return outer ring boundary coordinate for `side`. |
| `get_bounds` | `method` | `(self) -> tuple[float, float, float, float]` | Return local bounding box `(-radius, -radius, radius, radius)` relative to `(0, 0)`. |
| `xy` | `property` | `-> tuple[float, float]` | Alias returning the relative center coordinate `(cx, cy)`. |

---

## `class` ForkJoinState

UML 2.x concurrency synchronization bar splitting one incoming transition into orthogonal concurrent regions (`fork`) or synchronizing multiple regions back together (`join`). Subclass of [`StateNodeBase`](#statenodebase).

```python
ForkJoinState(
    name: str = "",
    orientation: Literal["horizontal", "vertical"] = "horizontal",
    length: float = 16.0,
    thickness: float = 1.8,
    style: Style | None = None,
    show: bool = True,
) -> None
```

- **Coordinate Anchor**: **Center `(cx, cy)`** when registered via `sd.add(bar, xy=(cx, cy))`.

### Constructor Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `name` | `str` | `""` | Optional identifier for the fork/join bar. |
| `orientation` | `Literal["horizontal", "vertical"]` | `"horizontal"` | Bar axis (`"horizontal"` wide bar for top-to-bottom flows; `"vertical"` tall bar for left-to-right flows). |
| `length` | `float` | `16.0` | Primary bar span along `orientation` in local units. |
| `thickness` | `float` | `1.8` | Cross-axis bar thickness in local units. |
| `style` | `Style \| None` | `None` | Optional solid fill style override for the bar. |
| `show` | `bool` | `True` | Visibility flag (`False` hides the bar and incident transitions). |

### Public Methods & Properties

| Member | Kind | Signature | Description |
| :--- | :--- | :--- | :--- |
| `center` | `property` | `-> tuple[float, float]` | Relative center coordinate `(cx, cy)` of the synchronization bar. |
| `effective_height` | `property` | `-> float` | Rendered height (`thickness` when `"horizontal"`, `length` when `"vertical"`). |
| `effective_width` | `property` | `-> float` | Rendered width (`length` when `"horizontal"`, `thickness` when `"vertical"`). |
| `get_anchor` | `method` | `(self, side: Side) -> tuple[float, float]` | Return boundary coordinate on `side`. |
| `get_bounds` | `method` | `(self) -> tuple[float, float, float, float]` | Return local bounding box `(min_x, min_y, max_x, max_y)` relative to `(0, 0)`. |
| `xy` | `property` | `-> tuple[float, float]` | Alias returning the relative center coordinate `(cx, cy)`. |

---

## `class` InitialState

UML 2.x initial pseudo-state rendered as a solid filled circle marking entry into a state machine. Subclass of [`StateNodeBase`](#statenodebase).

```python
InitialState(
    name: str = "",
    radius: float = 1.75,
    style: Style | None = None,
    show: bool = True,
) -> None
```

- **Coordinate Anchor**: **Center `(cx, cy)`** when registered via `sd.add(init, xy=(cx, cy))`.

### Constructor Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `name` | `str` | `""` | Optional identifier for the initial pseudo-state. |
| `radius` | `float` | `1.75` | Solid circle radius in local diagram units (total diameter `3.5`). |
| `style` | `Style \| None` | `None` | Optional solid fill color override. |
| `show` | `bool` | `True` | Visibility flag (`False` hides this node and outgoing transitions). |

### Public Methods & Properties

| Member | Kind | Signature | Description |
| :--- | :--- | :--- | :--- |
| `center` | `property` | `-> tuple[float, float]` | Relative center coordinate `(cx, cy)` of the circle. |
| `effective_height` | `property` | `-> float` | Actual rendered diameter (`2 * radius`). |
| `effective_width` | `property` | `-> float` | Actual rendered diameter (`2 * radius`). |
| `get_anchor` | `method` | `(self, side: Side) -> tuple[float, float]` | Return perimeter anchor coordinate on `side`. |
| `get_bounds` | `method` | `(self) -> tuple[float, float, float, float]` | Return local bounding box `(-radius, -radius, radius, radius)` relative to `(0, 0)`. |
| `xy` | `property` | `-> tuple[float, float]` | Alias returning the relative center coordinate `(cx, cy)`. |

---

## `type` PaddingType

Union type alias specifying endpoint clearance gap distances on [`StateTransition`](#statetransition) arrows.

```python
PaddingType = float | tuple[float, float]
```

- **Coordinate Anchor**: Offsets transition line endpoints outward from `start` and `end` state boundaries (`float` symmetric or `(start_pad, end_pad)` tuple).

---

## `type` RoutingType

Literal type controlling curve/segment geometry for [`StateTransition`](#statetransition) connectors.

```python
RoutingType = Literal["curved", "orthogonal", "direct"]
```

- **Coordinate Anchor**: Governs path interpolation between `start` and `end` boundary anchors.

| Literal Value | Path Geometry |
| :--- | :--- |
| `"curved"` | Smooth quadratic arc controlled by `bend` (default; separates bidirectional `A <-> B` transitions cleanly). |
| `"orthogonal"` | Right-angled horizontal and vertical Manhattan segments. |
| `"direct"` | Straight Euclidean line segment between resolved anchors. |

---

## `type` ShapeType

Literal type selecting the visual geometry of a [`State`](#state) node.

```python
ShapeType = Literal["box", "ellipse", "circle", "double_circle", "text_only"]
```

- **Coordinate Anchor**: All state shapes are centered at `(cx, cy)`.

| Literal Value | Visual Rendering | Typical Usage |
| :--- | :--- | :--- |
| `"box"` | Rounded rectangle (with optional internal action compartment divider) | Standard UML 2.x statechart state (default). |
| `"ellipse"` | Oval / ellipse | Conceptual FSM or Moore/Mealy state node. |
| `"circle"` | Single-ring circle | Mathematical DFA / NFA state vertex (`q0`, `q1`). |
| `"double_circle"` | Concentric double-ring circle | DFA / NFA accepting state vertex. |
| `"text_only"` | Borderless text label | Minimalist state label with invisible bounds. |

---

## `type` Side

Literal type specifying attachment ports (including diagonal corners) on [`StateNodeBase`](#statenodebase) nodes.

```python
Side = Literal[
    "left",
    "right",
    "top",
    "bottom",
    "auto",
    "top_right",
    "top_left",
    "bottom_right",
    "bottom_left",
]
```

- **Coordinate Anchor**: Resolves to the exact perimeter point on box, circle, ellipse, or diamond state boundaries (`"auto"` chooses the nearest facing side).

---

## `class` State

Primary state node supporting UML rounded boxes (with optional `entry /`, `do /`, `exit /` internal behavior compartment) as well as mathematical FSM circle/double-circle shapes. Subclass of [`StateNodeBase`](#statenodebase).

```python
State(
    name: str,
    shape: ShapeType = "box",
    entry: str = "",
    do: str = "",
    exit: str = "",
    width: float | None = None,
    height: float | None = None,
    style: Style | None = None,
    show: bool = True,
) -> None
```

- **Coordinate Anchor**: **Center `(cx, cy)`** when registered via `sd.add(state, xy=(cx, cy))`.

### Constructor Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `name` | `str` | *(Required)* | State title rendered in the main compartment (or header when internal actions exist). |
| `shape` | [`ShapeType`](#shapetype) | `"box"` | Node geometry (`"box"`, `"ellipse"`, `"circle"`, `"double_circle"`, `"text_only"`). |
| `entry` | `str` | `""` | Optional entry behavior formatted as `entry / <entry>` on `"box"` states. |
| `do` | `str` | `""` | Optional ongoing activity formatted as `do / <do>` on `"box"` states. |
| `exit` | `str` | `""` | Optional exit behavior formatted as `exit / <exit>` on `"box"` states. |
| `width` | `float \| None` | `None` | Optional explicit width (`None` auto-sizes from text/actions). |
| `height` | `float \| None` | `None` | Optional explicit height (`None` auto-sizes from header and action rows). |
| `style` | `Style \| None` | `None` | Optional fill, stroke, and text style override (falls back to `sd.node_style`). |
| `show` | `bool` | `True` | Visibility flag (`False` hides this state and incident transitions). |

### Public Methods & Properties

| Member | Kind | Signature | Description |
| :--- | :--- | :--- | :--- |
| `add_action` | `method` | `(self, kind: str, action: str) -> State` | Append a custom [`StateAction`](#stateaction) row (`"{kind} / {action}"`) to the internal compartment and return `self`. |
| `center` | `property` | `-> tuple[float, float]` | Relative center coordinate `(cx, cy)` of the state node. |
| `effective_height` | `property` | `-> float` | Computed rendered height of the state node. |
| `effective_width` | `property` | `-> float` | Computed rendered width of the state node. |
| `get_anchor` | `method` | `(self, side: Side) -> tuple[float, float]` | Return perimeter anchor coordinate on `side`. |
| `get_bounds` | `method` | `(self) -> tuple[float, float, float, float]` | Return local bounding box `(-effective_width/2, -effective_height/2, ...)` relative to `(0, 0)`. |
| `xy` | `property` | `-> tuple[float, float]` | Alias returning the relative center coordinate `(cx, cy)`. |

---

## `class` StateAction

Validated Pydantic data model representing a single internal state activity row (`entry /`, `do /`, `exit /`, or custom trigger) inside a [`State`](#state) box. Typically registered via `State(..., entry=..., do=..., exit=...)` or `state.add_action(kind, action)`.

```python
StateAction(
    *,
    kind: str,
    action: str,
) -> None
```

- **Coordinate Anchor**: Rendered left-aligned inside the lower compartment of a `"box"` [`State`](#state).

### Constructor Parameters & Fields

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `kind` | `str` | *(Required)* | Trigger label such as `"entry"`, `"do"`, `"exit"`, or an event name (keyword-only). |
| `action` | `str` | *(Required)* | Behavior expression or function signature string (keyword-only). |

### Public Methods & Properties

| Member | Kind | Signature | Description |
| :--- | :--- | :--- | :--- |
| `display_text` | `property` | `-> str` | Formatted UML internal behavior string (`"{kind} / {action}"`). |
| `model_copy` | `method` | `(self, *, update: Mapping[str, Any] \| None = None, deep: bool = False) -> Self` | Create a shallow or deep copy with optional field updates (`pydantic.BaseModel`). |
| `model_dump` | `method` | `(self, *, mode: str = "python", ...) -> dict[str, Any]` | Serialize fields to a Python dictionary (`pydantic.BaseModel`). |
| `model_dump_json` | `method` | `(self, *, indent: int \| None = None, ...) -> str` | Serialize fields to a JSON string (`pydantic.BaseModel`). |
| `model_validate` | `classmethod` | `(obj: Any, *, strict: bool \| None = None, ...) -> Self` | Validate an arbitrary mapping or object into `StateAction`. |
| `model_validate_json` | `classmethod` | `(json_data: str \| bytes \| bytearray, ...) -> Self` | Parse and validate JSON input into `StateAction`. |
| `model_validate_strings` | `classmethod` | `(obj: Any, ...) -> Self` | Validate string-typed input dictionary into `StateAction`. |
| `model_construct` | `classmethod` | `(_fields_set: set[str] \| None = None, **values: Any) -> Self` | Construct an unvalidated instance directly from field values. |
| `model_json_schema` | `classmethod` | `(by_alias: bool = True, ...) -> dict[str, Any]` | Generate a JSON Schema dictionary for `StateAction`. |

*(Also inherits standard `pydantic.BaseModel` lifecycle/compatibility members: `model_extra`, `model_fields_set`, `model_parametrized_name`, `model_post_init`, `model_rebuild`, `construct`, `copy`, `dict`, `from_orm`, `json`, `parse_file`, `parse_obj`, `parse_raw`, `schema`, `schema_json`, `update_forward_refs`, and `validate`.)*

---

## `class` StateDiagram

Top-level container managing states, pseudo-states, transitions, and bounding-box layout for UML statecharts and FSM diagrams.

```python
StateDiagram(
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
) -> None
```

- **Coordinate Anchor**: `draw(xy=(0.0, 0.0), align="bottom_left")` shifts local coordinates by `xy` (or centers `get_bounds()` at `xy` when `align="center"`).

### Constructor Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `node_style` | [`Style`](05_styles_and_types.md#style) | *(Required)* | Base style applied to state nodes and pseudo-states (keyword-only). |
| `edge_style` | [`Style`](05_styles_and_types.md#style) | *(Required)* | Base stroke and arrowhead style applied to [`StateTransition`](#statetransition) edges (keyword-only). |
| `edge_text_style` | [`Style`](05_styles_and_types.md#style) | *(Required)* | Base typography style applied to transition `event [guard] / action` labels (keyword-only). |
| `title` | `str` | `""` | Optional diagram title rendered centered above the statechart. |
| `title_style` | `Style \| None` | `None` | Optional typography style override for `title`. |
| `style` | `Style \| None` | `None` | Optional outer background card style for the diagram container. |
| `width` | `float \| None` | `None` | Optional fixed diagram width override (`None` auto-computes from `get_bounds()` + `margin`). |
| `height` | `float \| None` | `None` | Optional fixed diagram height override (`None` auto-computes from `get_bounds()` + `margin`). |
| `margin` | `float` | `5.0` | Outer margin padding surrounding all registered states and self-loops. |

### Public Methods & Properties

| Member | Kind | Signature | Description |
| :--- | :--- | :--- | :--- |
| `add` | `method` | `(self, item: NodeT, xy: tuple[float, float] = (0.0, 0.0), width: float \| None = None, height: float \| None = None, style: Style \| None = None, show: bool \| None = None) -> NodeT` | Register a [`State`](#state) or pseudo-state centered at `xy` (with optional size/style overrides) and return it. |
| `add_transition` | `method` | `(self, trans: StateTransition) -> StateTransition` | Register a pre-constructed [`StateTransition`](#statetransition) with this diagram. |
| `connect` | `method` | `(self, source: StateNodeBase, target: StateNodeBase, *, label: str = "", event: str = "", guard: str = "", action: str = "", side: LoopSide = "top", bend: float = 0.0, start_side: Side = "auto", end_side: Side = "auto", routing: RoutingType = "curved", style: Style \| None = None, text_style: Style \| None = None, padding: PaddingType = 0.0, loop_width: float \| None = None, loop_height: float \| None = None, loop_ratio: float = 0.88, show: bool = True) -> StateTransition` | Create and register a [`StateTransition`](#statetransition) (or self-loop when `source is target`). |
| `draw` | `method` | `(self, xy: tuple[float, float] = (0.0, 0.0), *, align: Literal["bottom_left", "center"] = "bottom_left", scale: PosFloat = 1.0) -> None` | Render the complete state diagram onto the active canvas anchored at `xy`. |
| `get_bounds` | `method` | `(self) -> tuple[float, float, float, float]` | Compute enclosing `(min_x, min_y, max_x, max_y)` of all states and self-transition loops. |
| `get_size` | `method` | `(self) -> tuple[float, float]` | Compute overall `(width, height)` of the diagram including `margin`. |

---

## `class` StateNodeBase

Abstract/common base class shared by [`State`](#state), [`InitialState`](#initialstate), [`FinalState`](#finalstate), [`ChoiceState`](#choicestate), and [`ForkJoinState`](#forkjoinstate).

```python
StateNodeBase(
    name: str = "",
    width: float = 20.0,
    height: float = 12.0,
    style: Style | None = None,
    show: bool = True,
) -> None
```

- **Coordinate Anchor**: **Center `(cx, cy)`** when registered on [`StateDiagram`](#statediagram).

### Constructor Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `name` | `str` | `""` | Node identifier or label string. |
| `width` | `float` | `20.0` | Base bounding box width in local units. |
| `height` | `float` | `12.0` | Base bounding box height in local units. |
| `style` | `Style \| None` | `None` | Optional [`Style`](05_styles_and_types.md#style) override. |
| `show` | `bool` | `True` | Visibility flag for this state node. |

### Public Methods & Properties

| Member | Kind | Signature | Description |
| :--- | :--- | :--- | :--- |
| `center` | `property` | `-> tuple[float, float]` | Relative center coordinate `(cx, cy)` of the state node. |
| `effective_height` | `property` | `-> float` | Actual rendered height of the state node. |
| `effective_width` | `property` | `-> float` | Actual rendered width of the state node. |
| `get_anchor` | `method` | `(self, side: Side) -> tuple[float, float]` | Return boundary anchor coordinate on `side`. |
| `get_bounds` | `method` | `(self) -> tuple[float, float, float, float]` | Return local bounding box `(min_x, min_y, max_x, max_y)` relative to `(0, 0)`. |
| `xy` | `property` | `-> tuple[float, float]` | Alias returning the relative center coordinate `(cx, cy)`. |

---

## `class` StateTransition

Directed transition edge (or self-loop ellipse) connecting two [`StateNodeBase`](#statenodebase) nodes with automatic UML `"event [guard] / action"` label formatting.

```python
StateTransition(
    start: StateNodeBase,
    end: StateNodeBase,
    label: str = "",
    event: str = "",
    guard: str = "",
    action: str = "",
    bend: float = 0.0,
    start_side: Side = "auto",
    end_side: Side = "auto",
    routing: RoutingType = "curved",
    style: Style | None = None,
    text_style: Style | None = None,
    padding: PaddingType = 0.0,
    loop_side: LoopSide = "top",
    loop_width: float | None = None,
    loop_height: float | None = None,
    loop_ratio: float = 0.88,
    is_loop: bool = False,
    show: bool = True,
) -> None
```

- **Coordinate Anchor**: Connects `start_side` on `start` to `end_side` on `end` (or attaches a self-loop arc to `loop_side` when `start is end`).

### Constructor Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `start` | [`StateNodeBase`](#statenodebase) | *(Required)* | Source state or pseudo-state. |
| `end` | [`StateNodeBase`](#statenodebase) | *(Required)* | Target state or pseudo-state (`start` for a self-transition). |
| `label` | `str` | `""` | Explicit full transition label (overrides `event`/`guard`/`action` formatting when non-empty). |
| `event` | `str` | `""` | Trigger event name formatted at the start of `"event [guard] / action"`. |
| `guard` | `str` | `""` | Guard condition automatically wrapped in `[guard]`. |
| `action` | `str` | `""` | Transition effect automatically prefixed with `/ action`. |
| `bend` | `float` | `0.0` | Arc deflection amount for `"curved"` routing (`0.0` straight; `0.25`–`0.45` separates bidirectional transitions). |
| `start_side` | [`Side`](#side) | `"auto"` | Departure anchor side on `start`. |
| `end_side` | [`Side`](#side) | `"auto"` | Arrival anchor side on `end`. |
| `routing` | [`RoutingType`](#routingtype) | `"curved"` | Path routing strategy (`"curved"`, `"orthogonal"`, or `"direct"`). |
| `style` | `Style \| None` | `None` | Optional line stroke style override (falls back to `sd.edge_style`). |
| `text_style` | `Style \| None` | `None` | Optional label typography style override (falls back to `sd.edge_text_style`). |
| `padding` | [`PaddingType`](#paddingtype) | `0.0` | Clearance offset between state borders and transition endpoints. |
| `loop_side` | `Literal["top", "bottom", "left", "right", ...]` | `"top"` | Attachment side for self-loops (`sd.connect(..., side=...)` forwards to `loop_side`). |
| `loop_width` | `float \| None` | `None` | Optional custom ellipse width for self-transition loops. |
| `loop_height` | `float \| None` | `None` | Optional custom ellipse height for self-transition loops. |
| `loop_ratio` | `float` | `0.88` | Fraction of loop ellipse circumference drawn (`0.0`–`1.0`). |
| `is_loop` | `bool` | `False` | Explicit self-loop flag (automatically `True` whenever `start is end`). |
| `show` | `bool` | `True` | Whether to render this transition. |

### Public Methods & Properties

| Member | Kind | Signature | Description |
| :--- | :--- | :--- | :--- |
| `effective_label` | `property` | `-> str` | Resolved transition label (`label` if non-empty, otherwise formatted `"event [guard] / action"`). |
| `is_self_transition` | `property` | `-> bool` | `True` when this transition loops back onto the same state (`is_loop` or `start is end`). |
