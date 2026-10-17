# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original DevOps concept icon: ansible."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    WHITE,
    draw_compound_polygon,
    draw_round_polyline,
    fill_style,
    setup_icon,
)


def _scale_pt(pt: tuple[float, float], s: float = 0.96) -> tuple[float, float]:
    """Scale point around (50, 50) by factor s."""
    return (50.0 + (pt[0] - 50.0) * s, 50.0 + (pt[1] - 50.0) * s)


def _arc_pts(
    cx: float,
    cy: float,
    r: float,
    deg_start: float,
    deg_end: float,
    steps: int = 16,
) -> list[tuple[float, float]]:
    """Sample circular arc points from deg_start to deg_end inclusive."""
    pts: list[tuple[float, float]] = []
    for i in range(steps + 1):
        t = i / steps
        ang = math.radians(deg_start + (deg_end - deg_start) * t)
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts


setup_icon()

w = 1.9
w_glyph = 1.6

# 1. Circular badge in Colors.Gray6
circle(
    (50.0, 50.0),
    radius=39.0,
    style=fill_style(Colors.Gray6, border_color=DARK, border_units=w),
)

# 2. Geometric WHITE 'A' glyph (outer silhouette + inner triangular hole)
top_arc = _arc_pts(50.70, 72.08, 2.65, 22.0, 158.0, steps=16)
foot_arc = _arc_pts(66.80, 32.55, 2.98, -132.0, 22.0, steps=18)

raw_outer: list[tuple[float, float]] = [
    *top_arc,
    (30.16, 29.96),
    (36.31, 29.96),
    (43.39, 47.69),
    *foot_arc,
]
raw_hole: list[tuple[float, float]] = [
    (50.66, 65.94),
    (61.24, 39.75),
    (45.30, 52.38),
]

a_outer = [_scale_pt(p, 0.96) for p in raw_outer]
a_hole = [_scale_pt(p, 0.96) for p in raw_hole]

draw_compound_polygon([a_outer, a_hole], color=WHITE)
draw_round_polyline(a_outer, width_units=w_glyph, color=DARK, closed=True)
draw_round_polyline(a_hole, width_units=w_glyph, color=DARK, closed=True)

save()
