# Drawlib Badge & Callout Shapes Guidelines (`lib-shapes-badge`)

API specification and geometric rules for callouts, location pins, metadata tags, ribbons, security shields, status indicators, and burst badges in `drawlib._core.l4_canvas._shapes._badge` (`bubblespeech`, `pin`, `tag`, `ribbon`, `shield`, `forbidden`, `checkmark`, `explosion`). See `lib-shapes-overview` for universal coordinate and styling rules.

---

## 1. Summary of Badge & Callout Shapes

All shapes in `_badge.py` require `*, style: Style` as a mandatory keyword-only argument. `pin`, `tag`, `ribbon`, `shield`, `forbidden`, `checkmark`, and `explosion` are **Center-Anchored at `xy = (cx, cy)`**, whereas `bubblespeech` is **Bottom-Left Anchored at `xy = (x0, y0)`** of the bubble body:

| Function | Positional Args | Keyword-Only Geometry Args | Primary Architectural Use Cases |
| :--- | :--- | :--- | :--- |
| **`bubblespeech`** | `xy, width, height, tail_edge, tail_start_ratio, tail_vertex_xy, tail_end_ratio` | — | Architectural annotations, review notes, actor dialogue callouts |
| **`pin`** | `xy, width, height` | `variant="pointer", hole_ratio=None` | Multi-region cloud deployment markers, edge PoPs, map locations |
| **`tag`** | `xy, width, height` | `variant="angled", mirror=False, hole_ratio=None` | Semantic version labels (`v2.4.0`), cost/env tags, K8s labels |
| **`ribbon`** | `xy, width, height` | `variant="down", tail_width_ratio=None, drop_ratio=None` | Section title banners, milestone headers, certification seals |
| **`shield`** | `xy, width, height` | `variant="classic"` | WAF/firewall boundaries, Zero-Trust IAM gates, TLS/KMS nodes |
| **`forbidden`** | `xy, radius` | `variant="slash", thickness_ratio=None` | Blocked traffic, deprecated APIs, firewall deny rules |
| **`checkmark`** | `xy, width, height=None` | `variant="standard", thickness_ratio=None` | Passing CI/CD checks, verified compliance, SLO healthy states |
| **`explosion`** | `xy, width, height` | `variant="standard"` | Outages, fault injection, DDoS impact bursts, critical alerts |

---

## 2. Callouts, Pins, Tags & Ribbons (`bubblespeech`, `pin`, `tag`, `ribbon`)

### 2.1. `bubblespeech`
Draws a rectangular speech/annotation callout with bottom-left corner `xy = (x0, y0)` and a triangular tail protruding from `tail_edge` to absolute canvas point `tail_vertex_xy`.

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
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None: ...
```
- **Parameters**:
  - `xy`: Bottom-left `(x0, y0)` of the rectangular callout body (excluding the tail).
  - `tail_edge`: Edge from which the tail sprouts (`"left"`, `"right"`, `"top"`, `"bottom"`).
  - `tail_start_ratio`, `tail_end_ratio`: Fractional attachment positions along `tail_edge` in `(0.0, 1.0)` (`0.0` = left/bottom corner, `1.0` = right/top corner; must satisfy `tail_start_ratio < tail_end_ratio`).
  - `tail_vertex_xy`: Absolute `(x, y)` canvas coordinate of the pointer tip (must lie outside the body box on the `tail_edge` side).

### 2.2. `pin`
Draws a callout pointer badge or map pin shape centered at `xy` within `(width, height)`.

```python
def pin(
    xy: tuple[float, float],
    width: float,
    height: float,
    *,
    variant: Literal["pointer", "standard", "teardrop", "drop", "pin", "badge"] = "pointer",
    hole_ratio: float | None = None,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None: ...
```
- `variant`: Pin silhouette (`"pointer"`, `"standard"`, `"teardrop"`, `"drop"`, `"pin"`, `"badge"`).
- `hole_ratio`: Optional center circular hole ratio in `(0.0, 1.0)`.

### 2.3. `tag`
Draws a perforated label tag or badge shape centered at `xy` within `(width, height)`.

```python
def tag(
    xy: tuple[float, float],
    width: float,
    height: float,
    *,
    variant: Literal["angled", "standard", "chamfered", "beveled", "rounded"] = "angled",
    mirror: bool = False,
    hole_ratio: float | None = None,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None: ...
```
- `variant`: Tag silhouette (`"angled"`, `"standard"`, `"chamfered"`, `"beveled"`, `"rounded"`).
- `mirror`: Whether to flip the tag tip direction horizontally.
- `hole_ratio`: Optional circular hole size ratio in `(0.0, 1.0)`.

### 2.4. `ribbon`
Draws a horizontal ribbon banner shape centered at `xy` within `(width, height)`.

```python
def ribbon(
    xy: tuple[float, float],
    width: float,
    height: float,
    *,
    variant: Literal["down", "standard", "up", "flat", "banner"] = "down",
    tail_width_ratio: float | None = None,
    drop_ratio: float | None = None,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None: ...
```
- `variant`: `"down"` / `"standard"` (side tails stepped down), `"up"` (side tails stepped up), or `"flat"` / `"banner"` (flat ribbon with V-notched ends).

```drawlib code=fold align=center file=shapes_badge_callouts_tags.png caption="bubblespeech, pin, tag, and ribbon Primitives"
from drawlib.canvas import save, setup
from drawlib.shapes import bubblespeech, pin, ribbon, tag
from drawlib.styles import Styles

setup(width=144, height=48)

bubblespeech(
    (8, 20),
    width=32,
    height=16,
    tail_edge="bottom",
    tail_start_ratio=0.35,
    tail_vertex_xy=(18, 9),
    tail_end_ratio=0.60,
    style=Styles.PrimaryNeutral,
    text="Note Callout",
    text_style=Styles.DarkBold.patch(text_size=10.0),
)

pin(
    (58, 26),
    width=15,
    height=21,
    style=Styles.PrimaryFlat,
    text="ap-northeast-1",
    text_style=Styles.DarkBold.patch(text_size=10.0, xy_abs_shift=(0, -15)),
)

tag(
    (92, 24),
    width=28,
    height=15,
    variant="angled",
    style=Styles.SecondaryNeutral.patch(shape_r=1.2),
    text="v2.4.0",
    text_style=Styles.DarkBold.patch(text_size=10.0, xy_abs_shift=(-2, 0)),
)

ribbon(
    (126, 24),
    width=30,
    height=15,
    variant="banner",
    style=Styles.PrimaryFlat,
    text="Milestone",
    text_style=Styles.WhiteBold.patch(text_size=10.0),
)

save()
```

---

## 3. Security Shields, Status Indicators & Impact Bursts (`shield`, `forbidden`, `checkmark`, `explosion`)

### 3.1. `shield`
Draws a heraldic security shield centered at `xy` within `(width, height)`.

```python
def shield(
    xy: tuple[float, float],
    width: float,
    height: float,
    *,
    variant: Literal["classic", "standard", "flat", "heater", "round"] = "classic",
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None: ...
```
- `variant`: `"classic"` / `"standard"`, `"flat"`, `"heater"`, or `"round"`.

### 3.2. `forbidden`
Draws a circular prohibition / no-entry mark centered at `xy` with outer `radius`.

```python
def forbidden(
    xy: tuple[float, float],
    radius: float,
    *,
    variant: Literal["slash", "standard", "backslash", "cross", "no_entry", "minus"] = "slash",
    thickness_ratio: float | None = None,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None: ...
```

### 3.3. `checkmark`
Draws a checkmark symbol or circular badge centered at `xy` within `(width, height)` (`height` defaults to `width` when `None`).

```python
def checkmark(
    xy: tuple[float, float],
    width: float,
    height: float | None = None,
    *,
    variant: Literal["standard", "check", "circle", "solid_circle"] = "standard",
    thickness_ratio: float | None = None,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None: ...
```

### 3.4. `explosion`
Draws an asymmetric explosion or impact burst shape centered at `xy` within `(width, height)`.

```python
def explosion(
    xy: tuple[float, float],
    width: float,
    height: float,
    *,
    variant: Literal["standard", "irregular", "heavy", "wild", "curved", "comic"] = "standard",
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None: ...
```

```drawlib code=fold align=center file=shapes_badge_security_status.png caption="shield, checkmark, forbidden, and explosion Status Primitives"
from drawlib.canvas import save, setup
from drawlib.shapes import checkmark, explosion, forbidden, shield
from drawlib.styles import Styles

setup(width=144, height=48)

shield(
    (22, 24),
    width=22,
    height=26,
    variant="classic",
    style=Styles.PrimaryNeutral,
    text="WAF",
    text_style=Styles.DarkBold.patch(text_size=10.5),
)

checkmark(
    (56, 26),
    width=20,
    variant="solid_circle",
    style=Styles.SuccessFlat,
    text="Passed",
    text_style=Styles.DarkBold.patch(text_size=10.0, xy_abs_shift=(0, -15)),
)

forbidden(
    (88, 26),
    radius=10,
    style=Styles.DangerFlat,
    text="Blocked",
    text_style=Styles.DarkBold.patch(text_size=10.0, xy_abs_shift=(0, -15)),
)

explosion(
    (122, 24),
    width=30,
    height=26,
    variant="standard",
    style=Styles.DangerNeutral,
    text="CRASH!",
    text_style=Styles.DarkBold.patch(text_size=10.0),
)

save()
```
