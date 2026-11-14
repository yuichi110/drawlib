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
# Process Pipelines, Lifecycles & Roadmaps
:::

::: block xy=(80, 130) width=1760 height=815
```drawlib file=process_cycle_roadmap.svg
from drawlib.canvas import clear, save, setup
from drawlib.icons import phosphor
from drawlib.smartarts import ChevronProcess, Cycle, Panel, Roadmap
from drawlib.styles import Styles

clear()
setup(width=176, height=81)

# 1. Top Wide Panel: ChevronProcess
p_top = Panel(
    "ChevronProcess — Sequential Delivery Pipeline",
    "4 Stages",
    style=Styles.Neutral.patch(shape_r=2.0),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=14.2),
    description_style=Styles.Muted.patch(text_size=11.5),
    icon=phosphor.arrow_right,
    icon_style=Styles.PrimaryBold,
    header_height=6.8,
)
p_top.draw((1.5, 53.0), width=173.0, height=26.5)
t_xy, t_w, t_h = p_top.get_content_box((1.5, 53.0), width=173.0, height=26.5, padding=(3.5, 2.6))

proc = ChevronProcess(
    style=Styles.White,
    text_style=Styles.DarkBold.patch(text_size=12.5),
    description_style=Styles.Muted.patch(text_size=11.0),
    corner_angle=62.0,
    spacing=2.0,
    flat_left_end=True,
)
proc.add("1. Author", description="Markdown + Python", style=Styles.PrimaryNeutral)
proc.add(
    "2. Render -g",
    description="Visual Grid Check",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=12.5),
    description_style=Styles.White.patch(text_size=11.0),
)
proc.add("3. Cache", description="SQLite Incremental", style=Styles.SecondaryNeutral)
proc.add("4. Publish", description="HTML, PDF & PPTX", style=Styles.White)
proc.draw(t_xy, width=t_w, height=t_h)

# 2. Bottom-Left Panel: Cycle with CycleCenter (45-deg diagonal orbit for wide landscape clearance)
p_bl = Panel(
    "Cycle — Feedback Loop",
    "4-Node Orbit",
    style=Styles.Neutral.patch(shape_r=2.0),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=14.2),
    description_style=Styles.Muted.patch(text_size=11.5),
    icon=phosphor.arrows_clockwise,
    icon_style=Styles.PrimaryBold,
    header_height=6.8,
)
p_bl.draw((1.5, 1.5), width=84.5, height=49.0)
c_xy, _, _ = p_bl.get_content_box(
    (1.5, 1.5), width=84.5, height=49.0, padding=(3.0, 2.0), content_align="center"
)

cyc = Cycle(
    style=Styles.White,
    text_style=Styles.DarkBold.patch(text_size=11.8),
    description_style=Styles.Muted.patch(text_size=10.5),
    arrow_style=Styles.PrimaryBold,
    clockwise=True,
    start_angle=135.0,
    node_shape="rectangle",
    node_width=20.5,
    node_height=8.0,
    arrow_type="arc",
    arrow_width=1.4,
    arrow_head_width=3.6,
    arrow_color_mode="monochrome",
    arrow_gap=2.2,
)
cyc.add(
    "1. Draft",
    description="Write API",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=11.8),
    description_style=Styles.White.patch(text_size=10.5),
)
cyc.add("2. Inspect", description="Show -g", style=Styles.PrimaryNeutral)
cyc.add("3. Refine", description="Tune XY", style=Styles.SecondaryNeutral)
cyc.add("4. Verify", description="Clean Diff", style=Styles.White)
cyc.set_center(
    "AI Loop",
    description="Self-Heal",
    radius=7.0,
    style=Styles.DarkFlat,
    text_style=Styles.WhiteBold.patch(text_size=11.8),
    description_style=Styles.White.patch(text_size=10.2),
)
cyc.draw(c_xy, radius=18.2, align="center")

# 3. Bottom-Right Panel: Roadmap
p_br = Panel(
    "Roadmap — Milestone Timeline",
    "Bezier Spine",
    style=Styles.Neutral.patch(shape_r=2.0),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=14.2),
    description_style=Styles.Muted.patch(text_size=11.5),
    icon=phosphor.git_branch,
    icon_style=Styles.PrimaryBold,
    header_height=6.8,
)
p_br.draw((90.0, 1.5), width=84.5, height=49.0)
r_xy, r_w, r_h = p_br.get_content_box((90.0, 1.5), width=84.5, height=49.0, padding=(3.5, 2.0))

rm = Roadmap(
    style=Styles.White,
    text_style=Styles.DarkBold.patch(text_size=11.6),
    description_style=Styles.Muted.patch(text_size=10.5),
    spine_style=Styles.PrimaryBold,
    badge_style=Styles.SecondaryNeutral,
    badge_text_style=Styles.DarkBold.patch(text_size=11.0),
    icon_style=Styles.PrimaryBold,
    direction="vertical",
    curve_bend=0.14,
    card_shape="rounded_rect",
    spacing=2.2,
)
rm.add("Core Vector Canvas", "Primitives, icons & theme tokens", badge_text="P1", icon=phosphor.pencil_simple)
rm.add(
    "SmartArts & Charts",
    "18 infographics & 10 declarative plots",
    badge_text="P2",
    icon=phosphor.chart_bar,
    badge_style=Styles.PrimaryFlat,
    badge_text_style=Styles.WhiteBold.patch(text_size=11.0),
)
rm.add("Diagrams & Graphs", "6 diagram engines & layout solvers", badge_text="P3", icon=phosphor.tree_structure)
rm.add("Multi-Format Export", "HTML, PDF, PPTX & AI rules CLI", badge_text="P4", icon=phosphor.rocket_launch)
rm.draw(r_xy, width=r_w, height=r_h)

save()
```
:::

::: note
This slide demonstrates how `Panel` (`get_content_box`) composes three sequential and cyclical SmartArt components on a single canvas:
- **Top (`ChevronProcess`)**: Ideal for linear pipelines such as CI/CD builds or document compilation stages (`1. Author` -> `2. Render -g` -> `3. Cache` -> `4. Publish`), automatically calculating interlocking chevron angles and widths.
- **Bottom-Left (`Cycle` + `CycleCenter`)**: Distributes steps radially along an orbit with curved block arrows and an optional central hub (`AI Loop`), making PDCA and self-healing workflows effortless to express.
- **Bottom-Right (`Roadmap`)**: Pairs numbered or labeled phase badges along a straight or curved Bezier spine with icon-equipped milestone cards.
:::
