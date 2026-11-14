# Drawlib クイックスタートガイド

**純粋 Python による「Illustration as Code」&「Illustrated Documentation as Code」**

Drawlib は、宣言的な Python 作図コードと Markdown 技術文書を単一の Git リポジトリ（Single Source of Truth）に統合し、ドキュメントサイト（`site`）・検索可能な API リファレンス辞書（`catalog`）・技術白書（`doc`）・16:9 プレゼンテーション（`slide`）・単体画像／アニメーション群（`images`）・ベクター PDF・編集可能な Microsoft Office 文書（`.docx` / `.pptx`）を一括生成するライブラリです。

```drawlib align=center code=hide file=cover_workflow_ja.png caption="図 0.1: Drawlib の Single Source of Truth — Python と Markdown から多様な成果物を一括生成"
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import ArchitectureDiagram, Node, NodeGroup, PhosphorIcon
from drawlib.styles import Styles

setup(width=144, height=56)

d = ArchitectureDiagram(
    node_style=Styles.PrimaryBold,
    node_text_style=Styles.DarkBold.patch(text_size=11.0),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
)

repo = d.add(
    NodeGroup(
        title="Git リポジトリ (Source of Truth)",
        width=41.0,
        height=44.0,
        style=Styles.PrimaryNeutral.patch(shape_r=2.2),
        text_style=Styles.DarkBold.patch(text_size=10.8, halign="left"),
    ),
    xy=(1.5, 4.0),
)
py_src = repo.add(
    Node(
        "Python 作図コード\n(*.py・埋め込みブロック)",
        width=33.0,
        height=14.0,
        icon=PhosphorIcon.CODE,
        icon_size=5.2,
        card_style=Styles.White.patch(shape_r=1.8),
    ),
    xy=(20.5, 28.5),
)
md_src = repo.add(
    Node(
        "Markdown 原稿\n(en/・ja/ 多言語対応)",
        width=33.0,
        height=14.0,
        icon=PhosphorIcon.FILE_TEXT,
        icon_size=5.2,
        card_style=Styles.White.patch(shape_r=1.8),
    ),
    xy=(20.5, 10.5),
)

compiler = d.add(
    Node(
        "Drawlib コンパイラ\n& AI グリッド検証",
        width=32.0,
        height=20.0,
        icon=PhosphorIcon.CPU,
        icon_size=6.0,
        style=Styles.WhiteBold,
        text_style=Styles.WhiteBold.patch(text_size=11.5),
        card_style=Styles.PrimaryFlat.patch(shape_r=2.2),
    ),
    xy=(66.0, 26.0),
)

out_web = d.add(
    Node(
        "Web サイト & API 辞書\n(HTML / SEO / llms.txt)",
        width=40.0,
        height=13.0,
        icon=PhosphorIcon.GLOBE,
        icon_size=5.0,
        card_style=Styles.SecondaryNeutral.patch(shape_r=1.8),
    ),
    xy=(118.0, 41.5),
)
out_doc = d.add(
    Node(
        "技術白書 & 設計仕様書\n(ベクター PDF & DOCX)",
        width=40.0,
        height=13.0,
        icon=PhosphorIcon.FILE_PDF,
        icon_size=5.0,
        card_style=Styles.Neutral.patch(shape_r=1.8),
    ),
    xy=(118.0, 26.0),
)
out_slide = d.add(
    Node(
        "16:9 スライド & 画像群\n(PPTX / PNG / WebP / GIF)",
        width=40.0,
        height=13.0,
        icon=PhosphorIcon.PRESENTATION_CHART,
        icon_size=5.0,
        card_style=Styles.Neutral.patch(shape_r=1.8),
    ),
    xy=(118.0, 10.5),
)

d.connect(repo, compiler, routing="direct", padding=0.8)
j_hub = d.junction((90.0, 26.0))
j_top = d.junction((90.0, 41.5))
j_bot = d.junction((90.0, 10.5))
d.connect(compiler, j_hub, arrow="-", routing="direct", padding=(0.8, 0.0))
d.connect(j_hub, j_top, arrow="-", routing="direct")
d.connect(j_hub, j_bot, arrow="-", routing="direct")
d.connect(j_top, out_web, arrow="->", routing="direct", padding=(0.0, 0.8))
d.connect(j_hub, out_doc, arrow="->", routing="direct", padding=(0.0, 0.8))
d.connect(j_bot, out_slide, arrow="->", routing="direct", padding=(0.0, 0.8))

d.draw(xy=(2.0, 2.0))
save()
```

---

### 本書の構成とロードマップ

本書は、ソフトウェアエンジニア・テクニカルライター・AI コーディングエージェント向けに Drawlib の基礎から実践的なドキュメント出版までを全 16 章で解説する入門ハンドブックです。

- **第1〜3章（基礎編）**: Drawlib の設計思想、`uv` / `uvx` によるゼロ設定導入、左下 `(0, 0)` のデカルト座標系とアンカー設計。
- **第4〜6章（基本図形・スタイル・アイコン編）**: 43 種の基本図形と接続線、`GoogleStyles` のニュートラル配色規律と多言語フォント、34 種のベクターアイコンスイート。
- **第7〜11章（高レベル描画エンジン編）**: 18 種の SmartArts、10 種の定量チャート（`BoxChart`・`HeatmapChart` 含む）、`ArchitectureDiagram`、UML ソフトウェア設計図、5 種の自動グラフレイアウトソルバー（`drawlib.graph`）。
- **第12〜15章（アニメーション・出版・AI 協業編）**: `APNG` / `WebP` / `GIF` アニメーションと 16:9 スライド、5 つのプロジェクト種別（`site` / `catalog` / `doc` / `slide` / `images`）、CLI キャッシュ、AI エージェントの 3 段階自律検証ループ。

| ドキュメント情報 | 内容 |
| :--- | :--- |
| **対象バージョン** | `0.3.10` |
| **ビジュアルテーマ** | `GoogleStyles` & `GoogleColors` (`style = "google"`) |
| **対応言語 (`[i18n]`)** | 英語 (`en`)・日本語 (`ja`) |
| **公式サイト** | `https://www.drawlib.com/` |
| **ソースリポジトリ** | `https://github.com/yuichi110/drawlib` |
| **ライセンス** | Apache License 2.0 |
