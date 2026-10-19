# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility concept icon: power_plant."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

Icon.setup()

w_outer = 2.0
w_inner = 1.6


def _hyperboloid_tower(
    cx: float,
    y_bot: float,
    y_top: float,
    w_bot: float,
    w_waist: float,
    w_top: float,
    waist_ratio: float = 0.68,
) -> list[tuple[float, float]]:
    y_waist = y_bot + (y_top - y_bot) * waist_ratio
    steps = 20
    left_pts: list[tuple[float, float]] = []
    right_pts: list[tuple[float, float]] = []

    p0_l = (cx - w_bot / 2.0, y_bot)
    p1_l = (cx - w_waist / 2.0 + 1.5, y_waist)
    p2_l = (cx - w_top / 2.0, y_top)

    p0_r = (cx + w_top / 2.0, y_top)
    p1_r = (cx + w_waist / 2.0 - 1.5, y_waist)
    p2_r = (cx + w_bot / 2.0, y_bot)

    for i in range(steps + 1):
        t = i / steps
        mt = 1.0 - t
        lx = (mt**2) * p0_l[0] + 2.0 * mt * t * p1_l[0] + (t**2) * p2_l[0]
        ly = (mt**2) * p0_l[1] + 2.0 * mt * t * p1_l[1] + (t**2) * p2_l[1]
        left_pts.append((lx, ly))

        rx = (mt**2) * p0_r[0] + 2.0 * mt * t * p1_r[0] + (t**2) * p2_r[0]
        ry = (mt**2) * p0_r[1] + 2.0 * mt * t * p1_r[1] + (t**2) * p2_r[1]
        right_pts.append((rx, ry))

    return left_pts + right_pts


def _top_rounded_box(x0: float, y0: float, x1: float, y1: float, r: float) -> list[tuple[float, float]]:
    pts: list[tuple[float, float]] = [(x0, y0), (x1, y0)]
    steps = 10
    for i in range(steps + 1):
        ang = math.radians(0.0 + 90.0 * (i / steps))
        pts.append((x1 - r + r * math.cos(ang), y1 - r + r * math.sin(ang)))
    for i in range(steps + 1):
        ang = math.radians(90.0 + 90.0 * (i / steps))
        pts.append((x0 + r + r * math.cos(ang), y1 - r + r * math.sin(ang)))
    return pts


# 1. Twin hyperboloid cooling towers in back (right: PASTEL_BLUE_LIGHT, center: WHITE)
tower_r = _hyperboloid_tower(73.0, 14.0, 76.0, w_bot=28.0, w_waist=15.0, w_top=20.0)
polygon(tower_r, style=Icon.no_border_fill(Icon.PASTEL_BLUE_LIGHT))
Icon.draw_round_polyline(tower_r, width_units=w_outer, color=Icon.DARK, closed=True)
Icon.draw_round_segment((63.6, 70.0), (82.4, 70.0), width_units=w_inner, color=Icon.DARK)

tower_l = _hyperboloid_tower(47.0, 14.0, 82.0, w_bot=30.0, w_waist=16.5, w_top=22.0)
polygon(tower_l, style=Icon.no_border_fill(Icon.WHITE))
Icon.draw_round_polyline(tower_l, width_units=w_outer, color=Icon.DARK, closed=True)
Icon.draw_round_segment((36.6, 75.5), (57.4, 75.5), width_units=w_inner, color=Icon.DARK)

# 2. Foreground power station turbine hall building (PASTEL_BLUE)
hall_pts = _top_rounded_box(13.0, 14.0, 61.0, 51.0, r=4.0)
polygon(hall_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(hall_pts, width_units=w_outer, color=Icon.DARK, closed=True)

# 3. PASTEL_GREEN lightning bolt emblem on turbine hall facade
bolt_pts = [
    (40.0, 46.0),
    (29.0, 31.5),
    (37.0, 31.5),
    (34.0, 19.0),
    (45.0, 33.5),
    (37.0, 33.5),
]
polygon(bolt_pts, style=Icon.no_border_fill(Icon.PASTEL_GREEN))
Icon.draw_round_polyline(bolt_pts, width_units=w_inner, color=Icon.DARK, closed=True)

# 4. Ground foundation line
Icon.draw_round_segment((11.5, 14.0), (88.5, 14.0), width_units=w_outer, color=Icon.DARK)

save()
