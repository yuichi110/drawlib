# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: superset."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 1.9
cy = 50.0
r_out = 20.5
r_in = 8.5
s45 = math.sqrt(0.5)

# Exact center offset so +/-45 deg crossing bands connect tangentially to both lobes
d = (r_out + r_in) * s45  # 20.506
cx_l = 50.0 - d
cx_r = 50.0 + d
v_off = (r_out - r_in) * s45  # 8.485 (half-diagonal of central crossing diamond)


def _arc_pts(
    cx: float,
    cy: float,
    r: float,
    deg_start: float,
    deg_end: float,
    steps: int = 28,
) -> list[tuple[float, float]]:
    """Sample circular arc points from deg_start to deg_end."""
    pts: list[tuple[float, float]] = []
    for i in range(steps + 1):
        ang = math.radians(deg_start + (deg_end - deg_start) * (i / steps))
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts


# 1. Exact outer infinity silhouette with top/bottom crossing valleys (Colors.Teal3 base)
outer_loop = [
    (50.0, cy + v_off),
    *_arc_pts(cx_l, cy, r_out, 45.0, 315.0, 36),
    (50.0, cy - v_off),
    *_arc_pts(cx_r, cy, r_out, 225.0, 495.0, 36),
]
polygon(outer_loop, style=no_border_fill(Colors.Teal3))

# 2. Under-strand accent segments (Colors.Gray5) flanking the central crossing
# Top-left accent segment (between 82 deg on left lobe and the over-strand top-left edge)
tl_accent = [
    *_arc_pts(cx_l, cy, r_out, 82.0, 45.0, 8),
    (50.0, cy + v_off),
    (50.0 - v_off, cy),
    *_arc_pts(cx_l, cy, r_in, 45.0, 82.0, 8),
]
polygon(tl_accent, style=no_border_fill(Colors.Gray5))

# Bottom-right accent segment (between the over-strand bottom-right edge and 262 deg on right lobe)
br_accent = [
    (50.0 + v_off, cy),
    *_arc_pts(cx_r, cy, r_in, 225.0, 262.0, 8),
    *_arc_pts(cx_r, cy, r_out, 262.0, 225.0, 8),
    (50.0, cy - v_off),
]
polygon(br_accent, style=no_border_fill(Colors.Gray5))

# 3. Left and right inner teardrop holes (WHITE)
left_hole = [
    (50.0 - v_off, cy),
    *_arc_pts(cx_l, cy, r_in, 45.0, 315.0, 28),
]
right_hole = [
    (50.0 + v_off, cy),
    *_arc_pts(cx_r, cy, r_in, 135.0, -135.0, 28),
]
polygon(left_hole, style=no_border_fill(WHITE))
polygon(right_hole, style=no_border_fill(WHITE))

# 4. Internal seam lines for accent bands and over-strand crossing
draw_round_segment(
    (cx_l + r_in * math.cos(math.radians(82.0)), cy + r_in * math.sin(math.radians(82.0))),
    (cx_l + r_out * math.cos(math.radians(82.0)), cy + r_out * math.sin(math.radians(82.0))),
    width_units=1.7,
    color=DARK,
)
draw_round_segment(
    (cx_r + r_in * math.cos(math.radians(262.0)), cy + r_in * math.sin(math.radians(262.0))),
    (cx_r + r_out * math.cos(math.radians(262.0)), cy + r_out * math.sin(math.radians(262.0))),
    width_units=1.7,
    color=DARK,
)
# Over-strand crossing edges across the middle diamond
draw_round_segment((50.0 - v_off, cy), (50.0, cy + v_off), width_units=1.8, color=DARK)
draw_round_segment((50.0, cy - v_off), (50.0 + v_off, cy), width_units=1.8, color=DARK)

# 5. Inner hole outlines and outer infinity silhouette outline
draw_round_polyline(left_hole, width_units=1.8, color=DARK, closed=True)
draw_round_polyline(right_hole, width_units=1.8, color=DARK, closed=True)
draw_round_polyline(outer_loop, width_units=w, color=DARK, closed=True)

save()
