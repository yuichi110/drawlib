from drawlib.apis import *

config(width=100, height=80)
y1 = 70
y2 = 40
y3 = 25
y4 = 10
rect_width = 25
rect_height = 10
rect_style = ShapeStyle(fcolor=Colors.White)
rect_text_style = ShapeTextStyle(size=18)

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
        style=(TextStyle(halign="left", valign="top")),
    )


def draw_line_arrows():
    x1 = 40
    x2 = 47.5
    x3 = 55
    line((x1, y1), (x3, y1), arrowhead="->")
    text((x2, y1 + 3), "inherit", style=TextStyle(size=20))
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
        style=(TextStyle(halign="left", valign="top")),
    )

    rectangle(
        (x, y2),
        width=rect_width,
        height=rect_height,
        style=rect_style,
        text="Colors140\n(CSS 140 Colors)",
        textstyle=rect_text_style,
    )

    text((x, y3), "...", style=TextStyle(size=32))

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
save()
