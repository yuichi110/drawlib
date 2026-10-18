# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: k8s_network_policy."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import (
    DARK,
    PASTEL_GREEN,
    WHITE,
    build_shield_half_points,
    draw_original_k8s_heptagon,
    draw_round_polyline,
    fill_style,
    setup_icon,
)

setup_icon()

draw_original_k8s_heptagon()

# Protective policy shield centered inside the heptagon
left_pts = build_shield_half_points(50.0, 24.0, 70.0, 20.0, side="left")
right_pts = build_shield_half_points(50.0, 24.0, 70.0, 20.0, side="right")
shield_pts = left_pts + list(reversed(right_pts[1:-1]))
polygon(
    shield_pts,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0),
)

# Center white policy badge circle
circle(
    (50.0, 48.5),
    radius=10.5,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0),
)

# Crisp dark checkmark inside the circle
draw_round_polyline(
    [(45.5, 48.0), (48.8, 44.8), (54.8, 51.8)],
    width_units=2.0,
    color=DARK,
)

save()
