# Drawlib Shapes Overview Guidelines (`lib-shapes-overview`)

Comprehensive architectural manual and cross-cutting reference for `drawlib.shapes`. Drawlib provides **43 geometric and domain shape primitives** organized into **6 sub-topics** (`lib-shapes-basic`, `lib-shapes-polygon`, `lib-shapes-arrow`, `lib-shapes-container`, `lib-shapes-badge`, and `lib-shapes-symbol`).

---

## 1. Sub-Topic Routing Table & 43-Shape Catalog

Query the specific shape sub-topic for detailed function signatures, parameter tables, and code examples:

| Rule Topic | CLI Command | Internal Module | Count | Covered Shape Functions |
| :--- | :--- | :--- | :---: | :--- |
| **`lib-shapes-basic`** | `uv run drawlib rules show lib-shapes-basic` | `_basic.py` | 6 (+`cylinder`) | `rectangle`, `circle`, `ellipse`, `wedge`, `fan`, `arc` (plus `cylinder` reference) |
| **`lib-shapes-polygon`** | `uv run drawlib rules show lib-shapes-polygon` | `_polygon.py` | 9 (+`rectangle`, `bubblespeech`) | `triangle`, `parallelogram`, `trapezoid`, `rhombus`, `regularpolygon`, `star`, `plaque`, `polygon`, `shape` (plus `rectangle`, `bubblespeech` reference) |
| **`lib-shapes-arrow`** | `uv run drawlib rules show lib-shapes-arrow` | `_arrow.py` | 6 | `arrow`, `arrow_polyline`, `arrow_arc`, `arrow_l`, `arrow_u`, `chevron` |
| **`lib-shapes-container`** | `uv run drawlib rules show lib-shapes-container` | `_container.py` | 6 | `cylinder`, `cube`, `document`, `funnel`, `cloud`, `brace` |
| **`lib-shapes-badge`** | `uv run drawlib rules show lib-shapes-badge` | `_badge.py` | 8 | `bubblespeech`, `pin`, `tag`, `ribbon`, `shield`, `forbidden`, `checkmark`, `explosion` |
| **`lib-shapes-symbol`** | `uv run drawlib rules show lib-shapes-symbol` | `_symbol.py` | 8 | `face`, `clock`, `sun`, `moon`, `heart`, `lightning`, `gear`, `math_symbol` |

```python
from drawlib.shapes import (
    # Basic (6)
    arc,
    circle,
    ellipse,
    fan,
    rectangle,
    wedge,
    # Polygon & Custom Path (9)
    parallelogram,
    plaque,
    polygon,
    regularpolygon,
    rhombus,
    shape,
    star,
    trapezoid,
    triangle,
    # Directed Block Arrows (6)
    arrow,
    arrow_arc,
    arrow_l,
    arrow_polyline,
    arrow_u,
    chevron,
    # 3D Containers & Grouping (6)
    brace,
    cloud,
    cube,
    cylinder,
    document,
    funnel,
    # Badges, Callouts & Status Indicators (8)
    bubblespeech,
    checkmark,
    explosion,
    forbidden,
    pin,
    ribbon,
    shield,
    tag,
    # Symbols, Clocks & Operators (8)
    clock,
    face,
    gear,
    heart,
    lightning,
    math_symbol,
    moon,
    sun,
)
```

---

## 2. Universal Coordinate Geometry & Center Anchor `(cx, cy)`

Drawlib operates on a resolution-independent 2D Cartesian coordinate system:
- **Origin `(0, 0)`**: Located at the **bottom-left** corner of the canvas (`X` increases right, `Y` increases up).
- **Angles**: Measured in **degrees counter-clockwise (CCW)** from the positive X-axis (`0°` = right/East, `90°` = up/North).

### 2.1. Anchor Categories Across All 43 Shapes

1. **Center-Anchored Shapes (`xy = (cx, cy)`) — Universal Default**:
   All planar, circular, container, badge, symbol, and box-bounded shapes take `xy=(cx, cy)` as their **geometric center**:
   - **Basic**: `rectangle`, `circle`, `ellipse`, `wedge`, `fan`, `arc`
   - **Polygon**: `triangle`, `parallelogram`, `trapezoid`, `rhombus`, `regularpolygon`, `star`, `plaque`
   - **Arrow (Box-Bounded)**: `chevron`, `arrow_arc`, `arrow_l`, `arrow_u`
   - **Container**: `cylinder`, `cube`, `document`, `funnel`, `cloud`, `brace`
   - **Badge**: `bubblespeech` (center of body box, excluding tail), `pin`, `tag`, `ribbon`, `shield`, `forbidden`, `checkmark`, `explosion`
   - **Symbol**: `face`, `clock`, `sun`, `moon`, `heart`, `lightning`, `gear`, `math_symbol`
2. **Vertex / Point-Vector Shapes (`xy1, xy2` or `xys`)**:
   - `arrow(xy1, xy2, ...)`: Anchored directly from tail start `xy1` to head tip `xy2`.
   - `arrow_polyline(xys, ...)`: Anchored along waypoint sequence `xys`.
   - `polygon(xys, ...)`: Anchored by explicit exterior vertex list `xys`.
3. **Low-Level Path Primitive (`shape`)**:
   - `shape(xy, path_points, *, style, ..., is_default_center=False)`: Defaults to bottom-left bounding-box origin unless `is_default_center=True` is passed.

```text
Center-Anchored (Default):             Point-Vector (arrow / polygon):
       +-------------+                        (x2, y2)
       |      ^      |                           ^
       | <--(cx,cy)->|  xy = (cx, cy)           /
       |      v      |                         /
       +-------------+                    (x1, y1)
```

### 2.2. Alignment Overrides (`halign` & `valign`)

For center-anchored shapes with bounding dimensions $(W, H)$, you can override the anchor point via `style.patch(halign=..., valign=...)`:

| Attribute | Valid Values | Center-Anchored Shift Formula |
| :--- | :--- | :--- |
| `halign` | `"left"`, `"center"` *(default)*, `"right"` | `"left"`: $cx = x + W/2$, `"center"`: $cx = x$, `"right"`: $cx = x - W/2$ |
| `valign` | `"bottom"`, `"center"` *(default)*, `"top"` | `"bottom"`: $cy = y + H/2$, `"center"`: $cy = y$, `"top"`: $cy = y - H/2$ |

*(Note: `arrow`, `arrow_polyline`, and `polygon` compute vertices directly from explicit coordinates and ignore `halign`/`valign`.)*

---

## 3. Required Keyword-Only `*, style: Style` & Corner Rounding (`shape_r`)

Every function in `drawlib.shapes` requires `*, style: Style` as a **mandatory keyword-only argument** (there is no `style=None` fallback). Always pass a semantic preset from `drawlib.styles.Styles` (`Styles.Neutral`, `Styles.PrimaryNeutral`, `Styles.SecondaryNeutral`, `Styles.PrimaryFlat`, etc.):

```python
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles

# 1. Standard preset style (required keyword-only argument)
rectangle((30, 25), width=28, height=16, style=Styles.Neutral, text="Service Card")

# 2. Corner rounding via style.patch(shape_r=...)
# Supported by rectangle, triangle, parallelogram, trapezoid, rhombus, regularpolygon, star, polygon
rectangle(
    (70, 25),
    width=28,
    height=16,
    style=Styles.PrimaryNeutral.patch(shape_r=2.5, shape_line_style="dashed"),
    text="Rounded Card",
)
```

- **Corner Radius (`shape_r`)**: Patch `style.patch(shape_r=2.0)` (or use `Styles.NeutralRounded` / `Styles.PrimaryRounded`) to round polygon vertices with quadratic Bézier arcs. In addition, `bubblespeech(..., r=1.5)`, `tag(..., r=1.0)`, `ribbon(..., r=0.5)`, `shield(..., r=0.5)`, `document(..., r=1.0)`, and `funnel(..., r=0.5)` accept an explicit `r: float = 0.0` keyword parameter.
- **Stroke-Only Shapes (`arc`, `brace`)**: Read stroke attributes (`line_color`, `line_width`, `line_style`) from `style` and ignore `shape_fill_color`.

---

## 4. Compound Cutouts (`hole_ratio` & `holes`), Rotation (`angle`), and Inline Text

### 4.1. Compound Hollow Cutouts (`hole_ratio` & `holes`)
Eight planar and radial shapes cut a true transparent compound path hole through their center without painting an opaque background patch:
- **`hole_ratio: float | None = None`** (`0.0 < hole_ratio < 1.0`): Supported on `rectangle`, `circle`, `ellipse`, `triangle`, `parallelogram`, `trapezoid`, `rhombus`, and `regularpolygon` (plus `gear` which defaults to `hole_ratio=0.35`).
- **`holes: list[list[tuple[float, float]]] | None = None`**: Supported on `polygon` for one or more arbitrary interior polygon cutouts.

### 4.2. Rotation (`style.angle`)
Setting `style=Styles.Primary.patch(angle=30)` rotates any shape counter-clockwise in degrees around its geometric center `(cx, cy)`:
- $$x_{\text{rot}} = (x - C_x)\cos\theta - (y - C_y)\sin\theta + C_x, \quad y_{\text{rot}} = (x - C_x)\sin\theta + (y - C_y)\cos\theta + C_y$$
- Embedded `text` rotates alongside the shape unless overridden by `text_style=Styles.DarkBold.patch(angle=0)`.

### 4.3. Inline Text (`text`, `text_style`, `xy_shift`, `xy_abs_shift`)
39 of the 43 shapes accept `text: str = ""` and `text_style: Style | None = None` *(the 4 multi-segment/curved block arrows `arrow_polyline`, `arrow_arc`, `arrow_l`, and `arrow_u` do not take `text` or `text_style`)*:
- **`text_size` Rule**: Keep in-diagram `text_size >= 10.0` (standard `10.5`–`12.0`).
- **`xy_shift=(dx, dy)`**: Shifts text in the shape's local (rotated) coordinate frame.
- **`xy_abs_shift=(dx, dy)`**: Shifts text along the unrotated canvas axes (ideal for placing labels below `pin`, `face`, `clock`, `gear`, or `shield`).

```drawlib code=fold align=center file=shapes_overview_mechanics.png caption="Core Shape Mechanics: Center Anchor, Corner Radius (shape_r), Hollow Cutout (hole_ratio), Rotation (angle), and Text Shift"
from drawlib.canvas import save, setup
from drawlib.shapes import circle, pin, rectangle, regularpolygon
from drawlib.styles import Styles

setup(width=140, height=46)

# 1. Rounded rectangle card via shape_r
rectangle(
    (22, 23),
    width=28,
    height=20,
    style=Styles.Neutral.patch(shape_r=3.0),
    text="shape_r=3.0",
    text_style=Styles.DarkBold.patch(text_size=10.5),
)

# 2. Hollow ring via hole_ratio
circle(
    (58, 23),
    radius=12,
    hole_ratio=0.55,
    style=Styles.PrimaryNeutral,
    text="55%",
    text_style=Styles.DarkBold.patch(text_size=10.5),
)

# 3. Rotated hexagon with horizontal text override
regularpolygon(
    (92, 23),
    6,
    12.5,
    style=Styles.SecondaryNeutral.patch(angle=15, shape_r=1.2),
    text="angle=15",
    text_style=Styles.DarkBold.patch(text_size=10.0, angle=0),
)

# 4. Badge with xy_abs_shift label below
pin(
    (124, 26),
    width=14,
    height=19,
    style=Styles.PrimaryFlat,
    text="us-east-1",
    text_style=Styles.DarkBold.patch(text_size=10.0, xy_abs_shift=(0, -14)),
)

save()
```
