# FlowDiagram: ISO Flowcharts & Cross-Functional Swimlanes

`FlowDiagram` implements standard flowchart symbols according to ISO 5807 and JIS X 0121 standards, with native support for cross-functional swimlane layouts (vertical columns or horizontal rows) sharing a unified global coordinate plane.

---

## 1. Overview & Standard Symbols

```drawlib fold-code 650px center file:flow_standard_symbols.png caption:"ISO 5807 Flowchart Symbol Classes in FlowDiagram"
from drawlib.canvas import save, setup
from drawlib.diagrams.flow import Data, Decision, End, FlowDiagram, Process, Start
from drawlib.shapes import circle
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=152, height=62)

flow = FlowDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark,
    width=144.0,
    height=54.0,
)

# 6 Standard Flowchart Symbol Classes: Start, Data, Process, Decision, Junction, End
s_start = flow.add(Start("Start\n(Terminal)", width=22.0, height=11.0, style=Styles.PrimaryNeutral), xy=(15.0, 40.0))
s_data = flow.add(Data("Data\n(Input / I/O)", width=26.0, height=12.0), xy=(52.0, 40.0))
s_proc = flow.add(Process("Process\n(Operation)", width=26.0, height=12.0), xy=(90.0, 40.0))
s_dec = flow.add(Decision("Decision\n(Branch?)", width=26.0, height=15.0, style=Styles.SecondaryNeutral), xy=(90.0, 15.0))

# Junction waypoint for orthogonal retry loop back to Data
j_retry = flow.junction((52.0, 15.0))
s_end = flow.add(
    End("End\n(Complete)", width=22.0, height=11.0, style=Styles.PrimaryFlat, text_style=Styles.WhiteBold),
    xy=(130.0, 15.0),
)

s_start.connect(s_data)
s_data.connect(s_proc)
s_proc.connect(s_dec, start_side="bottom", end_side="top")
s_dec.connect(s_end, label="Yes", start_side="right", end_side="left")
s_dec.connect(j_retry, label="No", start_side="left", end_side="right")
j_retry.connect(s_data, label="Retry", end_side="bottom")

flow.draw(xy=(4.0, 4.0))

# Highlight the zero-size Junction coordinate point (4 + 52 = 56, 4 + 15 = 19)
circle((56.0, 19.0), radius=1.3, style=Styles.PrimaryFlat)
text(
    (56.0, 14.0),
    "Junction (x, y)",
    style=Styles.DarkBold.patch(text_size=8.5, text_color=Colors.Primary5),
)

save()
```

### Flowchart Symbol Classes

| Class | Shape Geometry | Default Size ($W \times H$) | Standard ISO Usage |
|---|---|---|---|
| `Start` | Stadium / Pill (`shape_r=5.0`) | `20.0 x 10.0` | Initial entry point |
| `End` | Stadium / Pill (`shape_r=5.0`) | `20.0 x 10.0` | Terminal completion point |
| `Process` | Rectangle | `24.0 x 12.0` | Execution task, calculation, or step |
| `Decision` | Rhombus / Diamond | `22.0 x 14.0` | Conditional branch (Yes/No, True/False) |
| `Data` | Parallelogram | `24.0 x 12.0` | Input, output, or file I/O |
| `Junction` | Coordinate point | `0.0 x 0.0` | Wire tap, waypoint, or merge junction |
| `Lane` | Boundary container | Dynamic | Swimlane column or row |

---

## 2. Global Coordinate Architecture & Core API Reference

In Drawlib's `FlowDiagram`, swimlanes provide a structured visual background and column/row headers **without trapping nodes inside local relative coordinates**.

All nodes share a single global canvas coordinate system (`flow.add(node, xy=(cx, cy))` places the **center `(cx, cy)`** of the shape). This means:
- Steps occurring at the same stage in different departments can be placed at the exact same vertical $Y$ coordinate.
- Connecting lines cross swimlane boundaries cleanly with automatic orthogonal right-angle routing.

### Parameter Reference Tables

#### `FlowDiagram` Class
| Parameter | Type | Default | Description |
|---|---|---|---|
| `node_style` | `Style` | *(Required)* | Base `Style` object for flowchart shapes in the diagram. |
| `edge_style` | `Style` | *(Required)* | Base `Style` object for connection lines and arrowheads. |
| `edge_text_style` | `Style` | *(Required)* | Base `Style` object for connection text labels. |
| `title` | `str` | `""` | Optional banner title displayed above the diagram. |
| `title_style` | `Style \| None` | `None` | Optional `Style` override for the diagram title. |
| `width` | `float \| None` | `None` | Optional fixed width of the diagram canvas (auto-fit if `None`). |
| `height` | `float \| None` | `None` | Optional fixed height of the diagram canvas (auto-fit if `None`). |
| `style` | `Style \| None` | `None` | Optional `Style` for the overall diagram background card. |
| `lane_orientation` | `Literal["vertical", "horizontal"]` | `"vertical"` | Swimlane layout orientation (`"vertical"` columns or `"horizontal"` rows). |

#### `FlowNode` & Concrete Node Classes (`Start`, `End`, `Process`, `Decision`, `Data`)
| Parameter | Type | Default | Description |
|---|---|---|---|
| `text` | `str` | `""` (`"Start"` / `"End"` on terminals) | Text label centered inside the flowchart symbol (supports `\n`). |
| `width` | `float` | `24.0` (`20.0` for `Start`/`End`, `22.0` for `Decision`) | Outer width of the symbol in canvas units. |
| `height` | `float` | `12.0` (`10.0` for `Start`/`End`, `14.0` for `Decision`) | Outer height of the symbol in canvas units. |
| `style` | `Style \| None` | `None` | Optional `Style` override for shape fill, border stroke, and `shape_r`. |
| `text_style` | `Style \| None` | `None` | Optional `Style` override for the node text label. |
| `shape_type` | `Literal["process", "decision", "start", "end", "data"]` | `"process"` | Underlying symbol geometry (`FlowNode` base constructor only). |
| `show` | `bool` | `True` | Visibility flag (connected `FlowEdge` lines auto-hide when `False`). |

- **Anchor & Geometry Properties on `FlowNode`**: `node.xy`, `node.center`, `node.top`, `node.bottom`, `node.left`, `node.right`, `node.get_anchor(side="auto")`, and `node.get_bounds()`.

### Core Registration, Swimlane, Connection & Waypoint Methods

- **Node Registration (`flow.add`)**:
  ```python
  flow.add(item: FlowNode | Junction, xy: tuple[float, float], *, show: bool | None = None) -> FlowNode | Junction
  ```
  Places `item` at center coordinate `xy` and returns the mutable instance (`node.show`, `node.style`, `node.text_style`). If `show=False`, the node and its connected edges are hidden during rendering while diagram bounds remain unchanged.
- **Swimlane Registration (`flow.add_lane`)**:
  ```python
  flow.add_lane(
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
  Adds a vertical column (`width` or `size`, default `30.0`) or horizontal row (`height` or `size`, default `30.0`) swimlane and returns the `Lane` instance. Setting `show=False` hides the lane visual while keeping subsequent lane offsets fixed.
- **Connecting Nodes (`FlowNode.connect` & `flow.connect`)**:
  ```python
  node.connect(
      target: FlowNode | Junction,
      label: str = "",
      arrow: Literal["->", "<-", "<->", "-"] | None = None,
      routing: Literal["orthogonal", "direct"] = "orthogonal",
      start_side: Literal["left", "right", "top", "bottom", "auto"] = "auto",
      end_side: Literal["left", "right", "top", "bottom", "auto"] = "auto",
      style: Style | None = None,
      text_style: Style | None = None,
      padding: float | tuple[float, float] = 0.0,
      show: bool = True,
  ) -> FlowEdge
  ```
  Also callable at the diagram level via `flow.connect(start, end, ...) -> FlowEdge` (or `flow.add_edge(edge, *, show=None) -> FlowEdge`). When `arrow=None`, defaults to `"-"` if `target` is a `Junction`, otherwise `"->"`.
- **1-to-N Bus Fan-Out (`FlowNode.fork`) & `Junction`**:
  - **`node.fork(targets: list[Connectable], at_x: float | None = None, at_y: float | None = None, style: Style | None = None, padding: float | tuple[float, float] = 0.0, show: bool = True) -> list[FlowEdge]`**: Branches from `node` to multiple targets through an intermediate `Junction`.
  - **`flow.junction(xy: tuple[float, float], *, show: bool = True) -> Junction`**: Creates and registers a zero-size connectable waypoint at `xy` (`j.connect(...)`).
- **`FlowEdge` Waypoint Methods**:
  - **`edge.points(waypoints: list[tuple[float, float]]) -> FlowEdge`**: Sets explicit intermediate `(x, y)` waypoints and returns `self`.
  - **`edge.via(*waypoints: tuple[float, float]) -> FlowEdge`**: Unpacked variadic shorthand for `.points(list(waypoints))`.
  - **`edge.add_point(xy: tuple[float, float]) -> Junction`**: Appends `xy` as a waypoint on `edge` and returns a branching `Junction` registered at `xy`.
- **Sizing & Rendering (`flow.get_size` & `flow.draw`)**:
  - **`flow.get_size() -> tuple[float, float]`**: Returns the overall `(width, height)` of the diagram.
  - **`flow.draw(xy=(0.0, 0.0), *, scale: float = 1.0) -> None`**: Renders the diagram anchored at bottom-left `xy`, proportionally scaling all coordinates, lane widths/heights, node dimensions, and font sizes by `scale`.

---

## 3. Vertical Swimlanes: Approval Workflow

The following example illustrates a multi-department expense reimbursement process across three vertical swimlanes:

```drawlib show-code 650px center file:flow_approval_workflow.png caption:"Cross-Department Reimbursement Approval Workflow"
from drawlib.canvas import save, setup
from drawlib.diagrams.flow import Data, Decision, End, FlowDiagram, Process, Start
from drawlib.styles import Styles

setup(width=110, height=95)

flow = FlowDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark,
    title="Expense Reimbursement Approval Workflow",
    width=100.0,
    height=90.0,
)

# 1. Define vertical department lanes (columns from left to right)
flow.add_lane("Employee", width=30.0)
flow.add_lane("Line Manager", width=35.0)
flow.add_lane("Finance Dept", width=35.0)

# 2. Add nodes (Y coordinates align corresponding steps horizontally)
submit = flow.add(Start("Submit Claim"), xy=(15.0, 78.0))
receipt = flow.add(Data("Attach Receipt"), xy=(15.0, 62.0))
review = flow.add(
    Process("Review Details", style=Styles.PrimaryFlat, text_style=Styles.WhiteBold),
    xy=(47.5, 62.0),
)
decision = flow.add(Decision("Amount < $500?", style=Styles.SecondaryNeutral), xy=(47.5, 42.0))

audit = flow.add(Process("Compliance Audit"), xy=(82.5, 42.0))
auto_pay = flow.add(Process("Disburse Payment", style=Styles.PrimaryNeutral), xy=(82.5, 20.0))
end = flow.add(End("Claim Closed"), xy=(15.0, 20.0))

# 3. Connect steps
submit.connect(receipt)
receipt.connect(review)
review.connect(decision)

# Decision routing (separate vertical levels avoid label collisions)
decision.connect(audit, label="No", start_side="right", end_side="left")
decision.connect(auto_pay, label="Yes", start_side="bottom", end_side="left")
audit.connect(auto_pay, start_side="bottom", end_side="top")
auto_pay.connect(end, label="Notice Sent", start_side="left", end_side="right")

flow.draw(xy=(5.0, 5.0))
save()
```

---

## 4. Horizontal Swimlanes: Order Logistics

By specifying `lane_orientation="horizontal"`, lanes are laid out as stacked horizontal bands:

```drawlib show-code 650px center file:flow_fulfillment_pipeline.png caption:"Fulfillment Logistics Horizontal Pipeline"
from drawlib.canvas import save, setup
from drawlib.diagrams.flow import Decision, End, FlowDiagram, Process, Start
from drawlib.styles import Styles

setup(width=145, height=80)

flow = FlowDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark,
    title="Fulfillment Logistics Pipeline",
    lane_orientation="horizontal",
    width=130.0,
    height=65.0,
)

flow.add_lane("Sales Platform", height=32.5, header_size=22.0)
flow.add_lane("Distribution Center", height=32.5, header_size=22.0)

order = flow.add(Start("New Purchase", width=22.0), xy=(36.0, 48.0))
validate = flow.add(Decision("In Stock?", style=Styles.SecondaryNeutral), xy=(68.0, 48.0))
cancel = flow.add(End("Cancel & Refund", width=26.0), xy=(112.0, 48.0))
pack = flow.add(Process("Pick & Pack", style=Styles.PrimaryFlat, text_style=Styles.WhiteBold), xy=(68.0, 16.0))
dispatch = flow.add(End("Ship Carrier", width=24.0), xy=(112.0, 16.0))

order.connect(validate)
validate.connect(cancel, label="No", start_side="right", end_side="left")
validate.connect(pack, label="Yes", start_side="bottom", end_side="top")
pack.connect(dispatch)

flow.draw(xy=(8.0, 5.0))
save()
```

---

## 5. Best Practices & Guidelines

1. **Explicit Decision Exits**: Always specify `start_side` (e.g. `start_side="right"` for "No", `start_side="bottom"` for "Yes") on `Decision` nodes to keep branch directions clear and consistent.
2. **Merge with `flow.junction`**: When multiple paths lead to a single destination or pass through a bottleneck, route them through an intermediate junction to prevent crossing lines.
3. **Lane Width Balancing**: Ensure lane widths accommodate the widest nodes with at least 5 coordinate units of padding on either side.
