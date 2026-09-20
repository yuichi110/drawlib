from drawlib.canvas import save
from drawlib.colors import Colors140
from drawlib.shapes import circle
from drawlib.types import ShapeStyle

circle(
    xy=(50, 50),
    radius=30,
    style=ShapeStyle(
        line_style="dashed",
        line_color=Colors140.BlueViolet,
        line_width=5,
        fill_color=Colors140.Turquoise,
    ),
)
save()
