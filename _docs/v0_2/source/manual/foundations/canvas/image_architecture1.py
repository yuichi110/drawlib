from copy import deepcopy

from drawlib.apis import *

config(width=100, height=60, grid=True)

outer_y = 10
outer_height = 35
outer_r = 2
outer_style = ShapeStyle(halign="left", valign="bottom", fcolor=Colors.Transparent)
text_style = TextStyle(halign="left")


def left():
    rectangle(
        (10, outer_y),
        width=10,
        height=outer_height,
        r=outer_r,
        style=outer_style,
        text="Other drawlib features",
        textstyle=ShapeTextStyle(angle=270, font=FontRoboto.ROBOTO_BOLD, size=18),
    )


def center():
    pad_y = 10
    width = 25
    outer_style2 = deepcopy(outer_style)
    outer_style2.lcolor = Colors.Red
    rectangle(
        (30, outer_y + pad_y),
        width=width,
        height=outer_height - pad_y,
        r=outer_r,
        style=outer_style2,
    )

    text(
        (30 + width / 2, 42),
        "Canvas Instance",
        style=TextStyle(font=FontRoboto.ROBOTO_BOLD, size=18, color=Colors.Red),
    )
    x = 34
    y = 37
    pad_y = 4
    text_style2 = deepcopy(text_style)
    text_style2.color = Colors.Red
    text((x, y), "- config()", style=text_style2)
    text((x, y - pad_y * 1), "- save()", style=text_style2)
    text((x, y - pad_y * 2), "- circle()", style=text_style2)
    text((x, y - pad_y * 3), "- ...", style=text_style2)


def right():
    outer_style2 = deepcopy(outer_style)
    outer_style2.lstyle = "dashed"
    width = 25
    rectangle(
        (65, outer_y),
        width=width,
        height=outer_height,
        r=outer_r,
        style=outer_style2,
    )

    text(
        (65 + width / 2, 42),
        "Public APIs",
        style=TextStyle(font=FontRoboto.ROBOTO_BOLD, size=18),
    )
    x = 69
    y = 37
    pad_y = 4
    text((x, y), "- config()", style=text_style)
    text((x, y - pad_y * 1), "- save()", style=text_style)
    text((x, y - pad_y * 2), "- circle()", style=text_style)
    text((x, y - pad_y * 3), "- ...", style=text_style)
    text((x, y - pad_y * 5), "- Colors", style=text_style)
    text((x, y - pad_y * 6), "- ...", style=text_style)


def center_to_right():
    x1 = 45
    x2 = 68
    y = 37
    pad_y = 4
    for i in range(7):
        if i == 4:
            x1 = 23
            continue

        line((x1, y - pad_y * i), (x2, y - pad_y * i), arrowhead="->", width=1.5, style="dashed")
    text(((23 + 68) / 2, 10), "Publish private as API")


rectangle((5, 5), width=55, height=50, r=outer_r, style=outer_style)
text(
    (5 + 55 / 2, 50),
    "Drawlib's internal state (Private)",
    style=TextStyle(font=FontRoboto.ROBOTO_BOLD, size=18),
)
left()
arrow(
    (21.5, 30),
    (28.5, 30),
    tail_width=1.5,
    head_width=4,
    head_length=2,
    head="<->",
    style=outer_style,
)
center()
right()
center_to_right()

save()
