from drawlib.canvas import config, save
from drawlib.colors import Colors
from drawlib.preset_styles import default_styles
from drawlib.shapes import circle
from drawlib.text import text

config(width=100, height=50, grid_only=True)
ps = default_styles

circle(
    xy=(25, 25),
    radius=10,
    style=ps.primary.patch(text_halign="center", text_valign="center"),
)
circle(
    xy=(25, 25),
    radius=1,
    style=ps.primary.patch(shape_fill_color=Colors.Red, shape_line_color=Colors.Red),
)
text((25, 10), "Align center,center", style=ps.primary.patch(text_color=Colors.Red))

circle(
    xy=(75, 25),
    radius=10,
    style=ps.primary.patch(text_halign="left", text_valign="bottom"),
)
circle(
    xy=(75, 25),
    radius=1,
    style=ps.primary.patch(shape_fill_color=Colors.Red, shape_line_color=Colors.Red),
)
text((75, 10), "Align left,bottom", style=ps.primary.patch(text_color=Colors.Red))

save()

