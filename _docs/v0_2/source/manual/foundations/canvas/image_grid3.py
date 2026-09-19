from drawlib.apis import *

config(
    width=100,
    height=50,
    grid_only=True,
    grid_style=LineStyle(width=1, color=Colors.Red, style="dashed"),
    grid_centerstyle=LineStyle(width=2, color=Colors.Blue, style="dashed"),
)
circle((50, 25), radius=20)
save()
