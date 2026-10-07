::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils
utils.draw_page_number()
```
:::

::: block (80, 40) (1760, 60)
# Modular Drawing Helpers
:::

::: block (80, 140) (740, 840)
## Reusable Python Helpers in utils.py

Drawlib eliminates rigid DSL wrappers in favor of pure, reusable Python functions:

- **Illustration as Code**:
  - Reusable drawing functions reside in project-level `utils.py`
  - Automatically imported and accessible across all documentation & slide decks
  - Full IDE autocomplete, type annotations, and custom styling
- **Built-in Presentation Helpers**:
  - `draw_curved_agenda()`: Curved presentation agenda with numbered badges
  - `draw_kpi_cards()`: Vertically stacked metric cards with accent pills
  - `service_card()` & `connect()`: Microservice architectures and network flows
- **Declarative Invocation**:
  - Call pure Python functions directly inside `::: block` containers
:::

::: block (860, 140) (980, 840)
```drawlib file:kpi_metrics.svg
from drawlib.canvas import clear, setup
from utils import draw_kpi_cards

clear()
setup(width=100, height=84)
draw_kpi_cards(
    [
        ("99.99%", "System Availability", "Tier-1 SLA production target"),
        ("1.2s", "Fast Build Time", "Sub-second SQLite cache hit"),
        ("100%", "Verified Coverage", "Unit and integration tests passing"),
    ],
    width=100,
    height=84,
)
```
:::

::: block (80, 1010) (820, 30) font:14px
*Drawlib: Illustration as Code*
:::
