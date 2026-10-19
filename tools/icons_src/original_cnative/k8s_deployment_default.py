# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: k8s_deployment."""

import math

from drawlib.canvas import save
from drawlib.shapes import arc, polygon
from drawlib.utils import Icon, K8s

Icon.setup()

K8s.draw_original_heptagon()

# Central isometric workload cube
Icon.draw_iso_cube(
    50.0,
    44.0,
    radius=13.5,
    top_color=Icon.WHITE,
    left_color=Icon.PASTEL_BLUE_LIGHT,
    right_color=Icon.PASTEL_GREEN,
    border_color=Icon.DARK,
    border_units=2.0,
)

# Upper clockwise rollout arc around the cube
cx, cy, r_arc = 50.0, 45.0, 23.0
arc(
    (cx, cy),
    width=r_arc * 2.0,
    height=r_arc * 2.0,
    angle_start=20.0,
    angle_end=205.0,
    style=Icon.stroke_style(Icon.DARK, width_units=2.0),
)

# Round cap at the left tail of the arc
tail_rad = math.radians(205.0)
Icon.draw_cap(
    (cx + r_arc * math.cos(tail_rad), cy + r_arc * math.sin(tail_rad)),
    width_units=2.0,
    color=Icon.DARK,
)

# Crisp white filled arrowhead aligned tangent to the clockwise end (20 deg)
tip_rad = math.radians(20.0)
bx = cx + r_arc * math.cos(tip_rad)
by = cy + r_arc * math.sin(tip_rad)
ux, uy = math.sin(tip_rad), -math.cos(tip_rad)
nx, ny = math.cos(tip_rad), math.sin(tip_rad)
head_len, head_half_w = 8.5, 5.2
arrow_pts = [
    (bx + head_len * ux, by + head_len * uy),
    (bx - head_half_w * nx, by - head_half_w * ny),
    (bx + head_half_w * nx, by + head_half_w * ny),
]
polygon(arrow_pts, style=Icon.fill_style(Icon.WHITE))
Icon.draw_round_polyline(arrow_pts, width_units=2.0, color=Icon.DARK, closed=True)

save()
