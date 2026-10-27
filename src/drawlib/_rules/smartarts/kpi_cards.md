# Drawlib KpiCards SmartArt Guidelines (`lib-smartarts-kpi-cards`)

`KpiCards` (also exported as the singular alias `KpiCard`) renders KPI metrics, SLA targets, benchmark numbers, or specification highlights paired with titles (`text`), descriptions (`description`), optional vector icons (`icon`), and accent pills/bars in either a vertical stack (`columns=1`) or a multi-column grid (`columns=2..N`).

---

## 1. Layout Modes & Coordinate Geometry

- **Anchor (`align`)**: `KpiCards.draw(xy, width=90.0, height=60.0, *, columns=1, align="bottom_left", scale=1.0)` anchors the `"bottom_left"` corner (default) or `"center"` of the overall bounding box at `xy`.
- **Row-Major Grid Ordering**: When `columns > 1`, cards are arranged from **top row to bottom row, left to right**, so `items[0]` appears at the top-left of the bounding box.
- **Accent Positions (`accent_position`)**:
  - `"left_pill"` *(default)*: Draws a vertical rounded accent pill inside the left edge of each card (`accent_style` required).
  - `"top_bar"`: Draws a horizontal rounded accent bar along the top edge of each card (`accent_style` required).
  - `"none"`: Omits the accent indicator for a clean border-only card.
- **Metric Layouts (`metric_layout`)**:
  - `"left_column"` *(default)*: Splits each card horizontally into a left metric zone (`metric_width_ratio`, must be between `0.1` and `0.7`, default `0.28`) with a subtle vertical divider and a right title/description zone. Best for `columns=1` or wide `columns=2` layouts.
  - `"top_stack"`: Stacks the large metric (and optional icon) centered in the upper half of the card with the title (`text`) and `description` centered below. Best for compact multi-column grids (`columns=2` or `3`).

---

## 2. Constructor, `KpiCardItem` & Methods

```python
from drawlib.smartarts import KpiCard, KpiCardItem, KpiCards

kpi = KpiCards(
    *,
    style: Style,
    metric_style: Style,
    text_style: Style,
    description_style: Style | None = None,
    accent_style: Style | None = None,
    icon_style: Style | None = None,
    accent_position: Literal["left_pill", "top_bar", "none"] = "left_pill",
    metric_layout: Literal["left_column", "top_stack"] = "left_column",
    metric_width_ratio: float = 0.28,
    spacing: float = 3.0,
)
```

*(Note: `KpiCard` is an exact alias for `KpiCards`.)*

### Item Model (`KpiCardItem`) & `.items` Property

- `kpi.items -> list[KpiCardItem]`: Returns the list of registered `KpiCardItem` instances.
- `KpiCardItem` attributes (mutable before or between `draw()` calls):
  - `metric: str`: Primary highlighted metric value or short callout label (e.g. `"99.99%"`, `"< 12ms"`).
  - `text: str`: Primary card title text.
  - `description: str = ""`: Supporting description text.
  - `style: Style`: Card background rectangle style.
  - `metric_style: Style`: Text style for `metric`.
  - `text_style: Style`: Text style for `text`.
  - `description_style: Style | None = None`: Text style for `description` (required when `description` is non-empty).
  - `accent_style: Style | None = None`: Style for the accent pill or top bar (required when `accent_position != "none"`).
  - `icon: Callable[..., Any] | None = None`: Optional icon drawing callable (e.g. `phosphor.shield_check`).
  - `icon_style: Style | None = None`: Style passed to `icon` (required when `icon` is provided).
  - `show: bool = True`: Visibility flag. Setting `item.show = False` skips rendering that card while preserving the exact grid/stack geometry of all sibling cards.

### Per-Item Overrides (`add`) & Rendering (`draw`)

```python
item = kpi.add(
    metric: str,
    text: str,
    description: str = "",
    *,
    style: Style | None = None,
    metric_style: Style | None = None,
    text_style: Style | None = None,
    description_style: Style | None = None,
    accent_style: Style | None = None,
    icon: Callable[..., Any] | None = None,
    icon_style: Style | None = None,
    show: bool = True,
) -> KpiCardItem

kpi.draw(
    xy: tuple[float, float],
    width: float = 90.0,
    height: float = 60.0,
    *,
    columns: int = 1,
    align: Literal["bottom_left", "center"] = "bottom_left",
    scale: float = 1.0,
) -> Self
```

---

## 3. Production Example: Side-by-Side Stack and 2x2 Grid

```drawlib code=show
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.smartarts import KpiCards
from drawlib.styles import Styles

setup(width=180, height=70)

# 1. Left: Vertical Stack (left_column layout, columns=1)
kpi_stack = KpiCards(
    style=Styles.Neutral,
    metric_style=Styles.PrimaryBold.patch(text_size=18.0),
    text_style=Styles.DarkBold.patch(text_size=12.0),
    description_style=Styles.Muted.patch(text_size=10.5),
    accent_style=Styles.PrimaryFlat,
    icon_style=Styles.PrimaryBold,
    accent_position="left_pill",
    metric_layout="left_column",
    metric_width_ratio=0.28,
    spacing=3.0,
)
kpi_stack.add("99.99%", "High Availability SLA", "Multi-region active-active failover")
kpi_stack.add(
    "< 12ms",
    "Edge P99 Latency",
    "Global CDN & Anycast routing",
    icon=phosphor.lightning,
    metric_style=Styles.AccentBold.patch(text_size=18.0),
    accent_style=Styles.AccentFlat,
    icon_style=Styles.AccentBold,
)
kpi_stack.add("Zero-Dep", "Pure Python Core", "No external GUI tools required")
kpi_stack.draw(xy=(6.0, 7.0), width=82.0, height=56.0, columns=1, align="bottom_left", scale=1.0)

# 2. Right: 2x2 Grid (top_stack layout, columns=2)
kpi_grid = KpiCards(
    style=Styles.Neutral,
    metric_style=Styles.PrimaryBold.patch(text_size=18.0),
    text_style=Styles.DarkBold.patch(text_size=11.5),
    description_style=Styles.Muted.patch(text_size=10.0),
    accent_style=Styles.PrimaryFlat,
    accent_position="top_bar",
    metric_layout="top_stack",
    spacing=3.5,
)
kpi_grid.add("300M+", "Peak RPS", "Botnet flood volume")
kpi_grid.add(
    "$6,750",
    "Hourly Cost",
    "L7 EDoS billing spike",
    metric_style=Styles.AccentBold.patch(text_size=18.0),
    accent_style=Styles.AccentFlat,
)
kpi_grid.add("4.2 sec", "Auto Mitigation", "BGP Flowspec trigger")
kpi_grid.add("100%", "Traffic Scrubbed", "Zero customer downtime")
kpi_grid.draw(xy=(94.0, 7.0), width=80.0, height=56.0, columns=2, align="bottom_left", scale=1.0)

save()
```
