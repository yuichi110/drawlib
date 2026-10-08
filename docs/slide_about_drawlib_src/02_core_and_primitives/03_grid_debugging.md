::: block (80, 50) (1760, 120)
# Visual Debugging with Coordinate Grid (`grid=True` / `-g`)
Inspect exact coordinates and verify margins without touching production code.
:::

::: block (80, 190) (760, 770) compact
### Two Ways to Enable the Coordinate Grid

1. **CLI Flag (`-g` / `--grid`) — Recommended**
   - Render any Python script or embedded Markdown diagram with a temporary coordinate ruler overlay:
   ```bash
   # Preview a standalone script with grid
   uv run drawlib show arch.py -g -o preview.png

   # Preview an embedded Markdown diagram with grid
   uv run drawlib show docs_src/index.md arch.png -g -o preview.png
   ```

2. **Programmatic `setup(..., grid=True)`**
   - Turn on the grid directly inside `setup()` during interactive layout design:
   ```python
   setup(width=100, height=65, grid=True, grid_xpitch=10, grid_ypitch=10)
   ```

---

### Why the Grid Matters
- **Zero Guesswork**: Immediately see that `Client` sits at `(25, 30)`, `Gateway` at `(52, 30)`, and `DB` at `(78, 30)`.
- **Multimodal AI Anchor**: Allows AI coding agents to read exact `(x, y)` coordinates directly from the rendered image.
:::

::: block (880, 180) (960, 780)
```drawlib file:grid_preview.svg
from drawlib.canvas import clear, save, setup
from drawlib.lines import line
from drawlib.shapes import cylinder, rectangle
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=100, height=65, grid=True, grid_xpitch=10, grid_ypitch=10)

# Background container aligned to grid (X: 10..90, Y: 10..55)
rectangle(
    (50, 32.5),
    width=80,
    height=45,
    r=3,
    style=Styles.PrimaryNeutral,
)
text((14, 51), "VPC Boundary: center=(50, 32.5), size=80x45", style=Styles.PrimaryBold.patch(text_size=8.5, text_halign="left"))

# Node 1 at (25, 30)
rectangle(
    (25, 30),
    width=20,
    height=14,
    r=2,
    style=Styles.Neutral,
    text="Web UI\n(25, 30)",
    text_style=Styles.DarkBold.patch(text_size=9),
)

# Node 2 at (52, 30) - Hero
rectangle(
    (52, 30),
    width=20,
    height=14,
    r=2,
    style=Styles.PrimaryFlat,
    text="Gateway\n(52, 30)",
    text_style=Styles.WhiteBold.patch(text_size=9),
)

# Node 3 at (78, 30)
cylinder(
    (78, 30),
    width=16,
    height=16,
    disks=2,
    style=Styles.SecondaryNeutral,
    text="SQL DB\n(78, 30)",
    text_style=Styles.DarkBold.patch(text_size=8.5),
)

line((35, 30), (42, 30), arrow_head="->", style=Styles.DarkBold)
line((62, 30), (70, 30), arrow_head="->", style=Styles.DarkBold)

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
- When designing or debugging a diagram layout, you never have to guess coordinates blindly.
- Passing `-g` to `drawlib show` (or `grid=True` in `setup()`) overlays a crisp coordinate grid across the canvas, showing major and minor grid lines so you can verify exact alignment and outer margins at a glance.
:::
