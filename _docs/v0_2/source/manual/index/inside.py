from drawlib.apis import *

circle(
    xy=(50, 50),
    radius=30,
    style=ShapeStyle(
        lstyle="dashed",
        lcolor=Colors140.BlueViolet,
        lwidth=5,
        fcolor=Colors140.Turquoise,
    ),
)
save()
