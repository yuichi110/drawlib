from drawlib.canvas import config, save
from drawlib.colors import Colors
from drawlib.shapes import circle
from drawlib.text import text
from drawlib.types import Style

config(width=100, height=50, grid_only=True)

circle(
    xy=(25, 25),
    radius=10,
    style=Style(text_halign="center", text_valign="center"),
)
circle(
    xy=(25, 25),
    radius=1,
    style=Style(fill_color=Colors.Red, line_color=Colors.Red),
)
text((25, 10), "Align center,center", style=Style(text_color=Colors.Red))

circle(
    xy=(75, 25),
    radius=10,
    style=Style(text_halign="left", text_valign="bottom"),
)
circle(
    xy=(75, 25),
    radius=1,
    style=Style(fill_color=Colors.Red, line_color=Colors.Red),
)
text((75, 10), "Align left,bottom", style=Style(text_color=Colors.Red))

save()
