# 第8章: SmartArts（構造化ビジュアル）

`drawlib.smartarts` は、手作業で個々の四角形や直線の座標を計算することなく、洗練された構造化図版を自動レイアウトする高レベルモジュールです。

## 8.1 利用可能な SmartArts コンポーネント

- **`ChevronProcess`**: 矢羽型（シェブロン）による工程・デプロイパイプライン表現。
- **`Table`**: 均等セル配置、ヘッダー強調、罫線装飾を備えたデータ比較テーブル。
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

```drawlib 620px center file:fig_smartarts_sample.png caption:"図 8.1: ChevronProcess と Table を組み合わせたリリースフロー"
from drawlib.canvas import setup
from drawlib.smartarts import ChevronProcess, Table
from drawlib.styles import Styles

setup(width=110, height=65)

# 1. パイプラインの定義 (ChevronProcess)
pipeline = ChevronProcess(
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold,
    description_style=Styles.Muted,
    corner_angle=60.0,
    spacing=1.5,
    flat_left_end=True,
)
pipeline.extend(
    texts=["1. 要件定義", "2. 実装", "3. テスト", "4. デプロイ"],
    styles=Styles.PrimaryFlat,
    descriptions=["Issue 整理", "AI ペアプロ", "pytest 検証", "CI 自動配信"],
)
pipeline.draw(xy=(8, 48), width=94, height=12)

# 2. 比較表の定義 (Table)
table = Table(
    cell_style=Styles.White,
    text_style=Styles.Dark,
    header_cell_style=Styles.PrimaryFlat,
    header_text_style=Styles.WhiteBold,
    border_style=Styles.MutedDashed,
)
table.draw(
    xy=(8, 42),
    width=94,
    height=34,
    data=[
        ["カテゴリ", "主要コンポーネント", "メリット"],
        ["SmartArts", "ChevronProcess, Table, MindMap", "手作業の座標計算が不要"],
        ["Diagrams", "Architecture, Sequence, Flow", "業界標準記法に準拠した設計図"],
        ["Charts", "Gantt, Bar, Line, Pie", "ロードマップや進捗の可視化"],
    ],
)
```
