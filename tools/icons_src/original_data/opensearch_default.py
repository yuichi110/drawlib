# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: opensearch."""

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


def _cubic(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    steps: int = 16,
) -> list[tuple[float, float]]:
    """Sample a cubic Bezier curve from p0 to p3 excluding p0."""
    pts: list[tuple[float, float]] = []
    for i in range(1, steps + 1):
        t = i / steps
        mt = 1.0 - t
        x = (mt**3) * p0[0] + 3 * (mt**2) * t * p1[0] + 3 * mt * (t**2) * p2[0] + (t**3) * p3[0]
        y = (mt**3) * p0[1] + 3 * (mt**2) * t * p1[1] + 3 * mt * (t**2) * p2[1] + (t**3) * p3[1]
        pts.append((x, y))
    return pts


def _svg_pt(sx: float, sy: float) -> tuple[float, float]:
    """Map 256x256 OpenSearch design space into centered 76x76 canvas area."""
    scale = 76.0 / 256.0
    return (12.0 + sx * scale, 88.0 - sy * scale)


setup_icon()

w = 1.9

# 1. Upper-left sweeping comma wave (Colors.Blue4)
upper_segs = [
    ((192.33, 152.00), (201.03, 137.80), (209.45, 118.87), (207.79, 92.37)),
    ((207.79, 92.37), (204.36, 37.47), (154.64, -4.18), (107.68, 0.33)),
    ((107.68, 0.33), (89.30, 2.10), (70.43, 17.08), (72.10, 43.92)),
    ((72.10, 43.92), (72.83, 55.58), (78.54, 62.47), (87.82, 67.76)),
    ((87.82, 67.76), (96.65, 72.80), (107.99, 75.99), (120.85, 79.60)),
    ((120.85, 79.60), (136.38, 83.97), (154.40, 88.88), (168.25, 99.09)),
    ((168.25, 99.09), (184.85, 111.32), (196.20, 125.50), (192.33, 152.00)),
]

upper_pts: list[tuple[float, float]] = [_svg_pt(*upper_segs[0][0])]
for p0, p1, p2, p3 in upper_segs:
    upper_pts.extend(_cubic(_svg_pt(*p0), _svg_pt(*p1), _svg_pt(*p2), _svg_pt(*p3), steps=16))

polygon(upper_pts, style=no_border_fill(Colors.Blue4))
draw_round_polyline(upper_pts, width_units=w, color=DARK, closed=True)

# 2. Lower-right inner sweeping comma wave (Colors.Blue2), 180-deg reflection around (104, 104)
lower_pts: list[tuple[float, float]] = [_svg_pt(208.0 - upper_segs[0][0][0], 208.0 - upper_segs[0][0][1])]
for p0, p1, p2, p3 in upper_segs:
    rp0 = _svg_pt(208.0 - p0[0], 208.0 - p0[1])
    rp1 = _svg_pt(208.0 - p1[0], 208.0 - p1[1])
    rp2 = _svg_pt(208.0 - p2[0], 208.0 - p2[1])
    rp3 = _svg_pt(208.0 - p3[0], 208.0 - p3[1])
    lower_pts.extend(_cubic(rp0, rp1, rp2, rp3, steps=16))

polygon(lower_pts, style=no_border_fill(Colors.Blue2))
draw_round_polyline(lower_pts, width_units=w, color=DARK, closed=True)

# 3. Outer bottom-right concentric ring wave (Colors.Teal3)
arc_cx, arc_cy = _svg_pt(103.05, 103.05)
r_mid = 143.9 * (76.0 / 256.0)
half_t = 3.2  # 6.4 units thick capsule arc
r_in = r_mid - half_t
r_out = r_mid + half_t

arc_pts: list[tuple[float, float]] = []
steps_arc = 28
# Outer arc from 0 deg down to -90 deg
for i in range(steps_arc + 1):
    ang = math.radians(-90.0 * (i / steps_arc))
    arc_pts.append((arc_cx + r_out * math.cos(ang), arc_cy + r_out * math.sin(ang)))
# Bottom semicircular cap at -90 deg (center at (arc_cx, arc_cy - r_mid))
cap_bot_cx, cap_bot_cy = arc_cx, arc_cy - r_mid
for i in range(1, 13):
    ang = math.radians(-90.0 - 180.0 * (i / 12))
    arc_pts.append((cap_bot_cx + half_t * math.cos(ang), cap_bot_cy + half_t * math.sin(ang)))
# Inner arc from -90 deg back up to 0 deg
for i in range(1, steps_arc + 1):
    ang = math.radians(-90.0 + 90.0 * (i / steps_arc))
    arc_pts.append((arc_cx + r_in * math.cos(ang), arc_cy + r_in * math.sin(ang)))
# Top-right semicircular cap at 0 deg (center at (arc_cx + r_mid, arc_cy))
cap_top_cx, cap_top_cy = arc_cx + r_mid, arc_cy
for i in range(1, 12):
    ang = math.radians(180.0 - 180.0 * (i / 12))
    arc_pts.append((cap_top_cx + half_t * math.cos(ang), cap_top_cy + half_t * math.sin(ang)))

polygon(arc_pts, style=no_border_fill(Colors.Teal3))
draw_round_polyline(arc_pts, width_units=w, color=DARK, closed=True)

save()
