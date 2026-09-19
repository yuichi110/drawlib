from drawlib.apis import *

dtheme.change_default_fonts(FontRoboto.MONO_LIGHT, FontRoboto.MONO_REGULAR, FontRoboto.MONO_BOLD)
config(width=100, height=100, grid_only=True)

x1 = 15
x2 = 35
x3 = 75

arrow((x1, 20), (x1, 70), tail_width=5, head_width=10, head_length=10)
text((x1, 15), "arrow()", size=24)
arrow_polyline(
    [(x2, 30), (x2 - 5, 45), (x2 + 5, 60), (x2, 80)],
    tail_width=5,
    head_width=10,
    head_length=10,
    head="<->",
    r=5,
)
text((x2, 85), "arrow_polyline()", size=24)

arrow_l((x3, 20), 30, 20, tail_width=5, head_width=10, head_length=10)
text((x3, 20), "arrow_l()", size=24)

arrow_u((x3, 50), 30, 20, tail_width=5, head_width=10, head_length=10, head="<->", r=5)
text((x3, 55), "arrow_u()", size=24)

arrow_arc(
    (x3, 70),
    width=30,
    height=20,
    tail_width=5,
    head_width=10,
    head_angle=30,
    angle_start=0,
    angle_end=180,
)
text((x3, 90), "arrow_arc()", size=24)

save()
