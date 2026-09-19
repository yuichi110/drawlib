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
    style=ShapeStyle(lwidth=0, fcolor=Colors.Blue),
    text="Hello Drawlib!",
    textstyle=ShapeTextStyle(size=32, color=Colors.White),
)
save()
