# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: k8s_crd."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
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

# Slight up-right offset so the visual weight centers inside the heptagon
dx, dy = 2.0, 2.2

# Base white resource card
rectangle(
    (44.0 + dx, 44.0 + dy),
    width=30.0,
    height=30.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0, shape_r=5.0),
)

# Small inner resource block in bottom-left of base card
rectangle(
    (40.0 + dx, 40.0 + dy),
    width=12.0,
    height=12.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=2.0, shape_r=2.5),
)

# Interlocking top-right green custom extension block
rectangle(
    (60.0 + dx, 56.0 + dy),
    width=21.0,
    height=21.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0, shape_r=4.5),
)

# Crisp dark plus sign inside extension block
draw_round_segment((55.2 + dx, 56.0 + dy), (64.8 + dx, 56.0 + dy), width_units=2.0, color=DARK)
draw_round_segment((60.0 + dx, 51.2 + dy), (60.0 + dx, 60.8 + dy), width_units=2.0, color=DARK)

save()
