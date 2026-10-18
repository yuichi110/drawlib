# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: in_memory_cache."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
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

# 1. Top and bottom memory module pins
for px in (30.0, 50.0, 70.0):
    draw_round_segment((px, 76.0), (px, 86.0), width_units=w, color=DARK)
    draw_round_segment((px, 14.0), (px, 24.0), width_units=w, color=DARK)

# 2. Outer memory card body
rectangle(
    (50.0, 50.0),
    width=68.0,
    height=52.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=7.0),
)

# 3. Center WHITE circle badge with PASTEL_GREEN lightning bolt
circle(
    (50.0, 50.0),
    radius=18.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0),
)

bolt_pts = [
    (52.0, 62.0),
    (41.0, 49.0),
    (49.0, 49.0),
    (47.0, 38.0),
    (59.0, 51.0),
    (51.0, 51.0),
]
polygon(bolt_pts, style=fill_style(PASTEL_GREEN))
draw_round_polyline(bolt_pts, width_units=2.0, color=DARK, closed=True)

save()
