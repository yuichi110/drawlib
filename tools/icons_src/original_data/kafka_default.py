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
    WHITE,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
)


def _draw_spoke_bar(
    p1: tuple[float, float],
    p2: tuple[float, float],
    width_units: float,
    fill_color: Any,
) -> None:
    """Draw a clean rectangular spoke bar connecting two ring centers."""
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dist = math.hypot(dx, dy)
    nx = -dy / dist * (width_units / 2.0)
    ny = dx / dist * (width_units / 2.0)
    pts = [
        (p1[0] + nx, p1[1] + ny),
        (p2[0] + nx, p2[1] + ny),
        (p2[0] - nx, p2[1] - ny),
        (p1[0] - nx, p1[1] - ny),
    ]
    polygon(pts, style=no_border_fill(fill_color))
    draw_round_polyline(pts, width_units=1.8, color=DARK, closed=True)


setup_icon()

w = 1.9

hub_xy = (39.0, 50.0)
spoke_dist = 29.0

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

# 1. Draw the 4 connecting spokes behind all rings
for sat_xy, _ in sat_coords:
    _draw_spoke_bar(hub_xy, sat_xy, width_units=6.0, fill_color=Colors.Gray4)

# 2. Central hub ring (Colors.Gray6 outer + WHITE inner hole)
circle(
    hub_xy,
    radius=14.0,
    style=fill_style(Colors.Gray6, border_color=DARK, border_units=w),
)
circle(
    hub_xy,
    radius=6.6,
    style=fill_style(WHITE, border_color=DARK, border_units=1.7),
)

# 3. Four satellite ring nodes
for sat_xy, sat_col in sat_coords:
    circle(
        sat_xy,
        radius=10.6,
        style=fill_style(sat_col, border_color=DARK, border_units=w),
    )
    circle(
        sat_xy,
        radius=4.8,
        style=fill_style(WHITE, border_color=DARK, border_units=1.7),
    )

save()
