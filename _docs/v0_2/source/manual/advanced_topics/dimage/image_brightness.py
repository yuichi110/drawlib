from drawlib.apis import *

config(width=100, height=50, dpi=200)

image((20, 25), 20, Dimage("linux.png").brightness(0.5))
text((20, 10), "brightness(0.5)")

image((50, 25), 20, Dimage("linux.png").brightness(1.0))
text((50, 10), "brightness(1.0): Original")

image((80, 25), 20, Dimage("linux.png").brightness(2.0))
text((80, 10), "brightness(2.0)")

save()
