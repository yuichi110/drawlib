# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Client concept icon: game_console."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# Left and right shoulder bumper buttons
for bx in (31.0, 69.0):
    rectangle(
        (bx, 68.5),
        width=15.0,
        height=6.5,
        style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=2.2, shape_r=3.0),
    )

# Smooth ergonomic gamepad contour
body_pts: list[tuple[float, float]] = []
steps = 14

# Left shoulder arc around (31.0, 53.0), r=15.0 from 90 deg to 172 deg
for i in range(steps + 1):
    ang = math.radians(90.0 + 82.0 * (i / steps))
    body_pts.append((31.0 + 15.0 * math.cos(ang), 53.0 + 15.0 * math.sin(ang)))

# Left grip tip arc around (22.5, 32.0), r=9.5 from 172 deg to 332 deg
for i in range(steps + 1):
    ang = math.radians(172.0 + 160.0 * (i / steps))
    body_pts.append((22.5 + 9.5 * math.cos(ang), 32.0 + 9.5 * math.sin(ang)))

# Left inner grip-to-bridge concave fillet around (40.5, 36.5), r=4.5 from 152 deg down to 90 deg
for i in range(9):
    ang = math.radians(152.0 - 62.0 * (i / 8))
    body_pts.append((40.5 + 4.5 * math.cos(ang), 36.5 + 4.5 * math.sin(ang)))

# Right inner bridge-to-grip concave fillet around (59.5, 36.5), r=4.5 from 90 deg down to 28 deg
for i in range(9):
    ang = math.radians(90.0 - 62.0 * (i / 8))
    body_pts.append((59.5 + 4.5 * math.cos(ang), 36.5 + 4.5 * math.sin(ang)))

# Right grip tip arc around (77.5, 32.0), r=9.5 from 208 deg to 368 deg (8 deg)
for i in range(steps + 1):
    ang = math.radians(208.0 + 160.0 * (i / steps))
    body_pts.append((77.5 + 9.5 * math.cos(ang), 32.0 + 9.5 * math.sin(ang)))

# Right shoulder arc around (69.0, 53.0), r=15.0 from 8 deg to 90 deg
for i in range(steps + 1):
    ang = math.radians(8.0 + 82.0 * (i / steps))
    body_pts.append((69.0 + 15.0 * math.cos(ang), 53.0 + 15.0 * math.sin(ang)))

polygon(body_pts, style=fill_style(PASTEL_BLUE))
draw_round_polyline(body_pts, width_units=w, color=DARK, closed=True)

# WHITE D-pad cross on left side
cx_d, cy_d = 31.0, 53.0
arm, half_w = 8.0, 2.8
dpad_pts = [
    (cx_d - half_w, cy_d + arm),
    (cx_d + half_w, cy_d + arm),
    (cx_d + half_w, cy_d + half_w),
    (cx_d + arm, cy_d + half_w),
    (cx_d + arm, cy_d - half_w),
    (cx_d + half_w, cy_d - half_w),
    (cx_d + half_w, cy_d - arm),
    (cx_d - half_w, cy_d - arm),
    (cx_d - half_w, cy_d - half_w),
    (cx_d - arm, cy_d - half_w),
    (cx_d - arm, cy_d + half_w),
    (cx_d - half_w, cy_d + half_w),
]
polygon(dpad_pts, style=fill_style(WHITE))
draw_round_polyline(dpad_pts, width_units=1.9, color=DARK, closed=True)

# 4 PASTEL_GREEN action buttons on right side
for ax, ay in ((69.0, 59.0), (75.0, 53.0), (69.0, 47.0), (63.0, 53.0)):
    circle(
        (ax, ay),
        radius=3.2,
        style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=1.8),
    )

# Center menu dots
for mx in (46.5, 53.5):
    circle((mx, 54.0), radius=1.5, style=fill_style(DARK))

save()
