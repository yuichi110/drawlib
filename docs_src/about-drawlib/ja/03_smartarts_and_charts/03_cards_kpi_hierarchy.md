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
# KPIカード・リスト・階層・マインドマップ
:::

::: block xy=(80, 130) width=1760 height=815
```drawlib file=cards_kpi_hierarchy_ja.svg
from drawlib.canvas import clear, save, setup
from drawlib.icons import phosphor
from drawlib.smartarts import CardList, KpiCards, MindMapNode, Panel, Pyramid
from drawlib.styles import Styles

clear()
setup(width=176, height=81)

# 1. Top-Left Panel: KpiCards (2x2 Grid)
p_tl = Panel(
    "KpiCards — 指標グリッド",
    "2x2 マルチ列",
    style=Styles.Neutral.patch(shape_r=2.0),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=14.0),
    description_style=Styles.Muted.patch(text_size=11.2),
    icon=phosphor.gauge,
    icon_style=Styles.PrimaryBold,
    header_height=6.4,
)
p_tl.draw((1.5, 42.2), width=84.5, height=37.5)
tl_xy, tl_w, tl_h = p_tl.get_content_box((1.5, 42.2), width=84.5, height=37.5, padding=(3.0, 2.2))

kpi = KpiCards(
    style=Styles.White.patch(shape_r=1.8),
    metric_style=Styles.PrimaryBold.patch(text_size=16.5),
    text_style=Styles.DarkBold.patch(text_size=11.8),
    description_style=Styles.Muted.patch(text_size=10.6),
    accent_style=Styles.PrimaryFlat,
    accent_position="left_pill",
    metric_layout="left_column",
    metric_width_ratio=0.32,
    spacing=2.4,
)
kpi.add("18", "SmartArt 種別", "表から世界地図まで")
kpi.add("34", "アイコンスイート", "主要クラウド網羅", accent_style=Styles.SecondaryFlat)
kpi.add("0", "GUI 依存ゼロ", "100% コード管理", accent_style=Styles.DarkFlat)
kpi.add("4", "標準テーマ数", "一括パレット切替", accent_style=Styles.AccentFlat)
kpi.draw(tl_xy, width=tl_w, height=tl_h, columns=2)

# 2. Top-Right Panel: CardList (3 Icon/Badge Feature Cards)
p_tr = Panel(
    "CardList — 機能カードリスト",
    "アイコン + バッジ",
    style=Styles.Neutral.patch(shape_r=2.0),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=14.0),
    description_style=Styles.Muted.patch(text_size=11.2),
    icon=phosphor.stack,
    icon_style=Styles.PrimaryBold,
    header_height=6.4,
)
p_tr.draw((90.0, 42.2), width=84.5, height=37.5)
tr_xy, tr_w, tr_h = p_tr.get_content_box((90.0, 42.2), width=84.5, height=37.5, padding=(3.0, 2.2))

cl = CardList(
    style=Styles.White,
    text_style=Styles.DarkBold.patch(text_size=11.8),
    description_style=Styles.Muted.patch(text_size=10.6),
    badge_shape="rounded_rect",
    badge_style=Styles.PrimaryNeutral,
    badge_text_style=Styles.PrimaryBold.patch(text_size=11.0),
    icon_style=Styles.PrimaryBold,
    direction="vertical",
    spacing=1.8,
)
cl.add(
    "宣言的な要素ライフサイクル",
    ".add() で登録し .draw() で一括描画",
    badge_text="L1",
    icon=phosphor.code,
    badge_style=Styles.PrimaryFlat,
    badge_text_style=Styles.WhiteBold.patch(text_size=11.0),
    icon_style=Styles.WhiteBold,
)
cl.add("セマンティックな配色トークン", "落ち着いたベース色と焦点ハイライト", badge_text="L2", icon=phosphor.palette)
cl.add("アニメーション対応の表示制御", "座標を崩さず item.show で段階表示", badge_text="L3", icon=phosphor.eye)
cl.draw(tr_xy, width=tr_w, height=tr_h)

# 3. Bottom-Left Panel: Pyramid (3 Architectural Tiers)
p_bl = Panel(
    "Pyramid — アーキテクチャ階層",
    "3段階レイヤー",
    style=Styles.Neutral.patch(shape_r=2.0),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=14.0),
    description_style=Styles.Muted.patch(text_size=11.2),
    icon=phosphor.sliders,
    icon_style=Styles.PrimaryBold,
    header_height=6.4,
)
p_bl.draw((1.5, 1.5), width=84.5, height=37.5)
bl_xy, _, bl_h = p_bl.get_content_box(
    (1.5, 1.5), width=84.5, height=37.5, padding=(6.0, 2.2), content_align="center"
)

pyr = Pyramid(
    style=Styles.White,
    text_style=Styles.DarkBold.patch(text_size=12.0),
)
pyr.add(
    "資料",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=11.2),
)
pyr.add("構造化図解", style=Styles.PrimaryNeutral)
pyr.add("ベクター描画基盤", style=Styles.SecondaryNeutral)
pyr.draw(bl_xy, width=68.0, height=bl_h, margin=1.4, direction="bottom", order="vertex_to_base", align="center")

# 4. Bottom-Right Panel: MindMapNode (Root + 2 Left & 2 Right Leaves)
p_br = Panel(
    "MindMapNode — 放射ツリー",
    "2パス自動配線",
    style=Styles.Neutral.patch(shape_r=2.0),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=14.0),
    description_style=Styles.Muted.patch(text_size=11.2),
    icon=phosphor.tree_structure,
    icon_style=Styles.PrimaryBold,
    header_height=6.4,
)
p_br.draw((90.0, 1.5), width=84.5, height=37.5)
br_xy, _, _ = p_br.get_content_box(
    (90.0, 1.5), width=84.5, height=37.5, padding=(3.0, 2.2), content_align="center"
)

leaf_left_style = Styles.PrimaryNeutral.patch(shape_r=1.5)
leaf_right_style = Styles.SecondaryNeutral.patch(shape_r=1.5)
leaf_txt = Styles.DarkBold.patch(text_size=11.5)

mm = MindMapNode(
    "Drawlib",
    shape="ellipse",
    width=21.0,
    height=9.2,
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=12.5),
    line_style=Styles.DarkBold,
    line_length=6.2,
    horizontal_margin=3.0,
    vertical_margin=3.6,
    children=[
        MindMapNode("構造化図解", branch="left", shape="rectangle", width=21.0, height=7.8, style=leaf_left_style, text_style=leaf_txt),
        MindMapNode("10種チャート", branch="left", shape="rectangle", width=21.0, height=7.8, style=leaf_left_style, text_style=leaf_txt),
        MindMapNode("システム図", branch="right", shape="rectangle", width=21.0, height=7.8, style=leaf_right_style, text_style=leaf_txt),
        MindMapNode("文書・スライド", branch="right", shape="rectangle", width=21.0, height=7.8, style=leaf_right_style, text_style=leaf_txt),
    ],
)
mm.draw(xy=br_xy)

save()
```
:::

::: note
ここでは、情報整理や階層構造の表現に活躍する4種類の SmartArts を 2×2 の `Panel` グリッドに配置しています。
- **`KpiCards`** はアクセントピルと数値専用カラムを備えたエグゼクティブ向け指標カードを整然と並べます。
- **`CardList`** は番号バッジや Phosphor ベクターアイコンと機能説明文を組み合わせたカードリストを描画します。
- **`Pyramid`** はテストピラミッドや多層防御・基盤スタックなどの階層構造を頂点から土台まで均整よく構築します。
- **`MindMapNode`** は2パスの部分木サイズ計測により、中央ルートノードから左右・上下へ直交コネクタを自動配線します。
:::
