from drawlib.canvas import config, save
from drawlib.images import image
from drawlib.lines import line
from drawlib.shapes import circle
from drawlib.text import text

config(width=100, height=100)

line((10, 10), (90, 90))
circle((25, 75), radius=20)
image((75, 25), width=30, image="python.png")
text((75, 5), "Hello drawlib!")

save()
