# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: k8s_job."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import (
    DARK,
    PASTEL_GREEN,
    WHITE,
    draw_original_k8s_heptagon,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

draw_original_k8s_heptagon()

# White task card
rectangle(
    (46.0, 49.0),
    width=36.0,
    height=38.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0, shape_r=6.0),
)

# Two horizontal dark task lines
draw_round_segment((35.0, 58.0), (57.0, 58.0), width_units=2.0, color=DARK)
draw_round_segment((35.0, 49.0), (51.0, 49.0), width_units=2.0, color=DARK)

# Bottom-right overlapping green completion circle
circle(
    (62.0, 36.0),
    radius=12.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0),
)

# Crisp dark completion checkmark
draw_round_polyline(
    [(57.0, 35.5), (60.8, 31.8), (67.2, 39.8)],
    width_units=2.0,
    color=DARK,
)

save()
