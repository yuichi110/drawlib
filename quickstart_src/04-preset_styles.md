# 4. Preset Styles & Themes

Instead of constructing a custom `Style(...)` object for every shape, Drawlib includes a powerful **Preset Styles** system accessed via `from drawlib.config import styles`. Every drawing function accepts a preset style such as `style=styles.blue` or `style=styles.red_flat`.

## Official Style Presets

Drawlib ships with three curated preset themes:
- **`"default"`**: Clean, approachable palette with soft fills and crisp borders.
- **`"essentials"`**: Rich, high-contrast palette for modern technical presentations.
- **`"monochrome"`**: Grayscale palette tailored for print books and academic papers.

## Using Style Attributes

You can access color variants (`blue`, `green`, `red`, `black`, `white`) and style modifiers (`flat`, `solid`, `dashed`) directly from `styles`:

```python
from drawlib.config import styles

circle((20, 25), radius=10, style=styles.primary)            # Default style
circle((45, 25), radius=10, style=styles.blue)               # Blue accent
circle((70, 25), radius=10, style=styles.green)              # Green accent
```

```drawlib 600px center caption:"Figure 4.1: Applying Preset Style Names to Lines, Shapes, and Text"
from drawlib.canvas import setup
from drawlib.config import styles
from drawlib.lines import line
from drawlib.shapes import circle
from drawlib.text import text

setup(width=100, height=45)
line_y = 36
text_y = 9

# 1. Default style
line((12, line_y), (26, line_y), style=styles.primary)
circle((19, 23), radius=8, style=styles.primary)
text((19, text_y), text="default", style=styles.primary, size=10)

# 2. Blue style
line((33, line_y), (47, line_y), style=styles.blue)
circle((40, 23), radius=8, style=styles.blue)
text((40, text_y), text="styles.blue", style=styles.blue, size=10)

# 3. Green style
line((54, line_y), (68, line_y), style=styles.green)
circle((61, 23), radius=8, style=styles.green)
text((61, text_y), text="styles.green", style=styles.green, size=10)

# 4. Red style
line((75, line_y), (89, line_y), style=styles.red)
circle((82, 23), radius=8, style=styles.red)
text((82, text_y), text="styles.red", style=styles.red, size=10)
```
