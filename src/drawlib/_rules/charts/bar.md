# Drawlib BarChart Guidelines (`lib-charts-bar`)

`BarChart` (`drawlib.charts.bar`) compares discrete categories across one or more data series. It supports vertical columns and horizontal bars, side-by-side grouped clusters (`bar_mode="group"`), cumulative stacked bars (`bar_mode="stack"`), outer-tip corner rounding (`bar_r`), orientation-aware axis properties, and decoupled legend rendering.

---

## 1. Conceptual Overview & Imports

```python
from drawlib.charts.bar import (
    Axis,
    BarChart,
    DrawDirection,
    FormatterType,
    LegendPosition,
    Mode,
    Orientation,
    Series,
)
```

```text
       Vertical Grouped                      Horizontal Stacked
  Y ▲                                   Y ▲
    │  ┌──┐ ┌──┐                          │ ┌────────┬─────┬──┐ Cat 2
    │  │  │ │  │   ┌──┐ ┌──┐              │ └────────┴─────┴──┘
    │  │  │ │  │   │  │ │  │              │ ┌──────┬───────┐    Cat 1
    │  │  │ │  │   │  │ │  │              │ └──────┴───────┘
    └──┴──┴─┴──┴───┴──┴─┴──┴──► X         └──────────────────────► X
        Cat 1        Cat 2                    0%     50%    100%
```

- **`orientation` (`Orientation = Literal["vertical", "horizontal"]`)**:
  - `"vertical"` *(default)*: Columns grow upward from the bottom X-axis (`y_axis` is the numerical `value_axis`; `x_axis` is the `category_axis`).
  - `"horizontal"`: Bars grow rightward from the left Y-axis (`x_axis` is the numerical `value_axis`; `y_axis` is the `category_axis`).
- **`bar_mode` (`Mode = Literal["group", "stack"]`)**:
  - `"group"` *(default)*: Side-by-side clustered bars within each category slot.
  - `"stack"`: Cumulative stacked bars showing total volume and part-to-whole composition.
- **`bar_r`**: Corner rounding radius applied strictly to the **2 outer tip corners** of each bar (for stacked bars, only the outermost segment receives tip rounding while inner segment boundaries remain flush).

---

## 2. Constructor Parameters (`BarChart`)

All constructor arguments are **keyword-only** (`*`):

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| **`axis_line_style`** | `Style` | **Required** | Style for the Cartesian axes baseline and ticks. Mandatory anchor. |
| `width` / `height` | `float` | `60.0` / `40.0` | Total bounding box dimensions on the canvas. |
| `categories` | `list[str] \| None` | `None` | Category labels along the categorical axis (e.g. `["Q1", "Q2", "Q3"]`). |
| `orientation` | `"vertical"` \| `"horizontal"` | `"vertical"` | Direction of bar growth (`Orientation`). |
| `bar_mode` | `"group"` \| `"stack"` | `"group"` | Grouped side-by-side or stacked cumulatively (`Mode`). |
| `bar_width_ratio` | `float` | `0.7` | Relative thickness ratio of bars within each category slot (`0.1` to `1.0`). |
| `bar_r` | `float` | `0.0` | Corner rounding radius applied only to the 2 outer tip corners of bars. |
| `axis_text_style` | `Style \| None` | `None` | Style for axis tick marks and category labels. If `None`, labels are omitted. |
| `grid_style` | `Style \| None` | `None` | Style for value axis gridlines. If `None`, gridlines are omitted. |
| `value_text_style` | `Style \| None` | `None` | Style for numerical value labels drawn on bars. If `None`, value labels are omitted. |
| `value_format` | `FormatterType` | `None` | Format string (e.g. `"{:.1f}M"`) or `Callable[[float], str]` for bar value labels. |
| `background_style` | `Style \| None` | `None` | Outer chart background card style (fill, border, `shape_r`). If `None`, card is omitted. |
| `title` | `str` | `""` | Chart title text displayed at the top of the container. |
| `title_style` | `Style \| None` | `None` | Typography style for `title`. Required for the title to render. |

---

## 3. Methods, Properties & Data Models

### 3.1 Methods
- **`add_series(name: str, values: list[float], style: Style, legend_text_style: Style | None = None, *, show: bool = True, draw_ratio: float = 1.0, draw_direction: DrawDirection | None = None) -> Series`**:
  Registers a data series and returns the mutable `Series` instance.
  - When `draw_direction` is `None` *(default)*, `BarChart` automatically selects `"bottom_to_top"` for `orientation="vertical"` (bars grow upward from baseline) and `"left_to_right"` for `orientation="horizontal"` (bars grow rightward from baseline).
  - Passing the orthogonal direction (`"left_to_right"` on a vertical chart, or `"bottom_to_top"` on a horizontal chart) reveals bars sequentially category-by-category.
- **`configure_y_axis(scale=None, min_value=None, max_value=None, ticks=None, tick_step=None, format=None, unit=None, label=None, show_grid=None, grid_style=None, show_axis_line=None, line_style=None, show_ticks=None, tick_label_style=None) -> Axis`**:
  Configures the vertical axis (`value_axis` when vertical, `category_axis` when horizontal).
- **`configure_x_axis(...) -> Axis`**:
  Configures the horizontal axis (`category_axis` when vertical, `value_axis` when horizontal).
- **`get_size() -> tuple[float, float]`**:
  Returns `(width, height)` of the chart container.
- **`draw(xy: tuple[float, float] = (0.0, 0.0), *, width: float | None = None, height: float | None = None, align: Literal["bottom_left", "center"] = "bottom_left", scale: float = 1.0) -> None`**:
  Renders the bar chart onto the canvas anchored at `xy` (`"bottom_left"` or `"center"`), with optional one-call dimension overrides and proportional `scale`.
- **`draw_legend(xy: tuple[float, float], text_style: Style, orientation: Orientation = "vertical", swatch_width: float = 2.4, swatch_height: float = 1.2, item_gap: float = 4.0, *, scale: float = 1.0) -> None`**:
  Renders the standalone series legend at `xy`.

### 3.2 Properties & `Series` Model
- **`chart.series -> list[Series]`**: Copy of registered `Series` objects.
- **`chart.value_axis -> Axis`**: Orientation-aware property returning `y_axis` when vertical and `x_axis` when horizontal.
- **`chart.category_axis -> Axis`**: Orientation-aware property returning `x_axis` when vertical and `y_axis` when horizontal.
- **`chart.x_axis -> Axis`** / **`chart.y_axis -> Axis`**: Direct access to horizontal and vertical `Axis` instances.
- **`Series(name: str, values: list[float], style: Style, legend_text_style: Style | None = None, *, show: bool = True, draw_ratio: float = 1.0, draw_direction: DrawDirection = "bottom_to_top")`**:
  Stores `name`, `values`, `style`, `legend_text_style`, `show`, `draw_ratio`, and `draw_direction`.

---

## 4. Production Examples

### Example 4.1: Vertical Grouped Bar Chart with Value Labels
```drawlib code=show align=center file=rules_bar_vertical_grouped.png caption="Vertical Grouped BarChart with Value Labels"
from drawlib.canvas import save, setup
from drawlib.charts.bar import BarChart
from drawlib.styles import Styles

setup(width=100, height=76)

chart = BarChart(
    axis_line_style=Styles.MutedDashed,
    categories=["Q1", "Q2", "Q3", "Q4"],
    width=82.0,
    height=52.0,
    title="Quarterly Enterprise Revenue",
    title_style=Styles.BlackBold.patch(text_size=13.0),
    orientation="vertical",
    bar_mode="group",
    bar_width_ratio=0.72,
    bar_r=1.0,
    axis_text_style=Styles.Muted.patch(text_size=10.0),
    grid_style=Styles.MutedThin,
    value_text_style=Styles.DarkBold.patch(text_size=9.5),
    value_format="{:.1f}M",
)
chart.add_series("SaaS Subscriptions", [45.2, 58.0, 72.5, 91.0], style=Styles.PrimaryFlat)
chart.add_series("Professional Services", [22.0, 24.5, 21.0, 19.5], style=Styles.SecondaryNeutral)
chart.configure_y_axis(unit="$", label="Revenue (USD Millions)")
chart.draw(xy=(9.0, 10.0))
chart.draw_legend(xy=(22.0, 66.0), text_style=Styles.Muted.patch(text_size=10.0), orientation="horizontal")
save()
```

### Example 4.2: Horizontal Stacked Bar Chart with Resource Breakdown
```drawlib code=show align=center file=rules_bar_horizontal_stacked.png caption="Horizontal Stacked BarChart with Custom X-Axis Ticks"
from drawlib.canvas import save, setup
from drawlib.charts.bar import BarChart
from drawlib.styles import Styles

setup(width=110, height=70)

chart = BarChart(
    axis_line_style=Styles.MutedDashed,
    categories=["Frontend", "API Gateway", "Database", "Search Index"],
    width=84.0,
    height=48.0,
    orientation="horizontal",
    bar_mode="stack",
    bar_width_ratio=0.6,
    bar_r=0.8,
    title="Cluster Node Resource Allocation (%)",
    title_style=Styles.BlackBold.patch(text_size=13.0),
    axis_text_style=Styles.Muted.patch(text_size=10.0),
    grid_style=Styles.MutedThin,
    value_text_style=Styles.DarkBold.patch(text_size=9.5),
    value_format="{:.0f}%",
)
chart.add_series("Compute (CPU)", [38.0, 48.0, 52.0, 40.0], style=Styles.PrimaryFlat)
chart.add_series("Memory Cache", [28.0, 24.0, 26.0, 30.0], style=Styles.PrimaryNeutral)
chart.add_series("Storage I/O", [16.0, 14.0, 14.0, 18.0], style=Styles.SecondaryNeutral)
chart.configure_x_axis(min_value=0.0, max_value=100.0, tick_step=20.0, unit="%")
chart.draw(xy=(12.0, 8.0))
chart.draw_legend(xy=(18.0, 61.0), text_style=Styles.Muted.patch(text_size=10.0), orientation="horizontal")
save()
```

### Example 4.3: Logarithmic Scale Latency Benchmark
```drawlib code=show align=center file=rules_bar_log_scale.png caption="Logarithmic Y-Axis Scale (scale='log') BarChart"
from drawlib.canvas import save, setup
from drawlib.charts.bar import BarChart
from drawlib.styles import Styles

setup(width=105, height=68)

chart = BarChart(
    axis_line_style=Styles.MutedDashed,
    categories=["L1 Cache", "Main RAM", "NVMe SSD", "Regional RPC"],
    width=82.0,
    height=46.0,
    title="Storage & Network Read Latency (Log10 Scale)",
    title_style=Styles.BlackBold.patch(text_size=12.5),
    bar_width_ratio=0.55,
    bar_r=0.8,
    axis_text_style=Styles.Muted.patch(text_size=10.0),
    grid_style=Styles.MutedThin,
    value_text_style=Styles.DarkBold.patch(text_size=9.5),
    value_format="{:g} ns",
)
chart.add_series("Median Access Time", [1.0, 100.0, 150000.0, 45000000.0], style=Styles.PrimaryFlat)
chart.configure_y_axis(scale="log", unit="ns", label="Nanoseconds (log10)")
chart.draw(xy=(12.0, 10.0))
save()
```

---

## 5. Related Rules
- Charts Overview & Axis/Legend Architecture: `uv run drawlib rules show lib-charts-overview`
- Line Charts: `uv run drawlib rules show lib-charts-line`
- Area Charts: `uv run drawlib rules show lib-charts-area`
