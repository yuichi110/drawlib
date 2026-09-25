from drawlib.canvas import config, save
from drawlib.lines import line
from drawlib.preset_styles import get_styles
from drawlib.shapes import circle
from drawlib.text import text

config(width=100, height=50)
styles = get_styles()

x1 = 12
x2 = 34
x3 = 62
x4 = 88
line_y = 40
line_length = 7
circle_y = 25
text_y = 10

# blue style
line((x1 - line_length, line_y), (x1 + line_length, line_y), style=styles.blue)
circle((x1, circle_y), radius=8, style=styles.blue)
text((x1, text_y), text="styles.blue", style=styles.blue)

# blue solid style
line((x2 - line_length, line_y), (x2 + line_length, line_y), style=styles.blue_solid)
circle((x2, circle_y), radius=8, style=styles.blue_solid)
text((x2, text_y), text="styles.blue_solid", style=styles.blue)

# green dashed style
line((x3 - line_length, line_y), (x3 + line_length, line_y), style=styles.green_dashed)
circle((x3, circle_y), radius=8, style=styles.green_dashed)
text((x3, text_y), text="styles.green_dashed", style=styles.green_bold)

# red flat style
line((x4 - line_length, line_y), (x4 + line_length, line_y), style=styles.red)
circle((x4, circle_y), radius=8, style=styles.red_flat)
text((x4, text_y), text="styles.red_flat", style=styles.red)

save()

