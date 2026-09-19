from drawlib.apis import *

config(width=100, height=50, grid_only=True)
rhombus(xy=(25, 25), width=20, height=40)
rhombus(xy=(75, 25), width=40, height=20, angle=45, text="rhombus()")
save()
