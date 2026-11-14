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
# 単一リポジトリからあらゆる形式へ一括出力
:::

::: block xy=(80, 130) width=1760 height=115
単一の **`drawlib.toml`** と **`[i18n]`** 構造パリティ検証により、1つのGitコミットから日英同期された **Web・印刷・Office** の全成果物を一括コンパイルします。
:::

::: block xy=(80, 260) width=1760 height=685
```drawlib file=ssot_fanout_ja.svg
from drawlib.canvas import clear, save, setup
from drawlib.diagrams.architecture import ArchitectureDiagram, Node, NodeGroup, PhosphorIcon
from drawlib.styles import Styles

clear()
setup(width=176, height=69)

d = ArchitectureDiagram(
    node_style=Styles.PrimaryBold,
    node_text_style=Styles.DarkBold.patch(text_size=12.4),
    edge_style=Styles.PrimaryBold,
    edge_text_style=Styles.PrimaryBold.patch(text_size=12.0),
    node_card_style=Styles.Neutral,
)

repo_group = d.add(
    NodeGroup(
        title="Git リポジトリ: en/ + ja/ + styles.py",
        width=78.0,
        height=23.0,
        style=Styles.SecondaryNeutral.patch(shape_r=2.2),
        text_style=Styles.DarkBold.patch(text_size=13.5, halign="left"),
    ),
    xy=(2.0, 41.0),
)
repo_md = repo_group.add(
    Node(
        "en/ + ja/\nMarkdown",
        width=34.0,
        height=14.5,
        icon=PhosphorIcon.GIT_BRANCH,
        icon_size=5.6,
        card_style=Styles.White.patch(shape_r=1.8),
    ),
    xy=(20.0, 9.0),
)
repo_cfg = repo_group.add(
    Node(
        "drawlib.toml\n+ styles.py",
        width=34.0,
        height=14.5,
        icon=PhosphorIcon.FILE_CODE,
        icon_size=5.6,
        card_style=Styles.White.patch(shape_r=1.8),
    ),
    xy=(58.0, 9.0),
)

compiler = d.add(
    Node(
        "drawlib build  ·  SQLite SHA-256 キャッシュ",
        width=76.0,
        height=17.5,
        icon=PhosphorIcon.CPU,
        icon_size=6.5,
        style=Styles.WhiteBold,
        text_style=Styles.WhiteBold.patch(text_size=13.8),
        card_style=Styles.PrimaryFlat.patch(shape_r=2.2),
    ),
    xy=(132.0, 52.5),
)

d.connect(repo_group, compiler, routing="direct", padding=1.2)

outputs_spec = [
    (16.6, "HTML Docs &\nAPI カタログ", PhosphorIcon.GLOBE, Styles.Neutral),
    (51.3, "A4 ベクター PDF\n(印刷・配布対応)", PhosphorIcon.FILE_PDF, Styles.Neutral),
    (86.0, "編集可能 Word\n(.docx)", PhosphorIcon.FILE_DOC, Styles.Neutral),
    (120.7, "16:9 Web\nスライドデッキ", PhosphorIcon.PRESENTATION_CHART, Styles.PrimaryNeutral),
    (155.4, "編集可能 PPTX\n(PowerPoint)", PhosphorIcon.SLIDESHOW, Styles.PrimaryNeutral),
]

bus_y = 33.5
j_compiler = d.junction((132.0, bus_y))
d.connect(compiler, j_compiler, arrow="-", routing="direct", padding=(0.8, 0.0))

bus_junctions = []
for cx, label, icon_enum, c_style in outputs_spec:
    out_node = d.add(
        Node(
            label,
            width=31.6,
            height=22.5,
            icon=icon_enum,
            icon_size=6.8,
            card_style=c_style.patch(shape_r=2.0),
        ),
        xy=(cx, 14.5),
    )
    jn = d.junction((cx, bus_y))
    bus_junctions.append(jn)
    d.connect(jn, out_node, arrow="->", routing="direct", padding=(0.0, 0.8))

d.connect(bus_junctions[0], bus_junctions[1], arrow="-", routing="direct")
d.connect(bus_junctions[1], bus_junctions[2], arrow="-", routing="direct")
d.connect(bus_junctions[2], bus_junctions[3], arrow="-", routing="direct")
d.connect(bus_junctions[3], j_compiler, arrow="-", routing="direct")
d.connect(j_compiler, bus_junctions[4], arrow="-", routing="direct")

d.draw(xy=(2.0, 2.0))
save()
```
:::

::: note
第1章の締めくくりとして、単一のGitリポジトリがどのようにあらゆる納品フォーマットへ展開されるかを見てみましょう。
左上のGitリポジトリには、`en/` と `ja/` の多言語Markdownツリー、`drawlib.toml`、そして共通テーマを定義する `styles.py` が格納されています。
`drawlib build` を実行すると、まず日英のブロック構造パリティが自動検証され、変更のない図解は SHA-256 ベースの SQLite キャッシュから瞬時に再利用されます。
その上で、HTMLドキュメントサイト＆APIカタログ、印刷品質のA4ベクターPDF、ネイティブ編集可能なWord（`.docx`）、言語切り替え対応の16:9 Webスライド、そして編集可能なPowerPoint（`.pptx`）の5形式へ一括出力されます。
たった1回のGitコミットで、すべての媒体と言語が常に最新状態に保たれます。
:::
