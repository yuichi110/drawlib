# Drawlib Symbol Shapes Guidelines (`lib-shapes-symbol`)

API specification and geometric rules for expressive faces, analog/digital clocks, celestial/weather symbols, hearts, lightning bolts, mechanical gears, and arithmetic operators in `drawlib._core.l4_canvas._shapes._symbol` (`face`, `clock`, `sun`, `moon`, `heart`, `lightning`, `gear`, `math_symbol`). See `lib-shapes-overview` for universal coordinate and styling rules.

---

## 1. Summary of Symbol & Operator Shapes

All 8 shapes in `_symbol.py` are **Center-Anchored at `xy = (cx, cy)`** and require `*, style: Style` as a mandatory keyword-only argument:

| Function | Positional Args | Keyword-Only Geometry Args | Primary Architectural Use Cases |
| :--- | :--- | :--- | :--- |
| **`face`** | `xy, radius` | `variant="smile"` (`9` expressions/silhouettes) | User personas, UX sentiment, incident states (`"dizzy"`, `"dead"`), threat actors (`"skull"`, `"devil"`) |
| **`clock`** | `xy, radius` | `variant="standard", hour=10.0, minute=10.0` | Cron jobs, SLA timeouts, latency budgets, scheduled tasks |
| **`sun`** | `xy, radius` | `variant="rays", num_rays=8` | Daytime mode, active/warm state, solar/clean energy |
| **`moon`** | `xy, width, height` | `variant="crescent", mirror=False` | Dark mode, overnight batch window, sleep/standby state |
| **`heart`** | `xy, width, height` | `variant="standard"` | Health check / heartbeat probes, customer loyalty, favorites |
| **`lightning`** | `xy, width, height` | `variant="standard", mirror=False` | Fast-path cache hits, serverless cold/warm triggers, webhooks |
| **`gear`** | `xy, num_teeth, radius_ext, radius_int` | `tooth_ext_ratio=None, tooth_int_ratio=None, hole_radius=None` | Background worker daemons, config engines, automation jobs |
| **`math_symbol`** | `xy, symbol, width, height=None` | `thickness_ratio=None` | Visual equation diagrams (`A + B = C`), metric formulas, scale badges |

---

## 2. Expressive Faces & Clocks (`face`, `clock`)

### 2.1. `face`
Draws an expressive face or character silhouette (`variant`) centered at `xy` with outer `radius`. Eyes and mouth strokes automatically derive high-contrast colors from `style` (white on `*Flat` styles, dark/themed stroke on `*Neutral` styles).

```python
def face(
    xy: tuple[float, float],
    radius: float,
    *,
    variant: Literal[
        "smile",
        "neutral",
        "sad",
        "angry",
        "surprised",
        "dizzy",
        "dead",
        "skull",
        "devil",
    ] = "smile",
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None: ...
```
- **9 `variant` options**:
  - Standard expressions: `"smile"`, `"neutral"`, `"sad"`, `"angry"`, `"surprised"`
  - Incident / outage states: `"dizzy"` (X-eyes + wavy mouth), `"dead"` (X-eyes + flat mouth + protruding tongue)
  - Security / threat silhouettes: `"skull"` (cranium + jawbone + hollow eye/nose sockets + teeth), `"devil"` (curved horns + angry brows + fanged grin)

### 2.2. `clock`
Draws an analog or 7-segment digital clock centered at `xy` with dial `radius`.

```python
def clock(
    xy: tuple[float, float],
    radius: float,
    *,
    variant: Literal["standard", "ticks", "dial", "stopwatch", "timer", "alarm", "digital"] = "standard",
    hour: float = 10.0,
    minute: float = 10.0,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None: ...
```
- `variant`: `"standard"`, `"ticks"`, `"dial"`, `"stopwatch"`, `"timer"`, `"alarm"`, or `"digital"`.
- `hour`, `minute`: Clock time values (default `10.0`, `10.0`).

```drawlib code=fold align=center file=shapes_symbol_face_clock.png caption="face Variants (smile, dizzy, skull, devil) and clock"
from drawlib.canvas import save, setup
from drawlib.shapes import clock, face
from drawlib.styles import Styles

setup(width=144, height=48)

face(
    (18, 26),
    radius=10,
    variant="smile",
    style=Styles.SuccessNeutral,
    text="Healthy",
    text_style=Styles.DarkBold.patch(text_size=10.0, xy_abs_shift=(0, -15)),
)
face(
    (46, 26),
    radius=10,
    variant="dizzy",
    style=Styles.WarningNeutral,
    text="Degraded",
    text_style=Styles.DarkBold.patch(text_size=10.0, xy_abs_shift=(0, -15)),
)
face(
    (74, 26),
    radius=10,
    variant="skull",
    style=Styles.Neutral,
    text="Killed",
    text_style=Styles.DarkBold.patch(text_size=10.0, xy_abs_shift=(0, -15)),
)
face(
    (102, 26),
    radius=10,
    variant="devil",
    style=Styles.DangerFlat,
    text="Attacker",
    text_style=Styles.DarkBold.patch(text_size=10.0, xy_abs_shift=(0, -15)),
)
clock(
    (130, 26),
    radius=10,
    variant="alarm",
    hour=3,
    minute=0,
    style=Styles.PrimaryNeutral,
    text="03:00 Cron",
    text_style=Styles.DarkBold.patch(text_size=10.0, xy_abs_shift=(0, -15)),
)

save()
```

---

## 3. Celestial, Heart, Lightning, Gear & Math Symbols (`sun`, `moon`, `heart`, `lightning`, `gear`, `math_symbol`)

### 3.1. `sun` & `moon`
```python
def sun(
    xy: tuple[float, float],
    radius: float,
    *,
    variant: Literal["rays", "standard", "ring", "beams"] = "rays",
    num_rays: int = 8,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None: ...

def moon(
    xy: tuple[float, float],
    width: float,
    height: float,
    *,
    variant: Literal["crescent", "standard", "thin", "waxing", "half"] = "crescent",
    mirror: bool = False,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None: ...
```
- `sun`: `radius` is the outer radius to the ray tips (`num_rays >= 3`).
- `moon`: Takes `width` and `height` bounding dimensions, `variant` (`"crescent"`, `"standard"`, `"thin"`, `"waxing"`, `"half"`), and `mirror`.

### 3.2. `heart` & `lightning`
```python
def heart(
    xy: tuple[float, float],
    width: float,
    height: float,
    *,
    variant: Literal["standard", "classic", "broken"] = "standard",
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None: ...

def lightning(
    xy: tuple[float, float],
    width: float,
    height: float,
    *,
    variant: Literal["standard", "flat", "double", "flat_double", "angled", "slanted"] = "standard",
    mirror: bool = False,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None: ...
```

### 3.3. `gear` & `math_symbol`
```python
def gear(
    xy: tuple[float, float],
    num_teeth: int,
    radius_ext: float,
    radius_int: float,
    *,
    tooth_ext_ratio: float | None = None,
    tooth_int_ratio: float | None = None,
    hole_radius: float | None = None,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None: ...

def math_symbol(
    xy: tuple[float, float],
    symbol: Literal["+", "-", "*", "x", "×", "/", "÷", "=", "!=", "≠"],
    width: float,
    height: float | None = None,
    *,
    thickness_ratio: float | None = None,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None: ...
```
- `gear`: Positional arguments are `(xy, num_teeth, radius_ext, radius_int)` where `radius_ext > radius_int > 0` and optional `hole_radius < radius_int`.
- `math_symbol`: Positional arguments are `(xy, symbol, width, height=None)` where `symbol` is `"+"`, `"-"`, `"*"`, `"x"`, `"×"`, `"/"`, `"÷"`, `"="`, `"!="`, or `"≠"`.

```drawlib code=fold align=center file=shapes_symbol_gear_math_lightning.png caption="sun, moon, heart, lightning, gear, and math_symbol Primitives"
from drawlib.canvas import save, setup
from drawlib.shapes import gear, heart, lightning, math_symbol, moon, sun
from drawlib.styles import Styles

setup(width=144, height=48)

sun((16, 24), radius=10, style=Styles.WarningFlat)
moon((40, 24), width=18, height=20, variant="crescent", style=Styles.SecondaryNeutral)
heart((64, 24), width=18, height=17, style=Styles.DangerFlat)
lightning((88, 24), width=15, height=22, variant="standard", style=Styles.WarningFlat)
gear((112, 24), num_teeth=8, radius_ext=11, radius_int=8.5, hole_radius=4.0, style=Styles.Neutral)
math_symbol((134, 24), "!=", width=14, height=14, style=Styles.PrimaryFlat)

save()
```
