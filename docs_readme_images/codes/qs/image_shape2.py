from drawlib.canvas import config, save
from drawlib.colors import Colors
from drawlib.shapes import rectangle
from drawlib.text import text
from drawlib.types import ShapeStyle, ShapeTextStyle

config(width=100, height=50, grid=True)

rectangle(
    (25, 25),
    width=30,
    height=20,
    angle=45,
    text="Hello!",
    style=ShapeStyle(line_style="dashed", line_width=5, line_color=Colors.Red, fill_color=Colors.Transparent),
)
rectangle(
    (75, 25),
    width=30,
    height=20,
    angle=45,
    text="Hello!",
    textstyle=ShapeTextStyle(text_color=Colors.White, text_size=20, text_xy_shift=(-10, 0), text_angle=0),
)

save()
