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
# Illustration & Documentation as Code
:::

::: block xy=(80, 145) width=680 height=790
## Python と Markdown の統合

- **チューリング完全な記述**: ループ・変数・`utils.py` 共通関数を活用

- **Markdown 直書き**: 原稿内の `drawlib` ブロックから直接描画

- **決定論的な PR 差分**: 文章と図解の更新を同一コミットでレビュー

```python
setup(width=120, height=32)
p = ChevronProcess(style=Styles.Neutral)
for s in ("記述", "変換", "公開"): p.add(s)
p.draw((6, 8), width=108, height=16)
save()
```
:::

::: block xy=(800, 140) width=1040 height=800
```drawlib file=unified_paradigm_ja.svg
from drawlib.canvas import clear, save, setup
from drawlib.diagrams.architecture import ArchitectureDiagram, Node, NodeGroup, PhosphorIcon
from drawlib.icons import phosphor
from drawlib.smartarts import Panel
from drawlib.styles import Styles

clear()
setup(width=104, height=80)

panel = Panel(
    "コードから成果物への統合パイプライン",
    "コード -> 図解・文書を同時生成",
    style=Styles.Neutral.patch(shape_r=2.5),
    header_style=Styles.PrimaryBold,
    text_style=Styles.DarkBold.patch(text_size=15.0),
    description_style=Styles.Muted.patch(text_size=12.2),
    icon=phosphor.code,
    icon_style=Styles.PrimaryBold,
    header_variant="underline",
    header_height=9.5,
)
panel.draw((2.0, 2.0), width=100.0, height=76.0)

d = ArchitectureDiagram(
    node_style=Styles.PrimaryBold,
    node_text_style=Styles.DarkBold.patch(text_size=14.0),
    edge_style=Styles.PrimaryBold,
    edge_text_style=Styles.PrimaryBold.patch(text_size=12.5),
    node_card_style=Styles.White,
)

pr_group = d.add(
    NodeGroup(
        title="単一の Git プルリクエスト",
        width=88.0,
        height=21.5,
        style=Styles.SecondaryNeutral.patch(shape_r=2.0),
        text_style=Styles.DarkBold.patch(text_size=13.5, halign="left"),
    ),
    xy=(3.0, 41.5),
)
md_node = pr_group.add(
    Node(
        "Markdown (.md)\n本文・スライド構成",
        width=38.0,
        height=13.5,
        icon=PhosphorIcon.FILE_TEXT,
        icon_size=5.8,
        card_style=Styles.White.patch(shape_r=1.8),
    ),
    xy=(22.5, 8.5),
)
py_node = pr_group.add(
    Node(
        "Python (drawlib)\n描画ロジック・共通スタイル",
        width=38.0,
        height=13.5,
        icon=PhosphorIcon.CODE,
        icon_size=5.8,
        card_style=Styles.White.patch(shape_r=1.8),
    ),
    xy=(65.5, 8.5),
)

compiler = d.add(
    Node(
        "Drawlib コンパイラ (ヘッドレス描画 + キャッシュ)",
        width=66.0,
        height=14.5,
        icon=PhosphorIcon.CPU,
        icon_size=6.2,
        style=Styles.WhiteBold,
        text_style=Styles.WhiteBold.patch(text_size=14.0),
        card_style=Styles.PrimaryFlat.patch(shape_r=2.0),
    ),
    xy=(47.0, 27.5),
)

out_vis = d.add(
    Node(
        "ベクタービジュアル\nSVG · PNG · APNG",
        width=40.0,
        height=14.0,
        icon=PhosphorIcon.IMAGES,
        icon_size=5.8,
        card_style=Styles.PrimaryNeutral.patch(shape_r=1.8),
    ),
    xy=(24.0, 7.5),
)
out_docs = d.add(
    Node(
        "公開ドキュメント群\nHTML · Slide · PDF · Office",
        width=42.0,
        height=14.0,
        icon=PhosphorIcon.BOOK_OPEN,
        icon_size=5.8,
        card_style=Styles.PrimaryNeutral.patch(shape_r=1.8),
    ),
    xy=(71.0, 7.5),
)

j_in_l = d.junction((25.5, 38.0))
j_in_r = d.junction((68.5, 38.0))
j_in_m = d.junction((47.0, 38.0))
d.connect(md_node, j_in_l, arrow="-", routing="direct", padding=(0.8, 0.0))
d.connect(py_node, j_in_r, arrow="-", routing="direct", padding=(0.8, 0.0))
d.connect(j_in_l, j_in_m, arrow="-", routing="direct")
d.connect(j_in_r, j_in_m, arrow="-", routing="direct")
d.connect(j_in_m, compiler, arrow="->", routing="direct", padding=(0.0, 0.8))

j_out_m = d.junction((47.0, 17.8))
j_out_l = d.junction((24.0, 17.8))
j_out_r = d.junction((71.0, 17.8))
d.connect(compiler, j_out_m, arrow="-", routing="direct", padding=(0.8, 0.0))
d.connect(j_out_m, j_out_l, arrow="-", routing="direct")
d.connect(j_out_m, j_out_r, arrow="-", routing="direct")
d.connect(j_out_l, out_vis, arrow="->", routing="direct", padding=(0.0, 0.8))
d.connect(j_out_r, out_docs, arrow="->", routing="direct", padding=(0.0, 0.8))

d.draw(xy=(5.0, 4.0))
save()
```
:::

::: note
Drawlib が提唱する解決策が「Illustration & Documentation as Code」です。
独自の制限された記法を新しく覚える必要はありません。ループや変数、型補完、`styles.py` や `utils.py` による共通部品化といった純粋な Python の表現力を、標準的な Markdown のコードブロック内にそのまま記述できます。
システムの仕様変更時には、Markdown の説明文と Python の図解コードを同じ Git プルリクエスト上で同時に更新・レビューでき、Drawlib コンパイラがベクター図解と各種公開ドキュメントを決定論的に生成します。
:::
