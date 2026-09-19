from drawlib.apis import *

config(width=100, height=50, grid=True)

rectangle(
    (25, 25),
    width=30,
    height=20,
    angle=45,
    text="Hello!",
    style=ShapeStyle(lstyle="dashed", lwidth=5, lcolor=Colors.Red, fcolor=Colors.Transparent),
)
rectangle(
    (75, 25),
    width=30,
    height=20,
    angle=45,
    text="Hello!",
    textstyle=ShapeTextStyle(color=Colors.White, size=20, xy_shift=(-10, 0), angle=0),
)

save()
