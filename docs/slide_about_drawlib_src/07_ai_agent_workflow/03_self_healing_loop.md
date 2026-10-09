::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils
utils.draw_page_number()
```
:::

::: block (80, 40) (1760, 60)
# Autonomous Visual Self-Healing Loop
:::

::: block (80, 140) (740, 840) font:20px
## Closing the Loop with Multimodal Vision

Code that runs without syntax errors can still produce overlapping labels or cramped margins. Drawlib pairs **headless coordinate-grid rendering (`-g`)** with **multimodal agent vision (`view_file`)**:

```bash
# Render a single diagram block with a 10x10 coordinate grid
uv run drawlib show docs_src/arch.md service_arch.png \
    -g -o .drawlib/scratch/preview.png
```

### The 6-Step Autonomous Agent Cycle
1. **Read Rules (`drawlib rules show`)**: Load coordinate & style rules.
2. **Author Declarative Python**: Write high-level diagrams, charts, or SmartArts.
3. **Render with Coordinate Grid (`-g`)**: Export headless preview image in `< 1s`.
4. **Multimodal Inspection (`view_file`)**: Agent visually inspects the rendered PNG + coordinate grid lines.
5. **Self-Repair Visual Defects**: Adjust exact `(x, y)` coordinates, padding, or contrast if any clipping is spotted.
6. **Commit Source of Truth**: Check clean Markdown + Python into Git.
:::

::: block (860, 140) (980, 840)
```drawlib file:self_healing_cycle.svg
from drawlib.canvas import clear, save, setup
from drawlib.shapes import rectangle
from drawlib.smartarts import Cycle
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=98, height=84)

rectangle((49, 42), width=94, height=78, style=Styles.Neutral.patch(shape_r=2.5))
text((49, 75.5), "Closed-Loop Autonomous AI Visual Self-Healing Cycle", style=Styles.DarkBold.patch(text_size=11.5))

loop = Cycle(
    style=Styles.White,
    text_style=Styles.DarkBold.patch(text_size=8.5),
    description_style=Styles.Muted.patch(text_size=7.2),
    arrow_style=Styles.PrimaryBold,
    clockwise=True,
    start_angle=90.0,
    node_shape="rectangle",
    node_size=(25.0, 11.5),
    arrow_type="arc",
    arrow_width=1.8,
    arrow_head_width=4.2,
    arrow_color_mode="monochrome",
    arrow_gap=2.0,
    description_placement="inside",
)

loop.add(
    "1. Read Rules",
    description="drawlib rules show",
    style=Styles.PrimaryNeutral,
)
loop.add(
    "2. Author Code",
    description="Declarative Python",
    style=Styles.PrimaryNeutral,
)
loop.add(
    "3. Render Grid",
    description="drawlib show -g -o",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=8.5),
    description_style=Styles.White.patch(text_size=7.2),
)
loop.add(
    "4. Visual Check",
    description="Multimodal view_file",
    style=Styles.AccentFlat,
    text_style=Styles.WhiteBold.patch(text_size=8.5),
    description_style=Styles.White.patch(text_size=7.2),
)
loop.add(
    "5. Self-Repair",
    description="Fix Overlap / Margin",
    style=Styles.SecondaryNeutral,
)
loop.add(
    "6. Build & Ship",
    description="Git Commit SoT",
    style=Styles.BlueNeutral,
)

loop.set_center(
    text="Autonomous\nAI Agent",
    description="Zero GUI Handoff",
    radius=12.5,
    style=Styles.DarkFlat,
    text_style=Styles.WhiteBold.patch(text_size=9.5),
    description_style=Styles.White.patch(text_size=7.5),
)

loop.draw(xy=(49.0, 39.5), radius=25.5, align="center")

save()
```
:::

::: block (80, 1010) (820, 30) font:14px
*Chapter 7: AI Agent Workflow & Ecosystem — Autonomous Visual Self-Healing Loop*
:::

::: note
- This 6-step loop is the secret superpower of Drawlib with multimodal AI agents.
- By running `drawlib show <file> <block> -g -o preview.png`, the agent gets an immediate visual coordinate ruler overlaid on the diagram. If a label is slightly off-center at `x=42`, the agent sees the `x=50` grid line in `view_file` and fixes the coordinate deterministically on the very next edit!
:::
