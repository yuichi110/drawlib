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
    arc, arrow, arrow_arc, arrow_l, arrow_polyline, arrow_u, brace, bubblespeech,
    checkmark, chevron, circle, clock, cloud, cube, cylinder, document, ellipse,
    explosion, face, fan, forbidden, funnel, gear, heart, lightning, math_symbol,
    moon, parallelogram, pin, plaque, polygon, rectangle, regularpolygon, rhombus,
    ribbon, shape, shield, star, sun, tag, trapezoid, triangle, wedge,
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
    BoxList, BulletPoints, CalendarItem, CardList, ChevronProcess, Cycle,
    DayCalendar, GeoMap, GridLayout, KpiCard, KpiCards, MindMapNode,
    MonthCalendar, Panel, Pyramid, Roadmap, SourceCode, SourceCodeStyles,
    Table, TreeNode, WeekCalendar,
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
from drawlib.icons import (
    ai, aws, azure, cnative, code, data, devops, facility, font_icon, gcp, network,
    original_ai, original_cloud, original_cnative, original_code,
    original_data, original_devops, original_facility, original_network,
    original_security, original_server, phosphor, security, server, workspace,
)
from drawlib.images import Dimage, get_dimage_from_code, image
from drawlib.fonts import Font, FontFile, get_font, list_fonts, list_system_fonts

# 8. Geometry & Math
from drawlib.math import (
    get_angle,
    get_center_and_size,
    get_distance,
    get_intermediate_path_point,
    get_intermediate_path_points,
    get_intermediate_paths,
    get_intermediate_point,
    get_intermediate_points,
)

# 9. Animations (APNG & Animated WebP)
from drawlib.anim import Animation

# 10. Presentation Slides
from drawlib.slide import BoundingBox, SlideContext, build_slide, current_slide, draw_page_number, draw_section_header

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

```drawlib code=show file=canvas_lifecycle.png
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

All 43 shape primitives are organized into **6 semantic categories** (`Basic`, `Polygon`, `Arrow`, `Container`, `Badge`, `Symbol`) and accept `style: Style | None = None` (including `style.angle` for rotation, `style.halign`/`style.valign` for alignment), `text: str = ""`, and `text_style: Style | None = None`.  
Coordinates `xy` refer to the **center point** `(cx, cy)` unless otherwise noted.

| Category | Function | Geometric Parameters | Description |
| :--- | :--- | :--- | :--- |
| **Basic** | `rectangle(xy, width, height, ...)` | `width, height: float`, `hole_ratio: float \| None = None` | Rectangle, rounded rectangle (`style.shape_r`), or hollow rectangular frame (`hole_ratio`). |
| **Basic** | `circle(xy, radius, ...)` | `radius: float`, `hole_ratio: float \| None = None` | Perfect circle or hollow annular ring / donut (`hole_ratio`) centered at `xy`. |
| **Basic** | `ellipse(xy, width, height, ...)` | `width, height: float`, `hole_ratio: float \| None = None` | Ellipse or hollow elliptical ring (`hole_ratio`) centered at `xy`. |
| **Basic** | `wedge(xy, radius, width, angle_start, angle_end, ...)` | `angle_start: float`, `angle_end: float` | Annular sector / wedge slice from `angle_start` to `angle_end`. |
| **Basic** | `fan(xy, radius, angle_start, angle_end, ...)` | `angle_start: float`, `angle_end: float` | Circular pie sector from `angle_start` to `angle_end`. |
| **Basic** | `arc(xy, width, height, angle_start, angle_end, ...)` | `angle_start: float`, `angle_end: float` | Arc segment perimeter. |
| **Polygon** | `triangle(xy, width, height, ...)` | `width, height: float`, `topvertex_x: float \| None = None`, `hole_ratio: float \| None = None` | Triangle defined by bounding box width and height. |
| **Polygon** | `parallelogram(xy, width, height, corner_angle, ...)` | `width, height: float`, `corner_angle: float = 60.0`, `hole_ratio: float \| None = None` | Parallelogram with interior slant angle `corner_angle`. |
| **Polygon** | `trapezoid(xy, height, bottomedge_width, topedge_width, ...)` | `height, bottomedge_width, topedge_width: float`, `hole_ratio: float \| None = None` | Trapezoid with configurable top edge offset. |
| **Polygon** | `rhombus(xy, width, height, ...)` | `width, height: float`, `hole_ratio: float \| None = None` | Diamond / rhombus shape. |
| **Polygon** | `regularpolygon(xy, radius, num_vertex, ...)` | `radius: float`, `num_vertex: int`, `hole_ratio: float \| None = None` | Regular N-sided polygon (pentagon, hexagon, etc.). |
| **Polygon** | `star(xy, num_vertex, radius_ext, radius_int, ...)` | `num_vertex: int`, `radius_ext: float`, `radius_int: float` | Multi-pointed star shape. |
| **Polygon** | `plaque(xy, width, height, ...)` | `variant: str = "concave"` (`"concave"`, `"chamfered"`, `"octagon"`, `"notched"`), `cut_ratio=None` | Corner-cut plaque or ornamental plate centered at `xy`. |
| **Polygon** | `polygon(xys, ...)` | `xys: list[tuple[float, float]]` | Arbitrary closed polygon from coordinate list. |
| **Polygon** | `shape(xy, path_points, ...)` | `path_points: list[...]` | Custom path shape. |
| **Arrow** | `arrow(xy1, xy2, tail_width, head_width, head_length, ...)` | `xy1, xy2, tail_width, head_width, head_length`, `head: str = "->"` | Point-to-point block arrow shape. |
| **Arrow** | `arrow_l(xy, width, height, tail_width, head_width, head_length, ...)` | `width, height, tail_width, head_width, head_length` | L-shaped bent block arrow. |
| **Arrow** | `arrow_u(xy, width, height, tail_width, head_width, head_length, ...)` | `width, height, tail_width, head_width, head_length` | U-turn block arrow. |
| **Arrow** | `arrow_arc(xy, width, height, tail_width, head_width, ...)` | `width, height, tail_width, head_width, head_angle, angle_start, angle_end` | Curved circular block arrow. |
| **Arrow** | `arrow_polyline(xys, tail_width, head_width, head_length, ...)` | `xys: list[tuple[float, float]]`, `tail_width, head_width, head_length` | Polyline-following block arrow. |
| **Arrow** | `chevron(xy, width, height, corner_angle, ...)` | `width, height, corner_angle: float`, `mirror: bool = False` | Process chevron arrow shape. |
| **Container** | `cylinder(xy, width, height, ...)` | `disks: int = 1` | 3D cylinder / multi-disk database stack (`disks > 1`) centered at `xy`. |
| **Container** | `cube(xy, width, height, ...)` | `depth_ratio: float \| None = None` | 3D cube / rectangular block with 3-face automatic shading centered at `xy`. |
| **Container** | `document(xy, width, height, ...)` | `variant: str = "wave"` (`"wave"`, `"folded"`, `"double_wave"`, `"folded_wave"`), `stacked: int = 1`, `wave_ratio=None`, `fold_ratio=None` | Wavy-bottom or folded-corner document / multi-sheet stack centered at `xy`. |
| **Container** | `funnel(xy, width, height, ...)` | `variant: str = "standard"` (`"standard"`, `"3d"`, `"curved"`), `neck_width_ratio=None`, `neck_height_ratio=None` | Filter / conversion funnel centered at `xy`. |
| **Container** | `cloud(xy, width, height, ...)` | `variant: str = "standard"` (`"standard"`, `"flat"`, `"fluffy"`, `"simple"`), `bump_ratio=None` | Cloud node or VPC/SaaS boundary enclosure centered at `xy`. |
| **Container** | `brace(xy, width, height, ...)` | `symbol: str = "{"` (`"{"`, `"}"`, `"["`, `"]"`, `"("`, `")"`), `direction=None`, `tip_ratio=None`, `tip_position_ratio=None` | Curly, square, or round grouping bracket/brace (stroke thickness controlled via `style.line_width`). |
| **Badge** | `bubblespeech(xy, width, height, tail_edge, ...)` | `tail_edge, tail_start_ratio, tail_end_ratio, tail_vertex_xy` | Rectangular speech bubble with pointer tail. |
| **Badge** | `pin(xy, width, height, ...)` | `variant: str = "pointer"` (`"pointer"`, `"teardrop"`, `"pin"`, `"badge"`), `hole_ratio=None` | Callout pointer badge or map pin centered at `xy`. |
| **Badge** | `tag(xy, width, height, ...)` | `variant: str = "angled"` (`"angled"`, `"chamfered"`, `"beveled"`, `"rounded"`), `mirror: bool = False`, `hole_ratio=None` | Perforated label tag or badge centered at `xy`. |
| **Badge** | `ribbon(xy, width, height, ...)` | `variant: str = "down"` (`"down"`, `"up"`, `"flat"`), `tail_width_ratio=None`, `drop_ratio=None` | 3D or flat ribbon banner centered at `xy`. |
| **Badge** | `shield(xy, width, height, ...)` | `variant: str = "classic"` (`"classic"`, `"flat"`, `"heater"`, `"round"`) | Security shield silhouette centered at `xy`. |
| **Badge** | `forbidden(xy, radius, ...)` | `variant: str = "slash"` (`"slash"`, `"backslash"`, `"cross"`, `"no_entry"`), `thickness_ratio=None` | Forbidden / no-entry symbol centered at `xy`. |
| **Badge** | `checkmark(xy, width, height=None, ...)` | `variant: str = "standard"` (`"standard"`, `"circle"`, `"solid_circle"`), `thickness_ratio=None` | Checkmark symbol or badge centered at `xy`. |
| **Badge** | `explosion(xy, width, height, ...)` | `variant: str = "standard"` (`"standard"`, `"irregular"`, `"heavy"`, `"wild"`, `"curved"`, `"comic"`) | Asymmetric explosion / impact burst centered at `xy`. |
| **Symbol** | `face(xy, radius, ...)` | `variant: str = "smile"` | Expressive face (`"smile"`, `"neutral"`, `"sad"`, `"angry"`, `"surprised"`, `"dizzy"`, `"dead"`, `"skull"`, `"devil"`) centered at `xy`. |
| **Symbol** | `clock(xy, radius, ...)` | `variant: str = "standard"` (`"standard"`, `"ticks"`, `"stopwatch"`, `"alarm"`, `"digital"`), `hour=10.0`, `minute=10.0` | Analog or font-free 7-segment digital clock centered at `xy`. |
| **Symbol** | `sun(xy, radius, ...)` | `variant: str = "rays"` (`"rays"`, `"ring"`, `"beams"`), `num_rays: int = 8` | Sun with surrounding rays centered at `xy`. |
| **Symbol** | `moon(xy, width, height, ...)` | `variant: str = "crescent"` (`"crescent"`, `"thin"`, `"waxing"`, `"half"`), `mirror: bool = False` | Crescent or half moon centered at `xy`. |
| **Symbol** | `heart(xy, width, height, ...)` | `variant: str = "standard"` (`"standard"`, `"broken"`) | Heart or broken-heart shape centered at `xy`. |
| **Symbol** | `lightning(xy, width, height, ...)` | `variant: str = "standard"` (`"standard"`, `"flat"`, `"double"`, `"flat_double"`, `"angled"`, `"slanted"`), `mirror: bool = False` | Lightning bolt shape centered at `xy`. |
| **Symbol** | `gear(xy, num_teeth, radius_ext, radius_int, ...)` | `num_teeth: int`, `radius_ext, radius_int: float`, `tooth_ext_ratio=None`, `tooth_int_ratio=None`, `hole_radius=None` | Cogwheel / gear shape with configurable tooth ratios and optional center hole. |
| **Symbol** | `math_symbol(xy, symbol, width, height=None, ...)` | `symbol: str` (`"+"`, `"-"`, `"×"`, `"÷"`, `"="`, `"≠"`), `width: float`, `height=None`, `thickness_ratio=None` | Mathematical operator symbol shape for visual equations (`A + B = C`). |

```drawlib code=show file=shapes_primitives.png
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

```drawlib code=show file=lines_connectors.png
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

Renders single-line or multi-line strings with explicit anchor alignments and rotation via `style`.

| Function | Parameters | Description |
| :--- | :--- | :--- |
| `text(xy, text, ...)` | `(xy, text, *, style)` | Standard horizontal text string. Alignments and rotation controlled via `style.halign`, `style.valign`, and `style.angle`. |
| `text_vertical(xy, text, ...)` | `(xy, text, *, style)` | Vertically stacked characters (ideal for East Asian scripts or vertical axis labels). |

- **`style.halign` Options**: `"left"`, `"center"`, `"right"`
- **`style.valign` Options**: `"bottom"`, `"center"`, `"top"`
- **`style.text_line_spacing`**: `float | None` (line spacing multiplier for multi-line strings `\n`, e.g. `1.6` or `2.0`; defaults to `None` which uses `1.2`)

```drawlib code=show file=text_typography.png
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

```drawlib code=show file=custom_style.png
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

## 7. High-Level Diagrams (`drawlib.diagrams`) & Auto-Layout Graphs (`drawlib.graph`)

Always prefer high-level diagrams over manually drawing raw rectangles and connectors. Every diagram in `drawlib.diagrams` follows the unified component lifecycle:
- **Mutable Element References & Visibility (`show`)**: Registration methods (`add()`, `connect()`, `fork()`, `junction()`, `add_lane()`, `request()`, `reply()`, `note()`, `loop()`/`alt()`/`opt()`/`par()`) accept `show: bool = True` and return the mutable element instance. Mutating `.show = False`, `.style`, `.text_style`, or `.text` / `.label` updates rendering on the next `draw()` without shifting the diagram's layout bounds, swimlanes, or sequence timelines.
- **Automatic Edge & Dangling Junction Hiding**: Hiding a node (`node.show = False`) automatically hides all connected edges (and any dangling `Junction` pass-through stems whose outgoing or incoming branches are all hidden).
- **Anchor Alignment (`align`) & Proportional Scaling (`scale`)**: Every diagram supports `diag.draw(xy=(0.0, 0.0), *, align="bottom_left", scale=1.0)`, where `align="bottom_left"` (default) or `align="center"` anchors the diagram's visual bounding box at `xy`, and `scale` uniformly scales all coordinates, shapes, stroke widths, arrowheads, icons, and font sizes relative to `xy`.

### 7.1 Architecture Diagram (`drawlib.diagrams.architecture`)
Builds cloud topologies, microservice meshes, VPC boundaries, and icon-annotated infrastructure.

```drawlib code=show file=diagram_architecture.png
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
client = diag.add(Node("Web Client", width=18, height=16, icon=PhosphorIcon.GLOBE), (25, 30))
gateway = diag.add(
    Node(
        "API Gateway",
        width=20,
        height=16,
        icon=GcpIcon.CLOUD_API_GATEWAY,
        card_style=Styles.PrimaryFlat,
        text_style=Styles.WhiteBold,
    ),
    (60, 30),
)
db = diag.add(Node("Cloud SQL", width=18, height=16, icon=GcpIcon.CLOUD_SQL, card_style=Styles.SecondaryNeutral), (95, 30))

# 3. Smart Boundary-Clipping Edges
diag.connect(client, gateway, label="HTTPS")
diag.connect(gateway, db, label="TCP 5432")

diag.draw()
```

### 7.2 Flow Diagram (`drawlib.diagrams.flow`)
Constructs ISO 5807 flowcharts with decision gates, processes, start/stop terminals, and cross-lane routing.

```drawlib code=show file=diagram_flow.png
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

```drawlib code=show file=diagram_sequence.png
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
user = seq.add(Participant("User", width=18, height=8))
auth = seq.add(Participant("Auth API", width=18, height=8, card_style=Styles.PrimaryFlat, text_style=Styles.WhiteBold))
db = seq.add(Participant("Database", width=18, height=8, card_style=Styles.SecondaryNeutral))

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

### 7.5 Pure Coordinate Auto-Layout Solvers (`drawlib.graph`)
`drawlib.graph` is a **pure coordinate and layout calculator** (`get_layout()` only—no `.draw()`, `.export_code()`, or styling/label attributes). Use it in a **2-Step Workflow**:
1. **Step 1 (Solve & Inspect)**: Declare topology via `g.node(id, *, width=..., height=...)`, `g.edge(src, dst)`, and `g.cluster(id, nodes=[...], *, padding=4.0, header_height=3.5)`, then call `layout = g.get_layout(width=None, height=None, margin=10.0) -> GraphLayout`. Inspect via `print(layout)` or tweak with `layout.offset(id, dx=..., dy=...)`.
2. **Step 2 (Render)**: Pass `layout["id"].xy`, `layout["id"].local_xy`, `layout["cluster"].bottom_left`, `layout["cluster"].local_bottom_left`, and `edge.points` into `drawlib.diagrams` (`ArchitectureDiagram`, `FlowDiagram`, etc.) or `drawlib.shapes` / `drawlib.lines`.
- **`ArchitectureGraph`**: 2-level macro/micro container packing and 5-zone compass positioning (`pos="left"|"center"|"right"|"top"|"bottom"`, `parent=...`).
- **`LayerGraph`**: Sugiyama hierarchical DAG solver with `.tier(name, nodes, *, layer=...)` stage pinning.
- **`TreeGraph`**: Reingold-Tilford compact tree solver with `.child(parent, child_id, *, width=..., height=...)`.
- **`RadialGraph`**: Concentric hub-and-spoke solver with `.spoke(parent, spoke_id, *, ring=..., width=..., height=...)` and `layout.ring_radii`.
- **`GridGraph`**: 2D matrix solver with `.cell(cell_id, row=..., col=...)`, `.cluster_row(row, cluster_id)`, `.cluster_column(col, cluster_id)`.

---

## 8. SmartArts Structured Components (`drawlib.smartarts`)

High-level automated components for business and technical concepts. Every stateful SmartArt standardizes element registration via `add(..., show=True)` (returning a mutable item instance with `.show`, `.style`, `.text_style`, `.text` evaluated lazily at `draw()` time), anchor alignment via `align` (`"bottom_left"`, `"center"`, or `"top_left"`), and proportional scaling via `draw(..., scale=1.0)` / `draw_flexible(..., scale=1.0)`:

| Component | Default Anchor (`align`) | Typical Use Case | Primary Usage |
| :--- | :--- | :--- | :--- |
| `Table` | Top-Left (`"top_left" \| "bottom_left" \| "center"`) | Comparison matrix, data schemas | `t = Table(...); t.draw(xy, width, height, data, align="top_left", scale=1.0)` |
| `TreeNode` | Top-Left `(x, y)` | Directory trees, org charts | `node = TreeNode("Root", ...); node.add("Child", show=True); node.draw(xy, scale=1.0)` |
| `MindMapNode` | Center `(x, y)` | Radial concept maps | `root = MindMapNode("Topic", ...); root.add("Sub", show=True); root.draw(xy, scale=1.0)` |
| `ChevronProcess` | Bottom-Left (`"bottom_left" \| "center"`) | Linear pipelines & phases | `p = ChevronProcess(...); p.add(..., show=True); p.draw(xy, width, height, align="bottom_left", scale=1.0)` |
| `Cycle` | Center (`"center" \| "bottom_left"`) | Feedback loops, CI/CD cycles | `c = Cycle(...); c.add(..., show=True); c.draw(xy, radius, align="center", scale=1.0)` |
| `GridLayout` | Bottom-Left (`"bottom_left" \| "center"`) | Component matrices, layer decks | `g = GridLayout(...); g.add(..., show=True); g.draw(xy, width, height, margin, align="bottom_left", scale=1.0)` |
| `Pyramid` | Bottom-Left (`"bottom_left" \| "center"`) | Tiered hierarchy stacks | `p = Pyramid(...); p.add(..., show=True); p.draw(xy, width, height, margin, direction="bottom", align="bottom_left", scale=1.0)` |
| `BoxList` | Bottom-Left (`"bottom_left" \| "center"`) | Feature callouts, card stacks | `b = BoxList(...); b.add(..., show=True); b.draw(xy, box_width, box_height, direction="left", align="bottom_left", scale=1.0)` |
| `CardList` | Bottom-Left (`"bottom_left" \| "center"`) | Icon/badge feature & step cards | `c = CardList(...); c.add("Title", "Desc", icon=..., badge_text="1", show=True); c.draw(xy, width, height, align="bottom_left", scale=1.0)` |
| `KpiCards` (`KpiCard`) | Bottom-Left (`"bottom_left" \| "center"`) | KPI metrics, SLA/spec highlight cards | `k = KpiCards(...); k.add("99.99%", "SLA", "Desc", show=True); k.draw(xy, width, height, columns=1, align="bottom_left", scale=1.0)` |
| `Roadmap` | Bottom-Left (`"bottom_left" \| "center"`) | Linear timelines, curved agendas, roadmaps | `r = Roadmap(...); r.add("Phase 1", "Sub", badge_text="Q1", show=True); r.draw(xy, width, height, align="bottom_left", scale=1.0)` |
| `Panel` | Bottom-Left (`"bottom_left" \| "center"`) | Titled container frames with header bands | `p = Panel("Group", style=..., header_style=..., text_style=...); p.draw(xy, width, height, align="bottom_left"); inner_xy, w, h = p.get_content_box(xy, width, height, align="bottom_left", content_align=None)` |
| `MonthCalendar` | Bottom-Left (`"bottom_left" \| "center" \| "top_left"`) | Monthly or multi-week 7-column schedule grids | `m = MonthCalendar(start_date="2026-10-01", ...); m.add("2026-10-10", "2026-10-13", text="Sprint"); m.draw(xy, width, height)` |
| `WeekCalendar` | Bottom-Left (`"bottom_left" \| "center" \| "top_left"`) | Weekly/N-day hourly grids with top All-day field | `w = WeekCalendar(start_date="2026-10-05", start_hour=9, end_hour=18, ...); w.add("2026-10-06", "2026-10-08", text="Freeze"); w.add("2026-10-09 10:00", "2026-10-09 12:00", text="Sync"); w.draw(xy, width, height)` |
| `DayCalendar` | Bottom-Left (`"bottom_left" \| "center" \| "top_left"`) | Single-day schedule (`"vertical"` or `"horizontal"`) | `d = DayCalendar(date="2026-10-10", direction="vertical", ...); d.add("2026-10-10 09:00", "2026-10-10 11:00", text="Deploy"); d.draw(xy, width, height)` |
| `BulletPoints` | Top-Left `(x, y)` | Bulleted technical notes | `b = BulletPoints(...); b.add(..., show=True); b.draw(xy, scale=1.0)` |
| `SourceCode` | Top-Left (`"top_left" \| "bottom_left" \| "center"`) | Highlighted code snippets | `SourceCode.draw(xy, width, code, styles=..., align="top_left", scale=1.0)` |
| `GeoMap` | Bottom-Left (`"bottom_left" \| "center"`) | World, country, city & GeoJSON maps | `m = GeoMap(GeoMap.World.All); m.set_area_styles([...], style); m.draw(xy, width=..., align="bottom_left")` |

```drawlib code=show file=smartarts_chevron.png
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
- **Spatial Overrides, Anchor Alignment & Uniform Scaling**: `chart.draw(xy, *, width=None, height=None, radius=None, align="bottom_left", scale=1.0)` and `chart.draw_legend(xy, text_style, ..., scale=1.0)` allow temporary container resizing, bottom-left or center bounding-box anchoring (`align="bottom_left" | "center"`), and uniform proportional scaling around `xy`.

| Chart Class | Element Factory Methods | `draw()` Spatial Overrides |
| :--- | :--- | :--- |
| `BarChart` | `add_series(..., show=True, draw_ratio=1.0, draw_direction=...) -> Series` | `draw(xy, *, width=None, height=None, align="bottom_left", scale=1.0)` |
| `LineChart` | `add_series(..., show=True, draw_ratio=1.0, draw_direction="left_to_right") -> Series` | `draw(xy, *, width=None, height=None, align="bottom_left", scale=1.0)` |
| `AreaChart` | `add_series(..., show=True, draw_ratio=1.0, draw_direction="left_to_right") -> Series` | `draw(xy, *, width=None, height=None, align="bottom_left", scale=1.0)` |
| `ScatterChart` | `add(..., show=True) -> Point`, `add_series(..., show=True, draw_ratio=1.0, draw_direction="left_to_right") -> Series` | `draw(xy, *, width=None, height=None, align="bottom_left", scale=1.0)` |
| `PieChart` | `add_slice(..., show=True, draw_ratio=1.0, draw_direction="left_to_right") -> Slice` | `draw(xy, *, radius=None, width=None, height=None, align="bottom_left", scale=1.0)` |
| `RadarChart` | `add_series(..., show=True, draw_ratio=1.0, draw_direction="bottom_to_top") -> Series` | `draw(xy, *, radius=None, width=None, height=None, align="bottom_left", scale=1.0)` |
| `GanttChart` | `add_task(..., show=True, draw_ratio=1.0, draw_direction="left_to_right") -> Task`, `add_section`, `add_milestone`, `add_marker`, `add_dependency` | `draw(xy, *, width=None, height=None, align="bottom_left", scale=1.0)` |

```drawlib code=show file=charts_example.png
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
Drawlib integrates Phosphor vector icons alongside vendor and domain icon suites (`gcp`, `aws`, `azure`, `ai`, `cnative`, `code`, `data`, `devops`, `facility`, `network`, `security`, `server`, `workspace`, `original_cloud`, `original_cnative`, `original_code`, `original_data`, `original_devops`, `original_facility`, `original_ai`, `original_network`, `original_security`, `original_server`). `ai` provides 40 official AI, LLM, Agent framework, Protocol, and ML ecosystem icons, `cnative` provides 48 Kubernetes & Cloud Native (CNCF / Observability) icons, `code` provides 72 official Programming Language, Framework, Runtime, API & IDE icons, `data` provides 50 Database & Data Platform icons, `devops` provides 40 official DevOps, CI/CD, IaC, DevSecOps, and Observability icons, `facility` provides 40 official Data Center, IX, Telecom Carrier, and Facility Hardware icons, `network` provides 70 Network icons (48 official CDN, DNS, registrar, proxy, VPN, firewall, SOHO & network vendor logos + 22 Cisco topology icons with `variant="default" | "classic" | "modern"`), `security` provides 60 official Security vendor & OSS icons, `server` provides 82 Server icons (56 official server vendor, chip, SBC, OS, virtualization & storage logos + 26 Dell EMC & VMware hybrid infrastructure icons), `workspace` provides 50 official Workplace, Productivity, Collaboration, CRM/ERP, and Business SaaS icons, while `original_ai`, `original_cnative`, `original_code`, `original_data`, `original_devops`, `original_facility`, `original_network`, `original_security`, and `original_server` provide 2D flat Drawlib pastel counterparts:

```drawlib code=show file=icons_example.png
from drawlib.canvas import setup
from drawlib.icons import gcp, phosphor
from drawlib.styles import Styles

setup(width=100, height=40)

# Vector Phosphor Icon
phosphor.database((20, 20), width=14, style=Styles.PrimaryFlat)

# GCP Architecture Icons (default 3-tone blue & modern 4-color)
gcp.compute_engine((52, 20), width=15, style=Styles.PrimaryFlat, variant="default")
gcp.compute_engine((82, 20), width=15, style=Styles.PrimaryFlat, variant="modern")
```

### 10.2 Images & Dimage
Embed bitmap/vector images from `_assets/` or manipulate them in memory with `Dimage`:

```drawlib code=show file=images_example.png
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

```drawlib code=show file=fonts_example.png
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

| Class / Method / Property | Parameters / Type | Description |
| :--- | :--- | :--- |
| `Animation(fps=10.0, loop=0)` | `fps: float \| None = None`, `frame_rate: float \| None = None`, `loop: int = 0` | Initializes animation controller and registers with canvas. |
| `anim.fps` / `anim.frame_rate` | `float` (read-only property) | Returns the active playback frame rate in frames per second. |
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
| `current_slide` | Dynamic slide counter runtime proxy (`index`, `total`, `text`, `format()`). | `text((1800, 50), current_slide.text, style=Styles.Muted)` |
| `draw_page_number(...)` | Renders a standardized slide page counter badge (`14×3`, `alpha=0.0`). | `draw_page_number()` |
| `draw_section_header(...)` | Renders a full-bleed 16:9 section header slide (`192×108`) with 4 variants (`"split"`, `"centered"`, `"banner"`, `"minimal"`). | `draw_section_header(1, "Intro", "Overview", ["A", "B"], total_sections=4)` |
| `BoundingBox` | Dataclass representing rectangular layout bounds `(x, y, width, height)`. | `box = BoundingBox(x=100, y=200, width=800, height=600)` |
| `SlideContext` | Slide execution state container. | Internal slide runtime context |
| `build_slide(...)` | Programmatic slide deck compiler (`input_dir`, `output_dir`, `image_format`). | `build_slide("slide_src/", "slide_html/")` |

```python
from drawlib.slide import draw_page_number, draw_section_header

# Bottom-right page counter badge (14x3 transparent canvas)
draw_page_number()

# Full-bleed 16:9 section header slide (192x108 canvas)
draw_section_header(2, "Core Engine", "Geometry & Primitives", ["Shapes", "Lines"], total_sections=5, variant="split")
```

---

## 13. Geometry & Coordinate Math (`drawlib.math`)

Helper functions to eliminate manual trigonometry:

| Function | Signature | Returns | Description |
| :--- | :--- | :--- | :--- |
| `get_distance(xy1, xy2)` | `(xy1, xy2) -> float` | Distance `d` | Euclidean distance between two points. |
| `get_angle(xy1, xy2)` | `(xy1, xy2) -> float` | Degrees `0.0 - 360.0` | Direction angle from `xy1` to `xy2`. |
| `get_center_and_size(points)`| `(points) -> tuple[center, size]` | `((cx, cy), (w, h))` | Bounding box center and dimensions from point list. |
| `get_intermediate_point(xy1, xy2)` | `(xy1, xy2) -> tuple[float, float]` | `(mx, my)` | Exact 50% midpoint between `xy1` and `xy2`. |
| `get_intermediate_points(xy1, xy2, ...)` | `(xy1, xy2, num=1, *, include_ends=False) -> list[tuple[float, float]]` | `[(x, y), ...]` | `num` evenly spaced points between `xy1` and `xy2` (or `num + 2` when `include_ends=True`). |
| `get_intermediate_path_point(xys)` | `(xys) -> tuple[float, float]` | `(mx, my)` | 50% arc-length midpoint along a multi-point polyline trajectory `xys`. |
| `get_intermediate_path_points(xys, ...)` | `(xys, num=1, *, include_ends=False) -> list[tuple[float, float]]` | `[(x, y), ...]` | `num` evenly spaced points along the arc length of `xys` (or `num + 2` with endpoints). |
| `get_intermediate_paths(xys, ...)` | `(xys, num=1, *, include_ends=False) -> list[list[tuple[float, float]]]` | `[[p0, ..., pt], ...]` | Progressive prefix sub-paths along `xys` (with full `xys` appended when `include_ends=True`). |

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
