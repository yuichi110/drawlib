# drawlib.preset_styles & preset_colors

Built-in style theme catalogs (`DefaultStyles`, `DefaultStyles1`–`DefaultStyles6`, `GoogleStyles`, `MonochromeStyles`) and curated color palettes (`DefaultColors`, `DefaultColors1`–`DefaultColors6`, `GoogleColors`, `MonochromeColors`, `CssColors`). Configure project themes in `styles.py` via `from drawlib.preset_styles import DefaultStyles, GoogleStyles, MonochromeStyles` and `from drawlib.preset_colors import CssColors, DefaultColors, GoogleColors, MonochromeColors`.

```drawlib align=center code=fold file=06_presets_hero.png caption="Built-In Theme Catalogs (DefaultStyles, GoogleStyles, MonochromeStyles) and 6-Tone Color Scale"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.preset_styles import DefaultStyles, GoogleStyles, MonochromeStyles
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=120, height=58)

ds = DefaultStyles()
gs = GoogleStyles()
ms = MonochromeStyles()

text(
    (60.0, 52.5),
    "Built-In Theme Catalogs & 6-Tone Palettes",
    style=Styles.DarkBold.patch(text_size=12.2),
)

# Column 1: DefaultStyles
rectangle((22.5, 33.0), width=35, height=28, style=ds.Neutral.patch(shape_r=2.0))
phosphor.swatches((9.5, 42.8), width=3.6, style=ds.PrimaryBold)
text((12.5, 42.8), "DefaultStyles", style=ds.DarkBold.patch(text_size=10.8, halign="left"))
rectangle(
    (22.5, 34.5),
    width=29,
    height=7.5,
    style=ds.PrimaryFlat.patch(shape_r=1.5),
    text="PrimaryFlat",
    text_style=ds.WhiteBold.patch(text_size=10.2),
)
rectangle(
    (22.5, 24.5),
    width=29,
    height=7.5,
    style=ds.SecondaryNeutral.patch(shape_r=1.5),
    text="SecondaryNeutral",
    text_style=ds.DarkBold.patch(text_size=10.0),
)

# Column 2: GoogleStyles
rectangle((60.0, 33.0), width=35, height=28, style=gs.Neutral.patch(shape_r=2.0))
phosphor.presentation_chart((47.0, 42.8), width=3.6, style=gs.PrimaryBold)
text((50.0, 42.8), "GoogleStyles", style=gs.DarkBold.patch(text_size=10.8, halign="left"))
rectangle(
    (60.0, 34.5),
    width=29,
    height=7.5,
    style=gs.PrimaryFlat.patch(shape_r=1.5),
    text="PrimaryFlat",
    text_style=gs.WhiteBold.patch(text_size=10.2),
)
rectangle(
    (60.0, 24.5),
    width=29,
    height=7.5,
    style=gs.PrimaryNeutral.patch(shape_r=1.5),
    text="PrimaryNeutral",
    text_style=gs.DarkBold.patch(text_size=10.0),
)

# Column 3: MonochromeStyles
rectangle((97.5, 33.0), width=35, height=28, style=ms.Neutral.patch(shape_r=2.0))
phosphor.printer((84.5, 42.8), width=3.6, style=ms.DarkBold)
text((87.5, 42.8), "Monochrome", style=ms.DarkBold.patch(text_size=10.8, halign="left"))
rectangle(
    (97.5, 34.5),
    width=29,
    height=7.5,
    style=ms.PrimaryBold.patch(shape_r=1.5),
    text="PrimaryBold",
    text_style=ms.DarkBold.patch(text_size=10.2),
)
rectangle(
    (97.5, 24.5),
    width=29,
    height=7.5,
    style=ms.Gray2.patch(shape_r=1.5),
    text="Gray2 Card",
    text_style=ms.DarkBold.patch(text_size=10.0),
)

# Bottom Strip: 6-Tone Scale (DefaultColors1..6 / Blue1..6)
rectangle((60.0, 10.0), width=110, height=11.0, style=Styles.Neutral.patch(shape_r=2.0))
text((17.5, 10.0), "6-Tone Scale:", style=Styles.DarkBold.patch(text_size=10.2))
tones = [Colors.Blue1, Colors.Blue2, Colors.Blue3, Colors.Blue4, Colors.Blue5, Colors.Blue6]
for idx, tone_color in enumerate(tones, start=1):
    tx = 37.5 + (idx - 1) * 13.5
    label_style = Styles.DarkBold.patch(text_size=10.0) if idx <= 3 else Styles.WhiteBold.patch(text_size=10.0)
    swatch = Styles.NeutralFlat.patch(
        shape_fill_color=tone_color,
        shape_line_color=Colors.Gray4,
        shape_line_width=0.6,
        shape_r=1.2,
    )
    rectangle((tx, 10.0), width=12.0, height=6.8, style=swatch, text=f"T{idx}", text_style=label_style)

save()
```

---

## `class` DefaultStyles

Standard preset style catalog (`drawlib.preset_styles.DefaultStyles`, subclass of [`BaseStyles`](05_styles_and_types.md)) backing `drawlib.styles.Styles` by default (`style = "default"` in `drawlib.toml`). Centered on Tone 4 (`DefaultColors4`) for semantic anchors while exposing all 6 tone levels (`Primary1`–`Primary6`, `Blue1`–`Blue6`), 8 semantic roles across 17 orthogonal variants, and calm `*Neutral` card tokens (`2,239` style tokens total).

```python
# styles.py
from drawlib.preset_colors import DefaultColors
from drawlib.preset_styles import DefaultStyles

Colors = DefaultColors()
Styles = DefaultStyles()
```

| Attribute / Token Group | Type / Count | Description |
| :--- | :--- | :--- |
| `width` / `height` / `dpi` | `140` / `70` / `100` | Default canvas dimensions and DPI. |
| `background_color` | `(255, 255, 255, 1.0)` | Opaque white canvas background. |
| `sourcecode_font` | `FontSourceCode.SOURCECODEPRO` | Default monospace syntax-highlighting font. |
| `Primary`..`Success` (8 roles) | `Style` (×17 variants each) | `""` (`Bordered`), `Bold`, `Thin`, `Flat`, `Outline` (`Solid`), `Dashed`, `Dotted` + weight combinations. |
| `*Neutral` / `*NeutralFlat` | `Style` | Calm low-saturation card styles (`Neutral`, `PrimaryNeutral`, `SecondaryNeutral`, `BlueNeutral`, `TealNeutral`, etc.). |
| **Public Methods** | Inherited from [`BaseStyles`](05_styles_and_types.md) | `patch(**kwargs)`, `patch_font(regular=None, *, bold=None, thin=None, sourcecode=None, size=None)`, `styles()`, `field_names()`, `get(key, default=None)`. |

---

## `class` DefaultStyles1

Tone-1 (ultra-light pastel) view of the default theme (`drawlib.preset_styles.DefaultStyles1`, subclass of [`BaseStyles`](05_styles_and_types.md)). Maps unnumbered semantic and chromatic tokens (`Primary`, `Secondary`, `Blue`, `Green`, etc.) directly to Tone `1` (`#e8f2ff` primary fill), suited for pastel container backdrops and low-contrast background layers.

```python
from drawlib.preset_styles import DefaultStyles1

Styles = DefaultStyles1()  # Primary fill -> #e8f2ff (Tone 1)
```

| Property | Value | Description |
| :--- | :--- | :--- |
| **Tone Level** | Tone `1` (Ultra-light pastel) | `Primary` = `#e8f2ff`, `Secondary` = `#e6fafa`, `Accent` = `#f5e8ff`. |
| **Paired Palette** | `DefaultColors1` | Exposes all `2,239` style tokens anchored at Tone `1`. |
| **Public Methods** | Inherited from [`BaseStyles`](05_styles_and_types.md) | `patch()`, `patch_font()`, `styles()`, `field_names()`, `get()`. |

---

## `class` DefaultStyles2

Tone-2 (light card background) view of the default theme (`drawlib.preset_styles.DefaultStyles2`, subclass of [`BaseStyles`](05_styles_and_types.md)). Maps base semantic and hue tokens (`Primary`, `Secondary`, `Blue`, `Teal`, etc.) to Tone `2` (`#b0c4fa` primary fill) for soft card surfaces with dark text.

```python
from drawlib.preset_styles import DefaultStyles2

Styles = DefaultStyles2()  # Primary fill -> #b0c4fa (Tone 2)
```

| Property | Value | Description |
| :--- | :--- | :--- |
| **Tone Level** | Tone `2` (Light / card background) | `Primary` = `#b0c4fa`, `Secondary` = `#9edede`, `Accent` = `#cda8f8`. |
| **Paired Palette** | `DefaultColors2` | Exposes all `2,239` style tokens anchored at Tone `2`. |
| **Public Methods** | Inherited from [`BaseStyles`](05_styles_and_types.md) | `patch()`, `patch_font()`, `styles()`, `field_names()`, `get()`. |

---

## `class` DefaultStyles3

Tone-3 (medium-soft) view of the default theme (`drawlib.preset_styles.DefaultStyles3`, subclass of [`BaseStyles`](05_styles_and_types.md)). Maps base semantic and chromatic tokens to Tone `3` (`#7891f2` primary fill) for balanced mid-tone diagrams and chart series.

```python
from drawlib.preset_styles import DefaultStyles3

Styles = DefaultStyles3()  # Primary fill -> #7891f2 (Tone 3)
```

| Property | Value | Description |
| :--- | :--- | :--- |
| **Tone Level** | Tone `3` (Medium soft) | `Primary` = `#7891f2`, `Secondary` = `#55c3c3`, `Accent` = `#a56eeb`. |
| **Paired Palette** | `DefaultColors3` | Exposes all `2,239` style tokens anchored at Tone `3`. |
| **Public Methods** | Inherited from [`BaseStyles`](05_styles_and_types.md) | `patch()`, `patch_font()`, `styles()`, `field_names()`, `get()`. |

---

## `class` DefaultStyles4

Tone-4 (standard high-contrast base) view of the default theme (`drawlib.preset_styles.DefaultStyles4`, subclass of [`BaseStyles`](05_styles_and_types.md)). Matches `DefaultStyles` (`#4862da` primary fill), providing crisp white-text contrast on `*Flat` focal cards.

```python
from drawlib.preset_styles import DefaultStyles4

Styles = DefaultStyles4()  # Equivalent tone anchor to DefaultStyles()
```

| Property | Value | Description |
| :--- | :--- | :--- |
| **Tone Level** | Tone `4` (Standard base / high contrast) | `Primary` = `#4862da`, `Secondary` = `#2a989a`, `Accent` = `#8037c3`. |
| **Paired Palette** | `DefaultColors4` | Exposes all `2,239` style tokens anchored at Tone `4`. |
| **Public Methods** | Inherited from [`BaseStyles`](05_styles_and_types.md) | `patch()`, `patch_font()`, `styles()`, `field_names()`, `get()`. |

---

## `class` DefaultStyles5

Tone-5 (deep tone) view of the default theme (`drawlib.preset_styles.DefaultStyles5`, subclass of [`BaseStyles`](05_styles_and_types.md)). Maps base semantic and chromatic tokens to Tone `5` (`#263ea0` primary fill) for executive decks and rich dark-accent callouts.

```python
from drawlib.preset_styles import DefaultStyles5

Styles = DefaultStyles5()  # Primary fill -> #263ea0 (Tone 5)
```

| Property | Value | Description |
| :--- | :--- | :--- |
| **Tone Level** | Tone `5` (Deep tone) | `Primary` = `#263ea0`, `Secondary` = `#16686c`, `Accent` = `#5c2091`. |
| **Paired Palette** | `DefaultColors5` | Exposes all `2,239` style tokens anchored at Tone `5`. |
| **Public Methods** | Inherited from [`BaseStyles`](05_styles_and_types.md) | `patch()`, `patch_font()`, `styles()`, `field_names()`, `get()`. |

---

## `class` DefaultStyles6

Tone-6 (darkest shade) view of the default theme (`drawlib.preset_styles.DefaultStyles6`, subclass of [`BaseStyles`](05_styles_and_types.md)). Maps base semantic and chromatic tokens to Tone `6` (`#12205f` primary fill) for maximum stroke contrast and deep header banners.

```python
from drawlib.preset_styles import DefaultStyles6

Styles = DefaultStyles6()  # Primary fill -> #12205f (Tone 6)
```

| Property | Value | Description |
| :--- | :--- | :--- |
| **Tone Level** | Tone `6` (Darkest shade) | `Primary` = `#12205f`, `Secondary` = `#083e41`, `Accent` = `#3a1462`. |
| **Paired Palette** | `DefaultColors6` | Exposes all `2,239` style tokens anchored at Tone `6`. |
| **Public Methods** | Inherited from [`BaseStyles`](05_styles_and_types.md) | `patch()`, `patch_font()`, `styles()`, `field_names()`, `get()`. |

---

## `class` GoogleStyles

Google Workspace, Slides, and Material-aligned preset style catalog (`drawlib.preset_styles.GoogleStyles`, subclass of [`BaseStyles`](05_styles_and_types.md); `style = "google"` in `drawlib.toml`). Exposes the full semantic role matrix plus Google-specific color tokens (`GoogleBlue`, `GoogleGreen`, `GoogleYellow`, `GoogleRed`, `CornflowerBlue`, `RedBerry`; `2,596` style tokens total).

```python
# styles.py
from drawlib.preset_colors import GoogleColors
from drawlib.preset_styles import GoogleStyles

Colors = GoogleColors()
Styles = GoogleStyles()
```

| Token Group | Representative Tokens | Description |
| :--- | :--- | :--- |
| **Semantic Roles** | `Primary` (`#4285f4`), `Secondary` (`#674ea7`), `Accent` (`#f57c00`), `Success` (`#34a853`), `Warning` (`#fbbc04`), `Danger` (`#ea4335`) | Drop-in compatible with all `Styles.*` diagram scripts. |
| **Neutral Cards** | `Neutral`, `PrimaryNeutral`, `SecondaryNeutral`, `BlueNeutral`, `GreenNeutral` | Clean light surfaces designed for Google Slides and Docs parity. |
| **Google Hue Tokens** | `GoogleBlue*`, `GoogleGreen*`, `GoogleYellow*`, `GoogleRed*`, `CornflowerBlue1..6`, `RedBerry1..6` | Full 17-variant style tokens per named Google palette hue. |
| **Public Methods** | Inherited from [`BaseStyles`](05_styles_and_types.md) | `patch()`, `patch_font()`, `styles()`, `field_names()`, `get()`. |

---

## `class` MonochromeStyles

Grayscale print, academic publication, patent, and e-ink preset style catalog (`drawlib.preset_styles.MonochromeStyles`, subclass of [`BaseStyles`](05_styles_and_types.md); `style = "monochrome"` in `drawlib.toml`). Replaces chromatic fills with high-contrast black outlines, white cards, and 8-step gray ramps (`335` style tokens total).

```python
# styles.py
from drawlib.preset_colors import MonochromeColors
from drawlib.preset_styles import MonochromeStyles

Colors = MonochromeColors()
Styles = MonochromeStyles()
```

| Token Group | Visual Resolution | Description |
| :--- | :--- | :--- |
| `Primary` / `PrimaryBold` / `PrimaryThin` | White fill + Black solid border (`1.5pt` / `2.5pt` / `0.75pt`) | Clean black-and-white wireframe cards for monochrome printing. |
| `PrimaryFlat` / `DarkFlat` | Solid Black fill (`#000000`) + `0.0pt` border | Pair with `MonochromeStyles().WhiteBold` for inverted header badges. |
| `Neutral` / `Gray1`–`Gray8` | `#f5f5f5` (`Gray1`) to `#191919` (`Gray8`) | 8 grayscale steps for hierarchical shading without color reliance. |
| **Public Methods** | Inherited from [`BaseStyles`](05_styles_and_types.md) | `patch()`, `patch_font()`, `styles()`, `field_names()`, `get()`. |

---

## `class` CssColors

Complete W3C CSS Color Module catalog (`drawlib.preset_colors.CssColors`, subclass of [`BaseColors`](05_styles_and_types.md)) providing `141` standardized named web colors (`140` CSS named colors plus `Transparent`).

```python
from drawlib.preset_colors import CssColors

colors = CssColors()
fill = colors.AliceBlue       # Color(240, 248, 255, 1.0)
stroke = colors.MidnightBlue  # Color(25, 25, 112, 1.0)
clear = colors.Transparent    # Color(0, 0, 0, 0.0)
```

| Sample Attribute | RGB / RGBA | Hex | Description |
| :--- | :--- | :--- | :--- |
| `AliceBlue` | `(240, 248, 255)` | `#f0f8ff` | Cool pale blue surface tint. |
| `CornflowerBlue` | `(100, 149, 237)` | `#6495ed` | Medium web blue accent. |
| `DarkSlateGray` | `(47, 79, 79)` | `#2f4f4f` | Deep slate text and border tone. |
| `MediumSeaGreen` | `(60, 179, 113)` | `#3cb371` | Balanced green status tone. |
| `SteelBlue` | `(70, 130, 180)` | `#4682b4` | Muted technical blue. |
| `Transparent` | `(0, 0, 0, 0.0)` | `#00000000` | Fully transparent RGBA constant. |
| **Public Methods** | Inherited from [`BaseColors`](05_styles_and_types.md) | — | `colors() -> dict[str, Color]`, `get(key, default=None)`, `patch(**kwargs)`. |

---

## `class` DefaultColors

Standard color palette class (`drawlib.preset_colors.DefaultColors`, subclass of [`BaseColors`](05_styles_and_types.md)) backing `drawlib.styles.Colors` (`149` `Color` tokens). Combines 8 chromatic 6-tone scales, 8 gray levels, semantic role anchors (Tone 4), and calm `*Neutral` card fills.

```python
from drawlib.preset_colors import DefaultColors

palette = DefaultColors()
hero_hex = palette.Primary.hex        # '#4862da'
card_fill = palette.SecondaryNeutral  # Calm teal-tinted neutral Color
```

| Token Category | Representative Tokens & Hex | Description |
| :--- | :--- | :--- |
| **Semantic Anchors** | `Primary` (`#4862da`), `Secondary` (`#2a989a`), `Accent` (`#8037c3`), `Success` (`#3a964b`), `Warning` (`#d78614`), `Danger` (`#be3a44`) | Primary role colors plus numbered `Primary1..6`..`Danger1..6`. |
| **Neutral Card Fills** | `Neutral` (`#eef2f6`), `PrimaryNeutral`, `SecondaryNeutral`, `BlueNeutral`, `TealNeutral`, `AmberNeutral` | Soft background fills engineered for high dark-text legibility. |
| **6-Tone Scales** | `Blue1..6`, `Green1..6`, `Red1..6`, `Orange1..6`, `Amber1..6`, `Purple1..6`, `Teal1..6`, `Pink1..6` | `Blue1` (`#e8f2ff`) through `Blue6` (`#12205f`). |
| **Grayscale & Basics** | `White` (`#ffffff`), `Gray1`–`Gray8`, `Black` (`#000000`), `Transparent` | Neutral structural strokes, text, and backgrounds. |
| **Public Methods** | Inherited from [`BaseColors`](05_styles_and_types.md) | `colors()`, `get(key, default=None)`, `patch(**kwargs)`. |

---

## `class` DefaultColors1

Tone-1 (ultra-light pastel) color palette class (`drawlib.preset_colors.DefaultColors1`, subclass of [`BaseColors`](05_styles_and_types.md)). Resolves unnumbered role and hue attributes (`Primary`, `Secondary`, `Blue`, `Green`, etc.) to Tone `1`.

```python
from drawlib.preset_colors import DefaultColors1

c1 = DefaultColors1()
assert c1.Primary.hex == "#e8f2ff"
```

| Sample Token | Hex | RGB | Public Methods |
| :--- | :--- | :--- | :--- |
| `Primary` / `Blue` | `#e8f2ff` | `(232, 242, 255)` | `colors()`, `get()`, `patch()` (from [`BaseColors`](05_styles_and_types.md)). |
| `Secondary` / `Teal` | `#e6fafa` | `(230, 250, 250)` | — |
| `Accent` / `Purple` | `#f5e8ff` | `(245, 232, 255)` | — |

---

## `class` DefaultColors2

Tone-2 (light card background) color palette class (`drawlib.preset_colors.DefaultColors2`, subclass of [`BaseColors`](05_styles_and_types.md)). Resolves base semantic and hue attributes to Tone `2`.

```python
from drawlib.preset_colors import DefaultColors2

c2 = DefaultColors2()
assert c2.Primary.hex == "#b0c4fa"
```

| Sample Token | Hex | RGB | Public Methods |
| :--- | :--- | :--- | :--- |
| `Primary` / `Blue` | `#b0c4fa` | `(176, 196, 250)` | `colors()`, `get()`, `patch()` (from [`BaseColors`](05_styles_and_types.md)). |
| `Secondary` / `Teal` | `#9edede` | `(158, 222, 222)` | — |
| `Accent` / `Purple` | `#cda8f8` | `(205, 168, 248)` | — |

---

## `class` DefaultColors3

Tone-3 (medium-soft) color palette class (`drawlib.preset_colors.DefaultColors3`, subclass of [`BaseColors`](05_styles_and_types.md)). Resolves base semantic and hue attributes to Tone `3`.

```python
from drawlib.preset_colors import DefaultColors3

c3 = DefaultColors3()
assert c3.Primary.hex == "#7891f2"
```

| Sample Token | Hex | RGB | Public Methods |
| :--- | :--- | :--- | :--- |
| `Primary` / `Blue` | `#7891f2` | `(120, 145, 242)` | `colors()`, `get()`, `patch()` (from [`BaseColors`](05_styles_and_types.md)). |
| `Secondary` / `Teal` | `#55c3c3` | `(85, 195, 195)` | — |
| `Accent` / `Purple` | `#a56eeb` | `(165, 110, 235)` | — |

---

## `class` DefaultColors4

Tone-4 (standard high-contrast base) color palette class (`drawlib.preset_colors.DefaultColors4`, subclass of [`BaseColors`](05_styles_and_types.md)). Matches the default tone anchors of `DefaultColors`.

```python
from drawlib.preset_colors import DefaultColors4

c4 = DefaultColors4()
assert c4.Primary.hex == "#4862da"
```

| Sample Token | Hex | RGB | Public Methods |
| :--- | :--- | :--- | :--- |
| `Primary` / `Blue` | `#4862da` | `(72, 98, 218)` | `colors()`, `get()`, `patch()` (from [`BaseColors`](05_styles_and_types.md)). |
| `Secondary` / `Teal` | `#2a989a` | `(42, 152, 154)` | — |
| `Accent` / `Purple` | `#8037c3` | `(128, 55, 195)` | — |

---

## `class` DefaultColors5

Tone-5 (deep tone) color palette class (`drawlib.preset_colors.DefaultColors5`, subclass of [`BaseColors`](05_styles_and_types.md)). Resolves base semantic and hue attributes to Tone `5`.

```python
from drawlib.preset_colors import DefaultColors5

c5 = DefaultColors5()
assert c5.Primary.hex == "#263ea0"
```

| Sample Token | Hex | RGB | Public Methods |
| :--- | :--- | :--- | :--- |
| `Primary` / `Blue` | `#263ea0` | `(38, 62, 160)` | `colors()`, `get()`, `patch()` (from [`BaseColors`](05_styles_and_types.md)). |
| `Secondary` / `Teal` | `#16686c` | `(22, 104, 108)` | — |
| `Accent` / `Purple` | `#5c2091` | `(92, 32, 145)` | — |

---

## `class` DefaultColors6

Tone-6 (darkest shade) color palette class (`drawlib.preset_colors.DefaultColors6`, subclass of [`BaseColors`](05_styles_and_types.md)). Resolves base semantic and hue attributes to Tone `6`.

```python
from drawlib.preset_colors import DefaultColors6

c6 = DefaultColors6()
assert c6.Primary.hex == "#12205f"
```

| Sample Token | Hex | RGB | Public Methods |
| :--- | :--- | :--- | :--- |
| `Primary` / `Blue` | `#12205f` | `(18, 32, 95)` | `colors()`, `get()`, `patch()` (from [`BaseColors`](05_styles_and_types.md)). |
| `Secondary` / `Teal` | `#083e41` | `(8, 62, 65)` | — |
| `Accent` / `Purple` | `#3a1462` | `(58, 20, 98)` | — |

---

## `class` GoogleColors

Google Workspace and Google Slides palette catalog (`drawlib.preset_colors.GoogleColors`, subclass of [`BaseColors`](05_styles_and_types.md); `170` `Color` tokens) paired with `GoogleStyles`.

```python
from drawlib.preset_colors import GoogleColors

gc = GoogleColors()
blue = gc.GoogleBlue    # '#4285f4'
green = gc.GoogleGreen  # '#34a853'
```

| Token Category | Representative Tokens & Hex | Description |
| :--- | :--- | :--- |
| **Brand Primaries** | `GoogleBlue` (`#4285f4`), `GoogleGreen` (`#34a853`), `GoogleYellow` (`#fbbc04`), `GoogleRed` (`#ea4335`), `GoogleOrange`, `GooglePurple`, `GoogleGray` | Official Google Workspace brand accents. |
| **Semantic Roles** | `Primary` (`#4285f4`), `Secondary` (`#674ea7`), `Accent` (`#f57c00`), `Success` (`#34a853`), `Warning` (`#fbbc04`), `Danger` (`#ea4335`), `Neutral` (`#efefef`) | Full role compatibility with `DefaultColors`. |
| **Extended 6-Tone Scales** | `CornflowerBlue1..6`, `RedBerry1..6`, `Cyan1..6`, `Magenta1..6`, `Blue1..6`, `Green1..6` | Google Slides swatch matrix ramps plus `Transparent`. |
| **Public Methods** | Inherited from [`BaseColors`](05_styles_and_types.md) | `colors()`, `get(key, default=None)`, `patch(**kwargs)`. |

---

## `class` MonochromeColors

Grayscale color palette catalog (`drawlib.preset_colors.MonochromeColors`, subclass of [`BaseColors`](05_styles_and_types.md); `37` `Color` tokens) paired with `MonochromeStyles` for black-and-white printing and patent illustrations.

```python
from drawlib.preset_colors import MonochromeColors

mc = MonochromeColors()
card = mc.Gray2   # Color(230, 230, 230, 1.0) -> '#e6e6e6'
ink = mc.Black    # Color(0, 0, 0, 1.0) -> '#000000'
```

| Token | RGB / RGBA | Hex | Visual Role |
| :--- | :--- | :--- | :--- |
| `White` / `Primary` | `(255, 255, 255)` | `#ffffff` | Pure white card and canvas fill. |
| `Gray1` / `Gray2` (`Neutral`) | `(245, 245, 245)` / `(230, 230, 230)` | `#f5f5f5` / `#e6e6e6` | Subtle shaded cards and neutral containers (`*Neutral` aliases included). |
| `Gray3` / `Gray4` / `Gray5` | `(210, 210, 210)` / `(175, 175, 175)` / `(135, 135, 135)` | `#d2d2d2` / `#afafaf` / `#878787` | Mid-gray borders, dividers, and muted zones. |
| `Gray6` / `Gray7` / `Gray8` | `(95, 95, 95)` / `(55, 55, 55)` / `(25, 25, 25)` | `#5f5f5f` / `#373737` / `#191919` | High-contrast dark strokes and secondary headings. |
| `Black` / `Transparent` | `(0, 0, 0)` / `(0, 0, 0, 0.0)` | `#000000` / `#00000000` | Primary ink stroke/text and transparent fill. |
| **Public Methods** | Inherited from [`BaseColors`](05_styles_and_types.md) | — | `colors()`, `get(key, default=None)`, `patch(**kwargs)`. |

---

## `class` Style

Re-exported style specification class (`drawlib.preset_styles.Style`) for authoring custom preset catalogs in `styles.py` with a single import. See [`Style`](05_styles_and_types.md#style) in `drawlib.styles` for full fields and methods (`.copy()`, `.patch()`).

---

## `class` Color

Re-exported immutable RGBA color class (`drawlib.preset_colors.Color`) for defining custom palette classes in `styles.py`. See [`Color`](05_styles_and_types.md#color) in `drawlib.styles` for full constructor parameters, `.hex`, and `.alpha()`.

---

## `def` get_intermediate_color(color1, color2, ratio=0.5)

Re-exported linear RGBA interpolation helper (`drawlib.preset_colors.get_intermediate_color`). See [`get_intermediate_color()`](05_styles_and_types.md#get-intermediate-color) in `drawlib.styles` for full parameter details.

---

## `def` get_intermediate_colors(color1, color2, num=1, *, include_ends=False)

Re-exported multi-step RGBA gradient generator (`drawlib.preset_colors.get_intermediate_colors`). See [`get_intermediate_colors()`](05_styles_and_types.md#get-intermediate-colors) in `drawlib.styles` for full parameter details.

