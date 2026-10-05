# Drawlib Types & Style Models Guidelines

Drawlib employs a strongly-typed, object-oriented styling architecture.  
Rather than scattering dozens of loose formatting arguments across drawing calls, styles are encapsulated into cohesive `Style` models and reusable theme base classes.

---

## 1. Imports & Core Architecture

All public type models and styling base classes are imported from `drawlib.types`:

```python
from drawlib.types import (
    # Primary Styling Model
    Style,

    # Architectural Base Classes
    BaseColors,          # Base class for defining custom color palettes
    BaseStyles,          # Base class for defining custom preset styles
    FontBase,            # Base class for font representations
)
```

---

## 2. The `Style` Class Specification

`Style` is the universal, immutable configuration object for shapes, lines, text, icons, and images.
All properties are domain-segregated to prevent ambiguous collisions:

```python
Style(
    # Target declaration (inferred automatically from provided attributes if omitted)
    supports: frozenset[Literal["shape", "line", "text", "icon", "image"]] | set[str] | None = None,

    # Shape Properties (rectangle, circle, polygon, etc.)
    shape_fill_color: tuple[int, int, int] | tuple[int, int, int, float] | Color | str | None = None,
    shape_fill_alpha: float | None = None,
    shape_line_color: tuple[int, int, int] | tuple[int, int, int, float] | Color | str | None = None,
    shape_line_width: float | None = None,
    shape_line_style: Literal["solid", "dashed", "dotted", "dashdot"] | None = None,

    # Line / Arrow Properties (line, lines, arrow, etc.)
    line_color: tuple[int, int, int] | tuple[int, int, int, float] | Color | str | None = None,
    line_width: float | None = None,
    line_style: Literal["solid", "dashed", "dotted", "dashdot"] | None = None,
    line_alpha: float | None = None,
    line_arrow_head_fill: bool | None = None,
    line_arrow_head_scale: float | None = None,

    # Text & Typography Properties
    text_color: tuple[int, int, int] | tuple[int, int, int, float] | Color | str | None = None,
    text_size: float | Literal["small", "medium", "large"] | None = None,
    text_font: FontBase | FontFile | None = None,
    text_halign: Literal["left", "center", "right"] | None = None,
    text_valign: Literal["bottom", "center", "top"] | None = None,
    text_angle: float | None = None,
    text_flip: bool | None = None,
    text_line_spacing: float | None = None,
    text_xy_shift: tuple[float, float] | None = None,
    text_xy_abs_shift: tuple[float, float] | None = None,
    text_bg_fill_color: tuple[int, int, int] | tuple[int, int, int, float] | Color | str | None = None,
    text_bg_fill_alpha: float | None = None,
    text_bg_line_color: tuple[int, int, int] | tuple[int, int, int, float] | Color | str | None = None,
    text_bg_line_width: float | None = None,
    text_bg_line_style: Literal["solid", "dashed", "dotted", "dashdot"] | None = None,

    # Icon Properties (phosphor, font_icon, gcp)
    icon_color: tuple[int, int, int] | tuple[int, int, int, float] | Color | str | None = None,
    icon_style: Literal["regular", "bold", "fill", "thin", "light", "duotone"] | None = None,

    # Image Properties
    image_tint_color: tuple[int, int, int] | tuple[int, int, int, float] | Color | str | None = None,
    image_alpha: float | None = None,
    image_border_color: tuple[int, int, int] | tuple[int, int, int, float] | Color | str | None = None,
    image_border_width: float | None = None,
    image_border_style: Literal["solid", "dashed", "dotted", "dashdot"] | None = None,
)
```

### Complete Attribute Reference:
| Attribute | Type | Description |
| :--- | :--- | :--- |
| `supports` | `frozenset` | Declared targets (`"shape"`, `"line"`, `"text"`, `"icon"`, `"image"`). Inferred if omitted. |
| `shape_fill_color` | `ColorType` | Background/interior fill color for shapes (`tuple`, `Color`, or hex `str`). |
| `shape_fill_alpha` | `float` | Shape fill opacity (`0.0` = fully transparent, `1.0` = fully opaque). |
| `shape_line_color` | `ColorType` | Shape border stroke color. |
| `shape_line_width` | `float` | Shape border stroke thickness in points. |
| `shape_line_style` | `str` | Shape border pattern: `"solid"`, `"dashed"`, `"dotted"`, `"dashdot"`. |
| `line_color` | `ColorType` | Connector/path line stroke color. |
| `line_width` | `float` | Line stroke thickness in points. |
| `line_style` | `str` | Line dash pattern: `"solid"`, `"dashed"`, `"dotted"`, `"dashdot"`. |
| `line_arrow_head_fill` | `bool` | Whether arrowhead is filled triangle (`True`) or stick (`False`). |
| `line_arrow_head_scale` | `float` | Physical scaling factor for arrowheads (default: 20.0). |
| `text_color` | `ColorType` | Color for embedded text or standalone text labels. |
| `text_size` | `float \| str` | Font size in points or semantic label (`"small"`, `"medium"`, `"large"`). |
| `text_font` | `FontBase` | Font instance (e.g. `FontRoboto.ROBOTO_BOLD`, `Font.SANSSERIF_REGULAR`). |
| `text_halign` | `str` | Horizontal alignment: `"left"`, `"center"`, `"right"`. |
| `text_valign` | `str` | Vertical alignment: `"bottom"`, `"center"`, `"top"`. |
| `text_angle` | `float` | Counter-clockwise text rotation angle in degrees. |
| `text_flip` | `bool` | Whether to mirror text horizontally. |
| `text_line_spacing` | `float` | Line spacing multiplier for multi-line text (default: `1.2`). |
| `text_xy_shift` | `tuple` | Normalized relative offset `(dx, dy)` for embedded text within shapes. |
| `text_xy_abs_shift` | `tuple` | Absolute coordinate offset `(dx, dy)` in canvas units. |
| `icon_color` | `ColorType` | Color for vector icons. |
| `icon_style` | `str` | Icon weight/fill style variant (`"regular"`, `"bold"`, `"fill"`, etc.). |

### Immutability & Derivation via `.patch()`
In Drawlib v0.3, `Style` instances are strictly **frozen** and immutable (`frozen=True`, `extra="forbid"`). Attempting to mutate an attribute directly raises an error.

To create derivative styles, always use the `.patch()` method:
```python
from drawlib.styles import Colors, Styles

# Patch an existing preset to derive a new style:
highlighted_style = Styles.Primary.patch(
    shape_line_color=Colors.Red,
    shape_line_width=4.0,
)
```

---

## 3. Drawlib Core Type Conventions

Public Drawlib functions use standard Python typing rather than internal aliases to maximize IDE autocompletion and clarity:

- **Coordinates**:  
  `tuple[float, float]` representing `(x, y)` in canvas coordinate space.
- **Coordinate Sequences**:  
  `list[tuple[float, float]]` representing chained paths or polygon vertices.
- **Colors**:  
  `tuple[int, int, int]`, `tuple[int, int, int, float]`, `Color`, or hex `str` (e.g. `"#1a73e8"`).
- **Angles**:  
  `float` or `int` in degrees `[0.0, 360.0)`, measured counter-clockwise from horizontal East.
- **Arrowheads**:  
  `Literal["->", "<-", "<->", "-"]` (`"->"` forward, `"<-"` backward, `"<->"` bidirectional, `"-"` plain stroke).
- **Line Styles**:  
  `Literal["solid", "dashed", "dotted", "dashdot"]`.
- **Alignments**:  
  Horizontal: `Literal["left", "center", "right"]`. Vertical: `Literal["bottom", "center", "top"]`.

---

## 4. Custom Themes via `BaseStyles`

You can define cohesive organizational design systems by subclassing `BaseStyles`.

> **Important**: `BaseStyles` is built upon Pydantic `BaseModel`. All style attributes **must** be explicitly type-annotated (`primary: Style = ...`) so Pydantic properly registers them.

```python
from drawlib.preset_colors import Color
from drawlib.types import BaseColors, BaseStyles, Style

class AcmeColors(BaseColors):
    BrandBlue: Color = Color.from_hex("#0052cc")
    BrandOrange: Color = Color.from_hex("#ff5630")
    NeutralDark: Color = Color.from_hex("#172b4d")
    NeutralLight: Color = Color.from_hex("#f4f5f7")

acme_colors = AcmeColors()

class AcmeTheme(BaseStyles):
    primary: Style = Style(
        shape_fill_color=acme_colors.BrandBlue,
        shape_line_color=acme_colors.BrandBlue,
        shape_line_width=0,
        text_color=Color(255, 255, 255),
        text_size=14,
        text_font=FontRoboto.ROBOTO_REGULAR,
    )
    accent: Style = Style(
        shape_fill_color=acme_colors.BrandOrange,
        shape_line_color=acme_colors.BrandOrange,
        shape_line_width=0,
        text_color=Color(255, 255, 255),
        text_size=14,
        text_font=FontRoboto.ROBOTO_BOLD,
    )
```

---

## 5. Practical Code Examples

### 5.1. Creating and Applying Custom `Style` Objects

```drawlib fold-code 600px center caption:"Encapsulated Styling with the Style Model"
from drawlib.canvas import save, setup
from drawlib.fonts import FontRoboto
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles

setup(width=140, height=60)

# Base card style derived from Styles.Primary
card_style = Styles.Primary.patch(
    shape_fill_color=(245, 247, 250),
    shape_line_color=Colors.Blue,
    shape_line_width=2,
    shape_line_style="solid",
    text_color=(30, 40, 50),
    text_font=FontRoboto.ROBOTO_BOLD,
    text_size=14,
)

# Active card style derived via .patch()
active_card_style = card_style.patch(
    shape_fill_color=Colors.Blue,
    text_color=(255, 255, 255),
)

rectangle((40, 30), width=40, height=24, r=3, style=card_style, text="Standby Node")
rectangle((100, 30), width=40, height=24, r=3, style=active_card_style, text="Active Leader")

line((60, 30), (80, 30), arrow_head="->", style=Styles.PrimaryBold)
save()
```

---

## 6. Related Rules
- Preset Styles Catalog: `uv run drawlib rules show lib-preset-styles`
- Color Palettes & Helpers: `uv run drawlib rules show lib-preset-colors`
- Typography & Font Classes: `uv run drawlib rules show lib-fonts`
- Shapes Drawing Primitives: `uv run drawlib rules show lib-shapes`
