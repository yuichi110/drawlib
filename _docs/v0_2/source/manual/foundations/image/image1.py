from drawlib.apis import *

config(width=100, height=50, grid_only=True)

image(xy=(15, 25), width=10, image="python.png")
image(xy=(40, 25), width=20, image="python.png")
image(xy=(75, 25), width=30, image="python.png")

save()
