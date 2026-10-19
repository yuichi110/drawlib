# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud concept icon: hybrid_cloud."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
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


# Top-left public cloud
bumps = [
    (22.0, 62.0, 12.0),
    (35.0, 75.0, 16.0),
    (52.0, 72.0, 13.0),
    (61.0, 61.0, 11.0),
]
cloud_pts = _build_cloud(bumps)
polygon(cloud_pts, style=Icon.fill_style(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(cloud_pts, width_units=w, color=Icon.DARK, closed=True)

# Bottom-right on-premises 2U server rack
rx, ry_top, ry_bot = 66.0, 34.0, 18.0
for idx, (yc, col) in enumerate([(ry_top, Icon.WHITE), (ry_bot, Icon.PASTEL_GREEN)]):
    rectangle(
        (rx, yc),
        width=46.0,
        height=13.0,
        style=Icon.fill_style(col, border_color=Icon.DARK, border_units=w, shape_r=3.0),
    )
    circle(
        (rx - 15.0, yc),
        radius=2.2,
        style=Icon.fill_style(
            Icon.PASTEL_BLUE if idx == 1 else Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=1.5
        ),
    )
    Icon.draw_round_segment((rx - 6.0, yc), (rx + 16.0, yc), width_units=1.8, color=Icon.DARK)

# Bidirectional hybrid link arrows
Icon.draw_round_polyline([(28.0, 48.0), (28.0, 26.0), (39.0, 26.0)], width_units=w, color=Icon.DARK, corner_r=4.0)
polygon(
    [(28.0, 51.5), (24.0, 45.5), (32.0, 45.5)],
    style=Icon.fill_style(Icon.DARK, border_color=Icon.DARK, border_units=1.0),
)
polygon(
    [(41.5, 26.0), (35.5, 29.8), (35.5, 22.2)],
    style=Icon.fill_style(Icon.DARK, border_color=Icon.DARK, border_units=1.0),
)

save()
