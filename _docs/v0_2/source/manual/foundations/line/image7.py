from drawlib.apis import *

config(width=100, height=50)

circle((10, 40), radius=5)
lines_bezier(
    (20, 40),
    path_points=[
        (75, 40),
        ((90, 40), (90, 25)),
        (90, 20),
    ],
    arrowhead="->",
)
circle((90, 10), radius=5)

# bezier1 help line
line(xy1=(75, 40), xy2=(90, 40), style=LineStyle(style="dashed", color=Colors.Red))
line(xy1=(90, 40), xy2=(90, 25), style=LineStyle(style="dashed", color=Colors.Red))
circle(xy=(75, 40), radius=0.5, style=ShapeStyle(fcolor=Colors.White, lcolor=Colors.Red))
circle(xy=(90, 40), radius=0.5, style=ShapeStyle(fcolor=Colors.White, lcolor=Colors.Red))
circle(xy=(90, 25), radius=0.5, style=ShapeStyle(fcolor=Colors.White, lcolor=Colors.Red))

save()
