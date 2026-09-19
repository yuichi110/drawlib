from drawlib.apis import *

config(width=100, height=50, dpi=200)

# original
original_image = Dimage("linux.png")
image((20, 25), 20, original_image)
text((20, 10), "original")

# grayscale
image((50, 25), 20, Dimage("linux.png").grayscale())
text((50, 10), "grayscale()")

# sepia
image((80, 25), 20, original_image.sepia())
text((80, 10), "sepia()")

save()
