# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: npu_node."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

pin_coords = [32.0, 50.0, 68.0]
w = ORIG_STROKE

for pos in pin_coords:
    draw_round_segment((11.0, pos), (24.0, pos), width_units=w, color=DARK)
    draw_round_segment((76.0, pos), (89.0, pos), width_units=w, color=DARK)
    draw_round_segment((pos, 11.0), (pos, 24.0), width_units=w, color=DARK)
    draw_round_segment((pos, 76.0), (pos, 89.0), width_units=w, color=DARK)

rectangle(
    (50.0, 50.0),
    width=56.0,
    height=56.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w, shape_r=8.0),
)

# Systolic circuit traces connecting corner tensor nodes and center diamond
c_tl = (35.5, 64.5)
c_tr = (64.5, 64.5)
c_br = (64.5, 35.5)
c_bl = (35.5, 35.5)

draw_round_polyline([c_tl, c_tr, c_br, c_bl], width_units=2.0, color=DARK, closed=True)
draw_round_segment(c_tl, c_br, width_units=2.3, color=DARK)
draw_round_segment(c_bl, c_tr, width_units=2.3, color=DARK)

# Central diamond-shaped neural/tensor core
polygon(
    [(50.0, 60.8), (60.8, 50.0), (50.0, 39.2), (39.2, 50.0)],
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.4, shape_r=2.5),
)
circle(
    (50.0, 50.0),
    radius=2.8,
    style=fill_style(WHITE, border_color=DARK, border_units=1.8),
)

# 4 corner tensor nodes
for pt_node in (c_tl, c_tr, c_bl, c_br):
    circle(
        pt_node,
        radius=5.2,
        style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=2.2),
    )

save()
