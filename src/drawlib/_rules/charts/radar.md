# Drawlib RadarChart Guidelines (`lib-charts-radar`)

`RadarChart` (`drawlib.charts.radar`, also known as a spider web or star chart) evaluates multivariate entities across three or more symmetric radial dimensions emanating from a common center origin point. It is widely used for skill matrices, competitive benchmark profiles, and system architectural trade-off evaluations.

---

## 1. Conceptual Overview & Imports

```python
from drawlib.charts.radar import (
    DrawDirection,
    FormatterType,
    GridShape,
    LegendPosition,
    RadarChart,
    Series,
)
```

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

- **Minimum 3 Categories Required (`len(categories) >= 3`)**: A closed radial polygon mathematically requires at least 3 spokes; passing fewer than 3 categories raises a `ValueError`.
- **Concentric Grid Contours (`GridShape = Literal["polygon", "circle"]`)**: Rendered when `grid_style` is provided, supporting `grid_shape="polygon"` (straight web segments) or `grid_shape="circle"` (concentric rings) across `levels` rings.
- **Scale & Vertex Labels**: Provide `scale_text_style` and `scale_format` (not `grid_label_format`) to label concentric ring values along the top vertical spoke, and `value_text_style` and `value_format` to label series vertices.
- **Series Vertex Markers (`point_shape`)**: Configured per series in `add_series(..., point_shape="circle" | "square" | "none", point_size=0.8)`. Pass `point_shape="none"` to hide vertex markers on a series (there is no `show_points` parameter).

---

## 2. Constructor Parameters (`RadarChart`)

All constructor arguments are **keyword-only** (`*`):

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| **`categories`** | `list[str]` | **Required** | Names of radial dimensions around the perimeter (**minimum 3 required**). |
| **`axis_line_style`** | `Style` | **Required** | Style for the radial spoke axes lines. Mandatory anchor. |
| `radius` | `float` | `25.0` | Outer radius of the radar web in canvas units. |
| `min_value` | `float` | `0.0` | Baseline data value at the central origin point. |
| `max_value` | `float \| None` | `None` | Scale value at outer ring. If `None`, computed automatically from series values. |
| `levels` | `int` | `5` | Number of concentric grid contours (minimum `1`). |
| `grid_shape` | `"polygon"` \| `"circle"` | `"polygon"` | Shape of concentric gridlines (`GridShape`). |
| `axis_text_style` | `Style \| None` | `None` | Style for outer perimeter dimension category labels. If `None`, category labels are omitted. |
| `grid_style` | `Style \| None` | `None` | Style for concentric grid contours. If `None`, grid rings are omitted. |
| `scale_text_style` | `Style \| None` | `None` | Style for numeric scale labels along the top spoke. If `None`, scale labels are omitted. |
| `scale_format` | `FormatterType` | `None` | Format string or `Callable[[float], str]` for concentric ring scale levels. |
| `value_text_style` | `Style \| None` | `None` | Style for numerical data values next to series vertices. If `None`, vertex values are omitted. |
| `value_format` | `FormatterType` | `None` | Format string or `Callable[[float], str]` for series vertex values. |
| `background_style` | `Style \| None` | `None` | Outer chart background card style. If `None`, card is omitted. |
| `title` | `str` | `""` | Chart title text displayed at the top of the container. |
| `title_style` | `Style \| None` | `None` | Typography style for `title`. Required for the title to render. |
| `width` / `height` | `float \| None` | `None` | Optional explicit container width and height overrides. If `None`, computed from `radius` and `title`. |

---

## 3. Methods, Properties & Data Models

### 3.1 Methods
- **`add_series(name: str, values: list[float], style: Style, fill_alpha: float = 0.25, line_width: float = 2.0, line_style: LineStyle = "solid", point_shape: PointShape = "circle", point_size: float = 0.8, legend_text_style: Style | None = None, *, show: bool = True, draw_ratio: float = 1.0, draw_direction: DrawDirection = "bottom_to_top") -> Series`**:
  Registers a closed radar polygon series and returns the mutable `Series` instance.
  - `fill_alpha`: Transparency of the polygon fill (`0.0` to `1.0`; defaults to `0.25`).
  - `line_width` / `line_style`: Perimeter stroke width (`2.0`) and pattern (`"solid"`, `"dashed"`, `"dotted"`, `"dashdot"`).
  - `point_shape` / `point_size`: Vertex marker shape (`"circle"`, `"square"`, `"none"` — use `point_shape="none"` to hide points) and radius (`0.8`).
  - `draw_direction`: `"bottom_to_top"` *(default)* expands all spoke vertices radially outward from `min_value`; `"left_to_right"` sweeps spoke-by-spoke around the perimeter.
- **`configure_axis(*, min_value: float | None = None, max_value: float | None = None, levels: int | None = None, scale_format: FormatterType = None) -> RadarChart`**:
  Keyword-only method that updates radial scale bounds, concentric contour count, and scale label formatting in place (returns `self` for chaining).
- **`get_size() -> tuple[float, float]`**:
  Returns the computed `(width, height)` bounding box dimensions.
- **`draw(xy: tuple[float, float] = (0.0, 0.0), *, radius: float | None = None, width: float | None = None, height: float | None = None, align: Literal["bottom_left", "center"] = "bottom_left", scale: float = 1.0) -> None`**:
  Renders the radar chart body onto the canvas anchored at `xy` (`"bottom_left"` or `"center"`), with optional temporary `radius`/`width`/`height` overrides and uniform `scale`.
- **`draw_legend(xy: tuple[float, float], text_style: Style, orientation: Literal["vertical", "horizontal"] = "vertical", swatch_width: float = 2.4, swatch_height: float = 1.2, item_gap: float = 4.0, *, scale: float = 1.0) -> None`**:
  Renders the standalone series legend at `xy`.

### 3.2 Properties & `Series` Model
- **`chart.categories -> list[str]`**: Copy of the radial dimension names.
- **`chart.series -> list[Series]`**: Copy of registered `Series` objects.
- **`Series(name: str, values: list[float], style: Style, fill_alpha: float = 0.25, line_width: float = 2.0, line_style: LineStyle = "solid", point_shape: PointShape = "circle", point_size: float = 0.8, legend_text_style: Style | None = None, show: bool = True, draw_ratio: float = 1.0, draw_direction: DrawDirection = "bottom_to_top")`**:
  Stores `name`, `values`, `style`, `fill_alpha`, `line_width`, `line_style`, `point_shape`, `point_size`, `legend_text_style`, `show`, `draw_ratio`, and `draw_direction`.

---

## 4. Production Examples

### Example 4.1: Software Architecture Non-Functional Attributes (`grid_shape="polygon"`)
```drawlib code=show align=center file=rules_radar_non_functional.png caption="System Architecture Non-Functional Trade-off Analysis with RadarChart"
from drawlib.canvas import save, setup
from drawlib.charts.radar import RadarChart
from drawlib.styles import Styles

setup(width=105, height=88)

chart = RadarChart(
    categories=["Scalability", "Reliability", "Security", "Maintainability", "Latency"],
    axis_line_style=Styles.MutedDashed,
    axis_text_style=Styles.BlackBold.patch(text_size=10.5),
    grid_style=Styles.MutedThin,
    value_text_style=Styles.BlackBold.patch(text_size=10.0),
    radius=24.0,
    min_value=0.0,
    max_value=100.0,
    levels=5,
    grid_shape="polygon",
    title="System Architecture Trade-off Analysis",
    title_style=Styles.BlackBold.patch(text_size=13.0),
    value_format="{:.0f}",
)
chart.add_series("Microservices", [95, 80, 75, 85, 60], style=Styles.PrimaryFlat, fill_alpha=0.3)
chart.add_series(
    "Monolith",
    [60, 90, 85, 70, 95],
    style=Styles.SecondaryNeutral,
    fill_alpha=0.3,
    line_style="dashed",
    point_shape="square",
)
chart.draw(xy=(8.0, 8.0))
chart.draw_legend(xy=(72.0, 55.0), text_style=Styles.Black.patch(text_size=10.5), orientation="vertical")
save()
```

### Example 4.2: Circular Grid Product Evaluation (`grid_shape="circle"` & `scale_format`)
```drawlib code=show align=center file=rules_radar_circular_grid.png caption="Circular Grid Benchmark with scale_text_style and configure_axis()"
from drawlib.canvas import save, setup
from drawlib.charts.radar import RadarChart
from drawlib.styles import Styles

setup(width=100, height=85)

chart = RadarChart(
    categories=["UX Design", "Performance", "Battery Life", "Camera Quality", "Ecosystem", "Price"],
    axis_line_style=Styles.MutedDashed,
    axis_text_style=Styles.BlackBold.patch(text_size=10.5),
    grid_style=Styles.MutedThin,
    scale_text_style=Styles.Muted.patch(text_size=10.0),
    radius=24.0,
    levels=4,
    grid_shape="circle",
    title="Flagship Smartphone Benchmark",
    title_style=Styles.BlackBold.patch(text_size=13.0),
)
chart.configure_axis(min_value=0.0, max_value=10.0, levels=4, scale_format="{:.1f}")
chart.add_series("Device Pro Max", [9.2, 9.5, 8.8, 9.6, 9.0, 6.5], style=Styles.PrimaryFlat)
chart.add_series("Device Ultra", [8.5, 9.2, 9.4, 9.2, 8.2, 7.8], style=Styles.SecondaryNeutral, line_style="dashed")
chart.draw(xy=(13.0, 15.0))
chart.draw_legend(xy=(22.0, 10.0), text_style=Styles.Black.patch(text_size=10.5), orientation="horizontal")
save()
```

---

## 5. Related Rules
- Charts Overview & Axis/Legend Architecture: `uv run drawlib rules show lib-charts-overview`
- Pie & Donut Charts: `uv run drawlib rules show lib-charts-pie`
- Scatter & Bubble Charts: `uv run drawlib rules show lib-charts-scatter`
