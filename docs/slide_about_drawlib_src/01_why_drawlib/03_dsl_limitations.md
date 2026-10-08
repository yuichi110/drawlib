::: block (80, 50) (1760, 130)
# Pain Point 2: Text DSL Limitations (Mermaid / PlantUML / Graphviz)
Why black-box heuristic layout DSLs hit a wall on real-world production architectures.
:::

::: block (80, 200) (760, 760)
### Great for 5 Nodes — Frustrating for 25 Nodes

Text-to-diagram DSLs (`Mermaid`, `PlantUML`, `DOT`) rely on rigid, opaque layout heuristics:

- **Unpredictable Layout Shifts**
  - Adding a single edge or renaming a label can cause the layout engine to reshuffle the entire diagram unpredictably.
- **No Fine-Grained Coordinate Control**
  - You cannot say *"align these 3 databases vertically at `X=80`"* or *"route this error path around the VPC border"*.
  - Engineers resort to hacks like invisible dummy nodes (`A ~~~ B`) and hidden links just to nudge boxes.
- **No Programming Constructs**
  - Static DSL syntax lacks variables, `for` loops, math expressions, conditional branches, or shared Python functions.
- **Limited Visual Expressiveness**
  - Cannot combine cloud architecture topologies, statistical charts, custom vector shapes, and multi-frame animations on one canvas.
:::

::: block (880, 190) (960, 780)
```drawlib file:dsl_limits.svg
from drawlib.canvas import clear, save, setup
from drawlib.lines import line, line_curved, lines
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=100, height=82)

# Top Panel: Rigid Black-Box DSL
rectangle((50, 60), width=92, height=34, r=3, style=Styles.MutedDashed)
text((8, 73), "Black-Box Text DSL (Opaque Heuristic Auto-Layout)", style=Styles.DarkBold.patch(text_size=10, halign="left"))

# Tangled / misaligned nodes
n1 = (20, 62)
n2 = (46, 66)
n3 = (42, 49)
n4 = (76, 63)
n5 = (72, 48)
rectangle(n1, width=18, height=9, r=1.5, style=Styles.Neutral, text="Gateway")
rectangle(n2, width=18, height=9, r=1.5, style=Styles.Neutral, text="Auth Svc")
rectangle(n3, width=18, height=9, r=1.5, style=Styles.Neutral, text="Order Svc")
rectangle(n4, width=18, height=9, r=1.5, style=Styles.Neutral, text="Redis")
rectangle(n5, width=18, height=9, r=1.5, style=Styles.Neutral, text="Postgres")

# Awkward crossing wires
line((29, 62), (37, 66), arrow_head="->", style=Styles.DarkBold)
line((29, 60), (33, 49), arrow_head="->", style=Styles.DarkBold)
line((55, 66), (63, 48), arrow_head="->", style=Styles.DangerBold)
line((51, 49), (67, 63), arrow_head="->", style=Styles.DangerBold)
text((60, 56), "Unavoidable\nWire Crossings!", style=Styles.DangerBold.patch(text_size=8))

# Bottom Panel: Drawlib Deterministic + Auto-Layout Hybrid
rectangle((50, 20), width=92, height=36, r=3, style=Styles.PrimaryNeutral)
text((8, 34), "Drawlib: Deterministic Coordinates + Inspectable Solvers", style=Styles.DarkBold.patch(text_size=10, halign="left"))

rectangle((18, 17), width=18, height=10, r=2, style=Styles.PrimaryFlat, text="Gateway", text_style=Styles.WhiteBold.patch(text_size=9))
rectangle((48, 24), width=20, height=9, r=2, style=Styles.Neutral, text="Auth Svc")
rectangle((48, 10), width=20, height=9, r=2, style=Styles.Neutral, text="Order Svc")
rectangle((80, 24), width=18, height=9, r=2, style=Styles.SecondaryNeutral, text="Redis")
rectangle((80, 10), width=18, height=9, r=2, style=Styles.SecondaryNeutral, text="Postgres")

lines([(27, 17), (33, 17), (33, 24), (38, 24)], arrow_head="->", style=Styles.DarkBold)
lines([(27, 17), (33, 17), (33, 10), (38, 10)], arrow_head="->", style=Styles.DarkBold)
line((58, 24), (71, 24), arrow_head="->", style=Styles.DarkBold)
line((58, 10), (71, 10), arrow_head="->", style=Styles.DarkBold)

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
- Pain Point 2 is the limitation of text DSLs like Mermaid, PlantUML, and Graphviz DOT.
- While text DSLs are diffable in Git, they treat layout as a black box. They work well for a 5-node toy flowchart, but as soon as you model a multi-tier cloud architecture, adding one connection can scramble node positions or create awkward wire crossings that you cannot fix.
- Drawlib gives you both worlds: 5 automatic graph layout solvers (`drawlib.graph`) when you want topological auto-layout, AND 100% deterministic Cartesian coordinates (`drawlib.diagrams`) when you want exact alignment and routing.
:::
