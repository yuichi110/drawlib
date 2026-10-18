# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: transit_hub."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

cx, cy = 50.0, 50.0
spoke_r = 29.5
angles_deg = (0, 60, 120, 180, 240, 300)

spoke_pts = [
    (
        cx + spoke_r * math.cos(math.radians(ang)),
        cy + spoke_r * math.sin(math.radians(ang)),
    )
    for ang in angles_deg
]

# 6 radial spoke lines
for nx, ny in spoke_pts:
    draw_round_segment((cx, cy), (nx, ny), width_units=w, color=DARK)

# Central hexagonal transit hub
hub_r = 16.0
hex_pts = [
    (
        cx + hub_r * math.cos(math.radians(ang)),
        cy + hub_r * math.sin(math.radians(ang)),
    )
    for ang in angles_deg
]
polygon(hex_pts, style=fill_style(PASTEL_GREEN))
draw_round_polyline(hex_pts, width_units=w, color=DARK, closed=True)

circle(
    (cx, cy),
    radius=6.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0),
)

# 6 outer network spoke nodes alternating PASTEL_BLUE and WHITE
for idx, (nx, ny) in enumerate(spoke_pts):
    fill_col = PASTEL_BLUE if idx % 2 == 0 else WHITE
    circle(
        (nx, ny),
        radius=8.2,
        style=fill_style(fill_col, border_color=DARK, border_units=w),
    )

save()
