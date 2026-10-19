# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: virtualization_controller."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

# Branching orchestration lines from console to 3 managed VM nodes
Icon.draw_round_segment((50.0, 48.0), (50.0, 24.0), width_units=w, color=Icon.DARK)
Icon.draw_round_polyline(
    [(24.0, 24.0), (24.0, 39.0), (76.0, 39.0), (76.0, 24.0)],
    width_units=w,
    color=Icon.DARK,
    corner_r=4.0,
)

# Top central management console frame
rectangle(
    (50.0, 66.0),
    width=54.0,
    height=36.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w, shape_r=6.0),
)

# Control gear inside the management console
cx_g, cy_g = 50.0, 66.0
r_outer = 12.0
r_inner = 9.0
teeth = 8
gear_pts: list[tuple[float, float]] = []
for i in range(teeth):
    base_deg = i * (360.0 / teeth)
    for offset_deg, rad in (
        (-13.0, r_inner),
        (-7.5, r_outer),
        (7.5, r_outer),
        (13.0, r_inner),
    ):
        ang = math.radians(base_deg + offset_deg)
        gear_pts.append((cx_g + rad * math.cos(ang), cy_g + rad * math.sin(ang)))

polygon(gear_pts, style=Icon.fill_style(Icon.PASTEL_GREEN))
Icon.draw_round_polyline(gear_pts, width_units=2.0, color=Icon.DARK, closed=True)
circle(
    (cx_g, cy_g),
    radius=4.2,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0),
)

# 3 managed VM / host cubes below
for x_node in (24.0, 50.0, 76.0):
    Icon.draw_iso_cube(
        x_node,
        23.0,
        radius=11.0,
        top_color=Icon.WHITE,
        left_color=Icon.PASTEL_BLUE,
        right_color=Icon.PASTEL_GREEN,
        border_color=Icon.DARK,
        border_units=2.0,
    )

save()
