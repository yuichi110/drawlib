# Drawlib Charts Overview Guidelines (`lib-charts-overview`)

`drawlib.charts` provides a declarative, pure-Python visualization engine for statistical, comparative, relational, matrix, spatial thermal, and project schedule charts.
Unlike external plotting libraries that produce isolated raster images, Drawlib charts render directly into the Drawlib vector canvas using standard primitives, shapes, text, and styles. This ensures seamless visual and programmatic integration with system architectures, flowcharts, and technical documentation.

---

## 1. Overview & Architecture

### 1.1 Philosophy: Illustration-as-Code for Data
Drawlib charts adhere to four foundational principles:
1. **Canvas Coexistence**: Charts are first-class canvas elements positioned at arbitrary `(x, y)` coordinates. Multiple charts, architecture diagrams, callouts, and icon annotations can share a single canvas.
2. **Deterministic Layout**: Bounding boxes, margins, legend offsets, and tick spacing are computed deterministically from explicit dimensions (`width`, `height`, `radius`), preventing rendering drift.
3. **Pure-Python Data Models**: Series, slices, tasks, rows, cells, and points are defined through clean, strongly-typed data objects (`Series`, `Slice`, `Task`, `Point`, `Row`, `Cell`, `Spot`).
4. **Unified Styling Engine**: All chart elements—bars, area polygons, curves, gridlines, axes, text badges, colorbars, and legends—are styled using Drawlib's `Style`, `Colors`, and `Font` models.

### 1.2 Module Structure & Submodule Exports
All public chart classes, data models, axis configurations, and type literals are organized into 8 dedicated submodules under `drawlib.charts`:

- **`drawlib.charts`**: `DrawDirection`, `area`, `bar`, `gantt`, `heatmap`, `line`, `pie`, `radar`, `scatter`
- **`drawlib.charts.bar`**: `Axis`, `BarChart`, `DrawDirection`, `FormatterType`, `LegendPosition`, `Mode`, `Orientation`, `Series`
- **`drawlib.charts.line`**: `Axis`, `DrawDirection`, `FormatterType`, `LegendPosition`, `LineChart`, `LineStyle`, `PointShape`, `Series`
- **`drawlib.charts.area`**: `AreaChart`, `Axis`, `DrawDirection`, `FormatterType`, `LegendPosition`, `Mode`, `Series`
- **`drawlib.charts.pie`**: `DrawDirection`, `FormatterType`, `PieChart`, `Slice`
- **`drawlib.charts.radar`**: `DrawDirection`, `FormatterType`, `GridShape`, `LegendPosition`, `RadarChart`, `Series`
- **`drawlib.charts.scatter`**: `Axis`, `DrawDirection`, `LegendPosition`, `Point`, `PointShape`, `ScaleType`, `ScatterChart`, `Series`
- **`drawlib.charts.gantt`**: `Dependency`, `DrawDirection`, `GanttChart`, `Marker`, `Milestone`, `Section`, `Task`
- **`drawlib.charts.heatmap`**: `BlendMode`, `Cell`, `DrawDirection`, `FormatterType`, `HeatmapChart`, `HeatmapOverlay`, `Orientation`, `OverlayMode`, `Row`, `Spot`

```python
# Import from dedicated chart submodules (or DrawDirection directly from drawlib.charts)
from drawlib.charts import DrawDirection
from drawlib.charts.bar import Axis, BarChart, FormatterType, LegendPosition, Mode, Orientation, Series
from drawlib.charts.line import Axis, FormatterType, LegendPosition, LineChart, LineStyle, PointShape, Series
from drawlib.charts.area import AreaChart, Axis, FormatterType, LegendPosition, Mode, Series
from drawlib.charts.pie import FormatterType, PieChart, Slice
from drawlib.charts.radar import FormatterType, GridShape, LegendPosition, RadarChart, Series
from drawlib.charts.scatter import Axis, LegendPosition, Point, PointShape, ScaleType, ScatterChart, Series
from drawlib.charts.gantt import Dependency, GanttChart, Marker, Milestone, Section, Task
from drawlib.charts.heatmap import (
    BlendMode,
    Cell,
    FormatterType,
    HeatmapChart,
    HeatmapOverlay,
    Orientation,
    OverlayMode,
    Row,
    Spot,
)
```

### 1.3 Chart Family Taxonomy & Routing Table

```text
┌──────────────────────────────────────────────────────────────────────────────────┐
│                             drawlib.charts Taxonomy                              │
├──────────────────────────┬────────────────────────────┬──────────────────────────┤
│ Categorical & Matrix     │ Continuous & Relational    │ Radial & Temporal        │
├──────────────────────────┼────────────────────────────┼──────────────────────────┤
│ • BarChart (Group/Stack) │ • LineChart (Linear/Spline)│ • PieChart (Pie/Donut)   │
│ • HeatmapChart (2D Grid) │ • AreaChart (Overlap/Stack)│ • RadarChart (Spiderweb) │
│ • HeatmapOverlay (Spot)  │ • ScatterChart (XY/Bubble) │ • GanttChart (Timelines) │
└──────────────────────────┴────────────────────────────┴──────────────────────────┘
```

Query the detailed guidelines and API reference for any specific chart family using `drawlib rules show`:

| Rule Topic | Submodule | Primary Classes | Command |
| :--- | :--- | :--- | :--- |
| **`lib-charts-bar`** | `drawlib.charts.bar` | `BarChart`, `Series`, `Axis` | `uv run drawlib rules show lib-charts-bar` |
| **`lib-charts-line`** | `drawlib.charts.line` | `LineChart`, `Series`, `Axis` | `uv run drawlib rules show lib-charts-line` |
| **`lib-charts-area`** | `drawlib.charts.area` | `AreaChart`, `Series`, `Axis` | `uv run drawlib rules show lib-charts-area` |
| **`lib-charts-pie`** | `drawlib.charts.pie` | `PieChart`, `Slice` | `uv run drawlib rules show lib-charts-pie` |
| **`lib-charts-radar`** | `drawlib.charts.radar` | `RadarChart`, `Series` | `uv run drawlib rules show lib-charts-radar` |
| **`lib-charts-scatter`** | `drawlib.charts.scatter` | `ScatterChart`, `Series`, `Point`, `Axis` | `uv run drawlib rules show lib-charts-scatter` |
| **`lib-charts-gantt`** | `drawlib.charts.gantt` | `GanttChart`, `Section`, `Task`, `Milestone`, `Marker`, `Dependency` | `uv run drawlib rules show lib-charts-gantt` |
| **`lib-charts-heatmap`** | `drawlib.charts.heatmap` | `HeatmapChart`, `Row`, `Cell`, `HeatmapOverlay`, `Spot` | `uv run drawlib rules show lib-charts-heatmap` |

---

## 2. Universal Chart Architecture

### 2.1 Placement Coordinates (`align`), Spatial Overrides, and Proportional Scaling (`scale`)
Every chart class (`BarChart`, `LineChart`, `AreaChart`, `PieChart`, `RadarChart`, `ScatterChart`, `GanttChart`, `HeatmapChart`, `HeatmapOverlay`) implements a unified positioning, sizing override, and uniform scaling contract:

```python
chart.draw(
    xy: tuple[float, float] = (0.0, 0.0),
    *,
    width: float | None = None,
    height: float | None = None,
    # radius: float | None = None,  # Supported on PieChart and RadarChart
    align: Literal["bottom_left", "center"] = "bottom_left",
    scale: float = 1.0,
) -> None
```

- **Coordinate Anchor (`align: Literal["bottom_left", "center"] = "bottom_left"`)**:
  - When `align="bottom_left"` *(default)*, `xy` defines the **bottom-left corner** of the chart's total bounding container (including margins and titles).
  - When `align="center"`, `xy` defines the **geometric center** of the chart's total bounding box `(width, height)`.
- **Temporary Dimension Overrides (`width`, `height`, `radius`)**:
  - Passing `width`, `height`, or `radius` (on `PieChart` / `RadarChart`) temporarily overrides the layout dimensions for that `draw()` call without permanently mutating the chart instance.
- **Proportional Scaling (`scale: float = 1.0`)**:
  - Passing `scale != 1.0` applies a uniform proportional canvas transformation anchored at `xy`, scaling all plot geometry, stroke widths, marker radii, and font sizes together.
- **Bounding Box Inspection (`get_size() -> tuple[float, float]`)**:
  - Returns `(width, height)` representing the unscaled total bounding box dimensions in canvas units. (`HeatmapOverlay` also provides `get_bounds() -> tuple[float, float, float, float]`).

```text
   (x, y + height) ┌──────────────────────────────────────┐
                   │ Chart Title                          │
                   │   ┌──────────────────────────────┐   │
                   │   │ Data Plotting Area           │   │
                   │   │        (cx, cy)              │   │
                   │   │    align="center"            │   │
                   │   └──────────────────────────────┘   │
                   │       Axis Labels / Ticks            │
   (x, y)          └──────────────────────────────────────┘ (x + width, y)
   align="bottom_left" (default)
```

### 2.2 The Axis System (`Axis`, `configure_x_axis`, `configure_y_axis`)
Cartesian charts (`BarChart`, `LineChart`, `AreaChart`, `ScatterChart`) use the `Axis` model (`drawlib._charts._common._axis.Axis`) to control coordinate mapping, linear/logarithmic scaling, gridline/baseline/tick visibility, and label formatting.

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
        label_style: Style | None = None,
    ) -> None: ...
```

Axes are configured via `chart.configure_x_axis(...)` and `chart.configure_y_axis(...)` (which call `axis.configure(...)` in place and return the `Axis` instance):

```python
chart.configure_y_axis(
    scale: ScaleType | None = None,            # "linear" | "log"
    min_value: float | None = None,            # Explicit minimum axis bound
    max_value: float | None = None,            # Explicit maximum axis bound
    ticks: list[float] | None = None,          # Explicit tick positions override
    tick_step: float | None = None,            # Explicit linear step between ticks
    format: FormatterType = None,              # Tick label format (e.g. "{:.1f}%", "${:,.0f}", or callable)
    unit: str | None = None,                   # Unit suffix appended to tick labels (e.g. "ms", "Gbps")
    label: str | None = None,                  # Descriptive axis title
    show_grid: bool | None = None,             # Toggle gridlines along this axis
    grid_style: Style | None = None,           # Per-axis gridline Style override
    show_axis_line: bool | None = None,        # Toggle baseline stroke for this axis
    line_style: Style | None = None,           # Per-axis baseline stroke Style override
    show_ticks: bool | None = None,            # Toggle tick labels along this axis
    tick_label_style: Style | None = None,     # Per-axis tick label Style (font, size, color, rotation)
) -> Axis
```

| Axis Parameter / Property | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `scale` | `"linear"` \| `"log"` | `"linear"` | **Nice Numbers** linear scaling ($1, 2, 5 \times 10^k$) or base-10 logarithmic ($\log_{10}$) scaling. |
| `min_value` / `max_value` | `float \| None` | `None` | Explicit minimum and maximum axis domain bounds. |
| `tick_step` | `float \| None` | `None` | Explicit step interval between linear ticks. |
| `ticks` | `list[float] \| None` | `None` | Explicit list of tick values (overrides automatic tick generation). |
| `format` *(tick label format)* | `FormatterType` | `None` | Format string (`"{:.1f}%"`, `"${:,.0f}"`) or callable `Callable[[float], str]` used by `axis.format_value(v)` (do not pass `tick_label_format`; the parameter name is `format`). |
| `unit` | `str` | `""` | Unit suffix automatically appended to formatted tick labels if not already present. |
| `label` / `label_style` | `str` / `Style \| None` | `""` / `None` | Descriptive axis title and optional typography override (`axis.configure(label_style=...)` or `chart.y_axis.label_style = ...`). |
| `show_grid` / `grid_style` | `bool` / `Style \| None` | `True` / `None` | Whether to render gridlines for this axis and optional per-axis gridline `Style` override. |
| `show_axis_line` / `line_style` | `bool` / `Style \| None` | `True` / `None` | Whether to render the axis baseline stroke and optional per-axis baseline `Style` override. |
| `show_ticks` / `tick_label_style` | `bool` / `Style \| None` | `True` / `None` | Whether to render tick labels and optional per-axis `Style` override (for tick label rotation, set `text_angle` on `tick_label_style` or `axis_text_style`; there is no separate `tick_label_rotation` argument). |

- **Direct Axis Property Access**:
  - `chart.x_axis` and `chart.y_axis` on `BarChart`, `LineChart`, `AreaChart`, and `ScatterChart`.
  - `bar_chart.value_axis` (`y_axis` when vertical, `x_axis` when horizontal) and `bar_chart.category_axis` (`x_axis` when vertical, `y_axis` when horizontal).
  - `RadarChart` uses `chart.configure_axis(*, min_value=None, max_value=None, levels=None, scale_format=None) -> RadarChart`.

### 2.3 Decoupled Legend & Colorbar Rendering (`draw_legend`, `draw_colorbar`)
Legends are decoupled from the main chart container and rendered explicitly at any `(x, y)` coordinate:

```python
chart.draw_legend(
    xy: tuple[float, float],
    text_style: Style,
    orientation: Literal["vertical", "horizontal"] = "vertical",
    swatch_width: float = 2.4,
    swatch_height: float = 1.2,
    item_gap: float = 4.0,
    *,
    scale: float = 1.0,
) -> None
```

- **Supported Charts**: `BarChart`, `LineChart`, `AreaChart`, `PieChart`, `RadarChart`, `ScatterChart`, `HeatmapChart`, and `HeatmapOverlay`.
- **Coordinate Anchor `xy`**:
  - For `orientation="vertical"`, `xy` is the **top-left** starting position (items step downward).
  - For `orientation="horizontal"`, `xy` is the **middle-left** starting position (items advance rightward by `item_gap`).
- **Heatmap Legends & Colorbars**:
  - `HeatmapChart` and `HeatmapOverlay` also accept `num_steps: int` and `labels: Sequence[str] | None = None` in `draw_legend(...)`, and provide `draw_colorbar(xy, text_style, *, length=30.0, thickness=2.2, orientation="horizontal", num_ticks=5, value_format=None, label="", border_style=None, scale=1.0)` for continuous gradient bars.

### 2.4 Presence-Based Styling (`Style | None = None`)
Drawlib charts enforce a strict **"No Fallback / Style-as-Presence"** design:
1. **Mandatory Structural Anchor**: `BarChart`, `LineChart`, `AreaChart`, `RadarChart`, `ScatterChart`, and `GanttChart` require `axis_line_style: Style` (`HeatmapChart` and `HeatmapOverlay` require `styles=[Style, ...]` or `min_style` + `max_style`).
2. **Presence-Based Optional Elements**: Any optional style left as `None` completely omits that visual element:
   - `axis_text_style=None`: Tick labels, category names, spoke labels, and row/column headers are omitted.
   - `grid_style=None`: Gridlines, concentric radar rings, and vertical Gantt column dividers are omitted.
   - `value_text_style=None`: Inline numeric labels on bars, vertices, pie slices, cells, and spots are omitted.
   - `title_style=None`: Chart title is omitted even if `title` is non-empty.
   - `background_style=None`: Outer container card is omitted (transparent background).

### 2.5 Animation Support Across All 9 Chart Classes (`show`, `draw_ratio`, `draw_direction`)
All 9 chart classes follow Drawlib's 4-phase component lifecycle (**1. Instantiate -> 2. Register Elements -> 3. Mutate State -> 4. Render**), enabling smooth keyframe animations and step-by-step slide builds without shifting axis scales or layout geometry:

1. **Element Visibility (`show: bool = True`)**:
   - Supported on every data item across all 9 chart classes: `Series`, `Slice`, `Point`, `Task`, `Section`, `Milestone`, `Marker`, `Dependency`, `Row`, `Cell`, and `Spot`.
   - Setting `elem.show = False` (or `draw_ratio = 0.0`) hides the element (and its legend entry) while **preserving the full 100% dataset's automatic axis bounds, pie total sum, heatmap color range, and Gantt row positions**.
   - In `GanttChart`, hiding a `Task` (`task.show = False` or `task.draw_ratio = 0.0`) automatically hides any connected `Dependency` arrows.
2. **Partial Spatial Rendering (`draw_ratio: float = 1.0`, `draw_direction: DrawDirection`)**:

| Chart Class | Animated Element | Default `draw_direction` | `"bottom_to_top"` Behavior | `"left_to_right"` Behavior |
| :--- | :--- | :--- | :--- | :--- |
| **`BarChart`** | `Series` | `"bottom_to_top"` (`"vertical"`) / `"left_to_right"` (`"horizontal"`) | Vertical: all bars grow upward from baseline (`v * r`). Horizontal: bars reveal sequentially from bottom category to top. | Vertical: bars reveal sequentially left-to-right across categories. Horizontal: all bars grow rightward from baseline (`v * r`). |
| **`LineChart`** | `Series` | `"left_to_right"` | All vertices rise simultaneously from baseline toward target `y`. | Curve extends continuously from left to right along arc length; markers appear as reached. |
| **`AreaChart`** | `Series` | `"left_to_right"` | Area polygon and upper contour rise from baseline / lower stack boundary. | Area polygon and upper contour sweep continuously from left to right. |
| **`PieChart`** | `Slice` | `"left_to_right"` | Wedge grows radially outward from inner hole (`hole_ratio`) toward `radius`. | Wedge sweeps angularly from `start_angle` across `sweep_angle * r` (labels appear at `r >= 0.6`). |
| **`RadarChart`** | `Series` | `"bottom_to_top"` | All spoke vertices expand radially outward from center `min_value`. | Polygon sweeps spoke-by-spoke around the perimeter from spoke `0` to `N-1`. |
| **`ScatterChart`** | `Series` | `"left_to_right"` | Points rise from bottom axis toward target `y` while scaling `radius * r`. | Points reveal progressively left-to-right across the X-axis range. |
| **`GanttChart`** | `Task` | `"left_to_right"` | Task bar grows vertically from its bottom edge to full height (`bar_h * r`). | Task bar extends horizontally from `start` toward `start + (end - start) * r`. |
| **`HeatmapChart`** | `Row` | `"left_to_right"` | Cells in the row grow vertically from their bottom edge (`cell_h * r`). | Cells in the row reveal sequentially left-to-right across columns, interpolating the frontier cell width. |
| **`HeatmapOverlay`**| `Spot` | *(Radial intensity/radius)* | Scales hotspot intensity and influence radius by `draw_ratio` (`0.0` to `1.0`). | Scales hotspot intensity and influence radius by `draw_ratio` (`0.0` to `1.0`). |

---

## 3. Styling, Typography & Multi-Chart Dashboards

### 3.1 Typography Best Practices (`text_font` vs. `font`)
Always configure custom fonts on `Style` using `text_font=...` (never `font=...`), and use the exact enum member names on `FontRoboto`, `FontMonoSpace`, or `Font`:

```python
from drawlib.fonts import FontMonoSpace, FontRoboto
from drawlib.styles import Colors, Style, Styles

# CORRECT: Use text_font=FontRoboto.ROBOTO_BOLD (never font=FontRoboto.BOLD)
title_style = Style(
    text_font=FontRoboto.ROBOTO_BOLD,
    text_size=13.0,
    text_color=Colors.Black,
)

# Or patch an existing preset style token:
tick_style = Styles.Muted.patch(
    text_font=FontMonoSpace.ROBOTO_MONO_REGULAR,
    text_size=10.0,
)
```

- **720pt Typography Sizing**: Keep chart `axis_text_style`, `value_text_style`, and `legend` `text_size >= 10.0` (titles `11.5`–`13.5`) so rendered chart labels match prose body text.
- **50%+ Neutral Baseline**: Ground supporting series, slices, and background cards in calm neutral tokens (`Styles.Neutral`, `Styles.PrimaryNeutral`, `Styles.SecondaryNeutral`), reserving `Styles.PrimaryFlat` or `Styles.SecondaryFlat` for primary focal series.

### 3.2 Multi-Chart Dashboard Composition
Because every chart renders at an explicit `xy` coordinate on the shared canvas, you can combine multiple chart families inside framing cards to build executive dashboards:

```drawlib code=show align=center file=charts_overview_dashboard.png caption="Multi-Chart Executive Dashboard Coexisting on a Single Drawlib Canvas"
from drawlib.canvas import save, setup
from drawlib.charts.bar import BarChart
from drawlib.charts.pie import PieChart
from drawlib.charts.radar import RadarChart
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles

setup(width=132, height=54)

card_style = Styles.Neutral.patch(shape_r=2.0, shape_line_color=Colors.Gray4, shape_fill_color=Colors.White)
rectangle((22.5, 27.0), width=40.0, height=46.0, style=card_style)
rectangle((66.0, 27.0), width=40.0, height=46.0, style=card_style)
rectangle((109.5, 27.0), width=40.0, height=46.0, style=card_style)

# 1. Left Card: BarChart
bar = BarChart(
    categories=["Q1", "Q2", "Q3"],
    axis_line_style=Styles.MutedDashed,
    axis_text_style=Styles.Muted.patch(text_size=10.0),
    grid_style=Styles.MutedThin,
    width=36.0,
    height=33.0,
    bar_mode="group",
    bar_r=0.8,
    title="Quarterly Revenue ($M)",
    title_style=Styles.BlackBold.patch(text_size=11.0),
)
bar.add_series("2025", [18.0, 26.0, 32.0], style=Styles.SecondaryNeutral)
bar.add_series("2026", [24.0, 35.0, 44.0], style=Styles.PrimaryFlat)
bar.draw(xy=(4.5, 12.0))
bar.draw_legend(xy=(8.5, 7.8), text_style=Styles.DarkBold.patch(text_size=10.0), orientation="horizontal")

# 2. Center Card: Donut PieChart
pie = PieChart(
    radius=10.5,
    width=36.0,
    height=33.0,
    hole_ratio=0.58,
    center_text="99.9%\nSLA",
    center_text_style=Styles.DarkBold.patch(text_size=10.0),
    title="Traffic Share",
    title_style=Styles.BlackBold.patch(text_size=11.0),
    value_text_style=Styles.BlackBold.patch(text_size=10.0),
    value_format="{:.0f}%",
)
pie.add_slice("Core", 48.0, style=Styles.PrimaryFlat)
pie.add_slice("Edge", 32.0, style=Styles.PrimaryNeutral)
pie.add_slice("Ops", 20.0, style=Styles.SecondaryNeutral)
pie.draw(xy=(48.0, 12.0))
pie.draw_legend(xy=(49.0, 7.8), text_style=Styles.DarkBold.patch(text_size=10.0), orientation="horizontal", item_gap=1.8)

# 3. Right Card: RadarChart
radar = RadarChart(
    categories=["Scale", "Speed", "Sec", "UX", "SLA"],
    axis_line_style=Styles.MutedDashed,
    axis_text_style=Styles.DarkBold.patch(text_size=10.0),
    grid_style=Styles.MutedThin,
    radius=9.2,
    width=36.0,
    height=33.0,
    min_value=0.0,
    max_value=100.0,
    levels=3,
    grid_shape="polygon",
    title="Architecture Health",
    title_style=Styles.BlackBold.patch(text_size=11.0),
)
radar.add_series("Target", [65, 85, 70, 85, 75], style=Styles.SecondaryNeutral, fill_alpha=0.25, line_style="dashed")
radar.add_series("Actual", [90, 78, 88, 76, 95], style=Styles.PrimaryFlat, fill_alpha=0.28)
radar.draw(xy=(91.5, 12.0))
radar.draw_legend(xy=(94.5, 7.8), text_style=Styles.DarkBold.patch(text_size=10.0), orientation="horizontal")

save()
```
