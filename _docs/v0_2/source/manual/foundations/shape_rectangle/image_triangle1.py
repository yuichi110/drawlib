from drawlib.apis import *

config(width=100, height=50, grid_only=True)
triangle(xy=(25, 25), width=30, height=20)
triangle(xy=(75, 25), width=35, height=25, topvertex_x=0, angle=45, text="rectangle()")
save()
