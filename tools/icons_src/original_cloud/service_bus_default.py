# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: service_bus."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# Vertical tap stems
draw_round_segment((28.0, 50.0), (28.0, 76.0), width_units=w, color=DARK)
draw_round_segment((72.0, 50.0), (72.0, 76.0), width_units=w, color=DARK)
draw_round_segment((50.0, 50.0), (50.0, 24.0), width_units=w, color=DARK)

# Central horizontal bus bar
rectangle(
    (50.0, 50.0),
    width=76.0,
    height=14.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=7.0),
)

# Upper service nodes
for tx in (28.0, 72.0):
    rectangle(
        (tx, 76.0),
        width=20.0,
        height=16.0,
        style=fill_style(WHITE, border_color=DARK, border_units=w, shape_r=4.0),
    )

# Lower service node
rectangle(
    (50.0, 24.0),
    width=22.0,
    height=16.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w, shape_r=4.0),
)

save()
