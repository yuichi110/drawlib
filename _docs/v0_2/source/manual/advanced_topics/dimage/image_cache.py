from drawlib.apis import *

config(width=100, height=50)
Dimage.cache.set("linux", "linux.png")
im = Dimage.cache.get("linux")
image((50, 25), 25, im)
save()
