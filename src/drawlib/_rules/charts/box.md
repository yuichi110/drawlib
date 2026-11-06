# Drawlib BoxChart & Strip Plot Guidelines (`lib-charts-box`)

`BoxChart` (`drawlib.charts.box`) visualizes categorical numerical distributions, dispersion, quartiles, and tail latency across one or more series. With a single unified class, it renders **Box Plots** (`show_box=True, show_points=False`), **Strip / Jitter Plots** (`show_box=False, show_points=True`), and **Box + Strip Hybrid Overlays** (`show_box=True, show_points=True` — ideal for $N = 5 \sim 30$ PoC and benchmark runs), supporting both raw sample arrays and pre-aggregated `BoxStats` (e.g. `p5 / p50 / p95` from BigQuery or Cloud Monitoring).

---

## 1. Conceptual Overview & Imports

```python
from drawlib.charts.box import (
    Axis,
    BoxChart,
    BoxStats,
    DrawDirection,
    FormatterType,
    LegendPosition,
    Orientation,
    PointShape,
    ScaleType,
    Series,
    WhiskerMode,
)
```

```text
    Box Plot                  Strip / Jitter Plot         Box + Strip Overlay
  Y ▲                         Y ▲                         Y ▲
    │      ○ (outlier)          │      •                    │      •
    │     ─┬─ (max/p95)         │    •   •                  │     ─┬─ •
    │    ┌─┴─┐ Q3               │     • •                   │    ┌─┴•┐
    │    ├───┤ Median           │    • • •                  │    ├─•─┤ •
    │    └─┬─┘ Q1               │     •  •                  │    └•┬─┘
    │     ─┴─ (min/p5)          │      •                    │     ─┴─ •
    └──────────► X              └──────────► X              └──────────► X
```

- **3 Display Modes (`show_box` / `show_points`)**:
  - `show_box=True, show_points=False` *(default)*: Classic box-and-whisker plot with automatic outlier markers (`show_outliers=True`).
  - `show_box=False, show_points=True`: Pure strip / jitter plot (`jitter=0.0` aligns points into a straight 1D strip).
  - `show_box=True, show_points=True`: Overlays real sample points on top of the Q1–Q3 box and whiskers (automatically suppresses duplicate outlier markers).
- **3 Whisker Modes (`whisker_mode: WhiskerMode`)**:
  - `"iqr"` *(default)*: Standard Tukey fences ($[Q_1 - 1.5\cdot\text{IQR},\ Q_3 + 1.5\cdot\text{IQR}]$); points outside are plotted as outliers.
  - `"min_max"`: Full `0%–100%` sample range with no separate outliers.
  - `"percentile"`: Tail-latency percentiles via `whisker_percentiles=(5.0, 95.0)` (e.g. `p5–p95` or `p10–p90`), plotting extreme spikes outside as outliers.
- **Deterministic, Animation-Safe Jitter (`jitter_seed: int = 42`)**:
  - Uses isolated 32-bit prime mixing per `(jitter_seed, series_idx, category_idx)` so point positions never drift in Git diffs and never reshuffle other series when toggling `series.show = False` in animations.

---

## 2. Constructor Parameters (`BoxChart`) & `BoxStats`

All constructor arguments are **keyword-only** (`*`):

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| **`axis_line_style`** | `Style` | **Required** | Style for Cartesian axis baselines. Mandatory anchor. |
| `width` / `height` | `float` | `68.0` / `44.0` | Total bounding box dimensions on the canvas. |
| `categories` | `list[str] \| None` | `None` | Category labels along the categorical axis. |
| `orientation` | `"vertical"` \| `"horizontal"` | `"vertical"` | Vertical or horizontal distribution layout (`Orientation`). |
| `show_box` | `bool` | `True` | Default visibility of Q1–Q3 boxes, whiskers, and median lines. |
| `show_points` | `bool` | `False` | Default visibility of strip/jitter sample markers. |
| `show_outliers` | `bool` | `True` | Default visibility of outlier markers when `show_points=False`. |
| `show_mean` | `bool` | `False` | Default visibility of arithmetic mean markers (`mean_shape="rhombus"`). |
| `whisker_mode` | `WhiskerMode` | `"iqr"` | Raw-sample whisker rule: `"iqr"`, `"min_max"`, or `"percentile"`. |
| `iqr_k` | `float` | `1.5` | IQR multiplier when `whisker_mode="iqr"`. |
| `whisker_percentiles` | `tuple[float, float]` | `(5.0, 95.0)` | `(low_p, high_p)` in `[0, 100]` when `whisker_mode="percentile"`. |
| `box_width_ratio` | `float` | `0.65` | Ratio of category slot occupied by the box cluster (`(0.0, 1.0]`). |
| `cap_width_ratio` | `float` | `0.45` | Ratio of individual box width occupied by whisker T-caps (`[0.0, 1.0]`). |
| `box_r` | `float` | `0.0` | Corner rounding radius for Q1–Q3 boxes. |
| `jitter` | `float` | `0.45` | Normalized transverse spread ratio for strip points (`0.0` to `1.0`). |
| `jitter_seed` | `int` | `42` | Deterministic integer seed for strip point jitter. |
| `point_radius` | `float` | `0.58` | Default marker radius for strip, outlier, and mean points. |
| `point_shape` / `outlier_shape` / `mean_shape` | `PointShape` | `"circle"` / `"circle"` / `"rhombus"` | Marker shapes (`"circle"`, `"square"`, `"rhombus"`, `"triangle"`, `"none"`). |
| `axis_text_style` | `Style \| None` | `None` | Style for tick labels, category names, and default axis titles. |
| `grid_style` | `Style \| None` | `None` | Style for value axis gridlines. |
| `value_text_style` / `value_format` | `Style \| None` / `FormatterType` | `None` / `None` | Optional inline median value labels and format (`"{:.0f}ms"` or callable). |
| `background_style` | `Style \| None` | `None` | Outer chart background card style. |
| `title` / `title_style` | `str` / `Style \| None` | `""` / `None` | Chart title text and typography style. |

### `BoxStats` Pre-Aggregated Model
```python
BoxStats(
    *,
    min: float,                        # Lower whisker endpoint (e.g. min, fence, or p5)
    q1: float,                         # 25th percentile
    median: float,                     # 50th percentile
    q3: float,                         # 75th percentile
    max: float,                        # Upper whisker endpoint (e.g. max, fence, or p95)
    mean: float | None = None,         # Optional arithmetic mean
    outliers: Sequence[float] | None = None,
    points: Sequence[float] | None = None,
)
# Or compute directly from raw values:
stats = BoxStats.from_values(values, whisker_mode="iqr", iqr_k=1.5, whisker_percentiles=(5.0, 95.0))
```

---

## 3. Methods, Properties & Styling Auto-Derivation

- **`add_series(name, data, style, legend_text_style=None, *, show_box=None, show_points=None, show_outliers=None, show_mean=None, median_style=None, whisker_style=None, point_style=None, outlier_style=None, mean_style=None, point_radius=None, point_shape=None, jitter=None, show=True, draw_ratio=1.0, draw_direction=None) -> Series`**:
  - `data` accepts per-category raw sequences (`list[float]`), `BoxStats` instances, or `[]` / `None` (safely skipped).
  - Passing a single `style` (such as `Styles.PrimaryNeutral`, `Styles.SecondaryNeutral`, or `Styles.PrimaryFlat`) automatically derives contrasting whisker strokes, bold median lines (white on dark flat boxes, deep tone on neutral boxes), and legible strip/outlier/mean markers.
- **`configure_y_axis(...)` / `configure_x_axis(...)` / `value_axis` / `category_axis`**:
  - Supports `scale="linear"` (zoomed Nice Numbers without forced zero-anchoring; pass `min_value=0` to anchor at zero) and `scale="log"` (ideal for wide tail-latency spans).
- **`draw(xy=(0.0, 0.0), *, width=None, height=None, align="bottom_left", scale=1.0)`** & **`draw_legend(...)`**.

---

## 4. Production Examples

### Example 4.1: Benchmark Box + Strip Overlay (`show_box=True, show_points=True`)
```drawlib code=show align=center file=rules_box_overlay_benchmark.png caption="LLM Response Latency Benchmark Combining Quartile Boxes and Deterministic Strip Points"
from drawlib.canvas import save, setup
from drawlib.charts.box import BoxChart
from drawlib.styles import Styles

setup(width=104, height=62)

chart = BoxChart(
    axis_line_style=Styles.MutedDashed,
    categories=["Baseline", "Streaming", "Speculative"],
    width=88.0,
    height=46.0,
    show_box=True,
    show_points=True,
    show_mean=True,
    box_r=0.6,
    jitter=0.44,
    jitter_seed=42,
    axis_text_style=Styles.Muted.patch(text_size=10.0),
    grid_style=Styles.MutedThin,
    title="LLM Token Latency Distribution (N=10 Runs)",
    title_style=Styles.BlackBold.patch(text_size=12.5),
)
chart.add_series(
    "Cold Cache",
    [
        [410, 425, 438, 445, 452, 460, 475, 490, 520, 640],
        [280, 295, 305, 312, 318, 325, 340, 355, 380, 460],
        [195, 205, 212, 218, 224, 230, 238, 248, 265, 315],
    ],
    style=Styles.SecondaryNeutral,
)
chart.add_series(
    "Warm Cache",
    [
        [240, 248, 255, 260, 264, 270, 278, 285, 298, 335],
        [155, 162, 168, 172, 175, 180, 186, 194, 205, 235],
        [108, 114, 118, 121, 125, 128, 133, 138, 145, 168],
    ],
    style=Styles.PrimaryNeutral,
)
chart.configure_y_axis(unit="ms", label="Latency (ms)")
chart.draw(xy=(8.0, 8.0))
chart.draw_legend(xy=(34.0, 57.5), text_style=Styles.DarkBold.patch(text_size=10.0), orientation="horizontal")
save()
```

### Example 4.2: Horizontal Pre-Aggregated Tail Latency (`BoxStats` + `scale="log"`)
```drawlib code=show align=center file=rules_box_horizontal_log.png caption="Horizontal Tail-Latency BoxChart from Pre-Aggregated p5-p95 Cloud Monitoring Metrics on a Log Axis"
from drawlib.canvas import save, setup
from drawlib.charts.box import BoxChart, BoxStats
from drawlib.styles import Styles

setup(width=108, height=62)

chart = BoxChart(
    axis_line_style=Styles.MutedDashed,
    categories=["Edge CDN", "Auth API", "SQL Read", "Vector ANN"],
    orientation="horizontal",
    width=88.0,
    height=46.0,
    box_width_ratio=0.58,
    box_r=0.5,
    axis_text_style=Styles.Muted.patch(text_size=10.0),
    grid_style=Styles.MutedThin,
    title="Service Latency Distribution (p5 / p25 / p50 / p75 / p95 + p99 Outliers)",
    title_style=Styles.BlackBold.patch(text_size=11.5),
)
chart.add_series(
    "Prod Telemetry",
    [
        BoxStats(min=2.5, q1=4.0, median=5.8, q3=8.5, max=18.0, outliers=[42.0]),
        BoxStats(min=8.0, q1=12.0, median=16.5, q3=24.0, max=55.0, outliers=[135.0]),
        BoxStats(min=14.0, q1=22.0, median=31.0, q3=48.0, max=120.0, outliers=[310.0]),
        BoxStats(min=38.0, q1=58.0, median=84.0, q3=145.0, max=420.0, outliers=[980.0, 1450.0]),
    ],
    style=Styles.PrimaryNeutral,
)
chart.configure_x_axis(scale="log", unit="ms", label="Response Time (Log Scale)")
chart.draw(xy=(11.0, 9.0))
save()
```

---

## Related Topics
- Charts Overview & Axis/Legend Architecture: `uv run drawlib rules show lib-charts-overview`
- Bar Charts: `uv run drawlib rules show lib-charts-bar`
- Scatter & Bubble Charts: `uv run drawlib rules show lib-charts-scatter`
