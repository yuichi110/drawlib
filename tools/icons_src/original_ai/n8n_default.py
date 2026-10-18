# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original AI concept icon: n8n."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import (
    DARK,
    draw_compound_polygon,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 2.0
ROSE_PINK = "#EF4C74"


def _circle_pts(xc: float, yc: float, r: float, steps: int = 44) -> list[tuple[float, float]]:
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
    steps: int = 16,
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


def _offset_curve(
    pts: list[tuple[float, float]],
    offset: float,
) -> list[tuple[float, float]]:
    """Offset a 2D polyline along its left normal by offset units."""
    out: list[tuple[float, float]] = []
    n = len(pts)
    for i in range(n):
        p_prev = pts[max(0, i - 1)]
        p_next = pts[min(n - 1, i + 1)]
        dx = p_next[0] - p_prev[0]
        dy = p_next[1] - p_prev[1]
        length = math.hypot(dx, dy)
        nx = -dy / length * offset if length > 1e-6 else 0.0
        ny = dx / length * offset if length > 1e-6 else offset
        out.append((pts[i][0] + nx, pts[i][1] + ny))
    return out


# Node centers (kept well inside [9, 91] with radius 8.0 and w = 1.9 border)
n1 = (19.0, 50.0)
n2 = (39.0, 50.0)
n3 = (81.0, 62.0)
n4 = (73.0, 38.0)
half_bar = 2.15
r_trim = 5.6  # Bars end inside solid ring band [3.9, 8.0] so transparent holes stay clean

# 1. Left horizontal bar (n1 -> n2)
left_bar = [
    (n1[0] + r_trim, n1[1] + half_bar),
    (n2[0] - r_trim, n2[1] + half_bar),
    (n2[0] - r_trim, n2[1] - half_bar),
    (n1[0] + r_trim, n1[1] - half_bar),
]

# 2. Upper curved branch bar (n2 -> n3)
upper_spine = [
    (n2[0] + r_trim, n2[1]),
    (49.5, 50.0),
    *_cubic((49.5, 50.0), (56.5, 50.0), (56.5, 62.0), (63.5, 62.0), 18),
    (n3[0] - r_trim, n3[1]),
]
upper_bar = [
    *_offset_curve(upper_spine, +half_bar),
    *reversed(_offset_curve(upper_spine, -half_bar)),
]

# 3. Lower curved branch bar (n2 -> n4)
lower_spine = [
    (n2[0] + r_trim, n2[1]),
    (49.5, 50.0),
    *_cubic((49.5, 50.0), (56.5, 50.0), (56.5, 38.0), (63.5, 38.0), 18),
    (n4[0] - r_trim, n4[1]),
]
lower_bar = [
    *_offset_curve(lower_spine, +half_bar),
    *reversed(_offset_curve(lower_spine, -half_bar)),
]

# Draw all connecting link bars in ROSE_PINK with DARK borders
# (Draw outlines first, then fills so the Y-junction merges seamlessly)
for bar_pts in (left_bar, upper_bar, lower_bar):
    draw_round_polyline(bar_pts, width_units=w * 2.0, color=DARK, closed=True)
for bar_pts in (left_bar, upper_bar, lower_bar):
    polygon(bar_pts, style=no_border_fill(ROSE_PINK))

# 4. Four ring nodes (ROSE_PINK outer ring with transparent center hole)
for nx, ny in (n1, n2, n3, n4):
    outer_c = _circle_pts(nx, ny, 8.0)
    inner_c = _circle_pts(nx, ny, 3.9)
    draw_compound_polygon([outer_c, inner_c], color=ROSE_PINK)
    draw_round_polyline(outer_c, width_units=w, color=DARK, closed=True)
    draw_round_polyline(inner_c, width_units=1.7, color=DARK, closed=True)

save()
