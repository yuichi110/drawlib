# 5. Styling System, Design Tokens & Universal Fonts

Drawlib decouples coordinate geometry from visual presentation through immutable `Style` and `Color` models, semantic design tokens (`Styles.*` and `Colors.*`), and an on-demand multilingual font engine (`drawlib.fonts`) that renders Latin, monospace, and CJK scripts identically across every machine.

```drawlib align=center code=fold file=style_tokens_matrix.png caption="Figure 5.1: GoogleStyles Token Matrix — Neutral Surfaces, Outline/Role Tokens, Focal Solids, and Stroke Variants"
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=144, height=74)

row_hdr = Styles.DarkBold.patch(text_size=10.2, halign="left")
dark_lbl = Styles.DarkBold.patch(text_size=10.0)
white_lbl = Styles.WhiteBold.patch(text_size=10.0)
xs = [45.5, 72.2, 98.9, 125.6]
sw_w, sw_h = 24.2, 10.8

# Row 1: Neutral Foundations (>= 50% of every diagram)
text((6.0, 61.0), "1. Neutral Base\n   (>= 50% Rule)", style=row_hdr)
r1 = [
    ("Neutral", Styles.Neutral),
    ("PrimaryNeutral", Styles.PrimaryNeutral),
    ("SecondaryNeutral", Styles.SecondaryNeutral),
    ("White", Styles.White),
]
for cx, (name, st) in zip(xs, r1):
    rectangle((cx, 61.0), width=sw_w, height=sw_h, style=st.patch(shape_r=1.8), text=name, text_style=dark_lbl)

# Row 2: Outline & Role Tokens
text((6.0, 44.5), "2. Outline & Role\n   (*Outline / *)", style=row_hdr)
r2 = [
    ("PrimaryOutline", Styles.PrimaryOutline, Styles.PrimaryBold.patch(text_size=10.0)),
    ("SecondaryOutline", Styles.SecondaryOutline, Styles.SecondaryBold.patch(text_size=10.0)),
    ("AccentOutline", Styles.AccentOutline, Styles.DarkBold.patch(text_size=10.0)),
    ("Primary", Styles.Primary, white_lbl),
]
for cx, (name, st, ts) in zip(xs, r2):
    rectangle((cx, 44.5), width=sw_w, height=sw_h, style=st.patch(shape_r=1.8), text=name, text_style=ts)

# Row 3: Focal Solid Tokens (*Flat + WhiteBold)
text((6.0, 28.0), "3. Focal Solids\n   (*Flat + White)", style=row_hdr)
r3 = [
    ("PrimaryFlat", Styles.PrimaryFlat),
    ("AccentFlat", Styles.AccentFlat),
    ("SuccessFlat", Styles.SuccessFlat),
    ("DangerFlat", Styles.DangerFlat),
]
for cx, (name, st) in zip(xs, r3):
    rectangle((cx, 28.0), width=sw_w, height=sw_h, style=st.patch(shape_r=1.8), text=name, text_style=white_lbl)

# Row 4: Connector & Boundary Line Styles
text((6.0, 11.5), "4. Stroke Styles\n   (Bold / Dashed)", style=row_hdr)
r4 = [
    ("DarkBold", Styles.DarkBold),
    ("PrimaryBold", Styles.PrimaryBold),
    ("SecondaryDashed", Styles.SecondaryDashedBold),
    ("MutedDotted", Styles.MutedDottedBold),
]
for cx, (name, st) in zip(xs, r4):
    line((cx - 10.5, 14.2), (cx + 10.5, 14.2), arrow_head="->", style=st)
    text((cx, 8.2), name, style=dark_lbl)

save()
```

---

## 5.1 Dynamic Theme Injection: `drawlib.styles` vs. `preset_styles`

In every script and Markdown `drawlib` block, always import **PascalCase `Colors` and `Styles`** from `drawlib.styles`:

```python
from drawlib.styles import Colors, Styles
```

Never import lowercase `styles` or `colors` (which shadows the `drawlib.styles` module), and avoid hardcoding concrete catalogs like `GoogleStyles` inside diagram files. Instead, `drawlib.styles` acts as a dynamic runtime facade populated by your project's root `styles.py`—and optionally overridden per language by `<lang>/styles.py` (such as `ja/styles.py` for Japanese typography):

- **`DefaultStyles` / `DefaultColors`**: Balanced 6-tone chromatic palette (`DefaultStyles1` through `DefaultStyles6`) tailored for technical documentation.
- **`GoogleStyles` / `GoogleColors`**: Material and Google Workspace presentation palette (`style = "google"` in `drawlib.toml`, used throughout this guide).
- **`MonochromeStyles` / `MonochromeColors`**: High-contrast 8-step grayscale theme for print publications, academic papers, and patent drawings (plus `CssColors` for all 140 W3C named web colors).

Because every theme exposes the exact same semantic token names, switching `styles.py` from `GoogleStyles()` to `MonochromeStyles()` restyles hundreds of diagrams without changing a single line of diagram code.

---

## 5.2 Semantic Token Families & The `50%+` Neutral Discipline

Professional architecture diagrams rely on visual hierarchy rather than rainbow fills. Every built-in theme organizes tokens into semantic roles and orthogonal variant suffixes:

| Token Family / Suffix | Examples | Visual Behavior & Contrast Rule |
| :--- | :--- | :--- |
| **Neutral Foundations** | `Neutral`, `PrimaryNeutral`, `SecondaryNeutral`, `White` | Calm light/tinted card fills with subtle borders. **Ground `>= 50%` of shapes and containers in these tokens.** Always pass `text_style=Styles.DarkBold` when labeling `Styles.White`. |
| **Semantic Roles** | `Primary`, `Secondary`, `Accent`, `Warning`, `Success`, `Danger`, `Muted` | Blue (`Primary`), Purple/Indigo (`Secondary`), Orange (`Accent`), Green (`Success`), Red (`Danger`), and Gray (`Muted`), plus numbered tone scales (`Primary1` light tint through `Primary6` deep shade). |
| **Outline / Wireframe (`*Outline` / `*Solid`)** | `PrimaryOutline`, `SecondaryOutline`, `AccentOutline` | Transparent interior with a solid colored border (`1.5` width), ideal for logical zones, VPC frames, and lightweight badges. |
| **Focal Solids (`*Flat`)** | `PrimaryFlat`, `AccentFlat`, `SuccessFlat`, `DangerFlat` | Borderless saturated fills (`shape_line_width=0`). **Reserve strictly for 1–2 focal elements per diagram and pair with `Styles.WhiteBold`.** |
| **Weight & Pattern Suffixes** | `*Bold`, `*Thin`, `*Dashed`, `*Dotted` | Adjust stroke width (`Bold=2.5`, `Thin=0.75`, plus standalone `Styles.Light`) and dash pattern (`MutedDashed`, `SecondaryDashedBold`, `PrimaryDotted`). |

---

## 5.3 Immutable `.patch()`, `.patch_font()` & Universal Fonts

Every `Style` and `Color` instance is **strictly immutable**. To customize corner rounding, stroke thickness, alignment, font size, or opacity, call `.patch(...)` on an existing `Styles.*` preset rather than constructing a bare `Style(...)` from scratch. Deriving from `Styles.*` preserves coordinated font families, icon weights, arrow fills, and theme-switching compatibility:

```python
from drawlib.canvas import save, setup
from drawlib.fonts import FontFile, FontJapanese, FontMonoSpace
from drawlib.preset_styles import GoogleStyles
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles

# Locale-level font override pattern used in ja/styles.py:
JaStyles = GoogleStyles().patch_font(
    regular=FontJapanese.SANSSERIF_REGULAR,
    bold=FontJapanese.SANSSERIF_BOLD,
    thin=FontJapanese.SANSSERIF_THIN,
)
# Custom local .ttf/.otf files also work via FontFile("_assets/brand.ttf")
_ = FontFile

setup(width=120, height=36)

card_style = Styles.PrimaryNeutral.patch(
    shape_r=2.8,
    shape_line_width=2.0,
    alpha=0.95,
)
mono_label = Styles.DarkBold.patch(
    text_font=FontMonoSpace.ROBOTO_MONO_BOLD,
    text_size=11.0,
    halign="center",
    valign="center",
)
glass_tint = Colors.Primary.patch(alpha=0.15)
_ = (JaStyles, glass_tint)

rectangle((60, 18), width=56, height=18, style=card_style, text="api.internal:8443", text_style=mono_label)
save()
```

`drawlib.fonts` ships universal and script-specific font families that download automatically on first use and cache locally (manageable offline via `uv run drawlib cache download --all`):

- **Universal & Western Families**: `Font` (Noto Sans/Serif covering Latin + CJK), `FontSansSerif` (Lato, Montserrat, Poppins, Oswald, Raleway), `FontSerif` (Merriweather, Playfair Display, Platypi), and `FontRoboto` (Roboto, Condensed, Slab, Serif).
- **Code & Tabular Metrics**: `FontMonoSpace` (`ROBOTO_MONO_REGULAR`, `SOURCECODEPRO_REGULAR`, `SOURCEHANCODEJP_REGULAR`) and `FontSourceCode`.
- **CJK, Regional & Custom Files**: `FontJapanese`, `FontChinese` (Simplified, Traditional, Hong Kong), `FontKorean`, `FontArabic`, `FontThai`, `FontBrahmic`, and `FontFile("_assets/custom.ttf")` for project-bundled `.ttf` / `.otf` assets.

```drawlib align=center code=fold file=typography_and_patch.png caption="Figure 5.2: Immutable .patch() Style Progression and Cached Multilingual Font Specimens"
from drawlib.canvas import save, setup
from drawlib.fonts import FontJapanese, FontMonoSpace, FontRoboto, FontSerif
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=144, height=66)

sec_hdr = Styles.DarkBold.patch(text_size=10.8, halign="left")
xs = [26.0, 72.0, 118.0]

# Top Band: .patch() transformation pipeline
text((8.5, 59.5), "A. Immutable Style.patch() Transformation Chain", style=sec_hdr)

rectangle(
    (xs[0], 46.5),
    width=35.0,
    height=15.0,
    style=Styles.Neutral,
    text="Styles.Neutral\n(Sharp Base)",
    text_style=Styles.DarkBold.patch(text_size=10.2),
)
line((44.5, 46.5), (53.5, 46.5), arrow_head="->", style=Styles.DarkBold)

rectangle(
    (xs[1], 46.5),
    width=35.0,
    height=15.0,
    style=Styles.PrimaryNeutral.patch(shape_r=3.0),
    text=".patch(shape_r=3.0)\n(Rounded Card)",
    text_style=Styles.DarkBold.patch(text_size=10.2),
)
line((90.5, 46.5), (99.5, 46.5), arrow_head="->", style=Styles.DarkBold)

rectangle(
    (xs[2], 46.5),
    width=35.0,
    height=15.0,
    style=Styles.SecondaryNeutral.patch(
        shape_r=3.0,
        shape_line_style="dashed",
        shape_line_width=2.0,
    ),
    text='+ line_style="dashed"\n(Zone Boundary)',
    text_style=Styles.DarkBold.patch(text_size=10.2),
)

# Bottom Band: Typography specimens
text((8.5, 29.0), "B. Universal & Multilingual Font Specimens (drawlib.fonts)", style=sec_hdr)

rectangle((xs[0], 15.5), width=35.0, height=16.0, style=Styles.White.patch(shape_r=2.2))
text((xs[0], 18.8), "FontSerif", style=Styles.DarkBold.patch(text_font=FontSerif.MERRIWEATHER_BOLD, text_size=11.0))
text((xs[0], 12.2), "Merriweather & Roboto", style=Styles.Dark.patch(text_font=FontRoboto.ROBOTO_REGULAR, text_size=10.0))

rectangle((xs[1], 15.5), width=35.0, height=16.0, style=Styles.Neutral.patch(shape_r=2.2))
text((xs[1], 18.8), "FontMonoSpace", style=Styles.DarkBold.patch(text_font=FontMonoSpace.ROBOTO_MONO_BOLD, text_size=10.8))
text((xs[1], 12.2), "10.0.4.12:8443", style=Styles.Dark.patch(text_font=FontMonoSpace.ROBOTO_MONO_REGULAR, text_size=10.0))

rectangle((xs[2], 15.5), width=35.0, height=16.0, style=Styles.PrimaryFlat.patch(shape_r=2.2))
text((xs[2], 18.8), "FontJapanese", style=Styles.WhiteBold.patch(text_font=FontJapanese.SANSSERIF_BOLD, text_size=11.0))
text((xs[2], 12.2), "日本語・CJK Sans", style=Styles.White.patch(text_font=FontJapanese.SANSSERIF_REGULAR, text_size=10.2))

save()
```
