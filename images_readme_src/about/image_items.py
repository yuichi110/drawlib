# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.canvas import save, setup
from drawlib.fonts import FontJapanese, FontSansSerif, FontSerif
from drawlib.icons import phosphor
from drawlib.images import Dimage, image
from drawlib.lines import line, line_curved, lines, lines_curved
from drawlib.shapes import arrow, circle, ellipse, rectangle, star
from drawlib.styles import Colors, Styles
from drawlib.text import text

x1 = 10
title_style = Styles.Primary.patch(text_size=24)
icon_thin = Styles.Primary.patch(icon_style="thin")


def main():
    setup(width=100, height=60, color=Colors.Canvas)
    draw_icon()
    draw_image()
    draw_line()
    draw_shape()
    draw_text()
    save()


def draw_icon():
    y = 52
    w = 8
    text((x1, y), "Icon", style=title_style)
    phosphor.airplane_taxiing((30, y), width=w, style=icon_thin)
    phosphor.airplane_takeoff(xy=(40, y), width=w, style=icon_thin)
    phosphor.airplane_in_flight(
        xy=(50, y), width=w, style=Styles.Primary.patch(icon_color=Colors.Red, icon_style="thin")
    )
    phosphor.airplane_tilt(xy=(60, y), width=w, style=icon_thin)
    phosphor.airplane(xy=(70, y), width=w, angle=270, style=icon_thin)
    phosphor.airplane_landing(xy=(80, y), width=w, style=icon_thin)
    phosphor.airplane_taxiing(
        (90, y), width=w, style=Styles.Primary.patch(icon_style="fill", icon_color=Colors.Red)
    )


def draw_image():
    y = 41
    w = 7
    text((x1, y), "Image", style=title_style)
    image((30, y), w, image="../_assets/linux.png")
    image((40, y), w, image="../_assets/linux.png", style=Styles.Primary.patch(image_border_width=1))
    image((50, y), w, image="../_assets/linux.png", style=Styles.Primary.patch(image_tint_color=Colors.Red))
    image((60, y), w, image="../_assets/linux.png", angle=315)
    dimg = Dimage("../_assets/linux.png")
    image((70, y), w, image=dimg.flip().sepia())
    image((80, y), w, image=dimg.mosaic(24))
    image((90, y), w, image=dimg.brightness(0.5).mirror())


def draw_line():
    y = 29
    text((x1, y), "Line", style=title_style)
    line((30, y - 4), (30, y + 4), style=Styles.Primary)
    line((40, y - 4), (40, y + 4), arrow_head="->", style=Styles.Primary)
    line((50, y - 4), (50, y + 4), style=Styles.PrimaryDashed.patch(line_color=Colors.Red))
    line(
        (60, y - 4),
        (60, y + 4),
        arrow_head="<->",
        style=Styles.Primary.patch(line_color=Colors.Red, line_arrow_head_fill=True),
    )
    line_curved((69, y - 4), (69, y + 4), bend=-0.3, style=Styles.Primary)
    line_curved((71, y - 4), (71, y + 4), bend=0.3, style=Styles.Primary)
    lines(
        [(77, y - 4), (83, y - 2), (77, y), (83, y + 2), (77, y + 4)],
        style=Styles.Primary.patch(line_style="dotted", line_color=Colors.Red),
    )
    lines_curved([(87, y - 4), (87, y + 4), (93, y + 4), (93, y - 4)], r=2, arrow_head="->", style=Styles.Primary)


def draw_shape():
    y = 17
    w = 8
    text((x1, y), "Shape", style=title_style)
    circle((30, y), radius=w / 2, style=Styles.Primary)
    ellipse((40, y), width=w / 2, height=w, style=Styles.RedDashed)
    rectangle((50, y), width=7, height=7, text="rect", style=Styles.Primary, text_style=Styles.White)
    rectangle((60, y), width=7, height=4, angle=315, r=2, style=Styles.RedSolid)
    star((70, y), 5, 4, 2, style=Styles.Primary)
    arrow((80, y - 4), (80, y + 4), tail_width=3, head_width=6, head_length=3, style=Styles.RedFlat)
    arrow((90, y - 4), (90, y + 4), tail_width=2, head_width=5, head_length=3, head="<->", style=Styles.Primary)


def draw_text():
    y = 7
    text((x1, y), "Text", style=title_style)
    text((35, y), "Hello Drawlib!", style=Styles.Primary.patch(text_font=FontSansSerif.RALEWAYS_REGULAR, text_size=18))
    text(
        (60, y),
        "Hello\nDrawlib!",
        style=Styles.Primary.patch(text_font=FontSerif.COURIER_REGULAR, text_size=28, text_color=Colors.Red),
    )
    text(
        (85, y),
        "こんにちは Drawlib!",
        style=Styles.Primary.patch(
            text_font=FontJapanese.MPLUS1P_REGULAR,
            text_size=16,
            text_bg_fill_color=Colors.Black,
            text_bg_line_width=0,
            text_color=Colors.White,
        ),
    )


main()
