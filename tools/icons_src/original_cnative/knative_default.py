# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: knative."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE
cx, cy = 50.0, 50.0
r_hex = 40.5

# 1. Pointy-top rounded hexagon (PASTEL_BLUE)
hex_pts = [
    (
        cx + r_hex * math.cos(math.radians(90.0 - i * 60.0)),
        cy + r_hex * math.sin(math.radians(90.0 - i * 60.0)),
    )
    for i in range(6)
]
polygon(
    hex_pts,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=5.5),
)

# 2. Central WHITE geometric letter K block
k_pts = [
    (31.0, 29.0),
    (31.0, 71.0),
    (41.5, 71.0),
    (41.5, 54.5),
    (54.5, 71.0),
    (66.5, 71.0),
    (50.0, 50.0),
    (66.5, 29.0),
    (54.5, 29.0),
    (41.5, 45.5),
    (41.5, 29.0),
]
polygon(k_pts, style=no_border_fill(WHITE))
draw_round_polyline(k_pts, width_units=2.4, color=DARK, closed=True)

# 3. Right PASTEL_GREEN arrow-wing accent nested in the K opening
wing_pts = [
    (56.5, 50.0),
    (69.5, 59.5),
    (75.5, 50.0),
    (69.5, 40.5),
]
polygon(wing_pts, style=no_border_fill(PASTEL_GREEN))
draw_round_polyline(wing_pts, width_units=2.3, color=DARK, closed=True)

save()
