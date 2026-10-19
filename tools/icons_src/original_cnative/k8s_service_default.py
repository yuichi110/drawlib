# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: k8s_service."""

from drawlib.canvas import save
from drawlib.shapes import circle
from drawlib.utils import Icon, K8s

Icon.setup()

K8s.draw_original_heptagon()

# Orthogonal dark routing tree connecting top hub to 3 bottom pods
Icon.draw_round_segment((50.0, 64.0), (50.0, 33.0), width_units=2.0, color=Icon.DARK)
Icon.draw_round_polyline(
    [(33.0, 33.0), (33.0, 49.0), (67.0, 49.0), (67.0, 33.0)],
    width_units=2.0,
    color=Icon.DARK,
    corner_r=3.0,
)

# Top service hub circle
circle(
    (50.0, 64.0),
    radius=8.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0),
)

# Three bottom pod endpoint circles
for x_pos in (33.0, 50.0, 67.0):
    circle(
        (x_pos, 33.0),
        radius=6.5,
        style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0),
    )

save()
