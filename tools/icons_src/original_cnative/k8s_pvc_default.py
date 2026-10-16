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
from drawlib.utils import (
    DARK,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_cylinder_tier,
    draw_original_k8s_heptagon,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

draw_original_k8s_heptagon()

# Slight up-right offset so the cylinder and claim badge sit centered inside the heptagon
dx, dy = 1.6, 3.5

# White storage volume cylinder
draw_cylinder_tier(
    46.0 + dx,
    38.0 + dy,
    36.0,
    17.0,
    6.0,
    body_color=WHITE,
    top_color=PASTEL_BLUE_LIGHT,
    border_color=DARK,
    border_units=2.3,
    draw_top_cap=True,
)

# Overlapping bottom-right circular claim badge
circle(
    (64.0 + dx, 35.0 + dy),
    radius=11.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.3),
)

# Inward claim arrow pointing left into the volume
draw_round_segment((68.5 + dx, 35.0 + dy), (59.5 + dx, 35.0 + dy), width_units=2.2, color=DARK)
draw_round_polyline(
    [(63.2 + dx, 38.6 + dy), (59.5 + dx, 35.0 + dy), (63.2 + dx, 31.4 + dy)],
    width_units=2.2,
    color=DARK,
)

save()
