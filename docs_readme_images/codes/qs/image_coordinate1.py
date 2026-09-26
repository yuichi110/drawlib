from drawlib.canvas import save, setup
from drawlib.colors import Colors
from drawlib.config import styles
from drawlib.shapes import circle
from drawlib.text import text

setup(width=100, height=50, grid_only=True)
circle(
    xy=(25, 25),
    radius=10,
    style=styles.primary.patch(text_halign="center", text_valign="center"),
)
circle(
    xy=(25, 25),
    radius=1,
    style=styles.primary.patch(shape_fill_color=Colors.Red, shape_line_color=Colors.Red),
)
text((25, 10), "Align center,center", style=styles.primary.patch(text_color=Colors.Red))

circle(
    xy=(75, 25),
    radius=10,
    style=styles.primary.patch(text_halign="left", text_valign="bottom"),
)
circle(
    xy=(75, 25),
    radius=1,
    style=styles.primary.patch(shape_fill_color=Colors.Red, shape_line_color=Colors.Red),
)
text((75, 10), "Align left,bottom", style=styles.primary.patch(text_color=Colors.Red))

save()

