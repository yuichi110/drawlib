# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Server concept icon: backup_appliance."""

import math

from drawlib.canvas import save
from drawlib.shapes import arc, circle, polygon, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_cap,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
    stroke_style,
)

setup_icon()

w = ORIG_STROKE

# Rounded backup vault/server box
rectangle(
    (48.0, 48.0),
    width=66.0,
    height=66.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=8.0),
)

# 2 horizontal white storage tiers
for y_tier in (64.0, 48.0):
    rectangle(
        (48.0, y_tier),
        width=50.0,
        height=11.0,
        style=fill_style(WHITE, border_color=DARK, border_units=2.0, shape_r=2.5),
    )

# Overlapping bottom-right circular backup/restore badge
bx, by = 66.0, 32.0
circle(
    (bx, by),
    radius=19.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w),
)

# Counter-clockwise circular arrow around center dot
r_arc = 10.5
ang_start = -145.0
ang_end_dark = 128.0
ang_end_white = 132.0

# 1. Outer dark stroke for the circular shaft
arc(
    (bx, by),
    width=r_arc * 2.0,
    height=r_arc * 2.0,
    angle_start=ang_start,
    angle_end=ang_end_dark,
    style=stroke_style(DARK, width_units=6.2),
)
rad_s = math.radians(ang_start)
draw_cap(
    (bx + r_arc * math.cos(rad_s), by + r_arc * math.sin(rad_s)),
    width_units=6.2,
    color=DARK,
)

# 2. Arrowhead triangle at top-left pointing counter-clockwise (down-left)
rad_h = math.radians(130.0)
px = bx + r_arc * math.cos(rad_h)
py = by + r_arc * math.sin(rad_h)
tx, ty = -math.sin(rad_h), math.cos(rad_h)
nx, ny = math.cos(rad_h), math.sin(rad_h)

head_pts = [
    (px + tx * 5.8, py + ty * 5.8),
    (px - tx * 1.2 + nx * 4.8, py - ty * 1.2 + ny * 4.8),
    (px - tx * 1.2 - nx * 4.8, py - ty * 1.2 - ny * 4.8),
]
polygon(head_pts, style=no_border_fill(WHITE))
draw_round_polyline(head_pts, width_units=1.8, color=DARK, closed=True)

# 3. Inner white stroke for the circular shaft (seamless join into arrowhead)
arc(
    (bx, by),
    width=r_arc * 2.0,
    height=r_arc * 2.0,
    angle_start=ang_start,
    angle_end=ang_end_white,
    style=stroke_style(WHITE, width_units=2.6),
)
draw_cap(
    (bx + r_arc * math.cos(rad_s), by + r_arc * math.sin(rad_s)),
    width_units=2.6,
    color=WHITE,
)

# 4. Center dot inside the circular arrow
circle(
    (bx, by),
    radius=2.6,
    style=fill_style(WHITE, border_color=DARK, border_units=1.8),
)

save()
