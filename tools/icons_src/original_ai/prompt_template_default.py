# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: prompt_template."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
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

# 1. Prompt template card base and top header bar
rectangle(
    (46.0, 50.0),
    width=62.0,
    height=64.0,
    style=fill_style(WHITE, shape_r=8.0),
)
draw_rounded_corner_block(
    15.0,
    66.0,
    77.0,
    82.0,
    r=8.0,
    round_tl=True,
    round_tr=True,
    color=PASTEL_BLUE,
)
rectangle(
    (46.0, 50.0),
    width=62.0,
    height=64.0,
    style=fill_style(Colors.Transparent, border_color=DARK, border_units=w, shape_r=8.0),
)
draw_round_segment((15.0, 66.0), (77.0, 66.0), width_units=w, color=DARK)

for x_dot, col in ((24.0, PASTEL_GREEN), (32.5, WHITE)):
    circle(
        (x_dot, 74.0),
        radius=2.5,
        style=fill_style(col, border_color=DARK, border_units=1.8),
    )

# 2. Prompt chevron, template slot pill, and instruction line
draw_round_polyline(
    [(25.0, 56.5), (33.5, 50.0), (25.0, 43.5)],
    width_units=w,
    color=DARK,
)
rectangle(
    (53.0, 50.0),
    width=26.0,
    height=11.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.3, shape_r=5.0),
)
draw_round_segment((25.0, 33.0), (56.0, 33.0), width_units=w, color=DARK)

# 3. Bottom-right AI sparkle accent
sparkle_pts = build_sparkle_4pt_polygon(74.0, 28.0, outer_r=12.5, inner_r=4.3)
polygon(sparkle_pts, style=no_border_fill(PASTEL_GREEN))
draw_round_polyline(sparkle_pts, width_units=2.4, color=DARK, closed=True)

save()
