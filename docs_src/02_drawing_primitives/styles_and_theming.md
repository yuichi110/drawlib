# Styles & Theming

In complex technical diagrams, manually configuring RGB color codes, line widths, and font sizes for every single element leads to inconsistent branding and brittle drawing code. 
Drawlib resolves this with a **systematic design token system** in `drawlib.styles` and `drawlib.preset_styles`.

---

## 1. Overview of Semantic Styles

```drawlib 650px center file:semantic_color_roles.png caption:"Drawlib Semantic Color Roles and Variants"
from drawlib.canvas import setup
from drawlib.shapes import rectangle
from drawlib.styles import Styles

setup(width=140, height=52)

# Row 1: Core Functional Roles (Hero Anchor, Calm Neutral, Auxiliary)
rectangle((25, 36), width=32, height=18, style=Styles.PrimaryFlat, text="PrimaryFlat\n(Hero Anchor)", text_style=Styles.WhiteBold)
rectangle((70, 36), width=32, height=18, style=Styles.Neutral, text="Neutral\n(50%+ Cards)")
rectangle((115, 36), width=32, height=18, style=Styles.SecondaryNeutral, text="SecondaryNeutral\n(Auxiliary)")

# Row 2: Status & Boundary Roles (Success, Danger, Muted)
rectangle((25, 14), width=32, height=18, style=Styles.SuccessFlat, text="SuccessFlat\n(Verified)", text_style=Styles.WhiteBold)
rectangle((70, 14), width=32, height=18, style=Styles.DangerFlat, text="DangerFlat\n(Error/Risk)", text_style=Styles.WhiteBold)
rectangle((115, 14), width=32, height=18, style=Styles.MutedDashed, text="MutedDashed\n(Container)", text_style=Styles.DarkBold)
```

---

## 2. Active Design Tokens (`drawlib.styles`)

The active design system is imported from `drawlib.styles`:

```python
from drawlib.styles import Colors, Styles
```

- **`Styles`**: The active catalog of pre-configured `Style` objects (defaults to `DefaultStyles`).
- **`Colors`**: The active palette of color definitions (defaults to `DefaultColors`).

---

## 3. Semantic Role & Variant Matrix

Every style token is composed of a **Semantic Role** (or color name) and an optional **Visual Variant**:

### Semantic Roles:
- **`Primary`**: Main structural components and key architectural blocks.
- **`Secondary`**: Secondary supporting services and auxiliary nodes.
- **`Accent`**: Emphasized focal points and action triggers.
- **`Neutral`**: Calm card surfaces, general services, and worker nodes.
- **`Success`**: Healthy statuses, successful states, and completed steps.
- **`Danger`**: Error conditions, security threats, and terminating gates.
- **`Warning`**: Warnings, deprecations, and pending queues.
- **`Muted`**: Background boundaries, subtle partitions, and inactive states.

### Common Variants:
| Variant Suffix | Example | Visual Appearance |
| :--- | :--- | :--- |
| `Flat` | `Styles.PrimaryFlat` | Solid fill color without border lines. |
| `Bordered` | `Styles.PrimaryBordered` | Standard fill with a contrasting border. |
| `Bold` | `Styles.PrimaryBold` | Heavy stroke for lines and borders. |
| `Thin` | `Styles.PrimaryThin` | Thin stroke with thin font weight. |
| `Outline` | `Styles.PrimaryOutline` | Transparent fill with a colored border line. |
| `Dashed` | `Styles.MutedDashed` | Dashed border stroke (ideal for VPCs and clusters). |
| `Dotted` | `Styles.PrimaryDotted` | Dotted border stroke for ephemeral or preview components. |
| `Neutral` | `Styles.BlueNeutral` | Tinted card with ultra-light fill, soft border, high-contrast text. |
| `NeutralFlat` | `Styles.BlueNeutralFlat` | Borderless tinted card with high-contrast text. |

---

## 4. Typography & Icon Styles

Preset styles are also applied to text labels and icons:

```python
# Use WhiteBold for text inside filled dark containers
rectangle((50, 25), width=30, height=20, style=Styles.PrimaryFlat, text="Server", text_style=Styles.WhiteBold)
line((20, 25), (80, 25), arrow_head="->", style=Styles.DarkBold)
```

---

## 5. Customizing & Deriving Styles (`.patch()`)

Styles in Drawlib are immutable data models. To create custom variations without rebuilding a `Style` from scratch, use the `.patch()` method to override specific attributes:

```python
from drawlib.styles import Styles
from drawlib.preset_colors import Colors

# 1. Derive a custom branded node card
custom_card = Styles.PrimaryNeutral.patch(
    shape_line_width=2.0,
    shape_line_color=Colors.Blue,
    text_size=11.0,
)

# 2. Derive a high-contrast danger badge
danger_badge = Styles.DangerFlat.patch(
    shape_line_width=1.0,
    shape_line_color=(255, 255, 255, 0.8),
    text_size=9.0,
)
```

---

## 6. Official Preset Style Catalogs & Typography Patching

Drawlib includes three official style catalogs in `drawlib.preset_styles`:
1. **`DefaultStyles`**: Clean, balanced modern tech palette (Tailwind/VitePress inspired).
2. **`GoogleStyles`**: Material Design inspired palette (Google Blue, Red, Yellow, Green).
3. **`MonochromeStyles`**: Publication-grade grayscale palette for black-and-white academic papers and official specifications.

### Universal Typography Patching (`.patch_font()`)
When publishing documents in international languages (such as Japanese, Chinese, or Korean) or applying corporate typography, use `.patch_font()` to replace font families across all predefined tokens in one call:

```python
from drawlib.fonts import FontJapanese  # or FontRoboto, FontChinese, etc.
from drawlib.preset_styles import GoogleStyles

# Patch all styles with unified typography weights
Styles = GoogleStyles().patch_font(
    regular=FontJapanese.SANSSERIF_REGULAR,
    bold=FontJapanese.SANSSERIF_BOLD,
    thin=FontJapanese.SANSSERIF_THIN,
)
```

Switch the active preset globally via CLI flag during build:

```bash
$ uv run drawlib build html docs_src/ --styles google
```
