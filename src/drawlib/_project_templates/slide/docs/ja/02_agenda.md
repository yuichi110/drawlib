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
        ("Architecture Overview", "設計概要"),
        ("Native SVG Output", "検索可能テキスト"),
        ("Modular Drawing", "再利用可能関数"),
        ("Dynamic Animations", "WebPアニメーション"),
        ("Next Steps", "ロードマップ"),
    ],
    width=104,
    height=86,
)
```
