from drawlib.apis import *

width = 100
height = 50
config(width=width, height=height)

x = width / 7
y = height / 2
icon_phosphor.airplane_taxiing(xy=(x, y), width=10, style=IconStyle(color=Colors.Red))
icon_phosphor.airplane_takeoff(xy=(x * 2, y), width=10, style=IconStyle(style="thin"))
icon_phosphor.airplane_in_flight(xy=(x * 3, y), width=10, style=IconStyle(style="bold"))
icon_phosphor.airplane_tilt(xy=(x * 4, y), width=10, style=IconStyle("fill"))
icon_phosphor.airplane(xy=(x * 5, y), width=10, style=IconStyle(halign="left", valign="bottom"))
circle(xy=(x * 5, y), radius=0.5, style=ShapeStyle(fcolor=Colors.Red, lcolor=Colors.Red))
text(xy=(x * 5 + 5, y - 10), text="align left,bottom")

save()
