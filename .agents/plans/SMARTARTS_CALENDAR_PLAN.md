# Drawlib SmartArts カレンダー（`DayCalendar` / `WeekCalendar` / `MonthCalendar`）拡張計画書
(DRAWLIB SMARTARTS CALENDAR PLAN)

- **更新日**: 2026-10-13
- **対象バージョン**: Drawlib 次期マイナーリリース (`v0.3.x` / `v0.4.x`)
- **対象モジュール**:
  - `src/drawlib/_smartarts/_calendar/` (または `_calendar.py`：`DayCalendar`, `WeekCalendar`, `MonthCalendar`, `CalendarItem` の新規実装)
  - `src/drawlib/_smartarts/__init__.py`, `src/drawlib/smartarts.py` (公開ファサードへのエクスポート)
  - `src/drawlib/_rules/lib_smartarts.md`, `src/drawlib/_rules/api.md`, `src/drawlib/_rules/overview.md` (AIエージェント向けルールの更新)
  - `docs/` (公式ドキュメントおよびスライドデッキでのドッグフーディング)
  - `tests/drawlib/_smartarts/test_calendar.py` (単体テスト・バリデーション・アニメーション互換テスト)

---

## 1. 背景と設計原則 (Executive Summary & Design Principles)

プレゼンテーションや障害ポストモーテム、リリース計画、スプリント運用、メンテナンスウィンドウの説明では、「どの日程・曜日・時間帯にどのイベントや作業枠が入るか」を視覚化する **Outlook / Google Calendar スタイルのカレンダー図** が頻出する。

これにあたり、以下の **4つの設計原則** に基づいて SmartArts カレンダー群を構築する：

1. **他の SmartArts と統一された初期化方式（専用プリセット関数の廃止）**:
   - `Styles.SmartArts.get_calendar()` のような専用プリセット取得関数は設けず、`Table` や `Roadmap`, `Panel` と同様に、`Styles.White`, `Styles.PrimaryNeutral`, `Styles.PrimaryFlat`, `Styles.Text`, `Styles.LineSubtle` などの標準スタイルトークンをコンストラクタに直接渡して初期化する。
2. **Outlook / Google Calendar スタイルの 3 クラス構成 + 指定範囲期間の統合**:
   - 時間軸を持つ **`DayCalendar`**（1日タイムグリッド）と **`WeekCalendar`**（週間・任意N日間タイムグリッド）、および7曜グリッドを持つ **`MonthCalendar`**（月間・任意N週間グリッド）の3クラスを提供する。
   - 「指定範囲期間」については別クラスを乱立させず、以下の2軸で自然に吸収する：
     - **時間軸つきの任意日数範囲（例：平日5日間、3日間カンファレンス、障害発生前後4日間）** → `WeekCalendar(num_days=5)` 等で表現。
     - **月をまたぐ複数週の期間範囲（例：10/19〜11/8 の3週間スプリント）** → `MonthCalendar(year=2026, month=10, start_day=19, num_weeks=3)` で表現。
3. **「Python標準の閏年対応・実在カレンダー自動計算」と「自由テンプレート入力」のハイブリッド設計**:
   - **実在カレンダーモード**: `year` と `month`（および `day`）を指定すると、Python 標準の `calendar` / `datetime` モジュールにより、閏年（例：2024年2月29日）や大小の月（28/29/30/31日）、月またぎ・年またぎの日付と曜日を100%正確に自動計算する。これにより AI エージェントの曜日ハルシネーションを完全に防止する。
   - **自由・テンプレートモード**: 特定の年に縛られない概念図（例：「毎月1日が月曜から始まる30日間の定例運用サイクル図」や「具体的な日付なしの Mon〜Fri 週間ルーチン表」「Day 1〜Day 3 の相対日程表」）を描きたい場合は、`year` / `month` を省略して `num_days` / `start_weekday` やカスタム列ラベル `columns=["Mon", "Tue", ...]` を直接指定できる。
4. **`GanttChart` とは異なる「日時・期間をまたぐ枠（Spanning Frame / Window Box）」の表現**:
   - `MonthCalendar` では複数日を横断する帯枠（週末での次週行への自動折り返し・複数イベント重なり時の縦レーン自動段積み）を描画する。
   - `DayCalendar` / `WeekCalendar` では、単一日の時間帯ブロックだけでなく、**「複数日カラム × 時間帯をガバッと1つの大きな枠で囲む領域枠（例：月〜金の 13:00〜17:00 コアタイム枠、水〜木の 09:00〜18:00 コードフリーズ枠）」** や **「上部の終日（All-Day）帯での複数日横断バナー」** をサポートする。

---

## 2. コンポーネント一覧と役割分担

| クラス名 | カレンダー種別（軸構造） | 主な用途・特徴 |
| :--- | :--- | :--- |
| **`DayCalendar`** | **1日タイムグリッド**<br>（縦軸：`start_hour`〜`end_hour`、横軸：1日列＋上部終日枠） | 1日のタイムテーブル、分刻み/時間刻みの障害タイムライン、イベント当日のアジェンダ、メンテナンス作業手順の時間枠。同時間帯の並列イベントや時間またぎブロックに対応。 |
| **`WeekCalendar`** | **週間・N日間タイムグリッド**<br>（縦軸：`start_hour`〜`end_hour`、横軸：デフォルト7日列／`num_days=5` 平日／任意N日列＋上部終日帯） | 1週間（または平日5日間・3日間等）のスケジュール、オンコールシフト表、**複数日×時間帯を横断する作業ウィンドウ枠（コアタイム・コードフリーズ枠）**、上部終日帯の日またぎバナー。 |
| **`MonthCalendar`** | **月間・N週間デイトグリッド**<br>（横軸：7曜日列、縦軸：4〜6週行 または `num_weeks` 行） | 月間リリース計画、マイルストーンカレンダー、月をまたぐ2〜3週間スプリント計画。**日をまたぐ連続イベント枠（週またぎの自動折り返し＆自動レーン段積み）**に対応。 |

---

## 3. 共通スタイル初期化パターン & データモデル (`CalendarItem`)

### 3.1. 共通コンストラクタ・スタイル引数（`Styles.SmartArts.get_calendar()` 不使用）
既存の [`Table`](file:///usr/local/google/home/yuichiito/git_github/drawlib/src/drawlib/_smartarts/_table.py) や [`Roadmap`](file:///usr/local/google/home/yuichiito/git_github/drawlib/src/drawlib/_smartarts/_roadmap.py) と一貫した以下の基本スタイル引数を受け取る：

- **必須スタイル引数（5個）**:
  - `cell_style: Style`: 日付セル・時間スロットの基本背景スタイル（例：`Styles.White`, `Styles.Neutral`）
  - `text_style: Style`: 日付数字・時刻軸ラベルの基本テキストスタイル（例：`Styles.Text`）
  - `header_style: Style`: 曜日ヘッダー・上部タイトル帯の背景スタイル（例：`Styles.PrimaryNeutral`, `Styles.PrimaryFlat`）
  - `header_text_style: Style`: 曜日ヘッダー・上部タイトル帯のテキストスタイル（例：`Styles.PrimaryBold`, `Styles.WhiteBold`）
  - `border_style: Style`: グリッド罫線のスタイル（例：`Styles.LineSubtle`）
- **オプションスタイル引数（デフォルト `None`）**:
  - `event_style: Style | None = None`: `.add()` 時に `style` を省略した際のデフォルトイベント枠スタイル（未指定時は `Styles.PrimaryFlat` 相当または `header_style` から自動導出）
  - `event_text_style: Style | None = None`: `.add()` 時のデフォルトイベント文字スタイル
  - `sunday_text_style: Style | None = None`: 日曜列の曜日・日付文字スタイル（指定時のみ色分け、未指定時は `text_style` / `header_text_style`）
  - `saturday_text_style: Style | None = None`: 土曜列の曜日・日付文字スタイル（指定時のみ色分け）
  - `title_style: Style | None = None`: 最上部の月名・タイトルバーの背景スタイル（未指定時は `header_style` を使用）
  - `title_text_style: Style | None = None`: 最上部の月名・タイトルバーの文字スタイル（未指定時は `header_text_style` を使用）

### 3.2. ミュータブル・アイテムモデル (`CalendarItem`)
すべてのカレンダーの `.add(...)` メソッドは `CalendarItem` インスタンスを返し、`drawlib.anim` での段階的表示（`item.show = False -> True`）やスタイル変更に完全対応する。

```python
class CalendarItem(BaseModel):
    """Mutable item model for an event block or spanning window on a Calendar.

    Attributes:
        text: Primary event title or label displayed inside the frame.
        description: Optional secondary subtitle or time/detail note.
        days: Target day or inclusive (start_day, end_day) span.
        hours: Optional (start_hour, end_hour) time span for DayCalendar / WeekCalendar.
            When None on WeekCalendar, renders as an all-day banner in the top band.
        style: Style for the event box/banner container.
        text_style: Text style for the primary event label.
        description_style: Optional text style for the secondary description.
        show: Whether to render this event while preserving calendar grid geometry.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    text: str = ""
    description: str = ""
    days: int | tuple[int, int] = 1
    hours: tuple[float, float] | None = None
    style: Style
    text_style: Style
    description_style: Style | None = None
    show: bool = True
```

---

## 4. 各クラスの詳細仕様

### 4.1. `MonthCalendar`（月間・複数週グリッドカレンダー）

#### シグネチャ
```python
class MonthCalendar:
    """SmartArt component for rendering Outlook/Google-style monthly or multi-week grid calendars."""

    @validate_call
    def __init__(
        self,
        *,
        year: PosInt | None = None,
        month: int | None = None,
        start_day: PosInt = 1,
        num_weeks: PosInt | None = None,
        num_days: PosInt = 30,
        start_weekday: Literal["sun", "mon", "tue", "wed", "thu", "fri", "sat"] = "sun",
        first_weekday: Literal["sun", "mon"] = "sun",
        title: str | None = None,
        lang: Literal["en", "ja"] = "en",
        max_tracks: PosInt = 3,
        cell_style: Style,
        text_style: Style,
        header_style: Style,
        header_text_style: Style,
        border_style: Style,
        event_style: Style | None = None,
        event_text_style: Style | None = None,
        sunday_text_style: Style | None = None,
        saturday_text_style: Style | None = None,
        title_style: Style | None = None,
        title_text_style: Style | None = None,
    ) -> None: ...

    @validate_call
    def add(
        self,
        days: int | tuple[int, int],
        text: str = "",
        *,
        description: str = "",
        style: Style | None = None,
        text_style: Style | None = None,
        description_style: Style | None = None,
        show: bool = True,
    ) -> CalendarItem:
        """Register a single-day or multi-day spanning event bar on the month calendar."""

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
        """Return the canvas center coordinate (cx, cy) of a specific day cell."""

    @validate_call
    def draw(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        align: Literal["bottom_left", "center", "top_left"] = "bottom_left",
        scale: PosFloat = 1.0,
    ) -> Self: ...
```

#### 主な挙動
1. **実在カレンダーモード (`year` & `month` 指定時)**:
   - `calendar.monthrange(year, month)` を使用し、対象年月の正確な開始曜日と日数（閏年の2月29日含む）を算出する。
   - **指定範囲期間（月またぎの複数週表示）**: `start_day=19, num_weeks=3` のように指定された場合、`datetime.date(year, month, start_day)` を含む週の先頭から `num_weeks` 週間分のグリッドを生成する（翌月にまたがる日付も `11/1`, `2`, `3`... として連続表示可能）。
2. **自由テンプレートモード (`year=None` 時)**:
   - 現実の暦を無視し、`first_weekday`（左端の曜日：`"sun"` または `"mon"`）に対して `start_weekday` から `1` 日が始まり、`num_days`（デフォルト30日）まで続く汎用カレンダーを描画する。
3. **日をまたぐ連続枠と自動レーン割り当て**:
   - `days=12`（単日）または `days=(12, 20)`（複数日期間）を受け取る。
   - 期間が週（行）をまたぐ場合は、各週の行ごとにバーを自動分割して描画する。
   - 同一日に複数の期間バーが重なる場合は、各週行内で空きトラック（`0 .. max_tracks - 1`）をグリーディに割り当て、日付数字の下に重ならず段積み配置する。

---

### 4.2. `WeekCalendar`（週間・指定N日間タイムグリッドカレンダー）

#### シグネチャ
```python
class WeekCalendar:
    """SmartArt component for rendering multi-day time-grid calendars (7-day week, 5-day workweek, or custom N-day range)."""

    @validate_call
    def __init__(
        self,
        *,
        year: PosInt | None = None,
        month: int | None = None,
        day: PosInt = 1,
        num_days: PosInt = 7,
        columns: list[str] | None = None,
        first_weekday: Literal["sun", "mon"] = "sun",
        start_hour: float = 9.0,
        end_hour: float = 18.0,
        hour_step: PosFloat = 1.0,
        show_all_day: bool = True,
        title: str | None = None,
        lang: Literal["en", "ja"] = "en",
        cell_style: Style,
        text_style: Style,
        header_style: Style,
        header_text_style: Style,
        border_style: Style,
        event_style: Style | None = None,
        event_text_style: Style | None = None,
        sunday_text_style: Style | None = None,
        saturday_text_style: Style | None = None,
        title_style: Style | None = None,
        title_text_style: Style | None = None,
    ) -> None: ...

    @validate_call
    def add(
        self,
        days: int | tuple[int, int],
        hours: tuple[float, float] | None = None,
        text: str = "",
        *,
        description: str = "",
        style: Style | None = None,
        text_style: Style | None = None,
        description_style: Style | None = None,
        show: bool = True,
    ) -> CalendarItem:
        """Register a time-slot block, multi-day time window box, or all-day banner.

        Args:
            days: Column index (0..num_days-1, or matching day-of-month when year/month is set),
                or inclusive (start_day, end_day) span across multiple columns.
            hours: (start_hour, end_hour) time range on the vertical axis (e.g. (10.0, 12.0)).
                If None, the event is rendered in the top all-day / multi-day banner strip.
            text: Primary event title.
            description: Optional secondary subtitle text.
            style: Optional override style for the event frame.
            text_style: Optional override text style for the title.
            description_style: Optional override text style for the description.
            show: Whether to render this item.
        """

    @validate_call
    def get_slot_xy(
        self,
        day: int,
        hour: float,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        align: Literal["bottom_left", "center", "top_left"] = "bottom_left",
        scale: PosFloat = 1.0,
    ) -> Coordinate:
        """Return the canvas coordinate (cx, cy) for a specific (day, hour) slot."""

    @validate_call
    def draw(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        align: Literal["bottom_left", "center", "top_left"] = "bottom_left",
        scale: PosFloat = 1.0,
    ) -> Self: ...
```

#### 主な挙動
1. **カラム構成（実在日付モード vs 自由テンプレートモード）**:
   - `columns=["Mon", "Tue", "Wed", "Thu", "Fri"]` が指定された場合は、その文字列リストをそのまま列ヘッダーとして使用する（自由ラベルモード）。
   - `year, month, day` が指定された場合は、`datetime.date(year, month, day)` から `num_days` 日間（デフォルト7日間、平日のみなら `num_days=5`、3日間イベントなら `num_days=3`）の実在日付と曜日を `timedelta(days=i)` で自動計算する（閏年の2/29や月末の月またぎも自動処理）。
   - いずれも未指定（`year=None, columns=None`）の場合は、`first_weekday` から始まる `num_days` 分の曜日名（`"Sun", "Mon", ...` または `"日", "月", ...`）のみをヘッダーに表示する。
2. **3種類の「日時をまたぐ枠」の表現**:
   - **① 単日×時間帯ブロック (`days=13, hours=(10.0, 12.0)`)**: 対象日の列の `10:00`〜`12:00` を覆う角丸カード枠を描画。
   - **② 複数日×時間帯を横断する領域枠 / Span Window (`days=(12, 16), hours=(13.0, 17.0)`)**: 12日〜16日の複数カラムかつ `13:00`〜`17:00` の時間帯を **1つの大きな角丸矩形枠** で横断的に囲む（「月〜金の午後は集中開発・マイグレーション期間」「火〜木の終日コードフリーズ」などを視覚化）。
   - **③ 上部 All-Day 帯の期間バナー (`days=(12, 15), hours=None`)**: タイムグリッド上部の終日（All-Day）エリアに、複数日を貫く横長バナー枠を描画。

---

### 4.3. `DayCalendar`（1日タイムグリッドカレンダー）

#### シグネチャ
```python
class DayCalendar:
    """SmartArt component for rendering a single-day hourly schedule or incident timeline."""

    @validate_call
    def __init__(
        self,
        *,
        year: PosInt | None = None,
        month: int | None = None,
        day: PosInt | None = None,
        title: str | None = None,
        start_hour: float = 9.0,
        end_hour: float = 18.0,
        hour_step: PosFloat = 1.0,
        show_all_day: bool = False,
        lang: Literal["en", "ja"] = "en",
        cell_style: Style,
        text_style: Style,
        header_style: Style,
        header_text_style: Style,
        border_style: Style,
        event_style: Style | None = None,
        event_text_style: Style | None = None,
        title_style: Style | None = None,
        title_text_style: Style | None = None,
    ) -> None: ...

    @validate_call
    def add(
        self,
        hours: tuple[float, float] | None = None,
        text: str = "",
        *,
        description: str = "",
        style: Style | None = None,
        text_style: Style | None = None,
        description_style: Style | None = None,
        show: bool = True,
    ) -> CalendarItem:
        """Register a time-range block (or all-day banner when hours=None) on the day schedule."""

    @validate_call
    def get_hour_xy(
        self,
        hour: float,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        align: Literal["bottom_left", "center", "top_left"] = "bottom_left",
        scale: PosFloat = 1.0,
    ) -> Coordinate:
        """Return the canvas center coordinate (cx, cy) at a specific hour on the day schedule."""

    @validate_call
    def draw(
        self,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        align: Literal["bottom_left", "center", "top_left"] = "bottom_left",
        scale: PosFloat = 1.0,
    ) -> Self: ...
```

#### 主な挙動
- 左側に時刻軸ラベル（`09:00`, `10:00`, ...）、右側にイベント領域を配置した Outlook / Google Calendar の「1日表示」を描画する。
- `year, month, day` を指定した場合は正確な日付と曜日（例：`2026-10-13 (Tue)`）をヘッダーに表示し、省略時は `title`（例：`"Release Day Runbook"`）のみを表示する。
- 時間帯が重なる複数のイベントが登録された場合（例：`10:00〜12:00` と `11:00〜13:00`）、Google Calendar と同様に横幅を自動分割（並列カラム配置）して重ならずに描画する。

---

## 5. 実装・検証ステップ

1. **コア実装 (`src/drawlib/_smartarts/_calendar.py`)**:
   - `CalendarItem`, `MonthCalendar`, `WeekCalendar`, `DayCalendar` を実装し、`src/drawlib/_smartarts/__init__.py` および `src/drawlib/smartarts.py` からエクスポートする。
2. **単体テスト (`tests/drawlib/_smartarts/test_calendar.py`)**:
   - 実在カレンダーモード（閏年 `2024-02-29`、月またぎの複数週表示含む）と自由テンプレートモードの双方のテスト。
   - 日またぎ・週またぎ枠、複数日×時間帯の横断枠（Span Window）、同時間帯イベントの並列配置、`item.show = False`（アニメーション互換）、`scale`、異常値バリデーションのテストを作成し、`./dcli test target smartarts` をパスさせる。
3. **静的解析 (`./dcli code-check all`)**:
   - Ruff lint/format、Ty 型チェック、docstring チェックを完全パスさせる。
4. **ルール＆ドキュメント更新・視覚レビュー**:
   - `src/drawlib/_rules/lib_smartarts.md`, `src/drawlib/_rules/api.md`, `src/drawlib/_rules/overview.md` および `docs/docs_src/` に使用例を追加し、`./dcli docs build site` と `view_file`（および `drawlib show -g`）で視覚品質を確認する。
