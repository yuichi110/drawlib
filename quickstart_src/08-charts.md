# 8. Declarative Quantitative Charts

`drawlib.charts` provides a declarative, vector-grade charting engine directly integrated with Drawlib's canvas primitives. Unlike standalone plotting libraries that output static PNG plots in isolated windows, Drawlib charts can be composed alongside architectural diagrams, callouts, and system annotations on a single canvas.

## Supported Chart Types

- **`BarChart`**: Grouped and stacked bars with vertical or horizontal orientation and optional value labels.
- **`LineChart` & `AreaChart`**: Continuous trend lines, splines, markers, and filled cumulative areas.
- **`PieChart` & `RadarChart`**: Proportional slices, donut rings, and multivariate spider web diagrams.
- **`GanttChart`**: Project milestones, sprint roadmaps, and task dependency schedules.

## Grouped Bar Chart Example

```drawlib 640px center caption:"Figure 8.1: Declarative Grouped BarChart"
from drawlib.canvas import setup
from drawlib.charts.bar import BarChart

setup(width=120, height=60)

chart = BarChart(
    categories=["Q1", "Q2", "Q3", "Q4"],
    width=90,
    height=48,
    title="Quarterly Cloud vs On-Premises Throughput",
    show_values=True,
)

chart.add_series("Cloud Native", [48.0, 72.0, 96.0, 134.0])
chart.add_series("Legacy On-Prem", [52.0, 46.0, 39.0, 28.0])
chart.configure_y_axis(unit="req/s", show_grid=True)

chart.draw(xy=(15.0, 6.0))
```

## Multi-Series Line Chart Example

```drawlib 640px center caption:"Figure 8.2: Service Throughput & Error Rate LineChart"
from drawlib.canvas import setup
from drawlib.charts.line import LineChart

setup(width=120, height=60)

chart = LineChart(
    categories=["00:00", "04:00", "08:00", "12:00", "16:00", "20:00", "24:00"],
    width=90,
    height=48,
    title="24-Hour API Gateway Latency Trend",
    show_points=True,
)

chart.add_series("P99 Latency (ms)", [14.0, 12.0, 16.0, 28.0, 45.0, 32.0, 18.0])
chart.add_series("P50 Latency (ms)", [6.0, 5.5, 6.2, 8.1, 12.0, 9.4, 6.8])
chart.configure_x_axis(label="Hour of Day", show_grid=True)
chart.configure_y_axis(unit="ms", show_grid=True)

chart.draw(xy=(15.0, 6.0))
```
