# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: load_balancer."""

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

draw_round_segment((23.0, 50.0), (77.0, 50.0), width_units=w, color=DARK)
draw_round_polyline(
    [(47.0, 50.0), (47.0, 78.0), (77.0, 78.0)],
    width_units=w,
    color=DARK,
    corner_r=7.5,
)
draw_round_polyline(
    [(47.0, 50.0), (47.0, 22.0), (77.0, 22.0)],
    width_units=w,
    color=DARK,
    corner_r=7.5,
)

circle(
    (23.0, 50.0),
    radius=13.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w),
)
circle(
    (23.0, 50.0),
    radius=4.5,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0),
)

for ty in (78.0, 50.0, 22.0):
    circle(
        (77.0, ty),
        radius=10.5,
        style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w),
    )

save()
