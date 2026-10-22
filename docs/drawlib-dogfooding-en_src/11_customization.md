# Chapter 11: Style and Theme Customization

Drawlib provides complete control over document typography, color schemes, and visual styles.

## 11.1 Controlling Visual Themes via `styles.py`

In your project root or source directory, `styles.py` defines the active `Colors` and `Styles` namespaces:

```python
from drawlib.fonts import Font
from drawlib.preset_colors import GoogleColors
from drawlib.preset_styles import GoogleStyles

# Initialize color palette and style presets
Colors = GoogleColors()
Styles = GoogleStyles().patch_font(
    regular=Font.SANSSERIF_REGULAR,
    bold=Font.SANSSERIF_BOLD,
    thin=Font.SANSSERIF_THIN,
)
```

## 11.2 Available Style Presets and Neutral Card Tokens

Drawlib provides three global theme presets:

- **`DefaultStyles` / `DefaultColors`**: Modern developer theme inspired by Tailwind and VitePress.
- **`GoogleStyles` / `GoogleColors`**: Clean editorial theme inspired by Material Design and Google Docs.
- **`MonochromeStyles` / `MonochromeColors`**: Grayscale theme optimized for black-and-white printing.

Across all theme presets, Drawlib includes built-in neutral card tokens to support the **50%+ Neutral Baseline Rule** (grounding at least 50% of diagram shapes in calm neutral fills rather than creating noisy rainbow diagrams):

- **`Styles.Neutral`**: Clean white/light-gray card surface for standard nodes and containers.
- **`Styles.PrimaryNeutral`**: Soft primary-tinted background with a subtle border for primary subsystems.
- **`Styles.SecondaryNeutral`**: Soft secondary-tinted background with a subtle border for supporting components.
- **`Styles.PrimaryFlat` / `Styles.AccentFlat` / `Styles.DarkFlat`**: High-contrast saturated fills reserved strictly for 1–2 primary focal points or container header bars.

## 11.3 Deriving Custom Styles (`.patch()`) and Sharing `utils.py` Helpers

Derive custom styles from existing presets by overriding specific attributes with `.patch()`. Furthermore, any constants or helper functions defined in your project's `utils.py` are automatically exposed to embedded ````drawlib```` blocks via `from drawlib.utils import ...`:

```python
# Defined in utils.py
from drawlib.shapes import rectangle
from drawlib.styles import Styles

# Derive a custom card style from PrimaryNeutral
CARD_STYLE = Styles.PrimaryNeutral.patch(shape_r=2.0, shape_line_width=1.5)
HEADER_STYLE = Styles.PrimaryFlat.patch(shape_r=1.5)


def draw_titled_card(xy: tuple[float, float], width: float, height: float, title: str) -> None:
    """Reusable helper to draw a neutral container card with a header bar."""
    cx, cy = xy
    rectangle((cx, cy), width=width, height=height, style=CARD_STYLE)
    rectangle(
        (cx, cy + height / 2 - 3.5),
        width=width - 2.0,
        height=5.5,
        style=HEADER_STYLE,
        text=title,
        text_style=Styles.WhiteBold.patch(text_size=11.0),
    )
```

Import and call your shared helpers inside any chapter's ````drawlib```` block:

```python
from drawlib.utils import CARD_STYLE, draw_titled_card

draw_titled_card((50, 25), width=40, height=30, title="Auth Service")
```

## 11.4 Harmonizing with Document CSS (`style.css`)

When you run `drawlib init --style google`, both `styles.py` and `style.css` are configured with the Google theme. This ensures **complete visual harmony between technical text, tables, and embedded diagrams**.
