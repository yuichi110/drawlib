# Charts Overview

The `drawlib.charts` module provides a declarative, pure-Python data visualization engine for comparative, statistical, relational, and project schedule charts.

---

## 1. Why Pure-Python Charts in Drawlib?

Unlike traditional Python visualization libraries (such as Matplotlib, Seaborn, or Plotly) that generate isolated image files or web-only canvases, Drawlib charts are **first-class vector canvas elements**:

- **Seamless Canvas Coexistence**: Charts can share the same canvas with architecture schemas, callout bubbles, and icons.
- **Deterministic Layouts**: All margins, tick spaces, and legend boxes are mathematically computed from explicit canvas dimensions (`width`, `height`).
- **Consistent Visual Theming**: Chart elements—bars, areas, gridlines, axes, labels, and legends—automatically adapt to Drawlib's active styling presets (`Styles.primary_flat`, `Styles.accent_flat`, etc.).

```drawlib 650px center caption:"Declarative Multi-Series Bar Chart"
from drawlib.canvas import setup
from drawlib.charts.bar import BarChart
from drawlib.styles import Colors

setup(width=100, height=60)

chart = BarChart(
    width=80,
    height=45,
    categories=["Q1", "Q2", "Q3", "Q4"],
    title="Quarterly Revenue ($M)",
)
chart.add_series("2025", [12.5, 18.2, 22.0, 31.4], color=Colors.primary)
chart.add_series("2026", [15.0, 24.5, 29.8, 38.0], color=Colors.accent)

chart.draw(xy=(10, 8))
```

---

## 2. The Seven Chart Families

Drawlib organizes charts into seven specialized submodules under `drawlib.charts`:

| Module | Primary Class | Best Suited For |
| :--- | :--- | :--- |
| `drawlib.charts.bar` | **`BarChart`** | Categorical comparisons (vertical, horizontal, grouped, stacked). |
| `drawlib.charts.line` | **`LineChart`** | Continuous metrics and trends over time (linear or spline smoothed). |
| `drawlib.charts.area` | **`AreaChart`** | Cumulative volume and part-to-whole trends over time. |
| `drawlib.charts.pie` | **`PieChart`** | Proportional distributions, donut charts, and center KPI badges. |
| `drawlib.charts.radar` | **`RadarChart`** | Multi-attribute evaluation, skill matrices, and spiderweb plots. |
| `drawlib.charts.scatter` | **`ScatterChart`** | 2D correlations, cluster distributions, and 3D bubble plots. |
| `drawlib.charts.gantt` | **`GanttChart`** | Project roadmaps, phase tasks, milestones, and dependency arrows. |

---

## 3. Universal Chart Architecture

Every chart in Drawlib follows a consistent lifecycle and coordinate contract:

### 1. Dimension Instantiation
Specify virtual canvas dimensions (`width`, `height`) during initialization:
```python
chart = BarChart(width=90, height=50, categories=[...], title="Performance Metrics")
```

### 2. Adding Data Series
Add data series directly using intuitive methods:
```python
chart.add_series("US Region", [120, 180, 240])
chart.add_series("EU Region", [90, 150, 210])
```

### 3. Rendering via Bottom-Left Anchor
All charts are anchored by their **bottom-left corner** via `draw(xy=(x, y))`:
```python
chart.draw(xy=(15, 10))
```
