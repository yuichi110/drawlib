# ScatterChart: Dual-Axis Plots & Multidimensional Bubble Charts

`ScatterChart` plots continuous numerical data across dual Cartesian axes ($X$ and $Y$). It is ideal for identifying statistical correlations, clustering patterns, latency vs. throughput trade-offs, and 3D bubble analysis (where marker radius encodes a third numerical variable).

---

## 1. Overview & Topologies

```text
    Latency (ms) ▲
             100 │           ● Legacy (High Latency)
              80 │
              60 │                ▲ Competitor
              40 │        ●
              20 │    ● Optimized v2.0
               0 └────────────────────────────► Throughput (req/s)
                 0    200   400   600   800
```

- **Dual Continuous Axes**: Unlike categorical charts where the X-axis represents discrete bins, `ScatterChart` computes independent numerical scales for both axes using linear or logarithmic scaling.
- **Annotated Individual Points**: Use `chart.add()` to place highlighted reference points with dedicated text callouts (e.g., benchmark baselines or SLA targets).
- **Multidimensional Bubble Plots**: Passing 3-tuples `(x, y, radius)` to `add_series()` scales point sizes dynamically to communicate a third dimension (such as cost, memory footprint, or cluster size).

---

## 2. Constructor & Configuration

```python
from drawlib.charts.scatter import ScatterChart

chart = ScatterChart(
    width=85.0,                 # Total chart bounding width
    height=52.0,                # Total chart bounding height
    title="Service Throughput vs Latency",
    default_radius=1.0,         # Default radius for points
    default_shape="circle",     # "circle", "square", "rhombus", "triangle"
    legend_position="auto",     # "top", "bottom", "right", "none", "auto"
    show_labels=True,           # Display text annotation labels
)
```

### Parameter Reference

| Parameter | Type | Default | Description |
|---|---|---|---|
| `width` / `height` | `float` | `88.0` / `55.0` | Overall container dimensions in canvas units. |
| `title` | `str` | `""` | Chart title displayed at the top. |
| `default_radius` | `float` | `1.0` | Default radius for point markers when unspecified. |
| `default_shape` | `PointShape` | `"circle"` | Marker shape (`"circle"`, `"square"`, `"rhombus"`, `"triangle"`). |
| `legend_position` | `LegendPosition` | `"auto"` | Location of series legend box. |
| `show_labels` | `bool` | `True` | Whether to display text annotation labels next to points. |

---

## 3. Benchmark Scatter Plot with Baseline Callouts

Combining series with individually annotated baseline points makes system performance reports immediately actionable:

```drawlib 650px center caption:"Throughput vs p99 Latency Benchmark"
from drawlib import canvas
from drawlib.charts.scatter import ScatterChart
from drawlib.styles import Styles

canvas.clear()
canvas.setup(width=105, height=75)

chart = ScatterChart(
    width=85.0,
    height=52.0,
    title="Service Throughput vs p99 Latency Benchmark",
)
chart.configure_x_axis(label="Throughput (req/sec)", unit=" rps", min_value=0, max_value=1000)
chart.configure_y_axis(label="p99 Latency (ms)", unit=" ms", min_value=0, max_value=200)

# 1. Annotated Milestone Points
chart.add(xy=(100.0, 18.0), radius=1.6, label="v1.0 Baseline", style=Styles.MutedFlat)
chart.add(xy=(730.0, 35.0), radius=2.2, label="v2.5 Release", style=Styles.SuccessFlat)

# 2. Multi-Series Experimental Runs
chart.add_series(
    name="Async Rust Engine",
    data=[(300, 18.0), (500, 19.5), (700, 21.0), (950, 24.0)],
    shape="circle",
)
chart.add_series(
    name="Legacy Threadpool",
    data=[(150, 40.0), (300, 65.0), (450, 110.0), (600, 165.0)],
    shape="square",
)

chart.draw(xy=(10.0, 12.0))
```

---

## 4. Multidimensional Cloud Cost Bubble Chart

By providing 3-tuples `(x, y, radius)` in series data, the radius reflects a 3rd numerical dimension:

```drawlib 650px center caption:"Compute Workload Multidimensional Bubble Plot"
from drawlib import canvas
from drawlib.charts.scatter import ScatterChart

canvas.clear()
canvas.setup(width=105, height=75)

chart = ScatterChart(
    width=85.0,
    height=52.0,
    title="Compute Workload: Duration vs Memory vs Cost (Bubble Size)",
)
chart.configure_x_axis(label="Allocated RAM (GB)", unit=" GB", min_value=0, max_value=32)
chart.configure_y_axis(label="Job Execution Time (sec)", unit=" s", min_value=0, max_value=60)

# 3-Tuples encode: (RAM_GB, Execution_Time_Sec, Relative_Monthly_Cost_Radius)
chart.add_series(
    name="Serverless Functions",
    data=[(1.0, 48.0, 1.2), (2.0, 28.0, 1.6), (4.0, 16.0, 2.4), (8.0, 10.0, 3.8)],
    shape="circle",
)
chart.add_series(
    name="Dedicated Kubernetes Pods",
    data=[(4.0, 22.0, 2.2), (8.0, 14.0, 3.2), (16.0, 8.5, 4.8), (32.0, 5.0, 6.5)],
    shape="square",
)

chart.draw(xy=(10.0, 15.0))
```

---

## 5. Best Practices & Guidelines

1. **Explicit Axis Bounds**: Specifying `min_value` and `max_value` on both axes ensures consistent coordinate framing across comparative diagrams.
2. **Bubble Scaling**: Keep marker radii between `1.0` and `6.0` canvas coordinate units to prevent bubbles from occluding neighbouring points.
3. **Logarithmic Scaling**: If throughput or latency spans multiple orders of magnitude, set `scale="log"` on the respective axis via `chart.configure_x_axis(scale="log")`.
