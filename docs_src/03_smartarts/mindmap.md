# MindMap Component

The `MindMapNode` component renders multi-directional, radial mindmaps and hierarchical feature maps centered around a central root topic. 
Branches can project to the left, right, top, or bottom, with automatic elbow connector routing.

---

## 1. Quick Example: Architecture Topology Map

```drawlib 650px center file:mindmap_system_breakdown.png caption:"System Architecture Breakdown with MindMap"
from drawlib.canvas import setup
from drawlib.smartarts import MindMapNode
from drawlib.styles import Styles

setup(width=140, height=80)

root = MindMapNode(
    "API Gateway",
    shape="oval",
    size=(28, 12),
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold,
    line_style=Styles.DarkBold,
    line_length=12.0,
    horizontal_margin=4.0,
    vertical_margin=4.0,
    children=[
        MindMapNode(
            "Clients", branch="left", shape="rectangle", size=(20, 8), style=Styles.Neutral, text_style=Styles.DarkBold,
            children=[
                MindMapNode("Web Browser", shape="none", text_style=Styles.Dark),
                MindMapNode("Mobile App", shape="none", text_style=Styles.Dark),
            ],
        ),
        MindMapNode(
            "Services", branch="right", shape="rectangle", size=(20, 8), style=Styles.SecondaryNeutral, text_style=Styles.DarkBold,
            children=[
                MindMapNode("Auth Service", shape="none", text_style=Styles.Dark),
                MindMapNode("Order Service", shape="none", text_style=Styles.Dark),
            ],
        ),
    ],
)

root.draw(xy=(70, 40))
```

---

## 2. Geometry & Branching Directions

- **Center Anchor `(cx, cy)`**: The coordinate passed to `root.draw(xy=...)` anchors the **exact center** of the central root node.
- **Directional Branching (`branch`)**:
  - `"right"` *(default)*: Sub-branches extend to the right (`+x`).
  - `"left"`: Sub-branches extend to the left (`-x`).
  - `"top"`: Sub-branches extend upward (`+y`).
  - `"bottom"`: Sub-branches extend downward (`-y`).
- **Node Shapes**:
  - `"oval"`: Pill / ellipse container.
  - `"rectangle"`: Rectangular box with optional corner rounding (`r`).
  - `"none"`: Clean text label without border or background fill.

---

## 3. Node Class API

```python
MindMapNode(
    text: str,
    *,
    branch: Literal["left", "right", "top", "bottom"] | None = None,
    shape: Literal["oval", "rectangle", "none"] | None = None,
    size: tuple[float, float] | None = None,
    style: Style | None = None,
    r: float | None = None,
    text_style: Style | None = None,
    line_style: Style | None = None,
    horizontal_margin: float | None = None,
    vertical_margin: float | None = None,
    line_length: float | None = None,
    xy_shift: tuple[float, float] | None = None,
    children: list[MindMapNode] | None = None,
)
```
