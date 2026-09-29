from drawlib.canvas import save, setup
from drawlib.images import Dimage, image
from drawlib.styles import Colors

setup(width=100, height=50, grid=True, color=Colors.canvas)

image(xy=(25, 25), width=20, image="../_assets/python.png")

dimg = Dimage("../_assets/python.png").mirror().sepia()
image(xy=(75, 25), width=20, image=dimg)

save()
