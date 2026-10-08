::: block (110, 200) (860, 680)
# Drawlib
## Illustration & Illustrated Documentation as Code

Unify **declarative Python diagrams**, **technical documentation**, **vector PDFs**, and **16:9 presentations** inside a single version-controlled Git repository.

---

- **Pure-Python Declarative API** — Zero GUI silos, raw SVG math, or rigid text DSLs
- **Single Source of Truth (SoT)** — Code, architecture diagrams, and docs evolve together in PRs
- **Autonomous AI Agent Ready** — Built-in rules catalog & multimodal visual self-healing loop

<br>

**Drawlib Official Showcase Deck**  
*Pure Python (`>=3.11`) • Apache 2.0 License*
:::

::: block (980, 140) (840, 780)
```drawlib file:title_hero.svg
from drawlib.canvas import clear, save, setup
from drawlib.diagrams.architecture import ArchitectureDiagram, Node, NodeGroup, PhosphorIcon
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=105, height=95)

text(
    (52.5, 89.0),
    "Unified Illustration & Documentation Pipeline",
    style=Styles.DarkBold.patch(text_size=12.0),
)

d = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=9.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=8.8),
    node_card_style=Styles.White,
)

repo = d.add(
    NodeGroup(title="Unified Git Repository", padding=6.5, style=Styles.PrimaryNeutral),
    xy=(6.0, 14.0),
)
code_node = repo.add(
    Node((22, 18), "Python Code\n& Markdown", icon=PhosphorIcon.CODE, icon_size=9.0),
    xy=(16.0, 46.0),
)
engine_node = repo.add(
    Node(
        (22, 18),
        "Drawlib Engine",
        icon=PhosphorIcon.CPU,
        icon_size=9.5,
        style=Styles.White,
        card_style=Styles.PrimaryFlat,
        text_style=Styles.WhiteBold.patch(text_size=9.8),
    ),
    xy=(16.0, 16.0),
)

site_node = d.add(
    Node((20, 17), "Docs Site", icon=PhosphorIcon.GLOBE, icon_size=9.0, card_style=Styles.SecondaryNeutral),
    xy=(78.0, 62.0),
)
pdf_node = d.add(
    Node((20, 17), "Vector PDF", icon=PhosphorIcon.FILE_PDF, icon_size=9.0, card_style=Styles.Neutral),
    xy=(78.0, 38.0),
)
slides_node = d.add(
    Node((20, 17), "16:9 Slides", icon=PhosphorIcon.PRESENTATION_CHART, icon_size=9.0, card_style=Styles.BlueNeutral),
    xy=(78.0, 14.0),
)

d.connect(code_node, engine_node, label="Compile", padding=1.5)
engine_node.fork([site_node, pdf_node, slides_node], at_x=54.0, padding=1.5)

d.draw(xy=(4.0, 4.0))
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
- Welcome to the official Drawlib Showcase presentation.
- Drawlib is a pure-Python library built around the philosophy of "Illustration as Code" and "Illustrated Documentation as Code."
- As shown in the architecture diagram on the right, Drawlib unifies Python code and Markdown inside your Git repository and compiles them into interactive documentation websites, vector PDFs, and 16:9 presentation slide decks—including this very presentation.
:::
