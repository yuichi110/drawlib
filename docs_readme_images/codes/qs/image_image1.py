from drawlib.canvas import config, save
from drawlib.images import image
from drawlib.preset_styles import default_styles

config(width=100, height=50, grid=True)
ps = default_styles

image(xy=(25, 25), width=20, image="python.png")
image(
    xy=(75, 25),
    width=20,
    angle=45,
    image="python.png",
    style=ps.primary.patch(image_border_width=1),
)

save()

