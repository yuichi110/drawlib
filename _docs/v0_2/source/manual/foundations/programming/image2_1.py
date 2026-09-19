from drawlib.apis import *

width = 100
height = 100
config(width=width, height=height, grid_only=True)

num_items = 3
margin_x = width / (num_items + 1)
y = height / 2

# center center align
text((margin_x, y), "Drawlib", style=TextStyle(size=24))
icon_phosphor.heart((margin_x * 2, y), width=10)
circle((margin_x * 3, y), radius=5)

save()
