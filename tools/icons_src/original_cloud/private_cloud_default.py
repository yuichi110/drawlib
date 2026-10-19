# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud concept icon: private_cloud."""

import math

from drawlib.canvas import save
from drawlib.shapes import arc, circle, polygon, rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE


def _build_cloud(
    bumps: list[tuple[float, float, float]],
    *,
    steps: int = 24,
) -> list[tuple[float, float]]:
    def _intersect(
        c1: tuple[float, float, float],
        c2: tuple[float, float, float],
    ) -> tuple[float, float]:
        x1, y1, r1 = c1
        x2, y2, r2 = c2
        dx, dy = x2 - x1, y2 - y1
        d = math.hypot(dx, dy)
        b12 = math.atan2(dy, dx)
        b21 = math.atan2(-dy, -dx)
        a1 = math.acos(max(-1.0, min(1.0, (r1 * r1 + d * d - r2 * r2) / (2.0 * r1 * d))))
        a2 = math.acos(max(-1.0, min(1.0, (r2 * r2 + d * d - r1 * r1) / (2.0 * r2 * d))))
        return b12 + a1, b21 - a2

    starts = [math.radians(270.0)]
    ends: list[float] = []
    for i in range(len(bumps) - 1):
        e_ang, s_ang = _intersect(bumps[i], bumps[i + 1])
        ends.append(e_ang)
        starts.append(s_ang)
    ends.append(math.radians(-90.0))

    pts: list[tuple[float, float]] = []
    for i, (cx, cy, r) in enumerate(bumps):
        a0 = starts[i]
        a1 = ends[i]
        while a1 > a0:
            a1 -= 2.0 * math.pi
        for s in range(steps + 1):
            ang = a0 + (a1 - a0) * (s / steps)
            pts.append((round(cx + r * math.cos(ang), 2), round(cy + r * math.sin(ang), 2)))
    return pts


bumps = [
    (23.0, 48.0, 15.0),
    (40.0, 65.0, 21.0),
    (61.0, 61.0, 17.0),
    (73.0, 47.0, 14.0),
]
cloud_pts = _build_cloud(bumps)

polygon(cloud_pts, style=Icon.fill_style(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(cloud_pts, width_units=w, color=Icon.DARK, closed=True)

# Security shield in front-right protecting the private cloud
sx, sy_bot, sy_top, sh_w = 64.0, 12.0, 54.0, 18.0
left_half = Icon.build_shield_half_points(sx, sy_bot, sy_top, sh_w, side="left")
right_half = Icon.build_shield_half_points(sx, sy_bot, sy_top, sh_w, side="right")
full_shield = left_half + list(reversed(right_half[1:-1]))

polygon(left_half, style=Icon.fill_style(Icon.PASTEL_GREEN))
polygon(right_half, style=Icon.fill_style(Icon.WHITE))
Icon.draw_round_polyline(full_shield, width_units=w, color=Icon.DARK, closed=True)

# Padlock inside the shield
lx, ly = 64.0, 31.0
arc(
    (lx, ly + 5.0),
    width=9.0,
    height=10.0,
    angle_start=0.0,
    angle_end=180.0,
    style=Icon.stroke_style(Icon.DARK, width_units=2.0),
)
rectangle(
    (lx, ly),
    width=13.0,
    height=10.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8, shape_r=2.0),
)
circle((lx, ly), radius=1.6, style=Icon.fill_style(Icon.DARK))

save()
