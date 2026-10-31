# リリースノートと移行ガイド

## バージョン 0.3.2

*リリース日: 2026/10/30*

バージョン 0.3.2 では、ネイティブで編集可能な **MS Word（`.docx`）** および **MS PowerPoint（`.pptx`）** エクスポーターを新搭載し、**ヘッドレス Chromium・`python-docx`・`python-pptx`** を追加設定不要の標準依存パッケージへと統合したほか、組み込みの AI エージェントルールをカテゴリ別のモジュールディレクトリ構成へ再編成しました。

---

### ハイライトと新機能

#### 1. MS Word（`.docx`）・MS PowerPoint（`.pptx`）エクスポート（`drawlib build docx`, `drawlib build pptx`）
- **`drawlib build docx` と `drawlib.tools.build_docx()`**: 単一構成の `doc` プロジェクトまたは個別の `.md` ファイルを、スタイル付き見出し、本文、箇条書き・番号付きリスト、テーブル、引用ブロック、シンタックスハイライト付きコードブロック、任意の表紙ページ、自動目次（`--generate-index`）を備えたネイティブ編集可能な MS Word（`.docx`）文書へコンパイルします。````drawlib```` コードブロック（SVG、WebP、アニメーションを含む）は鮮明な高 DPI 静止画 PNG（デフォルト `--dpi 200`）として埋め込まれます。
- **`drawlib build pptx` と `drawlib.slide.build_pptx()` / `drawlib.tools.build_pptx()`**: ヘッドレス Chromium を用いて `1920x1080` スライドのレイアウト座標と計算済み CSS スタイルを計測し、ネイティブ編集可能な 16:9（`960x540 pt`）MS PowerPoint（`.pptx`）デッキを出力します。`rgba` アルファ塗りつぶし・枠線を持つ `::: block` カード、テキストボックス、箇条書き・番号付きリスト、テーブル、インラインコード、`::: note` スピーカーノートを保持しつつ、````drawlib```` 図解を高 DPI 静止画 PNG（デフォルト `--dpi 240`、`--anim-frame first|last` はデフォルト `last`）として埋め込みます。

#### 2. ゼロ設定のヘッドレス Chromium と標準依存パッケージの統合
- **標準依存パッケージへの統合**: `playwright>=1.49.0`、`python-docx>=1.2.0`、`python-pptx>=1.0.2` を標準の `dependencies` に昇格させ、`[project.optional-dependencies]` を廃止しました。`uv add drawlib` や `pip install drawlib` を実行するだけで、追加フラグなしで PDF、MS Word、MS PowerPoint エクスポートがそのまま利用できます。
- **ヘッドレスブラウザの自動プロビジョニング**: `drawlib build pdf` または `drawlib build pptx` の初回実行時に、Playwright 同梱ドライバ経由で `chromium-headless-shell` が自動インストールされます。オフライン環境向けの明示的な事前ダウンロード（`drawlib cache download --browser`、および `drawlib cache download --all` に統合）と、最小構成の Linux コンテナ向け共有ライブラリ診断ガイド（`playwright install-deps chromium`）も追加されました。

#### 3. カテゴリ別モジュール構造の AI エージェントルール（`drawlib rules`）
- **モジュール化された `_rules/` 構成**: 保守性の向上と高速なトピック検索のため、組み込みルールマニュアル（`src/drawlib/_rules/`）をカテゴリ別ディレクトリ（`charts/`, `diagrams/`, `graph/`, `icons/`, `shapes/`, `smartarts/`）へ再編成しました。

---

## バージョン 0.3.1

*リリース日: 2026/10/23*

バージョン 0.3.1 では、**`drawlib.charts.heatmap`** 可視化スイート（`HeatmapChart` および `HeatmapOverlay`）を新たに追加するとともに、ライブラリ全体および CLI の **起動・インポート性能の大幅な最適化** を実施しました。

---

### ハイライトと新機能

#### 1. 2D マトリクスヒートマップと空間サーマルオーバーレイ（`drawlib.charts.heatmap`）
- **`HeatmapChart`**: カテゴリ軸 `x_categories`・`y_categories` 上の宣言的 2D マトリクス／グリッドヒートマップです。`Style` ベースの多段階カラー補間（`styles=[...]` または `min_style` / `max_style`）、自動コントラスト調整付きのセル内数値ラベル、セル間隔・角丸の調整（`cell_gap`, `cell_r`）、連続カラーバー（`draw_colorbar`）、段階スウォッチ凡例（`draw_legend`）を備えています。
- **`HeatmapOverlay`**: 既存のダイアグラム（`ClassDiagram`, `ArchitectureDiagram`, `ERDiagram`, `FlowDiagram`, `GeoMap` など）の上に直接重ねて描画できる空間サーマル・ホットスポットオーバーレイです。`"smooth"`（2D ガウス熱分布グラデーション）または `"contour"`（同心ベクター等高線リング）モードと、`"add"` / `"max"` 集約（`Spot`）により、複雑度やインシデント密度、地域別ホットスポットを視覚的に強調できます。

#### 2. 起動・インポート性能の大幅な最適化
- **PEP 562 によるモジュールおよびアイコンスイートの遅延ロード**: `drawlib`、`drawlib.tools`、`drawlib.styles`、`drawlib.preset_styles`、`drawlib.preset_colors`、`drawlib.smartarts`、`drawlib.charts`、`drawlib.diagrams`、`drawlib.icons`、および各 CLI サブコマンドにサブモジュール遅延インポートを導入しました。`drawlib` のインポート、描画を伴わない `drawlib.tools` ユーティリティの呼び出し、軽量な CLI コマンド（`drawlib --version`, `drawlib init`, `drawlib serve`）の実行時に `matplotlib` や未使用のドメインモジュールが読み込まれなくなり、起動レイテンシを **15〜40 倍高速化**（`import drawlib` 時の関数呼び出し回数を **99% 以上削減**）しました。
- **プリセットテーマのオンデマンド生成と高速な `Style` 構築**: プリセットテーマ（`DefaultStyles`, `GoogleStyles`, `MonochromeStyles` など）のインスタンス化を初回アクセス時まで遅延させ、組み込みスタイルトークンへの `defer_build=True` と `model_construct` 高速パスの採用、`_BaseStylesMeta` の属性探索最適化、および `@validate_call` スキーマコンパイルの初回呼び出し時への遅延を実現しました。

#### 3. バグ修正と互換性向上
- Pydantic v2.11 以降で `BaseStyles` インスタンスの `model_fields` にアクセスした際に発生していた `PydanticDeprecatedSince211` 非推奨警告を解消しました。

---

## バージョン 0.3.0

*リリース日: 2026/10/21*

バージョン 0.3.0 は Drawlib にとって大きなアーキテクチャ上のマイルストーンであり、単なるベクター描画ツールから、ソフトウェア開発者と **自律型 AI コーディングエージェント** の双方に向けて設計された包括的な **「Illustration & Documentation as Code（コードとしての図解とドキュメント）」** プラットフォームへと進化しました。

---

### ハイライトと新機能

#### 1. モダンなフラットパッケージ構成
- 従来のバージョン名前空間付きパッケージを、標準的でモダンなフラットパッケージ構造（`drawlib`）へ統合しました。
- 各ドメインモジュールから直感的かつ簡潔にパブリック API をインポートできます。
  - `drawlib.canvas`, `drawlib.math`, `drawlib.types`, `drawlib.fonts`
  - `drawlib.shapes`, `drawlib.lines`, `drawlib.text`, `drawlib.icons`, `drawlib.images`
  - `drawlib.graph`, `drawlib.smartarts`, `drawlib.charts`, `drawlib.diagrams`
  - `drawlib.anim`, `drawlib.slide`, `drawlib.tools`
  - `drawlib.styles`, `drawlib.preset_colors`, `drawlib.preset_styles`, `drawlib.utils`

#### 2. 統合ドキュメントビルダ・スライドコンパイラ・開発者ツール（`drawlib.tools`）
- ネイティブの Markdown・HTML・スライド・PDF コンパイラ（`drawlib build html`, `drawlib build markdown`, `drawlib build pdf`, `drawlib build slide`, `drawlib build image`）を搭載しました。
- ````drawlib```` コードブロックを含む Markdown ドキュメントから以下の成果物をコンパイルできます。
  - レスポンシブなマルチページ静的 HTML ドキュメントサイト（`docs_html/`）。
  - 画像リンクが埋め込まれた GitHub 最適化 Markdown ドキュメント（`docs/`）。
  - 印刷品質のベクター PDF ドキュメント（`doc.pdf` / `slide.pdf`）。
  - インタラクティブな 16:9 ワイドスクリーン HTML プレゼンテーションデッキ（`slide_html/`）。
- **SQLite 差分ビルドキャッシュ（`.drawlib/cache.db`）**: コードブロック、`styles.py`、`utils.py`、およびローカルアセットの決定論的な SHA-256 コンテンツハッシュにより、未変更の図解の不要な再レンダリングを防止します。
- **プログラマティック開発者 API（`drawlib.tools`）**: CI/CD やカスタム自動化向けに完全な Python API（`build_html`, `build_markdown`, `build_pdf`, `build_slide`, `build_image`, `export_code_block`, `init_project`, `serve_docs`, `list_cache`, `download_cache`, `clear_cache`）を提供します。

#### 3. 自動レイアウトグラフエンジン（`drawlib.graph`）
- 手作業の座標計算を不要にし、ネストされた `Cluster` コンテナもサポートする 5 種類の専用自動レイアウトソルバーを搭載しました。
  - **`LayerGraph`**: 杉山法ベースの階層型 DAG レイアウト。
  - **`ArchitectureGraph`**: セマンティックなティア整列を備えたクラウド・システムトポロジソルバー。
  - **`TreeGraph`**: バランスの取れた親子階層ツリーレイアウト。
  - **`RadialGraph`**: 同心円状の放射リングレイアウト。
  - **`GridGraph`**: 構造化されたマトリクス配置ソルバー。
- **2 ステップのレイアウト確認とダイアグラム描画（`get_layout()`）**: 構造化された `GraphLayout` 座標（`xy`, `bottom_left`, `local_xy`, `local_bottom_left`, `points`）を算出し、人間にも AI にも読みやすい `print(layout)` 出力による確認と `offset()` による微調整が可能です。

#### 4. 高水準テクニカルダイアグラム（`drawlib.diagrams`）
- **アーキテクチャ図（`drawlib.diagrams.architecture.ArchitectureDiagram`）**: クラウドトポロジ、ネストされたクラスタグループ、Phosphor アイコンおよび公式 GCP ベクターアイコンに対応。
- **フロー図（`drawlib.diagrams.flow.FlowDiagram`）**: 標準フローチャート記号（ISO 5807 / JIS X 0121）、条件分岐、T 字合流、スイムレーン（`Lane`）に対応。
- **シーケンス図（`drawlib.diagrams.sequence.SequenceDiagram`）**: クライアント／サーバーのライフライン、実行仕様バー（アクティベーション）、同期／非同期メッセージ矢印、自己呼び出し、複合フラグメント（`alt`, `opt`, `loop`, `par`）に対応。
- **ER 図（`drawlib.diagrams.er.ERDiagram`）**: IE 記法（鳥の足記法 / Crow's Foot）のフルサポート、テーブルエンティティ区画、自動直交ルーティングに対応。
- **UML クラス図（`drawlib.diagrams.class_diagram.ClassDiagram`）**: 3 区画のクラスカード、ステレオタイプ（`«interface»`）、可視性記号、各種関連メソッド（`inherit()`, `realize()`, `composite()`, `aggregate()`, `associate()`, `depend()`）に対応。
- **ステートマシン図（`drawlib.diagrams.state.StateDiagram`）**: 開始／終了擬似状態、内部アクティビティ区画（`entry`, `do`, `exit`）、曲率制御付きの曲線遷移、自己遷移ループを備えた宣言的ステートチャート。

#### 5. Pure Python の宣言的チャート（`drawlib.charts`）
- 外部プロット専用ツールへの依存なしで以下の定量チャートを描画できます。
  - **BarChart**: 縦棒／横棒、集合（グループ）、積み上げ棒グラフ。
  - **LineChart**: 直線セグメント、滑らかなスプライン曲線、カスタムマーカー付き折れ線グラフ。
  - **AreaChart**: 重ね合わせおよび累積積み上げの面グラフ。
  - **PieChart**: 中央 KPI バッジに対応した円グラフおよびドーナツグラフ。
  - **RadarChart**: 多軸スパイダーウェブおよび同心円リングのレーダーチャート。
  - **ScatterChart**: カスタムマーカー形状に対応した 2D 散布図およびバブルチャート。
  - **GanttChart**: プロジェクト工程表、進捗バー、マイルストーン、タスク間依存矢印を備えたガントチャート。

#### 6. 拡張された SmartArts と地理マップ（`drawlib.smartarts`）
- **`GeoMap`**: 国・都道府県のハイライト、ピン、接続アーク、コロプレス（階級区分）色分けに対応したオフラインベクター地図（`World`, `Asia`, `Europe`, `USA`, `Japan` など）。
- **`TreeNode` と `MindMapNode`**: 階層型ノードツリーと放射状のブレインストーミング用マインドマップ。
- **`SourceCode`**: 行番号、ウィンドウフレーム、ダーク／ライトテーマを備えたシンタックスハイライト付きソースコードカード。
- **`ChevronProcess` と `Cycle`**: 順次シェブロン工程パイプラインと、中央ハブ付きの放射状サイクル図。
- **`Table`, `GridLayout`, `Pyramid`, `BoxList`, `BulletPoints`**: 構造化された表形式およびカードベースのビジュアルコンポーネント群。

#### 7. マルチフレームアニメーション（`drawlib.anim`）と 16:9 プレゼンテーションステージ（`drawlib.slide`）
- **`drawlib.anim.Animation`**: フレームコンテキストマネージャ（`with anim.frame():`）、FPS 設定、`drawlib.math` の補間ヘルパーを備え、ロスレス **APNG** および **アニメーション WebP** を出力する宣言的マルチフレームアニメーションビルダ。
- **`drawlib.slide`**: Markdown レイアウトコンテナ（`::: block`, `::: note`）、発表者ビュー（`?presenter=1`）、`current_slide` ランタイムプロキシ（`SlideContext`, `BoundingBox`）を備えた共通 `1920x1080`（16:9 ワイドスクリーン）プレゼンテーション座標ステージ。

#### 8. AI エージェントガイドラインとルールシステム（`drawlib rules`）
- CLI からオンデマンドで参照できる組み込みマニュアルを提供。
  - `drawlib rules show <topic>`: 簡潔な構文マニュアルをエージェントのコンテキストウィンドウへ直接注入。
  - `drawlib rules list`: 利用可能なすべての描画ルールトピックを一覧表示。
- 座標グリッドオーバーレイ（`drawlib show -g`）による自律的な視覚的自己修正ループをサポート。

#### 9. プロジェクトスキャフォールディング（`drawlib init`）
- 主要な 4 つのユースケースに対応する完全なスタータープロジェクトを即座に生成。
  - `drawlib init doc`: 単一構成の技術ドキュメント（HTML、PDF、Markdown、画像）。
  - `drawlib init site`: マルチページのドキュメント Web サイト。
  - `drawlib init slide`: 16:9 プレゼンテーションスライドデッキ（Web およびベクター PDF）。
  - `drawlib init images`: スタンドアロン Python 図解の一括生成プロジェクト。

---

### 破壊的変更と v0.2 からの移行ガイド

Drawlib v0.2 からアップグレードする場合は、以下の必須変更点を確認してください。

1. **Python 3.11 以降が必須**: Python 3.10 以前のサポートは終了しました。
2. **トップレベル CLI `drawlib export` の廃止**:
   - 代わりに `drawlib show input.py -o output.png` を使用してください。
3. **旧 `dsart` 名前空間の廃止と `Tree` から `TreeNode` への改名**:
   - `from drawlib.apis import dsart` を以下のように変更してください。
     ```python
     from drawlib.smartarts import Table, TreeNode, MindMapNode, ChevronProcess, Cycle, GeoMap, SourceCode
     ```
4. **セマンティックスタイル名の正規化**:
   - スタイルトークンは PascalCase（`Styles.PrimaryFlat`, `Styles.AccentBold`）に統一されました。従来の snake_case スタイル属性は完全に廃止されています。
5. **ダイアグラムクラス名の統一**:
   - すべてのダイアグラムコンテナは `Diagram` サフィックス付きの PascalCase に統一されました。
     - `ArchitectureDiagram`
     - `ERDiagram`
     - `FlowDiagram`
     - `SequenceDiagram`
     - `ClassDiagram`
     - `StateDiagram`

---

## バージョン 0.2.x アーカイブ

- **v0.2.3**（2024/09/08）: ブロック矢印関数（`arrow_polyline`, `arrow_l`, `arrow_u`, `arrow_arc`）および初期 SmartArts（`Table`, `Tree`, `GridLayout`, `Pyramid`, `BoxList`, `BulletPoints`）を追加。
- **v0.2.2**（2024/07/02）: Drawlib 0.2 の初回パブリックリリース。
