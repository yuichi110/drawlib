# PNI `pni.toml` オプトアウト機構・`Pillow 13` 更新・公開レポート連携計画書

- **作成日**: 2026-11-05
- **前提計画書**: `.agents/plans/PNI501_AUDIT_INTEGRATION_PLAN.md`（Phase P1〜P2 / D1〜D2 完了済み）
- **対象リポジトリ**:
  1. **`pni501` 側** (`yuichi110/pni501`): `.pni/pni.toml` マニフェスト・理由付きオプトアウト（Waiver）・`.gitignore` 連動スキャン・Web 公開向け HTML 出力パス制御の実装
  2. **`drawlib` 側** (`yuichi110/drawlib`): `pillow>=13.0.0` へのアップデート（41 CVE 一括解消）、オフライン `--network=none` / Docker 非 root 改善、`.pni/pni.toml` 導入によるクリーン再監査、および `docs/reports/` への HTML/PDF 公開ビルド統合
  3. **`drawlib-examples` 側** (`yuichi110/drawlib-examples` / `examples.drawlib.com`): 単なる `doc` 作例ではなく **「Drawlib を組込みドキュメント／レポートエンジンとして使うカテゴリ（Powered by Drawlib）」** の新設と導線接続

---

## 1. 全体ロードマップ（推奨実行順序）

| ステップ | 作業対象リポジトリ | フェーズ名 | 主な内容 | 依存関係 |
| :---: | :---: | :--- | :--- | :--- |
| **Step 1** | **`drawlib`** | **Phase D3: `pillow>=13.0.0` 更新 & 主要指摘の先行修正** | ・`pyproject.toml` の `pillow>=13.0.0` 更新と `uv lock --upgrade-package pillow`、全ゴールデン画像テスト検証（41 CVE → **0 CVE**）<br>・オフライン `--network=none` での `_download.py` / `_release_assets.py` `pkg.files` 事前照合（12 失敗解消）<br>・`tools/docker/Dockerfile.*` の非 root `USER` 対応（Trivy `DS-0002` 解消） | **単独で即時着手可** |
| **Step 2** | **`pni501`** | **Phase P3: `.pni/pni.toml` 導入 & 理由付きオプトアウト実装** | ・`.pni/pni.toml` ローダー & `pni init` スキャフォールド追加<br>・`[scan]` による `.gitignore` 連動 / `skip_files`（ローカル `.env` 混入防止）<br>・`[[opt_out]]`（`reason` 必須 Waiver）による決定論チェッカー / Trivy / スコア集計への反映とレポート透明化<br>・`[report]` デフォルト連携・直接 `html_output_dir` 指定・A4 印刷テーブル CSS 改善 | Step 1 と並行可 |
| **Step 3** | **`drawlib`** | **Phase D4: `pni.toml` 適用・再監査 & `docs/reports/` 公開統合** | ・Git から最新 `pni501` を更新（`uv lock --upgrade-package pni501`）<br>・`.pni/pni.toml` で意図的設計（`CWE-94` `exec()`、`DS-0026`、`uv.lock` gitignore 等）を理由付き宣言<br>・クリーン状態で `full_audit` 再実行 → `docs/reports/pni-full-audit/` へ HTML（`code=fold`）+ PDF をビルド・`./dcli docs` 連携 | Step 1 & Step 2 完了後 |
| **Step 4** | **`drawlib-examples`** | **Phase E1: `examples.drawlib.com` エンジン活用カテゴリ公開** | ・`examples.drawlib.com` に「組込みドキュメントエンジン活用事例（Powered by Drawlib）」カテゴリを追加し、`https://www.drawlib.com/reports/pni-full-audit/`（HTML / PDF）へリンク | Step 3 完了後 |

---

## 2. Part 1: `pni501` リポジトリ側の改善計画（`pni501` 共有用）

> **背景（`drawlib` フル監査 & Web 一般公開検討で判明した要件）**:
> 1. ワークフロー YAML（`full_audit.yaml`, `quick_check.yaml`）ごとに `targets`, `exclude`, `src_dir`, `output_dir` を重複記述しており、`pni report init/build` 単体実行時にも毎回 CLI 引数指定が必要になっている。
> 2. `security_scan`（`trivy fs`）がワークツリーをそのままマウントするため、`.gitignore` 済みの開発者ローカル `.env`（マスク済みトークン有無）まで `SecurityFacts` に記録され、レポートをそのまま Web 公開する際のノイズ・運用情報露出リスクになる。
> 3. 対象プロジェクトのアーキテクチャ上「仕様通り（By Design）」である項目（例: Drawlib の `CWE-94` `exec()`、バッチ CLI コンテナの `DS-0026` `HEALTHCHECK` 不要、複数 Python バージョン対応ライブラリの `uv.lock` gitignore、PEP 562 Facade の `_` サブパッケージ import）を、**「黙って隠蔽」するのではなく「理由付きで宣言的にオプトアウト（Waiver）」** できる仕組みが求められる。
> 4. GitHub Pages（`docs/reports/<slug>/`）へ直接 HTML 公開する際、現行 `compiler.py` は出力先を `<output_dir>/<target>_html/` に固定付与するため、URL に `_html` が入らない出力先制御（`html_output_dir`）が欲しい。

### 2.1. `.pni/pni.toml` マニフェスト仕様の定義とローダー実装

- **新規・変更対象ファイル**:
  - `src/pni/_config.py`（新規: `PniConfig` Pydantic モデル、`load_pni_config(workspace_root)`、デフォルト `pni.toml` テンプレート生成）
  - `src/pni/cli.py`（`pni init` 実行時に `.pni/pni.toml` が未存在ならコメント付き初期ファイルを生成、`--force` で再生成可能に）
- **TOML スキーマ仕様（Python 3.11+ 標準 `tomllib` で読み込み）**:

```toml
[project]
name = "drawlib"
archetypes = ["library", "cli"] # 任意: 自動判定の上書き・補強

[targets]
root = "."
source = ["src/drawlib"]
tests = ["tests/drawlib"]
docs = ["README.md", "docs_src"]
exclude = ["**/*_generated.py", "reports/**", "docs/**"]

[scan]
# true の場合、.gitignore で無視されている未追跡ファイルを secret / fs スキャン対象から除外
respect_gitignore = true
# respect_gitignore = true でも脆弱性スキャン等に含めたいローカルファイルを明示許可
include_gitignored = ["uv.lock"]
# 追加で強制スキップするファイル・ディレクトリパターン（Trivy --skip-files / --skip-dirs 等へ伝播）
skip_files = [".env", ".env.*", "**/.env"]
skip_dirs = ["reports", "docs", "output_tests"]

[report]
src_dir = "reports"
output_dir = "reports"
# 任意: Web 公開ディレクトリ（例: GitHub Pages の docs/reports/pni-full-audit）へ HTML を直接出す場合
html_output_dir = "docs/reports/pni-full-audit"
formats = ["pdf", "html"]
lang = "en"
style = "google"

# 理由付きの明示的オプトアウト（Waiver）定義 — reason を必須バリデーションとする
[[opt_out]]
id = "CWE-94"
scope = [
    "src/drawlib/_builder/**",
    "src/drawlib/_core/l4_canvas/_image_code.py",
]
reason = "Drawlib executes user-authored Python diagram blocks by design ('Illustration as Code')."

[[opt_out]]
id = "DS-0026"
scope = ["tools/docker/Dockerfile.*"]
reason = "Batch CLI and test containers exit upon command completion; daemon HEALTHCHECK is N/A."

[[opt_out]]
id = "python/lockfile_committed"
reason = "Pure-Python library supporting Python 3.11-3.13 intentionally gitignores uv.lock."

[[opt_out]]
id = "ast/private_submodule_import"
scope = ["src/drawlib/**"]
reason = "Public PEP 562 facades (drawlib/*.py) intentionally re-export internal _* subpackages."

[[opt_out]]
id = "ast/excessive_parameters"
scope = ["src/drawlib/_charts/**", "src/drawlib/_smartarts/**", "src/drawlib/shapes.py"]
reason = "Declarative styling and layout APIs expose keyword-only (*) configuration parameters by design."
```

- **設定優先順位（Precedence）**:
  - `CLI 明示オプション / ワークフロー step の with:` **＞** `ワークフロー YAML トップレベル (targets / outputs)` **＞** `.pni/pni.toml` **＞** `組込みデフォルト定数`。
  - ワークフロー YAML で `targets` を省略した場合、自動的に `.pni/pni.toml` の `[targets]` が継承される。

---

### 2.2. `[scan]` スコープ制御と `.gitignore` 連動（ローカル `.env` 露出の根絶）

- **変更対象ファイル**:
  - `src/pni/_actions/security_scan/trivy_runner.py`
  - `src/pni/_actions/security_scan/runner.py`
  - `src/pni/_actions/security_scan/models.py`
  - `src/pni/_actions/project_inspect.py`
- **改修仕様**:
  1. **`.gitignore` 対象ファイルの安全な除外**:
     - `scan.respect_gitignore = true`（デフォルト `true` 推奨）のとき、`git status --ignored --porcelain -z`（Git 管理下の場合）または `.gitignore` パターンから未追跡の無視ファイル一覧を取得し、`include_gitignored`（例: `["uv.lock"]`）を除いて Trivy の `--skip-files` / `--skip-dirs` に渡す（またはスキャン対象ステージングから除外する）。
     - これにより、開発者手元の `.env` や一時検証ファイルが `SecurityFacts.secrets` に混入することを構造的に防ぐ。
  2. **`scan.skip_files` / `scan.skip_dirs` の伝播**:
     - `trivy fs` 実行時に既存の `_SKIP_FS_DIRS` に加えて `pni.toml` の `skip_dirs` と `--skip-files`（`skip_files`）を渡す。

---

### 2.3. `[[opt_out]]`（理由付き Waiver）の決定論フィルタリングと透明性記録

- **変更対象ファイル**:
  - `src/pni/_config.py`（`OptOutEntry` モデル & マッチングヘルパー `match_opt_out(check_id, file_path)`）
  - `src/pni/_actions/base_model.py`（`AppliedOptOut` モデル追加、`ScoreResult` に `opt_outs: list[AppliedOptOut] = []` 追加）
  - `src/pni/_actions/security_scan/parsers.py`（Trivy Misconfig ID 例: `DS-0026`、CVE/Advisory ID、Secret rule ID の `scope` glob 照合フィルタ）
  - `src/pni/_actions/ast_analyze/runner.py`（`CWE-*` シンク、`ast/private_submodule_import`、`ast/excessive_parameters` 等の `scope` glob 照合フィルタ）
  - `src/pni/_actions/project_inspect.py` / `_repo_governance.py`（`python/lockfile_committed` 等のガバナンス項目フィルタ）
  - `src/pni/_workflows/engine.py` & `aggregator.py`
  - `src/pni/_reporter/blueprint.py`
- **改修仕様**:
  1. **バリデーション（黙殺防止）**:
     - `[[opt_out]]` の `id` と `reason`（空白除く 10 文字以上推奨）を必須とし、`reason` 空文字はバリデーションエラーにする。
     - `scope: list[str]` が指定されている場合は `fnmatch` / `PurePosixPath.match` で対象ファイルパスと照合し、省略時はリポジトリ全体に適用する。
  2. **多段フィルタリング**:
     - **決定論フェーズ（`project_inspect`, `ast_analyze`, `security_scan`）**: `opt_out` にマッチした検出項目は通常の違反リストから外し、代わりに「オプトアウト適用件数（`matched_count`）」を記録する。また `ai_interpret` プロンプトにも有効な `[[opt_out]]` 一覧（ID・対象スコープ・設計理由）を渡し、AI ステップがオプトアウト済み事項を違反（`WARN`/`FAIL` や減点・ActionPlan）として再計上しないようにする。
     - **集約フェーズ（`aggregator.py` / `emit_score`）**: 万一 `Finding` に `opt_out.id`（`rule_id` またはタグ一致）が含まれていた場合も決定論的に除外し、`ScoreResult.opt_outs` に `{ id, scope, reason, matched_count }` を保存する。ルール単位丸ごとのオプトアウト（例: `common/api_security`）は `RuleComplianceStatus = "not_applicable"` として扱う。
  3. **レポート Blueprint での透明性表示（Chapter 4）**:
     - `ScoreResult.opt_outs` が 1 件以上ある場合、`blueprint.py` の Chapter 4（Audit Standards, Rule Compliance & Findings）に「**Configured Scope & Accepted Design Waivers (`pni.toml`)**」サブセクションを自動出力し、何をどの設計理由でオプトアウトしているかを明示する（Chapter 3 の改善ロードマップからは除外）。

---

### 2.4. `[report]` 連携・`html_output_dir` 対応・印刷テーブル CSS 改善

- **変更対象ファイル**:
  - `src/pni/_reporter/compiler.py`, `src/pni/_reporter/base_model.py`, `src/pni/cli.py`
  - `src/pni/_actions/common/write_drawlib_report.yaml`
- **改修仕様**:
  1. **`pni report init` / `pni report build` の `pni.toml` デフォルト参照**:
     - `--src-dir`, `-o/--output-dir`, `-f/--formats`, `-l/--lang`, `-s/--style` が CLI で未指定のとき、`.pni/pni.toml` の `[report]` セクションの値をデフォルトとして使用する。
  2. **`html_output_dir` オプションの追加**:
     - `compile_report_project(..., html_output_dir: Path | None = None)`（CLI: `--html-output-dir`、`pni.toml`: `report.html_output_dir`、`write_drawlib_report` step `with: html_output_dir`）を追加する。
     - 指定時は `<output_dir>/<target>_html` ではなく、指定ディレクトリ直下（例: `docs/reports/pni-full-audit/index.html`）へ HTML 一式を出力し、`scan_broken_links` を実行する。
  3. **`pni report init` 時の印刷用ワイド表 CSS 補強**:
     - 長いファイルパス（`<code>src/...</code>`）を含む監査表を A4 PDF 出力した際に右端見切れも狭い列の 1 文字折り返し（`F/A/I/L`）も起きないよう、スキャフォールド時の `style.css` の `@media print` に以下を標準適用する：
       - `th, th code { overflow-wrap: normal; word-break: normal; }`
       - `td { overflow-wrap: break-word; word-break: normal; }`
       - `td code { white-space: normal; overflow-wrap: anywhere; word-break: normal; }`

---

## 3. Part 2: `drawlib` リポジトリ側の実装計画

### 3.1. Phase D3: `pillow>=13.0.0` アップデート & 高優先度指摘の解消

#### 1. `pillow>=13.0.0` へのアップデート（ユーザー明示要望・最優先 P0）
- **対象ファイル**:
  - `pyproject.toml`
  - `uv.lock`（ローカル環境ロック更新）
  - `tests/drawlib/**/test_*_answers/*.png`（デコーダ／フォントラスタライザ差異が生じた場合のみ差分確認の上で更新）
- **背景**:
  - 前回の Trivy スキャンで検出された全 41 件のアプリケーション CVE（Critical 5 / High 23 / Medium 13）は **100% が `pillow@12.3.0` 単一パッケージに起因**しており、PyPI リリース済みの **`pillow 13.0.0`** で全 41 件が一括修正される（残り 12 個の直接依存パッケージおよび OS レイヤーの CVE は 0 件）。
- **実施手順**:
  1. `pyproject.toml` の `[project].dependencies` にある `"pillow>=10.2"` を **`"pillow>=13.0.0"`** に更新する（あわせて `types-pillow` の最新版互換性も確認する）。
  2. `uv lock --upgrade-package pillow` および `uv sync` を実行し、Python 3.11 / 3.12 / 3.13 の依存解決と `matplotlib`・`python-docx`・`python-pptx` とのバージョン競合がないことを確認する。
  3. `./dcli code-check all` および `./dcli test all` を実行し、`tests/conftest.py` のピクセル比較フック（`check_image_match`）が全件パスするか検証する。
     - 万一 `pillow 13.0.0` の内部 `libjpeg` / `libtiff` / `libfreetype` 更新に伴う微細なアンチエイリアス差分で一部ゴールデン PNG が不一致となった場合は、`view_file` で視覚的に劣化がないことを 1 件ずつ確認した上でベースライン画像を更新する。

#### 2. オフライン `--network=none` 実行時の不要な外部通信バグ修正（P1）
- **対象ファイル**:
  - `src/drawlib/_release_assets.py`（`find_package_for_icon_path`, `find_package_for_resource_path`）
  - `src/drawlib/_core/l3_external/_download.py`（`download_if_not_exist`）
  - `tests/drawlib/core/test_external_download.py`（または対応する単体テスト）
- **背景**:
  - 存在しないアイコン名（例: `icons/ai/nonexistent_icon.png`）を指定したエラー系テスト 12 件が、`pkg.files` を確認せずに `pkg.download_and_extract()` を呼んでいたため、オフライン環境（`--network=none`）で DNS エラー失敗していた。
- **改修仕様**:
  - パッケージ特定後、要求された相対アセットパスが `pkg.files` マニフェスト内に存在しない場合はネットワーク通信を一切行わず即座にエラーを送出する。また `pkg.is_downloaded()` が真の場合も再ダウンロードを行わない。
  - あわせて `.pni/dockerfiles/root/Dockerfile` に `uv run drawlib cache download --all` と `playwright install --with-deps --only-shell chromium` を組み込み、完全オフライン（`--network=none`）での単体テスト通過率 **100%** を達成する。

#### 3. Docker コンテナの非 root `USER` 化（P1）
- **対象ファイル**:
  - `tools/docker/Dockerfile.prod`
  - `tools/docker/Dockerfile.test_local`
  - `tools/docker/Dockerfile.test_pypi`
- **改修仕様**:
  - `PLAYWRIGHT_BROWSERS_PATH=/opt/ms-playwright` および共有アセットキャッシュパス（または非 root ユーザーのホーム配下）を適切に構成した上で、専用非特権ユーザー `drawlib`（`UID 10001`）を作成し、`WORKDIR /workspace` / `CMD` 前に `USER drawlib` へ切り替える（Trivy `DS-0002` High 3 件をすべて解消）。

---

### 3.2. Phase D4: `.pni/pni.toml` 導入・再監査 & `docs/reports/` HTML 公開統合

#### 1. `.pni/pni.toml` の作成とワークフロー YAML のスリム化
- **対象ファイル**:
  - `.pni/pni.toml`（新規）
  - `.pni/workflows/full_audit.yaml`, `.pni/workflows/quick_check.yaml`
- **実施内容**:
  - `uv lock --upgrade-package pni501 && uv sync` で Part 1 対応済みの `pni501` を取り込む。
  - `.pni/pni.toml` を配置し、`respect_gitignore = true`・`skip_files = [".env", ".env.*"]` と、Drawlib の設計仕様に基づく `[[opt_out]]`（`CWE-94`, `DS-0026`, `python/lockfile_committed`, `ast/private_submodule_import` 等）を理由付きで宣言する。

#### 2. `docs/reports/pni-full-audit/` への HTML & PDF 公開構成と `./dcli` 統合
- **公開ディレクトリ設計**:
  - **ソースプロジェクト（Single Source of Truth）**: `reports/full_audit_src/`
    - `reports/full_audit_src/drawlib.toml` の `[seo]` を有効化する：
      ```toml
      [seo]
      site_url = "https://www.drawlib.com/reports/pni-full-audit"
      og_image = "_assets/ogp.png"
      twitter_card = "summary_large_image"
      sitemap = false
      robots = false
      llms_txt = false
      ```
      *(※ `robots = false` / `sitemap = false` にすることで、`www.drawlib.com` 本家マニュアルや API リファレンスの検索インデックスと競合させずにクリーンにホストできる。)*
  - **公開ビルド成果物（GitHub Pages `www.drawlib.com` 配下）**:
    - HTML 一式: `docs/reports/pni-full-audit/`（`index.html`, `en/index.html`, `images/*.png`, `_assets/`）
      - 全 14 図が `code=fold` のため、Web 上で各診断チャートの `▶ Source Code` を展開して Drawlib Python コードを閲覧可能。
    - PDF 版: `docs/reports/pni-full-audit/full_audit.pdf`（Web ページ上部または `examples.drawlib.com` のショーケースカードから直接開けるよう同階層に配置し、リポジトリ内の PDF 重複保持を避ける）。
    - スコア JSON: `reports/full_audit_score.json`
- **`./dcli docs` へのターゲット追加**:
  - `tools/dcli/docs/builder.py` および `tools/dcli/docs/cli.py` に任意ビルドターゲット `reports`（`clean_paths = ("docs/reports/pni-full-audit",)`、`SERVE_TARGET_MAP["reports"] = "docs/reports/pni-full-audit"`）を追加する。
  - 既存の `site` ターゲットの `clean_paths` は `docs/en`, `docs/ja`, `docs/images` 等の個別リスト指定であるため、`docs/reports/` と一切干渉しない（なお、`./dcli docs build --all` に含めるか、`./dcli docs build reports` の明示実行のみにするかはビルド時間に応じて選択可能とするが、キャッシュ有効時は数秒で完了するため統合も容易）。
  - `.agents/rules/docs.md` および `.agents/rules/dcli.md` のターゲット一覧表にも `reports` を追記する。

---

## 4. Part 3: `examples.drawlib.com`（`drawlib-examples`）側の連携計画

### 4.1. 新カテゴリ「組込みドキュメントエンジン活用事例（Powered by Drawlib）」の新設
- **位置づけの明確化**:
  - 既存の `doc` / `site` / `catalog` / `slide` カテゴリは「人間や AI エージェントが直接ドキュメント・スライドを執筆する作例」であるのに対し、本レポートは **「外部の診断・監査ツール（`pni501`）が、自前で HTML/CSS/Chart 描画や PDF 組版エンジンを実装する代わりに、Drawlib をバックエンドのレポート出力エンジンとして組み込む事例」** として独立カテゴリで展示する。
- **カテゴリ名称案**:
  - 英語: **`Powered by Drawlib — Embedded Reporting Engine`**
  - 日本語: **`組込みドキュメントエンジン活用事例（Powered by Drawlib）`**
- **ショーケースカードの構成要素**:
  - **タイトル**: `PNI501 Software Health & Security Audit Report (Target: Drawlib)`
  - **リンク導線**:
    1. **Interactive HTML Report**: `https://www.drawlib.com/reports/pni-full-audit/`（`▶ Source Code` で自動生成された 14 点のチャート・図解コードを閲覧可能）
    2. **Print-Ready A4 PDF**: `https://www.drawlib.com/reports/pni-full-audit/full_audit.pdf`
    3. **Generator Tool**: `https://github.com/yuichi110/pni501` / **Report Source**: `https://github.com/yuichi110/drawlib/tree/main/reports/full_audit_src`
  - **技術ハイライト説明**:
    - 構造化診断データ（`full_audit_score.json`）と Blueprint から Drawlib `doc` プロジェクトを自動構成し、単一ソースからインタラクティブ HTML と 40+ ページの印刷用ベクター A4 PDF を同時コンパイルしている点を紹介する。

---

## 5. 完了検証チェックリスト（Verification Gate）

1. **`drawlib` 品質・セキュリティ検証（Phase D3）**:
   - `./dcli code-check all` がエラー 0 件で通過すること。
   - `pillow>=13.0.0` 環境で `./dcli test all` が全件パスすること。
   - Trivy スキャン（`security_scan`）で `app_vuln_counts.total == 0`（41 件 → **0 件**）および `DS-0002 == 0` になること。
   - `--network=none` コンテナ実行（`run_check`）でオフライン単体テスト通過率 **100%** を確認すること。
2. **`pni.toml` & 公開レポート検証（Phase P3 / D4）**:
   - `.pni/pni.toml` 適用後の `reports/full_audit_score.json` にローカル未追跡 `.env` 情報が含まれず、`opt_outs` メタデータが記録されていること。
   - `./dcli docs build reports` と `./dcli docs serve reports --check` がリンク切れ 0 件で通過すること。
   - 生成された `docs/reports/pni-full-audit/en/index.html`（ブラウザ表示・`▶ Source Code` 展開）および `docs/reports/pni-full-audit/full_audit.pdf`（`view_file` 全ページ確認）で視覚崩れ・表見切れがないこと。
