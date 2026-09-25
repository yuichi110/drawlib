# Drawlib Lines Guidelines: The Exhaustive Developer Reference

Lines are the primary graphical primitives in Drawlib used to model relationships, data streams, network communication, control paths, and physical or logical boundaries. Following Drawlib's core philosophy of **"Illustration as Code"**, all line geometry, routing paths, curvatures, arrowheads, and styles are defined deterministically through readable, reproducible Python code.

This document serves as the comprehensive, production-grade technical manual for human software engineers and AI coding agents. It details exact function signatures, Cartesian coordinate mathematics, control-point mechanics, algorithmic Manhattan routing, label badge masking, and enterprise network topology patterns.

---

## 1. Module Architecture & Core Imports

All line-drawing functionality is implemented in the internal canvas engine (`drawlib._core.l4_canvas._line.CanvasLineFeature`) and re-exported through the public domain module `drawlib.lines`.

### 1.1. Public Domain Functions
```python
from drawlib.lines import (
    line,          # Straight line segment between two coordinates
    line_arc,      # Open arc along an elliptical or circular boundary
    line_bezier1,  # Quadratic Bézier curve with 1 control point
    line_bezier2,  # Cubic Bézier curve with 2 control points
    line_curved,   # Circular/arc-based spline with scalar bend factor
    lines,         # Chained polyline through a sequence of vertices
    lines_bezier,  # Multi-segment path mixing straight and Bézier segments
    lines_curved,  # Chained polyline with automatic corner fillet radius
)
```

### 1.2. Companion Domain Modules
Lines connect architectural elements and require styling, canvas configuration, and textual annotations:
```python
from drawlib.canvas import config, save, clear
from drawlib.colors import Colors
from drawlib.shapes import rectangle, circle
from drawlib.text import text
from drawlib.types import Style
```

### 1.3. Line Connectors vs. Arrow Shapes
Drawlib enforces a strict conceptual separation between line connectors and arrow shapes:
- **Line Connectors (`drawlib.lines`)**: 1-dimensional vector strokes with optional terminal arrowheads (`""`, `"->"`, `"<-"`, `"<->"`). They model dependencies, network connections, RPC calls, data flow, and visual boundaries between components.
- **Geometric Arrow Shapes (`drawlib.shapes.arrow`, `arrow_polyline`, `arrow_l`, `arrow_u`, `arrow_arc`)**: 2-dimensional filled polygon patches with a distinct shaft body, tail width, and triangular head. Use these for prominent stand-alone visual signposts, chevron phases, or large flowchart transitions, but not for connecting fine-grained architectural nodes.

---

## 2. Straight Lines: `line()`

The `line()` function renders a single direct line segment connecting a starting coordinate to an ending coordinate.

### 2.1. Function Signature & Parameters
```python
def line(
    xy1: tuple[float, float],
    xy2: tuple[float, float],
    width: float | None = None,
    arrowhead: Literal["", "->", "<-", "<->"] | str = "",
    style: Style | str | None = None,
) -> None:
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy1` | `tuple[float, float]` | *Required* | Starting coordinate `(x1, y1)` in virtual canvas units. |
| `xy2` | `tuple[float, float]` | *Required* | Ending coordinate `(x2, y2)` in virtual canvas units. |
| `width` | `float \| None` | `None` | Stroke width override in points. If omitted, uses `style.line_width` (default: `1.0`). |
| `arrowhead` | `str` | `""` | Terminal arrowhead style: `""` (none), `"->"` (forward), `"<-"` (reverse), `"<->"` (both). |
| `style` | `Style \| str \| None` | `None` | Named preset string (e.g. `"blue_bold"`, `"gray_dashed"`) or a `Style` object. |

### 2.2. Coordinate Geometry & Orientation Math
When computing line endpoints programmatically:
- **Euclidean Distance (Chord Length)**:
  $$d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2} = \operatorname{math.hypot}(x_2 - x_1, y_2 - y_1)$$
- **Angle of Inclination (Slope Angle)**:
  $$\theta = \operatorname{atan2}(y_2 - y_1, x_2 - x_1) \quad (\text{radians})$$
- **Unit Direction Vector**:
  $$\vec{u} = \left(\frac{x_2 - x_1}{d}, \frac{y_2 - y_1}{d}\right)$$
- **Perpendicular Normal Vector (Rotated $90^\circ$ CCW)**:
  $$\vec{n} = \left(-\frac{y_2 - y_1}{d}, \frac{x_2 - x_1}{d}\right)$$

```text
                     (x2, y2)
                       ▲
                      /
                     /   Slope angle θ
                    /
  (x1, y1) ────────┴──────────► Horizontal Axis
```

### 2.3. Common Architectural Alignments
- **Horizontal Swimlane Dividers**: $y_1 = y_2$. Creates visual tiers separating presentation, business logic, and data layers.
- **Vertical Tier Separators**: $x_1 = x_2$. Delimits functional domains, regions, or VPC subnets.
- **Direct Edge Connectors**: Shortest-distance vectors between adjacent shapes. When connecting rectangular nodes, calculate anchors at the center of the facing edges rather than shape centers to prevent lines from showing underneath transparent fills.

### 2.4. Code Example: Multi-Tier Architectural Dividers & Direct Edges
```drawlib show-code
from drawlib.canvas import config, save
from drawlib.colors import Colors
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.text import text
from drawlib.types import Style

config(width=120, height=60)

# 1. Tier boundary lines
tier_style = styles.bold.patch(line_color=Colors.Gray, line_style="dashed", line_width=1.0)
line((10, 40), (110, 40), style=tier_style)
line((10, 20), (110, 20), style=tier_style)

# Tier labels
text((12, 42), "Presentation Tier", style=styles.primary.patch(text_size=10, text_color=Colors.Gray, text_halign="left"))
text((12, 22), "Application Tier", style=styles.primary.patch(text_size=10, text_color=Colors.Gray, text_halign="left"))
text((12, 2), "Persistence Tier", style=styles.primary.patch(text_size=10, text_color=Colors.Gray, text_halign="left"))

# 2. Service nodes
rectangle((30, 48), width=24, height=10, style=styles.blue_flat, text="Web Client", textstyle=styles.white_bold)
rectangle((30, 28), width=24, height=10, style=styles.green_flat, text="API Gateway", textstyle=styles.white_bold)
rectangle((75, 28), width=24, height=10, style=styles.green_flat, text="Order Service", textstyle=styles.white_bold)
rectangle((75, 8), width=24, height=10, style=styles.purple_flat, text="Postgres DB", textstyle=styles.white_bold)

# 3. Direct straight connections
line((30, 43), (30, 33), arrowhead="->", style=styles.bold)
line((42, 28), (63, 28), arrowhead="->", style=styles.bold)
line((75, 23), (75, 13), arrowhead="->", style=styles.bold)

save()
```

---

## 3. Curved Splines: `line_curved()`

The `line_curved()` function creates a circular arc spline connecting two coordinates. It is the most intuitive method for rendering smooth curves because curvature is controlled by a single scalar factor (`bend`).

### 3.1. Function Signature & Parameters
```python
def line_curved(
    xy1: tuple[float, float],
    xy2: tuple[float, float],
    bend: float = 0,
    width: float | None = None,
    arrowhead: Literal["", "->", "<-", "<->"] | str = "",
    *,
    style: Style,
) -> None:
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy1` | `tuple[float, float]` | *Required* | Starting coordinate `(x1, y1)`. |
| `xy2` | `tuple[float, float]` | *Required* | Ending coordinate `(x2, y2)`. |
| `bend` | `float` | `0` | Curvature factor (typically `-1.0` to `1.0`). `0` is completely straight. |
| `width` | `float \| None` | `None` | Stroke width override in points. |
| `arrowhead` | `str` | `""` | Terminal arrowhead style (`""`, `"->"`, `"<-"`, `"<->"`). |
| `style` | `Style` | *Required* | Line style instance. |

### 3.2. Curvature Mechanics & Direction Rules
Internally, Drawlib configures Matplotlib's `matplotlib.patches.ConnectionStyle.Arc3(rad=bend)`:
- `bend = 0.0`: Completely straight chord.
- `bend > 0.0`: The line bulges **to the left** relative to an observer walking along the vector from `xy1` to `xy2`.
- `bend < 0.0`: The line bulges **to the right** relative to an observer walking along the vector from `xy1` to `xy2`.
- **Aesthetic Scale**:
  - `0.1` to `0.2`: Subtle, elegant curve (ideal for long cross-diagram links).
  - `0.3` to `0.4`: Standard architectural curve (ideal for request-response separation).
  - `0.5` to `0.8`: Pronounced semi-circular arc (ideal for bypassing intermediate components).
  - `> 1.0`: Exaggerated looping spline.

```text
                  bend = +0.3 (Bulges Left)
               ╭───────────────────────╮
               │                       ▼
  xy1 ─────────┴───────────────────────┴──────────► xy2
               │                       ▲
               ╰───────────────────────╯
                  bend = -0.3 (Bulges Right)
```

### 3.3. Bidirectional Request-Response Separation
When two architectural services exchange synchronous requests and responses, straight lines overlap and create visual confusion. `line_curved()` solves this cleanly:
- **Forward Request (`A -> B`)**: `line_curved(pos_a, pos_b, bend=0.25, arrowhead="->", style=styles.bold)`
- **Return Response (`B -> A`)**: `line_curved(pos_b, pos_a, bend=0.25, arrowhead="->", style=styles.bold)`
Because the travel direction is reversed in the second call, both lines bow outward in opposite directions, creating a clean symmetrical ellipse with space for labels in between.

### 3.4. Code Example: Microservice Request-Response Cycle & Bypass Path
```drawlib show-code
from drawlib.canvas import config, save
from drawlib.colors import Colors
from drawlib.lines import line_curved
from drawlib.shapes import circle, rectangle
from drawlib.text import text
from drawlib.types import Style

config(width=120, height=60)

# Nodes
circle((25, 30), radius=10, style=styles.blue_flat, text="Service A", textstyle=styles.white_bold)
rectangle((60, 30), width=18, height=14, style=styles.gray_flat, text="Proxy", textstyle=styles.bold.patch(text_color=Colors.Black))
circle((95, 30), radius=10, style=styles.green_flat, text="Service B", textstyle=styles.white_bold)

# 1. Forward request (A -> B, curving above the Proxy)
line_curved((35, 33), (85, 33), bend=0.35, arrowhead="->", style=styles.blue_bold)
text((60, 48), "HTTPS POST (Direct Bypass)", style=styles.primary.patch(text_size=9, text_color=Colors.Blue))

# 2. Reverse asynchronous callback (B -> A, curving below the Proxy)
line_curved((85, 27), (35, 27), bend=0.35, arrowhead="->", style=styles.green_dashed)
text((60, 12), "gRPC Stream Event (Ack)", style=styles.primary.patch(text_size=9, text_color=Colors.Green))

save()
```

---

## 4. Bézier Curves: `line_bezier1()` & `line_bezier2()`

When circular arcs cannot meet specific boundary or tangency requirements, polynomial Bézier curves provide exact mathematical trajectory control.

### 4.1. Quadratic Bézier Curve: `line_bezier1()`
A quadratic curve uses a single control point `cp` that pulls the curve toward itself like a gravitational anchor.

#### Function Signature & Parameter Order
```python
def line_bezier1(
    xy1: tuple[float, float],
    xy2: tuple[float, float],
    cp: tuple[float, float],
    width: float | None = None,
    arrowhead: Literal["", "->", "<-", "<->"] | str = "",
    *,
    style: Style,
) -> None:
```

> [!IMPORTANT]
> **Positional Argument Ordering**: The positional signature is `(xy1, xy2, cp)`. If arguments are passed positionally without names, the control point is the **third** argument. To prevent accidental bugs, always use explicit keyword arguments:
> `line_bezier1(xy1=(...), cp=(...), xy2=(...), style=styles.bold)`

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy1` | `tuple[float, float]` | *Required* | Starting coordinate `P0`. |
| `xy2` | `tuple[float, float]` | *Required* | Ending coordinate `P1`. |
| `cp` | `tuple[float, float]` | *Required* | Control point `Pc` defining the curve apex and tangency. |
| `width` | `float \| None` | `None` | Stroke width override in points. |
| `arrowhead` | `str` | `""` | Terminal arrowhead style (`""`, `"->"`, `"<-"`, `"<->"`). |
| `style` | `Style` | *Required* | Line style instance. |

#### Mathematical Formulation
For interpolation parameter $t \in [0, 1]$:
$$B(t) = (1-t)^2 P_0 + 2(1-t)t P_c + t^2 P_1$$
- Tangent at start ($t=0$): Collinear with $(P_c - P_0)$.
- Tangent at end ($t=1$): Collinear with $(P_1 - P_c)$.

```text
                  cp (Control Point)
                  ●
                 / \
      Tangent   /   \   Tangent
       Vector  /  .  \   Vector
              / .     \
  xy1 ●──────'         '──────► ● xy2
```

#### Application: Smooth $90^\circ$ Fillet Between Non-Aligned Points
To turn a smooth corner from $(x_1, y_1)$ to $(x_2, y_2)$ where the start segment is horizontal and the end segment is vertical:
$$\text{cp} = (x_2, y_1)$$
The curve leaves $(x_1, y_1)$ perfectly horizontally and arrives at $(x_2, y_2)$ perfectly vertically.

---

### 4.2. Cubic Bézier Curve: `line_bezier2()`
A cubic curve uses two control points `cp1` and `cp2`. This allows the curve to contain an inflection point, enabling smooth S-curves and parallel port connections.

#### Function Signature & Parameter Order
```python
def line_bezier2(
    xy1: tuple[float, float],
    xy2: tuple[float, float],
    cp1: tuple[float, float],
    cp2: tuple[float, float],
    width: float | None = None,
    arrowhead: Literal["", "->", "<-", "<->"] | str = "",
    *,
    style: Style,
) -> None:
```

> [!IMPORTANT]
> **Positional Argument Ordering**: The positional signature is `(xy1, xy2, cp1, cp2)`. Use keyword arguments `line_bezier2(xy1=..., cp1=..., cp2=..., xy2=..., style=styles.bold)` to maintain clear parameter identification.

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy1` | `tuple[float, float]` | *Required* | Starting coordinate `P0`. |
| `xy2` | `tuple[float, float]` | *Required* | Ending coordinate `P1`. |
| `cp1` | `tuple[float, float]` | *Required* | First control point controlling departure tangency. |
| `cp2` | `tuple[float, float]` | *Required* | Second control point controlling arrival tangency. |
| `width` | `float \| None` | `None` | Stroke width override in points. |
| `arrowhead` | `str` | `""` | Terminal arrowhead style (`""`, `"->"`, `"<-"`, `"<->"`). |
| `style` | `Style` | *Required* | Line style instance. |

#### Mathematical Formulation
$$B(t) = (1-t)^3 P_0 + 3(1-t)^2 t P_{c1} + 3(1-t) t^2 P_{c2} + t^3 P_1$$

#### Perfect Horizontal S-Curve Construction Formula
To connect component port $(x_1, y_1)$ to target port $(x_2, y_2)$ with horizontal entry and exit angles:
$$\Delta x = x_2 - x_1$$
$$\text{cp1} = \left(x_1 + \frac{\Delta x}{2}, y_1\right), \quad \text{cp2} = \left(x_2 - \frac{\Delta x}{2}, y_2\right)$$

```text
         cp1                         xy2
          ●───────────────────────────●
         /                           /
        /        Smooth S-Curve     /
       /                           /
  xy1 ●───────────────────────────●
                                 cp2
```

### 4.3. Code Example: ETL Pipeline S-Curves and Rounded Transitions
```drawlib show-code
from drawlib.canvas import config, save
from drawlib.lines import line_bezier1, line_bezier2
from drawlib.shapes import rectangle
from drawlib.types import Style

config(width=120, height=60)

# Pipeline stages
rectangle((15, 45), width=20, height=12, style=styles.blue_flat, text="Ingest", textstyle=styles.white_bold)
rectangle((60, 45), width=20, height=12, style=styles.blue_flat, text="Filter A", textstyle=styles.white_bold)
rectangle((60, 15), width=20, height=12, style=styles.purple_flat, text="Filter B", textstyle=styles.white_bold)
rectangle((105, 30), width=20, height=12, style=styles.green_flat, text="Sink", textstyle=styles.white_bold)

# 1. Quadratic curve: branch down to Filter B
line_bezier1(
    xy1=(25, 45),
    cp=(45, 15),
    xy2=(50, 15),
    arrowhead="->",
    style=styles.purple_bold,
)

# 2. Cubic S-curve: converge Filter B into Sink with horizontal tangents
x1, y1 = 70, 15
x2, y2 = 95, 30
dx = x2 - x1
line_bezier2(
    xy1=(x1, y1),
    cp1=(x1 + dx * 0.5, y1),
    cp2=(x2 - dx * 0.5, y2),
    xy2=(x2, y2),
    arrowhead="->",
    style=styles.green_bold,
)

save()
```

---

## 5. Multi-Point Chained Lines: `lines()`

The `lines()` function takes an ordered list of vertices and connects them in sequence. It is the primary tool for orthogonal (Manhattan) bus routing, multi-segment pipelines, and circuit layouts.

### 5.1. Function Signature & Parameters
```python
def lines(
    xys: list[tuple[float, float]],
    width: float | None = None,
    arrowhead: Literal["", "->", "<-", "<->"] | str = "",
    style: Style | str | None = None,
) -> None:
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xys` | `list[tuple[float, float]]` | *Required* | Sequence of 2 or more coordinates `[(x0, y0), (x1, y1), ...]`. |
| `width` | `float \| None` | `None` | Stroke width override in points. |
| `arrowhead` | `str` | `""` | Arrowhead placed on terminal segment(s). |
| `style` | `Style \| str \| None` | `None` | Named preset or `Style` instance. |

### 5.2. Built-in Optimizations: Sanitization & Collinear Merging
Drawlib's `LineUtil.sanitize_xys()` runs automatically prior to rendering:
1. **Consecutive Duplicate Elimination**: Sequences like `[(10, 10), (10, 10), (20, 20)]` are automatically collapsed to `[(10, 10), (20, 20)]`.
2. **Collinear Redundancy Merging**: Intermediate points that lie along the same straight slope are pruned, reducing matplotlib artist overhead and avoiding rendering seams.

### 5.3. Orthogonal Routing Paradigms (Manhattan Routing)
Orthogonal routing constrains paths to horizontal and vertical lines ($90^\circ$ turns). This is standard in technical system architecture:

#### Pattern A: L-Routing (1 Corner)
Connects $(x_1, y_1)$ to $(x_2, y_2)$ using one right angle:
- **Horizontal First**: `[(x1, y1), (x2, y1), (x2, y2)]`
- **Vertical First**: `[(x1, y1), (x1, y2), (x2, y2)]`

#### Pattern B: Dogleg / Z-Routing (2 Corners)
Connects two offset components across a channel using a midpoint split $x_{\text{mid}}$:
- `[(x1, y1), (x_mid, y1), (x_mid, y2), (x2, y2)]`

#### Pattern C: U-Turn / Bypass Routing (3 Corners)
Routes around an intermediate obstacle:
- `[(x1, y1), (x1, y_clear), (x2, y_clear), (x2, y2)]`

```text
       L-Route (H-First)              Dogleg / Z-Route             U-Turn Bypass
  (x1, y1) ───────┐               (x1, y1) ──┐                   ┌──────────────┐
                  │                          │                   │   Obstacle   │
                  ▼                          └──► (x2, y2)       │   [======]   │
              (x2, y2)                                           └───┬──────┬───┘
                                                                 (x1, y1)  (x2, y2)
```

### 5.4. Code Example: Orthogonal Bus Architecture
```drawlib show-code
from drawlib.canvas import config, save
from drawlib.colors import Colors
from drawlib.lines import line, lines
from drawlib.shapes import rectangle
from drawlib.types import Style

config(width=120, height=60)

# Central message bus spine (horizontal trunk)
line((15, 30), (105, 30), style=styles.bold.patch(line_width=3.0, line_color=Colors.Navy))

# Producer nodes (top tier)
rectangle((25, 48), width=20, height=10, style=styles.blue_flat, text="Sensor A", textstyle=styles.white_bold)
rectangle((55, 48), width=20, height=10, style=styles.blue_flat, text="Sensor B", textstyle=styles.white_bold)
rectangle((85, 48), width=20, height=10, style=styles.blue_flat, text="Sensor C", textstyle=styles.white_bold)

# Consumer nodes (bottom tier)
rectangle((40, 12), width=22, height=10, style=styles.green_flat, text="Analytics", textstyle=styles.white_bold)
rectangle((75, 12), width=22, height=10, style=styles.purple_flat, text="Storage", textstyle=styles.white_bold)

# Vertical bus taps from producers to trunk
lines([(25, 43), (25, 30)], arrowhead="->", style=styles.blue_bold)
lines([(55, 43), (55, 30)], arrowhead="->", style=styles.blue_bold)
lines([(85, 43), (85, 30)], arrowhead="->", style=styles.blue_bold)

# Dogleg taps from trunk to consumers
lines([(40, 30), (40, 17)], arrowhead="->", style=styles.green_bold)
lines([(75, 30), (75, 17)], arrowhead="->", style=styles.purple_bold)

save()
```

---

## 6. Multi-Point Curved Lines: `lines_curved()` & `lines_bezier()`

When polylines require rounded filleted corners or complex parametric curves, Drawlib provides two advanced functions.

### 6.1. Automatic Corner Rounding: `lines_curved()`
The `lines_curved()` function takes an ordinary polyline coordinate list and an additional radius parameter `r`. It automatically replaces every sharp corner with a smooth quadratic fillet.

#### Function Signature & Parameters
```python
def lines_curved(
    xys: list[tuple[float, float]],
    r: float,
    width: float | None = None,
    arrowhead: Literal["", "->", "<-", "<->"] | str = "",
    *,
    style: Style,
) -> None:
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xys` | `list[tuple[float, float]]` | *Required* | Sequence of 3 or more polyline coordinates. |
| `r` | `float` | *Required* | Fillet curvature radius (distance from vertex to start of curve). |
| `width` | `float \| None` | `None` | Stroke width override. |
| `arrowhead` | `str` | `""` | Terminal arrowhead style. |
| `style` | `Style` | *Required* | Line style instance. |

#### Corner Fillet Radius Constraint
At each vertex $P_i$, the rounding algorithm extracts control points at distance $r$ along incoming segment $P_{i-1} P_i$ and outgoing segment $P_i P_{i+1}$.
> [!CAUTION]
> **Radius Size Limit**: The radius `r` **must** be strictly smaller than half the distance between any two consecutive vertices:
> $$r < \frac{1}{2} \min_{i} \|P_{i+1} - P_i\|$$
> If `r` exceeds this threshold, the filleted curves will overlap and cause visual distortion or math errors.

```text
               Vertex P_i
                  ┌─────
                  │  . ◄── r ──► Rounded Fillet
                  │ .            Curve (Radius r)
                  ├─────────────
                 P_{i-1}
```

### 6.2. Arbitrary Mixed Paths: `lines_bezier()`
`lines_bezier()` offers the ultimate degree of path expressiveness. It starts at an initial coordinate `xy` and iterates through a list of `path_points` containing arbitrary mixtures of straight segments, quadratic curves, and cubic curves.

#### Signature & Tuple Structure
```python
def lines_bezier(
    xy: tuple[float, float],
    path_points: list[
        tuple[float, float]
        | tuple[tuple[float, float], tuple[float, float]]
        | tuple[tuple[float, float], tuple[float, float], tuple[float, float]]
    ],
    width: float | None = None,
    arrowhead: Literal["", "->", "<-", "<->"] | str = "",
    *,
    style: Style,
) -> None:
```

The elements of `path_points` determine the segment type dynamically:
1. `(x, y)`: **Straight segment** (`Path.LINETO`) to `(x, y)`.
2. `((cp_x, cp_y), (x, y))`: **Quadratic Bézier segment** (`Path.CURVE3`) to `(x, y)` with control point `(cp_x, cp_y)`.
3. `((cp1_x, cp1_y), (cp2_x, cp2_y), (x, y))`: **Cubic Bézier segment** (`Path.CURVE4`) to `(x, y)` with control points `cp1` and `cp2`.

### 6.3. Code Example: Filleted Circuit Tracks and Mixed Bézier Paths
```drawlib show-code
from drawlib.canvas import config, save
from drawlib.lines import lines_curved, lines_bezier
from drawlib.shapes import circle
from drawlib.types import Style

config(width=120, height=60)

circle((15, 15), radius=5, style=styles.blue_flat, text="IN", textstyle=styles.white_bold)
circle((105, 45), radius=5, style=styles.green_flat, text="OUT", textstyle=styles.white_bold)

# 1. Smoothly rounded Manhattan circuit trace
track_points = [
    (20, 15),
    (40, 15),
    (40, 45),
    (75, 45),
    (75, 25),
    (100, 25),
    (100, 45),
]
lines_curved(track_points, r=6.0, arrowhead="->", style=styles.blue_bold)

# 2. Mixed path: straight run -> cubic S-bend -> straight run
mixed_path = [
    (45, 10),                                       # straight to (45, 10)
    ((60, 10), (60, 35), (75, 35)),                 # cubic S-curve to (75, 35)
    (95, 35),                                       # straight to (95, 35)
]
lines_bezier((20, 10), path_points=mixed_path, arrowhead="->", style=styles.purple_dashed)

save()
```

---

## 7. Circular & Elliptical Arcs: `line_arc()`

The `line_arc()` function renders open curved strokes along the perimeter of an ellipse or circle. It is ideal for feedback loops, retry mechanisms, cyclic workflows, and radial indicators.

### 7.1. Function Signature & Parameters
```python
def line_arc(
    xy: tuple[float, float],
    width: float,
    height: float,
    angle_start: float = 0,
    angle_end: float = 180,
    angle: float = 0,
    linewidth: float | None = None,
    arrowhead: Literal["", "->", "<-", "<->"] | str = "",
    *,
    style: Style,
    ccw: bool = True,
) -> None:
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *Required* | Center coordinate `(cx, cy)` of the ellipse. |
| `width` | `float` | *Required* | Full horizontal diameter ($2 \times R_x$). |
| `height` | `float` | *Required* | Full vertical diameter ($2 \times R_y$). Circular if `width == height`. |
| `angle_start` | `float` | `0` | Starting angle in degrees ($0^\circ$ = positive X-axis). |
| `angle_end` | `float` | `180` | Ending angle in degrees. |
| `angle` | `float` | `0` | Rotation angle of the entire ellipse frame in degrees. |
| `linewidth` | `float \| None` | `None` | Stroke width override in points. *(Note: parameter name is `linewidth`)*. |
| `arrowhead` | `str` | `""` | Terminal arrowhead style (`""`, `"->"`, `"<-"`, `"<->"`). |
| `style` | `Style` | *Required* | Line style instance. |
| `ccw` | `bool` | `True` | Traversal direction: `True` for counter-clockwise, `False` for clockwise. |

### 7.2. Angle Navigation Reference
Angles in Drawlib adhere to standard Cartesian trigonometry:
- $0^\circ$: 3 o'clock (positive X-axis $\rightarrow$)
- $90^\circ$: 12 o'clock (positive Y-axis $\uparrow$)
- $180^\circ$: 9 o'clock (negative X-axis $\leftarrow$)
- $270^\circ$: 6 o'clock (negative Y-axis $\downarrow$)

```text
                     90° (12 o'clock)
                           ▲
                           │
      180° (9 o'clock) ────┼────► 0° (3 o'clock)
                           │
                           ▼
                    270° (6 o'clock)
```

### 7.3. Mathematical Arc Decomposition
Internally, `LineArcHelper` subdivides large angular sweeps into sub-arcs of $\le 90^\circ$ and approximates each segment using cubic Bézier splines (`bezier_ellipse_arc_approximation`). This guarantees high precision without raster distortion.

### 7.4. Code Example: Cyclic Feedback & Self-Loop Retry Arcs
```drawlib show-code
from drawlib.canvas import config, save
from drawlib.lines import line, line_arc
from drawlib.shapes import rectangle
from drawlib.text import text

config(width=100, height=60)

rectangle((30, 30), width=24, height=14, style=styles.blue_flat, text="Processor", textstyle=styles.white_bold)
rectangle((75, 30), width=24, height=14, style=styles.green_flat, text="Consumer", textstyle=styles.white_bold)

# Direct pipeline line
line((42, 30), (63, 30), arrowhead="->", style=styles.bold)

# 1. Self-loop retry arc (Processor retries itself on failure)
line_arc(
    xy=(30, 42),
    width=16,
    height=16,
    angle_start=220,
    angle_end=320,
    linewidth=1.5,
    arrowhead="->",
    style=styles.red_dashed,
    ccw=False,
)
text((30, 53), "Retry (3x)", style=styles.red)

# 2. Large feedback arc (Consumer sends feedback to Processor)
line_arc(
    xy=(52.5, 30),
    width=45,
    height=25,
    angle_start=0,
    angle_end=180,
    linewidth=1.5,
    arrowhead="->",
    style=styles.purple_dashed,
    ccw=False,
)
text((52.5, 12), "Negative ACK / Backpressure", style=styles.purple)

save()
```

---

## 8. Arrowhead System: Heads, Styles, and Scaling

Arrowheads impart semantic directionality to relationships. Drawlib provides flexible controls over arrowhead orientation, scale, and fill appearance.

### 8.1. Logical Arrowhead Types
The `arrowhead` parameter is accepted by all line functions:
- `""` or `"-"`: **No arrowhead** (plain undirected stroke). Use for physical wires, network backbones, undirected associations, or boundary borders.
- `"->"`: **Forward arrowhead** at the ending coordinate. Use for function calls, message delivery, unidirectional data replication, or process flow.
- `"<-"`: **Reverse arrowhead** at the starting coordinate. Use for dependency references ("inherits from", "depends on").
- `"<->"`: **Bidirectional arrowheads** at both endpoints. Use for duplex sockets, synchronous request/response pairs, or symmetric peering.

### 8.2. Arrowhead Styling via `Style`
Arrowheads inherit their color and transparency from the line stroke, but their visual geometry is governed by two dedicated attributes on `Style`:

| Style Property | Type | Default | Visual Effect |
| :--- | :--- | :--- | :--- |
| `line_arrow_head_fill` | `bool` | `False` | `False` renders open "stick" arrowheads (`->`). `True` renders solid filled triangular arrows (`-|>`). |
| `line_arrow_head_scale` | `float` | `20.0` | Controls the physical size of the arrowhead. Larger values create more prominent heads. |

```text
  line_arrow_head_fill=False (Stick)         line_arrow_head_fill=True (Filled Triangle)
  ─────────────────────────►                 ─────────────────────────►
        (Open V-notch)                            (Solid polygon)
```

### 8.3. Tangent Alignment Mechanics
On curved lines (`line_curved`, `line_bezier1`, `line_bezier2`, `line_arc`, `lines_curved`), Drawlib calculates the derivative tangent vector at the exact terminal point. The arrowhead rotates automatically to align seamlessly with the incoming trajectory.

### 8.4. Code Example: Arrowhead Style & Scale Gallery
```drawlib show-code
from drawlib.canvas import config, save
from drawlib.lines import line
from drawlib.text import text
from drawlib.types import Style

config(width=120, height=70)

# 1. Unfilled / Stick arrowheads (default)
text((15, 60), "Stick -> (scale=20)", style=styles.bold)
line((55, 60), (105, 60), arrowhead="->", style=styles.bold.patch(line_arrow_head_fill=False, line_arrow_head_scale=20))

text((15, 50), "Stick <- (scale=20)", style=styles.bold)
line((55, 50), (105, 50), arrowhead="<-", style=styles.bold.patch(line_arrow_head_fill=False, line_arrow_head_scale=20))

text((15, 40), "Stick <-> (scale=20)", style=styles.bold)
line((55, 40), (105, 40), arrowhead="<->", style=styles.bold.patch(line_arrow_head_fill=False, line_arrow_head_scale=20))

# 2. Filled triangular arrowheads
text((15, 30), "Filled -|> (scale=20)", style=styles.bold)
line((55, 30), (105, 30), arrowhead="->", style=styles.bold.patch(line_arrow_head_fill=True, line_arrow_head_scale=20))

text((15, 20), "Filled <|-|> (scale=20)", style=styles.bold)
line((55, 20), (105, 20), arrowhead="<->", style=styles.bold.patch(line_arrow_head_fill=True, line_arrow_head_scale=20))

# 3. Scaling variations
text((15, 10), "Large Scale (scale=35)", style=styles.bold)
line(
    (55, 10),
    (105, 10),
    arrowhead="->",
    style=styles.bold.patch(line_arrow_head_fill=True, line_arrow_head_scale=35, line_width=2.5),
)

save()
```

---

## 9. Line Styling & Presets: `LineStyle` & `Style`

Drawlib provides two ways to style lines: declarative `Style` objects for custom attributes, and concise preset strings for rapid diagram authoring.

### 9.1. Declarative Styling with `Style`
The universal `Style` dataclass supports these line-specific attributes:
```python
from drawlib.types import Style
from drawlib.colors import Colors

custom_style = styles.primary.patch(
    line_color=Colors.Red,        # Stroke color (RGB/RGBA tuple, Colors.*, or hex)
    line_width=2.5,               # Stroke width in points (default: 1.0)
    line_style="dashed",          # Stroke pattern: "solid" | "dashed" | "dotted" | "dashdot"
    line_alpha=0.85,              # Overall opacity [0.0 (transparent) to 1.0 (opaque)]
    line_arrow_head_fill=True,    # Filled arrowhead triangle
    line_arrow_head_scale=24.0,   # Arrowhead size
)
```

### 9.2. Stroke Patterns (`TypeLineStyle`)
The `line_style` attribute accepts four standardized patterns:
- `"solid"` (default): Continuous uninterrupted stroke.
- `"dashed"`: Evenly spaced dash marks.
- `"dotted"`: Sequence of small circular/square dots.
- `"dashdot"`: Alternating long dashes and short dots.

```text
  solid:    ────────────────────────────────────────
  dashed:   ───   ───   ───   ───   ───   ───   ───
  dotted:   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·
  dashdot:  ───  ·  ───  ·  ───  ·  ───  ·  ───  ·  ───
```

### 9.3. Preset String Naming Syntax
Drawlib includes built-in preset strings following the convention:
$$\text{<color>}\_\text{<type>}\_\text{<weight>}$$
- **`<color>`**: `"red"`, `"blue"`, `"green"`, `"gray"`, `"black"`, `"purple"`, etc.
- **`<type>`** (optional): `"solid"` (default), `"dashed"`.
- **`<weight>`** (optional): `"light"` (half width), `"bold"` (double width).

Examples of valid presets:
- `"blue"`: Solid blue line of regular width.
- `"red_dashed"`: Dashed red line of regular width.
- `"green_bold"`: Solid green line of double thickness.
- `"gray_light"`: Solid subtle gray line for grids and boundaries.
- `"bold"`: Standard black line of double thickness.

### 9.4. Semantic Conventions for Software Architecture Lines
Aligning visual stroke properties with architectural meanings makes diagrams instantly intuitive:

| Line Style | Visual Pattern | Architectural Meaning | Practical Examples |
| :--- | :--- | :--- | :--- |
| **Solid Normal** | `──────` | Synchronous Request/Response | REST API, gRPC unary calls, SQL queries. |
| **Solid Bold** | `━━━━━━` | Primary Data / High-Throughput | Kafka log streams, data warehouse ingest, replication bus. |
| **Dashed Normal**| `- - - -` | Asynchronous Event / Decoupled | Webhooks, pub/sub notifications, message queue jobs. |
| **Dotted Normal**| `······` | Control Plane / Health / Telemetry | Prometheus metrics, Kubernetes heartbeats, DNS discovery. |
| **Dashdot Bold** | `─·─·─·` | Cross-Boundary Network Transit | VPC peering, transit gateways, DMZ firewalls, Internet hops. |

### 9.5. Code Example: Multi-Protocol Network Styling
```drawlib show-code
from drawlib.canvas import config, save
from drawlib.colors import Colors
from drawlib.lines import line
from drawlib.text import text
from drawlib.types import Style

config(width=120, height=55)

protocols = [
    ("Synchronous REST API", Colors.Blue, "solid", 1.5, "->"),
    ("Asynchronous Event Queue", Colors.Purple, "dashed", 1.5, "->"),
    ("Telemetry / Health Check", Colors.Gray, "dotted", 1.0, "->"),
    ("Cross-VPC Transit Tunnel", Colors.Red, "dashdot", 2.0, "<->"),
]

for i, (label, color_name, pattern, thickness, arrow) in enumerate(protocols):
    y = 45 - i * 11
    text((10, y), label, style=styles.primary.patch(text_size=11, text_halign="left"))
    line(
        (70, y),
        (110, y),
        arrowhead=arrow,
        style=styles.bold.patch(line_color=color_name, line_style=pattern, line_width=thickness),
    )

save()
```

---

## 10. Line Labels & Annotations

Because Drawlib strictly decouples lines (strokes) from text (typography), annotations are added using `drawlib.text.text()`. Positioning and masking these labels properly ensures professional readability.

### 10.1. Midpoint Calculation Math
To place a label at the center of a line segment:
- **Midpoint Formula**:
  $$x_{\text{mid}} = \frac{x_1 + x_2}{2}, \quad y_{\text{mid}} = \frac{y_1 + y_2}{2}$$
- **Perpendicular Offset Formula**:
  To elevate text slightly above an angled line:
  $$d = \sqrt{\Delta x^2 + \Delta y^2}, \quad \text{offset} = h$$
  $$x_{\text{label}} = x_{\text{mid}} - h \cdot \frac{\Delta y}{d}, \quad y_{\text{label}} = y_{\text{mid}} + h \cdot \frac{\Delta x}{d}$$

### 10.2. Text Masking via Background Boxes
Placing text directly on top of a line stroke can make the letters illegible. Drawlib's `Style` provides background bounding box controls that automatically mask the line underneath:
```python
badge_style = styles.primary.patch(
    text_size=10,
    text_color=Colors.Navy,
    text_bg_fill_color=Colors.White,    # Masks the underlying line stroke
    text_bg_line_color=Colors.Gray,     # Optional border around the label badge
    text_bg_line_width=0.5,             # Subtle border width
    text_halign="center",
    text_valign="center",
)
```

### 10.3. Rotating Text Along Angled Lines
To align text with the slope of an angled connector:
$$\theta = \operatorname{atan2}(y_2 - y_1, x_2 - x_1) \times \frac{180}{\pi}$$
> [!TIP]
> **Human Readability Flip**: If $\theta > 90^\circ$ or $\theta < -90^\circ$, normal text rotation renders upside-down. Always normalize the angle:
> ```python
> if theta > 90:
>     theta -= 180
> elif theta < -90:
>     theta += 180
> ```

### 10.4. Code Example: Reusable Labeled Connector with Badges
```python
from drawlib.canvas import config, save
from drawlib.colors import Colors
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.text import text
from drawlib.types import Style

def draw_labeled_line(
    xy1: tuple[float, float],
    xy2: tuple[float, float],
    label: str,
    *,
    line_style: Style,
    arrowhead: str = "->",
    color: tuple[int, int, int] | str = Colors.Blue,
) -> None:
    """Draw a line with an automatically centered, masked text badge."""
    line(xy1, xy2, arrowhead=arrowhead, style=line_style)
    mx = (xy1[0] + xy2[0]) / 2
    my = (xy1[1] + xy2[1]) / 2
    badge = styles.primary.patch(
        text_size=9,
        text_color=color,
        text_bg_fill_color=Colors.White,
        text_bg_line_color=color,
        text_bg_line_width=0.5,
        text_halign="center",
        text_valign="center",
    )
    text((mx, my), label, style=badge)

config(width=120, height=50)
rectangle((20, 25), width=24, height=14, style=styles.blue_flat, text="Client", textstyle=styles.white_bold)
rectangle((100, 25), width=24, height=14, style=styles.green_flat, text="Service", textstyle=styles.white_bold)

draw_labeled_line((32, 29), (88, 29), "POST /api/checkout", arrowhead="->", line_style=styles.blue_bold, color=Colors.Blue)
draw_labeled_line((88, 21), (32, 21), "201 Created (45ms)", arrowhead="->", line_style=styles.green_dashed, color=Colors.Green)

save()
```

---

## 11. Complex Connection Patterns & Network Topologies

Real-world technical architecture diagrams demand sophisticated routing patterns to prevent visual clutter, crossings, and overlapping strokes.

### 11.1. Pattern 1: API Gateway Fan-Out (Dogleg Routing)
Route horizontally to an alignment trunk, then step vertically into each target's horizontal entry lane:
```drawlib show-code
from drawlib.canvas import config, save
from drawlib.lines import lines
from drawlib.shapes import rectangle

config(width=120, height=50)
rectangle((20, 25), width=20, height=16, style=styles.navy_flat, text="API Gateway", textstyle=styles.white_bold)

for name, y in [("Users", 40), ("Orders", 25), ("Payments", 10)]:
    rectangle((95, y), width=22, height=10, style=styles.green_flat, text=name, textstyle=styles.white_bold)
    lines([(30, 25), (55, 25), (55, y), (84, y)], arrowhead="->", style=styles.bold)

save()
```

### 11.2. Pattern 2: Circuit Routing & High-Density Parallel Bus Trunks
Parallel lines maintain uniform separation and turn corners in synchronized lockstep:
```drawlib show-code
from drawlib.canvas import config, save
from drawlib.lines import lines_curved

config(width=120, height=50)
pitch, base_r = 2.0, 4.0

for i in range(4):
    offset = i * pitch
    path = [(15, 12 + offset), (45 + offset, 12 + offset), (45 + offset, 38 - offset), (105, 38 - offset)]
    lines_curved(path, r=base_r + offset, arrowhead="->", style=styles.blue_bold)

save()
```

### 11.3. Pattern 3: Event-Driven Publish/Subscribe Backbone
A central message queue or event streaming log acts as an orthogonal trunk:
```drawlib show-code
from drawlib.canvas import config, save
from drawlib.lines import lines
from drawlib.shapes import rectangle

config(width=120, height=60)
rectangle((60, 30), width=90, height=8, style=styles.purple_flat, text="Kafka Event Log", textstyle=styles.white_bold)

for name, x in [("Auth Svc", 30), ("Order Svc", 60), ("Payment Svc", 90)]:
    rectangle((x, 50), width=20, height=10, style=styles.blue_flat, text=name, textstyle=styles.white_bold)
    lines([(x, 45), (x, 34)], arrowhead="->", style=styles.blue_bold)

for name, x in [("Email Worker", 40), ("Audit Log", 80)]:
    rectangle((x, 10), width=22, height=10, style=styles.green_flat, text=name, textstyle=styles.white_bold)
    lines([(x, 26), (x, 15)], arrowhead="->", style=styles.green_bold)

save()
```

### 11.4. Pattern 4: Cross-VPC Peering & Boundary Traversals
Security zones and perimeter firewalls traversed by distinct cross-boundary links:
```drawlib show-code
from drawlib.canvas import config, save
from drawlib.colors import Colors
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.text import text
from drawlib.types import Style

config(width=120, height=50)
line((60, 5), (60, 45), style=styles.bold.patch(line_color=Colors.Red, line_style="dashed", line_width=1.5))
text((58, 43), "Public DMZ", style=styles.primary.patch(text_size=9, text_halign="right", text_color=Colors.Gray))
text((62, 43), "Private Subnet", style=styles.primary.patch(text_size=9, text_halign="left", text_color=Colors.Gray))

rectangle((25, 25), width=22, height=12, style=styles.blue_flat, text="Reverse Proxy", textstyle=styles.white_bold)
rectangle((95, 25), width=22, height=12, style=styles.green_flat, text="App Backend", textstyle=styles.white_bold)
line(
    (36, 25),
    (84, 25),
    arrowhead="->",
    style=styles.bold.patch(line_color=Colors.Red, line_style="dashdot", line_width=2.0),
)
text((60, 28), "mTLS (Port 8443)", style=styles.primary.patch(text_size=9, text_bg_fill_color=Colors.White, text_bg_line_width=0.5))

save()
```

---

## 12. Algorithmic Routing Patterns & Obstacle Avoidance

When writing automated diagram generators or AI agents that render diagrams dynamically, hardcoding coordinates is brittle. Use these programmatic routing algorithms to compute collision-free paths.

### 12.1. Manhattan & Dogleg Router Functions
```python
def route_manhattan(
    start: tuple[float, float],
    end: tuple[float, float],
    horizontal_first: bool = True,
) -> list[tuple[float, float]]:
    x1, y1 = start
    x2, y2 = end
    return [(x1, y1), (x2, y1), (x2, y2)] if horizontal_first else [(x1, y1), (x1, y2), (x2, y2)]

def route_dogleg(
    start: tuple[float, float],
    end: tuple[float, float],
    split_ratio: float = 0.5,
    orientation: str = "horizontal",
) -> list[tuple[float, float]]:
    x1, y1, x2, y2 = start[0], start[1], end[0], end[1]
    if orientation == "horizontal":
        x_mid = x1 + (x2 - x1) * split_ratio
        return [(x1, y1), (x_mid, y1), (x_mid, y2), (x2, y2)]
    y_mid = y1 + (y2 - y1) * split_ratio
    return [(x1, y1), (x1, y_mid), (x2, y_mid), (x2, y2)]
```

### 12.2. Obstacle Avoidance Router
Routes around a rectangular obstacle by choosing a clear perimeter channel:
```python
def route_around_obstacle(
    start: tuple[float, float],
    end: tuple[float, float],
    box_center: tuple[float, float],
    box_height: float,
    padding: float = 5.0,
    prefer_top: bool = True,
) -> list[tuple[float, float]]:
    x1, y1 = start
    x2, y2 = end
    bx, by = box_center
    clear_y = by + (box_height / 2) + padding if prefer_top else by - (box_height / 2) - padding
    return [(x1, y1), (x1, clear_y), (x2, clear_y), (x2, y2)]
```

### 12.3. Code Example: Algorithmic Obstacle Avoidance in Action
```drawlib show-code
from drawlib.canvas import config, save
from drawlib.lines import lines_curved
from drawlib.shapes import rectangle
from drawlib.text import text

config(width=120, height=50)

start, end, obs = (15, 25), (105, 25), (60, 25)
rectangle(start, width=16, height=12, style=styles.blue_flat, text="Client", textstyle=styles.white_bold)
rectangle(obs, width=30, height=18, style=styles.red_flat, text="Firewall / WAF", textstyle=styles.white_bold)
rectangle(end, width=16, height=12, style=styles.green_flat, text="Server", textstyle=styles.white_bold)

bypass = [(23, 25), (38, 25), (38, 40), (82, 40), (82, 25), (97, 25)]
lines_curved(bypass, r=4.0, arrowhead="->", style=styles.blue_bold)
text((60, 44), "Authorized Bypass Channel", style=styles.blue)

save()
```

---

## 13. Developer Cheatsheet & Troubleshooting Guide

### 13.1. Line Function Selection Matrix

| Function | Curvature Control | Points Handled | Primary Use Cases |
| :--- | :--- | :--- | :--- |
| `line` | None (Straight) | Exactly 2 | Direct node-to-node connectors, boundaries, axes. |
| `line_curved` | `bend` scalar (`-1.0` to `1.0`) | Exactly 2 | Bidirectional separation, gentle arcs, bypass routes. |
| `line_bezier1` | 1 Control Point (`cp`) | Exactly 2 + 1 CP | Rounded 90° transitions, single-inflection trajectories. |
| `line_bezier2` | 2 Control Points (`cp1`, `cp2`) | Exactly 2 + 2 CPs | Smooth horizontal S-curves, flow transitions. |
| `lines` | Sharp Orthogonal Corners | 2 to $N$ | Manhattan routing, parallel data buses, pipelines. |
| `lines_curved` | Rounded Corner Radius `r` | 3 to $N$ | Metro map lines, PCB traces, rounded architecture paths. |
| `lines_bezier` | Mixed (Straight + B1 + B2) | 1 start + $N$ segments | Intricate custom vector trajectories, mixed pipelines. |
| `line_arc` | Elliptical Sweep (`angle_start`/`end`)| Center + Dimensions | Feedback loops, retry rings, cyclic lifecycle diagrams. |

### 13.2. Common Pitfalls & Solutions

#### Pitfall 1: Swapped Control Point in `line_bezier1` Positional Call
- **Error**: Calling `line_bezier1((10, 10), (50, 50), (90, 10))` expecting `(50, 50)` to be the control point.
- **Why**: The positional signature is `(xy1, xy2, cp)`. In positional calls, the second argument is `xy2`!
- **Fix**: Always use keyword arguments: `line_bezier1(xy1=(10, 10), cp=(50, 50), xy2=(90, 10))`.

#### Pitfall 2: Using `width` Instead of `linewidth` in `line_arc`
- **Error**: `line_arc((50, 50), width=40, height=40, width=2.0)` throws a Python `TypeError: duplicate keyword argument 'width'`.
- **Why**: In `line_arc()`, `width` is the horizontal diameter of the ellipse. The stroke thickness parameter is named `linewidth`.
- **Fix**: `line_arc((50, 50), width=40, height=40, linewidth=2.0)`.

#### Pitfall 3: Corner Radius `r` Exceeding Segment Length in `lines_curved`
- **Error**: Distorted loopbacks or rendering artifacts at polyline corners.
- **Why**: Parameter `r` is greater than half the distance between consecutive points.
- **Fix**: Ensure $r < \frac{1}{2} \min \|P_{i+1} - P_i\|$. For tight $10$-unit grids, use $r \le 4.0$.

#### Pitfall 4: Inverted Curvature in Reverse Directions with `line_curved`
- **Error**: Both forward and return lines curve to the same side and collide.
- **Why**: `bend > 0` curves to the left of the travel vector. When reversing $(xy1, xy2)$ to $(xy2, xy1)$, "left" flips $180^\circ$.
- **Fix**: Keep `bend` positive on both lines if you invert `xy1` and `xy2`, or keep `xy1` and `xy2` identical and invert `bend` from positive to negative.

#### Pitfall 5: Passing Unsupported Arrowhead Strings
- **Error**: Passing `arrowhead="<--"` or `arrowhead="==>"` throws a validation error.
- **Why**: `TypeArrowHead` is strictly validated to `["", "->", "<-", "<->"]`.
- **Fix**: Use only the four supported literal strings. For filled heads, configure `Style(line_arrow_head_fill=True)`.

### 13.3. Best Practices Checklist for AI Agents & Developers
1. **Always Set Canvas Bounds First**: Begin every drawing script with `config(width=..., height=...)` to establish the virtual coordinate scale.
2. **Prefer Declarative Overrides**: Use `Style(line_width=..., line_style=...)` to maintain centralized design coherence instead of scattered ad-hoc overrides.
3. **Mask Labels Over Connectors**: Always supply `text_bg_fill_color=Colors.White` (or the canvas background color) when labeling lines to avoid messy stroke collisions.
4. **Enforce Orthogonal Clarity**: In enterprise software architectures, prioritize `lines()` or `lines_curved()` over diagonal lines to preserve visual cleanliness.
5. **Reserve `line_curved` for Direct Bidirectional Pairs**: Use circular splines where two entities exchange requests and responses, or where an edge must bypass an obstacle.

