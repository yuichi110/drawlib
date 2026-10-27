# Drawlib AreaChart Guidelines (`lib-charts-area`)

`AreaChart` (`drawlib.charts.area`) communicates quantitative volume and stream contributions over ordered categories or time intervals through shaded geometric polygons anchored to the baseline ($Y=0$). It supports overlapping semi-transparent polygons (`mode="overlap"`), cumulative stacked areas (`mode="stack"`), smooth spline contours (`smooth=True`), vertex markers, and decoupled legend rendering.

---

## 1. Conceptual Overview & Imports

```python
from drawlib.charts.area import (
    AreaChart,
    Axis,
    DrawDirection,
    FormatterType,
    LegendPosition,
    Mode,
    Series,
)
```

```text
      mode="overlap" (Semi-transparent)           mode="stack" (Cumulative)
  Y ▲                                         Y ▲
    │        ▲                                  │         ▲ Layer 2
    │       ╱ █╲    ▲                           │        ╱█╲
    │     ▲╱  █ ╲  ╱ ╲                          │      ▲╱███╲
    │    ╱ █  █  ╲╱   ╲                         │     ╱██████╲ Layer 1
    └───┴──┴──┴───┴────┴──► X                   └────┴────────┴────► X
```

- **`mode="overlap"` *(default)***: Each series polygon starts independently at the baseline ($Y=0$) and overlaps with preceding series using semi-transparent fill opacity (`fill_alpha=0.35`).
- **`mode="stack"`**: Cumulative stacked areas where each series layer rests directly on top of the preceding series, visualizing aggregate volume and individual stream shares.
- **Vertex Value Labels (`value_text_style`)**: When `value_text_style` is provided alongside `show_points=True` and `point_shape != "none"`, numeric labels formatted via `y_axis.format_value(v)` are drawn above vertex markers.

---

## 2. Constructor Parameters (`AreaChart`)

All constructor arguments are **keyword-only** (`*`):

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| **`axis_line_style`** | `Style` | **Required** | Style for the Cartesian axes baseline and ticks. Mandatory anchor. |
| **`categories`** | `list[str]` | **Required** | Ordered category labels along the horizontal X-axis. |
| `width` / `height` | `float` | `80.0` / `50.0` | Total chart bounding box dimensions on the canvas. |
| `mode` | `"overlap"` \| `"stack"` | `"overlap"` | Area polygon composition mode (`Mode`). |
| `fill_alpha` | `float` | `0.35` | Default transparency opacity for area fill polygons (`0.0` to `1.0`). |
| `show_points` | `bool` | `False` | Whether to render markers along the upper boundary contour. |
| `point_shape` | `"circle"` \| `"square"` \| `"none"` | `"none"` | Default marker shape at data vertices when `show_points=True`. |
| `point_size` | `float` | `1.0` | Default radius (or half-width) of point markers in canvas units. |
| `smooth` | `bool` | `False` | When `True`, boundary lines and filled polygons follow smooth spline curves. |
| `axis_text_style` | `Style \| None` | `None` | Style for Y-axis tick labels and X-axis category names. If `None`, labels are omitted. |
| `grid_style` | `Style \| None` | `None` | Style for horizontal Y-axis gridlines. If `None`, gridlines are omitted. |
| `value_text_style` | `Style \| None` | `None` | Style for numeric labels drawn above vertex markers. If `None`, value labels are omitted. |
| `background_style` | `Style \| None` | `None` | Outer chart background card style. If `None`, card is omitted. |
| `title` | `str` | `""` | Chart title text displayed at the top of the container. |
| `title_style` | `Style \| None` | `None` | Typography style for `title`. Required for the title to render. |

---

## 3. Methods, Properties & Data Models

### 3.1 Methods
- **`add_series(name: str, values: list[float], style: Style, fill_alpha: float | None = None, line_width: float = 2.0, line_style: LineStyle = "solid", point_shape: PointShape | None = None, point_size: float | None = None, legend_text_style: Style | None = None, *, show: bool = True, draw_ratio: float = 1.0, draw_direction: DrawDirection = "left_to_right") -> Series`**:
  Registers an area series and returns the mutable `Series` instance.
  - `fill_alpha`: Per-series polygon fill opacity override (inherits `chart.fill_alpha` when `None`).
  - `line_width` / `line_style`: Stroke width (`2.0`) and pattern (`"solid"`, `"dashed"`, `"dotted"`, `"dashdot"`) for the upper boundary contour.
  - `point_shape` / `point_size`: Per-series vertex marker overrides (`"circle"`, `"square"`, `"none"`).
  - `draw_direction`: `"left_to_right"` *(default)* sweeps the area polygon and upper contour continuously from left to right; `"bottom_to_top"` raises the area polygon vertically from the baseline (or lower stack boundary).
- **`configure_y_axis(scale=None, min_value=None, max_value=None, ticks=None, tick_step=None, format=None, unit=None, label=None, show_grid=None, grid_style=None, show_axis_line=None, line_style=None, show_ticks=None, tick_label_style=None) -> Axis`**:
  Configures the vertical value axis scale, ticks, formatters, and labels.
- **`configure_x_axis(...) -> Axis`**:
  Configures the horizontal category axis baseline and tick label styles.
- **`get_size() -> tuple[float, float]`**:
  Returns `(width, height)` of the chart container.
- **`draw(xy: tuple[float, float] = (0.0, 0.0), *, width: float | None = None, height: float | None = None, align: Literal["bottom_left", "center"] = "bottom_left", scale: float = 1.0) -> None`**:
  Renders the area chart onto the canvas anchored at `xy` (`"bottom_left"` or `"center"`), with optional temporary size overrides and proportional `scale`.
- **`draw_legend(xy: tuple[float, float], text_style: Style, orientation: Literal["vertical", "horizontal"] = "vertical", swatch_width: float = 2.4, swatch_height: float = 1.2, item_gap: float = 4.0, *, scale: float = 1.0) -> None`**:
  Renders the standalone series legend at `xy`.

### 3.2 Properties & `Series` Model
- **`chart.series -> list[Series]`**: Copy of registered `Series` objects.
- **`chart.x_axis -> Axis`** / **`chart.y_axis -> Axis`**: Direct access to horizontal and vertical `Axis` instances.
- **`Series(name: str, values: list[float], style: Style, fill_alpha: float | None = None, line_width: float = 2.0, line_style: LineStyle = "solid", point_shape: PointShape = "none", point_size: float = 1.0, legend_text_style: Style | None = None, *, show: bool = True, draw_ratio: float = 1.0, draw_direction: DrawDirection = "left_to_right")`**:
  Stores `name`, `values`, `style`, `fill_alpha`, `line_width`, `line_style`, `point_shape`, `point_size`, `legend_text_style`, `show`, `draw_ratio`, and `draw_direction`.

---

## 4. Production Examples

### Example 4.1: Cumulative Stacked Revenue Streams (`mode="stack"`)
```drawlib code=show align=center file=rules_area_stacked_revenue.png caption="Cumulative Stacked Revenue Streams with AreaChart"
from drawlib.canvas import save, setup
from drawlib.charts.area import AreaChart
from drawlib.styles import Styles

setup(width=102, height=74)

chart = AreaChart(
    axis_line_style=Styles.MutedDashed,
    categories=["2021", "2022", "2023", "2024", "2025"],
    width=82.0,
    height=52.0,
    title="Cumulative Revenue Streams",
    title_style=Styles.BlackBold.patch(text_size=13.0),
    mode="stack",
    fill_alpha=0.65,
    axis_text_style=Styles.Muted.patch(text_size=10.0),
    grid_style=Styles.MutedThin,
)
chart.add_series("Enterprise Cloud", [40.0, 70.0, 110.0, 160.0, 225.0], style=Styles.PrimaryFlat)
chart.add_series("SaaS Products", [25.0, 38.0, 52.0, 68.0, 85.0], style=Styles.PrimaryNeutral)
chart.add_series("Support & Advisory", [15.0, 18.0, 22.0, 24.0, 26.0], style=Styles.SecondaryNeutral)
chart.configure_y_axis(unit="M$", label="Gross Revenue (USD Millions)")
chart.draw(xy=(10.0, 10.0))
chart.draw_legend(xy=(14.0, 65.0), text_style=Styles.Muted.patch(text_size=10.0), orientation="horizontal")
save()
```

### Example 4.2: Smooth Overlapping Gateway Traffic (`mode="overlap"`)
```drawlib code=show align=center file=rules_area_overlap_traffic.png caption="Smooth Overlapping Gateway Traffic with Per-Series fill_alpha"
from drawlib.canvas import save, setup
from drawlib.charts.area import AreaChart
from drawlib.styles import Colors, Style, Styles

setup(width=102, height=72)

chart = AreaChart(
    axis_line_style=Styles.MutedDashed,
    categories=["02:00", "06:00", "10:00", "14:00", "18:00", "22:00"],
    width=82.0,
    height=50.0,
    title="Ingress vs Egress Gateway Traffic (Smooth Spline)",
    title_style=Styles.BlackBold.patch(text_size=13.0),
    mode="overlap",
    fill_alpha=0.35,
    smooth=True,
    show_points=True,
    point_shape="circle",
    point_size=0.65,
    axis_text_style=Styles.Muted.patch(text_size=10.0),
    grid_style=Styles.MutedThin,
)
chart.add_series(
    "Ingress Traffic",
    [120.0, 180.0, 650.0, 920.0, 780.0, 310.0],
    style=Style(line_color=Colors.Primary),
    fill_alpha=0.32,
    line_width=2.2,
)
chart.add_series(
    "Egress Traffic",
    [80.0, 110.0, 420.0, 610.0, 530.0, 220.0],
    style=Style(line_color=Colors.Secondary),
    fill_alpha=0.22,
    line_width=2.0,
    line_style="dashed",
    point_shape="square",
)
chart.configure_y_axis(unit="Gbps", label="Throughput (Gbps)")
chart.draw(xy=(10.0, 10.0))
chart.draw_legend(xy=(24.0, 63.0), text_style=Styles.Muted.patch(text_size=10.0), orientation="horizontal")
save()
```

---

## 5. Related Rules
- Charts Overview & Axis/Legend Architecture: `uv run drawlib rules show lib-charts-overview`
- Line Charts: `uv run drawlib rules show lib-charts-line`
- Bar Charts: `uv run drawlib rules show lib-charts-bar`
