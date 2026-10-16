# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: duckdb."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 1.9

# 1. Outer circular badge (Colors.Gray6)
circle(
    (50.0, 50.0),
    radius=40.5,
    style=fill_style(Colors.Gray6, border_color=DARK, border_units=w),
)

# 2. Iconic circular duck head profile on the left (Colors.Amber2)
circle(
    (40.2, 50.0),
    radius=17.0,
    style=fill_style(Colors.Amber2, border_color=DARK, border_units=1.8),
)

# 3. Rounded D-shaped duck beak on the right (Colors.Amber3)
beak_x0 = 62.7
beak_arc_cx = 70.7
beak_r = 6.2
beak_pts: list[tuple[float, float]] = [
    (beak_x0, 50.0 - beak_r),
    (beak_x0, 50.0 + beak_r),
]
steps = 20
for i in range(steps + 1):
    ang = math.radians(90.0 - 180.0 * (i / steps))
    beak_pts.append((beak_arc_cx + beak_r * math.cos(ang), 50.0 + beak_r * math.sin(ang)))

polygon(beak_pts, style=no_border_fill(Colors.Amber3))
draw_round_polyline(beak_pts, width_units=1.8, color=DARK, closed=True)

save()
