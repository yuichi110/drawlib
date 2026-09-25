# Drawlib Charts Guidelines

`drawlib.charts` provides a declarative, pure-Python visualization engine for statistical, comparative, relational, and project schedule charts.  
Unlike external plotting libraries that produce isolated raster images, Drawlib charts render directly into the Drawlib vector canvas using standard primitives, shapes, text, and styles. This ensures seamless visual and programmatic integration with system architectures, flowcharts, and technical documentation.

---

## 1. Overview & Architecture

### 1.1 Philosophy: Illustration-as-Code for Data
Drawlib charts adhere to four foundational principles:
1. **Canvas Coexistence**: Charts are first-class canvas elements positioned at arbitrary `(x, y)` coordinates. Multiple charts, architecture diagrams, callouts, and icon annotations can share a single canvas.
2. **Deterministic Layout**: Bounding boxes, margins, legend offsets, and tick spacing are computed deterministically from explicit dimensions (`width`, `height`), preventing rendering drift.
3. **Pure-Python Data Models**: Series, slices, tasks, and points are defined through clean, strongly-typed data objects (`BarSeries`, `LineSeries`, `GanttTask`, `PieSlice`, `ScatterPoint`).
4. **Unified Styling Engine**: All chart elements—bars, area polygons, curves, gridlines, axes, text badges, and legends—are styled using Drawlib's `Style`, `Colors`, and `Font` models.

### 1.2 Module Structure & Imports
All public chart types, series models, configuration classes, and enums are exported directly from `drawlib.charts`:

```python
from drawlib.charts import (
    # Chart Containers
    AreaChart,
    BarChart,
    GanttChart,
    LineChart,
    PieChart,
    RadarChart,
    ScatterChart,
    # Axis & Configuration Models
    Axis,
    # Series & Data Models
    AreaSeries,
    BarSeries,
    GanttDependency,
    GanttMarker,
    GanttMilestone,
    GanttSection,
    GanttTask,
    LineSeries,
    PieSlice,
    RadarSeries,
    ScatterPoint,
    ScatterSeries,
    # Enums & Type Literals
    AreaMode,
    BarMode,
    ColorType,
    FormatterType,
    GridShape,
    LegendPosition,
    Orientation,
    PointShape,
    ScaleType,
)
```

### 1.3 Chart Family Taxonomy

```text
┌──────────────────────────────────────────────────────────────────────────────────┐
│                             drawlib.charts Taxonomy                              │
├──────────────────────────┬────────────────────────────┬──────────────────────────┤
│ Categorical Binned       │ Continuous & Relational    │ Radial & Temporal        │
├──────────────────────────┼────────────────────────────┼──────────────────────────┤
│ • BarChart (Group/Stack) │ • LineChart (Linear/Spline)│ • PieChart (Pie/Donut)   │
│   - Vertical bars        │ • AreaChart (Overlap/Stack)│ • RadarChart (Spiderweb) │
│   - Horizontal bars      │ • ScatterChart (XY/Bubble) │ • GanttChart (Timelines) │
└──────────────────────────┴────────────────────────────┴──────────────────────────┘
```

---

## 2. Core Architecture & Data Model Fundamentals

### 2.1 Placement Coordinates and Bounding Dimensions
Every chart class implements a consistent positioning and measurement interface:
- **`draw(xy=(x, y))`**: Renders the chart onto the canvas. The `xy` tuple defines the **bottom-left corner** of the chart's total bounding container (including margins, titles, and legends).
- **`get_size() -> tuple[float, float]`**: Returns `(width, height)` representing the total bounding box dimensions on the canvas.

```text
   (x, y + height) ┌──────────────────────────────────────┐
                   │ Chart Title                          │
                   │   ┌──────────────────────────────┐   │
                   │   │ Data Plotting Area           │   │
                   │   │                              │   │
                   │   │                              │   │
                   │   └──────────────────────────────┘   │
                   │       Legend / Axis Labels           │
   (x, y)          └──────────────────────────────────────┘ (x + width, y)
```

### 2.2 The Axis System (`Axis`)
Cartesian charts (`BarChart`, `LineChart`, `AreaChart`, `ScatterChart`) use the `Axis` model to control coordinate mapping, tick generation, and grid rendering.

```python
class Axis:
    def __init__(
        self,
        scale: ScaleType = "linear",
        min_value: float | None = None,
        max_value: float | None = None,
        ticks: list[float] | None = None,
        tick_step: float | None = None,
        format: FormatterType = None,
        unit: str = "",
        label: str = "",
        show_grid: bool = True,
        grid_style: Style | None = None,
        show_axis_line: bool = True,
        line_style: Style | None = None,
        show_ticks: bool = True,
        tick_label_style: Style | None = None,
        tick_label_angle: float = 0.0,
    ) -> None:
        ...
```

#### Axis Scaling Engines:
1. **`scale="linear"`**: Uses the **Nice Numbers algorithm** to automatically select human-readable steps ($1, 2, 5 \times 10^k$) across the data span. If `min_value` or `max_value` are omitted, bounds expand to the nearest nice tick.
2. **`scale="log"`**: Logarithmic base-10 scaling for exponential data. Bounds snap to powers of 10 ($10^0, 10^1, 10^2, \dots$), with intermediate ticks ($1, 2, 5 \times 10^k$) generated when the order-of-magnitude span is $\le 2$.

#### Value Formatting (`format` & `unit`):
- **String Formatter**: Standard Python format specifiers, e.g. `format="{:.1f}"` or `format="{:.0f}%"`.
- **Callable Formatter**: A custom formatting function `Callable[[float], str]`, e.g. `lambda v: f"${v:,.0f}k"`.
- **Unit Append**: If `unit` is supplied (e.g. `unit="ms"` or `unit="M$"`), it is automatically appended to formatted labels if not already present.

#### Axis Configuration Pattern:
Axes are typically configured via the chart's `configure_x_axis()` and `configure_y_axis()` helper methods:

```python
# Fluent in-place configuration of ticks, labels, and formatting
chart.configure_y_axis(
    min_value=0.0,
    max_value=500.0,
    tick_step=100.0,
    ticks=[0.0, 100.0, 250.0, 500.0],  # Explicit tick overrides
    format="${:,.0f}",
    unit="k",
    label="Operating Budget (USD)",
    show_grid=True,
    tick_label_angle=45.0,  # Angled labels for compact layouts
)
```

### 2.3 Default Color Palette
When series colors are left as `None`, Drawlib selects colors sequentially from the built-in categorical palette:

```python
DEFAULT_CHART_PALETTE: list[ColorType] = [
    (59, 130, 246, 1.0),   # Blue
    (16, 185, 129, 1.0),   # Emerald Green
    (245, 158, 11, 1.0),   # Amber
    (244, 63, 94, 1.0),    # Rose Red
    (99, 102, 241, 1.0),   # Indigo
    (6, 182, 212, 1.0),    # Cyan
    (168, 85, 247, 1.0),   # Purple
    (249, 115, 22, 1.0),   # Orange
]
```

---

## 3. BarChart: Grouped, Stacked, and Horizontal Bars

### 3.1 Conceptual Overview
`BarChart` compares discrete categories across one or more data series. It supports both vertical columns and horizontal bars, side-by-side grouped layouts, and cumulative stacked layouts.

```text
       Vertical Grouped                      Horizontal Stacked
  Y ▲                                   Y ▲
    │  ┌──┐ ┌──┐                          │ ┌────────┬─────┬──┐ Cat 2
    │  │  │ │  │   ┌──┐ ┌──┐              │ ├────────┼─────┴──┘
    │  │  │ │  │   │  │ │  │              │ ┌──────┬───────┐    Cat 1
    │  │  │ │  │   │  │ │  │              │ └──────┴───────┘
    └──┴──┴─┴──┴───┴──┴─┴──┴──► X         └──────────────────────► X
        Cat 1        Cat 2                    0%     50%    100%
```

### 3.2 Constructor Parameters
| Parameter | Type | Default | Description |
|---|---|---|---|
| `categories` | `list[str]` | `[]` | Category labels along the category axis. |
| `width` / `height` | `float` | `60.0` / `40.0` | Bounding box dimensions on the canvas. |
| `orientation` | `"vertical"` \| `"horizontal"` | `"vertical"` | Direction of bars. |
| `bar_mode` | `"group"` \| `"stack"` | `"group"` | Grouped side-by-side or stacked cumulatively. |
| `bar_width_ratio` | `float` | `0.7` | Relative thickness ratio of bars within category bin (0.1 to 1.0). |
| `r` | `float` | `0.0` | Corner rounding radius for bar rectangles. |
| `show_values` | `bool` | `False` | Whether to render numerical text labels on or above bars. |
| `value_format` | `FormatterType` | `None` | Formatter string or callable for value labels. |
| `legend_position` | `LegendPosition` | `"auto"` | Placement of legend (`"auto"`, `"top"`, `"bottom"`, `"right"`, `"none"`). |

### 3.3 Methods & Data Model
- `add_series(name: str, values: list[float], color: ColorType | None = None, style: Style | None = None) -> BarSeries`
- `configure_y_axis(...) -> Axis`: Configures vertical axis (value axis for vertical, category axis for horizontal).
- `configure_x_axis(...) -> Axis`: Configures horizontal axis (category axis for vertical, value axis for horizontal).
- `draw(xy: tuple[float, float] = (0.0, 0.0)) -> None`: Renders chart at bottom-left position `xy`.

`BarSeries` encapsulates `name: str`, `values: list[float]`, `color: ColorType | None`, and `style: Style | None`.

### 3.4 Production Examples

#### Example 3.4.1: Vertical Grouped Bar Chart with Value Labels
```drawlib show-code
from drawlib import canvas
from drawlib.charts import BarChart

canvas.initialize()
canvas.config(width=100, height=80)

chart = BarChart(
    categories=["Q1", "Q2", "Q3", "Q4"],
    width=80.0,
    height=55.0,
    title="Quarterly Enterprise Revenue",
    orientation="vertical",
    bar_mode="group",
    bar_width_ratio=0.75,
    r=1.0,
    show_values=True,
    value_format="{:.1f}M",
    legend_position="top",
)
chart.add_series("SaaS Subscriptions", [45.2, 58.0, 72.5, 91.0])
chart.add_series("Professional Services", [22.0, 24.5, 21.0, 19.5])
chart.configure_y_axis(unit="$", label="Revenue (USD Millions)", show_grid=True)
chart.draw(xy=(10.0, 15.0))
```

#### Example 3.4.2: Horizontal Stacked Bar Chart with Resource Breakdown
```drawlib show-code
from drawlib import canvas
from drawlib.charts import BarChart

canvas.initialize()
canvas.config(width=105, height=75)

chart = BarChart(
    categories=["Frontend", "API Gateway", "Database", "Search Index"],
    width=85.0,
    height=50.0,
    orientation="horizontal",
    bar_mode="stack",
    bar_width_ratio=0.6,
    r=0.8,
    title="Infrastructure Resource Utilization (%)",
    show_values=True,
    value_format="{:.0f}%",
    legend_position="right",
)
chart.add_series("CPU", [35.0, 55.0, 80.0, 45.0])
chart.add_series("Memory", [40.0, 30.0, 15.0, 35.0])
chart.add_series("Storage I/O", [25.0, 15.0, 5.0, 20.0])
chart.configure_x_axis(min_value=0.0, max_value=100.0, tick_step=20.0, unit="%", show_grid=True)
chart.draw(xy=(10.0, 15.0))
```

#### Example 3.4.3: Logarithmic Scale Latency Benchmark
```drawlib show-code
from drawlib import canvas
from drawlib.charts import BarChart

canvas.initialize()
canvas.config(width=100, height=75)

chart = BarChart(
    categories=["L1 Cache", "RAM", "NVMe SSD", "Cross-Region API"],
    width=80.0,
    height=55.0,
    title="Read Latency Comparison (Log Scale)",
    show_values=True,
    value_format="{:g} ns",
)
chart.add_series("Access Time", [1.0, 100.0, 150000.0, 150000000.0])
chart.configure_y_axis(scale="log", unit="ns", label="Nanoseconds (log10)", show_grid=True)
chart.draw(xy=(10.0, 12.0))
```

---

## 4. LineChart: Continuous Trends, Markers, and Splines

### 4.1 Conceptual Overview
`LineChart` displays continuous trends over categorical intervals, time periods, or experimental steps. It supports straight polygonal line segments or smooth cubic-like spline curves, customizable data point markers (`circle`, `square`, `none`), and multi-series line styles.

```text
  Y ▲                      Smooth Spline (smooth=True)
    │           ●─────●
    │         ╱         ╲
    │   ●───●             ●
    │ ╱
    └────────────────────────► X
       Jan  Feb  Mar  Apr  May
```

### 4.2 Constructor Parameters
| Parameter | Type | Default | Description |
|---|---|---|---|
| `categories` | `list[str]` | Required | Category labels along horizontal axis. |
| `width` / `height` | `float` | `80.0` / `50.0` | Bounding dimensions on the canvas. |
| `title` | `str` | `""` | Title text displayed at top of chart. |
| `show_points` | `bool` | `True` | Whether to draw marker points at vertex coordinates. |
| `point_shape` | `"circle"` \| `"square"` \| `"none"` | `"circle"` | Shape of vertex markers. |
| `point_size` | `float` | `0.7` | Marker radius or half-width. |
| `smooth` | `bool` | `False` | When True, uses smooth interpolated spline curve rendering. |
| `legend_position` | `LegendPosition` | `"auto"` | Position of the legend box. |
| `show_values` | `bool` | `False` | Whether to print numerical values above markers. |

### 4.3 Methods & Data Model
- `add_series(name: str, values: list[float], color=None, style=None, line_width=2.0, line_style="solid", point_shape=None, point_size=None) -> LineSeries`
- `configure_y_axis(...) -> Axis`: Configures vertical value axis scale, ticks, and gridlines.
- `configure_x_axis(...) -> Axis`: Configures horizontal category axis line and labels.
- `draw(xy=(0.0, 0.0))`: Renders chart on canvas.

`LineSeries` captures `name`, `values`, `color`, `style`, `line_width`, `line_style`, `point_shape`, and `point_size`.

### 4.4 Production Examples

#### Example 4.4.1: Multi-Series Active Users Comparison
```drawlib show-code
from drawlib import canvas
from drawlib.charts import LineChart

canvas.initialize()
canvas.config(width=100, height=80)

chart = LineChart(
    categories=["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    width=80.0,
    height=55.0,
    title="Platform MAU Growth (2025 vs 2026)",
    show_points=True,
    point_size=1.0,
    show_values=True,
    legend_position="top",
)
chart.add_series("2025 Baseline", [120.0, 140.0, 175.0, 210.0, 260.0, 310.0], line_style="dashed")
chart.add_series("2026 Accelerated", [150.0, 195.0, 270.0, 380.0, 520.0, 690.0], line_width=2.5)
chart.configure_y_axis(unit="k", label="Active Users (Thousands)", show_grid=True)
chart.draw(xy=(10.0, 15.0))
```

#### Example 4.4.2: Smooth Spline CPU Load with Custom Markers
```drawlib show-code
from drawlib import canvas
from drawlib.charts import LineChart

canvas.initialize()
canvas.config(width=100, height=75)

chart = LineChart(
    categories=["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"],
    width=80.0,
    height=50.0,
    title="Kubernetes Node CPU Load Average",
    smooth=True,
    show_points=True,
    point_shape="square",
    point_size=0.8,
)
chart.add_series("Node-A (Primary)", [22.0, 18.0, 65.0, 88.0, 74.0, 40.0])
chart.add_series("Node-B (Replica)", [15.0, 12.0, 42.0, 60.0, 52.0, 28.0], line_style="dotted")
chart.configure_y_axis(min_value=0.0, max_value=100.0, tick_step=25.0, unit="%", show_grid=True)
chart.draw(xy=(10.0, 15.0))
```

---

## 5. AreaChart: Stacked and Overlapping Volumes

### 5.1 Conceptual Overview
`AreaChart` communicates quantitative volume and stream contributions over time through shaded geometric polygons anchored to the base baseline ($Y=0$). It supports two structural modes:
1. **`mode="overlap"`**: Overlapping semi-transparent area polygons where each series begins at the baseline.
2. **`mode="stack"`**: Cumulative stacked areas where each layer rests on top of the preceding series.

```text
      mode="overlap" (Semi-transparent)           mode="stack" (Cumulative)
  Y ▲                                         Y ▲
    │        ▲                                  │         ▲ Layer 2
    │       ╱ █╲    ▲                           │        ╱█╲
    │     ▲╱  █ ╲  ╱ ╲                          │      ▲╱███╲
    │    ╱ █  █  ╲╱   ╲                         │     ╱██████╲ Layer 1
    └───┴──┴──┴───┴────┴──► X                   └────┴────────┴────► X
```

### 5.2 Constructor Parameters
| Parameter | Type | Default | Description |
|---|---|---|---|
| `categories` | `list[str]` | Required | Category labels along horizontal axis. |
| `width` / `height` | `float` | `80.0` / `50.0` | Total chart bounding dimensions. |
| `title` | `str` | `""` | Chart title displayed at the top. |
| `mode` | `"overlap"` \| `"stack"` | `"overlap"` | Area composition mode. |
| `fill_alpha` | `float` | `0.35` | Global transparency opacity for area fill polygons (0.0 to 1.0). |
| `show_points` | `bool` | `False` | Whether to render markers along top boundary contour. |
| `point_shape` | `"circle"` \| `"square"` \| `"none"` | `"none"` | Marker shape at vertices. |
| `point_size` | `float` | `1.0` | Size of point markers. |
| `smooth` | `bool` | `False` | Whether boundary lines follow smooth curves. |
| `legend_position` | `LegendPosition` | `"auto"` | Position of the legend box. |

### 5.3 Methods & Data Model
- `add_series(name: str, values: list[float], color=None, style=None, fill_alpha=None, line_width=2.0, line_style="solid", point_shape=None, point_size=None) -> AreaSeries`
- `configure_y_axis(...) -> Axis`: Configures vertical value axis scale, ticks, and gridlines.
- `configure_x_axis(...) -> Axis`: Configures horizontal category axis line and labels.
- `draw(xy=(0.0, 0.0))`: Renders chart on canvas.

`AreaSeries` tracks `name`, `values`, `color`, `style`, `fill_alpha`, `line_width`, `line_style`, `point_shape`, and `point_size`.

### 5.4 Production Examples

#### Example 5.4.1: Cumulative Stacked Revenue Streams
```drawlib show-code
from drawlib import canvas
from drawlib.charts import AreaChart

canvas.initialize()
canvas.config(width=100, height=80)

chart = AreaChart(
    categories=["2021", "2022", "2023", "2024", "2025"],
    width=80.0,
    height=55.0,
    title="Cumulative Revenue Streams",
    mode="stack",
    fill_alpha=0.65,
    legend_position="top",
)
chart.add_series("Enterprise Cloud", [40.0, 70.0, 110.0, 160.0, 225.0])
chart.add_series("SaaS Products", [25.0, 38.0, 52.0, 68.0, 85.0])
chart.add_series("Support & Advisory", [15.0, 18.0, 22.0, 24.0, 26.0])
chart.configure_y_axis(unit="M$", label="Gross Revenue (USD Millions)", show_grid=True)
chart.draw(xy=(10.0, 15.0))
```

#### Example 5.4.2: Overlapping Network Bandwidth with Custom Alpha
```drawlib show-code
from drawlib import canvas
from drawlib.charts import AreaChart

canvas.initialize()
canvas.config(width=100, height=75)

chart = AreaChart(
    categories=["02:00", "06:00", "10:00", "14:00", "18:00", "22:00"],
    width=80.0,
    height=50.0,
    title="Ingress vs Egress Gateway Traffic",
    mode="overlap",
    fill_alpha=0.35,
    show_points=True,
    point_shape="circle",
    point_size=0.6,
)
chart.add_series("Ingress Traffic", [120.0, 180.0, 650.0, 920.0, 780.0, 310.0])
chart.add_series("Egress Traffic", [80.0, 110.0, 420.0, 610.0, 530.0, 220.0])
chart.configure_y_axis(unit="Gbps", show_grid=True)
chart.draw(xy=(10.0, 15.0))
```

---

## 6. PieChart: Proportional Sectors and Donut Badges

### 6.1 Conceptual Overview
`PieChart` visualizes proportional compositions where slices represent parts of a whole ($100\%$). It supports classic solid pie charts, donut rings with center KPI text badges, outward slice explosions, and clockwise or counter-clockwise progressions.

```text
        Standard Pie                            Donut with Center KPI
           12 o'clock                                 12 o'clock
              ▲                                          ▲
          . - ~ - .                                  . - ~ - .
      . '    |    ' .                            . '    |    ' .
    /        |  45%   \                        /    ┌───────┐    \
   |  35%    |         |                      |     │ $250M │     |
   |         |         |                      |     │ Total │     |
    \        |        /                        \    └───────┘    /
      . '    |    ' .                            . '    |    ' .
          ' - ~ - '                                  ' - ~ - '
```

### 6.2 Constructor Parameters
| Parameter | Type | Default | Description |
|---|---|---|---|
| `radius` | `float` | `20.0` | Outer radius of the pie circle in canvas units. |
| `title` | `str` | `""` | Chart title displayed at the top. |
| `hole_ratio` | `float` | `0.0` | Inner hole ratio (0.0 for solid pie; 0.1 to 0.9 for donut ring). |
| `center_text` | `str` | `""` | Text rendered in center hole of donut (supports `\n`). |
| `start_angle` | `float` | `90.0` | Initial starting radial angle in degrees (90.0 is 12 o'clock). |
| `clockwise` | `bool` | `True` | Whether slices are ordered clockwise. |
| `show_values` | `bool` | `True` | Whether to display percentage labels on slices ($\ge 4\%$ share). |
| `value_format` | `FormatterType` | `"{:.1f}%"` | String format or function converting proportional ratio. |
| `legend_position` | `LegendPosition` | `"right"` | Legend box placement (`"right"`, `"bottom"`, `"top"`, `"none"`). |
| `width` / `height` | `float \| None` | `None` | Optional container dimension overrides. |

### 6.3 Methods & Data Model
- `add_slice(name: str, value: float, color: ColorType | None = None, style: Style | None = None, explode: float = 0.0) -> PieSlice`: Adds a proportional wedge. Setting `explode > 0.0` shifts slice radially outward.
- `get_size() -> tuple[float, float]`: Computes required bounding box dimensions based on radius, title, and legend.
- `draw(xy=(0.0, 0.0))`: Renders chart on canvas.

`PieSlice` encapsulates `name: str`, `value: float`, `color: ColorType | None`, `style: Style | None`, and `explode: float`.

### 6.4 Production Examples

#### Example 6.4.1: Donut Chart with Center Metric
```drawlib show-code
from drawlib import canvas
from drawlib.charts import PieChart

canvas.initialize()
canvas.config(width=95, height=75)

chart = PieChart(
    radius=26.0,
    hole_ratio=0.62,
    center_text="$1.2B\nARR",
    title="Revenue Contribution by Product Line",
    legend_position="right",
)
chart.add_slice("Cloud Infrastructure", 620.0)
chart.add_slice("AI Developer Tools", 340.0)
chart.add_slice("Security Suite", 180.0)
chart.add_slice("Legacy Support", 60.0)
chart.draw(xy=(10.0, 10.0))
```

#### Example 6.4.2: Exploded Slice Allocation
```drawlib show-code
from drawlib import canvas
from drawlib.charts import PieChart

canvas.initialize()
canvas.config(width=90, height=80)

chart = PieChart(
    radius=25.0,
    title="R&D Budget Allocation (2026)",
    legend_position="bottom",
)
chart.add_slice("Generative AI Models", 48.0, explode=3.0)
chart.add_slice("Core Infrastructure", 24.0)
chart.add_slice("DevOps & Tooling", 16.0)
chart.add_slice("Compliance & Security", 12.0)
chart.draw(xy=(15.0, 10.0))
```

---

## 7. RadarChart: Multivariate Radial Metrics and Spider Webs

### 7.1 Conceptual Overview
`RadarChart` (also known as a spider web or star chart) evaluates multivariate entities across three or more symmetric radial dimensions emanating from a common center origin point. It is widely used for skill matrices, competitive benchmark profiles, and system operational health.

```text
                  Dimension 1
                      ▲
                     ╱ ╲
                    ╱ ● ╲ Series Alpha
                   ╱ ╱ ╲ ╲
     Dimension 5  ●─┼───┼─●  Dimension 2
                  │ │ * │ │
                  │ └───┘ │
                   ╲     ╱
                    ╲   ╱
                     ╲ ╱
                      ▼
                 Dimension 3
```

### 7.2 Constructor Parameters
| Parameter | Type | Default | Description |
|---|---|---|---|
| `categories` | `list[str]` | Required | Names of radial dimensions (minimum 3 required). |
| `radius` | `float` | `25.0` | Radius of the outer boundary spoke circle. |
| `min_value` | `float` | `0.0` | Data value at the central origin point. |
| `max_value` | `float \| None` | `None` | Scale value at outer ring. If None, computed from series. |
| `levels` | `int` | `5` | Number of concentric grid contours. |
| `grid_shape` | `"polygon"` \| `"circle"` | `"polygon"` | Shape of concentric gridlines (regular polygon or circles). |
| `show_grid_labels` | `bool` | `True` | Whether to print numeric scale ticks along reference spoke. |
| `grid_label_format` | `FormatterType` | `None` | Formatter string or function for scale levels. |
| `legend_position` | `LegendPosition` | `"right"` | Position of the legend box. |
| `show_values` | `bool` | `False` | Whether to print numeric data values next to series vertices. |
| `value_format` | `FormatterType` | `None` | Formatter for vertex values. |

### 7.3 Methods & Data Model
- `add_series(name: str, values: list[float], color=None, fill_alpha=0.25, line_width=2.0, line_style="solid", show_points=True, point_shape="circle", point_size=0.8, style=None) -> RadarSeries`
- `get_size() -> tuple[float, float]`: Returns total computed bounding dimensions.
- `draw(xy=(0.0, 0.0))`: Renders radar chart on canvas.

`RadarSeries` maintains `name`, `values`, `color`, `fill_alpha`, `line_width`, `line_style`, `show_points`, `point_shape`, `point_size`, and `style`.

### 7.4 Production Examples

#### Example 7.4.1: Software Architecture Non-Functional Attributes
```drawlib show-code
from drawlib import canvas
from drawlib.charts import RadarChart

canvas.initialize()
canvas.config(width=105, height=88)

chart = RadarChart(
    categories=["Scalability", "Reliability", "Security", "Maintainability", "Latency"],
    radius=24.0,
    min_value=0.0,
    max_value=100.0,
    levels=5,
    grid_shape="polygon",
    title="System Architecture Trade-off Analysis",
    legend_position="right",
    show_values=True,
    value_format="{:.0f}",
)
chart.add_series("Microservices Architecture", [95, 80, 75, 85, 60], fill_alpha=0.3)
chart.add_series("Monolithic Architecture", [60, 90, 85, 70, 95], fill_alpha=0.3, line_style="dashed")
chart.draw(xy=(5.0, 5.0))
```

#### Example 7.4.2: Circular Grid Product Evaluation
```drawlib show-code
from drawlib import canvas
from drawlib.charts import RadarChart

canvas.initialize()
canvas.config(width=95, height=75)

chart = RadarChart(
    categories=["UX Design", "Performance", "Battery Life", "Camera Quality", "Ecosystem", "Price"],
    radius=26.0,
    levels=4,
    grid_shape="circle",
    title="Flagship Smartphone Benchmark",
    legend_position="bottom",
)
chart.add_series("Device Pro Max", [9.2, 9.5, 8.8, 9.6, 9.0, 6.5])
chart.add_series("Device Ultra", [8.5, 9.2, 9.4, 9.2, 8.2, 7.8])
chart.draw(xy=(15.0, 8.0))
```

---

## 8. ScatterChart: X-Y Coordinate Plots and Bubble Charts

### 8.1 Conceptual Overview
`ScatterChart` maps continuous numerical data points across dual independent Cartesian axes ($X$ and $Y$). It is ideal for identifying statistical correlations, clustering patterns, latency vs throughput tradeoffs, and multidimensional bubble analysis (where marker radius encodes a third numerical variable).

```text
  Latency (ms) ▲
           100 │           ● Legacy (High Latency)
            80 │
            60 │                ▲ Competitor
            40 │        ●
            20 │    ● Optimized v2.0
             0 └────────────────────────────► Throughput (req/s)
               0    200   400   600   800
```

### 8.2 Constructor Parameters
| Parameter | Type | Default | Description |
|---|---|---|---|
| `width` / `height` | `float` | `88.0` / `55.0` | Overall container dimensions in canvas units. |
| `title` | `str` | `""` | Chart title displayed at the top. |
| `default_radius` | `float` | `1.0` | Default radius for point markers when unspecified. |
| `default_shape` | `PointShape` | `"circle"` | Default marker shape (`"circle"`, `"square"`, `"rhombus"`, `"triangle"`). |
| `legend_position` | `LegendPosition` | `"auto"` | Location of series legend box. |
| `show_labels` | `bool` | `True` | Whether to display text annotation labels next to points. |

### 8.3 Methods & Data Models
- `add(xy, radius=None, style=None, shape=None, label="", label_style=None) -> ScatterPoint`: Adds an individual standalone point.
- `add_series(name, data, radius=None, style=None, shape=None) -> ScatterSeries`: Adds a named series of `(x, y)` or `(x, y, radius)` points.
- `configure_x_axis(...) -> Axis`: Configures the continuous numerical horizontal axis.
- `configure_y_axis(...) -> Axis`: Configures the continuous numerical vertical axis.
- `get_size() -> tuple[float, float]`: Returns container dimensions.
- `draw(xy)`: Renders scatter chart at bottom-left coordinate `xy`.

`ScatterPoint` represents `xy`, `radius`, `style`, `shape`, and `label`. `ScatterSeries` groups member points under `name`.

### 8.4 Production Examples

#### Example 8.4.1: Benchmark Scatter with Labeled Baseline Points
```drawlib show-code
from drawlib import canvas
from drawlib.charts import ScatterChart
from drawlib.types import Style

canvas.initialize()
canvas.config(width=105, height=75)

chart = ScatterChart(
    width=85.0,
    height=52.0,
    title="Service Throughput vs p99 Latency Benchmark",
)
chart.configure_x_axis(label="Throughput (req/sec)", unit=" rps", min_value=0, max_value=1000)
chart.configure_y_axis(label="p99 Latency (ms)", unit=" ms", min_value=0, max_value=200)

chart.add(xy=(100.0, 18.0), radius=1.6, label="v1.0 Baseline", style=Style(fill_color=(100, 116, 139, 0.9)))
chart.add(xy=(730.0, 35.0), radius=2.2, label="v2.5 Release", style=Style(fill_color=(16, 185, 129, 0.9)))

chart.add_series(
    name="Async Rust Engine",
    data=[(300, 18.0), (500, 19.5), (700, 21.0), (950, 24.0)],
    shape="circle",
)
chart.add_series(
    name="Legacy Threadpool",
    data=[(150, 40.0), (300, 65.0), (450, 110.0), (600, 165.0)],
    shape="square",
)
chart.draw(xy=(10.0, 12.0))
```

#### Example 8.4.2: Multidimensional Cloud Cost Bubble Chart
```drawlib show-code
from drawlib import canvas
from drawlib.charts import ScatterChart

canvas.initialize()
canvas.config(width=105, height=75)

chart = ScatterChart(
    width=85.0,
    height=52.0,
    title="Compute Workload: Duration vs Memory vs Cost (Bubble Size)",
)
chart.configure_x_axis(label="Allocated RAM (GB)", unit=" GB", min_value=0, max_value=32)
chart.configure_y_axis(label="Job Execution Time (sec)", unit=" s", min_value=0, max_value=60)

# 3-Tuples encode (RAM_GB, Execution_Time_Sec, Monthly_Cost_Radius)
chart.add_series(
    name="Serverless Functions",
    data=[(1.0, 48.0, 1.2), (2.0, 28.0, 1.6), (4.0, 16.0, 2.4), (8.0, 10.0, 3.8)],
    shape="circle",
)
chart.add_series(
    name="Dedicated Kubernetes Pods",
    data=[(4.0, 22.0, 2.2), (8.0, 14.0, 3.2), (16.0, 8.5, 4.8), (32.0, 5.0, 6.5)],
    shape="square",
)
chart.draw(xy=(10.0, 15.0))
```

---

## 9. GanttChart: Roadmaps, Schedules, and Dependencies

### 9.1 Conceptual Overview
`GanttChart` provides declarative, vector-grade project roadmaps, sprint schedules, and milestone timelines. Drawing inspiration from sequence diagrams, timeline columns are structured horizontally along the X-axis while task rows, section divider banners, and milestones are sequentially stacked downwards along the Y-axis.

```text
  Task / Milestone         Sprint 1       Sprint 2       Sprint 3       Sprint 4
 ┌──────────────────────┬──────────────┬──────────────┬──────────────┬──────────────┐
 │ ▼ Core Engine        │              │              │              │              │
 │ Database Migration   │ [██████████] │              │              │              │
 │ API Gateway V2       │       └──────┼───────────►[████████]       │              │
 │ ◆ Beta Code Freeze   │              │              │       ◆      │              │
 └──────────────────────┴──────────────┴──────────────┴──────────────┴──────────────┘
                                                       │
                                                Today's Marker
```

### 9.2 Constructor Parameters
| Parameter | Type | Default | Description |
|---|---|---|---|
| `columns` | `list[str]` | Required | Ordered timeline interval labels along horizontal header band. |
| `width` | `float` | `90.0` | Overall chart bounding width. |
| `height` | `float \| None` | `None` | Overall height. If None, calculated dynamically from total row count. |
| `row_height` | `float` | `4.5` | Height per task, milestone, or section row. |
| `header_height` | `float` | `5.5` | Height of the top column header band. |
| `label_width` | `float` | `24.0` | Width allocated for the left task name column. |
| `title` | `str` | `""` | Chart title displayed at the top. |
| `show_vertical_grid` | `bool` | `True` | Whether to draw vertical divider gridlines between columns. |
| `show_zebra` | `bool` | `True` | Whether to alternate row background colors. |
| `bar_radius` | `float` | `0.8` | Corner rounding radius for task bars. |

### 9.3 Methods & Schedule Models
- `add_task(name, start, end, progress=0.0, color=None, style=None, show_progress_text=True) -> GanttTask`
- `add_section(name: str, style: Style | None = None) -> GanttSection`
- `add_milestone(name: str, at: str | float, color=None, style=None) -> GanttMilestone`
- `add_marker(at: str | float, label="", color=None, style=None) -> GanttMarker`
- `add_dependency(from_task: GanttTask, to_task: GanttTask, color=None, style=None) -> GanttDependency`
- `get_size() -> tuple[float, float]`: Returns total computed dimensions.
- `draw(xy=(0.0, 0.0))`: Renders chart on canvas.

Data models include `GanttTask`, `GanttSection`, `GanttMilestone`, `GanttMarker`, and `GanttDependency`.

### 9.4 Production Examples

#### Example 9.4.1: Engineering Release Roadmap with Dependencies
```drawlib show-code
from drawlib import canvas
from drawlib.charts import GanttChart

canvas.initialize()
canvas.config(width=110, height=85)

chart = GanttChart(
    columns=["Apr", "May", "Jun", "Jul", "Aug", "Sep"],
    width=95.0,
    label_width=28.0,
    title="Core Platform Engineering Roadmap (2026)",
    header_height=6.0,
    row_height=5.0,
    bar_radius=1.0,
)

chart.add_section("1. Architecture & Core Services")
t1 = chart.add_task("Spec & Protocol Definition", start="Apr", end=0.8, progress=1.0)
t2 = chart.add_task("Storage Engine Overhaul", start=0.6, end=2.2, progress=0.85)
t3 = chart.add_task("Distributed Consensus Protocol", start=1.5, end=3.2, progress=0.4)

chart.add_section("2. APIs & Observability")
t4 = chart.add_task("gRPC & HTTP/3 Gateway", start=2.5, end=4.0, progress=0.2)
t5 = chart.add_task("Distributed Tracing Exporter", start=3.2, end=4.8, progress=0.0)

chart.add_milestone("Alpha Architecture Freeze", at="Jun")
chart.add_milestone("Public Beta Launch", at=4.0)

chart.add_dependency(t1, t2)
chart.add_dependency(t2, t4)
chart.add_dependency(t3, t4)
chart.add_marker(at=1.7, label="Today (Mid-May)")
chart.draw(xy=(8.0, 10.0))
```

#### Example 9.4.2: Agile Sprint Schedule with Custom Task Colors
```drawlib show-code
from drawlib import canvas
from drawlib.charts import GanttChart

canvas.initialize()
canvas.config(width=100, height=70)

chart = GanttChart(
    columns=["Sprint 1", "Sprint 2", "Sprint 3", "Sprint 4"],
    width=88.0,
    label_width=24.0,
    title="Q3 Core Feature Sprints",
    show_zebra=False,
    bar_radius=1.2,
)

s1 = chart.add_task("Auth Microservice", start=0.0, end=1.8, progress=1.0, color=(59, 130, 246))
s2 = chart.add_task("Payment Gateway", start=1.2, end=3.0, progress=0.6, color=(16, 185, 129))
s3 = chart.add_task("Load Testing & Tuning", start=2.5, end=4.0, progress=0.1, color=(245, 158, 11))

chart.add_dependency(s1, s2)
chart.add_milestone("Feature Complete", at=3.0)
chart.draw(xy=(6.0, 15.0))
```

---

## 10. Styling, Theming, and Typography Reference

### 10.1 Typography Integration with `Font`
Drawlib charts seamlessly inherit typographical settings from Drawlib's font modules (`FontRoboto`, `FontSansSerif`, `FontMonoSpace`, etc.).

```python
from drawlib.fonts import FontRoboto
from drawlib.types import Style

# Configure bold title typography
title_style = Style(
    font=FontRoboto.Bold,
    text_size=18,
    text_color=(30, 41, 59, 1.0),
)

# Configure monospaced numeric tick labels
tick_style = Style(
    font=FontRoboto.Light,
    text_size=10,
    text_color=(100, 116, 139, 1.0),
)
```

### 10.2 Custom Color Themes
You can define coordinated palettes using RGB/RGBA tuples:

```python
# Modern High-Contrast Corporate Palette
PALETTE_CORPORATE = {
    "primary": (15, 23, 42, 1.0),      # Slate Dark
    "accent_blue": (37, 99, 235, 1.0),  # Vivid Blue
    "accent_teal": (13, 148, 136, 1.0), # Teal
    "accent_amber": (217, 119, 6, 1.0), # Amber
    "grid": (226, 232, 240, 0.8),       # Light Slate Divider
}
```

### 10.3 Background and Border Styling
Every chart container accepts an optional `style: Style` argument to apply background fills, drop shadows, or container border outlines:

```python
card_style = Style(
    fill_color=(255, 255, 255, 0.95),
    line_color=(203, 213, 225, 1.0),
    line_width=1.0,
)
chart = BarChart(..., style=card_style)
```

---

## 11. Common Pitfalls, Edge Cases, and Best Practices

### 11.1 Canvas Budgeting & Margins
- **Container Placement**: Remember that `chart.draw(xy=(x, y))` anchors the **bottom-left corner** of the entire chart bounding box.
- **Canvas Sizing**: If your chart width is `80.0` and height is `50.0`, ensure your canvas width and height provide at least 10–15 units of surrounding padding:
  ```python
  canvas.config(width=100.0, height=75.0)
  chart.draw(xy=(10.0, 12.0))
  ```

### 11.2 Handling Non-Positive Values in Logarithmic Scales
- In `scale="log"`, data values $\le 0.0$ cannot be represented mathematically.
- Drawlib's logarithmic engine automatically clamps values to a safe floor ($10^{-6}$), but best practice is to pre-filter or shift input data to strictly positive domains ($> 0.0$).

### 11.3 Minimum Category Rules
- `RadarChart` mathematically requires at least **3 categories** to form a closed polygon. Providing fewer than 3 categories raises a descriptive `ValueError`.
- `GanttChart` requires at least **1 column** in its timeline header.

### 11.4 Slice Proportions and Minimum Label Threshold
- In `PieChart`, text value labels are automatically hidden for slices representing less than $4\%$ of the total sum to prevent unreadable text overlap on narrow wedges. Use `legend_position="right"` to ensure all slice names and quantities remain identifiable.

### 11.5 Gantt Task Time Indexing
- In `GanttChart`, time coordinates can be passed as column string names (`"Apr"`) or floating-point relative offsets (`0.5` = middle of first column). Ensure string names match column definitions exactly to avoid lookup errors.
