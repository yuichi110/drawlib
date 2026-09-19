from drawlib.apis import *

dtheme.apply_official_theme("monochrome")


start_x = 10
pad_x = 16
icon_y = 43
line_y = 36
rect_y = 27
image_y = 13
text_y = 5

rectangle(
    (82, 0),
    width=18,
    height=50,
    style=ShapeStyle(halign="left", valign="bottom", lwidth=0, fcolor=Colors140.LightGray),
)


def draw_styles(name: str):

    if name == "":
        style_names = ["", "flat", "solid", "dashed"]
    else:
        style_names = [name, f"{name}_flat", f"{name}_solid", f"{name}_dashed"]

    for i, style_name in enumerate(style_names):
        x = start_x + pad_x * i
        t = style_name if style_name != "" else "(default)"

        if dtheme.iconstyles.has(style_name):
            icon_phosphor.heart((x, icon_y), width=10, style=style_name)

        if dtheme.linestyles.has(style_name):
            line((x - 5, line_y), (x + 5, line_y), style=style_name)

        if dtheme.shapestyles.has(style_name):
            rectangle((x, rect_y), width=12, height=12, style=style_name)

        if dtheme.imagestyles.has(style_name):
            image((x, image_y), 10, "../python.png", style=style_name)

        if dtheme.textstyles.has(style_name):
            text((x, text_y), t, style=style_name)
        else:
            text((x, text_y), t)


def draw_colors(colors: list[str]):
    for color in colors:
        clear()
        if color not in ["white"]:
            config(width=100, height=50)
        else:
            config(width=100, height=50, background_color=Colors.Gray)

        draw_styles(color)

        if color != "":
            color = "_" + color
        save(f"image_style{color}.png")


draw_colors([""] + dtheme.colors.list())
