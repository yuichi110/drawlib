# Drawlib Charts Guidelines

Render analytical charts with customizable series, axes, legends, and styling.

## 1. Imports
```python
from drawlib.charts import (
    AreaChart,
    BarChart,
    GanttChart,
    LineChart,
    PieChart,
    RadarChart,
    ScatterChart,
)
```

## 2. Core Chart Classes
- `BarChart(categories, width, height, title="")`:
  - `add_series(name, values, color=None)`
  - `configure_y_axis(unit="", show_grid=True)`
  - `draw(xy)` (xy specifies bottom-left or center based on alignment)
- `LineChart(categories, width, height, title="")`:
  - `add_series(name, values, marker=True)`
  - `configure_y_axis(unit="", show_grid=True)`
  - `draw(xy)`
- `PieChart(width, height, title="")`:
  - `add_slice(label, value, color=None)`
  - `draw(xy)`
- `ScatterChart(width, height, title="")`:
  - `add_series(name, points=[(x, y), ...])`
  - `draw(xy)`
- `GanttChart(start_date, end_date, width, height, title="")`:
  - `add_task(name, start, end, ...)`
  - `draw(xy)`

## 3. Minimal Example (BarChart)
```python
from drawlib.canvas import config, save
from drawlib.charts import BarChart

config(width=100, height=70)
chart = BarChart(
    categories=["Q1", "Q2", "Q3", "Q4"],
    width=80,
    height=50,
    title="Quarterly Revenue",
    show_values=True,
)
chart.add_series("Product A", [25.0, 40.0, 55.0, 70.0])
chart.add_series("Product B", [30.0, 35.0, 45.0, 60.0])
chart.configure_y_axis(unit="k$", show_grid=True)
chart.draw(xy=(10, 10))
save()
```
