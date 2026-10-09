::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils
utils.draw_page_number()
```
:::

::: block (80, 40) (1760, 60)
# 16:9 Widescreen Stage Architecture (`1920x1080`)
:::

::: block (80, 140) (740, 840) font:20px
## Dual Coordinate Systems Working in Harmony

Drawlib slides (`drawlib init slide`) combine pixel-accurate stage containers with Cartesian vector canvases:

1. **Slide Stage (`::: block (x, y) (w, h)`) — Top-Left `(0, 0)`**:
   - Fixed **1920 × 1080** pixel widescreen stage (automatically scaled to fit any browser window or projector).
   - Supports hierarchical chapter folders (`00_opening/`, `01_why_drawlib/`, ...) sorted alphabetically.
2. **Drawlib Canvas (`setup(width=W, height=H)`) — Bottom-Left `(0, 0)`**:
   - Inside any ```` ```drawlib ```` block, coordinates use standard Cartesian geometry where `(0, 0)` is the bottom-left corner.

### Golden Aspect-Ratio Rule
Keep `setup(width=W, height=H)` proportional to the enclosing `::: block` `(w, h)` (typically `w / 10, h / 10`) so inline SVGs fill their containers with zero letterboxing:
- `::: block (860, 140) (980, 840)` → `setup(width=98, height=84)`
- `::: block (0, 0) (1920, 1080)` → `setup(width=192, height=108)`
:::

::: block (860, 140) (980, 840)
```drawlib file:slide_stage_blueprint.svg
from drawlib.canvas import clear, save, setup
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=98, height=84)

# Outer blueprint background
rectangle((49, 42), width=94, height=78, style=Styles.Neutral.patch(shape_r=2.5))
text((49, 75.5), "1920 x 1080 Widescreen Stage Blueprint (Top-Left Origin)", style=Styles.DarkBold.patch(text_size=11.5))

# 16:9 Stage Frame: width=80, height=45, centered at (51, 46) -> X: 11..91, Y: 23.5..68.5
rectangle((51, 46), width=80, height=45, style=Styles.White)

# Origin (0, 0) badge at top-left of stage frame (11, 68.5)
circle((11, 68.5), radius=1.6, style=Styles.AccentFlat)
text((11, 71.2), "Stage (0, 0) Top-Left", style=Styles.PrimaryBold.patch(text_size=7.8, halign="left"))
text((91, 20.8), "(1920, 1080)", style=Styles.MutedBold.patch(text_size=7.8, halign="right"))

# Header Block: (80, 40) (1760, 60)
rectangle(
    (51, 64.2),
    width=73.5,
    height=4.2,
    style=Styles.PrimaryNeutral.patch(shape_r=0.8),
    text="::: block (80, 40) (1760, 60)  —  # Slide Heading Title",
    text_style=Styles.DarkBold.patch(text_size=7.8),
)

# Left Narrative Block: (80, 140) (740, 840)
rectangle(
    (30.0, 45.5),
    width=31.0,
    height=29.5,
    style=Styles.SecondaryNeutral.patch(shape_r=1.2),
    text="::: block (80, 140) (740, 840)\n\nMarkdown Narrative\n• Headings & Bullets\n• Code Snippets\n• Tables & Callouts",
    text_style=Styles.DarkBold.patch(text_size=8.0),
)

# Right Diagram Block: (860, 140) (980, 840) -> Canvas setup(width=98, height=84)
rectangle(
    (67.2, 45.5),
    width=40.5,
    height=29.5,
    style=Styles.PrimaryFlat.patch(shape_r=1.2),
    text="::: block (860, 140) (980, 840)\n```drawlib file:diagram.svg\nsetup(width=98, height=84)\n\nCartesian Canvas (0, 0) at Bottom-Left!",
    text_style=Styles.WhiteBold.patch(text_size=8.0),
)
# Canvas bottom-left origin indicator inside right block
circle((47.0, 30.8), radius=1.5, style=Styles.AccentFlat)
text((49.2, 32.5), "Canvas (0, 0)", style=Styles.WhiteBold.patch(text_size=7.2, halign="left"))

# Footer & Page Number Blocks
rectangle(
    (31.5, 26.8),
    width=34.0,
    height=3.2,
    style=Styles.Neutral.patch(shape_r=0.6),
    text="::: block (80, 1010) (820, 30) — Footer",
    text_style=Styles.MutedBold.patch(text_size=7.0),
)
rectangle(
    (81.5, 26.8),
    width=12.0,
    height=3.2,
    style=Styles.AccentFlat.patch(shape_r=0.6),
    text="(1700, 1010) Page#",
    text_style=Styles.WhiteBold.patch(text_size=7.0),
)

# Bottom summary card: Chapter Directory Discovery
rectangle(
    (49, 11.5),
    width=84,
    height=10.0,
    style=Styles.White.patch(shape_r=1.5),
    text="Chapter Folder Discovery:  00_opening/*.md  ->  01_why_drawlib/*.md  ->  ...  ->  07_ai_agent_workflow/*.md\nCompiled in deterministic lexical order with automatic current_slide (index / total) injection.",
    text_style=Styles.DarkBold.patch(text_size=8.2),
)

save()
```
:::

::: block (80, 1010) (820, 30) font:14px
*Chapter 6: Documentation & Slide Engine — 16:9 Widescreen Stage Architecture*
:::

::: note
- Every slide in a Drawlib deck is authored on a 1920x1080 pixel stage where `(0, 0)` is the top-left corner, while each embedded `drawlib` block uses a Cartesian `(0, 0)` bottom-left coordinate canvas.
- Dividing the container's pixel width and height by `10` (for example, `(980, 840)` -> `setup(width=98, height=84)`) guarantees an exact 1:1 aspect ratio match.
:::
