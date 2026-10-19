# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original DevOps concept icon: jira."""

import math
from typing import Any

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

Icon.setup()

w = 2.0


def _arc_pts(
    cx: float,
    cy: float,
    r: float,
    deg_start: float,
    deg_end: float,
    steps: int = 18,
) -> list[tuple[float, float]]:
    """Sample circular arc points from deg_start to deg_end inclusive."""
    pts: list[tuple[float, float]] = []
    for i in range(steps + 1):
        ang = math.radians(deg_start + (deg_end - deg_start) * (i / steps))
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts


def _build_chevron(
    x_right: float,
    y_top: float,
    size: float = 40.0,
    arm_w: float = 16.5,
    r_tr: float = 3.2,
) -> list[tuple[float, float]]:
    """Build a Jira cascading boomerang chevron with top-right corner at (x_right, y_top)."""
    x_left = x_right - size
    y_bot = y_top - size
    return [
        # Top-right rounded corner (90 deg down to 0 deg)
        *_arc_pts(x_right - r_tr, y_top - r_tr, r_tr, 90.0, 0.0, steps=8),
        # Bottom-right curved leg tip (270 deg back to 180 deg)
        *_arc_pts(x_right, y_bot + arm_w, arm_w, 270.0, 180.0, steps=18),
        # Inner L-step
        (x_right - arm_w, y_top - arm_w),
        # Top-left curved arm tip (270 deg back to 180 deg)
        *_arc_pts(x_left + arm_w, y_top, arm_w, 270.0, 180.0, steps=18),
    ]


chevrons: list[tuple[list[tuple[float, float]], Any]] = [
    (_build_chevron(51.0, 51.0), Colors.Blue4),
    (_build_chevron(69.8, 69.8), Colors.Blue3),
    (_build_chevron(88.6, 88.6), Colors.Blue2),
]

for pts, col in chevrons:
    polygon(pts, style=Icon.no_border_fill(col))
    Icon.draw_round_polyline(pts, width_units=w, color=Icon.DARK, closed=True)

save()
