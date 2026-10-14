# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: dns."""

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

draw_round_segment((50.0, 62.0), (50.0, 42.0), width_units=w, color=DARK)
draw_round_polyline(
    [(43.5, 48.5), (50.0, 42.0), (56.5, 48.5)],
    width_units=w,
    color=DARK,
)

rectangle(
    (50.0, 72.0),
    width=70.0,
    height=20.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w, shape_r=6.0),
)
circle(
    (26.0, 72.0),
    radius=5.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=2.0),
)
draw_round_segment((36.0, 72.0), (74.0, 72.0), width_units=w, color=DARK)

rectangle(
    (50.0, 26.0),
    width=56.0,
    height=22.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=5.0),
)
for dot_x in (34.0, 50.0, 66.0):
    circle(
        (dot_x, 26.0),
        radius=4.0,
        style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0),
    )

save()
