# Heatmap Chart & Spatial Thermal Overlay Design Plan

## 1. Overview & Motivation
Add heatmap capabilities to `drawlib.charts` (`src/drawlib/_charts/heatmap_chart/` and `src/drawlib/charts/heatmap.py`) covering two complementary visualization paradigms:
1. **`HeatmapChart` (Standard 2D Matrix / Grid Heatmap)**:
   - Visualizes 2D tabular/matrix quantities across categorical X-axis columns and Y-axis rows (e.g., correlation matrices, confusion matrices, time-of-day vs. day-of-week activity grids, service latency matrices).
2. **`HeatmapOverlay` (Spatial / Thermal Hotspot Overlay)**:
   - Renders spatial heat/intensity hotspots at arbitrary `(x, y)` coordinates on the canvas—for example, overlaying directly on top of a `ClassDiagram`, `ArchitectureDiagram`, or `FlowDiagram` to highlight high-risk classes, bug hotspots, cyclomatic complexity, or bottleneck nodes.
   - Supports two visual rendering modes:
     - `mode="smooth"`: Smooth continuous 2D Gaussian thermal gradient rendered with alpha transparency so underlying diagram nodes and labels remain legible.
     - `mode="contour"`: Concentric vector isoline rings (`circle`) with progressive color stops and optional contour strokes.

---

## 2. Architecture & File Layout

```text
src/drawlib/
├── _charts/
│   ├── __init__.py                     # Export HeatmapChart, HeatmapOverlay, OverlayMode, BlendMode
│   ├── _common/
│   │   └── _types.py                   # Add OverlayMode, BlendMode
│   └── heatmap_chart/
│       ├── __init__.py                 # Package exports
│       ├── _models.py                  # Row, Cell, Spot models + Style color-stop interpolation & colorbar renderer
│       ├── _chart.py                   # HeatmapChart container class
│       ├── _renderer.py                # Matrix grid renderer for HeatmapChart
│       ├── _overlay.py                 # HeatmapOverlay container class
│       └── _overlay_renderer.py        # Smooth Gaussian & Contour vector renderers for HeatmapOverlay
└── charts/
    ├── __init__.py                     # Export heatmap submodule
    └── heatmap.py                      # Public facade for drawlib.charts.heatmap
```

---

## 3. Color Scale Specification via `Style`
In accordance with Drawlib's unified `Style` token system:
- Both `HeatmapChart` and `HeatmapOverlay` accept:
  - `styles: list[Style] | None = None`: Ordered list of $\ge 2$ `Style` objects defining color stops from minimum to maximum value (e.g., `[Styles.Neutral, Styles.PrimaryNeutral, Styles.PrimaryFlat, Styles.AccentFlat]`).
  - `min_style: Style | None = None` and `max_style: Style | None = None`: Convenience 2-stop specification when `styles` is omitted.
- Color extraction priority from each `Style` stop:
  1. `style.shape_fill_color` (when non-transparent)
  2. `style.line_color`
  3. `style.shape_line_color`
  4. `style.text_color`
- Multi-stop piecewise linear RGBA interpolation maps normalized value $t \in [0.0, 1.0]$ across the $N$ stops.

---

## 4. `HeatmapChart` Specification
- **Constructor Parameters**:
  - `styles: list[Style] | None = None`, `min_style: Style | None = None`, `max_style: Style | None = None`
  - `x_categories: list[str] | None = None`, `y_categories: list[str] | None = None`
  - `axis_line_style: Style | None = None`
  - `width: float = 80.0`, `height: float = 55.0`
  - `min_value: float | None = None`, `max_value: float | None = None`
  - `cell_gap: float = 0.6`, `cell_r: float = 0.4`, `cell_line_style: Style | None = None`
  - `value_format: FormatterType = None`, `auto_contrast_text: bool = True`
  - `x_label_position: Literal["bottom", "top"] = "bottom"`, `y_origin: Literal["top", "bottom"] = "top"`
  - `axis_text_style: Style | None = None`, `value_text_style: Style | None = None`, `background_style: Style | None = None`
  - `title: str = ""`, `title_style: Style | None = None`
- **Methods**:
  - `add_row(name: str, values: list[float | None], *, show: bool = True, draw_ratio: float = 1.0, draw_direction: DrawDirection = "left_to_right") -> Row`
  - `set_data(values: list[list[float | None]], *, x_categories: list[str] | None = None, y_categories: list[str] | None = None) -> HeatmapChart`
  - `set_cell(x: int | str, y: int | str, value: float | None, *, label: str = "", style: Style | None = None, show: bool = True) -> Cell`
  - `get_size() -> tuple[float, float]`
  - `draw(xy=(0.0, 0.0), *, width=None, height=None, align="bottom_left", scale=1.0) -> None`
  - `draw_colorbar(xy, text_style, *, length=30.0, thickness=2.2, orientation="horizontal", num_ticks=5, format=None, label="", border_style=None, scale=1.0) -> None`
  - `draw_legend(xy, text_style, orientation="vertical", swatch_width=2.4, swatch_height=1.2, item_gap=4.0, *, num_steps=5, scale=1.0) -> None`

---

## 5. `HeatmapOverlay` Specification
- **Constructor Parameters**:
  - `styles: list[Style] | None = None`, `min_style: Style | None = None`, `max_style: Style | None = None`
  - `width: float | None = None`, `height: float | None = None`
  - `mode: OverlayMode = "smooth"` (`"smooth"` or `"contour"`)
  - `blend_mode: BlendMode = "add"` (`"add"` or `"max"` for overlapping smooth hotspots)
  - `min_value: float = 0.0`, `max_value: float = 1.0`
  - `default_radius: float = 15.0`, `max_alpha: float = 0.55`
  - `levels: int = 4`, `show_contour_lines: bool = True`, `contour_line_width: float = 1.0`
  - `resolution: int = 240`
  - `value_format: FormatterType = None`, `value_text_style: Style | None = None`
  - `border_style: Style | None = None`, `title: str = ""`, `title_style: Style | None = None`
- **Methods**:
  - `add_spot(xy: tuple[float, float], value: float = 1.0, radius: float | None = None, *, label: str = "", label_style: Style | None = None, style: Style | None = None, show: bool = True, draw_ratio: float = 1.0) -> Spot`
  - `get_bounds() -> tuple[float, float, float, float]`
  - `get_size() -> tuple[float, float]`
  - `draw(xy=(0.0, 0.0), *, width=None, height=None, align="bottom_left", scale=1.0) -> None`
  - `draw_colorbar(...) -> None`
  - `draw_legend(...) -> None`

---

## 6. Verification & Dogfooding Plan
1. Unit & integration tests in `tests/drawlib/charts/test_heatmap_chart.py` covering `HeatmapChart` and `HeatmapOverlay` (including overlaying on `ClassDiagram`).
2. Static analysis via `./dcli code-check all`.
3. Update embedded agent rules (`src/drawlib/_rules/lib_charts.md`, `api.md`, `overview.md`) and documentation examples.
4. Visual inspection with coordinate grid (`-g`) via `view_file`.
