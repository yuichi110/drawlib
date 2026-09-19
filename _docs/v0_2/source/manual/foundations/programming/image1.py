from drawlib.apis import *

config(width=100, height=100, grid_only=True)

# alignment: horizontally left, vertically bottom
text(
    (19, 73),
    "Drawlib",
    style=TextStyle(size=24, halign="left", valign="bottom"),
)
icon_phosphor.heart(
    (45, 70),
    width=10,
    style=IconStyle(halign="left", valign="bottom"),
)
circle(
    (70, 70),
    radius=5,
    style=ShapeStyle(halign="left", valign="bottom"),
)

# alignment: horizontally center, vertically center
text(
    (25, 25),
    "Drawlib",
    style=TextStyle(size=24, halign="center", valign="center"),
)
icon_phosphor.heart(
    (50, 25),
    width=10,
    style=IconStyle(halign="center", valign="center"),
)
circle(
    (75, 25),
    radius=5,
    style=ShapeStyle(halign="center", valign="center"),
)

save()
