from drawlib.apis import *

config(width=100, height=50, grid=True)

line((20, 7), (80, 7))
line(
    (20, 16),
    (80, 16),
    style=LineStyle(style="dashed", width=5, color=Colors.Red),
)
line((20, 25), (80, 25), arrowhead="->")
line((20, 34), (80, 34), arrowhead="<->")
line((20, 43), (80, 43), arrowhead="<-", style=LineStyle(ahscale=50, style="dashdot", ahfill=True))

save()
