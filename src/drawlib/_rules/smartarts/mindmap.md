# Drawlib MindMapNode SmartArt Guidelines (`lib-smartarts-mindmap`)

`MindMapNode` creates hierarchical diagrams, organization charts, decision trees, and multi-directional mindmaps with automatic right-angled orthogonal junction routing and two-pass subtree bounding-box layout.

---

## 1. Architecture & Two-Pass Layout

1. **Pass 1 (Subtree Extent Measurement)**: Recursively traverses subtrees bottom-up to compute the exact bounding width and height for every branch direction (`"bottom"`, `"top"`, `"left"`, `"right"`).
2. **Pass 2 (Orthogonal Fork Routing)**: Draws right-angled connector lines from parent nodes through auto-calculated junction buses to child nodes.
- **Anchor**: Coordinate `xy=(cx, cy)` specifies the **center point** of the root node.
- **Root Node Requirement**: The root `MindMapNode` must define `style`, `text_style`, and `line_style` (calling `draw()` without them raises `ValueError`). All other parameters (`shape`, `width`, `height`, `branch`, `horizontal_margin`, `vertical_margin`, `line_length`) cascade downward to descendants unless overridden on a child node.

---

## 2. Constructor, Properties & Node Methods

```python
MindMapNode(
    text: str,
    *,
    branch: Literal["bottom", "top", "left", "right"] | None = None,
    shape: Literal["rectangle", "ellipse", "none"] | None = None,
    width: float | None = None,
    height: float | None = None,
    style: Style | None = None,
    text_style: Style | None = None,
    line_style: Style | None = None,
    horizontal_margin: float | None = None,
    vertical_margin: float | None = None,
    line_length: float | None = None,
    xy_shift: tuple[float, float] | None = None,
    children: list[MindMapNode] | None = None,
    show: bool = True,
)
```

### Properties & Mutation Attributes

- `node.text: str`
- `node.branch: Literal["bottom", "top", "left", "right"] | None`
- `node.shape: Literal["rectangle", "ellipse", "none"] | None`
- `node.width: float | None`
- `node.height: float | None`
- `node.style: Style | None`
- `node.text_style: Style | None`
- `node.line_style: Style | None`
- `node.children: list[MindMapNode]`
- `node.show: bool`: Setting `child.show = False` hides that node and its incoming connector branch while keeping the full two-pass subtree bounding coordinates of all sibling nodes unchanged.

### Adding Children (`node.add` vs. `children=[...]`)

```python
child = node.add(
    text: str,
    *,
    branch: Literal["bottom", "top", "left", "right"] | None = None,
    shape: Literal["rectangle", "ellipse", "none"] | None = None,
    width: float | None = None,
    height: float | None = None,
    style: Style | None = None,
    text_style: Style | None = None,
    line_style: Style | None = None,
    horizontal_margin: float | None = None,
    vertical_margin: float | None = None,
    line_length: float | None = None,
    xy_shift: tuple[float, float] | None = None,
    show: bool = True,
) -> MindMapNode
```

> **Important — `node.add(text: str, ...)` Signature**:
> `node.add()` accepts **`text: str`** (not `child: MindMapNode | str`), constructs a new child `MindMapNode`, appends it to `node.children`, and returns the created child `MindMapNode`.
> Pre-constructed `MindMapNode(...)` instances can only be passed via `MindMapNode(..., children=[...])` (or appended to `node.children`).

### Drawing Method

```python
node.draw(
    xy: tuple[float, float],
    branch: Literal["bottom", "top", "left", "right"] = "bottom",
    scale: float = 1.0,
) -> Self
```

- `xy`: Center coordinate `(cx, cy)` of the root node.
- `branch`: Default branch direction for child nodes that do not specify `branch` (`"bottom"` by default: top-to-bottom hierarchy).
- `scale`: Proportional scale factor around `xy` (`1.0` by default).
- Returns `Self` for method chaining.

---

## 3. Shapes & Layout Options

- **`shape`**:
  - `"rectangle"` (default if omitted on root): Rounded or sharp rectangle (controlled via `style.shape_r`).
  - `"ellipse"`: Elliptical node body.
  - `"none"`: Text-only label without a surrounding border shape (width/height are estimated automatically from font size and text length if omitted).
- **`branch`**:
  - `"bottom"` (default): Branches downward (`-y`), ideal for org charts and top-down trees.
  - `"top"`: Branches upward (`+y`).
  - `"right"`: Branches rightward (`+x`).
  - `"left"`: Branches leftward (`-x`).
  - **Multi-Directional Radial MindMap**: Assign different `branch` directions (`"left"`, `"right"`, `"top"`, `"bottom"`) on direct children of the root node to radiate outward in all 4 directions.
- **`xy_shift`**: Optional `(dx, dy)` offset applied after layout calculation to fine-tune a node's position.

---

## 4. Production Example: Multi-Directional Architecture Overview

```drawlib code=show
from drawlib.canvas import save, setup
from drawlib.smartarts import MindMapNode
from drawlib.styles import Styles

setup(width=220, height=110)

txt_white = Styles.WhiteBold.patch(text_size=10.0)
txt_branch = Styles.DarkBold.patch(text_size=9.5)
txt_leaf = Styles.Dark.patch(text_size=9.5)

root = MindMapNode(
    "Core API Gateway",
    shape="ellipse",
    width=30,
    height=12,
    style=Styles.PrimaryFlat,
    text_style=txt_white,
    line_style=Styles.DarkBold,
    line_length=12.0,
    horizontal_margin=4.0,
    vertical_margin=4.0,
    children=[
        MindMapNode(
            "Client Traffic",
            branch="left",
            shape="rectangle",
            width=24,
            height=8,
            style=Styles.PrimaryNeutral,
            text_style=txt_branch,
            children=[
                MindMapNode("Web App (SPA)", shape="none", text_style=txt_leaf),
                MindMapNode("Mobile Apps", shape="none", text_style=txt_leaf),
                MindMapNode("Public REST API", shape="none", text_style=txt_leaf),
            ],
        ),
        MindMapNode(
            "Internal Services",
            branch="right",
            shape="rectangle",
            width=26,
            height=8,
            style=Styles.SecondaryNeutral,
            text_style=txt_branch,
            children=[
                MindMapNode("Auth Service", shape="rectangle", width=24, height=6, style=Styles.Neutral, text_style=txt_branch),
                MindMapNode("Billing Engine", shape="rectangle", width=24, height=6, style=Styles.Neutral, text_style=txt_branch),
                MindMapNode("Notification Hub", shape="rectangle", width=24, height=6, style=Styles.Neutral, text_style=txt_branch),
            ],
        ),
        MindMapNode(
            "Telemetry Stack",
            branch="top",
            shape="rectangle",
            width=26,
            height=8,
            style=Styles.Neutral,
            text_style=txt_branch,
            children=[
                MindMapNode("Prometheus Metrics", shape="none", text_style=txt_leaf),
                MindMapNode("OpenTelemetry Traces", shape="none", text_style=txt_leaf),
            ],
        ),
        MindMapNode(
            "Persistence Tier",
            branch="bottom",
            shape="rectangle",
            width=26,
            height=8,
            style=Styles.Neutral,
            text_style=txt_branch,
            children=[
                MindMapNode("PostgreSQL Primary", shape="none", text_style=txt_leaf),
                MindMapNode("Redis Cache Cluster", shape="none", text_style=txt_leaf),
            ],
        ),
    ],
)
root.draw(xy=(110, 55), branch="bottom")
save()
```
