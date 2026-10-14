# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: switch."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_chunky_arrow,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

rectangle(
    (50.0, 50.0),
    width=76.0,
    height=48.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w, shape_r=6.0),
)

draw_chunky_arrow(
    y_center=60.0,
    x_tail=24.0,
    x_tip=76.0,
    x_head_base=62.0,
    shaft_half_h=3.8,
    head_half_h=8.5,
    fill_color=PASTEL_BLUE,
    border_units=2.4,
)

draw_chunky_arrow(
    y_center=40.0,
    x_tail=76.0,
    x_tip=24.0,
    x_head_base=38.0,
    shaft_half_h=3.8,
    head_half_h=8.5,
    fill_color=PASTEL_GREEN,
    border_units=2.4,
)

save()
