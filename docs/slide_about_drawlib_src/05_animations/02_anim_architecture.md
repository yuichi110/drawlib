::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils
utils.draw_page_number()
```
:::

::: block (80, 40) (1760, 60)
# Animation Architecture (`drawlib.anim.Animation`)
:::

::: block (80, 140) (760, 840) font:20px
## Declarative Frame Context Manager

Drawlib compiles multi-frame **APNG (`.png`)** and **Animated WebP (`.webp`)** directly from pure Python loops—with zero external video encoders required.

```python
from drawlib.anim import Animation
from drawlib.canvas import clear, save, setup
from drawlib.shapes import circle
from drawlib.styles import Styles

clear()
setup(width=100, height=40)
anim = Animation(fps=8.0, loop=0)

for idx, x in enumerate([20, 40, 60, 80]):
    is_last = idx == 3
    with anim.frame(duration=2.0 if is_last else None):
        circle((x, 20), radius=6, style=Styles.PrimaryFlat)

save("motion.png")  # APNG or Animated WebP
```

### Key Architectural Guarantees
- **Per-Frame Redraw (`clear=True` default)**: Each `with anim.frame():` clears the canvas and captures a clean snapshot on exit.
- **Per-Frame Duration Overrides**: Hold the final frame (`duration=2.0`) so viewers can absorb the completed state before looping.
- **Poster Frame Compatibility**: Frame 0 serves as the static fallback for GitHub Markdown and vector PDF exports.
:::

::: block (880, 140) (960, 840)
```drawlib file:anim_pipeline.svg
from drawlib.canvas import clear, save, setup
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=96, height=84)

# Outer pipeline container
rectangle((48, 42), width=92, height=80, style=Styles.Neutral.patch(shape_r=2.5))
text(
    (48, 77),
    "Animation Frame Capture & Encoding Pipeline",
    style=Styles.DarkBold.patch(text_size=12.5),
)

# Top Tier: Controller initialization
rectangle(
    (48, 66.5),
    width=82,
    height=9.5,
    style=Styles.PrimaryNeutral.patch(shape_r=1.8),
    text="1. Controller Init:  anim = Animation(fps=8.0, loop=0)   [Default dt = 125ms]",
    text_style=Styles.DarkBold.patch(text_size=9.5),
)

# Middle Tier: Frame snapshots captured by context manager
frame_xs = [17.0, 37.5, 58.0, 78.5]
frame_labels = ["Frame 0 (Poster)", "Frame 1", "Frame 2", "Frame 3 (Hold)"]
frame_dts = ["dt = 0.125s", "dt = 0.125s", "dt = 0.125s", "duration = 2.0s"]

for i, fx in enumerate(frame_xs):
    is_hero = i == 3
    card_style = Styles.PrimaryFlat if is_hero else Styles.White
    title_style = Styles.WhiteBold.patch(text_size=8.8) if is_hero else Styles.DarkBold.patch(text_size=8.8)
    sub_style = Styles.White.patch(text_size=8.0) if is_hero else Styles.Muted.patch(text_size=8.0)

    rectangle((fx, 43.0), width=18.5, height=24.0, style=card_style.patch(shape_r=1.5))
    text((fx, 51.5), frame_labels[i], style=title_style)

    # Mini canvas preview inside each frame card
    mini_bg = Styles.Neutral.patch(shape_fill_color=(241, 245, 249), shape_line_color=(203, 213, 225), shape_line_width=0.8)
    rectangle((fx, 42.5), width=15.0, height=10.0, style=mini_bg.patch(shape_r=0.8))
    line((fx - 5.5, 42.5), (fx + 5.5, 42.5), style=Styles.MutedDashed)
    dot_x = (fx - 5.5) + i * 3.6
    circle((dot_x, 42.5), radius=1.6, style=Styles.AccentFlat if is_hero else Styles.PrimaryFlat)

    text((fx, 34.0), frame_dts[i], style=sub_style)

    # Downward arrow from controller into frame
    line((fx, 61.5), (fx, 55.5), arrow_head="->", style=Styles.DarkBold)
    # Downward arrow from frame into encoder
    line((fx, 30.5), (fx, 24.5), arrow_head="->", style=Styles.DarkBold)

# Bottom Tier: Multi-format encoder output
rectangle(
    (28.0, 15.0),
    width=39.0,
    height=14.0,
    style=Styles.PrimaryFlat.patch(shape_r=1.8),
    text="APNG Encoder (.png)\nacTL / fcTL / fdAT Chunks + Static Frame 0",
    text_style=Styles.WhiteBold.patch(text_size=9.0),
)
rectangle(
    (69.5, 15.0),
    width=38.0,
    height=14.0,
    style=Styles.SecondaryNeutral.patch(shape_r=1.8),
    text="Animated WebP (.webp)\nLossless / Lossy Multi-Frame Container",
    text_style=Styles.DarkBold.patch(text_size=9.0),
)

save()
```
:::

::: block (80, 1010) (820, 30) font:14px
*Chapter 5: Multi-Frame Animations — Animation Context Manager & Encoding*
:::

::: note
- `Animation(fps=8.0, loop=0)` registers an animation controller with the active Drawlib canvas.
- Using `with anim.frame(duration=...):` automatically clears the canvas at the beginning of each iteration and captures a rasterized `Dimage` snapshot when the `with` block exits.
- Calling `save("file.png")` or `save("file.webp")` encodes all captured frames and per-frame durations into a single self-contained APNG or Animated WebP file.
:::
