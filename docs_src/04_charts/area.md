# AreaChart: Overlapping & Stacked Quantitative Volumes

`AreaChart` visualizes cumulative volumes, capacity distributions, and continuous trends over categorical intervals or time periods. By filling the geometric area between data series contours and the baseline ($Y=0$), it highlights both the total volume and individual series contributions.

---

## 1. Overview & Key Modes

Area charts support two core operational modes:
- **`mode="overlap"`**: Each series polygon starts at the baseline ($Y=0$) and overlaps with preceding series. Use a semi-transparent opacity (`fill_alpha=0.3` to `0.5`) to make underlying curves visible.
- **`mode="stack"`**: Each series rests directly on top of the preceding one, showing cumulative totals (e.g., total gross revenue broken down by product line).

```text
       mode="overlap" (Semi-transparent)           mode="stack" (Cumulative Total)
   Y ▲                                         Y ▲
     │        ▲                                  │         ▲ Total
     │       ╱ █╲    ▲                           │        ╱█╲
     │     ▲╱  █ ╲  ╱ ╲                          │      ▲╱███╲ Series B
     │    ╱ █  █  ╲╱   ╲                         │     ╱██████╲ Series A
     └───┴──┴──┴───┴────┴──► X                   └────┴────────┴────► X
```

---

## 2. Constructor & Configuration

```python
from drawlib.charts.area import AreaChart

chart = AreaChart(
    categories=["2021", "2022", "2023", "2024", "2025"],
    width=80.0,
    height=55.0,
    title="Cumulative Revenue Streams",
    mode="stack",               # "stack" or "overlap"
    fill_alpha=0.65,            # Polygon fill opacity (0.0 to 1.0)
    smooth=False,               # Smooth spline curve or straight lines
    show_points=False,          # Draw vertex markers
    legend_position="top",      # "top", "bottom", "right", "none", "auto"
)
```

### Parameter Reference

| Parameter | Type | Default | Description |
|---|---|---|---|
| `categories` | `list[str]` | Required | Category labels along the horizontal X-axis. |
| `width` / `height` | `float` | `80.0` / `50.0` | Bounding box dimensions on the canvas. |
| `title` | `str` | `""` | Chart title displayed at the top. |
| `mode` | `"overlap"` \| `"stack"` | `"overlap"` | Cumulative stacked or overlapping volume. |
| `fill_alpha` | `float` | `0.35` | Transparency opacity of the area fill polygon. |
| `smooth` | `bool` | `False` | When `True`, renders smooth cubic-like curves. |
| `show_points` | `bool` | `False` | Whether to draw marker points at vertex coordinates. |
| `point_shape` | `"circle"` \| `"square"` \| `"none"` | `"none"` | Shape of vertex markers. |
| `point_size` | `float` | `1.0` | Radius or half-width of vertex markers. |
| `legend_position` | `LegendPosition` | `"auto"` | Position of the legend box. |

---

## 3. Cumulative Stacked Area Chart

Stacked area charts are ideal for displaying total aggregate metrics and showing the proportional contribution of each stream over time.

```drawlib 650px center caption:"Cumulative Stacked Revenue Streams"
from drawlib import canvas
from drawlib.charts.area import AreaChart
from drawlib.styles import Styles

canvas.clear()
canvas.setup(width=100, height=80)

chart = AreaChart(
    categories=["2021", "2022", "2023", "2024", "2025"],
    width=80.0,
    height=55.0,
    title="Cumulative Revenue Streams",
    mode="stack",
    fill_alpha=0.65,
    legend_position="top",
)
chart.add_series("Enterprise Cloud", [40.0, 70.0, 110.0, 160.0, 225.0], style=Styles.PrimaryFlat)
chart.add_series("SaaS Products", [25.0, 38.0, 52.0, 68.0, 85.0], style=Styles.SecondaryFlat)
chart.add_series("Support & Advisory", [15.0, 18.0, 22.0, 24.0, 26.0], style=Styles.AccentFlat)

chart.configure_y_axis(unit="M$", label="Gross Revenue (USD Millions)", show_grid=True)
chart.draw(xy=(10.0, 15.0))
```

---

## 4. Overlapping Area Chart with Custom Markers

When comparing independent metrics that share the same scale (such as network ingress and egress traffic), use `mode="overlap"` with a lighter alpha and vertex markers:

```drawlib 650px center caption:"Gateway Ingress vs Egress Traffic"
from drawlib import canvas
from drawlib.charts.area import AreaChart
from drawlib.styles import Styles

canvas.clear()
canvas.setup(width=100, height=75)

chart = AreaChart(
    categories=["02:00", "06:00", "10:00", "14:00", "18:00", "22:00"],
    width=80.0,
    height=50.0,
    title="Ingress vs Egress Gateway Traffic",
    mode="overlap",
    fill_alpha=0.35,
    show_points=True,
    point_shape="circle",
    point_size=0.6,
    legend_position="top",
)
chart.add_series("Ingress Traffic", [120.0, 180.0, 650.0, 920.0, 780.0, 310.0], style=Styles.PrimaryFlat)
chart.add_series("Egress Traffic", [80.0, 110.0, 420.0, 610.0, 530.0, 220.0], style=Styles.SecondaryFlat)

chart.configure_y_axis(unit="Gbps", label="Throughput (Gbps)", show_grid=True)
chart.draw(xy=(10.0, 15.0))
```

---

## 5. Best Practices & Guidelines

1. **Alpha Selection in Overlap Mode**: Keep `fill_alpha` between `0.25` and `0.45` when overlapping 2–3 series. Higher opacity makes back layers invisible.
2. **Order of Series in Stack Mode**: Define the most stable, foundational series first (it anchors the bottom of the stack), and place fluctuating series higher up.
3. **Axis Anchoring**: Area charts must always anchor the value axis to zero (`min_value=0.0`) so proportional visual areas represent accurate relative quantities.
