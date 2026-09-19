from drawlib.apis import *

config(width=150, height=50)

# left
rectangle(xy=(25, 25), width=40, height=20)
circle(
    xy=(25, 25),
    radius=15,
    style=ShapeStyle(
        lwidth=5,
        lcolor=Colors.Red,
        lstyle="dashed",
        fcolor=Colors.White,
    ),
)

# center
rectangle(xy=(75, 25), width=40, height=20)
circle(
    xy=(75, 25),
    radius=15,
    style=ShapeStyle(
        lwidth=5,
        lcolor=Colors.Red,
        lstyle="dashed",
        fcolor=Colors.Transparent,
    ),
)

# right
rectangle(xy=(125, 25), width=40, height=20)
circle(
    xy=(125, 25),
    radius=15,
    style=ShapeStyle(
        lwidth=0,
        fcolor=Colors140.Orange,
        alpha=0.3,
    ),
)
save()
