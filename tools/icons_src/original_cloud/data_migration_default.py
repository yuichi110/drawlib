# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: data_migration."""

from drawlib.canvas import save
from drawlib.shapes import ellipse, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_chunky_arrow,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE
width = 28.0
w_half = width / 2.0
ry = 5.5
eh = ry * 2.0
tier_bottoms = [24.0, 40.0, 56.0]
tier_h = 16.0
y_bot = tier_bottoms[0]
y_top = tier_bottoms[-1] + tier_h

# 1. Left source database cylinder (cx=25, y=24..72, WHITE & PASTEL_BLUE_LIGHT)
cx_src = 25.0
for yb in tier_bottoms:
    ellipse(
        (cx_src, yb),
        width=width,
        height=eh,
        style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w),
    )
    rectangle(
        (cx_src, yb + tier_h / 2.0),
        width=width,
        height=tier_h,
        style=fill_style(PASTEL_BLUE_LIGHT),
    )

draw_round_segment((cx_src - w_half, y_bot), (cx_src - w_half, y_top), width_units=w, color=DARK)
draw_round_segment((cx_src + w_half, y_bot), (cx_src + w_half, y_top), width_units=w, color=DARK)

ellipse(
    (cx_src, y_top),
    width=width,
    height=eh,
    style=fill_style(WHITE, border_color=DARK, border_units=w),
)

# 2. Right target database cylinder (cx=75, y=24..72, PASTEL_BLUE & PASTEL_GREEN)
cx_tgt = 75.0
tgt_colors = [PASTEL_BLUE, PASTEL_BLUE, PASTEL_GREEN]
for yb, t_col in zip(tier_bottoms, tgt_colors, strict=True):
    ellipse(
        (cx_tgt, yb),
        width=width,
        height=eh,
        style=fill_style(t_col, border_color=DARK, border_units=w),
    )
    rectangle(
        (cx_tgt, yb + tier_h / 2.0),
        width=width,
        height=tier_h,
        style=fill_style(t_col),
    )

draw_round_segment((cx_tgt - w_half, y_bot), (cx_tgt - w_half, y_top), width_units=w, color=DARK)
draw_round_segment((cx_tgt + w_half, y_bot), (cx_tgt + w_half, y_top), width_units=w, color=DARK)

ellipse(
    (cx_tgt, y_top),
    width=width,
    height=eh,
    style=fill_style(WHITE, border_color=DARK, border_units=w),
)

# 3. Two chunky horizontal transfer arrows centered cleanly between the cylinders
for y_arrow in (57.0, 38.0):
    draw_chunky_arrow(
        y_center=y_arrow,
        x_tail=41.5,
        x_head_base=51.5,
        x_tip=59.5,
        shaft_half_h=3.2,
        head_half_h=6.6,
        fill_color=PASTEL_GREEN,
        border_units=2.3,
        border_color=DARK,
    )

save()
