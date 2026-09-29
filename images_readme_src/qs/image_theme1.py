from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.shapes import circle
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=100, height=50, background_color=Colors.canvas)
x1 = 12
x2 = 34
x3 = 62
x4 = 88
line_y = 40
line_length = 7
circle_y = 25
text_y = 10

# blue style
line((x1 - line_length, line_y), (x1 + line_length, line_y), style=Styles.Blue)
circle((x1, circle_y), radius=8, style=Styles.Blue)
text((x1, text_y), text="Styles.Blue", style=Styles.Blue)

# blue solid style
line((x2 - line_length, line_y), (x2 + line_length, line_y), style=Styles.BlueSolid)
circle((x2, circle_y), radius=8, style=Styles.BlueSolid)
text((x2, text_y), text="Styles.BlueSolid", style=Styles.Blue)

# green dashed style
line((x3 - line_length, line_y), (x3 + line_length, line_y), style=Styles.GreenDashed)
circle((x3, circle_y), radius=8, style=Styles.GreenDashed)
text((x3, text_y), text="Styles.GreenDashed", style=Styles.GreenBold)

# red flat style
line((x4 - line_length, line_y), (x4 + line_length, line_y), style=Styles.Red)
circle((x4, circle_y), radius=8, style=Styles.RedFlat)
text((x4, text_y), text="Styles.RedFlat", style=Styles.Red)

save()
