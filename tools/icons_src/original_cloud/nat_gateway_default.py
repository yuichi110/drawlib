# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: nat_gateway."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_chunky_arrow,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# 3 private source paths converging into the central NAT gateway box
draw_round_polyline(
    [(18.0, 74.0), (30.0, 74.0), (30.0, 59.0), (38.0, 59.0)],
    width_units=w,
    color=DARK,
    corner_r=5.0,
)
draw_round_segment((18.0, 50.0), (38.0, 50.0), width_units=w, color=DARK)
draw_round_polyline(
    [(18.0, 26.0), (30.0, 26.0), (30.0, 41.0), (38.0, 41.0)],
    width_units=w,
    color=DARK,
    corner_r=5.0,
)

# 3 private source nodes on the left
for sy in (74.0, 50.0, 26.0):
    circle(
        (18.0, sy),
        radius=6.8,
        style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w),
    )

# Single outbound public arrow on the right
draw_chunky_arrow(
    y_center=50.0,
    x_tail=60.0,
    x_tip=88.0,
    x_head_base=75.0,
    shaft_half_h=5.0,
    head_half_h=12.0,
    fill_color=PASTEL_GREEN,
    border_units=w,
)

# Central NAT gateway router box
rectangle(
    (50.0, 50.0),
    width=24.0,
    height=46.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w, shape_r=5.5),
)

# Internal many-to-one translation funnel lines and core node
draw_round_segment((38.0, 59.0), (50.0, 50.0), width_units=2.2, color=DARK)
draw_round_segment((38.0, 50.0), (62.0, 50.0), width_units=2.2, color=DARK)
draw_round_segment((38.0, 41.0), (50.0, 50.0), width_units=2.2, color=DARK)

circle(
    (50.0, 50.0),
    radius=6.2,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.2),
)

save()
