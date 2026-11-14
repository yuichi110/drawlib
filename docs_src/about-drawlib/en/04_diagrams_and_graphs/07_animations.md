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
# Interactive Frame Animations (APNG & WebP)
:::

::: block xy=(80, 145) width=680 height=790
## Motion as Code Across All Modules

- **Multi-Frame Engine**: Declarative `Animation(fps, loop)` API
- **Progressive Reveal**: `draw_ratio` on Lines, Charts & Diagrams
- **Interactive Stage**: Live `<canvas>` (`anim_trigger`, `anim_pause`, `A`)
- **Static Export Ready**: Auto-extracts clean frames for PDF & PPTX

```python
anim = Animation(fps=2.0, loop=0)
for r in [0.4, 0.7, 1.0]:
    series.draw_ratio = r
    with anim.frame():
        chart.draw(xy=(10, 6))
```
:::

::: block xy=(800, 140) width=1040 height=800
```drawlib file=anim_showcase.png anim_trigger=auto anim_loop=infinite
from drawlib.anim import Animation
from drawlib.canvas import clear, save, setup
from drawlib.charts.bar import BarChart
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.smartarts import Panel
from drawlib.styles import Styles

clear()
setup(width=104, height=80)
anim = Animation(fps=2.0, loop=0)

panel = Panel(
    "Live Pipeline & BarChart Growth",
    style=Styles.White,
    header_style=Styles.PrimaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=16.0),
    icon=phosphor.play_circle,
    icon_style=Styles.PrimaryBold,
    header_height=9.0,
)

chart = BarChart(
    axis_line_style=Styles.MutedDashed,
    categories=["Q1", "Q2", "Q3", "Q4"],
    width=84.0,
    height=37.0,
    title="Throughput Growth (k RPS)",
    title_style=Styles.DarkBold.patch(text_size=14.5),
    bar_width_ratio=0.68,
    bar_r=1.0,
    axis_text_style=Styles.DarkBold.patch(text_size=13.5),
    grid_style=Styles.MutedThin,
    value_text_style=Styles.DarkBold.patch(text_size=13.5),
    value_format="{:.0f}",
)
chart.configure_y_axis(min_value=0, max_value=105, tick_step=25)
s1 = chart.add_series("Stream", [42, 62, 78, 92], style=Styles.PrimaryFlat)
s2 = chart.add_series("Batch", [26, 36, 45, 54], style=Styles.SecondaryNeutral)

stages = ["Ingest", "Transform", "Index", "Serve"]
xs = [16.5, 40.0, 63.5, 87.0]
ratios = [0.35, 0.50, 0.65, 0.80, 0.92, 1.0, 1.0]

for idx, r in enumerate(ratios):
    is_last = idx == len(ratios) - 1
    active = min(idx, 3)
    s1.draw_ratio = r
    s2.draw_ratio = r

    with anim.frame(duration=2.0 if is_last else 0.5):
        panel.draw((2.0, 2.0), width=100.0, height=76.0)
        for j in range(3):
            e_st = Styles.PrimaryBold if j < active else Styles.MutedDashed
            line((xs[j] + 9.5, 57.5), (xs[j + 1] - 9.5, 57.5), arrow_head="->", style=e_st)
        for j, name in enumerate(stages):
            if j == active:
                st, tst = Styles.PrimaryFlat, Styles.WhiteBold.patch(text_size=13.8)
            elif j < active:
                st, tst = Styles.PrimaryNeutral, Styles.DarkBold.patch(text_size=13.8)
            else:
                st, tst = Styles.Neutral, Styles.Dark.patch(text_size=13.8)
            rectangle((xs[j], 57.5), width=19.0, height=9.2, style=st.patch(shape_r=1.8), text=name, text_style=tst)

        chart.draw(xy=(10.0, 6.0))
        chart.draw_legend(
            xy=(64.0, 44.5),
            text_style=Styles.DarkBold.patch(text_size=13.5),
            orientation="horizontal",
            item_gap=4.5,
        )

save()
```
:::

::: note
**Declarative Frame Animations Across Every Drawlib Module (`drawlib.anim`)**:
- **Unified `Animation(fps, loop)` Context Manager**: Wrapping standard Drawlib calls inside `with anim.frame(duration=...):` compiles lossless **APNG (`.png`)** or **Animated WebP (`.webp`)** assets directly from Markdown code blocks.
- **First-Class Component Animation Controls**: Every SmartArt, Diagram, and Chart supports `.show` (reserving spatial layout slots and axis scales without visual jumps) plus progressive `.draw_ratio` (`0.0` → `1.0`) for growing chart bars, sweeping lines, and revealing pipelines.
- **Interactive Presentation & Print Fallback**: HTML slides decode APNG/WebP frames onto an interactive `<canvas>` supporting `anim_trigger=auto|click`, `anim_pause=(...)`, and keyboard shortcut `A`, while PDF and PPTX exporters automatically extract clean static frames so both Frame 0 and the final completed state remain crisp and publication-ready.
:::
