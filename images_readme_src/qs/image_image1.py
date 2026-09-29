from drawlib.canvas import save, setup
from drawlib.images import image
from drawlib.styles import Colors, Styles

setup(width=100, height=50, grid=True, color=Colors.canvas)
image(xy=(25, 25), width=20, image="python.png")
image(
    xy=(75, 25),
    width=20,
    angle=45,
    image="python.png",
    style=Styles.Primary.patch(image_border_width=1),
)

save()
