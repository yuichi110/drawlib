# FlowDiagram: ISO Flowcharts & Cross-Functional Swimlanes

`FlowDiagram` implements standard flowchart symbols according to ISO 5807 and JIS X 0121 standards, with native support for cross-functional swimlane layouts (vertical columns or horizontal rows) sharing a unified global coordinate plane.

---

## 1. Overview & Standard Symbols

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

### Flowchart Symbol Classes

| Class | Shape Geometry | Default Size ($W \times H$) | Standard ISO Usage |
|---|---|---|---|
| `Start` | Stadium / Pill (`r=5.0`) | `20.0 x 10.0` | Initial entry point |
| `End` | Stadium / Pill (`r=5.0`) | `20.0 x 10.0` | Terminal completion point |
| `Process` | Rectangle | `24.0 x 12.0` | Execution task, calculation, or step |
| `Decision` | Rhombus / Diamond | `22.0 x 14.0` | Conditional branch (Yes/No, True/False) |
| `Data` | Parallelogram | `24.0 x 12.0` | Input, output, or file I/O |
| `Junction` | Coordinate point | `0.0 x 0.0` | Wire tap, waypoint, or merge junction |
| `Lane` | Boundary container | Dynamic | Swimlane column or row |

---

## 2. Global Coordinate Architecture & Core Methods

In Drawlib's `FlowDiagram`, swimlanes provide a structured visual background and column/row headers **without trapping nodes inside local relative coordinates**.

All nodes share a single global canvas coordinate system. This means:
- Steps occurring at the same stage in different departments can be placed at the exact same vertical $Y$ coordinate.
- Connecting lines cross swimlane boundaries cleanly with automatic orthogonal right-angle routing.

### Core Registration, Connection & Rendering Methods
- **`flow.add(node, xy=(x, y), *, show: bool = True) -> FlowNode`**: Places a flow node at `(x, y)` and returns the mutable `FlowNode` instance (`node.show`, `node.style`, `node.text_style`). If `show=False`, the node and its connected edges are hidden during rendering while diagram bounds remain unchanged.
- **`flow.add_lane(name, width=..., height=..., header_size=..., *, show: bool = True) -> Lane`**: Adds a vertical or horizontal swimlane (`show=False` hides the lane visual while keeping subsequent lane offsets fixed).
- **`node.connect(other, label="", start_side=None, end_side=None, routing="orthogonal", arrow="->", style=None, text_style=None, bend=0.25, show: bool = True) -> Edge`**: Connects two nodes and returns a mutable `Edge` (`edge.show`, `edge.style`, `edge.draw_ratio`, `edge.draw_direction`).
- **`flow.draw(xy=(0.0, 0.0), *, scale: float = 1.0) -> None`**: Renders the diagram at `xy`, proportionally scaling all coordinates, lane widths/heights, node dimensions, and font sizes by `scale`.

---

## 3. Vertical Swimlanes: Approval Workflow

The following example illustrates a multi-department expense reimbursement process across three vertical swimlanes:

```drawlib 650px center file:flow_approval_workflow.png caption:"Cross-Department Reimbursement Approval Workflow"
from drawlib import canvas
from drawlib.diagrams.flow import Data, Decision, End, FlowDiagram, Process, Start
from drawlib.styles import Styles

canvas.clear()
canvas.setup(width=110, height=95)

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
```

---

## 4. Horizontal Swimlanes: Order Logistics

By specifying `lane_orientation="horizontal"`, lanes are laid out as stacked horizontal bands:

```drawlib 650px center file:flow_fulfillment_pipeline.png caption:"Fulfillment Logistics Horizontal Pipeline"
from drawlib import canvas
from drawlib.diagrams.flow import Decision, End, FlowDiagram, Process, Start
from drawlib.styles import Styles

canvas.clear()
canvas.setup(width=145, height=80)

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
```

---

## 5. Best Practices & Guidelines

1. **Explicit Decision Exits**: Always specify `start_side` (e.g. `start_side="right"` for "No", `start_side="bottom"` for "Yes") on `Decision` nodes to keep branch directions clear and consistent.
2. **Merge with `flow.junction`**: When multiple paths lead to a single destination or pass through a bottleneck, route them through an intermediate junction to prevent crossing lines.
3. **Lane Width Balancing**: Ensure lane widths accommodate the widest nodes with at least 5 coordinate units of padding on either side.
