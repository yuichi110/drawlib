::: block (80, 40) (1760, 60)
# Topics Covered
:::

::: block (80, 140) (700, 840)
- **Architecture Overview**: Declarative drawing engine
- **Native Vector Output**: High-DPI & searchable text
- **Modular Drawing**: Component-based utilities
- **Dynamic Animations**: Keyframe WebP workflows
- **Next Steps**: Extensible design workflows
:::

::: block (820, 140) (1020, 840)
```drawlib file:agenda.svg
from drawlib.canvas import clear, setup
from utils import draw_curved_agenda

clear()
setup(width=102, height=84)
draw_curved_agenda(
    [
        ("Architecture Overview", "Core Design"),
        ("Native SVG Output", "Searchable Text"),
        ("Modular Drawing", "Reusable Functions"),
        ("Dynamic Animations", "WebP Workflows"),
        ("Next Steps", "Roadmap"),
    ],
    width=102,
    height=84,
)
```
:::

::: block (80, 1010) (1760, 30) font:14px
*Drawlib Presentation*
:::
