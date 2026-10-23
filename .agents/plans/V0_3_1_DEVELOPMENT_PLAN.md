# Drawlib v0.3.1 開発計画書 (Development Plan)

- **作成日**: 2026-10-22（**更新日**: 2026-10-23）
- **対象バージョン**: Drawlib `v0.3.1` (`0.3.1.dev1` → `0.3.1`)
- **方針変更メモ**:
  - ユーザーフィードバックのあった **起動・Import パフォーマンス問題（および Pydantic v2.11 非推奨警告）の解消** と、先行実装済みの **`HeatmapChart` / `HeatmapOverlay`** を迅速にリリースするため、`v0.3.1` のスコープをこれらに限定する。
  - 当初 `v0.3.1` に含めていた残りの設計改善・バグ修正・機能追加（`Charts` 基準線 / 100%積み上げ、`Lines` / `Slide` ユーティリティ等）はすべて [`V0_3_2_DEVELOPMENT_PLAN.md`](./V0_3_2_DEVELOPMENT_PLAN.md) へ移行した。

---

## 1. `v0.3.1` スコープと進捗状況

| フェーズ | 状態 | 対象領域 | 主な作業内容 |
| :--- | :---: | :--- | :--- |
| **Phase 1: `HeatmapChart` / `HeatmapOverlay` 実装** | ✅ 完了 | `src/drawlib/_charts/heatmap_chart/`, `src/drawlib/charts/`, `docs/` | ・2次元マトリクスヒートマップ `HeatmapChart` および空間サーマルオーバーレイ `HeatmapOverlay` の実装・単体テスト・ドキュメント作成（コミット `8fabcdc0`, `275ef054`） |
| **Phase 2: 起動・Import パフォーマンス最適化 & 非推奨警告解消** | ✅ 完了 | `__init__.py`, `tools.py`, `styles.py`, `icons.py`, `_core/l1_core/`, `_core/l3_styles/`, `_preset_styles/`, `_cli/`, `tests/` | ・`drawlib/__init__.py`（全20サブモジュール）および公開・内部ファサードの PEP 562 遅延ロード化<br>・`BaseStyles` / `_preset_styles` の 20,643 フィールド型注釈の `TYPE_CHECKING` 分離、`defer_build=True`、`model_construct` 高速生成、テーマ別オンデマンド生成、`_BaseStylesMeta` 最適化<br>・`PydanticDeprecatedSince211`（インスタンスからの `model_fields` 参照）の解消<br>・`ParamSpec` 型保持付きの遅延 `@validate_call` デコレータ導入（全57ファイル）<br>・`_IconsSubmoduleFinder` によるアイコンスイート個別オンデマンド読込<br>・CLI サブコマンドおよび `rules_builder.py` の遅延 import 化<br>・サブプロセス分離型の遅延ロード回帰テスト (`tests/drawlib/test_lazy_imports.py`) 追加 |
| **Phase 3: リリース準備・ドキュメント同期** | ✅ 完了 | `src/drawlib/_rules/`, `docs/docs_src/`, `README.md`, `docs/README_PYPI.md` | ・`docs/docs_src/05_charts/heatmap.md` および `overview.md` の `Upcoming in v0.3.1` 注記・バッジ削除と8チャート体系への更新<br>・`src/drawlib/_rules/`（`agent_instruction.md`, `api.md`, `lib_charts.md`）および `README.md` / `README_PYPI.md` への `HeatmapChart` / `HeatmapOverlay` 同期<br>・`docs/docs_src/01_getting_started/release_notes.md` への `Version 0.3.1` セクション追加とドキュメント全体ビルド・リンク検証 |

---

## 2. 実装済み詳細（Phase 2: 起動・Import パフォーマンス最適化）

### 2.1. パッケージ境界および CLI の PEP 562 遅延ロード導入
- **`src/drawlib/__init__.py`**:
  - 全 20 サブモジュール（`anim`, `canvas`, `charts`, `diagrams`, `fonts`, `graph`, `icons`, `images`, `lines`, `math`, `preset_colors`, `preset_styles`, `shapes`, `slide`, `smartarts`, `styles`, `text`, `tools`, `types`, `utils`）を `if TYPE_CHECKING:` + `__getattr__` / `__dir__` による PEP 562 遅延ロードへ移行。
- **公開・内部ファサード群**:
  - `src/drawlib/tools.py`, `src/drawlib/styles.py`, `src/drawlib/preset_styles.py`, `src/drawlib/preset_colors.py`, `src/drawlib/smartarts.py`, `src/drawlib/charts/__init__.py`, `src/drawlib/diagrams/__init__.py`、および `_preset_styles/__init__.py`, `_preset_colors/__init__.py`, `_smartarts/__init__.py` を PEP 562 遅延ロード化。
- **アイコンスイート (`src/drawlib/icons.py`, `src/drawlib/_icons/`)**:
  - 約 14,000 個のアイコン関数を一括 import していた構造を改め、`_IconsSubmoduleFinder` (`sys.meta_path`) と PEP 562 `__getattr__` により `from drawlib.icons.phosphor import airplane` 等のサブモジュール構文を維持したまま対象スイート 1 種のみを読み込むよう最適化。
- **CLI・ビルダー (`src/drawlib/_cli/commands/`, `src/drawlib/_builder/rules_builder.py`)**:
  - `build`, `show`, `serve`, `cache`, `styles`, `colors` 各コマンドおよび `rules_builder.py` のトップレベルから重い描画・ビルダ import を関数実行時へ移動。

### 2.2. `Style` / `BaseStyles` / `_preset_styles` の高速生成と非推奨警告解消
- **`Style` / `BaseColors` (`defer_build=True` & `model_construct`)**:
  - `Style` と `BaseColors` の `ConfigDict` に `defer_build=True` を設定し、`_preset_styles/_utils.py` 内のプリセット生成を `Style.model_construct(...)` + 事前定義 `frozenset` 定数によるバリデーションバイパス方式へ変更。
- **`BaseStyles` & `_preset_styles`**:
  - `BaseModel` 継承互換性を維持したまま、`BaseStyles`, `DefaultStyles`, `GoogleStyles`, `MonochromeStyles` の計 20,643 フィールド注釈を `if TYPE_CHECKING:` ブロックへ移動。
  - `register_default_factory()` と `_construct_preset()` により、実際にアクセスされたテーマのみを初回利用時に 1 度だけ生成する方式へ変更（未使用テーマの即時インスタンス化を廃止）。
  - `_BaseStylesMeta.__getattribute__` による約 18.5 万回の発火を排除し、`__dict__` 直接格納による高速属性参照とクラスレベル `model_fields` / `field_names()` 参照への統一によって `PydanticDeprecatedSince211` 警告を解消。

### 2.3. 遅延 `@validate_call` デコレータの導入
- **`src/drawlib/_core/l1_core/_validator.py`**:
  - `ParamSpec` / `TypeVar` と `@overload` によって `ty` 型チェッカー向けのシグネチャと `dcli code-check docstring` の AST 検査互換性を保ちつつ、`pydantic.validate_call` のスキーマ構築を関数の初回呼び出し時まで遅延するラッパーを実装し、全 57 ファイルに適用。

### 2.4. 実測パフォーマンス改善結果

| シナリオ | 改善前 | 改善後 (in-proc / subproc) | 関数呼び出し数 (`cProfile`) |
| :--- | ---: | ---: | ---: |
| `import drawlib` | 約 2,500〜4,522 ms | **59.8〜94.6 ms** / 139.6 ms | 7,450,000 → **48,610 (-99.3%)** |
| `from drawlib.tools import init_project, scan_broken_links` | 3,130.7 ms | **94.1〜140.9 ms** / 194.0 ms | — → **80,932** |
| `drawlib` CLI ロード (`_cli._drawlib`) | 3,156.2 ms | **158.8〜198.5 ms** / 310.1 ms | — |
| `from drawlib.styles import Colors, Styles` | 3,006.3 ms | **369.2 ms** / 469.3 ms | — → **586,730** |
| `canvas` + `shapes` + `styles` | 2,954.8 ms | **1,515.2 ms** / 1,784.9 ms | — → **2,117,654** |

---

## 3. Phase 3（リリース準備）残タスクと完了基準

1. **ドキュメント & ルール更新**:
   - `docs/docs_src/05_charts/heatmap.md` および `docs/docs_src/05_charts/overview.md` から `Upcoming in v0.3.1` 注記・バッジを削除する。
   - `src/drawlib/_rules/api.md` および `src/drawlib/_rules/lib_charts.md` に `HeatmapChart` / `HeatmapOverlay` が最新仕様で反映されていることを確認・更新する。
   - `docs/docs_src/01_getting_started/release_notes.md` に `Version 0.3.1` セクションを追加する（`HeatmapChart` / `HeatmapOverlay`、起動・Import パフォーマンス大幅改善、Pydantic v2.11 非推奨警告解消等を記載）。
2. **リリース前最終検証**:
   ```bash
   ./dcli code-check all
   ./dcli test all
   ./dcli docs build --all
   ./dcli docs serve site --check
   ```
