# Drawlib ScatterChart Guidelines (`lib-charts-scatter`)

`ScatterChart` (`drawlib.charts.scatter`) maps continuous numerical data points across dual independent Cartesian axes ($X$ and $Y$). It is ideal for identifying statistical correlations, clustering patterns, latency vs. throughput trade-offs, and multidimensional bubble analysis (where marker radius encodes a third numerical variable).

---

## 1. Conceptual Overview & Imports

```python
from drawlib.charts.scatter import (
    Axis,
    DrawDirection,
    LegendPosition,
    Point,
    PointShape,
    ScaleType,
    ScatterChart,
    Series,
)
```

```text
  Latency (ms) ▲
           100 │           ■ Legacy (High Latency)
            80 │
            60 │                ▲ Worker Pool
            40 │        ●
            20 │    ◆ v1.0 Baseline      ● Async Engine
             0 └────────────────────────────► Throughput (req/s)
               0    200   400   600   800
```

- **Dual Continuous Numerical Axes (`x_axis`, `y_axis`)**: Both horizontal and vertical axes use the `Axis` scaling engine (`ScaleType = Literal["linear", "log"]`, formatted via `FormatterType`).
- **Five Marker Shapes (`PointShape = Literal["circle", "square", "rhombus", "triangle", "none"]`)**: Supports `"circle"`, `"square"`, `"rhombus"`, `"triangle"`, and `"none"` (useful for text-only callout points via `add(..., shape="none", label="...")`).
- **Standalone Annotated Points (`add`) vs. Named Series (`add_series`)**:
  - `chart.add(...)` places an individual `(x, y)` point with an optional `label` and `label_style` callout (standalone points do not appear in the legend and do not take `legend_text_style`).
  - `chart.add_series(...)` registers a named group of `(x, y)` or `(x, y, radius)` points that appears in `chart.draw_legend(...)` (supports `legend_text_style`).

---

## 2. Constructor Parameters (`ScatterChart`)

All constructor arguments are **keyword-only** (`*`):

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| **`axis_line_style`** | `Style` | **Required** | Style for the X and Y coordinate axes baseline and ticks. Mandatory anchor. |
| `width` / `height` | `float` | `88.0` / `55.0` | Overall container dimensions in canvas units. |
| `default_radius` | `float` | `1.0` | Default radius for point markers when `radius` is omitted in `add()` or `add_series()`. |
| `default_shape` | `PointShape` | `"circle"` | Default marker shape (`"circle"`, `"square"`, `"rhombus"`, `"triangle"`, `"none"`). |
| `axis_text_style` | `Style \| None` | `None` | Style for X and Y axis tick marks, numerical labels, and axis titles. If `None`, labels are omitted. |
| `grid_style` | `Style \| None` | `None` | Style for horizontal and vertical Cartesian gridlines. If `None`, gridlines are omitted. |
| `value_text_style` | `Style \| None` | `None` | Default style for text annotation labels (`Point.label`) next to points when `label_style` is `None`. |
| `background_style` | `Style \| None` | `None` | Outer chart background card style. If `None`, card is omitted. |
| `title` | `str` | `""` | Chart title text displayed at the top of the container. |
| `title_style` | `Style \| None` | `None` | Typography style for `title`. Required for the title to render. |

---

## 3. Methods, Properties & Data Models

### 3.1 Methods
- **`add(xy: tuple[float, float], style: Style, radius: float | None = None, shape: PointShape | None = None, label: str = "", label_style: Style | None = None, *, show: bool = True) -> Point`**:
  Adds a single standalone data point at `(x, y)` and returns the mutable `Point` instance.
  - `radius` / `shape`: Per-point marker radius and shape override (inherits `default_radius` / `default_shape` when `None`).
  - `label` / `label_style`: Optional annotation text rendered next to the point (uses `label_style` or falls back to `chart.value_text_style`).
- **`add_series(name: str, data: list[tuple[float, float]] | list[tuple[float, float, float]], style: Style, radius: float | None = None, shape: PointShape | None = None, legend_text_style: Style | None = None, *, show: bool = True, draw_ratio: float = 1.0, draw_direction: DrawDirection = "left_to_right") -> Series`**:
  Adds a named series of 2-tuple `(x, y)` points or 3-tuple `(x, y, radius)` bubble points and returns the mutable `Series` instance.
  - `legend_text_style`: Optional custom `Style` for this series in `draw_legend(...)`.
  - `draw_direction`: `"left_to_right"` *(default)* reveals points progressively left-to-right across the X-axis range; `"bottom_to_top"` raises points from the bottom axis toward target `y` while scaling `radius * draw_ratio`.
- **`configure_x_axis(scale=None, min_value=None, max_value=None, ticks=None, tick_step=None, format=None, unit=None, label=None, show_grid=None, grid_style=None, show_axis_line=None, line_style=None, show_ticks=None, tick_label_style=None) -> Axis`**:
  Configures the continuous numerical horizontal X-axis (`format: FormatterType`).
- **`configure_y_axis(...) -> Axis`**:
  Configures the continuous numerical vertical Y-axis (`format: FormatterType`).
- **`get_size() -> tuple[float, float]`**:
  Returns `(width, height)` of the chart container.
- **`draw(xy: tuple[float, float] = (0.0, 0.0), *, width: float | None = None, height: float | None = None, align: Literal["bottom_left", "center"] = "bottom_left", scale: float = 1.0) -> None`**:
  Renders the scatter chart body onto the canvas anchored at `xy` (`"bottom_left"` or `"center"`), with optional temporary size overrides and proportional `scale`.
- **`draw_legend(xy: tuple[float, float], text_style: Style, orientation: Literal["vertical", "horizontal"] = "vertical", swatch_width: float = 2.4, swatch_height: float = 1.2, item_gap: float = 4.0, *, scale: float = 1.0) -> None`**:
  Renders the standalone series legend at `xy`.

### 3.2 Properties & Data Models (`Point`, `Series`)
- **`chart.points -> list[Point]`**: Copy of standalone `Point` objects registered via `add()`.
- **`chart.series -> list[Series]`**: Copy of `Series` objects registered via `add_series()`.
- **`chart.x_axis -> Axis`** / **`chart.y_axis -> Axis`**: Direct access to horizontal and vertical `Axis` instances.
- **`Point(xy: tuple[float, float], style: Style, radius: float = 1.0, shape: PointShape = "circle", label: str = "", label_style: Style | None = None, *, show: bool = True)`**:
  Stores `xy`, `style`, `radius`, `shape`, `label`, `label_style`, and `show` (note: `Point` does not have `legend_text_style`).
- **`Series(name: str, points: list[Point], style: Style, radius: float = 1.0, shape: PointShape = "circle", legend_text_style: Style | None = None, *, show: bool = True, draw_ratio: float = 1.0, draw_direction: DrawDirection = "left_to_right")`**:
  Groups member `points` under `name` with `style`, `radius`, `shape`, `legend_text_style`, `show`, `draw_ratio`, and `draw_direction`.

---

## 4. Production Examples

### Example 4.1: Benchmark Scatter with Labeled Baseline Points & Marker Shapes
```drawlib code=show align=center file=rules_scatter_benchmark.png caption="Service Throughput vs p99 Latency Benchmark with ScatterChart"
from drawlib.canvas import save, setup
from drawlib.charts.scatter import ScatterChart
from drawlib.styles import Styles

setup(width=105, height=75)

chart = ScatterChart(
    axis_line_style=Styles.MutedDashed,
    axis_text_style=Styles.Muted.patch(text_size=10.0),
    value_text_style=Styles.BlackBold.patch(text_size=9.5),
    grid_style=Styles.MutedThin,
    width=85.0,
    height=52.0,
    title="Service Throughput vs p99 Latency Benchmark",
    title_style=Styles.BlackBold.patch(text_size=13.0),
)
chart.configure_x_axis(label="Throughput (req/sec)", unit=" rps", min_value=0, max_value=1000)
chart.configure_y_axis(label="p99 Latency (ms)", unit=" ms", min_value=0, max_value=200)

chart.add(xy=(100.0, 20.0), style=Styles.Neutral, radius=1.5, shape="rhombus", label="v1.0 Baseline")
chart.add(xy=(720.0, 38.0), style=Styles.PrimaryNeutral, radius=1.8, shape="triangle", label="v2.5 Target")

chart.add_series(
    name="Async Rust Engine",
    data=[(360, 18.0), (540, 19.5), (720, 21.0), (950, 24.0)],
    style=Styles.PrimaryFlat,
    shape="circle",
)
chart.add_series(
    name="Go Worker Pool",
    data=[(320, 42.0), (480, 54.0), (650, 68.0), (850, 92.0)],
    style=Styles.SecondaryNeutral,
    shape="triangle",
)
chart.add_series(
    name="Legacy Threadpool",
    data=[(150, 45.0), (300, 75.0), (450, 120.0), (600, 168.0)],
    style=Styles.Dark,
    shape="square",
)
chart.draw(xy=(10.0, 10.0))
chart.draw_legend(xy=(18.0, 56.0), text_style=Styles.Muted.patch(text_size=10.0), orientation="horizontal")
save()
```

### Example 4.2: Multidimensional Cloud Cost Bubble Chart (`(x, y, radius)`)
```drawlib code=show align=center file=rules_scatter_bubble_plot.png caption="Compute Workload Multidimensional Bubble Plot"
from drawlib.canvas import save, setup
from drawlib.charts.scatter import ScatterChart
from drawlib.styles import Styles

setup(width=105, height=75)

chart = ScatterChart(
    axis_line_style=Styles.MutedDashed,
    axis_text_style=Styles.Muted.patch(text_size=10.0),
    grid_style=Styles.MutedThin,
    width=85.0,
    height=52.0,
    title="Compute Workload: Duration vs Memory vs Cost (Bubble Size)",
    title_style=Styles.BlackBold.patch(text_size=13.0),
)
chart.configure_x_axis(label="Allocated RAM (GB)", unit=" GB", min_value=0, max_value=36)
chart.configure_y_axis(label="Job Execution Time (sec)", unit=" s", min_value=0, max_value=60)

# 3-Tuples encode: (RAM_GB, Execution_Time_Sec, Monthly_Cost_Radius)
chart.add_series(
    name="Serverless Functions",
    data=[(1.0, 48.0, 0.8), (2.0, 28.0, 1.1), (4.0, 16.0, 1.5), (8.0, 10.0, 1.9)],
    style=Styles.PrimaryFlat,
    shape="circle",
)
chart.add_series(
    name="Dedicated Kubernetes Pods",
    data=[(4.0, 22.0, 1.2), (8.0, 14.0, 1.5), (16.0, 8.5, 1.9), (32.0, 5.0, 2.4)],
    style=Styles.SecondaryNeutral,
    shape="rhombus",
)
chart.draw(xy=(10.0, 10.0))
chart.draw_legend(xy=(22.0, 56.0), text_style=Styles.Muted.patch(text_size=10.0), orientation="horizontal")
save()
```

---

## 5. Related Rules
- Charts Overview & Axis/Legend Architecture: `uv run drawlib rules show lib-charts-overview`
- Line Charts: `uv run drawlib rules show lib-charts-line`
- Heatmap Charts & Overlays: `uv run drawlib rules show lib-charts-heatmap`
