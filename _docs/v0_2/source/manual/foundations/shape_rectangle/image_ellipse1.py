from drawlib.apis import *

config(width=100, height=50, grid_only=True)
ellipse(xy=(25, 25), width=30, height=20)
ellipse(xy=(75, 25), width=35, height=25, angle=45, text="ellipse()")
save()
