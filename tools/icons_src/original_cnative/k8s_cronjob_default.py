# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: k8s_cronjob."""

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

# Top alarm / schedule button stem and tab
draw_round_segment((50.0, 64.0), (50.0, 69.5), width_units=2.4, color=DARK)
rectangle(
    (50.0, 72.0),
    width=14.0,
    height=6.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.2, shape_r=2.5),
)

# White circular clock face
circle(
    (50.0, 44.0),
    radius=20.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.4),
)

# L-shaped dark clock hands
draw_round_polyline(
    [(50.0, 55.0), (50.0, 44.0), (58.5, 38.8)],
    width_units=2.4,
    color=DARK,
)

# Green center clock pivot dot
circle(
    (50.0, 44.0),
    radius=3.2,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0),
)

save()
