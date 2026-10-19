# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Workspace concept icon: erp."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, regularpolygon
from drawlib.utils import Icon

Icon.setup()

w_outer = 2.0
w_inner = 1.6

cx_hub, cy_hub = 50.0, 45.5
orbit_r = 29.5

satellites = [
    # (angle_deg, fill_color, inner_fill)
    (90.0, Icon.PASTEL_GREEN, Icon.WHITE),
    (210.0, Icon.PASTEL_BLUE_LIGHT, Icon.WHITE),
    (330.0, Icon.WHITE, Icon.PASTEL_BLUE_LIGHT),
]

sat_coords: list[tuple[float, float, str, str]] = []
for ang_deg, col, inner_col in satellites:
    rad = math.radians(ang_deg)
    sx = cx_hub + orbit_r * math.cos(rad)
    sy = cy_hub + orbit_r * math.sin(rad)
    sat_coords.append((sx, sy, col, inner_col))

# 1. Three symmetric DARK spokes connecting hub to satellite modules
for sx, sy, _, _ in sat_coords:
    Icon.draw_round_segment((cx_hub, cy_hub), (sx, sy), width_units=w_outer, color=Icon.DARK)

# 2. Central hexagonal hub (PASTEL_BLUE, pointy-top)
regularpolygon(
    (cx_hub, cy_hub),
    radius=16.0,
    num_vertex=6,
    style=Icon.fill_style(
        Icon.PASTEL_BLUE,
        border_color=Icon.DARK,
        border_units=w_outer,
        shape_r=2.5,
        angle=30.0,
    ),
)
circle(
    (cx_hub, cy_hub),
    radius=5.5,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_inner),
)

# 3. Three connected satellite module nodes around the hub
for sx, sy, col, inner_col in sat_coords:
    circle(
        (sx, sy),
        radius=11.0,
        style=Icon.fill_style(col, border_color=Icon.DARK, border_units=w_outer),
    )
    circle(
        (sx, sy),
        radius=4.0,
        style=Icon.fill_style(inner_col, border_color=Icon.DARK, border_units=w_inner),
    )

save()
