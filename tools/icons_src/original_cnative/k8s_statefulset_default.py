# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: k8s_statefulset."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.utils import (
    DARK,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_cylinder_tier,
    draw_original_k8s_heptagon,
    fill_style,
    setup_icon,
)

setup_icon()

draw_original_k8s_heptagon()

# Back stacked replica card
rectangle(
    (55.0, 53.0),
    width=36.0,
    height=28.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=2.0, shape_r=4.5),
)

# Front replica card
rectangle(
    (45.0, 43.0),
    width=36.0,
    height=28.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0, shape_r=4.5),
)

# Persistent storage cylinder inside the front replica card
draw_cylinder_tier(
    45.0,
    38.5,
    20.0,
    8.5,
    3.6,
    body_color=PASTEL_GREEN,
    top_color=PASTEL_GREEN,
    border_color=DARK,
    border_units=2.0,
    draw_top_cap=True,
)

save()
