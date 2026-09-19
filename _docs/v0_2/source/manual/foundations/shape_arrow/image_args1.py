from drawlib.apis import *

dtheme.change_default_font_size(24)
dtheme.change_default_fonts(FontRoboto.MONO_LIGHT, FontRoboto.MONO_REGULAR, FontRoboto.MONO_BOLD)
config(width=100, height=50)
arrow((20, 25), (80, 25), tail_width=10, head_width=20, head_length=10)

circle((20, 25), radius=1, style="red")
text((27, 25), "xy1", style="white_bold")
circle((80, 25), radius=1, style="red")
text((73, 25), "xy2", style="white_bold")

line((15, 20), (15, 30), style="dashed", arrowhead="<->")
text((15, 35), "tail_width")

line((85, 15), (85, 35), style="dashed", arrowhead="<->")
text((85, 40), "head_width")

line((70, 10), (80, 10), style="dashed", arrowhead="<->")
text((55, 10), "head_length")

save()
