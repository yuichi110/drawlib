# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco network topology icon: WAN cloud (modern 2D SAFE variant)."""

import math

from drawlib.canvas import save
from drawlib.utils import (
    WHITE,
    draw_cisco_modern_badge,
    draw_round_polyline,
    setup_icon,
)

setup_icon()

draw_cisco_modern_badge()

# 4 upper puff circles (cx, cy, r) over a flat baseline at y = 33.5
puffs: list[tuple[float, float, float]] = [
    (29.0, 43.0, 9.5),   # 0: Left lobe (bottom at 33.5)
    (38.5, 52.5, 10.5),  # 1: Upper-left lobe
    (55.5, 54.0, 14.5),  # 2: Upper-right main crown
    (71.0, 42.5, 9.0),   # 3: Right lobe (bottom at 33.5)
]

# Compute exact outer intersections between adjacent upper puffs (0->1, 1->2, 2->3)
intersections: list[tuple[float, float]] = []
for i in range(len(puffs) - 1):
    cx1, cy1, r1 = puffs[i]
    cx2, cy2, r2 = puffs[i + 1]
    dx = cx2 - cx1
    dy = cy2 - cy1
    d = math.hypot(dx, dy)
    ux, uy = dx / d, dy / d
    a = (r1 * r1 - r2 * r2 + d * d) / (2.0 * d)
    h = math.sqrt(max(0.0, r1 * r1 - a * a))
    intersections.append((cx1 + a * ux - h * uy, cy1 + a * uy + h * ux))

cloud_pts: list[tuple[float, float]] = []
start_pts = [(29.0, 33.5), *intersections]
end_pts = [*intersections, (71.0, 33.5)]

for i, (cx, cy, r) in enumerate(puffs):
    p_start = start_pts[i]
    p_end = end_pts[i]
    a_start = math.atan2(p_start[1] - cy, p_start[0] - cx)
    a_end = math.atan2(p_end[1] - cy, p_end[0] - cx)
    while a_end > a_start:
        a_end -= 2.0 * math.pi
    steps = 22
    for s in range(steps + (1 if i == len(puffs) - 1 else 0)):
        ang = a_start + (a_end - a_start) * (s / steps)
        cloud_pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))

# Clean 2D white cloud outline inside the badge
draw_round_polyline(cloud_pts, width_units=4.4, color=WHITE, closed=True)

# Connected puff-crease arc continuing inward from the upper-center valley (intersections[1])
v_cx, v_cy, v_r = puffs[2]
v_start = math.atan2(intersections[1][1] - v_cy, intersections[1][0] - v_cx)
crease_pts = [
    (
        v_cx + v_r * math.cos(v_start + math.radians(32.0 * (k / 10))),
        v_cy + v_r * math.sin(v_start + math.radians(32.0 * (k / 10))),
    )
    for k in range(11)
]
draw_round_polyline(crease_pts, width_units=3.8, color=WHITE)

save()
