# Drawlib HeatmapChart & HeatmapOverlay Guidelines (`lib-charts-heatmap`)

`drawlib.charts.heatmap` provides two complementary heatmap visualization classes powered by `Style`-based multi-stop color palette interpolation (`styles=[Style, ...]` or `min_style=...`, `max_style=...`):
1. **`HeatmapChart`**: A 2D matrix/grid heatmap across categorical `x_categories` and `y_categories` with auto-contrasting in-cell numerical labels (`auto_contrast_text=True`), configurable cell gaps and corner rounding (`cell_gap`, `cell_r`), cell-level overrides (`set_cell`), and continuous colorbar (`draw_colorbar`) or discrete stepped legend (`draw_legend`).
2. **`HeatmapOverlay`**: A spatial thermal/hotspot overlay designed to be drawn directly on top of diagrams (`ClassDiagram`, `ArchitectureDiagram`, `ERDiagram`, `FlowDiagram`, `GeoMap`) or canvas regions in either `"smooth"` (2D Gaussian thermal gradient) or `"contour"` (concentric vector isoline rings) mode.

---

## 1. Conceptual Overview, Imports & Color Palette Stops

```python
from drawlib.charts.heatmap import (
    BlendMode,
    Cell,
    DrawDirection,
    FormatterType,
    HeatmapChart,
    HeatmapOverlay,
    Orientation,
    OverlayMode,
    Row,
    Spot,
)
```

### Multi-Stop Color Palette Configuration (`styles` vs. `min_style` / `max_style`)
Instead of a separate `ColorPalette` enum, both `HeatmapChart` and `HeatmapOverlay` construct their continuous color gradient directly from Drawlib `Style` tokens (extracting `shape_fill_color`, `line_color`, `shape_line_color`, or `text_color`):
- **Multi-Stop Palette (`styles: list[Style]`)**: Pass 2 or more `Style` objects ordered from minimum value (cool/neutral) to maximum value (hot/accent):
  - Cool-to-Accent Matrix Palette: `styles=[Styles.Neutral, Styles.PrimaryNeutral, Styles.PrimaryFlat, Styles.AccentFlat]`
  - Thermal Risk / Incident Palette: `styles=[Styles.PrimaryNeutral, Styles.WarningFlat, Styles.DangerFlat]`
- **Two-Stop Shorthand (`min_style` + `max_style`)**: Pass `min_style=Styles.Neutral, max_style=Styles.PrimaryFlat` when `styles` is omitted.
- Passing neither `styles` ($\ge 2$ items) nor `(min_style, max_style)` raises a `ValueError`.

---

## 2. `HeatmapChart`: 2D Matrix Grid Heatmap

### 2.1 Constructor Parameters (`HeatmapChart`)
All constructor arguments are **keyword-only** (`*`):

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| **`styles`** | `list[Style] \| None` | `None` | Sequence of $\ge 2$ `Style` stops from `min_value` to `max_value` (required unless `min_style` and `max_style` are both provided). |
| `min_style` / `max_style` | `Style \| None` | `None` | Two-stop minimum and maximum `Style` when `styles` is omitted. |
| `x_categories` | `list[str] \| None` | `None` | Column category labels along the horizontal X-axis. |
| `y_categories` | `list[str] \| None` | `None` | Row category labels along the vertical Y-axis (auto-populated from `add_row(name, ...)` when omitted). |
| `axis_line_style` | `Style \| None` | `None` | Optional style for outer matrix plot frame lines. |
| `width` / `height` | `float` | `80.0` / `55.0` | Total bounding box dimensions of the chart container in canvas units. |
| `min_value` / `max_value` | `float \| None` | `None` | Explicit color scale domain bounds. If `None`, inferred automatically from cell data. |
| `cell_gap` | `float` | `0.6` | Spacing gap between adjacent matrix cells in canvas units. |
| `cell_r` | `float` | `0.4` | Corner rounding radius for matrix cells. |
| `cell_line_style` | `Style \| None` | `None` | Optional style overriding cell border stroke. |
| `value_format` | `FormatterType` | `None` | Format string (e.g. `"{:.1f}%"`) or `Callable[[float], str]` for cell values. |
| `auto_contrast_text` | `bool` | `True` | Automatically switches cell value text color between dark and light based on cell background luminance. |
| `x_label_position` | `"bottom"` \| `"top"` | `"bottom"` | Placement of X-axis column labels. |
| `y_origin` | `"top"` \| `"bottom"` | `"top"` | Vertical ordering of rows (`"top"` places row `0` at the top; `"bottom"` places row `0` at the bottom). |
| `axis_text_style` | `Style \| None` | `None` | Style for row and column category labels. If `None`, category labels are omitted. |
| `value_text_style` | `Style \| None` | `None` | Style for numerical value labels inside cells. If `None`, in-cell values are omitted. |
| `background_style` | `Style \| None` | `None` | Outer chart background card style. If `None`, card is omitted. |
| `title` | `str` | `""` | Chart title text displayed at the top of the container. |
| `title_style` | `Style \| None` | `None` | Typography style for `title`. Required for the title to render. |

### 2.2 `HeatmapChart` Methods, Properties & Data Models (`Row`, `Cell`)
- **`add_row(name: str, values: Sequence[float | None], *, show: bool = True, draw_ratio: float = 1.0, draw_direction: DrawDirection = "left_to_right") -> Row`**:
  Appends a horizontal row of cell values (`None` renders an empty cell) and returns the mutable `Row` instance. If `y_categories` was not pre-populated, `name` is automatically appended to `y_categories`.
  - `draw_direction`: `"left_to_right"` *(default)* reveals cells across columns from left to right; `"bottom_to_top"` grows cells vertically from their bottom edge.
- **`set_data(values: Sequence[Sequence[float | None]], *, x_categories: Sequence[str] | None = None, y_categories: Sequence[str] | None = None) -> HeatmapChart`**:
  Replaces all matrix rows with a 2D array (`rows x columns`) and returns `self` for method chaining.
- **`set_cell(x: int | str, y: int | str, value: float | None, *, label: str = "", style: Style | None = None, show: bool = True) -> Cell`**:
  Sets or overrides a specific cell by 0-based index or category name (`x` column, `y` row), allowing custom text `label` or explicit `style` overrides.
- **`get_size() -> tuple[float, float]`**:
  Returns `(width, height)` of the heatmap chart container.
- **`draw(xy: tuple[float, float] = (0.0, 0.0), *, width: float | None = None, height: float | None = None, align: Literal["bottom_left", "center"] = "bottom_left", scale: float = 1.0) -> None`**:
  Renders the heatmap matrix onto the canvas anchored at `xy` (`"bottom_left"` or `"center"`), with optional temporary size overrides and proportional `scale`.
- **`draw_colorbar(xy: tuple[float, float], text_style: Style, *, length: float = 30.0, thickness: float = 2.2, orientation: Orientation = "horizontal", num_ticks: int = 5, value_format: FormatterType = None, label: str = "", border_style: Style | None = None, scale: float = 1.0) -> None`**:
  Renders a 64-segment continuous gradient colorbar anchored at bottom-left `xy`.
- **`draw_legend(xy: tuple[float, float], text_style: Style, orientation: Orientation = "vertical", swatch_width: float = 2.4, swatch_height: float = 1.2, item_gap: float = 4.0, *, num_steps: int = 5, labels: Sequence[str] | None = None, scale: float = 1.0) -> None`**:
  Renders discrete stepped color swatches (`num_steps` or explicit `labels` list).
- **Properties & Models**:
  - `chart.styles -> list[Style]`, `chart.color_stops -> list[Color]`, `chart.rows -> list[Row]`, `chart.cells -> list[Cell]`.
  - `Row(name: str, values: Sequence[float | None], *, show: bool = True, draw_ratio: float = 1.0, draw_direction: DrawDirection = "left_to_right")`.
  - `Cell(x: int, y: int, value: float | None, *, label: str = "", style: Style | None = None, show: bool = True)`.

---

## 3. `HeatmapOverlay`: Spatial & Diagram Thermal Hotspot Overlay

### 3.1 Constructor Parameters (`HeatmapOverlay`)
All constructor arguments are **keyword-only** (`*`):

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| **`styles`** | `list[Style] \| None` | `None` | Sequence of $\ge 2$ `Style` stops from cool (`min_value`) to hot (`max_value`). |
| `min_style` / `max_style` | `Style \| None` | `None` | Two-stop minimum and maximum `Style` when `styles` is omitted. |
| `width` / `height` | `float \| None` | `None` | Optional fixed overlay bounding dimensions. If `None`, auto-computed from spots via `get_bounds()`. |
| `mode` | `"smooth"` \| `"contour"` | `"smooth"` | Visual rendering mode (`OverlayMode`: 2D Gaussian thermal gradient or concentric vector isoline rings). |
| `blend_mode` | `"add"` \| `"max"` | `"add"` | Hotspot accumulation mode when smooth spots overlap (`BlendMode`). |
| `min_value` / `max_value` | `float` | `0.0` / `1.0` | Intensity scale bounds mapped to the color stops. |
| `default_radius` | `float` | `15.0` | Default hotspot influence radius in canvas units when `radius` is omitted in `add_spot()`. |
| `max_alpha` | `float` | `0.55` | Peak opacity (`0.05` to `1.0`) at hotspot centers so underlying diagrams stay legible. |
| `levels` | `int` | `4` | Number of concentric isoline rings per spot when `mode="contour"`. |
| `show_contour_lines` | `bool` | `True` | Whether to draw contour ring stroke outlines when `mode="contour"`. |
| `contour_line_width` | `float` | `1.0` | Stroke width of contour rings when `mode="contour"`. |
| `resolution` | `int` | `240` | Raster grid resolution along the longer axis when `mode="smooth"` (`32` to `1024`). |
| `value_format` | `FormatterType` | `None` | Optional format string or callable for spot value labels. |
| `value_text_style` | `Style \| None` | `None` | Optional style for spot annotation labels. |
| `border_style` | `Style \| None` | `None` | Optional style for drawing an outer bounding frame around the overlay region. |
| `title` / `title_style` | `str` / `Style \| None` | `""` / `None` | Optional title text and typography style above the overlay region. |

### 3.2 `HeatmapOverlay` Methods, Node `.xy` Resolution & Bounding Sizing
- **`add_spot(xy: tuple[float, float] | _HasXYProtocol, value: float = 1.0, radius: float | None = None, *, label: str = "", label_style: Style | None = None, style: Style | None = None, show: bool = True, draw_ratio: float = 1.0) -> Spot`**:
  Registers a thermal hotspot and returns the mutable `Spot` instance.
  - **Flexible `xy` Input**: Accepts either a raw `(x, y)` coordinate tuple (including coordinates returned by `GeoMap.get_area_xy(name)` or `GeoMap.lonlat_to_xy(lon, lat)`) **or any diagram node/element exposing an `.xy` attribute** (such as `ClassDiagram` `ClassNode`, `ArchitectureDiagram` `Node` or `NodeGroup`, `FlowDiagram` `Node`, etc.). When a nested `ArchitectureDiagram` `Node` or `NodeGroup` is passed, `add_spot()` automatically traverses `_parent_group` offsets and `center` to resolve its exact canvas center!
  - **`draw_ratio`**: Scales both the hotspot's effective intensity and influence radius from `0.0` to `1.0` for smooth thermal animations.
- **`get_bounds() -> tuple[float, float, float, float]`**:
  Computes the local enclosing bounding box `(min_x, min_y, max_x, max_y)` across all registered spots (expanding each spot by `radius * 1.25` in `"smooth"` mode or `radius * 1.05` in `"contour"` mode when `width`/`height` are not fixed).
- **`get_size() -> tuple[float, float]`**:
  Computes the overall `(width, height)` dimensions of the overlay region from `get_bounds()`.
- **`draw(xy: tuple[float, float] = (0.0, 0.0), *, width: float | None = None, height: float | None = None, align: Literal["bottom_left", "center"] = "bottom_left", scale: float = 1.0) -> None`**:
  Renders the thermal overlay onto the canvas. When overlaying on top of a diagram (`diagram.draw(xy=(0.0, 0.0))`), pass the exact same `xy` base coordinate (`overlay.draw(xy=(0.0, 0.0))`) so spot coordinates align 1-to-1.
- **`draw_colorbar(...) -> None`** and **`draw_legend(..., num_steps: int = 4, labels: Sequence[str] | None = None, scale: float = 1.0) -> None`**:
  Renders a continuous gradient colorbar or discrete stepped legend (`labels=["Low", "Moderate", "High", "Critical"]`).
- **Properties & Model**:
  - `overlay.styles -> list[Style]`, `overlay.color_stops -> list[Color]`, `overlay.spots -> list[Spot]`.
  - `Spot(xy: tuple[float, float], value: float = 1.0, radius: float = 15.0, *, label: str = "", label_style: Style | None = None, style: Style | None = None, show: bool = True, draw_ratio: float = 1.0)`.

---

## 4. Production Examples

### Example 4.1: 2D Matrix Heatmap with Continuous Colorbar (`HeatmapChart`)
```drawlib code=show align=center file=rules_heatmap_matrix.png caption="2D Matrix HeatmapChart with Auto-Contrast Labels and Colorbar"
from drawlib.canvas import save, setup
from drawlib.charts.heatmap import HeatmapChart
from drawlib.styles import Styles

setup(width=115, height=80)

chart = HeatmapChart(
    styles=[Styles.Neutral, Styles.PrimaryNeutral, Styles.PrimaryFlat, Styles.AccentFlat],
    x_categories=["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"],
    axis_line_style=Styles.Muted,
    axis_text_style=Styles.Muted.patch(text_size=10.0),
    value_text_style=Styles.BlackBold.patch(text_size=10.0),
    width=92.0,
    height=50.0,
    cell_gap=0.7,
    cell_r=0.5,
    title="API Gateway Error Rate (%) by Day & Hour",
    title_style=Styles.BlackBold.patch(text_size=13.0),
    value_format="{:.1f}%",
)
chart.add_row("Monday", [0.2, 0.1, 1.4, 3.8, 2.9, 0.8])
chart.add_row("Tuesday", [0.3, 0.2, 1.8, 4.5, 3.1, 0.9])
chart.add_row("Wednesday", [0.1, 0.2, 2.2, 6.4, 4.8, 1.2])
chart.add_row("Thursday", [0.4, 0.3, 1.5, 3.2, 2.4, 0.7])
chart.add_row("Friday", [0.5, 0.2, 2.9, 8.5, 5.2, 1.9])

chart.draw(xy=(12.0, 22.0))
chart.draw_colorbar(
    xy=(36.0, 8.0),
    text_style=Styles.Muted.patch(text_size=10.0),
    length=48.0,
    thickness=2.4,
    label="Error Rate (%)",
)
save()
```

### Example 4.2: `ClassDiagram` Thermal Hotspot Overlay (`HeatmapOverlay`)
```drawlib code=show align=center file=rules_heatmap_overlay_class.png caption="ClassDiagram Complexity & Incident Hotspot Overlay (mode='smooth')"
from drawlib.canvas import save, setup
from drawlib.charts.heatmap import HeatmapOverlay
from drawlib.diagrams.class_diagram import ClassDiagram, ClassNode
from drawlib.styles import Styles

setup(width=130, height=78)

diagram = ClassDiagram(
    node_style=Styles.Neutral,
    header_style=Styles.PrimaryNeutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=9.5),
    title="Domain Model Complexity & Incident Hotspot Overlay",
    title_style=Styles.BlackBold.patch(text_size=13.0),
)
ctrl = diagram.add(ClassNode("OrderController", width=30.0).add_method("submit", "req", "Result"), xy=(25.0, 42.0))
god = diagram.add(
    ClassNode("LegacyBillingManager", width=34.0)
    .add_attribute("global_state", "dict")
    .add_method("process_invoice", "inv", "bool")
    .add_method("reconcile_all", "tx", "void"),
    xy=(70.0, 42.0),
)
repo = diagram.add(ClassNode("InvoiceRepository", width=28.0).add_method("save", "row", "void"), xy=(112.0, 42.0))
diagram.connect(ctrl, god, "dependency", directed=True)
diagram.connect(god, repo, "association", directed=True)
diagram.draw(xy=(0.0, 0.0))

overlay = HeatmapOverlay(
    styles=[Styles.PrimaryNeutral, Styles.WarningFlat, Styles.DangerFlat],
    mode="smooth",
    max_alpha=0.55,
)
overlay.add_spot(god, value=0.95, radius=22.0)
overlay.add_spot(ctrl, value=0.40, radius=15.0)
overlay.draw(xy=(0.0, 0.0))
overlay.draw_colorbar(
    xy=(45.0, 7.0),
    text_style=Styles.Muted.patch(text_size=10.0),
    length=40.0,
    label="Hotspot Risk Score",
)
save()
```

---

## 5. Related Rules
- Charts Overview & Axis/Legend Architecture: `uv run drawlib rules show lib-charts-overview`
- Scatter & Bubble Charts: `uv run drawlib rules show lib-charts-scatter`
- Diagrams (`ClassDiagram`, `ArchitectureDiagram`): `uv run drawlib rules show lib-diagrams-overview`
