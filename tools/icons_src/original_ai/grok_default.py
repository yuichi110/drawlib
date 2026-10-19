# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original AI concept icon: grok."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

Icon.setup()

w = 2.0
cx, cy = 50.0, 50.0


def _circle_pts(xc: float, yc: float, r: float, steps: int = 64) -> list[tuple[float, float]]:
    """Sample a circle polygon."""
    return [
        (xc + r * math.cos(2.0 * math.pi * i / steps), yc + r * math.sin(2.0 * math.pi * i / steps))
        for i in range(steps)
    ]


def _cubic(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    steps: int = 18,
) -> list[tuple[float, float]]:
    """Sample cubic Bezier curve excluding p0."""
    pts: list[tuple[float, float]] = []
    for i in range(1, steps + 1):
        t = i / steps
        mt = 1.0 - t
        pts.append(
            (
                (mt**3) * p0[0] + 3.0 * (mt**2) * t * p1[0] + 3.0 * mt * (t**2) * p2[0] + (t**3) * p3[0],
                (mt**3) * p0[1] + 3.0 * (mt**2) * t * p1[1] + 3.0 * mt * (t**2) * p2[1] + (t**3) * p3[1],
            )
        )
    return pts


# 1. Circular orbital ring (Colors.Gray6 with transparent inner hole)
outer_ring = _circle_pts(cx, cy, 29.0)
inner_ring = _circle_pts(cx, cy, 19.8)

polygon(outer_ring, holes=[inner_ring], style=Icon.fill_style(Colors.Gray6))
Icon.draw_round_polyline(outer_ring, width_units=w, color=Icon.DARK, closed=True)
Icon.draw_round_polyline(inner_ring, width_units=1.8, color=Icon.DARK, closed=True)

# 2. Bold diagonal slash blade piercing from bottom-left (11.5, 11.5) to top-right (88.5, 88.5)
p_bl = (11.5, 11.5)
p_tr = (88.5, 88.5)

upper_edge = [
    p_bl,
    *_cubic(p_bl, (26.0, 29.5), (39.0, 44.5), (45.8, 54.2), 14),
    *_cubic((45.8, 54.2), (53.0, 64.5), (69.5, 75.5), p_tr, 14),
]
lower_edge = [
    p_tr,
    *_cubic(p_tr, (74.0, 70.5), (61.0, 55.5), (54.2, 45.8), 14),
    *_cubic((54.2, 45.8), (47.0, 35.5), (30.5, 24.5), p_bl, 14),
]

blade_outline = [*upper_edge, *lower_edge[1:-1]]
polygon(blade_outline, style=Icon.no_border_fill(Colors.Gray6))
Icon.draw_round_polyline(blade_outline, width_units=w, color=Icon.DARK, closed=True)

save()
