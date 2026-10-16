# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: dbt."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    WHITE,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 1.9
cx, cy = 50.0, 50.0


def _arc(xc: float, yc: float, r: float, deg0: float, deg1: float, steps: int = 16) -> list[tuple[float, float]]:
    pts: list[tuple[float, float]] = []
    for i in range(steps + 1):
        a = math.radians(deg0 + (deg1 - deg0) * (i / steps))
        pts.append((xc + r * math.cos(a), yc + r * math.sin(a)))
    return pts


def _cubic(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    steps: int = 18,
) -> list[tuple[float, float]]:
    pts: list[tuple[float, float]] = []
    for i in range(1, steps + 1):
        t = i / steps
        mt = 1.0 - t
        pts.append((
            (mt**3) * p0[0] + 3.0 * (mt**2) * t * p1[0] + 3.0 * mt * (t**2) * p2[0] + (t**3) * p3[0],
            (mt**3) * p0[1] + 3.0 * (mt**2) * t * p1[1] + 3.0 * mt * (t**2) * p2[1] + (t**3) * p3[1],
        ))
    return pts


def _rot180(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(100.0 - x, 100.0 - y) for x, y in pts]


# Left boomerang (Top-Left + Bottom-Left lobes) with exact dbt propeller hook
# Lobe centers at (21.5, 78.5) and (21.5, 21.5), radius 9.8
r_lobe = 9.8
left_half: list[tuple[float, float]] = [
    # Top-Left lobe arc (from top-right tangent 60 deg CCW to bottom-left tangent 210 deg)
    *_arc(21.5, 78.5, r_lobe, 60.0, 210.0, 16),
    # Smooth concave left waist curve down to Bottom-Left lobe (meets at 150 deg)
    *_cubic((13.01, 73.60), (27.5, 56.5), (27.5, 43.5), (13.01, 26.40), 20),
    # Bottom-Left lobe arc (150 deg CCW to 300 deg exact tangent for +30 deg line!)
    *_arc(21.5, 21.5, r_lobe, 150.0, 300.0, 16)[1:],
    # Straight lower-left edge rising at exact +30 deg from (26.40, 13.01) to (44.20, 23.29)
    (44.20, 23.29),
    # Concave hook curve up-left to diagonal seam start (38.50, 33.30)
    *_cubic((44.20, 23.29), (40.5, 26.5), (38.8, 29.8), (38.50, 33.30), 10),
    # Straight diagonal seam across center to top-right hook tip (61.50, 66.70)
    (61.50, 66.70),
]

right_half = _rot180(left_half)

# 1. Draw both interlocking propeller halves (Colors.Orange3 left, Colors.Red3 right)
polygon(right_half, style=no_border_fill(Colors.Red3))
polygon(left_half, style=no_border_fill(Colors.Orange3))

draw_round_polyline(right_half, width_units=w, color=DARK, closed=True)
draw_round_polyline(left_half, width_units=w, color=DARK, closed=True)

# 2. Central rounded diamond cutout hole (WHITE, rotated 45 deg)
rectangle(
    (cx, cy),
    width=11.0,
    height=11.0,
    style=fill_style(WHITE, border_color=DARK, border_units=1.8, shape_r=2.0, angle=45.0),
)

save()
