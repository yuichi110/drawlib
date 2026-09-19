from drawlib.apis import *

config(width=100, height=50)
x1 = 12
x2 = 34
x3 = 62
x4 = 88
line_y = 40
line_length = 7
circle_y = 25
text_y = 10

# blue style
line((x1 - line_length, line_y), (x1 + line_length, line_y), style="blue")
circle((x1, circle_y), radius=8, style="blue")
text((x1, text_y), text="blue", style="blue")

# blue solid style
line((x2 - line_length, line_y), (x2 + line_length, line_y), style="blue_solid")
circle((x2, circle_y), radius=8, style="blue_solid")
text((x2, text_y), text='style="blue_solid"', style="blue")

# green dashed style
line((x3 - line_length, line_y), (x3 + line_length, line_y), style="green_dashed_bold")
circle((x3, circle_y), radius=8, style="green_dashed_bold")
text((x3, text_y), text='style="green_dashed_bold"', style="green_bold")

# red flat style
line((x4 - line_length, line_y), (x4 + line_length, line_y), style="red")
circle((x4, circle_y), radius=8, style="red_flat")
text((x4, text_y), text='style="red_flat"', style="red")

save()
