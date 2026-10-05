# Line Chart

The `LineChart` component visualizes numerical trends over ordered categories or continuous time points. 
It supports straight line segments, smoothed spline curves, custom point marker shapes, configurable line styles, and decoupled legend rendering.

---

## 1. Quick Example: User Growth Trends

```drawlib 600px center file:linechart_user_growth.png caption:"User Growth Trends with LineChart"
from drawlib.canvas import setup
from drawlib.charts.line import LineChart
from drawlib.styles import Styles

setup(width=100, height=70)

chart = LineChart(
    axis_line_style=Styles.MutedDashed,
    categories=["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    axis_text_style=Styles.Muted.patch(text_size=9.5),
    grid_style=Styles.MutedLight,
    width=80,
    height=45,
    title="Monthly Active Users (k)",
    title_style=Styles.BlackBold.patch(text_size=13.0),
    smooth=True,
    show_points=True,
)
chart.add_series("2025", [45, 52, 58, 65, 72, 80], style=Styles.DarkBold, line_width=2.5, line_style="dashed")
chart.add_series("2026", [60, 75, 88, 110, 135, 160], style=Styles.PrimaryFlat, line_width=2.5)

chart.draw(xy=(10, 8))
chart.draw_legend(xy=(25, 59), text_style=Styles.Muted.patch(text_size=9.0), orientation="horizontal")
```

---

## 2. Key Features

- **Smooth Spline Interpolation (`smooth=True`)**: Renders organic, flowing curves through data points rather than sharp zigzag angles.
- **Data Point Markers (`show_points=True`)**:
  - `point_shape`: Marker symbol (`"circle"`, `"square"`, `"none"`).
  - `point_size`: Radius / dimensions of markers.
- **Stroke Styles (`line_style`)**: Supports `"solid"`, `"dashed"`, and `"dotted"` strokes to differentiate targets from actuals.
- **Decoupled Legend (`draw_legend`)**: Allows rendering the series legend at any coordinate on the canvas.

---

## 3. Class API Reference

### Constructor
```python
LineChart(
    axis_line_style: Style,
    categories: list[str] | None = None,
    axis_text_style: Style | None = None,
    grid_style: Style | None = None,
    value_text_style: Style | None = None,
    background_style: Style | None = None,
    title: str = "",
    title_style: Style | None = None,
    width: float = 80.0,
    height: float = 50.0,
    smooth: bool = False,
    show_points: bool = True,
    point_shape: Literal["circle", "square", "none"] = "circle",
    point_size: float = 0.7,
)
```

### Adding Series & Rendering
```python
chart.add_series(
    name: str,
    values: list[float],
    style: Style,
    line_width: float = 2.0,
    line_style: LineStyle = "solid",
    point_shape: PointShape | None = None,
    point_size: float | None = None,
    legend_text_style: Style | None = None,
)
chart.draw(xy=(0.0, 0.0))
chart.draw_legend(xy, text_style=Styles.Black, orientation="vertical")
```
