---
layout: default
header: "Agenda"
footer: "Drawlib: Illustration as Code"
paginate: true
---

# Topics Covered

A unified, declarative approach to engineering illustration:

- **Why Drawlib?**: The transition from fragile manual drawings to version-controlled Python code.
- **Cloud Architecture**: Composing microservice topologies with vector icons and orthogonal routing.
- **Workflows & Pipelines**: CI/CD integration, SQLite hash caching, and animated WebP diagrams.
- **Modular SmartArts**: Extensible layout components and custom presentation cards.
- **Pure Canvas Stage**: Absolute 1920×1080 placement, partial bleed overlap, and z-index layers.
- **Full Canvas Hero**: Zero-margin full-bleed illustration stage (`layout: canvas`).
- **Unified Ecosystem**: Documentation sites, vector PDF books, and interactive slide decks.

```drawlib (820, 140) (1040, 860) file:agenda.svg
from drawlib.canvas import clear, setup
from utils import draw_curved_agenda

clear()
setup(width=104, height=86)
draw_curved_agenda(
    [
        ("Why Drawlib?", "Code vs Drawings"),
        ("Cloud Architecture", "Microservices Topology"),
        ("Workflows & Pipelines", "Animated CI/CD"),
        ("Modular Helpers", "Reusable Functions"),
        ("Pure Canvas Stage", "1920×1080 & Overlap"),
        ("Full Canvas Hero", "layout: canvas 一枚絵"),
        ("Unified Ecosystem", "Docs, PDF & Slides"),
    ],
    width=104,
    height=86,
)
```
