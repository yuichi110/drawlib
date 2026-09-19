from drawlib.apis import *

config(width=100, height=50)
line_y = 40
text_y = 10

# default style
line((8, line_y), (22, line_y), style="blue")
circle((15, 25), radius=8, style="blue")
text((15, text_y), text='style="blue"', style="blue")

# blue style
line((31, line_y), (45, line_y), style="blue_solid")
circle((38, 25), radius=8, style="blue_solid")
text((38, text_y), text='style="blue_solid"')

# green style
line((55, line_y), (69, line_y), style="blue_bold")
circle((62, 25), radius=8, style="blue_bold")
text((62, text_y), text='style="blue_bold"', style="blue_bold")

# pink style
line((78, line_y), (92, line_y), style="dashed")
circle((85, 25), radius=8, style="dashed")
text((85, text_y), text='style="dashed"')

save()
