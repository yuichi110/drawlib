# Drawlib Shapes Guidelines

Comprehensive architectural manual and API specification for `drawlib.shapes`. This guide details all 24 shape primitives, coordinate geometry, alignment engines, vector construction rules, and production diagram patterns.

---

## Table of Contents

- [1. Architectural Overview & Core Mechanics](#1-architectural-overview--core-mechanics)
  - [1.1 Package Facade & Exports](#11-package-facade--exports)
  - [1.2 Canvas Coordinate Space & The Cartesian Model](#12-canvas-coordinate-space--the-cartesian-model)
  - [1.3 Geometric Anchors: Center vs. Bottom-Left Origins](#13-geometric-anchors-center-vs-bottom-left-origins)
  - [1.4 Alignment Transformation Engine (`halign` & `valign`)](#14-alignment-transformation-engine-halign--valign)
  - [1.5 Rotation Coordinate Mathematics](#15-rotation-coordinate-mathematics)
  - [1.6 The Unified Styling System (`Style`)](#16-the-unified-styling-system-style)
  - [1.7 Embedded Text Rendering & Micro-Offsets (`text_style`)](#17-embedded-text-rendering--micro-offsets-text_style)
- [2. Circle-like Shapes](#2-circle-like-shapes)
  - [2.1 `circle`](#21-circle)
  - [2.2 `donuts`](#22-donuts)
  - [2.3 `ellipse`](#23-ellipse)
  - [2.4 `wedge`](#24-wedge)
  - [2.5 `fan`](#25-fan)
  - [2.6 `arc`](#26-arc)
  - [2.7 `cylinder`](#27-cylinder)
  - [2.8 `face`](#28-face)
- [3. Polygon & Planar Geometric Primitives](#3-polygon--planar-geometric-primitives)
  - [3.1 `rectangle`](#31-rectangle)
  - [3.2 `parallelogram`](#32-parallelogram)
  - [3.3 `rhombus`](#33-rhombus)
  - [3.4 `trapezoid`](#34-trapezoid)
  - [3.5 `triangle`](#35-triangle)
  - [3.6 `regularpolygon`](#36-regularpolygon)
  - [3.7 `polygon`](#37-polygon)
  - [3.8 `star`](#38-star)
  - [3.9 `bubblespeech`](#39-bubblespeech)
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

The `drawlib.shapes` module re-exports 24 functions implemented across internal canvas engines (`drawlib._core.l4_canvas._shapes`).

```python
from drawlib.shapes import (
    arc,
    arrow,
    arrow_arc,
    arrow_l,
    arrow_polyline,
    arrow_u,
    bubblespeech,
    chevron,
    circle,
    cylinder,
    donuts,
    ellipse,
    face,
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

Every shape function is decorated with `@validate_call`, providing runtime type validation, parameter constraint verification, and uniform error reporting.

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
   - Functions: `circle`, `cylinder`, `donuts`, `ellipse`, `face`, `wedge`, `fan`, `arc`, `regularpolygon`, `star`, `arrow_l`, `arrow_u`, `arrow_arc`.
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

When positioning shapes relative to layout grids or text baselines, you can override default anchor behavior by setting `halign` and `valign` on the shape's `Style`:

| Alignment Attribute | Valid Options | Default for Center Shapes | Default for Bounding-Box Shapes |
| :--- | :--- | :--- | :--- |
| `halign` | `"left"`, `"center"`, `"right"` | `"center"` | `"center"` (if `style.angle != 0`) / `"left"` (if unrotated) |
| `valign` | `"bottom"`, `"center"`, `"top"` | `"center"` | `"center"` (if `style.angle != 0`) / `"bottom"` (if unrotated) |

#### Transformation Mathematics
For a shape with unrotated width $W$ and height $H$, the internal alignment engine shifts the anchor coordinates `(x, y)` according to the following formulas:

- **For Center-Anchored Shapes (`is_default_center = True`)**:
  - Horizontal: `"left"`: $x' = x + \frac{W}{2}$ | `"center"`: $x' = x$ | `"right"`: $x' = x - \frac{W}{2}$
  - Vertical: `"bottom"`: $y' = y + \frac{H}{2}$ | `"center"`: $y' = y$ | `"top"`: $y' = y - \frac{H}{2}$

- **For Bottom-Left Anchored Shapes (`is_default_center = False`)**:
  - Horizontal: `"left"`: $x' = x$ | `"center"`: $x' = x - \frac{W}{2}$ | `"right"`: $x' = x - W$
  - Vertical: `"bottom"`: $y' = y$ | `"center"`: $y' = y - \frac{H}{2}$ | `"top"`: $y' = y - H$

> **Important**: `arrow`, `arrow_polyline`, and `polygon` compute vertices directly from coordinate vectors and **ignore** `halign` and `valign`.

---

### 1.5 Rotation Coordinate Mathematics

All shapes supporting `style.angle` rotate counterclockwise around the shape's **geometric center $(C_x, C_y)$**.
Even for shapes anchored at the bottom-left, the center is computed first as $C = (x + W/2, y + H/2)$, rotated by $\theta = \text{radians}(\text{style.angle})$, and the vertices are transformed:

$$x_{\text{rot}} = (x - C_x)\cos\theta - (y - C_y)\sin\theta + C_x$$
$$y_{\text{rot}} = (x - C_x)\sin\theta + (y - C_y)\cos\theta + C_y$$

Embedded shape text rotates alongside the shape by default, maintaining its relative orientation inside the shape boundary.

---

### 1.6 The Unified Styling System (`Style`)

Shape styling is driven by Drawlib's core `Style` model directly imported from `drawlib.styles.Styles` (e.g., `Styles.Primary`, `Styles.SecondaryFlat`, `Styles.AccentBold`) or custom `Style` instances.

```python
from drawlib.preset_colors import CssColors
from drawlib.types import Style

custom_shape_style = Style(
    shape_fill_color=CssColors.AliceBlue,      # Interior fill color (RGB, RGBA, or hex)
    alpha=0.85,                                # Opacity float: 0.0 (transparent) to 1.0 (opaque)
    shape_line_color=CssColors.SteelBlue,      # Stroke boundary color
    shape_line_width=2.5,                      # Stroke thickness in points (0 disables border)
    shape_line_style="dashed",                 # "solid" | "dashed" | "dotted" | "dashdot"
    halign="center",                      # Layout horizontal anchor
    valign="center",                      # Layout vertical anchor
)
```

#### System Defaults (`SYSTEM_DEFAULT_SHAPE_STYLE`)
Unless overridden, all shapes inherit these baseline attributes:
- `shape_fill_color`: `Colors.White` `(255, 255, 255)`
- `alpha`: `1.0` (fully opaque)
- `shape_line_color`: `Colors.Black` `(0, 0, 0)`
- `shape_line_width`: `1.0`
- `shape_line_style`: `"solid"`
- `halign`: `"center"`
- `valign`: `"center"`

To eliminate a shape's border line entirely, explicitly set `shape_line_width=0`. To make a shape interior hollow/transparent, pass `shape_fill_color=Colors.Transparent`.

---

### 1.7 Embedded Text Rendering & Micro-Offsets (`text_style`)

Almost all shapes accept `text` and `text_style` parameters.
- Text is automatically rendered at the centroid $(C_x, C_y)$ of the shape.
- Text automatically rotates with the shape's `style.angle` unless overridden by `angle` in `text_style`.
- Text styling and font size can be customized through `text_style=Style(text_size=...)` or by patching preset styles like `Styles.WhiteBold.patch(text_size=...).`

```python
from drawlib.fonts import FontRoboto
from drawlib.preset_colors import CssColors
from drawlib.types import Style

custom_text_style = Style(
    text_color=CssColors.MidnightBlue,
    text_size=18,
    text_font=FontRoboto.ROBOTO_BOLD,
    angle=0.0,                       # Freeze text horizontally even if shape rotates
    text_flip=False,                 # Invert 180 degrees if True
    xy_shift=(0.0, -3.0),            # Relative micro-adjustment offset (dx, dy)
)
```

#### Shift Semantics
- `xy_shift=(dx, dy)`: Moves the text relative to the shape's coordinate system. If the shape is rotated, the offset vector $(dx, dy)$ rotates with it.
- `xy_abs_shift=(dx, dy)`: Moves the text along the absolute, unrotated canvas axes.

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
    *,
    style: Style | None = None,
    text: str = "",
    text_style: Style | None = None,
) -> None:
    ...
```

#### Parameter Breakdown
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *Required* | Center coordinate `(x, y)`. |
| `radius` | `float` | *Required* | Radius of the circle (must be $> 0$). |
| `style` | `Style \| None` | `None` | `Style` instance (supports `angle` to rotate embedded text). |
| `text` | `str` | `""` | Text label drawn at the circle center. |
| `text_style` | `Style \| None` | `None` | `Style` instance for text formatting. |

#### Geometric & Alignment Mechanics
- **Anchor**: Geometric center `(x, y)`.
- Bounding box is $2r \times 2r$.
- Setting `style.halign="left"` shifts the circle so that `x` aligns with its left tangent boundary ($x' = x + r$).
- `style.angle` does not alter the appearance of a symmetric circle, but rotates embedded text around the center point.

#### Code Examples
```drawlib show-code
from drawlib.canvas import save, setup

setup(width=100, height=50)
from drawlib.preset_colors import CssColors
from drawlib.shapes import circle
from drawlib.types import Style
from drawlib.styles import Styles

# 1. Solid status node with embedded label
circle((30, 25), radius=14, style=Styles.GreenFlat, text="OK", text_style=Styles.WhiteBold.patch(text_size=14))

# 2. Semi-transparent dashed boundary zone with rotated label
circle(
    (70, 25),
    radius=18,
    style=Styles.Primary.patch(
        shape_fill_color=CssColors.DeepSkyBlue,
        alpha=0.3,
        shape_line_style="dashed",
        shape_line_width=2,
        angle=35,
    ),
    text="Zone B",
    text_style=Styles.Primary.patch(text_color=CssColors.Navy, text_size=12),
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
    *,
    style: Style | None = None,
    text: str = "",
    text_style: Style | None = None,
) -> None:
    ...
```

#### Parameter Breakdown
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *Required* | Center coordinate `(x, y)`. |
| `radius` | `float` | *Required* | Outer radius of the annular ring. |
| `width` | `float \| None` | `None` | Ring wall thickness. Inner radius = $\text{radius} - \text{width}$. If `None`, renders solid. |
| `style` | `Style \| None` | `None` | Shape fill and stroke configuration (supports `angle`). |
| `text` | `str` | `""` | Label rendered in the center void of the donut. |
| `text_style` | `Style \| None` | `None` | Text styling parameters. |

#### Geometric & Alignment Mechanics
- Built on top of `wedge(..., angle_start=0, angle_end=360)`.
- If `width >= radius`, the inner radius collapses to 0 or becomes invalid. Ensure $0 < \text{width} < \text{radius}$.
- Center text is positioned in the hollow central core.

#### Code Examples
```drawlib show-code
from drawlib.canvas import save, setup

setup(width=100, height=50)
from drawlib.preset_colors import CssColors
from drawlib.shapes import donuts
from drawlib.types import Style
from drawlib.styles import Styles

# 1. Thin status indicator ring
donuts((30, 22), radius=15, width=4, style=Styles.MutedFlat, text="Base")

# 2. KPI ring badge with custom fill and styled percentage label
donuts(
    (70, 22),
    radius=17,
    width=6,
    style=Styles.Primary.patch(
        shape_fill_color=CssColors.Purple, shape_line_color=CssColors.Indigo, shape_line_width=2
    ),
    text="78%",
    text_style=Styles.WhiteBold.patch(text_size=14, text_color=CssColors.White),
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
    *,
    style: Style | None = None,
    text: str = "",
    text_style: Style | None = None,
) -> None:
    ...
```

#### Parameter Breakdown
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *Required* | Center coordinate `(x, y)`. |
| `width` | `float` | *Required* | Total horizontal axis diameter before rotation. |
| `height` | `float` | *Required* | Total vertical axis diameter before rotation. |
| `style` | `Style \| None` | `None` | Shape style object (supports `angle` for rotation around `xy`). |
| `text` | `str` | `""` | Centered text annotation. |
| `text_style` | `Style \| None` | `None` | Text formatting style. |

#### Geometric & Alignment Mechanics
- Semi-major axis $a = \text{width} / 2$, Semi-minor axis $b = \text{height} / 2$.
- When rotated by `style.angle`, the ellipse and its text rotate synchronously.
- Widely used for database entities (ER diagrams), start/end states in flowcharts, and distributed cache clusters.

#### Code Examples
```drawlib show-code
from drawlib.canvas import save, setup

setup(width=100, height=50)
from drawlib.preset_colors import CssColors
from drawlib.shapes import ellipse
from drawlib.types import Style
from drawlib.styles import Styles

# 1. Database schema entity
ellipse((30, 22), width=36, height=20, style=Styles.YellowFlat, text="users_tbl")

# 2. Rotated processing stage node with dashed boundary
ellipse(
    (70, 22),
    width=38,
    height=18,
    style=Styles.Primary.patch(
        shape_fill_color=CssColors.AliceBlue,
        shape_line_color=CssColors.SteelBlue,
        shape_line_style="dashed",
        shape_line_width=2,
        angle=335,
    ),
    text="In-Flight Job",
    text_style=Styles.Primary.patch(text_size=11, text_color=CssColors.Navy),
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
    *,
    style: Style | None = None,
    text: str = "",
    text_style: Style | None = None,
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
| `style` | `Style \| None` | `None` | Shape fill and outline style (supports `angle` for global rotational shift). |
| `text` | `str` | `""` | Centered text label. |
| `text_style` | `Style \| None` | `None` | Style instance for text formatting. |

#### Geometric & Alignment Mechanics
- Draws CCW from `angle_start` to `angle_end`.
- If `width` is given, inner radius $r_{\text{in}} = \text{radius} - \text{width}$, forming a curved circular band segment.
- Ideal for custom gauge meters, donut chart slices, and progress wheels.

#### Code Examples
```drawlib show-code
from drawlib.canvas import save, setup

setup(width=100, height=50)
from drawlib.preset_colors import CssColors
from drawlib.shapes import wedge
from drawlib.types import Style
from drawlib.styles import Styles

# 1. Quarter gauge ring slice with thickness
wedge((30, 22), radius=18, angle_start=0, angle_end=90, width=5, style=Styles.BlueFlat, text="Q1")

# 2. Rotated multi-segment slice with border stroke
wedge(
    (70, 22),
    radius=18,
    angle_start=45,
    angle_end=225,
    width=6,
    style=Styles.Primary.patch(
        shape_fill_color=CssColors.Orange,
        shape_line_color=CssColors.DarkRed,
        shape_line_width=1.5,
        angle=15,
    ),
    text="60%",
    text_style=Styles.WhiteBold.patch(text_size=11, text_color=CssColors.White),
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
    *,
    style: Style | None = None,
    text: str = "",
    text_style: Style | None = None,
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
| `style` | `Style \| None` | `None` | Shape fill and line style (supports `angle` for rotational offset). |
| `text` | `str` | `""` | Centered text label. |
| `text_style` | `Style \| None` | `None` | Text formatting style. |

#### Geometric & Alignment Mechanics
- Functionally equivalent to `wedge(..., width=None)`.
- Vertex at `xy` connects via two radial edges to the arc endpoints.
- Perfect for radar vision cones, camera field-of-view indicators, and pie chart segments.

#### Code Examples
```drawlib show-code
from drawlib.canvas import save, setup

setup(width=100, height=50)
from drawlib.preset_colors import CssColors
from drawlib.shapes import fan
from drawlib.types import Style
from drawlib.styles import Styles

# 1. Radar scanner coverage cone
fan(
    (30, 15),
    radius=25,
    angle_start=30,
    angle_end=150,
    style=Styles.Primary.patch(
        shape_fill_color=CssColors.LightGreen,
        alpha=0.4,
        shape_line_color=CssColors.ForestGreen,
        shape_line_width=1.5,
    ),
    text="FOV",
)

# 2. Semi-circle gauge backdrop
fan((75, 15), radius=22, angle_start=0, angle_end=180, style=Styles.BlueFlat, text="Upper Range")
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
    *,
    style: Style | None = None,
    text: str = "",
    text_style: Style | None = None,
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
| `style` | `Style \| None` | `None` | Stroke styling (`line_color`, `line_width`, `line_style`, `angle`). |
| `text` | `str` | `""` | Centered text label at `xy`. |
| `text_style` | `Style \| None` | `None` | Text style parameters. |

#### Geometric & Alignment Mechanics
- Unlike `wedge`, `arc` is strictly a 1D stroke boundary line. Any `fill_color` is ignored.
- Set `line_width` to control thickness; set `line_style="dashed"` or `"dotted"` for trajectories.

#### Code Examples
```drawlib show-code
from drawlib.canvas import save, setup

setup(width=100, height=50)
from drawlib.preset_colors import CssColors
from drawlib.shapes import arc
from drawlib.types import Style
from drawlib.styles import Styles

# 1. Curved relationship bracket
arc(
    (30, 22),
    width=30,
    height=20,
    angle_start=30,
    angle_end=150,
    style=Styles.PrimaryBold.patch(line_color=CssColors.Navy, line_width=3),
)

# 2. Dashed orbit path with centered status label
arc(
    (70, 22),
    width=32,
    height=24,
    angle_start=315,
    angle_end=225,
    style=Styles.PrimaryBold.patch(
        line_color=CssColors.Crimson, line_width=2, line_style="dashed", angle=15
    ),
    text="Orbit A",
    text_style=Styles.Primary.patch(text_size=10, text_color=CssColors.Crimson),
)
save()
```

---

### 2.7 `cylinder`

Draws a 3D-shaded cylinder shape with an elliptical top cap and optional multi-disk horizontal divider rings, ideal for databases, storage volumes, data lakes, and message queues.

#### Signature
```python
def cylinder(
    xy: tuple[float, float],
    width: float,
    height: float,
    *,
    style: Style | None = None,
    disks: int = 1,
    text: str = "",
    text_style: Style | None = None,
) -> None:
    ...
```

#### Parameter Breakdown
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *Required* | Center coordinate `(x, y)` of the cylinder. |
| `width` | `float` | *Required* | Total horizontal width ($> 0$). |
| `height` | `float` | *Required* | Total vertical height including top/bottom caps ($> 0$). |
| `style` | `Style \| None` | `None` | Shape fill and stroke style (supports `angle=90` or `-90` for horizontal pipes/queues). Top cap is automatically lightened for 3D depth. |
| `disks` | `int` | `1` | Number of stacked storage disks ($\ge 1$). Values $> 1$ render curved divider seams. |
| `text` | `str` | `""` | Embedded text label centered on the cylinder body. |
| `text_style` | `Style \| None` | `None` | Text formatting style. |

#### Geometric & Alignment Mechanics
- Default coordinate `xy` is the geometric center of the cylinder.
- The top elliptical cap automatically computes a lighter tint from `style.shape_fill_color` to provide clean 3D visual depth even on flat styles (`Styles.PrimaryFlat`).
- Setting `disks=3` divides the cylinder body into 3 stacked storage tiers.

#### Code Examples
```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.shapes import cylinder
from drawlib.styles import Styles

setup(width=120, height=50)

# 1. Single-disk database cylinder (Primary hero anchor)
cylinder((30, 25), width=26, height=32, style=Styles.PrimaryFlat, text="Users DB", text_style=Styles.WhiteBold)

# 2. Multi-disk storage cluster (3 disks, calm tinted-neutral card)
cylinder((80, 25), width=28, height=34, disks=3, style=Styles.SecondaryNeutral, text="Data Lake")
save()
```

---

### 2.8 `face`

Draws an expressive face circle with eyes, optional eyebrows, and a configurable facial expression (`mood`), ideal for actors, user personas, customer journey states, and incident/health indicators.

#### Signature
```python
def face(
    xy: tuple[float, float],
    radius: float,
    *,
    style: Style | None = None,
    mood: Literal["smile", "neutral", "sad", "angry", "surprised"] = "smile",
    text: str = "",
    text_style: Style | None = None,
) -> None:
    ...
```

#### Parameter Breakdown
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *Required* | Center coordinate `(x, y)` of the face circle. |
| `radius` | `float` | *Required* | Radius of the face circle ($> 0$). |
| `style` | `Style \| None` | `None` | Shape fill and stroke style (supports `angle`). Eyes and mouth automatically derive their color from `shape_line_color` (or contrasting `text_color`/white on flat styles). |
| `mood` | `str` | `"smile"` | Facial expression: `"smile"`, `"neutral"`, `"sad"`, `"angry"`, or `"surprised"`. |
| `text` | `str` | `""` | Embedded text label (can be shifted below the face using `xy_shift`). |
| `text_style` | `Style \| None` | `None` | Text formatting style. |

#### Code Examples
```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.shapes import face
from drawlib.styles import Styles

setup(width=120, height=45)

face((20, 22.5), radius=10, style=Styles.SuccessNeutral, mood="smile")
face((50, 22.5), radius=10, style=Styles.Neutral, mood="neutral")
face((80, 22.5), radius=10, style=Styles.WarningNeutral, mood="sad")
face((105, 22.5), radius=10, style=Styles.DangerNeutral, mood="angry")
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
    *,
    style: Style | None = None,
    text: str = "",
    text_style: Style | None = None,
) -> None:
    ...
```

##### Parameter Breakdown
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *Required* | Center coordinate `(x, y)` of the rectangle. |
| `width` | `float` | *Required* | Width along horizontal axis (must be $> 0$). |
| `height` | `float` | *Required* | Height along vertical axis (must be $> 0$). |
| `style` | `Style \| None` | `None` | Fill, stroke, and corner radius style (`style.shape_r` as a scalar or 4-tuple `(bottom_left, top_left, top_right, bottom_right)`). |
| `text` | `str` | `""` | Embedded center text label. |
| `text_style` | `Style \| None` | `None` | Text formatting style. |

#### Geometric & Alignment Mechanics
- Default coordinate `xy` is the geometric center of the shape.
- Corner rounding via `style.shape_r` constructs smooth quadratic Bezier transitions at each vertex (accepts a scalar `float` or a 4-tuple of radii per vertex).
- Fundamental building block for system architecture diagrams, UI cards, and network topologies.

#### Code Examples
```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.preset_colors import CssColors
from drawlib.shapes import rectangle
from drawlib.types import Style
from drawlib.styles import Styles

setup(width=100, height=50)

# 1. API gateway block with sharp corners
rectangle((28, 25), width=35, height=20, style=Styles.BlueFlat, text="API Gateway", text_style=Styles.WhiteBold.patch(text_size=11))

# 2. Rounded worker card with dashed border
rectangle(
    (72, 25),
    width=35,
    height=20,
    style=Styles.Primary.patch(
        shape_fill_color=CssColors.GhostWhite,
        shape_line_color=CssColors.SlateGray,
        shape_line_width=2,
        shape_line_style="dashed",
        shape_r=4,
    ),
    text="Worker Node",
    text_style=Styles.Primary.patch(text_color=CssColors.MidnightBlue, text_size=11),
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
    *,
    style: Style | None = None,
    text: str = "",
    text_style: Style | None = None,
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
| `style` | `Style \| None` | `None` | Shape fill and stroke style (supports `angle` for rotation). |
| `text` | `str` | `""` | Centered text label. |
| `text_style` | `Style \| None` | `None` | Text formatting style. |

#### Geometric & Alignment Mechanics
- Centered at `xy`. Top edge is horizontally displaced by $\Delta x = \text{height} / \tan(\text{radians}(\text{corner\_angle}))$.
- Standard flowchart symbol for Input / Output operations and streaming event topics.

#### Code Examples
```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.preset_colors import CssColors
from drawlib.shapes import parallelogram
from drawlib.types import Style
from drawlib.styles import Styles

setup(width=100, height=50)

# 1. Flowchart I/O block
parallelogram((28, 25), width=35, height=20, corner_angle=70, style=Styles.BlueFlat, text="Read Input")

# 2. Rotated event stream block
parallelogram(
    (72, 25),
    width=35,
    height=20,
    corner_angle=65,
    style=Styles.Primary.patch(
        shape_fill_color=CssColors.LightYellow,
        shape_line_color=CssColors.GoldenRod,
        shape_line_width=2,
        angle=15,
    ),
    text="Kafka Stream",
    text_style=Styles.Primary.patch(text_size=10, text_color=CssColors.SaddleBrown),
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
    *,
    style: Style | None = None,
    text: str = "",
    text_style: Style | None = None,
) -> None:
    ...
```

#### Parameter Breakdown
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *Required* | Center coordinate `(x, y)` of the rhombus. |
| `width` | `float` | *Required* | Total horizontal diagonal span between left and right vertices. |
| `height` | `float` | *Required* | Total vertical diagonal span between bottom and top vertices. |
| `style` | `Style \| None` | `None` | Shape fill and line style (supports `angle` for rotation). |
| `text` | `str` | `""` | Centered text label. |
| `text_style` | `Style \| None` | `None` | Text formatting style. |

#### Geometric & Alignment Mechanics
- Centered at `xy`. Vertices span symmetrically along horizontal and vertical diagonals.
- Canonical decision block in flowchart logic diagrams and condition branch points.

#### Code Examples
```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.preset_colors import CssColors
from drawlib.shapes import rhombus
from drawlib.types import Style
from drawlib.styles import Styles

setup(width=100, height=50)

# 1. Flowchart decision condition diamond
rhombus(
    (28, 25),
    width=32,
    height=24,
    style=Styles.YellowFlat,
    text="Is Valid?",
    text_style=Styles.PrimaryBold.patch(text_size=10),
)

# 2. Rotated status checkpoint
rhombus(
    (72, 25),
    width=32,
    height=24,
    style=Styles.Primary.patch(
        shape_fill_color=CssColors.MistyRose,
        shape_line_color=CssColors.Crimson,
        shape_line_width=2,
        angle=20,
    ),
    text="Audit",
    text_style=Styles.Primary.patch(text_size=11, text_color=CssColors.DarkRed),
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
    *,
    style: Style | None = None,
    text: str = "",
    text_style: Style | None = None,
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
| `style` | `Style \| None` | `None` | Shape fill and stroke style (supports `angle` for rotation). |
| `text` | `str` | `""` | Centered text label. |
| `text_style` | `Style \| None` | `None` | Text styling parameters. |

#### Geometric & Alignment Mechanics
- Centered at `xy`.
- **Notice**: There is **no `width` parameter**! You must pass `bottomedge_width` and `topedge_width`.
- Used extensively in neural network architecture diagrams to represent pooling or dimensionality reduction layers.

#### Code Examples
```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.preset_colors import CssColors
from drawlib.shapes import trapezoid
from drawlib.types import Style
from drawlib.styles import Styles

setup(width=100, height=50)

# 1. Neural network downsampling / pooling layer
trapezoid(
    (28, 25),
    height=20,
    bottomedge_width=36,
    topedge_width=22,
    style=Styles.GreenFlat,
    text="MaxPool2D",
    text_style=Styles.WhiteBold.patch(text_size=10),
)

# 2. Right-angled projection layer
trapezoid(
    (72, 25),
    height=20,
    bottomedge_width=36,
    topedge_width=18,
    topedge_x=0,
    style=Styles.Primary.patch(
        shape_fill_color=CssColors.Lavender, shape_line_color=CssColors.Indigo, shape_line_width=2
    ),
    text="Proj",
    text_style=Styles.Primary.patch(text_size=10, text_color=CssColors.Indigo),
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
    *,
    style: Style | None = None,
    text: str = "",
    text_style: Style | None = None,
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
| `style` | `Style \| None` | `None` | Shape fill and outline style (supports `angle` for rotation). |
| `text` | `str` | `""` | Centered text label. |
| `text_style` | `Style \| None` | `None` | Text styling parameters. |

#### Geometric & Alignment Mechanics
- Centered at `xy`.
- Default `topvertex_x=None` produces an isosceles triangle with apex at center top.
- Set `topvertex_x=0` for a left-facing right triangle; set `topvertex_x=width` for a right-facing right triangle.

#### Code Examples
```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.preset_colors import CssColors
from drawlib.shapes import triangle
from drawlib.types import Style
from drawlib.styles import Styles

setup(width=100, height=50)

# 1. Warning indicator badge
triangle(
    (28, 25),
    width=30,
    height=26,
    style=Styles.Primary.patch(
        shape_fill_color=CssColors.Gold, shape_line_color=CssColors.DarkGoldenRod, shape_line_width=2
    ),
    text="!",
    text_style=Styles.Primary.patch(text_size=16, text_color=CssColors.Black, xy_shift=(0, -3)),
)

# 2. Right-angle ramp element
triangle((72, 25), width=32, height=26, topvertex_x=0, style=Styles.BlueFlat, text="Ramp")
save()
```

---

### 3.6 `regularpolygon`

Draws an equilateral regular polygon with $N$ equal sides, circumscribed in a circle.

#### Signature
```python
def regularpolygon(
    xy: tuple[float, float],
    radius: float,
    num_vertex: int,
    *,
    style: Style | None = None,
    text: str = "",
    text_style: Style | None = None,
) -> None:
    ...
```

#### Parameter Breakdown
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *Required* | Center coordinate `(x, y)`. |
| `radius` | `float` | *Required* | Circumscribed radius from center to each vertex. |
| `num_vertex` | `int` | *Required* | Number of vertices / sides ($N \ge 3$). Note singular name! |
| `style` | `Style \| None` | `None` | Shape fill and stroke style (supports `angle` for rotation). |
| `text` | `str` | `""` | Centered text label. |
| `text_style` | `Style \| None` | `None` | Text styling parameters. |

#### Geometric & Alignment Mechanics
- Centered at `xy`. Vertices generated at $\theta_k = \text{style.angle} + k(360^\circ / N)$.
- $N=3$ (equilateral triangle), $N=5$ (pentagon), $N=6$ (hexagon / Kubernetes pod), $N=8$ (octagon / stop sign).

#### Code Examples
```drawlib show-code
from drawlib.canvas import save, setup

setup(width=100, height=50)
from drawlib.preset_colors import CssColors
from drawlib.shapes import regularpolygon
from drawlib.types import Style
from drawlib.styles import Styles

# 1. Hexagon (Kubernetes Pod / Microservice)
regularpolygon((30, 22), radius=18, num_vertex=6, style=Styles.BlueFlat, text="Pod A")

# 2. Octagon (Security Firewall Boundary)
regularpolygon(
    (70, 22),
    radius=18,
    num_vertex=8,
    style=Styles.Primary.patch(
        shape_fill_color=CssColors.Tomato,
        shape_line_color=CssColors.DarkRed,
        shape_line_width=2,
        angle=22.5,
    ),
    text="WAF",
    text_style=Styles.WhiteBold.patch(text_size=12, text_color=CssColors.White),
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
    *,
    style: Style | None = None,
    text: str = "",
    text_style: Style | None = None,
) -> None:
    ...
```

#### Parameter Breakdown
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xys` | `list[tuple[float, float]]` | *Required* | Sequence of coordinate vertices (minimum 3 points). |
| `style` | `Style \| None` | `None` | Shape fill and line style. |
| `text` | `str` | `""` | Text placed at the centroid / bounding-box center. |
| `text_style` | `Style \| None` | `None` | Text formatting style. |

#### Geometric & Alignment Mechanics
- The path automatically closes by connecting the final vertex back to the first vertex.
- **Important**: `polygon` ignores `style.angle` and `halign`/`valign`. Vertex coordinates directly dictate orientation and position.

#### Code Examples
```drawlib show-code
from drawlib.canvas import save, setup

setup(width=100, height=50)
from drawlib.preset_colors import CssColors
from drawlib.shapes import polygon
from drawlib.types import Style
from drawlib.styles import Styles

# 1. Irregular network partition boundary
polygon(
    [(10, 15), (25, 35), (45, 30), (40, 10), (20, 8)],
    style=Styles.Primary.patch(
        shape_fill_color=CssColors.AliceBlue, shape_line_color=CssColors.SteelBlue, shape_line_width=2
    ),
    text="VLAN 1",
)

# 2. Custom 5-point chevron-like boundary
polygon(
    [(55, 10), (75, 10), (85, 22), (75, 34), (55, 34), (65, 22)],
    style=Styles.GreenFlat,
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
    *,
    style: Style | None = None,
    text: str = "",
    text_style: Style | None = None,
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
| `style` | `Style \| None` | `None` | Fill and stroke style (supports `angle` for rotation). |
| `text` | `str` | `""` | Text label at center. |
| `text_style` | `Style \| None` | `None` | Text styling parameters. |

#### Geometric & Alignment Mechanics
- Generates $2N$ alternating vertices around `xy`.
- Strict validation: `radius_ext > radius_int` (raises `ValueError` otherwise).

#### Code Examples
```drawlib show-code
from drawlib.canvas import save, setup

setup(width=100, height=50)
from drawlib.preset_colors import CssColors
from drawlib.shapes import star
from drawlib.types import Style
from drawlib.styles import Styles

# 1. 5-pointed award / milestone badge
star((30, 22), num_vertex=5, radius_ext=18, radius_int=8, style=Styles.YellowFlat, text="Star")

# 2. 8-pointed spark / security alert icon
star(
    (70, 22),
    num_vertex=8,
    radius_ext=18,
    radius_int=10,
    style=Styles.Primary.patch(
        shape_fill_color=CssColors.LightCoral,
        shape_line_color=CssColors.FireBrick,
        shape_line_width=2,
        angle=22.5,
    ),
    text="ALERT",
    text_style=Styles.Primary.patch(text_size=9, text_color=CssColors.DarkRed),
)
save()
```

---

### 3.9 `bubblespeech`

Draws an irregular speech bubble or callout box with a triangular pointer tail, designed for comic dialogue, system callouts, and migration notes.

#### Signature
```python
def bubblespeech(
    xy: tuple[float, float],
    width: float,
    height: float,
    tail_edge: Literal["left", "top", "right", "bottom"],
    tail_start_ratio: float,
    tail_vertex_xy: tuple[float, float],
    tail_end_ratio: float,
    *,
    style: Style | None = None,
    text: str = "",
    text_style: Style | None = None,
) -> None:
    ...
```

#### Parameter Breakdown
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *Required* | Bottom-left corner coordinate `(x, y)` of the bubble body. |
| `width` | `float` | *Required* | Horizontal width of the bubble body ($> 0$). |
| `height` | `float` | *Required* | Vertical height of the bubble body ($> 0$). |
| `tail_edge` | `Literal["left", "top", "right", "bottom"]` | *Required* | Edge where the tail originates. |
| `tail_start_ratio` | `float` | *Required* | Ratio in `[0.0, 1.0]` along edge where the tail begins. |
| `tail_vertex_xy` | `tuple[float, float]` | *Required* | Target coordinates pointing to vertex of the tail. |
| `tail_end_ratio` | `float` | *Required* | Ratio in `[0.0, 1.0]` along edge where the tail ends ($> \text{tail\_start\_ratio}$). |
| `style` | `Style \| None` | `None` | Shape fill and outline style. |
| `text` | `str` | `""` | Centered text label within bubble body. |
| `text_style` | `Style \| None` | `None` | Text styling parameters. |

#### Geometric Mechanics
- `xy` defines the **bottom-left** corner of the speech bubble rectangle.
- `tail_start_ratio` must be strictly smaller than `tail_end_ratio`.
- `tail_vertex_xy` is an absolute coordinate pointing to any external point (e.g. a server node or database).

#### Code Example
```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.shapes import bubblespeech, rectangle
from drawlib.styles import Styles

setup(width=100, height=50)

rectangle((25, 25), width=24, height=16, style=Styles.Neutral, text="Database")

bubblespeech(
    xy=(50, 16),
    width=44,
    height=18,
    tail_edge="left",
    tail_start_ratio=0.3,
    tail_end_ratio=0.7,
    tail_vertex_xy=(37, 25),
    style=Styles.PrimaryFlat,
    text="Replica Alert",
    text_style=Styles.WhiteBold,
)
save()
```

---

## 4. Custom Path & Vector Construction

### 4.1 `shape`

Builds an arbitrary vector polygon or curved shape using straight lines, quadratic Beziers, and cubic Beziers.

##### Signature
```python
def shape(
    xy: tuple[float, float],
    path_points: list[
        tuple[float, float]
        | tuple[tuple[float, float], tuple[float, float]]
        | tuple[tuple[float, float], tuple[float, float], tuple[float, float]]
    ],
    is_default_center: bool = False,
    *,
    style: Style | None = None,
    text: str = "",
    text_style: Style | None = None,
) -> None:
    ...
```

#### Parameter Breakdown
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *Required* | Reference starting point or geometric center. |
| `path_points` | `list[...]` | *Required* | Sequence of relative coordinate offsets or Bezier control tuples. |
| `is_default_center` | `bool` | `False` | If `False`, `xy` is path origin. If `True`, `xy` is centroid. |
| `style` | `Style \| None` | `None` | Shape fill and stroke style (supports `angle` for rotation). |
| `text` | `str` | `""` | Centered text label. |
| `text_style` | `Style \| None` | `None` | Text styling parameters. |

#### Path Point Segment Types
- `path_points` defines polygon vertices in local coordinate space (relative to origin `(0, 0)`). Drawlib automatically computes the bounding box and centers the resulting shape at `xy`.
- **Straight Segment**: `(x, y)` draws a straight line vertex.
- **Quadratic Bezier**: `((cp_x, cp_y), (end_x, end_y))` where `cp` is the control point.
- **Cubic Bezier**: `((cp1_x, cp1_y), (cp2_x, cp2_y), (end_x, end_y))` with two control points.

#### Code Examples
```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.preset_colors import CssColors
from drawlib.shapes import shape
from drawlib.styles import Colors, Styles
from drawlib.types import Style

setup(width=100, height=50)

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
    style=Styles.BlueFlat,
    text="Shield",
    text_style=Styles.WhiteBold.patch(text_size=10, text_color=Colors.White),
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
    style=Styles.Primary.patch(
        shape_fill_color=CssColors.Lavender, shape_line_color=CssColors.Purple, shape_line_width=1.5
    ),
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
    tail_width: float,
    head_width: float,
    head_length: float,
    *,
    head: Literal["->", "<-", "<->"] = "->",
    style: Style | None = None,
    text: str = "",
    text_style: Style | None = None,
) -> None:
    ...
```

#### Parameter Breakdown
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy1` | `tuple[float, float]` | *Required* | Base center of the arrow tail `(x1, y1)`. |
| `xy2` | `tuple[float, float]` | *Required* | Coordinate of the arrow tip `(x2, y2)`. |
| `tail_width` | `float` | *Required* | Width of the rectangular shaft. |
| `head_width` | `float` | *Required* | Full transverse width of the arrowhead base. |
| `head_length` | `float` | *Required* | Axial length of the arrowhead from base to tip. |
| `head` | `Literal["->", "<-", "<->"]` | `"->"` | Arrowhead direction. |
| `style` | `Style \| None` | `None` | Fill and stroke style. |
| `text` | `str` | `""` | Embedded label rendered along the arrow shaft. |
| `text_style` | `Style \| None` | `None` | Text styling parameters. |

#### Geometric & Alignment Mechanics
- The arrow direction and orientation angle are calculated automatically from $\Delta x = x_2 - x_1, \Delta y = y_2 - y_1$.
- `text` is rendered directly along the shaft, automatically rotated parallel to the arrow vector.

#### Code Examples
```drawlib show-code
from drawlib.canvas import save, setup

setup(width=100, height=50)
from drawlib.preset_colors import CssColors
from drawlib.shapes import arrow
from drawlib.types import Style
from drawlib.styles import Styles

# 1. Straight transaction flow arrow with shaft text
arrow((10, 25), (45, 25), tail_width=3, head_width=8, head_length=6, style=Styles.BlueFlat, text="POST /order")

# 2. Angled response arrow with custom styling
arrow(
    (55, 15),
    (85, 35),
    tail_width=2.5,
    head_width=7,
    head_length=5,
    style=Styles.Primary.patch(
        shape_fill_color=CssColors.LightGreen, shape_line_color=CssColors.ForestGreen, shape_line_width=1.5
    ),
    text="200 OK",
    text_style=Styles.Primary.patch(text_size=9, text_color=CssColors.DarkGreen),
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
    tail_width: float,
    head_width: float,
    head_length: float,
    head: Literal["->", "<-", "<->"] = "->",
    *,
    style: Style | None = None,
) -> None:
    ...
```

#### Parameter Breakdown
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *Required* | Center coordinate `(x, y)` of the bounding box. |
| `width` | `float` | *Required* | Total bounding box width. |
| `height` | `float` | *Required* | Total bounding box height. |
| `tail_width` | `float` | *Required* | Width of the shaft. |
| `head_width` | `float` | *Required* | Arrowhead width at the tip end. |
| `head_length` | `float` | *Required* | Arrowhead axial length. |
| `head` | `Literal["->", "<-", "<->"]` | `"->"` | Arrowhead direction. |
| `style` | `Style \| None` | `None` | Fill, stroke, rotation (`angle`), and elbow rounding radius (`shape_r` scalar or 1-tuple). |

> **Important**: `arrow_l` **does not accept `text`**. Place external `drawlib.text.text()` labels next to the elbow.

#### Code Examples
```drawlib show-code
from drawlib.canvas import save, setup

setup(width=100, height=50)
from drawlib.preset_colors import CssColors
from drawlib.shapes import arrow_l
from drawlib.types import Style
from drawlib.styles import Styles

# 1. Orthogonal L-routing pipe
arrow_l((25, 25), width=30, height=25, tail_width=3, head_width=8, head_length=6, style=Styles.BlueFlat)

# 2. Rounded elbow L-arrow with custom border
arrow_l(
    (70, 25),
    width=35,
    height=25,
    tail_width=4,
    head_width=10,
    head_length=7,
    style=Styles.Primary.patch(
        shape_fill_color=CssColors.MistyRose,
        shape_line_color=CssColors.Crimson,
        shape_line_width=2,
        shape_r=5,
    ),
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
    tail_width: float,
    head_width: float,
    head_length: float,
    head: Literal["->", "<-", "<->"] = "->",
    *,
    style: Style | None = None,
) -> None:
    ...
```

#### Parameter Breakdown
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *Required* | Center coordinate `(x, y)` of the bounding box. |
| `width` | `float` | *Required* | Total bounding box width. |
| `height` | `float` | *Required* | Total bounding box height. |
| `tail_width` | `float` | *Required* | Width of the shafts. |
| `head_width` | `float` | *Required* | Arrowhead width. |
| `head_length` | `float` | *Required* | Arrowhead axial length. |
| `head` | `Literal["->", "<-", "<->"]` | `"->"` | Arrowhead direction. |
| `style` | `Style \| None` | `None` | Fill, stroke, rotation (`angle`), and corner rounding radius at turns (`shape_r` scalar or 2-tuple). |

> **Important**: `arrow_u` **does not accept `text`**.

#### Code Examples
```drawlib show-code
from drawlib.canvas import save, setup

setup(width=100, height=50)
from drawlib.preset_colors import CssColors
from drawlib.shapes import arrow_u
from drawlib.types import Style
from drawlib.styles import Styles

# 1. Feedback loop return arrow
arrow_u((25, 25), width=25, height=30, tail_width=3, head_width=8, head_length=6, style=Styles.GreenFlat)

# 2. Rotated turnaround retry arrow
arrow_u(
    (70, 25),
    width=28,
    height=32,
    tail_width=3,
    head_width=9,
    head_length=7,
    style=Styles.Primary.patch(
        shape_fill_color=CssColors.Lavender,
        shape_line_color=CssColors.Purple,
        shape_line_width=1.5,
        angle=90,
        shape_r=4,
    ),
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
    tail_width: float,
    head_width: float,
    head_angle: float,
    angle_start: float,
    angle_end: float,
    *,
    head: Literal["->", "<-", "<->"] = "->",
    style: Style | None = None,
    text: str = "",
    text_style: Style | None = None,
) -> None:
    ...
```

#### Parameter Breakdown
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *Required* | Center coordinate `(x, y)` of the arc ellipse. |
| `width` | `float` | *Required* | Horizontal diameter of the ellipse. |
| `height` | `float` | *Required* | Vertical diameter of the ellipse. |
| `tail_width` | `float` | *Required* | Width of the curved body shaft. |
| `head_width` | `float` | *Required* | Arrowhead width at the end tip. |
| `head_angle` | `float` | *Required* | Angular span of the arrowhead in degrees. |
| `angle_start` | `float` | *Required* | Starting angle in degrees CCW. |
| `angle_end` | `float` | *Required* | Ending angle in degrees CCW (location of arrowhead). |
| `head` | `Literal["->", "<-", "<->"]` | `"->"` | Arrowhead direction. |
| `style` | `Style \| None` | `None` | Fill and stroke style (supports `angle` for rotational shift). |

#### Code Examples
```drawlib show-code
from drawlib.canvas import save, setup

setup(width=100, height=50)
from drawlib.preset_colors import CssColors
from drawlib.shapes import arrow_arc
from drawlib.types import Style
from drawlib.styles import Styles

# 1. Circular process cycle arrow (0 to 90 degrees)
arrow_arc((30, 25), width=30, height=30, tail_width=3, head_width=8, head_angle=20, angle_start=0, angle_end=90, style=Styles.BlueFlat)

# 2. Semi-circular feedback return arrow
arrow_arc(
    (70, 25),
    width=32,
    height=24,
    tail_width=3,
    head_width=8,
    head_angle=20,
    angle_start=0,
    angle_end=180,
    style=Styles.Primary.patch(
        shape_fill_color=CssColors.Gold, shape_line_color=CssColors.DarkGoldenRod, shape_line_width=1.5
    ),
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
    tail_width: float,
    head_width: float,
    head_length: float,
    *,
    head: Literal["->", "<-", "<->"] = "->",
    style: Style | None = None,
) -> None:
    ...
```

#### Parameter Breakdown
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xys` | `list[tuple[float, float]]` | *Required* | Sequence of path points. Arrowhead is attached to the final vertex. |
| `tail_width` | `float` | *Required* | Width of the polyline shaft. |
| `head_width` | `float` | *Required* | Arrowhead width at final tip. |
| `head_length` | `float` | *Required* | Arrowhead axial length. |
| `head` | `Literal["->", "<-", "<->"]` | `"->"` | Arrowhead direction. |
| `style` | `Style \| None` | `None` | Fill, stroke, and corner rounding radius at intermediate joints (`shape_r` scalar or `(len(xys) - 2)`-tuple). |

> **Important**: `arrow_polyline` **does not accept `text`**.

#### Code Examples
```drawlib show-code
from drawlib.canvas import save, setup

setup(width=100, height=50)
from drawlib.preset_colors import CssColors
from drawlib.shapes import arrow_polyline
from drawlib.types import Style
from drawlib.styles import Styles

# 1. S-curved routing channel with rounded corners
arrow_polyline(
    [(10, 15), (25, 15), (25, 35), (45, 35)],
    tail_width=3,
    head_width=8,
    head_length=6,
    style=Styles.BlueFlat.patch(shape_r=3),
)

# 2. Multi-segment bypass route
arrow_polyline(
    [(55, 10), (70, 10), (70, 25), (85, 25), (85, 40)],
    tail_width=2.5,
    head_width=7,
    head_length=5,
    style=Styles.Primary.patch(
        shape_fill_color=CssColors.LightGreen,
        shape_line_color=CssColors.ForestGreen,
        shape_line_width=1.5,
        shape_r=2,
    ),
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
    corner_angle: float,
    *,
    mirror: bool = False,
    style: Style | None = None,
    text: str = "",
    text_style: Style | None = None,
) -> None:
    ...
```

#### Parameter Breakdown
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *Required* | Center coordinate `(x, y)` of the chevron. |
| `width` | `float` | *Required* | Total horizontal length from rear notch apex to front point. |
| `height` | `float` | *Required* | Total vertical height. |
| `corner_angle` | `float` | *Required* | Point/notch angle in degrees ($0 < \theta < 180^\circ$). |
| `mirror` | `bool` | `False` | Mirror chevron horizontally if `True`. |
| `style` | `Style \| None` | `None` | Fill and stroke style (supports `angle` for rotation). |
| `text` | `str` | `""` | Embedded text label at center. |
| `text_style` | `Style \| None` | `None` | Text styling parameters. |

#### Geometric & Alignment Mechanics
- Centered at `xy`. Rear notch depth and forward point apex match, allowing multiple chevrons to tessellate horizontally into pipeline stages.

#### Code Examples
```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.shapes import chevron
from drawlib.types import Style
from drawlib.styles import Styles

setup(width=100, height=50)

# 1. CI/CD pipeline stage 1
chevron((35, 25), width=30, height=22, corner_angle=60, style=Styles.BlueFlat, text="Build")

# 2. Consecutive interlocking pipeline stage 2
chevron((68, 25), width=30, height=22, corner_angle=60, style=Styles.GreenFlat, text="Test")
save()
```

---

## 6. Production Architectural Blueprints & Schemas

### 6.1 Cloud Infrastructure Schema (AWS VPC / Multi-Tier)

This pattern illustrates a secure multi-tier virtual private cloud containing public and private subnets, an internet gateway, compute clusters, and a managed database.

```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.shapes import arrow, circle, ellipse, rectangle
from drawlib.styles import Styles

setup(width=150, height=90)

# 1. AWS VPC Boundary Enclosure (Centered at (75, 45))
rectangle(
    (75, 45),
    width=140,
    height=80,
    style=Styles.MutedDashed.patch(shape_r=4),
    text="VPC (10.0.0.0/16)",
    text_style=Styles.SecondaryBold.patch(text_size=12, xy_shift=(-45, 34)),
)

# 2. Internet Gateway
circle(
    (18, 45),
    radius=7,
    style=Styles.Neutral,
    text="IGW",
    text_style=Styles.DarkBold.patch(text_size=10),
)

# 3. Public Web Subnet
rectangle(
    (58, 62),
    width=50,
    height=32,
    style=Styles.MutedDashed.patch(shape_r=3),
    text="Public Subnet (DMZ)",
    text_style=Styles.SecondaryBold.patch(text_size=10, xy_shift=(-8, 12)),
)
rectangle(
    (46, 60),
    width=18,
    height=14,
    style=Styles.PrimaryFlat.patch(shape_r=2),
    text="ALB",
    text_style=Styles.WhiteBold.patch(text_size=10),
)
rectangle(
    (70, 60),
    width=18,
    height=14,
    style=Styles.PrimaryNeutral.patch(shape_r=2),
    text="Nginx",
)

# 4. Private App Subnet
rectangle(
    (58, 26),
    width=50,
    height=32,
    style=Styles.MutedDashed.patch(shape_r=3),
    text="Private App Subnet",
    text_style=Styles.SecondaryBold.patch(text_size=10, xy_shift=(-8, 12)),
)
rectangle(
    (46, 24),
    width=18,
    height=14,
    style=Styles.Neutral.patch(shape_r=2),
    text="Auth\nSvc",
)
rectangle(
    (70, 24),
    width=18,
    height=14,
    style=Styles.Neutral.patch(shape_r=2),
    text="Order\nSvc",
)

# 5. Database Tier
rectangle(
    (120, 44),
    width=44,
    height=60,
    style=Styles.MutedDashed.patch(shape_r=3),
    text="Database Tier (Multi-AZ)",
    text_style=Styles.SecondaryBold.patch(text_size=10, xy_shift=(0, 25)),
)
ellipse(
    (120, 56),
    width=32,
    height=14,
    style=Styles.SecondaryNeutral,
    text="Postgres Primary",
    text_style=Styles.DarkBold.patch(text_size=9),
)
ellipse(
    (120, 32),
    width=32,
    height=14,
    style=Styles.Neutral,
    text="Read Replica",
    text_style=Styles.DarkBold.patch(text_size=9),
)

# 6. Connecting Arrows
arrow((25, 45), (37, 60), tail_width=2, head_width=5, head_length=4, style=Styles.DarkFlat)
arrow((55, 60), (61, 60), tail_width=2, head_width=5, head_length=4, style=Styles.DarkFlat)
arrow((70, 53), (70, 31), tail_width=2, head_width=5, head_length=4, style=Styles.DarkFlat)
arrow((79, 24), (104, 56), tail_width=2, head_width=5, head_length=4, style=Styles.DarkFlat)

save()
```

---

### 6.2 Event-Driven Microservices Topology (Kafka / Event Mesh)

Demonstrates message publishers, Kafka message topic queues, consumer groups, and dead-letter queues (DLQ).

```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.shapes import arrow, donuts, parallelogram, rectangle
from drawlib.styles import Styles

setup(width=140, height=65)

# Producer (Hero node)
rectangle(
    (20, 32.5),
    width=24,
    height=20,
    style=Styles.PrimaryFlat.patch(shape_r=3),
    text="Order\nProducer",
    text_style=Styles.WhiteBold.patch(text_size=11),
)

# Event Bus / Kafka Stream Topic (Parallelogram)
parallelogram(
    (64, 32.5),
    width=40,
    height=28,
    corner_angle=70,
    style=Styles.PrimaryNeutral,
    text="orders.events\n(Kafka Topic)",
    text_style=Styles.DarkBold.patch(text_size=11),
)

# Consumer Group (Calm neutral workers)
rectangle(
    (115, 45),
    width=32,
    height=18,
    style=Styles.Neutral.patch(shape_r=3),
    text="Payment Worker",
)
rectangle(
    (115, 20),
    width=32,
    height=18,
    style=Styles.Neutral.patch(shape_r=3),
    text="Inventory Worker",
)

# Dead Letter Queue (Donuts)
donuts(
    (64, 9),
    radius=6,
    width=2,
    style=Styles.SecondaryNeutral,
    text="DLQ",
    text_style=Styles.DarkBold.patch(text_size=8),
)

# Event Flow Arrows
arrow((32, 32.5), (44, 32.5), tail_width=2.5, head_width=6, head_length=4, style=Styles.DarkFlat)
arrow((84, 38), (99, 45), tail_width=2.5, head_width=6, head_length=4, style=Styles.DarkFlat)
arrow((84, 27), (99, 20), tail_width=2.5, head_width=6, head_length=4, style=Styles.DarkFlat)
arrow(
    (99, 15),
    (71, 9),
    tail_width=2,
    head_width=5,
    head_length=4,
    style=Styles.DarkDashed,
)

save()
```

---

### 6.3 Deep Neural Network Layer Graph (CNN / ResNet Skip Connection)

Demonstrates convolution, pooling, batch normalization, and skip residual connections in machine learning architectures.

```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.shapes import arrow, arrow_polyline, circle, rectangle, trapezoid
from drawlib.styles import Styles

setup(width=150, height=55)

# Input Tensor
rectangle(
    (16, 25),
    width=18,
    height=22,
    style=Styles.Neutral,
    text="Input\n3x224x224",
    text_style=Styles.DarkBold.patch(text_size=8),
)

# Conv2D Layer (Hero)
rectangle(
    (42, 25),
    width=20,
    height=28,
    style=Styles.PrimaryFlat.patch(shape_r=2),
    text="Conv2D\n64 filters",
    text_style=Styles.WhiteBold.patch(text_size=9),
)

# Batch Norm & ReLU
rectangle(
    (68, 25),
    width=18,
    height=22,
    style=Styles.PrimaryNeutral.patch(shape_r=2),
    text="BN +\nReLU",
    text_style=Styles.DarkBold.patch(text_size=9),
)

# Conv2D Layer 2 (Hero)
rectangle(
    (92, 25),
    width=20,
    height=28,
    style=Styles.PrimaryFlat.patch(shape_r=2),
    text="Conv2D\n64 filters",
    text_style=Styles.WhiteBold.patch(text_size=9),
)

# Residual Elementwise Add Node
circle(
    (114, 25),
    radius=4.5,
    style=Styles.SecondaryNeutral,
    text="+",
    text_style=Styles.DarkBold.patch(text_size=12),
)

# Max Pooling (Trapezoid)
trapezoid(
    (134, 25),
    height=20,
    bottomedge_width=22,
    topedge_width=14,
    style=Styles.Neutral,
    text="Pool\n/2",
    text_style=Styles.DarkBold.patch(text_size=8),
)

# Forward Feed Connections
arrow((25, 25), (32, 25), tail_width=1.5, head_width=4, head_length=3, style=Styles.DarkFlat)
arrow((52, 25), (59, 25), tail_width=1.5, head_width=4, head_length=3, style=Styles.DarkFlat)
arrow((77, 25), (82, 25), tail_width=1.5, head_width=4, head_length=3, style=Styles.DarkFlat)
arrow((102, 25), (109.5, 25), tail_width=1.5, head_width=4, head_length=3, style=Styles.DarkFlat)
arrow((118.5, 25), (123, 25), tail_width=1.5, head_width=4, head_length=3, style=Styles.DarkFlat)

# ResNet Residual Skip Connection (arrow_polyline)
arrow_polyline(
    [(42, 39), (42, 47), (114, 47), (114, 29.5)],
    tail_width=1.5,
    head_width=4,
    head_length=3,
    style=Styles.SecondaryBold.patch(shape_r=3),
)

save()
```

---

### 6.4 UML State Machine Diagram

Constructs a standard UML state chart featuring initial pseudo-states, rounded composite states, guard conditions, and terminal states.

```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.shapes import arrow, circle, donuts, rectangle, rhombus
from drawlib.styles import Styles
from drawlib.text import text

setup(width=150, height=60)

# Initial State
circle((15, 30), radius=4.5, style=Styles.DarkFlat)

# State 1: Draft (Hero)
rectangle(
    (40, 30),
    width=26,
    height=20,
    style=Styles.PrimaryFlat.patch(shape_r=5),
    text="DRAFT",
    text_style=Styles.WhiteBold.patch(text_size=10),
)

# Choice Decision Pseudostate (Rhombus)
rhombus((70, 30), width=16, height=16, style=Styles.Neutral)

# State 2: Published
rectangle(
    (104, 43),
    width=26,
    height=18,
    style=Styles.SecondaryNeutral.patch(shape_r=5),
    text="PUBLISHED",
    text_style=Styles.DarkBold.patch(text_size=9),
)

# State 3: Rejected
rectangle(
    (104, 17),
    width=26,
    height=18,
    style=Styles.Neutral.patch(shape_r=5),
    text="REJECTED",
    text_style=Styles.DarkBold.patch(text_size=9),
)

# Terminal State (Bullseye / Donut with inner circle)
donuts(
    (136, 30),
    radius=5,
    width=1.2,
    style=Styles.DarkFlat,
)
circle((136, 30), radius=3, style=Styles.DarkFlat)

# Transitions
arrow((19.5, 30), (27, 30), tail_width=1.5, head_width=4, head_length=3, style=Styles.DarkFlat)
arrow((53, 30), (62, 30), tail_width=1.5, head_width=4, head_length=3, style=Styles.DarkFlat)

arrow((78, 35), (91, 43), tail_width=1.5, head_width=4, head_length=3, style=Styles.DarkFlat)
text((81, 43), "Valid", style=Styles.DarkBold.patch(text_size=8.5))

arrow((78, 25), (91, 17), tail_width=1.5, head_width=4, head_length=3, style=Styles.DarkFlat)
text((81, 17), "Invalid", style=Styles.DarkBold.patch(text_size=8.5))

arrow((117, 43), (131, 33), tail_width=1.5, head_width=4, head_length=3, style=Styles.DarkFlat)
arrow((117, 17), (131, 27), tail_width=1.5, head_width=4, head_length=3, style=Styles.DarkFlat)

save()
```

---

### 6.5 Modern Dashboard UI Component Kit (Cards, Badges, Metrics)

Demonstrates how human designers and AI coding agents can construct crisp application user interfaces, modals, and KPI telemetry cards using Drawlib primitives.

```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.shapes import arc, circle, rectangle
from drawlib.styles import Styles

setup(width=140, height=75)

# Outer Dashboard Frame
rectangle(
    (70, 37.5),
    width=130,
    height=65,
    style=Styles.MutedDashed.patch(shape_r=4),
)

# KPI Card 1: Server Load
rectangle(
    (28, 37.5),
    width=36,
    height=50,
    style=Styles.PrimaryNeutral.patch(shape_r=3),
    text="CPU LOAD\n\n42%",
    text_style=Styles.DarkBold.patch(text_size=11, xy_shift=(0, -8)),
)
arc(
    (28, 48),
    width=20,
    height=20,
    angle_start=0,
    angle_end=220,
    style=Styles.PrimaryBold.patch(line_width=3),
)

# KPI Card 2: Memory Usage
rectangle(
    (70, 37.5),
    width=36,
    height=50,
    style=Styles.Neutral.patch(shape_r=3),
    text="MEMORY\n\n78%",
    text_style=Styles.DarkBold.patch(text_size=11, xy_shift=(0, -8)),
)
arc(
    (70, 48),
    width=20,
    height=20,
    angle_start=0,
    angle_end=280,
    style=Styles.SecondaryBold.patch(line_width=3),
)

# KPI Card 3: Network Status
rectangle(
    (112, 37.5),
    width=36,
    height=50,
    style=Styles.Neutral.patch(shape_r=3),
    text="NETWORK\n\nActive",
    text_style=Styles.DarkBold.patch(text_size=11, xy_shift=(0, -8)),
)
circle(
    (112, 48),
    radius=5,
    style=Styles.SecondaryFlat,
)

save()
```

---

## 7. Quick Reference Matrix & Troubleshooting

### 7.1 Function Capabilities Matrix

| Function | Default Anchor | Primary Dimensions | Corner Radius (`style.shape_r`) | Rotation (`style.angle`) | Supports `text` | Ignores `halign/valign` |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| `circle` | Center `(x, y)` | `radius` | Ignored | Yes (text) | Yes | No |
| `donuts` | Center `(x, y)` | `radius`, `width` | Ignored | Yes (text) | Yes | No |
| `ellipse`| Center `(x, y)` | `width`, `height` | Ignored | Yes | Yes | No |
| `wedge`  | Center `(x, y)` | `radius`, `width`, `angle_start/end` | Ignored | Yes | Yes | No |
| `fan`    | Center `(x, y)` | `radius`, `angle_start/end` | Ignored | Yes | Yes | No |
| `arc`    | Center `(x, y)` | `width`, `height`, `angle_start/end` | Ignored | Yes | Yes | No |
| `cylinder` | Center `(x, y)` | `width`, `height`, `disks` | Ignored | Yes | Yes | No |
| `face`   | Center `(x, y)` | `radius`, `mood` | Ignored | Yes | Yes | No |
| `rectangle` | Center `(x, y)` | `width`, `height` | **Yes** (scalar or 4-tuple) | Yes | Yes | No |
| `parallelogram` | Center `(x, y)` | `width`, `height`, `corner_angle` | **Yes** (scalar or 4-tuple) | Yes | Yes | No |
| `rhombus` | Center `(x, y)` | `width`, `height` | **Yes** (scalar or 4-tuple) | Yes | Yes | No |
| `trapezoid` | Center `(x, y)` | `height`, `bottomedge_width`, `topedge_width` | **Yes** (scalar or 4-tuple) | Yes | Yes | No |
| `triangle` | Center `(x, y)` | `width`, `height`, `topvertex_x` | **Yes** (scalar or 3-tuple) | Yes | Yes | No |
| `regularpolygon` | Center `(x, y)` | `num_vertex`, `radius` | **Yes** (scalar or N-tuple) | Yes | Yes | No |
| `polygon` | Vertices `xys` | `xys: list[tuple[float, float]]` | **Yes** (scalar or N-tuple) | **No** | Yes | **Yes** |
| `star` | Center `(x, y)` | `num_vertex`, `radius_ext`, `radius_int` | **Yes** (scalar or 2N-tuple) | Yes | Yes | No |
| `shape` | Center `(x, y)` | `path_points` | Via Bezier | Yes | Yes | No |
| `arrow` | Endpoints `xy1, xy2` | `tail_width`, `head_width`, `head_length` | Ignored | Auto ($\Delta xy$) | Yes | **Yes** |
| `arrow_polyline` | Vertices `xys` | `tail_width`, `head_width`, `head_length` | **Yes** (scalar or (N-2)-tuple) | Path-driven | **No** | **Yes** |
| `arrow_arc` | Center `(x, y)` | `width`, `height`, `head_angle` | Ignored | Yes | **No** | **Yes** |
| `arrow_l` | Center `(x, y)` | `width`, `height`, head/tail dims | **Yes** (scalar or 1-tuple) | Yes | **No** | **Yes** |
| `arrow_u` | Center `(x, y)` | `width`, `height`, head/tail dims | **Yes** (scalar or 2-tuple) | Yes | **No** | **Yes** |
| `chevron` | Center `(x, y)` | `width`, `height`, `corner_angle` | **Yes** (scalar or 6-tuple) | Yes | Yes | No |
| `bubblespeech` | Bottom-Left `(x, y)` | `width`, `height`, `tail_*` | Ignored | No | Yes | **Yes** |

---

### 7.2 Common Pitfalls & Resolution Rules

1. **Passing `text` to Arrow Subtypes**:
   - *Error / Ignored*: `arrow_polyline`, `arrow_l`, `arrow_u`, and `arrow_arc` **do not accept** `text` or `text_style`.
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
   - To remove a shape border: set `shape_line_width=0`.
   - To make the interior transparent: set `shape_fill_color=Colors.Transparent` or `alpha=0.0`.
6. **Centering Text in Asymmetric Shapes**:
   - For `triangle()` and `trapezoid()`, the default bounding-box center may place text too close to narrow edges. Use `text_style=Style(xy_shift=(dx, dy))` to nudge the text into visual balance.
7. **Orientation in `polygon()`**:
   - `polygon()` derives its orientation entirely from vertex order in `xys` and ignores `style.angle`. To rotate a custom polygon, use `shape(xy, path_points, style=Style(angle=...))`.
