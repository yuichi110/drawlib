# PNI501 × Drawlib 品質監査・相互改善計画書 (Audit & Cross-Repo Integration Plan)

- **作成日**: 2026-11-03
- **対象リポジトリ**:
  1. **`pni501` 側** (`pni` パッケージ / CLI): 監査エンジン・AST アナライザ・Drawlib レポートコンパイラ側
  2. **`drawlib` 側** (`drawlib` `v0.3.5+`): 監査対象ライブラリ兼レポート描画エンジン側
- **目的**:
  - `pni501` を用いて `drawlib` のコード品質・アーキテクチャ境界・依存関係・テスト・セキュリティを定量診断し、`drawlib` 自身で診断レポート（PDF / HTML）を出力する継続的品質監査基盤を構築する。
  - 中規模 Python パッケージ（`src/drawlib`: 458ファイル・約18.8万行、`tests`: 179ファイル・約3.4万行）を実題材として、`pni501` 側のスケーラビリティ・最新 `drawlib v0.3.5` 対応・AST 解析精度を同時に引き上げる（二重のドッグフーディング）。

---

## 1. 全体ロードマップ（推奨実行順序）

| ステップ | 作業対象リポジトリ | フェーズ名 | 主な内容 | 依存関係 |
| :---: | :---: | :--- | :--- | :--- |
| **Step 1** | **`pni501`** | **Phase P1: ブロッカー解消（SCC 化 & `drawlib 0.3.5` 対応）** | ・`detect_cycles()` の Tarjan SCC 化（458ファイルでのハング解消）と `if TYPE_CHECKING:` 分離<br>・`drawlib >= 0.3.5` の `drawlib.toml` + `<target>_src/<lang>/` i18n レポート構造・`rules show` トピック名への追従 | 最優先 |
| **Step 2** | **`pni501`** | **Phase P2: AST 解析精度・ハイブリッド監査強化** | ・関数パラメータ抽出時のインラインコメント混入バグ修正<br>・生成コード（`*_generated.py`）除外オプション対応<br>・配布パッケージ名エイリアス拡充＋対象 `.venv` メタデータ参照<br>・`conftest.py` フック型アサーション認識・シークレット誤検知抑制・`hybrid` 判定強化 | Step 1 と並行可 |
| **Step 3** | **`drawlib`** | **Phase D1: 事前検出されたコード品質・依存・CI 課題の修正** | ・直接 import している `pillow` / `numpy` / `markupsafe` の `pyproject.toml` 明示宣言<br>・外部 HTTP タイムアウト・`hashlib.md5(..., usedforsecurity=False)`・`# type: ignore[...]` 修正<br>・レイヤー境界・内部循環参照・複雑度ホットスポット・GitHub Actions `permissions:` の整備 | 単独で先行着手可 |
| **Step 4** | **`drawlib`** | **Phase D2: `.pni/` ワークフロー・オフライン検証ハーネス導入と監査実行** | ・`.gitignore` 整理と `.pni/` 初期化<br>・`library_hygiene_audit` + `cli_guidelines_audit` を統合したカスタム `full_audit.yaml` 作成<br>・Playwright / 事前アセット取得を組み込んだ `.pni/dockerfiles/` ハーネス構築と監査レポート出力 | Step 1〜2 完了後 |

---

## 2. Part 1: `pni501` リポジトリ側の改善計画（`pni501` 共有用）

> **背景（`drawlib` に対する試験実行で判明した事実）**:
> `drawlib`（`src`: 458ファイル、`tests`: 179ファイル）に対して `run_project_inspect` と `PYTHON_SUITE` の各チェッカーを個別に計測したところ、ファイル探索（`0.08s`）・`ast-grep` パース（`1.26s`）・品質/型/Docstring 検査（各 `0.3s〜2.0s`）は極めて高速に動作した一方、以下のブロッカーと誤検知パターンが確認された。

### 2.1. Phase P1: ブロッカー解消（必須対応）

#### 1. 循環依存検出アルゴリズムの Tarjan SCC 化と `TYPE_CHECKING` 分離
- **対象ファイル**:
  - `src/pni/_actions/ast_analyze/base/dependencies.py`
  - `src/pni/_actions/ast_analyze/python/dependencies.py`
  - `src/pni/_actions/ast_analyze/models.py`（必要に応じてフィールド追加）
  - `tests/pni/test_health_checkers.py`
- **現状の課題**:
  - `BaseDependencyChecker.detect_cycles(graph)` が全ノードを始点に枝刈りなしで単純閉路を探索する DFS 実装になっているため、458ノード・1,607エッジ（10ノードの強連結成分や多層ダイヤモンド DAG を含む）で経路数が指数爆発し、数分以上経過しても完了しない。
  - また Python の `if TYPE_CHECKING:` ブロック内のみの import も通常の実行時 import と同一視しているため、型ヒント専用の相互参照（例: `_chart.py` ⇄ `_renderer.py`）によって強連結成分が肥大化し、実行時には発生しない循環依存として減点される。
- **改修仕様**:
  1. **Tarjan の強連結成分分解（SCC）の導入**:
     - まず線形時間 $O(V + E)$ で非自明な SCC（ノード数 $\ge 2$、または自己ループ）を抽出する。DAG 部分のエッジは一切探索しないため、循環ゼロの大規模グラフでは即座に完了する。
     - 各非自明 SCC の誘導部分グラフ内でのみ代表的な単純閉路を抽出し、1つの SCC あたりの閉路抽出数上限（例: `max_cycles_per_scc = 5`、全体上限 `max_total_cycles = 50`）および探索ステップ上限を設けて最悪計算量を保証する（`drawlib` 規模で `< 0.05s` を達成すること）。
  2. **`if TYPE_CHECKING:` ガード内 import の分離（Python）**:
     - `PythonDependencyChecker.build_import_graph()`（`_extract_unit_imports`）において、親ノードを辿って `if TYPE_CHECKING:`（または `if typing.TYPE_CHECKING:`）ブロック内にある import 文を判別する。
     - `internal_import_graph` / `circular_dependencies` は**実行時 import のみ**を対象とする（必要に応じて型チェック時のみの循環は別フィールド `type_checking_cycles` や情報メトリクスとして分離保持する）。

#### 2. `drawlib >= 0.3.5` の i18n プロジェクト構造（`drawlib.toml` + `<src_dir>/<lang>/`）への追従
- **対象ファイル**:
  - `pyproject.toml`, `uv.lock`
  - `src/pni/_reporter/compiler.py`
  - `src/pni/_reporter/drawlib_guide.py`
  - `src/pni/_reporter/blueprint.py`, `migration_blueprint.py`, `progress_blueprint.py`
  - `src/pni/_actions/common/write_drawlib_report.yaml`, `write_migration_report.yaml`, `write_progress_report.yaml`
  - `docs/doc_src/`（`pni501` 自身のドキュメントプロジェクト）
  - `tests/pni/test_reporter.py`, `tests/pni/test_architecture_and_cli_guides.py`
- **現状の課題**:
  - `pni501` は現在 `drawlib == 0.3.1` でロックされているが、`drawlib 0.3.5` では `init_project("doc", ..., lang="en")` が `<target>_src/drawlib.toml` とロケール別サブディレクトリ `<target>_src/en/00_cover.md` を生成し、`build_pdf` も `<target>_<lang>.pdf` を出力してデフォルトロケールの生成パス（`str`）を返す仕様に進化している。
  - 現行の `compiler.py` はフラットな `src_dir.glob("*.md")` のみを探索するため、`drawlib 0.3.5` 環境ではチャプター検出・サンプル削除・PDF 出力パス解決が不整合になる。
  - またプロンプト内の `drawlib rules show lib-smartarts` / `lib-charts` / `lib-diagrams` は、`drawlib 0.3.5` では `lib-smartarts-overview` / `lib-charts-overview` / `lib-diagrams-overview` に改称・分割されている。
- **改修仕様**:
  1. **依存バージョンの引き上げ**:
     - `pyproject.toml` の依存を `drawlib>=0.3.5` に更新し、`uv lock` で更新する。
  2. **`src/pni/_reporter/compiler.py` の `drawlib.toml` / `<lang>/` ネイティブ対応**:
     - `src_dir / "drawlib.toml"` が存在し `[i18n]` セクションがある場合、`default_lang`（未指定時 `"en"`）のディレクトリ `chapter_dir = src_dir / default_lang` をチャプター格納先として解決する（既存のレガシーフラット `<target>_src/*.md` プロジェクトも後方互換でフォールバック読み込み可能にする）。
     - `_restore_or_clean_chapters()` も `chapter_dir` 配下のスターターチャプター（`00_cover.md`, `01_overview.md`, `02_design.md`）を対象に保護・クリーンアップを行う。
     - `drawlib_tools.build_pdf(...)` 実行時、戻り値として返却される実出力 PDF パス（例: `reports/<target>_en.pdf`）を受け取り、呼び出し側が期待する `output_dir / f"{clean_target}.pdf"` と異なる場合はリネームまたはコピーで正規化（あるいは `ReportBuildResult.pdf_file` に実パスを正確に格納）して単一言語レポートの出力パス契約を維持する。
     - `_DrawlibToolsProtocol` のシグネチャを `drawlib 0.3.5` の `drawlib.tools`（`input_dir` / `input_path` 等）と整合させる。
  3. **AI ガイド・プロンプト・`pni501/docs` の同期**:
     - `write_*_report.yaml` および `drawlib_guide.py` のチャプター配置説明を `<src_dir>/<target>_src/<lang>/00_cover.md` に更新する。
     - `drawlib rules show` の参照コマンドを現行トピック名（`overview`, `style-guide`, `review-guide`, `api`, `project-doc`, `lib-smartarts-overview`, `lib-charts-overview`, `lib-diagrams-overview`）へ更新する。
     - `pni501` リポジトリ自身の `docs/doc_src/` および `reports_src/` も必要に応じて `drawlib 0.3.5` 形式でクリーンに再ビルドできることを確認する。

---

### 2.2. Phase P2: AST 解析精度・誤検知抑制・ハイブリッド監査の強化

#### 1. Python 関数パラメータ抽出へのコメントノード混入バグ修正
- **対象ファイル**: `src/pni/_actions/ast_analyze/python/_helpers.py`（`extract_callable_param_names`）
- **原因**: Tree-sitter Python（`ast-grep-py`）では、複数行の関数定義パラメータリスト内に書かれた `# noqa` や `# Icon Properties` などのコメントも `parameters` の `named_children()`（`kind() == "comment"`）に含まれるため、現行実装がこれをパラメータ名 `'# noqa'` として抽出し、`doc_signature_mismatches` に偽陽性を出している。
- **改修仕様**:
  - `extract_callable_param_names()`（および型・品質チェッカー側の `parameters.named_children()` 走査箇所すべて）で `param.kind() == "comment"` を明示的にスキップする（または有効なパラメータノード種別 `identifier`, `typed_parameter`, `default_parameter`, `typed_default_parameter`, `list_splat_pattern`, `dictionary_splat_pattern` のホワイトリストでフィルタする）。

#### 2. 自動生成ファイル（`*_generated.py` 等）の除外オプション追加
- **対象ファイル**:
  - `src/pni/_workflows/base_model.py`（`WorkflowTargets` に `exclude: list[str] = []` 追加）
  - `src/pni/_actions/ast_analyze/runner.py`（`discover_source_files` および `analyze` での除外 glob 適用）
  - `src/pni/_actions/project_inspect.py`
- **背景**: `drawlib` には `phosphor/_generated.py`（27,556行）をはじめ34個の `_generated.py`（計約8万行・約5,000関数）と、それを再エクスポートする `from ..._generated import *`（34箇所）が存在する。手書きコードの品質指標が生成コードの行数・関数数で希釈されたり、生成モジュール再エクスポートが `wildcard_imports` 違反になったりするのを防ぐ。
- **改修仕様**:
  - ワークフロー YAML の `targets.exclude`（例: `["**/*_generated.py"]`）を `project_inspect` と `ast_analyze` に伝播させ、対象外ファイルを除外できるようにする。
  - あわせて `PythonImportChecker` で `__init__.py` が同一パッケージ内の `._generated` を再エクスポートし `__all__` を定義しているパターン（または除外対象モジュールからの import）を考慮できるようにする。

#### 3. PyPI 配布名 ⇄ import 名解決の強化（対象プロジェクト `.venv` の活用）
- **対象ファイル**: `src/pni/_actions/ast_analyze/python/dependencies.py`
- **現状の課題**: `_build_env_import_to_dist_map()` が `pni` 自身の実行プロセス環境の `importlib.metadata.packages_distributions()` のみを参照するため、`pni` 環境に未インストールのパッケージ（例: `python-docx` → `docx`, `python-pptx` → `pptx`, `markdown-it-py` → `markdown_it`）が `unused_dependencies` / `undeclared_dependencies` と誤判定される。
- **改修仕様**:
  1. `_DIST_TO_IMPORT_ALIASES` に主要パッケージの対応（`"python_docx": ("docx",)`, `"python_pptx": ("pptx",)`, `"markdown_it_py": ("markdown_it",)`, `"pygments": ("pygments",)` 等）を追加する。
  2. `project_root / ".venv"` が存在する場合、`importlib.metadata.distributions(path=[...site-packages...])` から `top_level.txt` / `RECORD` を読み取り、対象プロジェクト自身の仮想環境にインストールされている正確な配布パッケージ名 ⇄ import 名マッピングをマージする。

#### 4. `conftest.py` フック型アサーション認識とシークレット定数誤検知の抑制
- **対象ファイル**:
  - `src/pni/_actions/ast_analyze/python/testing.py`, `src/pni/_actions/ast_analyze/models.py`
  - `src/pni/_actions/ast_analyze/base/operational.py`
- **改修仕様**:
  1. **テストアサーション検出の改善**:
     - `drawlib` の `tests/conftest.py` のように `pytest_runtest_call` フック内で生成物を自動検証（`assert check_image_match(...)`）するテストスイートに対応するため、`conftest.py` に `pytest_runtest_call` や `autouse=True` フィクスチャ内の `assert` が存在するかを検出し、`AstFacts` に補足コンテキスト（例: `test_harness_notes`）として記録するか、プロジェクト側で追加アサーションヘルパー名を認識できるようにする。
  2. **シークレット検出ヒューリスティックの精緻化 (`is_likely_secret_literal`)**:
     - 文字列リテラルが画像・データファイル名（`.png`, `.svg`, `.jpg`, `.json`, `.yaml`, `.ttf`, `.otf` 等の拡張子）やアイコン識別子である場合、および識別子に `icon`, `asset`, `image`, `color`, `style` 等の非シークレット語が含まれる場合は `False` を返し、`ONEPASSWORD = "..."` / `K8S_SECRET = "..."`（クラウド・ITサービスアイコン定数）の誤検知を解消する。

#### 5. `hybrid` アーキタイプ判定と大規模テスト実行オプションの拡充
- **対象ファイル**:
  - `src/pni/_actions/project_inspect.py`
  - `src/pni/_actions/runtime_check/models.py`, `runner.py`
- **改修仕様**:
  - `[project.scripts]` を持ちつつ、`py.typed` マーカーや複数の公開ライブラリファサードモジュールを持つパッケージを `runtime_type_hint = "hybrid"` と判定できるようにする。
  - `RuntimeCheckOptions` に `pytest_extra_args: list[str]`（例: `["-n", "auto", "--dist", "loadfile"]`）や事前セットアップコマンド（`pre_test_cmd`: 例 `drawlib cache download --all`）を指定可能にし、大規模・オフライン資産依存プロジェクトでも `.pni/workflows/full_audit.yaml` の `with:` だけで柔軟に制御できるようにする。

#### 6. `pni501` 側の検証ゲート
```bash
./pcli code-check all
./pcli test all
./docs/doc_src/build.sh
```

---

## 3. Part 2: `drawlib` リポジトリ側の品質改善・導入計画

### 3.1. Phase D1: 事前試験で判明した `drawlib` 本体の品質・依存・ガバナンス改善

*(※ 本フェーズは `pni501` 側の改修完了を待たずに、`drawlib` 単体の品質向上として先行実施可能)*

#### 1. 直接 import しているランタイム依存パッケージの明示宣言 (`DEP001` 解消)
- **対象ファイル**: `pyproject.toml`
- **内容**:
  - 現在 `src/drawlib/` 内で直接 `import PIL` / `import numpy` / `import markupsafe` を行っているが、`matplotlib` および `jinja2` の間接依存に頼っている。
  - `[project.dependencies]` に互換性のある柔軟な SemVer 下限（例: `"pillow>=10.2"`, `"numpy>=1.26"`, `"markupsafe>=2.1"` — `./dcli pypi deps` で現行解決ツリーと Python 3.11〜3.13 互換性を確認のうえ決定）を明示追加する。

#### 2. 外部通信タイムアウト・FIPS 互換 MD5・型 ignore・例外ハンドリングの改善
- **外部 HTTP タイムアウトの明示**:
  - `src/drawlib/_core/l3_external/_package.py`: `urllib.request.urlopen(req, timeout=60)` のように明示的タイムアウト引数を追加し、ネットワーク不調時の無期限ハングを防止する。
- **非暗号用途 MD5 の FIPS 環境対応**:
  - `src/drawlib/_core/l3_external/_download.py` および `src/drawlib/_core/l4_canvas/_text_utils.py`: キャッシュキー生成用の `hashlib.md5(...)` に `usedforsecurity=False` を付与する。
- **スコープなし `# type: ignore` の解消（4箇所）**:
  - `src/drawlib/_core/l3_images/_dimage.py`
  - `src/drawlib/_core/l4_canvas/_image_code.py`
  - `src/drawlib/_diagrams/state/_render_transition.py`
  - 上記の素の `# type: ignore` を具体的なエラーコード指定または型安全な記述へ修正し、`./dcli code-check type`（`ty`）を通過させる。
- **サイレントな `try ... except ...: pass` の整理（6箇所）**:
  - `src/drawlib/_builder/_common/office.py`, `src/drawlib/_builder/doc_builder/processor/options.py`, `src/drawlib/_cli/commands/show.py`, `src/drawlib/_core/l3_styles/_base_styles.py`, `src/drawlib/_slide/_blocks.py`, `src/drawlib/_templates/_project.py` の意図的な例外無視を `contextlib.suppress(...)` または適切なデバッグログ出力に統一する。

#### 3. レイヤー境界・内部循環参照・複雑度ホットスポットの点検
- **内部コア ⇄ 公開ファサード間の参照整理**:
  - `src/drawlib/_core/l4_canvas/_image_code.py` が公開ファサード `drawlib.canvas` を参照して生じている循環（`l4_canvas -> _image_code -> drawlib.canvas -> l4_canvas`）を確認し、`l4_canvas` 内部シンボルで完結できる場合は下位レイヤー内参照へ整理する。
- **サブパッケージ間のプライベートモジュール直接参照の整理**:
  - `src/drawlib/_diagrams/_common.py` から `_icons.*._generated` への直接 import や、`_builder` から `_core.l4_canvas._base` / `_canvas`・`_slide._assets` / `_blocks` への参照について、各サブパッケージの `__init__.py` を境界窓口として経由する形へ段階的に整理する。
- **高認知的複雑度関数の分割検討**:
  - `src/drawlib/_builder/_common/cache.py` の `_hash_referenced_local_assets` 等、分岐・ネストが深い関数を小さな純粋ヘルパー関数へ分割し保守性を高める。

#### 4. GitHub Actions 権限の最小化・サプライチェーン衛生
- **対象ファイル**:
  - `.github/workflows/quality.yml`
  - `.github/workflows/ut_github.yml`
  - `.github/workflows/ut_pypi.yml`
  - `.github/workflows/ut_template.yml`
- **内容**:
  - 各ワークフローの最上位（またはジョブ単位）に `permissions: contents: read` を明記し、`GITHUB_TOKEN` のデフォルト権限を最小化する（OpenSSF Scorecard 準拠）。

---

### 3.2. Phase D2: `pni501` 改修後の `drawlib` への `.pni/` 導入と監査運用

#### 1. 実行方式とリポジトリ管理方針
- **実行方式**:
  - `pyproject.toml` の `[dependency-groups].dev` および `[tool.uv.sources]` に `pni501 = { git = "https://github.com/yuichi110/pni501.git" }` を登録し、`uv run pni ...` で実行する。
- **レポート配置規約（ソース・出力とも `reports/` に集約）**:
  - PNI レポートの Drawlib ソースプロジェクトとコンパイル済み出力物の**両方**を `/usr/local/google/home/yuichiito/git_github/drawlib/reports` 配下に配置する：
    - レポートソースコード: `reports/full_audit_src/`（`src_dir: "reports"`）
    - スコア JSON / 生成 PDF: `reports/full_audit_score.json`, `reports/full_audit.pdf`（`output_dir: "reports"`）
  - `pyproject.toml` の `[tool.ruff] exclude` に `"reports"` を追加し、生成テンプレートファイルが `drawlib` 本体の著作権ヘッダ検査（`CPY`）等と干渉しないようにする。
- **`.gitignore` の整備**:
  - `.pni/cache/`、`.pni/state.db*` を `.gitignore` に追加する。
  - `.pni/workflows/`、`.pni/dockerfiles/`、および `reports/` はバージョン管理可能にする。

#### 2. `drawlib` 向けカスタムワークフロー (`.pni/workflows/full_audit.yaml`)
- `drawlib` は **Python ライブラリ（SDK）かつ CLI ツール（`drawlib` コマンド）** のハイブリッド構成であるため、以下の構成で定義する：
  - `targets`:
    - `source`: `["src/drawlib"]`
    - `tests`: `["tests/drawlib"]`
    - `docs`: `["README.md"]`
    - `exclude`: `["**/*_generated.py"]`（自動生成アイコンバインディングのノイズを分離）
  - `steps`:
    1. `repo_structure_audit`（リポジトリ構造・マニフェスト・CI 検査）
    2. `python_ast_audit`（Python AST 品質・型・Docstring・依存グラフ検査）
    3. `architecture_analysis`（3観点のアーキテクチャ記録：`l1_core..l4_canvas`, ドメインモジュール, `_builder`/`_cli`）
    4. `library_hygiene_audit`（公開 SDK 境界・`py.typed`・SemVer 依存境界・Import 純粋性）
    5. `cli_guidelines_audit`（`drawlib` CLI の `--help`/`--version`・終了コード・標準出力分離）
    6. `supply_chain_audit`（GitHub Actions 権限・シークレット衛生）
    7. `python_test_audit`（テストスイート構成・`conftest.py` 画像比較フック考慮）
    8. `container_runtime_audit`（クリーンルームビルド・`--network=none` 全単体テスト・実測カバレッジ・CLI/Import スモーク）
    9. `security_vulnerability_audit`（Trivy による CVE・シークレット・CWE シンク診断）
    10. `emit_score`（`output_dir: "reports"`, `target: "full_audit"` → `reports/full_audit_score.json`）
    11. `write_drawlib_report`（`src_dir: "reports"`, `output_dir: "reports"`, `target: "full_audit"` → `reports/full_audit_src/en/` から `reports/full_audit.pdf` を生成）

#### 3. `drawlib` 用コンテナ検証ハーネス (`.pni/dockerfiles/root/Dockerfile`)
- `tools/docker/Dockerfile.test_local` と同等のオフラインテスト成立条件を満たすハーネスを構成する：
  1. `apt-get` で `libgl1`, `libglx-mesa0`, `libglib2.0-0` を導入（`matplotlib` 用）。
  2. `.dockerignore` で除外される `docs_src/README_PYPI.md` に対し、パッケージインストール前に `mkdir -p docs_src && touch docs_src/README_PYPI.md` を実行して `uv pip install -e .` を通す。
  3. イメージビルド時（ネットワーク有効時）に `playwright install --with-deps --only-shell chromium` および `drawlib cache download --all` を実行し、`container_runtime_audit` の `--network=none` 環境でも PDF/PPTX テストおよびフォント・アイコンテストが100%オフライン通過するようにする。
  4. `pytest-xdist` を導入し、並列実行オプション（または十分な `test_timeout_sec`）でカバレッジ計測を実行する。

#### 4. `drawlib` 側の検証ゲート
```bash
./dcli code-check all
./dcli test all
./dcli docs build --all
./dcli docs serve site --check
```
- さらに `pni` が生成した `drawlib` 診断レポート（`00_cover.md` 〜 `06_security_and_supply_chain.md`）に対し、`drawlib show ... -g` によるグリッド目視確認（Stage 2）とビルド済み PDF の確認（Stage 3）を実施する。
