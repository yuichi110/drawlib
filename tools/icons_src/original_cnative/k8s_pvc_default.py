# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: k8s_pvc."""

from drawlib.canvas import save
from drawlib.shapes import circle
from drawlib.utils import Icon, K8s

Icon.setup()

K8s.draw_original_heptagon()

# Slight up-right offset so the cylinder and claim badge sit centered inside the heptagon
dx, dy = 1.6, 3.5

# White storage volume cylinder
Icon.draw_cylinder_tier(
    46.0 + dx,
    38.0 + dy,
    36.0,
    17.0,
    6.0,
    body_color=Icon.WHITE,
    top_color=Icon.PASTEL_BLUE_LIGHT,
    border_color=Icon.DARK,
    border_units=2.0,
    draw_top_cap=True,
)

# Overlapping bottom-right circular claim badge
circle(
    (64.0 + dx, 35.0 + dy),
    radius=11.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0),
)

# Inward claim arrow pointing left into the volume
Icon.draw_round_segment((68.5 + dx, 35.0 + dy), (59.5 + dx, 35.0 + dy), width_units=2.0, color=Icon.DARK)
Icon.draw_round_polyline(
    [(63.2 + dx, 38.6 + dy), (59.5 + dx, 35.0 + dy), (63.2 + dx, 31.4 + dy)],
    width_units=2.0,
    color=Icon.DARK,
)

save()
