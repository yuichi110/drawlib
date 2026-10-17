# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: etcd."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    draw_compound_polygon,
    draw_round_polyline,
    fill_style,
    setup_icon,
    stroke_style,
)

setup_icon()

w = ORIG_STROKE
cx, cy = 50.0, 50.0
r_outer = 40.0
r_base = 31.0

# 8-tooth rounded gear wheel
gear_pts: list[tuple[float, float]] = []
for k in range(8):
    center_deg = k * 45.0
    # Valley arc before tooth
    for step in range(5):
        deg = center_deg - 22.5 + step * (10.5 / 4.0)
        ang = math.radians(deg)
        gear_pts.append((cx + r_base * math.cos(ang), cy + r_base * math.sin(ang)))
    # Outer tooth arc
    for step in range(5):
        deg = center_deg - 8.5 + step * (17.0 / 4.0)
        ang = math.radians(deg)
        gear_pts.append((cx + r_outer * math.cos(ang), cy + r_outer * math.sin(ang)))
    # Valley start after tooth
    ang_end = math.radians(center_deg + 12.0)
    gear_pts.append((cx + r_base * math.cos(ang_end), cy + r_base * math.sin(ang_end)))

r_hole = 21.0
hole_pts = [
    (cx + r_hole * math.cos(math.radians(360.0 * i / 64)), cy + r_hole * math.sin(math.radians(360.0 * i / 64)))
    for i in range(64)
]

draw_compound_polygon([gear_pts, hole_pts], color=PASTEL_BLUE)
draw_round_polyline(gear_pts, width_units=w, color=DARK, closed=True)
circle((cx, cy), radius=r_hole, style=stroke_style(DARK, width_units=2.4))

# Two friendly pastel green circular eyes/nodes
circle(
    (42.0, 50.0),
    radius=5.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0),
)
circle(
    (58.0, 50.0),
    radius=5.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0),
)

save()
