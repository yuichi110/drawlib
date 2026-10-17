# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original DevOps concept icon: cypress."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    draw_compound_polygon,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 1.7
cx, cy = 50.0, 50.0


def _circle_pts(xc: float, yc: float, r: float, steps: int = 72) -> list[tuple[float, float]]:
    """Sample a closed circle polygon."""
    return [
        (xc + r * math.cos(2.0 * math.pi * i / steps), yc + r * math.sin(2.0 * math.pi * i / steps))
        for i in range(steps)
    ]


# 1. Circular ring (Colors.Green2) with transparent interior
r_out = 40.0
r_in = 34.4
outer_ring = _circle_pts(cx, cy, r_out, 80)
inner_ring = _circle_pts(cx, cy, r_in, 80)

draw_compound_polygon([outer_ring, inner_ring], color=Colors.Green2)
draw_round_polyline(outer_ring, width_units=w, color=DARK, closed=True)
draw_round_polyline(inner_ring, width_units=w, color=DARK, closed=True)


# 2. Crisp geometric 'c' and 'y' letterpaths inside (Colors.Gray6)
# Build 'c' as a clean circular C-band centered at (37.2, 52.8)
ccx, ccy = 37.2, 52.8
c_rout = 12.2
c_rin = 7.3
c_pts: list[tuple[float, float]] = []
# Outer arc of 'c' from 32 deg CCW to 328 deg
for i in range(49):
    deg = 32.0 + (328.0 - 32.0) * (i / 48)
    a = math.radians(deg)
    c_pts.append((ccx + c_rout * math.cos(a), ccy + c_rout * math.sin(a)))
# Inner arc of 'c' from 328 deg CW back to 32 deg
for i in range(49):
    deg = 328.0 - (328.0 - 32.0) * (i / 48)
    a = math.radians(deg)
    c_pts.append((ccx + c_rin * math.cos(a), ccy + c_rin * math.sin(a)))

polygon(c_pts, style=no_border_fill(Colors.Gray6))
draw_round_polyline(c_pts, width_units=w, color=DARK, closed=True)

# Build 'y' as a clean geometric sans-serif polygon next to 'c'
y_pts: list[tuple[float, float]] = [
    (49.2, 64.5),
    (54.8, 64.5),
    (61.5, 47.6),
    (68.2, 64.5),
    (73.8, 64.5),
    (58.8, 27.6),
    (53.2, 27.6),
    (58.7, 41.0),
]
polygon(y_pts, style=no_border_fill(Colors.Gray6))
draw_round_polyline(y_pts, width_units=w, color=DARK, closed=True)

save()
