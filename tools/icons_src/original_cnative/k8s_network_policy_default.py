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
from drawlib.utils import Icon, K8s

Icon.setup()

K8s.draw_original_heptagon()

# Protective policy shield centered inside the heptagon
left_pts = Icon.build_shield_half_points(50.0, 24.0, 70.0, 20.0, side="left")
right_pts = Icon.build_shield_half_points(50.0, 24.0, 70.0, 20.0, side="right")
shield_pts = left_pts + list(reversed(right_pts[1:-1]))
polygon(
    shield_pts,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0),
)

# Center white policy badge circle
circle(
    (50.0, 48.5),
    radius=10.5,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0),
)

# Crisp dark checkmark inside the circle
Icon.draw_round_polyline(
    [(45.5, 48.0), (48.8, 44.8), (54.8, 51.8)],
    width_units=2.0,
    color=Icon.DARK,
)

save()
