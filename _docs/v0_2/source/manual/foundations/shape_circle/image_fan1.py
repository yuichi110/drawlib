from drawlib.apis import *

config(width=100, height=50, grid_only=True)
fan(xy=(25, 25), radius=15, angle_start=0, angle_end=135)
fan(
    xy=(75, 25),
    radius=20,
    angle_start=0,
    angle_end=135,
    angle=45,
    text="fan",
)
save()
