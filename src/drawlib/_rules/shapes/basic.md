# Drawlib Basic Shapes Guidelines (`lib-shapes-basic`)

API specification and geometric rules for fundamental planar and circular primitives in `drawlib._core.l4_canvas._shapes._basic` (`rectangle`, `circle`, `ellipse`, `wedge`, `fan`, `arc`), plus the 3D `cylinder` primitive. See `lib-shapes-overview` for universal coordinate and styling rules.

---

## 1. Summary of Basic Shapes

All basic shapes are **Center-Anchored at `xy = (cx, cy)`** and require `*, style: Style` as a mandatory keyword-only argument:

| Function | Positional Args | Keyword-Only Geometry Args | Fill / Stroke Mode | Primary Architectural Use Cases |
| :--- | :--- | :--- | :--- | :--- |
| **`rectangle`** | `xy, width, height` | `hole_ratio: float \| None = None` | Fill + Stroke (`shape_r`) | Service cards, VPC boundaries, swimlanes, Hollow frames |
| **`circle`** | `xy, radius` | `hole_ratio: float \| None = None` | Fill + Stroke | Status nodes, numbered badges, annular donut rings |
| **`ellipse`** | `xy, width, height` | `hole_ratio: float \| None = None` | Fill + Stroke | ER attributes, start/end terminals, oval rings |
| **`wedge`** | `xy, radius` | `width=None, angle_start=0, angle_end=360` | Fill + Stroke | Gauge arcs, donut chart segments, pie wedges |
| **`fan`** | `xy, radius` | `angle_start=0, angle_end=180` | Fill + Stroke | Radar vision cones, pie slices, angular sectors |
| **`arc`** | `xy, width, height` | `angle_start=0.0, angle_end=360.0` | **Stroke-Only** (`line_*`) | Open elliptical/circular trajectories, gauges, orbit arcs |
| **`cylinder`** | `xy, width, height` | `disks: int = 1` *(in `_container.py`)* | Fill + Stroke (3D cap) | Relational databases, data lakes, persistent volumes |

---

## 2. Rectangular & Elliptical Primitives (`rectangle`, `circle`, `ellipse`)

### 2.1. `rectangle`
Draws an axis-aligned or rotated rectangle, rounded card (`style.patch(shape_r=...)`), or hollow frame (`hole_ratio`).

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
- **Parameters**:
  - `xy`: Center coordinate `(cx, cy)`.
  - `width`, `height`: Outer dimensions ($> 0$).
  - `hole_ratio`: Optional hollow cutout ratio in `(0.0, 1.0)`. Inner cutout is `(width * hole_ratio, height * hole_ratio)`.
  - `style`: Required `Style` instance. Supports `shape_r` for rounded corners and `angle` for CCW rotation.
  - `text`, `text_style`: Optional centered label and text style.

### 2.2. `circle`
Draws a circle or hollow annular ring / donut (`hole_ratio`) centered at `xy`.

```python
def circle(
    xy: tuple[float, float],
    radius: float,
    *,
    hole_ratio: float | None = None,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None: ...
```
- **Parameters**:
  - `xy`: Center coordinate `(cx, cy)`.
  - `radius`: Outer radius ($> 0$). Bounding box is $2r \times 2r$.
  - `hole_ratio`: Optional inner cutout ratio in `(0.0, 1.0)`. Inner radius is `radius * hole_ratio`.
  - `style`: Required `Style` instance (`angle` rotates embedded text).

### 2.3. `ellipse`
Draws an ellipse or hollow elliptical ring (`hole_ratio`) bounded by `width` and `height`.

```python
def ellipse(
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
- **Parameters**:
  - `xy`: Center coordinate `(cx, cy)`.
  - `width`, `height`: Total horizontal and vertical axis diameters ($> 0$).
  - `hole_ratio`: Optional inner cutout ratio in `(0.0, 1.0)`.
  - `style`: Required `Style` instance (`angle` rotates both the ellipse and embedded text).

```drawlib code=fold align=center file=shapes_basic_rect_circle_ellipse.png caption="rectangle, circle, and ellipse: Solid Cards and Compound Hollow Cutouts (hole_ratio)"
from drawlib.canvas import save, setup
from drawlib.shapes import circle, ellipse, rectangle
from drawlib.styles import Styles

setup(width=140, height=48)

rectangle(
    (22, 24),
    width=28,
    height=20,
    style=Styles.Neutral.patch(shape_r=2.5),
    text="Service Card",
    text_style=Styles.DarkBold.patch(text_size=10.5),
)

rectangle(
    (56, 24),
    width=26,
    height=20,
    hole_ratio=0.55,
    style=Styles.PrimaryNeutral.patch(shape_r=2.0),
    text="Frame",
    text_style=Styles.DarkBold.patch(text_size=10.0),
)

circle(
    (88, 24),
    radius=11,
    hole_ratio=0.6,
    style=Styles.PrimaryFlat,
    text="78%",
    text_style=Styles.DarkBold.patch(text_size=10.5),
)

ellipse(
    (120, 24),
    width=28,
    height=18,
    style=Styles.SecondaryNeutral,
    text="Start / End",
    text_style=Styles.DarkBold.patch(text_size=10.5),
)

save()
```

---

## 3. Angular Sectors & Open Arcs (`wedge`, `fan`, `arc`)

> **Important Signature Rule**: In `wedge`, `fan`, and `arc`, the angular bounds (`angle_start`, `angle_end`) and ring thickness (`width` on `wedge`) are **keyword-only arguments** placed after `*`.

### 3.1. `wedge`
Draws a circular pie slice (`width=None`) or curved annular ring segment (`width > 0`) sweeping CCW from `angle_start` to `angle_end`.

```python
def wedge(
    xy: tuple[float, float],
    radius: float,
    *,
    style: Style,
    width: float | None = None,
    angle_start: float = 0,
    angle_end: float = 360,
    text: str = "",
    text_style: Style | None = None,
) -> None: ...
```
- **Parameters**:
  - `xy`: Center coordinate `(cx, cy)` of the parent circle.
  - `radius`: Outer radius ($> 0$).
  - `style`: Required `Style` instance.
  - `width`: Optional radial ring thickness (`0 < width <= radius`). When `None`, connects to apex `xy` as a solid pie slice; when set, inner radius is `radius - width`.
  - `angle_start`, `angle_end`: CCW start and end angles in degrees (`[0, 360]`).

### 3.2. `fan`
Draws a filled circular sector (pie slice) from apex `xy` to the outer arc between `angle_start` and `angle_end` (equivalent to `wedge(..., width=None)` with default `angle_end=180`).

```python
def fan(
    xy: tuple[float, float],
    radius: float,
    *,
    style: Style,
    angle_start: float = 0,
    angle_end: float = 180,
    text: str = "",
    text_style: Style | None = None,
) -> None: ...
```

### 3.3. `arc`
Draws an **open, unfilled 1D stroke** along an elliptical or circular perimeter. Uses `style.line_color`, `style.line_width`, and `style.line_style` (`shape_fill_color` is ignored).

```python
def arc(
    xy: tuple[float, float],
    width: float,
    height: float,
    *,
    style: Style,
    angle_start: float = 0.0,
    angle_end: float = 360.0,
    text: str = "",
    text_style: Style | None = None,
) -> None: ...
```

```drawlib code=fold align=center file=shapes_basic_wedge_fan_arc.png caption="wedge (Ring Band), fan (Radar Sector), and arc (Open Elliptical Stroke)"
from drawlib.canvas import save, setup
from drawlib.shapes import arc, fan, wedge
from drawlib.styles import Styles

setup(width=136, height=48)

# 1. Annular gauge band via wedge(width=6)
wedge(
    (26, 20),
    radius=16,
    width=6,
    angle_start=20,
    angle_end=160,
    style=Styles.PrimaryFlat,
    text="SLA 99.9%",
    text_style=Styles.DarkBold.patch(text_size=10.0, xy_abs_shift=(0, -4)),
)

# 2. Filled circular sector via fan()
fan(
    (70, 14),
    radius=22,
    angle_start=35,
    angle_end=145,
    style=Styles.SecondaryNeutral,
    text="Radar FOV",
    text_style=Styles.DarkBold.patch(text_size=10.5, xy_abs_shift=(0, 11)),
)

# 3. Open stroke trajectory via arc()
arc(
    (112, 22),
    width=30,
    height=22,
    angle_start=300,
    angle_end=240,
    style=Styles.PrimaryBold.patch(line_style="dashed"),
    text="Orbit",
    text_style=Styles.DarkBold.patch(text_size=10.5),
)

save()
```

---

## 4. `cylinder` (Database & Storage Container Reference)

*(Implemented in `_container.py`; also documented in `lib-shapes-container`.)*
Draws a 3D-shaded cylinder centered at `xy` with an automatically lightened elliptical top cap and optional multi-disk seams (`disks >= 1`).

```python
def cylinder(
    xy: tuple[float, float],
    width: float,
    height: float,
    *,
    style: Style,
    disks: int = 1,
    text: str = "",
    text_style: Style | None = None,
) -> None: ...
```

```drawlib code=fold align=center file=shapes_basic_cylinder.png caption="cylinder: Single-Disk Primary Database and 3-Disk Storage Cluster"
from drawlib.canvas import save, setup
from drawlib.shapes import cylinder
from drawlib.styles import Styles

setup(width=110, height=48)

cylinder(
    (32, 24),
    width=26,
    height=32,
    style=Styles.PrimaryFlat,
    text="Users DB",
    text_style=Styles.WhiteBold.patch(text_size=10.5),
)

cylinder(
    (78, 24),
    width=28,
    height=32,
    disks=3,
    style=Styles.SecondaryNeutral,
    text="Data Lake",
    text_style=Styles.DarkBold.patch(text_size=10.5),
)

save()
```
