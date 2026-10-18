# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: notebook."""

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    build_sparkle_4pt_polygon,
    draw_round_polyline,
    draw_round_segment,
    draw_rounded_corner_block,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# 1. Spiral-bound notebook card with left PASTEL_BLUE spine strip
rectangle(
    (48.0, 48.0),
    width=56.0,
    height=64.0,
    style=fill_style(WHITE, shape_r=6.5),
)
draw_rounded_corner_block(
    20.0,
    16.0,
    32.0,
    80.0,
    r=6.5,
    round_tl=True,
    round_bl=True,
    color=PASTEL_BLUE,
)
rectangle(
    (48.0, 48.0),
    width=56.0,
    height=64.0,
    style=fill_style(Colors.Transparent, border_color=DARK, border_units=w, shape_r=6.5),
)
draw_round_segment((32.0, 16.0), (32.0, 80.0), width_units=w, color=DARK)

# 2. Four horizontal spiral binder rings
for ry in (67.0, 54.0, 42.0, 29.0):
    draw_round_segment((14.5, ry), (25.0, ry), width_units=3.2, color=DARK)

# 3. Simple horizontal notebook lines inside page
draw_round_segment((41.0, 60.0), (63.0, 60.0), width_units=w, color=DARK)
draw_round_segment((41.0, 48.0), (66.0, 48.0), width_units=w, color=DARK)
draw_round_segment((41.0, 36.0), (58.0, 36.0), width_units=w, color=DARK)

# 4. Top-right AI sparkle mark
sparkle_pts = build_sparkle_4pt_polygon(75.0, 76.0, outer_r=11.5, inner_r=4.0)
polygon(sparkle_pts, style=no_border_fill(PASTEL_GREEN))
draw_round_polyline(sparkle_pts, width_units=2.0, color=DARK, closed=True)

save()
