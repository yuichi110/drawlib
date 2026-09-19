from drawlib.apis import *

config(width=1920, height=1080, dpi=192, grid_only=True)
circle(
    (960, 540),
    radius=300,
    text="(960,540)",
    textstyle=ShapeTextStyle(size=36),
)
save()
