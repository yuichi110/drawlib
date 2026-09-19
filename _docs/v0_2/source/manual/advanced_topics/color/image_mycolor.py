from drawlib.apis import *


# Please define color at styling codes normally.
class ColorsGoogle(ColorsBase):
    # From Official Google Color Palette
    # At Partner Marketing Hub
    Blue = (23, 78, 166)
    Red = (165, 14, 14)
    Orange = (227, 116, 0)
    Green = (32, 33, 36)
    MediumBlue = (66, 103, 210)
    MediumRed = (234, 67, 53)
    Yellow = (251, 188, 4)
    MediumGreen = (52, 168, 83)
    LightBlue = (210, 227, 252)
    LightRed = (250, 210, 207)
    LightYellow = (254, 239, 195)
    LightGreen = (206, 234, 214)
    LightGrey = (241, 243, 244)
    Grey = (154, 160, 166)
    Black = (32, 33, 36)


config(width=100, height=50)
shape_y = 30
circle(
    (15, shape_y),
    radius=10,
    style=ShapeStyle(lwidth=0, fcolor=ColorsGoogle.MediumBlue),
)
triangle(
    (37.5, shape_y),
    width=20,
    height=15,
    style=ShapeStyle(lwidth=0, fcolor=ColorsGoogle.MediumRed),
)
rectangle(
    (62.5, shape_y),
    width=18,
    height=18,
    style=ShapeStyle(lwidth=0, fcolor=ColorsGoogle.Yellow),
)
wedge(
    (85, shape_y),
    radius=10,
    width=5,
    angle_end=270,
    style=ShapeStyle(lwidth=0, fcolor=ColorsGoogle.MediumGreen),
)
text(
    (50, 10),
    "Google Colors",
    style=TextStyle(
        color=ColorsGoogle.Black,
        size=32,
        font=FontRoboto.ROBOTO_REGULAR,
    ),
)
save()
