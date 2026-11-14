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
# 16:9 Slide Stage, Presenter View & PPTX
:::

::: block xy=(80, 130) width=1760 height=115
- **Dual-Layer Slide Markdown**: `::: block` places crisp visuals on a `1920×1080` stage while `::: note` stores speaker scripts in Git.
- **Live Sync & Office Export**: Sync Audience Stage with `?presenter=1` Presenter View via `BroadcastChannel`, plus Vector PDF & `.pptx`.
:::

::: block xy=(80, 260) width=1760 height=685
```drawlib file=slide_dual_engine.svg
from drawlib.canvas import clear, save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.smartarts import Panel
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=176, height=68)

dots = (Styles.DangerFlat, Styles.WarningFlat, Styles.SuccessFlat)

# 1. Left Source Panel: slide_src/
src_panel = Panel(
    "slide_src/",
    style=Styles.Neutral.patch(shape_r=2.2),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=13.8),
    icon=phosphor.code,
    icon_style=Styles.PrimaryBold,
    header_variant="filled",
    header_height=8.8,
)
src_panel.draw(xy=(2.0, 4.0), width=37.0, height=61.0)

# Layer 1 box inside source
rectangle((20.5, 44.5), width=32.0, height=18.5, style=Styles.White.patch(shape_r=1.6))
phosphor.presentation_chart((8.0, 49.5), width=4.0, style=Styles.PrimaryBold)
text((11.5, 49.5), "::: block (Stage)", style=Styles.PrimaryBold.patch(text_size=12.5, halign="left"))
text(
    (6.8, 41.2),
    "1920x1080 xy=(x, y)\nInline Python SVG art",
    style=Styles.Dark.patch(text_size=11.2, halign="left"),
)

# Layer 2 box inside source
rectangle((20.5, 22.0), width=32.0, height=18.5, style=Styles.White.patch(shape_r=1.6))
phosphor.note((8.0, 27.0), width=4.0, style=Styles.SecondaryBold)
text((11.5, 27.0), "::: note (Script)", style=Styles.DarkBold.patch(text_size=12.5, halign="left"))
text(
    (6.8, 18.7),
    "Speaker script in Git\nHidden from audience",
    style=Styles.Dark.patch(text_size=11.2, halign="left"),
)

rectangle((20.5, 8.2), width=32.0, height=5.2, style=Styles.PrimaryNeutral.patch(shape_r=1.2))
text((20.5, 8.2), "1:1 EN / JA Parity", style=Styles.PrimaryBold.patch(text_size=11.2))

# Compiler routing lines
line((39.0, 45.5), (46.5, 45.5), arrow_head="->", style=Styles.PrimaryBold)
line((42.2, 45.5), (42.2, 12.8), style=Styles.PrimaryBold)
circle((42.2, 45.5), radius=0.9, style=Styles.PrimaryFlat)
line((42.2, 12.8), (46.5, 12.8), arrow_head="->", style=Styles.PrimaryBold)

# 2. Top-Center: Audience Stage Window
stage_win = Panel(
    "Audience Stage",
    style=Styles.White.patch(shape_r=2.2),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=13.2),
    dot_styles=dots,
    header_variant="window",
    header_height=8.2,
)
stage_win.draw(xy=(46.5, 25.5), width=53.0, height=39.5)

rectangle((73.0, 46.5), width=48.0, height=16.5, style=Styles.PrimaryNeutral.patch(shape_r=1.5))
phosphor.sparkle((55.0, 46.5), width=5.0, style=Styles.PrimaryBold)
text(
    (60.2, 48.8),
    "Crisp Inline Vector SVG",
    style=Styles.DarkBold.patch(text_size=12.5, halign="left"),
)
text(
    (60.2, 43.5),
    "1920x1080 zero-blur scaling",
    style=Styles.Dark.patch(text_size=11.0, halign="left"),
)

rectangle((61.0, 31.8), width=24.0, height=6.6, style=Styles.Neutral.patch(shape_r=1.2))
text((61.0, 31.8), "L Key: EN ⇄ JA", style=Styles.PrimaryBold.patch(text_size=11.2))
rectangle((86.2, 31.8), width=21.5, height=6.6, style=Styles.Neutral.patch(shape_r=1.2))
text((86.2, 31.8), "P Key: Console", style=Styles.DarkBold.patch(text_size=11.2))

# 3. BroadcastChannel Bidirectional Sync
line((99.8, 45.2), (116.2, 45.2), arrow_head="<->", style=Styles.PrimaryBold)
rectangle((108.0, 51.8), width=15.2, height=8.2, style=Styles.PrimaryFlat.patch(shape_r=1.6))
text((108.0, 53.6), "Broadcast", style=Styles.WhiteBold.patch(text_size=11.0))
text((108.0, 49.8), "Channel", style=Styles.White.patch(text_size=10.8))

# 4. Top-Right: Presenter Console (?presenter=1)
pres_win = Panel(
    "Presenter (?presenter=1)",
    style=Styles.PrimaryNeutral.patch(shape_r=2.2),
    header_style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=13.0),
    dot_styles=dots,
    header_variant="window",
    header_height=8.2,
)
pres_win.draw(xy=(116.5, 25.5), width=57.5, height=39.5)

# Current / Next thumbnails + Timer
rectangle((130.8, 49.2), width=23.5, height=11.2, style=Styles.White.patch(shape_r=1.2))
text((130.8, 51.2), "Current Slide", style=Styles.PrimaryBold.patch(text_size=11.2))
text((130.8, 46.8), "Slide 18 / 26", style=Styles.Muted.patch(text_size=10.5))

rectangle((157.8, 49.2), width=25.0, height=11.2, style=Styles.White.patch(shape_r=1.2))
text((157.8, 51.2), "Next Preview", style=Styles.DarkBold.patch(text_size=11.2))
text((157.8, 46.8), "Timer  08:42", style=Styles.PrimaryBold.patch(text_size=10.8))

# Speaker Notes Pane
rectangle((145.2, 34.0), width=52.5, height=13.5, style=Styles.White.patch(shape_r=1.4))
phosphor.note((123.2, 36.2), width=3.8, style=Styles.PrimaryBold)
text(
    (126.8, 36.4),
    "::: note Live Speaker Script",
    style=Styles.DarkBold.patch(text_size=11.8, halign="left"),
)
text(
    (126.8, 31.6),
    "Scrollable script & Q&A notes",
    style=Styles.Muted.patch(text_size=10.8, halign="left"),
)

# 5. Bottom Offline & Office Export Strip
rectangle((110.2, 12.8), width=127.5, height=17.6, style=Styles.Neutral.patch(shape_r=2.0))

# Left export: Vector PDF
rectangle((78.5, 12.8), width=59.5, height=13.2, style=Styles.White.patch(shape_r=1.5))
phosphor.file_pdf((54.0, 12.8), width=5.0, style=Styles.PrimaryBold)
text((58.5, 15.2), "1920x1080 Vector PDF", style=Styles.DarkBold.patch(text_size=12.8, halign="left"))
text((58.5, 10.2), "drawlib build pdf  •  Vector deck", style=Styles.Muted.patch(text_size=11.0, halign="left"))

# Right export: Editable PPTX
rectangle((141.8, 12.8), width=59.5, height=13.2, style=Styles.White.patch(shape_r=1.5))
phosphor.presentation((117.2, 12.8), width=5.0, style=Styles.PrimaryBold)
text((121.8, 15.2), "Editable 960x540pt .pptx", style=Styles.DarkBold.patch(text_size=12.8, halign="left"))
text((121.8, 10.2), "drawlib build pptx  •  Native slides", style=Styles.Muted.patch(text_size=11.0, halign="left"))

save()
```
:::

::: note
This very presentation deck is built with `type = "slide"`.
Every slide file uses Drawlib's Dual-Layer Markdown syntax: `::: block` positions headlines, concise bullets, and inline Python SVG diagrams onto a deterministic `1920×1080` widescreen stage, while `::: note` captures the complete speaker script right inside the same Git-tracked file.
At presentation time, pressing `P` (or opening `?presenter=1`) launches a synchronized Presenter View window over browser `BroadcastChannel`, giving the speaker current and next slide previews, an elapsed timer, and scrollable `::: note` talking points—plus instant `L`-key switching between English and Japanese.
And when conference organizers or enterprise stakeholders request offline files, `drawlib build pdf` exports a razor-sharp `1920×1080` Vector PDF while `drawlib build pptx` generates a native editable `960×540pt` Microsoft PowerPoint deck complete with speaker notes.
:::
