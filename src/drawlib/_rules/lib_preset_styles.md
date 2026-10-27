# Drawlib Preset Styles Guidelines

Drawlib provides a comprehensive, centralized preset style system in `drawlib.preset_styles` designed to enforce visual consistency, eliminate boilerplate styling code, and enable rapid diagram prototyping. Under the "Illustration as Code" philosophy, styling is treated as a systematic design system where shapes, lines, icons, text, and images adhere to cohesive color palettes, line widths, and typographical hierarchies.

> [!IMPORTANT]
> **Color Discipline: Avoid Rainbow Chaos (50%+ Neutral-Grounded Architecture)**:
> Never color every box in a diagram with saturated fills (`PrimaryFlat`, `AccentFlat`, `SuccessFlat`, `WarningFlat`). Overly colorful diagrams look amateurish and cause visual fatigue.
> - **Ground 50% or more of nodes in calm neutral or tinted-neutral cards**: `Styles.Neutral`, `Styles.NeutralFlat`, `Styles.PrimaryNeutral`, `Styles.SecondaryNeutral`, `Styles.BlueNeutral`, `Styles.TealNeutral`.
> - **Reserve saturated hero fills (`Styles.PrimaryFlat`, `Styles.AccentFlat` with `text_style=Styles.WhiteBold`)** strictly for the 1–2 most important focal points.
> - **Use `Styles.MutedDashed` or `Styles.Muted`** for boundary containers, VPCs, and clusters.

---

## 1. Architectural Philosophy & Core Concepts

In complex technical diagrams and architectural illustrations, manually specifying colors, line widths, borders, and fonts for every individual element leads to verbose, brittle, and visually inconsistent code. Drawlib addresses this through three core design principles:

1. **Systematic Semantic Roles**:
   Rather than hardcoding arbitrary colors, Drawlib organizes styles around 8 semantic roles (`Primary`, `Secondary`, `Accent`, `Warning`, `Neutral`, `Muted`, `Danger`, `Success`) across 17 orthogonal variants (`""` / `Bordered`, `Bold`, `Thin`, `Flat`, `Outline`, `OutlineBold`, `OutlineThin`, `Solid`, `SolidBold`, `SolidThin`, `Dashed`, `DashedBold`, `DashedThin`, `Dotted`, `DottedBold`, `DottedThin`).

2. **First-Class Object Referencing**:
   Styles are passed as strongly-typed `Style` instances directly from `drawlib.styles.Styles` (or `Styles`), e.g., `style=Styles.PrimaryFlat` or `style=Styles.AccentBold`. Passing arbitrary strings to `style` is rejected by Pydantic validation to ensure compile-time safety.

3. **Layered Object Models**:
   At the core of the preset style system is `BaseStyles` (a Pydantic `BaseModel` with dynamic metaclass resolution), which exposes standard role-based styles (`Primary`, `Secondary`, `Accent`, `Warning`, `Neutral`, `Muted`, `Danger`, `Success`), default canvas background colors, and font definitions. Users can inspect, copy, patch, or subclass these models to define enterprise brand guidelines.

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
   │  - DefaultColors (1..6)         │       │  - DefaultStyles (1..6)         │
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
                    │  Token parsing: <Color><Type><Weight>   │
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
| `DefaultStyles` | Model Class | Default design system style catalog (Level 4 primary centered; `DefaultStyles1`..`DefaultStyles6` available). |
| `GoogleStyles` | Model Class | Google Slides & Workspace brand style catalog. |
| `MonochromeStyles` | Model Class | Grayscale style catalog for print, papers, and e-ink. |
| `Style` | Data Model | Core style model representing visual attributes. |
| `BaseStyles` | Base Model | Pydantic BaseModel providing dict-like access, copy, and patch operations. |

---

## 3. Official Palette Catalogs

Drawlib ships with three pre-built, production-ready style catalogs (`DefaultStyles`, `GoogleStyles`, and `MonochromeStyles`). Each catalog organizes styles into **8 semantic roles** (`Primary`, `Secondary`, `Accent`, `Warning`, `Neutral`, `Muted`, `Danger`, `Success`) across **17 orthogonal variants** alongside default canvas background colors, chart palettes (`Chart1`..`Chart6`), and typographical defaults:

```text
┌───────────────────────────────────────────────────────────────────────────────────────┐
│                                   BaseStyles Model                                    │
├───────────────────────────────────────────────────────────────────────────────────────┤
│ + background_color: ColorType = (255, 255, 255, 1.0)                                  │
│ + sourcecode_font: FontSourceCode = FontSourceCode.SOURCECODEPRO                      │
├───────────────────────────────────────────────────────────────────────────────────────┤
│ 8 Semantic Roles (17 orthogonal variants each: "", Bordered, Bold, Thin, Flat,        │
│                   Outline, OutlineBold, OutlineThin, Solid, SolidBold, SolidThin,     │
│                   Dashed, DashedBold, DashedThin, Dotted, DottedBold, DottedThin):    │
│   - Primary: Core application logic, main components                                  │
│   - Secondary: Databases, message queues, auxiliary services                          │
│   - Accent: Gateways, clients, focal points                                           │
│   - Warning: Alerts, transient states, review gates                                   │
│   - Neutral: Calm card surfaces, worker nodes, base containers                        │
│   - Muted: Boundaries, VPCs, subnets, containers                                      │
│   - Danger: Errors, alerts, security risks                                            │
│   - Success: Completed milestones, healthy status                                     │
├───────────────────────────────────────────────────────────────────────────────────────┤
│ Tinted Neutral Cards (Bordered and Flat variants):                                    │
│   - Semantic: PrimaryNeutral, SecondaryNeutral, AccentNeutral, WarningNeutral, ...    │
│   - Named Hues: GrayNeutral, BlueNeutral, GreenNeutral, TealNeutral, PurpleNeutral,   │
│                 AmberNeutral, RedNeutral, OrangeNeutral, PinkNeutral                  │
└───────────────────────────────────────────────────────────────────────────────────────┘
```

### 3.1. DefaultStyles (`"default"`)

The standard catalog optimized for technical documentation, flowcharts, and software architecture diagrams. It features systematic 6-tone chromatic scales (`DefaultStyles1` through `DefaultStyles6`, where `DefaultStyles` aliases `DefaultStyles4`), neutral grays, and 8 semantic roles.

- **Primary Colors**: 8 chromatic hues across 6 tone levels (`Blue1..6`, `Green1..6`, `Red1..6`, `Orange1..6`, `Amber1..6`, `Purple1..6`, `Teal1..6`, `Pink1..6`), 8 gray levels (`Gray1` to `Gray8`), `Black`, `White`, and standard primaries.
- **Visual Design**:
  - `Primary` / `PrimaryBordered`: `Blue4` fill, `Blue6` border (width `1.5`), sans-serif regular font.
  - `PrimaryThin`: `Blue4` fill, `Blue6` border (width `0.75`), sans-serif thin font, thin icons.
  - `PrimaryBold`: `Blue4` fill, `Blue6` border (width `2.5`), sans-serif bold font, bold icons.
  - `PrimaryFlat`: `Blue4` fill, borderless (`shape_line_width=0`), fill-style icons.
  - `PrimaryOutline` / `PrimarySolid`: Transparent fill, `Blue4` border (width `1.5`), regular icons.
  - `PrimaryDashed`: Transparent fill, `Blue4` dashed border (width `1.5`), regular icons.
  - `PrimaryDotted`: Transparent fill, `Blue4` dotted border (width `1.5`), regular icons.

```python
from drawlib.preset_styles import DefaultStyles
from drawlib.styles import Styles

default_catalog = Styles  # Defaults to DefaultStyles

print("Default Primary Fill:", default_catalog.Primary.shape_fill_color)
print("Default Primary Line:", default_catalog.Primary.shape_line_color)
print("Default Line Width:", default_catalog.Primary.shape_line_width)
print("Default Background:", DefaultStyles.background_color)
```

### 3.2. GoogleStyles (`"google"`)

Designed around Google Workspace, Material Design, and Google Cloud presentation aesthetics. It pairs Google Blue, Teal/Green, Yellow/Amber, and Red with clean Slate neutrals.

- **Primary Colors**: Google Blue (`#1A73E8`), Google Green (`#1E8E3E`), Google Yellow/Amber (`#F9AB00`), Google Red (`#D93025`), and Slate grays (`Gray1` to `Gray8`).
- **Visual Design**: Exposes the exact same 8 semantic roles, 17 orthogonal variants, and `*Neutral` card tokens as `DefaultStyles`, allowing zero-code-change theme switching via `drawlib init -s google`.

```python
from drawlib.preset_styles import GoogleStyles

print("Google Primary Fill:", GoogleStyles.Primary.shape_fill_color)
print("Google PrimaryNeutral Fill:", GoogleStyles.PrimaryNeutral.shape_fill_color)
```

### 3.3. MonochromeStyles (`"monochrome"`)

Specially designed for printed engineering manuals, formal academic papers, patents, and grayscale e-ink displays. It uses pure black, white, and balanced intermediate gray tones (`Gray1` to `Gray8`) to maintain razor-sharp contrast without color dependencies.

- **Primary Colors**: `Black` (`#000000`), `Gray1` (`#F5F5F5`) to `Gray8` (`#191919`), `White` (`#FFFFFF`).
- **Visual Design**:
  - `Primary`: White fill, black border (width `1.5`), black text, sans-serif regular font.
  - `PrimaryThin`: White fill, black border (width `0.75`), sans-serif light font.
  - `PrimaryBold`: White fill, black border (width `2.5`), sans-serif bold font.
  - `PrimaryFlat`: Solid black fill, borderless (`shape_line_width=0`).
  - `PrimaryOutline` / `PrimarySolid`: Transparent fill, black border (width `1.5`).
  - `PrimaryDashed`: Transparent fill, black dashed border (width `1.5`).

```drawlib code=show
from drawlib.canvas import save, setup
from drawlib.preset_styles import MonochromeStyles
from drawlib.shapes import rectangle
from drawlib.text import text

setup(width=120, height=40)
mono = MonochromeStyles

# White box with black outline
rectangle((30, 20), width=35, height=20, style=mono.Primary)
text((30, 20), "Primary (Outline)", style=mono.Primary)

# Solid black box with white text
rectangle((80, 20), width=35, height=20, style=mono.PrimaryFlat)
text((80, 20), "Flat (Filled)", style=mono.WhiteBold)

save()
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

## 5. Systematic Naming Rules & PascalCase Grammar

Every preset style follows a deterministic, composable PascalCase naming structure:

```text
                     Styles.<Color><Type><Weight>
                              │       │      │
                              │       │      └─► "Thin" | "Bold" | (omitted)
                              │       │
                              │       └─► "Flat" | "Solid" | "Dashed" | (omitted)
                              │
                              └─► "Blue" | "Red" | "Green" | "Teal" | "Dark" | ...
```

### 5.1. Grammar Token Breakdown

1. **`<Color>` (Color Token)**:
   - Any color name available in `DefaultColors`, `GoogleColors`, `MonochromeColors`, or semantic roles (`Primary`, `Secondary`, `Accent`, `Warning`, `Neutral`, `Muted`, `Light`, `Dark`, `Danger`, `Success`).
   - If omitted or using base role, the semantic anchor (e.g. `Primary`) is used.

2. **`<Type>` (Structural / Fill Type)**:
   - **`(omitted / default)` or `Bordered`**: Both fill and border outline are active. Line is solid.
   - **`Flat`**: Solid fill color with **no border outline** (`shape_line_width=0`). Ideal for modern cards and badges.
   - **`Outline` or `Solid`**: Transparent fill (`shape_fill_color=Colors.Transparent`) with a **solid border outline**. Ideal for wireframes and subnets.
   - **`Dashed`**: Transparent fill with a **dashed border outline** (`shape_line_style="dashed"`). Ideal for boundaries, regions, and future states.
   - **`Dotted`**: Transparent fill with a **dotted border outline** (`shape_line_style="dotted"`). Ideal for dependency links, soft boundaries, and degraded flows.

3. **`<Weight>` (Stroke Width & Font Weight)**:
   - **`Thin`**: Line border width is halved (`0.75` px). Font weight is thin (`Font.SANSSERIF_THIN`). Icons render in thin style.
   - **`(omitted / default)`**: Standard line border width (`1.5` px). Font weight is regular (`Font.SANSSERIF_REGULAR`).
   - **`Bold`**: Line border width is increased to `2.5` px. Font weight is bold (`Font.SANSSERIF_BOLD`).

### 5.2. Combinations and Preset Examples

| Style Token | Resolved Fill | Resolved Line | Line Style | Line Width | Font Weight |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Styles.Primary` (`PrimaryBordered`) | Blue | Black/Blue6 | Solid | 1.5 | Regular |
| `Styles.PrimaryThin` | Blue | Black/Blue6 | Solid | 0.75 | Thin |
| `Styles.PrimaryBold` | Blue | Black/Blue6 | Solid | 2.5 | Bold |
| `Styles.PrimaryFlat` | Blue | None | None | 0.0 | Regular |
| `Styles.PrimaryOutline` (`PrimarySolid`) | Transparent | Blue | Solid | 1.5 | Regular |
| `Styles.PrimaryDashed` | Transparent | Blue | Dashed | 1.5 | Regular |
| `Styles.PrimaryDotted` | Transparent | Blue | Dotted | 1.5 | Regular |
| `Styles.PrimarySolidThin` (`PrimaryOutlineThin`) | Transparent | Blue | Solid | 0.75 | Thin |
| `Styles.PrimarySolidBold` (`PrimaryOutlineBold`) | Transparent | Blue | Solid | 2.5 | Bold |
| `Styles.PrimaryDashedThin` | Transparent | Blue | Dashed | 0.75 | Thin |
| `Styles.PrimaryDashedBold` | Transparent | Blue | Dashed | 2.5 | Bold |
| `Styles.PrimaryDottedThin` | Transparent | Blue | Dotted | 0.75 | Thin |
| `Styles.PrimaryDottedBold` | Transparent | Blue | Dotted | 2.5 | Bold |
| `Styles.Neutral` | Neutral | Gray | Solid | 1.5 | Regular |
| `Styles.Warning` | Amber/Yellow | Black/Gray | Solid | 1.5 | Regular |
| `Styles.WarningDotted` | Transparent | Amber/Yellow | Dotted | 1.5 | Regular |
| `Styles.Red` | Red | Red | Solid | 1.5 | Regular |
| `Styles.RedThin` | Red | Red | Solid | 0.75 | Thin |
| `Styles.RedBold` | Red | Red | Solid | 2.5 | Bold |
| `Styles.RedFlat` | Red | None | None | 0.0 | Regular |
| `Styles.RedSolid` | Transparent | Red | Solid | 1.5 | Regular |
| `Styles.RedSolidBold` | Transparent | Red | Solid | 2.5 | Bold |
| `Styles.TealDashed` | Transparent | Teal | Dashed | 1.5 | Regular |
| `Styles.MutedFlat` | Muted | None | None | 0.0 | Regular |

### 5.3. Code Demonstration of Variations

```drawlib code=show
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=140, height=70)

# Column positions
x_coords = [20, 52, 84, 116]
y_top = 48
y_bot = 16

# Row 1: Flat fills vs Neutral cards vs Solid/Dashed outlines
rectangle((x_coords[0], y_top), width=26, height=18, style=Styles.PrimaryFlat)
text((x_coords[0], y_top), "PrimaryFlat", style=Styles.WhiteBold.patch(text_size=10))

rectangle((x_coords[1], y_top), width=26, height=18, style=Styles.Neutral)
text((x_coords[1], y_top), "Neutral", style=Styles.DarkBold.patch(text_size=10))

rectangle((x_coords[2], y_top), width=26, height=18, style=Styles.SecondaryNeutral)
text((x_coords[2], y_top), "SecNeutral", style=Styles.DarkBold.patch(text_size=10))

rectangle((x_coords[3], y_top), width=26, height=18, style=Styles.MutedDashed)
text((x_coords[3], y_top), "MutedDashed", style=Styles.MutedBold.patch(text_size=10))

# Row 2: Weight and Outline variations
rectangle((x_coords[0], y_bot), width=26, height=18, style=Styles.BlueNeutral)
text((x_coords[0], y_bot), "BlueNeutral", style=Styles.DarkBold.patch(text_size=10))

rectangle((x_coords[1], y_bot), width=26, height=18, style=Styles.TealNeutral)
text((x_coords[1], y_bot), "TealNeutral", style=Styles.DarkBold.patch(text_size=10))

rectangle((x_coords[2], y_bot), width=26, height=18, style=Styles.PrimarySolidBold)
text((x_coords[2], y_bot), "SolidBold", style=Styles.PrimaryBold.patch(text_size=10))

rectangle((x_coords[3], y_bot), width=26, height=18, style=Styles.AccentFlat)
text((x_coords[3], y_bot), "AccentFlat", style=Styles.WhiteBold.patch(text_size=10))

# Divider line showcasing dashed style
line((x_coords[0] - 13, 32), (x_coords[3] + 13, 32), style=Styles.MutedDashed)

save()
```

---

## 6. Complete Style Matrix & Element Compatibility

Not every visual property applies to every drawing element. For example, lines do not possess interior fills, and text elements do not possess perimeter borders. Drawlib gracefully applies only the valid properties of each style to each element.

### 6.1. Compatibility Matrix

```text
┌─────────────────┬───────────┬──────────────┬─────────────┬─────────────┬──────────────┬─────────────┐
│  Drawing Item   │  Default  │ Thin / Bold  │    Flat     │    Solid    │  Solid Thin/ │ Dashed All  │
│                 │ (<Color>) │ (<Color>*)   │ (<Color>*)  │ (<Color>*)  │  Solid Bold  │ (<Color>*)  │
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

1. **Shapes (`rectangle`, `circle(..., hole_ratio=...)`, `polygon`, `wedge`, `star`, etc.)**:
   - Supports 100% of preset variations.
   - `Flat` strips border outline by setting `shape_line_width=0`.
   - `Outline` / `Solid` removes background fill by setting `shape_fill_color=Colors.Transparent`.
   - `Dashed` sets `shape_fill_color=Colors.Transparent` and `shape_line_style="dashed"`.
   - `Dotted` sets `shape_fill_color=Colors.Transparent` and `shape_line_style="dotted"`.
   - `Thin` and `Bold` scale `shape_line_width` to `0.75` and `2.5` respectively.

2. **Lines & Connectors (`line`, `lines`, `line_bezier1`, `line_bezier2`, `lines_bezier`, `line_curved`, `lines_curved`, `line_arc`)**:
   - Lines do not have an interior fill; they only have stroke properties (`line_color`, `line_width`, `line_style`).
   - Suffixes `Solid`, `Dashed`, `Dotted`, `Thin`, `Bold` work seamlessly (`Thin` = `0.75`, default = `1.5`, `Bold` = `2.5`).
   - Applying `Flat` to a line is an anti-pattern because `Flat` sets `line_width=0` (or `shape_line_width=0`), which is intended for borderless filled shapes.

3. **Text (`text`, `text_vertical`, shape `text_style`)**:
   - Text elements only extract `text_color`, `text_size`, and `text_font`.
   - The `<Color>` token controls `text_color`.
   - Weight tokens `Thin` and `Bold` automatically select corresponding typography fonts:
     - `Thin` -> `Font.SANSSERIF_THIN`
     - `default` -> `Font.SANSSERIF_REGULAR`
     - `Bold` -> `Font.SANSSERIF_BOLD`
   - Outline tokens (`Flat`, `Solid`, `Dashed`, `Dotted`) have no effect on text glyphs.

4. **Icons (`drawlib.icons.phosphor`, `drawlib.icons.gcp`, `drawlib.icons.aws`, `drawlib.icons.azure`, etc.)**:
   - **Phosphor Vector Font Icons**:
     - `<Color>` maps to `text_color` (glyph color).
     - `Flat` triggers `icon_style="fill"` (solid silhouette icon).
     - `Thin` maps to `icon_style="thin"` or `icon_style="light"`.
     - `Bold` maps to `icon_style="bold"`.
   - **Raster / Cloud Architecture Icons**:
     - Render multi-color or monochrome graphics according to suite.

---

## 7. Creating Custom Preset Styles

In enterprise projects and client presentations, you often need custom color palettes and typography rules that match specific brand guidelines. Drawlib allows you to define custom style catalogs by subclassing `BaseStyles`.

### 7.1. Direct Instantiation of BaseStyles

You can construct a one-off `BaseStyles` instance directly with custom `Style` objects:

```drawlib code=show
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
    Primary=Style(shape_fill_color=CORP_CYAN, shape_line_color=CORP_NAVY, shape_line_width=2.0),
    PrimaryThin=Style(shape_fill_color=CORP_CYAN, shape_line_color=CORP_NAVY, shape_line_width=1.0),
    PrimaryBold=Style(shape_fill_color=CORP_GOLD, shape_line_color=CORP_NAVY, shape_line_width=3.0),
    PrimaryFlat=Style(shape_fill_color=CORP_CYAN, shape_line_width=0.0),
    PrimarySolid=Style(shape_fill_color=(0, 0, 0, 0.0), shape_line_color=CORP_NAVY, shape_line_width=2.0),
    PrimaryDashed=Style(shape_fill_color=(0, 0, 0, 0.0), shape_line_color=CORP_NAVY, shape_line_width=2.0, shape_line_style="dashed"),
)

setup(width=100, height=40, background_color=brand_preset.background_color)

rectangle((30, 20), width=30, height=20, style=brand_preset.Primary)
circle((80, 20), radius=10, style=brand_preset.PrimaryBold)

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
    Primary: Style
    PrimaryThin: Style
    PrimaryBold: Style
    PrimaryFlat: Style
    PrimarySolid: Style
    PrimaryDashed: Style

    # Domain-specific semantic roles
    VpcBoundary: Style
    PublicSubnet: Style
    PrivateSubnet: Style
    FirewallBlock: Style
    ActiveWorker: Style


# Factory function returning fully configured domain styles
def get_cloud_styles() -> CloudPlatformStyles:
    c_blue = Color.from_hex("#1a73e8")
    c_green = Color.from_hex("#34a853")
    c_red = Color.from_hex("#ea4335")
    c_gray = Color.from_hex("#5f6368")

    return CloudPlatformStyles(
        Primary=Style(shape_fill_color=c_blue, shape_line_color=c_gray, shape_line_width=1.5),
        PrimaryThin=Style(shape_fill_color=c_blue, shape_line_color=c_gray, shape_line_width=0.75),
        PrimaryBold=Style(shape_fill_color=c_blue, shape_line_color=c_gray, shape_line_width=2.5),
        PrimaryFlat=Style(shape_fill_color=c_blue, shape_line_width=0.0),
        PrimarySolid=Style(shape_fill_color=Colors.Transparent, shape_line_color=c_blue, shape_line_width=1.5),
        PrimaryDashed=Style(
            shape_fill_color=Colors.Transparent,
            shape_line_color=c_blue,
            shape_line_width=1.5,
            shape_line_style="dashed",
        ),
        # Domain roles
        VpcBoundary=Style(
            shape_fill_color=Colors.Transparent,
            shape_line_color=c_blue,
            shape_line_width=2.0,
            shape_line_style="dashed",
        ),
        PublicSubnet=Style(
            shape_fill_color=(235, 248, 255, 0.6),
            shape_line_color=c_blue,
            shape_line_width=1.0,
            shape_line_style="dotted",
        ),
        PrivateSubnet=Style(
            shape_fill_color=(240, 240, 240, 0.6),
            shape_line_color=c_gray,
            shape_line_width=1.0,
            shape_line_style="dotted",
        ),
        FirewallBlock=Style(
            shape_fill_color=c_red,
            shape_line_color=Colors.Black,
            shape_line_width=1.5,
        ),
        ActiveWorker=Style(
            shape_fill_color=c_green,
            shape_line_color=Colors.Black,
            shape_line_width=1.5,
        ),
    )
```

### 7.3. Iteration, Serialization, and Dictionary Access

`BaseStyles` provides robust Pythonic access patterns:

```python
cloud_styles = get_cloud_styles()

# 1. Dictionary item indexing
main_style = cloud_styles["Primary"]

# 2. Safe retrieval with fallback default
custom_metric = cloud_styles.get("LatencyAlert", cloud_styles.Primary)

# 3. Iterating all defined fields
for field_name, style_obj in cloud_styles:
    if isinstance(style_obj, Style):
        print(f"Role: {field_name}, Line Width: {style_obj.shape_line_width}")

# 4. Extracting only Style objects as a dictionary
style_dict = cloud_styles.styles()
print(f"Total defined style roles: {len(style_dict)}")
```

---

## 8. Applying Styles Across Multi-Element Diagrams

To understand the power of preset styling, consider realistic diagrams combining shapes, lines, icons, and text. Grounding 50%+ of nodes in calm neutral cards while reserving saturated fills (`PrimaryFlat`) for 1–2 focal components creates immediate visual hierarchy.

### 8.1. Production Microservice Architecture

The following diagram demonstrates how neutral cards and a single hero gateway distinguish user ingress, routing, processing, and persistence without rainbow chaos:

```drawlib code=show
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=140, height=90)

# Section Headers
text((70, 84), "Enterprise E-Commerce Microservices", style=Styles.DarkBold.patch(text_size=18))
text((70, 77), "Synchronous REST Ingress & Asynchronous Event Bus", style=Styles.Muted.patch(text_size=11))

# Subnet / Boundary Containers (Z-Layer 1)
rectangle((70, 40), width=132, height=62, style=Styles.MutedDashed.patch(shape_r=4))
text((24, 67), "Internal VPC (10.0.0.0/16)", style=Styles.MutedBold.patch(text_size=10))

# Tier 1: External Client (Neutral) & API Gateway (Hero PrimaryFlat)
rectangle((22, 40), width=22, height=30, style=Styles.Neutral.patch(shape_r=2))
phosphor.user((22, 48), width=8, style=Styles.Dark)
text((22, 38), "Client Apps", style=Styles.DarkBold.patch(text_size=10))
text((22, 31), "Web / Mobile", style=Styles.Muted.patch(text_size=8))

rectangle((50, 40), width=22, height=30, style=Styles.PrimaryFlat.patch(shape_r=2))
phosphor.cloud((50, 48), width=8, style=Styles.WhiteBold)
text((50, 38), "API Gateway", style=Styles.WhiteBold.patch(text_size=10))
text((50, 31), "Rate Limiting", style=Styles.White.patch(text_size=8))

# Tier 2: Backend Core Services (Calm Neutral Cards)
rectangle((80, 52), width=24, height=18, style=Styles.Neutral.patch(shape_r=2))
text((80, 55), "Order Service", style=Styles.DarkBold.patch(text_size=10))
text((80, 48), "gRPC :8081", style=Styles.Muted.patch(text_size=8))

rectangle((80, 28), width=24, height=18, style=Styles.Neutral.patch(shape_r=2))
text((80, 31), "Payment Service", style=Styles.DarkBold.patch(text_size=10))
text((80, 24), "gRPC :8082", style=Styles.Muted.patch(text_size=8))

# Tier 3: Asynchronous Pub/Sub Queue & Storage (Tinted Neutral Cards)
rectangle((114, 52), width=22, height=18, style=Styles.SecondaryNeutral.patch(shape_r=2))
phosphor.broadcast((114, 56), width=6, style=Styles.Dark)
text((114, 47), "Kafka Broker", style=Styles.DarkBold.patch(text_size=9))

rectangle((114, 28), width=22, height=18, style=Styles.PrimaryNeutral.patch(shape_r=2))
phosphor.database((114, 32), width=6, style=Styles.Dark)
text((114, 23), "PostgreSQL HA", style=Styles.DarkBold.patch(text_size=9))

# Connectors (Z-Layer 3)
line((33, 40), (39, 40), arrow_head="->", style=Styles.DarkBold)
line((61, 44), (68, 52), arrow_head="->", style=Styles.DarkBold)
line((61, 36), (68, 28), arrow_head="->", style=Styles.DarkBold)
line((92, 52), (103, 52), arrow_head="->", style=Styles.MutedDashedBold)
line((92, 28), (103, 28), arrow_head="<->", style=Styles.DarkBold)

save()
```

### 8.2. State Machine Diagram

Preset styles make state transitions intuitive while keeping the diagram calm and readable:

```drawlib code=show
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=130, height=52)

# Start State
circle((15, 26), radius=5, style=Styles.DarkFlat)
text((15, 15), "Initial", style=Styles.DarkBold.patch(text_size=10))

# Processing State (Hero Focal State)
rectangle((45, 26), width=24, height=16, style=Styles.PrimaryFlat.patch(shape_r=3))
text((45, 29), "Validating", style=Styles.WhiteBold.patch(text_size=10))
text((45, 22), "Worker Poll", style=Styles.White.patch(text_size=8))

# Decision Branches: Success vs Failure (Tinted Neutral Cards)
rectangle((82, 37), width=22, height=14, style=Styles.SuccessNeutral.patch(shape_r=3))
text((82, 37), "Processed", style=Styles.DarkBold.patch(text_size=10))

rectangle((82, 15), width=22, height=14, style=Styles.DangerNeutral.patch(shape_r=3))
text((82, 15), "Rejected", style=Styles.DarkBold.patch(text_size=10))

# Final State
circle((115, 37), radius=5, style=Styles.DarkOutlineBold)
circle((115, 37), radius=3, style=Styles.DarkFlat)
text((115, 26), "Completed", style=Styles.DarkBold.patch(text_size=10))

# Transitions
line((20, 26), (33, 26), arrow_head="->", style=Styles.DarkBold)
text((26.5, 30), "submit", style=Styles.Dark.patch(text_size=9))

line((57, 30), (71, 37), arrow_head="->", style=Styles.DarkBold)
text((62, 38), "valid", style=Styles.Dark.patch(text_size=9))

line((57, 22), (71, 15), arrow_head="->", style=Styles.DangerBold)
text((62, 13), "invalid", style=Styles.DangerBold.patch(text_size=9))

line((93, 37), (110, 37), arrow_head="->", style=Styles.DarkBold)

save()
```

### 8.3. Enterprise Data Lakehouse Architecture (Medallion Pattern)

Multi-element architectures frequently utilize the **Medallion Pattern** (Raw Ingestion -> Bronze -> Silver -> Gold -> Analytics). Using calm neutral cards with a single hero Gold analytical mart keeps the pipeline clean and legible:

```drawlib code=show
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=150, height=85)

# Architecture Title & Subtitle
text((75, 78), "Enterprise Medallion Data Lakehouse Architecture", style=Styles.DarkBold.patch(text_size=16))
text((75, 71), "Multi-Tier Ingestion, Delta Lake Curation, & BI Analytics", style=Styles.Muted.patch(text_size=11))

# Tier 1: Ingestion Sources (Neutral Outline)
rectangle((20, 38), width=24, height=44, style=Styles.MutedDashed.patch(shape_r=2))
phosphor.broadcast((20, 52), width=7, style=Styles.Dark)
text((20, 44), "IoT / CDC", style=Styles.DarkBold.patch(text_size=9))
phosphor.file_csv((20, 32), width=7, style=Styles.Dark)
text((20, 24), "Batch Files", style=Styles.DarkBold.patch(text_size=9))

# Tier 2: Bronze Layer (Warm Neutral Card)
rectangle((53, 38), width=24, height=44, style=Styles.AmberNeutral.patch(shape_r=2))
phosphor.database((53, 51), width=8, style=Styles.Dark)
text((53, 41), "Bronze Tier", style=Styles.DarkBold.patch(text_size=10))
text((53, 34), "Raw Append", style=Styles.Muted.patch(text_size=8))
text((53, 27), "Parquet / JSON", style=Styles.Muted.patch(text_size=8))

# Tier 3: Silver Layer (Cool Neutral Card)
rectangle((86, 38), width=24, height=44, style=Styles.Neutral.patch(shape_r=2))
phosphor.check_circle((86, 51), width=8, style=Styles.Dark)
text((86, 41), "Silver Tier", style=Styles.DarkBold.patch(text_size=10))
text((86, 34), "Cleaned / Joined", style=Styles.Muted.patch(text_size=8))
text((86, 27), "Delta Tables", style=Styles.Muted.patch(text_size=8))

# Tier 4: Gold Layer (Hero PrimaryFlat Focal Mart)
rectangle((120, 50), width=26, height=20, style=Styles.PrimaryFlat.patch(shape_r=2))
phosphor.chart_bar((120, 55), width=6, style=Styles.WhiteBold)
text((120, 47), "Gold Marts", style=Styles.WhiteBold.patch(text_size=10))
text((120, 42), "Star Schemas", style=Styles.White.patch(text_size=8))

# Tier 5: Consumers (SecondaryNeutral Card)
rectangle((120, 26), width=26, height=20, style=Styles.SecondaryNeutral.patch(shape_r=2))
phosphor.cpu((120, 31), width=6, style=Styles.Dark)
text((120, 23), "ML Models", style=Styles.DarkBold.patch(text_size=10))
text((120, 18), "Serving API", style=Styles.Muted.patch(text_size=8))

# Connectors with Flow Arrows
line((32, 38), (41, 38), arrow_head="->", style=Styles.DarkBold)
line((65, 38), (74, 38), arrow_head="->", style=Styles.DarkBold)
line((98, 44), (107, 50), arrow_head="->", style=Styles.DarkBold)
line((98, 32), (107, 26), arrow_head="->", style=Styles.DarkBold)

save()
```

---

## 9. Dynamic Retrieval and Dictionary Access

When programmatic or conditional styling is required (e.g., dynamically altering a shape's color based on telemetry data or configuration parameters), `Styles` supports dictionary item indexing and lookup methods:

```python
from drawlib.styles import Styles
from drawlib.types import Style

# 1. Dynamic retrieval via string key (PascalCase)
s_alert = Styles["RedSolidBold"]
assert s_alert.line_width == 2.5
assert s_alert.shape_fill_color == (0, 0, 0, 0.0)  # Transparent fill


# 2. Dynamic styling based on runtime condition
def get_node_style(health_status: str) -> Style:
    status_map = {
        "HEALTHY": Styles.GreenSolid,
        "DEGRADED": Styles.OrangeSolidBold,
        "UNHEALTHY": Styles.RedFlat,
    }
    return status_map.get(health_status, Styles.GrayDashed)
```

---

## 10. Common Pitfalls, Anti-Patterns, and Debugging

### Pitfall 1: Expecting String Color Names Inside `Style(...)`

`Style()` requires actual RGB/RGBA numeric tuples or `Color` instances for colors. Passing strings like `Style(shape_fill_color="red")` will raise a validation error.

```python
# INCORRECT (Raises ValidationError)
# s = Style(shape_fill_color="red")

# CORRECT: Pass color constant
from drawlib.preset_colors import DefaultColors

s = Style(shape_fill_color=DefaultColors.Red)

# CORRECT: Or access preset style directly
from drawlib.styles import Styles

s = Styles.RedFlat
```

### Pitfall 2: Attempting Direct Mutation on Frozen Catalogs

Official preset style classes and active singletons (`Styles`, `DefaultStyles`, `GoogleStyles`, `MonochromeStyles`) are immutable and frozen. Attempting to assign new attributes directly will raise an error:

```python
from drawlib.styles import Styles

# INVALID: Raises error because preset styles are frozen
# Styles.Primary = ...

# SAFE: Derive modified catalog or styles via patch() or copy()
custom_styles = Styles.patch(Primary=Styles.PrimaryBold)
custom_style = Styles.Primary.patch(line_width=10.0)
```

### Pitfall 3: Applying `Flat` to Line Elements

The `Flat` modifier explicitly strips border lines by configuring `line_width=0`. Because `line()` objects possess no interior fill, applying a `Flat` style renders the line completely invisible.

- For lines, always use `""`, `Solid`, `Dashed`, or `Dotted` along with `Thin` or `Bold` (e.g. `Styles.Blue`, `Styles.GreenDashed`, `Styles.RedBold`).

### Pitfall 4: Misinterpreting `Flat` vs `Solid` (`Outline`)

A common source of confusion for newcomers is the distinction between `Flat` and `Solid` (`Outline`):

- **`Flat`**: Solid fill color, **zero border outline**. Think of a borderless flat UI badge or solid card.
- **`Solid` / `Outline`**: **Solid continuous line border**, with a **transparent interior fill**. Think of a hollow wireframe container.

---

## 11. Quick Reference & Cheat Sheet

### 11.1. Color Shortcut Reference

```text
Default Colors:
  Red           RGB(255, 23, 23)     Green         RGB(15, 127, 15)
  Blue          RGB(31, 31, 255)     Black         RGB(0, 0, 0)
  White         RGB(255, 255, 255)

Popular Default Colors:
  Teal          RGB(15, 127, 127)    Orange        RGB(255, 120, 0)
  Navy          RGB(15, 25, 110)     Purple        RGB(130, 20, 160)
  Gray          RGB(140, 152, 170)   Amber         RGB(215, 134, 20)
  Aqua          RGB(47, 239, 239)    Olive         RGB(127, 127, 31)
  Brown         RGB(145, 45, 25)     Pink          RGB(255, 50, 150)
  Steel         RGB(96, 96, 143)     Yellow        RGB(255, 230, 0)
```

### 11.2. Structure & Weight Matrix (17 Orthogonal Variants)

| PascalCase Suffix | Fill Behavior | Outline Behavior | Border Line Style | Border Width | Font Weight |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `""` / `Bordered` | Color Fill | Black/Color Border | Solid | 1.5 px | Regular |
| `Thin` | Color Fill | Black/Color Border | Solid | 0.75 px | Thin |
| `Bold` | Color Fill | Black/Color Border | Solid | 2.5 px | Bold |
| `Flat` | Color Fill | No Border | None | 0.0 px | Regular |
| `Outline` / `Solid` | Transparent | Color Border | Solid | 1.5 px | Regular |
| `OutlineThin` / `SolidThin` | Transparent | Color Border | Solid | 0.75 px | Thin |
| `OutlineBold` / `SolidBold` | Transparent | Color Border | Solid | 2.5 px | Bold |
| `Dashed` | Transparent | Color Border | Dashed | 1.5 px | Regular |
| `DashedThin` | Transparent | Color Border | Dashed | 0.75 px | Thin |
| `DashedBold` | Transparent | Color Border | Dashed | 2.5 px | Bold |
| `Dotted` | Transparent | Color Border | Dotted | 1.5 px | Regular |
| `DottedThin` | Transparent | Color Border | Dotted | 0.75 px | Thin |
| `DottedBold` | Transparent | Color Border | Dotted | 2.5 px | Bold |

### 11.3. Essential Code Snippets

```drawlib code=show
# Standard imports
from drawlib.canvas import save, setup
from drawlib.preset_styles import DefaultStyles, MonochromeStyles
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles

# Initialize canvas with default or custom catalog
setup(width=100, height=60)

# 1. Preset style usage (1 Hero Flat + Neutral + Dashed)
rectangle((24, 38), width=22, height=20, style=Styles.PrimaryFlat, text="Flat", text_style=Styles.WhiteBold)
rectangle((50, 38), width=22, height=20, style=Styles.Neutral, text="Neutral")
circle((76, 38), radius=10, style=Styles.MutedDashedBold, text="Dashed", text_style=Styles.DarkBold)

# 2. Dynamic style retrieval via key lookup
accent_style = DefaultStyles["SecondaryNeutral"]
circle((88, 50), radius=5, style=accent_style)

# 3. Dedicated monochrome catalog retrieval
rectangle(
    (50, 12),
    width=82,
    height=12,
    style=MonochromeStyles.PrimaryFlat,
    text="Monochrome Catalog Banner",
    text_style=MonochromeStyles.WhiteBold,
)

save()
```

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
