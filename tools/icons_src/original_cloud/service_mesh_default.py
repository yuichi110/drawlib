# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: service_mesh."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle
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
mesh_r = 32.0
angles = [90.0, 30.0, 330.0, 270.0, 210.0, 150.0]

nodes = [(cx + mesh_r * math.cos(math.radians(a)), cy + mesh_r * math.sin(math.radians(a))) for a in angles]

draw_round_polyline(nodes, width_units=2.4, color=DARK, closed=True)
for node in nodes:
    draw_round_segment((cx, cy), node, width_units=2.4, color=DARK)

circle(
    (cx, cy),
    radius=10.5,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w),
)

for idx, node in enumerate(nodes):
    node_col = PASTEL_GREEN if idx % 2 == 0 else WHITE
    circle(
        node,
        radius=7.5,
        style=fill_style(node_col, border_color=DARK, border_units=2.5),
    )

save()
