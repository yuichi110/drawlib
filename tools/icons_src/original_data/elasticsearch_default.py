# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: elasticsearch."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import Icon


def _arc_points(
    cx: float,
    cy: float,
    radius: float,
    deg_start: float,
    deg_end: float,
    steps: int = 28,
) -> list[tuple[float, float]]:
    """Sample circular arc points from deg_start to deg_end inclusive."""
    pts: list[tuple[float, float]] = []
    for i in range(steps + 1):
        t = i / steps
        ang = math.radians(deg_start + (deg_end - deg_start) * t)
        pts.append((cx + radius * math.cos(ang), cy + radius * math.sin(ang)))
    return pts


def _bezier(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    steps: int = 14,
) -> list[tuple[float, float]]:
    """Sample cubic Bezier curve excluding p0."""
    pts: list[tuple[float, float]] = []
    for i in range(1, steps + 1):
        t = i / steps
        mt = 1.0 - t
        x = (mt**3) * p0[0] + 3 * (mt**2) * t * p1[0] + 3 * mt * (t**2) * p2[0] + (t**3) * p3[0]
        y = (mt**3) * p0[1] + 3 * (mt**2) * t * p1[1] + 3 * mt * (t**2) * p2[1] + (t**3) * p3[1]
        pts.append((x, y))
    return pts


Icon.setup()

w = 2.0
cx, cy = 50.0, 50.0
r = 40.0

# 1. Top dome (Colors.Amber3): chord at y = 66.5 with curved right lip up to 36 deg
y_top_chord = 66.5
ang_top_l = math.degrees(math.asin((y_top_chord - cy) / r))  # ~24.36 deg -> 155.64 deg on left
deg_tl = 180.0 - ang_top_l
deg_tr = 36.0
p_tr_outer = (cx + r * math.cos(math.radians(deg_tr)), cy + r * math.sin(math.radians(deg_tr)))
p_tr_flat_end = (69.5, y_top_chord)

top_dome_pts = [
    *_arc_points(cx, cy, r, deg_tr, deg_tl, steps=32),
    p_tr_flat_end,
    *_bezier(p_tr_flat_end, (74.5, y_top_chord), (79.0, 69.0), p_tr_outer, steps=12),
]
polygon(top_dome_pts, style=Icon.no_border_fill(Colors.Amber3))
Icon.draw_round_polyline(top_dome_pts, width_units=w, color=Icon.DARK, closed=True)

# 3. Bottom dome (Colors.Teal3): mirror of top dome across cy = 50.0
y_bot_chord = 33.5
deg_bl = 180.0 + ang_top_l
deg_br = 360.0 - deg_tr
p_br_outer = (cx + r * math.cos(math.radians(deg_br)), cy + r * math.sin(math.radians(deg_br)))
p_br_flat_end = (69.5, y_bot_chord)

bot_dome_pts = [
    *_arc_points(cx, cy, r, deg_bl, deg_br, steps=32),
    *_bezier(p_br_outer, (79.0, 31.0), (74.5, y_bot_chord), p_br_flat_end, steps=12),
]
polygon(bot_dome_pts, style=Icon.no_border_fill(Colors.Teal3))
Icon.draw_round_polyline(bot_dome_pts, width_units=w, color=Icon.DARK, closed=True)

# 4. Horizontal middle bar (Colors.Blue4): flush with left circle arc, semicircular right cap
bar_half_h = 9.5
ang_bar = math.degrees(math.asin(bar_half_h / r))  # ~13.74 deg
deg_bar_top = 180.0 - ang_bar
deg_bar_bot = 180.0 + ang_bar
bar_cap_cx = 61.5

mid_bar_pts = [
    *_arc_points(cx, cy, r, deg_bar_top, deg_bar_bot, steps=14),
    *_arc_points(bar_cap_cx, cy, bar_half_h, -90.0, 90.0, steps=20),
]
polygon(mid_bar_pts, style=Icon.no_border_fill(Colors.Blue4))
Icon.draw_round_polyline(mid_bar_pts, width_units=w, color=Icon.DARK, closed=True)

save()
