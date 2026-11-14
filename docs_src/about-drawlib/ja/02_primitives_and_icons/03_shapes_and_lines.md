::: block xy=(1700, 1008) width=140 height=32
```drawlib file=page.svg
import utils
utils.draw_page_number()
```
:::

::: block xy=(80, 1010) width=900 height=30 font_size=15px
*Drawlib — コードで描く図解と技術ドキュメント*
:::

::: block xy=(80, 36) width=1760 height=72
# 43種のプリミティブ図形とコネクタ
:::

::: block xy=(80, 130) width=1760 height=815
```drawlib file=shapes_lines_catalog_ja.svg
from drawlib.canvas import clear, setup
from drawlib.lines import line, lines, lines_bezier, lines_curved
from drawlib.shapes import (
    arrow,
    arrow_arc,
    bubblespeech,
    checkmark,
    chevron,
    circle,
    clock,
    cloud,
    cube,
    cylinder,
    document,
    forbidden,
    funnel,
    gear,
    lightning,
    parallelogram,
    pin,
    rectangle,
    regularpolygon,
    rhombus,
    ribbon,
    shield,
    star,
    tag,
)
from drawlib.smartarts import Panel
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=176, height=82)

pw, ph, hh = 55.4, 38.0, 7.0
cols = [1.5, 60.3, 119.1]
rows = [42.5, 1.5]
lbl_st = Styles.Dark.patch(text_size=11.8)

titles = [
    ["1. 基本図形・多角形", "2. ブロック矢印・フロー", "3. 3D・コンテナ図形"],
    ["4. バッジ・吹き出し", "5. ドメイン記号", "6. 線・折れ線・曲線コネクタ"],
]
for r_idx, y0 in enumerate(rows):
    h_st = Styles.PrimaryNeutral if r_idx == 0 else Styles.SecondaryNeutral
    for c_idx, x0 in enumerate(cols):
        Panel(
            titles[r_idx][c_idx],
            style=Styles.Neutral.patch(shape_r=1.8),
            header_style=h_st,
            text_style=Styles.DarkBold.patch(text_size=14.6),
            header_height=hh,
        ).draw(xy=(x0, y0), width=pw, height=ph)

st_pn = Styles.PrimaryNeutral.patch(shape_line_width=1.8)
st_sn = Styles.SecondaryNeutral.patch(shape_line_width=1.8)
st_an = Styles.AccentNeutral.patch(shape_line_width=1.8)

# 1. Basic & Polygons (col 0, row 0)
x0, y0 = cols[0], rows[0]
ty, by = y0 + 23.0, y0 + 9.8
rectangle((x0 + 10.2, ty), width=7.8, height=5.4, style=st_pn.patch(shape_r=1.0))
text((x0 + 10.2, ty - 5.8), "rectangle", style=lbl_st)
circle((x0 + 27.7, ty), radius=3.0, style=st_sn)
text((x0 + 27.7, ty - 5.8), "circle", style=lbl_st)
rhombus((x0 + 45.2, ty), width=7.8, height=5.8, style=st_pn)
text((x0 + 45.2, ty - 5.8), "rhombus", style=lbl_st)
regularpolygon((x0 + 18.2, by), num_vertex=6, radius=3.2, style=st_sn)
text((x0 + 18.2, by - 5.8), "regularpolygon", style=lbl_st)
star((x0 + 37.2, by), num_vertex=5, radius_ext=3.4, radius_int=1.5, style=Styles.PrimaryFlat)
text((x0 + 37.2, by - 5.8), "star", style=lbl_st)

# 2. Block Arrows & Flow (col 1, row 0)
x0, y0 = cols[1], rows[0]
chevron((x0 + 15.0, ty), width=9.0, height=5.4, corner_angle=55, style=Styles.PrimaryFlat)
text((x0 + 15.0, ty - 5.8), "chevron", style=lbl_st)
arrow((x0 + 35.4, ty), (x0 + 45.4, ty), tail_width=2.3, head_width=5.0, head_length=3.2, style=st_sn)
text((x0 + 40.4, ty - 5.8), "arrow", style=lbl_st)
arrow_arc((x0 + 15.0, by), width=7.2, height=6.2, tail_width=1.4, head_width=3.2, head_angle=28, angle_start=20, angle_end=215, style=st_pn)
text((x0 + 15.0, by - 5.8), "arrow_arc", style=lbl_st)
parallelogram((x0 + 40.4, by), width=9.2, height=5.4, corner_angle=68, style=st_an)
text((x0 + 40.4, by - 5.8), "parallelogram", style=lbl_st)

# 3. 3D & Containers (col 2, row 0)
x0, y0 = cols[2], rows[0]
cylinder((x0 + 10.2, ty), width=6.6, height=6.2, style=st_pn)
text((x0 + 10.2, ty - 5.8), "cylinder", style=lbl_st)
cube((x0 + 27.7, ty), width=6.6, height=6.0, style=st_sn)
text((x0 + 27.7, ty - 5.8), "cube", style=lbl_st)
document((x0 + 45.2, ty), width=6.8, height=6.0, style=st_pn)
text((x0 + 45.2, ty - 5.8), "document", style=lbl_st)
cloud((x0 + 18.2, by), width=8.6, height=5.8, style=st_sn)
text((x0 + 18.2, by - 5.8), "cloud", style=lbl_st)
funnel((x0 + 37.2, by), width=7.4, height=6.0, style=st_an)
text((x0 + 37.2, by - 5.8), "funnel", style=lbl_st)

# 4. Badges & Callouts (col 0, row 1)
x0, y0 = cols[0], rows[1]
ty, by = y0 + 23.0, y0 + 9.8
shield((x0 + 10.2, ty), width=6.0, height=6.2, style=st_pn)
text((x0 + 10.2, ty - 5.8), "shield", style=lbl_st)
bubblespeech((x0 + 23.7, ty - 2.3), width=8.0, height=4.8, tail_edge="bottom", tail_start_ratio=0.25, tail_vertex_xy=(x0 + 25.5, ty - 3.9), tail_end_ratio=0.52, style=st_sn)
text((x0 + 27.7, ty - 5.8), "bubblespeech", style=lbl_st)
tag((x0 + 45.2, ty), width=8.0, height=5.0, style=st_an)
text((x0 + 45.2, ty - 5.8), "tag", style=lbl_st)
ribbon((x0 + 18.2, by), width=5.6, height=6.2, style=Styles.AccentFlat)
text((x0 + 18.2, by - 5.8), "ribbon", style=lbl_st)
pin((x0 + 37.2, by), width=5.0, height=6.2, style=Styles.DangerNeutral.patch(shape_line_width=1.8))
text((x0 + 37.2, by - 5.8), "pin", style=lbl_st)

# 5. Domain Symbols (col 1, row 1)
x0, y0 = cols[1], rows[1]
gear((x0 + 10.2, ty), num_teeth=8, radius_ext=3.2, radius_int=2.3, hole_radius=1.0, style=st_sn)
text((x0 + 10.2, ty - 5.8), "gear", style=lbl_st)
lightning((x0 + 27.7, ty), width=4.8, height=6.4, style=Styles.WarningNeutral.patch(shape_line_width=1.8))
text((x0 + 27.7, ty - 5.8), "lightning", style=lbl_st)
checkmark((x0 + 45.2, ty), width=6.0, height=5.4, style=Styles.SuccessFlat)
text((x0 + 45.2, ty - 5.8), "checkmark", style=lbl_st)
clock((x0 + 18.2, by), radius=3.1, style=st_pn)
text((x0 + 18.2, by - 5.8), "clock", style=lbl_st)
forbidden((x0 + 37.2, by), radius=3.1, style=Styles.DangerNeutral.patch(shape_line_width=1.8))
text((x0 + 37.2, by - 5.8), "forbidden", style=lbl_st)

# 6. Lines & Curves (col 2, row 1)
x0, y0 = cols[2], rows[1]
lx, rx_c = x0 + 14.5, x0 + 41.0
line((lx - 6.2, ty - 2.0), (lx + 6.2, ty + 2.2), arrow_head="->", style=Styles.PrimaryBold)
circle((lx - 6.2, ty - 2.0), radius=0.55, style=Styles.PrimaryFlat)
text((lx, ty - 5.8), "line (->)", style=lbl_st)

lines([(rx_c - 6.2, ty - 2.0), (rx_c, ty - 2.0), (rx_c, ty + 2.2), (rx_c + 6.2, ty + 2.2)], arrow_head="->", style=Styles.SecondaryBold)
circle((rx_c - 6.2, ty - 2.0), radius=0.55, style=Styles.SecondaryFlat)
text((rx_c, ty - 5.8), "lines (ortho)", style=lbl_st)

lines_curved([(lx - 6.2, by - 2.0), (lx, by - 2.0), (lx, by + 2.2), (lx + 6.2, by + 2.2)], r=2.0, arrow_head="->", style=Styles.PrimaryBold)
circle((lx - 6.2, by - 2.0), radius=0.55, style=Styles.PrimaryFlat)
text((lx, by - 5.8), "lines_curved (r=2)", style=lbl_st)

lines_bezier((rx_c - 6.2, by - 2.0), [((rx_c + 0.5, by - 2.0), (rx_c - 0.5, by + 2.4), (rx_c + 6.2, by + 2.4))], arrow_head="->", style=Styles.AccentBold)
circle((rx_c - 6.2, by - 2.0), radius=0.55, style=Styles.AccentFlat)
text((rx_c, by - 5.8), "lines_bezier (->)", style=lbl_st)
```
:::

::: note
`drawlib.shapes` には43種類のパラメトリックな基本図形が収録されており、多角形、ブロック矢印、3Dストレージ・コンテナ、バッジや吹き出し、ドメイン記号の5カテゴリを網羅しています。また `drawlib.lines` は、単線 `line`、直交ポリライン `lines`、コーナーを半径 `r=2` で自動フィレット丸めする `lines_curved`、滑らかなS字ベジェ曲線を描く `lines_bezier`（`arrow_head="->"` 対応）など8種類のベクターコネクタを提供します。
:::
