# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: couchbase."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

Icon.setup()

w = 2.0
cx, cy = 50.0, 50.0


def _arc(xc: float, yc: float, r: float, deg0: float, deg1: float, steps: int = 10) -> list[tuple[float, float]]:
    pts: list[tuple[float, float]] = []
    for i in range(steps + 1):
        a = math.radians(deg0 + (deg1 - deg0) * (i / steps))
        pts.append((xc + r * math.cos(a), yc + r * math.sin(a)))
    return pts


def _circle_pts(xc: float, yc: float, r: float, steps: int = 64) -> list[tuple[float, float]]:
    pts: list[tuple[float, float]] = []
    for i in range(steps):
        a = 2.0 * math.pi * (i / steps)
        pts.append((xc + r * math.cos(a), yc + r * math.sin(a)))
    return pts


def _quad(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    steps: int = 16,
) -> list[tuple[float, float]]:
    pts: list[tuple[float, float]] = []
    for i in range(1, steps + 1):
        t = i / steps
        mt = 1.0 - t
        pts.append((
            (mt**2) * p0[0] + 2.0 * mt * t * p1[0] + (t**2) * p2[0],
            (mt**2) * p0[1] + 2.0 * mt * t * p1[1] + (t**2) * p2[1],
        ))
    return pts


# 1. Iconic Couchbase rounded U-shaped couch cutout contour
# Left armrest x = 24.5..36.5, Right armrest x = 63.5..75.5
# Top y = 62.5, Seat y = 50.8, Bottom base y = 38.8 (curving down to 37.2 at center)
r_out = 4.8
r_in = 1.8

p_bl_end = (24.5 + r_out, 38.8)
p_br_start = (75.5 - r_out, 38.8)

couch_pts: list[tuple[float, float]] = [
    # Bottom-left outer corner arc
    *_arc(24.5 + r_out, 38.8 + r_out, r_out, 180.0, 270.0),
    # Gentle downward curve across bottom base
    *_quad(p_bl_end, (50.0, 36.2), p_br_start, 18),
    # Bottom-right outer corner arc
    *_arc(75.5 - r_out, 38.8 + r_out, r_out, 270.0, 360.0),
    # Top-right outer armrest corner arc
    *_arc(75.5 - r_out, 62.0 - r_out, r_out, 0.0, 90.0),
    # Right armrest inner top corner arc
    *_arc(63.5 + r_in, 62.5 - r_in, r_in, 90.0, 180.0, 6),
    # Right armrest inner vertical drop to seat recess
    (63.5, 50.8),
    # Gentle seat curve across middle
    *_quad((63.5, 50.8), (50.0, 51.3), (36.5, 50.8), 12),
    # Left armrest inner vertical rise & inner top corner arc
    *_arc(36.5 - r_in, 62.5 - r_in, r_in, 0.0, 90.0, 6),
    # Top-left outer armrest corner arc
    *_arc(24.5 + r_out, 62.0 - r_out, r_out, 90.0, 180.0),
]

# 2. Outer circular medallion (Colors.Red2 outer ring + Colors.Red3 inner circle) with transparent couch hole
outer_circle_pts = _circle_pts(cx, cy, 40.5, 64)
inner_circle_pts = _circle_pts(cx, cy, 34.0, 64)

polygon(outer_circle_pts, holes=[couch_pts], style=Icon.fill_style(Colors.Red2))
polygon(inner_circle_pts, holes=[couch_pts], style=Icon.fill_style(Colors.Red3))

circle((cx, cy), radius=40.5, style=Icon.stroke_style(Icon.DARK, width_units=w))
circle((cx, cy), radius=34.0, style=Icon.stroke_style(Icon.DARK, width_units=1.7))
Icon.draw_round_polyline(couch_pts, width_units=1.8, color=Icon.DARK, closed=True)

save()
