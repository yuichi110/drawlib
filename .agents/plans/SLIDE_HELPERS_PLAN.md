# Drawlib Slide ステージヘルパー拡張計画書 (`drawlib.slide`)
(DRAWLIB SLIDE HELPERS EXPANSION PLAN — REVISED v2)

- **作成日**: 2026-10-10（2026-10-11 SmartArts 拡充およびセクションヘッダー複数パターン対応に伴い改訂）
- **対象バージョン**: Drawlib 次期マイナーリリース (`v0.3.x` / `v0.4.x`)
- **関連計画書**: [`.agents/plans/SMARTARTS_EXPANSION_PLAN.md`](file:///usr/local/google/home/yuichiito/git_github/drawlib/.agents/plans/SMARTARTS_EXPANSION_PLAN.md)（実装完了：`KpiCards`, `CardList`, `Roadmap`, `Panel`）
- **対象モジュール**:
  - `src/drawlib/slide.py` (公開ファサード: `draw_page_number`, `draw_section_header` をエクスポート)
  - `src/drawlib/_slide/helpers.py` (新規: スライド専用ステージ・ページ描画ヘルパーの実装)
  - `src/drawlib/_templates/_project.py` & `src/drawlib/_templates/project/slide/` (重複していた `utils/*.py.template` 3ファイル約1,600行の整理と `Roadmap` / `drawlib.slide` への移行)
  - `src/drawlib/_rules/lib_slide.md`, `project_slide.md`, `slide_guide.md`, `api.md` (AIエージェント向けルールの更新)
  - `docs/` (`slide_about_drawlib_src/`, `slide_ddos_incident_response_src/`, `docs_src/` のドッグフーディング更新)
  - `tests/drawlib/slide/` (単体テストの追加・更新)

---

## 1. 改訂の背景と基本方針 (Background & Core Decisions)

### 1.1. これまでの合意事項まとめ
1. **`drawlib.slide` に収録する関数を2つに厳選（スリム案）**:
   - **`draw_page_number()`**: スライド右下のページ番号（`current_slide.text` / `format`）を透過背景（`14×3`, `alpha=0.0`）で描画。
   - **`draw_section_header()`**: 16:9 フルブリード（`192×108`）のセクションヘッダーページ（`01_section.md`）を一括描画。
   - ※アジェンダ曲線・KPIカード・フェーズ進行バー・コールアウト枠などの汎用図解は、実装済みの `drawlib.smartarts`（`Roadmap`, `KpiCards`, `CardList`, `ChevronProcess`, `Panel`）に統一し、`drawlib.slide` には重複実装しない。
2. **命名は一般的なスライド用語である `| パターン名 (`variant`) | 視覚構造・特徴 (`192.0 × 108.0` キャンバス) | `topics` 指定時の描画方法 | 最適なユースケース |
| :--- | :--- | :--- | :--- |
| **`"split"`**<br>*(デフォルト・左右分割型)* | 左パネル (`w=72`, `DarkFlat`) に大きなセクション番号 (`01`) と進行ドット、境界に `PrimaryFlat` 縦バー、右パネル (`w=120`, `Neutral`) にタイトル・サブタイトルを配置。 | 右パネル下半分の領域に **`CardList(direction="vertical", badge_shape="circle")`** でトピックカードを縦積み描画（未指定時は右パネル上下中央にタイトルを配置）。 | 章ごとに3〜5個の具体的なトピックを予告したい長編・技術解説デッキ。 |
| **`"centered"`**<br>*(中央集中・キーノート型)* | 全面ニュートラル背景（＋上端アクセントバー・コーナー装飾）の中央に、パートバッジピル・大見出し `title`・`subtitle` を堂々と中央揃え配置。 | 下段領域に **`CardList(direction="horizontal", badge_shape="circle")`** でトピックカードを横一列に整列（未指定時は画面ど真ん中にタイトル群を大きく配置）。 | カンファレンス登壇（Keynote 風）、エグゼクティブサマリー、トピック一覧なしのシンプルな場面転換。 |
| **`"banner"`**<br>*(ワイド横断バンド型)* | 画面上〜中段を横断するワイドな `DarkFlat` の帯の中に角丸 `PrimaryFlat` 番号ボックスと白抜き大見出し `title`・`subtitle` を配置し、下半分を明るいワークスペースにする。 | 下半分の広い領域（`w=164`）に **`CardList(direction="horizontal", badge_shape="rounded_rect", show_arrows=False)`** でトピックカードを横並び（矢印なし）で展開。 | 章内の複数トピックやサブテーマをワイドに横並びで見せたいとき。 |
| **`"minimal"`**<br>*(左アクセント・エディトリアル型)* | ベタ塗りダークパネルを使わず、全面クリーンな `Neutral` 背景の左端に `PrimaryFlat` アクセントピルと `"SECTION 01"` バッジを配し、左揃えでモダンに構成。 | タイトル下部の領域に **`CardList(direction="vertical", badge_shape="rounded_rect")`** をワイドに配置。 | 設計書・RFC 風のクリーンなスライドや、**`MonochromeStyles`・PDF 印刷時**に大面積の黒ベタ塗りを避けたいとき。 |

### 2.2. 全パターン共通のスマート挙動・デフォルトスタイル
1. **`topics` の有無による自動レイアウト調整**:
   - `topics` が渡された場合：タイトル・サブタイトルを上段に寄せ、下段（または右パネル下段）に `CardList` を配置。
   - `topics` が空 `()` の場合：タイトル・サブタイトル・セクション番号のグループを垂直方向の中央付近へ自動シフトし、余白が間延びしない引き締まった扉ページにする。
2. **`topics` 要素の柔軟な型サポート**:
   - `Sequence[str | tuple[str, str]]` を受け付け、`["トピックA", "トピックB"]` のような1行文字列リストだけでなく、`[("トピックA", "補足説明..."), ("トピックB", "補足説明...")]` のような2段カードもそのまま `CardList` で描画できる。
3. **控えめで洗練されたカード枠線・区切り線**:
   - トピックカードのデフォルトスタイル（`topic_card_style`）には `Styles.White.patch(shape_line_color=Colors.Gray3, shape_line_width=0.9)` を用い、水平区切り線（`line_style`）には `Styles.Neutral.patch(line_color=Colors.Gray3, line_width=1.0)` を用いることで、重苦しい黒枠にならずモダンなUIカードとして描画する。
4. **`total_sections` の任意化 (`total_sections: int = 0`)**:
   - `total_sections > 0` のときは進行インジケータードット（`1..total_sections`）と `"Part {section_num} of {total_sections}"` バッジを自動描画。
   - `total_sections == 0`（デフォルト）のときは進行ドットを省略し、全体の章数を数えなくても `draw_section_header(1, "Introduction")` の最小引数だけで呼び出せる。��トピックを予告したい長編・技術解説デッキ。 |
| **`"centered"`**<br>*(中央集中・キーノート型)* | 全面ニュートラル背景（＋控えめな上下アクセントライン／コーナー装飾）の中央に、パートバッジ・大きなセクション番号・大見出し `title`・`subtitle` を堂々と中央揃え配置。 | 下段領域に **`CardList(direction="horizontal", badge_shape="rounded_rect")`** でトピックカードを横一列に整列（未指定時は画面ど真ん中にタイトル群を大きく配置）。 | カンファレンス登壇（Keynote 風）、エグゼクティブサマリー、トピック一覧なしのシンプルな場面転換。 |
| **`"banner"`**<br>*(ワイド横断バンド型)* | 画面上〜中段を横断するワイドな `PrimaryFlat`（または `DarkFlat`）の帯の中に番号バッジと白抜き大見出し `title`・`subtitle` を配置し、下半分を明るいワークスペースにする。 | 下半分の広い領域（`w=168`）に **`CardList(direction="horizontal", show_arrows=True)`** または縦スタックでトピックを大きく展開。 | 章内のストーリーの流れ（Step 1 → Step 2 → Step 3）をワイドに見せたいとき。 |
| **`"minimal"`**<br>*(左アクセント・エディトリアル型)* | ベタ塗りダークパネルを使わず、全面クリーンな `Neutral` / `White` 背景の左端に太い `PrimaryFlat` アクセントピルと大きな `"SECTION 01"` タイポグラフィを配し、左揃えでモダンに構成。 | タイトル下部の領域に **`CardList(direction="vertical", badge_shape="rounded_rect")`** をワイドに配置。 | 設計書・RFC 風のクリーンなスライドや、**`MonochromeStyles`・PDF 印刷時**に大面積の黒ベタ塗りを避けたいとき。 |

### 2.2. 全パターン共通のスマート挙動
1. **`topics` の有無による自動レイアウト調整**:
   - `topics` が渡された場合：タイトル・サブタイトルを上段に寄せ、下段（または右パネル下段）に `CardList` を配置。
   - `topics` が空 `()` の場合：タイトル・サブタイトル・セクション番号のグループを垂直方向の中央付近へ自動シフトし、余白が間延びしない引き締まった扉ページにする。
2. **`topics` 要素の柔軟な型サポート**:
   - `Sequence[str | tuple[str, str]]` を受け付け、`["トピックA", "トピックB"]` のような1行文字列リストだけでなく、`[("トピックA", "補足説明..."), ("トピックB", "補足説明...")]` のような2段カードもそのまま `CardList` で描画できる。
3. **`total_sections` の任意化 (`total_sections: int = 0`)**:
   - `total_sections > 0` のときは進行インジケータードット（`1..total_sections`）と `"Part {section_num} of {total_sections}"` バッジを自動描画。
   - `total_sections == 0`（デフォルト）のときは進行ドットを省略し、全体の章数を数えなくても `draw_section_header(1, "Introduction")` の最小引数だけで呼び出せる。

---

## 3. 各ヘルパー関数の詳細 API 設計 (`src/drawlib/_slide/helpers.py`)

### 3.1. `draw_page_number`
スライド右下のページカウンター（`::: block xy=(1700, 1010) width=140 height=30` 向け）を描画する関数。

```python
@validate_call
def draw_page_number(
    width: PosFloat = 14.0,
    height: PosFloat = 3.0,
    *,
    template: str = "{index} / {total}",
    style: Style | None = None,
    auto_setup: bool = True,
) -> None:
    """Draw a standardized slide page number badge using current_slide.

    Args:
        width: Canvas width in coordinate units. Defaults to 14.0.
        height: Canvas height in coordinate units. Defaults to 3.0.
        template: Format string with `{index}` and `{total}` placeholders.
            Defaults to "{index} / {total}".
        style: Text style for the page counter. Defaults to `Styles.Muted.patch(text_size=65.0)`.
        auto_setup: Whether to call `clear()` and `setup(width=width, height=height, alpha=0.0)`
            automatically before drawing. Defaults to True.
    """
```

---

### 3.2. `draw_section_header`
16:9 フルブリード（`::: block xy=(0, 0) width=1920 height=1080` 向け、`192.0 × 108.0` キャンバス）のセクションヘッダーページを一括描画する関数。

```python
@validate_call
def draw_section_header(  # noqa: PLR0913
    section_num: PosInt,
    title: str,
    subtitle: str = "",
    topics: Sequence[str | tuple[str, str]] = (),
    total_sections: int = 0,
    *,
    variant: Literal["split", "centered", "banner", "minimal"] = "split",
    section_label: str = "SECTION",
    badge_text: str | None = None,
    show_page_number: bool = True,
    show_decorations: bool = True,
    auto_setup: bool = True,
    left_panel_style: Style | None = None,
    right_panel_style: Style | None = None,
    divider_bar_style: Style | None = None,
    decoration_style: Style | None = None,
    section_label_style: Style | None = None,
    section_num_style: Style | None = None,
    active_dot_style: Style | None = None,
    completed_dot_style: Style | None = None,
    upcoming_dot_style: Style | None = None,
    badge_style: Style | None = None,
    badge_text_style: Style | None = None,
    title_style: Style | None = None,
    subtitle_style: Style | None = None,
    line_style: Style | None = None,
    topic_card_style: Style | None = None,
    topic_text_style: Style | None = None,
    topic_description_style: Style | None = None,
    topic_badge_style: Style | None = None,
    topic_badge_text_style: Style | None = None,
    page_number_style: Style | None = None,
) -> None:
    """Draw a full-bleed 16:9 section header slide (192.0 x 108.0 canvas)."""
```

---

## 4. テンプレートおよび既存スライドの整理計画

### 4.1. スライド用 `utils.py` テンプレートの重複解消
- [`src/drawlib/_templates/project/slide/utils/`](file:///usr/local/google/home/yuichiito/git_github/drawlib/src/drawlib/_templates/project/slide/utils/default.py.template) にある `default.py.template`, `google.py.template`, `monochrome.py.template`（約536行×3ファイル＝1,600行超）を削除し、`_shared/utils.py` に統一する。
- [`src/drawlib/_templates/_project.py`](file:///usr/local/google/home/yuichiito/git_github/drawlib/src/drawlib/_templates/_project.py) の `_validate_slide_style` / `_deploy_slide_utils` を廃止し、`default-dark`, `google-dark`, `github`, `minimal` 等の全 CSS テーマで `drawlib init slide -s <theme>` が動作するようにする。
- スターターテンプレートの `02_agenda.md`（`en` / `ja`）は、`drawlib.smartarts.Roadmap` と `drawlib.slide.draw_page_number` を使うコードに更新する。

### 4.2. ドッグフーディング・スライドデッキの更新
- `docs/slide_about_drawlib_src/` および `docs/slide_ddos_incident_response_src/` において：
  - `01_section.md` を `from drawlib.slide import draw_section_header` に移行。
  - 各スライドのページ番号を `from drawlib.slide import draw_page_number` に移行。
  - アジェンダスライドの `draw_curved_agenda` を `Roadmap` に移行。
  - KPI スライドの `draw_kpi_cards` を `KpiCards` に移行。
  - 両プロジェクトの `utils.py` から約450行の重複コードを削除しスリム化する。

---

## 5. 実装・検証ステップ (Implementation Roadmap)

1. **Step 1: `src/drawlib/_slide/helpers.py` の実装と公開エクスポート**
   - `draw_page_number` および複数パターン対応の `draw_section_header` を実装し、`src/drawlib/_slide/__init__.py` と `src/drawlib/slide.py` からエクスポートする。
2. **Step 2: テンプレート (`_templates/`) の刷新**
   - `src/drawlib/_templates/project/slide/utils/` の重複3ファイルを廃止し、`_project.py` と `slide/docs/{en,ja}/` を更新する。
3. **Step 3: 単体テストの追加・更新 (`tests/drawlib/slide/`)**
   - `draw_page_number` と `draw_section_header`（各 `variant`・オプション）の単体テストを追加し、`test_slide.py` を更新する。
   - `./dcli code-check all` および `./dcli test target slide`、`./dcli test target cli` をパスさせる。
4. **Step 4: ルール・ドキュメント・ドッグフーディングスライドの更新と視覚レビュー**
   - `src/drawlib/_rules/` (`lib_slide.md`, `project_slide.md`, `slide_guide.md`, `api.md`) および `docs/docs_src/08_doc_builder_and_cli/slide_layout_and_api.md` を更新する。
   - `docs/slide_about_drawlib_src/` と `docs/slide_ddos_incident_response_src/` を更新してビルド・視覚レビューを行う。
