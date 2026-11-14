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
# Why Visual Documentation Breaks Down
:::

::: block xy=(80, 130) width=1760 height=115
Engineering teams are forced to choose between **untrackable GUI binaries**, **rigid text DSLs**, and **isolated plotting libraries**—causing visual architecture docs to drift behind code on every release.
:::

::: block xy=(80, 260) width=1760 height=685
```drawlib file=dilemma_three_traps.svg
from drawlib.canvas import clear, save, setup
from drawlib.icons import phosphor
from drawlib.shapes import rectangle
from drawlib.smartarts import CardList, Panel
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=176, height=69)

traps = [
    (
        2.0,
        "GUI Tools (Figma / Draw.io)",
        phosphor.cursor_click,
        [
            ("Opaque Binary Files", "No Git PR diff review"),
            ("Manual PNG Exports", "Screenshots rot on release"),
            ("GUI Lock-In", "Uneditable by AI agents"),
        ],
    ),
    (
        60.5,
        "Text DSLs (Mermaid / UML)",
        phosphor.brackets_curly,
        [
            ("Rigid Auto-Layout", "Zero exact (x, y) control"),
            ("Narrow Vocabulary", "Weak KPIs, tables & maps"),
            ("Snippet-Only Scope", "No PDF or PPTX compiler"),
        ],
    ),
    (
        119.0,
        "Plotting Libs (Matplotlib)",
        phosphor.chart_bar,
        [
            ("Data Plots Only", "No cloud or UML engines"),
            ("Verbose Boilerplate", "Ad-hoc fonts and colors"),
            ("Detached Scripts", "Manual copy into slides"),
        ],
    ),
]

for px, title, hdr_icon, items in traps:
    p = Panel(
        title,
        style=Styles.Neutral.patch(shape_r=2.2),
        header_style=Styles.SecondaryNeutral.patch(shape_line_width=1.0),
        text_style=Styles.DarkBold.patch(text_size=12.4),
        icon=hdr_icon,
        icon_style=Styles.PrimaryBold,
        header_variant="filled",
        header_height=9.5,
    )
    p.draw((px, 16.5), width=55.0, height=50.0)
    c_xy, c_w, c_h = p.get_content_box(
        (px, 16.5),
        width=55.0,
        height=50.0,
        padding=(2.0, 2.2),
    )

    cl = CardList(
        style=Styles.White.patch(shape_r=1.8),
        text_style=Styles.DarkBold.patch(text_size=12.6),
        description_style=Styles.Muted.patch(text_size=11.5),
        badge_shape="circle",
        badge_style=Styles.DangerNeutral,
        icon_style=Styles.DangerBold,
        direction="vertical",
        spacing=2.0,
    )
    for item_title, item_desc in items:
        cl.add(item_title, item_desc, icon=phosphor.x_circle)
    cl.draw(c_xy, width=c_w, height=c_h)

rectangle(
    (88.0, 7.5),
    width=172.0,
    height=11.5,
    style=Styles.PrimaryFlat.patch(shape_r=2.2),
)
phosphor.sparkle((9.0, 7.5), width=5.4, style=Styles.WhiteBold)
text(
    (91.0, 7.5),
    "The Unmet Gap: Spatial Coordinates + Git PR Review + Unified Docs & Charts + AI Grid Verification",
    style=Styles.WhiteBold.patch(text_size=12.6),
)
save()
```
:::

::: note
Why do architecture diagrams and engineering slides go stale so quickly?
Because existing tools force teams into one of three traps.
First, GUI whiteboards like Figma, Lucidchart, or Draw.io give pixel control, but store opaque blobs outside normal code review—and AI coding agents cannot maintain them cleanly.
Second, text DSLs like Mermaid and PlantUML live in Markdown, but lock you into rigid auto-layout algorithms with zero coordinate control and almost no support for infographics, KPI cards, maps, or multi-format publishing.
Third, plotting libraries like Matplotlib handle numeric charts well, but lack cloud architecture diagrams, UML, SmartArts, and integrated document compilation.
Drawlib was created specifically to bridge this gap in one coherent Python ecosystem.
:::
