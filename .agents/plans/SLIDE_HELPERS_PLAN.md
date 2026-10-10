# Drawlib Slide ステージヘルパー拡張計画書 (`drawlib.slide`)
(DRAWLIB SLIDE HELPERS EXPANSION PLAN)

- **作成日**: 2026-10-10
- **対象バージョン**: Drawlib 次期マイナーリリース (`v0.3.x` / `v0.4.x`)
- **関連計画書**: [`.agents/plans/SMARTARTS_EXPANSION_PLAN.md`](file:///usr/local/google/home/yuichiito/git_github/drawlib/.agents/plans/SMARTARTS_EXPANSION_PLAN.md)（汎用図解コンポーネント `KpiCards`, `CardList`, `Roadmap` の `drawlib.smartarts` 拡張計画）
- **対象モジュール**:
  - `src/drawlib/slide.py` (公開ファサード: スライド描画ヘルパー関数群をエクスポート)
  - `src/drawlib/_slide/helpers.py` (新規: スライド専用ステージ描画ヘルパーの実装)
  - `src/drawlib/_templates/project/slide/utils/` (`default.py.template`, `google.py.template`, `monochrome.py.template` の重複解消とスリム化)
  - `src/drawlib/_rules/lib_slide.md`, `project_slide.md`, `slide_guide.md`, `api.md` (AIエージェント向けルールの更新)
  - `tests/drawlib/slide/` (単体テストの追加)

---

## 1. エグゼクティブサマリー & 背景 (Executive Summary & Background)

### 1.1. 現状の課題
現在、`drawlib.slide` モジュール（`src/drawlib/slide.py`）にはランタイム状態管理とビルド関数（`current_slide`, `SlideContext`, `BoundingBox`, `build_slide`）のみが定義されており、**スライド固有の描画ヘルパー関数は1つも含まれていない**。

その代わり、`drawlib init slide` 実行時に生成されるテンプレート [`src/drawlib/_templates/project/slide/utils/`](file:///usr/local/google/home/yuichiito/git_github/drawlib/src/drawlib/_templates/project/slide/utils/default.py.template)（`default.py.template`, `google.py.template`, `monochrome.py.template`）に、約536行×3ファイル（計1,600行超）のスライド描画コードがハードコードされて各プロジェクトの `utils.py` にコピーされている。これには以下の問題がある。

1. **3つのテンプレートファイル間の大規模なコード重複（1,600行超）**:
   - `default.py.template`, `google.py.template`, `monochrome.py.template` の違いは先頭の4色パレット定数（`_DEFAULT_PALETTE`, `_GOOGLE_PALETTE`, `_MONOCHROME_PALETTE`）と左パネルの背景色のみで、残りの約520行の座標計算・描画ロジックは完全に同一である。
   - 本来、テーマカラーは `styles.py` の `Styles`（`Styles.Primary`, `Styles.Secondary`, `Styles.Accent`, `Styles.Highlight`, `Styles.Neutral` 等）から動的に取得できるため、ライブラリ関数化すれば3ファイルに分ける必要自体がなくなる。
2. **ユーザーの `utils.py` が初期状態で500行超になり見通しが悪い**:
   - 本来プロジェクト固有のヘルパーを書くための `utils.py` が、最初から536行のテンプレートコードで埋め尽くされており、ユーザーがどこを触るべきか分かりにくい。
3. **実戦スライドで頻出するステージ演出パターンの未収録**:
   - `docs/slide_about_drawlib_src/` や `docs/slide_ddos_incident_response_src/` の作成を通じて、既存の `draw_page_number` / `draw_chapter_divider` / `draw_curved_agenda` に加え、**「複数スライドにまたがる上部フェーズ／Wave進行バー (`draw_phase_bar`)」** や **「スライド下部の1行結論コールアウトバー (`draw_takeaway_banner`)」** が技術プレゼンで非常に高い頻度で使われることが判明した。

### 1.2. 解決方針：`drawlib.slide` へのスライド専用ヘルパー集約
- **スライド固有のステージ演出・ページ構成ヘルパー**を `drawlib.slide`（内部実装 `src/drawlib/_slide/helpers.py`）に公式関数として収録する。
- 既存の `Styles` プリセット（`Styles.Primary`, `Styles.Secondary`, `Styles.Accent`, `Styles.Highlight` 等）からカラーパレットを自動解決する仕組みにすることで、`styles.py` のテーマ切り替えに完全連動させる。
- スライドプロジェクトの `utils.py` テンプレートは、`drawlib.slide`（および `drawlib.smartarts`）への薄い委譲ラッパー（後方互換用）＋ユーザー向けサンプルのみの数十行のクリーンなファイルへと劇的にスリム化する。

---

## 2. `drawlib.slide` に追加するヘルパー関数一覧

| 関数名 | 種別 | 役割 | キャンバス初期化 (`clear` + `setup`) |
| :--- | :---: | :--- | :---: |
| **`draw_page_number()`** | 既存昇格 | スライド右下のページ番号 (`current_slide.text`) を透過背景で描画 | 自動実行 (`auto_setup=True`) |
| **`draw_chapter_divider()`** | 既存昇格 | 16:9 フルブリード (`192×108`) の章扉スライド（左パネル・章番号・進行ドット・右トピック一覧・右下ページ番号）を一括描画 | 自動実行 (`auto_setup=True`) |
| **`draw_curved_agenda()`** | 既存昇格 | アジェンダスライド用のベジェ曲線＋番号バッジ＋ピル型トピック一覧を描画 | 任意 (`auto_setup=False` 既定) |
| **`draw_phase_bar()`** | **新規** | 連続スライド（Wave 1〜4 や Step 1〜5）の上部に配置する横長フェーズ進行インジケーターバーを描画 | 任意 (`auto_setup=False` 既定) |
| **`draw_takeaway_banner()`** | **新規** | スライド下部に配置する Key Takeaway / 結論サマリーバー（アクセントピルまたはアイコン＋太字メッセージ）を描画 | 任意 (`auto_setup=False` 既定) |

*(※従来 `utils.py` にあった `draw_kpi_cards` は、スライド以外のドキュメントでも汎用的に使えるため [`SMARTARTS_EXPANSION_PLAN.md`](file:///usr/local/google/home/yuichiito/git_github/drawlib/.agents/plans/SMARTARTS_EXPANSION_PLAN.md) の `drawlib.smartarts.KpiCards` として実装し、`drawlib.slide` または `utils.py` からはそのラッパーとして呼び出す。)*

---

## 3. 各ヘルパー関数の詳細 API 設計 (`src/drawlib/_slide/helpers.py`)

### 3.1. テーマパレット自動解決ヘルパー (`_resolve_slide_palette`)
ハードコードされた `_DEFAULT_PALETTE` 等を廃止し、現在アクティブな `Styles` から4色のアクセントパレットを動的に抽出する：
```python
def _resolve_slide_palette(
    colors: Sequence[tuple[int, int, int]] | None = None,
) -> list[tuple[int, int, int]]:
    """Resolve 4-color slide accent palette from explicit colors or active Styles."""
    if colors:
        return list(colors)
    return [
        Styles.PrimaryFlat.shape_fill_color[:3],
        Styles.SecondaryFlat.shape_fill_color[:3],
        Styles.AccentFlat.shape_fill_color[:3],
        Styles.HighlightFlat.shape_fill_color[:3],
    ]
```
これにより、`styles.py` が `default` / `google` / `monochrome` のどれであっても、自動的にそのテーマのカラートークンで描画される。

---

### 3.2. `draw_page_number`
スライド右下のページカウンター（`::: block (1700, 1010) (140, 30)` 向け）を1行で描画する関数。

```python
@validate_call
def draw_page_number(
    width: float = 14.0,
    height: float = 3.0,
    *,
    template: str = "{index} / {total}",
    style: Style | None = None,
    auto_setup: bool = True,
) -> None:
    """Draw a standardized slide page number badge using current_slide."""
```
- **動作仕様**:
  - `auto_setup=True`（デフォルト）のとき、`clear()` および `setup(width=width, height=height, alpha=0.0)` を自動実行し、中央 `(width / 2, height / 2)` に `current_slide.format(template)` を描画する。
  - スライド Markdown 内では `from drawlib.slide import draw_page_number; draw_page_number()` の2行だけで完結する（`save()` は `build_slide` が自動補完）。

---

### 3.3. `draw_chapter_divider`
16:9 フルブリード（`::: block (0, 0) (1920, 1080)` 向け、`192.0 × 108.0` キャンバス）の章扉スライドを一括描画する関数。

```python
@validate_call
def draw_chapter_divider(
    chapter_num: int,
    title: str,
    subtitle: str = "",
    topics: Sequence[str] = (),
    total_chapters: int = 4,
    *,
    chapter_label: str = "CHAPTER",
    part_label_template: str = "Part {chapter_num} of {total_chapters}",
    accent_color: tuple[int, int, int] | None = None,
    show_page_number: bool = True,
    auto_setup: bool = True,
) -> None:
    """Draw a full-bleed 16:9 chapter divider slide (192.0 x 108.0 canvas)."""
```
- **改善ポイント**:
  - `chapter_label`（例：`"CHAPTER"`, `"ACT"`, `"PHASE"`）や `part_label_template` をカスタマイズ可能にし、今回の DDoS スライド（`"ACT 02"` 等）でも関数をフォークせずにそのまま使えるようにする。
  - 右パネルの `topics` 一覧描画は、`SMARTARTS_EXPANSION_PLAN.md` の `CardList` を内部利用してクリーンに描画する。

---

### 3.4. `draw_curved_agenda`
アジェンダページ向けに、左側のベジェ曲線アークに沿って番号バッジとピル型カードを配置する関数。

```python
@validate_call
def draw_curved_agenda(
    items: Sequence[str | tuple[str, str]],
    width: float = 104.0,
    height: float = 86.0,
    *,
    xy: tuple[float, float] = (0.0, 0.0),
    accent_bar: bool = True,
    colors: Sequence[tuple[int, int, int]] | None = None,
    active_index: int | None = None,
) -> None:
    """Draw a curved agenda diagram with numbered badges and pill containers."""
```
- **改善ポイント**:
  - **`active_index: int | None = None`（1-based）の追加**: 指定された章番号のみをハイライト表示し、他の項目を薄いグレー（dimmed）で描画するオプションを追加する。これにより、プレゼン途中の「現在地ハイライト付きアジェンダスライド」も1引数で表現可能になる。

---

### 3.5. `draw_phase_bar` *(新規)*
今回の DDoS スライドの GeoMap 4連続スライド（Wave 1: China → Wave 2: Asia → Wave 3: World → Wave 4: Japan）で大活躍した、**スライド上部の横長ステップ／フェーズ進行バー**を1関数で描画するヘルパー。

```python
@validate_call
def draw_phase_bar(
    phases: Sequence[str | tuple[str, str]],
    active_phase: int,
    *,
    xy: tuple[float, float] = (2.0, 74.0),
    width: float = 172.0,
    height: float = 8.0,
    active_style: Style | None = None,
    completed_style: Style | None = None,
    upcoming_style: Style | None = None,
    show_connectors: bool = True,
) -> None:
    """Draw a horizontal multi-slide phase/wave progress bar highlighting the active step.

    Args:
        phases: Sequence of phase titles or (badge_label, title) tuples.
        active_phase: 1-based index of the currently active phase on this slide.
        xy: Bottom-left coordinate (x0, y0) of the phase bar.
        width: Total width of the phase bar.
        height: Height of the phase bar.
        active_style: Style for the active phase pill (defaults to Styles.AccentFlat or PrimaryFlat).
        completed_style: Style for already completed phases (defaults to Styles.PrimaryNeutral).
        upcoming_style: Style for future phases (defaults to dimmed Styles.Neutral).
        show_connectors: Whether to draw connecting arrows ('->') between phase pills.
    """
```
- **ユースケース**:
  - 複数枚のスライドにまたがって1つのストーリー（Wave 1〜4、Step 1〜5、Before / During / After）を展開する際、聴衆に「今どの段階を見ているか」を一目で伝える上部ナビゲーションバーとして利用する。

---

### 3.6. `draw_takeaway_banner` *(新規)*
技術スライドの最下部（例：`y = 2.0〜10.0`）に配置する **Key Takeaway / 結論コールアウトバー** を描画するヘルパー。

```python
@validate_call
def draw_takeaway_banner(
    title: str,
    subtitle: str = "",
    *,
    xy: tuple[float, float] = (2.0, 2.0),
    width: float = 172.0,
    height: float = 9.5,
    badge_label: str = "KEY TAKEAWAY",
    icon: Callable[..., None] | None = None,
    style: Style | None = None,
    accent_style: Style | None = None,
) -> None:
    """Draw a full-width bottom takeaway/conclusion callout banner on a slide."""
```
- **動作仕様**:
  - 左端にアクセントピル＋バッジラベル（例：`"KEY TAKEAWAY"`, `"INSIGHT"`, `"RESULT"`）または Phosphor アイコンを配置し、中央〜右側に太字の `title` と補足 `subtitle` を高コントラストで描画する。

---

## 4. スライドテンプレート (`_templates/project/slide/utils/`) のスリム化計画

上記のヘルパーを `drawlib.slide`（および `KpiCards` を `drawlib.smartarts`）に収録した後、[`src/drawlib/_templates/project/slide/utils/`](file:///usr/local/google/home/yuichiito/git_github/drawlib/src/drawlib/_templates/project/slide/utils/default.py.template) の3ファイル（計1,600行）は以下のように約40行の薄いモジュールに統一できる：

```python
"""Slide drawing utilities and project-specific presentation helpers."""

from __future__ import annotations

from drawlib.slide import (
    draw_chapter_divider,
    draw_curved_agenda,
    draw_page_number,
    draw_phase_bar,
    draw_takeaway_banner,
)

__all__ = [
    "draw_chapter_divider",
    "draw_curved_agenda",
    "draw_page_number",
    "draw_phase_bar",
    "draw_takeaway_banner",
]
```
- 既存のサンプルスライドやプロジェクトで `utils.draw_page_number()` や `utils.draw_chapter_divider()` を呼んでいるコードも**100%後方互換でそのまま動作**しつつ、新規スライドでは `from drawlib.slide import draw_page_number` と直接インポートすることも可能になる。

---

## 5. 実装フェーズと検証計画 (Implementation & Verification Roadmap)

1. **Phase 1: `src/drawlib/_slide/helpers.py` の実装とエクスポート**:
   - `draw_page_number`, `draw_chapter_divider`, `draw_curved_agenda`, `draw_phase_bar`, `draw_takeaway_banner` を実装し、`src/drawlib/_slide/__init__.py` と `src/drawlib/slide.py` から公開する。
2. **Phase 2: 単体テストの追加**:
   - `tests/drawlib/slide/test_helpers.py` を作成し、`SlideContext` 下での `draw_page_number` 動作、各テーマスタイル下での `draw_chapter_divider` / `draw_curved_agenda` / `draw_phase_bar` / `draw_takeaway_banner` の描画を検証する。
3. **Phase 3: スライドテンプレートと内部ルールの更新**:
   - `src/drawlib/_templates/project/slide/utils/` の重複コードを `drawlib.slide` 委譲に置き換える。
   - `src/drawlib/_rules/lib_slide.md` および `slide_guide.md` に新ヘルパー関数の使い方を追記する。
4. **Phase 4: ドッグフーディング検証**:
   - `./dcli docs build slide` を実行し、既存スライドデッキが視覚的退行なくビルドされることを確認する。
