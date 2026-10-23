# Drawlib v0.3.2 開発計画書 (Development & Refactoring Plan)

- **作成日**: 2026-10-23（`V0_3_1_DEVELOPMENT_PLAN.md` から未実施フェーズを移行）
- **対象バージョン**: Drawlib `v0.3.2` (`0.3.2.dev1` → `0.3.2`)
- **背景**:
  - `v0.3.1` では先行実装済みの `HeatmapChart` / `HeatmapOverlay` と、ユーザー報告のあった起動・Import パフォーマンス最適化（および Pydantic v2.11 非推奨警告解消）を優先リリースした（詳細は [`V0_3_1_DEVELOPMENT_PLAN.md`](./V0_3_1_DEVELOPMENT_PLAN.md) を参照）。
  - 本計画書では、当初 `v0.3.1` で計画していた残りの設計改善・バグ修正・機能追加・品質整備を `v0.3.2` のスコープとして定義する。
- **スコープ**:
  1. **設計の改善・バグ修正・品質整備**（API一貫性、座標・スタイルバグ修正、肥大化モジュール分割、ビルダ・CLI・`dcli`・AIルール・ドキュメント同期）
  2. **機能追加 A: `Charts` の表現力強化**（基準線 `add_reference_line`・ターゲット帯 `add_reference_band`・`BarChart` の `percent_stack`・`LineChart`/`AreaChart` の `value_format` 対応）
  3. **機能追加 B: `Lines` / `Slide` のユーティリティ強化**（直交クランク線 `elbow_line`、線プリミティブのインライン `text` ラベル対応、スライド表紙・標準ヘッダーヘルパー `draw_title_slide` / `draw_slide_header`）
  - *(※ `Diagrams × Graph` の自動レイアウト連携および `SmartArts` の `get_size()` / アイコン統合は `v0.3.3` 以降へ見送り)*

---

## 1. フェーズ全体構成

| フェーズ | 区分 | 対象領域 | 主な作業内容 | リスク |
| :--- | :---: | :--- | :--- | :---: |
| **Phase 1: ドメイン API 一貫性・座標バグ・テーマ互換性の修正** | 設計改善 | `_charts/`, `_diagrams/`, `_smartarts/`, `_preset_styles/`, `_slide/` | ・`Charts` / `Diagrams` の `.draw()`（および `.draw_legend()`, `.draw_colorbar()`）戻り値を `Self` に統一<br>・`ClassDiagram`, `StateDiagram`, `HeatmapOverlay`, `PieChart`, `RadarChart` の公開 `.width` / `.height` 属性統一<br>・`ClassDiagram` / `StateDiagram` の `align="bottom_left"` 原点ズレ修正 & `Diagrams` 共通レイアウト処理の統合<br>・`GridLayout.draw_flexible()` のセル内テキスト左寄せバグ修正<br>・`MonochromeStyles` の欠落トークン（`Neutral`, `PrimaryNeutral`, `Success`, `Chart1..6` 等）補完<br>・`Charts` / `Diagrams` のデフォルト `text_font` 継承改善（CJK 豆腐化防止）<br>・`_slide/helpers.py`, `_smartarts/_geomap/_geomap.py` の内部 import 整理 | 低〜中 |
| **Phase 2: 肥大化モジュール分割・Codegen・Builder・CLI・`dcli` 改善** | 設計改善 | `_diagrams/architecture/`, `_smartarts/_mindmap.py`, `_builder/`, `_slide/`, `_cli/`, `tools/dcli/` | ・`_diagrams/architecture/_icons.py` (4,781行) の分割と `./dcli codegen` 整理<br>・`_smartarts/_mindmap.py` の4方向分岐ラッパー共通化<br>・`drawlib css` CLI の `slide` ターゲット対応バグ修正 & `drawlib show` 一時ファイル削除<br>・`_slide/compiler.py` の `preserve_outer_fences` 適用・進捗表示・リンク検証・Overview 見出し反映・サブディレクトリ静的画像コピー<br>・`_builder/` の SQLite キャッシュ接続再利用・フォーマット別キー分離・重複マージ処理統合・`C901` 解消<br>・`tools/dcli/code_check/docstring.py` の現行型エイリアス対応 & `release_assets/sync.py` 修正 | 中 |
| **Phase 3: `Charts` の表現力強化** | 機能追加 | `src/drawlib/_charts/`, `src/drawlib/charts/` | ・`AxisChartMixin` (`BarChart`, `LineChart`, `AreaChart`, `ScatterChart`) に `add_reference_line()` と `add_reference_band()` を追加<br>・`BarChart` の `bar_mode` に `"percent_stack"`（100%積み上げ棒グラフ）を追加<br>・`LineChart` / `AreaChart` (`CartesianChartBase`) に `value_format` パラメータを追加 | 中 |
| **Phase 4: `Lines` / `Slide` のユーティリティ強化** | 機能追加 | `src/drawlib/_core/l4_canvas/`, `src/drawlib/lines.py`, `src/drawlib/_slide/`, `src/drawlib/slide.py` | ・`drawlib.lines` に直交クランク線 `elbow_line()`（L字 / Z字・角丸 `r` 対応）を追加<br>・`line()`, `line_curved()`, `lines()`, `lines_curved()`, `elbow_line()` にインライン `text` / `text_style` ラベル描画を追加<br>・`drawlib.slide` に `draw_title_slide()`（表紙スライド描画）と `draw_slide_header()`（コンテンツスライド上部ヘッダー描画）を追加 | 中 |
| **Phase 5: テスト 1:1 ミラーリング・AI ルール (`_rules/`)・ドキュメント・リリースノート整備** | 品質・Docs | `tests/`, `src/drawlib/_rules/`, `docs/`, `README.md` | ・`test_area_chart.py` 分離・未整備アイコンテスト確認・Phase 1〜4 新機能単体テスト追加<br>・`src/drawlib/_rules/` および `README.md` の旧構文（`fold-code`, `rectangle(..., r=2)`, `fontawesome` 等）修正と新機能反映<br>・`docs/` への新機能作例追加、`release_notes.md` への `v0.3.2` セクション追加と全ビルド検証 | 低 |

---

## 2. 各フェーズの詳細仕様

### 2.1. Phase 1: ドメイン API 一貫性・座標バグ・テーマ互換性の修正

#### 1. `.draw()` 戻り値の `Self` 統一
- **対象**:
  - `src/drawlib/_charts/`: `BarChart`, `LineChart`, `AreaChart`, `PieChart`, `RadarChart`, `ScatterChart`, `GanttChart`, `HeatmapChart`, `HeatmapOverlay` の `.draw()`、および `LegendChartMixin.draw_legend()`, `HeatmapChart.draw_colorbar()`, `HeatmapOverlay.draw_colorbar()` が `Self` (`return self`) を返すように変更する。
  - `src/drawlib/_diagrams/`: `ArchitectureDiagram`, `FlowDiagram`, `ERDiagram`, `ClassDiagram`, `SequenceDiagram`, `StateDiagram` の `.draw()` が `Self` (`return self`) を返すように変更する。

#### 2. `.width` / `.height` 属性の統一
- `ClassDiagram` (`src/drawlib/_diagrams/class_diagram/_diagram.py`)、`StateDiagram` (`src/drawlib/_diagrams/state/_diagram.py`)、`HeatmapOverlay` (`src/drawlib/_charts/heatmap_chart/_overlay.py`) の `self.custom_width` / `self.custom_height` を `self.width` / `self.height` に統一する（後方互換プロパティ `custom_width` / `custom_height` を維持）。
- `PieChart` (`src/drawlib/_charts/pie_chart/_chart.py`)、`RadarChart` (`src/drawlib/_charts/radar_chart/_chart.py`) の `RadialChartMixin` に `width` / `height` プロパティを提供する。

#### 3. 座標アンカー（`align`）バグ修正と `Diagrams` 共通レイアウト処理の統合
- **`ClassDiagram` / `StateDiagram` の `align="bottom_left"` 原点ズレ修正**:
  - `align="bottom_left"` の際に `base_xy = (xy[0] - (min_x - self.margin), xy[1] - (min_y - self.margin))` となるよう補正し、描画される図面全体の左下端が確実に `xy` に一致するように修正する。
- **`Diagrams` 共通レイアウトヘルパーの抽出**:
  - `src/drawlib/_diagrams/_common.py` にバウンディングボックス集計・`align` 原点変換ヘルパーを抽出し、6つの Diagram クラスでの重複コードを解消する。
- **`GridLayout.draw_flexible()` のテキスト配置バグ修正**:
  - `src/drawlib/_smartarts/_gridlayout.py` の `draw_flexible()` で、セル矩形描画時に `item.style.patch(halign="left", valign="bottom")` によってセル内テキストまで左下寄せになる問題を修正し、`draw()` と同様にセル中心座標 `(cx, cy)` を渡して `item.style` のテキストアライメントを維持する。

#### 4. `MonochromeStyles` のトークン互換性修正 & CJK フォント継承改善
- **`src/drawlib/_preset_styles/_style_monochrome.py`**:
  - `DefaultStyles` / `GoogleStyles` に存在する `Neutral`, `PrimaryNeutral`, `SecondaryNeutral`, `AccentNeutral`, `MutedNeutral`, `DarkNeutral`, `GrayNeutral`、セマンティックトークン（`Success*`, `Warning*`, `Danger*`, `Info*`）、および `Chart1`〜`Chart6` をグレースケール階調で追加し、テーマ切り替え時の `AttributeError` を完全に防止する（`TYPE_CHECKING` アノテーションと `_build_monochrome_styles_dict` の双方に追加）。
- **`Charts` / `Diagrams` のデフォルト `text_font` 継承**:
  - `src/drawlib/_charts/_common/_style_utils.py` および `src/drawlib/_diagrams/_common.py` において、`axis_text_style` や `title_style` が省略された場合でも、`axis_line_style` や `node_style` に設定されている `text_font` を優先継承するように改善する。
- **内部モジュールの公開ファサード import 解消**:
  - `src/drawlib/_slide/helpers.py` および `src/drawlib/_smartarts/_geomap/_geomap.py` の `from drawlib.styles import ...` を内部モジュール（`drawlib._preset_colors`, `drawlib._preset_styles`）からの import に変更する。

---

### 2.2. Phase 2: 肥大化モジュール分割・Codegen・Builder・CLI・`dcli` 改善

#### 1. `_diagrams/architecture/_icons.py` (4,781行) の分割と Codegen 整理
- `src/drawlib/_diagrams/architecture/_icons.py` をカテゴリ別サブモジュール（または `_icon_enums/`）に分割し、`_icons.py` は再エクスポートと `ICON_DRAWERS` ディスパッチャに集中させる。
- `tools/dcli/codegen/cli.py` の重複した `icon-*` コマンド定義をテーブル駆動に整理し、`./dcli codegen all`（または `icon-all`）を追加する。

#### 2. `_smartarts/_mindmap.py` の重複削減
- `src/drawlib/_smartarts/_mindmap.py` (1,105行) の `_connect_and_layout_{bottom,top,right,left}` を共通ヘルパーに統合し、ボイラープレートを削減する。

#### 3. CLI / Slide コンパイラ / Builder キャッシュのバグ・設計改善
- **`src/drawlib/_cli/commands/css.py`**:
  - `drawlib css list` / `drawlib css show` が `"slide"` ターゲットを受け付けるように修正する。
- **`src/drawlib/_builder/doc_builder/processor/viewer.py`**:
  - `drawlib show`（GUIプレビュー時）が生成する一時ファイル（`tmp_path`, `grid_path`）のクリーンアップ処理を追加する。
- **`src/drawlib/_slide/compiler.py` & `_assets.py`**:
  - `_process_drawlib_blocks()` の前後に `preserve_outer_fences()` / `restore_outer_fences()` を適用し、4バッククォート内の ```` ```drawlib ```` コード例が誤実行されないようにする。
  - `build_slide` に進捗表示・リンク検証・同一スライド内の重複 `file=` 検査を追加する。
  - Overview モーダル（`O` キー）のサムネイルタイトルに各スライドの H1/H2 見出し（またはファイル名）を表示する。
  - `copy_static_assets` でサブディレクトリ内の静的画像アセットも再帰的にコピーし、favicon の MIME タイプを拡張子に応じて設定する。
  - `draw_page_number(auto_setup=False)` 呼び出し時のデフォルト `text_size` スケールを適切に調整する。
- **`src/drawlib/_builder/_common/cache.py` & `doc_builder/` & `image_builder.py`**:
  - `BuildImageCache` のフォーマット別キャッシュキー分離と、ビルド単位での SQLite コネクション再利用を実装する。
  - `doc_builder/compiler/html.py` と `doc_builder/merger.py` の重複マージ・リンク書き換え処理を共通化し、`exporter_pdf.py` の Playwright 起動処理を共通ヘルパーに統合する。
  - `image_builder.py` の `build_image()` を機能別ヘルパーに分割し、`pyproject.toml` の `_builder` に対する `C901` 除外を解消する。
  - `_core/` や `_builder/` の docstring 内に残っている `Optional[...]`, `List[...]`, `Dict[...]`, `Tuple[...]` 表記（71箇所）をモダン型表記に統一する。

#### 4. `tools/dcli/` のチェッカー・同期ツールの修正
- **`tools/dcli/code_check/docstring.py`**:
  - `TYPES_TO_CHECK` を現行の `l2_types` 型エイリアス名（`Alpha`, `Angle`, `Angle90`, `PosFloat`, `PosInt`, `Coordinate`, `Coordinates`, `FilePath`, `ExistingFilePath`, `Ratio`, `ShapeRadius` 等）に更新し、検査対象を `src/drawlib/` 全域に拡大する。
- **`tools/dcli/release_assets/sync.py`**:
  - `find_package_for_resource_path()` が全34アイコンスイートを正しく解決できるよう修正する。

---

### 2.3. Phase 3: 機能追加 A — `Charts` の表現力強化

技術ドキュメント・SREレポート・ベンチマーク比較で頻出する以下の機能を `drawlib.charts` に追加する。

#### 1. 基準線 (`add_reference_line`) とターゲット帯 (`add_reference_band`)
- **対象クラス**: `AxisChartMixin`（`BarChart`, `LineChart`, `AreaChart`, `ScatterChart` 共通）
- **API 仕様**:
  ```python
  chart.add_reference_line(
      value: float,
      *,
      label: str = "",
      axis: Literal["y", "x"] = "y",
      style: Style | None = None,
      label_style: Style | None = None,
      label_position: Literal["start", "center", "end"] = "end",
      show: bool = True,
  ) -> Self

  chart.add_reference_band(
      min_value: float,
      max_value: float,
      *,
      label: str = "",
      axis: Literal["y", "x"] = "y",
      style: Style | None = None,
      label_style: Style | None = None,
      label_position: Literal["start", "center", "end"] = "end",
      show: bool = True,
  ) -> Self
  ```
- **描画仕様**:
  - `src/drawlib/_charts/_common/_reference.py` にデータモデル（`ReferenceLine`, `ReferenceBand`）と描画関数を実装する。
  - `ReferenceBand` はプロット領域内（グリッドの上・データシリーズの背面）に半透明帯として描画し、`ReferenceLine` はデータシリーズの前面に破線（デフォルト `line_style="dashed"`）およびラベルとして描画する（プロット範囲外の値はクリップ）。
  - `BarChart` の `orientation="horizontal"` の場合は、`axis="y"` / `"x"` または数値軸方向に自動対応する。

#### 2. `BarChart` の 100% 積み上げ棒グラフ (`bar_mode="percent_stack"`)
- **対象**: `src/drawlib/_charts/_common/_types.py` (`BarMode = Literal["group", "stack", "percent_stack"]`) および `src/drawlib/_charts/bar_chart/_renderer.py`
- **仕様**:
  - `bar_mode="percent_stack"` 指定時、各カテゴリのシリーズ合計値を `100.0%` として正規化し、数値軸の範囲を `0`〜`100`（単位未指定時は `%` 表記）として縦向き・横向きの両方で描画する。

#### 3. `LineChart` / `AreaChart` の `value_format` パラメータ対応
- **対象**: `CartesianChartBase` (`src/drawlib/_charts/line_chart/_base.py`)、`LineChart`、`AreaChart`、および `_renderer.py`
- **仕様**:
  - `BarChart` と同様に `value_format: FormatterType = None`（フォーマット文字列 `"{:.1f}%"` または `Callable[[float], str]`）をコンストラクタで受け取り、`value_text_style` 指定時のデータポイント数値ラベルを整形できるようにする。

---

### 2.4. Phase 4: 機能追加 B — `Lines` / `Slide` のユーティリティ強化

#### 1. 直交クランク線 `elbow_line()` の追加 (`drawlib.lines`)
- **対象**: `src/drawlib/_core/l4_canvas/_line.py`, `_line_utils.py`, `src/drawlib/lines.py`
- **API 仕様**:
  ```python
  @validate_call
  def elbow_line(
      xy1: Coordinate,
      xy2: Coordinate,
      *,
      style: Style,
      orientation: Literal["auto", "horizontal", "vertical", "hv", "vh"] = "auto",
      mid_ratio: float = 0.5,
      r: float = 0.0,
      arrow_head: ArrowHead = "",
      text: str = "",
      text_style: Style | None = None,
  ) -> None:
  ```
- **動作仕様**:
  - `"horizontal"`（Z字水平：`xy1 -> (mid_x, y1) -> (mid_x, y2) -> xy2`）、`"vertical"`（Z字垂直：`xy1 -> (x1, mid_y) -> (x2, mid_y) -> xy2`）、`"hv"`（L字水平→垂直：`xy1 -> (x2, y1) -> xy2`）、`"vh"`（L字垂直→水平：`xy1 -> (x1, y2) -> xy2`）、`"auto"`（`|dx| >= |dy|` なら `"horizontal"`、それ以外は `"vertical"`）の頂点列を自動計算する。
  - `r > 0` の場合は `lines_curved` で角丸描画し、`r == 0` の場合は `lines` で直角描画する。

#### 2. 線プリミティブのインライン `text` / `text_style` ラベル対応 (`drawlib.lines`)
- **対象**: `line()`, `line_curved()`, `lines()`, `lines_curved()`, `elbow_line()` (`src/drawlib/_core/l4_canvas/_line.py`)
- **API 仕様**:
  - 各関数にキーワード引数 `text: str = ""` および `text_style: Style | None = None` を追加する（`shapes.rectangle(..., text="...")` と同じ使い勝手）。
- **動作仕様**:
  - `text` が非空文字列の場合、線の中点（ポリラインの場合は全セグメント長の50%地点、ベジェ曲線の場合は曲線上の `t=0.5` 地点）を算出し、`text_style`（未指定時は `style`）を用いてラベルを描画する。

#### 3. スライド表紙・標準ヘッダーヘルパー (`drawlib.slide`)
- **対象**: `src/drawlib/_slide/helpers.py`, `src/drawlib/slide.py`
- **API 仕様**:
  1. **`draw_title_slide()`**:
     ```python
     @validate_call
     def draw_title_slide(
         title: str,
         subtitle: str = "",
         *,
         author: str = "",
         date: str = "",
         badge_text: str = "",
         variant: Literal["split", "centered", "banner", "minimal"] = "split",
         show_decorations: bool = True,
         auto_setup: bool = True,
         ...
     ) -> None:
     ```
     - `draw_section_header()` の4種類のデザインバリアント（`"split"`, `"centered"`, `"banner"`, `"minimal"`）と視覚的に統一された `192 × 108` フルキャンバスの表紙（カバー）スライドを1関数で描画する。
  2. **`draw_slide_header()`**:
     ```python
     @validate_call
     def draw_slide_header(
         title: str,
         subtitle: str = "",
         *,
         section_badge: str = "",
         width: PosFloat = 192.0,
         height: PosFloat = 14.0,
         show_divider: bool = True,
         auto_setup: bool = True,
         ...
     ) -> None:
     ```
     - コンテンツスライドの上部ヘッダー領域（または `auto_setup=False` でフルキャンバススライドの上部）に、セクションピル・タイトル・サブタイトル・アクセント区切り線を統一フォーマットで描画する。

---

### 2.5. Phase 5: テスト・AI ルール (`_rules/`)・ドキュメント・リリースノート整備

1. **テスト 1:1 ミラーリング・カバレッジ強化 (`tests/`)**:
   - `tests/drawlib/charts/test_area_chart.py` を `test_line_chart.py` から分離新設する。
   - `tests/drawlib/icons/` で未整備のアイコンモジュール単体テストがあれば補完する。
   - Phase 1〜4 の全変更・新機能（`.draw()` 戻り値、`MonochromeStyles` 互換性、`add_reference_line`, `add_reference_band`, `percent_stack`, `value_format`, `elbow_line`, 線ラベル `text`, `draw_title_slide`, `draw_slide_header` 等）の単体テストを追加する。
2. **AI エージェントルール (`src/drawlib/_rules/`) と `README.md` の更新**:
   - `overview.md`, `agent_instruction.md`, `review_guide.md`, `anim_guide.md`, `cli.md`, `project_doc.md`, `project_site.md`, `lib_anim.md`, `lib_slide.md`, `README.md` に残っている旧構文（`fold-code`, `file:xxx.png`, `rectangle(..., r=2)`, `fontawesome` 等）をすべて現行仕様に修正する。
   - `api.md`, `lib_charts.md`, `lib_lines.md`, `lib_slide.md` に Phase 3・Phase 4 の新機能を追記する。
3. **公式ドキュメント (`docs/`) とリリースノート (`release_notes.md`) の更新**:
   - `docs/docs_src/05_charts/`, `02_drawing_primitives/lines.md`, `09_slides_and_presentations/` に新機能のドキュメントと図面作例を追加し、グリッド付きプレビュー（`-g`）で視覚レビューを実施する。
   - `docs/docs_src/01_getting_started/release_notes.md` に `Version 0.3.2` セクションを追加する。

---

## 3. 検証・完了基準 (Verification Checklist)

各フェーズ完了時および最終完了時に以下をすべて満たすことを確認する：

1. **静的解析スイート**:
   ```bash
   ./dcli code-check all
   ./dcli release-assets sync --check
   ```
   - Ruff lint / format、Ty 型チェック、Docstring 型エイリアス検査（`src/drawlib/` 全域）がすべてエラーゼロで通過すること。
2. **単体・統合テスト & 起動パフォーマンス維持確認**:
   ```bash
   ./dcli test all
   ```
   - 全テスト（`tests/drawlib/test_lazy_imports.py` による遅延ロード・警告ゼロ回帰テストを含む）がパスし、カバレッジおよび起動速度が維持されていること。
3. **ドキュメントビルド & 視覚検査**:
   ```bash
   ./dcli docs build --all
   ./dcli docs serve site --check
   ```
   - 全ドキュメントターゲットがエラー・リンク切れゼロでビルド完了し、新規・更新図面を `view_file` で視覚確認済みであること。
