# Architecture & Implementation Plan: Charts Module (`drawlib.charts`)

## 1. Overview & Goals
- **Purpose**: Provide a declarative, pure-Python data visualization and charting module within `drawlib` designed specifically for documents, slide presentations, and technical reports.
- **Key Design Principles**:
  - **Component-Oriented (Illustration as Code)**: Charts are independent components placed at an arbitrary canvas coordinate `xy` with `(width, height)`, coexisting seamlessly with diagrams, shapes, and smartarts.
  - **Object-Oriented Builder Flow**: Follows Drawlib's standard pattern: instantiate a container (`BarChart(...)`), add series elements (`add_series(...)`), and render via `draw(xy)`.
  - **First-Class Customizable Axis & Scales**:
    - Linear and **Logarithmic (Log Scale)** modes.
    - Explicit tick values, tick steps, and minimum/maximum overrides.
    - Rich formatting via format strings (e.g. `"{:g} ms"`, `"${:,.0f}"`) or custom functions.
    - Full styling control over gridlines, axis lines, and tick typography.
  - **Automatic Legends & Layout**: Legend boxes, axis ticks, gridlines, and scales are calculated and rendered automatically without manual layout arithmetic.
  - **Decoupled Architecture**: Built 100% on Drawlib `_core` drawing primitives (`rectangle`, `line`, `lines`, `text`) without heavy third-party visualization dependencies.
  - **Modern, Publication-Ready Defaults**: Clean typography, pleasant modern palettes (Slate, Indigo, Emerald, Amber, Rose), and subtle gridlines right out of the box.

---

## 2. Package Architecture

Following Drawlib's single-package architecture (matching `smartarts.py`):

```text
src/drawlib/
├── _charts/
│   ├── __init__.py                 # Internal charts export
│   ├── _common/                    # Shared charting components
│   │   ├── __init__.py
│   │   ├── _types.py               # Orientation, BarMode, LegendPosition, ScaleType, etc.
│   │   ├── _axis.py                # Axis model, Nice-numbers algorithm, Log scale, tick generation
│   │   └── _legend.py              # Automatic legend layout and card rendering
│   │
│   └── bar_chart/                  # Phase 1: Bar Chart implementation
│       ├── __init__.py
│       ├── _series.py              # BarSeries model (name, values, color, style)
│       ├── _chart.py               # BarChart container class with x_axis & y_axis
│       └── _renderer.py            # BarChart coordinate mapping and rendering
│
├── charts.py                       # Public facade (re-exports BarChart, Axis, etc.)
└── __init__.py                     # Registers `charts` as a top-level module
```

---

## 3. Public API Specification (Phase 1: BarChart)

### 3.1. Simple Single-Series Bar Chart

```python
from drawlib import canvas
from drawlib.charts import BarChart
from drawlib.colors import Colors140

canvas.initialize()

chart = BarChart(
    title="Quarterly Active Users (M)",
    categories=["Q1", "Q2", "Q3", "Q4"],
    width=50.0,
    height=35.0,
)
chart.add_series("Users", [12.5, 18.2, 24.0, 31.5], color=Colors140.SteelBlue)

chart.draw(xy=(25.0, 32.5))
```

### 3.2. Grouped Bar Chart with Automatic Legend

```python
from drawlib import canvas
from drawlib.charts import BarChart
from drawlib.colors import Colors140

canvas.initialize()

chart = BarChart(
    title="Quarterly Sales by Region ($M)",
    categories=["Q1", "Q2", "Q3", "Q4"],
    bar_mode="group",  # "group" or "stack"
    width=60.0,
    height=40.0,
)

# Legends are automatically generated from added series!
chart.add_series("North America", [45, 60, 75, 90], color=Colors140.RoyalBlue)
chart.add_series("Europe", [30, 42, 55, 68], color=Colors140.MediumSeaGreen)
chart.add_series("Asia", [20, 35, 52, 74], color=Colors140.DarkOrange)

chart.draw(xy=(20.0, 30.0))
```

### 3.3. Customizable Ticks & Log Scale (Benchmark Example)

```python
from drawlib import canvas
from drawlib.charts import BarChart
from drawlib.colors import Colors140
from drawlib.types import Style

canvas.initialize()

chart = BarChart(
    title="Query Latency Benchmark",
    categories=["P50", "P95", "P99", "P99.9"],
    width=55.0,
    height=40.0,
)

# 1. Configure Value Axis (Log Scale & Custom Ticks)
chart.y_axis.scale = "log"
chart.y_axis.min_value = 1.0
chart.y_axis.max_value = 10000.0
chart.y_axis.ticks = [1, 10, 100, 1000, 10000]
chart.y_axis.format = "{:g} ms"

# 2. Appearance Customization
chart.y_axis.grid_style = Style(line_color=Colors140.LightSlateGray, line_style="dashed", line_width=0.8)
chart.y_axis.tick_label_style = Style(text_size=10, text_color=Colors140.DarkSlateGray)

# 3. Add Series
chart.add_series("PostgreSQL", [2.1, 15.4, 180.0, 3200.0], color=Colors140.CornflowerBlue)
chart.add_series("In-Memory Cache", [0.2, 0.5, 1.2, 8.5], color=Colors140.MediumSeaGreen)

chart.draw(xy=(20.0, 30.0))
```

### 3.4. Stacked Horizontal Bar Chart

```python
from drawlib import canvas
from drawlib.charts import BarChart
from drawlib.colors import Colors140

canvas.initialize()

chart = BarChart(
    title="Project Resource Allocation (Hours)",
    categories=["Sprint 1", "Sprint 2", "Sprint 3"],
    orientation="horizontal",  # horizontal bars
    bar_mode="stack",          # stacked segments
    width=65.0,
    height=35.0,
)

chart.add_series("Development", [120, 140, 110], color=Colors140.CornflowerBlue)
chart.add_series("Testing", [40, 50, 60], color=Colors140.LightCoral)
chart.add_series("Design", [30, 20, 15], color=Colors140.MediumPurple)

chart.draw(xy=(17.5, 32.5))
```

---

## 4. Detailed Component Design

### 4.1. Axis Model & Scaling Engine (`_common/_axis.py`)
- **`Axis` Class**:
  - `scale: Literal["linear", "log"] = "linear"`
  - `min_value: float | None = None`
  - `max_value: float | None = None`
  - `ticks: list[float] | None = None` (explicit tick positions)
  - `tick_step: float | None = None` (explicit tick intervals)
  - `format: str | Callable[[float], str] | None = None` (formatter function or string)
  - `unit: str = ""` (axis unit / label)
  - `show_grid: bool = True`
  - `grid_style: Style | None = None`
  - `show_axis_line: bool = True`
  - `line_style: Style | None = None`
  - `show_ticks: bool = True`
  - `tick_label_style: Style | None = None`
  - `tick_label_angle: float = 0.0`
- **Scaling Algorithms**:
  - `Linear`: Nice Numbers algorithm ($1, 2, 2.5, 5, 10 \times 10^n$).
  - `Logarithmic`: Power of 10 intervals ($10^0, 10^1, 10^2, 10^3, \dots$) with positive clamping.

### 4.2. Legend Auto-Layout Engine (`_common/_legend.py`)
- Automatically generates horizontal or vertical legend boxes for $\ge 2$ series.
- Color swatch chip + series name typography.

### 4.3. BarChart Container & Series (`bar_chart/_chart.py`, `_series.py`)
- **`BarSeries`**: Dataclass (`name`, `values`, `color`, `style`).
- **`BarChart`**:
  - `x_axis: Axis` (Category Axis for vertical, Value Axis for horizontal)
  - `y_axis: Axis` (Value Axis for vertical, Category Axis for horizontal)
  - Helper methods: `configure_y_axis(...)`, `configure_x_axis(...)`.
  - `bar_width_ratio: float = 0.7`
  - `r: float = 0.0` (bar corner radius)
  - `show_values: bool = False` (values displayed above/inside bars)

### 4.4. Rendering Pipeline (`bar_chart/_renderer.py`)
1. **Layer 0**: Background card and chart title.
2. **Layer 1**: Automatic Legend box.
3. **Layer 2**: Value axis gridlines and main axis line.
4. **Layer 3**: Bar geometries (grouped or stacked, linear or log scaled) + optional value labels.
5. **Layer 4**: Category labels and formatted value tick labels.

---

## 5. Implementation Roadmap

- [ ] **Phase 1: Common Infrastructure (`_charts/_common/`)**
  - Implement `_types.py`, `_axis.py` (with linear & log scale), `_legend.py`.
- [ ] **Phase 2: Bar Chart Core & Facade**
  - Implement `_series.py`, `_chart.py`, `_renderer.py`.
  - Expose `BarChart` and `Axis` in `drawlib.charts` and `src/drawlib/__init__.py`.
- [ ] **Phase 3: Unit & Integration Tests**
  - Implement `tests/test_bar_chart.py` (ticks, log scale, linear, grouped, stacked, horizontal).
  - Verify with `./dcli check all` and `pytest`.
- [ ] **Phase 4: Documentation & Guide**
  - Create `docs_src/charts/bar.md`.
  - Update `docs_src/index.md` navigation and release notes.
  - Compile docs via `./dcli docs build`.
