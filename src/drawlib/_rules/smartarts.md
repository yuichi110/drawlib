# Drawlib SmartArts Guidelines

The `drawlib.smartarts` module provides high-level graphical components designed for "Illustration as Code." These components automate the layout, geometry, text positioning, and styling of structured diagrams—including tabular datasets, organizational trees, mindmaps, process pipelines, cyclical workflows, matrix grids, tiered pyramids, bulleted lists, syntax-highlighted source code, and speech callouts.

---
## Table of Contents

1. [Architectural Overview & Core Concepts](#1-architectural-overview--core-concepts)
2. [Quick Reference Matrix](#2-quick-reference-matrix)
3. [Component 1: Table](#3-component-1-table)
4. [Component 2: TreeNode (Directory & Hierarchy Trees)](#4-component-2-treenode-directory--hierarchy-trees)
5. [Component 3: BoxList & BoxTreeNode](#5-component-3-boxlist--boxtreenode)
6. [Component 4: MindMapNode (Radial & Multi-Directional Trees)](#6-component-4-mindmapnode-radial--multi-directional-trees)
7. [Component 5: ChevronProcess (Pipeline & Workflow Stages)](#7-component-5-chevronprocess-pipeline--workflow-stages)
8. [Component 6: Cycle (Circular & Feedback Loops)](#8-component-6-cycle-circular--feedback-loops)
9. [Component 7: GridLayout (Matrix Cards & Architecture Layers)](#9-component-7-gridlayout-matrix-cards--architecture-layers)
10. [Component 8: Pyramid (Tiered Stacks & Hierarchies)](#10-component-8-pyramid-tiered-stacks--hierarchies)
11. [Component 9: BulletPoints (Formatted Bulleted Lists)](#11-component-9-bulletpoints-formatted-bulleted-lists)
12. [Component 10: SourceCode (Syntax-Highlighted Code Containers)](#12-component-10-sourcecode-syntax-highlighted-code-containers)
13. [Component 11: bubblespeech (Callouts & Speech Bubbles)](#13-component-11-bubblespeech-callouts--speech-bubbles)
14. [Design Patterns & Coordinate Anchor Systems](#14-design-patterns--coordinate-anchor-systems)
15. [Troubleshooting & Common Pitfalls](#15-troubleshooting--common-pitfalls)

---
## 1. Architectural Overview & Core Concepts

### 1.1 Imports
All SmartArts classes and helper functions are exported directly from `drawlib.smartarts`:
```python
from drawlib.smartarts import (
    BoxList,
    BoxTreeNode,
    BulletPoints,
    ChevronProcess,
    Cycle,
    GridLayout,
    MindMapNode,
    Pyramid,
    SourceCode,
    Table,
    TreeNode,
    bubblespeech,
)
```

Common auxiliary imports required for canvas setup, styling, and colors:
```python
from drawlib.canvas import config, save
from drawlib.colors import Colors, Colors140, ColorsEssentials
from drawlib.preset_styles import get_style
from drawlib.types import Style
```

### 1.2 Coordinate Anchor Conventions
Understanding anchor points is essential for programmatic generation and positioning:
- **Top-Left Anchored**: `Table`, `TreeNode`, `BulletPoints`. You specify top-left coordinate `(x, y)`; elements flow rightward and downward.
- **Bottom-Left Anchored**: `ChevronProcess`, `GridLayout`, `Pyramid`, `bubblespeech`. You specify bottom-left coordinate `(x, y)` of the bounding box; elements extend rightward and upward.
- **Center Anchored**: `MindMapNode` (root node center `(x, y)`), `Cycle` (default `align="center"` anchors orbit center).

### 1.3 Style Resolution
Every SmartArt accepts either:
- A `Style` instance: `Style(fill_color=Colors.Blue, line_color=Colors.White, line_width=1.5)`
- A preset style string key: `"blue"`, `"red_flat"`, `"green_solid"`, `"white_bold"`, `"light"`, `"bold"`
- `None`: falls back to default component styles or canvas theme defaults.

---
## 2. Quick Reference Matrix

| Component | Anchor Point | Layout Direction | Key Methods | Typical Architecture Use Cases |
| :--- | :--- | :--- | :--- | :--- |
| `Table` | Top-Left `(x, y)` | Downward & Rightward | `set_style_*()`, `draw()`, `draw_flexible()` | Service matrices, SLA comparisons, feature tables |
| `TreeNode` | Top-Left `(x, y)` | Downward tree lines | `register_drawing_item()`, `draw()` | Monorepo directories, file trees, package layouts |
| `BoxList` | Directional `(x, y)` | `"left"`, `"right"`, `"bottom"`, `"top"` | `append()`, `extend()`, `draw()` | Microservice cards, pipeline stages, status badges |
| `BoxTreeNode` | Center `(x, y)` | Multi-directional | Alias for `MindMapNode` | Backward compatibility, hierarchical card trees |
| `MindMapNode` | Center `(x, y)` | Radial (4 directions) | `draw(branch=...)` | Architecture overviews, decision trees, org charts |
| `ChevronProcess` | Bottom-Left `(x, y)` | Horizontal linear | `append()`, `extend()`, `draw()` | CI/CD pipelines, ETL workflows, order lifecycles |
| `Cycle` | Center / Bottom-Left | Radial circular | `append()`, `set_center()`, `draw()` | PDCA DevOps loops, token refresh cycles, state machines |
| `GridLayout` | Bottom-Left `(x, y)` | Matrix grid cells | `add()`, `draw()`, `draw_flexible()` | Multi-tier architecture layers, dashboard panels |
| `Pyramid` | Bottom-Left `(x, y)` | Stacked layers | `add()`, `draw()`, `draw_flexible()` | Defense-in-depth, testing pyramid, memory hierarchies |
| `BulletPoints` | Top-Left `(x, y)` | Downward list | `set_indent()`, `set_bullet_style()`, `draw()` | Architecture takeaways, RFC summaries, feature lists |
| `SourceCode` | Top-Left `(x, y)` | Raster code block | `get_image()`, `get_text()`, `draw()` | Embedded configuration, code samples, API payloads |
| `bubblespeech` | Bottom-Left `(x, y)` | Vector speech box | Direct function call | Bottleneck callouts, architectural migration notes |

---
## 3. Component 1: Table

`Table` renders 2D tabular data with precise styling control over borders, header cells, even/odd alternating rows, and individual cell coordinates.

### 3.1 Architecture & Coordinate Mechanics
- **Anchor**: Top-Left coordinate `xy=(x, y)`. The first row starts at `y`, and subsequent rows move downward (`y - row_height`).
- **Data Shape**: 2D list of any serializable values (`list[list[Any]]`).
- **Sizing Modes**:
  - `draw(xy, width, height, data)`: Uniform column widths (`width / cols`) and row heights (`height / rows`).
  - `draw_flexible(xy, column_widths, row_heights, data)`: Explicit per-column and per-row sizing.

### 3.2 Constructor & Style Methods
```python
table = Table()
```

#### Predefined Styles
- `set_predefined_style(name: Literal["default", "none", "monochrome", "border_simple"])`:
  - `"default"`: Light blue header with bold white text, alternating snow/white rows, thin bottom border.
  - `"none"`: Transparent backgrounds with charcoal text, no borders.
  - `"monochrome"`: Graphite gray header with bold white text, alternating snow/white rows.
  - `"border_simple"`: White backgrounds with bold charcoal header, double top borders, solid bottom border.
- `clear_styles()`: Resets all registered cell and border style overrides.

#### Cell Styling Methods
- `set_style_cell_headers(background_color, textstyle)`: Applies background and text style to both row 0 and column 0.
- `set_style_cell_header(background_color, textstyle)`: Applies style exclusively to column headers (row 0).
- `set_style_cell_rowheader(background_color, textstyle)`: Applies style exclusively to row headers (column 0).
- `set_style_cell_evenodd(even_color, even_textstyle, odd_color, odd_textstyle)`: Alternating styles for even/odd data rows.
- `set_style_cell(background_color, textstyle, rows=None, columns=None)`: Targets specific rows or columns (0-indexed indices).

#### Border Styling Methods
- `set_style_border(top=None, top2=None, bottom=None, left=None, left2=None, right=None, between_columns=None, between_rows=None)`:
  - `top`, `bottom`, `left`, `right`: Perimeter border lines.
  - `top2`: Secondary top border line beneath header row.
  - `left2`: Secondary vertical line to right of row header column.
  - `between_columns`: Vertical separator lines between inner data columns.
  - `between_rows`: Horizontal separator lines between inner data rows.

### 3.3 Production Example: Microservice SLA & Availability Table
```drawlib show-code
from drawlib.canvas import config, save
from drawlib.colors import Colors, Colors140, ColorsEssentials
from drawlib.smartarts import Table
from drawlib.types import Style

config(width=120, height=65)

table = Table(styles=styles)
table.clear_styles()

table.set_style_cell_header(background_color=ColorsEssentials.Graphite, textstyle=styles.white_bold)
table.set_style_cell_evenodd(
    even_color=ColorsEssentials.Snow,
    even_textstyle=styles.primary.patch(text_color=ColorsEssentials.Charcoal, text_size=10),
    odd_color=ColorsEssentials.White,
    odd_textstyle=styles.primary.patch(text_color=ColorsEssentials.Charcoal, text_size=10),
)
# SLA highlight (Row 2, Column 3)
table.set_style_cell(
    background_color=Colors140.PaleGreen,
    textstyle=styles.primary.patch(text_color=Colors140.ForestGreen, text_size=10),
    rows=[2],
    columns=[3],
)
table.set_style_border(
    top=styles.primary.patch(line_color=ColorsEssentials.Charcoal, line_width=1.5),
    top2=styles.primary.patch(line_color=ColorsEssentials.Charcoal, line_width=1.0),
    bottom=styles.primary.patch(line_color=ColorsEssentials.Charcoal, line_width=1.5),
    between_rows=styles.primary.patch(line_color=Colors140.LightGray, line_width=0.5),
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
- **Root Node Requirement**: Root `TreeNode` must define default propagation settings: `default_textstyle`, `default_linestyle`, `default_line_horizontal_margin`, `default_line_horizontal_length`, and `default_line_vertical_margin`.

### 4.2 Constructor Parameters
```python
TreeNode(
    text: str,
    textstyle: str | Style | None = None,
    linestyle: str | Style | None = None,
    line_horizontal_margin: float | None = None,
    line_horizontal_length: float | None = None,
    line_vertical_margin: float | None = None,
    children: list[TreeNode] | None = None,
    default_textstyle: str | Style | None = None,
    default_linestyle: str | Style | None = None,
    default_line_horizontal_margin: float | None = None,
    default_line_horizontal_length: float | None = None,
    default_line_vertical_margin: float | None = None,
)
```

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
from drawlib.canvas import config, save
from drawlib.colors import Colors140, ColorsEssentials
from drawlib.icons import phosphor
from drawlib.smartarts import TreeNode
from drawlib.types import Style

config(width=110, height=70)

TreeNode.register_drawing_item(
    name="dir_icon", location="before", padding_width=4.5, function=phosphor.folder,
    style=styles.primary.patch(icon_color=ColorsEssentials.LightBlue), args={"width": 3.0},
)
TreeNode.register_drawing_item(
    name="py_icon", location="before", padding_width=4.5, function=phosphor.file_py,
    style=styles.primary.patch(icon_color=Colors140.ForestGreen), args={"width": 3.0},
)
TreeNode.register_drawing_item(
    name="yaml_icon", location="before", padding_width=4.5, function=phosphor.file_code,
    style=styles.primary.patch(icon_color=ColorsEssentials.Graphite), args={"width": 3.0},
)

tree_root = TreeNode(
    "monorepo-root/",
    default_textstyle=styles.primary.patch(text_size=11),
    default_linestyle=styles.primary.patch(line_color=ColorsEssentials.Gray, line_width=1.0),
    default_line_horizontal_margin=3.0,
    default_line_horizontal_length=3.0,
    default_line_vertical_margin=6.0,
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
## 5. Component 3: BoxList & BoxTreeNode

`BoxList` draws sequential linear blocks or cards with optional individual highlight overrides, while `BoxTreeNode` is the standard alias for `MindMapNode` to maintain backward compatibility for card-based trees.

### 5.1 BoxList Architecture & Directional Alignment
- **Anchor**: Coordinate `xy=(x, y)` marks start point.
- **Alignment Modes (`align`)**:
  - `"left"`: Cards sequence toward right (`+x`), `xy` at left edge vertical center.
  - `"right"`: Cards sequence toward left (`-x`).
  - `"bottom"`: Cards stack upward (`+y`), `xy` at bottom edge horizontal center.
  - `"top"`: Cards stack downward (`-y`).

### 5.2 BoxList Methods
- `BoxList(default_box_style=None, default_text_style=None)`: Initializes defaults.
- `append(text, box_style=None, text_style=None)`: Appends a card with optional custom style override.
- `insert(index, text, box_style=None, text_style=None)`: Inserts a card at a specified index.
- `extend(texts, box_style=None, text_style=None)`: Batches multiple cards using default or uniform custom styles.
- `draw(xy, box_width, box_height, align="left")`: Renders all cards in specified orientation.

### 5.3 BoxTreeNode (MindMapNode Alias)
`BoxTreeNode` is defined as:
```python
from drawlib.smartarts import BoxTreeNode, MindMapNode
assert BoxTreeNode is MindMapNode
```
It accepts all parameters of `MindMapNode` (`text`, `children`, `branch`, `shape="rectangle"`, `size=(w, h)`, `style`, `r`).

### 5.4 Production Example: Horizontal Service Pipeline & Status Cards
```drawlib show-code
from drawlib.canvas import config, save
from drawlib.colors import Colors140, ColorsEssentials
from drawlib.smartarts import BoxList
from drawlib.types import Style

config(width=110, height=50)

pipeline = BoxList(
    styles=styles,
    default_box_style=styles.primary.patch(shape_fill_color=ColorsEssentials.LightBlue, shape_line_color=ColorsEssentials.Charcoal, shape_line_width=1.0),
    default_text_style=styles.white_bold.patch(text_size=10),
)
pipeline.append("1. Ingestion")
pipeline.append("2. Validation")
# Highlighted degraded step
pipeline.append(
    "3. ML Inference",
    box_style=styles.primary.patch(shape_fill_color=Colors140.Crimson, shape_line_color=Colors140.DarkRed, shape_line_width=1.5),
    text_style=styles.white_bold.patch(text_size=10),
)
pipeline.append("4. Persistence")
pipeline.append("5. Dispatch")
pipeline.draw(xy=(8, 30), box_width=18, box_height=10, align="left")

status_list = BoxList(styles=styles, default_box_style=styles.gray_flat, default_text_style=styles.white_bold)
status_list.extend(["Cluster A: OK", "Cluster B: OK", "Cluster C: WARN"])
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

### 6.2 Constructor Parameters
```python
MindMapNode(
    text: str,
    branch: Literal["bottom", "top", "left", "right"] | None = None,
    shape: Literal["rectangle", "oval", "none"] | None = None,
    size: tuple[float, float] | None = None,
    style: str | Style | None = None,
    r: float | None = None,
    textstyle: str | Style | None = None,
    linestyle: str | Style | None = None,
    horizontal_margin: float | None = None,
    vertical_margin: float | None = None,
    line_length: float | None = None,
    xy_shift: tuple[float, float] | None = None,
    children: list[MindMapNode] | None = None,
    default_branch: Literal["bottom", "top", "left", "right"] | None = None,
    default_shape: Literal["rectangle", "oval", "none"] | None = None,
    default_size: tuple[float, float] | None = None,
    default_style: str | Style | None = None,
    default_r: float | None = None,
    default_textstyle: str | Style | None = None,
    default_linestyle: str | Style | None = None,
    default_horizontal_margin: float | None = None,
    default_vertical_margin: float | None = None,
    default_line_length: float | None = None,
)
```

### 6.3 Shapes & Layout Options
- `shape`: `"rectangle"` (rounded via `r`), `"oval"`, or `"none"` (clean text label).
- `branch`: `"bottom"` (top-down), `"top"` (bottom-up), `"right"` (left-to-right), `"left"` (right-to-left), or multi-directional.
- `xy_shift`: Relative `(dx, dy)` offset applied after layout calculation to fine-tune placement or avoid label collisions.

### 6.4 Production Example: Multi-Directional Architecture Overview
```drawlib show-code
from drawlib.canvas import config, save
from drawlib.colors import ColorsEssentials
from drawlib.fonts import Font
from drawlib.smartarts import MindMapNode
from drawlib.types import Style

config(width=220, height=110)

txt_white = styles.primary.patch(text_color=ColorsEssentials.White, text_size=9, text_font=Font.SANSSERIF_BOLD)
txt_child = styles.primary.patch(text_size=8.5, text_font=Font.SANSSERIF_BOLD)
txt_leaf = styles.primary.patch(text_size=9)

root = MindMapNode(
    "Core API Gateway",
    shape="oval",
    size=(28, 12),
    style=styles.primary.patch(shape_fill_color=ColorsEssentials.Graphite, shape_line_color=ColorsEssentials.Charcoal),
    textstyle=txt_white,
    default_line_length=12.0,
    default_horizontal_margin=4.0,
    default_vertical_margin=4.0,
    children=[
        MindMapNode(
            "Client Traffic", branch="left", shape="rectangle", size=(22, 8), style=styles.blue_flat, textstyle=txt_white,
            children=[
                MindMapNode("Web App (SPA)", shape="none", textstyle=txt_leaf),
                MindMapNode("Mobile Apps", shape="none", textstyle=txt_leaf),
                MindMapNode("Public REST API", shape="none", textstyle=txt_leaf),
            ],
        ),
        MindMapNode(
            "Internal Services", branch="right", shape="rectangle", size=(24, 8), style=styles.green_flat, textstyle=txt_white,
            children=[
                MindMapNode("Auth Service", shape="rectangle", size=(22, 6), style=styles.light, textstyle=txt_child),
                MindMapNode("Billing Engine", shape="rectangle", size=(22, 6), style=styles.light, textstyle=txt_child),
                MindMapNode("Notification Hub", shape="rectangle", size=(22, 6), style=styles.light, textstyle=txt_child),
            ],
        ),
        MindMapNode(
            "Telemetry Stack", branch="top", shape="rectangle", size=(24, 8), style=styles.purple_flat, textstyle=txt_white,
            children=[
                MindMapNode("Prometheus Metrics", shape="none", textstyle=txt_leaf),
                MindMapNode("OpenTelemetry Traces", shape="none", textstyle=txt_leaf),
            ],
        ),
        MindMapNode(
            "Persistence Tier", branch="bottom", shape="rectangle", size=(24, 8), style=styles.orange_flat, textstyle=txt_white,
            children=[
                MindMapNode("PostgreSQL Primary", shape="none", textstyle=txt_leaf),
                MindMapNode("Redis Cache Cluster", shape="none", textstyle=txt_leaf),
            ],
        ),
    ],
)
root.draw(xy=(110, 55), styles=styles)
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
    corner_angle: float = 60.0,
    spacing: float = 1.5,
    flat_left_end: bool = False,
    default_style: str | Style | None = None,
    default_textstyle: str | Style | None = None,
    default_description_style: str | Style | None = None,
    palette: Sequence[tuple[int, int, int]] | None = None,
)
```

### 7.3 Step Management & Drawing
- `append(text, description="", style=None, textstyle=None, description_style=None)`: Appends an individual step.
- `extend(texts, descriptions=None)`: Appends multiple step titles with optional descriptions.
- `insert(index, text, description="", style=None, textstyle=None, description_style=None)`: Inserts a step at a given position.
- `draw(xy, width=90.0, height=12.0, item_width=None)`:
  - `width`: Total bounding width allocated; individual block widths are computed automatically:
    $$\text{item\_width} = \frac{\text{width} - (\text{num\_items} - 1) \cdot \text{spacing} - x_{\text{indent}}}{\text{num\_items}}$$
  - `item_width`: If provided, overrides automatic width distribution.

### 7.4 Production Example: Cloud CI/CD Deployment Pipeline
```drawlib show-code
from drawlib.canvas import config, save
from drawlib.colors import Colors140, ColorsEssentials
from drawlib.smartarts import ChevronProcess
from drawlib.types import Style

config(width=130, height=45)

pipeline = ChevronProcess(
    styles=styles,
    corner_angle=60.0,
    spacing=2.0,
    flat_left_end=True,
    default_textstyle=styles.white_bold.patch(text_size=9.5),
    default_description_style=styles.white.patch(text_size=8, text_color=ColorsEssentials.Snow),
)
pipeline.append("1. Commit", description="Lint / Hooks", style=styles.gray_flat)
pipeline.append("2. Build", description="Docker Image", style=styles.blue_flat)
# Active Stage Highlight
pipeline.append(
    text="3. Security",
    description="SAST & CVE",
    style=styles.primary.patch(shape_fill_color=Colors140.Crimson, shape_line_color=ColorsEssentials.Charcoal, shape_line_width=1.5),
    textstyle=styles.white_bold.patch(text_size=9.5),
    description_style=styles.white.patch(text_size=8, text_color=ColorsEssentials.Snow),
)
pipeline.append("4. Staging", description="Integration", style=styles.blue_flat)
pipeline.append("5. Production", description="Canary Deploy", style=styles.green_flat)
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
    default_style: str | Style | None = None,
    default_textstyle: str | Style | None = None,
    default_description_style: str | Style | None = None,
    default_arrow_style: str | Style | None = None,
    palette: Sequence[tuple[int, int, int]] | None = None,
    center_text: str = "",
    center_description: str = "",
    center_radius: float = 10.0,
    center_style: str | Style | None = None,
    center_textstyle: str | Style | None = None,
    center_description_style: str | Style | None = None,
)
```

### 8.3 Key Configuration Options
- `arrow_color_mode`: `"match_source"` (matches preceding node), `"match_target"` (matches succeeding node), `"monochrome"`.
- `description_placement`: `"inside"` (inside node body) or `"outside"` (radiates outward).
- `set_center(text, description="", radius=None, style=None, textstyle=None, description_style=None)`: Configures central hub node.

### 8.4 Production Example: SRE Incident Response Lifecycle
```drawlib show-code
from drawlib.canvas import config, save
from drawlib.colors import Colors140, ColorsEssentials
from drawlib.smartarts import Cycle
from drawlib.types import Style

config(width=100, height=90)

incident_cycle = Cycle(
    styles=styles,
    clockwise=True,
    start_angle=90.0,
    node_shape="circle",
    node_radius=8.0,
    arrow_type="arc",
    arrow_width=1.5,
    arrow_head_width=4.0,
    arrow_color_mode="match_source",
    default_textstyle=styles.white_bold.patch(text_size=9),
    default_description_style=styles.white.patch(text_size=7, text_color=ColorsEssentials.Snow),
    description_placement="inside",
)
incident_cycle.append("1. Detect", description="Alert Fires", style=styles.red_flat)
incident_cycle.append("2. Triage", description="Assess Scope", style=styles.orange_flat)
incident_cycle.append("3. Mitigate", description="Failover / Rollback", style=styles.green_flat)
incident_cycle.append("4. Resolve", description="Root Fix", style=styles.blue_flat)
incident_cycle.append("5. Learn", description="Action Items", style=styles.purple_flat)

incident_cycle.set_center(
    text="SRE",
    description="Command",
    radius=11.0,
    style=styles.charcoal_flat,
    textstyle=styles.white_bold.patch(text_size=12),
    description_style=styles.white.patch(text_color=Colors140.LightGray, text_size=8),
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
    num_column: int,
    num_row: int,
    default_r: float = 0,
    default_style: str | Style | None = None,
    default_textstyle: str | Style | None = None,
    default_textangle: float | None = None,
)
```

Adding items to the grid:
```python
grid.add(
    position: tuple[int, int],  # (column_start, row_start)
    width: int,                 # Number of columns spanned
    height: int,                # Number of rows spanned
    r: float | None = None,
    style: str | Style | None = None,
    text: str = "",
    textstyle: str | Style | None = None,
    textangle: float | None = None,
    text_xy_shift: tuple[float, float] | None = None,
)
```

### 9.3 Drawing Modes
- `draw(xy, width, height, margin, outer_r=None, outer_style=None)`: Even column and row dimensions with uniform `margin` gutters between cells and around borders.
- `draw_flexible(xy, column_widths, column_margins, row_heights, row_margins, outer_r=None, outer_style=None)`: Custom widths and heights for each individual column and row.

### 9.4 Production Example: Multi-Tier Cloud Software Architecture
```drawlib show-code
from drawlib.canvas import config, save
from drawlib.colors import Colors140, ColorsEssentials
from drawlib.smartarts import GridLayout
from drawlib.types import Style

config(width=110, height=75)

grid = GridLayout(styles=styles, num_column=4, num_row=4, default_r=1.5, default_style=styles.solid, default_textstyle=styles.white_bold)

# Row 3 (Top): Client & CDN Ingress
grid.add(position=(0, 3), width=4, height=1, text="Edge Ingress: Cloudflare CDN & WAF Gateway", style=styles.purple_flat)
# Row 2: Microservice Layer
grid.add(position=(0, 2), width=2, height=1, text="Order & Cart API", style=styles.blue_flat)
grid.add(position=(2, 2), width=1, height=1, text="Auth API", style=styles.blue_flat)
grid.add(position=(3, 2), width=1, height=1, text="Notify", style=styles.blue_flat)
# Row 1: Persistence Tier
grid.add(position=(0, 1), width=1, height=1, text="Postgres", style=styles.green_flat)
grid.add(position=(1, 1), width=1, height=1, text="Mongo", style=styles.green_flat)
grid.add(position=(2, 1), width=2, height=1, text="Redis Replication Cluster", style=styles.green_flat)
# Row 0 (Bottom): Cloud Infrastructure
grid.add(position=(0, 0), width=4, height=1, text="Kubernetes Core Platform (AWS EKS Multi-AZ)", style=styles.gray_flat)

grid.draw(
    xy=(10, 10),
    width=90,
    height=55,
    margin=1.5,
    outer_r=2.0,
    outer_style=styles.primary.patch(shape_line_color=ColorsEssentials.Charcoal, shape_line_width=1.0, shape_fill_color=ColorsEssentials.Snow),
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
    default_style: str | Style | None = None,
    default_textstyle: str | Style | None = None,
    default_textangle: float | None = None,
    default_text_xy_shift: tuple[float, float] | None = None,
)
```

Adding tiers:
```python
pyramid.add(
    text: str,
    style: str | Style | None = None,
    textstyle: str | Style | None = None,
    textangle: float | None = None,
    text_xy_shift: tuple[float, float] | None = None,
)
```

### 10.3 Drawing APIs
- `draw(xy, width, height, margin, align="bottom", order="vertex_to_base")`: Uniform tier heights:
  $$\text{tier\_height} = \frac{\text{height} - (N - 1) \cdot \text{margin}}{N}$$
- `draw_flexible(xy, width, item_heights, margins, align="bottom", order="vertex_to_base")`: Explicit heights per tier.

### 10.4 Production Example: Software Testing Pyramid
```drawlib show-code
from drawlib.canvas import config, save
from drawlib.colors import Colors140, ColorsEssentials
from drawlib.smartarts import Pyramid
from drawlib.types import Style

config(width=100, height=65)

test_pyramid = Pyramid(styles=styles, default_textstyle=styles.white_bold.patch(text_size=10))
test_pyramid.add("Manual (1%)", style=styles.red_flat, textstyle=styles.white_bold.patch(text_size=8.5))
test_pyramid.add("End-to-End UI Tests (9%)", style=styles.orange_flat)
test_pyramid.add("Integration & Contract Tests (20%)", style=styles.blue_flat)
test_pyramid.add("Unit Tests (70%)", style=styles.green_flat)

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
    styles: BasePresetStyles,
    vertical_margin: float,
    indent_width: float,
    default_style: Style | None = None,
)
```

- `set_indent(level: int)`: Changes active indent level for all subsequent `add()` calls.
- `set_bullet_style(indent_level: int, function: Callable, style: Style, args: dict)`: Overrides bullet marker shape for a specific indent level (e.g. `circle`, `rectangle`, or Phosphor icon functions).
- `add(text: str, style: Style | None = None)`: Appends an item at current active indent level.
- `draw(xy: tuple[float, float])`: Renders bullet points starting from `xy`.

### 11.3 Production Example: Architecture Decision RFC Summary
```drawlib show-code
from drawlib.canvas import config, save
from drawlib.colors import Colors140, ColorsEssentials
from drawlib.icons import phosphor
from drawlib.shapes import rectangle
from drawlib.smartarts import BulletPoints
from drawlib.types import Style

config(width=110, height=65)

bp = BulletPoints(
    styles=styles,
    vertical_margin=4.5,
    indent_width=5.0,
    default_style=styles.primary.patch(text_size=10, text_color=ColorsEssentials.Charcoal),
)
bp.set_bullet_style(
    indent_level=1,
    function=rectangle,
    style=styles.primary.patch(shape_fill_color=ColorsEssentials.LightBlue, shape_line_width=0),
    args={"width": 1.2, "height": 1.2},
)
bp.set_bullet_style(
    indent_level=2,
    function=phosphor.check_circle,
    style=styles.primary.patch(icon_color=Colors140.ForestGreen),
    args={"width": 2.0},
)

bp.set_indent(0)
bp.add("RFC 402: Event-Driven Order Processing", style=styles.bold)
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

`SourceCode` integrates the Pygments syntax highlighter with PIL image rendering to embed code snippets directly onto the canvas with syntax coloring, custom fonts, and line numbers.

### 12.1 Supported Languages & Themes
- **Languages (`language`)**:
  `"python"`, `"bash"`, `"go"`, `"rust"`, `"typescript"`, `"javascript"`, `"json"`, `"yaml"`, `"sql"`, `"docker"`, `"toml"`, `"c"`, `"c++"`, `"c#"`, `"java"`, `"kotlin"`, `"swift"`, `"html"`, `"css"`, `"protobuf"`, `"markdown"`, etc. Passing `None` enables automatic syntax guessing via Pygments.
- **Themes (`style`)**:
  `"monokai"`, `"github-dark"`, `"xcode"`, `"default"`, `"lightbulb"`, `"bw"`, `"sas"`, `"staroffice"`, `"rrt"`.

### 12.2 Constructor Parameters
```python
SourceCode(
    language: str | None = None,
    style: str = "default",
    font: FontSourceCode | FontFile | None = None,
    show_linenum: bool = False,
    linenum_textcolor: tuple[int, int, int] = (136, 136, 102),
    linenum_bgcolor: tuple[int, int, int] = (238, 238, 221),
)
```

### 12.3 Key Methods
- `draw(xy, width, code, style=None)`: Renders code block onto canvas. `xy` anchors code image, and `width` controls its display width.
- `get_image(code: str) -> Dimage`: Returns rendered raster image object directly.
- `get_text(file: str, strip: bool = True) -> str`: Static utility to load source code from an external file relative to script location.

### 12.4 Production Example: Embedded Configuration Block
```drawlib show-code
from drawlib.canvas import config, save
from drawlib.shapes import rectangle
from drawlib.smartarts import SourceCode
from drawlib.types import Style

config(width=110, height=105)

# Outer window frame
rectangle(xy=(55, 52.5), width=96, height=95, r=2, style=styles.charcoal_solid)
# Header bar
rectangle(
    xy=(55, 94),
    width=96,
    height=12,
    r=2,
    style=styles.charcoal_flat,
    text="Kubernetes Deployment Spec (v1)",
    textstyle=styles.white_bold,
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

sc = SourceCode(language="yaml", style="monokai", show_linenum=True)
sc.draw(xy=(55, 45), width=88, code=k8s_yaml)
save()
```

---
## 13. Component 11: bubblespeech (Callouts & Speech Bubbles)

`bubblespeech` draws an irregular speech bubble or callout box with a customized triangular pointer tail, designed for comic dialogue, system callouts, and migration notes.

### 13.1 Vector Tail Geometry
```
           tail_start_ratio         tail_end_ratio
                  │                      │
     ┌────────────▼──────────────────────▼────────────┐
     │                                                │
     │                 Speech Box Body                │
     │                                                │
     └───────────────────────────▲────────────────────┘
                                ╱ ╲
                               ╱   ╲
                              ╱     ╲
                             ▼       ▼
                        tail_vertex_xy
```
- **Body Anchor**: `xy=(x, y)` specifies **bottom-left corner** of rectangular bubble body.
- **Edge Selection (`tail_edge`)**: `"bottom"`, `"top"`, `"left"`, `"right"`.
- **Ratios along Edge**:
  - `tail_start_ratio`: Float in `[0.0, 1.0]` where tail begins along edge.
  - `tail_end_ratio`: Float in `[0.0, 1.0]` where tail ends along edge (must be $> \text{tail\_start\_ratio}$).
- **Target Vertex (`tail_vertex_xy`)**: Absolute coordinate `(vx, vy)` pointing directly to target shape, server, or bottleneck.

### 13.2 Function Signature
```python
bubblespeech(
    xy: tuple[float, float],
    width: float,
    height: float,
    tail_edge: Literal["left", "top", "right", "bottom"],
    tail_start_ratio: float,
    tail_vertex_xy: tuple[float, float],
    tail_end_ratio: float,
    *,
    style: Style,
    text: str = "",
    textsize: float | None = None,
    textstyle: Style | None = None,
)
```

### 13.3 Production Example: Architecture Bottleneck Callout
```drawlib show-code
from drawlib.canvas import config, save
from drawlib.colors import Colors140, ColorsEssentials
from drawlib.fonts import Font
from drawlib.shapes import rectangle
from drawlib.smartarts import bubblespeech
from drawlib.types import Style

config(width=110, height=60)

rectangle(
    xy=(25, 20),
    width=24,
    height=14,
    r=1.5,
    style=styles.red_flat,
    text="Legacy RDBMS\n(Bottleneck)",
    textstyle=styles.white_bold,
)

bubblespeech(
    xy=(55, 30),
    width=48,
    height=20,
    tail_edge="bottom",
    tail_start_ratio=0.15,
    tail_end_ratio=0.45,
    tail_vertex_xy=(25, 27),
    style=styles.primary.patch(
        shape_fill_color=Colors140.LightCoral,
        shape_line_color=Colors140.Crimson,
        shape_line_width=1.5,
    ),
    text="ACTION REQUIRED:\nExceeding IOPS threshold.\nMigrate read replicas to AWS Aurora.",
    textsize=9,
    textstyle=styles.primary.patch(
        text_color=Colors140.DarkRed,
        text_font=Font.SANSSERIF_BOLD,
        text_size=9,
    ),
)
save()
```

---
## 14. Design Patterns & Coordinate Anchor Systems

### 14.1 Coordinate Normalization Cheat Sheet

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
| `bubblespeech` | Bottom-Left `(x, y)` | Pass `(X, Y - H)` | Pass `(X, Y)` directly |
| `MindMapNode` | Root Center `(x, y)` | Pass `(X + W/2, Y - H/2)` | Pass `(X + W/2, Y + H/2)` |
| `Cycle` (align="center") | Orbit Center `(x, y)` | Pass `(X + R, Y - R)` | Pass `(X + R, Y + R)` |

### 14.2 Multi-Component Dashboard Integration Example
```drawlib show-code
from drawlib.canvas import config, save
from drawlib.colors import Colors140, ColorsEssentials
from drawlib.smartarts import ChevronProcess, GridLayout, SourceCode, Table
from drawlib.types import Style

config(width=120, height=80)

# 1. Top Section: Pipeline Status
pipeline = ChevronProcess(
    styles=styles,
    corner_angle=60.0,
    spacing=1.5,
    flat_left_end=True,
    default_textstyle=styles.white_bold,
    default_description_style=styles.light,
)
pipeline.extend(
    texts=["1. Plan", "2. Build", "3. Test", "4. Deploy"],
    descriptions=["Arch Review", "Docker Image", "E2E Verified", "Production"],
)
pipeline.draw(xy=(10, 62), width=100, height=12)

# 2. Bottom-Left Section: Service Matrix Table
table = Table(styles=styles)
table.set_predefined_style("default")
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

sc = SourceCode(language="python", style="monokai", show_linenum=True)
sc.draw(xy=(92, 32), width=44, code=snippet)

save()
```

---
## 15. Troubleshooting & Common Pitfalls

### 1. Inverted Table or Grid Placement
- **Problem**: Table rows or GridLayout cells render outside canvas or upside down.
- **Cause**: Confusing Top-Left vs. Bottom-Left anchors.
- **Resolution**:
  - `Table` takes `(x, y)` as **top-left** point. Providing `(10, 10)` on an $80$-tall canvas causes it to draw downward past bottom boundary ($y = 10 \to y = -35$). Use `(10, 70)`.
  - `GridLayout` takes `(x, y)` as **bottom-left** point, and `row=0` is at bottom.

### 2. Missing TreeNode Defaults on Root
- **Problem**: Calling `tree_root.draw(xy)` raises `ValueError: Root of TreeNode must be initialized with arg "default_textstyle"`.
- **Cause**: Root `TreeNode` requires default values to propagate down to descendants that do not specify explicit styles.
- **Resolution**: Always supply `default_textstyle`, `default_linestyle`, `default_line_horizontal_margin`, `default_line_horizontal_length`, and `default_line_vertical_margin` on root node instance.

### 3. Subtree Overlaps in MindMapNode
- **Problem**: Sibling subtrees collide or overlap when branching in same direction.
- **Resolution**: Increase `default_horizontal_margin` (for `"bottom"` or `"top"` branches) or `default_vertical_margin` (for `"left"` or `"right"` branches). You can also apply localized `xy_shift=(dx, dy)` on problematic child nodes.

### 4. bubblespeech Ratio Assertions
- **Problem**: `ValueError: tail_start_ratio must be smaller than tail_end_ratio`.
- **Cause**: Passing `tail_start_ratio >= tail_end_ratio` or ratios exceeding `1.0`.
- **Resolution**: Ensure `0.0 <= tail_start_ratio < tail_end_ratio <= 1.0`.

### 5. Cycle Arrow Overlaps
- **Problem**: Connecting curved arrows collide with step circles.
- **Resolution**: Increase `arrow_gap` (default 2.5) or enlarge `radius` relative to `node_radius`. Ensure `arrow_width <= arrow_head_width`.
