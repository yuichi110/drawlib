from drawlib.apis import *

config(width=100, height=50, grid_only=True)
text(
    xy=(15, 25),
    text="Hello Drawlib.",
    style=TextStyle(
        color=Colors140.Turquoise,
        size=24,
        halign="left",
        valign="bottom",
        font=FontSerif.MERRIWEATHER_REGULAR,
    ),
)
circle(xy=(15, 25), radius=0.5, style=ShapeStyle(fcolor=Colors.Red, lwidth=0))
text((15, 22), "align: left,bottom")

text(
    xy=(75, 25),
    angle=45,
    text="こんにちは Drawlib.",
    style=TextStyle(
        color=Colors.White,
        bglwidth=2,
        bglcolor=Colors.Red,
        bglstyle="dashed",
        bgfcolor=Colors.Black,
    ),
)
save()
