# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: vector_database."""

from drawlib.canvas import save
from drawlib.shapes import circle, ellipse, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# 1. 3-tier database cylinder (left/back, matching database & time_series_database)
cx = 41.0
width = 54.0
w_half = width / 2.0
ry = 8.5
eh = ry * 2.0
tier_bottoms = [20.0, 37.0, 54.0]
tier_h = 17.0
y_bot = tier_bottoms[0]
y_top = tier_bottoms[-1] + tier_h

for yb in tier_bottoms:
    ellipse(
        (cx, yb),
        width=width,
        height=eh,
        style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w),
    )
    rectangle(
        (cx, yb + tier_h / 2.0),
        width=width,
        height=tier_h,
        style=fill_style(PASTEL_BLUE),
    )

draw_round_segment((cx - w_half, y_bot), (cx - w_half, y_top), width_units=w, color=DARK)
draw_round_segment((cx + w_half, y_bot), (cx + w_half, y_top), width_units=w, color=DARK)

ellipse(
    (cx, y_top),
    width=width,
    height=eh,
    style=fill_style(WHITE, border_color=DARK, border_units=w),
)

# 2. Overlapping bottom-right vector space badge
badge_c = (68.0, 33.0)
circle(
    badge_c,
    radius=20.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w),
)

origin = (59.5, 24.5)
draw_round_segment(origin, (59.5, 43.5), width_units=2.2, color=DARK)
draw_round_segment(origin, (78.5, 24.5), width_units=2.2, color=DARK)

v_main = (74.5, 39.5)
draw_round_segment(origin, v_main, width_units=2.4, color=DARK)

circle(
    origin,
    radius=3.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=1.8),
)
circle(
    v_main,
    radius=5.2,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.2),
)

save()
