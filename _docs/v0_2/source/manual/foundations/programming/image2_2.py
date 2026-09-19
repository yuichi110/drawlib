from drawlib.apis import *

width = 100
height = 50  # <= CHANGED FROM 100 !!
config(width=width, height=height, grid_only=True)

num_items = 4  # <= CHANGED FROM 3!!
margin_x = width / (num_items + 1)
y = height / 2

# center center align
text((margin_x, y), "Drawlib", style=TextStyle(size=24))
icon_phosphor.heart((margin_x * 2, y), width=10)
circle((margin_x * 3, y), radius=5)
rectangle((margin_x * 4, y), width=10, height=10)

save()
