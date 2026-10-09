# Styles & Theming

In complex technical diagrams, manually configuring RGB tuples, stroke widths, and font weights on every drawing call leads to visual inconsistency and brittle code.
Drawlib solves this with a **unified design token system** in `drawlib.styles` and `drawlib.preset_styles`.

---

## 1. Overview of Semantic Styles & Variants



<figure class="drawlib-image" style="text-align: center;">
  <img src="styles_images/styles_overview.png" alt="styles_1" style="width: 650px; max-width: 100%;" />
  <figcaption class="drawlib-caption">Overview of Semantic Style Tokens and Orthogonal Variants</figcaption>
</figure>

<details class="drawlib-code-details">
<summary>Source Code</summary>

```python
from drawlib.canvas import save, setup
from drawlib.shapes import rectangle
from drawlib.styles import Styles

setup(width=140, height=54)

# Row 1: Core Semantic Card & Hero Roles
rectangle((26, 38), width=34, height=18, style=Styles.PrimaryFlat.patch(shape_r=2), text="PrimaryFlat\n(Hero Focal)", text_style=Styles.WhiteBold.patch(text_size=10))
rectangle((70, 38), width=34, height=18, style=Styles.Neutral.patch(shape_r=2), text="Neutral\n(50%+ Baseline)", text_style=Styles.DarkBold.patch(text_size=10))
rectangle((114, 38), width=34, height=18, style=Styles.SecondaryNeutral.patch(shape_r=2), text="SecondaryNeutral\n(Auxiliary Card)", text_style=Styles.DarkBold.patch(text_size=10))

# Row 2: Structural & Status Variants
rectangle((26, 15), width=34, height=18, style=Styles.SuccessNeutral.patch(shape_r=2), text="SuccessNeutral\n(Verified State)", text_style=Styles.DarkBold.patch(text_size=10))
rectangle((70, 15), width=34, height=18, style=Styles.DangerFlat.patch(shape_r=2), text="DangerFlat\n(Critical Alert)", text_style=Styles.WhiteBold.patch(text_size=10))
rectangle((114, 15), width=34, height=18, style=Styles.MutedDashed.patch(shape_r=2), text="MutedDashed\n(VPC / Boundary)", text_style=Styles.DarkBold.patch(text_size=10))

save()
```

</details>



---

## 2. Centralized `styles.py` Architecture

Drawlib separates **active project tokens** (`drawlib.styles`) from **immutable factory catalogs** (`drawlib.preset_styles` and `drawlib.preset_colors`):

```python
# Recommended in all drawing scripts and markdown blocks:
from drawlib.styles import Colors, Styles
```

| Import Pattern | Module | Behavior & Use Case |
| :--- | :--- | :--- |
| `from drawlib.styles import Colors, Styles` | `drawlib.styles` | **Recommended.** References the active project theme. Automatically reflects overrides defined in your project's `styles.py` or passed via `--styles`. |
| `from drawlib.preset_styles import DefaultStyles, GoogleStyles, MonochromeStyles` | `drawlib.preset_styles` | Static factory catalogs. Used inside `styles.py` to select a base theme or compare multiple themes side by side. |

> [!IMPORTANT]
> Always import PascalCase `Styles` and `Colors` from `drawlib.styles`. Never use lowercase `styles` or `colors` variables, which would shadow the `drawlib.styles` module.

### Customizing Project-Wide Defaults in `styles.py`

Every project scaffolded with `drawlib init` includes a root `styles.py` file. When `drawlib build` or `drawlib show` runs, Drawlib loads `styles.py` and binds its `Styles` and `Colors` objects into `drawlib.styles`:

```python
# styles.py
from drawlib.fonts import FontRoboto
from drawlib.preset_colors import GoogleColors
from drawlib.preset_styles import GoogleStyles

Colors = GoogleColors()
Styles = GoogleStyles().patch_font(
    regular=FontRoboto.ROBOTO_REGULAR,
    bold=FontRoboto.ROBOTO_BOLD,
    thin=FontRoboto.ROBOTO_THIN,
)
```



<figure class="drawlib-image" style="text-align: center;">
  <img src="styles_images/styles_centralized_architecture.png" alt="styles_2" style="width: 650px; max-width: 100%;" />
  <figcaption class="drawlib-caption">Centralized styles.py Theme and Token Architecture</figcaption>
</figure>

<details class="drawlib-code-details">
<summary>Source Code</summary>

```python
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles

setup(width=148, height=44)

stages = [
    (21, Styles.Neutral, "Immutable Presets\n(preset_colors,\npreset_styles, fonts)", Styles.DarkBold),
    (58, Styles.SecondaryNeutral, "Project Root styles.py\n(Global Theme &\nFont Patching)", Styles.DarkBold),
    (95, Styles.PrimaryFlat, "Runtime Singleton\n(drawlib.styles:\nColors, Styles)", Styles.WhiteBold),
    (131, Styles.PrimaryNeutral, "Markdown Blocks &\nDrawing Scripts\n(Single Source)", Styles.DarkBold),
]

for cx, st, label, txt_st in stages:
    rectangle(
        (cx, 22),
        width=30,
        height=26,
        style=st.patch(shape_r=2),
        text=label,
        text_style=txt_st.patch(text_size=8.0),
    )

for x1, x2 in [(36, 43), (73, 80), (110, 116)]:
    line((x1, 22), (x2, 22), arrow_head="->", style=Styles.DarkBold)

save()
```

</details>



---

## 3. The Unified `Style` Token Model

Rather than fragmenting styling across separate `ShapeStyle`, `LineStyle`, `TextStyle`, `IconStyle`, and `ImageStyle` classes, Drawlib uses a single immutable **`Style`** class (`from drawlib.types import Style`) with domain-prefixed attributes and explicit target support (`supports={"shape", "line", "text", "icon", "image"}`):

| Target Domain | `Style` Attribute | Type | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Shapes** (`"shape"`) | `shape_fill_color` | `Color \| tuple \| str` | Theme fill | Interior fill color of the shape (`Colors.Transparent` for wireframe). |
| | `shape_line_color` | `Color \| tuple \| str` | Theme border | Perimeter border stroke color. |
| | `shape_line_width` | `float` | `1.5` (`0.0` Flat) | Perimeter border stroke width in points. |
| | `shape_line_style` | `"solid" \| "dashed" \| "dotted" \| "dashdot"` | `"solid"` | Perimeter border dash pattern. |
| | `shape_r` | `float \| tuple[float, ...]` | `0.0` | Corner rounding radius in canvas units (scalar or per-vertex tuple). |
| **Lines & Arrows** (`"line"`) | `line_color` | `Color \| tuple \| str` | Theme stroke | Connector line and arrowhead stroke color. |
| | `line_width` | `float` | `1.5` (`2.5` Bold) | Connector stroke width in points. |
| | `line_style` | `"solid" \| "dashed" \| "dotted" \| "dashdot"` | `"solid"` | Connector stroke dash pattern. |
| | `line_arrow_head_fill` | `bool` | `False` | `False` = open stick arrow (`->`); `True` = solid filled triangle (`-\|>`). |
| | `line_arrow_head_scale` | `float` | `20.0` | Physical size multiplier for terminal arrowheads. |
| **Text & Badges** (`"text"`) | `text_color` | `Color \| tuple \| str` | Theme text | Character glyph fill color. |
| | `text_size` | `float \| str` | `16.0` | Font size in points or `"small"`, `"medium"`, `"large"`. |
| | `text_font` | `FontBase \| FontFile` | `Font.SANSSERIF_REGULAR` | Font family and weight token from [`drawlib.fonts`](fonts.md). |
| | `text_line_spacing` | `float` | `1.2` | Vertical line height multiplier for multi-line `\n` strings. |
| | `text_flip` | `bool` | `False` | Rotates embedded shape text by `180°` to prevent upside-down labels. |
| | `text_bg_fill_color` | `Color \| tuple \| str` | `None` | Padded background badge fill color behind text. |
| | `text_bg_line_color` | `Color \| tuple \| str` | `None` | Background badge border stroke color. |
| | `text_bg_line_width` | `float` | `1.0` | Background badge border stroke width (`0` for borderless). |
| | `text_bg_line_style` | `"solid" \| "dashed" \| "dotted" \| "dashdot"` | `"solid"` | Background badge border dash pattern. |
| **Icons** (`"icon"`) | `icon_color` | `Color \| tuple \| str` | Theme icon | Vector glyph fill/stroke color (`phosphor`, `font_icon`). |
| | `icon_style` | `"thin" \| "light" \| "regular" \| "bold" \| "fill"` | `"regular"` | Typographic weight for Phosphor vector icons. |
| **Images** (`"image"`) | `image_tint_color` | `Color \| tuple \| str` | `None` | Fills transparent background pixels of the image with a solid color. |
| | `image_border_color` | `Color \| tuple \| str` | `(0, 0, 0)` | Rectangular border stroke color around the image bounds. |
| | `image_border_width` | `float` | `0.0` | Rectangular border stroke width in points (`> 0` enables border). |
| | `image_border_style` | `"solid" \| "dashed" \| "dotted" \| "dashdot"` | `"solid"` | Rectangular border dash pattern around the image. |
| **Shared Transforms** | `halign` | `"left" \| "center" \| "right"` | `"center"` | Horizontal anchor alignment relative to `xy[0]`. |
| | `valign` | `"bottom" \| "center" \| "top"` | `"center"` | Vertical anchor alignment relative to `xy[1]`. |
| | `xy_shift` | `tuple[float, float]` | `None` | Relative `(dx, dy)` coordinate shift rotated with `angle`. |
| | `xy_abs_shift` | `tuple[float, float]` | `None` | Absolute `(dx, dy)` coordinate shift independent of `angle`. |
| | `angle` | `float` | `0.0` | Counter-clockwise rotation angle in degrees around anchor `xy`. |
| | `alpha` | `float` | `1.0` | Overall element opacity (`0.0` transparent to `1.0` opaque). |

### 3.2. Non-Mutating Derivation (`.patch()`)

`Style` instances are frozen Pydantic models (similar to frozen dataclasses with `dataclasses.replace`). To customize a preset token without mutating global state, call `.patch()`:



```python
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=126, height=48)

rectangle((63, 24), width=116, height=38, style=Styles.Neutral.patch(shape_r=2))

# 1. Original preset remains completely unchanged
rectangle(
    (28, 24),
    width=36,
    height=22,
    style=Styles.Primary,
    text="Styles.Primary\n(Original Preset)",
    text_style=Styles.WhiteBold.patch(text_size=9),
)

# 2. Derive a custom card & connector style via .patch()
highlight_card = Styles.Primary.patch(
    shape_r=4,
    shape_line_width=2.5,
    shape_line_style="dashed",
    line_width=2.5,
    line_style="dashed",
)

line((46, 24), (78, 24), arrow_head="->", style=highlight_card)
text((62, 30), ".patch()", style=Styles.DarkBold.patch(text_size=8.5))

rectangle(
    (97, 24),
    width=38,
    height=22,
    style=highlight_card,
    text="highlight_card\n(shape_r=4, dashed)",
    text_style=Styles.WhiteBold.patch(text_size=9),
)

save()
```

<figure class="drawlib-image" style="text-align: center;">
  <img src="styles_images/styles_unified_token_domains.png" alt="styles_3" style="width: 600px; max-width: 100%;" />
  <figcaption class="drawlib-caption">Deriving Custom Styles with .patch() Without Mutating Presets</figcaption>
</figure>




---

## 4. Complete Variant Naming Matrix

Every semantic role (`Primary`, `Secondary`, `Accent`, `Warning`, `Danger`, `Success`, `Neutral`, `Muted`, `Light`, `Dark`) and named hue (`Blue`, `Green`, `Red`, `Orange`, `Amber`, `Purple`, `Teal`, `Pink`, `Gray1`..`Gray8`) provides orthogonal visual variants following the grammar **`Styles.<RoleOrColor><Variant><Weight>`**:

| Variant Pattern | Example Token | Shape Fill | Shape / Line Stroke | Line Style | Font & Icon Weight |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`<Role>` / `<Role>Bordered`** | `Styles.Primary` | Role color | Dark border (`1.5`) | `"solid"` | Regular (`16pt`) |
| **`<Role>Bold`** | `Styles.PrimaryBold` | Role color | Heavy stroke (`2.5`) | `"solid"` | Bold font & `"bold"` icon |
| **`<Role>Thin`** | `Styles.PrimaryThin` | Role color | Hairline stroke (`0.75`) | `"solid"` | Thin font & `"thin"` icon |
| **`<Role>Flat`** | `Styles.PrimaryFlat` | Role color | Borderless (`0.0`) | `"solid"` | Regular (or `"fill"` icon) |
| **`<Role>Neutral`** | `Styles.PrimaryNeutral` | Tone 1 pastel | Tone 3 border (`1.5`) | `"solid"` | Tone 6 high-contrast text |
| **`<Role>NeutralFlat`** | `Styles.PrimaryNeutralFlat` | Tone 1 pastel | Borderless (`0.0`) | `"solid"` | Tone 6 high-contrast text |
| **`<Role>Outline` / `<Role>Solid`** | `Styles.PrimaryOutline` | Transparent | Role color (`1.5`) | `"solid"` | Shape/line outline only |
| **`<Role>OutlineBold` / `SolidBold`** | `Styles.PrimarySolidBold` | Transparent | Role color (`2.5`) | `"solid"` | Heavy wireframe / connector |
| **`<Role>OutlineThin` / `SolidThin`** | `Styles.PrimarySolidThin` | Transparent | Role color (`0.75`) | `"solid"` | Subtle wireframe / connector |
| **`<Role>Dashed` (`Bold` / `Thin`)** | `Styles.MutedDashed` | Transparent | Role color (`1.5`) | `"dashed"` | VPC / cluster boundary |
| **`<Role>Dotted` (`Bold` / `Thin`)** | `Styles.WarningDotted` | Transparent | Role color (`1.5`) | `"dotted"` | Ephemeral / fallback link |



```python
from drawlib.canvas import save, setup
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=140, height=62)

# Row 1: Filled & Tinted Card Variants
row1 = [
    (20, Styles.Neutral, "Neutral", Styles.DarkBold),
    (53, Styles.PrimaryNeutral, "PrimaryNeutral", Styles.DarkBold),
    (86, Styles.PrimaryFlat, "PrimaryFlat", Styles.WhiteBold),
    (119, Styles.PrimaryBold, "PrimaryBold", Styles.WhiteBold),
]
for x, st, label, txt_st in row1:
    rectangle((x, 44), width=28, height=18, style=st.patch(shape_r=2), text=label, text_style=txt_st.patch(text_size=9))

# Row 2: Wireframe / Stroke Variants (Outline/Solid, Dashed, Dotted)
row2 = [
    (20, Styles.PrimarySolid, "PrimarySolid"),
    (53, Styles.PrimarySolidBold, "SolidBold"),
    (86, Styles.MutedDashed, "MutedDashed"),
    (119, Styles.PrimaryDottedBold, "DottedBold"),
]
for x, st, label in row2:
    rectangle((x, 18), width=28, height=18, style=st.patch(shape_r=2))
    text((x, 18), label, style=Styles.DarkBold.patch(text_size=9))

save()
```

<figure class="drawlib-image" style="text-align: center;">
  <img src="styles_images/styles_variant_matrix.png" alt="styles_4" style="width: 650px; max-width: 100%;" />
  <figcaption class="drawlib-caption">Visual Matrix of Drawlib Style Variants (Neutral, Flat, Bordered, Solid, Dashed, Dotted)</figcaption>
</figure>



---

## 5. Preset Theme Catalogs (`drawlib.preset_styles`)

Drawlib ships with **9 preset style classes** across three design families in `drawlib.preset_styles`:

| Theme Class | CLI `--styles` Name | Description |
| :--- | :--- | :--- |
| **`DefaultStyles`** | `default` | Standard balanced tech theme (centered on Tone 4 semantic colors with calm Tone 1–2 neutral cards). |
| **`DefaultStyles1` .. `DefaultStyles6`** | `1` .. `6` (`light`, `dark`) | Tone-shifted variants of `DefaultStyles` anchored on Tone 1 (ultra-light pastel) through Tone 6 (deepest shade). |
| **`GoogleStyles`** | `google` | Google Workspace & Slides Material palette (Google Blue, Purple, Orange, Green, Red, Yellow). |
| **`MonochromeStyles`** | `monochrome` | High-contrast grayscale catalog (`Primary`, `Secondary`, `Accent`, `Neutral`, `Muted`) for academic papers, patents, and print. |



```python
from drawlib.canvas import save, setup
from drawlib.preset_styles import DefaultStyles, GoogleStyles, MonochromeStyles
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=140, height=64)

themes = [
    (26, "DefaultStyles", DefaultStyles()),
    (70, "GoogleStyles", GoogleStyles()),
    (114, "MonochromeStyles", MonochromeStyles()),
]

for cx, title, theme in themes:
    # Boundary container
    rectangle((cx, 32), width=38, height=50, style=theme.MutedDashed.patch(shape_r=2))
    text((cx, 51), title, style=Styles.DarkBold.patch(text_size=10))

    # Hero node (PrimaryFlat)
    rectangle((cx, 36), width=30, height=12, style=theme.PrimaryFlat.patch(shape_r=1.5), text="Hero Node", text_style=theme.WhiteBold.patch(text_size=9))

    # Supporting neutral card (SecondaryNeutral)
    rectangle((cx, 18), width=30, height=12, style=theme.SecondaryNeutral.patch(shape_r=1.5), text="Neutral Card", text_style=theme.DarkBold.patch(text_size=9))

save()
```

<figure class="drawlib-image" style="text-align: center;">
  <img src="styles_images/styles_theme_comparison.png" alt="styles_5" style="width: 650px; max-width: 100%;" />
  <figcaption class="drawlib-caption">Side-by-Side Comparison of DefaultStyles, GoogleStyles, and MonochromeStyles</figcaption>
</figure>


