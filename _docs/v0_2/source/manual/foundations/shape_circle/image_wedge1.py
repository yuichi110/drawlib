from drawlib.apis import *

config(width=100, height=50, grid_only=True)
wedge(xy=(25, 25), radius=15, width=5, angle_start=0, angle_end=135)
wedge(
    xy=(75, 25),
    radius=20,
    width=10,
    angle_start=0,
    angle_end=135,
    angle=45,
    text="wedge",
)
save()
