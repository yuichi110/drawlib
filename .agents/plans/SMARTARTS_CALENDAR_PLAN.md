# Drawlib SmartArts `Calendar` 拡張計画書
(DRAWLIB SMARTARTS CALENDAR PLAN)

- **作成日**: 2026-10-12
- **対象バージョン**: Drawlib 次期マイナーリリース (`v0.3.x` / `v0.4.x`)
- **対象モジュール**:
  - `src/drawlib/_smartarts/_calendar.py` (`Calendar`, `CalendarItem` の新規実装)
  - `src/drawlib/_smartarts/__init__.py`, `src/drawlib/smartarts.py` (`Calendar`, `CalendarItem` の公開)
  - `src/drawlib/_preset_styles/` (`Styles.SmartArts.get_calendar()` プリセットスタイルの追加)
  - `src/drawlib/_rules/lib_smartarts.md`, `src/drawlib/_rules/api.md`, `src/drawlib/_rules/overview.md` (AIエージェント向けルールの更新)
  - `docs/` (公式ドキュメントおよびスライドデッキでのドッグフーディング)
  - `tests/drawlib/_smartarts/test_calendar.py` (単体テスト・バリデーション・アニメーション互換テスト)

---

## 1. 背景と目的 (Executive Summary)

プレゼンテーションや障害ポストモーテム、リリース計画、メンテナンスウィンドウの説明では、「特定の月（または特定の日）のどの日程・曜日でイベントやインシデントが発生したか」を視覚化する**カレンダー図（月間グリッドカレンダー／日めくりカレンダーカード）**が頻出する。

従来これを `Table` や基本図形（`rectangle`, `text`）の組み合わせで AI エージェントに書かせると、以下の課題が発生していた：
1. **曜日計算とセル座標計算の肥大化**: 7列×5〜6週のグリッド計算、月初・月末の空白セル処理、土日（青・赤）のテキスト色分けだけで60〜100行のボイラープレートが発生する。
2. **日付数字とイベントラベル・期間バーの衝突**: セルの左上に日付数字を置きつつ、セル中央や複数日にまたがる期間帯（例：12日〜15日の4日間連続イベント）を描画する座標計算で文字重なりが起きやすい。

これを解決するため、`drawlib.smartarts` の統一ライフサイクル（`Instantiate -> add(..., show=True) -> Mutate -> draw(..., align="bottom_left", scale=1.0)`）に完全準拠した **`Calendar`** コンポーネントを新設する。

---

## 2. コンポーネント設計仕様 (`Calendar` & `CalendarItem`)

### 2.1. 2つの表示バリアント (`variant: Literal["month", "day"] = "month"`)
1. **`variant="month"`（月間グリッドカレンダー：デフォルト）**:
   - Python 標準ライブラリの `calendar.Calendar` を内部で使用し、`year` と `month` から正確な月間グリッド（7列 × 4〜6週行）を自動構築する。
   - 最上部に月タイトル帯（例：`"October 2026"` または `"2026年 10月"`）＋オプションのリングバインダー装飾を描画し、その下に曜日ヘッダー行（`"Sun".."Sat"` または `"日".."土"`）と日付グリッドを描画する。
   - `.add(day=..., text=..., ...)` で登録された単日イベント（`day=12`）や期間イベント（`day=(12, 15)`）を該当セル上にハイライトバッジ／期間バーとして自動配置する。週をまたぐ期間イベント（例：金曜〜翌週火曜）も各週の行に自動分割して描画する。
2. **`variant="day"`（日めくりカレンダーカード）**:
   - スライド上のマイルストーン強調や KPI 横のアイコンカードとして使いやすい、上部に月名ヘッダー帯（`"OCT"` / `"10月"`）＋バインダーリング、中央に大きく日付数字（`"12"`）、下部に曜日やイベント名（`"MON / Release v1.0"`）を表示する日めくりカレンダー。

---

### 2.2. データモデル (`CalendarItem`)

他の SmartArts（[`RoadmapItem`](file:///usr/local/google/home/yuichiito/git_github/drawlib/src/drawlib/_smartarts/_roadmap.py#L29-L59), [`KpiCardItem`](file:///usr/local/google/home/yuichiito/git_github/drawlib/src/drawlib/_smartarts/_kpicards.py#L31-L60)）と同様、`add()` が返すミュータブルなアイテムモデルとして定義し、`drawlib.anim` での段階的表示（`item.show = False -> True`）やスタイル変更に完全対応する。

```python
class CalendarItem(BaseModel):
    """Mutable item model for a highlighted date or date-range event in Calendar.

    Attributes:
        day: Single day of month (1..31) or inclusive (start_day, end_day) tuple.
        text: Event label or annotation text displayed on the calendar.
        style: Style for the event highlight cell/bar or badge.
        text_style: Text style for the event label.
        day_text_style: Optional override text style for the date number itself.
        show: Whether to render this event highlight while preserving calendar grid geometry.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    day: int | tuple[int, int]
    text: str = ""
    style: Style
    text_style: Style
    day_text_style: Style | None = None
    show: bool = True
```

---

### 2.3. `Calendar` クラス API シグネチャ

```python
class Calendar:
    """SmartArt component for rendering monthly grid calendars and tear-off daily calendar cards."""

    @validate_call
    def __init__(
        self,
        year: PosInt = 2026,
        month: int = 1,
        *,
        variant: Literal["month", "day"] = "month",
        day: int | None = None,
        title: str | None = None,
        first_weekday: Literal["sun", "mon"] = "sun",
        lang: Literal["en", "ja"] = "en",
        show_rings: bool = True,
        style: Style,
        header_style: Style,
        header_text_style: Style,
        weekday_style: Style,
        weekday_text_style: Style,
        cell_style: Style,
        day_text_style: Style,
        sunday_text_style: Style | None = None,
        saturday_text_style: Style | None = None,
        event_style: Style | None = None,
        event_text_style: Style | None = None,
    ) -> None: ...

    @property
    def items(self) -> list[CalendarItem]:
        """Return registered calendar event items."""

    @validate_call
    def add(
        self,
        day: int | tuple[int, int],
        text: str = "",
        *,
        style: Style | None = None,
        text_style: Style | None = None,
        day_text_style: Style | None = None,
        show: bool = True,
    ) -> CalendarItem:
        """Register a single-day or multi-day event highlight on the calendar."""

    @validate_call
    def get_day_xy(
        self,
        day: int,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        align: Literal["bottom_left", "center", "top_left"] = "bottom_left",
        scale: PosFloat = 1.0,
    ) -> Coordinate:
        """Return the canvas center coordinate (cx, cy) of a specific day cell for external callouts/arrows."""

    @validate_call
    def draw(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        align: Literal["bottom_left", "center", "top_left"] = "bottom_left",
        scale: PosFloat = 1.0,
    ) -> Self:
        """Render the calendar onto the canvas."""
```

---

## 3. 主要機能とレイアウト詳細

1. **正確な暦計算とバリデーション**:
   - `1 <= month <= 12`、および対象年月の実在日（`1 <= day <= calendar.monthrange(year, month)[1]`）を検証し、範囲外の日付（例：2月30日）や `start_day > end_day` が指定された場合は明確な `ValueError` を送出する。
2. **土日の自動カラーリング**:
   - `sunday_text_style` / `saturday_text_style` により、日曜列は赤系、土曜列は青系、平日はダークグレー系で日付・曜日ラベルを自動色分けする（モノクロテーマ等の場合はテーマに応じたスタイルが注入される）。
3. **セル内の日付数字とイベントバーの自動レイアウト（文字重なり防止）**:
   - 各日付セルの上部（左上または中央上）に日付数字を配置し、下部領域に `.add()` で登録されたイベントピル（角丸バー＋ラベルテキスト）を配置することで、日付数字とイベント名が絶対に重ならない構造とする。
   - 期間指定 `day=(start_day, end_day)` の場合、同一週内で連続するセルの下部領域を横断する1本の連続ピルバーを描画し、バー中央に `text` を配置する。期間が週末をまたいで翌週へ続く場合は、週ごとにバーを自動分割して描画する。
4. **外部矢印・ピン連携用の座標取得メソッド (`get_day_xy(day, ...)`):**
   - [`GeoMap.get_area_xy()`](file:///usr/local/google/home/yuichiito/git_github/drawlib/src/drawlib/_smartarts/_geomap.py) と同様、特定の日付セルの中心座標 `(cx, cy)` を取得できる `get_day_xy()` を提供し、今回新設する `shapes.pin` や `lines.arrow` で特定の日付を指し示す注釈を簡単に描けるようにする。
5. **`Styles.SmartArts.get_calendar()` プリセットの提供**:
   - 他の SmartArts と同様、`Styles.SmartArts.get_calendar()` でテーマ（`default`, `google`, `monochrome`, `essentials` 等）に調和したスタイル辞書を一括取得でき、`Calendar(**Styles.SmartArts.get_calendar(), year=2026, month=10)` の1行で即座に初期化できるようにする。

---

## 4. 実装・検証ステップ

1. **プリセットスタイル追加 (`src/drawlib/_preset_styles/`)**:
   - `get_calendar()` をプリセットスタイル群に追加し、全テーマで統一されたカレンダー配色を提供する。
2. **コア実装 (`src/drawlib/_smartarts/_calendar.py`)**:
   - `CalendarItem`, `Calendar`（`variant="month"` および `"day"`、`add()`, `get_day_xy()`, `draw()`）を実装し、`drawlib.smartarts` からエクスポートする。
3. **テスト＆コードチェック**:
   - `./dcli test target smartarts` および `./dcli code-check all` を実行し、全テスト・型チェック・Ruff・docstring チェックをパスさせる。
4. **ルール＆ドキュメント更新・視覚レビュー**:
   - `src/drawlib/_rules/lib_smartarts.md` と `docs/docs_src/` に `Calendar` の使用例を追加し、`./dcli docs build site` と `view_file` で描画品質を確認する。
