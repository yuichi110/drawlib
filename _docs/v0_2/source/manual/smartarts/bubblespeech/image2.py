from drawlib.apis import *

config(width=100, height=50)
dsart.bubblespeech(
    xy=(30, 10),
    width=50,
    height=30,
    tail_edge="left",
    tail_start_ratio=0.2,
    tail_vertex_xy=(10, 25),
    tail_end_ratio=0.6,
    style=ShapeStyle(lwidth=0, fcolor=Colors140.LightGray),
    text="Hello Drawlib!",
    textstyle=ShapeTextStyle(size=32, color=Colors.White),
)

line((30, 10), (30, 40), style=LineStyle(width=2, style="dashed", color=Colors.Blue))
text((30, 45), 'tail_edge = "left"')
circle(xy=(30, 10), radius=1, style=ShapeStyle(lwidth=0, fcolor=Colors.Red))
text((30, 5), "xy = (30, 10)")

line((27, 10), (27, 16), arrowhead="<->")
text((13, 13), "tail_from_ratio = 0.2")

circle(xy=(10, 25), radius=1, style=ShapeStyle(lwidth=0, fcolor=Colors.Red))
text((15, 30), "tail_vertex_xy = (30, 10)")

line((33, 10), (33, 28), arrowhead="<->")
text((45, 13), "tail_to_ratio = 0.6")

save()
