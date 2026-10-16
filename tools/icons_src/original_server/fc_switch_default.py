# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Server concept icon: fc_switch."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_cisco_arrow,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# Wide low-profile SAN switch chassis
rectangle(
    (50.0, 50.0),
    width=78.0,
    height=44.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=7.0),
)

# Inner white fabric panel
rectangle(
    (50.0, 50.0),
    width=66.0,
    height=32.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0, shape_r=4.5),
)

# Crossing X-fabric lines between corner port junctions
draw_round_segment((32.0, 42.0), (68.0, 58.0), width_units=2.4, color=DARK)
draw_round_segment((32.0, 58.0), (68.0, 42.0), width_units=2.4, color=DARK)

# 4 outward horizontal fabric arrows pointing left/right
for y_port in (42.0, 58.0):
    draw_cisco_arrow(
        (32.0, y_port),
        (20.5, y_port),
        shaft_w=2.4,
        head_len=5.0,
        head_w=6.6,
        color=DARK,
    )
    draw_cisco_arrow(
        (68.0, y_port),
        (79.5, y_port),
        shaft_w=2.4,
        head_len=5.0,
        head_w=6.6,
        color=DARK,
    )

# Central pastel green SAN fabric ring/node
circle(
    (50.0, 50.0),
    radius=6.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.2),
)

save()
