from drawlib.apis import *

config(width=100, height=50, grid_only=True)
regularpolygon(xy=(25, 25), radius=15, num_vertex=5)
regularpolygon(xy=(75, 25), radius=20, num_vertex=6, angle=45, text="regular polygon")
save()
