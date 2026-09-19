from drawlib.apis import *

config(width=100, height=50)

points = [
    ((10, 20), (30, 20)),
    (60, 10),
    ((60, 40), (90, 40), (90, 10)),
]
lines_bezier(xy=(10, 40), path_points=points)

# bezier1 help line
line(xy1=(10, 40), xy2=(10, 20), style=LineStyle(style="dashed", color=Colors.Red))
line(xy1=(10, 20), xy2=(30, 20), style=LineStyle(style="dashed", color=Colors.Red))
circle(xy=(10, 40), radius=0.5, style=ShapeStyle(fcolor=Colors.White, lcolor=Colors.Red))
circle(xy=(10, 20), radius=0.5, style=ShapeStyle(fcolor=Colors.White, lcolor=Colors.Red))
circle(xy=(30, 20), radius=0.5, style=ShapeStyle(fcolor=Colors.White, lcolor=Colors.Red))

# bezier2 help line
line(xy1=(60, 10), xy2=(60, 40), style=LineStyle(style="dashed", color=Colors.Red))
line(xy1=(60, 40), xy2=(90, 40), style=LineStyle(style="dashed", color=Colors.Red))
line(xy1=(90, 40), xy2=(90, 10), style=LineStyle(style="dashed", color=Colors.Red))
circle(xy=(60, 10), radius=0.5, style=ShapeStyle(fcolor=Colors.White, lcolor=Colors.Red))
circle(xy=(60, 40), radius=0.5, style=ShapeStyle(fcolor=Colors.White, lcolor=Colors.Red))
circle(xy=(90, 40), radius=0.5, style=ShapeStyle(fcolor=Colors.White, lcolor=Colors.Red))
circle(xy=(90, 10), radius=0.5, style=ShapeStyle(fcolor=Colors.White, lcolor=Colors.Red))

save()
