# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: logging."""

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

rectangle(
    (46.0, 52.0),
    width=58.0,
    height=68.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w, shape_r=7.0),
)

rows = [
    (68.0, PASTEL_BLUE),
    (52.0, PASTEL_GREEN),
    (36.0, PASTEL_GREEN),
]
for y, dot_color in rows:
    circle(
        (28.0, y),
        radius=3.8,
        style=fill_style(dot_color, border_color=DARK, border_units=2.0),
    )
    draw_round_segment((38.0, y), (64.0, y), width_units=2.6, color=DARK)

draw_round_segment((70.0, 28.0), (85.0, 13.0), width_units=3.5, color=DARK)
circle(
    (70.0, 28.0),
    radius=13.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w),
)
circle(
    (70.0, 28.0),
    radius=7.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0),
)

save()
