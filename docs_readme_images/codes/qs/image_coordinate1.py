from drawlib.canvas import config, save
from drawlib.colors import Colors
from drawlib.shapes import circle
from drawlib.text import text
from drawlib.types import ShapeStyle, TextStyle

config(width=100, height=50, grid_only=True)

circle(
    xy=(25, 25),
    radius=10,
    style=ShapeStyle(text_halign="center", text_valign="center"),
)
circle(
    xy=(25, 25),
    radius=1,
    style=ShapeStyle(fill_color=Colors.Red, line_color=Colors.Red),
)
text((25, 10), "Align center,center", style=TextStyle(text_color=Colors.Red))

circle(
    xy=(75, 25),
    radius=10,
    style=ShapeStyle(text_halign="left", text_valign="bottom"),
)
circle(
    xy=(75, 25),
    radius=1,
    style=ShapeStyle(fill_color=Colors.Red, line_color=Colors.Red),
)
text((75, 10), "Align left,bottom", style=TextStyle(text_color=Colors.Red))

save()
