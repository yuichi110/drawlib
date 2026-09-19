from drawlib.apis import *

config(width=100, height=50, grid=True)

p1 = dsart.Pyramid()
p1.add(text="A")
p1.add(text="B")
p1.add(text="C")
p1.draw((5, 5), width=40, height=40, margin=3)

p1 = dsart.Pyramid(default_style="solid", default_textangle=270)
p1.add(text="A")
p1.add(text="B", style="red_flat", textstyle="white")
p1.add(text="C")
p1.draw((55, 5), width=40, height=40, margin=3, align="left")

save()
