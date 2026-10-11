::: block xy=(80, 40) width=1760 height=60
# Topics Covered
:::

::: block xy=(80, 140) width=700 height=840
- **Architecture Overview**: Declarative drawing engine
- **Native Vector Output**: High-DPI & searchable text
- **Modular Drawing**: Component-based utilities
- **Dynamic Animations**: Keyframe WebP workflows
- **Next Steps**: Extensible design workflows
:::

::: block xy=(820, 140) width=1020 height=840
```drawlib file=agenda.svg
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

::: block xy=(80, 1010) width=1760 height=30 font_size=14px
*Drawlib Presentation*
:::
