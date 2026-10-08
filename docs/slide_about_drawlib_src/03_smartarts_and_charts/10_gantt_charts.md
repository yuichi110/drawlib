::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils

utils.draw_page_number()
```
:::

::: block (80, 40) (1760, 60)
# Engineering Roadmaps & Timelines (`GanttChart`)
:::

::: block (80, 140) (640, 840) compact
## Declarative Project Schedules as Code

Maintaining engineering roadmaps in external spreadsheet or GUI tools makes version control diffs impossible. `GanttChart` models schedules directly in Python:

### Core Schedule Building Blocks
- **`add_section(name)`**: Full-width horizontal divider bands that group tasks by workstream or team.
- **`add_task(name, start, end, style, progress=...)`**:
  - `start` and `end` accept column names (`"Apr"`) or continuous floating-point column indices (`1.5` = middle of 2nd column).
  - `progress` (`0.0` to `1.0`) renders a two-tone completion fill bar with percentage text (`progress_text_style`).
- **`add_milestone(name, at, style)`**: Renders a diamond milestone marker at exact timeline coordinate `at`.
- **`add_dependency(from_task, to_task)`**: Routes orthogonal finish-to-start dependency arrows between tasks.
- **`add_marker(at, style, label="Today")`**: Draws a vertical status line across all rows.
:::

::: block (760, 140) (1080, 840)
```drawlib file:gantt_roadmap.svg
from drawlib.canvas import clear, save, setup
from drawlib.charts.gantt import GanttChart
from drawlib.styles import Styles

clear()
setup(width=108, height=84)

chart = GanttChart(
    axis_line_style=Styles.Dark,
    columns=["Q1 (Jan-Mar)", "Q2 (Apr-Jun)", "Q3 (Jul-Sep)", "Q4 (Oct-Dec)"],
    width=100.0,
    label_width=28.0,
    title="Drawlib 2.0 Platform Engineering Roadmap",
    title_style=Styles.DarkBold.patch(text_size=10.5),
    header_height=6.2,
    row_height=5.4,
    bar_radius=0.9,
    axis_text_style=Styles.Dark.patch(text_size=8.0),
    grid_style=Styles.MutedDashed,
    zebra_style=Styles.MutedThin,
    progress_text_style=Styles.WhiteBold.patch(text_size=7.2),
    background_style=Styles.NeutralFlat,
)

# Section 1: Core Vector Engine
chart.add_section("1. Core Rendering & Vector Engine")
t1 = chart.add_task(
    "SVG Font & Icon Auto-Bundler",
    start=0.0,
    end=1.1,
    style=Styles.PrimaryFlat,
    progress=1.0,
)
t2 = chart.add_task(
    "Unified show & scale Lifecycle",
    start=0.7,
    end=2.0,
    style=Styles.PrimaryFlat,
    progress=0.85,
)
m1 = chart.add_milestone("v2.0 Core Freeze", at=2.0, style=Styles.AccentFlat)

# Section 2: Domain Diagrams & Auto-Layout
chart.add_section("2. Domain Diagrams & Graph Solvers")
t3 = chart.add_task(
    "6 Domain Diagram Engines",
    start=1.2,
    end=2.6,
    style=Styles.SecondaryFlat,
    progress=0.60,
)
t4 = chart.add_task(
    "5 Declarative Graph Solvers",
    start=2.1,
    end=3.4,
    style=Styles.SecondaryFlat,
    progress=0.25,
)

# Section 3: Interactive Slide & PDF Pipeline
chart.add_section("3. Slide Stage & Documentation CLI")
t5 = chart.add_task(
    "Dual-Window Presenter View",
    start=2.5,
    end=3.7,
    style=Styles.BlueNeutral,
    progress=0.0,
)
m2 = chart.add_milestone("GA Release v2.0", at=3.8, style=Styles.PrimaryFlat)

# Dependencies & Current Date Marker
chart.add_dependency(t1, t2)
chart.add_dependency(t2, t3)
chart.add_dependency(t3, t4)
chart.add_dependency(t4, t5)
chart.add_marker(at=1.85, style=Styles.DarkDashed, label="Today")

chart.draw(xy=(4.0, 8.0))

save()
```
:::

::: note
- Slide 10 concludes Chapter 3 with `GanttChart`, one of the most practical charts for software engineering teams.
- Notice how `GanttChart` combines all five scheduling primitives in a single declarative specification:
  1. `add_section()` divides the roadmap into three clear engineering workstreams.
  2. `add_task()` specifies start/end offsets across the four quarterly columns (`0.0` to `4.0`) along with completion ratios (`progress=1.0`, `0.85`, `0.60`, `0.25`).
  3. `add_milestone()` places diamond markers at `v2.0 Core Freeze` and `GA Release v2.0`.
  4. `add_dependency()` routes orthogonal arrows linking dependent tasks (`t1 -> t2 -> t3 -> t4 -> t5`).
  5. `add_marker(at=1.85, label="Today")` draws a dashed vertical line marking the current date across the entire schedule.
:::
