# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: dedicated_interconnect."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
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

# 3 parallel high-speed fiber trunk conduits
for fy in (63.0, 50.0, 37.0):
    draw_round_segment((32.0, fy), (68.0, fy), width_units=w, color=DARK)

# Central optical coupler sleeve at (50, 50)
rectangle(
    (50.0, 50.0),
    width=16.0,
    height=38.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w, shape_r=4.5),
)
for fy in (61.0, 50.0, 39.0):
    circle(
        (50.0, fy),
        radius=2.6,
        style=fill_style(WHITE, border_color=DARK, border_units=1.8),
    )

# Left on-premises building block
rectangle(
    (22.0, 50.0),
    width=20.0,
    height=50.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w, shape_r=4.0),
)
for wy in (63.0, 54.0, 45.0, 36.0):
    draw_round_segment((17.5, wy), (26.5, wy), width_units=2.2, color=DARK)

# Right cloud / VPC block
rectangle(
    (78.0, 50.0),
    width=20.0,
    height=50.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=4.0),
)
draw_round_segment((78.0, 39.0), (78.0, 61.0), width_units=2.2, color=DARK)
for cy in (61.0, 39.0):
    circle(
        (78.0, cy),
        radius=4.2,
        style=fill_style(WHITE, border_color=DARK, border_units=2.0),
    )

save()
