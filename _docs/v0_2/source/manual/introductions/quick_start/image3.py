from drawlib.apis import *

line(
    (10, 10),
    (90, 90),
    style=LineStyle(width=5, color=Colors.Red, style="dashed"),
)
circle(
    (25, 75),
    radius=20,
    style=ShapeStyle(lwidth=3, lcolor=Colors.Black, fcolor=Colors140.Pink),
    text="Circle",
    textstyle=ShapeTextStyle(size=32, color=Colors.White, font=FontSerif.COURIER_BOLD),
)
circle(
    (25, 75),
    radius=13,
    style=ShapeStyle(lwidth=10, lcolor=Colors.White, fcolor=Colors.Transparent),
)

image(
    (70, 30),
    width=30,
    image=Dimage("python.png").sepia(),
    angle=45,
    style=ImageStyle(lwidth=2, lcolor=Colors.Green),
)

text(
    (85, 15),
    text="こんにちは drawlib",
    angle=45,
    style=TextStyle(
        color=Colors140.RoyalBlue,
        size=18,
        font=FontFile("MPLUS1p-Regular.ttf"),
        bglcolor=Colors.Green,
    ),
)

save()
