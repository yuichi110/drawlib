# リリースノートと移行ガイド

## バージョン 0.3.5

*リリース日: 2026/11/03*

バージョン 0.3.5 では、API・CLI リファレンスやデータスキーマ辞書、マイクロサービス台帳、運用ランブックの構築に最適化された第 5 のプロジェクトアーキタイプ **図解付きカタログ & リファレンス（`catalog`, `drawlib init project catalog`）** を新搭載したほか、**宣言的プロジェクト SEO・Open Graph・`llms.txt` 自動生成（`[seo]`）**、**ゼロインストール `uvx` フォールバック対応ビルドスクリプト**、および **日英バイリンガル公式 Python API & CLI リファレンス（`/api/`）** を公開しました。

---

### ハイライトと新機能

#### 1. 図解付きカタログ & リファレンスプロジェクト（`catalog`, `drawlib init project catalog`）
- **`navbar.md` 不要の 2 カラム・カタログビルダ（`1 Markdown = 1 HTML ページ`）**: `drawlib init project catalog [target] [-l en,ja] [-s google]`（`drawlib.tools.init_project("catalog", ...)`）で初期構築できます。`<src_dir>/<lang>/` 内の各 Markdown ファイルから `# H1` カテゴリ（折りたたみ可能な `<details class="catalog-nav-group">`）と `## H2` エントリ（スクロールスパイ連動の `#slug` リンク）を自動抽出するため、手動の `navbar.md` 管理が不要です。
- **50 種以上のセマンティック `H2` バッジと `/` インクリメンタルフィルタ**: `## ` 見出し先頭にインラインコードの識別子（HTTP の `GET`・`POST`・`PUT`・`PATCH`・`DELETE`・`gRPC`、コード・CLI の `def`・`class`・`type`・`cmd`・`flag`・`env`・`config`、データ・基盤の `table`・`schema`・`service`・`job`・`pipeline`・`metric`、デザイン・規約の `token`・`style`・`icon`・`adr`・`rule`、状態の `ok`・`warn`・`error`・`deprecated` 等）を記述するだけで本文見出しとサイドバーの双方に色分けバッジを描画し、`/` キーによるリアルタイム絞り込み検索を提供します。
- **宣言的 `[catalog]` 設定と専用 CSS ターゲット**: `drawlib.toml` の `[catalog]` セクション（`sidebar_expanded`・`badge_text`・`badge_url`・`breadcrumb_root`・`repo_url`・`[[catalog.header_links]]`）、専用 CSS プリセット出力 `drawlib css list|show catalog`（`get_css(target="catalog")`・`export_css(target="catalog")`）、およびエージェント規約 `drawlib rules show project-catalog` を追加しました。

#### 2. 宣言的プロジェクト SEO・Open Graph・`llms.txt` 自動生成（`[seo]`, `[i18n.descriptions]`）
- **`site`・`doc`・`catalog`・`slide` 横断の検索・SNS メタデータ自動出力**: `drawlib.toml` に `[seo]`（`site_url`・`og_image`・`twitter_card`・`twitter_site`・`robots`・`sitemap`・`llms_txt`・`json_ld`・`cname`・`nojekyll`）および `[i18n.descriptions]` を宣言するだけで、`<link rel="canonical">`・多言語 `hreflang`・Open Graph / X Card タグ・Schema.org JSON-LD 構造化データ・`sitemap.xml`・`robots.txt`・`CNAME`・`.nojekyll` を一括出力します。
- **AI クローラ向け `llms.txt` 自動生成**: サイト構成・言語別エントリ URL・各ページ概要を整理した `llms.txt` を自動出力し、LLM エージェントや検索クローラによるドキュメント構造の正確な把握を支援します。

#### 3. ゼロインストール `uvx` フォールバックスクリプトと公式 API & CLI リファレンス公開（`/api/`, `/architecture/`）
- **他言語リポジトリでも即実行できる `uvx drawlib` 自動フォールバック**: 生成される `build*.sh` および `serve.sh` が `uv run drawlib` を優先検出しつつ、未設定環境では自動的に `uvx drawlib`（またはグローバル `drawlib`）へフォールバックするようになり、Go・Rust・TypeScript・Java 等の非 Python リポジトリでも環境構築なしで図解ビルドを実行できます。
- **日英バイリンガル公式 Python API & CLI リファレンス・アーキテクチャ仕様書の公開**: 新アーキタイプ `catalog` のドッグフーディングとして全 29 ページの公式 Python API & CLI リファレンス（`https://www.drawlib.com/api/`、日英完全対応）および内部ソフトウェアアーキテクチャ仕様書（`https://www.drawlib.com/architecture/`）を公開しました。

---

## バージョン 0.3.4

*リリース日: 2026/11/02*

バージョン 0.3.4 では、主要 9 種の AI コーディングアシスタントに対応した **AI エージェント向けワークスペースルール初期化機能（`drawlib init agent`）** を新搭載し、`drawlib init` を対称的な **`drawlib init project` / `drawlib init agent`** のサブコマンド階層へ再編成したほか、プロジェクトテンプレートに実行権限付きの **MS Word（`build_docx.sh`）** および **MS PowerPoint（`build_pptx.sh`）** ビルドスクリプトを追加しました。

---

### ハイライトと新機能

#### 1. AI エージェント向けワークスペースルール初期化（`drawlib init agent`, `drawlib.tools.init_agent_instruction`）
- **9 種の AI コーディングエージェントへのネイティブ対応**: `drawlib init agent <target...|all|list>` により、**Antigravity**（`.agents/rules/drawlib.md`）・**Claude Code**（`.claude/rules/drawlib.md`）・**Cursor**（`.cursor/rules/drawlib.mdc`）・**GitHub Copilot**（`.github/instructions/drawlib.instructions.md`）・**Windsurf**（`.windsurf/rules/drawlib.md`）・**Cline**（`.clinerules/drawlib.md`）・**Roo Code**（`.roo/rules/drawlib.md`）・**OpenAI Codex**（`AGENTS.md`）・**Gemini CLI**（`GEMINI.md`）向けの最適化済みルールファイルをワンコマンドで生成できます。
- **コンテキスト連動トリガーモードと既存ファイルへの安全なマージ**: `--mode auto|always`（標準は `.py`・`drawlib.toml`・`.md` 編集時に自動適用される `auto` モード、`< 10 KB` の軽量設計）や上書き保護（`--force`）に対応し、共有ルートファイル（`AGENTS.md` / `GEMINI.md`）では既存の記述を保持したまま `<!-- drawlib:begin -->` 〜 `<!-- drawlib:end -->` ブロックのみを冪等に更新します。
- **Python プログラム API（`drawlib.tools`）**: 自動化ツール連携向けに `init_agent_instruction()`・`list_agent_targets()`・`detect_agent_targets()`・`AgentTargetInfo` を追加しました。

#### 2. 対称的な `drawlib init` CLI 階層と実行可能な Office 出力スクリプト
- **`drawlib init project` と `drawlib init agent` の 2 階層構成**: プロジェクト雛形生成を `drawlib init project <doc|site|slide|images|list>`、AI エージェント設定生成を `drawlib init agent <agent...|all|list>` へと明確に整理しました。
- **実行権限付き `build_docx.sh` / `build_pptx.sh` テンプレートの追加**: `doc`（`drawlib init project doc`）および `slide`（`drawlib init project slide`）の初期生成ファイルに、実行可能権限（`chmod +x`）が付与された `build_docx.sh` および `build_pptx.sh` を追加しました。

#### 3. ドキュメント・README・アセットの拡充
- **GitHub / PyPI README とインストールガイドの刷新**: APNG / PNG ショーケース図版の刷新、インストール直後の AI エージェント設定ガイド（任意・強く推奨）の追加、および OGP / GitHub Social Preview バナー生成ターゲット（`docs/ogp_src/`）を追加しました。

---

### 破壊的変更と v0.3.3 からの移行ガイド

1. **プロジェクト初期化 CLI サブコマンドの `drawlib init project` 配下への移行**:
   - 従来の `drawlib init <doc|site|slide|images|list>` コマンドは、`drawlib init project <doc|site|slide|images|list>` 配下へ移動しました。
   ```bash
   # 従来 (v0.3.3 以前)
   drawlib init site -l en,ja
   drawlib init list

   # 新構文 (v0.3.4 以降)
   drawlib init project site -l en,ja
   drawlib init project list
   ```
   - なお、Python API の `drawlib.tools.init_project()` に変更はありません。

---

## バージョン 0.3.3

*リリース日: 2026/11/01*

バージョン 0.3.3 では、すべてのドキュメント（`doc`）・Web サイト（`site`）・プレゼンテーション（`slide`）プロジェクトに共通の **`drawlib.toml` プロジェクトマニフェスト** と **`i18n` ネイティブな `<src_dir>/<lang>/` 多言語ディレクトリ構成** を導入するとともに、**日英バイリンガル（`en`/`ja`）公式ドキュメント** および **パラメータツアーアニメーション** を全面拡充しました。

---

### ハイライトと新機能

#### 1. 統一プロジェクトマニフェスト（`drawlib.toml`）と多言語 `i18n` ネイティブ構成
- **宣言的マニフェスト `drawlib.toml`**: `doc`・`site`・`slide` の 3 アーキタイプすべてで `[project]` メタデータと `[i18n]` 言語設定（`default_lang`, `langs`, および任意の `[i18n.labels]`）を一元管理します（`images` プロジェクトでは `[project].lang` を使用）。`drawlib init <doc|site|slide> [-l en,ja]` または `drawlib.tools.init_project(..., lang="en,ja")` から単一言語・多言語プロジェクトを即座に生成できます。
- **統一 `<src_dir>/<lang>/` 構成とビルド前の構造パリティ検証**: すべての `doc`・`site`・`slide` プロジェクトで Markdown 原稿を `<src_dir>/<lang>/` 配下に配置し、必要に応じてロケール別の `<lang>/styles.py`・`<lang>/utils.py` オーバーライドも利用できます。ビルド時には全ロケール間で相対ファイルパス・見出し階層（`#`〜`######`）・````drawlib```` の `file=` ターゲット一覧が一致しているかを自動検証し、言語非依存の共通図版は 1 度だけレンダリングして `<output>/images/` で全言語から共有します。
- **多言語 16:9 スライドデッキ対応（`drawlib build slide`, `drawlib build pptx`, `drawlib build pdf`）**: インタラクティブ HTML スライドの下部コントロールバーに上方向展開の言語切り替えメニュー `.slide-lang-dropdown`（キーボードショートカット `L` 対応）を追加し、表示中の `#N` スライド番号を維持したまま言語を切り替えられるようになりました。ブラウザ言語に応じたルート `index.html` 自動リダイレクトと、言語別の PDF / PPTX 出力にも対応しています。
- **ロケール対応タイポグラフィ・`hreflang` SEO・出力ファイル名の統一**: `<html lang="..." dir="ltr|rtl">` 属性や `<link rel="alternate" hreflang="...">` タグの自動出力、CJK / RTL 向け CSS 組版最適化（`line-break: strict` や見出し字間の自動調整）、言語別フォントの自動構成（`FontJapanese`, `FontChinese`, `FontKorean`, `FontArabic` 等）、および単一言語・多言語を問わない `<stem>_<lang>.{pdf,docx,pptx}` 形式の統一ファイル名を採用しました。

#### 2. 日英バイリンガル公式ドキュメントとパラメータツアーアニメーション
- **公式ドキュメントサイト・Dogfooding ホワイトペーパーの日英完全対応**: 公式ドキュメントポータルおよび Dogfooding ホワイトペーパーの英語版（`en/`）・日本語版（`ja/`）を完全公開し、ページ内スイッチャーから即座に言語を切り替えられるようになりました。
- **パラメータツアーアニメーション（`drawlib.anim`）**: 基本図形・アイコン・SmartArts・定量チャート・各種ダイアグラム・自動レイアウトグラフ・ビルドワークフローにわたるロスレス APNG パラメータツアーアニメーションを追加しました。

#### 3. バグ修正と内部改善
- `drawlib._core` より先に `drawlib._release_assets` をインポートした際に発生していた `drawlib._release_assets` と `drawlib._core.l3_external` 間の循環インポートを解消しました。

---

### 破壊的変更と v0.3.2 からの移行ガイド

v0.3.2 以前で作成した既存の `doc`・`site`・`slide` ディレクトリプロジェクトをアップグレードする場合は、以下の手順で `i18n` ネイティブ構成へ移行してください。

1. **`[i18n]` を含む `drawlib.toml` の配置と `<src_dir>/<lang>/` への Markdown 移動**:
   - 従来のフラットディレクトリ構成（`doc_src/*.md`, `docs_src/*.md`, `slide_src/*.md`）および個別の `i18n.toml` / `i18nsite` 指定は、`drawlib.toml` + `<src_dir>/<lang>/` 構成へ統合されました（1 言語のみの `langs = ["en"]` や `langs = ["ja"]` でも共通です）。なお、単一 `.md` ファイル指定のビルド（`drawlib build html report.md`, `drawlib build pdf report.md` 等）は従来どおりそのまま動作します。
   ```toml
   [project]
   type = "site" # または "doc" / "slide"
   style = "default"

   [i18n]
   default_lang = "en"
   langs = ["en"] # または ["en", "ja"]
   ```
   - `*.md` ファイル（`site` の `navbar.md` を含む）を `<src_dir>/en/` 等へ移動し、共通の `styles.py`・`utils.py`・`_assets/`・`template.html`・`style.css`・`slide.js` は `<src_dir>/` 直下に維持してください。
2. **ロケールサフィックス付き出力パスへの統一（`<stem>_<lang>.{pdf,docx,pptx}` と `<output_dir>/<lang>/`）**:
   - `doc`・`site`・`slide` のディレクトリビルドでは、常に言語コード付きの成果物（例: `doc_en.pdf`, `doc_en.docx`, `slide_en.pdf`, `slide_en.pptx`）が出力され、HTML / Markdown ページは `<output_dir>/<lang>/` 配下（ルート `<output_dir>/index.html` は自動リダイレクトページ）に出力されます。

---

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
