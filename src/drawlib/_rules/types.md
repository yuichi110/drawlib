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

`Style` is the universal configuration object for shapes, lines, text, icons, and diagrams.

```python
Style(
    # Fill & Background
    fill_color: tuple[int, int, int] | tuple[int, int, int, float] | None = None,
    alpha: float | None = None,

    # Border & Stroke
    line_color: tuple[int, int, int] | tuple[int, int, int, float] | None = None,
    line_width: float | None = None,
    line_style: Literal["solid", "dashed", "dotted", "dashdot"] | None = None,

    # Typography & Text Formatting
    text_color: tuple[int, int, int] | tuple[int, int, int, float] | None = None,
    text_size: float | None = None,
    text_font: FontBase | FontFile | None = None,
    text_halign: Literal["left", "center", "right"] | None = None,
    text_valign: Literal["bottom", "center", "top"] | None = None,
    text_angle: float | None = None,
)
```

### Complete Attribute Reference:
| Attribute | Type | Description |
| :--- | :--- | :--- |
| `fill_color` | `tuple` | Background/interior fill color as RGB `(r, g, b)` or RGBA `(r, g, b, a)`. |
| `alpha` | `float` | Overall element opacity (`0.0` = fully transparent, `1.0` = fully opaque). |
| `line_color` | `tuple` | Stroke border or connector line color. |
| `line_width` | `float` | Stroke thickness in canvas points (e.g. `1`, `2`, `3`). |
| `line_style` | `str` | Dash pattern: `"solid"`, `"dashed"`, `"dotted"`, `"dashdot"`. |
| `text_color` | `tuple` | Color for embedded text or standalone text labels. |
| `text_size` | `float` | Font size in typographical points (e.g. `12`, `14`, `18`, `24`). |
| `text_font` | `Font` | Font instance (e.g. `FontRoboto.ROBOTO_BOLD`, `FontMonoSpace.MONOSPACE_REGULAR`). |
| `text_halign`| `str` | Horizontal alignment: `"left"`, `"center"`, `"right"`. |
| `text_valign`| `str` | Vertical alignment: `"bottom"`, `"center"`, `"top"`. |
| `text_angle` | `float` | Counter-clockwise text rotation angle in degrees. |

### Immutability & Copying Pattern
To prevent unintended side effects when deriving styles:
```python
from copy import deepcopy
from drawlib.colors import Colors
from drawlib.types import Style

base_style = Style(fill_color=Colors.Blue, line_color=Colors.Black, line_width=2)

# Create derivative without modifying the base style:
highlighted_style = deepcopy(base_style)
highlighted_style.line_color = Colors.Red
highlighted_style.line_width = 4
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
from copy import deepcopy
from drawlib.canvas import config, save
from drawlib.colors import ColorsDefault
from drawlib.fonts import FontRoboto
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.types import Style

config(width=140, height=60)

# Base card style
card_style = Style(
    fill_color=(245, 247, 250),
    line_color=ColorsDefault.Blue,
    line_width=2,
    line_style="solid",
    text_color=(30, 40, 50),
    text_font=FontRoboto.ROBOTO_BOLD,
    text_size=14,
)

# Active card style derived via deepcopy
active_card_style = deepcopy(card_style)
active_card_style.fill_color = ColorsDefault.Blue
active_card_style.text_color = (255, 255, 255)

rectangle((40, 30), width=40, height=24, r=3, style=card_style, text="Standby Node")
rectangle((100, 30), width=40, height=24, r=3, style=active_card_style, text="Active Leader")

line((60, 30), (80, 30), arrowhead="->", style="bold")
```

---

## 6. Related Rules
- Preset Styles Catalog: `uv run drawlib rules show preset_styles`
- Color Palettes & Helpers: `uv run drawlib rules show colors`
- Typography & Font Classes: `uv run drawlib rules show fonts`
- Shapes Drawing Primitives: `uv run drawlib rules show shapes`
