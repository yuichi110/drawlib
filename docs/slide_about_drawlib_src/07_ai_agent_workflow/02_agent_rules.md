::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils
utils.draw_page_number()
```
:::

::: block (80, 40) (1760, 60)
# Built-in AI Agent Knowledge Base (`drawlib rules`)
:::

::: block (80, 140) (740, 840) font:20px
## Zero Hallucination via On-Demand Rules

Why do AI coding agents struggle with niche libraries? Because their training data is outdated or incomplete. Drawlib solves this by **shipping its complete AI agent manual inside the Python package**:

```bash
# 1. List all 24+ embedded rule manuals
uv run drawlib rules list

# 2. Core orientation & design discipline
uv run drawlib rules show overview
uv run drawlib rules show style-guide
uv run drawlib rules show api

# 3. Specialized authoring & module deep-dives
uv run drawlib rules show slide-guide
uv run drawlib rules show anim-guide
uv run drawlib rules show lib-diagrams
uv run drawlib rules show lib-charts
```

### Progressive Context Loading
- Agents start with a lightweight `.agents/rules/drawlib.md` bootstrap and query specific `lib-<module>` manuals on demand—keeping LLM context windows lean and 100% version-accurate.
:::

::: block (860, 140) (980, 840)
```drawlib file:agent_rules_catalog.svg
from drawlib.canvas import clear, save, setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.smartarts import GridLayout
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=98, height=84)

rectangle((49, 42), width=94, height=78, r=2.5, style=Styles.Neutral)
text((49, 75), "Embedded Agent Knowledge Base Architecture (src/drawlib/_rules/)", style=Styles.DarkBold.patch(text_size=11.2))

# Top Hero Command Box
rectangle(
    (49, 64.5),
    width=84,
    height=9.0,
    r=1.8,
    style=Styles.PrimaryFlat,
    text="AI Coding Agent Query:   uv run drawlib rules show <topic>   (Offline & Version-Locked)",
    text_style=Styles.WhiteBold.patch(text_size=9.2),
)

# 3x2 GridLayout of Rule Categories
grid = GridLayout(
    num_column=2,
    num_row=3,
    style=Styles.White,
    text_style=Styles.DarkBold.patch(text_size=8.5),
    r=1.6,
)

grid.add(
    position=(0, 2),
    width=1,
    height=1,
    style=Styles.PrimaryNeutral,
    text="1. Core & Visual Discipline\n• overview (Cartesian 0,0)\n• style-guide (50%+ Neutral)",
    text_style=Styles.DarkBold.patch(text_size=8.2),
)
grid.add(
    position=(1, 2),
    width=1,
    height=1,
    style=Styles.PrimaryNeutral,
    text="2. Master API & CLI Index\n• api (Complete Symbol Index)\n• cli & project (Scaffolding)",
    text_style=Styles.DarkBold.patch(text_size=8.2),
)
grid.add(
    position=(0, 1),
    width=1,
    height=1,
    style=Styles.SecondaryNeutral,
    text="3. Slides & Animations\n• slide-guide (1920x1080 Stage)\n• anim-guide & lib-anim",
    text_style=Styles.DarkBold.patch(text_size=8.2),
)
grid.add(
    position=(1, 1),
    width=1,
    height=1,
    style=Styles.SecondaryNeutral,
    text="4. High-Level Engines\n• lib-diagrams (6 Engines)\n• lib-graph (5 Auto-Solvers)",
    text_style=Styles.DarkBold.patch(text_size=8.2),
)
grid.add(
    position=(0, 0),
    width=1,
    height=1,
    style=Styles.BlueNeutral,
    text="5. SmartArts & Charts\n• lib-smartarts (10 Builders)\n• lib-charts (7 Chart Types)",
    text_style=Styles.DarkBold.patch(text_size=8.2),
)
grid.add(
    position=(1, 0),
    width=1,
    height=1,
    style=Styles.TealNeutral,
    text="6. Primitives & Assets\n• lib-shapes, lib-lines, lib-text\n• lib-icons, lib-fonts, lib-styles",
    text_style=Styles.DarkBold.patch(text_size=8.2),
)

grid.draw(xy=(7.0, 16.0), width=84.0, height=43.0, margin=1.8)

# Bottom Benefit Bar
rectangle(
    (49, 9.5),
    width=84,
    height=7.0,
    r=1.5,
    style=Styles.White,
    text="Result: Zero Web Search Needed  •  Zero Hallucinated Signatures  •  Instant Agent Onboarding",
    text_style=Styles.PrimaryBold.patch(text_size=8.8),
)

save()
```
:::

::: block (80, 1010) (820, 30) font:14px
*Chapter 7: AI Agent Workflow & Ecosystem — Built-in AI Agent Knowledge Base*
:::

::: note
- Because `drawlib rules` ships inside the `drawlib` wheel itself, any AI coding agent (Claude Code, Gemini CLI, Cursor, Windsurf, Copilot) can immediately query the exact API signatures and style rules for the installed version of Drawlib without needing external web access.
:::
