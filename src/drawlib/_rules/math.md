# Drawlib Math Guidelines

Drawlib provides geometric and mathematical calculation utilities to streamline coordinate positioning, angle derivations, distance measurements, and bounding box computations for technical diagrams.

---

## 1. Imports & Core Architecture

All public math and geometry functions are imported from `drawlib.math`:

```python
from drawlib.math import (
    get_angle,            # Calculate angle in degrees from point A to point B
    get_center_and_size,  # Compute center coordinates and bounding box dimensions
    get_distance,         # Compute Euclidean distance between two points
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

```python
from drawlib.math import get_angle
from drawlib.lines import line
from drawlib.text import text

p1 = (30, 20)
p2 = (90, 60)

# Draw slanted connection
line(p1, p2, arrowhead="->", style=styles.bold)

# Calculate angle and midpoint
angle = get_angle(p1, p2)
midpoint = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2 + 3)

# Rotate text along the line
text(midpoint, "Data Sync (60°)", angle=angle, style=styles.bold)
```

---

## 4. Practical Code Examples

### 4.1. Automated Cluster Boundary via `get_center_and_size()`

```drawlib fold-code 600px center caption:"Automated Grouping Box with get_center_and_size()"
from drawlib.canvas import config, save
from drawlib.math import get_center_and_size
from drawlib.shapes import circle, rectangle
from drawlib.text import text

config(width=140, height=70)

# Define service node positions
nodes = [(40, 45), (70, 50), (100, 40), (60, 25)]

# Calculate bounding box of all nodes
(cx, cy), (bw, bh) = get_center_and_size(nodes)

# Draw encompassing cluster background with padding (+24 width, +20 height)
rectangle(
    (cx, cy),
    width=bw + 28,
    height=bh + 22,
    r=4,
    style=styles.blue_solid,
    text="Kubernetes Worker Nodes",
    textstyle=styles.bold,
)

# Render nodes on top
for i, (x, y) in enumerate(nodes, start=1):
    circle((x, y), radius=7, style=styles.blue_flat, text=f"Pod {i}", textstyle=styles.white_bold)

save()
```

### 4.2. Radial Network Hub with Calculated Angles & Distances

```drawlib fold-code 600px center caption:"Radial Topology with Math Angle & Distance Computations"
import math
from drawlib.canvas import config, save
from drawlib.lines import line
from drawlib.math import get_angle, get_distance
from drawlib.shapes import circle
from drawlib.text import text

config(width=120, height=80)

hub = (60, 40)
radius = 26
num_clients = 5

# Central Hub
circle(hub, radius=12, style=styles.purple_flat, text="Master", textstyle=styles.white_bold)

# Surrounding Worker Nodes
for i in range(num_clients):
    angle_rad = 2 * math.pi * i / num_clients
    node_xy = (hub[0] + radius * math.cos(angle_rad), hub[1] + radius * math.sin(angle_rad))
    
    # Calculate connection angle and distance
    dist = get_distance(hub, node_xy)
    angle_deg = get_angle(hub, node_xy)
    
    line(hub, node_xy, style=styles.bold)
    circle(node_xy, radius=6, style=styles.blue_flat, text=f"N{i+1}", textstyle=styles.white_bold)

save()
```

---

## 5. Related Rules
- Lines & Arrowhead Routing: `uv run drawlib rules show lines`
- Shapes Drawing Primitives: `uv run drawlib rules show shapes`
- SmartArts Radial Mindmap: `uv run drawlib rules show smartarts`
