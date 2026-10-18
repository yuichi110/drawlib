# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: k8s_node."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import (
    DARK,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_original_k8s_heptagon,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

draw_original_k8s_heptagon()

# Horizontal rack host chassis
rectangle(
    (50.0, 48.0),
    width=48.0,
    height=30.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0, shape_r=5.0),
)

# Horizontal bay divider
draw_round_segment((26.0, 44.0), (74.0, 44.0), width_units=2.0, color=DARK)

# Upper CPU bay: square processor chip and ventilation slots
rectangle(
    (38.0, 53.5),
    width=11.0,
    height=10.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=2.0, shape_r=2.0),
)
draw_round_segment((50.0, 55.8), (66.0, 55.8), width_units=2.0, color=DARK)
draw_round_segment((50.0, 51.2), (62.0, 51.2), width_units=2.0, color=DARK)

# Lower slot bar: drive slot line and active LED dot
draw_round_segment((33.0, 38.5), (54.0, 38.5), width_units=2.0, color=DARK)
circle(
    (64.0, 38.5),
    radius=3.3,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0),
)

save()
