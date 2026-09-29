from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.styles import Colors, Styles

setup(width=100, height=60, grid=True, color=Colors.canvas)
phosphor.airplane((25, 30), width=20, style=Styles.Primary)
phosphor.coffee(
    xy=(75, 30),
    width=20,
    angle=45,
    style=Styles.Primary.patch(icon_color=Colors.Red, icon_style="fill"),
)

save()
