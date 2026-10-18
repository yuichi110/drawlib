# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: inference_endpoint."""

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    build_sparkle_4pt_polygon,
    draw_chunky_arrow,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

rectangle(
    (38.0, 50.0),
    width=48.0,
    height=56.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w, shape_r=8.0),
)

sparkle_pts = build_sparkle_4pt_polygon(35.0, 50.0, outer_r=14.0, inner_r=4.8)
polygon(sparkle_pts, style=no_border_fill(PASTEL_BLUE))
draw_round_polyline(sparkle_pts, width_units=2.0, color=DARK, closed=True)

draw_chunky_arrow(
    y_center=50.0,
    x_tail=55.0,
    x_tip=88.0,
    x_head_base=73.0,
    shaft_half_h=5.5,
    head_half_h=13.0,
    fill_color=PASTEL_GREEN,
    border_units=w,
)

save()
