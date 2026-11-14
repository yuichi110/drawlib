::: block xy=(1700, 1008) width=140 height=32
```drawlib file=page.svg
import utils
utils.draw_page_number()
```
:::

::: block xy=(80, 1010) width=900 height=30 font_size=15px
*Drawlib — Illustration & Documentation as Code*
:::

::: block xy=(80, 36) width=1760 height=72
# Engineering Roadmaps with GanttChart
:::

::: block xy=(80, 130) width=1760 height=110
- **Declarative Schedule Modeling**: Group workstreams with `Section`, track completion via `Task(progress=...)`, and pin `Milestone` diamonds.
- **Dependencies & Live Status Markers**: Route orthogonal `Dependency` arrows and overlay vertical `Marker` lines (`Today`, `Release`) in code.
:::

::: block xy=(80, 255) width=1760 height=690
```drawlib file=gantt_release_plan.svg
from drawlib.canvas import clear, save, setup
from drawlib.charts.gantt import GanttChart
from drawlib.styles import Colors, Styles

clear()
setup(width=176, height=69)

chart = GanttChart(
    columns=["Jan (M1)", "Feb (M2)", "Mar (M3)", "Apr (M4)", "May (M5)", "Jun (M6)"],
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

chart.add_section("1. Architecture", style=Styles.PrimaryNeutral, text_style=Styles.DarkBold.patch(text_size=12.8))
t1 = chart.add_task("Canvas & Theme Spec", start=0.0, end=1.3, style=Styles.PrimaryFlat, progress=1.0)
t2 = chart.add_task("SmartArts & Charts API", start=1.0, end=2.5, style=Styles.PrimaryFlat, progress=1.0)
chart.add_milestone("Architecture Freeze", at=2.5, style=Styles.PrimaryFlat)

chart.add_section("2. Implementation", style=Styles.PrimaryNeutral, text_style=Styles.DarkBold.patch(text_size=12.8))
t3 = chart.add_task(
    "Diagram & Graph Solvers",
    start=2.2,
    end=3.8,
    style=Styles.PrimaryFlat,
    progress=0.80,
)
t4 = chart.add_task(
    "HTML, PDF & PPTX Builders",
    start=2.9,
    end=4.5,
    style=Styles.SecondaryFlat,
    progress=0.55,
)

chart.add_section("3. Verification & Launch", style=Styles.PrimaryNeutral, text_style=Styles.DarkBold.patch(text_size=12.8))
t5 = chart.add_task(
    "AI Agent Rules & Grid CLI",
    start=4.1,
    end=5.4,
    style=Styles.SecondaryFlat,
    progress=0.35,
)
t6 = chart.add_task("Bilingual Docs & Showcase", start=4.9, end=5.9, style=Styles.PrimaryNeutral, progress=0.0)
chart.add_milestone("v1.0 GA Release", at=5.9, style=Styles.AccentFlat)

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
`GanttChart` brings project management roadmaps into Git version control alongside engineering RFCs and sprint reviews.
Here we divide a 6-month release plan into three sections (`Architecture`, `Implementation`, and `Verification & Launch`), render partial completion bars (`progress=0.80`, `0.55`, `0.35`), connect dependent tasks with orthogonal arrows, place diamond milestones (`Architecture Freeze`, `v1.0 GA Release`), and draw a vertical `"Today"` marker badge across the timeline. Because every element supports `.show` and `draw_ratio`, teams can even animate phase-by-phase schedule reviews.
:::
