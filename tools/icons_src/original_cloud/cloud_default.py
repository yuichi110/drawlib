# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud concept icon: cloud."""

import math

from drawlib.canvas import save
from drawlib.shapes import arc, polygon
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    WHITE,
    draw_cap,
    draw_round_polyline,
    fill_style,
    setup_icon,
    stroke_style,
)

setup_icon()

w = ORIG_STROKE


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
    (25.0, 40.0, 16.0),
    (43.0, 58.0, 22.0),
    (65.0, 54.0, 18.0),
    (77.0, 39.0, 15.0),
]
cloud_pts = _build_cloud(bumps)

polygon(cloud_pts, style=fill_style(PASTEL_BLUE))
draw_round_polyline(cloud_pts, width_units=w, color=DARK, closed=True)

# Crisp white inner highlight arc on the top-left crown
arc(
    (43.0, 58.0),
    width=29.0,
    height=29.0,
    angle_start=82.0,
    angle_end=158.0,
    style=stroke_style(WHITE, width_units=3.2),
)
for deg in (82.0, 158.0):
    rad = math.radians(deg)
    draw_cap((43.0 + 14.5 * math.cos(rad), 58.0 + 14.5 * math.sin(rad)), width_units=3.2, color=WHITE)

save()
