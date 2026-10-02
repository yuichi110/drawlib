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
from drawlib.styles import Styles

chart = AreaChart(
    axis_line_style=Styles.MutedDashed,
    categories=["2021", "2022", "2023", "2024", "2025"],
    axis_text_style=Styles.Muted.patch(text_size=9.5),
    grid_style=Styles.MutedLight,
    width=80.0,
    height=55.0,
    title="Cumulative Revenue Streams",
    title_style=Styles.BlackBold.patch(text_size=13.0),
    mode="stack",               # "stack" or "overlap"
    fill_alpha=0.65,            # Polygon fill opacity (0.0 to 1.0)
    smooth=False,               # Smooth spline curve or straight lines
    show_points=False,          # Draw vertex markers
)
```

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
    axis_line_style=Styles.MutedDashed,
    categories=["2021", "2022", "2023", "2024", "2025"],
    axis_text_style=Styles.Muted.patch(text_size=9.5),
    grid_style=Styles.MutedLight,
    width=80.0,
    height=55.0,
    title="Cumulative Revenue Streams",
    title_style=Styles.BlackBold.patch(text_size=13.0),
    mode="stack",
    fill_alpha=0.65,
)
chart.add_series("Enterprise Cloud", [40.0, 70.0, 110.0, 160.0, 225.0], style=Styles.PrimaryFlat)
chart.add_series("SaaS Products", [25.0, 38.0, 52.0, 68.0, 85.0], style=Styles.SecondaryFlat)
chart.add_series("Support & Advisory", [15.0, 18.0, 22.0, 24.0, 26.0], style=Styles.AccentFlat)

chart.configure_y_axis(unit="M$", label="Gross Revenue (USD Millions)")
chart.draw(xy=(10.0, 15.0))
chart.draw_legend(xy=(20.0, 72.0), text_style=Styles.Muted.patch(text_size=9.0), orientation="horizontal")
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
    axis_line_style=Styles.MutedDashed,
    categories=["02:00", "06:00", "10:00", "14:00", "18:00", "22:00"],
    axis_text_style=Styles.Muted.patch(text_size=9.5),
    grid_style=Styles.MutedLight,
    width=80.0,
    height=50.0,
    title="Ingress vs Egress Gateway Traffic",
    title_style=Styles.BlackBold.patch(text_size=13.0),
    mode="overlap",
    fill_alpha=0.35,
    show_points=True,
    point_shape="circle",
    point_size=0.6,
)
chart.add_series("Ingress Traffic", [120.0, 180.0, 650.0, 920.0, 780.0, 310.0], style=Styles.PrimaryFlat)
chart.add_series("Egress Traffic", [80.0, 110.0, 420.0, 610.0, 530.0, 220.0], style=Styles.SecondaryFlat)

chart.configure_y_axis(unit="Gbps", label="Throughput (Gbps)")
chart.draw(xy=(10.0, 15.0))
chart.draw_legend(xy=(25.0, 67.0), text_style=Styles.Muted.patch(text_size=9.0), orientation="horizontal")
```
