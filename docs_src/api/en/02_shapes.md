# drawlib.shapes

`drawlib.shapes` provides 43 vector shape functions spanning basic geometry, polygons, block arrows, 3D containers, callout badges, and status symbols. Every function requires keyword-only `*, style: Style`; import shapes via `from drawlib.shapes import circle, cylinder, rectangle, ...`.

```drawlib align=center code=fold file=02_shapes_hero.png caption="43 Vector Primitives Across 5 Families in drawlib.shapes"
from drawlib.canvas import save, setup
from drawlib.shapes import (
    chevron,
    circle,
    cloud,
    cylinder,
    gear,
    rectangle,
    regularpolygon,
    shield,
    star,
    tag,
)
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=120, height=62, dpi=150)

text(
    (60, 55.5),
    "drawlib.shapes — 43 Vector Primitives (5 Families)",
    style=Styles.DarkBold.patch(text_size=12.2),
)

# 1. Basic Shapes
rectangle((14.7, 27), width=20.4, height=44, style=Styles.Neutral.patch(shape_r=2.0))
text((14.7, 44.5), "Basic", style=Styles.DarkBold.patch(text_size=10.5))
rectangle((14.7, 32.5), width=13, height=7.8, style=Styles.PrimaryNeutral.patch(shape_r=1.8))
circle((14.7, 16.5), radius=5.2, hole_ratio=0.5, style=Styles.SecondaryNeutral)

# 2. Polygons & Stars
rectangle((37.35, 27), width=20.4, height=44, style=Styles.SecondaryNeutral.patch(shape_r=2.0))
text((37.35, 44.5), "Polygons", style=Styles.DarkBold.patch(text_size=10.5))
regularpolygon((37.35, 32.5), 6, 5.5, style=Styles.Neutral.patch(shape_r=0.8))
star((37.35, 16.5), 5, 5.8, 2.6, style=Styles.PrimaryNeutral)

# 3. 3D Containers (Focal Hero)
rectangle((60.0, 27), width=20.4, height=44, style=Styles.PrimaryFlat.patch(shape_r=2.0))
text(
    (60.0, 44.5),
    "Containers",
    style=Styles.WhiteBold.patch(text_size=10.5, text_color=Colors.White),
)
cylinder((60.0, 32.5), width=12, height=9.5, disks=2, style=Styles.Neutral)
cloud((60.0, 16.5), width=14, height=8.5, style=Styles.Neutral)

# 4. Badges & Callouts
rectangle((82.65, 27), width=20.4, height=44, style=Styles.SecondaryNeutral.patch(shape_r=2.0))
text((82.65, 44.5), "Badges", style=Styles.DarkBold.patch(text_size=10.5))
shield((82.65, 32.5), width=10.8, height=10.2, style=Styles.PrimaryNeutral)
tag((82.65, 16.5), width=13.5, height=8.0, hole_ratio=0.22, style=Styles.Neutral)

# 5. Block Arrows & Symbols
rectangle((105.3, 27), width=20.4, height=44, style=Styles.Neutral.patch(shape_r=2.0))
text((105.3, 44.5), "Symbols", style=Styles.DarkBold.patch(text_size=10.5))
chevron((105.3, 32.5), width=13, height=7.8, corner_angle=55, style=Styles.PrimaryNeutral)
gear((105.3, 16.5), 8, 5.6, 4.0, hole_radius=1.8, style=Styles.SecondaryNeutral)

save()
```

### Coordinate Anchor & Styling Summary

- **Center Anchor `(cx, cy)` Default**: 39 shapes (all basic, polygon, 3D container, badge, symbol, and box-bounded arrow shapes except `bubblespeech`) center on `xy = (cx, cy)` by default; override alignment via `style.patch(halign=..., valign=...)`.
- **Non-Center Anchors**: `arrow(xy1, xy2, ...)` spans tail to tip; `arrow_polyline(xys, ...)` and `polygon(xys, ...)` take explicit vertex lists; `bubblespeech(xy, ...)` places `xy` at the **Bottom-Left `(x0, y0)`** of the bubble body.
- **Shared Modifiers**: Patch corner rounding via `style.patch(shape_r=2.0)`, rotation via `style.patch(angle=...)`, and true compound cutouts via `hole_ratio` / `holes`.

---

## `def` arc(xy, width, height, *, style, ...)

Draw a stroke-only elliptical or circular arc shape anchored at **Center `(cx, cy)`** (reads `line_color`, `line_width`, `line_style` from `style`).

```python
def arc(xy: Coordinate, width: PosFloat, height: PosFloat, *, style: Style, angle_start: Angle = 0.0, angle_end: Angle = 360.0, text: str = , text_style: Style | None = None) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *Required* | **Center `(cx, cy)`** of the reference ellipse. |
| `width / height` | `PosFloat` | *Required* | Full horizontal and vertical diameters of the arc ellipse. |
| `angle_start / angle_end` | `Angle` | `0.0 / 360.0` | Start and end sweep angles in CCW degrees (`0°` = right). |
| `style` | `Style` | *Required* | Keyword-only shape `Style` (`shape_fill_color`, `shape_line_*`, `shape_r`, `angle`, `halign`, `valign`). |
| `text` | `str` | `''` | Optional centered label string inside the shape (`\n` supported). |
| `text_style` | `Style \| None` | `None` | Optional typography `Style` override for `text` (e.g. `Styles.WhiteBold`). |

---

## `def` arrow(xy1, xy2, tail_width, head_width, head_length, ...)

Draw a straight 2D filled block arrow directly from tail coordinate **`xy1`** to tip coordinate **`xy2`**.

```python
def arrow(xy1: Coordinate, xy2: Coordinate, tail_width: PosFloat, head_width: PosFloat, head_length: PosFloat, head: ArrowHead = ->, *, style: Style, text: str = , text_style: Style | None = None) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy1 / xy2` | `Coordinate` | *Required* | **Point-Vector** start `(x1, y1)` and tip `(x2, y2)` coordinates. |
| `tail_width` | `PosFloat` | *Required* | Thickness of the arrow shaft. |
| `head_width / head_length` | `PosFloat` | *Required* | Outer width and length of the triangular arrowhead. |
| `head` | `ArrowHead` | `'->'` | Arrowhead placement: `'->'`, `'<-'`, or `'<->'`. |
| `style` | `Style` | *Required* | Keyword-only shape `Style` (`shape_fill_color`, `shape_line_*`, `shape_r`, `angle`, `halign`, `valign`). |
| `text` | `str` | `''` | Optional centered label string inside the shape (`\n` supported). |
| `text_style` | `Style \| None` | `None` | Optional typography `Style` override for `text` (e.g. `Styles.WhiteBold`). |

---

## `def` arrow_arc(xy, width, height, tail_width, head_width, ...)

Draw a curved 2D block arrow along an elliptical ring centered at **Center `(cx, cy)`**.

```python
def arrow_arc(xy: Coordinate, width: PosFloat, height: PosFloat, tail_width: PosFloat, head_width: PosFloat, head_angle: Angle = 10, head: ArrowHead = ->, angle_start: Angle = 0, angle_end: Angle = 180, *, style: Style) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *Required* | **Center `(cx, cy)`** of the arc bounding box. |
| `width / height` | `PosFloat` | *Required* | Outer width and height of the arc ellipse. |
| `tail_width / head_width` | `PosFloat` | *Required* | Shaft thickness and arrowhead width. |
| `head_angle` | `Angle` | `10` | Angular sweep length of the arrowhead in degrees. |
| `head` | `ArrowHead` | `'->'` | Arrowhead direction (`'->'`, `'<-'`, `'<->'`). |
| `angle_start / angle_end` | `Angle` | `0 / 180` | Start and end sweep angles in CCW degrees. |
| `style` | `Style` | *Required* | Keyword-only shape `Style` controlling fill, border stroke, rotation `angle`, and alignment. |

---

## `def` arrow_l(xy, width, height, tail_width, head_width, head_length, ...)

Draw a 90-degree L-shaped 2D block arrow centered at **Center `(cx, cy)`**.

```python
def arrow_l(xy: Coordinate, width: PosFloat, height: PosFloat, tail_width: PosFloat, head_width: PosFloat, head_length: PosFloat, head: ArrowHead = ->, *, style: Style) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *Required* | **Center `(cx, cy)`** of the L-arrow bounding box. |
| `width / height` | `PosFloat` | *Required* | Bounding width and height of the L-shape. |
| `tail_width / head_width / head_length` | `PosFloat` | *Required* | Shaft width, arrowhead width, and arrowhead length. |
| `head` | `ArrowHead` | `'->'` | Arrowhead placement (`'->'`, `'<-'`, `'<->'`). |
| `style` | `Style` | *Required* | Keyword-only shape `Style` controlling fill, border stroke, rotation `angle`, and alignment. |

---

## `def` arrow_polyline(xys, tail_width, head_width, head_length, ...)

Draw a multi-segment 2D filled block arrow routed through explicit **Vertex Waypoints `xys`**.

```python
def arrow_polyline(xys: Coordinates, tail_width: PosFloat, head_width: PosFloat, head_length: PosFloat, head: ArrowHead = ->, *, style: Style) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xys` | `Coordinates` | *Required* | **Waypoint sequence** `[(x0, y0), (x1, y1), ...]` along the shaft centerline. |
| `tail_width / head_width / head_length` | `PosFloat` | *Required* | Shaft width, arrowhead width, and arrowhead length. |
| `head` | `ArrowHead` | `'->'` | Arrowhead placement (`'->'`, `'<-'`, `'<->'`). |
| `style` | `Style` | *Required* | Keyword-only shape `Style` controlling fill, border stroke, rotation `angle`, and alignment. |

---

## `def` arrow_u(xy, width, height, tail_width, head_width, head_length, ...)

Draw a 180-degree U-turn 2D block arrow centered at **Center `(cx, cy)`**.

```python
def arrow_u(xy: Coordinate, width: PosFloat, height: PosFloat, tail_width: PosFloat, head_width: PosFloat, head_length: PosFloat, head: ArrowHead = ->, *, style: Style) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *Required* | **Center `(cx, cy)`** of the U-arrow bounding box. |
| `width / height` | `PosFloat` | *Required* | Bounding width and height of the U-turn arrow. |
| `tail_width / head_width / head_length` | `PosFloat` | *Required* | Shaft width, arrowhead width, and arrowhead length. |
| `head` | `ArrowHead` | `'->'` | Arrowhead placement (`'->'`, `'<-'`, `'<->'`). |
| `style` | `Style` | *Required* | Keyword-only shape `Style` controlling fill, border stroke, rotation `angle`, and alignment. |

---

## `def` brace(xy, width, height, *, symbol='{', ...)

Draw a curly, square, or round grouping brace anchored at **Center `(cx, cy)`** (stroke-only shape using `style.line_*`).

```python
def brace(xy: Coordinate, width: PosFloat, height: PosFloat, *, symbol: BraceSymbol = {, direction: BraceDirection | None = None, tip_ratio: Ratio | None = None, tip_position_ratio: Ratio | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *Required* | **Center `(cx, cy)`** of the brace bounding box. |
| `width / height` | `PosFloat` | *Required* | Bounding box width and height. |
| `symbol` | `BraceSymbol` | `'{'` | `'{'`, `'}'`, `'{}'`, `'curly'`, `'['`, `']'`, `'[]'`, `'square'`, `'('`, `')'`, `'()'`, or `'round'`. |
| `direction` | `BraceDirection \| None` | `None` | Explicit orientation (`'left'`, `'right'`, `'top'`, `'bottom'`) or inferred from `symbol`. |
| `tip_ratio / tip_position_ratio` | `Ratio \| None` | `None` | Curly-brace center tip depth and span position ratios in `(0.0, 1.0)`. |
| `style` | `Style` | *Required* | Keyword-only shape `Style` (`shape_fill_color`, `shape_line_*`, `shape_r`, `angle`, `halign`, `valign`). |
| `text` | `str` | `''` | Optional centered label string inside the shape (`\n` supported). |
| `text_style` | `Style \| None` | `None` | Optional typography `Style` override for `text` (e.g. `Styles.WhiteBold`). |

---

## `def` bubblespeech(xy, width, height, tail_edge, tail_start_ratio, tail_vertex_xy, tail_end_ratio, *, style, ...)

Draw a callout speech bubble whose rectangular body starts at **Bottom-Left `(x0, y0)`** with a triangular pointer reaching `tail_vertex_xy`.

```python
def bubblespeech(xy: Coordinate, width: PosFloat, height: PosFloat, tail_edge: TailEdge, tail_start_ratio: Ratio, tail_vertex_xy: Coordinate, tail_end_ratio: Ratio, *, style: Style, text: str = , text_style: Style | None = None) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *Required* | **Bottom-Left `(x0, y0)`** corner of the rectangular bubble body. |
| `width / height` | `PosFloat` | *Required* | Width and height of the bubble body (excluding tail). |
| `tail_edge` | `TailEdge` | *Required* | Edge where the tail attaches: `'left'`, `'top'`, `'right'`, or `'bottom'`. |
| `tail_start_ratio / tail_end_ratio` | `Ratio` | *Required* | Start and end ratios in `(0.0, 1.0)` along `tail_edge` (`start < end`). |
| `tail_vertex_xy` | `Coordinate` | *Required* | Target canvas coordinate `(tx, ty)` of the speech bubble pointer tip. |
| `style` | `Style` | *Required* | Keyword-only shape `Style` (`shape_fill_color`, `shape_line_*`, `shape_r`, `angle`, `halign`, `valign`). |
| `text` | `str` | `''` | Optional centered label string inside the shape (`\n` supported). |
| `text_style` | `Style \| None` | `None` | Optional typography `Style` override for `text` (e.g. `Styles.WhiteBold`). |

---

## `def` checkmark(xy, width, height=None, *, variant='standard', ...)

Draw a standalone checkmark or circular approval badge centered at **Center `(cx, cy)`**.

```python
def checkmark(xy: Coordinate, width: PosFloat, height: PosFloat | None = None, *, variant: CheckmarkVariant = standard, thickness_ratio: Ratio | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *Required* | **Center `(cx, cy)`** of the checkmark bounding box. |
| `width / height` | `PosFloat / PosFloat \| None` | *Required* / None | Bounding box width and height (`height` defaults to `width`). |
| `variant` | `CheckmarkVariant` | `'standard'` | `'standard'`, `'check'`, `'circle'`, or `'solid_circle'`. |
| `thickness_ratio` | `Ratio \| None` | `None` | Optional stroke bar thickness ratio in `(0.0, 1.0)`. |
| `style` | `Style` | *Required* | Keyword-only shape `Style` (`shape_fill_color`, `shape_line_*`, `shape_r`, `angle`, `halign`, `valign`). |
| `text` | `str` | `''` | Optional centered label string inside the shape (`\n` supported). |
| `text_style` | `Style \| None` | `None` | Optional typography `Style` override for `text` (e.g. `Styles.WhiteBold`). |

---

## `def` chevron(xy, width, height, corner_angle, mirror=False, *, style, ...)

Draw a directional process chevron block centered at **Center `(cx, cy)`** by default (supports `shape_r` rounding).

```python
def chevron(xy: Coordinate, width: PosFloat, height: PosFloat, corner_angle: Angle90, mirror: bool = False, *, style: Style, text: str = , text_style: Style | None = None) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *Required* | **Center `(cx, cy)`** by default (override via `style.patch(halign=..., valign=...)`). |
| `width / height` | `PosFloat` | *Required* | Outer width and height of the chevron block. |
| `corner_angle` | `Angle90` | *Required* | Pointed nose angle in `(0, 90)` degrees. |
| `mirror` | `bool` | `False` | Flip horizontal pointing direction (right-to-left when `True`). |
| `style` | `Style` | *Required* | Keyword-only shape `Style` (`shape_fill_color`, `shape_line_*`, `shape_r`, `angle`, `halign`, `valign`). |
| `text` | `str` | `''` | Optional centered label string inside the shape (`\n` supported). |
| `text_style` | `Style \| None` | `None` | Optional typography `Style` override for `text` (e.g. `Styles.WhiteBold`). |

---

## `def` circle(xy, radius, *, hole_ratio=None, style, ...)

Draw a solid circle or hollow donut ring (`hole_ratio`) centered at **Center `(cx, cy)`**.

```python
def circle(xy: Coordinate, radius: PosFloat, *, hole_ratio: Ratio | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *Required* | **Center `(cx, cy)`** of the circle. |
| `radius` | `PosFloat` | *Required* | Outer radius in canvas units. |
| `hole_ratio` | `Ratio \| None` | `None` | Optional inner transparent hole ratio in `(0.0, 1.0)`. |
| `style` | `Style` | *Required* | Keyword-only shape `Style` (`shape_fill_color`, `shape_line_*`, `shape_r`, `angle`, `halign`, `valign`). |
| `text` | `str` | `''` | Optional centered label string inside the shape (`\n` supported). |
| `text_style` | `Style \| None` | `None` | Optional typography `Style` override for `text` (e.g. `Styles.WhiteBold`). |

---

## `def` clock(xy, radius, *, variant='standard', hour=10.0, minute=10.0, ...)

Draw an analog dial, stopwatch, timer, alarm, or 7-segment digital clock centered at **Center `(cx, cy)`**.

```python
def clock(xy: Coordinate, radius: PosFloat, *, variant: ClockVariant = standard, hour: float = 10.0, minute: float = 10.0, style: Style, text: str = , text_style: Style | None = None) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *Required* | **Center `(cx, cy)`** of the clock. |
| `radius` | `PosFloat` | *Required* | Dial radius (or scale reference for `'digital'`). |
| `variant` | `ClockVariant` | `'standard'` | `'standard'`, `'ticks'`, `'dial'`, `'stopwatch'`, `'timer'`, `'alarm'`, or `'digital'`. |
| `hour / minute` | `float` | `10.0 / 10.0` | Displayed hour and minute hand/digit values. |
| `style` | `Style` | *Required* | Keyword-only shape `Style` (`shape_fill_color`, `shape_line_*`, `shape_r`, `angle`, `halign`, `valign`). |
| `text` | `str` | `''` | Optional centered label string inside the shape (`\n` supported). |
| `text_style` | `Style \| None` | `None` | Optional typography `Style` override for `text` (e.g. `Styles.WhiteBold`). |

---

## `def` cloud(xy, width, height, *, variant='standard', bump_ratio=None, ...)

Draw a network or SaaS cloud container silhouette centered at **Center `(cx, cy)`**.

```python
def cloud(xy: Coordinate, width: PosFloat, height: PosFloat, *, variant: CloudVariant = standard, bump_ratio: Ratio | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *Required* | **Center `(cx, cy)`** of the cloud bounding box. |
| `width / height` | `PosFloat` | *Required* | Outer width and height of the cloud. |
| `variant` | `CloudVariant` | `'standard'` | `'standard'`, `'flat'`, `'fluffy'`, or `'simple'`. |
| `bump_ratio` | `Ratio \| None` | `None` | Optional lobe bulge depth ratio in `(0.0, 1.0)`. |
| `style` | `Style` | *Required* | Keyword-only shape `Style` (`shape_fill_color`, `shape_line_*`, `shape_r`, `angle`, `halign`, `valign`). |
| `text` | `str` | `''` | Optional centered label string inside the shape (`\n` supported). |
| `text_style` | `Style \| None` | `None` | Optional typography `Style` override for `text` (e.g. `Styles.WhiteBold`). |

---

## `def` cube(xy, width, height, *, depth_ratio=None, style, ...)

Draw an isometric 3D cube or rectangular box centered at **Center `(cx, cy)`**.

```python
def cube(xy: Coordinate, width: PosFloat, height: PosFloat, *, depth_ratio: Ratio | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *Required* | **Center `(cx, cy)`** of the outer 3D bounding box. |
| `width / height` | `PosFloat` | *Required* | Total outer width and height including 3D faces. |
| `depth_ratio` | `Ratio \| None` | `None` | Optional 3D extrusion fraction in `(0.0, 1.0)` relative to `min(width, height)`. |
| `style` | `Style` | *Required* | Keyword-only shape `Style` (`shape_fill_color`, `shape_line_*`, `shape_r`, `angle`, `halign`, `valign`). |
| `text` | `str` | `''` | Optional centered label string inside the shape (`\n` supported). |
| `text_style` | `Style \| None` | `None` | Optional typography `Style` override for `text` (e.g. `Styles.WhiteBold`). |

---

## `def` cylinder(xy, width, height, *, style, disks=1, ...)

Draw a 3D database/storage cylinder (with optional multi-disk grooves) centered at **Center `(cx, cy)`**.

```python
def cylinder(xy: Coordinate, width: PosFloat, height: PosFloat, *, style: Style, disks: PosInt = 1, text: str = , text_style: Style | None = None) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *Required* | **Center `(cx, cy)`** of the cylinder. |
| `width / height` | `PosFloat` | *Required* | Total width and height of the cylinder. |
| `disks` | `PosInt` | `1` | Number of stacked top disk tiers (`>= 1`). |
| `style` | `Style` | *Required* | Keyword-only shape `Style` (`shape_fill_color`, `shape_line_*`, `shape_r`, `angle`, `halign`, `valign`). |
| `text` | `str` | `''` | Optional centered label string inside the shape (`\n` supported). |
| `text_style` | `Style \| None` | `None` | Optional typography `Style` override for `text` (e.g. `Styles.WhiteBold`). |

---

## `def` document(xy, width, height, *, variant='wave', stacked=1, ...)

Draw a wavy-bottom, folded-corner, or multi-sheet stacked document shape centered at **Center `(cx, cy)`**.

```python
def document(xy: Coordinate, width: PosFloat, height: PosFloat, *, variant: DocumentVariant = wave, stacked: PosInt = 1, wave_ratio: Ratio | None = None, fold_ratio: Ratio | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *Required* | **Center `(cx, cy)`** of the document bounding box. |
| `width / height` | `PosFloat` | *Required* | Outer width and height of the document. |
| `variant` | `DocumentVariant` | `'wave'` | `'wave'`, `'standard'`, `'folded'`, `'page'`, `'note'`, `'double_wave'`, `'snippet'`, `'folded_wave'`, or `'report'`. |
| `stacked` | `PosInt` | `1` | Number of stacked sheets (`1` for single sheet, `>= 2` for multi-document stack). |
| `wave_ratio / fold_ratio` | `Ratio \| None` | `None` | Optional bottom wave amplitude and corner fold size ratios in `(0.0, 1.0)`. |
| `style` | `Style` | *Required* | Keyword-only shape `Style` (`shape_fill_color`, `shape_line_*`, `shape_r`, `angle`, `halign`, `valign`). |
| `text` | `str` | `''` | Optional centered label string inside the shape (`\n` supported). |
| `text_style` | `Style \| None` | `None` | Optional typography `Style` override for `text` (e.g. `Styles.WhiteBold`). |

---

## `def` ellipse(xy, width, height, *, hole_ratio=None, style, ...)

Draw a solid ellipse or hollow oval ring (`hole_ratio`) centered at **Center `(cx, cy)`**.

```python
def ellipse(xy: Coordinate, width: PosFloat, height: PosFloat, *, hole_ratio: Ratio | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *Required* | **Center `(cx, cy)`** of the ellipse. |
| `width / height` | `PosFloat` | *Required* | Horizontal width (`2 * rx`) and vertical height (`2 * ry`). |
| `hole_ratio` | `Ratio \| None` | `None` | Optional inner cutout hole ratio in `(0.0, 1.0)`. |
| `style` | `Style` | *Required* | Keyword-only shape `Style` (`shape_fill_color`, `shape_line_*`, `shape_r`, `angle`, `halign`, `valign`). |
| `text` | `str` | `''` | Optional centered label string inside the shape (`\n` supported). |
| `text_style` | `Style \| None` | `None` | Optional typography `Style` override for `text` (e.g. `Styles.WhiteBold`). |

---

## `def` explosion(xy, width, height, *, variant='standard', style, ...)

Draw an asymmetric impact burst or incident callout star centered at **Center `(cx, cy)`**.

```python
def explosion(xy: Coordinate, width: PosFloat, height: PosFloat, *, variant: ExplosionVariant = standard, style: Style, text: str = , text_style: Style | None = None) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *Required* | **Center `(cx, cy)`** of the explosion bounding box. |
| `width / height` | `PosFloat` | *Required* | Outer width and height of the burst. |
| `variant` | `ExplosionVariant` | `'standard'` | `'standard'`, `'irregular'`, `'heavy'`, `'wild'`, `'curved'`, or `'comic'`. |
| `style` | `Style` | *Required* | Keyword-only shape `Style` (`shape_fill_color`, `shape_line_*`, `shape_r`, `angle`, `halign`, `valign`). |
| `text` | `str` | `''` | Optional centered label string inside the shape (`\n` supported). |
| `text_style` | `Style \| None` | `None` | Optional typography `Style` override for `text` (e.g. `Styles.WhiteBold`). |

---

## `def` face(xy, radius, *, variant='smile', style, ...)

Draw an expressive user-sentiment or incident-status face icon shape centered at **Center `(cx, cy)`**.

```python
def face(xy: Coordinate, radius: PosFloat, *, variant: FaceVariant = smile, style: Style, text: str = , text_style: Style | None = None) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *Required* | **Center `(cx, cy)`** of the face circle. |
| `radius` | `PosFloat` | *Required* | Outer radius of the face. |
| `variant` | `FaceVariant` | `'smile'` | `'smile'`, `'neutral'`, `'sad'`, `'angry'`, `'surprised'`, `'dizzy'`, `'dead'`, `'skull'`, or `'devil'`. |
| `style` | `Style` | *Required* | Keyword-only shape `Style` (`shape_fill_color`, `shape_line_*`, `shape_r`, `angle`, `halign`, `valign`). |
| `text` | `str` | `''` | Optional centered label string inside the shape (`\n` supported). |
| `text_style` | `Style \| None` | `None` | Optional typography `Style` override for `text` (e.g. `Styles.WhiteBold`). |

---

## `def` fan(xy, radius, *, style, angle_start=0, angle_end=180, ...)

Draw a filled pie-sector fan shape centered at **Center `(cx, cy)`**.

```python
def fan(xy: Coordinate, radius: PosFloat, *, style: Style, angle_start: Angle = 0, angle_end: Angle = 180, text: str = , text_style: Style | None = None) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *Required* | **Center `(cx, cy)`** of the fan circle. |
| `radius` | `PosFloat` | *Required* | Radius of the sector. |
| `angle_start / angle_end` | `Angle` | `0 / 180` | Starting and ending angles in CCW degrees. |
| `style` | `Style` | *Required* | Keyword-only shape `Style` (`shape_fill_color`, `shape_line_*`, `shape_r`, `angle`, `halign`, `valign`). |
| `text` | `str` | `''` | Optional centered label string inside the shape (`\n` supported). |
| `text_style` | `Style \| None` | `None` | Optional typography `Style` override for `text` (e.g. `Styles.WhiteBold`). |

---

## `def` forbidden(xy, radius, *, variant='slash', thickness_ratio=None, ...)

Draw a prohibited / deny / no-entry symbol centered at **Center `(cx, cy)`**.

```python
def forbidden(xy: Coordinate, radius: PosFloat, *, variant: ForbiddenVariant = slash, thickness_ratio: Ratio | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *Required* | **Center `(cx, cy)`** of the forbidden circle. |
| `radius` | `PosFloat` | *Required* | Outer circle radius. |
| `variant` | `ForbiddenVariant` | `'slash'` | `'slash'`, `'standard'`, `'backslash'`, `'cross'`, `'no_entry'`, or `'minus'`. |
| `thickness_ratio` | `Ratio \| None` | `None` | Optional ring and bar thickness ratio in `(0.0, 1.0)`. |
| `style` | `Style` | *Required* | Keyword-only shape `Style` (`shape_fill_color`, `shape_line_*`, `shape_r`, `angle`, `halign`, `valign`). |
| `text` | `str` | `''` | Optional centered label string inside the shape (`\n` supported). |
| `text_style` | `Style \| None` | `None` | Optional typography `Style` override for `text` (e.g. `Styles.WhiteBold`). |

---

## `def` funnel(xy, width, height, *, variant='standard', ...)

Draw a filtering or conversion pipeline funnel shape centered at **Center `(cx, cy)`**.

```python
def funnel(xy: Coordinate, width: PosFloat, height: PosFloat, *, variant: FunnelVariant = standard, neck_width_ratio: Ratio | None = None, neck_height_ratio: Ratio | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *Required* | **Center `(cx, cy)`** of the funnel bounding box. |
| `width / height` | `PosFloat` | *Required* | Top opening width and total funnel height. |
| `variant` | `FunnelVariant` | `'standard'` | `'standard'`, `'flat'`, `'3d'`, `'cylinder'`, or `'curved'`. |
| `neck_width_ratio / neck_height_ratio` | `Ratio \| None` | `None` | Optional bottom spout width and height ratios in `(0.0, 1.0)`. |
| `style` | `Style` | *Required* | Keyword-only shape `Style` (`shape_fill_color`, `shape_line_*`, `shape_r`, `angle`, `halign`, `valign`). |
| `text` | `str` | `''` | Optional centered label string inside the shape (`\n` supported). |
| `text_style` | `Style \| None` | `None` | Optional typography `Style` override for `text` (e.g. `Styles.WhiteBold`). |

---

## `def` gear(xy, num_teeth, radius_ext, radius_int, *, hole_radius=None, ...)

Draw a mechanical cog / worker-engine gear shape centered at **Center `(cx, cy)`**.

```python
def gear(xy: Coordinate, num_teeth: NumVertex, radius_ext: PosFloat, radius_int: PosFloat, *, tooth_ext_ratio: Ratio | None = None, tooth_int_ratio: Ratio | None = None, hole_radius: PosFloat | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *Required* | **Center `(cx, cy)`** of the gear. |
| `num_teeth` | `NumVertex` | *Required* | Number of gear teeth (`>= 3`). |
| `radius_ext / radius_int` | `PosFloat` | *Required* | Outer tooth-tip radius and inner tooth-valley radius. |
| `tooth_ext_ratio / tooth_int_ratio` | `Ratio \| None` | `None (0.35 / 0.55)` | Angular pitch fractions for outer tip and inner root widths. |
| `hole_radius` | `PosFloat \| None` | `None` | Optional center axle cutout radius. |
| `style` | `Style` | *Required* | Keyword-only shape `Style` (`shape_fill_color`, `shape_line_*`, `shape_r`, `angle`, `halign`, `valign`). |
| `text` | `str` | `''` | Optional centered label string inside the shape (`\n` supported). |
| `text_style` | `Style \| None` | `None` | Optional typography `Style` override for `text` (e.g. `Styles.WhiteBold`). |

---

## `def` heart(xy, width, height, *, variant='standard', style, ...)

Draw a health-check heart or broken-heart shape centered at **Center `(cx, cy)`**.

```python
def heart(xy: Coordinate, width: PosFloat, height: PosFloat, *, variant: HeartVariant = standard, style: Style, text: str = , text_style: Style | None = None) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *Required* | **Center `(cx, cy)`** of the heart bounding box. |
| `width / height` | `PosFloat` | *Required* | Bounding box width and height. |
| `variant` | `HeartVariant` | `'standard'` | `'standard'`, `'classic'`, or `'broken'`. |
| `style` | `Style` | *Required* | Keyword-only shape `Style` (`shape_fill_color`, `shape_line_*`, `shape_r`, `angle`, `halign`, `valign`). |
| `text` | `str` | `''` | Optional centered label string inside the shape (`\n` supported). |
| `text_style` | `Style \| None` | `None` | Optional typography `Style` override for `text` (e.g. `Styles.WhiteBold`). |

---

## `def` lightning(xy, width, height, *, variant='standard', mirror=False, ...)

Draw a high-voltage / fast-execution / event-trigger lightning bolt centered at **Center `(cx, cy)`**.

```python
def lightning(xy: Coordinate, width: PosFloat, height: PosFloat, *, variant: LightningVariant = standard, mirror: bool = False, style: Style, text: str = , text_style: Style | None = None) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *Required* | **Center `(cx, cy)`** of the lightning bounding box. |
| `width / height` | `PosFloat` | *Required* | Bounding box width and height. |
| `variant` | `LightningVariant` | `'standard'` | `'standard'`, `'flat'`, `'double'`, `'flat_double'`, `'angled'`, or `'slanted'`. |
| `mirror` | `bool` | `False` | Flip bolt horizontally when `True`. |
| `style` | `Style` | *Required* | Keyword-only shape `Style` (`shape_fill_color`, `shape_line_*`, `shape_r`, `angle`, `halign`, `valign`). |
| `text` | `str` | `''` | Optional centered label string inside the shape (`\n` supported). |
| `text_style` | `Style \| None` | `None` | Optional typography `Style` override for `text` (e.g. `Styles.WhiteBold`). |

---

## `def` math_symbol(xy, symbol, width, height=None, *, thickness_ratio=None, ...)

Draw a geometric mathematical operator shape (`+`, `-`, `×`, `÷`, `=`, `≠`) centered at **Center `(cx, cy)`**.

```python
def math_symbol(xy: Coordinate, symbol: MathSymbol, width: PosFloat, height: PosFloat | None = None, *, thickness_ratio: Ratio | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *Required* | **Center `(cx, cy)`** of the operator symbol. |
| `symbol` | `MathSymbol` | *Required* | `'+'`, `'-'`, `'*'`, `'x'`, `'×'`, `'/'`, `'÷'`, `'='`, `'!='`, or `'≠'`. |
| `width / height` | `PosFloat / PosFloat \| None` | *Required* / None | Symbol bounding width and height (`height` defaults to `width`). |
| `thickness_ratio` | `Ratio \| None` | `None (0.28)` | Bar thickness ratio relative to `min(width, height)`. |
| `style` | `Style` | *Required* | Keyword-only shape `Style` (`shape_fill_color`, `shape_line_*`, `shape_r`, `angle`, `halign`, `valign`). |
| `text` | `str` | `''` | Optional centered label string inside the shape (`\n` supported). |
| `text_style` | `Style \| None` | `None` | Optional typography `Style` override for `text` (e.g. `Styles.WhiteBold`). |

---

## `def` moon(xy, width, height, *, variant='crescent', mirror=False, ...)

Draw a crescent or half-moon shape (dark-mode / night-batch indicator) centered at **Center `(cx, cy)`**.

```python
def moon(xy: Coordinate, width: PosFloat, height: PosFloat, *, variant: MoonVariant = crescent, mirror: bool = False, style: Style, text: str = , text_style: Style | None = None) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *Required* | **Center `(cx, cy)`** of the moon bounding box. |
| `width / height` | `PosFloat` | *Required* | Bounding box width and height. |
| `variant` | `MoonVariant` | `'crescent'` | `'crescent'`, `'standard'`, `'thin'`, `'waxing'`, or `'half'`. |
| `mirror` | `bool` | `False` | Flip moon orientation horizontally when `True`. |
| `style` | `Style` | *Required* | Keyword-only shape `Style` (`shape_fill_color`, `shape_line_*`, `shape_r`, `angle`, `halign`, `valign`). |
| `text` | `str` | `''` | Optional centered label string inside the shape (`\n` supported). |
| `text_style` | `Style \| None` | `None` | Optional typography `Style` override for `text` (e.g. `Styles.WhiteBold`). |

---

## `def` parallelogram(xy, width, height, corner_angle, *, hole_ratio=None, ...)

Draw a slanted parallelogram (flowchart I/O block) centered at **Center `(cx, cy)`** with optional `shape_r` and `hole_ratio`.

```python
def parallelogram(xy: Coordinate, width: PosFloat, height: PosFloat, corner_angle: Angle90, *, hole_ratio: Ratio | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *Required* | **Center `(cx, cy)`** by default. |
| `width / height` | `PosFloat` | *Required* | Total bounding width and vertical height. |
| `corner_angle` | `Angle90` | *Required* | Bottom-left acute slant angle in `(0, 90)` degrees. |
| `hole_ratio` | `Ratio \| None` | `None` | Optional inner hollow cutout ratio in `(0.0, 1.0)`. |
| `style` | `Style` | *Required* | Keyword-only shape `Style` (`shape_fill_color`, `shape_line_*`, `shape_r`, `angle`, `halign`, `valign`). |
| `text` | `str` | `''` | Optional centered label string inside the shape (`\n` supported). |
| `text_style` | `Style \| None` | `None` | Optional typography `Style` override for `text` (e.g. `Styles.WhiteBold`). |

---

## `def` pin(xy, width, height, *, variant='pointer', hole_ratio=None, ...)

Draw a map location pin or teardrop callout pointer centered at **Center `(cx, cy)`**.

```python
def pin(xy: Coordinate, width: PosFloat, height: PosFloat, *, variant: PinVariant = pointer, hole_ratio: Ratio | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *Required* | **Center `(cx, cy)`** of the pin bounding box. |
| `width / height` | `PosFloat` | *Required* | Bounding box width and height. |
| `variant` | `PinVariant` | `'pointer'` | `'pointer'`, `'standard'`, `'teardrop'`, `'drop'`, `'pin'`, or `'badge'`. |
| `hole_ratio` | `Ratio \| None` | `None` | Optional circular hole ratio inside the pin head. |
| `style` | `Style` | *Required* | Keyword-only shape `Style` (`shape_fill_color`, `shape_line_*`, `shape_r`, `angle`, `halign`, `valign`). |
| `text` | `str` | `''` | Optional centered label string inside the shape (`\n` supported). |
| `text_style` | `Style \| None` | `None` | Optional typography `Style` override for `text` (e.g. `Styles.WhiteBold`). |

---

## `def` plaque(xy, width, height, *, variant='concave', cut_ratio=None, ...)

Draw a corner-notched or chamfered ornamental plaque plate centered at **Center `(cx, cy)`**.

```python
def plaque(xy: Coordinate, width: PosFloat, height: PosFloat, *, variant: PlaqueVariant = concave, cut_ratio: Ratio | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *Required* | **Center `(cx, cy)`** of the plaque. |
| `width / height` | `PosFloat` | *Required* | Outer width and height. |
| `variant` | `PlaqueVariant` | `'concave'` | `'concave'`, `'standard'`, `'chamfered'`, `'octagon'`, or `'notched'`. |
| `cut_ratio` | `Ratio \| None` | `None` | Optional corner cutout depth ratio in `(0.0, 1.0)`. |
| `style` | `Style` | *Required* | Keyword-only shape `Style` (`shape_fill_color`, `shape_line_*`, `shape_r`, `angle`, `halign`, `valign`). |
| `text` | `str` | `''` | Optional centered label string inside the shape (`\n` supported). |
| `text_style` | `Style \| None` | `None` | Optional typography `Style` override for `text` (e.g. `Styles.WhiteBold`). |

---

## `def` polygon(xys, *, holes=None, style, ...)

Draw a custom closed polygon through explicit **Exterior Vertices `xys`** with optional interior cutout `holes` and `shape_r` corner rounding.

```python
def polygon(xys: Coordinates, *, holes: list[Coordinates] | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xys` | `Coordinates` | *Required* | **Exterior vertex list** `[(x1, y1), ..., (xn, yn)]`. |
| `holes` | `list[Coordinates] \| None` | `None` | Optional list of interior polygon hole vertex lists. |
| `style` | `Style` | *Required* | Keyword-only shape `Style` (`shape_fill_color`, `shape_line_*`, `shape_r`, `angle`, `halign`, `valign`). |
| `text` | `str` | `''` | Optional centered label string inside the shape (`\n` supported). |
| `text_style` | `Style \| None` | `None` | Optional typography `Style` override for `text` (e.g. `Styles.WhiteBold`). |

---

## `def` rectangle(xy, width, height, *, hole_ratio=None, style, ...)

Draw a sharp or rounded (`style.patch(shape_r=...)`) rectangle or hollow frame (`hole_ratio`) centered at **Center `(cx, cy)`**.

```python
def rectangle(xy: Coordinate, width: PosFloat, height: PosFloat, *, hole_ratio: Ratio | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *Required* | **Center `(cx, cy)`** by default (override via `style.patch(halign=..., valign=...)`). |
| `width / height` | `PosFloat` | *Required* | Horizontal width and vertical height in canvas units. |
| `hole_ratio` | `Ratio \| None` | `None` | Optional inner frame cutout ratio in `(0.0, 1.0)`. |
| `style` | `Style` | *Required* | Keyword-only shape `Style` (`shape_fill_color`, `shape_line_*`, `shape_r`, `angle`, `halign`, `valign`). |
| `text` | `str` | `''` | Optional centered label string inside the shape (`\n` supported). |
| `text_style` | `Style \| None` | `None` | Optional typography `Style` override for `text` (e.g. `Styles.WhiteBold`). |

---

## `def` regularpolygon(xy, num_vertex, radius, *, hole_ratio=None, style, ...)

Draw an $N$-sided regular polygon (pentagon, hexagon, octagon, etc.) circumscribed by `radius` around **Center `(cx, cy)`**.

```python
def regularpolygon(xy: Coordinate, num_vertex: NumVertex, radius: PosFloat, *, hole_ratio: Ratio | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *Required* | **Center `(cx, cy)`** of the circumscribed circle. |
| `num_vertex` | `NumVertex` | *Required* | Number of polygon vertices/sides (`>= 3`). |
| `radius` | `PosFloat` | *Required* | Circumscribed circle radius. |
| `hole_ratio` | `Ratio \| None` | `None` | Optional inner hollow ring ratio in `(0.0, 1.0)`. |
| `style` | `Style` | *Required* | Keyword-only shape `Style` (`shape_fill_color`, `shape_line_*`, `shape_r`, `angle`, `halign`, `valign`). |
| `text` | `str` | `''` | Optional centered label string inside the shape (`\n` supported). |
| `text_style` | `Style \| None` | `None` | Optional typography `Style` override for `text` (e.g. `Styles.WhiteBold`). |

---

## `def` rhombus(xy, width, height, *, hole_ratio=None, style, ...)

Draw a diamond / flowchart decision rhombus centered at **Center `(cx, cy)`** with diagonals `width` and `height`.

```python
def rhombus(xy: Coordinate, width: PosFloat, height: PosFloat, *, hole_ratio: Ratio | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *Required* | **Center `(cx, cy)`** by default. |
| `width / height` | `PosFloat` | *Required* | Horizontal and vertical diagonal lengths. |
| `hole_ratio` | `Ratio \| None` | `None` | Optional inner hollow cutout ratio in `(0.0, 1.0)`. |
| `style` | `Style` | *Required* | Keyword-only shape `Style` (`shape_fill_color`, `shape_line_*`, `shape_r`, `angle`, `halign`, `valign`). |
| `text` | `str` | `''` | Optional centered label string inside the shape (`\n` supported). |
| `text_style` | `Style \| None` | `None` | Optional typography `Style` override for `text` (e.g. `Styles.WhiteBold`). |

---

## `def` ribbon(xy, width, height, *, variant='down', ...)

Draw a decorative title or milestone ribbon banner centered at **Center `(cx, cy)`**.

```python
def ribbon(xy: Coordinate, width: PosFloat, height: PosFloat, *, variant: RibbonVariant = down, tail_width_ratio: Ratio | None = None, drop_ratio: Ratio | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *Required* | **Center `(cx, cy)`** of the ribbon bounding box. |
| `width / height` | `PosFloat` | *Required* | Outer width and height of the ribbon. |
| `variant` | `RibbonVariant` | `'down'` | `'down'`, `'standard'`, `'up'`, `'flat'`, or `'banner'`. |
| `tail_width_ratio / drop_ratio` | `Ratio \| None` | `None` | Optional side tail width and vertical step drop ratios in `(0.0, 1.0)`. |
| `style` | `Style` | *Required* | Keyword-only shape `Style` (`shape_fill_color`, `shape_line_*`, `shape_r`, `angle`, `halign`, `valign`). |
| `text` | `str` | `''` | Optional centered label string inside the shape (`\n` supported). |
| `text_style` | `Style \| None` | `None` | Optional typography `Style` override for `text` (e.g. `Styles.WhiteBold`). |

---

## `def` shape(xy, path_points, *, style, ..., is_default_center=False)

Low-level vector path primitive rendering custom straight and quadratic/cubic Bézier `path_points` centered on **`xy = (cx, cy)`** by default.

```python
def shape(xy: Coordinate, path_points: PathPoints, *, style: Style, text: str = , text_style: Style | None = None, is_default_center: bool = False) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *Required* | Target anchor coordinate (`(cx, cy)` when `halign`/`valign` are centered). |
| `path_points` | `PathPoints` | *Required* | List of `(x, y)`, `(cp, end)`, or `(cp1, cp2, end)` local path tuples. |
| `is_default_center` | `bool` | `False` | Controls alignment reference origin when explicit `halign`/`valign` shifts are applied. |
| `style` | `Style` | *Required* | Keyword-only shape `Style` (`shape_fill_color`, `shape_line_*`, `shape_r`, `angle`, `halign`, `valign`). |
| `text` | `str` | `''` | Optional centered label string inside the shape (`\n` supported). |
| `text_style` | `Style \| None` | `None` | Optional typography `Style` override for `text` (e.g. `Styles.WhiteBold`). |

---

## `def` shield(xy, width, height, *, variant='classic', style, ...)

Draw a security, firewall, or IAM protection shield centered at **Center `(cx, cy)`**.

```python
def shield(xy: Coordinate, width: PosFloat, height: PosFloat, *, variant: ShieldVariant = classic, style: Style, text: str = , text_style: Style | None = None) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *Required* | **Center `(cx, cy)`** of the shield bounding box. |
| `width / height` | `PosFloat` | *Required* | Shield width and height. |
| `variant` | `ShieldVariant` | `'classic'` | `'classic'`, `'standard'`, `'flat'`, `'heater'`, or `'round'`. |
| `style` | `Style` | *Required* | Keyword-only shape `Style` (`shape_fill_color`, `shape_line_*`, `shape_r`, `angle`, `halign`, `valign`). |
| `text` | `str` | `''` | Optional centered label string inside the shape (`\n` supported). |
| `text_style` | `Style \| None` | `None` | Optional typography `Style` override for `text` (e.g. `Styles.WhiteBold`). |

---

## `def` star(xy, num_vertex, radius_ext, radius_int, *, style, ...)

Draw an $N$-pointed star shape centered at **Center `(cx, cy)`** (supports `shape_r` tip rounding).

```python
def star(xy: Coordinate, num_vertex: NumVertex, radius_ext: PosFloat, radius_int: PosFloat, *, style: Style, text: str = , text_style: Style | None = None) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *Required* | **Center `(cx, cy)`** of the star. |
| `num_vertex` | `NumVertex` | *Required* | Number of outer star points (`>= 3`). |
| `radius_ext / radius_int` | `PosFloat` | *Required* | Outer point radius and inner valley radius. |
| `style` | `Style` | *Required* | Keyword-only shape `Style` (`shape_fill_color`, `shape_line_*`, `shape_r`, `angle`, `halign`, `valign`). |
| `text` | `str` | `''` | Optional centered label string inside the shape (`\n` supported). |
| `text_style` | `Style \| None` | `None` | Optional typography `Style` override for `text` (e.g. `Styles.WhiteBold`). |

---

## `def` sun(xy, radius, *, variant='rays', num_rays=8, ...)

Draw a sun icon shape with surrounding rays centered at **Center `(cx, cy)`**.

```python
def sun(xy: Coordinate, radius: PosFloat, *, variant: SunVariant = rays, num_rays: NumVertex = 8, style: Style, text: str = , text_style: Style | None = None) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *Required* | **Center `(cx, cy)`** of the sun. |
| `radius` | `PosFloat` | *Required* | Outer radius to the tips of the rays. |
| `variant` | `SunVariant` | `'rays'` | `'rays'`, `'standard'`, `'ring'`, or `'beams'`. |
| `num_rays` | `NumVertex` | `8` | Number of surrounding rays (`>= 3`). |
| `style` | `Style` | *Required* | Keyword-only shape `Style` (`shape_fill_color`, `shape_line_*`, `shape_r`, `angle`, `halign`, `valign`). |
| `text` | `str` | `''` | Optional centered label string inside the shape (`\n` supported). |
| `text_style` | `Style \| None` | `None` | Optional typography `Style` override for `text` (e.g. `Styles.WhiteBold`). |

---

## `def` tag(xy, width, height, *, variant='angled', mirror=False, hole_ratio=None, ...)

Draw a version/metadata label tag with an optional punch hole centered at **Center `(cx, cy)`**.

```python
def tag(xy: Coordinate, width: PosFloat, height: PosFloat, *, variant: TagVariant = angled, mirror: bool = False, hole_ratio: Ratio | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *Required* | **Center `(cx, cy)`** of the tag bounding box. |
| `width / height` | `PosFloat` | *Required* | Tag width and height. |
| `variant` | `TagVariant` | `'angled'` | `'angled'`, `'standard'`, `'chamfered'`, `'beveled'`, or `'rounded'`. |
| `mirror` | `bool` | `False` | Flip tag tip direction horizontally when `True`. |
| `hole_ratio` | `Ratio \| None` | `None` | Optional punch-hole size ratio in `(0.0, 1.0)`. |
| `style` | `Style` | *Required* | Keyword-only shape `Style` (`shape_fill_color`, `shape_line_*`, `shape_r`, `angle`, `halign`, `valign`). |
| `text` | `str` | `''` | Optional centered label string inside the shape (`\n` supported). |
| `text_style` | `Style \| None` | `None` | Optional typography `Style` override for `text` (e.g. `Styles.WhiteBold`). |

---

## `def` trapezoid(xy, height, bottomedge_width, topedge_width, topedge_x=None, *, hole_ratio=None, ...)

Draw a symmetric or asymmetric trapezoid centered at **Center `(cx, cy)`** (supports `shape_r` and `hole_ratio`).

```python
def trapezoid(xy: Coordinate, height: PosFloat, bottomedge_width: PosFloat, topedge_width: PosFloat, topedge_x: float | None = None, *, hole_ratio: Ratio | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *Required* | **Center `(cx, cy)`** by default. |
| `height` | `PosFloat` | *Required* | Vertical height of the trapezoid. |
| `bottomedge_width / topedge_width` | `PosFloat` | *Required* | Lengths of the bottom and top parallel edges. |
| `topedge_x` | `float \| None` | `None` | Horizontal offset of the top-left vertex (centered symmetrically when `None`). |
| `hole_ratio` | `Ratio \| None` | `None` | Optional inner hollow cutout ratio in `(0.0, 1.0)`. |
| `style` | `Style` | *Required* | Keyword-only shape `Style` (`shape_fill_color`, `shape_line_*`, `shape_r`, `angle`, `halign`, `valign`). |
| `text` | `str` | `''` | Optional centered label string inside the shape (`\n` supported). |
| `text_style` | `Style \| None` | `None` | Optional typography `Style` override for `text` (e.g. `Styles.WhiteBold`). |

---

## `def` triangle(xy, width, height, topvertex_x=None, *, hole_ratio=None, ...)

Draw an isosceles or custom-apex triangle centered at **Center `(cx, cy)`** (supports `shape_r` and `hole_ratio`).

```python
def triangle(xy: Coordinate, width: PosFloat, height: PosFloat, topvertex_x: float | None = None, *, hole_ratio: Ratio | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *Required* | **Center `(cx, cy)`** by default. |
| `width / height` | `PosFloat` | *Required* | Base width and vertical height. |
| `topvertex_x` | `float \| None` | `None` | X-offset of the apex from the left base vertex (`width / 2` when `None`). |
| `hole_ratio` | `Ratio \| None` | `None` | Optional inner hollow cutout ratio in `(0.0, 1.0)`. |
| `style` | `Style` | *Required* | Keyword-only shape `Style` (`shape_fill_color`, `shape_line_*`, `shape_r`, `angle`, `halign`, `valign`). |
| `text` | `str` | `''` | Optional centered label string inside the shape (`\n` supported). |
| `text_style` | `Style \| None` | `None` | Optional typography `Style` override for `text` (e.g. `Styles.WhiteBold`). |

---

## `def` wedge(xy, radius, *, style, width=None, angle_start=0, angle_end=360, ...)

Draw a full circular wedge or annular ring sector (`width` thickness) centered at **Center `(cx, cy)`**.

```python
def wedge(xy: Coordinate, radius: PosFloat, *, style: Style, width: PosFloat | None = None, angle_start: Angle = 0, angle_end: Angle = 360, text: str = , text_style: Style | None = None) -> None
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *Required* | **Center `(cx, cy)`** of the wedge circle. |
| `radius` | `PosFloat` | *Required* | Outer radius of the wedge. |
| `width` | `PosFloat \| None` | `None` | Radial ring thickness (`inner_radius = radius - width`; solid sector when `None`). |
| `angle_start / angle_end` | `Angle` | `0 / 360` | Start and end sweep angles in CCW degrees. |
| `style` | `Style` | *Required* | Keyword-only shape `Style` (`shape_fill_color`, `shape_line_*`, `shape_r`, `angle`, `halign`, `valign`). |
| `text` | `str` | `''` | Optional centered label string inside the shape (`\n` supported). |
| `text_style` | `Style \| None` | `None` | Optional typography `Style` override for `text` (e.g. `Styles.WhiteBold`). |
