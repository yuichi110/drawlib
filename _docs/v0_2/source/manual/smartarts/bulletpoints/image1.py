from drawlib.apis import *

config(width=100, height=50, grid=True)


def center():
    bp = dsart.BulletPoints(vertical_margin=4, indent_width=4)
    bp.add("Type of Drawlib shapes")
    bp.set_indent(1)
    bp.add("Circle Like Shapes")
    bp.set_indent(2)
    bp.add("Circle")
    bp.add("Start etc.")
    bp.set_indent(1)
    bp.add("Rectangle Like Shapes")
    bp.set_indent(2)
    bp.add("Rectangle")
    bp.add("Ellipse etc.")
    bp.draw(xy=(42, 40))


def left():
    x1 = 17
    x2 = 27
    x3 = 37

    text((x1, 40), "Indent Level 0", style="light")
    line((x2, 40), (x3, 40), style="dashed_light", arrowhead="->")
    text((x1, 36), "Indent Level 1", style="light")
    line((x2, 36), (x3, 36), style="dashed_light", arrowhead="->")
    text((x1, 32), "Indent Level 2", style="light")
    line((x2, 32), (x3, 32), style="dashed_light", arrowhead="->")

    line((x2, 21), (42, 24), style="dashed_light", arrowhead="->")
    line((x2, 19), (46, 16), style="dashed_light", arrowhead="->")
    text((x1, 20), "indent_style", style="light")


def others():
    line((70, 40), (70, 36), style="dashed_light", arrowhead="<->")
    text((82, 38), "vertical_margin", style="light")
    line((42, 12), (46, 12), style="dashed_light", arrowhead="<->")
    text((44, 9), "indent_width", style="light")


center()
left()
others()
save()
