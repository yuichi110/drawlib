::: block xy=(100, 210) width=780 height=660
# Drawlib

## コードで描く図解と技術ドキュメント

ソフトウェアエンジニアとAIコーディングエージェントのために設計された、純粋Pythonの宣言的作図エンジン＆マルチターゲット文書コンパイラ。

---

**公式ショーケースデッキ** · **v0.3.10 対応**
:::

::: block xy=(920, 130) width=900 height=820
```drawlib file=title_hero_ja.svg
from drawlib.canvas import clear, save, setup
from drawlib.diagrams.architecture import ArchitectureDiagram, Node, NodeGroup, PhosphorIcon
from drawlib.icons import phosphor
from drawlib.smartarts import Panel
from drawlib.styles import Styles

clear()
setup(width=90, height=82)

panel = Panel(
    "図解・ドキュメント統合パイプライン",
    "Git -> 多形式一括出力",
    style=Styles.Neutral.patch(shape_r=2.5),
    header_style=Styles.PrimaryBold,
    text_style=Styles.DarkBold.patch(text_size=14.8),
    description_style=Styles.Muted.patch(text_size=12.2),
    icon=phosphor.sparkle,
    icon_style=Styles.PrimaryBold,
    header_variant="underline",
    header_height=10.0,
)
panel.draw((2.0, 2.0), width=86.0, height=78.0)

d = ArchitectureDiagram(
    node_style=Styles.PrimaryBold,
    node_text_style=Styles.DarkBold.patch(text_size=13.8),
    edge_style=Styles.PrimaryBold,
    edge_text_style=Styles.PrimaryBold.patch(text_size=12.5),
    node_card_style=Styles.White,
)

src_group = d.add(
    NodeGroup(
        title="Git 単一情報源 (SoT)",
        width=37.0,
        height=22.0,
        style=Styles.SecondaryNeutral.patch(shape_r=2.0),
        text_style=Styles.DarkBold.patch(text_size=13.5, halign="left"),
    ),
    xy=(1.0, 42.0),
)
src_node = src_group.add(
    Node(
        "Python + Markdown",
        width=31.0,
        height=13.5,
        icon=PhosphorIcon.GIT_BRANCH,
        icon_size=5.8,
        card_style=Styles.White.patch(shape_r=1.8),
    ),
    xy=(18.5, 8.8),
)

compiler = d.add(
    Node(
        "Drawlib コンパイラ",
        width=36.0,
        height=17.5,
        icon=PhosphorIcon.CPU,
        icon_size=6.5,
        style=Styles.WhiteBold,
        text_style=Styles.WhiteBold.patch(text_size=14.2),
        card_style=Styles.PrimaryFlat.patch(shape_r=2.0),
    ),
    xy=(62.0, 53.0),
)

out_site = d.add(
    Node(
        "Docs サイト & API カタログ",
        width=36.0,
        height=14.5,
        icon=PhosphorIcon.GLOBE,
        icon_size=5.8,
        card_style=Styles.PrimaryNeutral.patch(shape_r=1.8),
    ),
    xy=(19.0, 27.0),
)
out_slide = d.add(
    Node(
        "16:9 スライド & PPTX",
        width=36.0,
        height=14.5,
        icon=PhosphorIcon.PRESENTATION_CHART,
        icon_size=5.8,
        card_style=Styles.PrimaryNeutral.patch(shape_r=1.8),
    ),
    xy=(63.0, 27.0),
)
out_pdf = d.add(
    Node(
        "ベクター PDF & DOCX",
        width=36.0,
        height=14.5,
        icon=PhosphorIcon.FILE_PDF,
        icon_size=5.8,
        card_style=Styles.White.patch(shape_r=1.8),
    ),
    xy=(19.0, 9.0),
)
out_img = d.add(
    Node(
        "SVG / PNG / APNG",
        width=36.0,
        height=14.5,
        icon=PhosphorIcon.IMAGES,
        icon_size=5.8,
        card_style=Styles.White.patch(shape_r=1.8),
    ),
    xy=(63.0, 9.0),
)

d.connect(src_group, compiler, routing="direct", padding=0.8)

j_drop = d.junction((62.0, 38.0))
j_bus_top = d.junction((41.0, 38.0))
j_row1 = d.junction((41.0, 27.0))
j_row2 = d.junction((41.0, 9.0))

d.connect(compiler, j_drop, arrow="-", routing="direct", padding=(0.8, 0.0))
d.connect(j_drop, j_bus_top, arrow="-", routing="direct")
d.connect(j_bus_top, j_row1, arrow="-", routing="direct")
d.connect(j_row1, j_row2, arrow="-", routing="direct")

d.connect(j_row1, out_site, arrow="->", routing="direct", padding=(0.0, 0.8))
d.connect(j_row1, out_slide, arrow="->", routing="direct", padding=(0.0, 0.8))
d.connect(j_row2, out_pdf, arrow="->", routing="direct", padding=(0.0, 0.8))
d.connect(j_row2, out_img, arrow="->", routing="direct", padding=(0.0, 0.8))

d.draw(xy=(4.0, 4.0))
save()
```
:::

::: note
Drawlib v0.3.10 公式ショーケースデッキへようこそ。
Drawlib は「Illustration & Documentation as Code（コードで描く図解と技術ドキュメント）」を実現する純粋Pythonフレームワークです。
GUIホワイトボードのバイナリファイルや表現力に制約のあるテキストDSL、手作業によるスライド貼り付けから脱却し、Git管理されたPythonコードとMarkdown原稿から、ドキュメントサイト、APIカタログ、16:9スライド、PowerPoint・Wordファイル、A4ベクターPDF、SVG/PNG/APNG画像をヘッドレスで一括生成します。
本プレゼンテーション自体もすべて Drawlib で記述・ビルドされています。
:::
