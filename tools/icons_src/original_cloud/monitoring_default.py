# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: monitoring."""

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

rectangle(
    (50.0, 22.0),
    width=15.0,
    height=16.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w),
)
draw_round_segment((30.0, 14.0), (70.0, 14.0), width_units=w, color=DARK)

rectangle(
    (50.0, 56.0),
    width=76.0,
    height=52.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w, shape_r=7.0),
)

wave_pts = [
    (21.0, 54.0),
    (34.0, 54.0),
    (42.5, 73.0),
    (52.5, 39.0),
    (61.0, 62.0),
    (68.0, 54.0),
    (79.0, 54.0),
]
draw_round_polyline(wave_pts, width_units=w, color=DARK)
circle(
    (42.5, 73.0),
    radius=4.5,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.2),
)

save()
