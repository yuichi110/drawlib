# 第8章: SmartArts（構造化ビジュアル）

`drawlib.smartarts` は、手作業で個々の四角形や直線の座標を計算することなく、洗練された構造化図版を自動レイアウトする高レベルモジュールです。SmartArts コンポーネントの `.draw(xy=...)` は、コンポーネント全体の **左下座標 `(x0, y0)`** を基準に配置します（`Table` は `align="bottom_left"` またはデフォルトの `align="top_left"` を指定可能）。

## 8.1 利用可能な SmartArts コンポーネント

- **`ChevronProcess`**: 矢羽型（シェブロン）による工程・デプロイパイプライン表現。
- **`Table`**: 均等セル配置、ヘッダー強調、罫線装飾を備えたデータ比較テーブル。
- **`GeoMap`**: 世界・地域・日本都道府県のオフラインベクター地図、特定国や都道府県のハイライト、ピン配置、拠点間アーク接続。
- **`MindMapNode`**: 放射状または特定方向に広がるアイデアマップ・機能構造図。
- **`TreeNode`**: 組織図やディレクトリツリーを表す階層構造図。
- **`Cycle`**: フィードバックループや継続的改善サイクル図。
- **`Pyramid`**: テストピラミッドやセキュリティ階層モデル。
- **`BoxList` / `BulletPoints`**: 箇条書きやカードスタックの整列配置。
- **`GridLayout`**: 均等グリッドによるダッシュボード風レイアウト。
- **`SourceCode`**: シンタックスハイライト付きコードブロック表示。

> [!NOTE]
> 特定のノードを指し示すコールアウト吹き出しは、基本図形モジュール `drawlib.shapes.bubblespeech` から利用できます。

## 8.2 パイプラインと機能比較の作成例

```drawlib align=center file=fig_smartarts_sample.png caption="図 8.1: ChevronProcess と Table を組み合わせたリリースフロー"
from drawlib.canvas import save, setup
from drawlib.smartarts import ChevronProcess, Table
from drawlib.styles import Styles

setup(width=110, height=65)

# 1. パイプラインの定義 (ChevronProcess: PrimaryNeutral ベース + 主役ステップのみ PrimaryFlat)
pipeline = ChevronProcess(
    style=Styles.PrimaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=10.5),
    description_style=Styles.Dark.patch(text_size=9.5),
    corner_angle=60.0,
    spacing=1.5,
    flat_left_end=True,
)
pipeline.add("1. 要件定義", description="Issue 整理")
pipeline.add(
    "2. 実装",
    description="AI ペアプロ",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=10.5),
    description_style=Styles.White.patch(text_size=9.5),
)
pipeline.add("3. テスト", description="pytest 検証")
pipeline.add("4. デプロイ", description="CI 自動配信")
pipeline.draw(xy=(6, 46), width=98, height=14)

# 2. 比較表の定義 (Table)
table = Table(
    cell_style=Styles.Neutral,
    text_style=Styles.Dark.patch(text_size=10.0),
    header_cell_style=Styles.PrimaryFlat,
    header_text_style=Styles.WhiteBold.patch(text_size=10.5),
    border_style=Styles.Muted,
)
table.draw(
    xy=(6, 6),
    width=98,
    height=35,
    align="bottom_left",
    data=[
        ["カテゴリ", "主要コンポーネント", "メリット"],
        ["SmartArts", "ChevronProcess, Table, GeoMap", "手作業の座標計算が不要"],
        ["Diagrams", "Architecture, Sequence, Flow", "業界標準記法に準拠した設計図"],
        ["Charts", "Gantt, Bar, Line, Pie, Scatter", "ロードマップや定量指標の可視化"],
    ],
)

save()
```
