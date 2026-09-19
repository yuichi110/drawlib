from drawlib.apis import *

config(width=100, height=50)

b1 = dsart.BoxList(default_text_style="white")
b1.extend(["1", "2", "3", "4"])
b1.draw(xy=(10, 35), box_width=8, box_height=6)


b2 = dsart.BoxList(default_box_style="solid", default_text_style="")
b2.extend(["1", "2"])
b2.append("3", box_style="red_solid_bold", text_style="red_bold")
b2.extend(["4", "", ""])
b2.draw(xy=(10, 10), box_width=8, box_height=6)

b3 = dsart.BoxList(default_text_style="white")
b3.extend(["1", "2", "3", "4"])
b3.draw(xy=(75, 10), box_width=8, box_height=6, align="bottom")

save()
