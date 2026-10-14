# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: model_registry."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    build_sparkle_4pt_polygon,
    draw_iso_cube,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

draw_iso_cube(
    46.0,
    46.0,
    radius=34.0,
    top_color=WHITE,
    left_color=PASTEL_BLUE,
    right_color=PASTEL_BLUE_LIGHT,
    border_color=DARK,
    border_units=w,
)

circle(
    (72.0, 70.0),
    radius=16.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w),
)

sparkle_pts = build_sparkle_4pt_polygon(72.0, 70.0, outer_r=9.5, inner_r=3.3)
polygon(sparkle_pts, style=no_border_fill(WHITE))
draw_round_polyline(sparkle_pts, width_units=2.0, color=DARK, closed=True)

save()
