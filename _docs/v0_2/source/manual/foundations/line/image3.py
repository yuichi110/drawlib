from drawlib.apis import *

config(width=100, height=50)
line_bezier1(xy1=(10, 10), cp=(10, 40), xy2=(40, 40))
line(xy1=(10, 10), xy2=(10, 40), style=LineStyle(style="dashed", color=Colors.Red))
line(xy1=(10, 40), xy2=(40, 40), style=LineStyle(style="dashed", color=Colors.Red))
circle(xy=(10, 10), radius=0.5, style=ShapeStyle(fcolor=Colors.White, lcolor=Colors.Red))
circle(xy=(10, 40), radius=0.5, style=ShapeStyle(fcolor=Colors.White, lcolor=Colors.Red))
circle(xy=(40, 40), radius=0.5, style=ShapeStyle(fcolor=Colors.White, lcolor=Colors.Red))

line_bezier1(xy1=(60, 40), cp=(90, 40), xy2=(90, 10))
line(xy1=(60, 40), xy2=(90, 40), style=LineStyle(style="dashed", color=Colors.Red))
line(xy1=(90, 40), xy2=(90, 10), style=LineStyle(style="dashed", color=Colors.Red))
circle(xy=(60, 40), radius=0.5, style=ShapeStyle(fcolor=Colors.White, lcolor=Colors.Red))
circle(xy=(90, 40), radius=0.5, style=ShapeStyle(fcolor=Colors.White, lcolor=Colors.Red))
circle(xy=(90, 10), radius=0.5, style=ShapeStyle(fcolor=Colors.White, lcolor=Colors.Red))

save()
