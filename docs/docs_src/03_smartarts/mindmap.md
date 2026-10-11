# MindMap Component

The `MindMapNode` component renders multi-directional, radial mindmaps and hierarchical feature maps centered around a central root topic. 
Branches can project to the left, right, top, or bottom, with automatic elbow connector routing.

```drawlib fold-code center file:mindmap_hero.png caption:"Overview of MindMapNode: Multi-Directional Radial Branching (left, right, top, bottom)"
from drawlib.canvas import save, setup
from drawlib.smartarts import MindMapNode
from drawlib.styles import Styles

setup(width=130, height=58)

root = MindMapNode(
    "Cloud Platform",
    shape="oval",
    width=26,
    height=9.5,
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=10.5),
    line_style=Styles.DarkBold,
    line_length=6.5,
    horizontal_margin=3.5,
    vertical_margin=3.8,
    children=[
        # Left Branch (shape="rectangle" + leaf shape="none")
        MindMapNode(
            "Ingress (left)",
            branch="left",
            shape="rectangle",
            width=22,
            height=7.5,
            style=Styles.PrimaryNeutral.patch(shape_r=1.2),
            text_style=Styles.DarkBold.patch(text_size=10.0),
            children=[
                MindMapNode("CDN Edge", shape="none", text_style=Styles.Dark.patch(text_size=10.0)),
                MindMapNode("WAF Rules", shape="none", text_style=Styles.Dark.patch(text_size=10.0)),
            ],
        ),
        # Right Branch (shape="rectangle" + leaf shape="none")
        MindMapNode(
            "Workloads (right)",
            branch="right",
            shape="rectangle",
            width=24,
            height=7.5,
            style=Styles.SecondaryNeutral.patch(shape_r=1.2),
            text_style=Styles.DarkBold.patch(text_size=10.0),
            children=[
                MindMapNode("gRPC API", shape="none", text_style=Styles.Dark.patch(text_size=10.0)),
                MindMapNode("Async Workers", shape="none", text_style=Styles.Dark.patch(text_size=10.0)),
            ],
        ),
        # Top Branch (branch="top")
        MindMapNode(
            "Control Plane (top)",
            branch="top",
            shape="rectangle",
            width=28,
            height=7.5,
            style=Styles.Neutral.patch(shape_r=1.2),
            text_style=Styles.DarkBold.patch(text_size=10.0),
        ),
        # Bottom Branch (branch="bottom")
        MindMapNode(
            "Storage Tier (bottom)",
            branch="bottom",
            shape="rectangle",
            width=28,
            height=7.5,
            style=Styles.Neutral.patch(shape_r=1.2),
            text_style=Styles.DarkBold.patch(text_size=10.0),
        ),
    ],
)

root.draw(xy=(63, 29))
save()
```

---

## 1. Quick Example: Architecture Topology Map

```drawlib show-code center file:mindmap_system_breakdown.png caption:"System Architecture Breakdown with MindMap"
from drawlib.canvas import setup
from drawlib.smartarts import MindMapNode
from drawlib.styles import Styles

setup(width=130, height=40)

root = MindMapNode(
    "API Gateway",
    shape="oval",
    width=26,
    height=11,
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=11.0),
    line_style=Styles.DarkBold,
    line_length=7.5,
    horizontal_margin=4.0,
    vertical_margin=4.0,
    children=[
        MindMapNode(
            "Clients", branch="left", shape="rectangle", width=20, height=8, style=Styles.Neutral,
            text_style=Styles.DarkBold.patch(text_size=10.5),
            children=[
                MindMapNode("Web Browser", shape="none", text_style=Styles.Dark.patch(text_size=10.0)),
                MindMapNode("Mobile App", shape="none", text_style=Styles.Dark.patch(text_size=10.0)),
            ],
        ),
        MindMapNode(
            "Services", branch="right", shape="rectangle", width=20, height=8, style=Styles.SecondaryNeutral,
            text_style=Styles.DarkBold.patch(text_size=10.5),
            children=[
                MindMapNode("Auth Service", shape="none", text_style=Styles.Dark.patch(text_size=10.0)),
                MindMapNode("Order Service", shape="none", text_style=Styles.Dark.patch(text_size=10.0)),
            ],
        ),
    ],
)

root.draw(xy=(62, 20))
```

---

## 2. Imperative Construction (`.add()`) & Top-Down Hierarchy (`branch="bottom"`, `xy_shift`)

Instead of passing nested `children=[...]` lists to the constructor, you can construct mindmaps and organization trees imperatively with `parent.add(text, ...) -> MindMapNode`. When calling `root.draw(xy, branch="bottom")`, all branches default to flowing top-down (`-y`). You can also fine-tune any node's placement relative to its auto-calculated position using `xy_shift=(dx, dy)`.

```drawlib show-code center file:mindmap_imperative_topdown.png caption:"Imperative MindMapNode Construction with Top-Down Branching (branch='bottom') and xy_shift"
from drawlib.canvas import save, setup
from drawlib.smartarts import MindMapNode
from drawlib.styles import Styles

setup(width=130, height=54)

root = MindMapNode(
    "Platform Engineering",
    shape="rectangle",
    width=34,
    height=9.5,
    style=Styles.PrimaryFlat.patch(shape_r=1.5),
    text_style=Styles.WhiteBold.patch(text_size=11.0),
    line_style=Styles.DarkBold,
    line_length=8.5,
    horizontal_margin=4.0,
    vertical_margin=3.5,
)

# 1. Left Subtree: Cloud Infrastructure
infra = root.add(
    "Cloud Infra",
    width=26,
    height=8.5,
    style=Styles.PrimaryNeutral.patch(shape_r=1.2),
    text_style=Styles.DarkBold.patch(text_size=10.5),
)
infra.add("EKS Clusters", shape="none", text_style=Styles.Dark.patch(text_size=10.0))
infra.add("Terraform IaC", shape="none", text_style=Styles.Dark.patch(text_size=10.0))

# 2. Center Subtree: Developer Experience (nudged slightly downward with xy_shift)
devex = root.add(
    "Developer Experience",
    width=31,
    height=8.5,
    style=Styles.SecondaryNeutral.patch(shape_r=1.2),
    text_style=Styles.DarkBold.patch(text_size=10.5),
    xy_shift=(0.0, -1.5),
)
devex.add("CI/CD Runners", shape="none", text_style=Styles.Dark.patch(text_size=10.0))
devex.add("Preview Envs", shape="none", text_style=Styles.Dark.patch(text_size=10.0))

# 3. Right Subtree: Security & SRE
sec = root.add(
    "Security & SRE",
    width=26,
    height=8.5,
    style=Styles.Neutral.patch(shape_r=1.2),
    text_style=Styles.DarkBold.patch(text_size=10.5),
)
sec.add("Zero-Trust Mesh", shape="none", text_style=Styles.Dark.patch(text_size=10.0))
sec.add("SLOs & Paging", shape="none", text_style=Styles.Dark.patch(text_size=10.0))

# Default branch direction in draw() is "bottom" (top-down org chart layout)
root.draw(xy=(65, 44), branch="bottom")
save()
```

---

## 3. Geometry, Cascading & Layout Mechanics

- **Center Anchor `(cx, cy)`**: The coordinate passed to `root.draw(xy=...)` anchors the **exact center** of the root node.
- **Root Mandatory Parameters**: The root `MindMapNode` **must** be initialized with `style`, `text_style`, and `line_style` (otherwise `root.draw()` raises a `ValueError`). If omitted on the root, `shape` defaults to `"rectangle"`, `width` to `20.0`, `height` to `8.0`, `horizontal_margin` to `4.0`, `vertical_margin` to `4.0`, and `line_length` to `10.0`. All descendant nodes inherit any unassigned style, shape, width/height, or spacing parameter from their parent.
- **Directional Branching (`branch`)**:
  - `"bottom"` *(default in `root.draw()`)*: Sub-branches extend downward (`-y`), ideal for top-down org charts and WBS trees.
  - `"top"`: Sub-branches extend upward (`+y`).
  - `"right"`: Sub-branches extend rightward (`+x`).
  - `"left"`: Sub-branches extend leftward (`-x`).
  - You can mix directions on the same root by setting `branch="left"`, `"right"`, `"top"`, or `"bottom"` on individual child nodes.
- **Node Shapes & Automatic Text Sizing (`shape`, `width`, `height`)**:
  - `"rectangle"`: Rectangular box with optional corner rounding (`style.shape_r`).
  - `"oval"`: Pill / ellipse container.
  - `"none"`: Clean borderless text label. When `shape="none"` and `width=None` / `height=None`, `MindMapNode` **automatically measures the text width and height** from `text_style.text_size` (including CJK wide-character compensation) so sibling labels never overlap.
- **Layout & Spacing Parameters**:
  - `horizontal_margin`: Horizontal gap between sibling subtrees when branching `"bottom"` or `"top"`.
  - `vertical_margin`: Vertical gap between sibling subtrees when branching `"left"` or `"right"`.
  - `line_length`: Orthogonal connector distance between parent and child hierarchy levels (with the right-angled fork junction placed at `line_length / 2`).
  - `xy_shift`: Optional `(dx, dy)` coordinate offset applied after automatic layout to fine-tune a node's position.

---

## 4. API Reference

### Constructor (`MindMapNode`)
```python
MindMapNode(
    text: str,
    *,
    branch: Literal["bottom", "top", "left", "right"] | None = None,
    shape: Literal["rectangle", "oval", "none"] | None = None,
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

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| **`text`** | `str` | *(Required)* | Text content displayed in this node. |
| **`branch`** | `Literal["bottom", "top", "left", "right"] \| None` | `None` | Branch direction for this node/subtree (inherits parent or `draw(branch=...)` default if `None`). |
| **`shape`** | `Literal["rectangle", "oval", "none"] \| None` | `None` | Node shape (root defaults to `"rectangle"` if `None`; children inherit parent `shape`). |
| **`width`** | `float \| None` | `None` | Node width (root defaults to `20.0`; auto-sized from text when `shape="none"` and `width=None`). |
| **`height`** | `float \| None` | `None` | Node height (root defaults to `8.0`; auto-sized from text when `shape="none"` and `height=None`). |
| **`style`** | `Style \| None` | `None` | Node shape style (**required on root**; inherited by children if `None`). |
| **`text_style`** | `Style \| None` | `None` | Node text style (**required on root**; inherited by children if `None`). |
| **`line_style`** | `Style \| None` | `None` | Connector line style (**required on root**; inherited by children if `None`). |
| **`horizontal_margin`** | `float \| None` | `None` | Horizontal gap between sibling subtrees (root defaults to `4.0`). |
| **`vertical_margin`** | `float \| None` | `None` | Vertical gap between sibling subtrees (root defaults to `4.0`). |
| **`line_length`** | `float \| None` | `None` | Connector span between parent and child levels (root defaults to `10.0`). |
| **`xy_shift`** | `tuple[float, float] \| None` | `None` | Optional `(dx, dy)` offset applied to this node after two-pass layout calculation. |
| **`children`** | `list[MindMapNode] \| None` | `None` | Initial list of child `MindMapNode` instances. |
| **`show`** | `bool` | `True` | Whether to render this node and its connectors (preserves subtree layout bounding boxes when `False`). |

### Adding Child Nodes (`.add()`)
```python
node.add(
    text: str,
    *,
    branch: Literal["bottom", "top", "left", "right"] | None = None,
    shape: Literal["rectangle", "oval", "none"] | None = None,
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
Creates a new child `MindMapNode` from `text: str` (note: `.add()` takes a string `text`, not a `MindMapNode` instance), appends it to `node.children`, and returns the newly created child `MindMapNode`.

### Drawing & Mutable Properties
```python
root.draw(
    xy: tuple[float, float],
    branch: Literal["bottom", "top", "left", "right"] = "bottom",
    scale: float = 1.0,
) -> None
```
- **`xy`**: Center coordinate `(cx, cy)` of the root node.
- **`branch`**: Fallback branch direction (`"bottom"`, `"top"`, `"left"`, `"right"`, default `"bottom"`) used when `root.branch` is `None`.
- **`scale`**: Proportional scale factor around `xy` (`> 0`, default `1.0`).
- **Mutable Node Properties**:
  - `node.text: str`
  - `node.branch: Literal["bottom", "top", "left", "right"] | None`
  - `node.shape: Literal["rectangle", "oval", "none"] | None`
  - `node.width: float | None`
  - `node.height: float | None`
  - `node.style: Style | None`
  - `node.text_style: Style | None`
  - `node.line_style: Style | None`
  - `node.children -> list[MindMapNode]`
  - `node.show: bool`

