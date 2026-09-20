from drawlib.canvas import config, save
from drawlib.colors import Colors
from drawlib.icons import icon_phosphor
from drawlib.types import IconStyle

config(width=100, height=60, grid=True)

icon_phosphor.airplane((25, 30), width=20)
icon_phosphor.coffee(
    xy=(75, 30),
    width=20,
    angle=45,
    style=IconStyle(text_color=Colors.Red, icon_style="fill"),
)

save()
