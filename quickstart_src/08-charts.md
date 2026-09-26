# 8. Declarative Charts

`drawlib.charts` provides vector-grade data visualization built directly on Drawlib's canvas primitives. You can place charts alongside annotations, icons, or architecture diagrams on any canvas.

## Supported Chart Types

- **`BarChart`**: Vertical and horizontal grouped/stacked bars with linear or logarithmic scales.
- **`LineChart` & `AreaChart`**: Trend lines, smooth splines, custom markers, and stacked areas.
- **`PieChart` & `RadarChart`**: Proportional slices, donut rings, and multivariate spider charts.
- **`ScatterChart` & `GanttChart`**: 2D correlation plots and project schedule timelines.

## Example: Grouped Bar Chart

```drawlib 600px center caption:"Figure 8.1: Declarative Grouped BarChart"
from drawlib import canvas
from drawlib.charts import BarChart

canvas.initialize()

chart = BarChart(
    categories=["Q1", "Q2", "Q3", "Q4"],
    width=80,
    height=56,
    title="Quarterly Cloud vs On-Premises Throughput",
    show_values=True,
)
chart.add_series("Cloud Native", [48.0, 72.0, 96.0, 128.0])
chart.add_series("Legacy On-Prem", [52.0, 46.0, 39.0, 32.0])
chart.configure_y_axis(unit="req/s", show_grid=True)
chart.draw(xy=(10.0, 18.0))
```
