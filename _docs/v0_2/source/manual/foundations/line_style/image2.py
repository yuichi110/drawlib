from drawlib.apis import *

"""
config(width=100, height=50)

text((10, 5), "LineArrowStyle()", style=TextStyle(size=14))
line((20, 5), (40, 5), )
text((10, 13), "width: 5")
line((20, 13), (40, 13), style=LineArrowStyle(lwidth=5))
text((10, 21), "color: Red")
line((20, 21), (40, 21), style=LineArrowStyle(color=Colors.Red))
text((10, 29), "alpha: 0.2")
line((20, 29), (40, 29), style=LineArrowStyle(alpha=0.2))
text((10, 37), "lstyle: dashed")
line((20, 37), (40, 37), style=LineArrowStyle(lstyle="dashed"))
text((10, 45), "hscale: 50\n(default: 20)")
line((20, 45), (40, 45), style=LineArrowStyle(hscale=50))

text((60, 5), "hstyle: ->\n(default)")
line((70, 5), (90, 5), style=LineArrowStyle(hstyle="->"))
text((60, 13), "style: <-")
line((70, 13), (90, 13), style=LineArrowStyle(hstyle="<-"))
text((60, 21), "style: <->")
line((70, 21), (90, 21), style=LineArrowStyle(hstyle="<->"))
text((60, 29), "style: -|>")
line((70, 29), (90, 29), style=LineArrowStyle(hstyle="-|>"))
text((60, 37), "style: <|-")
line((70, 37), (90, 37), style=LineArrowStyle(hstyle="<|-"))
text((60, 45), "style: <|-|>")
line((70, 45), (90, 45), style=LineArrowStyle(hstyle="<|-|>"))

save()
"""
