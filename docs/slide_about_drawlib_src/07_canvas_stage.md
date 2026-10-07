::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils
utils.draw_page_number()
```
:::

::: block (80, 40) (820, 60)
# 1920×1080 Stage Architecture
:::

::: block (80, 160) (780, 800) font:22px
## Total Spatial Freedom

Every slide is a mathematically defined **1920×1080 Cartesian stage**:

- **Absolute Placement**: Position diagrams, SmartArts, and text boxes at explicit `(x, y)` and `(w, h)` coordinates.
- **Partial Overlap & Bleed**: Notice how the diagram on the right extends beyond the normal content zone, bleeding from `Y: 0` to `Y: 1080` across the stage.
- **Layer Stacking**: Manage depth with `z: N` to compose backgrounds, content panels, and overlays.
- **Modular Scoping**: Use `::: block` for scoped typography and density control (`compact`, `font: 20px`).
:::

::: block (940, 0) (980, 1080) z:5
```drawlib file:bleed_stack.svg
from drawlib.canvas import clear, save, setup
from drawlib.lines import line
from drawlib.shapes import rectangle, circle
from drawlib.styles import Styles, Colors
from drawlib.text import text

clear()
setup(width=98, height=108)

# Vertical backdrop with subtle border
rectangle((49, 54), width=94, height=104, style=Styles.MutedDashed)

# Title badge at top
rectangle((49, 98), width=80, height=8, style=Styles.MutedFlat, text="Full-Bleed Stage Stack (Y: 0 ~ 1080)", text_style=Styles.PrimaryBold)

# Edge Gateway Layer
rectangle((49, 82), width=80, height=16, style=Styles.PrimaryFlat, text="Anycast Global Edge / Cloud Armor", text_style=Styles.WhiteBold)

# Microservice Cluster Layer
rectangle((49, 58), width=80, height=22, style=Styles.SecondaryFlat, text="Service Mesh & Regional Pods", text_style=Styles.WhiteBold)

# Event Bus & Streaming
rectangle((49, 34), width=80, height=16, style=Styles.AccentFlat, text="Pub/Sub & Kafka Event Stream", text_style=Styles.WhiteBold)

# Distributed Storage Layer
rectangle((49, 12), width=80, height=18, style=Styles.DarkFlat, text="Spanner & Multi-Cloud Data Lake", text_style=Styles.WhiteBold)

# Connecting flows
line((49, 74), (49, 69), arrow_head="->", style=Styles.PrimaryBold)
line((49, 47), (49, 42), arrow_head="->", style=Styles.PrimaryBold)
line((49, 26), (49, 21), arrow_head="->", style=Styles.PrimaryBold)

save()
```
:::
::: block (80, 1010) (820, 30) font:14px
*Drawlib: Illustration as Code*
:::
