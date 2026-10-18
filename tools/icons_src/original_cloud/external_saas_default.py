# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: external_saas."""

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
    draw_round_segment,
    fill_style,
    no_border_fill,
    setup_icon,
    stroke_style,
)

setup_icon()

w = ORIG_STROKE

# Cloud outline shifted slightly up-left to accommodate the bottom-right connector badge
bumps = [
    (27.0, 50.0, 15.0),
    (43.0, 65.0, 20.0),
    (62.0, 61.0, 16.0),
    (72.0, 48.0, 13.0),
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

polygon(cloud_pts, style=no_border_fill(WHITE))
draw_round_polyline(cloud_pts, width_units=w, color=DARK, closed=True)

# Subtle cloud inner highlight arc on top-left with round caps
arc_cx, arc_cy, arc_r = 43.0, 65.0, 12.5
a0, a1 = 85.0, 155.0
arc(
    (arc_cx, arc_cy),
    width=arc_r * 2.0,
    height=arc_r * 2.0,
    angle_start=a0,
    angle_end=a1,
    style=stroke_style(PASTEL_BLUE, width_units=3.2),
)
for deg in (a0, a1):
    rad = math.radians(deg)
    draw_cap((arc_cx + arc_r * math.cos(rad), arc_cy + arc_r * math.sin(rad)), width_units=3.2, color=PASTEL_BLUE)

# Interlocking external connector badge at (66, 30)
badge_cx, badge_cy = 66.0, 30.0
circle(
    (badge_cx, badge_cy),
    radius=16.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w),
)

# Plug prongs and body inside the badge
draw_round_segment((62.5, 33.0), (62.5, 39.5), width_units=2.0, color=DARK)
draw_round_segment((69.5, 33.0), (69.5, 39.5), width_units=2.0, color=DARK)
draw_round_segment((66.0, 19.5), (66.0, 24.5), width_units=2.0, color=DARK)

rectangle(
    (66.0, 29.0),
    width=14.0,
    height=9.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0, shape_r=3.0),
)

save()
