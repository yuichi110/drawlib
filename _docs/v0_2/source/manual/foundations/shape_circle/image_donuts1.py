from drawlib.apis import *

config(width=100, height=50, grid_only=True)
donuts(xy=(25, 25), radius=15, width=5)
donuts(xy=(75, 25), radius=20, width=10, angle=45, text="donuts")
save()
