# Drawlib PieChart Guidelines (`lib-charts-pie`)

`PieChart` (`drawlib.charts.pie`) visualizes proportional compositions where slices represent parts of a whole ($100\%$). It supports classic solid pie charts (`hole_ratio=0.0`), donut rings (`hole_ratio > 0.0`) with center KPI text badges (`center_text`), outward slice explosions (`explode`), clockwise or counter-clockwise ordering, and decoupled legend rendering.

---

## 1. Conceptual Overview & Imports

```python
from drawlib.charts.pie import (
    DrawDirection,
    FormatterType,
    PieChart,
    Slice,
)
```

```text
        Standard Pie                            Donut with Center KPI
           12 o'clock                                 12 o'clock
              ▲                                          ▲
          . - ~ - .                                  . - ~ - .
      . '    |    ' .                            . '    |    ' .
    /        |  45%   \                        /    ┌───────┐    \
   |  35%    |         |                      |     │ $1.2B │     |
   |         |         |                      |     │  ARR  │     |
    \        |        /                        \    └───────┘    /
      . '    |    ' .                            . '    |    ' .
          ' - ~ - '                                  ' - ~ - '
```

- **Solid Pie (`hole_ratio=0.0`) vs. Donut (`hole_ratio=0.5` to `0.7`)**: `hole_ratio` is clamped to `[0.0, 0.9]`. When `hole_ratio > 0.0`, `center_text` (supporting multiline `\n`) and `center_text_style` render a KPI badge inside the donut hole.
- **Exploded Slices (`explode > 0.0`)**: Shifts a wedge radially outward along its bisector angle for visual emphasis.
- **Automatic `< 4%` Inline Label Threshold**: When `value_text_style` is provided, inline percentage labels are automatically hidden for slices representing **less than $4\%$** of the total sum (or when `draw_ratio < 0.6`) to prevent unreadable text overlap on narrow wedges. Always pair charts containing small slices with `chart.draw_legend(...)`.

---

## 2. Constructor Parameters (`PieChart`)

All constructor arguments are **keyword-only** (`*`):

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `radius` | `float` | `20.0` | Outer radius of the pie circle in canvas units. |
| `hole_ratio` | `float` | `0.0` | Inner hole radius ratio (`0.0` for solid pie; `0.1` to `0.9` for donut ring). |
| `start_angle` | `float` | `90.0` | Initial starting radial angle in degrees (`90.0` is 12 o'clock, `0.0` is 3 o'clock). |
| `clockwise` | `bool` | `True` | Whether slices progress clockwise (`True`) or counter-clockwise (`False`). |
| `value_text_style` | `Style \| None` | `None` | Style for percentage/value labels on slices ($\ge 4\%$ share). If `None`, slice labels are omitted. |
| `value_format` | `FormatterType` | `"{:.1f}%"` | Format string or `Callable[[float], str]` receiving the slice's percentage (`0.0`–`100.0`). |
| `center_text` | `str` | `""` | Text rendered inside the donut hole (supports `\n`; requires `hole_ratio > 0`). |
| `center_text_style` | `Style \| None` | `None` | Typography style for `center_text`. Required for center text to render. |
| `background_style` | `Style \| None` | `None` | Outer chart background card style. If `None`, card is omitted. |
| `title` | `str` | `""` | Chart title text displayed at the top of the container. |
| `title_style` | `Style \| None` | `None` | Typography style for `title`. Required for the title to render. |
| `width` / `height` | `float \| None` | `None` | Optional container dimension overrides. If `None`, computed from `radius` and `title`. |

---

## 3. Methods, Properties & Data Models

### 3.1 Methods
- **`add_slice(name: str, value: float, style: Style, explode: float = 0.0, legend_text_style: Style | None = None, *, show: bool = True, draw_ratio: float = 1.0, draw_direction: DrawDirection = "left_to_right") -> Slice`**:
  Adds a proportional wedge and returns the mutable `Slice` instance.
  - `explode`: Outward radial offset distance from center (`0.0` = flush).
  - `show`: Toggles slice visibility while preserving the 100% pie sum across all slices so remaining wedges do not rescale.
  - `draw_direction`: `"left_to_right"` *(default)* sweeps angularly from the slice's start angle across `span * draw_ratio`; `"bottom_to_top"` grows radially outward from the inner hole edge toward `radius`.
- **`get_size() -> tuple[float, float]`**:
  Computes total `(width, height)` bounding box dimensions based on `radius` and `title`.
- **`draw(xy: tuple[float, float] = (0.0, 0.0), *, radius: float | None = None, width: float | None = None, height: float | None = None, align: Literal["bottom_left", "center"] = "bottom_left", scale: float = 1.0) -> None`**:
  Renders the pie chart onto the canvas anchored at `xy` (`"bottom_left"` or `"center"`), with optional temporary `radius`/`width`/`height` overrides and uniform `scale`.
- **`draw_legend(xy: tuple[float, float], text_style: Style, orientation: Literal["vertical", "horizontal"] = "vertical", swatch_width: float = 2.4, swatch_height: float = 1.2, item_gap: float = 4.0, *, scale: float = 1.0) -> None`**:
  Renders the standalone slice legend at `xy`.

### 3.2 Properties & `Slice` Model
- **`chart.slices -> list[Slice]`**: Copy of registered `Slice` objects.
- **`Slice(name: str, value: float, style: Style, explode: float = 0.0, legend_text_style: Style | None = None, show: bool = True, draw_ratio: float = 1.0, draw_direction: DrawDirection = "left_to_right")`**:
  Stores `name`, `value`, `style`, `explode`, `legend_text_style`, `show`, `draw_ratio`, and `draw_direction`.

---

## 4. Production Examples

### Example 4.1: Donut Chart with Center KPI Badge
```drawlib code=show align=center file=rules_pie_donut_kpi.png caption="Revenue Contribution Donut Chart with Center KPI"
from drawlib.canvas import save, setup
from drawlib.charts.pie import PieChart
from drawlib.styles import Styles

setup(width=102, height=78)

chart = PieChart(
    radius=24.0,
    hole_ratio=0.62,
    center_text="$1.2B\nARR",
    center_text_style=Styles.BlackBold.patch(text_size=12.0),
    title="Revenue Contribution by Product Line",
    title_style=Styles.BlackBold.patch(text_size=13.0),
    value_text_style=Styles.BlackBold.patch(text_size=10.5),
)
chart.add_slice("Cloud Infrastructure", 540.0, style=Styles.PrimaryFlat)
chart.add_slice("AI Developer Tools", 340.0, style=Styles.PrimaryNeutral)
chart.add_slice("Security Suite", 220.0, style=Styles.SecondaryNeutral)
chart.add_slice("Legacy Support", 100.0, style=Styles.Neutral)

chart.draw(xy=(8.0, 8.0))
chart.draw_legend(xy=(64.0, 48.0), text_style=Styles.Dark.patch(text_size=10.5), orientation="vertical")
save()
```

### Example 4.2: Exploded Slice Allocation & Callable Formatter
```drawlib code=show align=center file=rules_pie_exploded.png caption="Exploded Slice Allocation with Callable Formatter"
from drawlib.canvas import save, setup
from drawlib.charts.pie import PieChart
from drawlib.styles import Styles

setup(width=102, height=78)

chart = PieChart(
    radius=24.0,
    title="R&D Budget Allocation (2026)",
    title_style=Styles.BlackBold.patch(text_size=13.0),
    value_text_style=Styles.BlackBold.patch(text_size=10.5),
    value_format=lambda pct: f"{pct:.0f}%",
)
chart.add_slice("Generative AI Models", 45.0, style=Styles.PrimaryFlat, explode=2.8)
chart.add_slice("Core Infrastructure", 28.0, style=Styles.PrimaryNeutral)
chart.add_slice("DevOps & Tooling", 16.0, style=Styles.SecondaryNeutral)
chart.add_slice("Compliance & Audit", 8.0, style=Styles.Neutral)
chart.add_slice("Experimental Labs (3%)", 3.0, style=Styles.Muted)

chart.draw(xy=(8.0, 8.0))
chart.draw_legend(xy=(64.0, 50.0), text_style=Styles.Dark.patch(text_size=10.5), orientation="vertical")
save()
```

---

## 5. Related Rules
- Charts Overview & Axis/Legend Architecture: `uv run drawlib rules show lib-charts-overview`
- Radar Charts: `uv run drawlib rules show lib-charts-radar`
- Bar Charts: `uv run drawlib rules show lib-charts-bar`
