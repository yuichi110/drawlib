from drawlib.apis import *

config(width=100, height=50, grid_only=True)
rectangle(xy=(25, 25), width=30, height=20)
rectangle(xy=(75, 25), width=35, height=25, r=2, angle=45, text="rectangle()")
save()
