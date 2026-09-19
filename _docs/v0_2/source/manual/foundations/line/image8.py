from drawlib.apis import *

config(width=100, height=50)

circle((10, 40), radius=5)
lines(
    [(20, 40), (30, 40), (30, 10), (90, 40), (90, 22)],
    style=LineStyle(color=Colors.Red, style="dashed", width=1.5),
)
lines_curved(
    [(20, 40), (30, 40), (30, 10), (90, 40), (90, 20)],
    r=8,
    width=2.5,
    arrowhead="->",
)
circle((90, 10), radius=5)
save()
