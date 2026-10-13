# Drawlib v0.3.1 リリースに向けたリファクタリング計画書
(DRAWLIB v0.3.1 RELEASE REFACTORING PLAN)

- **更新日**: 2026-10-13
- **対象バージョン**: Drawlib `v0.3.1`
- **対象モジュール**:
  - `pyproject.toml`, `src/drawlib/__init__.py` (バージョン定義・メタデータ・バグ修正)
  - `src/drawlib/_templates/`, `src/drawlib/_core/l3_styles/`, `src/drawlib/_preset_styles/` (デッドコード削除・重複関数統合)
  - `src/drawlib/_core/l4_canvas/_shapes/` (`_symbol.py`, `_container.py`, `_badge.py`, `_util.py` の内部構造整理)
  - `src/drawlib/_smartarts/` (`_sourcecode.py`, `_mindmap.py`, `_calendar/`, および `.draw()` 戻り値 `Self` 統一)
  - `src/drawlib/_builder/`, `src/drawlib/_cli/`, `src/drawlib/_slide/`, `src/drawlib/_graph/` (`from __future__ import annotations`・PEP 604/585 モダン型ヒント統一・内部 import 整理)
  - `tests/drawlib/_core/l4_canvas/`, `.agents/plans/`, `tools/dcli/docs/`, `.agents/rules/docs.md` (テスト構成 1:1 ミラーリング・完了済み計画書整理・ビルドターゲット同期)

---

## 1. 背景と目的 (Executive Summary & Goals)

`v0.3` タグ以降、**376コミット**にわたり以下の大規模な機能拡張が行われてきた：
- **Shapes 43種への拡充**: `hole_ratio` 中抜き統合、`forbidden`, `checkmark`, `shield`, `ribbon`, `tag`, `pin`, `explosion`, `funnel`, `plaque`, `heart`, `sun`, `moon`, `clock`, `lightning`, `gear`, `math_symbol`, `cloud`, `brace` 等。
- **SmartArts コンポーネント群の新設**: `KpiCards`, `CardList`, `Roadmap`, `Panel`, `GeoMap`, `DayCalendar`, `WeekCalendar`, `MonthCalendar`。
- **Slide & ドキュメントビルダの強化**: `drawlib.slide` ヘルパー、マルチエージェント並列ワークフロー、新規ケーススタディ・スライドデッキ群の追加。

現時点で `./dcli code-check all` および `./dcli test all`（1,264件・カバレッジ 90%）はすべてパスしているものの、急速な機能追加に伴い **肥大化した単一ファイル（700〜1,850行）**、**重複ボイラープレート**、**旧来の型ヒント表記（`Optional`/`Union`/`List`）の混在**、**内部命名や `.draw()` シグネチャの不統一**、**完了済み計画書や未使用互換シムの残存** が生じている。

本計画では、公開 API の後方互換性と視覚出力を維持しながら、**6つのフェーズ**で段階的かつ安全にリファクタリングを実施し、`v0.3.1` リリースに向けたコードベース品質を確立する。

---

## 2. リファクタリング全体フェーズ一覧

| フェーズ | 対象領域 | 主な作業内容 | リスク |
| :--- | :--- | :--- | :---: |
| **Phase 1: バージョン・メタデータ SoT 統一 & デッドコード整理** | `pyproject.toml`<br>`src/drawlib/_core/l1_core/_const.py`<br>`src/drawlib/__init__.py`<br>`tools/dcli/pypi/`<br>`_templates/builder.py`<br>`_base_styles.py` / `_utils.py`<br>`.agents/plans/` | ・`pyproject.toml` をバージョン・メタデータの唯一の SoT（`"0.3.1.dev1"`）に統一<br>・`l1_core/_const.py` で `importlib.metadata.version(LIB_NAME)`（フォールバックなし）から `LIB_VERSION` を取得し `drawlib.__init__` へ再エクスポート<br>・`dcli pypi` の `pyproject.toml` 直接参照化と `update-pyproject` 廃止・バージョン構文検証の `dcli pypi` への移設<br>・未使用の `_templates/builder.py` 削除、重複関数 `_resolve_target_font()` の一元化、完了済み計画書の整理 | 低 |
| **Phase 2: モダン型ヒント（PEP 604/585）と `future annotations` 統一** | `src/drawlib/` 全域<br>（対象 45〜47 ファイル） | ・`from __future__ import annotations` 欠落ファイルへの追加<br>・`Optional[T]`, `Union[A, B]`, `List[T]`, `Dict[K, V]`, `Tuple[...]` を `T \| None`, `list[T]`, `dict[K, V]`, `tuple[...]` に統一（特に `_builder/image_builder.py`, `doc_builder/` 等） | 低 |
| **Phase 3: SmartArts の重複削減・API 一貫性向上** | `src/drawlib/_smartarts/` | ・`_sourcecode.py`: `SourceCodeStyles` の4テーマ生成ボイラープレート（約290行）を共通ファクトリに統合<br>・`_mindmap.py`: 4方向レイアウトメソッド（`_connect_and_layout_*` 約270行）の共通化<br>・`_calendar/`: `DayCalendar` / `WeekCalendar` / `MonthCalendar` 間の共通ヘッダー・タイトルバー・All-Day 描画ロジックの抽出<br>・既存 SmartArts の `.draw()` 戻り値を `Self`（メソッドチェーン可能）へ統一 | 中 |
| **Phase 4: Shapes 内部実装モジュールの構造整理** | `src/drawlib/_core/l4_canvas/_shapes/` | ・肥大化した `_symbol.py` (1,847行)、`_container.py` (1,434行)、`_badge.py` (1,021行)、`_util.py` (957行) のパス生成ヘルパー関数群と Canvas Feature クラス群の責務分離・モジュール分割 | 中 |
| **Phase 5: アーキテクチャ階層・内部 import・Builder 整理** | `src/drawlib/_core/`<br>`src/drawlib/_builder/`<br>`src/drawlib/_graph/`<br>`src/drawlib/_slide/` | ・内部モジュール（`_graph`, `_slide`, `_builder`, `_cli`）から公開ファサードへの import を内部モジュール直接参照へ整理<br>・`_slide/` 等の内部ファイル命名・構造の整理<br>・`image_builder.py` (909行) の責務整理（AST 解析・キャッシュ処理の分離） | 中 |
| **Phase 6: テスト構成 1:1 ミラーリング & `dcli docs` 同期** | `tests/drawlib/_core/l4_canvas/`<br>`tools/dcli/docs/builder.py`<br>`.agents/rules/docs.md` | ・`test_new_shapes.py` / `test_patches.py` 等を `_shapes/` の6カテゴリ（`test_basic.py`, `test_polygon.py`, `test_arrow.py`, `test_container.py`, `test_badge.py`, `test_symbol.py`）に合わせて再編<br>・`dcli docs` ターゲットと `docs.md` に `architecture` / `slide_ddos_incident_response` 等を同期 | 低 |

---

## 3. 各フェーズの詳細仕様

### 3.1. Phase 1: バージョン・メタデータ SoT 統一 & デッドコード・完了計画書の整理

1. **バージョン・メタデータの Single Source of Truth (SoT) 統一（最優先で先行実施）**:
   - [`pyproject.toml`](../../pyproject.toml) をパッケージメタデータ（`name`, `version`, `description`, `readme`, `authors`, `urls`）の唯一の SoT とし、`version = "0.3.1.dev1"`（リリース時は `"0.3.1"`）に更新する。
   - [`src/drawlib/_core/l1_core/_const.py`](../../src/drawlib/_core/l1_core/_const.py) にて `LIB_NAME: Final[str] = "drawlib"` および `LIB_VERSION: Final[str] = importlib.metadata.version(LIB_NAME)`（ハードコードされたフォールバック値なし）を定義し、[`src/drawlib/_core/l1_core/__init__.py`](../../src/drawlib/_core/l1_core/__init__.py) からエクスポートする。
   - [`src/drawlib/_core/l1_core/_logging.py`](../../src/drawlib/_core/l1_core/_logging.py) および内部モジュール（`_builder/_common/cache.py`, `_cli/_drawlib.py`, `_cli/_visualizers/colors/base.py`, `_cli/_visualizers/styles/base.py`）が `drawlib._core.l1_core` から `LIB_NAME` / `LIB_VERSION` を直接参照するように整理し、最下層 `l1_core` からルートパッケージ `drawlib` への逆方向依存を解消する。
   - [`src/drawlib/__init__.py`](../../src/drawlib/__init__.py) のコピーライト年号を `2026` に更新し、`l1_core` から `LIB_NAME`, `LIB_VERSION` を再エクスポート（`__version__: Final[str] = LIB_VERSION`）する。不要となった重複メタデータ定数（`AUTHORS`, `DESCRIPTION`, `HOMEPAGE`, `REPOSITORY`, `README`）、フォールバック関数 `_get_version()`、および import 時の `_check_version_syntax()` 実行を除去する。
   - [`tools/dcli/pypi/client.py`](../../tools/dcli/pypi/client.py) の `get_new_version()` が [`pyproject.toml`](../../pyproject.toml) から直接バージョンを読み取るように変更し、バージョン構文チェック関数 `check_version_syntax()`（Patch バージョン `parts[2]` 判定バグ修正済み）を `client.py` 側に統合する。これに伴い不要となった `tools/dcli/pypi/pyproject.py` および `./dcli pypi update-pyproject` サブコマンドを廃止する。
2. **デッドコード・重複コードの削除**:
   - 参照箇所ゼロ・カバレッジ 0% の後方互換ファイル [`src/drawlib/_templates/builder.py`](../../src/drawlib/_templates/builder.py) を削除する。
   - [`src/drawlib/_core/l3_styles/_base_styles.py`](../../src/drawlib/_core/l3_styles/_base_styles.py) と [`src/drawlib/_preset_styles/_utils.py`](../../src/drawlib/_preset_styles/_utils.py) に重複定義されている `_resolve_target_font()` を `_base_styles.py` 側に一元化し、`_utils.py` から削除（または import）する。
3. **完了済み計画書のクリーンアップ (`.agents/plans/`)**:
   - すでに実装・テスト・ドキュメント反映が完了している `SHAPES_EXPANSION_PLAN.md` と `SMARTARTS_CALENDAR_PLAN.md` を削除し、未実装の `DRAWLIB_NATIVE_ICONS_PLAN.md` と本計画書 `REFACTORING_0_3_1_PLAN.md` のみを残す。

---

### 3.2. Phase 2: モダン型ヒント（PEP 604 / PEP 585）と `from __future__ import annotations` の統一

[`code-style-guide.md`](../rules/code-style-guide.md) の「3. Type Hinting (`from __future__ import annotations`, built-in types for Python 3.11+)」に従い、コードベース全体の型アノテーションを統一する。

1. **`from __future__ import annotations` の追加**:
   - `src/drawlib/` 内で未記述のモジュール（`_core/l1_core/*`, `_core/l2_types/*`, `_core/l4_canvas/*`, `_smartarts/_bulletpoints.py`, `_smartarts/_gridlayout.py`, `_smartarts/_pyramid.py` 等 45ファイル）に `from __future__ import annotations` を追加する。
2. **レガシー `typing` コンテナ・Union 表記の刷新（47ファイル）**:
   - `_builder/image_builder.py`（63箇所）、`_builder/doc_builder/compiler/html.py`（44箇所）、`_builder/doc_builder/exporter_html.py`（34箇所）、`_builder/doc_builder/navbar.py`（34箇所）、`_builder/_common/styles_loader.py`（28箇所）、`_builder/_common/cache.py`（27箇所）等に残っている `Optional[X]`, `Union[X, Y]`, `List[X]`, `Dict[K, V]`, `Tuple[...]` を `X | None`, `X | Y`, `list[X]`, `dict[K, V]`, `tuple[...]` に置換する。
   - **注意点**: `@validate_call` デコレータが付与された公開関数・メソッドのシグネチャおよび docstring については、`./dcli code-check docstring` の規約（内部型エイリアス名を docstring に露出させない）を厳守する。

---

### 3.3. Phase 3: SmartArts の重複削減と API 一貫性向上

1. **[`src/drawlib/_smartarts/_sourcecode.py`](../../src/drawlib/_smartarts/_sourcecode.py)（773行 → 約520行へ削減）**:
   - `SourceCodeStyles` 内の `_get_default()`, `_get_monochrome()`, `_get_dark()`, `_get_google()`（各72行×4＝288行）は、9種類のトークン色（`box_fill`, `box_border`, `linenum`, `default`, `keyword`, `string`, `comment`, `number`, `function`, `type_`, `operator`）が異なるだけで `Style(...)` 生成コードが完全に重複している。
   - 共通ヘルパー `_build_theme_styles(...)` に統合し、ボイラープレートを約200行削減する。
2. **[`src/drawlib/_smartarts/_mindmap.py`](../../src/drawlib/_smartarts/_mindmap.py)（815行 → 約600行へ削減）**:
   - `_connect_and_layout_bottom`, `_connect_and_layout_top`, `_connect_and_layout_right`, `_connect_and_layout_left`（各67行×4＝268行）を、垂直分岐（`bottom` / `top`、符号 `sign = -1 | +1`）と水平分岐（`left` / `right`、符号 `sign = -1 | +1`）のパラメータ化ヘルパーに統合する。
3. **[`src/drawlib/_smartarts/_calendar/`](../../src/drawlib/_smartarts/_calendar/)（計2,193行の共通化）**:
   - `_week.py` (723行)、`_day.py` (575行)、`_month.py` (552行) で重複している上部タイトルバー描画（`_draw_title_bar`）、曜日テキストスタイル解決（日曜・土曜の色分け判定）、およびデフォルトイベントスタイル初期化処理を `_models.py`（または `_common.py`）の共通ヘルパーへ集約する。
4. **SmartArts `.draw()` 戻り値の `Self` 統一**:
   - 新規コンポーネント（`CardList`, `KpiCards`, `Panel`, `Roadmap`, `GeoMap`, `DayCalendar`, `WeekCalendar`, `MonthCalendar`）と同様に、`BoxList`, `BulletPoints`, `ChevronProcess`, `Cycle`, `GridLayout`, `MindMapNode`, `Pyramid`, `Table`, `TreeNode` の `.draw()`（および `.draw_flexible()`）が `return self` (`-> Self`) を返すように統一し、宣言的メソッドチェーンを一貫して利用可能にする。

---

### 3.4. Phase 4: Shapes (`_core/l4_canvas/_shapes/`) のモジュール分割・責務整理

現在、`src/drawlib/_core/l4_canvas/_shapes/` 配下のファイルが以下のように肥大化している：
- [`_symbol.py`](../../src/drawlib/_core/l4_canvas/_shapes/_symbol.py): **1,847行**（L1〜1409 が `face`, `clock`, `sun`, `moon`, `heart`, `lightning`, `gear`, `math_symbol` のパス構築関数、L1410〜1842 が `CanvasShapeSymbolFeature`）
- [`_container.py`](../../src/drawlib/_core/l4_canvas/_shapes/_container.py): **1,434行**（L1〜916 が `cylinder`, `cloud`, `brace`, `cube`, `document`, `funnel` のパス構築関数、L919〜1429 が `CanvasShapeContainerFeature`）
- [`_badge.py`](../../src/drawlib/_core/l4_canvas/_shapes/_badge.py): **1,021行**（L1〜631 がパス構築関数、L634〜1016 が `CanvasShapeBadgeFeature`）
- [`_util.py`](../../src/drawlib/_core/l4_canvas/_shapes/_util.py): **957行**（`ShapeUtil` クラス単体に28メソッドが集約）

#### リファクタリング方針
- 外部公開インターフェース（`drawlib.shapes` および `drawlib._core.l4_canvas._shapes.CanvasShapeFeature`, `ShapeUtil`）は 100% 維持したまま、各カテゴリまたはパス構築ロジックを 300〜600行程度の見通しの良い内部モジュール（またはサブパッケージ）に分割する：
  - 例：`_symbol.py` の幾何パス構築ヘルパー群を `_symbol_builders.py`（または個別ヘルパーモジュール）へ分離し、`_symbol.py` 本体は `CanvasShapeSymbolFeature` の `@validate_call` メソッド定義（約430行）に集中させる。
  - 同様に `_container.py` と `_badge.py` もパス・パッチ構築ロジック（`_container_builders.py`, `_badge_builders.py`）と Feature クラス定義を分離する。

---

### 3.5. Phase 5: アーキテクチャ階層・内部 import・Builder 整理

1. **内部モジュールにおける公開ファサード import の整理**:
   - `_graph/`（`_common/_renderer.py` 等）、`_slide/`（`helpers.py` 等）、`_smartarts/` 等で `from drawlib.shapes import ...` や `from drawlib.styles import ...` を使っている箇所を、レイヤー構造に従い `from drawlib._core.l4_canvas import ...` / `from drawlib._core.l3_styles import ...` / `from drawlib._preset_styles import ...` に統一する（ただしコード生成文字列を出力する `_graph/_common/_code_generator.py` やテンプレート用ファイルは除く）。
2. **`_builder/image_builder.py` (909行) の構造整理**:
   - [`image_builder.py`](../../src/drawlib/_builder/image_builder.py) から AST による静的 `save()` 解析・重複出力検査ロジックを独立した内部ヘルパーモジュールへ抽出し、`DrawlibExecuter` 本体の可読性と保守性を高める。

---

### 3.6. Phase 6: テスト構成の 1:1 ミラーリング & `dcli docs` 同期

1. **`tests/drawlib/_core/l4_canvas/` のテストファイル再編**:
   - [`testing.md`](../rules/testing.md) の「1:1 パッケージ構造ミラーリング」原則に従い、暫定的なファイル名になっている [`test_new_shapes.py`](../../tests/drawlib/_core/l4_canvas/test_new_shapes.py)（`hole_ratio` + 新規13図形のテスト）および個別図形テスト（`test_cloud_and_brace.py`, `test_cube_and_document.py`, `test_cylinder.py`, `test_face.py`, `test_gear.py`, `test_math_symbol.py`, `test_bubblespeech.py`, `test_patches.py`）を、`src/drawlib/_core/l4_canvas/_shapes/` の6カテゴリ（`test_basic.py`, `test_polygon.py`, `test_arrow.py`, `test_container.py`, `test_badge.py`, `test_symbol.py`, `test_shape_utils.py`）に対応付けて整理する。
2. **[`tools/dcli/docs/builder.py`](../../tools/dcli/docs/builder.py) と [`.agents/rules/docs.md`](../rules/docs.md) の同期**:
   - `docs/slide_ddos_incident_response_src/`（ターゲット名 `slide-ddos` / `slide_ddos_incident_response`）および `docs/logo_src/`（ターゲット名 `logo`）を `tools/dcli/docs/builder.py` の `ALL_TARGETS` に追加する。
   - `.agents/rules/docs.md` および `.agents/rules/dcli.md` のターゲット一覧テーブルを更新し、リポジトリ内の全ドキュメントプロジェクトを `./dcli docs build --all` で一括検証できるようにする。

---

## 4. 検証・品質保証手順 (Verification Workflow)

各フェーズの完了ごとに、必ず以下の検証ループを実行する：

1. **静的解析スイートの実行**:
   ```bash
   ./dcli code-check all
   ./dcli code-check lines
   ```
   - Ruff lint / format、Ty 型チェック、`@validate_call` の docstring 型エイリアス検査がエラーゼロで通過することを確認する。
2. **単体・統合テストの実行**:
   ```bash
   ./dcli test all
   ```
   - 全テストスイートが 100% パスし、リファクタリング前後でテスト欠落やカバレッジ低下がないことを確認する。
3. **ドキュメントビルド & リンク検証（最終フェーズ）**:
   ```bash
   ./dcli docs build site --no-clean
   ./dcli docs serve site --check
   ```
   - 実際のドキュメント・図面ビルドで破壊的変更がないことを確認する。
