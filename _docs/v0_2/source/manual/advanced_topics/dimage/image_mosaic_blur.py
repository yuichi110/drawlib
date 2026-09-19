from drawlib.apis import *

config(width=100, height=50, dpi=200)

image((20, 25), 20, Dimage("linux.png").mosaic(8))
text((20, 10), "mosaic(8)")

image((50, 25), 20, Dimage("linux.png").mosaic(16))
text((50, 10), "mosaic(16)")

image((80, 25), 20, Dimage("linux.png").blur())
text((80, 10), "blur()")

save()
