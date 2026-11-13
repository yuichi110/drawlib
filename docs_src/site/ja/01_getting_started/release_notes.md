# リリースノートと移行ガイド

## バージョン 0.3.10

*リリース日: 2026/11/13*

バージョン 0.3.10 では、16:9 HTML スライドデッキ向けに **アニメーションのフレーム範囲ループ制御（`anim_pause=(0-3, 4-7)`）** を新搭載し、定常状態のデータフローやリクエスト／レスポンスのサイクルを特定フレーム範囲でループ再生させながら、クリック・`A` キー・発表者ビューの `⏭ Next Step` 操作で即座に次のフェーズへ進められるようにしたほか、**ドキュメントポータルへの Google Analytics 導入と日英ガイド・AI ルールの拡充** を実施しました。

---

### ハイライトと新機能

#### 1. スライドアニメーションのフレーム範囲ループ制御（`anim_pause=(0-3, 4-7)`, `slide`）
- **ハイフン記法によるループ範囲指定（`options.py`, `_assets.py`）**: スライド内の ```` ```drawlib ```` コードブロック属性 `anim_pause` において、従来の単一フレーム一時停止（`0`, `2`, `4`）に加え、0 始まりのハイフン範囲記法（`start-end`、`0 <= start < end`）をサポートしました。`anim_pause=(0, 1-4, 5-8)` のように単一停止フレームと範囲ループを自由に組み合わせて宣言できます。
- **Canvas ループ再生エンジンと即時ステップ進行（`slide.js`, `slide.css`）**: HTML スライドの `<canvas>` WebP / GIF フレームデコーダに専用の `LOOPING` 状態を追加しました。`start-end` の終端 `end` に到達すると自動的に `start` へ戻ってループ再生を継続し、キャンバスクリック・`A` キー・発表者ビュー（`?presenter=1`）の `⏭ Next Step` ボタン操作が行われた瞬間にループを抜け、終端まで待たずに即座に次フレーム `end + 1` へジャンプします（`→` / `Space` キーは常に次スライド移動として一貫動作します）。ループ再生中のアニメーションにマウスホバーすると `▶Click` バッジが表示され、進行操作が可能であることを視覚的に案内します。

#### 2. ドキュメントポータルの計測対応と日英ガイド・AI ルールの更新
- **ドキュメントテンプレート改善とガイド拡充（`docs_src/`, `_rules/`）**: 公式ドキュメントテンプレート（`site`・`api`・`architecture`）への Google Analytics（`gtag.js`）導入に加え、AI エージェント向けルール（`anim-guide`・`project-slide`）および日英ドキュメント（`08_animations/overview`・`09_doc_builder_and_cli/code_blocks`・`09_doc_builder_and_cli/project_slide`・アーキテクチャ仕様書）に範囲ループの設計パターンと状態遷移仕様を追記しました。

---

## バージョン 0.3.9

*リリース日: 2026/11/08*

バージョン 0.3.9 では、すべての曲線ラインおよびダイアグラムプリミティブに対する **割線（Secant）基準の曲線矢頭角度計算と de Casteljau ベジェ分割トリミング**、**`StateDiagram` 通常遷移でのオフセット辺アンカー（`top_right`・`top_left`・`bottom_right`・`bottom_left`）対応**、および **`drawlib show` 実行時の非致命的な矢頭埋もれ検出警告（`[Geometry Warning]`）** を追加したほか、AI エージェント向け幾何レビュー規約と日英ドキュメント図表の直交ルーティング品質を強化しました。

---

### ハイライトと新機能

#### 1. 割線基準の曲線矢頭レンダリング & `StateDiagram` オフセットアンカー対応（`l4_canvas`, `diagrams.state`）
- **割線角度アライメントと de Casteljau 先端分割（`_SecantCurveArrowStyle`）**: 曲線矢印（`line_curved`・`line_bezier1`・`line_bezier2`・`line_arc`・`lines_curved`・曲線を含む `lines_bezier`）において、後退させた先端 `P_tip` から曲線に沿って矢頭長分戻った `P_base` への割線ベクトルに矢の羽根を揃え、同時にベジェ曲線本体を de Casteljau アルゴリズムで正確に分割するよう改善しました。手動の角度調整オプションを追加したり矢頭サイズを縮小したりすることなく、急カーブや短い円弧でも曲線が左右の羽根の中央へ綺麗に収まります。
- **`StateDiagram` 通常遷移での双方向オフセットアンカー（`_state_node.py`, `_render_transition.py`）**: `StateDiagram.connect(...)` の通常遷移でも `"top_right"`・`"top_left"`・`"bottom_right"`・`"bottom_left"` の境界オフセット（副軸方向 `±0.35`）を解決するようになり、コンパクトな状態ノード間の双方向遷移アーク（`A <-> B`）を重なりなく分離できます。

#### 2. 矢頭クリアランスの非致命的ジオメトリ警告（`drawlib show`）
- **末端セグメント長チェッカー（`LineUtils.check_arrowhead_segment_warnings`）**: Drawlib の `720pt` 基準キャンバス幅に基づき描画済み `FancyArrowPatch` の物理矢頭サイズを判定し、直交折れ線の最終セグメント（または線・曲線の全長）が矢頭サイズを下回る場合に、`drawlib show` 実行時の `stderr` へ非致命的な `[Geometry Warning]` を出力します（`line_arrow_head_scale` の自動縮小やビルドエラー化は行わず、宣言的スタイルの統一性を維持します）。

#### 3. AI エージェント向け幾何レビュー規約と日英ドキュメント図表の品質改善
- **Stage 2 直交クリアランス規約の整備（`_rules/`）**: `review-guide`・`lib-lines`・`lib-graph-layer`・`lib-graph-tree`・`lib-diagrams-state` および `drawlib init agent` テンプレートに、`[Geometry Warning]` の確認手順と直交 Z ルーティング時の最小ノード間隔目安（`>= 6.0` 単位）を追記しました。
- **日英ドキュメント図表の一斉ブラッシュアップ（`docs_src/`）**: `site`・`api`・`architecture`・`readme` 全プロジェクトの直交分岐位置やランク／レベル間隔を最適化し、リポジトリ全体でジオメトリ警告ゼロを達成しました。

---

## バージョン 0.3.8

*リリース日: 2026/11/07*

バージョン 0.3.8 では、`drawlib build` の全 7 サブコマンドおよびプログラマティック `build_*` API に **マルチコア並列レンダリング（`-w` / `--workers`、`DRAWLIB_BUILD_WORKERS`）** を新搭載し、ウォームキャッシュ時の瞬時ビルドを維持したままマルチコア環境でのコールドビルドを **約 3〜6 倍高速化** したほか、**外部アセット取得のプロセス間排他ロック & Zip Slip 対策付きアトミック展開**、および **Python 3.14 公式サポート（`Python 3.11–3.14`）** を追加しました。

---

### ハイライトと新機能

#### 1. 全 7 種の `drawlib build` ターゲットにおけるマルチコア並列レンダリング（`-w` / `--workers`, `DRAWLIB_BUILD_WORKERS`）
- **2 フェーズ・マルチプロセス事前レンダリングエンジン（`_builder._common.parallel`）**: 未キャッシュの埋め込み ```` ```drawlib ```` コードブロックおよび単体 `.py` スクリプトを、`spawn` 方式の `ProcessPoolExecutor` ワーカー群で並列描画します（`html`・`markdown`・`pdf`・`docx`・`slide`・`pptx`・`image` すべてに対応）。多言語間の共有図解を事前重複排除したうえで `Animation` 等の重いジョブから優先投入する **Longest-Job-First** スケジューリングを採用し、非デーモンワーカーにより `get_dimage_from_code()` のネスト子プロセス実行にも完全対応しています。
- **スマートな `"auto"` ワーカー数解決とウォームキャッシュ時オーバーヘッドゼロ**: デフォルトの `-w auto` / `workers="auto"` は **`1 <= (CPUコア数 - 1) <= 8`** へ自動解決され、`-w <N>`・`workers=<N>`・環境変数 `DRAWLIB_BUILD_WORKERS=<N>` で明示制御できます（`-w 1` で同一プロセス内の逐次実行）。キャッシュミスが 1 件以下のウォームビルド時はプロセスプール起動を完全にスキップし、`.drawlib/cache.db`（SQLite WAL）への書き込みは親プロセスへ一本化されます（`--no-cache` 指定の `pdf` / `docx` インラインビルド時も `BuildImageCache.prerendered_blobs` により親プロセスの二重描画を防止）。

#### 2. 外部アセットのプロセス間ロックと Zip Slip 防止アトミック展開（`l3_external`）
- **パッケージ単位のプロセス間アドバイザリロック（`_download.py`）**: POSIX の `fcntl.flock` と Windows の `msvcrt.locking` によるプロセス間ファイルロック（読み取り専用コンテナ環境向けの XDG / `LOCALAPPDATA` / 一時ディレクトリへのフォールバック付き）とロック取得後のチェックサム再確認を導入し、並列ビルドワーカー間での初回フォント・アイコン・地図アーカイブ取得の競合を完全に排除しました。
- **Zip Slip 境界検証とアトミック置換（`_package.py`）**: `ReleaseAssetPackage.download_and_extract()` に `Path.is_relative_to()` によるパストラバーサル検証と `.tmp_<pid>_<tid>_*` + `os.replace()` アトミック書き込みを導入し、並列読み込み中の中途半端なファイル参照を防止しました。

#### 3. Python 3.14 公式ランタイムサポート（`Python 3.11–3.14`）
- **クロスプラットフォーム Python 3.14 互換性の検証と対応**: `pyproject.toml` の PyPI 分類子・GitHub Actions（Linux / Windows / macOS）テストマトリクス・`./dcli docker` クリーンルーム検証を Python `3.11`〜`3.14` へ拡張し、Python 3.14 で廃止された旧 AST ノード参照の `ast.Constant` 統一および `drawlib.utils` リセット時の `__spec__` 保持（`importlib.reload()` 互換性）を実施しました。

---

## バージョン 0.3.7

*リリース日: 2026/11/07*

バージョン 0.3.7 では、SNS・プレゼン資料・社内 Wiki 等あらゆる環境で再生できる **ディザノイズのないアニメーション／静止画 GIF 出力（`.gif`）** を `Animation`・`canvas.save()`・Markdown コードブロック・CLI バッチビルドへ新搭載したほか、Windows / POSIX 横断での **Headless Chromium 並列セットアップ排他ロック強化**、多言語 **`navbar.md` のロケール別外部 URL 対応**、および **マルチポータル SEO / `llms.txt` 導線と README の整備** を実施しました。

---

### ハイライトと新機能

#### 1. ディザノイズのないアニメーション & 静止画 GIF 出力（`Animation`, `save("*.gif")`, `drawlib build image -f gif`）
- **図解・テキストに最適化された 256 色パレット量子化（`l3_images._gif`）**: ディザリングを無効化した Median Cut 減色（`Image.Quantize.MEDIANCUT` + `Image.Dither.NONE`）による `.gif` 出力（`ImageFormat` に `"gif"`・`"apng"`・`"svg"` を追加）に対応し、`Styles.Neutral` 等のフラットなカード塗りに粒状ノイズを発生させず鮮明な文字エッジを維持します。
- **アニメーション・Markdown フェンス・CLI の一貫対応**: `save("flow.gif")` や `save("flow", format="gif")` によるマルチフレーム GIF 書き出し（`10ms` 単位の GIF 仕様フレーム間隔丸め、および透過背景時のパレット `255` 番予約＋`disposal=2` による残像防止）、Markdown ```` ```drawlib ```` ブロックでの `file=demo.gif` / `format=gif` 指定（`.docx` / `.pptx` 変換時は静止 PNG フレームを自動抽出）、および `drawlib build image -f gif` での一括変換をサポートします。

#### 2. クロスプラットフォーム並列ブラウザロックと多言語ナビゲーション改善
- **Headless Chromium のプロセス間排他ロックとセンチネル検証（`browser.py`）**: POSIX の `fcntl.flock` に加えて Windows の `msvcrt.locking` によるプロセス間ファイルロックに対応し、ロック取得後に `INSTALLATION_COMPLETE` センチネルを確認することで、`pytest-xdist` 等の並列ワーカーや同時 PDF / PPTX ビルドにおける初回 `chromium-headless-shell` 取得の競合と重複起動を防止しました。
- **多言語 `navbar.md` でのロケール別外部リンク対応（`i18n.py`）**: 多言語 `site` プロジェクトの構造パリティ検証において、外部 URL 内の `/{lang}/` パス切り替え（例：`en/navbar.md` で `/api/en/`、`ja/navbar.md` で `/api/ja/` を指定）を正規化して許容するようになりました。

#### 3. CLI・テンプレート・SEO 発見性・ドキュメントの整備
- **Catalog 雛形メッセージ・CLI ヘルプ・型処理の整理**: `drawlib init project` のヘルプ表記および `catalog` テンプレートのビルドスクリプト出力（`Catalog HTML`）を統一し、`l3_math`・`l4_canvas` のベジェ／座標タプル判定を改善しました。
- **マルチポータル `sitemap.xml` / `llms.txt` 導線と README 刷新**: `www.drawlib.com` ルートの `robots.txt` および `llms.txt` から `/api/`・`/architecture/` への導線を追加し、GitHub / PyPI README の全 10 種チャート（`BoxChart` 含む）・15 種テックブランドアイコンスイート表記および `uvx` クイックスタート案内を更新しました。

---

## バージョン 0.3.6

*リリース日: 2026/11/06*

バージョン 0.3.6 では、箱ひげ図・ストリップ／ジッタープロット・ベンチマーク向けハイブリッド重ね描きを 1 クラスに統合した統計分布チャート **`BoxChart` および `BoxStats`（`drawlib.charts.box`）** を新搭載したほか、PNI501 ソフトウェア監査に基づく **サプライチェーンセキュリティ強化・非 root コンテナ実行・オフライン動作信頼性の改善** を実施しました。

---

### ハイライトと新機能

#### 1. 箱ひげ図・ストリッププロット・ハイブリッド重ね描き（`drawlib.charts.box`, `BoxChart`, `BoxStats`）
- **1 クラス 3 モードの分布可視化ビルダ（`show_box`, `show_points`, `show_outliers`, `show_mean`）**: カテゴリ別の数値分布を **箱ひげ図**（`show_box=True, show_points=False`）、**1D／ジッター付きストリッププロット**（`show_box=False, show_points=True`）、および **$N = 5 \sim 30$ のベンチマーク評価に最適な箱ひげ＋実測点ハイブリッド重ね描き**（`show_box=True, show_points=True`）として宣言的に描画できます（`BoxChart` 全体のデフォルト指定および `add_series(...)` 単位での個別上書きに対応）。
- **生データ配列と事前集計 `BoxStats` のハイブリッド入力（`whisker_mode="iqr" | "min_max" | "percentile"`）**: 生データ配列（`Sequence[float]`）からの Pure Python 四分位・外れ値自動算出（`iqr_k=1.5` の Tukey 方式、最小最大 `min_max`、テールレイテンシ向け `whisker_percentiles=(5.0, 95.0)`）に加え、BigQuery や Cloud Monitoring から取得した集計値 `BoxStats(min=..., q1=..., median=..., q3=..., max=..., mean=..., outliers=...)` の直接描画をサポートします。
- **決定論的ジッターと単一 `Style` からの高コントラスト自動導出**: `(jitter_seed, series_idx, category_idx)` ごとに独立した 32bit 整数ミキシングで乱数を分離することで Git 差分やアニメーション時の点シャッフルを完全に防止し、単一 `Style`（`Styles.PrimaryNeutral`・`Styles.PrimaryFlat` 等）からの箱・ひげ・中央値・マーカー色の自動導出、縦向き／横向き配置、`scale="log"` 対数軸、`draw_ratio` 部分描画、および `drawlib rules show lib-charts-box` に対応しました。

#### 2. サプライチェーンセキュリティ強化・非 root コンテナ・オフライン動作改善
- **依存関係更新と非 root コンテナ化**: `pillow>=13.0.0` への引き上げによる脆弱性解消と、本番・検証用すべての Dockerfile における非 root ユーザー（`USER drawlib`, `UID 10001`）実行への強化を実施しました。
- **エアギャップ環境での事前検証と監査レポート公開（[`/reports/pni-full-audit/`](https://www.drawlib.com/reports/pni-full-audit/)）**: オフライン環境（`--network=none`）におけるネットワーク取得前の `pkg.files` メンバーシップ検証、SQLite ビルドキャッシュ接続の改善、および [PNI501 ソフトウェア品質・セキュリティ監査レポート](https://www.drawlib.com/reports/pni-full-audit/)の公開を行いました。

---

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
- **`site`・`doc`・`catalog`・`slide` 横断の検索・SNS メタデータ自動出力**: `drawlib.toml` に `[seo]`（`site_url`・`og_image`・`twitter_card`・`twitter_site`・`sitemap`・`robots`・`llms_txt`）および `[i18n.descriptions]` を宣言するだけで、`<meta name="description">`・`<link rel="canonical">`・多言語 `hreflang` / `og:locale`・Open Graph / X Card タグ・`sitemap.xml`・`robots.txt`・`llms.txt` を一括出力します（`www.drawlib.com` デプロイ用の `.nojekyll`・`CNAME` と連携）。
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
