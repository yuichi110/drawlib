from drawlib.canvas import config, save
from drawlib.colors import Colors
from drawlib.preset_styles import default_styles
from drawlib.shapes import rectangle

config(width=100, height=50, grid=True)
ps = default_styles

rectangle(
    (25, 25),
    width=30,
    height=20,
    angle=45,
    text="Hello!",
    style=ps.dashed.patch(
        shape_line_width=5,
        shape_line_color=Colors.Red,
        shape_fill_color=Colors.Transparent,
    ),
)
rectangle(
    (75, 25),
    width=30,
    height=20,
    angle=45,
    text="Hello!",
    style=ps.primary,
    textstyle=ps.primary.patch(text_color=Colors.White, text_size=20, text_xy_shift=(-10, 0), text_angle=0),
)

save()

