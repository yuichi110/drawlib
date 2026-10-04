---
header: "Agenda"
layout: default
---

# Topics Covered

```drawlib (820, 140) (1040, 860) file:agenda.svg
from drawlib.canvas import clear, setup
from utils import draw_curved_agenda

clear()
setup(width=104, height=86)
draw_curved_agenda(
    [
        ("Architecture Overview", "Core Design"),
        ("Native SVG Output", "Searchable Text"),
        ("Modular Drawing", "Reusable Functions"),
        ("Dynamic Animations", "WebP Workflows"),
        ("Next Steps", "Roadmap"),
    ],
    width=104,
    height=86,
)
```
