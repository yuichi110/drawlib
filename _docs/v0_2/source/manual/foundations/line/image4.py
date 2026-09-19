from drawlib.apis import *

config(width=100, height=50)
line_bezier2(xy1=(10, 10), cp1=(10, 40), cp2=(40, 40), xy2=(40, 10))
line(xy1=(10, 10), xy2=(10, 40), style=LineStyle(style="dashed", color=Colors.Red))
line(xy1=(10, 40), xy2=(40, 40), style=LineStyle(style="dashed", color=Colors.Red))
line(xy1=(40, 40), xy2=(40, 10), style=LineStyle(style="dashed", color=Colors.Red))
circle(xy=(10, 10), radius=0.5, style=ShapeStyle(fcolor=Colors.White, lcolor=Colors.Red))
circle(xy=(10, 40), radius=0.5, style=ShapeStyle(fcolor=Colors.White, lcolor=Colors.Red))
circle(xy=(40, 40), radius=0.5, style=ShapeStyle(fcolor=Colors.White, lcolor=Colors.Red))
circle(xy=(40, 10), radius=0.5, style=ShapeStyle(fcolor=Colors.White, lcolor=Colors.Red))

line_bezier2(xy1=(60, 40), cp1=(60, 10), cp2=(90, 10), xy2=(90, 40))
line(xy1=(60, 40), xy2=(60, 10), style=LineStyle(style="dashed", color=Colors.Red))
line(xy1=(60, 10), xy2=(90, 10), style=LineStyle(style="dashed", color=Colors.Red))
line(xy1=(90, 10), xy2=(90, 40), style=LineStyle(style="dashed", color=Colors.Red))
circle(xy=(60, 40), radius=0.5, style=ShapeStyle(fcolor=Colors.White, lcolor=Colors.Red))
circle(xy=(60, 10), radius=0.5, style=ShapeStyle(fcolor=Colors.White, lcolor=Colors.Red))
circle(xy=(90, 10), radius=0.5, style=ShapeStyle(fcolor=Colors.White, lcolor=Colors.Red))
circle(xy=(90, 40), radius=0.5, style=ShapeStyle(fcolor=Colors.White, lcolor=Colors.Red))

save()
