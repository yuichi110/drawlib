from drawlib.apis import *

config(width=100, height=50, dpi=200)

# original
original_image = Dimage("linux.png")
image((20, 25), 20, original_image)
text((20, 10), "original")

# mirror
image((50, 25), 20, original_image.mirror())
text((50, 10), "mirror()")

# flip
image((80, 25), 20, original_image.flip())
text((80, 10), "flip()")

save()
