# 第3章: Drawlib の全体像と主要機能

Drawlib は、"Illustrated Documentation as Code" を支える統合描画・ドキュメント作成プラットフォームです。ドキュメント構築パイプラインに加え、低レベルの基本図形描画から高度なシステムアーキテクチャ設計、プレゼンテーション・アニメーション生成までをカバーする 6 つの機能レイヤーを提供しています。

## 3.1 描画・ドキュメントコンポーネントレイヤー

| レイヤー | 提供モジュール | 主な用途・描画対象 |
| :--- | :--- | :--- |
| **1. Primitives (基本要素)** | `drawlib.shapes`, `lines`, `text`, `icons`, `images` | **43種**の幾何図形、折れ線・曲線・ブロック矢印、リッチテキスト、Phosphor / FontAwesome / 公式 GCP アイコン |
| **2. SmartArts (構造化)** | `drawlib.smartarts` | プロセスシェブロン、表組み (`Table`)、オフライン世界・日本地図 (`GeoMap`)、シンタックスハイライト付きコードカード (`SourceCode`)、マインドマップ (`MindMapNode`)、ツリー階層 (`TreeNode`)、サイクル図 (`Cycle`)、ピラミッド、グリッド等 |
| **3. Charts (定量データ)** | `drawlib.charts` | ガントチャート、棒グラフ、折れ線グラフ、面グラフ、円・ドーナツグラフ、レーダー、散布図・バブルチャート（共通軸・対数スケール・凡例基盤） |
| **4. Diagrams & Graphs (システム設計)** | `drawlib.diagrams`, `drawlib.graph` | クラウド構成図、フロー図、シーケンス図、ER図、クラス図、状態遷移図、および 5 種の Pure Python 自動レイアウトソルバー (`get_layout()`) |
| **5. Presentation & Animation** | `drawlib.slide`, `drawlib.anim` | 16:9 プレゼンテーションステージ (`::: block` / `::: note`, Presenter View)、APNG / Animated WebP マルチフレームアニメーション |
| **6. Builder, CLI & Tools (ドキュメント基盤)** | `drawlib.tools`（CLI: `drawlib`） | HTML / PDF / スライド / Markdown / 画像一括ビルド、SQLite 差分ビルドキャッシュ (`.drawlib/cache.db`)、アセットキャッシュ管理 (`drawlib cache`)、ローカル検証サーバー (`drawlib serve --check`) |

## 3.2 統一デザインシステムとセマンティックカラー

Drawlib では、作図のたびに RGB 値を迷う必要はありません。洗練された **セマンティック 6 色パレット** と **ニュートラルベースライン**、および一貫したスタイル命名規則が標準で組み込まれています。

- **`Styles.Neutral` / `Styles.PrimaryNeutral` / `Styles.SecondaryNeutral`**: 図版全体の土台となる落ち着いたニュートラルカード（淡いグレー・ブルーグレー・スレート系）
- **`Styles.Primary`**: システムの中核ノードや主動線（青系）
- **`Styles.Secondary`**: 外部システムやクライアント（スレート・インディゴ系）
- **`Styles.Accent`**: 注目させたいハイライトや補助サービス（アンバー・ティール系）
- **`Styles.Muted`**: 境界枠や補助注記、背景コンテナ（薄いグレー系）
- **`Styles.Success` / `Styles.Danger`**: 正常ステータス（緑系）および異常・警告・エラー（赤系）

各カラーには `PrimaryFlat`（塗りつぶし）、`PrimaryOutline`（枠線）、`PrimaryBold`（太線）、`PrimaryDashed`（破線）などの PascalCase 定数トークンが用意されています。

### 50%以上ニュートラルベースライン原則（虹色ダイアグラムの防止）

すべてのノードに鮮やかな原色（`PrimaryFlat`, `AccentFlat`, `SuccessFlat` 等）を割り当てると、どこが重要なのか判別できない「虹色ダイアグラム」になってしまいます。Drawlib ではプロフェッショナルな視覚的階層を保つため、以下の配色原則を採用しています:

- **50%以上をニュートラルカードで構成**: 図内の 50% 以上のノードには **`Styles.Neutral`**、**`Styles.PrimaryNeutral`**、**`Styles.SecondaryNeutral`** を使用し、穏やかな背景トーンで構造を整えます。
- **高彩度カラーは 1〜2 個の焦点（Focal Point）に限定**: **`Styles.PrimaryFlat`** や **`Styles.AccentFlat`** などの強い塗りつぶしは、図の中で最も注目させたい 1〜2 個の主要要素だけに厳選して使用します。

### テキストおよび接続線のニュートラルカラー原則

視認性の確保と見やすいレイアウトのため、テキストと接続線にも以下の基本ルールが定められています:
- **ニュートラルタイポグラフィ**: 背景が明るいカードやキャンバス上では **`Styles.Dark`** または **`Styles.DarkBold`** を基本とします。`PrimaryFlat` などの濃い塗りつぶしノード内部では **`Styles.WhiteBold`** または **`Styles.Light`** を使用します（意味なく文字自体に `Primary` や `Secondary` を選ぶことは避けます）。
- **ニュートラルコネクタ**: 通常の処理進行や接続線・矢印は **`Styles.DarkBold`** を推奨します。`Styles.Primary` や `Styles.Danger` などのカラー矢印は、クリティカル動線やエラーロールバックなど、強調すべき意味がある場合のみ使用します。

## 3.3 日本語フォント・CJK の完全サポート

Drawlib は、日本語を含む多言語タイポグラフィをファーストクラスでサポートしています。
`--lang ja` を指定してプロジェクトを作成すると、以下の環境が自動的に整います:
- **HTML / PDF 出力**: Google Fonts（Noto Sans JP）およびローカルシステムフォント（Hiragino Sans, Yu Gothic）の適切なフォントスタックが適用されます。
- **キャンバス描画**: `drawlib.fonts.FontJapanese` が自動適用され、図形内の日本語テキストの文字化けやレイアウト崩れを防ぎます。
