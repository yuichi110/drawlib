from drawlib.canvas import save, setup
from drawlib.colors import Colors
from drawlib.icons import phosphor
from drawlib.config import styles

setup(width=100, height=60, grid=True)
phosphor.airplane((25, 30), width=20, style=styles.primary)
phosphor.coffee(
    xy=(75, 30),
    width=20,
    angle=45,
    style=styles.primary.patch(icon_color=Colors.Red, icon_style="fill"),
)

save()

