from drawlib.canvas import config, save
from drawlib.colors import Colors
from drawlib.icons import phosphor
from drawlib.types import Style

config(width=100, height=60, grid=True)

phosphor.airplane((25, 30), width=20)
phosphor.coffee(
    xy=(75, 30),
    width=20,
    angle=45,
    style=Style(text_color=Colors.Red, icon_style="fill"),
)

save()
