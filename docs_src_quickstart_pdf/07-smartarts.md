# 7. SmartArts Components

`drawlib.smartarts` provides high-level presentation graphics inspired by PowerPoint SmartArt. Instead of calculating geometry manually, you instantiate a SmartArt component, add items, and call `.draw()`.

## Available SmartArt Classes

- **`Pyramid`**: Hierarchical pyramid layers with customizable orientation and styles.
- **`BoxList` / `ChevronProcess`**: Sequential process blocks and arrowhead pipelines.
- **`Cycle` / `MindMap` / `Tree`**: Circular workflows, mind maps, and hierarchical trees.
- **`Table` / `GridLayout` / `SourceCode`**: Structured tables, grid cards, and syntax-highlighted code blocks.

## Example: Hierarchical Pyramid

```drawlib 580px center caption:"Figure 7.1: SmartArt Pyramid Comparing Default and Custom Styled Layers"
from drawlib.canvas import config
from drawlib.smartarts import Pyramid

config(width=100, height=48)

p1 = Pyramid(styles=styles)
p1.add(text="Strategy")
p1.add(text="Architecture")
p1.add(text="Implementation")
p1.draw((6, 5), width=40, height=38, margin=2.5)

p2 = Pyramid(default_style=styles.solid, styles=styles)
p2.add(text="Vision", style=styles.blue_flat, textstyle=styles.white)
p2.add(text="Platform", style=styles.green_flat, textstyle=styles.white)
p2.add(text="Operations", style=styles.red_flat, textstyle=styles.white)
p2.draw((54, 5), width=40, height=38, margin=2.5, align="left")
```
