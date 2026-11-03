# drawlib.styles & drawlib.types

Dynamic theme facades (`Styles`, `Colors`), immutable styling and color models (`Style`, `Color`), linear RGBA color interpolation helpers, and extensible theme base classes (`BaseColors`, `BaseStyles`, `FontBase`). Import active tokens via `from drawlib.styles import Colors, Style, Styles` and architectural base classes via `from drawlib.types import BaseColors, BaseStyles, Color, FontBase, Style`.

```drawlib align=center code=fold file=05_styles_and_types_hero.png caption="Universal Style & Color Token System — Neutral Baseline, Focal Flat Tokens, .patch() Derivation, and Color Interpolation"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles, get_intermediate_colors
from drawlib.text import text

setup(width=120, height=58)

# Outer boundary container
rectangle((60, 29), width=112, height=50, style=Styles.MutedDashed.patch(shape_r=2.5))
phosphor.palette((11.5, 49.0), width=4.2, style=Styles.PrimaryBold)
text(
    (15.0, 49.0),
    "Style & Color Token System  (Styles · Colors · .patch())",
    style=Styles.DarkBold.patch(text_size=12.0, halign="left"),
)

# Row 1: Semantic & Neutral Token Hierarchy (50%+ neutral baseline + 1 focal hero)
rectangle((20.0, 35.5), width=24, height=13.5, style=Styles.PrimaryFlat.patch(shape_r=2.0))
phosphor.sparkle((11.5, 38.0), width=3.4, style=Styles.WhiteBold)
text((21.5, 38.0), "PrimaryFlat", style=Styles.WhiteBold.patch(text_size=10.5))
text((20.0, 32.2), "Focal Hero", style=Styles.White.patch(text_size=10.0))

rectangle((46.5, 35.5), width=24, height=13.5, style=Styles.Neutral.patch(shape_r=2.0))
text((46.5, 38.0), "Neutral", style=Styles.DarkBold.patch(text_size=10.5))
text((46.5, 32.2), "Base Card", style=Styles.Dark.patch(text_size=10.0))

rectangle((73.5, 35.5), width=24, height=13.5, style=Styles.PrimaryNeutral.patch(shape_r=2.0))
text((73.5, 38.0), "PrimaryNeutral", style=Styles.DarkBold.patch(text_size=10.2))
text((73.5, 32.2), "Tinted Card", style=Styles.Dark.patch(text_size=10.0))

rectangle((100.0, 35.5), width=24, height=13.5, style=Styles.PrimaryDashed.patch(shape_r=2.0))
text((100.0, 38.0), "PrimaryDashed", style=Styles.PrimaryBold.patch(text_size=10.2))
text((100.0, 32.2), "Zone Outline", style=Styles.Dark.patch(text_size=10.0))

# Row 2 Left: Immutable .patch() derivation
rectangle((19.5, 15.0), width=23, height=13.5, style=Styles.Neutral.patch(shape_r=2.0))
text((19.5, 17.5), "Style", style=Styles.DarkBold.patch(text_size=10.8))
text((19.5, 11.8), "Immutable", style=Styles.Dark.patch(text_size=10.0))

line((31.5, 15.0), (41.0, 15.0), arrow_head="->", style=Styles.PrimaryBold)
text((36.2, 19.2), ".patch()", style=Styles.PrimaryBold.patch(text_size=10.0))

derived_style = Styles.SecondaryNeutral.patch(
    shape_line_color=Colors.Primary,
    shape_line_width=2.2,
    shape_r=2.5,
)
rectangle((54.0, 15.0), width=25, height=13.5, style=derived_style)
text((54.0, 17.5), "Derived Style", style=Styles.DarkBold.patch(text_size=10.5))
text((54.0, 11.8), "r=2.5, w=2.2", style=Styles.Dark.patch(text_size=10.0))

# Row 2 Right: Linear RGBA color ramp via get_intermediate_colors()
rectangle((91.5, 15.0), width=41, height=13.5, style=Styles.Neutral.patch(shape_r=2.0))
text((91.5, 19.0), "get_intermediate_colors()", style=Styles.DarkBold.patch(text_size=10.0))
ramp = get_intermediate_colors(Colors.Blue1, Colors.Blue6, num=3, include_ends=True)
for idx, swatch in enumerate(ramp):
    sx = 76.3 + idx * 7.6
    swatch_style = Styles.NeutralFlat.patch(
        shape_fill_color=swatch,
        shape_line_color=Colors.Gray4,
        shape_line_width=0.6,
        shape_r=1.0,
    )
    rectangle((sx, 11.8), width=6.4, height=4.8, style=swatch_style)

save()
```

---

## `class` Color

Immutable RGBA color model (`frozen=True`) exported by `drawlib.styles`, `drawlib.types`, and [`drawlib.preset_colors`](06_presets.md). `Color` validates 8-bit integer RGB channels (`0`–`255`) and floating-point opacity (`0.0`–`1.0`), parses 3/4/6/8-digit hexadecimal strings, and supports immutable channel derivation via `.patch()`.

```python
from drawlib.styles import Color, Colors

# Construct from RGBA channels, hex string, or tuple
brand_blue = Color(26, 115, 232, alpha=1.0)
from_hex = Color.from_hex("#1a73e8", alpha=0.85)
shorthand = Color("#3498db80")

# Derive semi-transparent color without mutating the original token
backdrop = Colors.Primary.patch(alpha=0.15)
```

### Attributes & Properties

| Attribute / Property | Type | Description |
| :--- | :--- | :--- |
| `r` | `int` | Red channel (`0`–`255`). |
| `g` | `int` | Green channel (`0`–`255`). |
| `b` | `int` | Blue channel (`0`–`255`). |
| `alpha` | `float` | Opacity channel (`0.0` transparent to `1.0` opaque; default `1.0`). |
| `a` | `float` | Read-only alias for `alpha` (`0.0`–`1.0`). |
| `rgb` | `tuple[int, int, int]` | 3-tuple `(r, g, b)`. |
| `rgba` | `tuple[int, int, int, float]` | 4-tuple `(r, g, b, alpha)`. |
| `hex` | `str` | Lowercase hexadecimal string (`"#rrggbb"` when `alpha == 1.0`, else `"#rrggbbaa"`). |

### Public Methods

| Method | Signature | Description |
| :--- | :--- | :--- |
| `from_hex` | `(hexcode: str, alpha: float \| None = None) -> Color` | Classmethod parsing `"#rgb"`, `"#rgba"`, `"#rrggbb"`, or `"#rrggbbaa"` with optional `alpha` override. |
| `patch` | `(*, r: int \| None = None, g: int \| None = None, b: int \| None = None, alpha: float \| None = None) -> Color` | Return a new `Color` instance with selected channels updated. |
| `to_mplot_rgba` | `() -> tuple[float, float, float, float]` | Convert channels into normalized `(0.0..1.0)` RGBA floats for Matplotlib rendering. |

---

## `const` Colors

Active project-wide color palette singleton in `drawlib.styles` (`Colors: DefaultColors`). By default, `Colors` resolves to an instance of [`DefaultColors`](06_presets.md), and is automatically replaced whenever a project `styles.py` (or CLI `--styles` / `-s`) defines a custom `Colors` object.

```python
from drawlib.styles import Colors

border_color = Colors.Primary
subtle_fill = Colors.PrimaryNeutral
glass_tint = Colors.Blue4.patch(alpha=0.2)
```

| Token Group | Representative Tokens | Purpose |
| :--- | :--- | :--- |
| **Semantic Roles** | `Primary`, `Secondary`, `Accent`, `Warning`, `Danger`, `Success`, `Neutral`, `Muted`, `Light`, `Dark`, `Canvas` | Theme-adaptive role colors (`Primary1..6`..`Warning1..6` tone variants included). |
| **Tinted Card Fills** | `PrimaryNeutral`, `SecondaryNeutral`, `AccentNeutral`, `BlueNeutral`, `TealNeutral`, `AmberNeutral`, `GrayNeutral` | Calm, low-saturation card fills matching `Styles.*Neutral`. |
| **6-Tone Scales** | `Blue1..6`, `Green1..6`, `Red1..6`, `Orange1..6`, `Amber1..6`, `Purple1..6`, `Teal1..6`, `Pink1..6` | Chromatic scales from Tone `1` (lightest tint) to Tone `6` (darkest shade). |
| **Neutrals & Primaries** | `White`, `Gray1`–`Gray8`, `Black`, `Transparent`, `Red`, `Green`, `Blue`, `Teal`, `Navy`, `Gold` | Grayscale ramp, full transparency `(0, 0, 0, 0.0)`, and named constants. |

---

## `class` Style

Immutable universal styling model (`frozen=True`, `extra="forbid"`) exported by `drawlib.styles`, `drawlib.types`, and [`drawlib.preset_styles`](06_presets.md). Properties are segregated by target domain (`shape_*`, `line_*`, `text_*`, `icon_*`, `image_*`) alongside shared alignment and transform controls so a single `Style` token can safely configure shapes, connectors, text, icons, and images without attribute collisions.

```python
from drawlib.fonts import FontRoboto
from drawlib.styles import Colors, Style, Styles

# Derive from an existing preset token (recommended)
card_style = Styles.Neutral.patch(
    shape_line_color=Colors.Primary,
    shape_line_width=2.0,
    shape_r=2.5,
)

# Construct a standalone Style from scratch
badge_style = Style(
    shape_fill_color=Colors.Primary,
    shape_line_width=0.0,
    shape_r=3.0,
    text_color=Colors.White,
    text_font=FontRoboto.ROBOTO_BOLD,
    text_size=11.5,
)
```

### Attributes

| Attribute | Type | Description |
| :--- | :--- | :--- |
| `supports` | `frozenset[Literal["shape", "line", "text", "icon", "image"]]` | Supported drawing targets (automatically inferred from populated fields when omitted). |
| `shape_fill_color` | `Color \| tuple \| str \| None` | Shape interior fill color (`Colors.Transparent` for unfilled outlines). |
| `shape_line_color` | `Color \| tuple \| str \| None` | Shape border stroke color. |
| `shape_line_width` | `float \| None` | Shape border stroke width in points (`0.0` disables border). |
| `shape_line_style` | `Literal["solid", "dashed", "dotted", "dashdot"] \| None` | Shape border dash pattern. |
| `shape_r` | `float \| tuple[float, ...] \| None` | Corner rounding radius in canvas units (scalar for all vertices or per-vertex tuple). |
| `line_color` | `Color \| tuple \| str \| None` | Line and connector stroke color. |
| `line_width` | `float \| None` | Line stroke thickness in points. |
| `line_style` | `Literal["solid", "dashed", "dotted", "dashdot"] \| None` | Line dash pattern. |
| `line_arrow_head_fill` | `bool \| None` | Filled triangle arrowhead (`True`) or open stick arrowhead (`False`). |
| `line_arrow_head_scale` | `float \| None` | Arrowhead size scaling factor (`>= 0.0`). |
| `text_color` | `Color \| tuple \| str \| None` | Text glyph color for `text()` and embedded shape labels. |
| `text_size` | `float \| Literal["small", "medium", "large"] \| None` | Font size in points (`>= 10.0` recommended for `720pt` parity) or semantic preset size. |
| `text_font` | `FontBase \| FontFile \| None` | Font enum member from [`drawlib.fonts`](07_fonts.md) or custom `FontFile`. |
| `text_flip` | `bool \| None` | Flip embedded text orientation when rotated upside down. |
| `text_line_spacing` | `float \| None` | Multi-line vertical spacing multiplier (`>= 0.0`). |
| `text_bg_fill_color` | `Color \| tuple \| str \| None` | Background callout box fill color behind text labels. |
| `text_bg_line_color` | `Color \| tuple \| str \| None` | Border color of the text background box. |
| `text_bg_line_width` | `float \| None` | Border stroke width of the text background box in points. |
| `text_bg_line_style` | `Literal["solid", "dashed", "dotted", "dashdot"] \| None` | Border dash style of the text background box. |
| `icon_color` | `Color \| tuple \| str \| None` | Glyph color for vector font icons (`phosphor`, `font_icon`). |
| `icon_style` | `Literal["thin", "light", "regular", "bold", "fill"] \| None` | Weight/fill variant for Phosphor vector icons. |
| `image_tint_color` | `Color \| tuple \| str \| None` | Background fill or tint color behind raster images and PNG icons. |
| `image_border_color` | `Color \| tuple \| str \| None` | Frame border color around raster images and PNG icons. |
| `image_border_width` | `float \| None` | Frame border width in points around raster images and PNG icons. |
| `image_border_style` | `Literal["solid", "dashed", "dotted", "dashdot"] \| None` | Frame border dash pattern around raster images and PNG icons. |
| `halign` | `Literal["left", "center", "right"] \| None` | Horizontal anchor alignment relative to `xy`. |
| `valign` | `Literal["bottom", "center", "top"] \| None` | Vertical anchor alignment relative to `xy`. |
| `xy_shift` | `tuple[float, float] \| None` | Local coordinate shift `(dx, dy)` rotated with the element's `angle`. |
| `xy_abs_shift` | `tuple[float, float] \| None` | Absolute canvas coordinate shift `(dx, dy)` independent of rotation. |
| `angle` | `float \| None` | Counter-clockwise rotation angle in degrees normalized to `[0.0, 360.0)`. |
| `alpha` | `float \| None` | Element-wide opacity multiplier (`0.0`–`1.0`). |

### Public Methods

| Method | Signature | Description |
| :--- | :--- | :--- |
| `patch` | `(other: Style \| None = None, **kwargs) -> Style` | Merge another `Style` and/or keyword attribute overrides into a new immutable `Style` instance. |
| `validate_for` | `(target: Literal["shape", "line", "text", "icon", "image"]) -> None` | Validate that `target` is declared in `self.supports`, raising `ValueError` otherwise. |

---

## `const` Styles

Active project-wide style catalog singleton in `drawlib.styles` (`Styles: DefaultStyles`). Always import uppercase `Styles` from `drawlib.styles` rather than hardcoding `DefaultStyles` in diagram scripts so an entire project can switch themes (`DefaultStyles`, `GoogleStyles`, `MonochromeStyles`, or custom subclasses) via `styles.py` without code edits.

```python
from drawlib.shapes import rectangle
from drawlib.styles import Styles

# 50%+ neutral baseline card + 1 focal PrimaryFlat hero
rectangle((35, 25), width=36, height=18, style=Styles.Neutral, text="Worker Node")
rectangle(
    (85, 25),
    width=36,
    height=18,
    style=Styles.PrimaryFlat,
    text="API Gateway",
    text_style=Styles.WhiteBold,
)

# Dictionary-style dynamic lookup
dynamic_style = Styles["SecondaryNeutral"]
```

| Token Pattern | Examples | Visual Behavior |
| :--- | :--- | :--- |
| **Neutral Cards (50%+ Baseline)** | `Styles.Neutral`, `Styles.PrimaryNeutral`, `Styles.SecondaryNeutral`, `Styles.BlueNeutral`, `Styles.TealNeutral` | Calm light fills with subtle borders (`*NeutralFlat` omits border) for readable dark labels. |
| **Bordered (`<Role>`)** | `Styles.Primary`, `Styles.Secondary`, `Styles.Warning`, `Styles.Success`, `Styles.Danger` | Filled background + solid border (`1.5pt`), regular font weight (`*Thin` = `0.75pt`, `*Bold` = `2.5pt`). |
| **Borderless Fill (`<Role>Flat`)** | `Styles.PrimaryFlat`, `Styles.AccentFlat`, `Styles.DarkFlat` | Solid fill with `shape_line_width=0.0` (pair dark fills with `Styles.WhiteBold`; use `.patch(icon_style="fill")` for filled icons). |
| **Unfilled Outlines** | `Styles.PrimaryOutline` (`PrimarySolid`), `Styles.MutedDashed`, `Styles.WarningDotted` | Transparent interior fill with solid, dashed, or dotted stroke (`*Thin` and `*Bold` weights supported). |
| **Canvas Tokens** | `Styles.Canvas`, `Styles.CanvasFlat` | Background-matched fill tokens for masking connectors or framing overlays. |

---

## `def` get_intermediate_color(color1, color2)

Compute the exact 50% midpoint RGBA `Color` between two colors. Exported by both `drawlib.styles` and [`drawlib.preset_colors`](06_presets.md).

```python
from drawlib.styles import Colors, get_intermediate_color

mid_blue = get_intermediate_color(Colors.Blue1, Colors.Blue6)
mid_hex = get_intermediate_color("#ffffff", "#1a73e8")
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `color1` | `Color \| tuple[int, int, int] \| tuple[int, int, int, float] \| str` | *Required* | Starting color in `Color`, RGB/RGBA tuple, or hex string format. |
| `color2` | `Color \| tuple[int, int, int] \| tuple[int, int, int, float] \| str` | *Required* | Ending color in `Color`, RGB/RGBA tuple, or hex string format. |
| **Returns** | `Color` | — | Interpolated midpoint `Color` equivalent to `get_intermediate_colors(color1, color2, num=1)[0]`. |

---

## `def` get_intermediate_colors(color1, color2, num=1, *, include_ends=False)

Generate a list of evenly spaced linear RGBA `Color` steps between `color1` and `color2`. Useful for custom chart ramps, heatmaps, and multi-frame animation transitions.

```python
from drawlib.styles import Colors, get_intermediate_colors

# 3 interior steps between Neutral and Primary -> returns 3 Color objects
interior = get_intermediate_colors(Colors.Neutral, Colors.Primary, num=3)

# Include endpoints -> returns 5 Color objects (color1, 3 interior, color2)
full_ramp = get_intermediate_colors(Colors.Blue1, Colors.Blue6, num=3, include_ends=True)
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `color1` | `Color \| tuple[int, int, int] \| tuple[int, int, int, float] \| str` | *Required* | Starting color (`Color`, RGB/RGBA tuple, or hex string). |
| `color2` | `Color \| tuple[int, int, int] \| tuple[int, int, int, float] \| str` | *Required* | Ending color (`Color`, RGB/RGBA tuple, or hex string). |
| `num` | `int` | `1` | Number of interior colors to generate (`>= 1`; raises `ValueError` if `< 1`). |
| `include_ends` | `bool` | `False` | When `True`, prepends `color1` and appends `color2` (returning `num + 2` colors). |
| **Returns** | `list[Color]` | — | Ordered list of interpolated `Color` instances. |

---

## `class` BaseColors

Pydantic-backed base class (`drawlib.types.BaseColors`) for preset and custom color catalogs. Provides attribute access, dictionary indexing (`palette["BrandBlue"]`), membership checks, `(name, color)` iteration, and immutable `.patch()` derivation.

```python
from drawlib.types import BaseColors, Color


class BrandColors(BaseColors):
    Navy: Color = Color.from_hex("#0d1b2a")
    Teal: Color = Color.from_hex("#00a896")
    Surface: Color = Color.from_hex("#f4f6f9")


Colors = BrandColors()
all_named = Colors.colors()  # dict[str, Color]
```

### Public Methods

| Method | Signature | Description |
| :--- | :--- | :--- |
| `colors` | `() -> dict[str, Color]` | Return a dictionary containing all `Color` attributes defined on the catalog instance. |
| `get` | `(key: str, default: Any = None) -> Any` | Retrieve a color or attribute by name with an optional fallback `default`. |
| `patch` | `(**kwargs: Any) -> Self` | Return a new catalog copy with specified color tokens replaced. |

---

## `class` BaseStyles

Pydantic-backed base class (`drawlib.types.BaseStyles`) for preset and custom theme catalogs (`DefaultStyles`, `GoogleStyles`, `MonochromeStyles`). Encapsulates default canvas dimensions, DPI, background color, source-code font, associated `BaseColors` palette, and typed `Style` tokens.

```python
from drawlib.fonts import FontRoboto, FontSourceCode
from drawlib.preset_styles import DefaultStyles
from drawlib.types import BaseStyles, Style

# Replace typography across every style token in a theme at once
Styles = DefaultStyles().patch_font(
    FontRoboto.ROBOTO_REGULAR,
    bold=FontRoboto.ROBOTO_BOLD,
    thin=FontRoboto.ROBOTO_THIN,
    sourcecode=FontSourceCode.ROBOTO_MONO,
)
```

### Configuration Attributes

| Attribute | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `width` | `int` | `140` | Default canvas width in coordinate units used by `setup()`. |
| `height` | `int` | `70` | Default canvas height in coordinate units used by `setup()`. |
| `dpi` | `int` | `100` | Default rendering resolution in dots per inch. |
| `background_color` | `Color \| tuple \| str` | `(255, 255, 255, 1.0)` | Default canvas background fill color. |
| `sourcecode_font` | `FontSourceCode` | `FontSourceCode.SOURCECODEPRO` | Default monospace font used by `SourceCode` SmartArt blocks. |
| `colors` | `type[BaseColors] \| BaseColors` | `DefaultColors` | Associated color palette class or instance backing this style catalog. |

### Public Methods

| Method | Signature | Description |
| :--- | :--- | :--- |
| `patch` | `(**kwargs: Any) -> Self` | Return a new theme copy with updated canvas settings or `Style` tokens. |
| `patch_font` | `(regular: FontBase \| FontFile \| None = None, *, bold: FontBase \| FontFile \| None = None, thin: FontBase \| FontFile \| None = None, sourcecode: FontSourceCode \| None = None, size: float \| None = None) -> Self` | Return a new theme copy with `text_font` and/or `text_size` updated across regular, `*Bold`, `*Thin`, and `sourcecode_font` tokens. |
| `styles` | `() -> dict[str, Style]` | Extract all `Style` tokens defined on this preset as a `{token_name: Style}` dictionary. |
| `field_names` | `() -> list[str]` | Return ordered field and dynamically generated style token names on this instance. |
| `get` | `(key: str, default: Any = None) -> Any` | Safely look up a style token or attribute by name with an optional fallback. |

---

## `enum` FontBase

Abstract `StrEnum` base class (`drawlib.types.FontBase` and [`drawlib.fonts.FontBase`](07_fonts.md)) inherited by all built-in font enumerations (`Font`, `FontSansSerif`, `FontSerif`, `FontMonoSpace`, `FontRoboto`, `FontSourceCode`, `FontJapanese`, `FontChinese`, `FontKorean`, `FontArabic`, `FontThai`, `FontBrahmic`).

```python
from drawlib.fonts import Font, FontRoboto
from drawlib.types import FontBase, Style


def make_label_style(font: FontBase) -> Style:
    return Style(text_font=font, text_size=12.0)


header_style = make_label_style(FontRoboto.ROBOTO_BOLD)
body_style = make_label_style(Font.SANSSERIF_REGULAR)
```

| Characteristic | Specification |
| :--- | :--- |
| **Base Type** | `enum.StrEnum` (zero direct enum members; subclassed by all 12 built-in font families in [`drawlib.fonts`](07_fonts.md)). |
| **Primary Role** | Shared runtime and static type annotation for `Style.text_font` (`FontBase \| FontFile \| None`) and `BaseStyles.patch_font()`. |
