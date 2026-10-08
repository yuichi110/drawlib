::: block (80, 60) (1760, 140)
# Presentation Roadmap
A comprehensive 7-chapter tour from the philosophy of Illustration as Code to high-level diagrams, animations, and AI workflows.
:::

::: block (80, 210) (960, 760)
```drawlib file:agenda.svg
from drawlib.canvas import clear, save, setup
import utils

clear()
setup(width=104, height=86)

utils.draw_curved_agenda(
    [
        ("1. Why Drawlib?", "Solving tool fragmentation, DSL limits & plotting boilerplate"),
        ("2. Core Engine & Primitives", "Cartesian canvas, 23 shapes, curves, fonts, icons & design tokens"),
        ("3. SmartArts & Quantitative Charts", "Pipelines, hierarchies, tables & 7 statistical/project charts"),
        ("4. Domain Diagrams & Auto-Layout Graphs", "Cloud VPCs, UML/ER models & 5 automatic layout solvers"),
        ("5. Multi-Frame Animations", "Keyframes, progressive reveal & interactive slide controls"),
        ("6. Documentation & Slide Engine", "Sites, vector PDFs, 16:9 spatial stage & presenter view"),
        ("7. AI Agent Workflow & Ecosystem", "Built-in rules, visual self-healing loop & SQLite caching"),
    ],
    width=104.0,
    height=86.0,
)
save()
```
:::

::: block (1080, 240) (760, 680)
### Live Dogfooding in Action

This 60-slide presentation is **100% authored and compiled with Drawlib**:

- **Source of Truth**: Markdown files and embedded `drawlib` Python blocks in `docs/slide_about_drawlib_src/`
- **Shared Theme & Macros**: Centralized palette in `styles.py` and reusable layout helpers in `utils.py`
- **Inline Vector SVGs**: Every static diagram renders as crisp inline `<svg>` with automatic `@font-face` bundling
- **Interactive `<canvas>` Animations**: Step-by-step animated diagrams controlled via `A` or Presenter View (`P`)
- **Dual Output**: Compiled into both an interactive HTML5 web deck and a 1920×1080 vector PDF
:::

::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils
utils.draw_page_number()
```
:::

::: note
- Here is our 7-chapter roadmap for the presentation.
- We begin in Chapter 1 with why Drawlib exists and the problems it solves, move through the core engine and primitives in Chapter 2, SmartArts and quantitative charts in Chapter 3, domain diagrams and auto-layout graphs in Chapter 4, multi-frame animations in Chapter 5, the documentation and slide engine in Chapter 6, and finally the AI agent workflow in Chapter 7.
- Notably, this entire slide deck is dogfooded directly from `docs/slide_about_drawlib_src/` using the exact features we are showcasing.
:::
