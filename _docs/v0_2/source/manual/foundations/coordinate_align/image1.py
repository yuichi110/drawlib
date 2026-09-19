from drawlib.apis import *

config(width=10, height=10, grid_only=True)
for i in range(11):
    circle(xy=(i, i), radius=0.2)
save()
