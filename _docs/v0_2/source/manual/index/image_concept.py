from drawlib.apis import *

dtheme.change_default_font_size(18)

config(width=100, height=60)


def left():
    x = 18
    circle((x, 30), radius=8, text="Circle", style=ShapeStyle(fcolor=Colors.Transparent))
    text((x, 15), size=24, text="Content")


def center():
    x = 50
    length = 30
    arrow(
        (x - length / 2, 30),
        (x + length / 2, 30),
        tail_width=6,
        head_width=14,
        head_length=10,
        style="green",
        text="Apply Styles",
        textsize=20,
        textstyle="white",
    )


def right():
    x = 82
    circle((x, 49), radius=8, text="Circle")
    circle((x, 30), radius=8, text="Circle", style="blue_flat", textstyle="white")
    circle((x, 11), radius=8, text="Circle", style="red_solid_bold", textstyle="red")


left()
center()
right()
save()
