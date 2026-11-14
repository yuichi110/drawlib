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
# 5種類の専用グラフレイアウトソルバー
:::

::: block xy=(80, 130) width=1760 height=815
```drawlib file=five_graph_solvers_ja.svg
import math

from drawlib.canvas import clear, save, setup
from drawlib.graph import (
    ArchitectureGraph,
    GridGraph,
    LayerGraph,
    RadialGraph,
    TreeGraph,
)
from drawlib.icons import phosphor
from drawlib.lines import line, lines
from drawlib.shapes import circle, rectangle
from drawlib.smartarts import Panel
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=176, height=82)

t_node = Styles.DarkBold.patch(text_size=11.0)
t_hero = Styles.WhiteBold.patch(text_size=11.0)
t_hdr = Styles.DarkBold.patch(text_size=13.0)


def shift_pts(pts: list[tuple[float, float]], ox: float, oy: float) -> list[tuple[float, float]]:
    return [(p[0] + ox, p[1] + oy) for p in pts]


# 1. ArchitectureGraph (Top-Left)
p1 = Panel(
    "1. ArchitectureGraph (境界)",
    style=Styles.White,
    header_style=Styles.PrimaryNeutral,
    text_style=t_hdr,
    icon=phosphor.cloud,
    icon_style=Styles.PrimaryBold,
    header_height=6.8,
)
p1.draw((2.0, 42.8), width=55.0, height=37.2)
(ox1, oy1), iw1, ih1 = p1.get_content_box((2.0, 42.8), width=55.0, height=37.2, padding=(2.0, 1.4))

g1 = ArchitectureGraph(direction="LR", container_sep=5.5, default_node_width=13.0, default_node_height=5.0)
g1.cluster("edge", ["cdn"], pos="left", padding=1.8, header_height=3.4)
g1.cluster("vpc", ["api", "db"], pos="center", padding=1.8, header_height=3.4)
g1.edge("cdn", "api")
g1.edge("cdn", "db")
l1 = g1.get_layout(width=iw1, height=ih1, margin=1.5)
min_x1 = min(c.left for c in l1.clusters.values())
max_x1 = max(c.right for c in l1.clusters.values())
min_y1 = min(c.bottom for c in l1.clusters.values())
max_y1 = max(c.top for c in l1.clusters.values())
dx1 = ox1 + iw1 / 2 - (min_x1 + max_x1) / 2
dy1 = oy1 + ih1 / 2 - (min_y1 + max_y1) / 2

for cid, ctitle in [("edge", "Edge"), ("vpc", "VPC")]:
    c = l1[cid]
    rectangle((c.cx + dx1, c.cy + dy1), width=c.width, height=c.height, style=Styles.MutedDashed.patch(shape_r=1.5))
    text((c.left + dx1 + 1.2, c.top + dy1 - 1.8), ctitle, style=Styles.Muted.patch(text_size=11.0, halign="left"))
for e in l1.edges:
    lines(shift_pts(e.points, dx1, dy1), arrow_head="->", style=Styles.DarkBold)
for nid, lbl, st, tst in [
    ("cdn", "CDN", Styles.PrimaryNeutral, t_node),
    ("api", "API", Styles.PrimaryFlat, t_hero),
    ("db", "DB", Styles.SecondaryNeutral, t_node),
]:
    n = l1[nid]
    rectangle((n.x + dx1, n.y + dy1), width=n.width, height=n.height, style=st.patch(shape_r=1.2), text=lbl, text_style=tst)

# 2. LayerGraph (Top-Center)
p2 = Panel(
    "2. LayerGraph (階層型 DAG)",
    style=Styles.White,
    header_style=Styles.SecondaryNeutral,
    text_style=t_hdr,
    icon=phosphor.graph,
    icon_style=Styles.SecondaryBold,
    header_height=6.8,
)
p2.draw((60.5, 42.8), width=55.0, height=37.2)
(ox2, oy2), iw2, ih2 = p2.get_content_box((60.5, 42.8), width=55.0, height=37.2, padding=(2.0, 1.4))

g2 = LayerGraph(direction="LR", rank_sep=5.2, node_sep=4.5, default_node_width=11.5, default_node_height=6.2)
g2.edge("in", "a")
g2.edge("in", "b")
g2.edge("a", "out")
g2.edge("b", "out")
l2 = g2.get_layout(width=iw2, height=ih2, margin=1.5)

for e in l2.edges:
    lines(shift_pts(e.points, ox2, oy2), arrow_head="->", style=Styles.DarkBold)
for nid, lbl, st, tst in [
    ("in", "入力", Styles.Neutral, t_node),
    ("a", "変換A", Styles.PrimaryNeutral, t_node),
    ("b", "変換B", Styles.SecondaryNeutral, t_node),
    ("out", "出力", Styles.PrimaryFlat, t_hero),
]:
    n = l2[nid]
    rectangle((n.x + ox2, n.y + oy2), width=n.width, height=n.height, style=st.patch(shape_r=1.2), text=lbl, text_style=tst)

# 3. TreeGraph (Top-Right)
p3 = Panel(
    "3. TreeGraph (整列ツリー)",
    style=Styles.White,
    header_style=Styles.PrimaryNeutral,
    text_style=t_hdr,
    icon=phosphor.tree_structure,
    icon_style=Styles.PrimaryBold,
    header_height=6.8,
)
p3.draw((119.0, 42.8), width=55.0, height=37.2)
(ox3, oy3), iw3, ih3 = p3.get_content_box((119.0, 42.8), width=55.0, height=37.2, padding=(2.0, 1.4))

g3 = TreeGraph(root="root", direction="TB", default_node_width=13.5, default_node_height=6.8)
g3.child("root", "web")
g3.child("root", "api")
g3.child("root", "db")
l3 = g3.get_layout(width=iw3, height=ih3, margin=2.0)

for e in l3.edges:
    lines(shift_pts(e.points, ox3, oy3), arrow_head="->", style=Styles.DarkBold)
for nid, lbl, st, tst in [
    ("root", "親拠点", Styles.PrimaryFlat, t_hero),
    ("web", "Web", Styles.PrimaryNeutral, t_node),
    ("api", "API", Styles.PrimaryNeutral, t_node),
    ("db", "データ", Styles.SecondaryNeutral, t_node),
]:
    n = l3[nid]
    rectangle((n.x + ox3, n.y + oy3), width=n.width, height=n.height, style=st.patch(shape_r=1.2), text=lbl, text_style=tst)

# 4. RadialGraph (Bottom-Left)
p4 = Panel(
    "4. RadialGraph (同心円ハブ＆スポーク)",
    style=Styles.White,
    header_style=Styles.SecondaryNeutral,
    text_style=t_hdr,
    icon=phosphor.circles_three,
    icon_style=Styles.SecondaryBold,
    header_height=6.8,
)
p4.draw((2.0, 2.0), width=84.0, height=37.2)
(ox4, oy4), iw4, ih4 = p4.get_content_box((2.0, 2.0), width=84.0, height=37.2, padding=(2.0, 1.4))

g4 = RadialGraph(hub="hub", radius_step=12.5, start_angle=45.0, default_node_width=15.0, default_node_height=6.0)
g4.node("hub", width=11.0, height=11.0)
for s in ["s1", "s2", "s3", "s4"]:
    g4.spoke("hub", s)
l4 = g4.get_layout(width=iw4, height=ih4, margin=1.5)
l4.offset("s1", dx=10.0).offset("s4", dx=10.0).offset("s2", dx=-10.0).offset("s3", dx=-10.0)

hub = l4["hub"]
circle((hub.x + ox4, hub.y + oy4), radius=10.0, style=Styles.MutedDashed)
for s in ["s1", "s2", "s3", "s4"]:
    n = l4[s]
    ddx, ddy = n.x - hub.x, n.y - hub.y
    dist = math.hypot(ddx, ddy)
    sx = hub.x + ox4 + (ddx / dist) * 5.9
    sy = hub.y + oy4 + (ddy / dist) * 5.9
    t_edge = (abs(ddx) - n.width / 2 - 0.3) / abs(ddx)
    ex = hub.x + ox4 + ddx * t_edge
    ey = hub.y + oy4 + ddy * t_edge
    line((sx, sy), (ex, ey), arrow_head="->", style=Styles.DarkBold)
circle((hub.x + ox4, hub.y + oy4), radius=5.6, style=Styles.PrimaryFlat, text="中核", text_style=t_hero)
for nid, lbl, st in [
    ("s1", "認証", Styles.PrimaryNeutral),
    ("s2", "注文", Styles.SecondaryNeutral),
    ("s3", "決済", Styles.PrimaryNeutral),
    ("s4", "検索", Styles.SecondaryNeutral),
]:
    n = l4[nid]
    rectangle((n.x + ox4, n.y + oy4), width=n.width, height=n.height, style=st.patch(shape_r=1.2), text=lbl, text_style=t_node)

# 5. GridGraph (Bottom-Right)
p5 = Panel(
    "5. GridGraph (2D マトリクス・蛇行フロー)",
    style=Styles.White,
    header_style=Styles.PrimaryNeutral,
    text_style=t_hdr,
    icon=phosphor.grid_four,
    icon_style=Styles.PrimaryBold,
    header_height=6.8,
)
p5.draw((90.0, 2.0), width=84.0, height=37.2)
(ox5, oy5), iw5, ih5 = p5.get_content_box((90.0, 2.0), width=84.0, height=37.2, padding=(2.0, 1.4))

g5 = GridGraph(columns=3, default_node_width=18.5, default_node_height=6.8)
g5.cell("c1", row=0, col=0)
g5.cell("c2", row=0, col=1)
g5.cell("c3", row=0, col=2)
g5.cell("c4", row=1, col=2)
g5.cell("c5", row=1, col=1)
g5.cell("c6", row=1, col=0)
for a, b in [("c1", "c2"), ("c2", "c3"), ("c3", "c4"), ("c4", "c5"), ("c5", "c6")]:
    g5.edge(a, b)
l5 = g5.get_layout(width=iw5, height=ih5, margin=2.0)

for e in l5.edges:
    lines(shift_pts(e.points, ox5, oy5), arrow_head="->", style=Styles.DarkBold)
for nid, lbl, st, tst in [
    ("c1", "1. 計画", Styles.Neutral, t_node),
    ("c2", "2. 実装", Styles.PrimaryNeutral, t_node),
    ("c3", "3. ビルド", Styles.PrimaryNeutral, t_node),
    ("c4", "4. 検証", Styles.SecondaryNeutral, t_node),
    ("c5", "5. 承認", Styles.SecondaryNeutral, t_node),
    ("c6", "6. 本番", Styles.PrimaryFlat, t_hero),
]:
    n = l5[nid]
    rectangle((n.x + ox5, n.y + oy5), width=n.width, height=n.height, style=st.patch(shape_r=1.2), text=lbl, text_style=tst)

save()
```
:::

::: note
**5種類の専用グラフレイアウトソルバー (`drawlib.graph`) の使い分け**:
1. **`ArchitectureGraph` (左上)**: 東西南北＋中央の5ゾーン配置（`pos`）と2階層コンテナに対応し、クラウド VPC やマイクロサービス構成図の座標計算に最適です。
2. **`LayerGraph` (中央上)**: 杉山法ベースの階層型 DAG ソルバーで、サイクル除去・ランク割り当て・エッジ交差最小化を自動実行します。
3. **`TreeGraph` (右上)**: Reingold-Tilford アルゴリズムにより、親ノードを子グループの中央に揃えつつ部分木同士の重なりを完全に防ぎます。
4. **`RadialGraph` (左下)**: 中心ハブの周囲に同心円リング（`ring=1, 2...`）でスポークを放射配置し、`layout.ring_radii` で軌道ガイド円も描画できます。
5. **`GridGraph` (右下)**: 均等な `(row, col)` マトリクス上にノードを整列させ、蛇行フローやセル間チャネル配線（`smart` ルーティング）を実現します。
:::
