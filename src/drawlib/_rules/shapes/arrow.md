# Drawlib Arrow Shapes Guidelines (`lib-shapes-arrow`)

API specification and geometric rules for thick filled block arrows and process step chevrons in `drawlib._core.l4_canvas._shapes._arrow` (`arrow`, `arrow_polyline`, `arrow_arc`, `arrow_l`, `arrow_u`, `chevron`). See `lib-shapes-overview` for universal coordinate and styling rules, or `lib-lines` for thin 1D connector lines.

---

## 1. Summary of Block Arrow Shapes

All block arrow functions require `*, style: Style` as a **mandatory keyword-only argument**. Only `arrow` and `chevron` accept `text` and `text_style`; the curved and bent block arrows (`arrow_polyline`, `arrow_arc`, `arrow_l`, `arrow_u`) do **not** accept `text` or `text_style`.

| Function | Coordinate Anchor | Head Options (`ArrowHead`) | Inline `text` / `text_style` | Primary Use Cases |
| :--- | :--- | :---: | :---: | :--- |
| **`arrow`** | Point-to-Point (`xy1` $\to$ `xy2`) | `"->"`, `"<-"`, `"<->"` | **Yes** | Emphasized data flows, stage transitions, hero callout arrows |
| **`arrow_polyline`** | Multi-Point Path (`xys`) | `"->"`, `"<-"`, `"<->"` | **No** | Orthogonal multi-segment block pipelines |
| **`arrow_arc`** | Center `(cx, cy)` of ellipse `(width, height)` | `"->"`, `"<-"`, `"<->"` | **No** | Circular feedback loops, PDCA/DevOps cycles |
| **`arrow_l`** | Center `(cx, cy)` of `(width, height)` box | `"->"`, `"<-"`, `"<->"` | **No** | 90° L-bend corner transfers |
| **`arrow_u`** | Center `(cx, cy)` of `(width, height)` box | `"->"`, `"<-"`, `"<->"` | **No** | 180° U-turn rollback/retry arrows |
| **`chevron`** | Center `(cx, cy)` of `(width, height)` box | `mirror: bool = False` | **Yes** | Sequential pipeline banners, phase headers |

---

## 2. Straight & Multi-Segment Block Arrows (`arrow`, `arrow_polyline`)

### 2.1. `arrow`
Draws a straight filled polygon block arrow from start point `xy1` to end point `xy2`.

```python
def arrow(
    xy1: tuple[float, float],
    xy2: tuple[float, float],
    tail_width: float,
    head_width: float,
    head_length: float,
    head: Literal["->", "<-", "<->"] = "->",
    *,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None: ...
```
- **Parameters**:
  - `xy1`, `xy2`: Start `(x1, y1)` and end `(x2, y2)` coordinates. Total distance must exceed `head_length` (or `2 * head_length` for `"<->"`).
  - `tail_width`: Shaft thickness ($> 0$).
  - `head_width`: Outer width of the arrowhead fin ($> \text{tail\_width}$).
  - `head_length`: Length of the arrowhead along the shaft vector ($> 0$).
  - `head`: `"->"` (tip at `xy2`), `"<-"` (tip at `xy1`), or `"<->"` (bidirectional).
  - `style`: Required keyword-only `Style` (`halign`/`valign` are ignored).
  - `text`, `text_style`: Optional label rendered at the midpoint between `xy1` and `xy2` and rotated along the shaft angle.

### 2.2. `arrow_polyline`
Draws a continuous multi-segment block arrow along waypoint list `xys` with automatically mitered interior corners. **Does not accept `text` or `text_style`.**

```python
def arrow_polyline(
    xys: list[tuple[float, float]],
    tail_width: float,
    head_width: float,
    head_length: float,
    head: Literal["->", "<-", "<->"] = "->",
    *,
    style: Style,
) -> None: ...
```

---

## 3. Curved & Bent Block Arrows (`arrow_arc`, `arrow_l`, `arrow_u`)

> **Important Signature Rule**: `arrow_arc`, `arrow_l`, and `arrow_u` are **Center-Anchored at `xy = (cx, cy)`** and do **not** accept `text` or `text_style` parameters. If you need a label inside or beside an `arrow_arc` loop, call `drawlib.text.text((cx, cy), ...)` separately.

### 3.1. `arrow_arc`
Draws a curved block arrow following an elliptical ring path centered at `xy` from `angle_start` to `angle_end` (CCW degrees).

```python
def arrow_arc(
    xy: tuple[float, float],
    width: float,
    height: float,
    tail_width: float,
    head_width: float,
    head_angle: float = 10,
    head: Literal["->", "<-", "<->"] = "->",
    angle_start: float = 0,
    angle_end: float = 180,
    *,
    style: Style,
) -> None: ...
```
- `width`, `height`: Midline diameter of the underlying ellipse ($> 0$).
- `tail_width`, `head_width`: Radial thickness of the shaft and arrowhead fin.
- `head_angle`: Angular sweep in degrees occupied by the arrowhead tip (default `10`).
- `angle_start`, `angle_end`: CCW start and end angles in degrees (`[0, 360]`).

### 3.2. `arrow_l`
Draws a 90° L-shaped bent block arrow centered at `xy` within `(width, height)`.

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
    style: Style,
) -> None: ...
```

### 3.3. `arrow_u`
Draws a 180° U-turn block arrow centered at `xy` within `(width, height)`.

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
    style: Style,
) -> None: ...
```

---

## 4. Process Step Banner (`chevron`)

Draws a notched or flat-tailed process step chevron anchored at `xy` (bottom-left `(x0, y0)` by default, or center when `style.patch(halign="center", valign="center")` is used). *(For multi-step interlocking process rows with automatic layout, also consider `drawlib.smartarts.ChevronProcess`.)*

```python
def chevron(
    xy: tuple[float, float],
    width: float,
    height: float,
    corner_angle: float,
    mirror: bool = False,
    *,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None: ...
```
- **Parameters**:
  - `xy`: Bottom-left coordinate `(x0, y0)` by default (inherits `shape()` alignment).
  - `width`, `height`: Total bounding width and height ($> 0$).
  - `corner_angle`: Arrowhead point angle in degrees (`0 < corner_angle <= 90`, e.g. `45`–`60`).
  - `mirror`: If `False` (default), points rightward; if `True`, mirrors horizontally to point leftward.
  - `style`: Required keyword-only `Style` (`shape_r` rounds corners; `angle` rotates the chevron).
  - `text`, `text_style`: Optional centered label and text style.

```drawlib code=fold align=center file=shapes_arrow_showcase.png caption="Block Arrow Primitives: arrow, arrow_arc (with separate text), arrow_u, and chevron"
from drawlib.canvas import save, setup
from drawlib.shapes import arrow, arrow_arc, arrow_u, chevron
from drawlib.styles import Styles
from drawlib.text import text

setup(width=144, height=50)

# 1. Straight block arrow with inline label
arrow(
    (8, 25),
    (40, 25),
    tail_width=8,
    head_width=15,
    head_length=8,
    style=Styles.PrimaryFlat,
    text="Ingest",
    text_style=Styles.WhiteBold.patch(text_size=10.5),
)

# 2. Curved cycle via arrow_arc (labels placed via drawlib.text.text)
arrow_arc(
    (64, 25),
    width=24,
    height=24,
    tail_width=3.5,
    head_width=7.0,
    head_angle=25,
    angle_start=20,
    angle_end=160,
    style=Styles.PrimaryFlat,
)
arrow_arc(
    (64, 25),
    width=24,
    height=24,
    tail_width=3.5,
    head_width=7.0,
    head_angle=25,
    angle_start=200,
    angle_end=340,
    style=Styles.SecondaryNeutral,
)
text((64, 25), "Loop", style=Styles.DarkBold.patch(text_size=10.0))

# 3. 180-degree U-turn arrow
arrow_u(
    (96, 25),
    width=18,
    height=22,
    tail_width=4.0,
    head_width=8.0,
    head_length=5.5,
    style=Styles.PrimaryNeutral,
)

# 4. Process step chevrons (bottom-left xy, corner_angle <= 90)
chevron(
    (111, 28),
    width=26,
    height=13,
    corner_angle=60,
    mirror=False,
    style=Styles.PrimaryFlat,
    text="1. Build",
    text_style=Styles.WhiteBold.patch(text_size=10.0),
)
chevron(
    (111, 10),
    width=26,
    height=13,
    corner_angle=60,
    mirror=False,
    style=Styles.Neutral,
    text="2. Ship",
    text_style=Styles.DarkBold.patch(text_size=10.0),
)

save()
```
