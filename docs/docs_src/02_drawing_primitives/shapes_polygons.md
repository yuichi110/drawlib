# Polygons & Custom Paths

In addition to basic rectangles and circles, `drawlib.shapes` provides planar polygons (`parallelogram`, `rhombus`, `trapezoid`, `triangle`), radial equilateral shapes (`regularpolygon`, `star`), arbitrary coordinate polygons (`polygon`), and a low-level Bézier vector path builder (`shape`).

---

## 1. Overview of Polygons & Custom Paths

```drawlib fold-code 650px center file:shapes_polygons_overview.png caption:"Overview of Polygons and Custom Path Primitives"
from drawlib.canvas import save, setup
from drawlib.shapes import (
    parallelogram,
    polygon,
    regularpolygon,
    rhombus,
    shape,
    star,
    trapezoid,
    triangle,
)
from drawlib.styles import Styles

setup(width=130, height=62)

# Row 1: Planar Quadrilaterals & Triangle
parallelogram((20, 44), width=22, height=14, corner_angle=68, style=Styles.Neutral, text="parallel")
rhombus(
    (52, 44),
    width=24,
    height=16,
    style=Styles.PrimaryFlat,
    text="rhombus",
    text_style=Styles.WhiteBold,
)
trapezoid(
    (84, 44),
    height=14,
    bottomedge_width=24,
    topedge_width=14,
    style=Styles.SecondaryNeutral,
    text="trapezoid",
)
triangle((114, 44), width=20, height=15, style=Styles.Neutral, text="tri")

# Row 2: Regular Polygons, Stars, Polygon & Custom Shape
regularpolygon((20, 16), num_vertex=6, radius=10, style=Styles.SecondaryNeutral, text="hexagon")
star((52, 16), num_vertex=5, radius_ext=11, radius_int=5.5, style=Styles.Neutral, text="star")
polygon(
    [(73, 9), (91, 9), (96, 16), (91, 23), (73, 23)],
    style=Styles.Neutral.patch(shape_r=1.5),
    text="polygon",
)
shape(
    (114, 16),
    path_points=[(0, 6), (0, 18), (11, 22), (22, 18), (22, 6), (11, 0)],
    style=Styles.PrimaryNeutral,
    text="shape",
)

save()
```

---

## 2. Planar Quadrilaterals & Triangles

All planar quadrilateral and triangle primitives support corner rounding via `style.patch(shape_r=...)` (either a uniform `float` or a per-vertex tuple: 4-tuple for `parallelogram`, `rhombus`, and `trapezoid`; 3-tuple for `triangle`) and rotation via `style.patch(angle=...)`:

| Function | Signature & Key Geometric Arguments | Typical Use Cases |
| :--- | :--- | :--- |
| **`parallelogram`** | `parallelogram(xy, width, height, corner_angle=60.0, *, style, text="", text_style=None)` | Flowchart I/O blocks, data streams (`corner_angle` in $(0^\circ, 90^\circ)$; `shape_r`: `float` or 4-tuple). |
| **`rhombus`** | `rhombus(xy, width, height, *, style, text="", text_style=None)` | Flowchart decision diamonds, conditional gateways (`shape_r`: `float` or 4-tuple). |
| **`trapezoid`** | `trapezoid(xy, height, bottomedge_width, topedge_width, topedge_x=None, *, style, text="", text_style=None)` | Funnels, neural network pooling layers (`topedge_x=None` centers the top edge symmetrically; `shape_r`: `float` or 4-tuple). |
| **`triangle`** | `triangle(xy, width, height, topvertex_x=None, *, style, text="", text_style=None)` | Warning badges, tree apexes, right-angled ramps (`topvertex_x=None` defaults to `width / 2`; `shape_r`: `float` or 3-tuple). |

```drawlib show-code 640px center file:shapes_polygons_planar.png caption:"Parallelogram, Rhombus, Trapezoid, and Triangle"
from drawlib.canvas import save, setup
from drawlib.shapes import parallelogram, rhombus, trapezoid, triangle
from drawlib.styles import Styles

setup(width=130, height=45)

# 1. Parallelogram (I/O Stream)
parallelogram(
    (20, 22.5),
    width=24,
    height=16,
    corner_angle=70,
    style=Styles.Neutral,
    text="Input I/O",
)

# 2. Rhombus (Decision Gate with rounded vertices)
rhombus(
    (54, 22.5),
    width=28,
    height=20,
    style=Styles.PrimaryFlat.patch(shape_r=1.5),
    text="Valid?",
    text_style=Styles.WhiteBold,
)

# 3. Symmetric Trapezoid (Pooling / Funnel Layer)
trapezoid(
    (88, 22.5),
    height=16,
    bottomedge_width=26,
    topedge_width=14,
    style=Styles.SecondaryNeutral,
    text="Pool",
)

# 4. Asymmetric Triangle (topvertex_x shifts apex horizontally)
triangle(
    (116, 22.5),
    width=18,
    height=16,
    topvertex_x=4,
    style=Styles.Neutral,
    text="Skew",
    text_style=Styles.Dark.patch(xy_shift=(-1.5, -2.5)),
)

save()
```

---

## 3. Regular Polygons & Stars (`regularpolygon`, `star`)

- **`regularpolygon(xy, num_vertex, radius, *, style, text="", text_style=None)`**: Draws an equilateral $N$-sided polygon circumscribed inside `radius`. Set `style.patch(shape_r=...)` (a scalar `float` or a `num_vertex`-tuple of per-vertex radii) to round vertices, or `style.patch(angle=...)` to rotate.
- **`star(xy, num_vertex, radius_ext, radius_int, *, style, text="", text_style=None)`**: Draws a symmetric $N$-pointed star alternating between outer peak radius `radius_ext` and inner valley radius `radius_int` (`radius_ext > radius_int`). Also supports corner rounding via `style.patch(shape_r=...)` (either a uniform `float` or a `(2 * num_vertex)`-tuple of alternating outer/inner vertex radii).

```drawlib show-code 640px center file:shapes_polygons_regular_and_star.png caption:"Regular Polygons and Stars with Optional Corner Rounding"
from drawlib.canvas import save, setup
from drawlib.shapes import regularpolygon, star
from drawlib.styles import Styles

setup(width=125, height=45)

# 1. Pentagon (num_vertex=5)
regularpolygon(
    (20, 22.5),
    num_vertex=5,
    radius=12,
    style=Styles.Neutral,
    text="N=5",
)

# 2. Rounded Hexagon Pod (num_vertex=6, shape_r=2)
regularpolygon(
    (52, 22.5),
    num_vertex=6,
    radius=12,
    style=Styles.PrimaryFlat.patch(shape_r=2),
    text="Pod",
    text_style=Styles.WhiteBold,
)

# 3. 5-Point Star (radius_ext=13, radius_int=6)
star(
    (84, 22.5),
    num_vertex=5,
    radius_ext=13,
    radius_int=6,
    style=Styles.SecondaryNeutral,
    text="Star",
)

# 4. Rounded 8-Point Seal Badge (shape_r=1.2)
star(
    (110, 22.5),
    num_vertex=8,
    radius_ext=12,
    radius_int=8.5,
    style=Styles.Neutral.patch(shape_r=1.2),
    text="Seal",
)

save()
```

---

## 4. Arbitrary Vertex Polygons (`polygon`)

`polygon(xys, *, style, text="", text_style=None)` constructs a closed polygon directly from a list of canvas vertex coordinates `xys=[(x1, y1), (x2, y2), ...]`.

- **Corner Rounding (`style.shape_r`)**: Pass a single float to round all vertices equally, or a tuple of radii `(r1, r2, ..., rN)` matching `len(xys)` to round individual vertices selectively.
- **Centroid Label**: Embedded `text` is automatically placed at the bounding-box center of `xys`.

```drawlib show-code 600px center file:shapes_polygons_custom_polygon.png caption:"Custom Coordinate Polygons with Uniform and Per-Vertex Rounding"
from drawlib.canvas import save, setup
from drawlib.shapes import polygon
from drawlib.styles import Styles

setup(width=115, height=45)

# 1. Irregular network zone with uniform corner rounding
polygon(
    xys=[(10, 10), (14, 34), (44, 36), (50, 14), (28, 8)],
    style=Styles.Neutral.patch(shape_r=3),
    text="Subnet Zone A",
)

# 2. Custom tag card with per-vertex radii (sharp tip on right)
polygon(
    xys=[(62, 10), (62, 35), (92, 35), (105, 22.5), (92, 10)],
    style=Styles.PrimaryFlat.patch(shape_r=(3, 3, 2, 0, 2)),
    text="Pipeline Tag",
    text_style=Styles.WhiteBold,
)

save()
```

---

## 5. Custom Vector & Bézier Path Builder (`shape`)

For custom icons, shields, waves, or irregular components that need relative positioning, rotation, and Bézier curves, use `shape()`:

```python
shape(
    xy: tuple[float, float],
    path_points: list[...],
    *,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
    is_default_center: bool = False,
)
```

`path_points` defines a closed vector path in local coordinates, which Drawlib automatically aligns and rotates around `xy` according to `style`:
- **Line Vertex**: `(x, y)` adds a straight line segment.
- **Quadratic Bézier Segment**: `((cp_x, cp_y), (end_x, end_y))` curves toward control point `cp` before ending at `end`.
- **Cubic Bézier Segment**: `((cp1_x, cp1_y), (cp2_x, cp2_y), (end_x, end_y))` uses two control points for smooth S-curves and waves.
- **`is_default_center`**: Controls fallback alignment when `style.halign` or `style.valign` is `None`. All preset `Styles.*` explicitly set `halign="center", valign="center"`, centering the path's bounding box at `xy`. When using a raw `Style()` with `halign=None, valign=None`, `is_default_center=False` (default) anchors the bounding box's bottom-left corner at `xy`, whereas `is_default_center=True` centers the bounding box at `xy`.

```drawlib show-code 600px center file:shapes_polygons_custom_shape.png caption:"Custom Vector Shapes Using Straight and Cubic Bézier Path Points"
from drawlib.canvas import save, setup
from drawlib.shapes import shape
from drawlib.styles import Styles

setup(width=115, height=48)

# 1. Custom Shield Badge (Quadratic Bézier curved bottom)
shape(
    xy=(32, 24),
    path_points=[
        (0, 14),
        (0, 28),
        (14, 32),
        (28, 28),
        (28, 14),
        ((28, 4), (14, 0)),
        ((0, 4), (0, 14)),
    ],
    style=Styles.PrimaryFlat,
    text="Shield",
    text_style=Styles.WhiteBold,
)

# 2. Document Card with Wavy Bottom Edge (Cubic Bézier)
shape(
    xy=(80, 24),
    path_points=[
        (0, 4),
        (0, 30),
        (36, 30),
        (36, 4),
        ((24, 12), (12, -4), (0, 4)),
    ],
    style=Styles.Neutral,
    text="Custom Wave\nDocument",
)

save()
```
