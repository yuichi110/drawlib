::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils

utils.draw_page_number()
```
:::

::: block (80, 40) (1760, 60)
# SmartArts Architecture & Unified Lifecycle
:::

::: block (80, 140) (760, 840) compact
## 10 High-Level Structured Components (`drawlib.smartarts`)

Instead of manually calculating polygon vertices and text offsets, `drawlib.smartarts` automates layout geometry for **10 essential diagram patterns**:

| Anchor Convention | SmartArt Components | Flow Direction |
| :--- | :--- | :--- |
| **Top-Left `(x, y)`** | `Table`, `TreeNode`, `BulletPoints`, `SourceCode` | Rightward (`+x`) & Downward (`-y`) |
| **Bottom-Left `(x, y)`** | `ChevronProcess`, `GridLayout`, `Pyramid` | Rightward (`+x`) & Upward (`+y`) |
| **Center `(x, y)`** | `MindMapNode`, `Cycle` *(default)* | Radial outward from center |
| **Directional `(x, y)`** | `BoxList` (`"left"`, `"right"`, `"bottom"`, `"top"`) | Along chosen axis |

### Unified 4-Phase Component Lifecycle
1. **Instantiate**: Configure default `style` and `text_style` tokens.
2. **Register (`add(..., show=True)`)**: Returns a mutable item reference.
3. **Mutate in Place**: Toggle `item.show = False` or patch `item.style` across animation frames **without shifting layout coordinates**.
4. **Render (`draw(xy, scale=1.0)`)**: Uniformly scales shapes, strokes, and fonts around `xy`.
:::

::: block (880, 140) (960, 840)
```drawlib file:smartarts_overview.svg
from drawlib.canvas import clear, save, setup
from drawlib.shapes import rectangle
from drawlib.smartarts import (
    BulletPoints,
    ChevronProcess,
    SourceCode,
    SourceCodeStyles,
)
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=96, height=84)

# Outer container card
rectangle((48, 42), width=92, height=80, style=Styles.MutedOutline.patch(shape_r=2.0))

# 1. Top Section: 4-Phase Lifecycle ChevronProcess (Bottom-Left Anchored)
text(
    (6, 77),
    "Unified 4-Phase Lifecycle (ChevronProcess)",
    style=Styles.DarkBold.patch(text_size=10, halign="left"),
)
lifecycle = ChevronProcess(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=8.5),
    description_style=Styles.Muted.patch(text_size=7.0),
    corner_angle=60.0,
    spacing=1.5,
    flat_left_end=True,
)
lifecycle.add("1. Instantiate", description="Styles & Config", style=Styles.PrimaryNeutral)
lifecycle.add("2. add(show=True)", description="Mutable Items", style=Styles.SecondaryNeutral)
lifecycle.add("3. Mutate State", description="Flip show / style", style=Styles.BlueNeutral)
lifecycle.add(
    "4. draw(scale)",
    description="Vector Render",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=8.5),
    description_style=Styles.White.patch(text_size=7.0),
)
lifecycle.draw(xy=(6, 61), width=84, height=12)

# 2. Bottom-Left Section: BulletPoints Takeaways (Top-Left Anchored)
rectangle((26, 30), width=40, height=50, style=Styles.NeutralFlat.patch(shape_r=1.5))
bp = BulletPoints(
    text_style=Styles.Dark.patch(text_size=8.5),
    vertical_margin=5.2,
    indent_width=4.2,
)
bp.set_indent(0)
bp.add("Key Architectural Benefits", text_style=Styles.DarkBold.patch(text_size=9.5))
bp.set_indent(1)
bp.add("Zero manual vertex math")
bp.add("Layout-preserving visibility:")
bp.set_indent(2)
bp.add("item.show = False hides item")
bp.add("Siblings never shift or jump")
bp.set_indent(1)
bp.add("Lazy style & text evaluation")
bp.add("Proportional scale=1.0 transform")
bp.draw(xy=(8, 50))

# 3. Bottom-Right Section: SourceCode Vector Snippet (Top-Left Anchored)
text(
    (49, 52),
    "Declarative Python API (SourceCode)",
    style=Styles.DarkBold.patch(text_size=9.5, halign="left"),
)
snippet = """from drawlib.smartarts import ChevronProcess
from drawlib.styles import Styles

proc = ChevronProcess(
    style=Styles.Neutral,
    text_style=Styles.DarkBold,
    description_style=Styles.Muted,
    flat_left_end=True,
)
s1 = proc.add("Build", description="CI")
s2 = proc.add("Deploy", style=Styles.PrimaryFlat,
              text_style=Styles.WhiteBold)

# Hide step 2 without shifting step 1:
s2.show = False
proc.draw(xy=(10, 20), width=80, scale=1.0)"""

code_styles = SourceCodeStyles.get("dark", font_lang="en", text_size=7.2)
SourceCode.draw(
    xy=(49, 48),
    width=41,
    code=snippet,
    styles=code_styles,
    code_lang="python",
    show_linenum=True,
)

save()
```
:::

::: note
- `drawlib.smartarts` provides 10 high-level graphical components that bridge the gap between low-level geometric primitives and full domain diagrams.
- Notice the **Coordinate Anchor Table** on the left:
  - Components that read top-to-bottom like text (`Table`, `TreeNode`, `BulletPoints`, `SourceCode`) anchor at their **Top-Left `(x, y)`** coordinate.
  - Structural blocks that stack or extend from a baseline (`ChevronProcess`, `GridLayout`, `Pyramid`) anchor at their **Bottom-Left `(x, y)`** coordinate.
  - Radial structures (`MindMapNode`, `Cycle`) anchor at their **Center `(x, y)`**.
- Every stateful SmartArt shares the **4-Phase Lifecycle** shown in the top `ChevronProcess`:
  1. Instantiate with base styles.
  2. Register items via `.add(..., show=True)`, which returns a mutable item object.
  3. Mutate `.show` or `.style` between frames for step-by-step slide builds without shifting other items.
  4. Call `.draw(xy, scale=1.0)` to render at any resolution or scale factor.
:::
