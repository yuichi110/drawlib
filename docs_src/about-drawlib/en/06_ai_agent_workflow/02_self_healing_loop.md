::: block xy=(1700, 1008) width=140 height=32
```drawlib file=page.svg
import utils
utils.draw_page_number()
```
:::

::: block xy=(80, 1010) width=900 height=30 font_size=15px
*Drawlib — Illustration & Documentation as Code*
:::

::: block xy=(80, 36) width=1760 height=72
# Autonomous Multimodal Verification Loop
:::

::: block xy=(80, 130) width=1760 height=115
- **On-Demand Context**: AI agents (Gemini, Claude Code, Cursor) query exact API specs via `uv run drawlib rules show <topic>`.
- **Visual Self-Correction**: Agents inspect `-g` coordinate grid previews multimodally and fix overlaps before publishing.
:::

::: block xy=(80, 260) width=1760 height=685
```drawlib file=ai_self_healing_loop.svg
from drawlib.canvas import clear, save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.smartarts import Panel
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=176, height=68)

# Upper 4-step pipeline + final verified exit card
steps = [
    {
        "x": 2.0,
        "w": 30.0,
        "header": "1. Query Rules",
        "cmd": "drawlib rules show",
        "desc": "Fetch exact API &\nslide layout specs\nwith zero bloat",
        "icon": phosphor.book_open,
        "featured": False,
    },
    {
        "x": 36.2,
        "w": 30.0,
        "header": "2. Author Code",
        "cmd": "Write Python / MD",
        "desc": "Compose SmartArts,\nDiagrams & typed\n::: block layouts",
        "icon": phosphor.code,
        "featured": False,
    },
    {
        "x": 70.4,
        "w": 30.0,
        "header": "3. Grid Preview",
        "cmd": "drawlib show -g",
        "desc": "Render headless PNG\nwith (X, Y) rulers\nin < 1 second",
        "icon": phosphor.squares_four,
        "featured": False,
    },
    {
        "x": 104.6,
        "w": 32.0,
        "header": "4. Vision Check",
        "cmd": "Multimodal Inspect",
        "desc": "Verify margins,\ntext_size balance\n& zero overlaps",
        "icon": phosphor.robot,
        "featured": True,
    },
]

card_y = 26.5
card_h = 39.0

for idx, s in enumerate(steps):
    x0 = s["x"]
    w = s["w"]
    cx = x0 + w / 2.0
    feat = s["featured"]

    p = Panel(
        s["header"],
        style=(Styles.PrimaryNeutral if feat else Styles.White).patch(shape_r=2.0),
        header_style=Styles.PrimaryFlat if feat else Styles.SecondaryNeutral,
        text_style=(Styles.WhiteBold if feat else Styles.DarkBold).patch(text_size=13.2),
        header_variant="filled",
        header_height=8.4,
        header_align="center",
    )
    p.draw(xy=(x0, card_y), width=w, height=card_h)

    circle(
        (cx, 50.2),
        radius=4.4,
        style=Styles.WhiteFlat if feat else Styles.PrimaryNeutral,
    )
    s["icon"]((cx, 50.2), width=5.0, style=Styles.PrimaryBold)

    rectangle(
        (cx, 41.2),
        width=w - 3.6,
        height=5.2,
        style=(Styles.PrimaryFlat if feat else Styles.Neutral).patch(shape_r=1.2),
    )
    text(
        (cx, 41.2),
        s["cmd"],
        style=(Styles.WhiteBold if feat else Styles.PrimaryBold).patch(text_size=11.0),
    )

    text((cx, 32.5), s["desc"], style=Styles.Dark.patch(text_size=11.2))

    if idx < 3:
        nx = steps[idx + 1]["x"]
        line((x0 + w + 0.3, 46.0), (nx - 0.3, 46.0), arrow_head="->", style=Styles.PrimaryBold)

# Exit arrow -> Verified Artifact card
line((136.9, 46.0), (143.7, 46.0), arrow_head="->", style=Styles.SuccessBold)
text((140.3, 49.2), "Pass", style=Styles.SuccessBold.patch(text_size=11.2))

exit_x = 144.0
exit_w = 30.0
exit_cx = exit_x + exit_w / 2.0
exit_panel = Panel(
    "Verified Output",
    style=Styles.White.patch(shape_r=2.0),
    header_style=Styles.SuccessFlat,
    text_style=Styles.WhiteBold.patch(text_size=13.2),
    header_variant="filled",
    header_height=8.4,
    header_align="center",
)
exit_panel.draw(xy=(exit_x, card_y), width=exit_w, height=card_h)
circle((exit_cx, 50.2), radius=4.6, style=Styles.SecondaryNeutral)
phosphor.check_circle((exit_cx, 50.2), width=5.4, style=Styles.SuccessBold)
rectangle((exit_cx, 41.2), width=26.2, height=5.2, style=Styles.SecondaryNeutral.patch(shape_r=1.2))
text((exit_cx, 41.2), "✓ Ready to Publish", style=Styles.DarkBold.patch(text_size=11.0))
text(
    (exit_cx, 32.5),
    "Compile crisp HTML,\nVector PDF, DOCX\n& 16:9 PPTX",
    style=Styles.Dark.patch(text_size=11.2),
)

# Step 5: Bottom Feedback Self-Correction Loop (4 -> 5 -> 2)
loop_x = 57.5
loop_w = 57.5
loop_y = 3.5
loop_h = 16.5
loop_cy = loop_y + loop_h / 2.0

# Orthogonal path from Step 4 bottom (123.5, 26.5) -> (115.0, 11.75)
line((123.5, 26.5), (123.5, loop_cy), style=Styles.WarningBold)
line((123.5, loop_cy), (loop_x + loop_w + 0.4, loop_cy), arrow_head="->", style=Styles.WarningBold)
text((126.5, 14.8), "Overlap / Clipping Found", style=Styles.DarkBold.patch(text_size=11.0, halign="left"))

# Step 5 Card
rectangle((loop_x + loop_w / 2.0, loop_cy), width=loop_w, height=loop_h, style=Styles.SecondaryNeutral.patch(shape_r=2.0))
circle((loop_x + 6.5, loop_cy), radius=4.2, style=Styles.WhiteFlat)
phosphor.arrows_clockwise((loop_x + 6.5, loop_cy), width=4.8, style=Styles.PrimaryBold)
text(
    (loop_x + 12.5, loop_cy + 3.2),
    "5. Self-Correct Coordinates",
    style=Styles.DarkBold.patch(text_size=12.8, halign="left"),
)
text(
    (loop_x + 12.5, loop_cy - 2.6),
    "Refine (x, y) & text_size via -g rulers",
    style=Styles.Dark.patch(text_size=11.0, halign="left"),
)

# Orthogonal return path from Step 5 left (57.5, 11.75) -> Step 2 bottom (51.2, 26.5)
line((loop_x, loop_cy), (51.2, loop_cy), style=Styles.PrimaryBold)
line((51.2, loop_cy), (51.2, card_y - 0.4), arrow_head="->", style=Styles.PrimaryBold)
text((49.2, 17.5), "Iterate", style=Styles.PrimaryBold.patch(text_size=11.2, halign="right"))

save()
```
:::

::: note
Why do traditional diagramming tools fail with AI agents? Raw XML formats like `.drawio` or `.pptx` are opaque token walls, while static DSLs give agents zero visibility into rendered text collisions.
Drawlib closes the loop in five deterministic steps:
1. **`drawlib rules show`**: Instead of stuffing thousands of lines into the system prompt, the agent loads only the specific SmartArt or Diagram guide it needs on demand.
2. **Write Python / Markdown**: The agent composes clean, typed Python code and `::: block` coordinates.
3. **`drawlib show -g`**: Drawlib renders a headless PNG overlaid with explicit Cartesian `(X, Y)` coordinate rulers in under a second.
4. **Multimodal Inspection**: Vision-capable models inspect the actual rendered image for margin balance, `text_size` legibility, and clipping.
5. **Self-Correct Coordinates**: Whenever an overlap is spotted, the agent reads the exact coordinate delta off the `-g` grid and patches `(x, y)` before compiling the final verified artifact.
:::
