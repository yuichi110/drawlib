from drawlib.canvas import save, setup
from drawlib.colors import Colors
from drawlib.config import styles
from drawlib.shapes import rectangle

setup(width=100, height=50, grid=True)
rectangle(
    (25, 25),
    width=30,
    height=20,
    angle=45,
    text="Hello!",
    style=styles.dashed.patch(
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
    style=styles.primary,
    textstyle=styles.primary.patch(text_color=Colors.White, text_size=20, text_xy_shift=(-10, 0), text_angle=0),
)

save()

