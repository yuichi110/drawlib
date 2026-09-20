from drawlib.canvas import config, save
from drawlib.images import image
from drawlib.types import Style

config(width=100, height=50, grid=True)

image(xy=(25, 25), width=20, image="python.png")
image(
    xy=(75, 25),
    width=20,
    angle=45,
    image="python.png",
    style=Style(line_width=1),
)

save()
