from drawlib.apis import *

config(width=100, height=50, dpi=200, background_color=Colors.Gray)
tstyle = TextStyle(color=Colors.White)

# invert
image((20, 25), 20, Dimage("linux.png").invert())
text((20, 10), "invert()", style=tstyle)

# brightness
image(
    (50, 25),
    20,
    Dimage("linux.png").colorize(
        from_black_to=Colors.Blue,
        from_white_to=Colors.Red,
    ),
)
text((50, 10), "colorize()", style=tstyle)

# invert (rectangle is just background)
image(
    (80, 25),
    20,
    Dimage("linux.png").colorize(
        from_black_to=Colors.Blue,
        from_white_to=Colors.Red,
        from_mid_to=Colors.Green,
    ),
)
text((80, 10), "colorize()", style=tstyle)

save()
