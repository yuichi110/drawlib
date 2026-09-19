from drawlib.apis import *

config(width=100, height=50, grid_only=True)
parallelogram(xy=(25, 25), width=20, height=15, corner_angle=30)
parallelogram(xy=(75, 25), width=30, height=20, corner_angle=60, angle=45, text="parallelogram()")
save()
