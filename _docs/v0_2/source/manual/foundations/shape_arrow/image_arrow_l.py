from drawlib.apis import *

dtheme.apply_official_theme("essentials")
dtheme.change_default_fonts(FontRoboto.MONO_LIGHT, FontRoboto.MONO_REGULAR, FontRoboto.MONO_BOLD)

config(width=100, height=50, grid=True)
arrow_l(
    xy=(15, 25),
    width=20,
    height=30,
    tail_width=3,
    head_width=6,
    head_length=3,
)

arrow_l(
    xy=(40, 25),
    width=20,
    height=30,
    tail_width=3,
    head_width=6,
    head_length=3,
    style="white",
)
lines([(30, 40), (30, 10), (50, 10)], style="dashed")
for dot in [(30, 40), (30, 10), (50, 10)]:
    circle(dot, radius=0.7, style="red_flat")

circle((40, 25), radius=0.7, style="blue_flat")
line((30, 25), (50, 25), style="blue_dashed", arrowhead="<->")
text((47.5, 27.5), "width", style="blue")
line((40, 40), (40, 10), style="blue_dashed", arrowhead="<->")
text((40, 42.5), "height", style="blue")

arrow_l(
    xy=(75, 10),
    width=10,
    height=15,
    tail_width=3,
    head_width=6,
    head_length=3,
    angle=90,
    head="<->",
)
text((70, 10), "angle=90")

arrow_l(
    xy=(75, 25),
    width=10,
    height=15,
    tail_width=3,
    head_width=6,
    head_length=3,
    angle=180,
    head="<-",
)
text((70, 25), "angle=180")

arrow_l(
    xy=(75, 40),
    width=10,
    height=15,
    tail_width=3,
    head_width=6,
    head_length=3,
    angle=270,
    head="<-",
)
text((80, 40), "angle=270")

save()
