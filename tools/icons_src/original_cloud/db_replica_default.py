# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: db_replica."""

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
width = 44.0
w_half = width / 2.0
ry = 7.5
eh = ry * 2.0
tier_h = 18.0

# 1. Back/right replica cylinder (PASTEL_GREEN)
cx_back = 62.0
back_bottoms = [32.0, 50.0]
y_bot_back = back_bottoms[0]
y_top_back = back_bottoms[-1] + tier_h

for yb in back_bottoms:
    ellipse(
        (cx_back, yb),
        width=width,
        height=eh,
        style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w),
    )
    rectangle(
        (cx_back, yb + tier_h / 2.0),
        width=width,
        height=tier_h,
        style=fill_style(PASTEL_GREEN),
    )

draw_round_segment((cx_back - w_half, y_bot_back), (cx_back - w_half, y_top_back), width_units=w, color=DARK)
draw_round_segment((cx_back + w_half, y_bot_back), (cx_back + w_half, y_top_back), width_units=w, color=DARK)

ellipse(
    (cx_back, y_top_back),
    width=width,
    height=eh,
    style=fill_style(WHITE, border_color=DARK, border_units=w),
)

# 2. Front/left primary cylinder (PASTEL_BLUE)
cx_front = 38.0
front_bottoms = [20.0, 38.0]
y_bot_front = front_bottoms[0]
y_top_front = front_bottoms[-1] + tier_h

for yb in front_bottoms:
    ellipse(
        (cx_front, yb),
        width=width,
        height=eh,
        style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w),
    )
    rectangle(
        (cx_front, yb + tier_h / 2.0),
        width=width,
        height=tier_h,
        style=fill_style(PASTEL_BLUE),
    )

draw_round_segment((cx_front - w_half, y_bot_front), (cx_front - w_half, y_top_front), width_units=w, color=DARK)
draw_round_segment((cx_front + w_half, y_bot_front), (cx_front + w_half, y_top_front), width_units=w, color=DARK)

ellipse(
    (cx_front, y_top_front),
    width=width,
    height=eh,
    style=fill_style(WHITE, border_color=DARK, border_units=w),
)

# 3. Status LED dots on front cylinder
for y_led in (21.0, 39.0):
    circle(
        (50.0, y_led),
        radius=2.8,
        style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=1.8),
    )

save()
