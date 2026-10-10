# Drawlib SmartArts Guidelines

The `drawlib.smartarts` module provides high-level graphical components designed for "Illustration as Code." These components automate the layout, geometry, text positioning, and styling of structured diagrams—including tabular datasets, organizational trees, mindmaps, process pipelines, cyclical workflows, matrix grids, tiered pyramids, bulleted lists, syntax-highlighted source code, and speech callouts.

---
## Table of Contents

1. [Architectural Overview & Core Concepts](#1-architectural-overview--core-concepts)
2. [Quick Reference Matrix](#2-quick-reference-matrix)
3. [Component 1: Table](#3-component-1-table)
4. [Component 2: TreeNode (Directory & Hierarchy Trees)](#4-component-2-treenode-directory--hierarchy-trees)
5. [Component 3: BoxList](#5-component-3-boxlist)
6. [Component 4: MindMapNode (Radial & Multi-Directional Trees)](#6-component-4-mindmapnode-radial--multi-directional-trees)
7. [Component 5: ChevronProcess (Pipeline & Workflow Stages)](#7-component-5-chevronprocess-pipeline--workflow-stages)
8. [Component 6: Cycle (Circular & Feedback Loops)](#8-component-6-cycle-circular--feedback-loops)
9. [Component 7: GridLayout (Matrix Cards & Architecture Layers)](#9-component-7-gridlayout-matrix-cards--architecture-layers)
10. [Component 8: Pyramid (Tiered Stacks & Hierarchies)](#10-component-8-pyramid-tiered-stacks--hierarchies)
11. [Component 9: BulletPoints (Formatted Bulleted Lists)](#11-component-9-bulletpoints-formatted-bulleted-lists)
12. [Component 10: SourceCode (Syntax-Highlighted Code Containers)](#12-component-10-sourcecode-syntax-highlighted-code-containers)
13. [Component 11: GeoMap (Geographical Vector Maps)](#12b-component-11-geomap-geographical-vector-maps)
14. [Design Patterns & Coordinate Anchor Systems](#13-design-patterns--coordinate-anchor-systems)
15. [Troubleshooting & Common Pitfalls](#14-troubleshooting--common-pitfalls)

---
## 1. Architectural Overview & Core Concepts

### 1.1 Imports
All SmartArts classes and helper functions are exported directly from `drawlib.smartarts`:
```python
from drawlib.smartarts import (
    BoxList,
    BulletPoints,
    ChevronProcess,
    Cycle,
    GeoMap,
    GridLayout,
    MindMapNode,
    Pyramid,
    SourceCode,
    Table,
    TreeNode,
)
```

Common auxiliary imports required for canvas setup, styling, and colors:
```python
from drawlib.canvas import save, setup
from drawlib.preset_colors import CssColors
from drawlib.styles import Colors, Styles
from drawlib.types import Style
```

### 1.2 Coordinate Anchor Conventions
Understanding anchor points is essential for programmatic generation and positioning:
- **Top-Left Anchored**: `Table`, `TreeNode`, `BulletPoints`. You specify top-left coordinate `(x, y)`; elements flow rightward and downward.
- **Bottom-Left Anchored**: `ChevronProcess`, `GridLayout`, `Pyramid`, `GeoMap`. You specify bottom-left coordinate `(x, y)` of the bounding box; elements extend rightward and upward.
- **Center Anchored**: `MindMapNode` (root node center `(x, y)`), `Cycle` (default `align="center"` anchors orbit center).

### 1.3 Style Resolution
Every SmartArt accepts:
- A `Style` instance: `Style(shape_fill_color=Colors.Blue, shape_line_color=Colors.White, shape_line_width=1.5)`
- A predefined theme style from `drawlib.styles.Styles`: `Styles.Primary`, `Styles.SecondaryFlat`, `Styles.WhiteBold`, `Styles.PrimaryBold`, etc.
- `None`: falls back to default component styles or canvas theme defaults.

### 1.4 Unified Component Lifecycle (`add()`, `show`, Deferred Mutation & `scale`)
All SmartArts follow a unified 4-phase lifecycle (**1. Instantiate -> 2. Register via `add()` -> 3. Mutate State -> 4. Render via `draw()`**):
1. **Standardized Registration (`add(..., show=True)`)**: Every item-based SmartArt (`BoxList`, `ChevronProcess`, `Cycle`, `GridLayout`, `Pyramid`, `BulletPoints`, `TreeNode`, `MindMapNode`) uses `.add(...)` to register elements and returns a reference to the newly created item object.
2. **Layout-Preserving Visibility (`item.show`)**: Every item exposes `item.show: bool = True`. Setting `item.show = False` skips drawing that specific element while **keeping the overall component geometry, item widths, orbit angles, and grid/tree coordinates completely unchanged**.
3. **Deferred Style & Text Evaluation**: Item attributes (`item.style`, `item.text_style`, `item.text`, `item.description`, etc.) are resolved lazily inside `draw()`. Mutating an item's style or text between `draw()` calls immediately reflects on the next render without reconstructing the component.
4. **Proportional Scaling (`scale: float = 1.0`)**: Every `draw(...)` and `draw_flexible(...)` method accepts `scale: float = 1.0`. Passing `scale != 1.0` uniformly scales all shapes, margins, corner radii, line widths, and font sizes relative to the anchor coordinate `xy`.

---
## 2. Quick Reference Matrix

| Component | Anchor Point | Layout Direction | Key Methods | Typical Architecture Use Cases |
| :--- | :--- | :--- | :--- | :--- |
| `Table` | Top-Left `(x, y)` | Downward & Rightward | `set_style_*()`, `draw(scale=1.0)`, `draw_flexible(scale=1.0)` | Service matrices, SLA comparisons, feature tables |
| `TreeNode` | Top-Left `(x, y)` | Downward tree lines | `add(show=True)`, `register_drawing_item()`, `draw(scale=1.0)` | Monorepo directories, file trees, package layouts |
| `BoxList` | Directional `(x, y)` | `"left"`, `"right"`, `"bottom"`, `"top"` | `add(show=True)`, `draw(scale=1.0)` | Microservice cards, pipeline stages, status badges |
| `MindMapNode` | Center `(x, y)` | Radial (4 directions) | `add(show=True)`, `draw(branch=..., scale=1.0)` | Architecture overviews, decision trees, org charts |
| `ChevronProcess` | Bottom-Left `(x, y)` | Horizontal linear | `add(show=True)`, `draw(scale=1.0)` | CI/CD pipelines, ETL workflows, order lifecycles |
| `Cycle` | Center / Bottom-Left | Radial circular | `add(show=True)`, `set_center(show=True)`, `draw(scale=1.0)` | PDCA DevOps loops, token refresh cycles, state machines |
| `GridLayout` | Bottom-Left `(x, y)` | Matrix grid cells | `add(show=True)`, `draw(scale=1.0)`, `draw_flexible(scale=1.0)` | Multi-tier architecture layers, dashboard panels |
| `Pyramid` | Bottom-Left `(x, y)` | Stacked layers | `add(show=True)`, `draw(scale=1.0)`, `draw_flexible(scale=1.0)` | Defense-in-depth, testing pyramid, memory hierarchies |
| `BulletPoints` | Top-Left `(x, y)` | Downward list | `add(show=True)`, `set_indent()`, `set_bullet_style()`, `draw(scale=1.0)` | Architecture takeaways, RFC summaries, feature lists |
| `SourceCode` | Top-Left `(x, y)` | Vector code block | `draw(scale=1.0)`, `get_text()` | Embedded configuration, code samples, API payloads |
| `GeoMap` | Bottom-Left `(x, y)` | Equirectangular vector map | `get_areas()`, `set_area_styles()`, `draw()`, `get_area_xy()`, `lonlat_to_xy()` | Multi-region cloud topology, country/city territory maps |

---
## 3. Component 1: Table

`Table` renders 2D tabular data with precise styling control over borders, header cells, even/odd alternating rows, and individual cell coordinates.

### 3.1 Architecture & Coordinate Mechanics
- **Anchor**: Top-Left coordinate `xy=(x, y)`. The first row starts at `y`, and subsequent rows move downward (`y - row_height`).
- **Data Shape**: 2D list of any serializable values (`list[list[Any]]`).
- **Sizing Modes**:
  - `draw(xy, width, height, data, scale=1.0)`: Uniform column widths (`width / cols`) and row heights (`height / rows`), with optional proportional scaling around `xy`.
  - `draw_flexible(xy, column_widths, row_heights, data, scale=1.0)`: Explicit per-column and per-row sizing, with optional proportional scaling around `xy`.

### 3.2 Constructor & Style Methods
```python
table = Table(
    cell_style=Styles.White,
    text_style=Styles.Primary,
    header_cell_style=Styles.PrimaryThin,
    header_text_style=Styles.PrimaryBold,
    border_style=Styles.MutedThin,
    has_header=True,
)
```

- `Table(*, cell_style, text_style, header_cell_style, header_text_style, border_style, has_header=True)`:
  Initializes table with mandatory styles for cell background, text, header cells, header text, and borders.
- `reset_styles()`: Resets all cell and border style overrides back to initial settings.

#### Cell Styling Methods
- `set_style_cell_headers(background_color, text_style)`: Applies background and text style to both row 0 and column 0.
- `set_style_cell_header(background_color, text_style)`: Applies style exclusively to column headers (row 0).
- `set_style_cell_rowheader(background_color, text_style)`: Applies style exclusively to row headers (column 0).
- `set_style_cell_evenodd(even_color, even_text_style, odd_color, odd_text_style)`: Alternating styles for even/odd data rows.
- `set_style_cell(background_color, text_style, rows=None, columns=None)`: Targets specific rows or columns (0-indexed indices).

#### Border Styling Methods
- `set_style_border(top=None, top2=None, bottom=None, left=None, left2=None, right=None, between_columns=None, between_rows=None)`:
  - `top`, `bottom`, `left`, `right`: Perimeter border lines.
  - `top2`: Secondary top border line beneath header row.
  - `left2`: Secondary vertical line to right of row header column.
  - `between_columns`: Vertical separator lines between inner data columns.
  - `between_rows`: Horizontal separator lines between inner data rows.

### 3.3 Production Example: Microservice SLA & Availability Table
```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.preset_colors import CssColors
from drawlib.smartarts import Table
from drawlib.styles import Colors, Styles
from drawlib.types import Style

setup(width=120, height=65)

table = Table(
    cell_style=Styles.White,
    text_style=Styles.Primary.patch(text_color=Colors.Dark, text_size=10),
    header_cell_style=Styles.Primary.patch(shape_fill_color=Colors.Dark),
    header_text_style=Styles.WhiteBold,
    border_style=Styles.Primary.patch(line_color=Colors.Dark, line_width=1.5),
)

table.set_style_cell_evenodd(
    even_color=Colors.Light,
    even_text_style=Styles.Primary.patch(text_color=Colors.Dark, text_size=10),
    odd_color=Colors.White,
    odd_text_style=Styles.Primary.patch(text_color=Colors.Dark, text_size=10),
)
# SLA highlight (Row 2, Column 3)
table.set_style_cell(
    background_color=CssColors.PaleGreen,
    text_style=Styles.Primary.patch(text_color=CssColors.ForestGreen, text_size=10),
    rows=[2],
    columns=[3],
)
table.set_style_border(
    top=Styles.Primary.patch(line_color=Colors.Dark, line_width=1.5),
    top2=Styles.Primary.patch(line_color=Colors.Dark, line_width=1.0),
    bottom=Styles.Primary.patch(line_color=Colors.Dark, line_width=1.5),
    between_rows=Styles.Primary.patch(line_color=CssColors.LightGray, line_width=0.5),
)

sla_data = [
    ["Service Name", "Protocol", "P99 Latency", "Availability", "Tier"],
    ["Auth Gateway", "gRPC / HTTPS", "18 ms", "99.99 %", "Tier 0"],
    ["Order Engine", "gRPC", "8 ms", "99.999 %", "Tier 0"],
    ["Notification", "Async Kafka", "120 ms", "99.9 %", "Tier 2"],
    ["Analytics", "Batch REST", "450 ms", "99.5 %", "Tier 3"],
]
table.draw_flexible(xy=(10, 55), column_widths=[30, 22, 20, 18, 10], row_heights=[8, 8, 8, 8, 8], data=sla_data)
save()
```

---
## 4. Component 2: TreeNode (Directory & Hierarchy Trees)

`TreeNode` renders hierarchical file-tree and directory-like terminal listings with orthogonal connector lines, customized text styles, and support for prepended/appended custom icons.

### 4.1 Architecture & Geometry
- **Anchor**: Top-Left coordinate `xy=(x, y)`. Root text is drawn at `xy`, and descendant branches step downward: `child_y = current_y - line_vertical_margin`.
- **Root Node Requirement**: Root `TreeNode` must define settings for propagation: `text_style`, `line_style`, `line_horizontal_margin`, `line_horizontal_length`, and `line_vertical_margin`. Child nodes inherit these settings automatically via cascading unless individually overridden.

### 4.2 Constructor & Node Methods
```python
TreeNode(
    text: str,
    *,
    text_style: Style | None = None,
    line_style: Style | None = None,
    line_horizontal_margin: float | None = None,
    line_horizontal_length: float | None = None,
    line_vertical_margin: float | None = None,
    children: list[TreeNode] | None = None,
    show: bool = True,
)
```
- `node.add(child: TreeNode | str, *, text_style=None, line_style=None, ..., show: bool = True) -> TreeNode`: Appends a child `TreeNode` (or constructs one from a string) and returns the child `TreeNode` instance. Setting `child.show = False` hides the node and its connector tick while preserving vertical row spacing for all sibling/following nodes.
- `node.draw(xy, scale=1.0)`: Renders the tree hierarchy starting at top-left `xy` with optional proportional scaling.

### 4.3 Custom Drawing Items (Icons & Badges)
Register icon functions (e.g. Phosphor icons) before or after node text:
- `TreeNode.register_drawing_item(name, location, padding_width, function, style, args)`:
  - `location`: `"before"` (prepends icon to left) or `"after"` (appends to right).
  - `padding_width`: Spacing allocated between icon and text.
  - `function`: Drawing callable (e.g., `phosphor.folder`, `phosphor.file_code`).
  - `style`: `Style` applied to the icon.
  - `args`: Keyword arguments dict passed to drawing function (e.g. `{"width": 3}`).
- `node.set_drawing_item(name)`: Links a node instance to the registered drawing item.

### 4.4 Production Example: Monorepo Project Structure
```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.preset_colors import CssColors
from drawlib.smartarts import TreeNode
from drawlib.styles import Colors, Styles

setup(width=110, height=70)

TreeNode.register_drawing_item(
    name="dir_icon", location="before", padding_width=4.5, function=phosphor.folder,
    style=Styles.Primary.patch(icon_color=Colors.Primary), args={"width": 3.0},
)
TreeNode.register_drawing_item(
    name="py_icon", location="before", padding_width=4.5, function=phosphor.file_py,
    style=Styles.Primary.patch(icon_color=CssColors.ForestGreen), args={"width": 3.0},
)
TreeNode.register_drawing_item(
    name="yaml_icon", location="before", padding_width=4.5, function=phosphor.file_code,
    style=Styles.Primary.patch(icon_color=Colors.Dark), args={"width": 3.0},
)

tree_root = TreeNode(
    "monorepo-root/",
    text_style=Styles.Dark.patch(text_size=11),
    line_style=Styles.Muted.patch(line_width=1.0),
    line_horizontal_margin=3.0,
    line_horizontal_length=3.0,
    line_vertical_margin=6.0,
    children=[
        TreeNode(
            "services/",
            children=[
                TreeNode(
                    "auth_api/",
                    children=[TreeNode("main.py").set_drawing_item("py_icon"), TreeNode("config.py").set_drawing_item("py_icon")],
                ).set_drawing_item("dir_icon"),
                TreeNode("payment_api/", children=[TreeNode("worker.py").set_drawing_item("py_icon")]).set_drawing_item("dir_icon"),
            ],
        ).set_drawing_item("dir_icon"),
        TreeNode(
            "deploy/",
            children=[TreeNode("k8s-prod.yaml").set_drawing_item("yaml_icon"), TreeNode("docker-compose.yaml").set_drawing_item("yaml_icon")],
        ).set_drawing_item("dir_icon"),
        TreeNode("pyproject.toml").set_drawing_item("yaml_icon"),
    ],
).set_drawing_item("dir_icon")

tree_root.draw(xy=(10, 62))
save()
```

---
## 5. Component 3: BoxList

`BoxList` draws sequential linear blocks or cards with optional individual highlight overrides.

### 5.1 BoxList Architecture & Directional Alignment
- **Anchor**: Coordinate `xy=(x, y)` marks start point.
- **Alignment Modes (`align`)**:
  - `"left"`: Cards sequence toward right (`+x`), `xy` at left edge vertical center.
  - `"right"`: Cards sequence toward left (`-x`).
  - `"bottom"`: Cards stack upward (`+y`), `xy` at bottom edge horizontal center.
  - `"top"`: Cards stack downward (`-y`).

### 5.2 BoxList Methods
- `BoxList(*, style: Style, text_style: Style)`: Initializes mandatory default box and text styles.
- `add(text, *, style=None, text_style=None, show=True) -> _BoxListItem`: Adds a card with optional custom style override and returns the mutable item instance.
- `draw(xy, box_width, box_height, align="left", scale=1.0)`: Renders all cards in specified orientation.

### 5.3 Production Example: Horizontal Service Pipeline & Status Cards
```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.smartarts import BoxList
from drawlib.styles import Styles

setup(width=110, height=50)

pipeline = BoxList(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=10),
)
pipeline.add("1. Ingestion")
pipeline.add("2. Validation")
# Highlighted hero step
pipeline.add(
    "3. ML Inference",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=10),
)
pipeline.add("4. Persistence", style=Styles.SecondaryNeutral)
pipeline.add("5. Dispatch")
pipeline.draw(xy=(8, 30), box_width=18, box_height=10, align="left")

status_list = BoxList(style=Styles.NeutralFlat, text_style=Styles.DarkBold.patch(text_size=9))
for label in ("Cluster A: OK", "Cluster B: OK", "Cluster C: SYNC"):
    status_list.add(label)
status_list.draw(xy=(8, 5), box_width=25, box_height=6, align="left")
save()
```

---
## 6. Component 4: MindMapNode (Radial & Multi-Directional Trees)

`MindMapNode` creates hierarchical diagrams, organization charts, decision trees, and multi-directional mindmaps with automatic right-angled orthogonal junction routing and clean subtree bounding box calculation.

### 6.1 Architecture & Two-Pass Layout
1. **Pass 1 (Extent Measurement)**: Recursively traverses subtrees bottom-up to compute exact bounding width and height for every branch.
2. **Pass 2 (Orthogonal Drawing)**: Draws connector lines from parent nodes to auto-calculated junction lines, branching out to child nodes.
- **Anchor**: Root coordinate `xy=(x, y)` specifies the **center point** of the root node.

### 6.2 Constructor & Node Methods
```python
MindMapNode(
    text: str,
    *,
    branch: Literal["bottom", "top", "left", "right"] | None = None,
    shape: Literal["rectangle", "oval", "none"] | None = None,
    size: tuple[float, float] | None = None,
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
- `node.add(child: MindMapNode | str, *, branch=None, shape=None, ..., show: bool = True) -> MindMapNode`: Appends a child `MindMapNode` (or creates one from a string) and returns the child `MindMapNode` instance. Setting `child.show = False` hides that node and its connector branch while keeping the full two-pass subtree bounding coordinates unchanged.
- `node.draw(xy, branch="right", scale=1.0)`: Renders the mindmap centered at `xy` with optional proportional `scale`.

### 6.3 Shapes & Layout Options
- `shape`: `"rectangle"` (rounded via `style.shape_r`), `"oval"`, or `"none"` (clean text label).
- `branch`: `"bottom"` (top-down), `"top"` (bottom-up), `"right"` (left-to-right), `"left"` (right-to-left), or multi-directional.
- `xy_shift`: Relative `(dx, dy)` offset applied after layout calculation to fine-tune placement or avoid label collisions.
- Cascading: Children automatically inherit unassigned style, size, shape, margins, and line styles from parent nodes. Root requires `style`, `text_style`, and `line_style`.

### 6.4 Production Example: Multi-Directional Architecture Overview
```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.smartarts import MindMapNode
from drawlib.styles import Styles

setup(width=220, height=110)

txt_white = Styles.WhiteBold.patch(text_size=9)
txt_branch = Styles.DarkBold.patch(text_size=8.5)
txt_leaf = Styles.Dark.patch(text_size=9)

root = MindMapNode(
    "Core API Gateway",
    shape="oval",
    size=(28, 12),
    style=Styles.PrimaryFlat,
    text_style=txt_white,
    line_style=Styles.DarkBold,
    line_length=12.0,
    horizontal_margin=4.0,
    vertical_margin=4.0,
    children=[
        MindMapNode(
            "Client Traffic", branch="left", shape="rectangle", size=(22, 8), style=Styles.PrimaryNeutral, text_style=txt_branch,
            children=[
                MindMapNode("Web App (SPA)", shape="none", text_style=txt_leaf),
                MindMapNode("Mobile Apps", shape="none", text_style=txt_leaf),
                MindMapNode("Public REST API", shape="none", text_style=txt_leaf),
            ],
        ),
        MindMapNode(
            "Internal Services", branch="right", shape="rectangle", size=(24, 8), style=Styles.SecondaryNeutral, text_style=txt_branch,
            children=[
                MindMapNode("Auth Service", shape="rectangle", size=(22, 6), style=Styles.Neutral, text_style=txt_branch),
                MindMapNode("Billing Engine", shape="rectangle", size=(22, 6), style=Styles.Neutral, text_style=txt_branch),
                MindMapNode("Notification Hub", shape="rectangle", size=(22, 6), style=Styles.Neutral, text_style=txt_branch),
            ],
        ),
        MindMapNode(
            "Telemetry Stack", branch="top", shape="rectangle", size=(24, 8), style=Styles.Neutral, text_style=txt_branch,
            children=[
                MindMapNode("Prometheus Metrics", shape="none", text_style=txt_leaf),
                MindMapNode("OpenTelemetry Traces", shape="none", text_style=txt_leaf),
            ],
        ),
        MindMapNode(
            "Persistence Tier", branch="bottom", shape="rectangle", size=(24, 8), style=Styles.Neutral, text_style=txt_branch,
            children=[
                MindMapNode("PostgreSQL Primary", shape="none", text_style=txt_leaf),
                MindMapNode("Redis Cache Cluster", shape="none", text_style=txt_leaf),
            ],
        ),
    ],
)
root.draw(xy=(110, 55))
save()
```

---
## 7. Component 5: ChevronProcess (Pipeline & Workflow Stages)

`ChevronProcess` draws horizontal, sequential process pipelines consisting of interlocking arrowhead blocks (chevrons). It is the premier component for CI/CD pipelines, fulfillment lifecycles, and phased migrations.

### 7.1 Geometry & Anchor Mechanics
- **Anchor**: Bottom-Left coordinate `xy=(x, y)` represents bottom-left boundary of the process diagram.
- **Angle Calculation**: Arrowhead indentation is governed by `corner_angle` (degrees between 10.0 and 80.0, default 60.0).
- **First Chevron**: Setting `flat_left_end=True` replaces the first chevron's left indent with a clean vertical edge (a flat-backed pentagon).
- **Text Alignment**: Supports primary titles and optional secondary supporting descriptions placed cleanly within the chevron body.

### 7.2 Constructor Parameters
```python
ChevronProcess(
    *,
    style: Style,
    text_style: Style,
    description_style: Style,
    corner_angle: float = 60.0,
    spacing: float = 1.5,
    flat_left_end: bool = False,
)
```

### 7.3 Step Management & Drawing
- `add(text, *, description="", style=None, text_style=None, description_style=None, show=True) -> _ChevronItem`: Adds an individual step with optional style overrides and returns the mutable item instance.
- `draw(xy, width=90.0, height=12.0, item_width=None, scale=1.0)`:
  - `width`: Total bounding width allocated; individual block widths are computed automatically:
    $$\text{item\_width} = \frac{\text{width} - (\text{num\_items} - 1) \cdot \text{spacing} - x_{\text{indent}}}{\text{num\_items}}$$
  - `item_width`: If provided, overrides automatic width distribution.

### 7.4 Production Example: Cloud CI/CD Deployment Pipeline
```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.smartarts import ChevronProcess
from drawlib.styles import Styles

setup(width=130, height=45)

pipeline = ChevronProcess(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=9.5),
    description_style=Styles.Muted.patch(text_size=8),
    corner_angle=60.0,
    spacing=2.0,
    flat_left_end=True,
)
pipeline.add("1. Commit", description="Lint / Hooks")
pipeline.add("2. Build", description="Docker Image")
# Active Stage Highlight
pipeline.add(
    text="3. Security",
    description="SAST & CVE",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=9.5),
    description_style=Styles.White.patch(text_size=8),
)
pipeline.add("4. Staging", description="Integration")
pipeline.add("5. Production", description="Canary Deploy", style=Styles.SecondaryNeutral)
pipeline.draw(xy=(10, 15), width=110.0, height=16.0)
save()
```

---
## 8. Component 6: Cycle (Circular & Feedback Loops)

`Cycle` renders cyclical workflows, feedback loops, and radial hubs—such as DevOps PDCA iterations, token refresh flows, and distributed consensus rounds.

### 8.1 Architecture & Circular Geometry
- **Anchor**: Coordinate `xy=(x, y)`. Default `align="center"` anchors circular orbit center. If `align="bottom_left"`, `xy` anchors bounding box.
- **Node Placements**: Steps are distributed evenly along orbit radius $R$:
  $$\theta_i = \text{start\_angle} \mp \left(i \cdot \frac{360^\circ}{N}\right)$$
- **Curved Connectors**: Steps are connected by circular arc arrows (`arrow_type="arc"`) or line arcs (`"line"`).
- **Center Hub**: Optional center node (`set_center()`) transforms diagram into a Radial Cycle.

### 8.2 Constructor Parameters
```python
Cycle(
    *,
    style: Style,
    text_style: Style,
    description_style: Style | None = None,
    arrow_style: Style | None = None,
    clockwise: bool = True,
    start_angle: float = 90.0,
    node_shape: Literal["circle", "rectangle", "none"] = "circle",
    node_radius: float = 8.0,
    node_size: tuple[float, float] = (18.0, 10.0),
    description_placement: Literal["inside", "outside"] = "inside",
    arrow_type: Literal["arc", "line", "none"] = "arc",
    arrow_width: float = 2.0,
    arrow_head_width: float = 4.5,
    arrow_color_mode: Literal["monochrome", "match_source", "match_target"] = "match_source",
    arrow_gap: float = 2.5,
    center_text: str = "",
    center_description: str = "",
    center_radius: float = 10.0,
    center_style: Style | None = None,
    center_text_style: Style | None = None,
    center_description_style: Style | None = None,
)
```

### 8.3 Key Configuration Options
- `arrow_color_mode`: `"match_source"` (matches preceding node), `"match_target"` (matches succeeding node), `"monochrome"`.
- `description_placement`: `"inside"` (inside node body) or `"outside"` (radiates outward).
- `add(text, *, style=None, text_style=None, description="", description_style=None, arrow_style=None, show=True) -> _CycleItem`: Adds an individual step and returns the mutable item instance.
- `set_center(text, *, style=None, text_style=None, description="", radius=None, description_style=None, show=True) -> _CycleCenter`: Configures central hub node and returns the mutable center instance.
- `draw(xy, radius=35.0, align="center", scale=1.0)`: Renders the circular cycle anchored at `xy` with orbit radius `radius` and optional proportional `scale`.

### 8.4 Production Example: SRE Incident Response Lifecycle
```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.preset_colors import CssColors
from drawlib.smartarts import Cycle
from drawlib.styles import Styles

setup(width=100, height=90)

incident_cycle = Cycle(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=9),
    description_style=Styles.Muted.patch(text_size=7),
    arrow_style=Styles.DarkBold,
    clockwise=True,
    start_angle=90.0,
    node_shape="circle",
    node_radius=8.0,
    arrow_type="arc",
    arrow_width=1.5,
    arrow_head_width=4.0,
    arrow_color_mode="monochrome",
    description_placement="inside",
)
incident_cycle.add(
    "1. Detect",
    description="Alert Fires",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=9),
    description_style=Styles.White.patch(text_size=7),
)
incident_cycle.add("2. Triage", description="Assess Scope", style=Styles.PrimaryNeutral)
incident_cycle.add("3. Mitigate", description="Failover", style=Styles.SecondaryNeutral)
incident_cycle.add("4. Resolve", description="Root Fix", style=Styles.Neutral)
incident_cycle.add("5. Learn", description="Action Items", style=Styles.Neutral)

incident_cycle.set_center(
    text="SRE",
    description="Command",
    radius=11.0,
    style=Styles.DarkFlat,
    text_style=Styles.WhiteBold.patch(text_size=12),
    description_style=Styles.White.patch(text_color=CssColors.LightGray, text_size=8),
)
incident_cycle.draw(xy=(50, 45), radius=32.0, align="center")
save()
```

---
## 9. Component 7: GridLayout (Matrix Cards & Architecture Layers)

`GridLayout` positions cards and rectangles across a uniform or flexible column/row matrix, supporting cell spanning across multiple columns and rows, custom corner radii, rotated labels, and outer borders.

### 9.1 Coordinate & Indexing Rules
- **Anchor**: Coordinate `xy=(x, y)` marks **bottom-left corner** of entire grid.
- **Row Indexing**: `row_start=0` is **bottom-most row**. Rows increment upward towards row `num_row - 1`.
- **Column Indexing**: `column_start=0` is **left-most column**. Columns increment rightward towards `num_column - 1`.
- **Cell Spanning**: A card starting at `position=(col, row)` spans `width` column cells and `height` row cells.

### 9.2 Constructor & Item Addition
```python
GridLayout(
    *,
    num_column: int,
    num_row: int,
    style: Style,
    text_style: Style,
)
```

Adding items to the grid (returns the mutable `_GridLayoutItem` instance):
```python
item = grid.add(
    position: tuple[int, int],  # (column_start, row_start)
    width: int,                 # Number of columns spanned
    height: int,                # Number of rows spanned
    *,
    style: Style | None = None,
    text: str = "",
    text_style: Style | None = None,
    show: bool = True,
) -> _GridLayoutItem
```

### 9.3 Drawing Modes
- `draw(xy, width, height, margin, outer_style=None, scale=1.0)`: Even column and row dimensions with uniform `margin` gutters between cells and around borders, plus optional proportional `scale`.
- `draw_flexible(xy, column_widths, column_margins, row_heights, row_margins, outer_style=None, scale=1.0)`: Custom widths and heights for each individual column and row, plus optional proportional `scale`.

### 9.4 Production Example: Multi-Tier Cloud Software Architecture
```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.smartarts import GridLayout
from drawlib.styles import Styles

setup(width=110, height=75)

grid = GridLayout(num_column=4, num_row=4, style=Styles.Neutral.patch(shape_r=1.5), text_style=Styles.DarkBold)

# Row 3 (Top): Client & CDN Ingress (Hero layer)
grid.add(
    position=(0, 3),
    width=4,
    height=1,
    text="Edge Ingress: Cloudflare CDN & WAF Gateway",
    style=Styles.PrimaryFlat.patch(shape_r=1.5),
    text_style=Styles.WhiteBold,
)
# Row 2: Microservice Layer
grid.add(position=(0, 2), width=2, height=1, text="Order & Cart API", style=Styles.PrimaryNeutral.patch(shape_r=1.5))
grid.add(position=(2, 2), width=1, height=1, text="Auth API", style=Styles.PrimaryNeutral.patch(shape_r=1.5))
grid.add(position=(3, 2), width=1, height=1, text="Notify", style=Styles.PrimaryNeutral.patch(shape_r=1.5))
# Row 1: Persistence Tier
grid.add(position=(0, 1), width=1, height=1, text="Postgres", style=Styles.SecondaryNeutral.patch(shape_r=1.5))
grid.add(position=(1, 1), width=1, height=1, text="Mongo", style=Styles.SecondaryNeutral.patch(shape_r=1.5))
grid.add(position=(2, 1), width=2, height=1, text="Redis Replication Cluster", style=Styles.SecondaryNeutral.patch(shape_r=1.5))
# Row 0 (Bottom): Cloud Infrastructure
grid.add(position=(0, 0), width=4, height=1, text="Kubernetes Core Platform (AWS EKS Multi-AZ)", style=Styles.Neutral.patch(shape_r=1.5))

grid.draw(
    xy=(10, 10),
    width=90,
    height=55,
    margin=1.5,
    outer_style=Styles.MutedDashed.patch(shape_r=2.0),
)
save()
```

---
## 10. Component 8: Pyramid (Tiered Stacks & Hierarchies)

`Pyramid` renders tiered, hierarchical trapezoids crowned by an apex triangle. It is ideal for visualizing defense-in-depth security, testing pyramids, memory hierarchies, and organizational governance.

### 10.1 Architecture & Geometry
- **Anchor**: Bottom-Left coordinate `xy=(x, y)` anchors bounding box.
- **Apex and Slices**: Top-most slice is drawn as a triangle; lower slices are drawn as trapezoids widening progressively toward the base.
- **Alignments (`align`)**: `"bottom"` (standard upright), `"top"` (inverted funnel), `"left"` (points left), `"right"` (points right).
- **Ordering (`order`)**:
  - `"vertex_to_base"`: First added item is positioned at the apex/vertex; subsequent items move toward the base.
  - `"base_to_vertex"`: First added item is positioned at the wide base; subsequent items move toward the vertex.

### 10.2 Constructor & Item Addition
```python
Pyramid(
    *,
    style: Style,
    text_style: Style,
)
```

Adding tiers (returns the mutable `_PyramidItem` instance):
```python
tier = pyramid.add(
    text: str,
    *,
    style: Style | None = None,
    text_style: Style | None = None,
    show: bool = True,
) -> _PyramidItem
```

### 10.3 Drawing APIs
- `draw(xy, width, height, margin, align="bottom", order="vertex_to_base", scale=1.0)`: Uniform tier heights with optional proportional `scale`:
  $$\text{tier\_height} = \frac{\text{height} - (N - 1) \cdot \text{margin}}{N}$$
- `draw_flexible(xy, width, item_heights, margins, align="bottom", order="vertex_to_base", scale=1.0)`: Explicit heights per tier with optional proportional `scale`.

### 10.4 Production Example: Software Testing Pyramid
```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.smartarts import Pyramid
from drawlib.styles import Styles

setup(width=100, height=65)

test_pyramid = Pyramid(style=Styles.Neutral, text_style=Styles.DarkBold.patch(text_size=10))
test_pyramid.add("Manual (1%)", style=Styles.Neutral, text_style=Styles.DarkBold.patch(text_size=8.5))
test_pyramid.add("End-to-End UI Tests (9%)", style=Styles.PrimaryNeutral)
test_pyramid.add("Integration & Contract Tests (20%)", style=Styles.SecondaryNeutral)
test_pyramid.add(
    "Unit Tests (70%)",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=10),
)

test_pyramid.draw(xy=(15, 10), width=70, height=45, margin=1.5, align="bottom", order="vertex_to_base")
save()
```

---
## 11. Component 9: BulletPoints (Formatted Bulleted Lists)

`BulletPoints` renders nested lists with custom indentation levels, custom bullet marker shapes or icons, and uniform vertical line spacing.

### 11.1 Coordinate & Indent Structure
- **Anchor**: Top-Left coordinate `xy=(x, y)`. First line is rendered at `y`, subsequent items step downward (`y - vertical_margin`).
- **Indentation Levels**:
  - `level = 0`: Section headers or root items (no bullet marker drawn by default).
  - `level = 1`: Primary bullet items (defaults to filled circle bullet).
  - `level = 2`: Secondary nested items (defaults to open outline circle bullet).
- **Bullet Marker Position**: Calculated automatically at `x_marker = x + indent_width * (indent - 0.5)`.

### 11.2 Constructor & Methods
```python
BulletPoints(
    *,
    text_style: Style,
    vertical_margin: float,
    indent_width: float,
)
```

- `set_indent(level: int)`: Changes active indent level for all subsequent `add()` calls.
- `set_bullet_style(indent_level: int, function: Callable, style: Style, args: dict)`: Overrides bullet marker shape for a specific indent level (e.g. `circle`, `rectangle`, or Phosphor icon functions).
- `add(text: str, *, text_style: Style | None = None, show: bool = True) -> _BulletPointItem`: Appends an item at current active indent level and returns the mutable `_BulletPointItem` instance.
- `draw(xy: tuple[float, float], scale: float = 1.0)`: Renders bullet points starting from `xy` with optional proportional `scale`.

### 11.3 Production Example: Architecture Decision RFC Summary
```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.preset_colors import CssColors
from drawlib.shapes import rectangle
from drawlib.smartarts import BulletPoints
from drawlib.styles import Colors, Styles
from drawlib.types import Style

setup(width=110, height=65)

bp = BulletPoints(
    text_style=Styles.Primary.patch(text_size=10, text_color=Colors.Dark),
    vertical_margin=4.5,
    indent_width=5.0,
)
bp.set_bullet_style(
    indent_level=1,
    function=rectangle,
    style=Styles.Primary.patch(shape_fill_color=Colors.Primary, shape_line_width=0),
    args={"width": 1.2, "height": 1.2},
)
bp.set_bullet_style(
    indent_level=2,
    function=phosphor.check_circle,
    style=Styles.Primary.patch(icon_color=CssColors.ForestGreen),
    args={"width": 2.0},
)

bp.set_indent(0)
bp.add("RFC 402: Event-Driven Order Processing", text_style=Styles.PrimaryBold)
bp.set_indent(1)
bp.add("Core Architectural Guarantees:")
bp.set_indent(2)
bp.add("At-least-once message delivery via Apache Kafka partitioned topics")
bp.add("Idempotent event consumers using Redis deduplication filters")
bp.add("Dead-letter queue (DLQ) with automatic retry backoff")
bp.set_indent(1)
bp.add("Migration & Rollout Plan:")
bp.set_indent(2)
bp.add("Phase 1: Shadow write events to Kafka cluster")
bp.add("Phase 2: Gradual 10% canary traffic migration")

bp.draw(xy=(15, 55))
save()
```

---
## 12. Component 10: SourceCode (Syntax-Highlighted Code Containers)

`SourceCode` renders syntax-highlighted code snippets directly as sharp vector shapes and text.
Unlike stateful SmartArts (`Table`, `TreeNode`), `SourceCode` is stateless: you draw code directly via `SourceCode.draw(...)` or the `sourcecode(...)` function alias.

### 12.1 Supported Languages & Themes
- **Code Languages (`code_lang`)**:
  `"python"`, `"bash"`, `"go"`, `"rust"`, `"typescript"`, `"javascript"`, `"json"`, `"yaml"`, `"sql"`, `"docker"`, `"toml"`, `"c"`, `"c++"`, `"c#"`, `"java"`, `"kotlin"`, `"swift"`, `"html"`, `"css"`, `"protobuf"`, `"markdown"`, etc. Passing `None` enables automatic syntax guessing via Pygments.
- **Font Languages (`font_lang`)**:
  `"en"`, `"ja"`, `"zh-cn"`, `"zh-tw"`, `"ko"`, etc. Passing `"ja"` automatically applies `FontSourceCode.SOURCEHANCODEJP` to all tokens and line numbers, preventing tofu for CJK comments and strings.
- **Themes (`styles`)**:
  `"default"`, `"monochrome"`, `"dark"`, `"monokai"`, `"google"`.

### 12.2 Signature
```python
SourceCode.draw(
    xy: tuple[float, float],           # Top-left corner (x, y) of the code container
    width: float,                      # Total container width
    code: str | None = None,           # Code string to render (or use `file`)
    *,
    styles: SourceCodeStyles,          # Required style configuration
    file: str | None = None,           # Path to code file (alternative to `code`)
    code_lang: str | None = None,      # Language: "python", "json", "yaml", "sql", etc.
    show_linenum: bool = False,        # Whether to show line numbers in a gutter
    scale: float = 1.0,                # Proportional scaling anchored at xy
)
```

### 12.3 Style Management (`SourceCodeStyles`)
Styles are configured via `SourceCodeStyles.get(...)` (or `get_source_code_styles(...)`) and can be patched via `.patch()` (the outer box corner radius is controlled via `styles.box_style.shape_r`, defaulting to `1.5`):
```python
styles = SourceCodeStyles.get("dark", font_lang="en", text_size=11.0)
custom = styles.patch(keyword=Styles.PrimaryBold, comment=Styles.MutedItalic)
```

### 12.4 Production Example: Embedded Configuration Block
```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.shapes import rectangle
from drawlib.smartarts import SourceCode, SourceCodeStyles
from drawlib.styles import Styles

setup(width=110, height=105)

# Outer window frame
rectangle(xy=(55, 52.5), width=96, height=95, style=Styles.DarkSolid.patch(shape_r=2))
# Header bar
rectangle(
    xy=(55, 94),
    width=96,
    height=12,
    style=Styles.DarkFlat.patch(shape_r=2),
    text="Kubernetes Deployment Spec (v1)",
    text_style=Styles.WhiteBold,
)

k8s_yaml = """apiVersion: apps/v1
kind: Deployment
metadata:
  name: auth-service
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: auth-service
  template:
    spec:
      containers:
      - name: auth
        image: gcr.io/company/auth:v1.4.2"""

code_styles = SourceCodeStyles.get("dark", font_lang="en", text_size=10.0)
SourceCode.draw(xy=(11, 86), width=88, code=k8s_yaml, styles=code_styles, code_lang="yaml", show_linenum=True)
save()
```

---
## 12b. Component 11: GeoMap (Geographical Vector Maps)

`GeoMap` renders vector geographical maps (`GeoMap.World.*`, `GeoMap.Countries.*`, `GeoMap.Cities.*`, or custom GeoJSON files) onto the Drawlib canvas without external GIS dependencies.

### 12b.1 Geometry, Anchor & Sizing Rules
- **Anchor**: Coordinate `xy=(x, y)` marks the **Bottom-Left** corner of the map bounding box on the canvas.
- **Required Dimension (`width` or `height` Must Be Provided)**:
  Although `width` and `height` both default to `None` in the method signature, **at least one of `width` or `height` MUST be passed to `draw()`**. Calling `m.draw()` with both `width=None` and `height=None` raises `ValueError: At least one of 'width' or 'height' must be provided to GeoMap.draw().`
- **Aspect Ratio & `background_style` Alignment**:
  - **Single-Dimension Sizing (Recommended for Natural Fit)**: Pass only `width=...` (or only `height=...`). `GeoMap` automatically calculates the other dimension from the map's natural geographical aspect ratio:
    $$\text{natural\_aspect} = \frac{(\text{max\_lon} - \text{min\_lon}) \cdot \cos(\text{mid\_lat})}{\text{max\_lat} - \text{min\_lat}}$$
    Both `background_style` and map polygons will match edge-to-edge with zero letterboxing.
  - **Dual-Dimension Sizing (`width` AND `height` with `lon_range` / `lat_range`)**: When both `width` and `height` are specified, `background_style` fills the entire `width × height` outer box, while the map polygons are clipped to `lon_range` / `lat_range` and centered inside that box. If $\text{natural\_aspect}$ does not match `width / height`, continental landmasses will appear abruptly clipped inside the ocean background box. To fill a fixed `width × height` frame edge-to-edge, choose `lon_range` and `lat_range` so that $\text{natural\_aspect} \approx \text{width} / \text{height}$.
- **Coordinate Lookup Order (`draw()` First)**:
  - `get_area_xy(area)` and `lonlat_to_xy(lon, lat)` rely on the projection computed during `draw()` and **must be called AFTER `m.draw(...)`** (calling them before `draw()` raises `RuntimeError`).
  - To inspect valid area names before drawing, call `m.get_areas()` (which does not require `draw()`). `set_area_styles()` and `get_area_xy()` accept canonical English names (`"Japan"`), ISO codes (`"JP"`, `"JPN"`), or Japanese names (`"日本"`).

### 12b.2 Presets & Targets
- `GeoMap.World`: `All`, `Asia`, `Europe`, `NorthAmerica`, `SouthAmerica`, `Africa`, `Oceania`, `EastAsia`, `SoutheastAsia`, `APAC`, `MiddleEast`
- `GeoMap.Countries`: All 215 countries & territories (`Japan`, `UnitedStates`, `UnitedKingdom`, `Germany`, `France`, ...)
- `GeoMap.Cities`: 16 global metropolitan maps (`Australia_Sydney`, `China_HongKong`, `China_Shanghai`, `France_Paris`, `Germany_Berlin`, `Italy_Rome`, `Japan_Kyoto`, `Japan_Osaka`, `Japan_Tokyo`, `Singapore_Singapore`, `SouthKorea_Seoul`, `Taiwan_Taipei`, `UnitedKingdom_London`, `UnitedStates_LosAngeles`, `UnitedStates_NewYork`, `UnitedStates_SanFrancisco`)
- Custom GeoJSON: Any `.geojson` path (e.g. `"_assets/geodata/okinawa.geojson"`) or GeoJSON `dict`.

### 12b.3 Constructor & 5-Method API
```python
m = GeoMap(target, *, area_style=Styles.Neutral, background_style=None, id_key=None, name_key=None)
m.get_areas() -> list[str]
m.set_area_styles(areas: list[str], style: Style) -> Self
m.draw(xy=(0.0, 0.0), width=None, height=None, *, lon_range=None, lat_range=None, scale=1.0) -> Self
m.get_area_xy(area: str) -> tuple[float, float]
m.lonlat_to_xy(lon: float, lat: float) -> tuple[float, float]
```

### 12b.4 Production Example: Regional Map with Curved Trajectories & Pin Overlays
```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.lines import line_curved
from drawlib.shapes import circle, rectangle
from drawlib.smartarts import GeoMap
from drawlib.styles import Styles
from drawlib.text import text

setup(width=115, height=70)

asia = GeoMap(
    GeoMap.World.Asia,
    area_style=Styles.White,
    background_style=Styles.PrimaryNeutral.patch(shape_r=1.5),
)
asia.set_area_styles(["China", "Vietnam", "Philippines"], Styles.AccentFlat)
asia.set_area_styles(["Japan"], Styles.PrimaryFlat)

# Match lon_range / lat_range aspect ratio (~1.75) to width / height (103 / 59)
asia.draw(xy=(6.0, 6.0), width=103.0, height=58.0, lon_range=(73, 148), lat_range=(16, 53))

tokyo_xy = asia.lonlat_to_xy(139.69, 35.69)
for lon, lat, bend in [(116.40, 39.90, -0.18), (121.47, 31.23, 0.15), (105.83, 21.03, 0.18)]:
    src_xy = asia.lonlat_to_xy(lon, lat)
    line_curved(src_xy, tokyo_xy, bend=bend, arrow_head="->", style=Styles.AccentBold)
    circle(src_xy, radius=1.0, style=Styles.DarkFlat)

circle(tokyo_xy, radius=1.4, style=Styles.PrimaryFlat)
rectangle((tokyo_xy[0] - 5.0, tokyo_xy[1] + 8.0), width=24.0, height=5.8, style=Styles.PrimaryFlat.patch(shape_r=1.2))
text((tokyo_xy[0] - 5.0, tokyo_xy[1] + 8.0), "Tokyo Origin", style=Styles.WhiteBold.patch(text_size=10.5))
save()
```

---
## 13. Design Patterns & Coordinate Anchor Systems

### 13.1 Coordinate Normalization Cheat Sheet

When integrating multiple SmartArts onto a single canvas, harmonize their coordinate origins according to the following formulas:

```python
# Converting between Top-Left, Bottom-Left, and Center anchors:
# Given a bounding box of size (W, H):
center_x = left_x + W / 2.0
center_y = bottom_y + H / 2.0

top_left_x = left_x
top_left_y = bottom_y + H
```

| Component | Input `xy` Meaning | To Align with Canvas Top-Left `(X, Y)` | To Align with Canvas Bottom-Left `(X, Y)` |
| :--- | :--- | :--- | :--- |
| `Table` | Top-Left `(x, y)` | Pass `(X, Y)` directly | Pass `(X, Y + H)` |
| `TreeNode` | Top-Left `(x, y)` | Pass `(X, Y)` directly | Pass `(X, Y + H)` |
| `BulletPoints` | Top-Left `(x, y)` | Pass `(X, Y)` directly | Pass `(X, Y + H)` |
| `ChevronProcess` | Bottom-Left `(x, y)` | Pass `(X, Y - H)` | Pass `(X, Y)` directly |
| `GridLayout` | Bottom-Left `(x, y)` | Pass `(X, Y - H)` | Pass `(X, Y)` directly |
| `Pyramid` | Bottom-Left `(x, y)` | Pass `(X, Y - H)` | Pass `(X, Y)` directly |
| `GeoMap` | Bottom-Left `(x, y)` | Pass `(X, Y - H)` | Pass `(X, Y)` directly |
| `MindMapNode` | Root Center `(x, y)` | Pass `(X + W/2, Y - H/2)` | Pass `(X + W/2, Y + H/2)` |
| `Cycle` (align="center") | Orbit Center `(x, y)` | Pass `(X + R, Y - R)` | Pass `(X + R, Y + R)` |

### 13.2 Multi-Component Dashboard Integration Example
```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.smartarts import ChevronProcess, SourceCode, SourceCodeStyles, Table
from drawlib.styles import Styles

setup(width=120, height=80)

# 1. Top Section: Pipeline Status
pipeline = ChevronProcess(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=9),
    description_style=Styles.Muted.patch(text_size=7.5),
    corner_angle=60.0,
    spacing=1.5,
    flat_left_end=True,
)
pipeline.add("1. Plan", description="Arch Review")
pipeline.add("2. Build", description="Docker Image")
pipeline.add("3. Test", description="E2E Verified", style=Styles.SecondaryNeutral)
pipeline.add(
    "4. Deploy",
    description="Production",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=9),
    description_style=Styles.White.patch(text_size=7.5),
)
pipeline.draw(xy=(10, 62), width=100, height=12)

# 2. Bottom-Left Section: Service Matrix Table
table = Table(
    cell_style=Styles.White,
    text_style=Styles.Dark,
    header_cell_style=Styles.PrimaryFlat,
    header_text_style=Styles.WhiteBold,
    border_style=Styles.MutedThin,
)
table.draw(
    xy=(10, 55),
    width=50,
    height=45,
    data=[
        ["Service", "Status", "Latency"],
        ["User API", "Active", "12 ms"],
        ["Cart API", "Active", "15 ms"],
        ["Checkout", "Warning", "120 ms"],
        ["Billing", "Active", "45 ms"],
    ],
)

# 3. Bottom-Right Section: Active Schema Code Snippet
snippet = """# Migration Hook
def handle_event(ctx):
    ctx.metrics.inc("migrated")
    return ctx.forward()"""

code_styles = SourceCodeStyles.get("dark", font_lang="en", text_size=9.0)
SourceCode.draw(xy=(66, 45), width=48, code=snippet, styles=code_styles, code_lang="python", show_linenum=True)

save()
```

---
## 14. Troubleshooting & Common Pitfalls

### 1. Inverted Table or Grid Placement
- **Problem**: Table rows or GridLayout cells render outside canvas or upside down.
- **Cause**: Confusing Top-Left vs. Bottom-Left anchors.
- **Resolution**:
  - `Table` takes `(x, y)` as **top-left** point. Providing `(10, 10)` on an $80$-tall canvas causes it to draw downward past bottom boundary ($y = 10 \to y = -35$). Use `(10, 70)`.
  - `GridLayout` takes `(x, y)` as **bottom-left** point, and `row=0` is at bottom.

### 2. Missing TreeNode Styles on Root
- **Problem**: Calling `tree_root.draw(xy)` raises `ValueError: Root of TreeNode must be initialized with "text_style"`.
- **Cause**: Root `TreeNode` requires default style and margin values to propagate down to descendants that do not specify explicit styles.
- **Resolution**: Always supply `text_style`, `line_style`, `line_horizontal_margin`, `line_horizontal_length`, and `line_vertical_margin` on the root node instance.

### 3. Subtree Overlaps in MindMapNode
- **Problem**: Sibling subtrees collide or overlap when branching in same direction.
- **Resolution**: Increase `horizontal_margin` (for `"bottom"` or `"top"` branches) or `vertical_margin` (for `"left"` or `"right"` branches). You can also apply localized `xy_shift=(dx, dy)` on problematic child nodes.

### 4. Cycle Arrow Overlaps
- **Problem**: Connecting curved arrows collide with step circles or rectangular nodes.
- **Resolution**: Increase `arrow_gap` (default 2.5) or enlarge orbit `radius` relative to `node_radius` / `node_size`. For 5-node pentagonal `Cycle` diagrams with rectangular nodes, keep `node_size[0] <= 0.9 * radius` so the bottom two nodes maintain a clean horizontal gap for their connecting arrow.

### 5. GeoMap Missing Dimensions or Clipped Continents Inside `background_style`
- **Problem A**: Calling `m.draw()` without `width` or `height` raises `ValueError: At least one of 'width' or 'height' must be provided to GeoMap.draw().`, or calling `m.get_area_xy()` before `m.draw()` raises `RuntimeError`.
- **Resolution A**: Always pass at least `width=...` (or `height=...`) to `m.draw(...)`, and call `get_area_xy()` / `lonlat_to_xy()` only after `m.draw(...)` has executed. Use `m.get_areas()` if you only need to inspect area names without drawing.
- **Problem B**: When passing both `width` and `height` along with `background_style` and custom `lon_range` / `lat_range`, landmasses appear vertically or horizontally sliced off inside the background box.
- **Resolution B**: Either pass only `width` (or only `height`) so the box auto-sizes to the map's aspect ratio, or widen `lon_range` / `lat_range` so that $(\Delta\text{lon} \cdot \cos(\text{mid\_lat})) / \Delta\text{lat} \approx \text{width} / \text{height}$.
