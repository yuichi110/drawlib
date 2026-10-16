# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Server concept icon: datastore."""

from drawlib.canvas import save
from drawlib.shapes import circle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_cylinder_tier,
    draw_iso_cube,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE
cx = 46.0
width = 56.0
ry = 8.5
body_h = 15.0
tier_bottoms = (20.0, 38.0, 56.0)

for i, y_bot in enumerate(tier_bottoms):
    is_top = i == len(tier_bottoms) - 1
    tier_h = body_h if is_top else tier_bottoms[i + 1] - y_bot
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

# Front LED dots on each storage tier
for y_bot in tier_bottoms:
    circle(
        (28.0, y_bot + 2.0),
        radius=2.6,
        style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=1.8),
    )
    circle(
        (36.5, y_bot + 0.5),
        radius=2.6,
        style=fill_style(WHITE, border_color=DARK, border_units=1.8),
    )

# Overlapping bottom-right 3D VM cube badge
draw_iso_cube(
    72.0,
    30.0,
    radius=14.5,
    top_color=WHITE,
    left_color=PASTEL_GREEN,
    right_color=PASTEL_BLUE_LIGHT,
    border_color=DARK,
    border_units=2.4,
)

save()
