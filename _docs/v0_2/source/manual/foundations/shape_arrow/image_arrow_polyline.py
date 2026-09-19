from drawlib.apis import *

dtheme.apply_official_theme("essentials")
dtheme.change_default_fonts(FontRoboto.MONO_LIGHT, FontRoboto.MONO_REGULAR, FontRoboto.MONO_BOLD)
config(width=100, height=50, grid=True)
arrow_polyline(
    [(25, 5), (15, 25), (25, 45)],
    tail_width=5,
    head_width=10,
    head_length=5,
)

arrow_polyline(
    [(50, 5), (40, 25), (50, 45)],
    tail_width=5,
    head_width=10,
    head_length=5,
)
lines([(50, 5), (40, 25), (50, 45)], style="white_dashed")
for dot in [(50, 5), (40, 25), (50, 45)]:
    circle(dot, radius=1, style="red_flat")

arrow_polyline(
    [(75, 5), (85, 25), (75, 45)],
    tail_width=5,
    head_width=10,
    head_length=5,
    r=5,
    head="<->",
)
lines_curved([(75, 5), (85, 25), (75, 45)], r=5, style="white_dashed")
for dot in [(75, 5), (85, 25), (75, 45)]:
    circle(dot, radius=1, style="red_flat")

save()
