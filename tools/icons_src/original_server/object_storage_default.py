# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Server concept icon: object_storage."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_cylinder_tier,
    draw_iso_cube,
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
        width_units=2.1,
        color=DARK,
    )

# Bottom-right circular badge for Object Storage
circle(
    (71.0, 28.0),
    radius=21.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w),
)

# Object 1: Pastel green circle at top-left of badge
circle(
    (63.5, 34.0),
    radius=5.4,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=1.9),
)

# Object 2: Pastel blue light triangle at top-right of badge
polygon(
    [
        (72.5, 29.0),
        (84.0, 29.0),
        (78.25, 39.2),
    ],
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=1.9, shape_r=1.3),
)

# Object 3: Bottom 3D isometric cube inside badge
draw_iso_cube(
    cx=71.0,
    cy=21.0,
    radius=6.8,
    top_color=WHITE,
    left_color=PASTEL_BLUE,
    right_color=PASTEL_GREEN,
    border_color=DARK,
    border_units=1.9,
)

save()
