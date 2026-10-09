::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils
utils.draw_page_number()
```
:::

::: block (80, 40) (1760, 60)
# Presenter View, Overview Grid & Standalone Portability
:::

::: block (80, 140) (740, 840) font:20px
## Built for Live Stage Delivery & Offline Sharing

Compiled Drawlib slide decks (`slide_html/`) include a zero-dependency presentation runtime (`slide.js`) and self-contained assets:

| Shortcut | Feature | Description |
| :--- | :--- | :--- |
| **`P` / `S`** | **Presenter View** | Opens dual-window `?presenter=1` synced via `BroadcastChannel` + `postMessage`. |
| **`O` / `Esc`** | **Overview Grid** | Interactive 16:9 thumbnail grid of all slides for instant navigation. |
| **`A`** | **Animation Step** | Plays, pauses, resumes, or resets `<canvas>` animations on the current slide. |
| **`F`** | **Fullscreen** | Toggles native widescreen browser fullscreen mode. |
| **`→` / `Space`** | **Next Slide** | Advances slides (`←` / `Home` / `End` for navigation). |

### 100% Standalone `file://` & Vector PDF Portability
- **Auto-Bundled SVG Fonts (`_assets/fonts/`)**: Copies used `.ttf`/`.otf` text & icon fonts and injects `@font-face` rules into `style.css`.
- **Double-Click Ready**: Zip and share the output folder—anyone can open `index.html` directly from disk (`file://`) or print to `slide.pdf`.
:::

::: block (860, 140) (980, 840)
```drawlib file:presenter_features.svg
from drawlib.canvas import clear, save, setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=98, height=84)

rectangle((49, 42), width=94, height=78, style=Styles.Neutral.patch(shape_r=2.5))
text((49, 75), "Dual-Window Presenter View & Self-Contained Bundle Architecture", style=Styles.DarkBold.patch(text_size=11.2))

# Top Left: Audience Main Window
rectangle((26.5, 55.0), width=39.0, height=28.0, style=Styles.White.patch(shape_r=2.0))
rectangle(
    (26.5, 66.0),
    width=39.0,
    height=5.0,
    style=Styles.DarkFlat.patch(shape_r=1.0),
    text="Audience Screen (index.html — Fullscreen 'F')",
    text_style=Styles.WhiteBold.patch(text_size=7.8),
)
rectangle(
    (26.5, 52.5),
    width=34.0,
    height=17.5,
    style=Styles.PrimaryNeutral.patch(shape_r=1.2),
    text="1920 x 1080 Widescreen Stage\n• Crisp Inline Vector SVGs\n• Interactive <canvas> Animations",
    text_style=Styles.DarkBold.patch(text_size=7.8),
)

# Top Right: Presenter View Window (?presenter=1)
rectangle((71.5, 55.0), width=39.0, height=28.0, style=Styles.White.patch(shape_r=2.0))
rectangle(
    (71.5, 66.0),
    width=39.0,
    height=5.0,
    style=Styles.PrimaryFlat.patch(shape_r=1.0),
    text="Presenter View (Press 'P' — ?presenter=1)",
    text_style=Styles.WhiteBold.patch(text_size=7.8),
)
# Left thumb strip inside presenter view
rectangle((57.5, 52.5), width=8.0, height=17.5, style=Styles.Neutral.patch(shape_r=0.8), text="Slide\n Strip", text_style=Styles.MutedBold.patch(text_size=6.8))
# Right preview + timer + speaker notes inside presenter view
rectangle((75.5, 57.5), width=25.0, height=7.5, style=Styles.SecondaryNeutral.patch(shape_r=0.8), text="Live Slide Preview + Timer", text_style=Styles.DarkBold.patch(text_size=7.2))
rectangle((75.5, 48.0), width=25.0, height=9.0, style=Styles.BlueNeutral.patch(shape_r=0.8), text="::: note Speaker Notes\n+ ▶ Play Animation Button", text_style=Styles.DarkBold.patch(text_size=7.2))

# Sync Arrow between windows
line((46.0, 55.0), (52.0, 55.0), arrow_head="<->", style=Styles.PrimaryBold)
text((49.0, 58.2), "BroadcastChannel", style=Styles.PrimaryBold.patch(text_size=7.2))

# Bottom Section: Self-Contained Output Directory
rectangle((49.0, 21.5), width=84.0, height=29.0, style=Styles.PrimaryNeutral.patch(shape_r=2.0))
text((49.0, 32.5), "Zero-Dependency Output Bundle (Works Offline via file:// & Headless PDF)", style=Styles.PrimaryBold.patch(text_size=9.2))

bundle_items = [
    (20.5, "index.html + slide.js", "Inline SVGs + Base64\nAPNG/WebP + Overview ('O')", Styles.White, Styles.DarkBold),
    (49.0, "_assets/fonts/*.ttf", "Auto-Bundled SVG Fonts\n+ @font-face in style.css", Styles.PrimaryFlat, Styles.WhiteBold),
    (77.5, "slide.pdf + README.md", "1920x1080 Vector PDF\n+ Quickstart Guide", Styles.SecondaryNeutral, Styles.DarkBold),
]
for bx, b_title, b_sub, b_st, b_tst in bundle_items:
    rectangle((bx, 18.5), width=25.5, height=16.5, style=b_st.patch(shape_r=1.5))
    text((bx, 22.5), b_title, style=b_tst.patch(text_size=8.5))
    sub_c = Styles.White.patch(text_size=7.5) if b_st == Styles.PrimaryFlat else Styles.Dark.patch(text_size=7.5)
    text((bx, 15.0), b_sub, style=sub_c)

save()
```
:::

::: block (80, 1010) (820, 30) font:14px
*Chapter 6: Documentation & Slide Engine — Presenter View, Font Bundling & Portability*
:::

::: note
- Press `P` right now to see the dual-window Presenter View in action, or press `O` to open the thumbnail Overview Grid!
- When `drawlib build` compiles a slide deck, it scans every inline SVG for font metadata (`drawlib-svg-fonts`), automatically copies the required `.ttf` / `.otf` files into `_assets/fonts/`, and injects `@font-face` declarations into `style.css`.
- That means custom typography and Phosphor/FontAwesome icons render identically on any machine—even offline via `file://` or inside a headless Chromium PDF build.
:::
