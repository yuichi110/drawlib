# Drawlib LineChart Guidelines (`lib-charts-line`)

`LineChart` (`drawlib.charts.line`) displays continuous trends over ordered categorical intervals, time periods, or experimental steps. It supports straight polygonal line segments (`smooth=False`) or smooth cubic spline curves (`smooth=True`), customizable vertex markers (`PointShape`), multi-series stroke patterns (`LineStyle`), and decoupled legend rendering.

---

## 1. Conceptual Overview & Imports

```python
from drawlib.charts.line import (
    Axis,
    DrawDirection,
    FormatterType,
    LegendPosition,
    LineChart,
    LineStyle,
    PointShape,
    Series,
)
```

```text
  Y ▲                      Smooth Spline (smooth=True)
    │           ●─────●
    │         ╱         ╲
    │   ●───●             ●
    │ ╱
    └────────────────────────► X
       Jan  Feb  Mar  Apr  May
```

- **Straight vs. Smooth Curves (`smooth`)**:
  - `smooth=False` *(default)*: Connects category vertices with crisp, straight polygonal line segments.
  - `smooth=True`: Interpolates smooth curved segments through data vertices (when 3 or more points are present).
- **Vertex Markers (`PointShape = Literal["circle", "square", "rhombus", "triangle", "none"]`)**:
  - Chart-level `show_points`, `point_shape` (`"circle"`, `"square"`, `"none"`), and `point_size` (`0.7` default) apply to all series unless overridden per series in `add_series(..., point_shape=..., point_size=...)`.
  - Setting `point_shape="none"` on a specific series suppresses both its vertex markers and its `value_text_style` labels—ideal for flat target or threshold reference lines.
- **Stroke Patterns (`LineStyle = Literal["solid", "dashed", "dotted", "dashdot"]`)**:
  - Configured per series via `add_series(..., line_width=2.0, line_style="solid")`.
- **Vertex Value Formatting**:
  - `LineChart` does not take a `value_format` constructor parameter; when `value_text_style` is provided, vertex values are formatted using `chart.y_axis.format_value(v)` (configured via `chart.configure_y_axis(format=..., unit=...)`).

---

## 2. Constructor Parameters (`LineChart`)

All constructor arguments are **keyword-only** (`*`):

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| **`axis_line_style`** | `Style` | **Required** | Style for the Cartesian axes baseline and ticks. Mandatory anchor. |
| **`categories`** | `list[str]` | **Required** | Ordered category labels along the horizontal X-axis. |
| `width` / `height` | `float` | `80.0` / `50.0` | Total bounding box dimensions on the canvas. |
| `show_points` | `bool` | `True` | Whether to draw marker points at vertex coordinates. |
| `point_shape` | `PointShape` | `"circle"` | Default shape of vertex markers (`"circle"`, `"square"`, `"none"`). |
| `point_size` | `float` | `0.7` | Default marker radius or half-width in canvas units. |
| `smooth` | `bool` | `False` | When `True`, uses smooth interpolated spline curve rendering. |
| `axis_text_style` | `Style \| None` | `None` | Style for Y-axis tick labels and X-axis category names. If `None`, labels are omitted. |
| `grid_style` | `Style \| None` | `None` | Style for horizontal Y-axis gridlines. If `None`, gridlines are omitted. |
| `value_text_style` | `Style \| None` | `None` | Style for numerical values above vertex markers. If `None`, values are omitted. |
| `background_style` | `Style \| None` | `None` | Outer chart background card style. If `None`, card is omitted. |
| `title` | `str` | `""` | Title text displayed at the top of the chart. |
| `title_style` | `Style \| None` | `None` | Typography style for `title`. Required for the title to render. |

---

## 3. Methods, Properties & Data Models

### 3.1 Methods
- **`add_series(name: str, values: list[float], style: Style, line_width: float = 2.0, line_style: LineStyle = "solid", point_shape: PointShape | None = None, point_size: float | None = None, legend_text_style: Style | None = None, *, show: bool = True, draw_ratio: float = 1.0, draw_direction: DrawDirection = "left_to_right") -> Series`**:
  Registers a line series and returns the mutable `Series` instance.
  - `point_shape` and `point_size` override chart-level defaults when not `None`.
  - `draw_direction`: `"left_to_right"` *(default)* extends the polyline/spline continuously from left to right along arc length; `"bottom_to_top"` raises all vertices simultaneously from the baseline toward target `y`.
- **`configure_y_axis(scale=None, min_value=None, max_value=None, ticks=None, tick_step=None, format=None, unit=None, label=None, show_grid=None, grid_style=None, show_axis_line=None, line_style=None, show_ticks=None, tick_label_style=None) -> Axis`**:
  Configures the vertical value axis scale, ticks, formatters, and labels.
- **`configure_x_axis(...) -> Axis`**:
  Configures the horizontal category axis baseline and tick label styles.
- **`get_size() -> tuple[float, float]`**:
  Returns `(width, height)` of the chart container.
- **`draw(xy: tuple[float, float] = (0.0, 0.0), *, width: float | None = None, height: float | None = None, align: Literal["bottom_left", "center"] = "bottom_left", scale: float = 1.0) -> None`**:
  Renders the line chart onto the canvas anchored at `xy` (`"bottom_left"` or `"center"`), with optional temporary size overrides and proportional `scale`.
- **`draw_legend(xy: tuple[float, float], text_style: Style, orientation: Literal["vertical", "horizontal"] = "vertical", swatch_width: float = 2.4, swatch_height: float = 1.2, item_gap: float = 4.0, *, scale: float = 1.0) -> None`**:
  Renders the standalone series legend at `xy`.

### 3.2 Properties & `Series` Model
- **`chart.series -> list[Series]`**: Copy of registered `Series` objects.
- **`chart.x_axis -> Axis`** / **`chart.y_axis -> Axis`**: Direct access to horizontal and vertical `Axis` instances.
- **`Series(name: str, values: list[float], style: Style, line_width: float = 2.0, line_style: LineStyle = "solid", point_shape: PointShape = "circle", point_size: float = 0.7, legend_text_style: Style | None = None, *, show: bool = True, draw_ratio: float = 1.0, draw_direction: DrawDirection = "left_to_right")`**:
  Stores `name`, `values`, `style`, `line_width`, `line_style`, `point_shape`, `point_size`, `legend_text_style`, `show`, `draw_ratio`, and `draw_direction`.

---

## 4. Production Examples

### Example 4.1: Multi-Series Active Users Growth (Smooth Spline)
```drawlib code=show align=center file=rules_line_user_growth.png caption="Smooth Spline Multi-Series Growth with LineChart"
from drawlib.canvas import save, setup
from drawlib.charts.line import LineChart
from drawlib.styles import Styles

setup(width=100, height=70)

chart = LineChart(
    axis_line_style=Styles.MutedDashed,
    categories=["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    width=82.0,
    height=46.0,
    title="Platform MAU Growth (2025 vs 2026)",
    title_style=Styles.BlackBold.patch(text_size=13.0),
    smooth=True,
    show_points=True,
    point_size=0.75,
    axis_text_style=Styles.Muted.patch(text_size=10.0),
    grid_style=Styles.MutedThin,
)
chart.add_series("2025 Baseline", [45.0, 52.0, 58.0, 65.0, 72.0, 80.0], style=Styles.DarkFlat, line_width=2.2, line_style="dashed")
chart.add_series("2026 Accelerated", [60.0, 75.0, 88.0, 110.0, 135.0, 160.0], style=Styles.PrimaryFlat, line_width=2.5)
chart.configure_y_axis(unit="k", label="Active Users (Thousands)")
chart.draw(xy=(9.0, 8.0))
chart.draw_legend(xy=(24.0, 58.0), text_style=Styles.Muted.patch(text_size=10.0), orientation="horizontal")
save()
```

### Example 4.2: Straight Segments, Square Markers, Value Labels & SLO Threshold
```drawlib code=show align=center file=rules_line_markers_and_thresholds.png caption="Straight Line Segments with Square Vertex Markers, Value Labels, and Dashdot SLO Threshold"
from drawlib.canvas import save, setup
from drawlib.charts.line import LineChart
from drawlib.styles import Styles

setup(width=110, height=70)

chart = LineChart(
    axis_line_style=Styles.MutedDashed,
    categories=["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"],
    width=88.0,
    height=48.0,
    title="API Gateway p95 Latency & Alert Thresholds",
    title_style=Styles.BlackBold.patch(text_size=13.0),
    smooth=False,
    show_points=True,
    axis_text_style=Styles.Muted.patch(text_size=10.0),
    grid_style=Styles.MutedThin,
    value_text_style=Styles.DarkBold.patch(text_size=9.5),
)
chart.add_series(
    "Primary Region (p95)",
    [24.0, 20.0, 46.0, 68.0, 54.0, 32.0],
    style=Styles.PrimaryFlat,
    line_width=2.2,
    point_shape="square",
    point_size=0.8,
)
chart.add_series(
    "Failover Replica",
    [18.0, 15.0, 30.0, 42.0, 35.0, 22.0],
    style=Styles.SecondaryFlat,
    line_width=2.0,
    line_style="dotted",
    point_shape="none",
)
chart.add_series(
    "SLO Ceiling (80 ms)",
    [80.0, 80.0, 80.0, 80.0, 80.0, 80.0],
    style=Styles.DarkFlat,
    line_width=1.8,
    line_style="dashdot",
    point_shape="none",
)
chart.configure_y_axis(min_value=0.0, max_value=100.0, tick_step=20.0, format="{:.0f}", unit="ms")
chart.draw(xy=(11.0, 8.0))
chart.draw_legend(xy=(13.0, 60.5), text_style=Styles.Muted.patch(text_size=10.0), orientation="horizontal")
save()
```

---

## 5. Related Rules
- Charts Overview & Axis/Legend Architecture: `uv run drawlib rules show lib-charts-overview`
- Area Charts: `uv run drawlib rules show lib-charts-area`
- Bar Charts: `uv run drawlib rules show lib-charts-bar`
