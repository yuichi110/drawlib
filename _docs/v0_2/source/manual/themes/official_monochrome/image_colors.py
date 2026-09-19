from drawlib.apis import *

# Changing theme to "default" is optional.
dtheme.apply_official_theme("monochrome")

config(width=100, height=50)
start_x = 10
pad_x = 13
rect_y = 30
text1_y = 15
text2_y = 10

for i, color_name in enumerate(["black", "charcoal", "graphite", "gray", "silver", "snow", "white"]):
    color = dtheme.colors.get(color_name)
    x = start_x + pad_x * i
    lwidth = 0 if color_name != "white" else 1
    rectangle(
        (x, rect_y),
        width=10,
        height=10,
        style=ShapeStyle(fcolor=color, lwidth=lwidth, lcolor=Colors.Black),
    )
    text((x, text1_y), color_name, style=TextStyle(size=14))
    text((x, text2_y), str(color[:3]), style=TextStyle(size=12))

save()
