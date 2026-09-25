# Drawlib Shapes Guidelines

Comprehensive architectural manual and API specification for `drawlib.shapes`. This guide details all 21 shape primitives, coordinate geometry, alignment engines, vector construction rules, and production diagram patterns.

---

## Table of Contents

- [1. Architectural Overview & Core Mechanics](#1-architectural-overview--core-mechanics)
  - [1.1 Package Facade & Exports](#11-package-facade--exports)
  - [1.2 Canvas Coordinate Space & The Cartesian Model](#12-canvas-coordinate-space--the-cartesian-model)
  - [1.3 Geometric Anchors: Center vs. Bottom-Left Origins](#13-geometric-anchors-center-vs-bottom-left-origins)
  - [1.4 Alignment Transformation Engine (`halign` & `valign`)](#14-alignment-transformation-engine-halign--valign)
  - [1.5 Rotation Coordinate Mathematics](#15-rotation-coordinate-mathematics)
  - [1.6 The Unified Styling System (`Style`)](#16-the-unified-styling-system-style)
  - [1.7 Embedded Text Rendering & Micro-Offsets (`textstyle`)](#17-embedded-text-rendering--micro-offsets-textstyle)
- [2. Circle-like Shapes](#2-circle-like-shapes)
  - [2.1 `circle`](#21-circle)
  - [2.2 `donuts`](#22-donuts)
  - [2.3 `ellipse`](#23-ellipse)
  - [2.4 `wedge`](#24-wedge)
  - [2.5 `fan`](#25-fan)
  - [2.6 `arc`](#26-arc)
- [3. Polygon & Planar Geometric Primitives](#3-polygon--planar-geometric-primitives)
  - [3.1 `rectangle`](#31-rectangle)
  - [3.2 `parallelogram`](#32-parallelogram)
  - [3.3 `rhombus`](#33-rhombus)
  - [3.4 `trapezoid`](#34-trapezoid)
  - [3.5 `triangle`](#35-triangle)
  - [3.6 `regularpolygon`](#36-regularpolygon)
  - [3.7 `polygon`](#37-polygon)
  - [3.8 `star`](#38-star)
- [4. Custom Path & Vector Construction](#4-custom-path--vector-construction)
  - [4.1 `shape`](#41-shape)
- [5. Directed Block Arrow Shapes](#5-directed-block-arrow-shapes)
  - [5.1 `arrow`](#51-arrow)
  - [5.2 `arrow_l`](#52-arrow_l)
  - [5.3 `arrow_u`](#53-arrow_u)
  - [5.4 `arrow_arc`](#54-arrow_arc)
  - [5.5 `arrow_polyline`](#55-arrow_polyline)
  - [5.6 `chevron`](#56-chevron)
- [6. Production Architectural Blueprints & Schemas](#6-production-architectural-blueprints--schemas)
  - [6.1 Cloud Infrastructure Schema (AWS VPC / Multi-Tier)](#61-cloud-infrastructure-schema-aws-vpc--multi-tier)
  - [6.2 Event-Driven Microservices Topology (Kafka / Event Mesh)](#62-event-driven-microservices-topology-kafka--event-mesh)
  - [6.3 Deep Neural Network Layer Graph (CNN / ResNet Skip Connection)](#63-deep-neural-network-layer-graph-cnn--resnet-skip-connection)
  - [6.4 UML State Machine Diagram](#64-uml-state-machine-diagram)
  - [6.5 Modern Dashboard UI Component Kit (Cards, Badges, Metrics)](#65-modern-dashboard-ui-component-kit-cards-badges-metrics)
- [7. Quick Reference Matrix & Troubleshooting](#7-quick-reference-matrix--troubleshooting)
  - [7.1 Function Capabilities Matrix](#71-function-capabilities-matrix)
  - [7.2 Common Pitfalls & Resolution Rules](#72-common-pitfalls--resolution-rules)

---

## 1. Architectural Overview & Core Mechanics

### 1.1 Package Facade & Exports

The `drawlib.shapes` module re-exports 21 functions implemented across internal canvas engines (`drawlib._core.l4_canvas._base`, `_patches`, `_polygon`, and `_arrow`).

```python
from drawlib.shapes import (
    arc,
    arrow,
    arrow_arc,
    arrow_l,
    arrow_polyline,
    arrow_u,
    chevron,
    circle,
    donuts,
    ellipse,
    fan,
    parallelogram,
    polygon,
    rectangle,
    regularpolygon,
    rhombus,
    shape,
    star,
    trapezoid,
    triangle,
    wedge,
)
```

Every shape function is decorated with `@guarded`, providing runtime type validation, parameter constraint verification, and uniform error reporting.

---

### 1.2 Canvas Coordinate Space & The Cartesian Model

Drawlib operates on an intuitive, resolution-independent Cartesian 2D coordinate system:
- **Origin `(0, 0)`**: Located at the **bottom-left** corner of the canvas.
- **X-axis**: Extends horizontally to the right, from `0` to `width`.
- **Y-axis**: Extends vertically upwards, from `0` to `height`.
- **Angles**: Measured in **degrees counterclockwise (CCW)** from the positive X-axis (standard mathematical convention).

```text
Y ^
  |  (0, height)                   (width, height)
  |       +-------------------------------+
  |       |                               |
  |       |          Canvas Area          |
  |       |                               |
  |       +-------------------------------+
  |  (0, 0)                        (width, 0)
  +---------------------------------------------> X
```

---

### 1.3 Geometric Anchors: Center vs. Bottom-Left Origins

Shape functions fall into three distinct coordinate anchoring categories:

1. **Center-Anchored Shapes (`is_default_center = True`)**:
   The input `xy=(x, y)` parameter specifies the exact **geometric center** of the shape.
   - Functions: `circle`, `donuts`, `ellipse`, `wedge`, `fan`, `arc`, `regularpolygon`, `star`, `arrow_l`, `arrow_u`, `arrow_arc`.
2. **Bottom-Left Anchored Shapes (`is_default_center = False`)**:
   The input `xy=(x, y)` parameter specifies the **bottom-left corner of the shape's unrotated bounding box**.
   - Functions: `rectangle`, `parallelogram`, `rhombus`, `trapezoid`, `triangle`, `chevron`, `shape` (when `is_default_center=False`).
3. **Directed & Multi-Point Shapes (Point-Defined)**:
   Position is explicitly defined by specific vertex sequences or directional endpoints.
   - Functions: `arrow` (`xy1` start, `xy2` end), `arrow_polyline` (`xys` path), `polygon` (`xys` vertices).

```text
Center-Anchored:                       Bottom-Left Anchored:
       +-------+                              +-------+
       |   ^   |                              |       |
       | <-xy->|  xy = (center_x, center_y)   |       |
       |   v   |                              +-------+
       +-------+                             xy = (min_x, min_y)
```

---

### 1.4 Alignment Transformation Engine (`halign` & `valign`)

When positioning shapes relative to layout grids or text baselines, you can override default anchor behavior by setting `text_halign` and `text_valign` on the shape's `Style`:

| Alignment Attribute | Valid Options | Default for Center Shapes | Default for Bounding-Box Shapes |
| :--- | :--- | :--- | :--- |
| `text_halign` | `"left"`, `"center"`, `"right"` | `"center"` | `"center"` (if `angle != 0`) / `"left"` (if unrotated) |
| `text_valign` | `"bottom"`, `"center"`, `"top"` | `"center"` | `"center"` (if `angle != 0`) / `"bottom"` (if unrotated) |

#### Transformation Mathematics
For a shape with unrotated width $W$ and height $H$, the internal alignment engine shifts the anchor coordinates `(x, y)` according to the following formulas:

- **For Center-Anchored Shapes (`is_default_center = True`)**:
  - Horizontal: `"left"`: $x' = x + \frac{W}{2}$ | `"center"`: $x' = x$ | `"right"`: $x' = x - \frac{W}{2}$
  - Vertical: `"bottom"`: $y' = y + \frac{H}{2}$ | `"center"`: $y' = y$ | `"top"`: $y' = y - \frac{H}{2}$

- **For Bottom-Left Anchored Shapes (`is_default_center = False`)**:
  - Horizontal: `"left"`: $x' = x$ | `"center"`: $x' = x - \frac{W}{2}$ | `"right"`: $x' = x - W$
  - Vertical: `"bottom"`: $y' = y$ | `"center"`: $y' = y - \frac{H}{2}$ | `"top"`: $y' = y - H$

> **Important**: `arrow`, `arrow_polyline`, and `polygon` compute vertices directly from coordinate vectors and **ignore** `text_halign` and `text_valign`.

---

### 1.5 Rotation Coordinate Mathematics

All shapes accepting an `angle` parameter rotate counterclockwise around the shape's **geometric center $(C_x, C_y)$**.
Even for shapes anchored at the bottom-left, the center is computed first as $C = (x + W/2, y + H/2)$, rotated by $\theta = \text{radians}(\text{angle})$, and the vertices are transformed:

$$x_{\text{rot}} = (x - C_x)\cos\theta - (y - C_y)\sin\theta + C_x$$
$$y_{\text{rot}} = (x - C_x)\sin\theta + (y - C_y)\cos\theta + C_y$$

Embedded shape text rotates alongside the shape by default, maintaining its relative orientation inside the shape boundary.

---

### 1.6 The Unified Styling System (`Style`)

Shape styling is driven by Drawlib's core `Style` dataclass or predefined style preset strings (e.g., `"blue"`, `"green_flat"`, `"red_dashed"`).

```python
from drawlib.colors import Colors, Colors140
from drawlib.types import Style

custom_shape_style = Style(
    fill_color=Colors140.AliceBlue,      # Interior fill color (RGB, RGBA, or hex)
    fill_alpha=0.85,                     # Opacity float: 0.0 (transparent) to 1.0 (opaque)
    line_color=Colors140.SteelBlue,      # Stroke boundary color
    line_width=2.5,                      # Stroke thickness in points (0 disables border)
    line_style="dashed",                 # "solid" | "dashed" | "dotted" | "dashdot"
    text_halign="center",                # Layout horizontal anchor
    text_valign="center",                # Layout vertical anchor
)
```

#### System Defaults (`SYSTEM_DEFAULT_SHAPE_STYLE`)
Unless overridden, all shapes inherit these baseline attributes:
- `fill_color`: `Colors.White` `(255, 255, 255)`
- `fill_alpha`: `1.0` (fully opaque)
- `line_color`: `Colors.Black` `(0, 0, 0)`
- `line_width`: `1.0`
- `line_style`: `"solid"`
- `text_halign`: `"center"`
- `text_valign`: `"center"`

To eliminate a shape's border line entirely, explicitly pass `line_width=0`. To make a shape completely hollow/transparent, pass `fill_color=Colors.Transparent` or `fill_alpha=0.0`.

---

### 1.7 Embedded Text Rendering & Micro-Offsets (`textstyle`)

Almost all shapes accept `text`, `textsize`, and `textstyle` parameters.
- Text is automatically rendered at the centroid $(C_x, C_y)$ of the shape.
- Text automatically rotates with the shape's `angle` unless overridden by `text_angle`.
- Font size can be specified directly via `textsize` (numeric float or `"small" | "medium" | "large"`), or through `textstyle=Style(text_size=...)`. The `textstyle` parameter is preferred.

```python
from drawlib.fonts import FontSansSerif
from drawlib.types import Style

custom_text_style = Style(
    text_color=Colors140.MidnightBlue,
    text_size=18,
    text_font=FontSansSerif.ROBOTO_BOLD,
    text_angle=0.0,                  # Freeze text horizontally even if shape rotates
    text_flip=False,                 # Invert 180 degrees if True
    text_xy_shift=(0.0, -3.0),       # Relative micro-adjustment offset (dx, dy)
)
```

#### Shift Semantics
- `text_xy_shift=(dx, dy)`: Moves the text relative to the shape's coordinate system. If the shape is rotated, the offset vector $(dx, dy)$ rotates with it.
- `text_xy_abs_shift=(dx, dy)`: Moves the text along the absolute, unrotated canvas axes.

---

## 2. Circle-like Shapes

Circle-like shapes are centered at `xy=(x, y)` and sized primarily using radii.

```text
                  *** 0 deg (top/right) ***
               *             *
            *                   *
          *                       *
         *                         *  Radius r
         *            xy           * <-------->
         *                         *
          *                       *
            *                   *
               *             *
                  *********
```

---

### 2.1 `circle`

Draws a standard geometric circle.

#### Signature
```python
def circle(
    xy: tuple[float, float],
    radius: float,
    angle: float = 0.0,
    style: Style | str | None = None,
    text: str = "",
    textsize: float | Literal["small", "medium", "large"] | None = None,
    textstyle: Style | str | None = None,
) -> None:
    ...
```

#### Parameter Breakdown
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *Required* | Center coordinate `(x, y)`. |
| `radius` | `float` | *Required* | Radius of the circle (must be $> 0$). |
| `angle` | `float` | `0.0` | Rotation angle in degrees CCW (affects embedded text orientation). |
| `style` | `Style \| str \| None` | `None` | Preset style string or `Style` instance. |
| `text` | `str` | `""` | Text label drawn at the circle center. |
| `textsize` | `float \| str \| None` | `None` | Text font size override. |
| `textstyle` | `Style \| str \| None` | `None` | Preset text style string or `Style` instance. |

#### Geometric & Alignment Mechanics
- **Anchor**: Geometric center `(x, y)`.
- Bounding box is $2r \times 2r$.
- Setting `style.text_halign="left"` shifts the circle so that `x` aligns with its left tangent boundary ($x' = x + r$).
- `angle` does not alter the appearance of a symmetric circle, but rotates embedded text around the center point.

#### Code Examples
```drawlib show-code
from drawlib.canvas import config, save

config(width=100, height=50)
from drawlib.colors import Colors140
from drawlib.shapes import circle
from drawlib.types import Style

# 1. Solid status node with embedded label
circle((30, 25), radius=14, style="green_flat", text="OK", textstyle=Style(text_size=14))

# 2. Semi-transparent dashed boundary zone with rotated label
circle(
    (70, 25),
    radius=18,
    angle=35,
    style=Style(fill_color=Colors140.DeepSkyBlue, fill_alpha=0.3, line_style="dashed", line_width=2),
    text="Zone B",
    textstyle=Style(text_color=Colors140.Navy, text_size=12),
)
save()

```

---

### 2.2 `donuts`

Draws an annular ring defined by an outer radius and filled wall thickness.

#### Signature
```python
def donuts(
    xy: tuple[float, float],
    radius: float,
    width: float | None = None,
    angle: float = 0.0,
    style: Style | str | None = None,
    text: str = "",
    textsize: float | Literal["small", "medium", "large"] | None = None,
    textstyle: Style | str | None = None,
) -> None:
    ...
```

#### Parameter Breakdown
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *Required* | Center coordinate `(x, y)`. |
| `radius` | `float` | *Required* | Outer radius of the annular ring. |
| `width` | `float \| None` | `None` | Ring wall thickness. Inner radius = $\text{radius} - \text{width}$. If `None`, renders solid. |
| `angle` | `float` | `0.0` | Rotation angle in degrees CCW (affects embedded text). |
| `style` | `Style \| str \| None` | `None` | Shape fill and stroke configuration. |
| `text` | `str` | `""` | Label rendered in the center void of the donut. |
| `textsize` | `float \| str \| None` | `None` | Text font size override. |
| `textstyle` | `Style \| str \| None` | `None` | Text styling parameters. |

#### Geometric & Alignment Mechanics
- Built on top of `wedge(..., angle_start=0, angle_end=360)`.
- If `width >= radius`, the inner radius collapses to 0 or becomes invalid. Ensure $0 < \text{width} < \text{radius}$.
- Center text is positioned in the hollow central core.

#### Code Examples
```drawlib show-code
from drawlib.canvas import config, save

config(width=100, height=50)
from drawlib.colors import Colors140
from drawlib.shapes import donuts
from drawlib.types import Style

# 1. Thin status indicator ring
donuts((30, 22), radius=15, width=4, style="gray", text="Base")

# 2. KPI ring badge with custom fill and styled percentage label
donuts(
    (70, 22),
    radius=17,
    width=6,
    style=Style(fill_color=Colors140.Purple, line_color=Colors140.Indigo, line_width=2),
    text="78%",
    textstyle=Style(text_size=14, text_color=Colors140.White),
)
save()

```

---

### 2.3 `ellipse`

Draws an axis-aligned or rotated ellipse bounded by width and height.

#### Signature
```python
def ellipse(
    xy: tuple[float, float],
    width: float,
    height: float,
    angle: float = 0.0,
    style: Style | str | None = None,
    text: str = "",
    textsize: float | Literal["small", "medium", "large"] | None = None,
    textstyle: Style | str | None = None,
) -> None:
    ...
```

#### Parameter Breakdown
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *Required* | Center coordinate `(x, y)`. |
| `width` | `float` | *Required* | Total horizontal axis diameter before rotation. |
| `height` | `float` | *Required* | Total vertical axis diameter before rotation. |
| `angle` | `float` | `0.0` | Rotation angle in degrees CCW around center `xy`. |
| `style` | `Style \| str \| None` | `None` | Shape style or preset name. |
| `text` | `str` | `""` | Centered text annotation. |
| `textsize` | `float \| str \| None` | `None` | Text font size override. |
| `textstyle` | `Style \| str \| None` | `None` | Text formatting style. |

#### Geometric & Alignment Mechanics
- Semi-major axis $a = \text{width} / 2$, Semi-minor axis $b = \text{height} / 2$.
- When rotated by `angle`, the ellipse and its text rotate synchronously.
- Widely used for database entities (ER diagrams), start/end states in flowcharts, and distributed cache clusters.

#### Code Examples
```drawlib show-code
from drawlib.canvas import config, save

config(width=100, height=50)
from drawlib.colors import Colors140
from drawlib.shapes import ellipse
from drawlib.types import Style

# 1. Database schema entity
ellipse((30, 22), width=36, height=20, style="yellow_flat", text="users_tbl")

# 2. Rotated processing stage node with dashed boundary
ellipse(
    (70, 22),
    width=38,
    height=18,
    angle=335,
    style=Style(fill_color=Colors140.AliceBlue, line_color=Colors140.SteelBlue, line_style="dashed", line_width=2),
    text="In-Flight Job",
    textstyle=Style(text_size=11, text_color=Colors140.Navy),
)
save()

```

---

### 2.4 `wedge`

Draws an angular slice of a circle or ring between two angles (`angle_start` to `angle_end`).

#### Signature
```python
def wedge(
    xy: tuple[float, float],
    radius: float,
    angle_start: float,
    angle_end: float,
    width: float | None = None,
    angle: float = 0.0,
    style: Style | str | None = None,
    text: str = "",
    textsize: float | Literal["small", "medium", "large"] | None = None,
    textstyle: Style | str | None = None,
) -> None:
    ...
```

#### Parameter Breakdown
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *Required* | Center origin of the arc/circle. |
| `radius` | `float` | *Required* | Outer radius of the sector. |
| `angle_start` | `float` | *Required* | Starting angle in degrees CCW. |
| `angle_end` | `float` | *Required* | Ending angle in degrees CCW. |
| `width` | `float \| None` | `None` | Annular thickness. If `None`, extends to apex `xy` (solid pie wedge). |
| `angle` | `float` | `0.0` | Global rotational shift applied to the entire wedge. |
| `style` | `Style \| str \| None` | `None` | Shape fill and outline style. |
| `text` | `str` | `""` | Centered text label. |
| `textsize` | `float \| str \| None` | `None` | Font size override. |
| `textstyle` | `Style \| str \| None` | `None` | Style instance for text formatting. |

#### Geometric & Alignment Mechanics
- Draws CCW from `angle_start` to `angle_end`.
- If `width` is given, inner radius $r_{\text{in}} = \text{radius} - \text{width}$, forming a curved circular band segment.
- Ideal for custom gauge meters, donut chart slices, and progress wheels.

#### Code Examples
```drawlib show-code
from drawlib.canvas import config, save

config(width=100, height=50)
from drawlib.colors import Colors140
from drawlib.shapes import wedge
from drawlib.types import Style

# 1. Quarter gauge ring slice with thickness
wedge((30, 22), radius=18, angle_start=0, angle_end=90, width=5, style="blue_flat", text="Q1")

# 2. Rotated multi-segment slice with border stroke
wedge(
    (70, 22),
    radius=18,
    angle_start=45,
    angle_end=225,
    width=6,
    angle=15,
    style=Style(fill_color=Colors140.Orange, line_color=Colors140.DarkRed, line_width=1.5),
    text="60%",
    textstyle=Style(text_size=11, text_color=Colors140.White),
)
save()

```

---

### 2.5 `fan`

Draws a filled circular sector (pie slice) extending from the apex at `xy` to the outer circular arc.

#### Signature
```python
def fan(
    xy: tuple[float, float],
    radius: float,
    angle_start: float,
    angle_end: float,
    angle: float = 0.0,
    style: Style | str | None = None,
    text: str = "",
    textsize: float | Literal["small", "medium", "large"] | None = None,
    textstyle: Style | str | None = None,
) -> None:
    ...
```

#### Parameter Breakdown
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *Required* | Apex coordinate (center of the circle). |
| `radius` | `float` | *Required* | Radius from apex to circular rim. |
| `angle_start` | `float` | *Required* | Starting angle in degrees CCW. |
| `angle_end` | `float` | *Required* | Ending angle in degrees CCW. |
| `angle` | `float` | `0.0` | Global rotational offset in degrees. |
| `style` | `Style \| str \| None` | `None` | Shape fill and line style. |
| `text` | `str` | `""` | Centered text label. |
| `textsize` | `float \| str \| None` | `None` | Text font size override. |
| `textstyle` | `Style \| str \| None` | `None` | Text formatting style. |

#### Geometric & Alignment Mechanics
- Functionally equivalent to `wedge(..., width=None)`.
- Vertex at `xy` connects via two radial edges to the arc endpoints.
- Perfect for radar vision cones, camera field-of-view indicators, and pie chart segments.

#### Code Examples
```drawlib show-code
from drawlib.canvas import config, save

config(width=100, height=50)
from drawlib.colors import Colors140
from drawlib.shapes import fan
from drawlib.types import Style

# 1. Radar scanner coverage cone
fan(
    (30, 15),
    radius=25,
    angle_start=30,
    angle_end=150,
    style=Style(fill_color=Colors140.LightGreen, fill_alpha=0.4, line_color=Colors140.ForestGreen, line_width=1.5),
    text="FOV",
)

# 2. Semi-circle gauge backdrop
fan((75, 15), radius=22, angle_start=0, angle_end=180, style="blue_flat", text="Upper Range")
save()

```

---

### 2.6 `arc`

Draws an open, unfilled curved stroke along an elliptical or circular perimeter.

#### Signature
```python
def arc(
    xy: tuple[float, float],
    width: float,
    height: float,
    angle_start: float,
    angle_end: float,
    angle: float = 0.0,
    style: Style | str | None = None,
    text: str = "",
    textsize: float | Literal["small", "medium", "large"] | None = None,
    textstyle: Style | str | None = None,
) -> None:
    ...
```

#### Parameter Breakdown
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *Required* | Center of the underlying ellipse `(x, y)`. |
| `width` | `float` | *Required* | Horizontal diameter of the ellipse. |
| `height` | `float` | *Required* | Vertical diameter of the ellipse. |
| `angle_start` | `float` | *Required* | Starting angle of the arc in degrees CCW. |
| `angle_end` | `float` | *Required* | Ending angle of the arc in degrees CCW. |
| `angle` | `float` | `0.0` | Global rotation angle around center `xy`. |
| `style` | `Style \| str \| None` | `None` | Stroke styling (`line_color`, `line_width`, `line_style`). |
| `text` | `str` | `""` | Centered text label at `xy`. |
| `textsize` | `float \| str \| None` | `None` | Text font size override. |
| `textstyle` | `Style \| str \| None` | `None` | Text style parameters. |

#### Geometric & Alignment Mechanics
- Unlike `wedge`, `arc` is strictly a 1D stroke boundary line. Any `fill_color` is ignored.
- Set `line_width` to control thickness; set `line_style="dashed"` or `"dotted"` for trajectories.

#### Code Examples
```drawlib show-code
from drawlib.canvas import config, save

config(width=100, height=50)
from drawlib.colors import Colors140
from drawlib.shapes import arc
from drawlib.types import Style

# 1. Curved relationship bracket
arc((30, 22), width=30, height=20, angle_start=30, angle_end=150, style=Style(line_color=Colors140.Navy, line_width=3))

# 2. Dashed orbit path with centered status label
arc(
    (70, 22),
    width=32,
    height=24,
    angle_start=315,
    angle_end=225,
    angle=15,
    style=Style(line_color=Colors140.Crimson, line_width=2, line_style="dashed"),
    text="Orbit A",
    textstyle=Style(text_size=10, text_color=Colors140.Crimson),
)
save()

```

---

## 3. Polygon & Planar Geometric Primitives

Planar geometric shapes construct closed 2D boundaries. Unless noted otherwise, planar shapes are **anchored at their bottom-left corner `(x, y)`** of their unrotated bounding box.

```text
       (x, y + height) +-------------------+ (x + width, y + height)
                       |                   |
                       |      Polygon      |
                       |     Interior      |
                       |                   |
       xy = (x, y)     +-------------------+ (x + width, y)
```

---

### 3.1 `rectangle`

Draws an axis-aligned or rotated box with optional rounded corners.

#### Signature
```python
def rectangle(
    xy: tuple[float, float],
    width: float,
    height: float,
    r: float = 0.0,
    angle: float = 0.0,
    style: Style | str | None = None,
    text: str = "",
    textsize: float | Literal["small", "medium", "large"] | None = None,
    textstyle: Style | str | None = None,
) -> None:
    ...
```

##### Parameter Breakdown
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *Required* | Center coordinate `(x, y)` of the rectangle. |
| `width` | `float` | *Required* | Width along horizontal axis (must be $> 0$). |
| `height` | `float` | *Required* | Height along vertical axis (must be $> 0$). |
| `r` | `float` | `0.0` | Corner rounding radius ($r \ge 0$). Must not exceed $\min(W, H)/2$. |
| `angle` | `float` | `0.0` | Rotation in degrees CCW around geometric center. |
| `style` | `Style \| str \| None` | `None` | Fill and stroke style. |
| `text` | `str` | `""` | Embedded center text label. |
| `textsize` | `float \| str \| None` | `None` | Font size override. |
| `textstyle` | `Style \| str \| None` | `None` | Text formatting style. |

#### Geometric & Alignment Mechanics
- Default coordinate `xy` is the geometric center of the shape.
- Corner rounding `r > 0` constructs smooth quadratic or arc transitions at each vertex.
- Fundamental building block for system architecture diagrams, UI cards, and network topologies.

#### Code Examples
```drawlib show-code
from drawlib.canvas import config, save
from drawlib.colors import Colors140
from drawlib.shapes import rectangle
from drawlib.types import Style

config(width=100, height=50)

# 1. API gateway block with sharp corners
rectangle((28, 25), width=35, height=20, style="blue_flat", text="API Gateway", textstyle=Style(text_size=11))

# 2. Rounded worker card with dashed border
rectangle(
    (72, 25),
    width=35,
    height=20,
    r=4,
    style=Style(fill_color=Colors140.GhostWhite, line_color=Colors140.SlateGray, line_width=2, line_style="dashed"),
    text="Worker Node",
    textstyle=Style(text_color=Colors140.MidnightBlue, text_size=11),
)
save()
```

---

### 3.2 `parallelogram`

Draws a quadrilateral with opposite sides parallel and skewed by an interior slant angle.

#### Signature
```python
def parallelogram(
    xy: tuple[float, float],
    width: float,
    height: float,
    corner_angle: float = 60.0,
    angle: float = 0.0,
    style: Style | str | None = None,
    text: str = "",
    textsize: float | Literal["small", "medium", "large"] | None = None,
    textstyle: Style | str | None = None,
) -> None:
    ...
```

#### Parameter Breakdown
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *Required* | Center coordinate `(x, y)` of the parallelogram. |
| `width` | `float` | *Required* | Length of top and bottom parallel horizontal edges. |
| `height` | `float` | *Required* | Perpendicular vertical height between base and top. |
| `corner_angle` | `float` | `60.0` | Bottom-left interior slant angle ($0 < \theta < 180^\circ$). |
| `angle` | `float` | `0.0` | Global CCW rotation angle around center. |
| `style` | `Style \| str \| None` | `None` | Shape fill and stroke style. |
| `text` | `str` | `""` | Centered text label. |
| `textsize` | `float \| str \| None` | `None` | Font size override. |
| `textstyle` | `Style \| str \| None` | `None` | Text formatting style. |

#### Geometric & Alignment Mechanics
- Centered at `xy`. Top edge is horizontally displaced by $\Delta x = \text{height} / \tan(\text{radians}(\text{corner\_angle}))$.
- Standard flowchart symbol for Input / Output operations and streaming event topics.

#### Code Examples
```drawlib show-code
from drawlib.canvas import config, save
from drawlib.colors import Colors140
from drawlib.shapes import parallelogram
from drawlib.types import Style

config(width=100, height=50)

# 1. Flowchart I/O block
parallelogram((28, 25), width=35, height=20, corner_angle=70, style="blue_flat", text="Read Input")

# 2. Rotated event stream block
parallelogram(
    (72, 25),
    width=35,
    height=20,
    corner_angle=65,
    angle=15,
    style=Style(fill_color=Colors140.LightYellow, line_color=Colors140.GoldenRod, line_width=2),
    text="Kafka Stream",
    textstyle=Style(text_size=10, text_color=Colors140.SaddleBrown),
)
save()
```

---

### 3.3 `rhombus`

Draws an equilateral diamond / rhombus centered in a bounding box.

#### Signature
```python
def rhombus(
    xy: tuple[float, float],
    width: float,
    height: float,
    angle: float = 0.0,
    style: Style | str | None = None,
    text: str = "",
    textsize: float | Literal["small", "medium", "large"] | None = None,
    textstyle: Style | str | None = None,
) -> None:
    ...
```

#### Parameter Breakdown
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *Required* | Center coordinate `(x, y)` of the rhombus. |
| `width` | `float` | *Required* | Total horizontal diagonal span between left and right vertices. |
| `height` | `float` | *Required* | Total vertical diagonal span between bottom and top vertices. |
| `angle` | `float` | `0.0` | Rotation angle in degrees CCW around center. |
| `style` | `Style \| str \| None` | `None` | Shape fill and line style. |
| `text` | `str` | `""` | Centered text label. |
| `textsize` | `float \| str \| None` | `None` | Font size override. |
| `textstyle` | `Style \| str \| None` | `None` | Text formatting style. |

#### Geometric & Alignment Mechanics
- Centered at `xy`. Vertices span symmetrically along horizontal and vertical diagonals.
- Canonical decision block in flowchart logic diagrams and condition branch points.

#### Code Examples
```drawlib show-code
from drawlib.canvas import config, save
from drawlib.colors import Colors140
from drawlib.shapes import rhombus
from drawlib.types import Style

config(width=100, height=50)

# 1. Flowchart decision condition diamond
rhombus((28, 25), width=32, height=24, style="yellow_flat", text="Is Valid?", textstyle=Style(text_size=10))

# 2. Rotated status checkpoint
rhombus(
    (72, 25),
    width=32,
    height=24,
    angle=20,
    style=Style(fill_color=Colors140.MistyRose, line_color=Colors140.Crimson, line_width=2),
    text="Audit",
    textstyle=Style(text_size=11, text_color=Colors140.DarkRed),
)
save()
```

---

### 3.4 `trapezoid`

Draws a quadrilateral with parallel top and bottom horizontal edges.

#### Signature
```python
def trapezoid(
    xy: tuple[float, float],
    height: float,
    bottomedge_width: float,
    topedge_width: float,
    topedge_x: float | None = None,
    angle: float = 0.0,
    style: Style | str | None = None,
    text: str = "",
    textsize: float | Literal["small", "medium", "large"] | None = None,
    textstyle: Style | str | None = None,
) -> None:
    ...
```

#### Parameter Breakdown
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *Required* | Center coordinate `(x, y)` of the trapezoid. |
| `height` | `float` | *Required* | Perpendicular vertical height ($> 0$). |
| `bottomedge_width` | `float` | *Required* | Width of the bottom horizontal edge ($> 0$). |
| `topedge_width` | `float` | *Required* | Width of the top horizontal edge ($> 0$). |
| `topedge_x` | `float \| None` | `None` | X-offset of top-left vertex. Defaults to symmetric isosceles: `(bottomedge_width - topedge_width)/2`. |
| `angle` | `float` | `0.0` | Rotation angle CCW around center. |
| `style` | `Style \| str \| None` | `None` | Shape fill and stroke style. |
| `text` | `str` | `""` | Centered text label. |
| `textsize` | `float \| str \| None` | `None` | Font size override. |
| `textstyle` | `Style \| str \| None` | `None` | Text styling parameters. |

#### Geometric & Alignment Mechanics
- Centered at `xy`.
- **Notice**: There is **no `width` parameter**! You must pass `bottomedge_width` and `topedge_width`.
- Used extensively in neural network architecture diagrams to represent pooling or dimensionality reduction layers.

#### Code Examples
```drawlib show-code
from drawlib.canvas import config, save
from drawlib.colors import Colors140
from drawlib.shapes import trapezoid
from drawlib.types import Style

config(width=100, height=50)

# 1. Neural network downsampling / pooling layer
trapezoid(
    (28, 25),
    height=20,
    bottomedge_width=36,
    topedge_width=22,
    style="green_flat",
    text="MaxPool2D",
    textstyle=Style(text_size=10),
)

# 2. Right-angled projection layer
trapezoid(
    (72, 25),
    height=20,
    bottomedge_width=36,
    topedge_width=18,
    topedge_x=0,
    style=Style(fill_color=Colors140.Lavender, line_color=Colors140.Indigo, line_width=2),
    text="Proj",
    textstyle=Style(text_size=10, text_color=Colors140.Indigo),
)
save()
```

---

### 3.5 `triangle`

Draws a triangle defined by a horizontal base and a customizable apex vertex.

#### Signature
```python
def triangle(
    xy: tuple[float, float],
    width: float,
    height: float,
    topvertex_x: float | None = None,
    angle: float = 0.0,
    style: Style | str | None = None,
    text: str = "",
    textsize: float | Literal["small", "medium", "large"] | None = None,
    textstyle: Style | str | None = None,
) -> None:
    ...
```

#### Parameter Breakdown
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *Required* | Center coordinate `(x, y)` of the triangle. |
| `width` | `float` | *Required* | Horizontal base length ($> 0$). |
| `height` | `float` | *Required* | Perpendicular vertical height ($> 0$). |
| `topvertex_x` | `float \| None` | `None` | Horizontal offset of apex from base left. Defaults to symmetric apex `width / 2`. |
| `angle` | `float` | `0.0` | Rotation angle CCW around center. |
| `style` | `Style \| str \| None` | `None` | Shape fill and outline style. |
| `text` | `str` | `""` | Centered text label. |
| `textsize` | `float \| str \| None` | `None` | Font size override. |
| `textstyle` | `Style \| str \| None` | `None` | Text styling parameters. |

#### Geometric & Alignment Mechanics
- Centered at `xy`.
- Default `topvertex_x=None` produces an isosceles triangle with apex at center top.
- Set `topvertex_x=0` for a left-facing right triangle; set `topvertex_x=width` for a right-facing right triangle.

#### Code Examples
```drawlib show-code
from drawlib.canvas import config, save
from drawlib.colors import Colors140
from drawlib.shapes import triangle
from drawlib.types import Style

config(width=100, height=50)

# 1. Warning indicator badge
triangle(
    (28, 25),
    width=30,
    height=26,
    style=Style(fill_color=Colors140.Gold, line_color=Colors140.DarkGoldenRod, line_width=2),
    text="!",
    textstyle=Style(text_size=16, text_color=Colors140.Black, text_xy_shift=(0, -3)),
)

# 2. Right-angle ramp element
triangle((72, 25), width=32, height=26, topvertex_x=0, style="blue_flat", text="Ramp")
save()
```

---

### 3.6 `regularpolygon`

Draws an equilateral regular polygon with $N$ equal sides, circumscribed in a circle.

#### Signature
```python
def regularpolygon(
    xy: tuple[float, float],
    num_vertex: int,
    radius: float,
    angle: float = 0.0,
    style: Style | str | None = None,
    text: str = "",
    textsize: float | Literal["small", "medium", "large"] | None = None,
    textstyle: Style | str | None = None,
) -> None:
    ...
```

#### Parameter Breakdown
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *Required* | Center coordinate `(x, y)`. |
| `num_vertex` | `int` | *Required* | Number of vertices / sides ($N \ge 3$). Note singular name! |
| `radius` | `float` | *Required* | Circumscribed radius from center to each vertex. |
| `angle` | `float` | `0.0` | Rotation angle CCW around center. |
| `style` | `Style \| str \| None` | `None` | Shape fill and stroke style. |
| `text` | `str` | `""` | Centered text label. |
| `textsize` | `float \| str \| None` | `None` | Font size override. |
| `textstyle` | `Style \| str \| None` | `None` | Text styling parameters. |

#### Geometric & Alignment Mechanics
- Centered at `xy`. Vertices generated at $\theta_k = \text{angle} + k(360^\circ / N)$.
- $N=3$ (equilateral triangle), $N=5$ (pentagon), $N=6$ (hexagon / Kubernetes pod), $N=8$ (octagon / stop sign).

#### Code Examples
```drawlib show-code
from drawlib.canvas import config, save

config(width=100, height=50)
from drawlib.colors import Colors140
from drawlib.shapes import regularpolygon
from drawlib.types import Style

# 1. Hexagon (Kubernetes Pod / Microservice)
regularpolygon((30, 22), num_vertex=6, radius=18, style="blue_flat", text="Pod A")

# 2. Octagon (Security Firewall Boundary)
regularpolygon(
    (70, 22),
    num_vertex=8,
    radius=18,
    angle=22.5,
    style=Style(fill_color=Colors140.Tomato, line_color=Colors140.DarkRed, line_width=2),
    text="WAF",
    textstyle=Style(text_size=12, text_color=Colors140.White),
)
save()

```

---

### 3.7 `polygon`

Draws an arbitrary closed planar polygon through an explicit list of vertices.

#### Signature
```python
def polygon(
    xys: list[tuple[float, float]],
    style: Style | str | None = None,
    text: str = "",
    textsize: float | Literal["small", "medium", "large"] | None = None,
    textstyle: Style | str | None = None,
) -> None:
    ...
```

#### Parameter Breakdown
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xys` | `list[tuple[float, float]]` | *Required* | Sequence of coordinate vertices (minimum 3 points). |
| `style` | `Style \| str \| None` | `None` | Shape fill and line style. |
| `text` | `str` | `""` | Text placed at the centroid / bounding-box center. |
| `textsize` | `float \| str \| None` | `None` | Font size override. |
| `textstyle` | `Style \| str \| None` | `None` | Text formatting style. |

#### Geometric & Alignment Mechanics
- The path automatically closes by connecting the final vertex back to the first vertex.
- **Important**: `polygon` has **no `angle` parameter** and **ignores `text_halign`/`text_valign`**. Vertex coordinates directly dictate orientation and position.

#### Code Examples
```drawlib show-code
from drawlib.canvas import config, save

config(width=100, height=50)
from drawlib.colors import Colors140
from drawlib.shapes import polygon
from drawlib.types import Style

# 1. Irregular network partition boundary
polygon(
    [(10, 15), (25, 35), (45, 30), (40, 10), (20, 8)],
    style=Style(fill_color=Colors140.AliceBlue, line_color=Colors140.SteelBlue, line_width=2),
    text="VLAN 1",
)

# 2. Custom 5-point chevron-like boundary
polygon(
    [(55, 10), (75, 10), (85, 22), (75, 34), (55, 34), (65, 22)],
    style="green_flat",
    text="Route B",
)
save()

```

---

### 3.8 `star`

Draws a symmetric $N$-pointed star with alternating outer peaks and inner valleys.

#### Signature
```python
def star(
    xy: tuple[float, float],
    num_vertex: int,
    radius_ext: float,
    radius_int: float,
    angle: float = 0.0,
    style: Style | str | None = None,
    text: str = "",
    textsize: float | Literal["small", "medium", "large"] | None = None,
    textstyle: Style | str | None = None,
) -> None:
    ...
```

#### Parameter Breakdown
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *Required* | Center coordinate `(x, y)`. |
| `num_vertex` | `int` | *Required* | Number of outer points ($N \ge 3$). Note singular name! |
| `radius_ext` | `float` | *Required* | Outer radius from center to peaks (must be $> \text{radius\_int}$). |
| `radius_int` | `float` | *Required* | Inner radius from center to valleys. |
| `angle` | `float` | `0.0` | Rotation angle CCW around center. |
| `style` | `Style \| str \| None` | `None` | Fill and stroke style. |
| `text` | `str` | `""` | Text label at center. |
| `textsize` | `float \| str \| None` | `None` | Font size override. |
| `textstyle` | `Style \| str \| None` | `None` | Text styling parameters. |

#### Geometric & Alignment Mechanics
- Generates $2N$ alternating vertices around `xy`.
- Strict validation: `radius_ext > radius_int` (raises `ValueError` otherwise).

#### Code Examples
```drawlib show-code
from drawlib.canvas import config, save

config(width=100, height=50)
from drawlib.colors import Colors140
from drawlib.shapes import star
from drawlib.types import Style

# 1. 5-pointed award / milestone badge
star((30, 22), num_vertex=5, radius_ext=18, radius_int=8, style="yellow_flat", text="Star")

# 2. 8-pointed spark / security alert icon
star(
    (70, 22),
    num_vertex=8,
    radius_ext=18,
    radius_int=10,
    angle=22.5,
    style=Style(fill_color=Colors140.LightCoral, line_color=Colors140.FireBrick, line_width=2),
    text="ALERT",
    textstyle=Style(text_size=9, text_color=Colors140.DarkRed),
)
save()

```

---

## 4. Custom Path & Vector Construction

### 4.1 `shape`

Builds an arbitrary vector polygon or curved shape using straight lines, quadratic Beziers, and cubic Beziers.

#### Signature
```python
def shape(
    xy: tuple[float, float],
    path_points: list[
        tuple[float, float]
        | tuple[tuple[float, float], tuple[float, float]]
        | tuple[tuple[float, float], tuple[float, float], tuple[float, float]]
    ],
    is_default_center: bool = False,
    angle: float = 0.0,
    style: Style | str | None = None,
    text: str = "",
    textsize: float | Literal["small", "medium", "large"] | None = None,
    textstyle: Style | str | None = None,
) -> None:
    ...
```

#### Parameter Breakdown
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *Required* | Reference starting point or geometric center. |
| `path_points` | `list[...]` | *Required* | Sequence of relative coordinate offsets or Bezier control tuples. |
| `is_default_center` | `bool` | `False` | If `False`, `xy` is path origin. If `True`, `xy` is centroid. |
| `angle` | `float` | `0.0` | Rotation angle CCW around center. |
| `style` | `Style \| str \| None` | `None` | Shape fill and stroke style. |
| `text` | `str` | `""` | Centered text label. |
| `textsize` | `float \| str \| None` | `None` | Font size override. |
| `textstyle` | `Style \| str \| None` | `None` | Text styling parameters. |

#### Path Point Segment Types
- `path_points` defines polygon vertices in local coordinate space (relative to origin `(0, 0)`). Drawlib automatically computes the bounding box and centers the resulting shape at `xy`.
- **Straight Segment**: `(x, y)` draws a straight line vertex.
- **Quadratic Bezier**: `((cp_x, cp_y), (end_x, end_y))` where `cp` is the control point.
- **Cubic Bezier**: `((cp1_x, cp1_y), (cp2_x, cp2_y), (end_x, end_y))` with two control points.

#### Code Examples
```drawlib show-code
from drawlib.canvas import config, save
from drawlib.colors import Colors, Colors140
from drawlib.shapes import shape
from drawlib.types import Style

config(width=100, height=50)

# 1. Custom pentagonal shield badge
shape(
    xy=(30, 25),
    path_points=[
        (0, 8),
        (0, 26),
        (15, 30),
        (30, 26),
        (30, 8),
        (15, 0),
    ],
    style="blue_flat",
    text="Shield",
    textstyle=Style(text_size=10, text_color=Colors.White),
)

# 2. Smooth symmetric wave tab (Cubic Bezier)
shape(
    xy=(70, 25),
    path_points=[
        (0, 0),
        (0, 15),
        ((10, 25), (20, 5), (30, 15)),      # Cubic wave
        (30, 0),
    ],
    style=Style(fill_color=Colors140.Lavender, line_color=Colors140.Purple, line_width=1.5),
)
save()
```

---

## 5. Directed Block Arrow Shapes

Directed block arrows produce filled 2D planar arrow shapes (not 1D lines).

```text
              head_width
                |<---->|
                +      ^
               /|      |
              / |      | head_length
  tail_width /  |      |
    |<--->| /   +      v
    +-----+    /
    |     |   /
    |     |  /
    |     | /
    +-----+
    xy1          xy2 (tip)
```

---

### 5.1 `arrow`

Draws a straight 2D directed block arrow from `xy1` to `xy2`.

#### Signature
```python
def arrow(
    xy1: tuple[float, float],
    xy2: tuple[float, float],
    tail_width: float | None = None,
    head_width: float | None = None,
    head_length: float | None = None,
    head_angle: float | None = None,
    style: Style | str | None = None,
    text: str = "",
    textsize: float | Literal["small", "medium", "large"] | None = None,
    textstyle: Style | str | None = None,
) -> None:
    ...
```

#### Parameter Breakdown
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy1` | `tuple[float, float]` | *Required* | Base center of the arrow tail `(x1, y1)`. |
| `xy2` | `tuple[float, float]` | *Required* | Coordinate of the arrow tip `(x2, y2)`. |
| `tail_width` | `float \| None` | `None` | Width of the rectangular shaft. Auto-proportioned if `None`. |
| `head_width` | `float \| None` | `None` | Full transverse width of the arrowhead base. |
| `head_length` | `float \| None` | `None` | Axial length of the arrowhead from base to tip. |
| `head_angle` | `float \| None` | `None` | Arrowhead tip angle in degrees (mutually exclusive with `head_length`). |
| `style` | `Style \| str \| None` | `None` | Fill and stroke style. |
| `text` | `str` | `""` | Embedded label rendered along the arrow shaft. |
| `textsize` | `float \| str \| None` | `None` | Font size override. |
| `textstyle` | `Style \| str \| None` | `None` | Text styling parameters. |

#### Geometric & Alignment Mechanics
- The arrow direction and orientation angle are calculated automatically from $\Delta x = x_2 - x_1, \Delta y = y_2 - y_1$.
- `text` is rendered directly along the shaft, automatically rotated parallel to the arrow vector.

#### Code Examples
```drawlib show-code
from drawlib.canvas import config, save

config(width=100, height=50)
from drawlib.colors import Colors140
from drawlib.shapes import arrow
from drawlib.types import Style

# 1. Straight transaction flow arrow with shaft text
arrow((10, 25), (45, 25), tail_width=3, head_width=8, head_length=6, style="blue_flat", text="POST /order")

# 2. Angled response arrow with custom styling
arrow(
    (55, 15),
    (85, 35),
    tail_width=2.5,
    head_width=7,
    head_length=5,
    style=Style(fill_color=Colors140.LightGreen, line_color=Colors140.ForestGreen, line_width=1.5),
    text="200 OK",
    textstyle=Style(text_size=9, text_color=Colors140.DarkGreen),
)
save()

```

---

### 5.2 `arrow_l`

Draws an L-shaped (90-degree orthogonal corner) directed block arrow.

#### Signature
```python
def arrow_l(
    xy: tuple[float, float],
    width: float,
    height: float,
    head_width: float | None = None,
    head_length: float | None = None,
    head_angle: float | None = None,
    tail_width: float | None = None,
    r: float = 0.0,
    angle: float = 0.0,
    style: Style | str | None = None,
) -> None:
    ...
```

#### Parameter Breakdown
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *Required* | Center coordinate `(x, y)` of the bounding box. |
| `width` | `float` | *Required* | Total bounding box width. |
| `height` | `float` | *Required* | Total bounding box height. |
| `head_width` | `float \| None` | `None` | Arrowhead width at the tip end. |
| `head_length` | `float \| None` | `None` | Arrowhead axial length. |
| `head_angle` | `float \| None` | `None` | Tip vertex angle in degrees. |
| `tail_width` | `float \| None` | `None` | Width of the shaft. |
| `r` | `float` | `0.0` | Elbow corner rounding radius ($r \ge 0$). |
| `angle` | `float` | `0.0` | Rotation angle CCW around center. |
| `style` | `Style \| str \| None` | `None` | Fill and stroke style. |

> **Important**: `arrow_l` **does not accept `text`**. Place external `drawlib.text.text()` labels next to the elbow.

#### Code Examples
```drawlib show-code
from drawlib.canvas import config, save

config(width=100, height=50)
from drawlib.colors import Colors140
from drawlib.shapes import arrow_l
from drawlib.types import Style

# 1. Orthogonal L-routing pipe
arrow_l((25, 25), width=30, height=25, tail_width=3, head_width=8, head_length=6, style="blue_flat")

# 2. Rounded elbow L-arrow with custom border
arrow_l(
    (70, 25),
    width=35,
    height=25,
    tail_width=4,
    head_width=10,
    head_length=7,
    r=5,
    style=Style(fill_color=Colors140.MistyRose, line_color=Colors140.Crimson, line_width=2),
)
save()

```

---

### 5.3 `arrow_u`

Draws a U-shaped (180-degree turnaround) directed block arrow.

#### Signature
```python
def arrow_u(
    xy: tuple[float, float],
    width: float,
    height: float,
    head_width: float | None = None,
    head_length: float | None = None,
    head_angle: float | None = None,
    tail_width: float | None = None,
    r: float = 0.0,
    angle: float = 0.0,
    style: Style | str | None = None,
) -> None:
    ...
```

#### Parameter Breakdown
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *Required* | Center coordinate `(x, y)` of the bounding box. |
| `width` | `float` | *Required* | Total bounding box width. |
| `height` | `float` | *Required* | Total bounding box height. |
| `head_width` | `float \| None` | `None` | Arrowhead width. |
| `head_length` | `float \| None` | `None` | Arrowhead axial length. |
| `head_angle` | `float \| None` | `None` | Tip vertex angle in degrees. |
| `tail_width` | `float \| None` | `None` | Width of the shafts. |
| `r` | `float` | `0.0` | Corner rounding radius at turns. |
| `angle` | `float` | `0.0` | Rotation angle CCW around center. |
| `style` | `Style \| str \| None` | `None` | Fill and stroke style. |

> **Important**: `arrow_u` **does not accept `text`**.

#### Code Examples
```drawlib show-code
from drawlib.canvas import config, save

config(width=100, height=50)
from drawlib.colors import Colors140
from drawlib.shapes import arrow_u
from drawlib.types import Style

# 1. Feedback loop return arrow
arrow_u((25, 25), width=25, height=30, tail_width=3, head_width=8, head_length=6, style="green_flat")

# 2. Rotated turnaround retry arrow
arrow_u(
    (70, 25),
    width=28,
    height=32,
    tail_width=3,
    head_width=9,
    head_length=7,
    r=4,
    angle=90,
    style=Style(fill_color=Colors140.Lavender, line_color=Colors140.Purple, line_width=1.5),
)
save()

```

---

### 5.4 `arrow_arc`

Draws a curved circular or elliptical directed block arrow along an angular span.

#### Signature
```python
def arrow_arc(
    xy: tuple[float, float],
    width: float,
    height: float,
    angle_start: float,
    angle_end: float,
    head_width: float | None = None,
    head_length: float | None = None,
    head_angle: float | None = None,
    tail_width: float | None = None,
    angle: float = 0.0,
    style: Style | str | None = None,
) -> None:
    ...
```

#### Parameter Breakdown
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *Required* | Center coordinate `(x, y)` of the arc ellipse. |
| `width` | `float` | *Required* | Horizontal diameter of the ellipse. |
| `height` | `float` | *Required* | Vertical diameter of the ellipse. |
| `angle_start` | `float` | *Required* | Starting angle in degrees CCW. |
| `angle_end` | `float` | *Required* | Ending angle in degrees CCW (location of arrowhead). |
| `head_width` | `float \| None` | `None` | Arrowhead width at the end tip. |
| `head_length` | `float \| None` | `None` | Arrowhead axial length. |
| `head_angle` | `float \| None` | `None` | Tip vertex angle. |
| `tail_width` | `float \| None` | `None` | Width of the curved body shaft. |
| `angle` | `float` | `0.0` | Global rotational shift in degrees. |
| `style` | `Style \| str \| None` | `None` | Fill and stroke style. |

> **Important**: `arrow_arc` **does not accept `text`**.

#### Code Examples
```drawlib show-code
from drawlib.canvas import config, save

config(width=100, height=50)
from drawlib.colors import Colors140
from drawlib.shapes import arrow_arc
from drawlib.types import Style

# 1. Circular process cycle arrow (90 to 0 degrees)
arrow_arc((30, 25), width=30, height=30, angle_start=90, angle_end=0, tail_width=3, head_width=8, style="blue_flat")

# 2. Semi-circular feedback return arrow
arrow_arc(
    (70, 25),
    width=32,
    height=24,
    angle_start=180,
    angle_end=0,
    tail_width=3,
    head_width=8,
    style=Style(fill_color=Colors140.Gold, line_color=Colors140.DarkGoldenRod, line_width=1.5),
)
save()

```

---

### 5.5 `arrow_polyline`

Draws an arbitrary multi-segment polyline directed block arrow with optional rounded corners.

#### Signature
```python
def arrow_polyline(
    xys: list[tuple[float, float]],
    head_width: float | None = None,
    head_length: float | None = None,
    head_angle: float | None = None,
    tail_width: float | None = None,
    r: float = 0.0,
    style: Style | str | None = None,
) -> None:
    ...
```

#### Parameter Breakdown
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xys` | `list[tuple[float, float]]` | *Required* | Sequence of path points. Arrowhead is attached to the final vertex. |
| `head_width` | `float \| None` | `None` | Arrowhead width at final tip. |
| `head_length` | `float \| None` | `None` | Arrowhead axial length. |
| `head_angle` | `float \| None` | `None` | Tip vertex angle. |
| `tail_width` | `float \| None` | `None` | Width of the polyline shaft. |
| `r` | `float` | `0.0` | Corner rounding radius at all intermediate vertex joints. |
| `style` | `Style \| str \| None` | `None` | Fill and stroke style. |

> **Important**: `arrow_polyline` **does not accept `text`** or `angle`.

#### Code Examples
```drawlib show-code
from drawlib.canvas import config, save

config(width=100, height=50)
from drawlib.colors import Colors140
from drawlib.shapes import arrow_polyline
from drawlib.types import Style

# 1. S-curved routing channel with rounded corners
arrow_polyline(
    [(10, 15), (25, 15), (25, 35), (45, 35)],
    tail_width=3,
    head_width=8,
    head_length=6,
    r=3,
    style="blue_flat",
)

# 2. Multi-segment bypass route
arrow_polyline(
    [(55, 10), (70, 10), (70, 25), (85, 25), (85, 40)],
    tail_width=2.5,
    head_width=7,
    head_length=5,
    r=2,
    style=Style(fill_color=Colors140.LightGreen, line_color=Colors140.ForestGreen, line_width=1.5),
)
save()

```

---

### 5.6 `chevron`

Draws an arrow-like pentagonal chevron with an indented rear notch.

#### Signature
```python
def chevron(
    xy: tuple[float, float],
    width: float,
    height: float,
    corner_angle: float = 60.0,
    angle: float = 0.0,
    style: Style | str | None = None,
    text: str = "",
    textsize: float | Literal["small", "medium", "large"] | None = None,
    textstyle: Style | str | None = None,
) -> None:
    ...
```

#### Parameter Breakdown
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *Required* | Center coordinate `(x, y)` of the chevron. |
| `width` | `float` | *Required* | Total horizontal length from rear notch apex to front point. |
| `height` | `float` | *Required* | Total vertical height. |
| `corner_angle` | `float` | `60.0` | Point/notch angle in degrees ($0 < \theta < 180^\circ$). |
| `angle` | `float` | `0.0` | Rotation angle CCW around center. |
| `style` | `Style \| str \| None` | `None` | Fill and stroke style. |
| `text` | `str` | `""` | Embedded text label at center. |
| `textsize` | `float \| str \| None` | `None` | Font size override. |
| `textstyle` | `Style \| str \| None` | `None` | Text styling parameters. |

#### Geometric & Alignment Mechanics
- Centered at `xy`. Rear notch depth and forward point apex match, allowing multiple chevrons to tessellate horizontally into pipeline stages.

#### Code Examples
```drawlib show-code
from drawlib.canvas import config, save
from drawlib.shapes import chevron
from drawlib.types import Style

config(width=100, height=50)

# 1. CI/CD pipeline stage 1
chevron((35, 25), width=30, height=22, corner_angle=60, style="blue_flat", text="Build")

# 2. Consecutive interlocking pipeline stage 2
chevron((68, 25), width=30, height=22, corner_angle=60, style="green_flat", text="Test")
save()
```

---

## 6. Production Architectural Blueprints & Schemas

### 6.1 Cloud Infrastructure Schema (AWS VPC / Multi-Tier)

This pattern illustrates a secure multi-tier virtual private cloud containing public and private subnets, an internet gateway, compute clusters, and a managed database.

```drawlib show-code
from drawlib.canvas import config, save
from drawlib.colors import Colors, Colors140
from drawlib.shapes import arrow, circle, ellipse, rectangle
from drawlib.types import Style

config(width=150, height=90)

# 1. AWS VPC Boundary Enclosure (Centered at (75, 45))
rectangle(
    (75, 45), width=140, height=80, r=4,
    style=Style(fill_color=Colors140.GhostWhite, line_color=Colors140.RoyalBlue, line_width=2, line_style="dashed"),
    text="VPC (10.0.0.0/16)",
    textstyle=Style(text_size=12, text_color=Colors140.RoyalBlue, text_xy_shift=(-45, 34))
)

# 2. Internet Gateway
circle((20, 45), radius=7, style=Style(fill_color=Colors140.MediumPurple, line_color=Colors140.Indigo, line_width=1.5),
       text="IGW", textstyle=Style(text_size=10, text_color=Colors.White))

# 3. Public Web Subnet
rectangle((60, 62), width=48, height=32, r=3,
          style=Style(fill_color=Colors140.HoneyDew, line_color=Colors140.ForestGreen, line_width=1.5),
          text="Public Subnet (DMZ)", textstyle=Style(text_size=10, text_color=Colors140.ForestGreen, text_xy_shift=(-6, 12)))
rectangle((48, 60), width=18, height=14, r=2, style="blue_flat", text="ALB", textstyle=Style(text_size=10, text_color=Colors.White))
rectangle((72, 60), width=18, height=14, r=2, style="blue_flat", text="Nginx", textstyle=Style(text_size=10, text_color=Colors.White))

# 4. Private App Subnet
rectangle((60, 26), width=48, height=32, r=3,
          style=Style(fill_color=Colors140.AliceBlue, line_color=Colors140.SteelBlue, line_width=1.5),
          text="Private App Subnet", textstyle=Style(text_size=10, text_color=Colors140.SteelBlue, text_xy_shift=(-8, 12)))
rectangle((48, 24), width=18, height=14, r=2, style="green_flat", text="Auth\nSvc", textstyle=Style(text_size=9, text_color=Colors.White))
rectangle((72, 24), width=18, height=14, r=2, style="green_flat", text="Order\nSvc", textstyle=Style(text_size=9, text_color=Colors.White))

# 5. Database Tier
rectangle((118, 45), width=45, height=60, r=3,
          style=Style(fill_color=Colors140.MistyRose, line_color=Colors140.IndianRed, line_width=1.5),
          text="Database Tier (Multi-AZ)", textstyle=Style(text_size=10, text_color=Colors140.DarkRed, text_xy_shift=(0, 25)))
ellipse((118, 58), width=30, height=14,
        style=Style(fill_color=Colors140.LightGoldenRodYellow, line_color=Colors140.GoldenRod, line_width=2),
        text="Postgres Primary", textstyle=Style(text_size=9, text_color=Colors.Black))
ellipse((118, 32), width=30, height=14,
        style=Style(fill_color=Colors140.WhiteSmoke, line_color=Colors140.DimGray, line_width=1.5),
        text="Read Replica", textstyle=Style(text_size=9, text_color=Colors.Black))

# 6. Connecting Arrows
arrow((27, 45), (39, 58), tail_width=2, head_width=5, head_length=4, style="gray")
arrow((57, 60), (63, 60), tail_width=2, head_width=5, head_length=4, style="gray")
arrow((72, 53), (72, 31), tail_width=2, head_width=5, head_length=4, style="gray")
arrow((81, 24), (102, 58), tail_width=2, head_width=5, head_length=4, style="gray")

save("cloud_architecture.png")
```

---

### 6.2 Event-Driven Microservices Topology (Kafka / Event Mesh)

Demonstrates message publishers, Kafka message topic queues, consumer groups, and dead-letter queues (DLQ).

```drawlib show-code
from drawlib.canvas import config, save
from drawlib.colors import Colors, Colors140
from drawlib.shapes import arrow, donuts, parallelogram, rectangle
from drawlib.types import Style

config(width=140, height=65)

# Producer
rectangle((20, 32.5), width=24, height=20, r=3, style="blue_flat",
          text="Order\nProducer", textstyle=Style(text_size=11, text_color=Colors.White))

# Event Bus / Kafka Stream Topic (Parallelogram)
parallelogram((64, 32.5), width=40, height=28, corner_angle=70,
              style=Style(fill_color=Colors140.LightSteelBlue, line_color=Colors140.SteelBlue, line_width=2),
              text="orders.events\n(Kafka Topic)", textstyle=Style(text_size=11, text_color=Colors140.MidnightBlue))

# Consumer Group
rectangle((115, 45), width=32, height=18, r=3, style="green_flat",
          text="Payment Worker", textstyle=Style(text_size=10, text_color=Colors.White))
rectangle((115, 20), width=32, height=18, r=3, style="green_flat",
          text="Inventory Worker", textstyle=Style(text_size=10, text_color=Colors.White))

# Dead Letter Queue (Donuts)
donuts((64, 9), radius=6, width=2,
       style=Style(fill_color=Colors140.IndianRed, line_color=Colors140.DarkRed, line_width=1.5),
       text="DLQ", textstyle=Style(text_size=8, text_color=Colors140.DarkRed))

# Event Flow Arrows
arrow((32, 32.5), (44, 32.5), tail_width=3, head_width=7, head_length=5, style="blue")
arrow((84, 38), (99, 45), tail_width=2.5, head_width=6, head_length=4, style="green")
arrow((84, 27), (99, 20), tail_width=2.5, head_width=6, head_length=4, style="green")
arrow((99, 15), (71, 9), tail_width=2, head_width=5, head_length=4, style="red_dashed")

save("event_mesh_architecture.png")
```

---

### 6.3 Deep Neural Network Layer Graph (CNN / ResNet Skip Connection)

Demonstrates convolution, pooling, batch normalization, and skip residual connections in machine learning architectures.

```drawlib show-code
from drawlib.canvas import config, save
from drawlib.colors import Colors, Colors140
from drawlib.shapes import arrow, arrow_polyline, circle, rectangle, trapezoid
from drawlib.types import Style

config(width=150, height=55)

# Input Tensor
rectangle((16, 25), width=18, height=22,
          style=Style(fill_color=Colors140.LightGray, line_color=Colors140.DimGray, line_width=1.5),
          text="Input\n3x224x224", textstyle=Style(text_size=8, text_color=Colors.Black))

# Conv2D Layer
rectangle((42, 25), width=20, height=28, r=2, style="blue_flat",
          text="Conv2D\n64 filters", textstyle=Style(text_size=9, text_color=Colors.White))

# Batch Norm & ReLU
rectangle((68, 25), width=18, height=22, r=2, style="green_flat",
          text="BN +\nReLU", textstyle=Style(text_size=9, text_color=Colors.White))

# Conv2D Layer 2
rectangle((92, 25), width=20, height=28, r=2, style="blue_flat",
          text="Conv2D\n64 filters", textstyle=Style(text_size=9, text_color=Colors.White))

# Residual Elementwise Add Node
circle((114, 25), radius=4.5,
       style=Style(fill_color=Colors140.LightGoldenRodYellow, line_color=Colors140.GoldenRod, line_width=1.5),
       text="+", textstyle=Style(text_size=12, text_color=Colors.Black))

# Max Pooling (Trapezoid)
trapezoid((134, 25), height=20, bottomedge_width=22, topedge_width=14, style="red_flat",
          text="Pool\n/2", textstyle=Style(text_size=8, text_color=Colors.White))

# Forward Feed Connections
arrow((25, 25), (32, 25), tail_width=1.5, head_width=4, head_length=3, style="gray")
arrow((52, 25), (59, 25), tail_width=1.5, head_width=4, head_length=3, style="gray")
arrow((77, 25), (82, 25), tail_width=1.5, head_width=4, head_length=3, style="gray")
arrow((102, 25), (109.5, 25), tail_width=1.5, head_width=4, head_length=3, style="gray")
arrow((118.5, 25), (123, 25), tail_width=1.5, head_width=4, head_length=3, style="gray")

# ResNet Residual Skip Connection (arrow_polyline)
arrow_polyline(
    [(42, 39), (42, 47), (114, 47), (114, 29.5)],
    tail_width=1.5, head_width=4, head_length=3, r=3,
    style=Style(fill_color=Colors140.DarkOrange, line_color=Colors140.DarkOrange)
)

save("cnn_resnet_architecture.png")
```

---

### 6.4 UML State Machine Diagram

Constructs a standard UML state chart featuring initial pseudo-states, rounded composite states, guard conditions, and terminal states.

```drawlib show-code
from drawlib.canvas import config, save
from drawlib.colors import Colors, Colors140
from drawlib.shapes import arrow, circle, donuts, rectangle, rhombus
from drawlib.types import Style

config(width=150, height=60)

# Initial State
circle((15, 30), radius=5, style=Style(fill_color=Colors.Black, line_width=0))

# State 1: Draft
rectangle((40, 30), width=26, height=20, r=5, style="blue_flat",
          text="DRAFT", textstyle=Style(text_size=10, text_color=Colors.White))

# Choice Decision Pseudostate (Rhombus)
rhombus((70, 30), width=18, height=18, style="yellow_flat")

# State 2: Published
rectangle((104, 43), width=26, height=18, r=5, style="green_flat",
          text="PUBLISHED", textstyle=Style(text_size=9, text_color=Colors.White))

# State 3: Rejected
rectangle((104, 17), width=26, height=18, r=5, style="red_flat",
          text="REJECTED", textstyle=Style(text_size=9, text_color=Colors.White))

# Terminal State (Bullseye / Donut with inner circle)
donuts((136, 30), radius=6, width=1.5, style=Style(fill_color=Colors.Black, line_width=0))
circle((136, 30), radius=3.5, style=Style(fill_color=Colors.Black, line_width=0))

# Transitions
arrow((20, 30), (27, 30), tail_width=1.5, head_width=4, head_length=3, style="gray")
arrow((53, 30), (61, 30), tail_width=1.5, head_width=4, head_length=3, style="gray")
arrow((78, 35), (91, 43), tail_width=1.5, head_width=4, head_length=3, text="Valid", textstyle=Style(text_size=8), style="green")
arrow((78, 25), (91, 17), tail_width=1.5, head_width=4, head_length=3, text="Invalid", textstyle=Style(text_size=8), style="red")
arrow((117, 43), (130, 33), tail_width=1.5, head_width=4, head_length=3, style="gray")
arrow((117, 17), (130, 27), tail_width=1.5, head_width=4, head_length=3, style="gray")

save("state_machine_schema.png")
```

---

### 6.5 Modern Dashboard UI Component Kit (Cards, Badges, Metrics)

Demonstrates how human designers and AI coding agents can construct crisp application user interfaces, modals, and KPI telemetry cards using Drawlib primitives.

```drawlib show-code
from drawlib.canvas import config, save
from drawlib.colors import Colors, Colors140
from drawlib.shapes import arc, circle, rectangle
from drawlib.types import Style

config(width=140, height=75)

# Outer Dashboard Frame
rectangle((70, 37.5), width=130, height=65, r=4,
          style=Style(fill_color=Colors140.WhiteSmoke, line_color=Colors140.LightGray, line_width=1.5))

# KPI Card 1: Server Load
rectangle((28, 37.5), width=36, height=50, r=3,
          style=Style(fill_color=Colors.White, line_color=Colors140.Gainsboro, line_width=1),
          text="CPU LOAD\n\n42%", textstyle=Style(text_size=12, text_color=Colors140.DarkSlateGray, text_xy_shift=(0, -8)))
arc((28, 48), width=20, height=20, angle_start=0, angle_end=220,
    style=Style(line_color=Colors140.DodgerBlue, line_width=3))

# KPI Card 2: Memory Usage
rectangle((70, 37.5), width=36, height=50, r=3,
          style=Style(fill_color=Colors.White, line_color=Colors140.Gainsboro, line_width=1),
          text="MEMORY\n\n78%", textstyle=Style(text_size=12, text_color=Colors140.DarkSlateGray, text_xy_shift=(0, -8)))
arc((70, 48), width=20, height=20, angle_start=0, angle_end=280,
    style=Style(line_color=Colors140.MediumSeaGreen, line_width=3))

# KPI Card 3: Network Status
rectangle((112, 37.5), width=36, height=50, r=3,
          style=Style(fill_color=Colors.White, line_color=Colors140.Gainsboro, line_width=1),
          text="NETWORK\n\nActive", textstyle=Style(text_size=12, text_color=Colors140.DarkSlateGray, text_xy_shift=(0, -8)))
circle((112, 48), radius=6,
       style=Style(fill_color=Colors140.PaleGreen, line_color=Colors140.ForestGreen, line_width=2))

save("dashboard_ui_kit.png")
```

---

## 7. Quick Reference Matrix & Troubleshooting

### 7.1 Function Capabilities Matrix

| Function | Default Anchor | Primary Dimensions | Corner Radius `r` | Rotation `angle` | Supports `text` | Ignores `halign/valign` |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| `circle` | Center `(x, y)` | `radius` | No | Yes (text) | Yes | No |
| `donuts` | Center `(x, y)` | `radius`, `width` | No | Yes (text) | Yes | No |
| `ellipse`| Center `(x, y)` | `width`, `height` | No | Yes | Yes | No |
| `wedge`  | Center `(x, y)` | `radius`, `width`, `angle_start/end` | No | Yes | Yes | No |
| `fan`    | Center `(x, y)` | `radius`, `angle_start/end` | No | Yes | Yes | No |
| `arc`    | Center `(x, y)` | `width`, `height`, `angle_start/end` | No | Yes | Yes | No |
| `rectangle` | Center `(x, y)` | `width`, `height` | **Yes** | Yes | Yes | No |
| `parallelogram` | Center `(x, y)` | `width`, `height`, `corner_angle` | No | Yes | Yes | No |
| `rhombus` | Center `(x, y)` | `width`, `height` | No | Yes | Yes | No |
| `trapezoid` | Center `(x, y)` | `height`, `bottomedge_width`, `topedge_width` | No | Yes | Yes | No |
| `triangle` | Center `(x, y)` | `width`, `height`, `topvertex_x` | No | Yes | Yes | No |
| `regularpolygon` | Center `(x, y)` | `num_vertex`, `radius` | No | Yes | Yes | No |
| `polygon` | Vertices `xys` | `xys: list[tuple[float, float]]` | No | **No** | Yes | **Yes** |
| `star` | Center `(x, y)` | `num_vertex`, `radius_ext`, `radius_int` | No | Yes | Yes | No |
| `shape` | Center `(x, y)` | `path_points` | Via Bezier | Yes | Yes | No |
| `arrow` | Endpoints `xy1, xy2` | `tail_width`, `head_width`, `head_length` | No | Auto ($\Delta xy$) | Yes | **Yes** |
| `arrow_polyline` | Vertices `xys` | `tail_width`, `head_width`, `head_length` | **Yes** | Path-driven | **No** | **Yes** |
| `arrow_arc` | Center `(x, y)` | `width`, `height`, `head_angle` | No | Yes | **No** | **Yes** |
| `arrow_l` | Center `(x, y)` | `width`, `height`, head/tail dims | **Yes** | Yes | **No** | **Yes** |
| `arrow_u` | Center `(x, y)` | `width`, `height`, head/tail dims | **Yes** | Yes | **No** | **Yes** |
| `chevron` | Center `(x, y)` | `width`, `height`, `corner_angle` | No | Yes | Yes | No |

---

### 7.2 Common Pitfalls & Resolution Rules

1. **Passing `text` to Arrow Subtypes**:
   - *Error / Ignored*: `arrow_polyline`, `arrow_l`, `arrow_u`, and `arrow_arc` **do not accept** `text` or `textstyle`.
   - *Resolution*: Only straight `arrow()` accepts embedded `text`. For other arrows, place a dedicated `drawlib.text.text(xy, "label")` at the desired position.
2. **`trapezoid()` Parameter Names**:
   - *Error*: Passing `width=...` to `trapezoid()`.
   - *Resolution*: `trapezoid()` requires `height`, `bottomedge_width`, and `topedge_width`. There is no `width` argument.
3. **`star()` Radius Order Constraint**:
   - *Error*: `ValueError("radius_ext must be bigger than radius_int.")`
   - *Resolution*: Ensure `radius_ext > radius_int`.
4. **Vertex Count Argument Naming**:
   - *Error*: Passing `num_vertices=...` to `regularpolygon()` or `star()`.
   - *Resolution*: The parameter is singular: `num_vertex` (e.g., `num_vertex=6`).
5. **No Border vs Transparent Fill**:
   - To remove a shape border: set `line_width=0`.
   - To make the interior transparent: set `fill_color=Colors.Transparent` or `fill_alpha=0.0`.
6. **Centering Text in Asymmetric Shapes**:
   - For `triangle()` and `trapezoid()`, the default bounding-box center may place text too close to narrow edges. Use `textstyle=Style(text_xy_shift=(dx, dy))` to nudge the text into visual balance.
7. **Orientation in `polygon()`**:
   - `polygon()` derives its orientation entirely from vertex order in `xys` and has no `angle` parameter. To rotate a custom polygon, use `shape(xy, path_points, angle=...)`.
