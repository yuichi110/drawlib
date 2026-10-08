::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils
utils.draw_page_number()
```
:::

::: block (80, 40) (1760, 60)
# Zero-Dependency Base64 Canvas Playback (`file://` Ready)
:::

::: block (80, 140) (740, 840) font:20px
## Why Standard `<img>` APNGs Fail in Slide Decks

Browsers play `<img src="anim.png">` passively with **zero JavaScript API** to pause, step, reset on slide entry, or synchronize with Presenter View—and `fetch("anim.png")` fails with CORS errors when opened via `file://`.

### Drawlib's Offline `<canvas>` Architecture
1. **Build-Time Base64 Embedding (`_assets.py`)**:
   - During `drawlib build`, the compiled APNG/WebP binary is Base64-encoded directly into `<canvas class="drawlib-anim-canvas" data-base64="...">` alongside the file in `images/`.
2. **Zero-CORS Binary Decoding (`slide.js`)**:
   - `window.atob(base64Data)` reconstructs the raw `Uint8Array` buffer in memory—working 100% offline via double-click (`file://`) without an HTTP server.
3. **Dual-Engine Frame Extractor**:
   - **Primary Path**: Hardware-accelerated WebCodecs `ImageDecoder` API extracts `ImageBitmap` frames + microsecond durations.
   - **Fallback Path**: Built-in pure-JS APNG chunk parser (`acTL`, `fcTL`, `IDAT`, `fdAT` + CRC32) composites frames onto an offscreen canvas.
:::

::: block (860, 140) (980, 840)
```drawlib file:b64_canvas_engine.svg
from drawlib.canvas import clear, save, setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=98, height=84)

# Outer background
rectangle((49, 42), width=94, height=78, r=2.5, style=Styles.Neutral)
text(
    (49, 75),
    "Offline-First Animation Compilation & Runtime Pipeline",
    style=Styles.DarkBold.patch(text_size=11.5),
)

# Phase 1: Build Time (Top)
rectangle((49, 59.5), width=86, height=21.0, r=2.0, style=Styles.PrimaryNeutral)
text((9.0, 67.5), "PHASE 1: COMPILE TIME (drawlib build)", style=Styles.PrimaryBold.patch(text_size=8.5, text_halign="left"))

rectangle(
    (20.0, 57.5),
    width=22.0,
    height=11.5,
    r=1.5,
    style=Styles.White,
    text="Python Block\nAnimation(fps=8)\n+ anim.frame()",
    text_style=Styles.DarkBold.patch(text_size=8.2),
)
rectangle(
    (49.0, 57.5),
    width=22.0,
    height=11.5,
    r=1.5,
    style=Styles.White,
    text="Binary Asset\nimages/.../anim.png\n(APNG / WebP)",
    text_style=Styles.DarkBold.patch(text_size=8.2),
)
rectangle(
    (78.0, 57.5),
    width=22.0,
    height=11.5,
    r=1.5,
    style=Styles.PrimaryFlat,
    text="Inline Base64\n<canvas data-base64>\nin index.html",
    text_style=Styles.WhiteBold.patch(text_size=8.2),
)
line((31.0, 57.5), (38.0, 57.5), arrow_head="->", style=Styles.DarkBold)
line((60.0, 57.5), (67.0, 57.5), arrow_head="->", style=Styles.DarkBold)

# Connector from Compile Time to Runtime
line((78.0, 51.5), (78.0, 44.5), arrow_head="->", style=Styles.PrimaryBold)
text((62.0, 47.8), "Works over file:// & http:// (Zero CORS)", style=Styles.PrimaryBold.patch(text_size=8.2))

# Phase 2: Browser Runtime (Bottom)
rectangle((49, 24.5), width=86, height=37.0, r=2.0, style=Styles.SecondaryNeutral)
text((9.0, 40.5), "PHASE 2: BROWSER RUNTIME (slide.js State Machine)", style=Styles.DarkBold.patch(text_size=8.5, text_halign="left"))

# Step A: atob() -> ArrayBuffer
rectangle(
    (20.0, 30.5),
    width=22.0,
    height=11.0,
    r=1.5,
    style=Styles.White,
    text="1. Memory Decode\natob(data-base64)\n-> Uint8Array",
    text_style=Styles.DarkBold.patch(text_size=8.2),
)

# Step B: Dual Decoders
rectangle(
    (49.0, 34.5),
    width=24.0,
    height=7.5,
    r=1.2,
    style=Styles.White,
    text="2a. WebCodecs ImageDecoder\n(Hardware Accelerated)",
    text_style=Styles.DarkBold.patch(text_size=7.8),
)
rectangle(
    (49.0, 25.0),
    width=24.0,
    height=7.5,
    r=1.2,
    style=Styles.White,
    text="2b. Pure-JS APNG Parser\n(fcTL / fdAT + CRC32)",
    text_style=Styles.DarkBold.patch(text_size=7.8),
)
line((31.0, 32.5), (37.0, 34.5), arrow_head="->", style=Styles.DarkBold)
line((31.0, 28.5), (37.0, 25.0), arrow_head="->", style=Styles.DarkBold)

# Step C: Frame Bitmaps + State Machine
rectangle(
    (78.0, 30.0),
    width=22.0,
    height=12.5,
    r=1.5,
    style=Styles.AccentFlat,
    text="3. <canvas> Player\nImageBitmap[]\nREADY/PLAY/PAUSE",
    text_style=Styles.WhiteBold.patch(text_size=8.2),
)
line((61.0, 34.5), (67.0, 31.5), arrow_head="->", style=Styles.DarkBold)
line((61.0, 25.0), (67.0, 28.5), arrow_head="->", style=Styles.DarkBold)

# Bottom BroadcastChannel bar
rectangle(
    (49.0, 12.5),
    width=80.0,
    height=6.5,
    r=1.2,
    style=Styles.White,
    text="BroadcastChannel('drawlib_slide_sync')  <-->  Synchronized Dual-Window Presenter View",
    text_style=Styles.DarkBold.patch(text_size=8.5),
)

save()
```
:::

::: block (80, 1010) (820, 30) font:14px
*Chapter 5: Multi-Frame Animations — Zero-Dependency Base64 Canvas Engine*
:::

::: note
- This slide explains how Drawlib achieves interactive frame-accurate animation control even when you open `index.html` directly from disk via `file://`.
- By embedding the Base64 payload (`data-base64`) on the `<canvas>` element at compile time and decoding frames in memory via WebCodecs `ImageDecoder` (with a built-in pure-JS APNG chunk parser fallback), Drawlib avoids `file://` CORS restrictions completely.
:::
