from drawlib.apis import *

config(width=100, height=50, dpi=200)

# original
original_image = Dimage("linux.png")
image((25, 30), 20, original_image)
text((25, 15), "original")
width, height = original_image.get_image_size()
text((25, 10), f"width={width}, height={height}")

# resize
new_height = int(height / 2)
resized_image = original_image.resize(width, new_height)
image((75, 30), 20, resized_image)
text((75, 15), "resize()")
text((75, 10), f"width={width}, height={new_height}")

save()
