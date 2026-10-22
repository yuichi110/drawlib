# HeatmapChart & HeatmapOverlay: 2D Matrix Grids & Diagram Thermal Overlays

`drawlib.charts.heatmap` provides two complementary heatmap visualization classes styled via `Style` color-stop interpolation (`styles=[Style, ...]` or `min_style=...`, `max_style=...`):
1. **`HeatmapChart`**: A standard 2D matrix/grid heatmap across categorical `x_categories` and `y_categories` with auto-contrasting in-cell numerical labels, configurable cell gaps and corner rounding (`cell_gap`, `cell_r`), and continuous colorbar (`draw_colorbar`) or stepped legend (`draw_legend`).
2. **`HeatmapOverlay`**: A spatial thermal/hotspot overlay designed to be drawn directly on top of diagrams (such as `ClassDiagram`, `ArchitectureDiagram`, or `FlowDiagram`) to highlight high-risk classes, cyclomatic complexity, bug density, or performance bottlenecks in either `"smooth"` (2D Gaussian thermal gradient) or `"contour"` (concentric vector isoline rings) mode.

---

## 1. Overview & Topologies

```drawlib align=center code=fold file=heatmap_topologies_overview.png caption="Heatmap Topologies: 2D Matrix HeatmapChart vs. ClassDiagram Thermal HeatmapOverlay"
from drawlib.canvas import save, setup
from drawlib.charts.heatmap import HeatmapChart, HeatmapOverlay
from drawlib.diagrams.class_diagram import ClassDiagram, ClassNode
from drawlib.styles import Styles

setup(width=136, height=62)

# Left: 2D Matrix HeatmapChart
matrix = HeatmapChart(
    styles=[Styles.Neutral, Styles.PrimaryNeutral, Styles.PrimaryFlat, Styles.AccentFlat],
    x_categories=["00h", "06h", "12h", "18h"],
    axis_line_style=Styles.Muted,
    axis_text_style=Styles.Muted.patch(text_size=10.0),
    value_text_style=Styles.BlackBold.patch(text_size=10.0),
    width=58.0,
    height=40.0,
    title="1. 2D Matrix HeatmapChart",
    title_style=Styles.BlackBold.patch(text_size=11.5),
    value_format="{:.1f}%",
)
matrix.add_row("API", [0.4, 1.2, 4.8, 2.1])
matrix.add_row("Auth", [0.2, 0.8, 2.5, 1.4])
matrix.add_row("Billing", [0.5, 1.9, 7.6, 3.8])
matrix.draw(xy=(4.0, 16.0))
matrix.draw_colorbar(
    xy=(14.0, 6.5),
    text_style=Styles.Muted.patch(text_size=9.5),
    length=38.0,
    thickness=2.0,
)

# Right: Spatial Thermal HeatmapOverlay on ClassDiagram
diag = ClassDiagram(
    node_style=Styles.Neutral,
    header_style=Styles.PrimaryNeutral,
    edge_style=Styles.Primary,
    edge_text_style=Styles.Muted.patch(text_size=9.5),
    title="2. ClassDiagram + HeatmapOverlay",
    title_style=Styles.BlackBold.patch(text_size=11.5),
)
c_api = diag.add(ClassNode("OrderService", width=26.0).add_method("submit", "req", "bool"), xy=(82.0, 36.0))
c_god = diag.add(
    ClassNode("LegacyBillingGodClass", width=32.0)
    .add_attribute("flags", "dict")
    .add_method("process_all", "tx", "void"),
    xy=(116.0, 36.0),
)
diag.connect(c_api, c_god, "dependency", directed=True)
diag.draw(xy=(0.0, 0.0))

overlay = HeatmapOverlay(
    styles=[Styles.PrimaryNeutral, Styles.WarningFlat, Styles.DangerFlat],
    mode="smooth",
    max_alpha=0.55,
)
overlay.add_spot(c_god, value=0.95, radius=19.0)
overlay.add_spot(c_api, value=0.35, radius=14.0)
overlay.draw(xy=(0.0, 0.0))
overlay.draw_colorbar(
    xy=(82.0, 6.5),
    text_style=Styles.Muted.patch(text_size=9.5),
    length=38.0,
    thickness=2.0,
)

save()
```

---

## 2. Standard 2D Matrix Heatmap (`HeatmapChart`)

`HeatmapChart` maps a 2D grid of values across `x_categories` and `y_categories` into interpolated `Style` colors, automatically adjusting cell label contrast (`auto_contrast_text=True`) so numbers stay legible across both light and dark cells:

```drawlib align=center code=show file=heatmap_matrix_latency.png caption="Service Latency & Error Correlation Matrix with Continuous Colorbar"
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
    title="Production Gateway Error Rate (%) by Day & Hour",
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

---

## 3. Diagram Hotspot Overlay (`HeatmapOverlay`: Smooth vs. Contour)

When analyzing codebases, architecture topologies, or UML class models, `HeatmapOverlay` lets you raise the visual temperature over fragile or complex components (`add_spot(class_node, value=..., radius=...)`). You can choose between **`mode="smooth"`** (continuous Gaussian thermal glow) and **`mode="contour"`** (concentric vector isoline rings):

```drawlib align=center code=show file=heatmap_overlay_class_diagram.png caption="Highlighting High-Risk Classes on a UML ClassDiagram (Smooth Thermal Gradient Mode)"
from drawlib.canvas import save, setup
from drawlib.charts.heatmap import HeatmapOverlay
from drawlib.diagrams.class_diagram import ClassDiagram, ClassNode
from drawlib.styles import Styles

setup(width=136, height=70)

# Build UML ClassDiagram
diagram = ClassDiagram(
    node_style=Styles.Neutral,
    header_style=Styles.PrimaryNeutral,
    edge_style=Styles.Primary,
    edge_text_style=Styles.Muted.patch(text_size=10.0),
    title="Order Subsystem: Cyclomatic Complexity & Bug Hotspot Analysis",
    title_style=Styles.BlackBold.patch(text_size=13.0),
)
ctrl = diagram.add(
    ClassNode("OrderController", width=30.0)
    .add_method("create_order", "req", "Response")
    .add_method("cancel_order", "id", "bool"),
    xy=(26.0, 40.0),
)
god_cls = diagram.add(
    ClassNode("LegacyPaymentProcessor", width=36.0)
    .add_attribute("retry_buffer", "list")
    .add_attribute("global_locks", "dict")
    .add_method("execute_charge", "order", "Receipt")
    .add_method("reconcile_ledger", "batch", "void")
    .add_method("handle_fallback", "err", "void"),
    xy=(72.0, 40.0),
)
repo = diagram.add(
    ClassNode("LedgerRepository", width=28.0)
    .add_method("save_entry", "row", "void"),
    xy=(116.0, 40.0),
)

diagram.connect(ctrl, god_cls, "dependency", label="delegates", directed=True)
diagram.connect(god_cls, repo, "association", label="writes", directed=True)
diagram.draw(xy=(0.0, 0.0))

# Overlay Thermal Hotspots directly onto ClassNode coordinates
overlay = HeatmapOverlay(
    styles=[Styles.PrimaryNeutral, Styles.WarningFlat, Styles.DangerFlat],
    mode="smooth",
    max_alpha=0.55,
)
overlay.add_spot(god_cls, value=0.95, radius=21.0)
overlay.add_spot(ctrl, value=0.45, radius=15.0)
overlay.add_spot(repo, value=0.18, radius=12.0)
overlay.draw(xy=(0.0, 0.0))

overlay.draw_colorbar(
    xy=(46.0, 7.0),
    text_style=Styles.Muted.patch(text_size=10.0),
    length=44.0,
    thickness=2.2,
    label="Complexity / Bug Risk Score",
)

save()
```

---

## 4. Concentric Isoline Ring Overlay (`mode="contour"`)

For crisp vector diagrams or print documentation where discrete isoline rings are preferred over continuous gradients, set `mode="contour"` and `levels=4`:

```drawlib align=center code=show file=heatmap_overlay_contour_mode.png caption="Concentric Vector Isoline Rings (mode='contour') Highlighting Blast Radius on a ClassDiagram"
from drawlib.canvas import save, setup
from drawlib.charts.heatmap import HeatmapOverlay
from drawlib.diagrams.class_diagram import ClassDiagram, ClassNode
from drawlib.styles import Styles

setup(width=136, height=72)

diagram = ClassDiagram(
    node_style=Styles.Neutral,
    header_style=Styles.PrimaryNeutral,
    edge_style=Styles.Primary,
    edge_text_style=Styles.Muted.patch(text_size=10.0),
    title="Change Blast Radius Analysis (mode='contour')",
    title_style=Styles.BlackBold.patch(text_size=13.0),
    margin=14.0,
)
auth_cls = diagram.add(
    ClassNode("AuthSessionStore", width=30.0)
    .add_attribute("token_cache", "dict")
    .add_method("verify_token", "jwt", "User"),
    xy=(32.0, 38.0),
)
core_cls = diagram.add(
    ClassNode("CoreSecurityContext", width=34.0)
    .add_attribute("permissions", "set")
    .add_method("authorize", "ctx", "bool")
    .add_method("audit_event", "ev", "void"),
    xy=(92.0, 38.0),
)
diagram.connect(auth_cls, core_cls, "association", label="validates via", directed=True)
diagram.draw(xy=(0.0, 0.0))

overlay = HeatmapOverlay(
    styles=[Styles.PrimaryNeutral, Styles.WarningFlat, Styles.DangerFlat],
    mode="contour",
    levels=4,
    max_alpha=0.45,
)
overlay.add_spot(core_cls, value=0.95, radius=19.0)
overlay.add_spot(auth_cls, value=0.55, radius=15.0)
overlay.draw(xy=(0.0, 0.0))

overlay.draw_legend(
    xy=(42.0, 7.0),
    text_style=Styles.Muted.patch(text_size=10.0),
    orientation="horizontal",
    labels=["Low", "Moderate", "High", "Critical"],
)

save()
```
