from drawlib.apis import *

config(width=100, height=100, grid_only=True)

x1 = 20
x2 = 50
x3 = 80
y1 = 20
y2 = 50
y3 = 80

circle((x1, y1), radius=5)
rectangle((x1, y2), width=20, height=10, angle=45)
star((x1, y3), 5, 15, 6, angle=45)

image((x2, y1), width=20, image="python.png", angle=315)
icon_phosphor.heart((x2, y2), 10, angle=315)
text((x2, y3), "Drawlib", angle=315, style=TextStyle(size=24))

chevron((x3, y1), 35, 10, corner_angle=45, angle=45)
parallelogram((x3, y2), 15, 10, corner_angle=60, angle=45)
regularpolygon((x3, y3), 5, num_vertex=6, angle=45)

for x in [x1, x2, x3]:
    for y in [y1, y2, y3]:
        circle((x, y), 1, style=ShapeStyle(fcolor=Colors.Red, lcolor=Colors.Red))

save()
