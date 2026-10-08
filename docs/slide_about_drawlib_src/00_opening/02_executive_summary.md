::: block (80, 60) (1760, 150)
# What is Drawlib?
A declarative, pure-Python graphics and documentation engine that treats architectural diagrams, quantitative charts, animations, and technical documents as first-class software artifacts.
:::

::: block (80, 230) (760, 720)
### 1. Pure-Python Declarative API
- Write expressive Python (`>=3.11`) using variables, loops, type-checked models, and reusable project helpers (`styles.py` & `utils.py`).
- No opaque Graphviz/Java binaries, no fragile XML/SVG hand-editing, and no 200-line `matplotlib` patch boilerplate.

### 2. Four Publishing Archetypes
- Scaffold and build **Multi-Page Documentation Sites** (`site`), **Linear Technical Specs & Vector PDFs** (`doc`), **16:9 Widescreen Slide Decks** (`slide`), and **Standalone Images** (`image`) from one unified CLI.

### 3. Autonomous AI Agent Ready
- Ships with an embedded **On-Demand Rules Catalog** (`drawlib rules show`) and headless coordinate-grid preview (`drawlib show -g`), enabling AI coding agents to write, inspect, and self-heal visual diagrams autonomously.
:::

::: block (880, 220) (960, 740)
```drawlib file:exec_kpi.svg
from drawlib.canvas import clear, save, setup
import utils

clear()
setup(width=100, height=84)

utils.draw_kpi_cards(
    [
        (
            "100%",
            "Pure Python & Git-Native",
            "Zero external GUI tools or proprietary binary formats",
        ),
        (
            "23+",
            "Shapes, SmartArts & Charts",
            "From geometric primitives to Gantt & Radar charts",
        ),
        (
            "7+",
            "Domain Diagrams & Solvers",
            "Architecture, Flow, Sequence, ER, Class, State & Auto-Graph",
        ),
        (
            "4",
            "Unified Output Targets",
            "Documentation Sites, Technical PDFs, 16:9 Slides & Standalone Images",
        ),
    ],
    width=100.0,
    height=84.0,
)
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
- At an executive level, Drawlib rests on three core pillars: a pure-Python declarative API, four integrated publishing archetypes, and first-class ergonomics for AI coding agents.
- On the right, our KPI cards summarize the scope of the ecosystem: 100% pure Python and Git-native, 23+ geometric primitives paired with 10 SmartArts and 7 quantitative charts, 7+ domain diagram engines and auto-layout solvers, and 4 unified publishing targets.
:::
