from drawlib.apis import *

textstyle_bold = TextStyle(font=FontRoboto.ROBOTO_BOLD, size=20)
shapetextstyle_bold = ShapeTextStyle(font=FontRoboto.ROBOTO_BOLD, size=20)
config(width=100, height=60, grid=True)


def bottom():
    rectangle(
        (50, 7),
        width=90,
        height=10,
        r=2,
        style=ShapeStyle(fcolor=Colors.Transparent),
        text="Canvas and coordinate system, theme etc.",
        textstyle=shapetextstyle_bold,
    )


def middle(x, width, name, functions, styles):
    rectangle(
        (x, 30),
        width=width,
        height=30,
        r=2,
        style=ShapeStyle(halign="left", fcolor=Colors.Transparent),
    )
    tx = x + width / 2
    text((tx, 42), name, style=textstyle_bold)

    for i, function in enumerate(functions):
        text(
            (x + 1, 36 - i * 3),
            f"- {function}",
            style=TextStyle(halign="left", size=12),
        )

    line((x + 1, 26), (x + width - 1, 26), style=LineStyle(style="dashed"))

    for i, style in enumerate(styles):
        text(
            (x + 1, 22 - i * 3),
            f"- {style}",
            style=TextStyle(halign="left", size=12),
        )


def top():
    rectangle(
        (50, 53),
        width=90,
        height=10,
        r=2,
        style=ShapeStyle(fcolor=Colors.Transparent),
        text="Advanced topics, handle many files etc.",
        textstyle=shapetextstyle_bold,
    )


bottom()

for i, t in enumerate([
    ("icon", ["icon()", "icon_phosphor()"], ["IconStyle"]),
    ("image", ["image()"], ["ImageStyle"]),
    ("line", ["line()", "line_curved()", "..."], ["LineStyle"]),
    ("shape", ["circle()", "rectangle()", "..."], ["ShapeStyle", "ShapeTextStyle"]),
    ("text", ["text()"], ["TextStyle"]),
]):
    start = 5
    width = 16.5
    space = (90 - (width * 5)) / 4
    x = start + (width + space) * i
    name = t[0]
    functions = t[1]
    styles = t[2]
    middle(x, width, name, functions, styles)

top()

save()
