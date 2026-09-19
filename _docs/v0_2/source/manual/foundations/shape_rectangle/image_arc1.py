from drawlib.apis import *

config(width=100, height=50, grid_only=True)
arc(xy=(25, 25), width=30, height=20, angle_start=0, angle_end=135)
arc(
    xy=(75, 25),
    width=40,
    height=30,
    angle_start=0,
    angle_end=135,
    angle=45,
    text="arc",
)
save()
