# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud concept icon: multi_cloud."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
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


# Back-left cloud (Provider A)
bumps_left = [
    (18.0, 55.0, 10.0),
    (29.0, 66.0, 14.0),
    (43.0, 64.0, 11.0),
    (50.0, 54.0, 9.0),
]
pts_left = _build_cloud(bumps_left)
polygon(pts_left, style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT))
Icon.draw_round_polyline(pts_left, width_units=w, color=Icon.DARK, closed=True)

# Back-right cloud (Provider B)
bumps_right = [
    (50.0, 54.0, 9.5),
    (60.0, 65.0, 13.5),
    (74.0, 62.0, 11.0),
    (82.0, 53.0, 9.5),
]
pts_right = _build_cloud(bumps_right)
polygon(pts_right, style=Icon.fill_style(Icon.PASTEL_GREEN))
Icon.draw_round_polyline(pts_right, width_units=w, color=Icon.DARK, closed=True)

# Front-center cloud (Primary / Unified Control Plane)
bumps_front = [
    (29.0, 31.0, 13.0),
    (44.0, 45.0, 18.0),
    (62.0, 42.0, 14.5),
    (72.0, 30.0, 12.0),
]
pts_front = _build_cloud(bumps_front)
polygon(pts_front, style=Icon.fill_style(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(pts_front, width_units=w, color=Icon.DARK, closed=True)

# Multi-cloud interconnect hub inside front cloud
n_c = (50.0, 31.5)
n_l = (38.0, 37.5)
n_r = (62.0, 37.5)
Icon.draw_round_segment(n_c, n_l, width_units=1.8, color=Icon.DARK)
Icon.draw_round_segment(n_c, n_r, width_units=1.8, color=Icon.DARK)
circle(n_l, radius=3.5, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=1.7))
circle(n_r, radius=3.5, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=1.7))
circle(n_c, radius=4.2, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=1.8))

save()
