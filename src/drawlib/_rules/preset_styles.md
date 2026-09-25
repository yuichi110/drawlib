# Drawlib Preset Styles Guidelines

Drawlib provides a comprehensive, centralized preset style system in `drawlib.preset_styles` designed to enforce visual consistency, eliminate boilerplate styling code, and enable rapid diagram prototyping. Under the "Illustration as Code" philosophy, styling is treated as a systematic design system where shapes, lines, icons, text, and images adhere to cohesive color palettes, line widths, and typographical hierarchies.

---

## 1. Architectural Philosophy & Core Concepts

In complex technical diagrams and architectural illustrations, manually specifying colors, line widths, borders, and fonts for every individual element leads to verbose, brittle, and visually inconsistent code. Drawlib addresses this through three core design principles:

1. **Convention over Configuration**:
   When drawing any shape, line, text, or icon without an explicit style, Drawlib automatically applies the active preset's default style. A circle, a line, and a label created with zero styling arguments naturally harmonize.

2. **Systematic String Shortcuts**:
   Instead of instantiating verbose `Style(...)` objects for standard variations, Drawlib parses ergonomic shorthand strings such as `"blue"`, `"green_flat"`, `"red_solid_bold"`, or `"dashed"`. These strings are resolved dynamically into full `Style` instances.

3. **Layered Object Models**:
   At the core of the preset style system is `BasePresetStyles` (a Pydantic `BaseModel`), which exposes standard role-based styles (`primary`, `light`, `bold`, `flat`, `solid`, `dashed`), default canvas background colors, and font definitions. Users can inspect, iterate, serialize, or subclass these models to define enterprise brand guidelines.

### 1.1. High-Level Architecture Overview

```text
┌───────────────────────────────────────────────────────────────────────────────────┐
│                               Public Facade API                                   │
│            from drawlib.preset_styles import get_style, get_styles, ...           │
│            from drawlib.colors import Colors, ColorsDefault, ColorsEssentials     │
└────────────────────────────────────────┬──────────────────────────────────────────┘
                                         │
                    ┌────────────────────┴────────────────────┐
                    ▼                                         ▼
   ┌─────────────────────────────────┐       ┌─────────────────────────────────┐
   │       Color Collections         │       │     Official Style Catalogs     │
   │  - ColorsDefault (5 colors)     │       │  - DefaultStyles                │
   │  - ColorsMonochrome (7 colors)  │       │  - MonochromeStyles             │
   │  - ColorsEssentials (25 colors) │       │  - EssentialsStyles             │
   │  - Colors140 (140 CSS colors)   │       │  (Base: BasePresetStyles)       │
   │  - Colors (16 basic web colors) │       │                                 │
   └────────────────┬────────────────┘       └────────────────┬────────────────┘
                    │                                         │
                    └────────────────────┬────────────────────┘
                                         │
                                         ▼
                    ┌─────────────────────────────────────────┐
                    │      Style Resolution: get_style()      │
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
# Preset styles functions and model classes
from drawlib.preset_styles import (
    BasePresetStyles,
    DefaultStyles,
    EssentialsStyles,
    MonochromeStyles,
    PresetStyles,
    get_default_styles,
    get_essentials_styles,
    get_monochrome_styles,
    get_style,
    get_styles,
)

# Color collections and utilities
from drawlib.colors import (
    Colors,
    Colors140,
    ColorsDefault,
    ColorsEssentials,
    ColorsMonochrome,
    from_grayscale,
    from_hex,
    with_alpha,
)

# Underlying Style model
from drawlib.types import Style
```

### 2.1. Re-exported Symbol Summary

| Symbol | Category | Description |
| :--- | :--- | :--- |
| `get_style(style=None)` | Resolver Function | Resolves a style string shortcut, `Style` object, or `None` into an active `Style`. |
| `get_styles(name="default")` | Catalog Factory | Returns the `BasePresetStyles` catalog for `"default"`, `"essentials"`, or `"monochrome"`. |
| `get_default_styles()` | Catalog Factory | Directly constructs and returns a `DefaultStyles` instance. |
| `get_essentials_styles()` | Catalog Factory | Directly constructs and returns an `EssentialsStyles` instance. |
| `get_monochrome_styles()` | Catalog Factory | Directly constructs and returns a `MonochromeStyles` instance. |
| `BasePresetStyles` | Base Model | Pydantic base model providing dict-like access, iteration, and field validation. |
| `PresetStyles` | Alias | Backward-compatible alias for `BasePresetStyles`. |
| `DefaultStyles` | Model Class | Strongly typed model containing default style definitions. |
| `EssentialsStyles` | Model Class | Strongly typed model containing 25-color essentials style definitions. |
| `MonochromeStyles` | Model Class | Strongly typed model containing grayscale style definitions. |

---

## 3. Official Palette Catalogs

Drawlib ships with three pre-built, production-ready style catalogs. Each catalog defines standard style roles (`primary`, `light`, `bold`, `flat`, `solid`, `dashed`), default canvas background colors, and typographical defaults.

```text
┌───────────────────────────────────────────────────────────────────────────────────────┐
│                               BasePresetStyles Model                                  │
├───────────────────────────────────────────────────────────────────────────────────────┤
│ + background_color: TypeColor = (255, 255, 255, 1.0)                                  │
│ + sourcecode_font: FontSourceCode = FontSourceCode.SOURCECODEPRO                      │
├───────────────────────────────────────────────────────────────────────────────────────┤
│ + primary: Style   --> Core default fill, outline, and text style                     │
│ + light: Style     --> Half-width line borders, lighter font weight                   │
│ + bold: Style      --> 1.5x to 2x line borders, bold font weight                      │
│ + flat: Style      --> Borderless solid color fill (line_width=0)                     │
│ + solid: Style     --> Transparent fill with solid colored border outline             │
│ + dashed: Style    --> Transparent fill with dashed colored border outline            │
└───────────────────────────────────────────────────────────────────────────────────────┘
```

### 3.1. DefaultStyles (`"default"`)

The standard catalog optimized for technical documentation, flowcharts, and software architecture diagrams. It uses a calming, clean light blue (`ColorsDefault.Blue`) as the primary fill and black (`ColorsDefault.Black`) for crisp border definition.

- **Primary Colors**: Blue (`#6F6FEF`), Black (`#000000`), White (`#FFFFFF`), Green (`#4FBF4F`), Red (`#EF5F5F`).
- **Visual Design**:
  - `primary`: Blue fill, black border (width 1.5), sans-serif regular font.
  - `light`: Blue fill, black border (width 0.75), sans-serif light font, thin icons.
  - `bold`: Blue fill, black border (width 2.25), sans-serif bold font, regular icons.
  - `flat`: Blue fill, blue border with `line_width=0` (borderless), fill-style icons.
  - `solid`: Transparent fill, blue border (width 1.5), regular icons.
  - `dashed`: Transparent fill, blue dashed border (width 1.5), regular icons.

```python
from drawlib.preset_styles import get_default_styles

default_catalog = get_default_styles()

print("Default Primary Fill:", default_catalog.primary.fill_color)
print("Default Primary Line:", default_catalog.primary.line_color)
print("Default Line Width:", default_catalog.primary.line_width)
```

### 3.2. MonochromeStyles (`"monochrome"`)

Specially designed for printed engineering manuals, formal academic papers, patents, and grayscale e-ink displays. It uses pure black, white, and balanced intermediate gray tones to maintain razor-sharp contrast without color dependencies.

- **Primary Colors**: Black (`#000000`), Charcoal (`#272727`), Graphite (`#3F3F3F`), Gray (`#7F7F7F`), Silver (`#BFBFBF`), Snow (`#EFEFEF`), White (`#FFFFFF`).
- **Visual Design**:
  - `primary`: White fill, black border (width 1.5), black text, sans-serif regular font.
  - `light`: White fill, black border (width 0.75), sans-serif light font.
  - `bold`: White fill, black border (width 2.25), sans-serif bold font.
  - `flat`: Solid black fill, black border with `line_width=0`.
  - `solid`: Transparent fill, black border (width 1.5).
  - `dashed`: Transparent fill, black dashed border (width 1.5).

```drawlib show-code
from drawlib.canvas import config, save
from drawlib.preset_styles import get_monochrome_styles
from drawlib.shapes import rectangle
from drawlib.text import text

config(width=120, height=40)
mono = get_monochrome_styles()

# White box with black outline
rectangle((30, 20), width=35, height=20, style=mono.primary)
text((30, 20), "Primary (Outline)", style=mono.primary)

# Solid black box with white text
rectangle((80, 20), width=35, height=20, style=mono.flat)
text((80, 20), "Flat (Filled)", style=mono.white_bold)

save()
```

### 3.3. EssentialsStyles (`"essentials"`)

An expressive, modern palette featuring 25 rich, coordinated colors. It is the recommended base for complex multi-tier system designs, data visualization dashboards, and cloud infrastructure diagrams where distinct subsystems require dedicated semantic colors.

- **Primary Colors**: Red, LightRed, Pink, Brown, Orange, Green, LightGreen, GreenYellow, Teal, Olive, Blue, LightBlue, Aqua, Navy, Steel, Yellow, Purple, Ivory, Black, Charcoal, Graphite, Gray, Silver, Snow, White.
- **Visual Design**:
  - `primary`: LightBlue fill, Charcoal border (width 1.5), Charcoal text.
  - `light`: LightBlue fill, Charcoal border (width 0.75), sans-serif light font.
  - `bold`: LightBlue fill, Charcoal border (width 2.25), sans-serif bold font.
  - `flat`: LightBlue fill, borderless (`line_width=0`).
  - `solid`: Transparent fill, LightBlue border (width 1.5).
  - `dashed`: Transparent fill, LightBlue dashed border (width 1.5).

```python
from drawlib.preset_styles import get_styles

# Retrieve catalog dynamically
essentials = get_styles("essentials")

print("Essentials Primary Text Color:", essentials.primary.text_color)
print("Essentials Background:", essentials.background_color)
```

---

## 4. Color Collections & Color Management

Drawlib enforces strict RGB or RGBA tuples internally for maximum precision and rendering consistency. To avoid hardcoding raw numeric tuples across codebases, Drawlib provides structured static color classes.

### 4.1. Color Classes Overview

| Class | Number of Colors | Base Class | Primary Purpose |
| :--- | :--- | :--- | :--- |
| `ColorsDefault` | 5 | `ColorsBase` | Core 5 colors matching the `"default"` preset catalog. |
| `ColorsMonochrome` | 7 | `ColorsBase` | Pure grayscale gradient from Black to White. |
| `ColorsEssentials` | 25 | `ColorsBase` | Comprehensive 25-color palette for rich diagrams. |
| `Colors140` | 140 | `ColorsBase` | Complete W3C CSS Color Module Level 3 named colors. |
| `Colors` | 16 | `ColorsBase` | Classic 16 standard HTML/VGA web colors + Transparent. |

### 4.2. Exact RGB Values of Built-In Palettes

#### ColorsDefault
- `Red`: `(239, 95, 95)`
- `Green`: `(79, 191, 79)`
- `Blue`: `(111, 111, 239)`
- `Black`: `(0, 0, 0)`
- `White`: `(255, 255, 255)`

#### ColorsMonochrome
- `Black`: `(0, 0, 0)`
- `Charcoal`: `(39, 39, 39)`
- `Graphite`: `(63, 63, 63)`
- `Gray`: `(127, 127, 127)`
- `Silver`: `(191, 191, 191)`
- `Snow`: `(239, 239, 239)`
- `White`: `(255, 255, 255)`

#### ColorsEssentials
| Color Name | RGB Value | Hex Equivalent | Visual Role |
| :--- | :--- | :--- | :--- |
| `Red` | `(255, 23, 23)` | `#FF1717` | Critical alerts, destructive actions |
| `LightRed` | `(239, 95, 95)` | `#EF5F5F` | Soft errors, warnings |
| `Pink` | `(239, 63, 239)` | `#EF3FEF` | Special events, highlights |
| `Brown` | `(159, 31, 31)` | `#9F1F1F` | Legacy components, storage blocks |
| `Orange` | `(255, 95, 31)` | `#FF5F1F` | Compute nodes, warning thresholds |
| `Green` | `(15, 127, 15)` | `#0F7F0F` | Production status, valid states |
| `LightGreen` | `(79, 191, 79)` | `#4FBF4F` | Healthy services, operational nodes |
| `GreenYellow` | `(127, 207, 31)`| `#7FCF1F` | Minor notices, caches |
| `Teal` | `(15, 127, 127)` | `#0F7F7F` | Networking, API gateways |
| `Olive` | `(127, 127, 31)` | `#7F7F1F` | Secondary systems, batch jobs |
| `Blue` | `(31, 31, 255)`  | `#1F1FFF` | High-priority primary services |
| `LightBlue` | `(111, 111, 239)`| `#6F6FEF` | Standard application services |
| `Aqua` | `(47, 239, 239)` | `#2FEFEF` | Ingress streams, client connections |
| `Navy` | `(15, 15, 127)`  | `#0F0F7F` | Databases, persistent storage |
| `Steel` | `(96, 96, 143)`  | `#60608F` | Infrastructure hosts, containers |
| `Yellow` | `(239, 239, 31)` | `#EFEF1F` | Authentication, token services |
| `Purple` | `(127, 31, 127)` | `#7F1F7F` | Message queues, asynchronous pub/sub |
| `Ivory` | `(239, 239, 207)`| `#EFEFCF` | Canvas background, callout panels |
| `Black` | `(0, 0, 0)`      | `#000000` | Borders, primary dark text |
| `Charcoal` | `(39, 39, 39)`   | `#272727` | High-contrast structural borders |
| `Graphite` | `(63, 63, 63)`   | `#3F3F3F` | Secondary structural borders |
| `Gray` | `(127, 127, 127)`| `#7F7F7F` | Inactive nodes, boundary lines |
| `Silver` | `(191, 191, 191)`| `#BFBFBF` | Subnet backdrops, divider lines |
| `Snow` | `(239, 239, 239)`| `#EFEFEF` | Neutral container card backdrops |
| `White` | `(255, 255, 255)`| `#FFFFFF` | Canvas default, card surfaces |

### 4.3. Color Utilities: Hex, Grayscale, Alpha

Drawlib provides helper functions in `drawlib.colors` to convert standard color formats into valid Drawlib RGB/RGBA tuples:

```python
from drawlib.colors import from_grayscale, from_hex, with_alpha

# 1. Parse standard 6-digit hex code
brand_blue = from_hex("#1a73e8")  # returns (26, 115, 232)

# 2. Parse 8-digit hex code with alpha channel
semi_transparent = from_hex("#1a73e880")  # returns (26, 115, 232, 0.5)

# 3. Create calibrated grayscale values
mid_gray = from_grayscale(128)  # returns (128, 128, 128)
light_shade = from_grayscale(240, alpha=0.8)  # returns (240, 240, 240, 0.8)

# 4. Dynamically adjust transparency on existing color constants
from drawlib.colors import ColorsEssentials

backdrop_color = with_alpha(ColorsEssentials.Navy, 0.15)
# returns (15, 15, 127, 0.15)
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
                        └─► "blue" | "red" | "green" | "teal" | "charcoal" | ...
```

### 5.1. Grammar Token Breakdown

1. **`<color>` (Color Token)**:
   - Any color name available in `ColorsEssentials`, `Colors140`, or `Colors`.
   - Matching is case-insensitive (e.g. `"blue"`, `"Blue"`, `"deepskyblue"`, `"darkorange"`).
   - If omitted, the default primary accent color (`ColorsDefault.Blue`) is used.

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
| `"charcoal_flat"` | Charcoal | None | None | 0.0 | Regular |

### 5.3. Code Demonstration of Shorthand Variations

```drawlib show-code
from drawlib.canvas import config, save
from drawlib.lines import line
from drawlib.preset_styles import get_styles
from drawlib.shapes import rectangle
from drawlib.text import text

config(width=140, height=70)
styles = get_styles("essentials")

# Column positions
x_coords = [20, 50, 80, 110]
y_top = 45
y_bot = 15

# Row 1: Flat fills (no border) vs Solid outlines (no fill)
rectangle((x_coords[0], y_top), width=24, height=18, style=styles.blue_flat)
text((x_coords[0], y_top), "blue_flat", style=styles.white_bold)

rectangle((x_coords[1], y_top), width=24, height=18, style=styles.green_flat)
text((x_coords[1], y_top), "green_flat", style=styles.white_bold)

rectangle((x_coords[2], y_top), width=24, height=18, style=styles.red_solid)
text((x_coords[2], y_top), "red_solid", style=styles.red)

rectangle((x_coords[3], y_top), width=24, height=18, style=styles.purple_dashed)
text((x_coords[3], y_top), "purple_dashed", style=styles.purple)

# Row 2: Weight variations (light, standard, bold)
rectangle((x_coords[0], y_bot), width=24, height=18, style=styles.orange_solid)
text((x_coords[0], y_bot), "solid", style=styles.orange)

rectangle((x_coords[1], y_bot), width=24, height=18, style=styles.orange_bold)
text((x_coords[1], y_bot), "bold", style=styles.orange_bold)

rectangle((x_coords[2], y_bot), width=24, height=18, style=styles.orange_flat)
text((x_coords[2], y_bot), "flat", style=styles.white_bold)

# Connecting line showcasing weight
line((x_coords[0] - 12, 32), (x_coords[3] + 12, 32), style=styles.charcoal_dashed)

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

In enterprise projects and client presentations, you often need custom color palettes and typography rules that match specific brand guidelines. Drawlib allows you to define custom style catalogs by subclassing `BasePresetStyles`.

### 7.1. Direct Instantiation of PresetStyles

You can construct a one-off `PresetStyles` instance directly with custom `Style` objects:

```drawlib show-code
from drawlib.canvas import config, save
from drawlib.colors import Colors140, from_hex
from drawlib.preset_styles import PresetStyles
from drawlib.shapes import circle, rectangle
from drawlib.types import Style

# Brand corporate identity colors
CORP_NAVY = from_hex("#0D1B2A")
CORP_CYAN = from_hex("#00A896")
CORP_GOLD = from_hex("#F4A261")

brand_preset = PresetStyles(
    background_color=(250, 250, 252, 1.0),
    primary=Style(shape_fill_color=CORP_CYAN, shape_line_color=CORP_NAVY, shape_line_width=2.0),
    light=Style(shape_fill_color=CORP_CYAN, shape_line_color=CORP_NAVY, shape_line_width=1.0),
    bold=Style(shape_fill_color=CORP_GOLD, shape_line_color=CORP_NAVY, shape_line_width=3.0),
    flat=Style(shape_fill_color=CORP_CYAN, shape_line_width=0.0),
    solid=Style(shape_fill_color=(0, 0, 0, 0.0), shape_line_color=CORP_NAVY, shape_line_width=2.0),
    dashed=Style(shape_fill_color=(0, 0, 0, 0.0), shape_line_color=CORP_NAVY, shape_line_width=2.0, shape_line_style="dashed"),
)

config(width=100, height=40, background_color=brand_preset.background_color)

rectangle((30, 20), width=30, height=20, style=brand_preset.primary)
circle((80, 20), radius=10, style=brand_preset.bold)

save()
```

### 7.2. Domain-Driven Subclassing with Type Hints

Because `BasePresetStyles` inherits from Pydantic's `BaseModel`, creating a dedicated subclass provides IDE autocompletion, type safety, field validation, and dictionary iteration:

```python
from drawlib.colors import Colors, from_hex
from drawlib.preset_styles import BasePresetStyles
from drawlib.types import Style


class CloudPlatformStyles(BasePresetStyles):
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
    c_blue = from_hex("#1a73e8")
    c_green = from_hex("#34a853")
    c_red = from_hex("#ea4335")
    c_gray = from_hex("#5f6368")

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

`BasePresetStyles` provides robust Pythonic access patterns:

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
from drawlib.canvas import config, save
from drawlib.colors import Colors, ColorsEssentials
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.text import text

config(width=140, height=90)
styles = get_styles("essentials")

# Section Headers
text((70, 84), "Enterprise E-Commerce Microservices", style=styles.bold, size=18)
text((70, 78), "Synchronous REST Ingress & Asynchronous Event Bus", style=styles.charcoal, size=12)

# Subnet / Boundary Containers
rectangle((70, 42), width=132, height=60, r=4, style=styles.silver_dashed)
text((22, 68), "Internal VPC (10.0.0.0/16)", style=styles.gray_bold, size=11)

# Tier 1: External Client & API Gateway
rectangle((22, 42), width=22, height=30, r=2, style=styles.blue_solid)
phosphor.user((22, 50), width=9, style=styles.blue)
text((22, 40), "Client Apps", style=styles.blue_bold, size=11)
text((22, 33), "Web / Mobile", style=styles.charcoal, size=9)

rectangle((50, 42), width=22, height=30, r=2, style=styles.teal_flat)
phosphor.cloud((50, 50), width=9, style=styles.white_bold)
text((50, 40), "API Gateway", style=styles.white_bold, size=11)
text((50, 33), "Rate Limiting", style=styles.white, size=9)

# Tier 2: Backend Core Services
rectangle((80, 53), width=24, height=18, r=2, style=styles.green_bold)
text((80, 56), "Order Service", style=styles.green_bold, size=11)
text((80, 48), "gRPC :8081", style=styles.charcoal, size=9)

rectangle((80, 27), width=24, height=18, r=2, style=styles.green_bold)
text((80, 30), "Payment Service", style=styles.green_bold, size=11)
text((80, 22), "gRPC :8082", style=styles.charcoal, size=9)

# Tier 3: Asynchronous Pub/Sub Queue & Storage
rectangle((114, 53), width=22, height=18, r=2, style=styles.purple_flat)
phosphor.broadcast((114, 56), width=7, style=styles.white_bold)
text((114, 48), "Kafka Broker", style=styles.white_bold, size=10)

rectangle((114, 27), width=22, height=18, r=2, style=styles.navy_solid)
phosphor.database((114, 31), width=7, style=styles.navy)
text((114, 22), "PostgreSQL HA", style=styles.navy_bold, size=10)

# Connectors with semantic weights
line((33, 42), (39, 42), arrowhead="->", style=styles.blue_bold)
line((61, 46), (68, 53), arrowhead="->", style=styles.charcoal)
line((61, 38), (68, 27), arrowhead="->", style=styles.charcoal)
line((92, 53), (103, 53), arrowhead="->", style=styles.purple_dashed)
line((92, 27), (103, 27), arrowhead="<->", style=styles.navy_bold)

save()
```

### 8.2. State Machine Diagram

Preset styles make state transitions intuitive by mapping distinct semantic meanings to colors:
- Blue = Initial / Start State
- Green = Active / Normal Execution
- Orange = Paused / Pending Review
- Red = Failed / Terminated Error State

```drawlib show-code
from drawlib.canvas import config, save
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.text import text

config(width=130, height=50)
styles = get_styles("essentials")

# Start State
circle((15, 25), radius=5, style=styles.blue_flat)
text((15, 14), "Initial", style=styles.blue_bold, size=10)

# Processing State
rectangle((45, 25), width=22, height=16, r=3, style=styles.green_bold)
text((45, 27), "Validating", style=styles.green_bold, size=11)
text((45, 20), "Worker Poll", style=styles.charcoal, size=9)

# Decision Branches: Success vs Failure
rectangle((80, 36), width=22, height=14, r=3, style=styles.green_flat)
text((80, 36), "Processed", style=styles.white_bold, size=10)

rectangle((80, 14), width=22, height=14, r=3, style=styles.red_flat)
text((80, 14), "Rejected", style=styles.white_bold, size=10)

# Final State
circle((115, 36), radius=5, style=styles.green_bold)
circle((115, 36), radius=3.2, style=styles.green_flat)
text((115, 24), "Completed", style=styles.green_bold, size=10)

# Transitions
line((20, 25), (34, 25), arrowhead="->", style=styles.charcoal_bold)
text((27, 28), "submit", style=styles.charcoal, size=9)

line((56, 29), (69, 36), arrowhead="->", style=styles.green_bold)
text((60, 37), "valid", style=styles.green, size=9)

line((56, 21), (69, 14), arrowhead="->", style=styles.red_bold)
text((60, 13), "invalid", style=styles.red, size=9)

line((91, 36), (110, 36), arrowhead="->", style=styles.green_bold)

save()
```

### 8.3. Enterprise Data Lakehouse Architecture (Medallion Pattern)

Multi-element architectures frequently utilize the **Medallion Pattern** (Raw Ingestion -> Bronze -> Silver -> Gold -> Analytics). Preset styles make distinct processing tiers instantly recognizable:

- **Brown / Orange (`brown_flat`, `orange_solid`)**: Raw Ingestion & Bronze Landing (unfiltered CDC & Kafka logs).
- **Silver / Gray (`silver_flat`, `steel_solid_bold`)**: Cleansed, deduplicated, and enriched Delta tables.
- **Gold / Yellow (`yellow_flat`, `green_solid_bold`)**: Business-level aggregates, feature stores, and BI marts.
- **Teal / Navy (`teal_solid`, `navy_bold`)**: Query engines, dashboards, and automated ML pipelines.

```drawlib show-code
from drawlib.canvas import config, save
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.text import text

config(width=150, height=85)
styles = get_styles("essentials")

# Architecture Title & Subtitle
text((75, 78), "Enterprise Medallion Data Lakehouse Architecture", style=styles.bold, size=18)
text((75, 72), "Multi-Tier Ingestion, Delta Lake Curation, & BI Analytics", style=styles.charcoal, size=11)

# Tier 1: Ingestion Sources
rectangle((20, 40), width=22, height=44, r=2, style=styles.orange_solid)
phosphor.broadcast((20, 54), width=7, style=styles.orange)
text((20, 46), "IoT / CDC", style=styles.orange_bold, size=10)
phosphor.file_csv((20, 34), width=7, style=styles.orange)
text((20, 26), "Batch Files", style=styles.orange_bold, size=10)

# Tier 2: Bronze Layer (Raw Storage)
rectangle((52, 40), width=24, height=44, r=2, style=styles.brown_flat)
phosphor.database((52, 53), width=8, style=styles.white_bold)
text((52, 43), "Bronze Tier", style=styles.white_bold, size=11)
text((52, 36), "Raw Append", style=styles.white, size=9)
text((52, 28), "Parquet / JSON", style=styles.white, size=8)

# Tier 3: Silver Layer (Cleaned & Enriched)
rectangle((86, 40), width=24, height=44, r=2, style=styles.steel_bold)
phosphor.check_circle((86, 53), width=8, style=styles.steel)
text((86, 43), "Silver Tier", style=styles.steel_bold, size=11)
text((86, 36), "Cleaned / Joined", style=styles.charcoal, size=9)
text((86, 28), "Delta Tables", style=styles.charcoal, size=8)

# Tier 4: Gold Layer (Business Aggregates)
rectangle((120, 52), width=24, height=22, r=2, style=styles.green_flat)
phosphor.chart_bar((120, 58), width=7, style=styles.white_bold)
text((120, 49), "Gold Marts", style=styles.white_bold, size=10)
text((120, 44), "Star Schemas", style=styles.white, size=8)

# Tier 5: Consumers (ML & BI)
rectangle((120, 25), width=24, height=22, r=2, style=styles.teal_bold)
phosphor.cpu((120, 31), width=7, style=styles.teal)
text((120, 22), "ML Models", style=styles.teal_bold, size=10)
text((120, 17), "Serving API", style=styles.charcoal, size=8)

# Connectors with Flow Arrows
line((31, 40), (40, 40), arrowhead="->", style=styles.orange_bold)
line((64, 40), (74, 40), arrowhead="->", style=styles.charcoal_bold)
line((98, 45), (108, 52), arrowhead="->", style=styles.green_bold)
line((98, 35), (108, 25), arrowhead="->", style=styles.teal_bold)

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
3. Resolve `<color_name>` against `ColorsEssentials`, `Colors140`, and `Colors`.
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
from drawlib.colors import ColorsDefault

s = Style(fill_color=ColorsDefault.Red)

# CORRECT: Or resolve via get_style
s = get_style("red_flat")
```

### Pitfall 2: Mutating Shared Style References Without Copying

If you retrieve a style from a catalog and modify its attributes directly without copying, you may unintentionally mutate subsequent drawing operations that rely on that catalog:

```python
from drawlib.preset_styles import get_default_styles

catalog = get_default_styles()

# RISKY: Modifying catalog directly
# catalog.primary.line_width = 10.0

# SAFE: Always clone with copy() or get_style()
custom_style = catalog.primary.copy()
custom_style.line_width = 10.0
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
  red           RGB(239, 95, 95)     green         RGB(79, 191, 79)
  blue          RGB(111, 111, 239)   black         RGB(0, 0, 0)
  white         RGB(255, 255, 255)

Popular Essentials Colors:
  teal          RGB(15, 127, 127)    orange        RGB(255, 95, 31)
  navy          RGB(15, 15, 127)     purple        RGB(127, 31, 127)
  charcoal      RGB(39, 39, 39)      graphite      RGB(63, 63, 63)
  silver        RGB(191, 191, 191)   snow          RGB(239, 239, 239)
  aqua          RGB(47, 239, 239)    olive         RGB(127, 127, 31)
  brown         RGB(159, 31, 31)     pink          RGB(239, 63, 239)
  steel         RGB(96, 96, 143)     yellow        RGB(239, 239, 31)
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
from drawlib.canvas import config, save
from drawlib.colors import Colors, ColorsEssentials, from_hex, with_alpha
from drawlib.preset_styles import BasePresetStyles, get_styles
from drawlib.shapes import circle, rectangle
from drawlib.text import text

styles = get_styles("essentials")

# Initialize canvas with default or custom catalog
config(width=100, height=60)

# 1. Preset style usage
rectangle((25, 36), width=20, height=20, style=styles.blue_flat, text="Flat", textstyle=styles.white_bold)
rectangle((50, 36), width=20, height=20, style=styles.green_bold, text="Solid", textstyle=styles.green_bold)
circle((75, 36), radius=10, style=styles.red_dashed, text="Dashed", textstyle=styles.red_bold)

# 2. Dynamic style retrieval via key lookup
accent_style = styles["teal_flat"]
circle((85, 48), radius=5, style=accent_style)

# 3. Dedicated monochrome catalog retrieval
monochrome = get_styles("monochrome")
rectangle((50, 12), width=80, height=12, style=monochrome.flat, text="Monochrome Catalog Banner", textstyle=monochrome.white_bold)

save()
```

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
