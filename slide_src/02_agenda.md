::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils
utils.draw_page_number()
```
:::

::: block (80, 40) (1760, 60)
# Topics Covered
:::

::: block (80, 140) (700, 840)
A unified, declarative approach to engineering illustration:

- **Why Drawlib?**: The transition from fragile manual drawings to version-controlled Python code.
- **Cloud Architecture**: Composing microservice topologies with vector icons and orthogonal routing.
- **Workflows & Pipelines**: CI/CD integration, SQLite hash caching, and animated WebP diagrams.
- **Modular SmartArts**: Extensible layout components and custom presentation cards.
- **Pure Canvas Stage**: Absolute 1920×1080 placement, partial bleed overlap, and z-index layers.
- **Full Canvas Hero**: Zero-margin full-bleed illustration stage without boilerplate.
- **Unified Ecosystem**: Documentation sites, vector PDF books, and interactive slide decks.
:::

::: block (820, 140) (1020, 840)
```drawlib file:agenda.svg
from drawlib.canvas import clear, setup
from utils import draw_curved_agenda

clear()
setup(width=102, height=84)
draw_curved_agenda(
    [
        ("Why Drawlib?", "Code vs Drawings"),
        ("Cloud Architecture", "Microservices Topology"),
        ("Workflows & Pipelines", "Animated CI/CD"),
        ("Modular Helpers", "Reusable Functions"),
        ("Pure Canvas Stage", "1920×1080 & Overlap"),
        ("Full Canvas Hero", "Pure Stage 一枚絵"),
        ("Unified Ecosystem", "Docs, PDF & Slides"),
    ],
    width=102,
    height=84,
)
```
:::

::: block (80, 1010) (820, 30) font:14px
*Drawlib: Illustration as Code*
:::
