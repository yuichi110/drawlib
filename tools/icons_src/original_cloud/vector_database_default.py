# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: vector_database."""

from drawlib.canvas import save
from drawlib.shapes import circle
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
origin = (38.0, 42.0)

# 1. 3D orthogonal coordinate axes with arrow tips
y_tip = (38.0, 84.0)
x_tip = (84.0, 42.0)
z_tip = (16.0, 20.0)

draw_round_segment(origin, y_tip, width_units=w, color=DARK)
draw_round_segment(origin, x_tip, width_units=w, color=DARK)
draw_round_segment(origin, z_tip, width_units=w, color=DARK)

draw_round_polyline([(33.5, 78.5), y_tip, (42.5, 78.5)], width_units=w, color=DARK)
draw_round_polyline([(78.5, 46.5), x_tip, (78.5, 37.5)], width_units=w, color=DARK)
draw_round_polyline([(16.0, 26.8), z_tip, (22.8, 20.0)], width_units=w, color=DARK)

# 2. Vector rays from origin to embedding nodes
v1 = (70.0, 75.0)
v2 = (72.0, 55.0)
v3 = (49.0, 70.0)

draw_round_segment(origin, v1, width_units=2.3, color=DARK)
draw_round_segment(origin, v2, width_units=2.3, color=DARK)
draw_round_segment(origin, v3, width_units=2.3, color=DARK)

# 3. Origin node and vector embedding nodes
circle(
    origin,
    radius=5.5,
    style=fill_style(WHITE, border_color=DARK, border_units=2.2),
)
circle(
    v3,
    radius=6.5,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w),
)
circle(
    v2,
    radius=7.5,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w),
)
circle(
    v1,
    radius=8.5,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w),
)

save()
