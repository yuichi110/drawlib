# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: directory_service."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

root_xy = (50.0, 78.0)
mid_left = (32.0, 50.0)
mid_right = (68.0, 50.0)
leaf_left = (22.0, 22.0)
leaf_mid = (50.0, 22.0)
leaf_right = (78.0, 22.0)

# Pyramid hierarchy connector frame
draw_round_polyline([root_xy, mid_left, mid_right], width_units=w, color=DARK, closed=True)
draw_round_segment(mid_left, leaf_left, width_units=w, color=DARK)
draw_round_segment(mid_left, leaf_mid, width_units=w, color=DARK)
draw_round_segment(mid_right, leaf_mid, width_units=w, color=DARK)
draw_round_segment(mid_right, leaf_right, width_units=w, color=DARK)
draw_round_segment(leaf_left, leaf_right, width_units=w, color=DARK)

# Top root diamond node (rotated rounded square)
rectangle(
    root_xy,
    width=15.0,
    height=15.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w, shape_r=2.5, angle=45.0),
)

# Middle organizational unit (OU) rounded square nodes
for m_xy in (mid_left, mid_right):
    rectangle(
        m_xy,
        width=15.0,
        height=15.0,
        style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=3.5),
    )

# Bottom leaf object/user nodes
for l_xy in (leaf_left, leaf_mid, leaf_right):
    circle(
        l_xy,
        radius=7.5,
        style=fill_style(WHITE, border_color=DARK, border_units=w),
    )
    circle(
        l_xy,
        radius=2.6,
        style=fill_style(DARK),
    )

save()
