# PieChart: Proportional Compositions & Donut Badges

`PieChart` visualizes proportional compositions where slices represent parts of a whole ($100\%$). It supports classic solid pie charts, modern donut rings with center KPI badges, and outward slice explosion for emphasizing key figures.

---

## 1. Overview & Topologies

```text
        Standard Pie Chart                          Donut Chart with Center KPI
            12 o'clock                                      12 o'clock
                ▲                                               ▲
            . - ~ - .                                       . - ~ - .
        . '    |    ' .                             . '    |    ' .
      /        |  45%   \                         /    ┌───────┐    \
     |  35%    |         |                       |     │ $1.2B │     |
     |         |   20%   |                       |     │  ARR  │     |
      \        |        /                         \    └───────┘    /
        . '    |    ' .                             . '    |    ' .
            ' - ~ - '                                       ' - ~ - '
```

- **Solid Pie (`hole_ratio=0.0`)**: Traditional full sector representation.
- **Donut Chart (`hole_ratio=0.5` to `0.7`)**: Modern ring layout that provides central canvas real estate for large numeric key indicators (`center_text`).
- **Exploded Slices (`explode > 0.0`)**: Displaces a specific wedge radially outwards from the center for visual emphasis.

---

## 2. Constructor & Configuration

```python
from drawlib.charts.pie import PieChart

chart = PieChart(
    radius=26.0,                # Outer radius in canvas coordinate units
    hole_ratio=0.62,            # Inner hole ratio (0.0 for pie, 0.6+ for donut)
    center_text="$1.2B\nARR",   # Center badge text (supports multiline)
    title="Revenue by Product", # Top title text
    start_angle=90.0,           # Starting angle in degrees (90.0 = 12 o'clock)
    clockwise=True,             # Clockwise slice progression
    show_values=True,           # Display percentage labels on slices
    value_format="{:.1f}%",     # Formatter for percentage badges
    legend_position="right",    # "right", "bottom", "top", "none"
)
```

### Parameter Reference

| Parameter | Type | Default | Description |
|---|---|---|---|
| `radius` | `float` | `20.0` | Outer radius of the pie circle in canvas units. |
| `title` | `str` | `""` | Chart title displayed at the top. |
| `hole_ratio` | `float` | `0.0` | Inner hole ratio (0.0 for solid pie; 0.1 to 0.9 for donut ring). |
| `center_text` | `str` | `""` | Text rendered in center hole of donut (supports `\n`). |
| `start_angle` | `float` | `90.0` | Starting radial angle in degrees (90.0 is 12 o'clock). |
| `clockwise` | `bool` | `True` | Whether slices are ordered clockwise. |
| `show_values` | `bool` | `True` | Whether to display percentage labels on slices ($\ge 4\%$). |
| `value_format` | `FormatterType` | `"{:.1f}%"` | String format or function converting proportional ratio. |
| `legend_position` | `LegendPosition` | `"right"` | Legend box placement (`"right"`, `"bottom"`, `"top"`, `"none"`). |
| `width` / `height` | `float \| None` | `None` | Optional container dimension overrides. |

---

## 3. Donut Chart with Center KPI Badge

Donut charts are the preferred choice for enterprise dashboards and executive presentations.

```drawlib 650px center caption:"Revenue Contribution Donut Chart"
from drawlib import canvas
from drawlib.charts.pie import PieChart

canvas.clear()
canvas.setup(width=95, height=75)

chart = PieChart(
    radius=26.0,
    hole_ratio=0.62,
    center_text="$1.2B\nARR",
    title="Revenue Contribution by Product Line",
    legend_position="right",
)
chart.add_slice("Cloud Infrastructure", 620.0)
chart.add_slice("AI Developer Tools", 340.0)
chart.add_slice("Security Suite", 180.0)
chart.add_slice("Legacy Support", 60.0)

chart.draw(xy=(10.0, 10.0))
```

---

## 4. Exploded Slice Allocation

Setting `explode > 0.0` radially displaces a slice away from the center origin, drawing immediate focus to that wedge:

```drawlib 650px center caption:"Budget Allocation with Exploded Slice"
from drawlib import canvas
from drawlib.charts.pie import PieChart

canvas.clear()
canvas.setup(width=90, height=80)

chart = PieChart(
    radius=25.0,
    title="R&D Budget Allocation (2026)",
    legend_position="bottom",
)
chart.add_slice("Generative AI Models", 48.0, explode=3.0)
chart.add_slice("Core Infrastructure", 24.0)
chart.add_slice("DevOps & Tooling", 16.0)
chart.add_slice("Compliance & Security", 12.0)

chart.draw(xy=(15.0, 10.0))
```

---

## 5. Best Practices & Guidelines

1. **Category Count**: Keep total slices between 3 and 7. More than 7 slices makes comparison difficult; consider grouping smaller items into an `"Others"` category.
2. **Small Slice Suppression**: Drawlib automatically suppresses percentage labels for slices with $< 4\%$ share to prevent label collisions. Rely on the legend for small items.
3. **Canvas Bounds**: Since the pie chart radius extends equally in all radial directions, ensure sufficient canvas padding on all four sides (`canvas.setup(width=95, height=75)` with `radius=26`).
