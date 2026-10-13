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

これにあたり、以下の **5つの設計原則** に基づいて SmartArts カレンダー群を構築する：

1. **他の SmartArts と統一された初期化方式（専用プリセット関数の廃止）**:
   - `Styles.SmartArts.get_calendar()` のような専用プリセット取得関数は設けず、`Table` や `Roadmap`, `Panel` と同様に、`Styles.White`, `Styles.PrimaryNeutral`, `Styles.PrimaryFlat`, `Styles.Text`, `Styles.LineSubtle` などの標準スタイルトークンをコンストラクタに直接渡して初期化する。
2. **Outlook / Google Calendar スタイルの 3 クラス構成 + 指定範囲期間の統合**:
   - 時間軸を持つ **`DayCalendar`**（1日タイムグリッド）と **`WeekCalendar`**（週間・任意N日間タイムグリッド）、および7曜グリッドを持つ **`MonthCalendar`**（月間・月またぎ範囲グリッド）の3クラスを提供する。
   - 「指定範囲期間」については別クラスを乱立させず、以下の2軸で自然に吸収する：
     - **時間軸つきの任意日数範囲（例：平日5日間、3日間カンファレンス、障害発生前後4日間）** → `WeekCalendar(start_date="2026-10-12", end_date="2026-10-16")`（または `num_days=5`）で表現。
     - **月をまたぐ複数週の期間範囲（例：10/19〜11/08 の3週間スプリント）** → `MonthCalendar(start_date="2026-10-19", end_date="2026-11-08")` で表現。
3. **AI が最も扱いやすい厳格な ISO フォーマット（`"YYYY-MM-DD"` / `"YYYY-MM-DD HH:MM"` の2種のみ）への限定**:
   - `days` と `hours` を別引数に分けると「10日の 09:00 から 13日の 15:00 まで」のような日時またぎの指定が煩雑になり、AI の引数ミスも誘発する。
   - そのため、日時指定はスラッシュ区切りや省略表記を排除し、以下の **2フォーマットのみに厳格化** する：
     1. **`"YYYY-MM-DD"`**（例：`"2026-10-10"`）→ 時刻なし＝自動的に **「全日（All-Day）」イベント** として扱う。
     2. **`"YYYY-MM-DD HH:MM"`**（例：`"2026-10-10 09:00"`）→ 時刻あり＝ **「時間枠（Timed）」イベント**（日またぎ連続時間対応）として扱う。
   - Python 標準の `datetime` により閏年（例：`2024-02-29`）や月末・曜日も100%正確に自動計算し、それ以外のフォーマット文字列が渡された場合は明確な `ValueError` を送出する。
4. **`DayCalendar` の縦長 (`"vertical"`) ＆ 横長 (`"horizontal"`) 両対応**:
   - `DayCalendar` は通常の縦長タイムグリッド（`direction="vertical"`：上から下へ時間経過）だけでなく、16:9 ワイドスライドやページ上部の Hero 図で使いやすい **横長タイムライン（`direction="horizontal"`：左から右へ時間経過）** にも対応する。
5. **Google Calendar 方式の「全日（All-Day）」フィールドと、日時をまたぐ枠のスマートな表現**:
   - `WeekCalendar`（および `DayCalendar`）では、曜日ヘッダーの直下・時間枠グリッドの上に **「全日（All-Day）」フィールド** を設ける。
   - `"2026-10-12"` 〜 `"2026-10-14"`（月〜水）のような全日・複数日イベントは、この「全日」フィールド内に **X軸方向の横断バー** として配置され（重なり時は縦レーン自動段積み）、下部の時間枠グリッドと一切衝突しない。
   - `"2026-10-10 09:00"` 〜 `"2026-10-13 15:00"` のように時刻つきで複数日にまたがる場合は、10日の `09:00〜下端`、11日・12日の `終日枠`、13日の `上端〜15:00` へと各日カラムを連続して埋める枠（または複数日カラムを横断する単一ボックス `span_mode="box"`）として表現できる。

---

## 2. コンポーネント一覧と役割分担

| クラス名 | カレンダー種別（軸構造） | 主な用途・特徴 |
| :--- | :--- | :--- |
| **`DayCalendar`** | **1日タイムグリッド**<br>・`direction="vertical"`（縦軸＝時間）<br>・`direction="horizontal"`（横軸＝時間）<br>＋「全日」フィールド | 1日のタイムテーブル、分刻み/時間刻みの障害タイムライン、イベント当日のアジェンダ。縦長配置と 16:9 スライド向けの横長配置の両方に対応し、重複時間帯は自動で並列レーン分割。 |
| **`WeekCalendar`** | **週間・N日間タイムグリッド**<br>（上部：**全日フィールド**、縦軸：`start_hour`〜`end_hour`、横軸：デフォルト7日列／平日5日列／任意期間列） | 1週間（または平日5日間・3日間等）のスケジュール、オンコールシフト表。**上部の「全日（All-Day）」フィールドで「月〜水」などの複数日期間を X軸横断バーとして表現**し、下部の時間グリッドで単日・日またぎの時間枠予定を表現。 |
| **`MonthCalendar`** | **月間・複数週デイトグリッド**<br>（横軸：7曜日列、縦軸：対象月または `start_date`〜`end_date` の週行） | 月間リリース計画、マイルストーンカレンダー、月をまたぐ2〜3週間スプリント計画。**日をまたぐ連続イベント枠（週またぎの自動折り返し＆自動レーン段積み）**に対応。 |

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

### 3.2. サポートする ISO 日付・日時文字列フォーマット（2種のみ）
日付・日時の指定は以下の **2つのフォーマットのみ** を受け付ける（スラッシュ区切り `"YYYY/MM/DD"` や時刻のみ `"HH:MM"` は不可とし、バリデーションエラーとする）：
1. **`"YYYY-MM-DD"`**（例：`"2026-10-10"`）：日付のみ（全日イベント、およびカレンダーの `date` / `start_date` / `end_date` 指定に使用）
2. **`"YYYY-MM-DD HH:MM"`**（例：`"2026-10-10 09:00"`）：日付＋24時間表記の時刻（時間指定イベントに使用）

### 3.3. ミュータブル・アイテムモデル (`CalendarItem`)
すべてのカレンダーの `.add(...)` メソッドは `CalendarItem` インスタンスを返し、`drawlib.anim` での段階的表示（`item.show = False -> True`）やスタイル変更に完全対応する。

```python
class CalendarItem(BaseModel):
    """Mutable item model for an event block or all-day spanning bar on a Calendar.

    Attributes:
        start: Start date ("YYYY-MM-DD") or datetime ("YYYY-MM-DD HH:MM").
        end: Optional end date ("YYYY-MM-DD") or datetime ("YYYY-MM-DD HH:MM").
            Defaults to start when None for single-day all-day events.
        text: Primary event title or label displayed inside the frame.
        description: Optional secondary subtitle or time/detail note.
        all_day: Optional explicit override to force rendering in the All-Day ("全日") field.
            When None, inferred automatically (True if start/end are "YYYY-MM-DD", False if "YYYY-MM-DD HH:MM").
        span_mode: How multi-day timed events ("2026-10-10 09:00" to "2026-10-13 15:00") are rendered in WeekCalendar:
            - "columns" (default): Fills 10th (09:00..end_hour), 11th-12th (start_hour..end_hour), 13th (start_hour..15:00).
            - "box": Draws a single unified rectangle spanning across columns 10th..13th and hours 09:00..15:00.
            - "all_day": Renders as an X-axis bar in the top All-Day field.
        style: Style for the event box/banner container.
        text_style: Text style for the primary event label.
        description_style: Optional text style for the secondary description.
        show: Whether to render this event while preserving calendar grid geometry.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    start: str
    end: str | None = None
    text: str = ""
    description: str = ""
    all_day: bool | None = None
    span_mode: Literal["columns", "box", "all_day"] = "columns"
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
        start_date: str = "2026-10-01",
        end_date: str | None = None,
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
        start: str,
        end: str | None = None,
        text: str = "",
        *,
        description: str = "",
        style: Style | None = None,
        text_style: Style | None = None,
        description_style: Style | None = None,
        show: bool = True,
    ) -> CalendarItem:
        """Register a single-day or multi-day spanning event bar on the month calendar.

        Examples:
            cal.add("2026-10-12", text="Release v1.0")
            cal.add("2026-10-14", "2026-10-20", text="DB Migration Phase")
        """

    @validate_call
    def get_date_xy(
        self,
        date: str,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        align: Literal["bottom_left", "center", "top_left"] = "bottom_left",
        scale: PosFloat = 1.0,
    ) -> Coordinate:
        """Return the canvas center coordinate (cx, cy) of a specific date cell ('YYYY-MM-DD')."""

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
1. **1ヶ月表示 (`start_date="2026-10-01", end_date=None`) と 任意期間表示 (`start_date="2026-10-19", end_date="2026-11-08"`)**:
   - `end_date=None` の場合は、`start_date` が属する年月（例：2026年10月）の1日〜末日（閏年2月は29日）の4〜6週グリッドを自動構築する。
   - `end_date`（`"YYYY-MM-DD"`）が指定された場合は、`start_date` を含む週の先頭（日曜または月曜）から `end_date` を含む週の末尾までの複数週グリッド（月またぎ・年またぎ対応）をシームレスに構築する。
2. **日をまたぐ連続枠と自動レーン割り当て**:
   - `cal.add("2026-10-10", "2026-10-13", text="...")`（時刻つき `"2026-10-10 09:00"` が渡された場合も日付部分を抽出して同様に描画可能）。
   - 期間が週（行）をまたぐ場合は、各週の行ごとにバーを自動分割して折り返し描画する。
   - 同一日に複数の期間バーが重なる場合は、各週行内で空きトラック（`0 .. max_tracks - 1`）をグリーディに割り当て、日付数字の下に重ならず段積み配置する。

---

### 4.2. `WeekCalendar`（週間・指定期間タイムグリッドカレンダー）

#### シグネチャ
```python
class WeekCalendar:
    """SmartArt component for rendering multi-day time-grid calendars (7-day week, 5-day workweek, or custom date range)."""

    @validate_call
    def __init__(
        self,
        *,
        start_date: str = "2026-10-11",
        end_date: str | None = None,
        num_days: PosInt = 7,
        columns: list[str] | None = None,
        start_hour: int = 9,
        end_hour: int = 18,
        hour_step: PosInt = 1,
        show_all_day: bool | None = None,
        all_day_label: str | None = None,
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
        start: str,
        end: str | None = None,
        text: str = "",
        *,
        description: str = "",
        all_day: bool | None = None,
        span_mode: Literal["columns", "box", "all_day"] = "columns",
        style: Style | None = None,
        text_style: Style | None = None,
        description_style: Style | None = None,
        show: bool = True,
    ) -> CalendarItem:
        """Register an all-day X-axis bar or a timed event on the week calendar.

        Examples:
            # 1. All-Day / Multi-Day X-axis bar in the top "全日" field ("YYYY-MM-DD"):
            cal.add("2026-10-12", "2026-10-14", text="DB Migration (Mon-Wed)")

            # 2. Single-day timed block in the hourly grid ("YYYY-MM-DD HH:MM"):
            cal.add("2026-10-12 10:00", "2026-10-12 12:00", text="Kickoff")

            # 3. Multi-day continuous timed span ("10日の9:00 から 13日の15:00 まで"):
            cal.add("2026-10-10 09:00", "2026-10-13 15:00", text="Continuous Load Test")
        """

    @validate_call
    def get_slot_xy(
        self,
        dt: str,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        align: Literal["bottom_left", "center", "top_left"] = "bottom_left",
        scale: PosFloat = 1.0,
    ) -> Coordinate:
        """Return the canvas coordinate (cx, cy) for 'YYYY-MM-DD' (all-day cell) or 'YYYY-MM-DD HH:MM' (time slot)."""

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
1. **期間指定 (`start_date` + `end_date` または `num_days`)**:
   - `start_date="2026-10-12", end_date="2026-10-16"`（または `start_date="2026-10-12", num_days=5`）のように、7日間の週表示・5日間の稼働日表示・3日間のイベント期間表示を自在に構成できる（`columns=["Mon", "Tue", ...]` によるカスタムヘッダー上書きも可能）。
2. **表示時間帯 (`start_hour: int = 9, end_hour: int = 18, hour_step: PosInt = 1`)**:
   - 24時間表記の整数（`0 <= start_hour < end_hour <= 24`）で表示時間帯を指定する。デフォルトは一般的なビジネスアワーの `9`（`09:00`）〜 `18`（`18:00`）、1時間刻み（`hour_step=1`）。
   - 24時間フル表示や夜間メンテナンスの場合は `start_hour=0, end_hour=24, hour_step=2` 等を指定することで時刻ラベルが詰まらず描画できる。
3. **上部「全日（All-Day）」フィールドの表示制御 (`show_all_day: bool | None = None`)**:
   - **`None`（デフォルト：自動表示／非表示）**: 登録された全日イベントが0件なら「All-day」行を消して時間グリッドを広く使い、1件以上 `.add()` されていれば必要な段数（レーン数）で自動表示する。
   - **`drawlib.anim` レイアウト保持**: 自動判定およびレーン段数の計算は `item.show=False` のアイテムも含めた全登録アイテム基準で行うため、アニメーション中に `item.show` を切り替えても「All-day」欄の出現・高さ変化による時間グリッドの位置ズレが起きない。
   - **`True`（常時表示）**: 全日イベントが0件でも空の「All-day」行（1段分）を表示する。
   - **`False`（常時非表示）**: 「All-day」行を描画しない。
4. **イベントの自動振り分けと日時またぎ表現**:
   - **時刻なし (`"2026-10-12"` 〜 `"2026-10-14"`) または `all_day=True`**:
     - 曜日ヘッダー直下の **「全日（All-Day）」フィールド** に、月〜水を X軸方向に横断する角丸バーとして描画する（複数バーが重なる場合は自動で縦レーン段積み＆「全日」フィールド高さを自動拡張）。
   - **時刻あり・単日 (`"2026-10-12 10:00"` 〜 `"2026-10-12 12:00"`)**:
     - 12日のカラムの `10:00`〜`12:00` に縦方向の予定ブロックを描画（同時間帯の重複予定は横幅を自動分割）。
   - **時刻あり・複数日またぎ (`"2026-10-10 09:00"` 〜 `"2026-10-13 15:00"`)**:
     - `span_mode="columns"`（デフォルト）: 各日の `[start_hour, end_hour]` に自動クリッピングし、10日の `09:00〜下端`、11日・12日の `上端〜下端`、13日の `上端〜15:00` にそれぞれ予定枠を連続描画する。
     - `span_mode="box"`: 10日〜13日のカラム × `09:00`〜`15:00` の時間帯を1つの大きな横断矩形枠（コアタイム枠や共通ウィンドウ枠）として囲む。
     - `span_mode="all_day"`: 上部の「全日」フィールドに `10/10 09:00 - 10/13 15:00` の X軸横断バーとして描画する。

---

### 4.3. `DayCalendar`（1日タイムグリッドカレンダー：縦長 `"vertical"` ＆ 横長 `"horizontal"` 対応）

#### シグネチャ
```python
class DayCalendar:
    """SmartArt component for rendering a single-day schedule in vertical or horizontal orientation."""

    @validate_call
    def __init__(
        self,
        *,
        date: str = "2026-10-13",
        direction: Literal["vertical", "horizontal"] = "vertical",
        start_hour: int = 9,
        end_hour: int = 18,
        hour_step: PosInt = 1,
        show_all_day: bool | None = None,
        all_day_label: str | None = None,
        title: str | None = None,
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
        start: str,
        end: str | None = None,
        text: str = "",
        *,
        description: str = "",
        all_day: bool | None = None,
        style: Style | None = None,
        text_style: Style | None = None,
        description_style: Style | None = None,
        show: bool = True,
    ) -> CalendarItem:
        """Register a time-range block ("YYYY-MM-DD HH:MM") or all-day banner ("YYYY-MM-DD") on the day schedule.

        Examples:
            cal.add("2026-10-13 09:00", "2026-10-13 10:30", text="Morning Triage")
            cal.add("2026-10-13 13:00", "2026-10-13 15:30", text="Release Deployment")
            cal.add("2026-10-13", text="Change Freeze Day")
        """

    @validate_call
    def get_time_xy(
        self,
        dt: str,
        xy: Coordinate,
        width: PosFloat,
        height: PosFloat,
        *,
        align: Literal["bottom_left", "center", "top_left"] = "bottom_left",
        scale: PosFloat = 1.0,
    ) -> Coordinate:
        """Return the canvas center coordinate (cx, cy) at a specific datetime ('YYYY-MM-DD HH:MM') or all-day ('YYYY-MM-DD')."""

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
1. **縦長 (`direction="vertical"`) と 横長 (`direction="horizontal"`) の切り替え**:
   - **`direction="vertical"`（デフォルト）**: 左側に時刻ラベル列（`09:00`, `10:00`...）、右側にイベント領域を配置し、上から下へ時間が流れる標準の1日カレンダー。重複する時間帯のイベントは左右の並列カラムに自動分割される。
   - **`direction="horizontal"`（横長）**: 上部に時刻ヘッダー行（`09:00`, `10:00`...）、下部にイベント領域を配置し、左から右へ時間が流れるワイドな1日タイムテーブル。重複する時間帯のイベントは上下の並列レーンに自動分割されるため、16:9 スライドやドキュメント上部の横長 Hero 図に最適。
2. **表示時間帯 (`start_hour: int = 9, end_hour: int = 18, hour_step: PosInt = 1`) と `show_all_day: bool | None = None`**:
   - `WeekCalendar` と同一の仕様（`0 <= start_hour < end_hour <= 24`、`show_all_day=None` で全日イベントがあるときのみ自動表示、または `True` / `False` で明示指定）。
3. **厳格な ISO フォーマット（`"YYYY-MM-DD"` / `"YYYY-MM-DD HH:MM"`）**:
   - `WeekCalendar` / `MonthCalendar` と完全に同一の2フォーマット（`"2026-10-13"` または `"2026-10-13 09:00"`）で統一する。

---

## 5. 実装・検証ステップ

1. **コア実装 (`src/drawlib/_smartarts/_calendar.py` または `_calendar/` パッケージ)**:
   - 厳格な ISO 日付・日時パーサー（`"YYYY-MM-DD"` および `"YYYY-MM-DD HH:MM"` の2種のみ許容）、`CalendarItem`, `MonthCalendar`, `WeekCalendar`, `DayCalendar` を実装し、`src/drawlib/_smartarts/__init__.py` および `src/drawlib/smartarts.py` からエクスポートする。
2. **単体テスト (`tests/drawlib/_smartarts/test_calendar.py`)**:
   - 2つの ISO フォーマット文字列（`"YYYY-MM-DD"`, `"YYYY-MM-DD HH:MM"`、閏年 `"2024-02-29"`）のパースと、不正フォーマット（スラッシュ区切り等）や不正時間帯（`start_hour >= end_hour`）に対する `ValueError` バリデーション。
   - `MonthCalendar` の月またぎ範囲・週折り返し連続バー・縦レーン自動段積み。
   - `WeekCalendar` の `show_all_day=None / True / False` 制御、上部「全日（All-Day）」X軸横断バー、および日時またぎ（`"2026-10-10 09:00"` 〜 `"2026-10-13 15:00"`）の3モード（`"columns"`, `"box"`, `"all_day"`）。
   - `DayCalendar` の `direction="vertical"` / `"horizontal"` 両レイアウトと重複時間帯の並列分割。
   - `item.show = False`（アニメーション互換：All-Day 欄のレイアウト保持含む）、`scale`、座標取得メソッド（`get_date_xy`, `get_slot_xy`, `get_time_xy`）のテストを作成し、`./dcli test target smartarts` をパスさせる。
3. **静的解析 (`./dcli code-check all`)**:
   - Ruff lint/format、Ty 型チェック、docstring チェックを完全パスさせる。
4. **ルール＆ドキュメント更新・視覚レビュー**:
   - `src/drawlib/_rules/lib_smartarts.md`, `src/drawlib/_rules/api.md`, `src/drawlib/_rules/overview.md` および `docs/docs_src/` に使用例を追加し、`./dcli docs build site` と `view_file`（および `drawlib show -g`）で視覚品質を確認する。
