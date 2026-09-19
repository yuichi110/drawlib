from drawlib.apis import *

x1 = 10


def main():
    config(width=100, height=60)
    dtheme.apply_official_theme("essentials")
    dtheme.iconstyles.merge(IconStyle(style="thin"))
    dtheme.textstyles.merge(TextStyle(size=24))
    draw_icon()
    draw_image()
    draw_line()
    draw_shape()
    draw_text()
    save()


def draw_icon():
    y = 52
    w = 8
    text((x1, y), "Icon")
    icon_phosphor.airplane_taxiing((30, y), width=w)
    icon_phosphor.airplane_takeoff(xy=(40, y), width=w)
    icon_phosphor.airplane_in_flight(xy=(50, y), width=w, style=IconStyle(color=Colors140.Red))
    icon_phosphor.airplane_tilt(xy=(60, y), width=w)
    icon_phosphor.airplane(xy=(70, y), width=w, angle=270)
    icon_phosphor.airplane_landing(xy=(80, y), width=w)
    icon_phosphor.airplane_taxiing((90, y), width=w, style=IconStyle(style="fill", color=Colors140.Red))


def draw_image():
    y = 41
    w = 7
    text((x1, y), "Image")
    image((30, y), w, image="linux.png")
    image((40, y), w, image="linux.png", style=ImageStyle(lwidth=1))
    image((50, y), w, image="linux.png", style=ImageStyle(fcolor=Colors.Red))
    image((60, y), w, image="linux.png", angle=315)
    dimg = Dimage("linux.png")
    image((70, y), w, image=dimg.flip().sepia())
    image((80, y), w, image=dimg.mosaic(24))
    image((90, y), w, image=dimg.brightness(0.5).mirror())


def draw_line():
    y = 29
    text((x1, y), "Line")
    line((30, y - 4), (30, y + 4))
    line((40, y - 4), (40, y + 4), arrowhead="->")
    line((50, y - 4), (50, y + 4), style=LineStyle(style="dashed", color=Colors.Red))
    line((60, y - 4), (60, y + 4), arrowhead="<->", style=LineStyle(color=Colors.Red, ahfill=True))
    line_curved((69, y - 4), (69, y + 4), bend=-0.3)
    line_curved((71, y - 4), (71, y + 4), bend=0.3)
    lines(
        [(77, y - 4), (83, y - 2), (77, y), (83, y + 2), (77, y + 4)],
        style=LineStyle(style="dotted", color=Colors.Red),
    )
    lines_curved([(87, y - 4), (87, y + 4), (93, y + 4), (93, y - 4)], r=2, arrowhead="->")


def draw_shape():
    y = 17
    w = 8
    text((x1, y), "Shape")
    circle((30, y), radius=w / 2)
    ellipse((40, y), width=w / 2, height=w, style="red_dashed")
    rectangle((50, y), width=7, height=7, text="rect", textstyle="white")
    rectangle((60, y), width=7, height=4, angle=315, r=2, style="red_solid")
    star((70, y), 5, 4, 2)
    arrow((80, y - 4), (80, y + 4), tail_width=3, head_width=6, head_length=3, style="red_flat")
    arrow((90, y - 4), (90, y + 4), tail_width=2, head_width=5, head_length=3, head="<->")


def draw_text():
    y = 7
    text((x1, y), "Text")
    text((35, y), "Hello Drawlib!", style=TextStyle(font=FontSansSerif.RALEWAYS_REGULAR, size=18))
    text(
        (60, y),
        "Hello\nDrawlib!",
        style=TextStyle(font=FontSerif.COURIER_REGULAR, size=28, color=Colors.Red),
    )
    text(
        (85, y),
        "こんにちは Drawlib!",
        style=TextStyle(
            font=FontJapanese.MPLUS1P_REGULAR,
            size=16,
            bgfcolor=Colors.Black,
            bglwidth=0,
            color=Colors.White,
        ),
    )


main()
