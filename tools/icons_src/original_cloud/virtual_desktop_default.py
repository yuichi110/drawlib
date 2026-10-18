# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: virtual_desktop."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# Monitor stand neck and base
rectangle(
    (43.0, 26.0),
    width=14.0,
    height=14.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w),
)
draw_round_segment((25.0, 18.0), (61.0, 18.0), width_units=w, color=DARK)

# Monitor outer bezel and inner screen
rectangle(
    (43.0, 56.0),
    width=62.0,
    height=46.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w, shape_r=6.5),
)
rectangle(
    (43.0, 56.0),
    width=50.0,
    height=34.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=2.0, shape_r=3.5),
)

# Mini desktop window inside the VDI screen
rectangle(
    (32.0, 60.0),
    width=18.0,
    height=13.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0, shape_r=2.0),
)

# Overlapping Cloud badge in the bottom-right indicating Cloud VDI
bumps = [
    (56.0, 35.0, 8.5),
    (65.0, 43.0, 11.0),
    (76.0, 40.5, 9.0),
    (81.5, 33.5, 7.5),
]


def _outer_intersect_angles(
    c1: tuple[float, float, float],
    c2: tuple[float, float, float],
) -> tuple[float, float]:
    x1, y1, r1 = c1
    x2, y2, r2 = c2
    dx, dy = x2 - x1, y2 - y1
    d = math.hypot(dx, dy)
    base_12 = math.atan2(dy, dx)
    base_21 = math.atan2(-dy, -dx)
    a1 = math.acos(max(-1.0, min(1.0, (r1 * r1 + d * d - r2 * r2) / (2.0 * r1 * d))))
    a2 = math.acos(max(-1.0, min(1.0, (r2 * r2 + d * d - r1 * r1) / (2.0 * r2 * d))))
    return base_12 + a1, base_21 - a2


start_angles = [math.radians(270.0)]
end_angles: list[float] = []
for i in range(len(bumps) - 1):
    ang1, ang2 = _outer_intersect_angles(bumps[i], bumps[i + 1])
    end_angles.append(ang1)
    start_angles.append(ang2)
end_angles.append(math.radians(-90.0))

cloud_pts: list[tuple[float, float]] = []
steps = 24
for i, (cx, cy, r) in enumerate(bumps):
    a_start = start_angles[i]
    a_end = end_angles[i]
    while a_end > a_start:
        a_end -= 2.0 * math.pi
    for s in range(steps + 1):
        ang = a_start + (a_end - a_start) * (s / steps)
        cloud_pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))

polygon(cloud_pts, style=fill_style(PASTEL_GREEN))
draw_round_polyline(cloud_pts, width_units=2.0, color=DARK, closed=True)

save()
