# drawlib.charts.area

2D area chart builder supporting semi-transparent overlapping polygons (`mode="overlap"`), cumulative stacked streams (`mode="stack"`), smooth spline contours, and decoupled legends. Import from `drawlib.charts.area` (`from drawlib.charts.area import AreaChart, Axis, Series`).

```drawlib align=center code=fold file=13_charts_area_hero.png caption="Smooth Overlapping and Cumulative Stacked AreaChart Modes"
from drawlib.canvas import save, setup
from drawlib.charts.area import AreaChart
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles

setup(width=120, height=58)

card_style = Styles.Neutral.patch(shape_r=2.0, shape_line_color=Colors.Gray4, shape_fill_color=Colors.White)
rectangle((31.5, 29.0), width=53.0, height=50.0, style=card_style)
rectangle((88.5, 29.0), width=53.0, height=50.0, style=card_style)

# Left: Smooth Overlapping AreaChart (mode="overlap")
overlap = AreaChart(
    axis_line_style=Styles.MutedDashed,
    categories=["00h", "06h", "12h", "18h"],
    width=48.0,
    height=37.0,
    mode="overlap",
    fill_alpha=0.32,
    smooth=True,
    show_points=True,
    point_shape="circle",
    point_size=0.65,
    axis_text_style=Styles.Muted.patch(text_size=10.0),
    grid_style=Styles.MutedThin,
    title="Overlap Traffic (Gbps)",
    title_style=Styles.BlackBold.patch(text_size=11.5),
)
overlap.add_series("Ingress", [14.0, 28.0, 76.0, 44.0], style=Styles.PrimaryFlat, line_width=2.2)
overlap.add_series("Egress", [9.0, 18.0, 48.0, 30.0], style=Styles.SecondaryNeutral, line_width=2.0, line_style="dashed")
overlap.configure_y_axis(min_value=0.0, max_value=90.0, tick_step=45.0)
overlap.draw(xy=(7.5, 13.5))
overlap.draw_legend(xy=(17.0, 8.5), text_style=Styles.DarkBold.patch(text_size=10.0), orientation="horizontal")

# Right: Cumulative Stacked AreaChart (mode="stack")
stacked = AreaChart(
    axis_line_style=Styles.MutedDashed,
    categories=["Q1", "Q2", "Q3", "Q4"],
    width=48.0,
    height=37.0,
    mode="stack",
    fill_alpha=0.68,
    smooth=False,
    axis_text_style=Styles.Muted.patch(text_size=10.0),
    grid_style=Styles.MutedThin,
    title="Stacked Revenue ($M)",
    title_style=Styles.BlackBold.patch(text_size=11.5),
)
stacked.add_series("Cloud", [28.0, 38.0, 52.0, 68.0], style=Styles.PrimaryFlat)
stacked.add_series("SaaS", [16.0, 20.0, 24.0, 28.0], style=Styles.PrimaryNeutral)
stacked.add_series("Ops", [10.0, 12.0, 13.0, 14.0], style=Styles.SecondaryNeutral)
stacked.configure_y_axis(min_value=0.0, max_value=120.0, tick_step=60.0)
stacked.draw(xy=(64.5, 13.5))
stacked.draw_legend(xy=(71.0, 8.5), text_style=Styles.DarkBold.patch(text_size=10.0), orientation="horizontal", item_gap=2.0)

save()
```

---

## `class` AreaChart

2D area chart builder visualizing quantitative volume and stream contributions through shaded polygons anchored to the baseline ($Y = 0$) or stacked cumulatively.

- **Coordinate Anchor**: **Bottom-Left `(x0, y0)`** by default in `draw(xy=..., align="bottom_left")`, or geometric center when `align="center"`.
- **Vertex Value Labels**: Rendered via `y_axis.format_value(v)` when `value_text_style` is provided alongside `show_points=True` and `point_shape != "none"`.

```python
class AreaChart:
    def __init__(
        self,
        *,
        axis_line_style: Style,
        categories: list[str],
        width: float = 80.0,
        height: float = 50.0,
        mode: Mode = "overlap",
        fill_alpha: float = 0.35,
        show_points: bool = False,
        point_shape: PointShape = "none",
        point_size: float = 1.0,
        smooth: bool = False,
        axis_text_style: Style | None = None,
        grid_style: Style | None = None,
        value_text_style: Style | None = None,
        background_style: Style | None = None,
        title: str = "",
        title_style: Style | None = None,
    ) -> None: ...
```

### Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `axis_line_style` | `Style` | **Required** | Mandatory style for the Cartesian axes baseline and ticks. |
| `categories` | `list[str]` | **Required** | Ordered category labels along the horizontal X-axis. |
| `width` | `float` | `80.0` | Total chart bounding box width in canvas units. |
| `height` | `float` | `50.0` | Total chart bounding box height in canvas units. |
| `mode` | `Mode` | `"overlap"` | Area polygon composition mode (`"overlap"` independent from $Y=0$ or `"stack"` cumulative). |
| `fill_alpha` | `float` | `0.35` | Default fill opacity (`0.0` to `1.0`) applied to shaded area polygons. |
| `show_points` | `bool` | `False` | Whether to render vertex markers along the upper boundary contour. |
| `point_shape` | `PointShape` | `"none"` | Default vertex marker shape when `show_points=True` (`"circle"`, `"square"`, `"rhombus"`, `"triangle"`, `"none"`). |
| `point_size` | `float` | `1.0` | Default radius (or half-width) of vertex markers in canvas units. |
| `smooth` | `bool` | `False` | When `True`, upper contours and shaded polygons follow smooth spline curves. |
| `axis_text_style` | `Style \| None` | `None` | Style for Y-axis tick labels and X-axis category names. Omitted when `None`. |
| `grid_style` | `Style \| None` | `None` | Style for horizontal Y-axis gridlines. Omitted when `None`. |
| `value_text_style` | `Style \| None` | `None` | Style for numeric labels drawn above vertex markers. Omitted when `None`. |
| `background_style` | `Style \| None` | `None` | Outer chart background card style. Omitted when `None`. |
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
    fill_alpha: float | None = None,
    line_width: float = 2.0,
    line_style: LineStyle = "solid",
    point_shape: PointShape | None = None,
    point_size: float | None = None,
    legend_text_style: Style | None = None,
    *,
    show: bool = True,
    draw_ratio: float = 1.0,
    draw_direction: DrawDirection = "left_to_right",
) -> Series
```

Adds a new area series to the chart and returns the mutable [Series](#series) instance (`fill_alpha` overrides the chart-level default when not `None`).

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

Configures horizontal X-axis parameters in a single call and returns `x_axis`.

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

Configures vertical Y-axis scale, bounds, ticks, formatters, and labels in a single call and returns `y_axis`.

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

Renders the area chart onto the canvas anchored at `xy` (**Bottom-Left `(x0, y0)`** by default, or geometric center when `align="center"`).

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

Renders a standalone series legend at `xy` (`"vertical"` or `"horizontal"`).

#### `get_size`

```python
def get_size(self) -> tuple[float, float]
```

Returns `(width, height)` of the chart container in canvas units.

#### `series` *(property)*

```python
@property
def series(self) -> list[Series]
```

Returns a list copy of [Series](#series) instances registered with this chart.

---

## `class` Axis

Represents a coordinate axis (value axis or category axis) of an [AreaChart](#areachart), controlling scaling, bounds, ticks, gridlines, and label formatting.

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
| `scale` | `"linear" \| "log"` | `"linear"` | Linear nice-number scaling or base-10 logarithmic (`log10`) scaling. |
| `min_value` | `float \| None` | `None` | Explicit minimum axis domain bound. |
| `max_value` | `float \| None` | `None` | Explicit maximum axis domain bound. |
| `ticks` | `list[float] \| None` | `None` | Explicit tick positions overriding automatic tick generation. |
| `tick_step` | `float \| None` | `None` | Explicit linear interval between ticks. |
| `format` | `FormatterType` | `None` | Format string or callable `Callable[[float], str]` for tick and vertex labels. |
| `unit` | `str` | `""` | Unit suffix appended to formatted tick labels (e.g. `"Gbps"`, `"M$"`). |
| `label` | `str` | `""` | Descriptive axis title text. |
| `show_grid` | `bool` | `True` | Whether to draw gridlines along this axis when chart `grid_style` is set. |
| `grid_style` | `Style \| None` | `None` | Optional per-axis [Style](05_styles_and_types.md) override for gridlines. |
| `show_axis_line` | `bool` | `True` | Whether to draw the axis baseline stroke. |
| `line_style` | `Style \| None` | `None` | Optional per-axis [Style](05_styles_and_types.md) override for the axis baseline. |
| `show_ticks` | `bool` | `True` | Whether to draw tick labels along this axis. |
| `tick_label_style` | `Style \| None` | `None` | Optional per-axis [Style](05_styles_and_types.md) override for tick labels. |
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

Updates multiple axis configuration options in place.

#### `format_value`

```python
def format_value(self, value: float) -> str
```

Formats a numeric `value` into a display label string using `format` and `unit`.

---

## `type` DrawDirection

Spatial partial-rendering direction used with `Series.draw_ratio` (`0.0` to `1.0`) for progressive area chart animations.

```python
DrawDirection = Literal["bottom_to_top", "left_to_right"]
```

| Literal Value | `AreaChart` Behavior |
| :--- | :--- |
| `"left_to_right"` | Sweeps the shaded area polygon and upper contour continuously from left to right *(default)*. |
| `"bottom_to_top"` | Raises the shaded area polygon and upper contour vertically from the baseline (or lower stack boundary). |

---

## `type` FormatterType

Union type for formatting axis tick labels and vertex annotations (`Axis.format`).

```python
FormatterType = str | Callable[[float], str] | None
```

- **`str`**: Python format string (e.g. `"{:.1f}"`, `"${:,.0f}"`).
- **`Callable[[float], str]`**: Custom formatter callable accepting a `float` and returning a `str`.
- **`None`**: Automatic compact numeric formatting.

---

## `type` LegendPosition

Literal type representing preset legend placement identifiers.

```python
LegendPosition = Literal["top", "bottom", "right", "none", "auto"]
```

- Note: `AreaChart` places legends explicitly on the canvas via [`AreaChart.draw_legend()`](#areachart).

---

## `type` Mode

Literal type specifying how multi-series area polygons are layered (`AreaChart.mode`).

```python
Mode = Literal["overlap", "stack"]
```

| Literal Value | Description |
| :--- | :--- |
| `"overlap"` | Anchors every series independently to the baseline ($Y = 0$) with semi-transparent overlap *(default)*. |
| `"stack"` | Layers each series cumulatively on top of preceding series to visualize aggregate volume. |

---

## `class` Series

Mutable data model representing a registered area series in an [AreaChart](#areachart).

```python
class Series:
    def __init__(
        self,
        name: str,
        values: list[float],
        style: Style,
        fill_alpha: float | None = None,
        line_width: float = 2.0,
        line_style: LineStyle = "solid",
        point_shape: PointShape = "none",
        point_size: float = 1.0,
        legend_text_style: Style | None = None,
        *,
        show: bool = True,
        draw_ratio: float = 1.0,
        draw_direction: DrawDirection = "left_to_right",
    ) -> None: ...
```

### Parameters & Attributes

| Parameter / Attribute | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `name` | `str` | **Required** | Series display name shown in `draw_legend()`. |
| `values` | `list[float]` | **Required** | Numeric values aligned with `AreaChart.categories`. |
| `style` | `Style` | **Required** | Fill and upper contour [Style](05_styles_and_types.md). |
| `fill_alpha` | `float \| None` | `None` | Per-series polygon fill opacity override (`None` inherits `AreaChart.fill_alpha`). |
| `line_width` | `float` | `2.0` | Stroke width of the upper boundary contour line. |
| `line_style` | `"solid" \| "dashed" \| "dotted" \| "dashdot"` | `"solid"` | Stroke dash pattern of the upper boundary contour line. |
| `point_shape` | `"circle" \| "square" \| "rhombus" \| "triangle" \| "none"` | `"none"` | Marker geometry at data vertices when `show_points=True`. |
| `point_size` | `float` | `1.0` | Marker radius (or half-width) in canvas units. |
| `legend_text_style` | `Style \| None` | `None` | Optional custom text style for this series in `draw_legend()`. |
| `show` | `bool` | `True` | Toggles visibility while preserving full-dataset axis domain bounds. |
| `draw_ratio` | `float` | `1.0` | Spatial rendering progress (`0.0` to `1.0`) for animations. |
| `draw_direction` | `DrawDirection` | `"left_to_right"` | Partial rendering direction (`"left_to_right"` or `"bottom_to_top"`). |
