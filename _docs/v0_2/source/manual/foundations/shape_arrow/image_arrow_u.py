from drawlib.apis import *

dtheme.apply_official_theme("essentials")
dtheme.change_default_fonts(FontRoboto.MONO_LIGHT, FontRoboto.MONO_REGULAR, FontRoboto.MONO_BOLD)
config(width=100, height=50, grid=True)

arrow_u(
    xy=(15, 25),
    width=15,
    height=30,
    tail_width=3,
    head_width=6,
    head_length=3,
)

arrow_u(
    xy=(40, 25),
    width=15,
    height=30,
    tail_width=3,
    head_width=6,
    head_length=3,
    style="white",
)
lines([(32.5, 40), (32.5, 10), (47.5, 10), (47.5, 40)], style="dashed")
for dot in [(32.5, 40), (32.5, 10), (47.5, 10), (47.5, 40)]:
    circle(dot, radius=0.7, style="red_flat")

circle((40, 25), radius=1, style="blue_flat")
line((32.5, 25), (47.5, 25), style="blue_dashed", arrowhead="<->")
text((45, 27.5), "width", style="blue")
line((40, 40), (40, 10), style="blue_dashed", arrowhead="<->")
text((40, 42.5), "height", style="blue")

arrow_u(
    xy=(75, 10),
    width=8,
    height=12,
    tail_width=3,
    head_width=6,
    head_length=3,
    angle=90,
    head="<->",
)
text((70, 10), "angle=90")

arrow_u(
    xy=(75, 25),
    width=8,
    height=12,
    tail_width=3,
    head_width=6,
    head_length=3,
    angle=180,
    head="<-",
)
text((70, 25), "angle=180")

arrow_u(
    xy=(75, 40),
    width=8,
    height=12,
    tail_width=3,
    head_width=6,
    head_length=3,
    angle=270,
    head="<-",
)
text((80, 40), "angle=270")

save()
