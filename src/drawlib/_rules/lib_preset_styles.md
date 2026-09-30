# Drawlib Preset Styles Guidelines

Drawlib provides a comprehensive, centralized preset style system in `drawlib.preset_styles` designed to enforce visual consistency, eliminate boilerplate styling code, and enable rapid diagram prototyping. Under the "Illustration as Code" philosophy, styling is treated as a systematic design system where shapes, lines, icons, text, and images adhere to cohesive color palettes, line widths, and typographical hierarchies.

---

## 1. Architectural Philosophy & Core Concepts

In complex technical diagrams and architectural illustrations, manually specifying colors, line widths, borders, and fonts for every individual element leads to verbose, brittle, and visually inconsistent code. Drawlib addresses this through three core design principles:

1. **Systematic Semantic Roles**:
   Rather than hardcoding arbitrary colors, Drawlib organizes styles around 6 semantic roles (`primary`, `secondary`, `accent`, `muted`, `danger`, `success`) across 10 orthogonal variants (`flat`, `bold`, `light`, `outline`, `dashed`, etc.).

2. **First-Class Object Referencing**:
   Styles are passed as strongly-typed `Style` instances directly from `drawlib.styles.Styles` (or `Styles`), e.g., `style=Styles.primary_flat` or `style=Styles.accent_bold`. Passing arbitrary strings to `style` is rejected by Pydantic validation to ensure compile-time safety.

3. **Layered Object Models**:
   At the core of the preset style system is `BaseStyles` (a Pydantic `BaseModel` with dynamic metaclass resolution), which exposes standard role-based styles (`primary`, `secondary`, `accent`, `muted`), default canvas background colors, and font definitions. Users can inspect, copy, patch, or subclass these models to define enterprise brand guidelines.

### 1.1. High-Level Architecture Overview

```text
┌───────────────────────────────────────────────────────────────────────────────────┐
│                               Public Facade API                                   │
│       from drawlib.preset_styles import DefaultStyles, GoogleStyles, ...          │
│       from drawlib.preset_colors import DefaultColors, GoogleColors, ...          │
│       from drawlib.styles import Styles, Colors                                   │
└────────────────────────────────────────┬──────────────────────────────────────────┘
                                         │
                    ┌────────────────────┴────────────────────┐
                    ▼                                         ▼
   ┌─────────────────────────────────┐       ┌─────────────────────────────────┐
   │       Color Collections         │       │     Official Style Catalogs     │
   │  - DefaultColors                │       │  - DefaultStyles                │
   │  - MonochromeColors             │       │  - MonochromeStyles             │
   │  - GoogleColors                 │       │  - GoogleStyles                 │
   │  - CssColors (140 CSS colors)   │       │  - Styles (Active Facade)       │
   │  - Colors (Active Facade)       │       │  (Base: BaseStyles)             │
   └────────────────┬────────────────┘       └────────────────┬────────────────┘
                    │                                         │
                    └────────────────────┬────────────────────┘
                                         │
                                         ▼
                    ┌─────────────────────────────────────────┐
                    │      Style Resolution                   │
                    │  Token parsing: <color>_<type>_<weight> │
                    └────────────────────┬────────────────────┘
                                         │
       ┌───────────────────┬─────────────┴─────┬───────────────────┐
       ▼                   ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│    Shapes    │    │    Lines     │    │     Text     │    │    Icons     │
│ (Fill/Line)  │    │(Stroke/Dash) │    │ (Font/Weight)│    │(Tint/Weight) │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
```

---

## 2. Public API & Module Imports

All preset styling symbols and color utilities are accessed through clean, public module namespaces:

```python
# Active theme styling tokens (recommended for general drawing)
from drawlib.styles import Colors, Styles

# Preset style catalog classes
from drawlib.preset_styles import (
    DefaultStyles,
    DefaultStyles1,
    DefaultStyles2,
    DefaultStyles3,
    DefaultStyles4,
    DefaultStyles5,
    DefaultStyles6,
    GoogleStyles,
    MonochromeStyles,
    Style,
)

# Color collections and utilities
from drawlib.preset_colors import (
    Color,
    CssColors,
    DefaultColors,
    DefaultColors1,
    DefaultColors2,
    DefaultColors3,
    DefaultColors4,
    DefaultColors5,
    DefaultColors6,
    GoogleColors,
    MonochromeColors,
)

# Architectural Base classes
from drawlib.types import BaseColors, BaseStyles
```

### 2.1. Re-exported Symbol Summary

| Symbol | Category | Description |
| :--- | :--- | :--- |
| `Styles` | Active Facade | Active style catalog singleton imported from `drawlib.styles`. |
| `Colors` | Active Facade | Active color palette singleton imported from `drawlib.styles`. |
| `DefaultStyles` | Model Class | Default design system style catalog (Level 4 primary centered). |
| `GoogleStyles` | Model Class | Google Slides & Workspace brand style catalog. |
| `MonochromeStyles` | Model Class | Grayscale style catalog for print, papers, and e-ink. |
| `Style` | Data Model | Core style model representing visual attributes. |
| `BaseStyles` | Base Model | Pydantic BaseModel providing dict-like access, copy, and patch operations. |

---

## 3. Official Palette Catalogs

Drawlib ships with three pre-built, production-ready style catalogs. Each catalog organizes styles into semantic roles (with 10 orthogonal variants each) alongside default canvas background colors and typographical defaults:
- **Color Catalogs (`DefaultStyles`, `GoogleStyles`)**: **6 Semantic Roles** (`primary`, `secondary`, `accent`, `muted`, `danger`, `success`).
- **Monochrome Catalog (`MonochromeStyles`)**: **4 Semantic Roles** (`primary`, `secondary`, `accent`, `muted`) — Grayscale excludes danger/success.

```text
┌───────────────────────────────────────────────────────────────────────────────────────┐
│                                   BaseStyles Model                                    │
├───────────────────────────────────────────────────────────────────────────────────────┤
│ + background_color: ColorType = (255, 255, 255, 1.0)                                  │
│ + sourcecode_font: FontSourceCode = FontSourceCode.SOURCECODEPRO                      │
├───────────────────────────────────────────────────────────────────────────────────────┤
│ Semantic Roles (10 orthogonal variants each: bordered, bold, light, flat, outline,    │
│                 outline_bold, outline_light, dashed, dashed_bold, dashed_light):      │
│   - primary: Core application logic, main components                                  │
│   - secondary: Databases, message queues, auxiliary services                          │
│   - accent: Gateways, clients, focal points                                           │
│   - muted: Boundaries, VPCs, subnets, containers                                      │
│   - danger: Errors, alerts, security risks (Color catalogs only)                      │
│   - success: Completed milestones, healthy status (Color catalogs only)               │
└───────────────────────────────────────────────────────────────────────────────────────┘
```

### 3.1. DefaultStyles (`"default"`)

The standard catalog optimized for technical documentation, flowcharts, and software architecture diagrams. It uses a calming, clean light blue (`DefaultStyleColors.Blue`) as the primary fill and black (`DefaultStyleColors.Black`) for crisp border definition.

- **Primary Colors**: Blue (`#6F6FEF`), Black (`#000000`), White (`#FFFFFF`), Green (`#4FBF4F`), Red (`#EF5F5F`).
- **Visual Design**:
  - `primary`: Blue fill, black border (width 1.5), sans-serif regular font.
  - `light`: Blue fill, black border (width 0.75), sans-serif light font, thin icons.
  - `bold`: Blue fill, black border (width 2.25), sans-serif bold font, regular icons.
  - `flat`: Blue fill, blue border with `line_width=0` (borderless), fill-style icons.
  - `solid`: Transparent fill, blue border (width 1.5), regular icons.
  - `dashed`: Transparent fill, blue dashed border (width 1.5), regular icons.

```python
from drawlib.styles import Styles

default_catalog = Styles

print("Default Primary Fill:", default_catalog.primary.shape_fill_color)
print("Default Primary Line:", default_catalog.primary.shape_line_color)
print("Default Line Width:", default_catalog.primary.shape_line_width)
```

### 3.2. MonochromeStyles (`"monochrome"`)

Specially designed for printed engineering manuals, formal academic papers, patents, and grayscale e-ink displays. It uses pure black, white, and balanced intermediate gray tones to maintain razor-sharp contrast without color dependencies.

- **Primary Colors**: Black (`#000000`), Gray1 (`#F5F5F5`) to Gray8 (`#191919`), White (`#FFFFFF`).
- **Visual Design**:
  - `primary`: White fill, black border (width 1.5), black text, sans-serif regular font.
  - `light`: White fill, black border (width 0.75), sans-serif light font.
  - `bold`: White fill, black border (width 2.25), sans-serif bold font.
  - `flat`: Solid black fill, black border with `line_width=0`.
  - `solid`: Transparent fill, black border (width 1.5).
  - `dashed`: Transparent fill, black dashed border (width 1.5).

```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.preset_styles import MonochromeStyles
from drawlib.shapes import rectangle
from drawlib.text import text

setup(width=120, height=40)
mono = MonochromeStyles

# White box with black outline
rectangle((30, 20), width=35, height=20, style=mono.primary)
text((30, 20), "Primary (Outline)", style=mono.primary)

# Solid black box with white text
rectangle((80, 20), width=35, height=20, style=mono.flat)
text((80, 20), "Flat (Filled)", style=mono.white_bold)

save()
```

### 3.3. DefaultStyles (`"essentials"`)

An expressive, modern palette featuring systematic 6-tone chromatic scales, neutral grays, and semantic roles. It is the recommended base for complex multi-tier system designs, data visualization dashboards, and cloud infrastructure diagrams where distinct subsystems require dedicated semantic colors.

- **Primary Colors**: 8 chromatic hues across 6 tone levels (Blue, Green, Red, Orange, Amber, Purple, Teal, Pink), 8 gray levels (Gray1 to Gray8), Black, White, and standard primaries.
- **Visual Design**:
  - `primary`: Blue4 fill, Blue6 border (width 1.5), white text.
  - `light`: Blue1 fill, Blue5 border (width 0.75), sans-serif light font.
  - `bold`: Blue4 fill, Blue6 border (width 2.25), sans-serif bold font.
  - `flat`: Blue4 fill, borderless (`line_width=0`).
  - `solid`: Transparent fill, Blue4 border (width 1.5).
  - `dashed`: Transparent fill, Blue4 dashed border (width 1.5).

```python
from drawlib.preset_styles import DefaultStyles

# Access class attributes directly
essentials = DefaultStyles

print("Default Primary Text Color:", essentials.primary.text_color)
print("Default Background:", essentials.background_color)
```

---

## 4. Color Collections & Color Management

Drawlib enforces strict RGB or RGBA tuples internally for maximum precision and rendering consistency. To avoid hardcoding raw numeric tuples across codebases, Drawlib provides structured static color classes.

### 4.1. Color Classes Overview

| Class | Base Class | Primary Purpose |
| :--- | :--- | :--- |
| `DefaultColors` | `BaseColors` | Core palette matching the `"default"` preset catalog (6-tone scales + neutrals + semantics). |
| `MonochromeColors` | `BaseColors` | Pure grayscale gradient from Black to White (Gray1 to Gray8). |
| `GoogleColors` | `BaseColors` | Official Google corporate color palette. |
| `CssColors` | `BaseColors` | Complete W3C CSS Color Module Level 3 named colors. |

### 4.2. Exact RGB Values of Built-In Palettes

#### MonochromeColors
- `White`: `(255, 255, 255)`
- `Gray1`: `(245, 245, 245)`
- `Gray2`: `(230, 230, 230)`
- `Gray3`: `(210, 210, 210)`
- `Gray4`: `(175, 175, 175)`
- `Gray5`: `(135, 135, 135)`
- `Gray6`: `(95, 95, 95)`
- `Gray7`: `(55, 55, 55)`
- `Gray8`: `(25, 25, 25)`
- `Black`: `(0, 0, 0)`

#### DefaultColors (Selected Tones and Primaries)
| Color Name | RGB Value | Hex Equivalent | Visual Role |
| :--- | :--- | :--- | :--- |
| `Blue4` | `(72, 98, 218)` | `#4862DA` | Default primary tone, key service cards |
| `Blue1` | `(232, 242, 255)` | `#E8F2FF` | Light background fills, subtle highlights |
| `Green4` | `(58, 150, 75)` | `#3A964B` | Success states, operational services |
| `Red4` | `(190, 58, 68)` | `#BE3A44` | Danger states, critical alerts |
| `Orange4` | `(215, 100, 20)` | `#D76414` | Compute nodes, warnings |
| `Amber4` | `(215, 134, 20)` | `#D78614` | Accent highlight, caches |
| `Purple4` | `(128, 55, 195)` | `#8037C3` | Asynchronous queues, brokers |
| `Teal4` | `(42, 152, 154)` | `#2A989A` | API gateways, network routing |
| `Pink4` | `(195, 45, 125)` | `#C32D7D` | Special events, security tags |
| `Gray3` | `(220, 226, 235)` | `#DCE2EB` | Container card backdrops, muted fills |
| `Gray5` | `(140, 152, 170)` | `#8C98AA` | Subnet borders, divider lines |
| `Black` | `(0, 0, 0)` | `#000000` | Borders, primary dark text |
| `White` | `(255, 255, 255)` | `#FFFFFF` | Canvas default, card surfaces |

### 4.3. Color Manipulation: Color Model, Hex, and .patch()

Drawlib provides a first-class `Color` model in `drawlib.preset_colors` (and `drawlib.styles.Color`) with hex parsing and channel patching:

```python
from drawlib.preset_colors import Color, DefaultColors

# 1. Parse standard hex code or initialize Color
brand_blue = Color.from_hex("#1a73e8")  # returns Color(26, 115, 232, 1.0)
brand_blue_direct = Color("#1a73e8")

# 2. Parse 8-digit hex code with alpha channel
semi_transparent = Color.from_hex("#1a73e880")  # returns Color(26, 115, 232, 0.5)

# 3. Dynamically adjust transparency on existing color constants
backdrop_color = DefaultColors.Navy.patch(alpha=0.15)
# returns Color(15, 15, 127, 0.15)
```

---

## 5. Systematic Naming Rules & Grammar

Every preset style shortcut string follows a deterministic, composable three-part grammar:

```text
                     <color> _ <type> _ <weight>
                        │        │         │
                        │        │         └─► "light" | "bold" | (omitted)
                        │        │
                        │        └─► "flat" | "solid" | "dashed" | (omitted)
                        │
                        └─► "blue" | "red" | "green" | "teal" | "dark" | ...
```

### 5.1. Grammar Token Breakdown

1. **`<color>` (Color Token)**:
   - Any color name available in `DefaultColors`, `CssColors`, or `Colors`.
   - Matching is case-insensitive (e.g. `"blue"`, `"Blue"`, `"deepskyblue"`, `"darkorange"`).
   - If omitted, the default primary accent color (`DefaultStyleColors.Blue`) is used.

2. **`<type>` (Structural / Fill Type)**:
   - **`(omitted / default)`**: Both fill and border outline are active. Line is solid.
   - **`flat`**: Solid fill color with **no border outline** (`line_width=0`). Ideal for modern card cards and badges.
   - **`solid`**: Transparent fill (`fill_color=Colors.Transparent`) with a **solid border outline**. Ideal for wireframes and subnets.
   - **`dashed`**: Transparent fill with a **dashed border outline** (`line_style="dashed"`). Ideal for boundaries, regions, and future states.

3. **`<weight>` (Stroke Width & Font Weight)**:
   - **`light`**: Line border width is halved (0.75 px). Font weight is light (`Font.SANSSERIF_LIGHT`). Icons render in thin style.
   - **`(omitted / default)`**: Standard line border width (1.5 px). Font weight is regular (`Font.SANSSERIF_REGULAR`).
   - **`bold`**: Line border width is increased to 2.25 px. Font weight is bold (`Font.SANSSERIF_BOLD`).

### 5.2. Combinations and Shortcut Examples

| Shorthand String | Resolved Fill | Resolved Line | Line Style | Line Width | Font Weight |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `""` or `None` | Blue | Black | Solid | 1.5 | Regular |
| `"light"` | Blue | Black | Solid | 0.75 | Light |
| `"bold"` | Blue | Black | Solid | 2.25 | Bold |
| `"flat"` | Blue | None | None | 0.0 | Regular |
| `"solid"` | Transparent | Blue | Solid | 1.5 | Regular |
| `"dashed"` | Transparent | Blue | Dashed | 1.5 | Regular |
| `"solid_light"` | Transparent | Blue | Solid | 0.75 | Light |
| `"solid_bold"` | Transparent | Blue | Solid | 2.25 | Bold |
| `"dashed_light"` | Transparent | Blue | Dashed | 0.75 | Light |
| `"dashed_bold"` | Transparent | Blue | Dashed | 2.25 | Bold |
| `"red"` | Red | Red | Solid | 1.5 | Regular |
| `"red_light"` | Red | Red | Solid | 0.75 | Light |
| `"red_bold"` | Red | Red | Solid | 2.25 | Bold |
| `"red_flat"` | Red | None | None | 0.0 | Regular |
| `"red_solid"` | Transparent | Red | Solid | 1.5 | Regular |
| `"red_solid_bold"`| Transparent | Red | Solid | 2.25 | Bold |
| `"teal_dashed"` | Transparent | Teal | Dashed | 1.5 | Regular |
| `"muted_flat"` | Muted | None | None | 0.0 | Regular |

### 5.3. Code Demonstration of Shorthand Variations

```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=140, height=70)

# Column positions
x_coords = [20, 50, 80, 110]
y_top = 45
y_bot = 15

# Row 1: Flat fills (no border) vs Solid outlines (no fill)
rectangle((x_coords[0], y_top), width=24, height=18, style=Styles.blue_flat)
text((x_coords[0], y_top), "blue_flat", style=Styles.white_bold)

rectangle((x_coords[1], y_top), width=24, height=18, style=Styles.green_flat)
text((x_coords[1], y_top), "green_flat", style=Styles.white_bold)

rectangle((x_coords[2], y_top), width=24, height=18, style=Styles.red_solid)
text((x_coords[2], y_top), "red_solid", style=Styles.red)

rectangle((x_coords[3], y_top), width=24, height=18, style=Styles.purple_dashed)
text((x_coords[3], y_top), "purple_dashed", style=Styles.purple)

# Row 2: Weight variations (light, standard, bold)
rectangle((x_coords[0], y_bot), width=24, height=18, style=Styles.orange_solid)
text((x_coords[0], y_bot), "solid", style=Styles.orange)

rectangle((x_coords[1], y_bot), width=24, height=18, style=Styles.orange_bold)
text((x_coords[1], y_bot), "bold", style=Styles.orange_bold)

rectangle((x_coords[2], y_bot), width=24, height=18, style=Styles.orange_flat)
text((x_coords[2], y_bot), "flat", style=Styles.white_bold)

# Connecting line showcasing weight
line((x_coords[0] - 12, 32), (x_coords[3] + 12, 32), style=Styles.muted_dashed)

save()
```

---

## 6. Complete Style Matrix & Element Compatibility

Not every visual property applies to every drawing element. For example, lines do not possess interior fills, and text elements do not possess perimeter borders. Drawlib gracefully applies only the valid properties of each style to each element.

### 6.1. Compatibility Matrix

```text
┌─────────────────┬───────────┬──────────────┬─────────────┬─────────────┬──────────────┬─────────────┐
│  Drawing Item   │  Default  │ Light / Bold │    Flat     │    Solid    │ Solid Light/ │ Dashed All  │
│                 │ (<color>) │ (<color>_*)  │ (<color>_*) │ (<color>_*) │  Solid Bold  │ (<color>_*) │
├─────────────────┼───────────┼──────────────┼─────────────┼─────────────┼──────────────┼─────────────┤
│ Shapes          │     ✓     │      ✓       │      ✓      │      ✓      │      ✓       │      ✓      │
│ Lines & Connect │     ✓     │      ✓       │     N/A     │      ✓      │      ✓       │      ✓      │
│ Text            │     ✓     │      ✓       │     N/A     │     N/A     │     N/A      │     N/A     │
│ Shape Embedded  │     ✓     │      ✓       │     N/A     │     N/A     │     N/A      │     N/A     │
│ Phosphor Icons  │     ✓     │      ✓       │  ✓ (Fill)   │     N/A     │     N/A      │     N/A     │
│ GCP Icons       │     ✓     │      ✓       │  ✓ (Tint)   │      ✓      │      ✓       │      ✓      │
│ Image Frames    │     ✓     │      ✓       │  ✓ (No line)│      ✓      │      ✓       │      ✓      │
└─────────────────┴───────────┴──────────────┴─────────────┴─────────────┴──────────────┴─────────────┘
```

### 6.2. Element-Specific Resolution Rules

1. **Shapes (`rectangle`, `circle`, `polygon`, `wedge`, `donut`, `star`, etc.)**:
   - Supports 100% of preset variations.
   - `flat` strips border outline by setting `line_width=0`.
   - `solid` removes background fill by setting `fill_color=Colors.Transparent`.
   - `dashed` sets `fill_color=Colors.Transparent` and `line_style="dashed"`.
   - `light` and `bold` scale `line_width` to 0.75 and 2.25 respectively.

2. **Lines & Connectors (`line`, `lines`, `bezier`, `arrow`, `line_curved`)**:
   - Lines do not have an interior fill; they only have stroke properties (`line_color`, `line_width`, `line_style`).
   - Suffixes `solid`, `dashed`, `light`, `bold` work seamlessly.
   - Applying `flat` to a line is an anti-pattern because `flat` sets `line_width=0`, making the line invisible.

3. **Text (`text`, `text_vertical`, shape `textstyle`)**:
   - Text elements only extract `text_color`, `text_size`, and `text_font`.
   - The `<color>` token controls `text_color`.
   - Weight tokens `light` and `bold` automatically select corresponding typography fonts:
     - `light` -> `Font.SANSSERIF_LIGHT`
     - `default` -> `Font.SANSSERIF_REGULAR`
     - `bold` -> `Font.SANSSERIF_BOLD`
   - Outline tokens (`flat`, `solid`, `dashed`) have no effect on text glyphs.

4. **Icons (`drawlib.icons.phosphor`, `drawlib.icons.gcp`)**:
   - **Phosphor Vector Font Icons**:
     - `<color>` maps to `text_color` (glyph color).
     - `flat` triggers `icon_style="fill"` (solid silhouette icon).
     - `light` maps to `icon_style="thin"` or `icon_style="light"`.
     - `bold` maps to `icon_style="bold"`.
   - **GCP Architecture Icons**:
     - Render multi-color graphics by default.
     - `solid`, `dashed`, and weight modifiers apply to the surrounding rectangular icon boundary frame.
     - `flat` ensures the boundary frame has zero border outline.

---

## 7. Creating Custom Preset Styles

In enterprise projects and client presentations, you often need custom color palettes and typography rules that match specific brand guidelines. Drawlib allows you to define custom style catalogs by subclassing `BaseStyles`.

### 7.1. Direct Instantiation of BaseStyles

You can construct a one-off `BaseStyles` instance directly with custom `Style` objects:

```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.preset_colors import Color
from drawlib.shapes import circle, rectangle
from drawlib.types import BaseStyles, Style

# Brand corporate identity colors
CORP_NAVY = Color.from_hex("#0D1B2A")
CORP_CYAN = Color.from_hex("#00A896")
CORP_GOLD = Color.from_hex("#F4A261")

brand_preset = BaseStyles(
    background_color=(250, 250, 252, 1.0),
    primary=Style(shape_fill_color=CORP_CYAN, shape_line_color=CORP_NAVY, shape_line_width=2.0),
    light=Style(shape_fill_color=CORP_CYAN, shape_line_color=CORP_NAVY, shape_line_width=1.0),
    bold=Style(shape_fill_color=CORP_GOLD, shape_line_color=CORP_NAVY, shape_line_width=3.0),
    flat=Style(shape_fill_color=CORP_CYAN, shape_line_width=0.0),
    solid=Style(shape_fill_color=(0, 0, 0, 0.0), shape_line_color=CORP_NAVY, shape_line_width=2.0),
    dashed=Style(shape_fill_color=(0, 0, 0, 0.0), shape_line_color=CORP_NAVY, shape_line_width=2.0, shape_line_style="dashed"),
)

setup(width=100, height=40, background_color=brand_preset.background_color)

rectangle((30, 20), width=30, height=20, style=brand_preset.primary)
circle((80, 20), radius=10, style=brand_preset.bold)

save()
```

### 7.2. Domain-Driven Subclassing with Type Hints

Subclassing `BaseStyles` provides IDE autocompletion, type safety, field validation, and dictionary iteration:

```python
from drawlib.preset_colors import Color
from drawlib.styles import Colors
from drawlib.types import BaseStyles, Style


class CloudPlatformStyles(BaseStyles):
    """Custom enterprise styling catalog for cloud infrastructure diagrams."""

    # Canvas default overrides
    background_color: tuple[int, int, int, float] = (248, 249, 250, 1.0)

    # Standard preset roles
    primary: Style
    light: Style
    bold: Style
    flat: Style
    solid: Style
    dashed: Style

    # Domain-specific semantic roles
    vpc_boundary: Style
    public_subnet: Style
    private_subnet: Style
    firewall_block: Style
    active_worker: Style


# Factory function returning fully configured domain styles
def get_cloud_styles() -> CloudPlatformStyles:
    c_blue = Color.from_hex("#1a73e8")
    c_green = Color.from_hex("#34a853")
    c_red = Color.from_hex("#ea4335")
    c_gray = Color.from_hex("#5f6368")

    return CloudPlatformStyles(
        primary=Style(fill_color=c_blue, line_color=c_gray, line_width=1.5),
        light=Style(fill_color=c_blue, line_color=c_gray, line_width=0.75),
        bold=Style(fill_color=c_blue, line_color=c_gray, line_width=2.5),
        flat=Style(fill_color=c_blue, line_width=0),
        solid=Style(fill_color=Colors.Transparent, line_color=c_blue, line_width=1.5),
        dashed=Style(fill_color=Colors.Transparent, line_color=c_blue, line_width=1.5, line_style="dashed"),
        # Domain roles
        vpc_boundary=Style(
            fill_color=Colors.Transparent,
            line_color=c_blue,
            line_width=2.0,
            line_style="dashed",
        ),
        public_subnet=Style(
            fill_color=(235, 248, 255, 0.6),
            line_color=c_blue,
            line_width=1.0,
            line_style="dotted",
        ),
        private_subnet=Style(
            fill_color=(240, 240, 240, 0.6),
            line_color=c_gray,
            line_width=1.0,
            line_style="dotted",
        ),
        firewall_block=Style(
            fill_color=c_red,
            line_color=Colors.Black,
            line_width=1.5,
        ),
        active_worker=Style(
            fill_color=c_green,
            line_color=Colors.Black,
            line_width=1.5,
        ),
    )
```

### 7.3. Iteration, Serialization, and Dictionary Access

`BaseStyles` provides robust Pythonic access patterns:

```python
cloud_styles = get_cloud_styles()

# 1. Dictionary item indexing
primary_style = cloud_styles["primary"]

# 2. Safe retrieval with fallback default
custom_metric = cloud_styles.get("latency_alert", cloud_styles.primary)

# 3. Iterating all defined fields
for field_name, style_obj in cloud_styles:
    if isinstance(style_obj, Style):
        print(f"Role: {field_name}, Line Width: {style_obj.line_width}")

# 4. Extracting only Style objects as a dictionary
style_dict = cloud_styles.styles()
print(f"Total defined style roles: {len(style_dict)}")
```

---

## 8. Applying Styles Across Multi-Element Diagrams

To understand the power of preset styling, consider realistic diagrams combining shapes, lines, icons, and text. Consistent use of semantic presets creates immediate visual clarity.

### 8.1. Production Microservice Architecture

The following diagram demonstrates how color and style variations distinguish user ingress, routing, processing, caching, and persistence:

```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=140, height=90)

# Section Headers
text((70, 84), "Enterprise E-Commerce Microservices", style=Styles.bold, size=18)
text((70, 78), "Synchronous REST Ingress & Asynchronous Event Bus", style=Styles.dark, size=12)

# Subnet / Boundary Containers
rectangle((70, 42), width=132, height=60, r=4, style=Styles.muted_dashed)
text((22, 68), "Internal VPC (10.0.0.0/16)", style=Styles.muted_bold, size=11)

# Tier 1: External Client & API Gateway
rectangle((22, 42), width=22, height=30, r=2, style=Styles.blue_solid)
phosphor.user((22, 50), width=9, style=Styles.blue)
text((22, 40), "Client Apps", style=Styles.blue_bold, size=11)
text((22, 33), "Web / Mobile", style=Styles.dark, size=9)

rectangle((50, 42), width=22, height=30, r=2, style=Styles.teal_flat)
phosphor.cloud((50, 50), width=9, style=Styles.white_bold)
text((50, 40), "API Gateway", style=Styles.white_bold, size=11)
text((50, 33), "Rate Limiting", style=Styles.white, size=9)

# Tier 2: Backend Core Services
rectangle((80, 53), width=24, height=18, r=2, style=Styles.green_bold)
text((80, 56), "Order Service", style=Styles.green_bold, size=11)
text((80, 48), "gRPC :8081", style=Styles.dark, size=9)

rectangle((80, 27), width=24, height=18, r=2, style=Styles.green_bold)
text((80, 30), "Payment Service", style=Styles.green_bold, size=11)
text((80, 22), "gRPC :8082", style=Styles.dark, size=9)

# Tier 3: Asynchronous Pub/Sub Queue & Storage
rectangle((114, 53), width=22, height=18, r=2, style=Styles.purple_flat)
phosphor.broadcast((114, 56), width=7, style=Styles.white_bold)
text((114, 48), "Kafka Broker", style=Styles.white_bold, size=10)

rectangle((114, 27), width=22, height=18, r=2, style=Styles.navy_solid)
phosphor.database((114, 31), width=7, style=Styles.navy)
text((114, 22), "PostgreSQL HA", style=Styles.navy_bold, size=10)

# Connectors with semantic weights
line((33, 42), (39, 42), arrowhead="->", style=Styles.blue_bold)
line((61, 46), (68, 53), arrowhead="->", style=Styles.bold)
line((61, 38), (68, 27), arrowhead="->", style=Styles.bold)
line((92, 53), (103, 53), arrowhead="->", style=Styles.purple_dashed)
line((92, 27), (103, 27), arrowhead="<->", style=Styles.navy_bold)

save()
```

### 8.2. State Machine Diagram

Preset styles make state transitions intuitive by mapping distinct semantic meanings to colors:
- Blue = Initial / Start State
- Green = Active / Normal Execution
- Orange = Paused / Pending Review
- Red = Failed / Terminated Error State

```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=130, height=50)

# Start State
circle((15, 25), radius=5, style=Styles.blue_flat)
text((15, 14), "Initial", style=Styles.blue_bold, size=10)

# Processing State
rectangle((45, 25), width=22, height=16, r=3, style=Styles.green_bold)
text((45, 27), "Validating", style=Styles.green_bold, size=11)
text((45, 20), "Worker Poll", style=Styles.dark, size=9)

# Decision Branches: Success vs Failure
rectangle((80, 36), width=22, height=14, r=3, style=Styles.green_flat)
text((80, 36), "Processed", style=Styles.white_bold, size=10)

rectangle((80, 14), width=22, height=14, r=3, style=Styles.red_flat)
text((80, 14), "Rejected", style=Styles.white_bold, size=10)

# Final State
circle((115, 36), radius=5, style=Styles.green_bold)
circle((115, 36), radius=3.2, style=Styles.green_flat)
text((115, 24), "Completed", style=Styles.green_bold, size=10)

# Transitions
line((20, 25), (34, 25), arrowhead="->", style=Styles.dark_bold)
text((27, 28), "submit", style=Styles.dark, size=9)

line((56, 29), (69, 36), arrowhead="->", style=Styles.green_bold)
text((60, 37), "valid", style=Styles.green, size=9)

line((56, 21), (69, 14), arrowhead="->", style=Styles.red_bold)
text((60, 13), "invalid", style=Styles.red, size=9)

line((91, 36), (110, 36), arrowhead="->", style=Styles.green_bold)

save()
```

### 8.3. Enterprise Data Lakehouse Architecture (Medallion Pattern)

Multi-element architectures frequently utilize the **Medallion Pattern** (Raw Ingestion -> Bronze -> Silver -> Gold -> Analytics). Preset styles make distinct processing tiers instantly recognizable:

- **Brown / Orange (`brown_flat`, `orange_solid`)**: Raw Ingestion & Bronze Landing (unfiltered CDC & Kafka logs).
- **Steel / Gray (`muted_flat`, `steel_solid_bold`)**: Cleansed, deduplicated, and enriched Delta tables.
- **Gold / Yellow (`yellow_flat`, `green_solid_bold`)**: Business-level aggregates, feature stores, and BI marts.
- **Teal / Navy (`teal_solid`, `navy_bold`)**: Query engines, dashboards, and automated ML pipelines.

```drawlib show-code
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=150, height=85)

# Architecture Title & Subtitle
text((75, 78), "Enterprise Medallion Data Lakehouse Architecture", style=Styles.bold, size=18)
text((75, 72), "Multi-Tier Ingestion, Delta Lake Curation, & BI Analytics", style=Styles.dark, size=11)

# Tier 1: Ingestion Sources
rectangle((20, 40), width=22, height=44, r=2, style=Styles.orange_solid)
phosphor.broadcast((20, 54), width=7, style=Styles.orange)
text((20, 46), "IoT / CDC", style=Styles.orange_bold, size=10)
phosphor.file_csv((20, 34), width=7, style=Styles.orange)
text((20, 26), "Batch Files", style=Styles.orange_bold, size=10)

# Tier 2: Bronze Layer (Raw Storage)
rectangle((52, 40), width=24, height=44, r=2, style=Styles.brown_flat)
phosphor.database((52, 53), width=8, style=Styles.white_bold)
text((52, 43), "Bronze Tier", style=Styles.white_bold, size=11)
text((52, 36), "Raw Append", style=Styles.white, size=9)
text((52, 28), "Parquet / JSON", style=Styles.white, size=8)

# Tier 3: Silver Layer (Cleaned & Enriched)
rectangle((86, 40), width=24, height=44, r=2, style=Styles.steel_bold)
phosphor.check_circle((86, 53), width=8, style=Styles.steel)
text((86, 43), "Silver Tier", style=Styles.steel_bold, size=11)
text((86, 36), "Cleaned / Joined", style=Styles.dark, size=9)
text((86, 28), "Delta Tables", style=Styles.dark, size=8)

# Tier 4: Gold Layer (Business Aggregates)
rectangle((120, 52), width=24, height=22, r=2, style=Styles.green_flat)
phosphor.chart_bar((120, 58), width=7, style=Styles.white_bold)
text((120, 49), "Gold Marts", style=Styles.white_bold, size=10)
text((120, 44), "Star Schemas", style=Styles.white, size=8)

# Tier 5: Consumers (ML & BI)
rectangle((120, 25), width=24, height=22, r=2, style=Styles.teal_bold)
phosphor.cpu((120, 31), width=7, style=Styles.teal)
text((120, 22), "ML Models", style=Styles.teal_bold, size=10)
text((120, 17), "Serving API", style=Styles.dark, size=8)

# Connectors with Flow Arrows
line((31, 40), (40, 40), arrowhead="->", style=Styles.orange_bold)
line((64, 40), (74, 40), arrowhead="->", style=Styles.dark_bold)
line((98, 45), (108, 52), arrowhead="->", style=Styles.green_bold)
line((98, 35), (108, 25), arrowhead="->", style=Styles.teal_bold)

save()
```

---

## 9. Advanced Dynamic Resolution with `get_style()`

When programmatic or conditional styling is required (e.g., dynamically altering a shape's color based on telemetry data or configuration parameters), `get_style()` acts as a universal factory.

### 9.1. Resolver Mechanics

The `get_style()` function accepts three input forms:

1. **`Style` instance**: Returns a deep copy of the provided object.
2. **`None` or `""`**: Returns a deep copy of the active preset's `primary` style.
3. **`str` name**: Resolves standard role names (`"primary"`, `"light"`, `"bold"`, `"flat"`, `"solid"`, `"dashed"`, etc.) or compound color expressions (`"<color>_<type>_<weight>"`).

```python
from drawlib.preset_styles import get_style
from drawlib.types import Style

# 1. Copying existing style
s1 = Style(fill_color=(10, 20, 30), line_width=3.0)
s2 = get_style(s1)
assert s1 is not s2  # Guaranteed deep copy

# 2. Resolving shorthand compound tokens
s_alert = get_style("red_solid_bold")
assert s_alert.line_width == 2.25
assert s_alert.fill_color == (0, 0, 0, 0.0)  # Transparent fill

# 3. Dynamic styling based on runtime condition
def get_node_style(health_status: str) -> str:
    status_map = {
        "HEALTHY": "green_solid",
        "DEGRADED": "orange_solid_bold",
        "UNHEALTHY": "red_flat",
    }
    return status_map.get(health_status, "gray_dashed")
```

### 9.2. How `get_style()` Resolves Tokens Internally

Under the hood, `_officials.py` processes the string through a deterministic sequence:

1. Check if the string matches one of the canonical pre-built role keys:
   `["primary", "light", "bold", "flat", "solid", "dashed", "solid_light", "solid_bold", "dashed_light", "dashed_bold"]`.
2. If not an exact match, check if it ends with `_{role_key}`. If found, split into `<color_name>` and `<preset_name>`.
3. Resolve `<color_name>` against `DefaultColors`, `CssColors`, and `Colors`.
4. Clone the base role template corresponding to `<preset_name>` (or `primary` if no role was appended).
5. Mutate the cloned style:
   - Assign `text_color = color`
   - Assign `line_color = color`
   - If `fill_color != Colors.Transparent`, assign `fill_color = color`
6. Return the finalized `Style` instance.

---

## 10. Common Pitfalls, Anti-Patterns, and Debugging

### Pitfall 1: Expecting String Color Names Inside `Style(...)`

`Style()` requires actual RGB/RGBA numeric tuples for colors. Passing strings like `Style(fill_color="red")` will raise a validation error. String shortcuts are exclusively interpreted by the `style` argument of drawing functions or by `get_style()`.

```python
# INCORRECT (Raises ValidationError)
# s = Style(fill_color="red")

# CORRECT: Pass color constant
from drawlib.preset_colors import DefaultColors

s = Style(fill_color=DefaultColors.Red)

# CORRECT: Or resolve via get_style
s = get_style("red_flat")
```

### Pitfall 2: Attempting Direct Mutation on Frozen Catalogs

Official preset style classes and active singletons (`Styles`, `DefaultStyles`, `GoogleStyles`, `MonochromeStyles`) are immutable and frozen. Attempting to assign new attributes directly will raise an error:

```python
from drawlib.styles import Styles

# INVALID: Raises error because preset styles are frozen
# Styles.primary = ...

# SAFE: Derive modified catalog or styles via patch() or copy()
custom_styles = Styles.patch(primary=Styles.bold)
custom_style = Styles.primary.patch(line_width=10.0)
```

### Pitfall 3: Applying `flat` to Line Elements

The `flat` modifier explicitly strips border lines by configuring `line_width=0`. Because `line()` objects possess no interior fill, applying a `_flat` style renders the line completely invisible.

- For lines, always use `""`, `_solid`, or `_dashed` along with `_light` or `_bold` (e.g. `"blue"`, `"green_dashed"`, `"red_bold"`).

### Pitfall 4: Misinterpreting `flat` vs `solid`

A common source of confusion for newcomers is the distinction between `flat` and `solid`:

- **`flat`**: Solid fill color, **zero border outline**. Think of a borderless flat UI badge or solid card.
- **`solid`**: **Solid continuous line border**, with a **transparent interior fill**. Think of a hollow wireframe container.

---

## 11. Quick Reference & Cheat Sheet

### 11.1. Color Shortcut Reference

```text
Default Colors:
  red           RGB(255, 23, 23)     green         RGB(15, 127, 15)
  blue          RGB(31, 31, 255)     black         RGB(0, 0, 0)
  white         RGB(255, 255, 255)

Popular Default Colors:
  teal          RGB(15, 127, 127)    orange        RGB(255, 120, 0)
  navy          RGB(15, 25, 110)     purple        RGB(130, 20, 160)
  gray          RGB(140, 152, 170)   amber         RGB(215, 134, 20)
  aqua          RGB(47, 239, 239)    olive         RGB(127, 127, 31)
  brown         RGB(145, 45, 25)     pink          RGB(255, 50, 150)
  steel         RGB(96, 96, 143)     yellow        RGB(255, 230, 0)
```

### 11.2. Structure & Weight Matrix

| Suffix | Fill Behavior | Outline Behavior | Border Line Style | Border Width | Font Weight |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `""` | Color Fill | Black/Color Border | Solid | 1.5 px | Regular |
| `_light` | Color Fill | Black/Color Border | Solid | 0.75 px | Light |
| `_bold` | Color Fill | Black/Color Border | Solid | 2.25 px | Bold |
| `_flat` | Color Fill | No Border | None | 0.0 px | Regular |
| `_solid` | Transparent | Color Border | Solid | 1.5 px | Regular |
| `_solid_light` | Transparent | Color Border | Solid | 0.75 px | Light |
| `_solid_bold` | Transparent | Color Border | Solid | 2.25 px | Bold |
| `_dashed` | Transparent | Color Border | Dashed | 1.5 px | Regular |
| `_dashed_light`| Transparent | Color Border | Dashed | 0.75 px | Light |
| `_dashed_bold` | Transparent | Color Border | Dashed | 2.25 px | Bold |

### 11.3. Essential Code Snippets

```drawlib show-code
# Standard imports
from drawlib.canvas import save, setup
from drawlib.preset_styles import DefaultStyles, MonochromeStyles
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles
from drawlib.text import text

# Initialize canvas with default or custom catalog
setup(width=100, height=60)

# 1. Preset style usage
rectangle((25, 36), width=20, height=20, style=Styles.blue_flat, text="Flat", textstyle=Styles.white_bold)
rectangle((50, 36), width=20, height=20, style=Styles.green_bold, text="Solid", textstyle=Styles.green_bold)
circle((75, 36), radius=10, style=Styles.red_dashed, text="Dashed", textstyle=Styles.red_bold)

# 2. Dynamic style retrieval via key lookup
accent_style = DefaultStyles["teal_flat"]
circle((85, 48), radius=5, style=accent_style)

# 3. Dedicated monochrome catalog retrieval
rectangle((50, 12), width=80, height=12, style=MonochromeStyles.flat, text="Monochrome Catalog Banner", textstyle=MonochromeStyles.white_bold)

save()
```

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
