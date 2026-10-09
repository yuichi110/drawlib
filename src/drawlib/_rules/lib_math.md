# Drawlib Math Guidelines

Drawlib provides geometric and mathematical calculation utilities to streamline coordinate positioning, angle derivations, distance measurements, and bounding box computations for technical diagrams.

---

## 1. Imports & Core Architecture

All public math and geometry functions are imported from `drawlib.math`:

```python
from drawlib.math import (
    get_angle,                     # Calculate angle in degrees from point A to point B
    get_center_and_size,           # Compute center coordinates and bounding box dimensions
    get_distance,                  # Compute Euclidean distance between two points
    get_intermediate_path_point,   # Compute 50% arc-length midpoint along a polyline path
    get_intermediate_path_points,  # Compute evenly spaced points along a polyline path
    get_intermediate_paths,        # Compute progressive partial sub-paths along a polyline
    get_intermediate_point,        # Compute the 50% midpoint between two points
    get_intermediate_points,       # Compute evenly spaced points along a segment
)
```

---

## 2. Function Specifications

### 2.1. `get_angle()`
Calculates the counter-clockwise angle in degrees from point `xy1` to point `xy2`.

```python
get_angle(
    xy1: tuple[float, float],
    xy2: tuple[float, float],
) -> float
```

- **Reference Line**: 0° points horizontally along the positive X-axis (East).
- **Return Range**: `[0.0, 360.0)`.
  - Point directly to the right: `0.0°`
  - Point directly above: `90.0°`
  - Point directly to the left: `180.0°`
  - Point directly below: `270.0°`
- **Primary Use Case**: Aligning text labels or rotating directional chevrons parallel to slanted connection lines.

### 2.2. `get_distance()`
Calculates the Euclidean distance $\sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$ between two points.

```python
get_distance(
    xy1: tuple[float, float],
    xy2: tuple[float, float],
) -> float
```

- **Primary Use Case**: Determining connection line lengths, radii for radial layouts, or collision thresholds.

### 2.3. `get_center_and_size()`
Computes the geometric midpoint and outer bounding box dimensions for an arbitrary collection of coordinates.

```python
get_center_and_size(
    xys: list[tuple[float, float]],
) -> tuple[tuple[float, float], tuple[float, float]]
```

- **Returns**: A nested tuple: `((center_x, center_y), (width, height))`.
- **Primary Use Case**: Enclosing multiple microservice nodes or cluster components inside an automated background container rectangle with dynamic padding.

### 2.4. `get_intermediate_point()` & `get_intermediate_points()`
Computes evenly spaced coordinates along the linear segment from `xy1` to `xy2`:

```python
get_intermediate_point(
    xy1: tuple[float, float],
    xy2: tuple[float, float],
) -> tuple[float, float]

get_intermediate_points(
    xy1: tuple[float, float],
    xy2: tuple[float, float],
    num: int = 1,
    *,
    include_ends: bool = False,
) -> list[tuple[float, float]]
```

- **`get_intermediate_point(xy1, xy2)`**: Returns the exact 50% midpoint `(mx, my)`.
- **`get_intermediate_points(xy1, xy2, num=1, *, include_ends=False)`**: Divides the segment into `num + 1` equal intervals and returns the `num` interior points (or `num + 2` points including `xy1` and `xy2` when `include_ends=True`).
- **Primary Use Case**: Animating moving packets or progressively extending block arrows (`arrow(xy1, pt, ...)`) and lines across frames.

### 2.5. `get_intermediate_path_point()`, `get_intermediate_path_points()` & `get_intermediate_paths()`
Computes trajectory-aware intermediate points and progressive prefix sub-paths along a multi-point polyline `xys` (such as L-shaped or U-shaped routes):

```python
get_intermediate_path_point(
    xys: list[tuple[float, float]],
) -> tuple[float, float]

get_intermediate_path_points(
    xys: list[tuple[float, float]],
    num: int = 1,
    *,
    include_ends: bool = False,
) -> list[tuple[float, float]]

get_intermediate_paths(
    xys: list[tuple[float, float]],
    num: int = 1,
    *,
    include_ends: bool = False,
) -> list[list[tuple[float, float]]]
```

- **`get_intermediate_path_point(xys)`**: Returns the coordinate at 50% of the total arc length along `xys` (e.g. the center of the bottom bar of a U-shaped path).
- **`get_intermediate_path_points(xys, num=1, *, include_ends=False)`**: Returns `num` evenly spaced `(x, y)` coordinates along the trajectory of `xys` (or `num + 2` points with `include_ends=True`).
- **`get_intermediate_paths(xys, num=1, *, include_ends=False)`**: Returns `num` progressive partial coordinate lists `[(x0, y0), ..., (xt, yt)]` starting at `xys[0]`, passing through all corners reached so far, and ending at the step's tip (plus the full `xys` at the end when `include_ends=True`). Ideal for growing `lines()`, `lines_curved()`, or `arrow_polyline()` along L/U trajectories.

---

## 3. Common Geometric Patterns & Math Recipes

### 3.1. Radial / Circular Node Distribution
To position $N$ nodes evenly around a central hub:

```python
import math

center_x, center_y = 70.0, 45.0
radius = 30.0
total_nodes = 6

node_points = []
for i in range(total_nodes):
    # Angle in radians
    theta = 2 * math.pi * i / total_nodes
    nx = center_x + radius * math.cos(theta)
    ny = center_y + radius * math.sin(theta)
    node_points.append((nx, ny))
```

### 3.2. Slanted Line Text Annotation
Align text perfectly parallel to a connecting line between points `p1` and `p2`:

```drawlib show-code 600px center file:math_slanted_line_text.png caption:"Slanted Line Annotation with get_angle()"
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.math import get_angle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=120, height=80)

p1 = (30, 20)
p2 = (90, 60)

# Draw slanted connection
line(p1, p2, arrow_head="->", style=Styles.DarkBold)

# Calculate angle and midpoint
angle = get_angle(p1, p2)
midpoint = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2 + 4)

# Rotate text along the line
text(midpoint, f"Data Sync ({angle:.1f}°)", style=Styles.DarkBold.patch(angle=angle))

save()
```

---

## 4. Practical Code Examples

### 4.1. Automated Cluster Boundary via `get_center_and_size()`

```drawlib fold-code 600px center caption:"Automated Grouping Box with get_center_and_size()"
from drawlib.canvas import save, setup
from drawlib.math import get_center_and_size
from drawlib.shapes import circle, rectangle
from drawlib.text import text
from drawlib.styles import Styles

setup(width=140, height=75)

# Define service node positions
nodes = [(40, 42), (70, 48), (100, 38), (60, 22)]

# Calculate bounding box of all nodes
(cx, cy), (bw, bh) = get_center_and_size(nodes)
box_w, box_h = bw + 32, bh + 26

# Draw encompassing cluster background
rectangle(
    (cx, cy),
    width=box_w,
    height=box_h,
    style=Styles.MutedDashed.patch(shape_r=4),
)
text((cx, cy + box_h / 2 - 4), "Kubernetes Worker Nodes", style=Styles.SecondaryBold)

# Render nodes: 1 hero leader, remaining calm neutral pods
for i, (x, y) in enumerate(nodes, start=1):
    style = Styles.PrimaryFlat if i == 1 else Styles.Neutral
    text_style = Styles.WhiteBold if i == 1 else Styles.DarkBold
    circle((x, y), radius=7, style=style, text=f"Pod {i}", text_style=text_style)

save()
```

### 4.2. Radial Network Hub with Calculated Angles & Distances

```drawlib fold-code 600px center caption:"Radial Topology with Math Angle & Distance Computations"
import math
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.math import get_angle, get_distance
from drawlib.shapes import circle
from drawlib.text import text
from drawlib.styles import Styles

setup(width=120, height=80)

hub = (60, 40)
radius = 26
num_clients = 5

# Central Hub (radius=12, PrimaryFlat hero)
circle(hub, radius=12, style=Styles.PrimaryFlat, text="Leader", text_style=Styles.WhiteBold)

# Surrounding Worker Nodes (radius=6, SecondaryNeutral)
for i in range(num_clients):
    angle_rad = 2 * math.pi * i / num_clients
    node_xy = (hub[0] + radius * math.cos(angle_rad), hub[1] + radius * math.sin(angle_rad))
    
    # Calculate connection angle and distance
    dist = get_distance(hub, node_xy)
    angle_deg = get_angle(hub, node_xy)
    
    # Offset connection endpoints to shape boundaries rather than shape centers
    hub_edge = (hub[0] + 13 * math.cos(angle_rad), hub[1] + 13 * math.sin(angle_rad))
    node_edge = (node_xy[0] - 7 * math.cos(angle_rad), node_xy[1] - 7 * math.sin(angle_rad))
    line(hub_edge, node_edge, arrow_head="->", style=Styles.DarkBold)
    
    # Label line distance
    label_xy = ((hub_edge[0] + node_edge[0]) / 2, (hub_edge[1] + node_edge[1]) / 2 + 2)
    rot_angle = angle_deg if angle_deg < 180 else angle_deg - 180
    text(label_xy, f"{dist:.0f}u", style=Styles.Dark.patch(text_size=7, angle=rot_angle))
    
    circle(node_xy, radius=6, style=Styles.SecondaryNeutral, text=f"N{i+1}", text_style=Styles.DarkBold)

save()
```

---

## 5. Related Rules
- Lines & Arrowhead Routing: `uv run drawlib rules show lib-lines`
- Shapes Drawing Primitives: `uv run drawlib rules show lib-shapes`
- SmartArts Radial Mindmap: `uv run drawlib rules show lib-smartarts`
