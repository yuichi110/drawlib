# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: time_series_db."""

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

# 1. Database cylinder (left/back)
cx = 42.0
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

# 2. Overlapping bottom-right clock badge
clock_center = (68.0, 32.0)
circle(
    clock_center,
    radius=18.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w),
)

# Clock hands
draw_round_segment(clock_center, (68.0, 42.5), width_units=2.5, color=DARK)
draw_round_segment(clock_center, (76.5, 32.0), width_units=2.5, color=DARK)

# Center PASTEL_GREEN pivot dot
circle(
    clock_center,
    radius=3.4,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=1.8),
)

save()
