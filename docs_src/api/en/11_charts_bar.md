# drawlib.charts.bar

Vertical column and horizontal bar chart builder supporting grouped clusters, cumulative stacks, outer-tip corner rounding, orientation-aware axes, and decoupled legends. Import from `drawlib.charts.bar` (`from drawlib.charts.bar import Axis, BarChart, Series`).

```drawlib align=center code=fold file=11_charts_bar_hero.png caption="Vertical Grouped and Horizontal Stacked BarChart Layouts"
from drawlib.canvas import save, setup
from drawlib.charts.bar import BarChart
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles

setup(width=120, height=58)

card_style = Styles.Neutral.patch(shape_r=2.0, shape_line_color=Colors.Gray4, shape_fill_color=Colors.White)
rectangle((31.5, 29.0), width=53.0, height=50.0, style=card_style)
rectangle((88.5, 29.0), width=53.0, height=50.0, style=card_style)

# Left: Vertical Grouped BarChart
v_bar = BarChart(
    axis_line_style=Styles.MutedDashed,
    categories=["Q1", "Q2", "Q3", "Q4"],
    width=48.0,
    height=37.0,
    orientation="vertical",
    bar_mode="group",
    bar_width_ratio=0.72,
    bar_r=0.8,
    axis_text_style=Styles.Muted.patch(text_size=10.0),
    grid_style=Styles.MutedThin,
    title="Vertical Grouped ($M)",
    title_style=Styles.BlackBold.patch(text_size=11.5),
)
v_bar.add_series("2025", [22.0, 28.0, 32.0, 38.0], style=Styles.SecondaryNeutral)
v_bar.add_series("2026", [30.0, 41.0, 48.0, 58.0], style=Styles.PrimaryFlat)
v_bar.draw(xy=(7.5, 13.5))
v_bar.draw_legend(xy=(19.5, 8.5), text_style=Styles.DarkBold.patch(text_size=10.0), orientation="horizontal")

# Right: Horizontal Stacked BarChart
h_bar = BarChart(
    axis_line_style=Styles.MutedDashed,
    categories=["Cache", "API", "DB"],
    width=48.0,
    height=37.0,
    orientation="horizontal",
    bar_mode="stack",
    bar_width_ratio=0.62,
    bar_r=0.8,
    axis_text_style=Styles.Muted.patch(text_size=10.0),
    grid_style=Styles.MutedThin,
    title="Horizontal Stacked (%)",
    title_style=Styles.BlackBold.patch(text_size=11.5),
)
h_bar.add_series("CPU", [35.0, 46.0, 50.0], style=Styles.PrimaryFlat)
h_bar.add_series("RAM", [30.0, 26.0, 28.0], style=Styles.PrimaryNeutral)
h_bar.add_series("I/O", [15.0, 16.0, 14.0], style=Styles.SecondaryNeutral)
h_bar.configure_x_axis(min_value=0.0, max_value=100.0, tick_step=50.0, unit="%")
h_bar.draw(xy=(64.5, 13.5))
h_bar.draw_legend(xy=(72.5, 8.5), text_style=Styles.DarkBold.patch(text_size=10.0), orientation="horizontal", item_gap=2.2)

save()
```

---

## `class` Axis

Represents a Cartesian coordinate axis (numerical value axis or categorical axis) shared across [BarChart](#barchart), [LineChart](12_charts_line.md), [AreaChart](13_charts_area.md), and [ScatterChart](16_charts_scatter.md). Controls linear or logarithmic scaling, domain bounds, tick generation, gridline visibility, and tick value formatting.

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

### Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `scale` | `"linear" \| "log"` | `"linear"` | Nice-numbers linear scaling or base-10 logarithmic (`log10`) scaling. |
| `min_value` | `float \| None` | `None` | Explicit minimum axis domain bound. Auto-computed when `None`. |
| `max_value` | `float \| None` | `None` | Explicit maximum axis domain bound. Auto-computed when `None`. |
| `ticks` | `list[float] \| None` | `None` | Explicit tick positions overriding automatic tick generation. |
| `tick_step` | `float \| None` | `None` | Explicit linear interval step between adjacent ticks. |
| `format` | `FormatterType` | `None` | Format string (e.g. `"{:.1f}%"`, `"${:,.0f}"`) or callable `Callable[[float], str]` for tick labels. |
| `unit` | `str` | `""` | Unit suffix appended to formatted tick labels if not already present (e.g. `"ms"`, `"%"`). |
| `label` | `str` | `""` | Descriptive axis title text. |
| `show_grid` | `bool` | `True` | Whether to render gridlines along this axis when chart `grid_style` is set. |
| `grid_style` | `Style \| None` | `None` | Optional per-axis [Style](05_styles_and_types.md) override for gridlines. |
| `show_axis_line` | `bool` | `True` | Whether to render the axis baseline stroke. |
| `line_style` | `Style \| None` | `None` | Optional per-axis [Style](05_styles_and_types.md) override for the axis baseline. |
| `show_ticks` | `bool` | `True` | Whether to render tick labels along this axis. |
| `tick_label_style` | `Style \| None` | `None` | Optional per-axis [Style](05_styles_and_types.md) override for tick labels (use `text_angle` for rotated labels). |
| `label_style` | `Style \| None` | `None` | Optional [Style](05_styles_and_types.md) override for the axis `label` title. |

### Methods

#### `configure`

```python
def configure(
    self,
    scale: ScaleType | None = None,
    min_value: float | None = None,
    max_value: float | None = None,
    ticks: list[float] | None = None,
    tick_step: float | None = None,
    format: FormatterType = None,
    unit: str | None = None,
    label: str | None = None,
    show_grid: bool | None = None,
    grid_style: Style | None = None,
    show_axis_line: bool | None = None,
    line_style: Style | None = None,
    show_ticks: bool | None = None,
    tick_label_style: Style | None = None,
    label_style: Style | None = None,
) -> None
```

Updates any non-`None` axis configuration attributes in place.

#### `format_value`

```python
def format_value(self, value: float) -> str
```

Formats `value` into a display string using `format` (string template, callable, or compact numeric default) and appends `unit` when configured.

---

## `class` BarChart

Configurable container and fluent builder for vertical column and horizontal bar charts.

- **Coordinate Anchor**: **Bottom-Left `(x0, y0)`** by default in `draw(xy=..., align="bottom_left")`, or geometric center when `align="center"`.

```python
class BarChart:
    def __init__(
        self,
        *,
        axis_line_style: Style,
        width: float = 60.0,
        height: float = 40.0,
        categories: list[str] | None = None,
        orientation: Orientation = "vertical",
        bar_mode: Mode = "group",
        bar_width_ratio: float = 0.7,
        bar_r: float = 0.0,
        axis_text_style: Style | None = None,
        grid_style: Style | None = None,
        value_text_style: Style | None = None,
        value_format: FormatterType = None,
        background_style: Style | None = None,
        title: str = "",
        title_style: Style | None = None,
    ) -> None: ...
```

### Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `axis_line_style` | `Style` | **Required** | Mandatory style for the Cartesian axes baseline and ticks. |
| `width` | `float` | `60.0` | Total chart bounding box width in canvas units. |
| `height` | `float` | `40.0` | Total chart bounding box height in canvas units. |
| `categories` | `list[str] \| None` | `None` | Category labels along the categorical axis (`x_axis` when vertical, `y_axis` when horizontal). |
| `orientation` | `Orientation` | `"vertical"` | Bar growth direction (`"vertical"` columns or `"horizontal"` bars). |
| `bar_mode` | `Mode` | `"group"` | Series arrangement within each category (`"group"` side-by-side or `"stack"` cumulative). |
| `bar_width_ratio` | `float` | `0.7` | Relative thickness ratio of bars within each category slot (`0.1` to `1.0`). |
| `bar_r` | `float` | `0.0` | Corner rounding radius applied strictly to the 2 outer tip corners of each bar. |
| `axis_text_style` | `Style \| None` | `None` | Style for tick labels and category names. Omitted when `None`. |
| `grid_style` | `Style \| None` | `None` | Style for value-axis gridlines. Omitted when `None`. |
| `value_text_style` | `Style \| None` | `None` | Style for inline numeric labels drawn on bars. Omitted when `None`. |
| `value_format` | `FormatterType` | `None` | Format string (e.g. `"{:.1f}M"`) or callable for inline bar value labels. |
| `background_style` | `Style \| None` | `None` | Outer chart container card style (`shape_fill_color`, `shape_r`). Omitted when `None`. |
| `title` | `str` | `""` | Chart title text displayed at the top of the container. |
| `title_style` | `Style \| None` | `None` | Typography style required to render `title`. Omitted when `None`. |

### Methods & Properties

#### `add_series`

```python
def add_series(
    self,
    name: str,
    values: list[float],
    style: Style,
    legend_text_style: Style | None = None,
    *,
    show: bool = True,
    draw_ratio: float = 1.0,
    draw_direction: DrawDirection | None = None,
) -> Series
```

Registers a data series and returns the mutable [Series](#series) instance. When `draw_direction` is `None`, defaults to `"bottom_to_top"` for vertical charts and `"left_to_right"` for horizontal charts.

#### `category_axis` *(property)*

```python
@property
def category_axis(self) -> Axis
```

Orientation-aware property returning the categorical [Axis](#axis) (`x_axis` when `orientation="vertical"`, `y_axis` when `orientation="horizontal"`).

#### `configure_x_axis`

```python
def configure_x_axis(
    self,
    scale: ScaleType | None = None,
    min_value: float | None = None,
    max_value: float | None = None,
    ticks: list[float] | None = None,
    tick_step: float | None = None,
    format: FormatterType = None,
    unit: str | None = None,
    label: str | None = None,
    show_grid: bool | None = None,
    grid_style: Style | None = None,
    show_axis_line: bool | None = None,
    line_style: Style | None = None,
    show_ticks: bool | None = None,
    tick_label_style: Style | None = None,
) -> Axis
```

Configures horizontal X-axis parameters in a single call and returns the updated [Axis](#axis).

#### `configure_y_axis`

```python
def configure_y_axis(
    self,
    scale: ScaleType | None = None,
    min_value: float | None = None,
    max_value: float | None = None,
    ticks: list[float] | None = None,
    tick_step: float | None = None,
    format: FormatterType = None,
    unit: str | None = None,
    label: str | None = None,
    show_grid: bool | None = None,
    grid_style: Style | None = None,
    show_axis_line: bool | None = None,
    line_style: Style | None = None,
    show_ticks: bool | None = None,
    tick_label_style: Style | None = None,
) -> Axis
```

Configures vertical Y-axis parameters in a single call and returns the updated [Axis](#axis).

#### `draw`

```python
def draw(
    self,
    xy: tuple[float, float] = (0.0, 0.0),
    *,
    width: float | None = None,
    height: float | None = None,
    align: Literal["bottom_left", "center"] = "bottom_left",
    scale: float = 1.0,
) -> None
```

Renders the bar chart onto the canvas anchored at `xy` (**Bottom-Left `(x0, y0)`** when `align="bottom_left"`, or geometric center when `align="center"`), with optional temporary dimension overrides and uniform proportional `scale`.

#### `draw_legend`

```python
def draw_legend(
    self,
    xy: tuple[float, float],
    text_style: Style,
    orientation: Orientation = "vertical",
    swatch_width: float = 2.4,
    swatch_height: float = 1.2,
    item_gap: float = 4.0,
    *,
    scale: float = 1.0,
) -> None
```

Renders a standalone series legend at `xy` (top-left start when `"vertical"`, middle-left start when `"horizontal"`). Hidden series (`show=False`) are automatically excluded.

#### `get_size`

```python
def get_size(self) -> tuple[float, float]
```

Returns `(width, height)` of the unscaled chart container in canvas units.

#### `series` *(property)*

```python
@property
def series(self) -> list[Series]
```

Returns a list copy of registered [Series](#series) instances.

#### `value_axis` *(property)*

```python
@property
def value_axis(self) -> Axis
```

Orientation-aware property returning the numerical value [Axis](#axis) (`y_axis` when `orientation="vertical"`, `x_axis` when `orientation="horizontal"`).

---

## `type` DrawDirection

Spatial partial-rendering direction used with `draw_ratio` (`0.0` to `1.0`) for progressive chart animations.

```python
DrawDirection = Literal["bottom_to_top", "left_to_right"]
```

| Literal Value | Vertical `BarChart` Behavior | Horizontal `BarChart` Behavior |
| :--- | :--- | :--- |
| `"bottom_to_top"` | All bars grow upward from the baseline (`v * draw_ratio`). | Bars reveal sequentially category-by-category from bottom to top. |
| `"left_to_right"` | Bars reveal sequentially category-by-category from left to right. | All bars grow rightward from the baseline (`v * draw_ratio`). |

---

## `type` FormatterType

Union type controlling numeric formatting for axis ticks (`Axis.format`) and inline bar labels (`BarChart.value_format`).

```python
FormatterType = str | Callable[[float], str] | None
```

- **`str`**: Standard Python format specification or template string (e.g. `"{:.1f}M"`, `"${:,.0f}"`, `"{:.0f}%"`).
- **`Callable[[float], str]`**: Custom formatter function mapping a numeric `float` value to a display string.
- **`None`**: Uses Drawlib's automatic compact number formatting.

---

## `type` LegendPosition

Literal type representing preset legend placement identifiers for chart layout helpers.

```python
LegendPosition = Literal["top", "bottom", "right", "none", "auto"]
```

- Note: `BarChart` renders legends at explicit canvas coordinates via [`BarChart.draw_legend()`](#barchart) for full dashboard layout control.

---

## `type` Mode

Literal type specifying how multi-series bars are arranged within each category slot (`BarChart.bar_mode`).

```python
Mode = Literal["group", "stack"]
```

| Literal Value | Description |
| :--- | :--- |
| `"group"` | Places series bars side-by-side in clustered groups within each category slot *(default)*. |
| `"stack"` | Stacks series bars cumulatively to show aggregate totals and part-to-whole composition. |

---

## `type` Orientation

Literal type specifying the primary direction of chart bars (`BarChart.orientation`) or legend item flow (`draw_legend`).

```python
Orientation = Literal["vertical", "horizontal"]
```

| Literal Value | Description |
| :--- | :--- |
| `"vertical"` | Columns grow vertically upward along `y_axis`; legend items stack top-to-bottom. |
| `"horizontal"` | Bars grow horizontally rightward along `x_axis`; legend items flow left-to-right. |

---

## `class` Series

Mutable data model representing a single registered data series in a [BarChart](#barchart).

```python
class Series:
    def __init__(
        self,
        name: str,
        values: list[float],
        style: Style,
        legend_text_style: Style | None = None,
        *,
        show: bool = True,
        draw_ratio: float = 1.0,
        draw_direction: DrawDirection = "bottom_to_top",
    ) -> None: ...
```

### Parameters & Attributes

| Parameter / Attribute | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `name` | `str` | **Required** | Series display name shown in `draw_legend()`. |
| `values` | `list[float]` | **Required** | Numeric values aligned with `BarChart.categories`. |
| `style` | `Style` | **Required** | Fill and stroke [Style](05_styles_and_types.md) applied to bars in this series. |
| `legend_text_style` | `Style \| None` | `None` | Optional per-series text style override in `draw_legend()`. |
| `show` | `bool` | `True` | Toggles series visibility while preserving 100% dataset axis bounds. |
| `draw_ratio` | `float` | `1.0` | Partial rendering progress (`0.0` to `1.0`) for keyframe animations. |
| `draw_direction` | `DrawDirection` | `"bottom_to_top"` | Direction of partial spatial rendering (`"bottom_to_top"` or `"left_to_right"`). |
