# Color Classes


Drawlib's color format is standard RGB `(0-255, 0-255, 0-255)` or RGBA `(0-255, 0-255, 0-255, 0.0-1.0)`. 
To make color handling intuitive, Drawlib provides pre-defined Color classes as well as utility functions (`from_hex`, `from_grayscale`, `with_alpha`) in `drawlib.colors`:

- `Colors`: Basic web 16 colors + Transparent
- `Colors140`: Full CSS web 140 colors + Transparent
- `ColorsDefault`: Colors used in preset style `default`
- `ColorsEssentials`: Colors used in preset style `essentials`
- `ColorsMonochrome`: Grayscale colors used in preset style `monochrome`

Here is an image showing their relationships:


```drawlib fold-code 600px center
from drawlib.canvas import config, save
from drawlib.colors import Colors, Colors140
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.text import text
from drawlib.types import Style

config(width=100, height=80)
y1 = 70
y2 = 40
y3 = 25
y4 = 10
rect_width = 25
rect_height = 10
rect_style = Style(fill_color=Colors.White)
rect_text_style = Style(text_size=18)

COLORS_BASE_TEXT = """
- Transparent = (0, 0, 0, 0.0)

- get_rgba()

- get_rgba_from_hexcode()

- get_rgba_from_grayscale()
""".strip()

COLORS_TEXT = """
- BLACK = (0, 0, 0)
- WHITE = (255, 255, 255)
- . . .
""".strip()


def draw_base():
    rectangle(
        (20, y1),
        width=rect_width,
        height=rect_height,
        style=rect_style,
        text="ColorsBase\n(Base Class)",
        textstyle=rect_text_style,
    )

    text(
        (7.5, 60),
        COLORS_BASE_TEXT,
        style=(Style(text_halign="left", text_valign="top")),
    )


def draw_line_arrows():
    x1 = 40
    x2 = 47.5
    x3 = 55
    line((x1, y1), (x3, y1), arrowhead="->")
    text((x2, y1 + 3), "inherit", style=Style(text_size=20))
    line((x2, y1), (x2, y4))
    line((x2, y2), (x3, y2), arrowhead="->")
    line((x2, y3), (x3, y3), arrowhead="->")
    line((x2, y4), (x3, y4), arrowhead="->")


def draw_childs():
    x = 75
    rectangle(
        (x, y1),
        width=rect_width,
        height=rect_height,
        style=rect_style,
        text="Colors\n(CSS 16 Colors)",
        textstyle=rect_text_style,
    )

    text(
        (62.5, 60),
        COLORS_TEXT,
        style=(Style(text_halign="left", text_valign="top")),
    )

    rectangle(
        (x, y2),
        width=rect_width,
        height=rect_height,
        style=rect_style,
        text="Colors140\n(CSS 140 Colors)",
        textstyle=rect_text_style,
    )

    text((x, y3), "...", style=Style(text_size=32))

    rectangle(
        (x, y4),
        width=rect_width,
        height=rect_height,
        style=rect_style,
        text="Your_Colors_Class",
        textstyle=rect_text_style,
    )


draw_base()
draw_line_arrows()
draw_childs()
```

As you can see, `ColorsBase` class implements the `Transparent` color and utility functions. 
Each child class inherits these and implements its own colors. 

You can create your own color class as well. 
Let's look at an example of creating a Google color class at end of this page.


# Colors


The `Colors` class contains the following members:

- Transparent: (0, 0, 0, 0.0)
- Aqua: (0, 255, 255)
- Black: (0, 0, 0)
- Blue: (0, 0, 255)
- Fuchsia: (255, 0, 255)
- Gray: (128, 128, 128)
- Green: (0, 128, 0)
- Lime: (0, 255, 0)
- Maroon: (128, 0, 0)
- Navy: (0, 0, 128)
- Olive: (128, 128, 0)
- Purple: (128, 0, 128)
- Red: (255, 0, 0)
- Silver: (192, 192, 192)
- Teal: (0, 128, 128)
- White: (255, 255, 255)
- Yellow: (255, 255, 0)


# Colors140


The `Colors140` class contains the following members:

- Transparent: (0, 0, 0, 0.0)
- AliceBlue: (240, 248, 255)
- AntiqueWhite: (250, 235, 215)
- Aqua: (0, 255, 255)
- Aquamarine: (127, 255, 212)
- Azure: (240, 255, 255)
- Beige: (245, 245, 220)
- Bisque: (255, 228, 196)
- Black: (0, 0, 0)
- BlanchedAlmond: (255, 235, 205)
- Blue: (0, 0, 255)
- BlueViolet: (138, 43, 226)
- Brown: (165, 42, 42)
- BurlyWood: (222, 184, 135)
- CadetBlue: (95, 158, 160)
- Chartreuse: (127, 255, 0)
- Chocolate: (210, 105, 30)
- Coral: (255, 127, 80)
- CornflowerBlue: (100, 149, 237)
- Cornsilk: (255, 248, 220)
- Crimson: (220, 20, 60)
- Cyan: (0, 255, 255)
- DarkBlue: (0, 0, 139)
- DarkCyan: (0, 139, 139)
- DarkGoldenRod: (184, 134, 11)
- DarkGray: (169, 169, 169)
- DarkGreen: (0, 100, 0)
- DarkKhaki: (189, 183, 107)
- DarkMagenta: (139, 0, 139)
- DarkOliveGreen: (85, 107, 47)
- DarkOrange: (255, 140, 0)
- DarkOrchid: (153, 50, 204)
- DarkRed: (139, 0, 0)
- DarkSalmon: (233, 150, 122)
- DarkSeaGreen: (143, 188, 143)
- DarkSlateBlue: (72, 61, 139)
- DarkSlateGray: (47, 79, 79)
- DarkTurquoise: (0, 206, 209)
- DarkViolet: (148, 0, 211)
- DeepPink: (255, 20, 147)
- DeepSkyBlue: (0, 191, 255)
- DimGray: (105, 105, 105)
- DodgerBlue: (30, 144, 255)
- FireBrick: (178, 34, 34)
- FloralWhite: (255, 250, 240)
- ForestGreen: (34, 139, 34)
- Fuchsia: (255, 0, 255)
- Gainsboro: (220, 220, 220)
- GhostWhite: (248, 248, 255)
- Gold: (255, 215, 0)
- GoldenRod: (218, 165, 32)
- Gray: (128, 128, 128)
- Green: (0, 128, 0)
- GreenYellow: (173, 255, 47)
- HoneyDew: (240, 255, 240)
- HotPink: (255, 105, 180)
- IndianRed: (205, 92, 92)
- Indigo: (75, 0, 130)
- Ivory: (255, 255, 240)
- Khaki: (240, 230, 140)
- Lavender: (230, 230, 250)
- LavenderBlush: (255, 240, 245)
- LawnGreen: (124, 252, 0)
- LemonChiffon: (255, 250, 205)
- LightBlue: (173, 216, 230)
- LightCoral: (240, 128, 128)
- LightCyan: (224, 255, 255)
- LightGoldenRodYellow: (250, 250, 210)
- LightGray: (211, 211, 211)
- LightGreen: (144, 238, 144)
- LightPink: (255, 182, 193)
- LightSalmon: (255, 160, 122)
- LightSeaGreen: (32, 178, 170)
- LightSkyBlue: (135, 206, 250)
- LightSlateGray: (119, 136, 153)
- LightSteelBlue: (176, 196, 222)
- LightYellow: (255, 255, 224)
- Lime: (0, 255, 0)
- LimeGreen: (50, 205, 50)
- Linen: (250, 240, 230)
- Magenta: (255, 0, 255)
- Maroon: (128, 0, 0)
- MediumAquaMarine: (102, 205, 170)
- MediumBlue: (0, 0, 205)
- MediumOrchid: (186, 85, 211)
- MediumPurple: (147, 112, 219)
- MediumSeaGreen: (60, 179, 113)
- MediumSlateBlue: (123, 104, 238)
- MediumSpringGreen: (0, 250, 154)
- MediumTurquoise: (72, 209, 204)
- MediumVioletRed: (199, 21, 133)
- MidnightBlue: (25, 25, 112)
- MintCream: (245, 255, 250)
- MistyRose: (255, 228, 225)
- Moccasin: (255, 228, 181)
- NavajoWhite: (255, 222, 173)
- Navy: (0, 0, 128)
- OldLace: (253, 245, 230)
- Olive: (128, 128, 0)
- OliveDrab: (107, 142, 35)
- Orange: (255, 165, 0)
- OrangeRed: (255, 69, 0)
- Orchid: (218, 112, 214)
- PaleGoldenRod: (238, 232, 170)
- PaleGreen: (152, 251, 152)
- PaleTurquoise: (175, 238, 238)
- PaleVioletRed: (219, 112, 147)
- PapayaWhip: (255, 239, 213)
- PeachPuff: (255, 218, 185)
- Peru: (205, 133, 63)
- Pink: (255, 192, 203)
- Plum: (221, 160, 221)
- PowderBlue: (176, 224, 230)
- Purple: (128, 0, 128)
- RebeccaPurple: (102, 51, 153)
- Red: (255, 0, 0)
- RosyBrown: (188, 143, 143)
- RoyalBlue: (65, 105, 225)
- SaddleBrown: (139, 69, 19)
- Salmon: (250, 128, 114)
- SandyBrown: (244, 164, 96)
- SeaGreen: (46, 139, 87)
- SeaShell: (255, 245, 238)
- Sienna: (160, 82, 45)
- Silver: (192, 192, 192)
- SkyBlue: (135, 206, 235)
- SlateBlue: (106, 90, 205)
- SlateGray: (112, 128, 144)
- Snow: (255, 250, 250)
- SpringGreen: (0, 255, 127)
- SteelBlue: (70, 130, 180)
- Tan: (210, 180, 140)
- Teal: (0, 128, 128)
- Thistle: (216, 191, 216)
- Tomato: (255, 99, 71)
- Turquoise: (64, 224, 208)
- Violet: (238, 130, 238)
- Wheat: (245, 222, 179)
- White: (255, 255, 255)
- WhiteSmoke: (245, 245, 245)
- Yellow: (255, 255, 0)
- YellowGreen: (154, 205, 50)



# ColorsDefault


The `ColorsDefault` class contains the following members:

- Red: (239, 95, 95)
- Green: (79, 191, 79)
- Blue: (111, 111, 239)
- Black: (0, 0, 0)
- White: (255, 255, 255)




# ColorsEssentials


The `ColorsEssentials` class contains the following members:

- Red:  (255, 23, 23)
- LightRed: (239, 95, 95)
- Green: (15, 127, 15)
- LightGreen: (79, 191, 79)
- Blue: (31, 31, 255)
- LightBlue: (111, 111, 239)
- Yellow: (239, 239, 31)
- Purple: (127, 31, 127)
- Orange: (255, 95, 31)
- Navy: (15, 15, 127)
- Pink: (239, 63, 239)
- Charcoal: (39, 39, 39)
- Graphite: (63, 63, 63)
- Gray: (127, 127, 127)
- Silver: (191, 191, 191)
- Snow: (239, 239, 239)
- Teal: (15, 127, 127)
- Olive: (127, 127, 31)
- Brown: (159, 31, 31)
- Black: (0, 0, 0)
- White: (255, 255, 255)
- Aqua: (47, 239, 239)
- GreenYellow: (127, 207, 31)
- Ivory: (239, 239, 207)
- Steel: (96, 96, 143)



# ColorsMonochrome


The `ColorsMonochrome` class contains the following members:

- Black: (0, 0, 0)
- Charcoal: (39, 39, 39)
- Graphite: (63, 63, 63)
- Gray: (127, 127, 127)
- Silver: (191, 191, 191)
- Snow: (239, 239, 239)
- White: (255, 255, 255)




# Implement Your Own Colors


We provide a base class for colors called `ColorsBase`. 
You can define your own color palette class by extending this base class.

Suppose you are an official partner of Google, eligible to use their corporate colors. 
Let's define these colors and use them.

Partner Marketing Hub: Google News Color Palette.
https://partnermarketinghub.withgoogle.com/brands/google-news/visual-identity/color-palette/


```python
from drawlib.canvas import config, save
from drawlib.colors import Colors
from drawlib.fonts import FontRoboto
from drawlib.shapes import circle, rectangle, triangle, wedge
from drawlib.text import text
from drawlib.types import Style


# Please define color at styling codes normally.
class ColorsGoogle(ColorsBase):
    # From Official Google Color Palette
    # At Partner Marketing Hub
    Blue = (23, 78, 166)
    Red = (165, 14, 14)
    Orange = (227, 116, 0)
    Green = (32, 33, 36)
    MediumBlue = (66, 103, 210)
    MediumRed = (234, 67, 53)
    Yellow = (251, 188, 4)
    MediumGreen = (52, 168, 83)
    LightBlue = (210, 227, 252)
    LightRed = (250, 210, 207)
    LightYellow = (254, 239, 195)
    LightGreen = (206, 234, 214)
    LightGrey = (241, 243, 244)
    Grey = (154, 160, 166)
    Black = (32, 33, 36)


config(width=100, height=50)
shape_y = 30
circle(
    (15, shape_y),
    radius=10,
    style=Style(line_width=0, fill_color=ColorsGoogle.MediumBlue),
)
triangle(
    (37.5, shape_y),
    width=20,
    height=15,
    style=Style(line_width=0, fill_color=ColorsGoogle.MediumRed),
)
rectangle(
    (62.5, shape_y),
    width=18,
    height=18,
    style=Style(line_width=0, fill_color=ColorsGoogle.Yellow),
)
wedge(
    (85, shape_y),
    radius=10,
    width=5,
    angle_end=270,
    style=Style(line_width=0, fill_color=ColorsGoogle.MediumGreen),
)
text(
    (50, 10),
    "Google Colors",
    style=Style(
        text_color=ColorsGoogle.Black,
        text_size=32,
        text_font=FontRoboto.ROBOTO_REGULAR,
    ),
)
save()
```

In this example, we define a color class and use it in image drawing code. 
Typically, you should define your color class in a styling module and import it into your image code.

Here is the output:


```drawlib 600px center
from drawlib.canvas import config, save
from drawlib.colors import Colors
from drawlib.fonts import FontRoboto
from drawlib.shapes import circle, rectangle, triangle, wedge
from drawlib.text import text
from drawlib.types import Style


# Please define color at styling codes normally.
class ColorsGoogle(ColorsBase):
    # From Official Google Color Palette
    # At Partner Marketing Hub
    Blue = (23, 78, 166)
    Red = (165, 14, 14)
    Orange = (227, 116, 0)
    Green = (32, 33, 36)
    MediumBlue = (66, 103, 210)
    MediumRed = (234, 67, 53)
    Yellow = (251, 188, 4)
    MediumGreen = (52, 168, 83)
    LightBlue = (210, 227, 252)
    LightRed = (250, 210, 207)
    LightYellow = (254, 239, 195)
    LightGreen = (206, 234, 214)
    LightGrey = (241, 243, 244)
    Grey = (154, 160, 166)
    Black = (32, 33, 36)


config(width=100, height=50)
shape_y = 30
circle(
    (15, shape_y),
    radius=10,
    style=Style(line_width=0, fill_color=ColorsGoogle.MediumBlue),
)
triangle(
    (37.5, shape_y),
    width=20,
    height=15,
    style=Style(line_width=0, fill_color=ColorsGoogle.MediumRed),
)
rectangle(
    (62.5, shape_y),
    width=18,
    height=18,
    style=Style(line_width=0, fill_color=ColorsGoogle.Yellow),
)
wedge(
    (85, shape_y),
    radius=10,
    width=5,
    angle_end=270,
    style=Style(line_width=0, fill_color=ColorsGoogle.MediumGreen),
)
text(
    (50, 10),
    "Google Colors",
    style=Style(
        text_color=ColorsGoogle.Black,
        text_size=32,
        text_font=FontRoboto.ROBOTO_REGULAR,
    ),
)
```


# Color Utilities

Drawlib provides helper functions in `drawlib.colors` for converting between hex strings, grayscales, and RGBA tuples:

```python
from drawlib.colors import from_grayscale, from_hex, with_alpha

# 1. Hex code to RGBA:
color1 = from_hex("#4285F4")         # Google Blue (66, 133, 244, 1.0)
color2 = from_hex("#34A85380")       # With alpha (52, 168, 83, 0.5)

# 2. Grayscale to RGBA:
dark_gray = from_grayscale(40)       # (40, 40, 40, 1.0)

# 3. Add or modify alpha channel of an existing color:
transparent_blue = with_alpha(color1, 0.3)  # (66, 133, 244, 0.3)
```

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
