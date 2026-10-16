# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Server icon: dell_hci_appliance_default."""

from drawlib.canvas import save
from drawlib.shapes import arc, ellipse, rectangle
from drawlib.styles import Colors
from drawlib.utils import (
    DELL_BLUE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    no_border_fill,
    setup_icon,
    stroke_style,
)

setup_icon()

BORDER = 4.8

# Top horizontal rack server (outer x=15..85, y=62..87)
rectangle(
    (50.0, 74.5),
    width=70.0 - BORDER,
    height=25.0 - BORDER,
    style=fill_style(
        Colors.Transparent,
        border_color=DELL_BLUE,
        border_units=BORDER,
        shape_r=2.5,
    ),
)
rectangle(
    (50.0, 74.5),
    width=28.0,
    height=5.0,
    style=no_border_fill(DELL_BLUE),
)

# Middle-left half-server C-bracket (outer x=15..36, y=30..55, open on right)
draw_round_polyline(
    [(36.0, 52.6), (17.4, 52.6), (17.4, 32.4), (36.0, 32.4)],
    width_units=BORDER,
    color=DELL_BLUE,
    corner_r=2.5,
)

# Bottom-left bus bar (x=15..36, y=12..17, height=5.0)
rectangle(
    (25.5, 14.5),
    width=21.0,
    height=5.0,
    style=no_border_fill(DELL_BLUE),
)

# Bottom-right storage cylinder (cx=66.0, outer y=12..55, outer width=42.0)
CYL_CX = 66.0
CYL_STROKE = 4.6
CYL_W = 42.0 - CYL_STROKE
CYL_EH = 21.5 - CYL_STROKE
CYL_Y_TOP = 55.0 - CYL_STROKE / 2.0 - CYL_EH / 2.0
CYL_Y_BOT = 12.0 + CYL_STROKE / 2.0 + CYL_EH / 2.0

# DELL_BLUE top ellipse (including middle waist front arc) + bottom arc + side walls
ellipse(
    (CYL_CX, CYL_Y_TOP),
    width=CYL_W,
    height=CYL_EH,
    style=stroke_style(DELL_BLUE, width_units=CYL_STROKE),
)
arc(
    (CYL_CX, CYL_Y_BOT),
    width=CYL_W,
    height=CYL_EH,
    angle_start=180.0,
    angle_end=360.0,
    style=stroke_style(DELL_BLUE, width_units=CYL_STROKE),
)
for side_x in (CYL_CX - CYL_W / 2.0, CYL_CX + CYL_W / 2.0):
    draw_round_segment(
        (side_x, CYL_Y_BOT),
        (side_x, CYL_Y_TOP),
        width_units=CYL_STROKE,
        color=DELL_BLUE,
    )

save()
