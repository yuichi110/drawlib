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
# 数字で見る Drawlib の全体像
:::

::: block xy=(80, 140) width=640 height=800
```drawlib file=glance_kpis_ja.svg
from drawlib.canvas import clear, save, setup
import utils

clear()
setup(width=64, height=80)

utils.draw_kpi_cards(
    [
        ("4,500+", "ベクターアイコン", "公式クラウド・汎用など全34スイート"),
        ("39+", "高水準ビジュアル", "18 SmartArts・10 Charts\n6 Diagrams・5 Graphs"),
        ("5", "プロジェクト型", "site, catalog, doc, slide, images"),
        ("100%", "純粋Python & Git", "GUIロックインなし・AI自己検証可能"),
    ],
    width=64,
    height=80,
)
save()
```
:::

::: block xy=(760, 140) width=1080 height=800
```drawlib file=ecosystem_layers_ja.svg
from drawlib.canvas import clear, save, setup
from drawlib.icons import phosphor
from drawlib.smartarts import CardList, Panel
from drawlib.styles import Styles

clear()
setup(width=108, height=80)

panel = Panel(
    "Drawlib 4層アーキテクチャスタック",
    "CLI基盤から多形式出力まで統合",
    style=Styles.Neutral.patch(shape_r=2.5),
    header_style=Styles.PrimaryBold,
    text_style=Styles.DarkBold.patch(text_size=15.5),
    description_style=Styles.Muted.patch(text_size=12.8),
    icon=phosphor.stack,
    icon_style=Styles.PrimaryBold,
    header_variant="underline",
    header_height=9.5,
)
panel.draw((2.0, 2.0), width=104.0, height=76.0)
inner_xy, inner_w, inner_h = panel.get_content_box(
    (2.0, 2.0),
    width=104.0,
    height=76.0,
    padding=(3.5, 2.8),
)

layers = CardList(
    style=Styles.White.patch(shape_r=2.0),
    text_style=Styles.DarkBold.patch(text_size=14.5),
    description_style=Styles.Dark.patch(text_size=13.0),
    badge_shape="rounded_rect",
    badge_style=Styles.SecondaryNeutral,
    badge_text_style=Styles.DarkBold.patch(text_size=12.5),
    icon_style=Styles.PrimaryBold,
    direction="vertical",
    spacing=2.6,
)
layers.add(
    "Layer 4 · マルチターゲット・コンパイラ",
    "HTML · Catalog · Slide · PDF · DOCX · PPTX",
    badge_text="L4",
    icon=phosphor.rocket_launch,
    style=Styles.PrimaryNeutral.patch(shape_r=2.0),
    badge_style=Styles.PrimaryFlat,
    badge_text_style=Styles.WhiteBold.patch(text_size=12.5),
    icon_style=Styles.WhiteBold,
)
layers.add(
    "Layer 3 · 宣言的ビジュアルエンジン群",
    "SmartArts · Charts · Diagrams · Graphs · Anim",
    badge_text="L3",
    icon=phosphor.chart_bar,
)
layers.add(
    "Layer 2 · 基本図形・34種アイコン群・スタイル",
    "43種の幾何図形 · 4,500+ ベクターアイコン · 意味論テーマ",
    badge_text="L2",
    icon=phosphor.paint_brush,
)
layers.add(
    "Layer 1 · AI エージェント CLI 基盤",
    "rules 参照 · show -g グリッド検証 · SQLite キャッシュ",
    badge_text="L1",
    icon=phosphor.robot,
    badge_style=Styles.PrimaryFlat,
    badge_text_style=Styles.WhiteBold.patch(text_size=12.5),
    icon_style=Styles.WhiteBold,
)
layers.draw(inner_xy, width=inner_w, height=inner_h)
save()
```
:::

::: note
まず、Drawlib の全体像を主要な数値と4層アーキテクチャでご紹介します。
左側のKPIカードの通り、GCP・AWS・Azureなどの公式アイコンや汎用スイートを含む全34スイート・4,500種類以上のベクターアイコン、18種のSmartArts・10種のCharts・6種のDiagrams・5種のGraphsからなる39以上の高水準ビジュアル、5つのプロジェクトアーキタイプを備え、100%純粋なPythonとGitで完結します。
右側の4層スタックは、下層のAIエージェント向けCLIとSQLiteキャッシュ基盤から、プリミティブ＆アイコン層、宣言的ビジュアルエンジン層、そして最上層のマルチターゲット文書コンパイラまでが一貫して統合されていることを示しています。
:::
