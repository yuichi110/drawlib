::: block (80, 50) (1760, 130)
# Designed for Both Humans and AI Coding Agents
Why pure Python + multimodal visual inspection unlocks autonomous documentation engineering.
:::

::: block (80, 200) (760, 760)
### Python is the Native Lingua Franca of LLMs

- **Zero Proprietary Syntax Friction**
  - LLMs are pre-trained on billions of lines of Python—they naturally understand functions, loops, arithmetic coordinate layout, and Pydantic type hints.
- **Self-Contained Rules Catalog (`drawlib rules`)**
  - Agents query `uv run drawlib rules show <topic>` on demand to inspect exact function signatures and style guidelines without bloating context windows.
- **Autonomous Visual Self-Healing Loop**
  1. **Author**: Write or update `drawlib` Python code in `*_src/`.
  2. **Render with Grid**: Export a preview with `-g` (`drawlib show ... -g -o preview.png`).
  3. **Inspect Multimodally**: View the rendered image to check alignment, margins, and contrast.
  4. **Self-Repair**: Adjust coordinates or styles until the visual output is publication-grade.
:::

::: block (880, 190) (960, 780)
```drawlib file:human_ai_synergy.svg
from drawlib.canvas import clear, save, setup
from drawlib.diagrams.architecture import ArchitectureDiagram, Node, NodeGroup, PhosphorIcon
from drawlib.styles import Styles

clear()
setup(width=105, height=84)

d = ArchitectureDiagram(
    node_style=Styles.Neutral,
    node_text_style=Styles.DarkBold.patch(text_size=9.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=8.5),
    title="Human + AI Agent Collaborative Loop",
    title_style=Styles.DarkBold.patch(text_size=13),
)

# Left: Collaborators
human = d.add(
    Node("Human Engineer\n(Intent & Review)", icon=PhosphorIcon.USER, icon_size=9.0, style=Styles.SecondaryNeutral),
    xy=(14.0, 56.0),
)
agent = d.add(
    Node(
        "AI Coding Agent\n(Autonomous Loop)",
        icon=PhosphorIcon.ROBOT,
        icon_size=9.5,
        style=Styles.PrimaryFlat,
        text_style=Styles.WhiteBold.patch(text_size=9.5),
    ),
    xy=(14.0, 22.0),
)

# Center: Drawlib Workspace & Feedback Engine
workspace = d.add(
    NodeGroup(title="Drawlib Repository & Self-Healing Loop", padding=6.5, style=Styles.PrimaryNeutral),
    xy=(36.0, 8.0),
)
rules_node = workspace.add(
    Node("Rules Catalog\n(drawlib rules)", icon=PhosphorIcon.BOOK_OPEN, icon_size=8.5, style=Styles.Neutral),
    xy=(15.0, 52.0),
)
code_node = workspace.add(
    Node("Declarative Code\n(.md & .py)", icon=PhosphorIcon.CODE, icon_size=8.5, style=Styles.Neutral),
    xy=(15.0, 28.0),
)
grid_node = workspace.add(
    Node("Grid Preview (-g)\n& Multimodal Check", icon=PhosphorIcon.EYE, icon_size=8.5, style=Styles.BlueNeutral),
    xy=(45.0, 28.0),
)
output_node = workspace.add(
    Node("Verified Output\n(Site / PDF / Slides)", icon=PhosphorIcon.CHECK_CIRCLE, icon_size=8.5, style=Styles.SecondaryNeutral),
    xy=(45.0, 52.0),
)

d.connect(human, code_node, label="Architecture Goal", padding=1.5)
d.connect(rules_node, agent, label="API Specs", padding=1.5)
d.connect(agent, code_node, label="Write / Fix", padding=1.5)
d.connect(code_node, grid_node, label="Render -g", padding=1.5)
d.connect(grid_node, agent, label="Visual Feedback", padding=1.5)
d.connect(grid_node, output_node, label="Pass", padding=1.5)

d.draw(xy=(4.0, 5.0))
save()
```
:::

::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils
utils.draw_page_number()
```
:::

::: note
- Crucially, Drawlib is designed from the ground up for both human engineers and AI coding agents.
- Because AI models reason natively in Python, they can query `drawlib rules show`, write declarative drawing code, render a preview with the coordinate grid (`-g`), visually inspect the output image, and autonomously self-heal any layout or overlap issues before presenting the final result to the human engineer.
:::
