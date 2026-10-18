# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: network_peering."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
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

w = ORIG_STROKE

# Left virtual network frame
rectangle(
    (25.0, 50.0),
    width=26.0,
    height=52.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=6.0),
)
draw_round_segment((23.0, 37.0), (23.0, 63.0), width_units=2.0, color=DARK)
for ly in (63.0, 37.0):
    circle(
        (23.0, ly),
        radius=4.5,
        style=fill_style(WHITE, border_color=DARK, border_units=2.0),
    )

# Right virtual network frame
rectangle(
    (75.0, 50.0),
    width=26.0,
    height=52.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w, shape_r=6.0),
)
draw_round_segment((77.0, 37.0), (77.0, 63.0), width_units=2.0, color=DARK)
for ry in (63.0, 37.0):
    circle(
        (77.0, ry),
        radius=4.5,
        style=fill_style(WHITE, border_color=DARK, border_units=2.0),
    )

# Bidirectional horizontal peering arrows across the center
aw = 2.5
# Top arrow: left to right
draw_round_segment((38.0, 62.0), (62.0, 62.0), width_units=aw, color=DARK)
draw_round_polyline([(56.5, 66.5), (62.0, 62.0), (56.5, 57.5)], width_units=aw, color=DARK)

# Bottom arrow: right to left
draw_round_segment((38.0, 38.0), (62.0, 38.0), width_units=aw, color=DARK)
draw_round_polyline([(43.5, 42.5), (38.0, 38.0), (43.5, 33.5)], width_units=aw, color=DARK)

# Central peering bridge ring at (50, 50)
draw_round_segment((38.0, 50.0), (62.0, 50.0), width_units=w, color=DARK)
circle(
    (50.0, 50.0),
    radius=7.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w),
)
circle(
    (50.0, 50.0),
    radius=2.5,
    style=fill_style(DARK),
)

save()
