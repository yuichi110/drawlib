from drawlib.apis import *

config(width=100, height=50, grid_only=True)
circle(xy=(25, 25), radius=15)
circle(xy=(75, 25), radius=20, angle=45, text="circle")
save()
