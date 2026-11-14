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
# Presentation Roadmap
:::

::: block xy=(80, 150) width=640 height=780
## Six Core Chapters

- **Motivation (Ch. 1)**: Solving visual documentation drift with Python and Git

- **Visual Engines (Ch. 2–4)**: Primitives, 34 icon suites, SmartArts, charts, and diagrams

- **Publishing & AI (Ch. 5–6)**: Five project archetypes, Office export, and AI grid review
:::

::: block xy=(760, 135) width=1080 height=820
```drawlib file=agenda_roadmap.svg
from drawlib.canvas import clear, save, setup
import utils

clear()
setup(width=108, height=82)

utils.draw_curved_agenda(
    [
        ("1. Why Drawlib?", "Solving visual documentation drift"),
        ("2. Primitives & 34 Icon Suites", "Canvas, 43 shapes, styles & 4,500+ icons"),
        ("3. 18 SmartArts & 10 Charts", "Infographics, GeoMap & pure-Python plots"),
        ("4. Diagrams, Graphs & Animation", "Cloud, UML, auto-layout & APNG"),
        ("5. 5 Archetypes & Publishing", "site, catalog, doc, slide, PDF/DOCX/PPTX"),
        ("6. AI-Native Agent Workflow", "Rules CLI, -g grid loop & SQLite cache"),
    ],
    width=108,
    height=82,
)
save()
```
:::

::: note
This presentation walks through six chapters arranged in three natural acts.
First, Chapter 1 examines why traditional visual documentation drifts out of sync with production systems and how treating illustrations and docs as Python code solves that dilemma.
Next, Chapters 2 through 4 tour Drawlib's visual building blocks—starting from canvas coordinates, 43 shapes, and 34 icon suites, moving up to 18 SmartArts and 10 pure-Python charts, and culminating in cloud/UML diagrams, graph layout solvers, and keyframe animations.
Finally, Chapters 5 and 6 demonstrate how Drawlib compiles five project archetypes across Web, PDF, and Office formats, and how AI coding agents autonomously author and visually verify diagrams using the built-in `-g` coordinate grid workflow.
:::
