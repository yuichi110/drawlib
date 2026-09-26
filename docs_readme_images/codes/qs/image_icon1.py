from drawlib.canvas import config, save
from drawlib.colors import Colors
from drawlib.icons import phosphor
from drawlib.preset_styles import default_styles

config(width=100, height=60, grid=True)
ps = default_styles

phosphor.airplane((25, 30), width=20, style=ps.primary)
phosphor.coffee(
    xy=(75, 30),
    width=20,
    angle=45,
    style=ps.primary.patch(icon_color=Colors.Red, icon_style="fill"),
)

save()

