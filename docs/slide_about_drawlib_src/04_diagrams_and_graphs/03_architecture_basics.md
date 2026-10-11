::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils

utils.draw_page_number()
```
:::

::: block (80, 40) (1760, 60)
# `ArchitectureDiagram` Fundamentals: Icons, Groups & Forks
:::

::: block (80, 140) (680, 840) compact
## Why `ArchitectureDiagram` Wires Never Kink

In naive diagramming tools, adding a 2-line label underneath an icon shifts the node's bounding center downward, causing horizontal arrows between aligned icons to develop ugly Z-bends.

### 3 Core Innovations
1. **Card-Centric Coordinates (`xy` = Card Center)**:
   - When you call `d.add(Node("Label", width=w, height=h, icon=...), xy=(x, y))`, `(x, y)` is strictly the **center of the node card** `(w, h)`.
   - Multi-line labels fit inside the card without shifting the card's center—so nodes sharing the same `y` always connect with a razor-straight horizontal line!
2. **Auto-Bounding `NodeGroup` Containers**:
   - Calling `group = d.add(NodeGroup(title="...", padding=6.0), xy=(gx, gy))` creates a relative coordinate group that automatically expands its boundary box to enclose all child nodes and nested subgroups.
3. **1-to-N Bus Fan-Out (`node.fork()`)**:
   - `lb.fork([svc1, svc2, svc3], at_x=55.0, padding=2.0)` creates a clean vertical distribution bus at `at_x` with orthogonal taps into every target node.
:::

::: block (800, 140) (1040, 840)
```drawlib file:arch_fundamentals.svg
from drawlib.canvas import clear, save, setup
from drawlib.diagrams.architecture import (
    ArchitectureDiagram,
    Node,
    NodeGroup,
    PhosphorIcon,
)
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=104, height=84)

d = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=8.0),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=7.5),
    node_card_style=Styles.Neutral,
    title="Card-Centric Alignment, Auto-Bounding NodeGroup & node.fork()",
    title_style=Styles.DarkBold.patch(text_size=10.0),
)

# 1. External Client & Ingress Gateway (Aligned at Y = 38.0 -> Straight wire!)
client = d.add(
    Node("Mobile & Web\nClient App\n(3-line label)", width=18, height=17, icon=PhosphorIcon.DEVICES, icon_size=8.0),
    xy=(10.0, 38.0),
)
gateway = d.add(
    Node(
        "API Gateway",
        width=18,
        height=17,
        icon=PhosphorIcon.SHIELD_CHECK,
        icon_size=8.5,
        style=Styles.White,
        card_style=Styles.PrimaryFlat,
        text_style=Styles.WhiteBold.patch(text_size=8.0),
    ),
    xy=(36.0, 38.0),
)

# 2. Auto-Bounding NodeGroup with 3 Worker Services
cluster = d.add(
    NodeGroup(
        title="Auto-Bounding NodeGroup (Worker Mesh)",
        padding=6.5,
        style=Styles.MutedDashed,
    ),
    xy=(58.0, 8.0),
)
w1 = cluster.add(
    Node("Auth Worker", width=18, height=15, icon=PhosphorIcon.KEY, icon_size=7.5, card_style=Styles.PrimaryNeutral),
    xy=(16.0, 52.0),
)
w2 = cluster.add(
    Node("Order Worker", width=18, height=15, icon=PhosphorIcon.PACKAGE, icon_size=7.5, card_style=Styles.SecondaryNeutral),
    xy=(16.0, 30.0),
)
w3 = cluster.add(
    Node("Audit Logger", width=18, height=15, icon=PhosphorIcon.FILE_TEXT, icon_size=7.5, card_style=Styles.Neutral),
    xy=(16.0, 8.0),
)

# 3. Straight connection & 1-to-3 fork() fan-out
d.connect(client, gateway, label="Straight Y=38", padding=1.5)
gateway.fork([w1, w2, w3], at_x=52.0, padding=1.5)

d.draw(xy=(4.0, 6.0))

# Callout badges explaining the mechanics
rectangle((26, 13), width=42, height=11, style=Styles.BlueNeutral.patch(shape_r=1.5))
text(
    (26, 15.2),
    "1. Card-Centric xy=(x, 38.0)",
    style=Styles.DarkBold.patch(text_size=7.8),
)
text(
    (26, 10.8),
    "Multi-line text never shifts the card center!",
    style=Styles.Dark.patch(text_size=7.0),
)

save()
```
:::

::: note
- This slide illustrates the three core design mechanics of `ArchitectureDiagram`:
  1. **Card-Centric Alignment**: Look at `Mobile & Web Client App` (which has a 3-line label) and `API Gateway` (which has a 1-line label). Because both are placed at `y=38.0`, their cards are horizontally aligned and the `"Straight Y=38"` arrow between them is completely flat without any vertical jog.
  2. **`gateway.fork([w1, w2, w3], at_x=52.0)`**: Instead of drawing three overlapping diagonal lines from the gateway, `.fork()` places a clean vertical bus at `x=52.0` and branches orthogonally into each worker.
  3. **Auto-Bounding `NodeGroup`**: The dashed container around the three workers calculates its width and height automatically from the enclosed nodes plus `padding=6.5`.
:::
