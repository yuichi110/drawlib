# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: kafka."""

import math
from typing import Any

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    draw_compound_polygon,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
    stroke_style,
)


def _circle_pts(xc: float, yc: float, r: float, steps: int = 48) -> list[tuple[float, float]]:
    """Sample full circle polygon around (xc, yc) with radius r."""
    pts: list[tuple[float, float]] = []
    for i in range(steps):
        a = 2.0 * math.pi * (i / steps)
        pts.append((xc + r * math.cos(a), yc + r * math.sin(a)))
    return pts


def _draw_spoke_bar(
    hub_center: tuple[float, float],
    sat_center: tuple[float, float],
    r_hub_trim: float,
    r_sat_trim: float,
    width_units: float,
    fill_color: Any,
) -> None:
    """Draw a trimmed rectangular spoke bar between solid ring bands."""
    dx = sat_center[0] - hub_center[0]
    dy = sat_center[1] - hub_center[1]
    dist = math.hypot(dx, dy)
    ux = dx / dist
    uy = dy / dist
    p1 = (hub_center[0] + ux * r_hub_trim, hub_center[1] + uy * r_hub_trim)
    p2 = (sat_center[0] - ux * r_sat_trim, sat_center[1] - uy * r_sat_trim)
    nx = -uy * (width_units / 2.0)
    ny = ux * (width_units / 2.0)
    pts = [
        (p1[0] + nx, p1[1] + ny),
        (p2[0] + nx, p2[1] + ny),
        (p2[0] - nx, p2[1] - ny),
        (p1[0] - nx, p1[1] - ny),
    ]
    polygon(pts, style=no_border_fill(fill_color))
    draw_round_polyline(pts, width_units=1.8, color=DARK, closed=True)


setup_icon()

w = 2.0

hub_xy = (39.0, 50.0)
spoke_dist = 29.0
r_hub_trim = 10.3
r_sat_trim = 7.7

satellites = [
    (90.0, Colors.Gray6),
    (30.0, Colors.Gray5),
    (-30.0, Colors.Gray5),
    (-90.0, Colors.Gray6),
]

sat_coords: list[tuple[tuple[float, float], Any]] = []
for ang_deg, col in satellites:
    ang = math.radians(ang_deg)
    sx = hub_xy[0] + spoke_dist * math.cos(ang)
    sy = hub_xy[1] + spoke_dist * math.sin(ang)
    sat_coords.append(((sx, sy), col))

# 1. Draw the 4 connecting spokes behind all rings (trimmed to solid bands)
for sat_xy, _ in sat_coords:
    _draw_spoke_bar(hub_xy, sat_xy, r_hub_trim, r_sat_trim, width_units=6.0, fill_color=Colors.Gray4)

# 2. Central hub ring (Colors.Gray6 outer + transparent inner hole)
draw_compound_polygon([_circle_pts(*hub_xy, 14.0), _circle_pts(*hub_xy, 6.6)], color=Colors.Gray6)
circle(hub_xy, radius=14.0, style=stroke_style(DARK, width_units=w))
circle(hub_xy, radius=6.6, style=stroke_style(DARK, width_units=1.7))

# 3. Four satellite ring nodes (transparent inner holes)
for sat_xy, sat_col in sat_coords:
    draw_compound_polygon([_circle_pts(*sat_xy, 10.6), _circle_pts(*sat_xy, 4.8)], color=sat_col)
    circle(sat_xy, radius=10.6, style=stroke_style(DARK, width_units=w))
    circle(sat_xy, radius=4.8, style=stroke_style(DARK, width_units=1.7))

save()
