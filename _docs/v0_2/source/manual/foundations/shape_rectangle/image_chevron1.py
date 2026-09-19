from drawlib.apis import *

config(width=100, height=50, grid_only=True)
chevron(xy=(25, 25), width=30, height=20, corner_angle=30)
chevron(xy=(75, 25), width=35, height=25, corner_angle=60, mirror=True, angle=45, text="chevron()")
save()
