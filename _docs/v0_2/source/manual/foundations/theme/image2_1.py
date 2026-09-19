from drawlib.apis import *

config(width=100, height=50)
line_y = 40
text_y = 10

# default style
line((13, line_y), (27, line_y))
circle((20, 25), radius=8)
text((20, text_y), text="no style")

# blue style
line((33, line_y), (47, line_y), style="blue")
circle((40, 25), radius=8, style="blue")
text((40, text_y), text='style="blue"', style="blue")

# green style
line((53, line_y), (67, line_y), style="green")
circle((60, 25), radius=8, style="green")
text((60, text_y), text='style="green"', style="green")

# red style
line((73, line_y), (87, line_y), style="red")
circle((80, 25), radius=8, style="red")
text((80, text_y), text='style="red"', style="red")

save()
