# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original AI concept icon: haystack."""

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

setup_icon()

w = 1.9


def _rounded_square_pts(
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    r: float,
    steps: int = 14,
) -> list[tuple[float, float]]:
    """Generate smooth rounded square vertices."""
    corners = [
        (x1 - r, y1 - r, 0.0, 90.0),
        (x0 + r, y1 - r, 90.0, 180.0),
        (x0 + r, y0 + r, 180.0, 270.0),
        (x1 - r, y0 + r, 270.0, 360.0),
    ]
    pts: list[tuple[float, float]] = []
    for cx, cy, deg0, deg1 in corners:
        for i in range(steps + 1):
            ang = math.radians(deg0 + (deg1 - deg0) * (i / steps))
            pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts


# 1. Outer rounded square badge (Colors.Blue3)
badge_pts = _rounded_square_pts(10.5, 10.5, 89.5, 89.5, r=12.0)
polygon(badge_pts, style=no_border_fill(Colors.Blue3))
draw_round_polyline(badge_pts, width_units=w, color=DARK, closed=True)

# 2. Stylized geometric "h" / chair tuning stem (WHITE)
h_stem_pts = [
    (36.8, 38.2),
    (42.2, 38.2),
    (42.2, 49.4),
    (57.8, 49.4),
    (57.8, 29.8),
    (63.2, 29.8),
    (63.2, 54.6),
    (42.2, 54.6),
    (42.2, 70.2),
    (36.8, 70.2),
]
polygon(h_stem_pts, style=no_border_fill(WHITE))
draw_round_polyline(h_stem_pts, width_units=1.7, color=DARK, closed=True)

# 3. Dot below left stem (WHITE)
circle(
    (39.5, 32.3),
    radius=2.9,
    style=fill_style(WHITE, border_color=DARK, border_units=1.7),
)

save()
