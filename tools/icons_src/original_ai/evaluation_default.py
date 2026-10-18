# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: evaluation."""

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    build_sparkle_4pt_polygon,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# 1. Benchmark chart card
rectangle(
    (48.0, 48.0),
    width=66.0,
    height=64.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w, shape_r=9.0),
)

# 2. Rising vertical benchmark bars and baseline
bars = [
    (31.0, 17.0, PASTEL_BLUE_LIGHT),
    (47.0, 27.0, PASTEL_BLUE),
    (63.0, 37.0, PASTEL_GREEN),
]
for bx, bh, bcol in bars:
    rectangle(
        (bx, 27.0 + bh / 2.0),
        width=10.5,
        height=bh,
        style=fill_style(bcol, border_color=DARK, border_units=2.0, shape_r=2.0),
    )
draw_round_segment((23.0, 27.0), (72.0, 27.0), width_units=w, color=DARK)

# 3. Top-right AI sparkle mark (matching fine_tuning & prompt_template)
sparkle_pts = build_sparkle_4pt_polygon(76.0, 76.0, outer_r=11.5, inner_r=4.0)
polygon(sparkle_pts, style=no_border_fill(PASTEL_GREEN))
draw_round_polyline(sparkle_pts, width_units=2.0, color=DARK, closed=True)

save()
