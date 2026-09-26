# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.canvas import config, save
from drawlib.colors import Colors, Colors140
from drawlib.fonts import FontJapanese, FontSansSerif, FontSerif
from drawlib.icons import phosphor
from drawlib.images import Dimage, image
from drawlib.lines import line, line_curved, lines, lines_curved
from drawlib.preset_styles import default_styles
from drawlib.shapes import arrow, circle, ellipse, rectangle, star
from drawlib.text import text

ps = default_styles
x1 = 10
title_style = ps.primary.patch(text_size=24)
icon_thin = ps.primary.patch(icon_style="thin")


def main():
    config(width=100, height=60)
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
        xy=(50, y), width=w, style=ps.primary.patch(icon_color=Colors140.Red, icon_style="thin")
    )
    phosphor.airplane_tilt(xy=(60, y), width=w, style=icon_thin)
    phosphor.airplane(xy=(70, y), width=w, angle=270, style=icon_thin)
    phosphor.airplane_landing(xy=(80, y), width=w, style=icon_thin)
    phosphor.airplane_taxiing(
        (90, y), width=w, style=ps.primary.patch(icon_style="fill", icon_color=Colors140.Red)
    )


def draw_image():
    y = 41
    w = 7
    text((x1, y), "Image", style=title_style)
    image((30, y), w, image="linux.png")
    image((40, y), w, image="linux.png", style=ps.primary.patch(image_border_width=1))
    image((50, y), w, image="linux.png", style=ps.primary.patch(image_tint_color=Colors.Red))
    image((60, y), w, image="linux.png", angle=315)
    dimg = Dimage("linux.png")
    image((70, y), w, image=dimg.flip().sepia())
    image((80, y), w, image=dimg.mosaic(24))
    image((90, y), w, image=dimg.brightness(0.5).mirror())


def draw_line():
    y = 29
    text((x1, y), "Line", style=title_style)
    line((30, y - 4), (30, y + 4), style=ps.primary)
    line((40, y - 4), (40, y + 4), arrowhead="->", style=ps.primary)
    line((50, y - 4), (50, y + 4), style=ps.dashed.patch(line_color=Colors.Red))
    line(
        (60, y - 4),
        (60, y + 4),
        arrowhead="<->",
        style=ps.primary.patch(line_color=Colors.Red, line_arrow_head_fill=True),
    )
    line_curved((69, y - 4), (69, y + 4), bend=-0.3, style=ps.primary)
    line_curved((71, y - 4), (71, y + 4), bend=0.3, style=ps.primary)
    lines(
        [(77, y - 4), (83, y - 2), (77, y), (83, y + 2), (77, y + 4)],
        style=ps.primary.patch(line_style="dotted", line_color=Colors.Red),
    )
    lines_curved([(87, y - 4), (87, y + 4), (93, y + 4), (93, y - 4)], r=2, arrowhead="->", style=ps.primary)


def draw_shape():
    y = 17
    w = 8
    text((x1, y), "Shape", style=title_style)
    circle((30, y), radius=w / 2, style=ps.primary)
    ellipse((40, y), width=w / 2, height=w, style=ps.red_dashed)
    rectangle((50, y), width=7, height=7, text="rect", style=ps.primary, textstyle=ps.white)
    rectangle((60, y), width=7, height=4, angle=315, r=2, style=ps.red_solid)
    star((70, y), 5, 4, 2, style=ps.primary)
    arrow((80, y - 4), (80, y + 4), tail_width=3, head_width=6, head_length=3, style=ps.red_flat)
    arrow((90, y - 4), (90, y + 4), tail_width=2, head_width=5, head_length=3, head="<->", style=ps.primary)


def draw_text():
    y = 7
    text((x1, y), "Text", style=title_style)
    text((35, y), "Hello Drawlib!", style=ps.primary.patch(text_font=FontSansSerif.RALEWAYS_REGULAR, text_size=18))
    text(
        (60, y),
        "Hello\nDrawlib!",
        style=ps.primary.patch(text_font=FontSerif.COURIER_REGULAR, text_size=28, text_color=Colors.Red),
    )
    text(
        (85, y),
        "こんにちは Drawlib!",
        style=ps.primary.patch(
            text_font=FontJapanese.MPLUS1P_REGULAR,
            text_size=16,
            text_bg_fill_color=Colors.Black,
            text_bg_line_width=0,
            text_color=Colors.White,
        ),
    )


main()

