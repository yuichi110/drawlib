# Drawlib Preset Styles Guidelines

Preset styles allow applying consistent colors, border styles, line widths, and font weights using string names.

## 1. Style Naming Syntax
Syntax format: `<color>_<type>_<weight>`
Any component set to default can be omitted.

- `<color>`:
  - Official default colors: `red`, `green`, `blue`, `black`, `white`.
  - Essentials colors: `pink`, `brown`, `orange`, `teal`, `olive`, `aqua`, `navy`, `purple`, `gray`, `charcoal`, etc.
- `<type>`:
  - (default): Shape has border line and fill color. Line is solid.
  - `flat`: Shape has fill color with NO border line.
  - `solid`: Shape has border line outline with NO fill color.
  - `dashed`: Shape or line has dashed outline with NO fill color.
- `<weight>`:
  - `light`: Half of default line width; light font weight.
  - (default): Standard line width; regular font weight.
  - `bold`: Double line width; bold font weight.

Examples: `"blue"`, `"red_flat"`, `"green_dashed_bold"`, `"white_bold"`, `"black_solid_light"`.

## 2. Color Palette Classes
```python
from drawlib.colors import Colors, ColorsDefault, ColorsEssentials, ColorsMonochrome

# RGB tuples with alpha:
c1 = ColorsDefault.Blue
c2 = ColorsEssentials.Navy
c3 = ColorsMonochrome.Charcoal
c4 = Colors.White
```

## 3. Minimal Example
```python
from drawlib.canvas import config, save
from drawlib.lines import line
from drawlib.shapes import rectangle

config(width=100, height=50)
rectangle((30, 25), width=30, height=20, style="blue_flat", text="Flat Fill", textstyle="white")
rectangle((70, 25), width=30, height=20, style="red_solid_bold", text="Solid Outline", textstyle="red_bold")
line((15, 8), (85, 8), style="green_dashed")
save()
```
