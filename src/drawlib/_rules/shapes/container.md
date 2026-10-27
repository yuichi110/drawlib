# Drawlib Container Shapes Guidelines (`lib-shapes-container`)

API specification and geometric rules for 3D storage/compute blocks, document symbols, pipeline funnels, cloud boundaries, and grouping braces in `drawlib._core.l4_canvas._shapes._container` (`cylinder`, `cube`, `document`, `funnel`, `cloud`, `brace`). See `lib-shapes-overview` for universal coordinate and styling rules.

---

## 1. Summary of Container & Grouping Shapes

All 6 shapes in `_container.py` are **Center-Anchored at `xy = (cx, cy)`** and require `*, style: Style` as a mandatory keyword-only argument:

| Function | Positional Args | Keyword-Only Geometry Args | Fill / Stroke Mode | Primary Architectural Use Cases |
| :--- | :--- | :--- | :--- | :--- |
| **`cylinder`** | `xy, width, height` | `disks: int = 1` | Fill + Stroke (3D cap) | Relational/NoSQL databases, persistent volumes, queues |
| **`cube`** | `xy, width, height` | `depth_ratio: float \| None = None` | Fill + Stroke (3 faces) | Containers, VM nodes, artifact packages, 3D blocks |
| **`document`** | `xy, width, height` | `variant="wave", stacked=1, wave_ratio=None, fold_ratio=None` | Fill + Stroke | Reports, log files, YAML/JSON manifests, multi-docs |
| **`funnel`** | `xy, width, height` | `variant="standard", neck_width_ratio=None, neck_height_ratio=None` | Fill + Stroke | ETL data filtering, conversion funnels, log sampling |
| **`cloud`** | `xy, width, height` | `variant="standard", bump_ratio=None` | Fill + Stroke | Public internet, VPC/SaaS boundaries, cloud enclosures |
| **`brace`** | `xy, width, height` | `symbol="{", direction=None, tip_ratio=None, tip_position_ratio=None` | **Stroke-Only** (`line_*`) | Layer annotations, grouping brackets `{ }`, `[ ]`, `( )` |

---

## 2. 3D Storage & Compute Containers (`cylinder`, `cube`)

### 2.1. `cylinder`
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
- `disks`: Number of stacked disk tiers (`>= 1`). Values `> 1` draw curved horizontal divider rings across the cylinder body.
- Pass `style.patch(angle=90)` or `angle=-90` to render horizontal message queues / data pipes.

### 2.2. `cube`
Draws an isometric 3D box centered at `xy` within total outer bounding box `(width, height)`, automatically shading the top and side faces relative to the front face.

```python
def cube(
    xy: tuple[float, float],
    width: float,
    height: float,
    *,
    depth_ratio: float | None = None,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None: ...
```
- `depth_ratio`: Optional 3D depth fraction strictly in `(0.0, 1.0)` relative to `min(width, height)`.
- Embedded `text` is automatically centered on the **front face** of the cube.

---

## 3. Document & Funnel Primitives (`document`, `funnel`)

### 3.1. `document`
Draws a flowchart document with a wavy bottom edge (`"wave"`) or a folded corner (`"folded"`) centered at `xy`, with optional stacked sheets (`stacked >= 1`).

```python
def document(
    xy: tuple[float, float],
    width: float,
    height: float,
    *,
    variant: Literal[
        "wave", "standard", "folded", "page", "note",
        "double_wave", "snippet", "folded_wave", "report"
    ] = "wave",
    stacked: int = 1,
    wave_ratio: float | None = None,
    fold_ratio: float | None = None,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None: ...
```
- `variant`: `"wave"` / `"standard"`, `"folded"` / `"page"` / `"note"`, `"double_wave"` / `"snippet"`, or `"folded_wave"` / `"report"`.
- `stacked`: Number of stacked document sheets (`>= 1`, default `1`).

### 3.2. `funnel`
Draws a symmetric filtering funnel centered at `xy` tapering from full top `width` down to a central spout.

```python
def funnel(
    xy: tuple[float, float],
    width: float,
    height: float,
    *,
    variant: Literal["standard", "flat", "3d", "cylinder", "curved"] = "standard",
    neck_width_ratio: float | None = None,
    neck_height_ratio: float | None = None,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None: ...
```
- `variant`: `"standard"`, `"flat"`, `"3d"`, `"cylinder"`, or `"curved"`.
- `neck_width_ratio`: Optional bottom spout width ratio in `(0.0, 1.0)`.
- `neck_height_ratio`: Optional bottom spout height ratio in `(0.0, 1.0)`.

```drawlib code=fold align=center file=shapes_container_storage_doc.png caption="cylinder, cube, document (folded), and funnel Primitives"
from drawlib.canvas import save, setup
from drawlib.shapes import cube, cylinder, document, funnel
from drawlib.styles import Styles

setup(width=144, height=48)

cylinder(
    (20, 24),
    width=24,
    height=30,
    disks=2,
    style=Styles.PrimaryNeutral,
    text="Postgres",
    text_style=Styles.DarkBold.patch(text_size=10.0),
)

cube(
    (54, 24),
    width=26,
    height=28,
    style=Styles.Neutral,
    text="Pod Node",
    text_style=Styles.DarkBold.patch(text_size=10.0),
)

document(
    (88, 24),
    width=24,
    height=28,
    variant="folded",
    stacked=2,
    style=Styles.SecondaryNeutral,
    text="config.yml",
    text_style=Styles.DarkBold.patch(text_size=10.0),
)

funnel(
    (122, 24),
    width=28,
    height=26,
    variant="3d",
    style=Styles.PrimaryFlat,
    text="Filter",
    text_style=Styles.WhiteBold.patch(text_size=10.0, xy_abs_shift=(0, 3)),
)

save()
```

---

## 4. Cloud Boundaries & Grouping Braces (`cloud`, `brace`)

### 4.1. `cloud`
Draws a smooth cubic-Bézier cloud silhouette scaled to fit `(width, height)` centered at `xy`.

```python
def cloud(
    xy: tuple[float, float],
    width: float,
    height: float,
    *,
    variant: Literal["standard", "flat", "fluffy", "simple"] = "standard",
    bump_ratio: float | None = None,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None: ...
```
- `variant`: `"standard"`, `"flat"`, `"fluffy"`, or `"simple"`.
- `bump_ratio`: Outward bulge depth ratio strictly in `(0.0, 1.0)`.

### 4.2. `brace`
Draws a **stroke-only** curly (`{`, `}`), square (`[`, `]`), or round (`(`, `)`) grouping bracket centered at `xy` within `(width, height)`. Uses `style.line_color`, `style.line_width`, and `style.line_style`.

```python
def brace(
    xy: tuple[float, float],
    width: float,
    height: float,
    *,
    symbol: Literal["{", "}", "{}", "curly", "[", "]", "[]", "square", "(", ")", "()", "round"] = "{",
    direction: Literal["left", "right", "top", "bottom"] | None = None,
    tip_ratio: float | None = None,
    tip_position_ratio: float | None = None,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None: ...
```
- `symbol`: Bracket family (`"{"`, `"}"`, `"["`, `"]"`, `"("`, `")"`).
- `direction`: Pointing / bowing direction (`"left"`, `"right"`, `"top"`, `"bottom"`). When `None`, inferred from `symbol`.

```drawlib code=fold align=center file=shapes_container_cloud_brace.png caption="cloud Variants and Directional brace Grouping Annotations"
from drawlib.canvas import save, setup
from drawlib.shapes import brace, cloud, rectangle
from drawlib.styles import Styles

setup(width=144, height=50)

cloud(
    (28, 25),
    width=40,
    height=26,
    variant="standard",
    style=Styles.PrimaryNeutral.patch(shape_line_style="dashed"),
    text="Public Cloud",
    text_style=Styles.DarkBold.patch(text_size=10.5),
)

rectangle((78, 34), width=26, height=11, style=Styles.Neutral.patch(shape_r=1.5), text="Worker A")
rectangle((78, 16), width=26, height=11, style=Styles.Neutral.patch(shape_r=1.5), text="Worker B")

brace(
    (96, 25),
    width=5,
    height=30,
    symbol="}",
    style=Styles.DarkBold,
    text="Auto-Scale Pool",
    text_style=Styles.DarkBold.patch(text_size=10.5, halign="left", xy_abs_shift=(2, 0)),
)

save()
```
