# Line Chart

The `LineChart` component visualizes numerical trends over ordered categories or continuous time points. 
It supports straight line segments, smoothed spline curves, custom point marker shapes, and configurable line styles.

---

## 1. Quick Example: User Growth Trends



<figure class="drawlib-image" style="text-align: center;">
  <img src="line_images/1.png" alt="line_1" style="width: 600px; max-width: 100%;" />
  <figcaption class="drawlib-caption">User Growth Trends with LineChart</figcaption>
</figure>



---

## 2. Key Features

- **Smooth Spline Interpolation (`smooth=True`)**: Renders organic, flowing curves through data points rather than sharp zigzag angles.
- **Data Point Markers (`show_points=True`)**:
  - `point_shape`: Marker symbol (`"circle"`, `"square"`, `"none"`).
  - `point_size`: Radius / dimensions of markers.
- **Stroke Styles (`line_style`)**: Supports `"solid"`, `"dashed"`, and `"dotted"` strokes to differentiate targets from actuals.

---

## 3. Class API Reference

### Constructor
```python
LineChart(
    categories: list[str],
    width: float = 80.0,
    height: float = 50.0,
    title: str = "",
    smooth: bool = False,
    show_points: bool = True,
    point_shape: Literal["circle", "square", "none"] = "circle",
    point_size: float = 0.7,
    show_values: bool = False,
    legend_position: Literal["auto", "top", "bottom", "right", "none"] = "auto",
)
```

### Adding Series
```python
chart.add_series(
    name: str,
    values: list[float],
    color: ColorType | None = None,
    line_width: float = 2.0,
    line_style: LineStyle = "solid",
    point_shape: PointShape | None = None,
    point_size: float | None = None,
)
```
