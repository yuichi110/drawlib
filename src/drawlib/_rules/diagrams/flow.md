# Drawlib FlowDiagram Guidelines (`lib-diagrams-flow`)

`drawlib.diagrams.flow` implements standard flowchart symbols according to ISO 5807 and JIS X 0121 standards, with support for cross-functional vertical or horizontal swimlane layouts (`Lane`) sharing a unified coordinate plane.

```text
  Lane: Customer                Lane: Gateway              Lane: Warehouse
 ┌───────────────────────────┬───────────────────────────┬───────────────────────────┐
 │   (Start)                 │                           │                           │
 │      │                    │                           │                           │
 │      ▼                    │                           │                           │
 │ [Submit Order]───────────►│ <Payment Valid?>          │                           │
 │                           │    │           │ (No)     │                           │
 │                           │    ▼ (Yes)     ▼          │                           │
 │                           │    │        [Show Error]  │                           │
 │                           │    ▼                      │                           │
 │                           │    └─────────────────────►│ [Pack & Ship]             │
 └───────────────────────────┴───────────────────────────┴───────────────────────────┘
```

---

## 1. Public Exports & Imports

```python
from drawlib.diagrams.flow import (
    ArrowType,
    Connectable,
    Data,
    Decision,
    End,
    FlowDiagram,
    FlowEdge,
    FlowNode,
    Junction,
    Lane,
    Orientation,
    PaddingType,
    Process,
    RoutingType,
    ShapeType,
    Side,
    Start,
)
```

---

## 2. Core Classes, Symbols & Constructor Parameters

### 2.1 `FlowDiagram`

```python
flow = FlowDiagram(
    *,
    node_style: Style,
    edge_style: Style,
    edge_text_style: Style,
    title: str = "",
    title_style: Style | None = None,
    width: float | None = None,
    height: float | None = None,
    style: Style | None = None,
    lane_orientation: Orientation = "vertical",
)
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `node_style` | `Style` | *(Required)* | Default fill, stroke, and text style for all flow nodes (keyword-only). |
| `edge_style` | `Style` | *(Required)* | Default stroke style for connection lines and arrowheads (keyword-only). |
| `edge_text_style` | `Style` | *(Required)* | Default typography style for branch/edge labels (keyword-only). |
| `title` | `str` | `""` | Optional diagram title rendered at the top center. |
| `title_style` | `Style \| None` | `None` | Optional typography style for the diagram title. |
| `width` | `float \| None` | `None` | Optional explicit diagram width override (auto-calculated from lanes/nodes if `None`). |
| `height` | `float \| None` | `None` | Optional explicit diagram height override (auto-calculated from lanes/nodes if `None`). |
| `style` | `Style \| None` | `None` | Optional outer background/border style for the entire diagram container. |
| `lane_orientation` | `Literal["vertical", "horizontal"]` | `"vertical"` | Swimlane orientation (`"vertical"` for side-by-side columns, `"horizontal"` for stacked rows). |

#### Diagram Methods:
- **`flow.add(item, xy=(0.0, 0.0), *, show=None) -> FlowNode | Junction`**:
  Registers a flow node (`Start`, `End`, `Process`, `Decision`, `Data`, `FlowNode`) or `Junction` centered at `(cx, cy)` in the diagram's coordinate space. Optionally overrides `item.show`.
- **`flow.add_lane(title, size=None, width=None, height=None, style=None, text_style=None, header_size=6.0, header_style=None, show=True) -> Lane`**:
  Adds a swimlane column (when `lane_orientation="vertical"`) or row (when `lane_orientation="horizontal"`).
- **`flow.connect(start, end, label="", arrow=None, routing="orthogonal", start_side="auto", end_side="auto", style=None, text_style=None, padding=0.0, show=True) -> FlowEdge`**:
  Creates and registers a `FlowEdge` between two connectables (`FlowNode` or `Junction`). When `arrow=None`, defaults to `"-"` if `end` is a `Junction`, otherwise `"->"`.
- **`flow.add_edge(edge, *, show=None) -> FlowEdge`**:
  Registers a pre-constructed `FlowEdge` instance on the diagram.
- **`flow.junction(xy, *, show=True) -> Junction`**:
  Creates and registers a zero-size routing waypoint / merge point at `xy`.
- **`flow.get_size() -> tuple[float, float]`**:
  Returns the total `(width, height)` of the diagram in unscaled local units.
- **`flow.draw(xy=(0.0, 0.0), *, align="bottom_left", scale=1.0) -> None`**:
  Renders the flowchart onto the active canvas anchored at `xy` (`align: Literal["bottom_left", "center"] = "bottom_left"`, `scale: float = 1.0`).

---

### 2.2 Standard Flowchart Symbols (`FlowNode` Subclasses)

All 5 semantic symbol classes inherit from `FlowNode(text="", shape="process", width=24.0, height=12.0, style=None, text_style=None, show=True)`:

| Class | Symbol / Geometry | `shape` (`ShapeType`) | Default Size (`width x height`) | Standard Usage |
| :--- | :--- | :--- | :--- | :--- |
| **`Start`** | Stadium / Pill | `"start"` | `20.0 x 10.0` | Initial entry point of the workflow |
| **`End`** | Stadium / Pill | `"end"` | `20.0 x 10.0` | Terminal exit point of the workflow |
| **`Process`** | Rectangle | `"process"` | `24.0 x 12.0` | Execution step, action, or operation |
| **`Decision`** | Rhombus / Diamond | `"decision"` | `24.0 x 14.0` | Conditional branch (`Yes`/`No`, `Valid`/`Invalid`) |
| **`Data`** | Parallelogram | `"data"` | `24.0 x 12.0` | Data input/output, payload, or file I/O |

```python
node = Process(
    text: str = "",
    width: float = 24.0,
    height: float = 12.0,
    style: Style | None = None,
    text_style: Style | None = None,
    show: bool = True,
)
```

---

### 2.3 Connections (`node.connect()`, `node.fork()`, `FlowEdge`, `Junction`)

- **`node.connect(...)` Signature**:
  ```python
  edge = node.connect(
      target: Connectable,
      label: str = "",
      arrow: ArrowType | None = None,
      routing: RoutingType = "orthogonal",
      start_side: Side = "auto",
      end_side: Side = "auto",
      style: Style | None = None,
      text_style: Style | None = None,
      padding: PaddingType = 0.0,
      show: bool = True,
  ) -> FlowEdge
  ```
  - `routing`: `"orthogonal"` (default right-angled L/Z-bends), `"direct"` (straight line), or `"curved"` (smooth spline).
  - `start_side` / `end_side`: `"auto"` (default), `"left"`, `"right"`, `"top"`, or `"bottom"`. Use explicit sides on `Decision` diamonds (e.g. `start_side="bottom"` for the primary path and `start_side="right"` for the alternate branch) to guarantee clean branch separation.
  - `arrow`: `"->"`, `"<-"`, `"<->"`, `"-"`, or `None` (resolves to `"-"` when connecting into a `Junction`, else `"->"`).
- **`node.fork(targets, at_x=None, at_y=None, style=None, padding=0.0, show=True) -> list[FlowEdge]`**:
  Splits a single outgoing stem from `node` into multiple `targets` via an auto-created `Junction` (placed at `at_x` or `at_y`, or midpoint by default).
- **`FlowEdge` Fluent Waypoint & Styling Methods**:
  - `edge.points(waypoints: list[tuple[float, float]]) -> Self`: Sets intermediate `(x, y)` waypoints.
  - `edge.via(*waypoints: tuple[float, float]) -> Self`: Variadic shorthand for `.points(list(waypoints))`.
  - `edge.add_point(xy: tuple[float, float]) -> Junction`: Appends an intermediate `(x, y)` waypoint and returns a connectable `Junction` at `xy` for branching.
  - `edge.set_label(text: str, pos: float = 0.5) -> Self`: Sets label text and normalized position (`0.0` to `1.0`).
  - `edge.set_arrow(arrow: ArrowType) -> Self`, `edge.set_style(style: Style) -> Self`, `edge.set_text_style(text_style: Style) -> Self`, `edge.set_padding(padding: PaddingType) -> Self`.

---

### 2.4 Swimlane Architecture (`flow.add_lane()` & `Lane`)

```python
lane = flow.add_lane(
    title: str,
    size: float | None = None,
    width: float | None = None,
    height: float | None = None,
    style: Style | None = None,
    text_style: Style | None = None,
    header_size: float = 6.0,
    header_style: Style | None = None,
    show: bool = True,
) -> Lane
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `title` | `str` | *(Required)* | Swimlane header banner text (e.g. `"Customer"`, `"Payment Service"`). |
| `size` | `float \| None` | `None` | Primary dimension of the lane (`width` for vertical lanes, `height` for horizontal lanes; defaults to `30.0` if neither `size` nor `width`/`height` is given). |
| `width` / `height` | `float \| None` | `None` | Explicit lane width or height alias for `size`. |
| `style` | `Style \| None` | `None` | Background fill and border style for the lane body. |
| `text_style` | `Style \| None` | `None` | Typography style for the lane header title. |
| `header_size` | `float` | `6.0` | Thickness of the lane header band (`height` for vertical lanes, `width` for horizontal lanes). |
| `header_style` | `Style \| None` | `None` | Optional distinct background/border style for the lane header band. |
| `show` | `bool` | `True` | Whether to render this swimlane band. |

- **Unified Global Coordinate System Across Swimlanes**:
  Swimlanes provide a structured visual background without trapping nodes inside isolated local coordinate frames. **All nodes share the diagram's global coordinate space**, so steps across different vertical lanes align horizontally by sharing the exact same `y` coordinate:
  - For vertical lanes of widths $W_0, W_1, W_2$, their horizontal centerlines are $X_0 = W_0 / 2$, $X_1 = W_0 + W_1 / 2$, $X_2 = W_0 + W_1 + W_2 / 2$.

---

## 3. Production Examples

### Example 3.1: Cross-Functional Vertical Swimlane Order Fulfillment
```drawlib align=center code=fold file=flow_swimlane_order.png caption="Cross-Functional Order Fulfillment Swimlane Flowchart"
from drawlib import canvas
from drawlib.diagrams.flow import Data, Decision, End, FlowDiagram, Process, Start
from drawlib.styles import Styles

canvas.clear()
canvas.setup(width=148, height=96)

flow = FlowDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold,
    title="E-Commerce Order Fulfillment Workflow",
    width=138,
    height=86,
    lane_orientation="vertical",
)

# 3 Vertical Swimlanes: widths 46 + 46 + 46 = 138 (centerlines at X = 23, 69, 115)
flow.add_lane("Customer", width=46, style=Styles.Neutral, header_style=Styles.PrimaryNeutral)
flow.add_lane("Payment Gateway", width=46, style=Styles.Neutral, header_style=Styles.SecondaryNeutral)
flow.add_lane("Warehouse", width=46, style=Styles.Neutral, header_style=Styles.PrimaryNeutral)

# Nodes placed on lane centerlines (X = 23, 69, 115)
start = flow.add(Start("Start Order", width=22, height=9, style=Styles.PrimaryFlat), xy=(23, 68))
submit = flow.add(Process("Submit Cart", width=26, height=11), xy=(23, 50))
verify = flow.add(Decision("Payment\nAuthorized?", width=28, height=15, style=Styles.WarningNeutral), xy=(69, 50))
declined = flow.add(Data("Decline Notice", width=26, height=11, style=Styles.DangerNeutral), xy=(23, 28))
pack = flow.add(Process("Pick & Pack\nItems", width=26, height=12, style=Styles.PrimaryNeutral), xy=(115, 50))
ship = flow.add(Process("Dispatch Parcel", width=26, height=11), xy=(115, 28))
done = flow.add(End("Order Closed", width=22, height=9, style=Styles.SecondaryFlat), xy=(69, 12))

# Connections with explicit decision attachment sides
start.connect(submit, padding=1.0)
submit.connect(verify, label="Charge", padding=1.0)
verify.connect(pack, label="Yes", start_side="right", end_side="left", padding=1.0)
verify.connect(declined, label="No", start_side="bottom", end_side="right", padding=1.0)
pack.connect(ship, padding=1.0)
declined.connect(done, start_side="bottom", end_side="left", padding=1.0)
ship.connect(done, start_side="bottom", end_side="right", padding=1.0)

flow.draw(xy=(5.0, 5.0))
canvas.save()
```

### Example 3.2: CI/CD Release Gate with `Junction` Merge & Loopback
```drawlib align=center code=fold file=flow_cicd_junction.png caption="CI/CD Pipeline with Waypoint Loopback and Junction Merge"
from drawlib import canvas
from drawlib.diagrams.flow import Decision, End, FlowDiagram, Process, Start
from drawlib.styles import Styles

canvas.clear()
canvas.setup(width=136, height=72)

flow = FlowDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark,
    title="CI/CD Automated Release Gate",
)

start = flow.add(Start("Git Push", width=20, height=10, style=Styles.PrimaryFlat), xy=(16, 36))
build = flow.add(Process("Build & Unit Test", width=26, height=12), xy=(48, 36))
check = flow.add(Decision("Tests Pass?", width=24, height=14, style=Styles.PrimaryNeutral), xy=(84, 36))
deploy = flow.add(Process("Deploy to Prod", width=26, height=12, style=Styles.SuccessNeutral), xy=(118, 50))
rollback = flow.add(Process("Alert & Abort", width=26, height=12, style=Styles.DangerNeutral), xy=(118, 22))
finish = flow.add(End("Done", width=18, height=10, style=Styles.SecondaryFlat), xy=(118, 36))

start.connect(build, padding=1.0)
build.connect(check, padding=1.0)
check.connect(deploy, label="Yes", start_side="top", end_side="left", padding=1.0)
check.connect(rollback, label="No", start_side="bottom", end_side="left", padding=1.0)
deploy.connect(finish, start_side="bottom", end_side="top", padding=1.0)
rollback.connect(finish, start_side="top", end_side="bottom", padding=1.0)

flow.draw(xy=(4.0, 4.0))
canvas.save()
```
