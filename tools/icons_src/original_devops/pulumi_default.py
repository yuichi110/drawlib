# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original DevOps concept icon: pulumi."""

import math
from typing import Any

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import Icon


def _iso_ellipse_pts(
    cx: float,
    cy: float,
    rx: float,
    ry: float,
    angle_deg: float,
    steps: int = 60,
) -> list[tuple[float, float]]:
    """Sample a rotated ellipse centered at (cx, cy) with semi-axes rx, ry."""
    rad = math.radians(angle_deg)
    ca, sa = math.cos(rad), math.sin(rad)
    pts: list[tuple[float, float]] = []
    for i in range(steps):
        t = 2.0 * math.pi * (i / steps)
        lx = rx * math.cos(t)
        ly = ry * math.sin(t)
        pts.append((cx + lx * ca - ly * sa, cy + lx * sa + ly * ca))
    return pts


Icon.setup()

w_ellipse = 2.0

# Isometric circle projections (rx / ry = sqrt(3))
rx = 10.1
ry = rx / math.sqrt(3.0)

# Step vectors along the 3 isometric axes (step length = 22.8)
s = 22.8
dx = s * math.cos(math.radians(30.0))  # 19.745
dy = s * math.sin(math.radians(30.0))  # 11.4

# Top 4 ellipses (Colors.Amber3, horizontal 0 deg)
top_centers = [
    (50.0, 83.2),
    (50.0 - dx, 83.2 - dy),
    (50.0 + dx, 83.2 - dy),
    (50.0, 83.2 - 2.0 * dy),
]

# Left 4 ellipses (Colors.Pink3, tilted -60 deg)
left_centers = [
    (50.0 - 1.5 * dx, 54.7),
    (50.0 - 1.5 * dx, 54.7 - s),
    (50.0 - 0.5 * dx, 54.7 - dy),
    (50.0 - 0.5 * dx, 54.7 - dy - s),
]

# Right 4 ellipses (Colors.Purple3, tilted +60 deg)
right_centers = [
    (50.0 + 1.5 * dx, 54.7),
    (50.0 + 1.5 * dx, 54.7 - s),
    (50.0 + 0.5 * dx, 54.7 - dy),
    (50.0 + 0.5 * dx, 54.7 - dy - s),
]

groups: list[tuple[list[tuple[float, float]], float, Any]] = [
    (left_centers, -60.0, Colors.Pink3),
    (right_centers, 60.0, Colors.Purple3),
    (top_centers, 0.0, Colors.Amber3),
]

for centers, ang, col in groups:
    for ex, ey in centers:
        pts = _iso_ellipse_pts(ex, ey, rx, ry, ang)
        polygon(pts, style=Icon.no_border_fill(col))
        Icon.draw_round_polyline(pts, width_units=w_ellipse, color=Icon.DARK, closed=True)

save()
