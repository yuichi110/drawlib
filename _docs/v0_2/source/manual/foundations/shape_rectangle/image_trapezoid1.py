from drawlib.apis import *

config(width=100, height=50, grid_only=True)
trapezoid(xy=(25, 25), height=20, bottomedge_width=30, topedge_width=20)
trapezoid(
    xy=(75, 25),
    height=20,
    bottomedge_width=30,
    topedge_width=20,
    topedge_x=0,
    angle=45,
    text="trapezoid()",
)
save()
