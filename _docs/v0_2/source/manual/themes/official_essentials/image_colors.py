from drawlib.apis import *

dtheme.apply_official_theme("essentials")

config(width=100, height=100)
start_x = 12
pad_x = 19


def draw_horizon(colors: list[str], y):
    rect_y = y
    text1_y = y - 6
    text2_y = y - 9

    for i, color_name in enumerate(colors):
        color = dtheme.colors.get(color_name)
        x = start_x + pad_x * i
        lwidth = 0 if color_name not in ["white", "ivory"] else 1
        rectangle(
            (x, rect_y),
            width=12,
            height=6,
            style=ShapeStyle(fcolor=color, lwidth=lwidth, lcolor=Colors.Black),
        )
        text((x, text1_y), color_name)
        text((x, text2_y), str(color[:3]), style=TextStyle(size=14))


draw_horizon(["red", "lightred", "pink", "brown", "orange"], 90)
draw_horizon(["green", "lightgreen", "greenyellow", "teal", "olive"], 70)
draw_horizon(["blue", "lightblue", "aqua", "navy", "steel"], 50)
draw_horizon(["yellow", "purple", "ivory", "black", "charcoal"], 32.5)
draw_horizon(["graphite", "gray", "silver", "snow", "white"], 15)
save()
