# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: api_gateway."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.utils import DARK, ORIG_STROKE, PASTEL_BLUE, PASTEL_GREEN, WHITE, draw_chunky_arrow, fill_style, setup_icon

setup_icon()

w = ORIG_STROKE

for px in (19.0, 81.0):
    rectangle(
        (px, 50.0),
        width=14.0,
        height=68.0,
        style=fill_style(WHITE, border_color=DARK, border_units=w, shape_r=5.0),
    )

draw_chunky_arrow(
    y_center=63.0,
    x_tail=33.0,
    x_tip=67.5,
    x_head_base=53.5,
    shaft_half_h=4.6,
    head_half_h=11.0,
    fill_color=PASTEL_BLUE,
    border_units=w,
)

draw_chunky_arrow(
    y_center=37.0,
    x_tail=67.0,
    x_tip=32.5,
    x_head_base=46.5,
    shaft_half_h=4.6,
    head_half_h=11.0,
    fill_color=PASTEL_GREEN,
    border_units=w,
)

save()
