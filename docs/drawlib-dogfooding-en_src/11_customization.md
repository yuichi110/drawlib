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

## 11.2 Available Style Presets

- **`DefaultStyles` / `DefaultColors`**: Modern developer theme inspired by Tailwind and VitePress.
- **`GoogleStyles` / `GoogleColors`**: Clean editorial theme inspired by Material Design and Google Docs.
- **`MonochromeStyles` / `MonochromeColors`**: Grayscale theme optimized for black-and-white printing.

## 11.3 Deriving Custom Styles (`.patch()`)

Derive custom styles from existing presets by overriding specific attributes:

```python
from drawlib.styles import Styles

# Derive a custom card style from PrimaryFlat
my_card_style = Styles.PrimaryFlat.patch(
    shape_fill_color=(235, 248, 255),
    shape_line_color=(49, 130, 206),
    shape_line_width=1.5,
)
```

## 11.4 Harmonizing with Document CSS (`style.css`)

When you run `drawlib init --style google`, both `styles.py` and `style.css` are configured with the Google theme. This ensures **complete visual harmony between technical text, tables, and embedded diagrams**.
