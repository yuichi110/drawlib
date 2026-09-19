from drawlib.apis import *

width = 100
height = 50
config(width=width, height=height)

file_brand = "fontawesome-free/brands.ttf"
file_regular = "fontawesome-free/regular.ttf"
file_solid = "fontawesome-free/solid.ttf"

google = "\uf1a0"
gmail = "\uf0e0"
google_map = "\uf3c5"
google_drive = "\uf3aa"
google_play = "\uf3ab"
google_pay = "\ue079"

x = width / 7
y = height / 2
icon(xy=(x, y), width=10, code=google, file=file_brand)
icon(xy=(x * 2, y), width=10, code=gmail, file=file_regular)
icon(xy=(x * 3, y), width=10, code=google_map, file=file_solid, angle=270)
text(xy=(x * 3, y - 10), text="angle 270")
icon(
    xy=(x * 4, y),
    width=10,
    code=google_drive,
    file=file_brand,
)
icon(
    xy=(x * 5, y),
    width=10,
    code=google_play,
    file=file_brand,
)


save()
