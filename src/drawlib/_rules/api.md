# Drawlib API Reference & Cheat Sheet

Drawlib is a pure-Python library for **"Illustration as Code"** and **"Documentation as Code"**.  
This document serves as the unified, high-speed API index and cheat sheet covering all public modules, classes, drawing primitives, styling tokens, and developer utilities.

---

## 1. Quick Import Cheat Sheet

```python
# 1. Canvas Lifecycle
from drawlib.canvas import canvas, clear, get_dimage, save, setup, show

# 2. Design Tokens & Styling (Always PascalCase!)
from drawlib.styles import Colors, Styles
from drawlib.types import Color, Style
from drawlib.preset_colors import CssColors, DefaultColors, GoogleColors, MonochromeColors

# 3. Drawing Primitives
from drawlib.shapes import (
    arc, arrow, arrow_arc, arrow_l, arrow_polyline, arrow_u, chevron,
    circle, donuts, ellipse, fan, parallelogram, polygon, rectangle,
    regularpolygon, rhombus, shape, star, trapezoid, triangle, wedge,
)
from drawlib.lines import (
    line, line_arc, line_bezier1, line_bezier2, line_curved,
    lines, lines_bezier, lines_curved,
)
from drawlib.text import text, text_vertical

# 4. High-Level Diagrams
from drawlib.diagrams.architecture import ArchitectureDiagram, Edge, Junction, Node, NodeGroup
from drawlib.diagrams.flow import FlowDiagram
from drawlib.diagrams.sequence import SequenceDiagram
from drawlib.diagrams.state_diagram import StateDiagram
from drawlib.diagrams.class_diagram import ClassDiagram
from drawlib.diagrams.er import ERDiagram

# 5. SmartArts Structured Components
from drawlib.smartarts import (
    BoxList, BulletPoints, ChevronProcess, Cycle, GridLayout,
    MindMapNode, Pyramid, SourceCode, Table, TreeNode, bubblespeech,
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

# 9. Developer Tools
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

```python
from drawlib.canvas import setup, save, clear

setup(width=120, height=80)
# ... drawing code ...
save("output.png")
clear()
```

---

## 3. Geometric Shapes Primitives (`drawlib.shapes`)

All shape primitives accept `style: Style | None = None`, `text: str = ""`, and `textstyle: Style | None = None`.  
Coordinates `xy` refer to the **center point** `(cx, cy)` unless otherwise noted.

| Function | Geometric Parameters | Description |
| :--- | :--- | :--- |
| `rectangle(xy, width, height, ...)` | `r: float = 0`, `angle: float = 0` | Rectangle or rounded rectangle (`r > 0`). |
| `circle(xy, radius, ...)` | `radius: float` | Perfect circle centered at `xy`. |
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
| `star(xy, radius_outer, radius_inner, num_vertices, ...)` | `radius_outer, radius_inner, num_vertices: int`, `angle: float = 0` | Multi-pointed star shape. |
| `chevron(xy, width, height, shift=..., ...)` | `width, height`, `shift: float`, `angle: float = 0` | Process chevron arrow shape. |
| `arrow(xy, width, height, ...)` | `width, height`, `angle: float = 0` | Block arrow shape pointing right (or rotated). |
| `arrow_l(xy, width, height, ...)` | `width, height`, `angle: float = 0` | L-shaped bent block arrow. |
| `arrow_u(xy, width, height, ...)` | `width, height`, `angle: float = 0` | U-turn block arrow. |
| `arrow_arc(xy, radius, angle1, angle2, ...)` | `radius, angle1, angle2`, `width: float` | Curved circular block arrow. |
| `arrow_polyline(points, width, ...)` | `points: list[tuple[float, float]]`, `width: float` | Polyline-following block arrow. |
| `shape(points, ...)` | `points: list[tuple[float, float]]` | Custom path shape. |

```python
from drawlib.shapes import rectangle, circle, chevron
from drawlib.styles import Styles

# Center-positioned rectangle with label
rectangle((50, 25), width=40, height=20, style=Styles.primary_flat, text="App Server", textstyle=Styles.white_bold)

# Circle
circle((80, 25), radius=10, style=Styles.accent_flat)
```

---

## 4. Lines & Connectors (`drawlib.lines`)

Lines connect coordinates and support arrowheads: `"-"` (none), `"->"` (forward), `"<-"` (reverse), and `"<->"` (bidirectional).

| Function | Signature | Description |
| :--- | :--- | :--- |
| `line(xy1, xy2, ...)` | `(xy1, xy2, *, arrowhead="-", style=None, text="", textstyle=None)` | Straight line between two points. |
| `lines(points, ...)` | `(points, *, arrowhead="-", style=None, text="", textstyle=None)` | Multi-segment chained polyline (orthogonal routing). |
| `line_curved(xy1, xy2, ...)` | `(xy1, xy2, curve_angle=30, *, arrowhead="-", style=None, ...)` | Smooth circular arc curve between two points. |
| `lines_curved(points, ...)` | `(points, *, arrowhead="-", style=None, ...)` | Continuous curve passing smoothly through points. |
| `line_bezier1(xy1, xy2, cp, ...)` | `(xy1, xy2, cp, *, arrowhead="-", style=None, ...)` | Quadratic Bezier curve with 1 control point `cp`. |
| `line_bezier2(xy1, xy2, cp1, cp2, ...)`| `(xy1, xy2, cp1, cp2, *, arrowhead="-", style=None, ...)` | Cubic Bezier curve with 2 control points `cp1, cp2`. |
| `lines_bezier(points_and_controls, ...)`| `(points_and_controls, *, arrowhead="-", style=None, ...)` | Chained multi-segment Bezier spline. |
| `line_arc(xy, radius, angle1, angle2, ...)`| `(xy, radius, angle1, angle2, *, arrowhead="-", style=None, ...)` | Arc segment line from `angle1` to `angle2`. |

```python
from drawlib.lines import line, lines
from drawlib.styles import Styles

# Straight connector
line((30, 20), (50, 20), arrowhead="->", style=Styles.bold)

# Orthogonal stepped connector via lines()
lines([(30, 20), (40, 20), (40, 35), (60, 35)], arrowhead="->", style=Styles.bold)
```

---

## 5. Text Typography (`drawlib.text`)

Renders single-line or multi-line strings with explicit anchor alignments.

| Function | Parameters | Description |
| :--- | :--- | :--- |
| `text(xy, text, ...)` | `xy: tuple[float, float]`, `text: str`, `angle: float = 0`, `halign: str = "center"`, `valign: str = "center"`, `style: Style \| None = None` | Standard horizontal text string. |
| `text_vertical(xy, text, ...)` | `xy: tuple[float, float]`, `text: str`, `halign: str = "center"`, `valign: str = "center"`, `style: Style \| None = None` | Vertically stacked characters (ideal for East Asian scripts or vertical axis labels). |

- **`halign` Options**: `"left"`, `"center"`, `"right"`
- **`valign` Options**: `"bottom"`, `"center"`, `"top"`

```python
from drawlib.text import text
from drawlib.styles import Styles

# Centered title
text((50, 90), "System Overview", style=Styles.primary_bold)

# Left-aligned note
text((10, 10), "Note: All connections use TLS 1.3", halign="left", valign="bottom", style=Styles.muted_thin)
```

---

## 6. Design Tokens & Styling (`drawlib.styles`, `drawlib.types`)

### 6.1 PascalCase Design Tokens Rule
- **Always import**: `from drawlib.styles import Colors, Styles`
- **Never lowercase** to `styles` or `colors` (prevents shadowing module `drawlib.styles`).

### 6.2 Preset Style Families (`Styles.<color>_<variant>`)
Styles are systematically constructed as `<color>_<variant>`:

- **6 Semantic Colors**: `primary`, `secondary`, `accent`, `support`, `success`, `danger`  
  *(Plus utility shades: `muted`, `light`, `dark`, `white`, `black`, `blue`, `green`, `red`, `purple`, etc.)*
- **10 Structural Variants**:
  - `_flat`: Filled background with subtle outline.
  - `_outline`: Transparent background with colored border.
  - `_thin`: Minimalist thin stroke.
  - `_bold`: High-contrast prominent stroke.
  - `_dashed`: Dashed border for boundaries or speculative stages.
  - `_dotted`: Dotted border for ephemeral or mock objects.
  - `_double`: Double border stroke.
  - `_glow`: Radiant glow effect.
  - `_glass`: Translucent glassmorphism fill.
  - `_neon`: High-intensity vibrant stroke.
- **Typography Styles**: `Styles.white_bold`, `Styles.primary_bold`, `Styles.muted_thin`, etc.

### 6.3 Custom Style and Color Construction

```python
from drawlib.types import Color, Style

# Custom Color (RGBA: values 0-255 for RGB, 0.0-1.0 for Alpha)
my_color = Color(33, 150, 243, 0.9)

# Custom Style Model
custom_style = Style(
    color=my_color,           # Primary shape fill / line color
    lcolor=Color(20, 20, 20), # Line / border color
    lwidth=2.5,               # Border stroke width
    lstyle="dashed",          # "solid", "dashed", "dotted"
    tcolor=Color(255, 255, 255), # Text color
    tsize=14,                 # Text font size
)
```

---

## 7. High-Level Diagrams (`drawlib.diagrams`)

Always prefer high-level diagrams over manually drawing raw rectangles and connectors.

### 7.1 Architecture Diagram (`drawlib.diagrams.architecture`)
Builds cloud topologies, microservice meshes, VPC boundaries, and icon-annotated infrastructure.

```python
from drawlib.canvas import setup, save
from drawlib.diagrams.architecture import ArchitectureDiagram

setup(width=120, height=80)
diag = ArchitectureDiagram()

# 1. Container Boundaries / Groups
vpc = diag.add_group((10, 10), width=100, height=60, label="Production VPC")

# 2. Nodes with Built-in Cloud / Phosphor Icons
client = diag.add_node((25, 40), label="Web Client", icon="phosphor.globe")
gateway = diag.add_node((60, 40), label="API Gateway", icon="gcp.api_gateway")
db = diag.add_node((95, 40), label="Cloud SQL", icon="gcp.cloud_sql")

# 3. Smart Boundary-Clipping Edges
diag.add_edge(client, gateway, label="HTTPS", arrowhead="->")
diag.add_edge(gateway, db, label="TCP 5432", arrowhead="->")

diag.draw()
save("architecture.png")
```

### 7.2 Flow Diagram (`drawlib.diagrams.flow`)
Constructs ISO 5807 flowcharts with decision gates, processes, start/stop terminals, and cross-lane routing.

```python
from drawlib.diagrams.flow import FlowDiagram

flow = FlowDiagram()
start = flow.add_terminal((50, 90), label="Start")
proc = flow.add_process((50, 70), label="Execute Job")
gate = flow.add_decision((50, 45), label="Success?")
end = flow.add_terminal((50, 15), label="End")

flow.add_edge(start, proc, arrowhead="->")
flow.add_edge(proc, gate, arrowhead="->")
flow.add_edge(gate, end, label="Yes", arrowhead="->")
flow.add_edge(gate, proc, label="No (Retry)", routing="orthogonal", arrowhead="->")

flow.draw()
```

### 7.3 Sequence Diagram (`drawlib.diagrams.sequence`)
Generates lifelines, synchronous/asynchronous request-response messages, activations, and note boxes.

```python
from drawlib.diagrams.sequence import SequenceDiagram

seq = SequenceDiagram()
user = seq.add_lifeline("User")
auth = seq.add_lifeline("Auth API")
db = seq.add_lifeline("Database")

seq.add_message(user, auth, label="POST /login", arrowhead="->")
seq.add_message(auth, db, label="SELECT user WHERE ...", arrowhead="->")
seq.add_message(db, auth, label="UserRecord", style="dashed", arrowhead="->")
seq.add_message(auth, user, label="200 OK (JWT)", style="dashed", arrowhead="->")

seq.draw()
```

### 7.4 Other Supported Diagrams
- **State Diagram** (`drawlib.diagrams.state_diagram.StateDiagram`): FSM states, composite states, transitions, guard conditions.
- **Class Diagram** (`drawlib.diagrams.class_diagram.ClassDiagram`): UML classes, methods, inheritance (`--|>`), associations, composition.
- **ER Diagram** (`drawlib.diagrams.er.ERDiagram`): Relational tables, columns, primary keys, foreign keys, Crow's foot cardinality.

---

## 8. SmartArts Structured Components (`drawlib.smartarts`)

High-level automated components for business and technical concepts:

| Component | Anchor | Typical Use Case | Primary Constructor |
| :--- | :--- | :--- | :--- |
| `Table` | Top-Left `(x, y)` | Comparison matrix, data schemas | `Table(xy, data, col_widths, row_heights, headers=...)` |
| `TreeNode` | Top-Left `(x, y)` | Directory trees, org charts | `node = TreeNode("Root", children=[...]); node.draw(xy)` |
| `MindMapNode` | Center `(x, y)` | Radial concept maps | `root = MindMapNode("Topic", children=[...]); root.draw(xy)` |
| `ChevronProcess` | Bottom-Left `(x, y)` | Linear pipelines & phases | `ChevronProcess(stages, xy=..., width=..., height=...)` |
| `Cycle` | Center `(x, y)` | Feedback loops, CI/CD cycles | `Cycle(items, xy=..., radius=...)` |
| `GridLayout` | Bottom-Left `(x, y)` | Component matrices, layer decks | `GridLayout(items, xy=..., width=..., height=..., cols=...)` |
| `Pyramid` | Bottom-Left `(x, y)` | Tiered hierarchy stacks | `Pyramid(levels, xy=..., width=..., height=...)` |
| `BoxList` | Bottom-Left `(x, y)` | Feature callouts, card stacks | `BoxList(items, xy=..., width=..., height=...)` |
| `BulletPoints` | Top-Left `(x, y)` | Bulleted technical notes | `BulletPoints(items, xy=..., width=..., height=...)` |
| `SourceCode` | Bottom-Left `(x, y)` | Highlighted code snippets | `SourceCode(code, xy=..., width=..., height=..., language="python")` |
| `bubblespeech` | Bounding Box `(x, y)` | Callout speech bubbles | `bubblespeech(xy, width, height, tail_xy, text=...)` |

```python
from drawlib.smartarts import ChevronProcess
from drawlib.styles import Styles

ChevronProcess(
    stages=["1. Ingest", "2. Transform", "3. Validate", "4. Export"],
    xy=(10, 30),
    width=100,
    height=20,
    style=Styles.primary_flat,
)
```

---

## 9. Statistical & Project Charts (`drawlib.charts`)

Drawlib charts render directly into the unified vector canvas alongside architectural diagrams:

```python
# Bar Chart
from drawlib.charts.bar import BarChart, Series
chart = BarChart(xy=(10, 10), width=80, height=50, title="Quarterly Revenue")
chart.set_categories(["Q1", "Q2", "Q3", "Q4"])
chart.add_series(Series(name="Cloud", data=[45, 52, 68, 85]))
chart.draw()

# Line Chart
from drawlib.charts.line import LineChart, Series
line_chart = LineChart(xy=(10, 10), width=80, height=50, title="Latency Trends")
line_chart.add_series(Series(name="p99", data=[120, 115, 95, 88, 80]))
line_chart.draw()

# Pie / Donut Chart
from drawlib.charts.pie import PieChart, Slice
pie = PieChart(xy=(50, 50), radius=30, is_donut=True)
pie.add_slice(Slice("Compute", 45))
pie.add_slice(Slice("Storage", 35))
pie.add_slice(Slice("Network", 20))
pie.draw()

# Gantt Project Schedule
from drawlib.charts.gantt import GanttChart, Task
gantt = GanttChart(xy=(10, 10), width=100, height=60, title="Sprint Plan")
gantt.add_task(Task("Design Spec", start="2026-10-01", end="2026-10-05"))
gantt.add_task(Task("Implementation", start="2026-10-06", end="2026-10-20"))
gantt.draw()
```

---

## 10. Icons & Media (`drawlib.icons`, `drawlib.images`, `drawlib.fonts`)

### 10.1 Icons
Drawlib integrates Phosphor vector icons and Google Cloud official architecture icons:

```python
from drawlib.icons import phosphor, gcp

# Vector Phosphor Icon
phosphor.database((30, 40), width=12, height=12, style=Styles.primary_flat)

# Official GCP Architecture Icon
gcp.compute_engine((70, 40), width=14, height=14)
```

### 10.2 Images & Dimage
Embed bitmap/vector images or convert canvases in memory:

```python
from drawlib.images import image, Dimage

# Draw an external image onto canvas
image((50, 50), "assets/logo.png", width=30, height=20, angle=0)
```

---

## 11. Geometry & Coordinate Math (`drawlib.math`)

Helper functions to eliminate manual trigonometry:

| Function | Signature | Returns | Description |
| :--- | :--- | :--- | :--- |
| `get_distance(xy1, xy2)` | `(xy1, xy2) -> float` | Distance `d` | Euclidean distance between two points. |
| `get_angle(xy1, xy2)` | `(xy1, xy2) -> float` | Degrees `0.0 - 360.0` | Direction angle from `xy1` to `xy2`. |
| `get_center_and_size(points)`| `(points) -> tuple[center, size]` | `((cx, cy), (w, h))` | Bounding box center and dimensions from point list. |

---

## 12. Developer Tools (`drawlib.tools`)

Programmatic Python tools for compilation and documentation management:

```python
from drawlib.tools import init_project, serve_docs, scan_broken_links, clear_cache

# Initialize a project scaffold ('site', 'simple', 'pdf', 'image')
init_project("site", target_dir="my_docs")

# Run headless verification or local documentation preview
serve_docs("docs_html", port=8000)

# Validate hyperlinks and assets
broken = scan_broken_links("docs_html")
```

---

## 13. Essential Best Practice Checklist

1. **Explicit Semantic Coordinate Variables**:
   Always declare semantic coordinate anchors (`gateway_xy`, `db_xy`) and compute horizontal/vertical gaps mathematically (`gap = (width - margins - total_node_width) / (n - 1)`). Avoid hardcoded magic numbers or raw list index lookups (`points[1]`).
2. **PascalCase Design Tokens**:
   Always use `from drawlib.styles import Colors, Styles` and `Styles.primary_flat`. Never lowercase to `styles` or `colors`.
3. **Z-Order Layering Discipline**:
   Always draw background boundaries/containers first, main entity shapes second, connector lines third, and text/badges last.
4. **Perimeter Margins & Right-Edge Protection**:
   Ensure minimum outer margins of **10–15%** around the canvas canvas perimeter so labels and arrowheads are never clipped by canvas borders.
5. **Headless Verification with Coordinate Grid**:
   For terminal/agent workflows, always use headless export:
   ```bash
   uv run drawlib show docs_src/doc.md file_name.png -g -o scratch/preview.png
   ```
