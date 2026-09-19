from drawlib.apis import *

config(width=200, height=200, grid_only=True)
circle(
    (50, 50),
    radius=30,
    text="(50,50)",
    textstyle=ShapeTextStyle(size=36),
)
save()
