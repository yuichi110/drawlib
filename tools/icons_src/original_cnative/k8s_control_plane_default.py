# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: k8s_control_plane."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_original_k8s_heptagon,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

draw_original_k8s_heptagon()

cx, cy = 50.0, 48.0
angles_deg = [90.0 + i * (360.0 / 7.0) for i in range(7)]

# Outer wheel spoke handles
for deg in angles_deg:
    rad = math.radians(deg)
    ux, uy = math.cos(rad), math.sin(rad)
    draw_round_segment(
        (cx + ux * 17.5, cy + uy * 17.5),
        (cx + ux * 24.5, cy + uy * 24.5),
        width_units=2.0,
        color=DARK,
    )

# White outer ship's wheel ring
circle(
    (cx, cy),
    radius=18.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0),
)

# Inner hollow cutout matching heptagon fill
circle(
    (cx, cy),
    radius=11.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=2.0),
)

# Inner wheel spokes radiating from hub to inner rim
for deg in angles_deg:
    rad = math.radians(deg)
    ux, uy = math.cos(rad), math.sin(rad)
    draw_round_segment(
        (cx, cy),
        (cx + ux * 11.0, cy + uy * 11.0),
        width_units=2.0,
        color=DARK,
    )

# Central green control hub
circle(
    (cx, cy),
    radius=6.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0),
)

save()
