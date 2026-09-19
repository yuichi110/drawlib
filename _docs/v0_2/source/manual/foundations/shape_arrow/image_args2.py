from drawlib.apis import *

dtheme.change_default_font_size(24)
dtheme.change_default_fonts(FontRoboto.MONO_LIGHT, FontRoboto.MONO_REGULAR, FontRoboto.MONO_BOLD)
config(width=100, height=50)

arrow((10, 25), (30, 25), tail_width=5, head_width=10, head_length=7, head="->")
text((20, 15), 'head="->"')

arrow((40, 25), (60, 25), tail_width=5, head_width=10, head_length=7, head="<-")
text((50, 15), 'head="<-"')

arrow((70, 25), (90, 25), tail_width=5, head_width=10, head_length=7, head="<->")
text((80, 15), 'head="<->"')

save()
