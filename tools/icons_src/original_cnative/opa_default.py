# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: opa."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import Icon

Icon.setup()

w = 2.0


def _bezier_quad(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    steps: int = 16,
) -> list[tuple[float, float]]:
    """Sample a quadratic Bezier curve from p0 to p2 with control point p1."""
    pts: list[tuple[float, float]] = []
    for i in range(steps + 1):
        t = i / steps
        mt = 1.0 - t
        bx = (mt**2) * p0[0] + 2.0 * mt * t * p1[0] + (t**2) * p2[0]
        by = (mt**2) * p0[1] + 2.0 * mt * t * p1[1] + (t**2) * p2[1]
        pts.append((bx, by))
    return pts


# 1. Left & right curved Viking horns (WHITE)
left_outer = _bezier_quad((31.0, 44.0), (9.0, 56.0), (24.0, 83.0), steps=18)
left_inner = _bezier_quad((24.0, 83.0), (20.0, 62.0), (35.0, 57.0), steps=18)
left_horn = left_outer + left_inner[1:]
polygon(left_horn, style=Icon.no_border_fill(Icon.WHITE))
Icon.draw_round_polyline(left_horn, width_units=w, color=Icon.DARK, closed=True)

right_horn = [(100.0 - px, py) for px, py in left_horn]
polygon(right_horn, style=Icon.no_border_fill(Icon.WHITE))
Icon.draw_round_polyline(right_horn, width_units=w, color=Icon.DARK, closed=True)

# 2. Central helmet dome + tapered lower face guard (PASTEL_BLUE)
dome_pts: list[tuple[float, float]] = []
steps_dome = 24
for i in range(steps_dome + 1):
    ang = math.radians(180.0 - 180.0 * (i / steps_dome))
    dome_pts.append((50.0 + 22.0 * math.cos(ang), 50.0 + 22.0 * math.sin(ang)))

right_cheek = _bezier_quad((72.0, 31.0), (59.0, 26.0), (50.0, 17.0), steps=12)
left_cheek = _bezier_quad((50.0, 17.0), (41.0, 26.0), (28.0, 31.0), steps=12)
helmet_pts = dome_pts + right_cheek + left_cheek
polygon(helmet_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(helmet_pts, width_units=w, color=Icon.DARK, closed=True)

# 3. PASTEL_GREEN vertical nose guard (drawn before brow band so top tuck is clean)
rectangle(
    (50.0, 36.5),
    width=8.2,
    height=25.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0, shape_r=3.2),
)

# 4. PASTEL_GREEN horizontal brow band
rectangle(
    (50.0, 49.0),
    width=46.0,
    height=7.6,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0, shape_r=3.0),
)

# 5. Central WHITE emblem rivet at brow intersection
circle(
    (50.0, 49.0),
    radius=5.2,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0),
)

save()
