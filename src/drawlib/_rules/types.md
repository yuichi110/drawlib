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
    ColorsBase,          # Base class for defining custom color palettes
    FontBase,            # Base class for font representations
    BasePresetStyles,    # Base class for defining custom preset themes
    PresetStyles,        # Concrete container for theme preset styles
)
```

---

## 2. The `Style` Class Specification

`Style` is the universal, immutable configuration object for shapes, lines, text, icons, and images.
All properties are domain-segregated to prevent ambiguous collisions:

```python
Style(
    # Shape Properties (rectangle, circle, polygon, etc.)
    shape_fill_color: tuple[int, int, int] | tuple[int, int, int, float] | None = None,
    shape_fill_alpha: float | None = None,
    shape_line_color: tuple[int, int, int] | tuple[int, int, int, float] | None = None,
    shape_line_width: float | None = None,
    shape_line_style: Literal["solid", "dashed", "dotted", "dashdot"] | None = None,

    # Line / Arrow Properties (line, lines, arrow, etc.)
    line_color: tuple[int, int, int] | tuple[int, int, int, float] | None = None,
    line_width: float | None = None,
    line_style: Literal["solid", "dashed", "dotted", "dashdot"] | None = None,
    line_alpha: float | None = None,
    line_arrow_head_fill: bool | None = None,
    line_arrow_head_scale: float | None = None,

    # Text & Typography Properties
    text_color: tuple[int, int, int] | tuple[int, int, int, float] | None = None,
    text_size: float | None = None,
    text_font: FontBase | FontFile | None = None,
    text_halign: Literal["left", "center", "right"] | None = None,
    text_valign: Literal["bottom", "center", "top"] | None = None,
    text_angle: float | None = None,
    text_bg_fill_color: tuple[int, int, int] | tuple[int, int, int, float] | None = None,
    text_bg_line_color: tuple[int, int, int] | tuple[int, int, int, float] | None = None,
    text_bg_line_width: float | None = None,

    # Icon Properties (phosphor, font_icon, gcp)
    icon_color: tuple[int, int, int] | tuple[int, int, int, float] | None = None,
    icon_style: Literal["regular", "bold", "fill", "thin", "light", "duotone"] | None = None,

    # Image Properties
    image_tint_color: tuple[int, int, int] | tuple[int, int, int, float] | None = None,
    image_alpha: float | None = None,
    image_border_color: tuple[int, int, int] | tuple[int, int, int, float] | None = None,
    image_border_width: float | None = None,
    image_border_style: Literal["solid", "dashed", "dotted", "dashdot"] | None = None,
)
```

### Complete Attribute Reference:
| Attribute | Type | Description |
| :--- | :--- | :--- |
| `shape_fill_color` | `tuple` | Background/interior fill color for shapes. |
| `shape_fill_alpha` | `float` | Shape fill opacity (`0.0` = fully transparent, `1.0` = fully opaque). |
| `shape_line_color` | `tuple` | Shape border stroke color. |
| `shape_line_width` | `float` | Shape border stroke thickness in points. |
| `shape_line_style` | `str` | Shape border pattern: `"solid"`, `"dashed"`, `"dotted"`, `"dashdot"`. |
| `line_color` | `tuple` | Connector/path line stroke color. |
| `line_width` | `float` | Line stroke thickness in points. |
| `line_style` | `str` | Line dash pattern: `"solid"`, `"dashed"`, `"dotted"`, `"dashdot"`. |
| `line_arrow_head_fill` | `bool` | Whether arrowhead is filled triangle (`True`) or stick (`False`). |
| `line_arrow_head_scale` | `float` | Physical scaling factor for arrowheads (default: 20.0). |
| `text_color` | `tuple` | Color for embedded text or standalone text labels. |
| `text_size` | `float` | Font size in typographical points (e.g. `12`, `14`, `18`, `24`). |
| `text_font` | `Font` | Font instance (e.g. `FontRoboto.ROBOTO_BOLD`, `Font.SANSSERIF_REGULAR`). |
| `text_halign` | `str` | Horizontal alignment: `"left"`, `"center"`, `"right"`. |
| `text_valign` | `str` | Vertical alignment: `"bottom"`, `"center"`, `"top"`. |
| `text_angle` | `float` | Counter-clockwise text rotation angle in degrees. |
| `icon_color` | `tuple` | Color for vector icons. |
| `icon_style` | `str` | Icon weight/fill style variant (`"regular"`, `"bold"`, `"fill"`, etc.). |

### Immutability & Derivation via `.patch()`
In Drawlib v0.3, `Style` instances are strictly **frozen** and immutable (`frozen=True`, `extra="forbid"`). Attempting to mutate an attribute directly raises an error.

To create derivative styles, always use the `.patch()` method:
```python
from drawlib.colors import Colors
from drawlib.config import styles

# Patch an existing preset to derive a new style:
highlighted_style = styles.primary.patch(
    shape_line_color=Colors.Red,
    shape_line_width=4.0,
)
```

---

## 3. Drawlib Core Type Conventions

When reading function signatures across Drawlib modules, parameters adhere to these conventions:

- **Coordinates (`TypeCoordinate`)**:  
  `tuple[float, float]` representing `(x, y)` in canvas coordinate space.
- **Coordinate Sequences (`TypeCoordinates`)**:  
  `list[tuple[float, float]]` representing chained paths or polygon vertices.
- **Colors (`TypeColor`)**:  
  RGB `tuple[int, int, int]` or RGBA `tuple[int, int, int, float]`.
- **Angles (`TypeAngle`)**:  
  `float` or `int` in degrees `[0.0, 360.0)`, measured counter-clockwise from horizontal East.
- **Arrowheads (`TypeArrowHead`)**:  
  `"->"` (forward), `"<-"` (backward), `"<->"` (bidirectional), `"-"` (plain stroke without head).
- **Line Styles (`TypeLineStyle`)**:  
  `"solid"`, `"dashed"`, `"dotted"`, `"dashdot"`.
- **Alignments (`TypeHAlign`, `TypeVAlign`)**:  
  Horizontal: `"left"`, `"center"`, `"right"`. Vertical: `"bottom"`, `"center"`, `"top"`.

---

## 4. Custom Themes via `BasePresetStyles`

You can define cohesive organizational design systems by subclassing `BasePresetStyles`:

```python
from drawlib.colors import ColorsBase, from_hex
from drawlib.types import BasePresetStyles, Style

class AcmeColors(ColorsBase):
    BrandBlue = from_hex("#0052cc")
    BrandOrange = from_hex("#ff5630")
    NeutralDark = from_hex("#172b4d")
    NeutralLight = from_hex("#f4f5f7")

class AcmeTheme(BasePresetStyles):
    def __init__(self) -> None:
        super().__init__()
        # Register custom shape styles
        self.shape_styles["primary"] = Style(
            fill_color=AcmeColors.BrandBlue,
            text_color=(255, 255, 255),
            line_width=0,
        )
        self.shape_styles["accent"] = Style(
            fill_color=AcmeColors.BrandOrange,
            text_color=(255, 255, 255),
            line_width=0,
        )
```

---

## 5. Practical Code Examples

### 5.1. Creating and Applying Custom `Style` Objects

```drawlib fold-code 600px center caption:"Encapsulated Styling with the Style Model"
from drawlib.canvas import save, setup
from drawlib.colors import ColorsDefault
from drawlib.fonts import FontRoboto
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.config import styles

setup(width=140, height=60)

# Base card style derived from styles.primary
card_style = styles.primary.patch(
    shape_fill_color=(245, 247, 250),
    shape_line_color=ColorsDefault.Blue,
    shape_line_width=2,
    shape_line_style="solid",
    text_color=(30, 40, 50),
    text_font=FontRoboto.ROBOTO_BOLD,
    text_size=14,
)

# Active card style derived via .patch()
active_card_style = card_style.patch(
    shape_fill_color=ColorsDefault.Blue,
    text_color=(255, 255, 255),
)

rectangle((40, 30), width=40, height=24, r=3, style=card_style, text="Standby Node")
rectangle((100, 30), width=40, height=24, r=3, style=active_card_style, text="Active Leader")

line((60, 30), (80, 30), arrowhead="->", style=styles.bold)
save()
```

---

## 6. Related Rules
- Preset Styles Catalog: `uv run drawlib rules show preset_styles`
- Color Palettes & Helpers: `uv run drawlib rules show colors`
- Typography & Font Classes: `uv run drawlib rules show fonts`
- Shapes Drawing Primitives: `uv run drawlib rules show shapes`
