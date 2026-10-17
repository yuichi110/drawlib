# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Server concept icon: fedora."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import (
    DARK,
    WHITE,
    draw_compound_polygon,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)

setup_icon()

w_badge = 1.9
w_f = 1.6
s = 0.95


def sc(x: float, y: float) -> tuple[float, float]:
    """Scale point around canvas center (50.0, 50.0)."""
    return (round(50.0 + (x - 50.0) * s, 2), round(50.0 + (y - 50.0) * s, 2))


# 1. Speech-bubble circular badge (radius 41.0, bottom-left corner radius 9.32)
badge_pts: list[tuple[float, float]] = [sc(18.32, 9.0)]
for i in range(55):
    ang = math.radians(-90.0 + 270.0 * (i / 54))
    badge_pts.append(sc(50.0 + 41.0 * math.cos(ang), 50.0 + 41.0 * math.sin(ang)))
for i in range(13):
    ang = math.radians(180.0 + 90.0 * (i / 12))
    badge_pts.append(sc(18.32 + 9.32 * math.cos(ang), 18.32 + 9.32 * math.sin(ang)))

polygon(badge_pts, style=no_border_fill("#526E9C"))
draw_round_polyline(badge_pts, width_units=w_badge, color=DARK, closed=True)

# 2. WHITE infinity 'f' loop (outer contour + 2 inner teardrop holes)
outer_inf: list[tuple[float, float]] = []
for i in range(49):
    ang = math.radians(90.0 + 270.0 * (i / 48))
    outer_inf.append(sc(32.64 + 19.24 * math.cos(ang), 32.64 + 19.24 * math.sin(ang)))
outer_inf.append(sc(51.88, 42.80))
for i in range(49):
    ang = math.radians(270.0 + 270.0 * (i / 48))
    outer_inf.append(sc(62.04 + 19.24 * math.cos(ang), 62.04 + 19.24 * math.sin(ang)))
outer_inf.append(sc(42.80, 51.88))

hole_bl: list[tuple[float, float]] = []
for i in range(37):
    ang = math.radians(90.0 + 270.0 * (i / 36))
    hole_bl.append(sc(32.64 + 10.16 * math.cos(ang), 32.64 + 10.16 * math.sin(ang)))
for i in range(7):
    ang = math.radians(0.0 + 90.0 * (i / 6))
    hole_bl.append(sc(41.35 + 1.45 * math.cos(ang), 41.35 + 1.45 * math.sin(ang)))

hole_tr: list[tuple[float, float]] = []
for i in range(37):
    ang = math.radians(270.0 + 270.0 * (i / 36))
    hole_tr.append(sc(62.04 + 10.16 * math.cos(ang), 62.04 + 10.16 * math.sin(ang)))
for i in range(7):
    ang = math.radians(180.0 + 90.0 * (i / 6))
    hole_tr.append(sc(53.33 + 1.45 * math.cos(ang), 53.33 + 1.45 * math.sin(ang)))

draw_compound_polygon([outer_inf, hole_bl, hole_tr], color=WHITE)

# 3. Secondary loop bridges in #6B9EE8 (left and right outer arcs)
def arc_pts(
    cx_arc: float,
    cy_arc: float,
    r_arc: float,
    start_deg: float,
    span_deg: float,
    steps: int,
) -> list[tuple[float, float]]:
    """Sample a circular arc scaled around canvas center."""
    pts: list[tuple[float, float]] = []
    for i in range(steps + 1):
        rad = math.radians(start_deg + span_deg * (i / steps))
        pts.append(sc(cx_arc + r_arc * math.cos(rad), cy_arc + r_arc * math.sin(rad)))
    return pts


left_bar_cap = arc_pts(34.72, 47.34, 4.54, 90.0, 180.0, 12)
right_bar_cap = arc_pts(59.96, 47.34, 4.54, -90.0, 180.0, 12)
bl_hook_cap = arc_pts(28.96, 18.41, 4.54, 75.5, 180.0, 12)
tr_hook_cap = arc_pts(65.72, 76.27, 4.54, -104.5, 180.0, 12)

left_bridge = [
    sc(34.72, 51.88),
    *arc_pts(32.64, 32.64, 19.24, 90.0, 165.5, 24),
    *reversed(bl_hook_cap),
    *arc_pts(32.64, 32.64, 10.16, 255.5, -165.5, 24),
    sc(34.72, 42.80),
    *reversed(left_bar_cap),
]

right_bridge = [
    sc(59.96, 42.80),
    *arc_pts(62.04, 62.04, 19.24, 270.0, 165.5, 24),
    *reversed(tr_hook_cap),
    *arc_pts(62.04, 62.04, 10.16, 435.5, -165.5, 24),
    sc(59.96, 51.88),
    *reversed(right_bar_cap),
]

polygon(left_bridge, style=no_border_fill("#6B9EE8"))
polygon(right_bridge, style=no_border_fill("#6B9EE8"))

for ring in (outer_inf, hole_bl, hole_tr):
    draw_round_polyline(ring, width_units=w_f, color=DARK, closed=True)
for cap_arc in (left_bar_cap, right_bar_cap, bl_hook_cap, tr_hook_cap):
    draw_round_polyline(cap_arc, width_units=w_f, color=DARK, closed=False)

save()
