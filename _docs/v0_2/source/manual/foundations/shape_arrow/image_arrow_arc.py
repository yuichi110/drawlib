from drawlib.apis import *

dtheme.apply_official_theme("essentials")
dtheme.change_default_fonts(FontRoboto.MONO_LIGHT, FontRoboto.MONO_REGULAR, FontRoboto.MONO_BOLD)
config(width=100, height=50, grid=True)

arrow_arc(
    xy=(15, 25),
    width=15,
    height=15,
    tail_width=3,
    head_width=6,
    head_angle=20,
    angle_start=20,
    angle_end=340,
)

arrow_arc(
    xy=(40, 25),
    width=15,
    height=15,
    tail_width=3,
    head_width=6,
    head_angle=20,
    angle_start=20,
    angle_end=340,
    style="white",
)
arc(
    xy=(40, 25),
    width=15,
    height=15,
    # angle_start=20,
    # angle_end=340,
    style="dashed",
)
circle((40, 25), radius=1, style="blue_flat")
line((32.5, 25), (47.5, 25), style="blue_dashed", arrowhead="<->")
text((53, 25), "width", style="blue")
line((40, 17.5), (40, 32.5), style="blue_dashed", arrowhead="<->")
text((40, 37.5), "height", style="blue")

for dot in [(47, 27.5), (47, 22.5)]:
    circle(dot, radius=0.7, style="red_flat")

text((57.5, 29), "angle_start", style="red")
text((57.5, 21), "angle_end", style="red")

text((32.5, 7.5), 'The arrow is drawn counterclockwise.\nTo draw a clockwise arrow, specify head="<-".')

arrow_arc(
    xy=(80, 12.5),
    width=25,
    height=15,
    tail_width=3,
    head_width=6,
    head_angle=20,
    angle_start=225,
    angle_end=135,
    head="<->",
)
text((72.5, 12.5), "width=25, height=15")

arc(xy=(80, 37.5), width=25, height=15, angle=45, style="dashed")
arrow_arc(
    xy=(80, 37.5),
    width=25,
    height=15,
    tail_width=3,
    head_width=6,
    head_angle=20,
    angle_start=90,
    angle_end=270,
    angle=45,
    head="<-",
)
text((82.5, 40), 'angle=45\nhead="<-"')

save()
