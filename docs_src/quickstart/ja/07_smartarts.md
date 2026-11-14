# 7. SmartArts：18種の構造化ビジュアルコンポーネント

業務フロー図や比較表のたびに矩形やテキストの座標を手計算する必要はありません。`drawlib.smartarts` は、余白・整列・枠線・タイポグラフィを自動計算する **全18種の高レベル構造化コンポーネント** を提供します。すべての SmartArt が `GoogleStyles` のデザイントークンと同一キャンバスを共有するため、KPI サマリー・パイプライン・SLA 比較表・ディレクトリツリーを1枚の図内で自在に組み合わせられます。

```drawlib align=center code=fold file=smartarts_chevron_kpi_ja.png caption="図 7.1: KpiCards と ChevronProcess を組み合わせたリリースメトリクス・ダッシュボード"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.smartarts import ChevronProcess, KpiCards
from drawlib.styles import Styles
from drawlib.text import text

setup(width=148, height=66)

text(
    (74.0, 60.5),
    "v0.3.10 リリース品質指標とドキュメント公開パイプライン",
    style=Styles.DarkBold.patch(text_size=12.5),
)

kpi = KpiCards(
    style=Styles.Neutral.patch(shape_r=1.8),
    metric_style=Styles.DarkBold.patch(text_size=15.5),
    text_style=Styles.DarkBold.patch(text_size=11.0),
    description_style=Styles.Muted.patch(text_size=10.0),
    accent_style=Styles.SecondaryFlat,
    icon_style=Styles.PrimaryBold,
    accent_position="top_bar",
    metric_layout="top_stack",
    spacing=3.5,
)
kpi.add(
    "99.99%",
    "稼働率 SLA",
    "マルチリージョン冗長構成",
    icon=phosphor.shield_check,
)
kpi.add(
    "11.4 ms",
    "エッジ P99 遅延",
    "v0.3.10 ゼロコピールーター",
    icon=phosphor.lightning,
    style=Styles.PrimaryFlat.patch(shape_r=1.8),
    metric_style=Styles.WhiteBold.patch(text_size=15.5),
    text_style=Styles.WhiteBold.patch(text_size=11.0),
    description_style=Styles.White.patch(text_size=10.0),
    accent_style=Styles.WhiteFlat,
    icon_style=Styles.WhiteBold,
)
kpi.add(
    "4.2x",
    "ビルド処理速度",
    "差分 SQLite キャッシュ",
    icon=phosphor.cpu,
    style=Styles.PrimaryNeutral.patch(shape_r=1.8),
    accent_style=Styles.PrimaryFlat,
)
kpi.draw(xy=(6.0, 29.0), width=136.0, height=26.0, columns=3)

pipeline = ChevronProcess(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=10.8),
    description_style=Styles.Muted.patch(text_size=10.0),
    corner_angle=60.0,
    spacing=2.0,
    flat_left_end=True,
)
pipeline.add("1. 原稿執筆", description="Python + Markdown")
pipeline.add("2. グリッド検証", description="drawlib show -g")
pipeline.add(
    "3. 一括ビルド",
    description="HTML / PDF / Office",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=10.8),
    description_style=Styles.White.patch(text_size=10.0),
)
pipeline.add(
    "4. 公開配信",
    description="CI / 静的ポータル",
    style=Styles.SecondaryNeutral,
)
pipeline.draw(xy=(6.0, 7.0), width=136.0, height=16.5)

save()
```

## 7.1 全18種 SmartArts カタログと基準座標（アンカー）

Drawlib は左下 `(0, 0)`・上向き `+Y` のデカルト座標系を採用しているため、各 SmartArt の `.draw(xy=...)` がどの基準点（アンカー）を受け取るかを把握しておけば、試行錯誤なしで一発で正確な位置に配置できます。

- **左下アンカー `Bottom-Left (x0, y0)`**: 大半のボックス型コンポーネント（`ChevronProcess`、`KpiCards`、`GeoMap`、`*Calendar` など）は左下 `(x0, y0)` を起点に右方向（`+X`）・上方向（`+Y`）へ展開します。
- **左上アンカー `Top-Left (x0, y_top)`**: 上から下へ読む構造のコンポーネント（`Table`、`BulletPoints`、`SourceCode`、`TreeNode`）は左上 `(x0, y_top)` を起点に下方向（`-Y`）へ伸びるため、上側の `y_top` 座標を渡します。
- **中央アンカー `Center (cx, cy)`**: 放射状コンポーネント（`Cycle`、`MindMapNode`）は中心 `(cx, cy)` から周囲へ展開します。

### 7.1.1 プロセス・サイクル・タイムライン

| コンポーネント | 要素・補助モデル | `.draw(xy=...)` 既定アンカー | 主なエンジニアリング用途 |
| :--- | :--- | :--- | :--- |
| **`ChevronProcess`** | `ChevronItem` | **Bottom-Left** (`align="bottom_left"`) | CI/CD パイプライン、ETL 処理段階、段階的移行フロー（`flat_left_end=True`） |
| **`Cycle`** | `CycleItem`, `CycleCenter` | **Center** (`align="center"`) | PDCA 改善ループ、トークン更新サイクル、SRE 運用フィードバック |
| **`Roadmap`** | `RoadmapItem` | **Bottom-Left** (`align="bottom_left"`) | 四半期リリースマイルストーン、移行ロードマップ、障害時系列の記録 |

### 7.1.2 カード・グリッド・サマリー

| コンポーネント | 要素・補助モデル | `.draw(xy=...)` 既定アンカー | 主なエンジニアリング用途 |
| :--- | :--- | :--- | :--- |
| **`KpiCards`** (`KpiCard`) | `KpiCardItem` | **Bottom-Left** (`align="bottom_left"`) | SLA 目標値、レイテンシ指標、ベンチマーク結果のエグゼクティブサマリー |
| **`CardList`** | `CardListItem` | **Bottom-Left** (`align="bottom_left"`) | 縦並び・横並びの機能カード一覧（オプションで `->` 接続矢印付き） |
| **`BoxList`** | `BoxListItem` | **Bottom-Left** (`align="bottom_left"`) | 密着配置のサービス群、プロトコルヘッダ構造、ステータスバッジ列 |
| **`GridLayout`** | `GridItem` | **Bottom-Left** (`align="bottom_left"`) | 行・列結合に対応した多層アーキテクチャマトリクス（`row=0` が最下段） |
| **`Pyramid`** | `PyramidItem` | **Bottom-Left** (`align="bottom_left"`) | テストピラミッド、記憶階層モデル、多層防御セキュリティ構造 |
| **`Panel`** | — | **Bottom-Left** (`align="bottom_left"`) | タイトル付き枠コンテナ（`"filled"` / `"underline"` / `"floating"` / `"window"`） |

### 7.1.3 テーブル・箇条書き・ソースコード

| コンポーネント | 要素・補助モデル | `.draw(xy=...)` 既定アンカー | 主なエンジニアリング用途 |
| :--- | :--- | :--- | :--- |
| **`Table`** | — | **Top-Left** (`align="top_left"`) | サービス SLA 一覧表、機能比較マトリクス、クォータ仕様表（`draw_flexible`） |
| **`BulletPoints`** | `BulletPointItem` | **Top-Left** *(固定 `(x, y)`)* | 設計レビュー要点、チェックリスト、スライド内の構造化箇条書き |
| **`SourceCode`** | `SourceCodeStyles`, `sourcecode` | **Top-Left** (`align="top_left"`) | 図内に直接埋め込む構文ハイライト付き Python / YAML / JSON コード枠 |

### 7.1.4 ツリー階層・マインドマップ

| コンポーネント | 要素・補助モデル | `.draw(xy=...)` 既定アンカー | 主なエンジニアリング用途 |
| :--- | :--- | :--- | :--- |
| **`TreeNode`** | — | **Top-Left** *(固定 `(x, y)`)* | モノレポのディレクトリ構成、パッケージ階層、CLI サブコマンド体系 |
| **`MindMapNode`** | — | **Center** *(固定 `(cx, cy)`)* | 上下左右4方向に展開するシステム分類図、ドメイン分割、組織図 |

### 7.1.5 地図・カレンダースケジュール

| コンポーネント | 要素・補助モデル | `.draw(xy=...)` 既定アンカー | 主なエンジニアリング用途 |
| :--- | :--- | :--- | :--- |
| **`GeoMap`** | — | **Bottom-Left** (`align="bottom_left"`) | マルチリージョン拠点マップ（`World` / `Countries` / `Cities`、`lonlat_to_xy`） |
| **`MonthCalendar`** | `CalendarItem` | **Bottom-Left** (`align="bottom_left"`) | 7列の月間・複数週リリース計画カレンダー（ISO 8601 `"YYYY-MM-DD"`） |
| **`WeekCalendar`** | `CalendarItem` | **Bottom-Left** (`align="bottom_left"`) | 時間軸付きのスプリント計画・メンテナンス枠（`"YYYY-MM-DD HH:MM"`） |
| **`DayCalendar`** | `CalendarItem` | **Bottom-Left** (`align="bottom_left"`) | 1日単位のタイムライン、障害対応・切り替え作業ランブック |

> **ヒント — Top-Left 系と Bottom-Left 系を横並びで揃える計算式**: 高さ `H` の `Table` や `TreeNode` を、下端 `y_bottom` の Bottom-Left コンポーネントと上端揃えにするには、`xy=(x0, y_bottom + H)` を渡します（`Table` と `SourceCode` では `align="bottom_left"` の直接指定も可能です）。

## 7.2 左上アンカーの組み合わせ：Table と TreeNode の並列配置

`Table` と `TreeNode` はどちらも **左上 `Top-Left (x0, y_top)`** を起点とするため、仕様表とディレクトリ構成を横並びに配置する設計図で抜群の相性を発揮します。

- **`Table` のセルスタイル適用順序ルール**: `Table` は登録順にセル装飾を上書き評価します。`0` 行目（ヘッダー）は偶数インデックスであるため、ゼブラ配色を行う `set_style_cell_evenodd(...)` を **先に** 呼び出し、**その後に** `set_style_cell_header(...)` でヘッダー行を再設定し、最後に `set_style_cell(..., rows=[r], columns=[c])` で注目セルを強調します。
- **`TreeNode` のルート継承とアイコン登録**: ルート `TreeNode` に5つのレイアウト設定（`text_style`、`line_style`、`line_horizontal_margin`、`line_horizontal_length`、`line_vertical_margin`）を指定すると子孫ノードへ自動継承されます。`TreeNode.register_drawing_item(...)` と `.set_drawing_item(name)` で `phosphor` アイコンを付与でき、構築済みノードは `children=[...]`、文字列からの動的追加は `node.add("filename.py")` を使います。

```drawlib align=center code=fold file=smartarts_table_tree_ja.png caption="図 7.2: 左上アンカー（Top-Left）で揃えた Table と TreeNode の並列レイアウト"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.shapes import rectangle
from drawlib.smartarts import Table, TreeNode
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=148, height=64)

text(
    (43.0, 56.5),
    "プロジェクト種別と出力マトリクス (Table)",
    style=Styles.DarkBold.patch(text_size=11.5),
)
text(
    (114.5, 56.5),
    "自動生成されるディレクトリ構成 (TreeNode)",
    style=Styles.DarkBold.patch(text_size=11.5),
)

table = Table(
    cell_style=Styles.White,
    text_style=Styles.Dark.patch(text_size=10.2),
    header_cell_style=Styles.DarkFlat,
    header_text_style=Styles.WhiteBold.patch(text_size=10.5),
    border_style=Styles.MutedThin,
)
table.set_style_cell_evenodd(
    even_color=Colors.Gray1,
    even_text_style=Styles.Dark.patch(text_size=10.2),
    odd_color=Colors.White,
    odd_text_style=Styles.Dark.patch(text_size=10.2),
)
table.set_style_cell_header(
    background_color=Colors.Gray8,
    text_style=Styles.WhiteBold.patch(text_size=10.5),
)
table.set_style_cell(
    background_color=Colors.Primary,
    text_style=Styles.WhiteBold.patch(text_size=10.2),
    rows=[1],
    columns=[2],
)
table.set_style_border(
    top=Styles.DarkBold.patch(line_width=1.4),
    top2=Styles.DarkBold.patch(line_width=1.0),
    bottom=Styles.DarkBold.patch(line_width=1.4),
    between_rows=Styles.MutedThin.patch(line_width=0.6),
)

matrix = [
    ["種別", "主な Web 出力", "Office / 印刷出力"],
    ["doc", "章構成 HTML", "PDF + DOCX"],
    ["site", "多階層ドキュメント", "llms.txt + SEO"],
    ["catalog", "検索付き API 辞書", "JSON インデックス"],
    ["slide", "16:9 Web スライド", "PDF + PPTX"],
]
table.draw_flexible(
    xy=(7.0, 51.5),
    column_widths=[18.0, 29.0, 25.0],
    row_heights=[8.6, 8.6, 8.6, 8.6, 8.6],
    data=matrix,
    align="top_left",
)

rectangle(
    (114.5, 30.0),
    width=53.0,
    height=43.0,
    style=Styles.Neutral.patch(shape_r=2.0),
)

TreeNode.register_drawing_item(
    name="ch07_dir_ja",
    location="before",
    padding_width=4.4,
    function=phosphor.folder,
    style=Styles.PrimaryBold,
    args={"width": 3.2},
)
TreeNode.register_drawing_item(
    name="ch07_py_ja",
    location="before",
    padding_width=4.4,
    function=phosphor.file_py,
    style=Styles.SecondaryBold,
    args={"width": 3.2},
)
TreeNode.register_drawing_item(
    name="ch07_md_ja",
    location="before",
    padding_width=4.4,
    function=phosphor.file_text,
    style=Styles.DarkBold,
    args={"width": 3.2},
)

root = TreeNode(
    "quickstart/",
    text_style=Styles.DarkBold.patch(text_size=10.2),
    line_style=Styles.Muted.patch(line_width=1.1),
    line_horizontal_margin=2.8,
    line_horizontal_length=2.8,
    line_vertical_margin=5.4,
    children=[
        TreeNode(
            "en/",
            text_style=Styles.DarkBold.patch(text_size=10.2),
            children=[
                TreeNode("00_cover.md", text_style=Styles.Dark.patch(text_size=10.0)).set_drawing_item("ch07_md_ja"),
                TreeNode("07_smartarts.md", text_style=Styles.PrimaryBold.patch(text_size=10.0)).set_drawing_item("ch07_md_ja"),
            ],
        ).set_drawing_item("ch07_dir_ja"),
        TreeNode(
            "ja/",
            text_style=Styles.DarkBold.patch(text_size=10.2),
            children=[
                TreeNode("07_smartarts.md", text_style=Styles.Dark.patch(text_size=10.0)).set_drawing_item("ch07_md_ja"),
            ],
        ).set_drawing_item("ch07_dir_ja"),
    ],
).set_drawing_item("ch07_dir_ja")
root.add("styles.py", text_style=Styles.Dark.patch(text_size=10.0)).set_drawing_item("ch07_py_ja")

root.draw(xy=(91.5, 47.0))

save()
```

## 7.3 `show=False` による段階的ビルドとアニメーション対応

状態を持つすべての SmartArt は4段階のライフサイクル（**インスタンス生成 -> `.add()` で要素登録 -> `.items` / `.children` の状態変更 -> `.draw()` で描画**）に従います。登録された各アイテムおよびノード（`ChevronItem`、`KpiCardItem`、`CardListItem`、`BoxListItem`、`CycleItem`、`GridItem`、`PyramidItem`、`RoadmapItem`、`BulletPointItem`、`CalendarItem`、`TreeNode`、`MindMapNode`）は共通して `show: bool = True` 属性を備えています。

`item.show = False` を設定（または `.add(..., show=False)` を指定）すると、**他の兄弟要素の幅・列位置・円周角度・行間隔を一切変化させずに該当要素だけを非表示**にできます。これにより、16:9 スライドの段階表示や `drawlib.anim` によるマルチフレームアニメーションでも、前段の要素がガタつくことなく滑らかにステップを追加できます。

```python
from drawlib.canvas import save, setup
from drawlib.smartarts import ChevronProcess
from drawlib.styles import Styles

setup(width=120, height=32)

flow = ChevronProcess(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=10.5),
    description_style=Styles.Muted.patch(text_size=10.0),
    flat_left_end=True,
)
flow.add("1. 収集", description="Parquet ストリーム")
flow.add(
    "2. 検証",
    description="スキーマ検査",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=10.5),
    description_style=Styles.White.patch(text_size=10.0),
)
# フレーム1では非表示にしても、ステップ1・2は4列分の正確な幅と座標を維持
step3 = flow.add("3. 変換", description="ベクトル結合", show=False)
step4 = flow.add("4. 配信", description="低遅延 API", show=False)

flow.draw(xy=(8.0, 8.0), width=104.0, height=16.0)
save()
```

各 SmartArt の詳細なコンストラクタ引数は、`uv run drawlib rules show lib-smartarts-overview`（または `lib-smartarts-calendar`、`lib-smartarts-geomap`、`lib-smartarts-source-code` などの個別トピック）でいつでも参照できます。
