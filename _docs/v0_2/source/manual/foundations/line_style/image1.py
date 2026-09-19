from drawlib.apis import *

config(width=100, height=40)

text((10, 5), "no style")
line((20, 5), (40, 5))
text((10, 15), "width: 5")
line((20, 15), (40, 15), style=LineStyle(width=5))
text((10, 25), "color: Red")
line((20, 25), (40, 25), style=LineStyle(color=Colors.Red))
text((10, 35), "alpha: 0.2")
line((20, 35), (40, 35), style=LineStyle(alpha=0.2))

text((60, 5), "style: solid\n(default)")
line((70, 5), (90, 5), style=LineStyle(style="solid"))
text((60, 15), "style: dashed")
line((70, 15), (90, 15), style=LineStyle(style="dashed"))
text((60, 25), "style: dotted")
line((70, 25), (90, 25), style=LineStyle(style="dotted"))
text((60, 35), "style: dashdot")
line((70, 35), (90, 35), style=LineStyle(style="dashdot"))

save()
