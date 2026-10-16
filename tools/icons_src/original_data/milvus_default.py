# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: milvus."""

import math

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


def _build_left_teardrop(cx_right: float, cy: float, r_right: float, r_tip: float) -> list[tuple[float, float]]:
    """Build an exact 45-degree left-pointing teardrop contour."""
    cx_tip = cx_right - (r_right - r_tip) * math.sqrt(2.0)
    pts: list[tuple[float, float]] = []

    steps_right = 36
    for i in range(steps_right + 1):
        ang = math.radians(-135.0 + 270.0 * (i / steps_right))
        pts.append((cx_right + r_right * math.cos(ang), cy + r_right * math.sin(ang)))

    steps_tip = 14
    for i in range(steps_tip + 1):
        ang = math.radians(135.0 + 90.0 * (i / steps_tip))
        pts.append((cx_tip + r_tip * math.cos(ang), cy + r_tip * math.sin(ang)))

    return pts


setup_icon()

w = 1.9

# 1. Outer left-pointing teardrop body (Colors.Teal2)
outer_pts = _build_left_teardrop(cx_right=47.5, cy=50.0, r_right=28.0, r_tip=2.6)
polygon(outer_pts, style=no_border_fill(Colors.Teal2))
draw_round_polyline(outer_pts, width_units=w, color=DARK, closed=True)

# 2. Inner left-pointing teardrop cutout (WHITE)
inner_pts = _build_left_teardrop(cx_right=48.2, cy=50.0, r_right=20.0, r_tip=1.8)
polygon(inner_pts, style=no_border_fill(WHITE))
draw_round_polyline(inner_pts, width_units=1.8, color=DARK, closed=True)

# 3. Central circular core (Colors.Blue3)
circle(
    (48.2, 50.0),
    radius=13.0,
    style=fill_style(Colors.Blue3, border_color=DARK, border_units=1.8),
)

# 4. Right tail wing triangle (Colors.Teal3)
tail_pts: list[tuple[float, float]] = []
# Concave left edge from top (81.5, 60.0) down to bottom (81.5, 40.0)
steps_curve = 12
for i in range(steps_curve + 1):
    t = i / steps_curve
    y = 60.0 - 20.0 * t
    x = 81.5 + 1.4 * (1.0 - (2.0 * t - 1.0) ** 2)
    tail_pts.append((x, y))

# Rounded right tip around (89.0, 50.0) with radius 1.8
r_tail_tip = 1.8
cx_tail_tip = 89.2
for i in range(10):
    ang = math.radians(-45.0 + 90.0 * (i / 9.0))
    tail_pts.append((cx_tail_tip + r_tail_tip * math.cos(ang), 50.0 + r_tail_tip * math.sin(ang)))

polygon(tail_pts, style=no_border_fill(Colors.Teal3))
draw_round_polyline(tail_pts, width_units=1.8, color=DARK, closed=True)

save()
