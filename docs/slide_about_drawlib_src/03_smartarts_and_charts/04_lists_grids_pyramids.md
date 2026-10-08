::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils

utils.draw_page_number()
```
:::

::: block (80, 40) (1760, 60)
# Stacks, Matrices & Tiered Layers (`BoxList`, `GridLayout`, `Pyramid`)
:::

::: block (80, 140) (680, 840) compact
## Structured Card & Layer Components

### 1. `BoxList` — Directional Card Sequences
- Aligns sequential cards along `"left"`, `"right"`, `"bottom"`, or `"top"` orientations.
- Ideal for status badges, KPI ribbons, and linear step stacks.

### 2. `GridLayout` — Multi-Span Architecture Matrices
- **Bottom-Left Indexed**: `(col=0, row=0)` starts at the bottom-left cell; rows increment upward (`+y`) and columns increment rightward (`+x`).
- **Cell Spanning**: Any item can span multiple columns and rows (`position=(col, row), width=w, height=h`) to model full-width ingress/platform layers alongside multi-column microservice cells.
- **Outer Container**: Optional `outer_style` and `outer_r` wrap the entire matrix in a dashed or solid boundary.

### 3. `Pyramid` — Proportional Tiered Hierarchies
- Slices a triangular pyramid into an apex triangle and progressive trapezoidal tiers.
- Supports `align="bottom"` (upright) or `"top"` (inverted funnel) and `order="vertex_to_base"` or `"base_to_vertex"`.
:::

::: block (800, 140) (1040, 840)
```drawlib file:grids_and_pyramids.svg
from drawlib.canvas import clear, save, setup
from drawlib.smartarts import BoxList, GridLayout, Pyramid
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=104, height=84)

# 1. Left Column: Multi-Tier Platform Matrix (GridLayout)
text(
    (4, 79),
    "Multi-Tier Platform Matrix (GridLayout)",
    style=Styles.DarkBold.patch(text_size=9.5, text_halign="left"),
)

grid = GridLayout(
    num_column=4,
    num_row=4,
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=7.8),
    r=1.2,
)
# Row 3 (Top): Edge Ingress (spans all 4 columns)
grid.add(
    position=(0, 3),
    width=4,
    height=1,
    text="Edge Ingress: Global CDN & WAF Gateway",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=8.5),
)
# Row 2: Application Services
grid.add(position=(0, 2), width=2, height=1, text="Order & Checkout API", style=Styles.PrimaryNeutral)
grid.add(position=(2, 2), width=1, height=1, text="Auth", style=Styles.PrimaryNeutral)
grid.add(position=(3, 2), width=1, height=1, text="Search", style=Styles.PrimaryNeutral)
# Row 1: Persistence & Messaging
grid.add(position=(0, 1), width=1, height=1, text="Cloud SQL", style=Styles.SecondaryNeutral)
grid.add(position=(1, 1), width=1, height=1, text="Redis", style=Styles.SecondaryNeutral)
grid.add(position=(2, 1), width=2, height=1, text="Kafka Event Mesh", style=Styles.BlueNeutral)
# Row 0 (Bottom): Infrastructure Foundation (spans all 4 columns)
grid.add(
    position=(0, 0),
    width=4,
    height=1,
    text="Multi-Zone Kubernetes Foundation (GKE)",
    style=Styles.Neutral,
)
grid.draw(
    xy=(4, 22),
    width=48,
    height=53,
    margin=1.2,
    outer_r=1.8,
    outer_style=Styles.MutedDashed,
)

# 2. Right Column: Software Testing Pyramid (Pyramid)
text(
    (56, 79),
    "Software Testing Pyramid (Pyramid)",
    style=Styles.DarkBold.patch(text_size=9.5, text_halign="left"),
)

pyramid = Pyramid(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=8.2),
)
pyramid.add(
    "Manual\n(1%)",
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=7.0),
)
pyramid.add("E2E UI Tests (9%)", style=Styles.BlueNeutral)
pyramid.add("Integration & Contract (20%)", style=Styles.SecondaryNeutral)
pyramid.add(
    "Automated Unit Tests (70%)",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=8.8),
)
pyramid.draw(
    xy=(56, 22),
    width=44,
    height=53,
    margin=1.4,
    align="bottom",
    order="vertex_to_base",
)

# 3. Bottom Strip: BoxList Status Ribbon across the bottom
text(
    (4, 15.5),
    "Regional Cluster Health Ribbon — BoxList(align='left')",
    style=Styles.DarkBold.patch(text_size=8.8, text_halign="left"),
)
ribbon = BoxList(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=7.8),
)
ribbon.add("us-east1: 99.99% OK", style=Styles.TealNeutral)
ribbon.add("europe-west1: 99.98% OK", style=Styles.TealNeutral)
ribbon.add("asia-northeast1: Primary", style=Styles.PrimaryFlat, text_style=Styles.WhiteBold.patch(text_size=7.8))
ribbon.add("us-west1: DR Standby", style=Styles.Neutral)
ribbon.draw(xy=(4, 7.5), box_width=24.0, box_height=8.5, align="left")

save()
```
:::

::: note
- On this slide, we combine three structural SmartArt components on a single canvas: `GridLayout` on the left, `Pyramid` on the right, and `BoxList` along the bottom ribbon.
- **Left (`GridLayout`)**: Demonstrates cell spanning in a 4x4 matrix. Remember that `GridLayout` is anchored at the bottom-left `(x, y)` and `row=0` is the bottom-most row ("Multi-Zone Kubernetes Foundation"), while `row=3` is the top-most row ("Edge Ingress"). Middle rows span 1 or 2 columns to represent individual microservices and data stores.
- **Right (`Pyramid`)**: Models the classic Software Testing Pyramid using `order="vertex_to_base"`: Manual exploratory testing (1%) at the apex, E2E UI tests (9%), Integration & Contract tests (20%), and Automated Unit Tests (70%) anchored at the wide foundation in `Styles.PrimaryFlat`.
- **Bottom (`BoxList`)**: Shows a horizontal sequence of regional status cards using `align="left"`.
:::
