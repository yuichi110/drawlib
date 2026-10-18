# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original DevOps concept icon: sonarqube."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 2.0
cx, cy = 10.5, 10.5


def _curved_pill(
    r_mid: float,
    thickness: float,
    deg_start: float,
    deg_end: float,
    arc_steps: int = 40,
    cap_steps: int = 16,
) -> list[tuple[float, float]]:
    """Build a smooth rounded-cap circular arc band around (cx, cy)."""
    r_cap = thickness / 2.0
    r_in = r_mid - r_cap
    r_out = r_mid + r_cap
    pts: list[tuple[float, float]] = []

    # Outer arc from deg_start to deg_end
    for i in range(arc_steps + 1):
        a = math.radians(deg_start + (deg_end - deg_start) * (i / arc_steps))
        pts.append((cx + r_out * math.cos(a), cy + r_out * math.sin(a)))

    # Rounded end cap at deg_end (CCW from deg_end to deg_end + 180)
    a_end = math.radians(deg_end)
    end_cx = cx + r_mid * math.cos(a_end)
    end_cy = cy + r_mid * math.sin(a_end)
    for i in range(1, cap_steps):
        a = math.radians(deg_end + 180.0 * (i / cap_steps))
        pts.append((end_cx + r_cap * math.cos(a), end_cy + r_cap * math.sin(a)))

    # Inner arc from deg_end back to deg_start
    for i in range(arc_steps + 1):
        a = math.radians(deg_end + (deg_start - deg_end) * (i / arc_steps))
        pts.append((cx + r_in * math.cos(a), cy + r_in * math.sin(a)))

    # Rounded start cap at deg_start (CCW from deg_start + 180 to deg_start + 360)
    a_start = math.radians(deg_start)
    start_cx = cx + r_mid * math.cos(a_start)
    start_cy = cy + r_mid * math.sin(a_start)
    for i in range(1, cap_steps):
        a = math.radians(deg_start + 180.0 + 180.0 * (i / cap_steps))
        pts.append((start_cx + r_cap * math.cos(a), start_cy + r_cap * math.sin(a)))

    return pts


# Three concentric sonar arcs (inner, middle, outer)
arcs = [
    (64.0, 5.6, 4.0, 86.0, Colors.Blue3),
    (76.2, 5.0, 19.5, 70.5, Colors.Blue2),
    (87.8, 4.4, 32.5, 57.5, Colors.Blue3),
]

for r_mid, thick, deg0, deg1, col in arcs:
    band_pts = _curved_pill(r_mid, thick, deg0, deg1)
    polygon(band_pts, style=no_border_fill(col))
    draw_round_polyline(band_pts, width_units=w, color=DARK, closed=True)

save()
