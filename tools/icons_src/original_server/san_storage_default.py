# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Server concept icon: san_storage."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_cylinder_tier,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE
cx = 42.0
width = 56.0
ry = 8.5
tier_bottoms = (22.0, 40.0, 58.0)

for i, y_bot in enumerate(tier_bottoms):
    is_top = i == len(tier_bottoms) - 1
    tier_h = 17.0 if is_top else tier_bottoms[i + 1] - y_bot
    draw_cylinder_tier(
        cx,
        y_bot,
        width=width,
        body_h=tier_h,
        ry=ry,
        body_color=PASTEL_BLUE,
        top_color=WHITE if is_top else None,
        border_color=DARK,
        border_units=w,
        draw_top_cap=is_top,
    )

# Status LED and horizontal drive slit line (parallel to x-axis) on each tier
for y_bot in tier_bottoms:
    y_line = y_bot + 1.2
    circle(
        (25.0, y_line),
        radius=2.4,
        style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=1.7),
    )
    draw_round_segment(
        (32.0, y_line),
        (43.5, y_line),
        width_units=2.0,
        color=DARK,
    )

# Bottom-right circular badge for Block Storage
circle(
    (71.0, 28.0),
    radius=21.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w),
)

# 2x2 symmetric data blocks inside the badge (Top: Blue Green / Bottom: Green Blue)
for bx, by, bcolor in (
    (64.75, 34.25, PASTEL_BLUE),
    (77.25, 34.25, PASTEL_GREEN),
    (64.75, 21.75, PASTEL_GREEN),
    (77.25, 21.75, PASTEL_BLUE),
):
    rectangle(
        (bx, by),
        width=9.5,
        height=9.5,
        style=fill_style(bcolor, border_color=DARK, border_units=2.0, shape_r=2.0),
    )

save()
