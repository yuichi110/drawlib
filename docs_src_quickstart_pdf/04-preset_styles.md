# 4. Preset Styles & Themes

Instead of constructing a custom `Style(...)` object for every shape, Drawlib includes a powerful **Preset Styles** system (`drawlib.preset_styles`). Every drawing function accepts a shorthand style name string such as `style="blue"` or `style="red_flat"`.

## Official Style Presets

Drawlib ships with three curated preset themes:
- **`"default"`**: Clean, approachable palette with soft fills and crisp borders.
- **`"essentials"`**: Rich, high-contrast palette for modern technical presentations.
- **`"monochrome"`**: Grayscale palette tailored for print books and academic papers.

## Using Style Name Shortcuts

You can combine color names (`blue`, `green`, `red`, `black`, `white`) with variant modifiers (`flat`, `solid`, `dashed`) directly in the `style` parameter:

```python
circle((20, 25), radius=10)                 # Default style
circle((45, 25), radius=10, style="blue")   # Blue accent
circle((70, 25), radius=10, style="green")  # Green accent
```

```drawlib 600px center caption:"Figure 4.1: Applying Preset Style Names to Lines, Shapes, and Text"
from drawlib.canvas import config
from drawlib.lines import line
from drawlib.shapes import circle
from drawlib.text import text

config(width=100, height=45)
line_y = 36
text_y = 9

# 1. Default style
line((12, line_y), (26, line_y))
circle((19, 23), radius=8)
text((19, text_y), text="default", size=10)

# 2. Blue style
line((33, line_y), (47, line_y), style="blue")
circle((40, 23), radius=8, style="blue")
text((40, text_y), text='style="blue"', style="blue", size=10)

# 3. Green style
line((54, line_y), (68, line_y), style="green")
circle((61, 23), radius=8, style="green")
text((61, text_y), text='style="green"', style="green", size=10)

# 4. Red style
line((75, line_y), (89, line_y), style="red")
circle((82, 23), radius=8, style="red")
text((82, text_y), text='style="red"', style="red", size=10)
```
