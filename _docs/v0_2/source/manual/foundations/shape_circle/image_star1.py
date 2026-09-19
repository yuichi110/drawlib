from drawlib.apis import *

config(width=100, height=50, grid_only=True)
star(xy=(25, 25), num_vertex=5, radius_ext=15, radius_int=5)
star(xy=(75, 25), num_vertex=9, radius_ext=20, radius_int=7.5, angle=45, text="star")
save()
