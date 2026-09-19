from drawlib.apis import *

config(width=100, height=40)

text((12, 5), "no style")
line((25, 5), (40, 5))
text((12, 15), 'style="red"')
line((25, 15), (40, 15), style="red")
text((12, 25), 'style="red_solid"')
line((25, 25), (40, 25), style="red_solid")
text((12, 35), 'style="red_dashed"')
line((25, 35), (40, 35), style="red_dashed")

text((60, 5), 'style="red_solid_light"')
line((75, 5), (90, 5), arrowhead="->", style="red_solid_light")
text((60, 15), 'style="red_solid_bold"')
line((75, 15), (90, 15), arrowhead="->", style="red_solid_bold")
text((60, 25), 'style="dashed"')
line((75, 25), (90, 25), arrowhead="->", style="dashed")
text((60, 35), 'style="bold"')
line((75, 35), (90, 35), arrowhead="->", style="bold")

save()
