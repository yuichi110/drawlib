# Drawlib Polygon Shapes Guidelines (`lib-shapes-polygon`)

API specification and geometric rules for planar polygons and custom vector path primitives in `drawlib._core.l4_canvas._shapes._polygon` (`triangle`, `parallelogram`, `trapezoid`, `rhombus`, `regularpolygon`, `star`, `plaque`, `polygon`, `shape`), plus `rectangle` and `bubblespeech` references. See `lib-shapes-overview` for universal coordinate and styling rules.

---

## 1. Summary of Polygon & Path Primitives

> **Coordinate Anchor Rule**: All planar shapes (`rectangle`, `triangle`, `parallelogram`, `trapezoid`, `rhombus`, `regularpolygon`, `star`, `plaque`, and `bubblespeech`) are **Center-Anchored at `xy = (cx, cy)`**. `polygon` takes explicit vertices `xys`, and only low-level `shape` defaults to `is_default_center=False` (bottom-left) unless `is_default_center=True` is passed.

| Function | Positional Args | Keyword-Only Geometry Args | `hole_ratio` / `holes` | `shape_r` |
| :--- | :--- | :--- | :---: | :---: |
| **`rectangle`** | `xy, width, height` | `hole_ratio=None` | `hole_ratio` | Yes |
| **`triangle`** | `xy, width, height, topvertex_x=None` | `hole_ratio=None` | `hole_ratio` | Yes |
| **`parallelogram`** | `xy, width, height, corner_angle` *(required)* | `hole_ratio=None` | `hole_ratio` | Yes |
| **`trapezoid`** | `xy, height, bottomedge_width, topedge_width, topedge_x=None` | `hole_ratio=None` | `hole_ratio` | Yes |
| **`rhombus`** | `xy, width, height` | `hole_ratio=None` | `hole_ratio` | Yes |
| **`regularpolygon`** | `xy, num_vertex, radius` *(`num_vertex` 2nd, `radius` 3rd)* | `hole_ratio=None` | `hole_ratio` | Yes |
| **`star`** | `xy, num_vertex, radius_ext, radius_int` | — | No | Yes |
| **`plaque`** | `xy, width, height` | `variant="concave", cut_ratio=None` | No | Via `cut_ratio` |
| **`polygon`** | `xys` | `holes=None` | `holes` | Yes |
| **`bubblespeech`** | `xy, width, height, tail_edge, tail_start_ratio, tail_vertex_xy, tail_end_ratio` | `r=0.0` *(in `_badge.py`)* | No | `r` param |
| **`shape`** | `xy, path_points` | `is_default_center=False` | No | Manual |

---

## 2. Bounded Planar Polygons (`rectangle`, `triangle`, `parallelogram`, `trapezoid`, `rhombus`)

All five shapes below are **Center-Anchored at `xy = (cx, cy)`**, support corner rounding via `style.patch(shape_r=...)`, and support compound hollow cutouts via `hole_ratio: float | None = None` (`0.0 < hole_ratio < 1.0`).

### 2.1. `rectangle`
*(Defined in `_basic.py`; see also `lib-shapes-basic`.)*
```python
def rectangle(
    xy: tuple[float, float],
    width: float,
    height: float,
    *,
    hole_ratio: float | None = None,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None: ...
```

### 2.2. `triangle`
Draws an isosceles, right, or skewed triangle centered at `xy`.

```python
def triangle(
    xy: tuple[float, float],
    width: float,
    height: float,
    topvertex_x: float | None = None,
    *,
    hole_ratio: float | None = None,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None: ...
```
- `topvertex_x`: Horizontal offset of the top apex from the left edge (`0` = left-aligned right triangle, `width / 2` = symmetric isosceles default, `width` = right-aligned right triangle).

### 2.3. `parallelogram`
Draws a slanted four-sided parallelogram centered at `xy` (classic flowchart Data / I/O symbol).

```python
def parallelogram(
    xy: tuple[float, float],
    width: float,
    height: float,
    corner_angle: float,
    *,
    hole_ratio: float | None = None,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None: ...
```
- **Required `corner_angle`**: Interior bottom-left angle in degrees (`0 < corner_angle < 180`, e.g. `70` or `75`). Has **no default value** and must be passed explicitly.

### 2.4. `trapezoid`
Draws a symmetric or skewed four-sided trapezoid centered at `xy` (load balancers, mux/demux, stage funnels).

```python
def trapezoid(
    xy: tuple[float, float],
    height: float,
    bottomedge_width: float,
    topedge_width: float,
    topedge_x: float | None = None,
    *,
    hole_ratio: float | None = None,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None: ...
```
- **Positional Order**: Note that `height` is the **2nd** argument, followed by `bottomedge_width` (3rd) and `topedge_width` (4rd).
- `topedge_x`: Optional horizontal shift of the top edge from the left origin. Defaults to `(bottomedge_width - topedge_width) / 2` (symmetric trapezoid).

### 2.5. `rhombus`
Draws a diamond shape with vertices at the 4 midpoints of the `(width, height)` bounding box centered at `xy` (flowchart decision gateway).

```python
def rhombus(
    xy: tuple[float, float],
    width: float,
    height: float,
    *,
    hole_ratio: float | None = None,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None: ...
```

```drawlib code=fold align=center file=shapes_polygon_planar.png caption="Planar Polygons: triangle, parallelogram, trapezoid, and rhombus"
from drawlib.canvas import save, setup
from drawlib.shapes import parallelogram, rhombus, trapezoid, triangle
from drawlib.styles import Styles

setup(width=144, height=48)

triangle(
    (20, 24),
    width=24,
    height=22,
    style=Styles.Neutral.patch(shape_r=1.5),
    text="Delta",
    text_style=Styles.DarkBold.patch(text_size=10.5, xy_abs_shift=(0, -3)),
)

parallelogram(
    (54, 24),
    width=30,
    height=20,
    corner_angle=72,
    style=Styles.PrimaryNeutral.patch(shape_r=1.5),
    text="Stream I/O",
    text_style=Styles.DarkBold.patch(text_size=10.5),
)

trapezoid(
    (90, 24),
    height=20,
    bottomedge_width=30,
    topedge_width=18,
    style=Styles.SecondaryNeutral.patch(shape_r=1.5),
    text="Ingress LB",
    text_style=Styles.DarkBold.patch(text_size=10.5),
)

rhombus(
    (125, 24),
    width=28,
    height=22,
    style=Styles.PrimaryFlat.patch(shape_r=1.5),
    text="Valid?",
    text_style=Styles.WhiteBold.patch(text_size=10.5),
)

save()
```

---

## 3. Radial Polygons & Decorative Plaques (`regularpolygon`, `star`, `plaque`)

### 3.1. `regularpolygon`
Draws an equilateral, equiangular $N$-sided polygon (`num_vertex >= 3`) inscribed within `radius` around `xy`.

```python
def regularpolygon(
    xy: tuple[float, float],
    num_vertex: int,
    radius: float,
    *,
    hole_ratio: float | None = None,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None: ...
```
- **Positional Order**: `num_vertex: int` is the **2nd** argument and `radius: float` is the **3rd** argument (e.g. `regularpolygon((50, 25), 6, 14, style=Styles.PrimaryNeutral)`).
- Supports both `hole_ratio` (hollow ring polygon) and `style.patch(shape_r=...)` (rounded polygon vertices).

### 3.2. `star`
Draws a $2N$-vertex star alternating between `radius_ext` (outer tips) and `radius_int` (inner valleys) around `xy`.

```python
def star(
    xy: tuple[float, float],
    num_vertex: int,
    radius_ext: float,
    radius_int: float,
    *,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None: ...
```
- Supports `style.patch(shape_r=...)` for soft, rounded star tips and valleys.

### 3.3. `plaque`
Draws an ornamental plaque frame with inward-scooped (`"concave"`), outward-bulging (`"convex"`), or chamfered (`"bevel"` / `"chamfer"` / `"octagon"`) corners centered at `xy`.

```python
def plaque(
    xy: tuple[float, float],
    width: float,
    height: float,
    *,
    variant: Literal["concave", "convex", "bevel", "chamfer", "octagon"] = "concave",
    cut_ratio: float | None = None,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None: ...
```
- `cut_ratio`: Corner scoop/chamfer depth as a ratio of `min(width, height)` (`0.0 < cut_ratio < 0.48`, default `0.22`).

```drawlib code=fold align=center file=shapes_polygon_radial_plaque.png caption="regularpolygon (Hexagon & Hollow Octagon), star, and plaque Variants"
from drawlib.canvas import save, setup
from drawlib.shapes import plaque, regularpolygon, star
from drawlib.styles import Styles

setup(width=144, height=48)

regularpolygon(
    (20, 24),
    6,
    13,
    style=Styles.PrimaryNeutral.patch(shape_r=1.5),
    text="Hex Node",
    text_style=Styles.DarkBold.patch(text_size=10.0),
)

regularpolygon(
    (52, 24),
    8,
    13,
    hole_ratio=0.55,
    style=Styles.SecondaryNeutral,
    text="Oct",
    text_style=Styles.DarkBold.patch(text_size=10.0),
)

star(
    (84, 24),
    5,
    14,
    6.5,
    style=Styles.WarningFlat.patch(shape_r=0.8),
    text="Featured",
    text_style=Styles.DarkBold.patch(text_size=10.0, xy_abs_shift=(0, -17)),
)

plaque(
    (120, 24),
    width=34,
    height=22,
    variant="concave",
    style=Styles.Neutral,
    text="Cert Frame",
    text_style=Styles.DarkBold.patch(text_size=10.5),
)

save()
```

---

## 4. Arbitrary Vertex Polygons & Low-Level Vector Paths (`polygon`, `bubblespeech`, `shape`)

### 4.1. `polygon`
Draws a closed polygon from an explicit list of `(x, y)` canvas coordinates (`len(xys) >= 3`), with optional interior cutouts (`holes`) and corner rounding (`style.patch(shape_r=...)`).

```python
def polygon(
    xys: list[tuple[float, float]],
    *,
    holes: list[list[tuple[float, float]]] | None = None,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None: ...
```
- `xys`: Exterior boundary vertices in canvas coordinates.
- `holes`: Optional list of interior cutout vertex loops (each loop must contain $\ge 3$ `(x, y)` points).
- Embedded `text` and `style.angle` rotation are automatically centered at the arithmetic centroid of `xys`.

### 4.2. `bubblespeech` (Callout Reference)
*(Implemented in `_badge.py`; see `lib-shapes-badge` for full callout details.)*
Draws a rectangular callout centered at `xy` with a pointer tail protruding from `tail_edge` (`"left"`, `"right"`, `"top"`, `"bottom"`) to absolute coordinate `tail_vertex_xy`.

```python
def bubblespeech(
    xy: tuple[float, float],
    width: float,
    height: float,
    tail_edge: Literal["left", "right", "top", "bottom"],
    tail_start_ratio: float,
    tail_vertex_xy: tuple[float, float],
    tail_end_ratio: float,
    *,
    r: float = 0.0,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None: ...
```

### 4.3. `shape` (Low-Level Mixed Vertex / Bézier Path Builder)
Constructs custom vector artwork from local coordinates and nested quadratic (2-point) or cubic (3-point) Bézier control tuples.

```python
def shape(
    xy: tuple[float, float],
    path_points: Sequence[
        tuple[float, float]
        | Sequence[tuple[float, float]]
        | Path
        | tuple[Path, str | tuple[int, int, int] | tuple[int, int, int, float]]
    ],
    *,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
    is_default_center: bool = False,
) -> None: ...
```
- **`is_default_center: bool = False` (Keyword-Only)**: When `False` (default), `xy` anchors the **bottom-left** of the path's bounding box; pass `is_default_center=True` so `xy` anchors the **center** `(cx, cy)`.
- **`path_points` grammar**:
  - `(x, y)` tuple: Straight line (`LINETO`) to `(x, y)` (first point is `MOVETO`).
  - `[(cx, cy), (end_x, end_y)]` (2-point sequence): Quadratic Bézier curve (`CURVE3`).
  - `[(c1x, c1y), (c2x, c2y), (end_x, end_y)]` (3-point sequence): Cubic Bézier curve (`CURVE4`).
