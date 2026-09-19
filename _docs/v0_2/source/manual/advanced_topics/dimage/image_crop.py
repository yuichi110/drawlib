from drawlib.apis import *

config(width=100, height=50, dpi=200)

# original
original_image = Dimage("linux.png")
image((25, 25), 20, original_image, style=ImageStyle(lwidth=1))
text((25, 10), "original")
width, height = original_image.get_image_size()

# trimming
x_start = int(width / 4)
crop_width = int(width / 2)
y_start = int(height / 4)
crop_height = int(height / 2)
cropped_image = original_image.crop(x_start, y_start, crop_width, crop_height)
image((75, 25), 20, cropped_image, style=ImageStyle(lwidth=1))
text((75, 10), "crop()")

save()
