::: block xy=(1700, 1008) width=140 height=32
```drawlib file=page.svg
import utils
utils.draw_page_number()
```
:::

::: block xy=(80, 1010) width=900 height=30 font_size=15px
*Drawlib — Illustration & Documentation as Code*
:::

::: block xy=(80, 36) width=1760 height=72
# Tables, SourceCode, Calendars & GeoMap
:::

::: block xy=(80, 130) width=1760 height=815
```drawlib file=tables_code_geomap.svg
from drawlib.canvas import clear, save, setup
from drawlib.icons import phosphor
from drawlib.lines import line_curved
from drawlib.shapes import circle, rectangle
from drawlib.smartarts import GeoMap, Panel, SourceCode, SourceCodeStyles, Table, WeekCalendar
from drawlib.styles import Colors, Styles
from drawlib.text import text

clear()
setup(width=176, height=81)

# 1. Top-Left Panel: Table (4x3 Benchmark Matrix)
p_tl = Panel(
    "Table — Benchmark Matrix",
    "Zebra Rows",
    style=Styles.Neutral.patch(shape_r=2.0),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=14.0),
    description_style=Styles.Muted.patch(text_size=11.2),
    icon=phosphor.table,
    icon_style=Styles.PrimaryBold,
    header_height=6.4,
)
p_tl.draw((1.5, 42.2), width=84.5, height=37.5)
tl_xy, tl_w, tl_h = p_tl.get_content_box((1.5, 42.2), width=84.5, height=37.5, padding=(3.2, 2.4))

tbl = Table(
    cell_style=Styles.White,
    text_style=Styles.Dark.patch(text_size=11.6),
    header_cell_style=Styles.PrimaryFlat,
    header_text_style=Styles.WhiteBold.patch(text_size=11.8),
    border_style=Styles.MutedThin,
)
tbl.set_style_cell_evenodd(
    even_color=Colors.Light,
    even_text_style=Styles.Dark.patch(text_size=11.6),
    odd_color=Colors.White,
    odd_text_style=Styles.Dark.patch(text_size=11.6),
)
tbl.set_style_cell_header(
    background_color=Colors.Primary,
    text_style=Styles.WhiteBold.patch(text_size=11.8),
)
tbl.set_style_cell(
    background_color=Colors.White,
    text_style=Styles.PrimaryBold.patch(text_size=11.6),
    rows=[1, 2, 3],
    columns=[2],
)
row_h = tl_h / 4.0
tbl.draw_flexible(
    tl_xy,
    column_widths=[34.5, 23.6, 20.0],
    row_heights=[row_h, row_h, row_h, row_h],
    data=[
        ["Output Target", "Format", "Cold Build"],
        ["16:9 Slide Deck", "HTML / PDF", "0.42 s"],
        ["Documentation Site", "Multi-Page", "0.65 s"],
        ["Standalone Diagram", "SVG / PNG", "0.18 s"],
    ],
    align="bottom_left",
)

# 2. Top-Right Panel: SourceCode inside Window Chrome Panel
p_tr = Panel(
    "SourceCode — Syntax Box",
    "card_demo.py",
    style=Styles.Neutral.patch(shape_r=2.0),
    header_style=Styles.DarkFlat,
    text_style=Styles.WhiteBold.patch(text_size=13.6),
    description_style=Styles.White.patch(text_size=11.0),
    dot_styles=(
        Styles.DangerFlat.patch(shape_line_width=0),
        Styles.WarningFlat.patch(shape_line_width=0),
        Styles.SuccessFlat.patch(shape_line_width=0),
    ),
    header_variant="window",
    header_height=5.8,
)
p_tr.draw((90.0, 42.2), width=84.5, height=37.5)
tr_xy, tr_w, _ = p_tr.get_content_box(
    (90.0, 42.2), width=84.5, height=37.5, padding=(3.2, 1.4), content_align="center"
)

snippet = """from drawlib.canvas import save, setup
from drawlib.shapes import rectangle
from drawlib.styles import Styles
setup(width=120, height=60)
rectangle((60, 30), 80, 36, Styles.Primary)
save("card.svg")"""

code_styles = SourceCodeStyles.get("dark", font_lang="en", text_size=9.2)
SourceCode.draw(
    xy=tr_xy,
    width=tr_w,
    code=snippet,
    styles=code_styles,
    code_lang="python",
    show_linenum=True,
    align="center",
)

# 3. Bottom-Left Panel: WeekCalendar (Sprint Release Milestones)
p_bl = Panel(
    "WeekCalendar — Sprint Plan",
    "ISO 8601",
    style=Styles.Neutral.patch(shape_r=2.0),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=14.0),
    description_style=Styles.Muted.patch(text_size=11.2),
    icon=phosphor.calendar_blank,
    icon_style=Styles.PrimaryBold,
    header_height=6.4,
)
p_bl.draw((1.5, 1.5), width=84.5, height=37.5)
bl_xy, bl_w, bl_h = p_bl.get_content_box((1.5, 1.5), width=84.5, height=37.5, padding=(2.8, 2.0))

wcal = WeekCalendar(
    start_date="2026-11-02",
    end_date="2026-11-06",
    start_hour=9,
    end_hour=18,
    hour_step=3,
    show_all_day=False,
    title="",
    lang="en",
    cell_style=Styles.White,
    text_style=Styles.Dark.patch(text_size=10.5),
    header_style=Styles.SecondaryNeutral,
    header_text_style=Styles.DarkBold.patch(text_size=10.8),
    border_style=Styles.MutedThin,
    event_style=Styles.SecondaryNeutral,
    event_text_style=Styles.DarkBold.patch(text_size=10.6),
)
wcal.add(
    "2026-11-02 09:00",
    "2026-11-03 13:30",
    text="RC Freeze & Spec",
    span_mode="box",
    style=Styles.PrimaryNeutral,
)
wcal.add("2026-11-03 13:30", "2026-11-04 17:30", text="QA & Grid Audit", span_mode="box")
wcal.add(
    "2026-11-05 09:30",
    "2026-11-06 17:30",
    text="v1.0 Launch",
    span_mode="box",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=11.0),
)
wcal.draw(bl_xy, width=bl_w, height=bl_h)

# 4. Bottom-Right Panel: GeoMap (Multi-Region Deployment)
p_br = Panel(
    "GeoMap — Global Regions",
    "US, EU & JP",
    style=Styles.Neutral.patch(shape_r=2.0),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=14.0),
    description_style=Styles.Muted.patch(text_size=11.2),
    icon=phosphor.globe,
    icon_style=Styles.PrimaryBold,
    header_height=6.4,
)
p_br.draw((90.0, 1.5), width=84.5, height=37.5)
br_xy, br_w, br_h = p_br.get_content_box((90.0, 1.5), width=84.5, height=37.5, padding=(2.8, 2.0))

world = GeoMap(
    GeoMap.World.All,
    area_style=Styles.White,
    background_style=Styles.PrimaryNeutral.patch(shape_r=1.5),
)
world.set_area_styles(["Germany", "France", "United Kingdom", "Singapore", "Australia"], Styles.SecondaryFlat)
world.set_area_styles(["United States", "Japan"], Styles.PrimaryFlat)
world.draw(br_xy, width=br_w, height=br_h, lon_range=(-135, 158), lat_range=(-44, 72))

us_xy = world.lonlat_to_xy(-98.0, 38.0)
eu_xy = world.lonlat_to_xy(10.0, 50.0)
jp_xy = world.lonlat_to_xy(139.7, 35.7)

line_curved(us_xy, eu_xy, bend=-0.18, arrow_head="<->", style=Styles.PrimaryBold)
line_curved(eu_xy, jp_xy, bend=-0.18, arrow_head="<->", style=Styles.PrimaryBold)

for pt, lbl, dy in [(us_xy, "US-West", -4.2), (eu_xy, "EU-West", -4.2), (jp_xy, "Tokyo", -4.2)]:
    circle(pt, radius=1.1, style=Styles.AccentFlat)
    rectangle((pt[0], pt[1] + dy), width=14.8, height=4.2, style=Styles.DarkFlat.patch(shape_r=1.0))
    text((pt[0], pt[1] + dy), lbl, style=Styles.WhiteBold.patch(text_size=10.2))

save()
```
:::

::: note
Four specialized data and spatial SmartArts round out the toolkit:
- **`Table`** supports zebra striping (`set_style_cell_evenodd`), distinct headers (`set_style_cell_header`), and flexible per-column widths (`draw_flexible`).
- **`SourceCode`** tokenizes 20+ languages via Pygments into crisp vector glyphs with CJK-safe font options and dark/light editor themes.
- **`WeekCalendar`** (alongside `MonthCalendar` and `DayCalendar`) renders ISO 8601 sprint schedules with multi-day `span_mode="box"` blocks.
- **`GeoMap`** ships built-in world, regional, 215-country, and 16-city vector maps with `lonlat_to_xy()` coordinate projection for overlaying live replication arcs and pins.
:::
