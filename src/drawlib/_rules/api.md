# Drawlib API Reference & Cheat Sheet

Drawlib is a pure-Python library for **"Illustration as Code"** and **"Illustrated Documentation as Code"**.  
This document serves as the unified, high-speed API index and cheat sheet covering all public modules, classes, drawing primitives, styling tokens, and developer utilities.

---

## 1. Quick Import Cheat Sheet

```python
# 1. Canvas Lifecycle
from drawlib.canvas import canvas, clear, get_dimage, save, setup, show

# 2. Design Tokens & Styling (Always PascalCase!)
from drawlib.styles import Colors, Styles, get_intermediate_color, get_intermediate_colors
from drawlib.types import Color, Style
from drawlib.preset_colors import CssColors, DefaultColors, GoogleColors, MonochromeColors

# 3. Drawing Primitives
from drawlib.shapes import (
    arc, arrow, arrow_arc, arrow_l, arrow_polyline, arrow_u, bubblespeech, chevron,
    circle, cylinder, donuts, ellipse, face, fan, parallelogram, polygon, rectangle,
    regularpolygon, rhombus, shape, star, trapezoid, triangle, wedge,
)
from drawlib.lines import (
    line, line_arc, line_bezier1, line_bezier2, line_curved,
    lines, lines_curved, lines_bezier,
)
from drawlib.text import text, text_vertical

# 4. High-Level Diagrams & Auto-Layout Graphs
from drawlib.graph import (
    ArchitectureGraph, Cluster, Edge, GraphLayout, GridGraph,
    LayerGraph, Node, RadialGraph, TreeGraph,
)
from drawlib.diagrams.architecture import ArchitectureDiagram, Edge, Junction, Node, NodeGroup
from drawlib.diagrams.flow import FlowDiagram
from drawlib.diagrams.sequence import SequenceDiagram
from drawlib.diagrams.state import StateDiagram
from drawlib.diagrams.class_diagram import ClassDiagram
from drawlib.diagrams.er import ERDiagram

# 5. SmartArts Structured Components
from drawlib.smartarts import (
    BoxList, BulletPoints, ChevronProcess, Cycle, GridLayout,
    MindMapNode, Pyramid, SourceCode, SourceCodeStyles, Table, TreeNode,
)

# 6. Statistical & Project Charts
from drawlib.charts.bar import BarChart, Series
from drawlib.charts.line import LineChart, Series
from drawlib.charts.area import AreaChart, Series
from drawlib.charts.pie import PieChart, Slice
from drawlib.charts.radar import RadarChart, Series
from drawlib.charts.scatter import Point, ScatterChart, Series
from drawlib.charts.gantt import Dependency, GanttChart, Marker, Milestone, Section, Task

# 7. Icons & Media
from drawlib.icons import font_icon, gcp, phosphor
from drawlib.images import Dimage, get_dimage_from_code, image
from drawlib.fonts import Font, FontFile, get_font, list_fonts, list_system_fonts

# 8. Geometry & Math
from drawlib.math import get_angle, get_center_and_size, get_distance

# 9. Animations (APNG & Animated WebP)
from drawlib.anim import Animation

# 10. Presentation Slides
from drawlib.slide import BoundingBox, SlideContext, build_slide, current_slide

# 11. Developer Tools
from drawlib.tools import clear_cache, init_project, list_cache, scan_broken_links, serve_docs
```

---

## 2. Canvas Lifecycle (`drawlib.canvas`)

The canvas operates in a Cartesian coordinate space with the origin `(0, 0)` located at the **bottom-left corner**.

| Function | Parameters | Description |
| :--- | :--- | :--- |
| `setup(...)` | `width: float = 100`, `height: float = 100`, `style: Style \| None = None`, `background: Color \| None = None`, `grid: bool = False`, `grid_interval: float = 10` | Initializes canvas dimensions, background color, and optional coordinate grid. |
| `save(...)` | `file_path: str = ...` | Exports the drawn canvas to an image file (`.png`, `.jpg`, `.svg`, `.pdf`). |
| `clear()` | None | Clears the active canvas and resets state for the next diagram. |
| `show(...)` | None | Displays the interactive GUI preview window (avoid in headless CI / agents). |
| `get_dimage()` | None | Returns the current canvas as an in-memory `Dimage` object. |
| `canvas` | Singleton | Global canvas context object. |

```drawlib show-code file:canvas_lifecycle.png
from drawlib.canvas import setup
from drawlib.shapes import rectangle
from drawlib.styles import Styles

# 1. Initialize canvas dimensions (width=100, height=45)
setup(width=100, height=45)

# 2. Draw canvas content
rectangle((50, 22), width=80, height=26, style=Styles.PrimaryFlat, text="Canvas (100x45)", text_style=Styles.WhiteBold)
```

---

## 3. Geometric Shapes Primitives (`drawlib.shapes`)

All shape primitives accept `style: Style | None = None`, `text: str = ""`, and `text_style: Style | None = None`.  
Coordinates `xy` refer to the **center point** `(cx, cy)` unless otherwise noted.

| Function | Geometric Parameters | Description |
| :--- | :--- | :--- |
| `rectangle(xy, width, height, ...)` | `r: float = 0`, `angle: float = 0` | Rectangle or rounded rectangle (`r > 0`). |
| `circle(xy, radius, ...)` | `radius: float` | Perfect circle centered at `xy`. |
| `cylinder(xy, width, height, ...)` | `disks: int = 1`, `angle: float = 0` | 3D cylinder / multi-disk database stack (`disks > 1`) centered at `xy`. |
| `face(xy, radius, ...)` | `mood: str = "smile"`, `angle: float = 0` | Expressive face (`"smile"`, `"neutral"`, `"sad"`, `"angry"`, `"surprised"`) centered at `xy`. |
| `ellipse(xy, width, height, ...)` | `angle: float = 0` | Ellipse centered at `xy` with rotation angle. |
| `wedge(xy, radius, angle1, angle2, ...)` | `angle1: float`, `angle2: float` | Circular sector / wedge slice from `angle1` to `angle2`. |
| `fan(xy, radius, angle1, angle2, ...)` | `angle1: float`, `angle2: float` | Fan shape (wedge with arc perimeter). |
| `arc(xy, radius, angle1, angle2, ...)` | `angle1: float`, `angle2: float` | Arc segment perimeter. |
| `donuts(xy, radius_outer, radius_inner, ...)` | `radius_outer: float`, `radius_inner: float` | Annular ring / donut shape. |
| `triangle(xy1, xy2, xy3, ...)` | `xy1, xy2, xy3: tuple[float, float]` | Triangle defined by 3 vertices. |
| `trapezoid(xy, width_bottom, width_top, height, ...)` | `width_bottom, width_top, height`, `angle: float = 0` | Symmetrical trapezoid. |
| `parallelogram(xy, width, height, shift, ...)` | `width, height, shift`, `angle: float = 0` | Parallelogram with horizontal vertex skew `shift`. |
| `rhombus(xy, width, height, ...)` | `width, height`, `angle: float = 0` | Diamond / rhombus shape. |
| `regularpolygon(xy, radius, num_edges, ...)` | `radius, num_edges: int`, `angle: float = 0` | Regular N-sided polygon (pentagon, hexagon, etc.). |
| `polygon(points, ...)` | `points: list[tuple[float, float]]` | Arbitrary closed polygon from coordinate list. |
| `star(xy, num_vertex, radius_ext, radius_int, ...)` | `num_vertex: int`, `radius_ext: float`, `radius_int: float`, `angle: float = 0` | Multi-pointed star shape. |
| `chevron(xy, width, height, corner_angle, ...)` | `width, height, corner_angle: float`, `mirror: bool = False`, `angle: float = 0` | Process chevron arrow shape centered at `xy`. |
| `arrow(xy, width, height, ...)` | `width, height`, `angle: float = 0` | Block arrow shape pointing right (or rotated). |
| `arrow_l(xy, width, height, ...)` | `width, height`, `angle: float = 0` | L-shaped bent block arrow. |
| `arrow_u(xy, width, height, ...)` | `width, height`, `angle: float = 0` | U-turn block arrow. |
| `arrow_arc(xy, radius, angle1, angle2, ...)` | `radius, angle1, angle2`, `width: float` | Curved circular block arrow. |
| `arrow_polyline(points, width, ...)` | `points: list[tuple[float, float]]`, `width: float` | Polyline-following block arrow. |
| `bubblespeech(xy, width, height, tail_edge, ...)` | `tail_edge, tail_start_ratio, tail_end_ratio, tail_vertex_xy` | Rectangular speech bubble with pointer tail. |
| `shape(points, ...)` | `points: list[tuple[float, float]]` | Custom path shape. |

```drawlib show-code file:shapes_primitives.png
from drawlib.canvas import setup
from drawlib.shapes import chevron, circle, rectangle, star
from drawlib.styles import Styles

setup(width=140, height=40)

rectangle((22, 20), width=26, height=18, style=Styles.PrimaryFlat, text="Rectangle", text_style=Styles.WhiteBold)
circle((56, 20), radius=10, style=Styles.Neutral, text="Circle")
chevron((90, 20), width=26, height=18, corner_angle=45, style=Styles.SecondaryNeutral, text="Chevron")
star((122, 20), num_vertex=5, radius_ext=10, radius_int=5, style=Styles.PrimaryNeutral)
```

---

## 4. Lines & Connectors (`drawlib.lines`)

Lines connect coordinates and support arrowheads: `"-"` (none), `"->"` (forward), `"<-"` (reverse), and `"<->"` (bidirectional).

| Function | Signature | Description |
| :--- | :--- | :--- |
| `line(xy1, xy2, ...)` | `(xy1, xy2, *, style, arrow_head="")` | Straight line between two points. |
| `lines(points, ...)` | `(points, *, style, arrow_head="")` | Multi-segment chained polyline (orthogonal routing). |
| `line_curved(xy1, xy2, ...)` | `(xy1, xy2, *, style, bend=0.0, arrow_head="")` | Smooth circular arc curve between two points (`bend` controls curvature). |
| `lines_curved(points, r, ...)` | `(points, r, *, style, arrow_head="")` | Continuous curve passing smoothly through points with corner radius `r`. |
| `line_bezier1(xy1, xy2, cp, ...)` | `(xy1, xy2, cp, *, style, arrow_head="")` | Quadratic Bezier curve with 1 control point `cp`. |
| `line_bezier2(xy1, xy2, cp1, cp2, ...)`| `(xy1, xy2, cp1, cp2, *, style, arrow_head="")` | Cubic Bezier curve with 2 control points `cp1, cp2`. |
| `lines_bezier(xy, path_points, ...)`| `(xy, path_points, *, style, arrow_head="")` | Chained multi-segment Bezier spline. |
| `line_arc(xy, width, height, ...)`| `(xy, width, height, *, style, angle_start=0, angle_end=180, ...)` | Elliptical arc segment line. |

```drawlib show-code file:lines_connectors.png
from drawlib.canvas import setup
from drawlib.lines import line, line_curved, lines
from drawlib.styles import Styles

setup(width=120, height=40)

# 1. Straight connector
line((10, 20), (35, 20), arrow_head="->", style=Styles.DarkBold)

# 2. Curved arc connector
line_curved((45, 12), (75, 12), bend=0.3, arrow_head="<->", style=Styles.PrimaryBold)

# 3. Orthogonal stepped connector via lines()
lines([(85, 12), (98, 12), (98, 28), (115, 28)], arrow_head="->", style=Styles.DarkBold)
```

---

## 5. Text Typography (`drawlib.text`)

Renders single-line or multi-line strings with explicit anchor alignments.

| Function | Parameters | Description |
| :--- | :--- | :--- |
| `text(xy, text, ...)` | `(xy, text, *, style, angle=0.0)` | Standard horizontal text string. Alignments controlled via `style.halign` / `style.valign`. |
| `text_vertical(xy, text, ...)` | `(xy, text, *, style, angle=0.0)` | Vertically stacked characters (ideal for East Asian scripts or vertical axis labels). |

- **`style.halign` Options**: `"left"`, `"center"`, `"right"`
- **`style.valign` Options**: `"bottom"`, `"center"`, `"top"`
- **`style.text_line_spacing`**: `float | None` (line spacing multiplier for multi-line strings `\n`, e.g. `1.6` or `2.0`; defaults to `None` which uses `1.2`)

```drawlib show-code file:text_typography.png
from drawlib.canvas import setup
from drawlib.styles import Styles
from drawlib.text import text, text_vertical

setup(width=120, height=45)

# Centered main title
text((60, 36), "System Architecture", style=Styles.DarkBold)

# Left-aligned and right-aligned annotations using style.patch()
text((15, 20), "Left Aligned", style=Styles.Dark.patch(halign="left"))
text((105, 20), "Right Aligned", style=Styles.Dark.patch(halign="right"))

# Vertical text
text_vertical((60, 16), "STATUS", style=Styles.MutedBold)
```

---

## 6. Design Tokens & Styling (`drawlib.styles`, `drawlib.types`)

### 6.1 PascalCase Design Tokens Rule
- **Always import**: `from drawlib.styles import Colors, Styles`
- **Never lowercase** to `styles` or `colors` (prevents shadowing module `drawlib.styles`).

### 6.2 Preset Style Families (`Styles.<color>_<variant>`)
Styles are systematically constructed as `<color>_<variant>`:

- **Semantic Roles**: `Primary`, `Secondary`, `Accent`, `Warning`, `Neutral`, `Muted`, `Light`, `Dark`, `Danger`, `Success`  
  *(Plus utility shades: `White`, `Black`, `Gray1`..`Gray8`, `Blue`, `Green`, `Red`, `Purple`, etc.)*
- **Card Neutral Tokens (50%+ Neutral Grounding)**:
  - Base: `Styles.Neutral`, `Styles.NeutralFlat`, `Styles.GrayNeutral`, `Styles.GrayNeutralFlat`
  - Semantic cards: `Styles.PrimaryNeutral`, `Styles.SecondaryNeutral`, `Styles.AccentNeutral`, `Styles.WarningNeutral`, ...
  - Named hue cards: `Styles.BlueNeutral`, `Styles.TealNeutral`, `Styles.PurpleNeutral`, `Styles.GreenNeutral`, `Styles.AmberNeutral`, `Styles.RedNeutral`, ...
- **13 Orthogonal Structural Variants**:
  - `Bordered` (default): Solid border (1.5) with soft fill, high-contrast text.
  - `Flat`: Borderless shape (`shape_line_width=0.0`).
  - `Bold`: Thick stroke (2.5) with bold font.
  - `Thin`: Thin stroke (0.75) with thin font.
  - `Outline` / `Solid`: Transparent background with colored border.
  - `Dashed`, `DashedBold`, `DashedThin`: Dashed stroke for boundaries or groupings.
  - `Dotted`, `DottedBold`, `DottedThin`: Dotted stroke for ephemeral objects.
- **Typography Styles**: `Styles.WhiteBold`, `Styles.PrimaryBold`, `Styles.MutedThin`, etc.

### 6.3 Custom Style, Color Construction & Color Interpolation

- **`get_intermediate_color(color1, color2) -> Color`**: Returns the 50% midpoint `Color` between `color1` and `color2`.
- **`get_intermediate_colors(color1, color2, num=1, *, include_ends=False) -> list[Color]`**: Returns `num` evenly spaced intermediate `Color` instances between `color1` and `color2` (or `num + 2` including both endpoints when `include_ends=True`).

```drawlib show-code file:custom_style.png
from drawlib.canvas import setup
from drawlib.shapes import rectangle
from drawlib.types import Color, Style

setup(width=100, height=45)

custom_style = Style(
    shape_fill_color=Color(33, 150, 243, alpha=0.2), # Translucent blue fill
    shape_line_color=Color(33, 150, 243),             # Solid blue border
    shape_line_width=2.5,
    shape_line_style="dashed",
    text_color=Color(20, 20, 20),
    text_size=14,
)

rectangle((50, 22), width=80, height=28, style=custom_style, text="Custom Style Container")
```

---

## 7. High-Level Diagrams (`drawlib.diagrams`)

Always prefer high-level diagrams over manually drawing raw rectangles and connectors. Every diagram and auto-layout graph follows the unified component lifecycle:
- **Mutable Element References & Visibility (`show`)**: Registration methods (`add()`, `connect()`, `fork()`, `junction()`, `add_lane()`, `request()`, `reply()`, `note()`, `loop()`/`alt()`/`opt()`/`par()`, `node()`, `edge()`, `cluster()`) accept `show: bool = True` and return the mutable element instance. Mutating `.show = False`, `.style`, `.text_style`, or `.text` / `.label` updates rendering on the next `draw()` without shifting the diagram's layout bounds, swimlanes, or sequence timelines.
- **Automatic Edge & Dangling Junction Hiding**: Hiding a node (`node.show = False`) automatically hides all connected edges (and any dangling `Junction` pass-through stems whose outgoing or incoming branches are all hidden).
- **Proportional Scaling (`scale`)**: Every diagram supports `diag.draw(xy=(0.0, 0.0), *, scale=1.0)`, uniformly scaling all coordinates, shapes, stroke widths, arrowheads, icons, and font sizes relative to `xy`.

### 7.1 Architecture Diagram (`drawlib.diagrams.architecture`)
Builds cloud topologies, microservice meshes, VPC boundaries, and icon-annotated infrastructure.

```drawlib show-code file:diagram_architecture.png
from drawlib.canvas import setup
from drawlib.diagrams.architecture import ArchitectureDiagram, GcpIcon, Node, NodeGroup, PhosphorIcon
from drawlib.styles import Styles

setup(width=120, height=60)
diag = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark,
    node_card_style=Styles.Neutral,
)

# 1. Container Boundaries / Groups
group = diag.add(NodeGroup(title="Production VPC", width=100, height=44), (10, 8))

# 2. Nodes with Built-in Cloud / Phosphor Icons (1 hero focal node, 2 neutral nodes)
client = diag.add(Node((18, 16), text="Web Client", icon=PhosphorIcon.GLOBE), (25, 30))
gateway = diag.add(
    Node(
        (20, 16),
        text="API Gateway",
        icon=GcpIcon.CLOUD_API_GATEWAY,
        card_style=Styles.PrimaryFlat,
        text_style=Styles.WhiteBold,
    ),
    (60, 30),
)
db = diag.add(Node((18, 16), text="Cloud SQL", icon=GcpIcon.CLOUD_SQL, card_style=Styles.SecondaryNeutral), (95, 30))

# 3. Smart Boundary-Clipping Edges
diag.connect(client, gateway, label="HTTPS")
diag.connect(gateway, db, label="TCP 5432")

diag.draw()
```

### 7.2 Flow Diagram (`drawlib.diagrams.flow`)
Constructs ISO 5807 flowcharts with decision gates, processes, start/stop terminals, and cross-lane routing.

```drawlib show-code file:diagram_flow.png
from drawlib.canvas import setup
from drawlib.diagrams.flow import Decision, End, FlowDiagram, Process, Start
from drawlib.styles import Styles

setup(width=100, height=76)
flow = FlowDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark,
)
start = flow.add(Start("Start"), (50, 66))
proc = flow.add(Process("Execute Job", style=Styles.PrimaryFlat, text_style=Styles.WhiteBold), (50, 48))
gate = flow.add(Decision("Success?", style=Styles.SecondaryNeutral), (50, 28))
end = flow.add(End("End"), (50, 8))

flow.connect(start, proc)
flow.connect(proc, gate)
flow.connect(gate, end, label="Yes")

flow.draw()
```

### 7.3 Sequence Diagram (`drawlib.diagrams.sequence`)
Generates lifelines, synchronous/asynchronous request-response messages, activations, and note boxes.

```drawlib show-code file:diagram_sequence.png
from drawlib.canvas import setup
from drawlib.diagrams.sequence import Participant, SequenceDiagram
from drawlib.styles import Styles

setup(width=100, height=60)
seq = SequenceDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark,
    node_card_style=Styles.Neutral,
)
user = seq.add(Participant((18, 8), "User"))
auth = seq.add(Participant((18, 8), "Auth API", card_style=Styles.PrimaryFlat, text_style=Styles.WhiteBold))
db = seq.add(Participant((18, 8), "Database", card_style=Styles.SecondaryNeutral))

seq.request(user, auth, label="POST /login")
seq.request(auth, db, label="SELECT user")
seq.reply(db, auth, label="UserRecord")
seq.reply(auth, user, label="200 OK")

seq.draw()
```

### 7.4 Other Supported Diagrams
- **State Diagram** (`drawlib.diagrams.state.StateDiagram`): FSM states, composite states, transitions, guard conditions.
- **Class Diagram** (`drawlib.diagrams.class_diagram.ClassDiagram`): UML classes, methods, inheritance (`--|>`), associations, composition.
- **ER Diagram** (`drawlib.diagrams.er.ERDiagram`): Relational tables, columns, primary keys, foreign keys, Crow's foot cardinality.

### 7.5 Declarative Auto-Layout Graphs (`drawlib.graph`)
When you want automatic coordinate computation from topological declarations (`node(..., show=True)`, `edge(..., show=True)`, `cluster(..., show=True)`) with support for post-layout tweaking (`calc()` + `offset()`), translation/scaling (`g.draw(xy=(0, 0), width=None, height=None, margin=10.0, scale=1.0)` / `layout.draw(xy=(0, 0), scale=1.0)`), or code scaffolding (`export_code()`):
- **`ArchitectureGraph`**: 2-level macro/micro container packing and 5-zone compass positioning (`pos="left"|"center"|"right"|"top"|"bottom"`, `parent=...`).
- **`LayerGraph`**: Sugiyama hierarchical DAG solver with `.tier()` stage pinning.
- **`TreeGraph`**: Reingold-Tilford compact tree solver with `.child()`.
- **`RadialGraph`**: Concentric hub-and-spoke solver with `.spoke()`.
- **`GridGraph`**: 2D matrix solver with `.cell()`, `.cluster_row()`, `.cluster_col()`.

---

## 8. SmartArts Structured Components (`drawlib.smartarts`)

High-level automated components for business and technical concepts. Every stateful SmartArt standardizes element registration via `add(..., show=True)` (returning a mutable item instance with `.show`, `.style`, `.text_style`, `.text` evaluated lazily at `draw()` time) and supports proportional scaling via `draw(..., scale=1.0)` / `draw_flexible(..., scale=1.0)`:

| Component | Anchor | Typical Use Case | Primary Usage |
| :--- | :--- | :--- | :--- |
| `Table` | Top-Left `(x, y)` | Comparison matrix, data schemas | `t = Table(...); t.draw(xy, width, height, data, scale=1.0)` |
| `TreeNode` | Top-Left `(x, y)` | Directory trees, org charts | `node = TreeNode("Root", ...); node.add("Child", show=True); node.draw(xy, scale=1.0)` |
| `MindMapNode` | Center `(x, y)` | Radial concept maps | `root = MindMapNode("Topic", ...); root.add("Sub", show=True); root.draw(xy, scale=1.0)` |
| `ChevronProcess` | Bottom-Left `(x, y)` | Linear pipelines & phases | `p = ChevronProcess(...); p.add(..., show=True); p.draw(xy, width, height, scale=1.0)` |
| `Cycle` | Center `(x, y)` | Feedback loops, CI/CD cycles | `c = Cycle(...); c.add(..., show=True); c.draw(xy, radius, scale=1.0)` |
| `GridLayout` | Bottom-Left `(x, y)` | Component matrices, layer decks | `g = GridLayout(...); g.add(..., show=True); g.draw(xy, width, height, margin, scale=1.0)` |
| `Pyramid` | Bottom-Left `(x, y)` | Tiered hierarchy stacks | `p = Pyramid(...); p.add(..., show=True); p.draw(xy, width, height, margin, scale=1.0)` |
| `BoxList` | Bottom-Left `(x, y)` | Feature callouts, card stacks | `b = BoxList(...); b.add(..., show=True); b.draw(xy, box_width, box_height, scale=1.0)` |
| `BulletPoints` | Top-Left `(x, y)` | Bulleted technical notes | `b = BulletPoints(...); b.add(..., show=True); b.draw(xy, scale=1.0)` |
| `SourceCode` | Top-Left `(x, y)` | Highlighted code snippets | `SourceCode.draw(xy, width, code, styles=..., scale=1.0)` |

```drawlib show-code file:smartarts_chevron.png
from drawlib.canvas import setup
from drawlib.smartarts import ChevronProcess
from drawlib.styles import Styles

setup(width=120, height=35)

process = ChevronProcess(
    style=Styles.Neutral,
    text_style=Styles.DarkBold,
    description_style=Styles.Muted,
)
process.add("1. Ingest")
process.add("2. Transform", style=Styles.PrimaryFlat, text_style=Styles.WhiteBold)
process.add("3. Validate")
process.add("4. Export", style=Styles.SecondaryNeutral)
process.draw((10, 8), width=100, height=18)
```

---

## 9. Statistical & Project Charts (`drawlib.charts`)

Drawlib charts render directly into the unified vector canvas alongside architectural diagrams. Every chart supports:
- **Element-Level Visibility & Partial Rendering**: Returned elements (`Series`, `Slice`, `Point`, `Task`, `Section`, `Milestone`, `Marker`, `Dependency`) expose mutable `.show: bool = True`, and quantitative elements (`Series`, `Slice`, `Task`) expose `.draw_ratio: float = 1.0` (`0.0` to `1.0`) and `.draw_direction: DrawDirection` (`"bottom_to_top"` or `"left_to_right"`). Axis scales and layout slots remain locked to the full 100% dataset even when elements are hidden or partially drawn.
- **Spatial Overrides & Uniform Scaling**: `chart.draw(xy, *, width=None, height=None, radius=None, scale=1.0)` and `chart.draw_legend(xy, text_style, ..., scale=1.0)` allow temporary container resizing and uniform proportional scaling around `xy`.

| Chart Class | Element Factory Methods | `draw()` Spatial Overrides |
| :--- | :--- | :--- |
| `BarChart` | `add_series(..., show=True, draw_ratio=1.0, draw_direction=...) -> Series` | `draw(xy, *, width=None, height=None, scale=1.0)` |
| `LineChart` | `add_series(..., show=True, draw_ratio=1.0, draw_direction="left_to_right") -> Series` | `draw(xy, *, width=None, height=None, scale=1.0)` |
| `AreaChart` | `add_series(..., show=True, draw_ratio=1.0, draw_direction="left_to_right") -> Series` | `draw(xy, *, width=None, height=None, scale=1.0)` |
| `ScatterChart` | `add(..., show=True) -> Point`, `add_series(..., show=True, draw_ratio=1.0, draw_direction="left_to_right") -> Series` | `draw(xy, *, width=None, height=None, scale=1.0)` |
| `PieChart` | `add_slice(..., show=True, draw_ratio=1.0, draw_direction="left_to_right") -> Slice` | `draw(xy, *, radius=None, width=None, height=None, scale=1.0)` |
| `RadarChart` | `add_series(..., show=True, draw_ratio=1.0, draw_direction="bottom_to_top") -> Series` | `draw(xy, *, radius=None, width=None, height=None, scale=1.0)` |
| `GanttChart` | `add_task(..., show=True, draw_ratio=1.0, draw_direction="left_to_right") -> Task`, `add_section`, `add_milestone`, `add_marker`, `add_dependency` | `draw(xy, *, width=None, height=None, scale=1.0)` |

```drawlib show-code file:charts_example.png
from drawlib.canvas import setup
from drawlib.charts.bar import BarChart
from drawlib.charts.pie import PieChart
from drawlib.styles import Styles

setup(width=140, height=62)

# 1. Bar Chart on the left
bar_chart = BarChart(
    axis_line_style=Styles.Dark,
    width=52,
    height=38,
    title="Quarterly Sales",
    categories=["Q1", "Q2", "Q3", "Q4"],
)
bar_chart.add_series(name="Cloud", values=[45, 52, 68, 85], style=Styles.PrimaryFlat)
bar_chart.draw((10, 10))

# 2. Donut Chart on the right
pie = PieChart(radius=14, hole_ratio=0.5, title="Resource Usage")
pie.add_slice("Compute", 45, style=Styles.PrimaryFlat)
pie.add_slice("Storage", 35, style=Styles.SecondaryNeutral)
pie.add_slice("Network", 20, style=Styles.Neutral)
pie.draw((104, 26))
```

---

## 10. Icons & Media (`drawlib.icons`, `drawlib.images`, `drawlib.fonts`)

### 10.1 Icons
Drawlib integrates Phosphor vector icons and Google Cloud official architecture icons:

```drawlib show-code file:icons_example.png
from drawlib.canvas import setup
from drawlib.icons import gcp, phosphor
from drawlib.styles import Styles

setup(width=100, height=40)

# Vector Phosphor Icon
phosphor.database((30, 20), width=14, style=Styles.PrimaryFlat)

# Official GCP Architecture Icon
gcp.compute_engine((70, 20), width=16, style=Styles.PrimaryFlat)
```

### 10.2 Images & Dimage
Embed bitmap/vector images from `_assets/` or manipulate them in memory with `Dimage`:

```drawlib show-code file:images_example.png
from drawlib.canvas import setup
from drawlib.images import Dimage, image
from drawlib.shapes import rectangle
from drawlib.styles import Styles

setup(width=100, height=45)

# Background container
rectangle((50, 22), width=85, height=36, style=Styles.LightFlat)

# 1. Original bitmap image loaded from _rules/_assets/
image((32, 22), width=24, image="_assets/linux.png")

# 2. Image manipulated with Dimage effect (grayscale)
image((68, 22), width=24, image=Dimage("_assets/linux.png").grayscale())
```

### 10.3 Custom Typography & Fonts (`drawlib.fonts`)
Embed custom local TTF/OTF font files with `FontFile` or use universal typography presets:

```drawlib show-code file:fonts_example.png
from drawlib.canvas import setup
from drawlib.fonts import FontFile, FontRoboto
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=100, height=45)

# Background container
rectangle((50, 22), width=85, height=36, style=Styles.LightFlat)

# 1. Built-in universal typography preset
text((50, 29), "Roboto Regular Preset", style=Styles.PrimaryBold.patch(text_font=FontRoboto.ROBOTO_REGULAR, text_size=16))

# 2. Custom local TTF font loaded from _rules/_assets/
avenger_style = Styles.AccentBold.patch(text_font=FontFile("_assets/avenger/regular.ttf"), text_size=18)
text((50, 15), "AVENGER FONT", style=avenger_style)
```

---

## 11. Multi-Frame Animations (`drawlib.anim`)

Drawlib natively supports multi-frame animations in **APNG** (`.png`) and **Animated WebP** (`.webp`) formats.

| Class / Method | Parameters | Description |
| :--- | :--- | :--- |
| `Animation(fps=10.0, loop=0)` | `fps: float = 10.0`, `loop: int = 0` | Initializes animation controller and registers with canvas. |
| `anim.frame(duration=None, clear=True)` | `duration: float \| None = None`, `clear: bool = True` | Context manager defining shapes drawn in a single frame. |
| `anim.add_frame(duration=None, clear=True)` | `duration: float \| None = None`, `clear: bool = True` | Imperative method to capture the current canvas as a frame. |

```python
from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.shapes import circle
from drawlib.styles import Styles

setup(width=100, height=40)
anim = Animation(fps=10.0)

for x in range(15, 86, 10):
    with anim.frame():
        circle((x, 20), radius=6, style=Styles.Primary)

save("motion.png")  # Automatically writes APNG or WebP based on extension
```

---

## 12. Presentation Slides & Stage (`drawlib.slide`)

Drawlib presentation slides operate on a universal **16:9 widescreen stage (1920x1080)** with origin `(0, 0)` at the bottom-left corner.

| Symbol / Model | Description | Example Usage |
| :--- | :--- | :--- |
| `current_slide` | Dynamic slide counter runtime proxy (`index`, `total`, `text`, `format()`). | `text((1800, 50), current_slide.text, style=Styles.MutedSmall)` |
| `BoundingBox` | Dataclass representing rectangular layout bounds `(x, y, width, height)`. | `box = BoundingBox(x=100, y=200, width=800, height=600)` |
| `SlideContext` | Slide execution state container. | Internal slide runtime context |
| `build_slide(...)` | Programmatic slide deck compiler (`input_dir`, `output_dir`, `image_format`). | `build_slide("slide_src/", "slide_html/")` |

```python
from drawlib.canvas import save, setup
from drawlib.slide import current_slide
from drawlib.styles import Styles
from drawlib.text import text

setup(width=120, height=30)
text((60, 15), f"Slide {current_slide.index} of {current_slide.total}", style=Styles.PrimaryBold)
```

---

## 13. Geometry & Coordinate Math (`drawlib.math`)

Helper functions to eliminate manual trigonometry:

| Function | Signature | Returns | Description |
| :--- | :--- | :--- | :--- |
| `get_distance(xy1, xy2)` | `(xy1, xy2) -> float` | Distance `d` | Euclidean distance between two points. |
| `get_angle(xy1, xy2)` | `(xy1, xy2) -> float` | Degrees `0.0 - 360.0` | Direction angle from `xy1` to `xy2`. |
| `get_center_and_size(points)`| `(points) -> tuple[center, size]` | `((cx, cy), (w, h))` | Bounding box center and dimensions from point list. |

---

## 14. Developer Tools (`drawlib.tools`)

Programmatic Python tools for compilation and documentation management:

```python
from drawlib.tools import clear_cache, init_project, scan_broken_links, serve_docs

# Initialize a project scaffold ('site', 'doc', 'slide', 'images')
init_project("site", target="docs")

# Run headless verification or local documentation preview
serve_docs("docs_html", port=8000)

# Validate hyperlinks and assets
broken = scan_broken_links("docs_html")
```

---

## 15. Essential Best Practice Checklist

1. **50%+ Neutral-Grounded Color Discipline (Avoid Rainbow Chaos)**:
   Ground **50% or more of nodes in calm neutral or tinted-neutral cards** (`Styles.Neutral`, `Styles.PrimaryNeutral`, `Styles.SecondaryNeutral`, `Styles.BlueNeutral`, `Styles.TealNeutral`). Reserve saturated hero fills (`Styles.PrimaryFlat`, `Styles.AccentFlat` with `text_style=Styles.WhiteBold`) strictly for 1–2 focal nodes.
2. **Explicit Semantic Coordinate Variables**:
   Always declare semantic coordinate anchors (`gateway_xy`, `db_xy`) and compute horizontal/vertical gaps mathematically (`gap = (width - margins - total_node_width) / (n - 1)`). Avoid hardcoded magic numbers or raw list index lookups (`points[1]`).
3. **PascalCase Design Tokens**:
   Always use `from drawlib.styles import Colors, Styles` and `Styles.PrimaryFlat`. Never lowercase to `styles` or `colors`.
4. **Z-Order Layering Discipline**:
   Always draw background boundaries/containers first, main entity shapes second, connector lines third, and text/badges last.
5. **Perimeter Margins & Right-Edge Protection**:
   Ensure minimum outer margins of **10–15%** around the canvas perimeter so labels and arrowheads are never clipped by canvas borders.
6. **Headless Verification with Coordinate Grid**:
   For terminal/agent workflows, always use headless export:
   ```bash
   uv run drawlib show docs_src/doc.md file_name.png -g -o .drawlib/scratch/preview.png
   ```
