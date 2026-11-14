::: block xy=(1700, 1008) width=140 height=32
```drawlib file=page.svg
import utils
utils.draw_page_number()
```
:::

::: block xy=(80, 1010) width=900 height=30 font_size=15px
*Drawlib — コードで描く図解と技術ドキュメント*
:::

::: block xy=(80, 36) width=1760 height=72
# GanttChart によるプロジェクト工程管理
:::

::: block xy=(80, 130) width=1760 height=110
- **宣言的なスケジュール定義**: `Section` による工程分割、`Task(progress=...)` の進捗バー、`Milestone` をコードで一元管理。
- **依存関係と基準日マーカー**: タスク間の直交 `Dependency` 矢印や、`Today`・`Release` などの垂直 `Marker` を自動描画。
:::

::: block xy=(80, 255) width=1760 height=690
```drawlib file=gantt_release_plan_ja.svg
from drawlib.canvas import clear, save, setup
from drawlib.charts.gantt import GanttChart
from drawlib.styles import Colors, Styles

clear()
setup(width=176, height=69)

chart = GanttChart(
    columns=["1月 (M1)", "2月 (M2)", "3月 (M3)", "4月 (M4)", "5月 (M5)", "6月 (M6)"],
    axis_line_style=Styles.MutedDashed,
    axis_text_style=Styles.Dark.patch(text_size=12.5),
    grid_style=Styles.MutedThin,
    header_style=Styles.SecondaryNeutral,
    zebra_style=Styles.NeutralFlat,
    background_style=Styles.White.patch(shape_r=2.0, shape_line_color=Colors.Gray4),
    progress_text_style=Styles.WhiteBold.patch(text_size=12.0),
    width=172.0,
    label_width=46.0,
    header_height=6.2,
    row_height=4.8,
    bar_radius=1.0,
)

chart.add_section("1. Architecture (設計)", style=Styles.PrimaryNeutral, text_style=Styles.DarkBold.patch(text_size=12.5))
t1 = chart.add_task("キャンバス・テーマ仕様策定", start=0.0, end=1.3, style=Styles.PrimaryFlat, progress=1.0)
t2 = chart.add_task("SmartArts・Charts API 設計", start=1.0, end=2.5, style=Styles.PrimaryFlat, progress=1.0)
chart.add_milestone("アーキテクチャ凍結", at=2.5, style=Styles.PrimaryFlat)

chart.add_section("2. Implementation (実装)", style=Styles.PrimaryNeutral, text_style=Styles.DarkBold.patch(text_size=12.5))
t3 = chart.add_task(
    "ダイアグラム・自動配置エンジン",
    start=2.2,
    end=3.8,
    style=Styles.PrimaryFlat,
    progress=0.80,
)
t4 = chart.add_task(
    "HTML / PDF / PPTX ビルダ実装",
    start=2.9,
    end=4.5,
    style=Styles.SecondaryFlat,
    progress=0.55,
)

chart.add_section("3. Verification & Launch (検証・公開)", style=Styles.PrimaryNeutral, text_style=Styles.DarkBold.patch(text_size=12.5))
t5 = chart.add_task(
    "AI ルール・グリッド検証 CLI",
    start=4.1,
    end=5.4,
    style=Styles.SecondaryFlat,
    progress=0.35,
)
t6 = chart.add_task("日英ドキュメント・ショーケース", start=4.9, end=5.9, style=Styles.PrimaryNeutral, progress=0.0)
chart.add_milestone("v1.0 正式リリース", at=5.9, style=Styles.AccentFlat)

chart.add_dependency(t1, t2)
chart.add_dependency(t2, t3)
chart.add_dependency(t3, t5)

chart.add_marker(
    at=3.92,
    style=Styles.AccentBold.patch(line_style="dashed"),
    label="Today",
    label_style=Styles.WhiteBold.patch(text_size=9.8),
)

chart.draw(xy=(2.0, 2.5))
save()
```
:::

::: note
`GanttChart` を用いることで、エンジニアリングロードマップやリリース工程表も設計ドキュメントと同じ Git リポジトリ内でコード管理できます。
この例では6ヶ月間のリリース計画を `Architecture`・`Implementation`・`Verification & Launch` の3セクションに整理し、進捗率バー（`100%`・`80%`・`55%`・`35%`）、タスク間の依存関係を示す直交矢印、マイルストーンのひし形マーカー、そして現在地点を示す `"Today"` 破線マーカーを描画しています。すべての要素が `.show` と `draw_ratio` に対応しているため、フェーズごとの段階表示アニメーションも容易に作成できます。
:::
