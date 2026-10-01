# Bar Chart

The `BarChart` component renders vertical or horizontal bar charts for comparing categorical metrics. 
It supports multi-series grouping, stacked bars, custom corner radii, value annotations, and automatic legend placement.

---

## 1. Quick Example: Stacked Resource Allocation

```drawlib 600px center caption:"Stacked Resource Allocation with BarChart"
from drawlib.canvas import setup
from drawlib.charts.bar import BarChart
from drawlib.styles import Colors

setup(width=100, height=60)

chart = BarChart(
    width=80,
    height=45,
    categories=["Dev", "Stage", "Prod"],
    title="Container Resource Limits (vCPU)",
    bar_mode="stack",
    r=1.0,
    show_values=True,
)
chart.add_series("Allocated", [4.0, 16.0, 64.0], color=Colors.Primary)
chart.add_series("Burst Buffer", [2.0, 8.0, 32.0], color=Colors.Accent)

chart.draw(xy=(10, 8))
```

---

## 2. Modes and Orientations

- **`orientation`**:
  - `"vertical"` *(default)*: Columns grow upward from the bottom X-axis.
  - `"horizontal"`: Bars grow rightward from the left Y-axis.
- **`bar_mode`**:
  - `"group"` *(default)*: Side-by-side clustered bars for comparing distinct series across categories.
  - `"stack"`: Accumulates series vertically/horizontally to show part-to-whole proportions.
- **`r`**: Corner rounding radius applied to the outer edges of the bars.
- **`show_values`**: Automatically displays numerical values directly on top of or inside the bars.

---

## 3. Class API Reference

### Constructor
```python
BarChart(
    title: str = "",
    categories: list[str] | None = None,
    width: float = 60.0,
    height: float = 40.0,
    orientation: Literal["vertical", "horizontal"] = "vertical",
    bar_mode: Literal["group", "stack"] = "group",
    bar_width_ratio: float = 0.7,
    r: float = 0.0,
    show_values: bool = False,
    legend_position: Literal["top", "bottom", "right", "none", "auto"] = "auto",
)
```

### Adding Data
- **`add_series(name: str, values: list[float], color=None, style=None)`**:  
  Registers a series. `values` must align with the length of `categories`.
- **`configure_y_axis(min_value=None, max_value=None, ticks=None, unit=None)`**:  
  Customizes numerical axis scaling and units.
