::: block (1700, 1010) (140, 30) z:10
```drawlib file:page.svg
import utils
utils.draw_page_number()
```
:::

::: block (0, 0) (1920, 1080)
```drawlib file:full_canvas_showcase.svg
import utils
from drawlib.canvas import clear, save, setup
from drawlib.charts.bar import BarChart
from drawlib.diagrams.architecture import ArchitectureDiagram, GcpIcon, Node, NodeGroup, PhosphorIcon
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.slide import current_slide
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=192.0, height=108.0)

# 1. Full-bleed canvas backdrop
rectangle(
    (96.0, 54.0),
    width=192.0,
    height=108.0,
    style=Styles.WhiteFlat.patch(shape_fill_color=(248, 250, 252)),
)

# 2. Top Full-Bleed Dark Slate Header Banner
rectangle(
    (96.0, 98.5),
    width=192.0,
    height=19.0,
    style=Styles.WhiteFlat.patch(shape_fill_color=(15, 23, 42)),
)
rectangle(
    (96.0, 89.0),
    width=192.0,
    height=1.2,
    style=Styles.PrimaryFlat,
)
text(
    (8.0, 101.0),
    "Full-Canvas Pure Stage  —  ::: block (0, 0) (1920, 1080)  +  setup(width=192, height=108)",
    style=Styles.WhiteBold.patch(text_size=12.8, text_halign="left"),
)
text(
    (8.0, 94.0),
    "100% Programmatic Slide Design: Header Banner, Cloud ArchitectureDiagram, BarChart & KPI Cards on One Unified Vector Canvas",
    style=Styles.White.patch(text_size=9.2, text_color=(199, 210, 254), text_halign="left"),
)
rectangle(
    (174.0, 98.5),
    width=24.0,
    height=7.5,
    r=2.0,
    style=Styles.PrimaryFlat,
    text=f"Pure SVG ({current_slide.text})",
    text_style=Styles.WhiteBold.patch(text_size=8.8),
)

# 3. Left Zone: ArchitectureDiagram Card (X: 6..94, Y: 12..84)
rectangle((50.0, 48.0), width=88.0, height=72.0, r=2.5, style=Styles.White)
text((50.0, 79.0), "1. Cloud Topology (drawlib.diagrams.architecture)", style=Styles.DarkBold.patch(text_size=10.5))

diag = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=8.0),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=7.5),
    node_card_style=Styles.White,
)
vpc = diag.add(
    NodeGroup(title="Regional Cloud VPC", padding=5.5, style=Styles.PrimaryNeutral),
    xy=(22.0, 6.0),
)
n_user = diag.add(Node((14, 13), "Users", icon=PhosphorIcon.USERS, icon_size=6.5, card_style=Styles.Neutral), xy=(7.0, 22.0))
n_lb = vpc.add(Node((15, 13), "Cloud LB", icon=GcpIcon.CLOUD_LOAD_BALANCING, icon_size=6.5), xy=(9.0, 16.0))
n_run = vpc.add(Node((15, 13), "Cloud Run", icon=GcpIcon.CLOUD_RUN, icon_size=6.5), xy=(28.0, 16.0))
n_sql = vpc.add(Node((15, 13), "Cloud SQL", icon=GcpIcon.CLOUD_SQL, icon_size=6.5), xy=(47.0, 24.0))
n_bq = vpc.add(Node((15, 13), "BigQuery", icon=GcpIcon.BIGQUERY, icon_size=6.5), xy=(47.0, 8.0))

diag.connect(n_user, n_lb, label="HTTPS", padding=1.0)
diag.connect(n_lb, n_run, label="gRPC", padding=1.0)
diag.connect(n_run, n_sql, label="OLTP", padding=1.0)
diag.connect(n_run, n_bq, label="OLAP", padding=1.0)
diag.draw(xy=(8.0, 16.0))

# 4. Top-Right Zone: Quantitative BarChart Card (X: 98..186, Y: 49..84)
rectangle((142.0, 66.5), width=88.0, height=35.0, r=2.5, style=Styles.White)
chart = BarChart(
    axis_line_style=Styles.Dark,
    categories=["v0.1", "v0.2", "v0.3", "v0.4"],
    width=76.0,
    height=27.0,
    title="2. Build Throughput (Diagrams / Sec) — drawlib.charts.bar",
    title_style=Styles.DarkBold.patch(text_size=9.2),
    r=0.8,
    bar_width_ratio=0.58,
    axis_text_style=Styles.Muted.patch(text_size=8.0),
    grid_style=Styles.MutedDashed,
    value_text_style=Styles.PrimaryBold.patch(text_size=7.8),
    value_format="{:.0f}/s",
)
chart.configure_y_axis(min_value=0, max_value=150, tick_step=50)
chart.add_series("Throughput", [28.0, 54.0, 86.0, 112.0], style=Styles.PrimaryFlat)
chart.draw(xy=(104.0, 50.5))

# 5. Bottom-Right Zone: 3 KPI Callout Cards (X: 98..186, Y: 12..45)
rectangle((142.0, 28.5), width=88.0, height=33.0, r=2.5, style=Styles.White)
text((142.0, 40.5), "3. Programmatic KPI Badges & Cross-Zone Connectors", style=Styles.DarkBold.patch(text_size=10.0))

kpis = [
    ("192 x 108", "Cartesian Grid", Styles.PrimaryFlat, Styles.WhiteBold),
    ("100% Vector", "Zero Pixel Blur", Styles.SecondaryNeutral, Styles.DarkBold),
    ("< 1 ms", "Warm SQLite Hit", Styles.BlueNeutral, Styles.DarkBold),
]
for idx, (val_s, lbl_s, st_card, st_txt) in enumerate(kpis):
    kx = 114.5 + idx * 27.5
    rectangle((kx, 24.5), width=24.5, height=18.0, r=1.8, style=st_card)
    text((kx, 27.5), val_s, style=st_txt.patch(text_size=11.0))
    sub_st = Styles.White.patch(text_size=8.0) if idx == 0 else Styles.MutedBold.patch(text_size=8.0)
    text((kx, 20.0), lbl_s, style=sub_st)

# Cross-zone arrow connecting Left Architecture Card to Right KPI Card
line((94.0, 28.5), (98.0, 28.5), arrow_head="->", style=Styles.PrimaryBold)

# 6. Bottom Footer Strip drawn directly on canvas
text(
    (8.0, 4.5),
    "Chapter 6: Documentation & Slide Engine — Full-Canvas Pure Stage (::: block (0, 0) (1920, 1080))",
    style=Styles.Muted.patch(text_size=8.2, text_halign="left"),
)

save()
```
:::

::: note
- This entire slide is rendered from a single `::: block (0, 0) (1920, 1080)` container with `setup(width=192.0, height=108.0)`.
- Because `ArchitectureDiagram`, `BarChart`, primitive cards, and `current_slide.text` all share the same Drawlib canvas, you can draw arrows directly between an architecture diagram on the left and a chart or KPI panel on the right!
:::
