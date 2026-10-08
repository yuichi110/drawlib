::: block (80, 50) (1760, 130)
# Pain Point 3: Raw SVG & Matplotlib Boilerplate
Why general-purpose plotting libraries and raw vector XML are too low-level for architecture diagrams.
:::

::: block (80, 200) (760, 760)
### The Low-Level Productivity Trap

When engineers outgrow text DSLs, they sometimes reach for raw `<svg>` templates or Python's `matplotlib.patches`:

- **Verbose Patch & Bezier Boilerplate**
  - Drawing a single rounded service box with an icon, centered two-line title, and orthogonal boundary-clipped arrow in raw `matplotlib` requires **40–60 lines** of `FancyBboxPatch`, `ConnectionPatch`, `Path`, and manual bounding-box math.
- **Inverted or Confusing Coordinate Defaults**
  - Raw SVG uses top-left origins with manual `<text dy="...">` baseline offsets and no automatic word/boundary clipping.
- **No Domain Semantics**
  - Plotting libraries know about scatter plots and histograms, not **VPC NodeGroups, UML Class relationships, Sequence lifelines, ER Crow's foot notation, or Phosphor/GCP icons**.
:::

::: block (880, 190) (960, 780)
```drawlib file:low_level_limits.svg
from drawlib.canvas import clear, save, setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=100, height=82)

# Left Card: Low-Level Boilerplate
rectangle((26, 42), width=44, height=70, r=3, style=Styles.Neutral)
rectangle((26, 71), width=44, height=12, r=3, style=Styles.DarkFlat, text="Raw Matplotlib / SVG\n(~180 Lines of Boilerplate)", text_style=Styles.WhiteBold.patch(text_size=9.5))

low_level_items = [
    "fig, ax = plt.subplots(figsize=...)",
    "FancyBboxPatch((x-w/2, y-h/2), ...)",
    "Manual Z-order & alpha clipping",
    "Manual trig for arrowhead angles",
    "Manual font TTF path registration",
    "Manual PNG icon extent math",
    "No VPC groups or UML connectors",
]
for idx, item in enumerate(low_level_items):
    cy = 58 - idx * 7.2
    rectangle((26, cy), width=38, height=5.4, r=1.2, style=Styles.White)
    text((9, cy), f"✗  {item}", style=Styles.Dark.patch(text_size=8.0, text_halign="left"))

# Right Card: Drawlib High-Level Declarative API
rectangle((74, 42), width=44, height=70, r=3, style=Styles.PrimaryNeutral)
rectangle((74, 71), width=44, height=12, r=3, style=Styles.PrimaryFlat, text="Drawlib Declarative API\n(~15 Lines of Clean Python)", text_style=Styles.WhiteBold.patch(text_size=9.5))

drawlib_items = [
    "setup(width=120, height=70)",
    "Center-anchored shapes & icons",
    "Smart boundary-clipped edges",
    "13 orthogonal style variants",
    "1,500+ Phosphor & 250+ GCP icons",
    "10 SmartArts & 7 Domain Diagrams",
    "Built-in APNG/WebP animations",
]
for idx, item in enumerate(drawlib_items):
    cy = 58 - idx * 7.2
    rectangle((74, cy), width=38, height=5.4, r=1.2, style=Styles.White)
    text((57, cy), f"✓  {item}", style=Styles.PrimaryBold.patch(text_size=8.0, text_halign="left"))

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
- Pain Point 3 is the opposite extreme: writing raw SVG XML or low-level `matplotlib.patches` code directly.
- While Matplotlib is a powerhouse for scientific plotting, building an architecture diagram or sequence diagram with raw `FancyBboxPatch` and `ConnectionPatch` objects takes nearly 200 lines of tedious coordinate math per diagram.
- Drawlib wraps the rendering engine in a clean, type-validated, domain-aware Python API where 15 lines of declarative code replace 180 lines of boilerplate.
:::
