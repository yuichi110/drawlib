# Architecture & Implementation Plan: Charts Expansion Module (`drawlib.charts`)

## 1. Overview & Goals
- **Purpose**: Provide a comprehensive, vector-grade, pure-Python data visualization library within `drawlib` designed for technical documents, slides, and system architecture presentations.
- **Key Design Principles**:
  - **Component-Oriented (Illustration as Code)**: Charts are self-contained components anchored at `xy` on the canvas with explicit width and height, coexisting naturally with diagrams, smartarts, and shapes.
  - **Object-Oriented Builder Flow**: Consistent usage pattern across all charts: instantiate container (`SomethingChart(...)`), register series or slices (`add_series(...)` / `add_slice(...)`), configure axes, and render via `draw(xy)`.
  - **Reusability & DRY Foundation**: Maximum reuse of `_charts/_common/` modules (`Axis` with Nice Numbers/Log Scale, `render_legend`, `DEFAULT_CHART_PALETTE`).
  - **Zero External Data-Viz Dependencies**: Built 100% on Drawlib's core drawing primitives (`line`, `lines`, `rectangle`, `circle`, `wedge`, `polygon`, `text`).

---

## 2. Target Chart Family & Architecture

```text
src/drawlib/
├── _charts/
│   ├── _common/                       # Shared Foundation
│   │   ├── _types.py                  # Shared types & chart enums
│   │   ├── _axis.py                   # Axis model, Nice Numbers, Log Scale
│   │   └── _legend.py                 # Automatic legend layout & rendering
│   │
│   ├── bar_chart/                     # [Complete] BarChart
│   │   ├── _chart.py, _series.py, _renderer.py
│   │
│   ├── line_chart/                    # [Phase 1] LineChart & AreaChart
│   │   ├── _base.py                   # Shared Cartesian line/area base container
│   │   ├── _line.py                   # LineChart
│   │   ├── _area.py                   # AreaChart (overlap & stacked area)
│   │   ├── _series.py                 # LineSeries, AreaSeries
│   │   └── _renderer.py               # Polyline, smooth curve, area polygon renderer
│   │
│   ├── pie_chart/                     # [Phase 2] PieChart & DonutChart
│   │   ├── _slice.py                  # PieSlice model (name, value, color, explode)
│   │   ├── _chart.py                  # PieChart container (radius, hole_ratio, center_text)
│   │   └── _renderer.py               # Wedge sector drawing, text positioning, legend
│   │
│   └── radar_chart/                   # [Phase 3] RadarChart
│       ├── _series.py                 # RadarSeries model
│       ├── _chart.py                  # RadarChart container (categories, radius, concentric ticks)
│       └── _renderer.py               # Regular polygon grid, radial lines, closed polygon fill
│
├── charts.py                          # Public facade (BarChart, LineChart, AreaChart, PieChart, RadarChart)
└── __init__.py                        # Module registry
```

---

## 3. Detailed Specifications

### 3.1. LineChart (折れ線グラフ)

#### Concept
- Visualizes continuous trends, timeseries, and multi-series benchmark comparisons.
- Full reuse of `Axis` (X category axis, Y linear/log value axis) and `Legend`.

#### Usage Example
```python
from drawlib import canvas
from drawlib.charts import LineChart

canvas.initialize()

chart = LineChart(
    categories=["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    width=80,
    height=55,
    title="Monthly Active Users (Thousands)",
    show_points=True,  # Plot markers at data points
    point_shape="circle",  # "circle", "square", "none"
    point_size=1.2,
    smooth=False,  # Straight line vs smooth spline
    show_values=False,
    legend_position="auto",
)

chart.add_series("2023", [120, 145, 190, 240, 310, 390])
chart.add_series("2024", [150, 195, 270, 360, 480, 620])

chart.configure_y_axis(unit="k", show_grid=True)
chart.draw(xy=(10.0, 20.0))
```

---

### 3.2. AreaChart (面グラフ)

#### Concept
- Standalone top-level class sharing the underlying engine with `LineChart`.
- Specialized for volume trends, capacity saturation, and resource allocation over time.
- Supports both **overlapping semi-transparent areas** (`mode="overlap"`) and **cumulative stacked areas** (`mode="stack"`).

#### Usage Example
```python
from drawlib import canvas
from drawlib.charts import AreaChart

canvas.initialize()

chart = AreaChart(
    categories=["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"],
    width=80,
    height=55,
    title="Inbound vs Outbound Network Traffic",
    mode="overlap",  # "overlap" or "stack"
    fill_alpha=0.35,  # Default transparency for filled polygons
    show_points=False,
)

chart.add_series("Inbound", [120, 160, 480, 850, 780, 340])
chart.add_series("Outbound", [80, 110, 320, 520, 490, 210])

chart.configure_y_axis(unit="MB/s", show_grid=True)
chart.draw(xy=(10.0, 20.0))
```

---

### 3.3. PieChart (円・ドーナツグラフ)

#### Concept
- Visualizes proportional shares and composition breakdown.
- Automatically transitions into a **Donut Chart** when `hole_ratio > 0.0`.
- Supports slice explosion, percentage formatting, and center KPI callouts.

#### Usage Example
```python
from drawlib import canvas
from drawlib.charts import PieChart

canvas.initialize()

chart = PieChart(
    radius=22.0,
    title="Cloud Infrastructure Cost Breakdown",
    hole_ratio=0.55,  # Donut hole (0.0 = solid pie)
    center_text="Total\n$14,200",  # Centered badge for donut chart
    show_values=True,  # Display percentages
    value_format="{:.1f}%",
    start_angle=90.0,  # 12 o'clock starting position
    legend_position="right",
)

chart.add_slice("Compute (EC2/EKS)", 52.0)
chart.add_slice("Storage (S3/EBS)", 24.0)
chart.add_slice("Database (RDS)", 16.0)
chart.add_slice("Networking", 8.0, explode=2.0)  # Emphasized slice

chart.draw(xy=(25.0, 25.0))
```

---

### 3.4. RadarChart (レーダーチャート)

#### Concept
- Visualizes multivariate comparisons across 3 or more metric axes.
- Essential for architecture trade-off evaluation, tech stack comparisons, and non-functional requirements.
- Concentric polygon or circular gridlines with radial axis spokes.

#### Usage Example
```python
from drawlib import canvas
from drawlib.charts import RadarChart

canvas.initialize()

chart = RadarChart(
    categories=["Throughput", "Latency", "Scalability", "Security", "Cost Efficiency"],
    radius=22.0,
    title="Database Architecture Evaluation",
    fill_alpha=0.25,
    show_points=True,
    legend_position="top",
)

chart.add_series("PostgreSQL", [85, 90, 75, 95, 80])
chart.add_series("DynamoDB", [95, 85, 95, 75, 70])

chart.configure_axis(
    min_value=0.0,
    max_value=100.0,
    ticks=[20.0, 40.0, 60.0, 80.0, 100.0],
    show_grid=True,
)

chart.draw(xy=(25.0, 25.0))
```

---

## 4. Implementation Phases

### Phase 1: LineChart & AreaChart
1. **Core Models**:
   - `_charts/line_chart/_base.py`: Base container class managing data coordinates and boundaries.
   - `_charts/line_chart/_series.py`: `LineSeries` and `AreaSeries`.
   - `_charts/line_chart/_line.py`: `LineChart` implementation.
   - `_charts/line_chart/_area.py`: `AreaChart` implementation with `overlap` and `stack` algorithms.
2. **Renderer (`_renderer.py`)**:
   - Path interpolation (straight segment & smooth spline).
   - Area polygon construction (connecting data points to baseline or previous stacked series).
   - Point marker drawing (`circle`, `square`).
3. **Tests (`tests/test_line_chart.py`, `tests/test_area_chart.py`)**:
   - Coordinate calculations, multi-series, log scale, and rendering tests.
4. **Documentation & Verification**:
   - `docs_src/charts/line.md`, `docs_src/charts/area.md`.
   - `./dcli check all`, `./dcli test all`, `./dcli docs build`.

### Phase 2: PieChart
1. **Models & Renderer (`_charts/pie_chart/`)**:
   - Slice angle calculation ($\theta_i = 360^\circ \times \frac{v_i}{\sum v}$).
   - Wedge primitive rendering with optional hole cutout (`hole_ratio`).
   - Label angle positioning and leader lines if crowded.
2. **Tests & Docs**:
   - `tests/test_pie_chart.py`, `docs_src/charts/pie.md`.

### Phase 3: RadarChart
1. **Models & Renderer (`_charts/radar_chart/`)**:
   - Polar-to-Cartesian transformation ($x = r \cos \theta, y = r \sin \theta$).
   - N-gon concentric gridline generation.
   - Closed semi-transparent polygon rendering per series.
2. **Tests & Docs**:
   - `tests/test_radar_chart.py`, `docs_src/charts/radar.md`.

---

## 5. Verification Checklist for Each Phase
- [ ] `./dcli check all` (Ruff, Ty, Docstrings) passes with 0 errors.
- [ ] Pytest unit and integration tests pass 100%.
- [ ] `./dcli docs build` compiles all markdown codeblocks into clear PNG images.
- [ ] Visual inspection confirms high typographic quality and balance.
