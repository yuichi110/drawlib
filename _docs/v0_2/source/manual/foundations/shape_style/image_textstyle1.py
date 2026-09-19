from drawlib.apis import *

config(width=150, height=50)

# left
rectangle(
    xy=(25, 25),
    width=40,
    height=20,
    text="rectangle()",
    textstyle=ShapeTextStyle(
        color=Colors.White,
        size=24,
        font=FontSerif.COURIER_BOLD,
    ),
)


# center
rectangle(
    xy=(75, 25),
    width=40,
    height=20,
    angle=45,
    text="rectangle()",
    textstyle=ShapeTextStyle(
        color=Colors.White,
        size=24,
        font=FontSansSerif.RALEWAYS_REGULAR,
    ),
)


# right
rectangle(
    xy=(125, 25),
    width=40,
    height=20,
    angle=45,
    text="rectangle()",
    textstyle=ShapeTextStyle(
        color=Colors.White,
        angle=0,
        xy_shift=(-12, -3),
    ),
)

save()
