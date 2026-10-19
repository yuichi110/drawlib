# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Server concept icon: nas_storage."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE
cx = 42.0
width = 56.0
ry = 8.5
tier_bottoms = (22.0, 40.0, 58.0)

for i, y_bot in enumerate(tier_bottoms):
    is_top = i == len(tier_bottoms) - 1
    tier_h = 17.0 if is_top else tier_bottoms[i + 1] - y_bot
    Icon.draw_cylinder_tier(
        cx,
        y_bot,
        width=width,
        body_h=tier_h,
        ry=ry,
        body_color=Icon.PASTEL_BLUE,
        top_color=Icon.WHITE if is_top else None,
        border_color=Icon.DARK,
        border_units=w,
        draw_top_cap=is_top,
    )

# Status LED and horizontal drive slit line (parallel to x-axis) on each tier
for y_bot in tier_bottoms:
    y_line = y_bot + 1.2
    circle(
        (25.0, y_line),
        radius=2.4,
        style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=1.7),
    )
    Icon.draw_round_segment(
        (32.0, y_line),
        (43.5, y_line),
        width_units=2.0,
        color=Icon.DARK,
    )

# Bottom-right circular badge for NAS / File Storage
circle(
    (71.0, 28.0),
    radius=21.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w),
)

# Shared file folder back with top-left tab inside the badge
polygon(
    [
        (58.5, 19.0),
        (83.5, 19.0),
        (83.5, 35.5),
        (69.5, 35.5),
        (67.0, 38.5),
        (58.5, 38.5),
    ],
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=2.0, shape_r=2.2),
)

# White inner file sheet peeking out
rectangle(
    (71.0, 28.0),
    width=19.5,
    height=11.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=1.8, shape_r=1.8),
)

# Pastel green front folder flap
rectangle(
    (71.0, 24.5),
    width=25.0,
    height=11.5,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0, shape_r=2.2),
)

save()
