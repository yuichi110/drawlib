# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: virtual_network."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# Cloud bumps: (cx, cy, r)
bumps = [
    (28.0, 42.0, 16.0),
    (44.0, 58.0, 21.0),
    (64.0, 54.0, 17.0),
    (74.0, 40.0, 14.0),
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
steps = 28
for i, (cx, cy, r) in enumerate(bumps):
    a_start = start_angles[i]
    a_end = end_angles[i]
    while a_end > a_start:
        a_end -= 2.0 * math.pi
    for s in range(steps + 1):
        ang = a_start + (a_end - a_start) * (s / steps)
        cloud_pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))

polygon(cloud_pts, style=fill_style(WHITE))
draw_round_polyline(cloud_pts, width_units=w, color=DARK, closed=True)

# 3-node subnet triangle inside the cloud
n_top = (50.0, 60.0)
n_bl = (35.0, 41.0)
n_br = (65.0, 41.0)

draw_round_polyline([n_top, n_bl, n_br], width_units=2.0, color=DARK, closed=True)

circle(n_top, radius=6.5, style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0))
circle(n_bl, radius=6.5, style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=2.0))
circle(n_br, radius=6.5, style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=2.0))

save()
