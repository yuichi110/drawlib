# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security concept icon: casb (Cloud Access Security Broker)."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import Icon

Icon.setup()

w_shape = 2.0
w_line = 2.0

# 1. Fluffy PASTEL_BLUE cloud silhouette (x=10..90, y=34..86)
bumps = [
    (26.0, 50.0, 16.0),
    (45.0, 64.0, 22.0),
    (66.0, 60.0, 18.0),
    (76.0, 48.0, 14.0),
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

polygon(cloud_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(cloud_pts, width_units=w_shape, color=Icon.DARK, closed=True)

# 2. Bottom-center WHITE rounded gate card
rectangle(
    (50.0, 36.0),
    width=40.0,
    height=34.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_shape, shape_r=6.0),
)

# 3. Padlock shackle arc (drawn behind padlock body)
shackle_cx, shackle_cy, shackle_r = 50.0, 42.5, 6.5
shackle_pts: list[tuple[float, float]] = [(shackle_cx - shackle_r, 37.5)]
for i in range(25):
    ang = math.radians(180.0 - 180.0 * (i / 24))
    shackle_pts.append(
        (
            shackle_cx + shackle_r * math.cos(ang),
            shackle_cy + shackle_r * math.sin(ang),
        )
    )
shackle_pts.append((shackle_cx + shackle_r, 37.5))
Icon.draw_round_polyline(shackle_pts, width_units=w_line, color=Icon.DARK)

# 4. PASTEL_GREEN padlock body + DARK keyhole
rectangle(
    (50.0, 30.0),
    width=22.0,
    height=18.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_shape, shape_r=3.5),
)
circle((50.0, 31.8), radius=2.2, style=Icon.fill_style(Icon.DARK))
Icon.draw_round_segment((50.0, 31.8), (50.0, 27.2), width_units=2.0, color=Icon.DARK)

save()
