# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: block_storage."""

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
    (50.0, 50.0),
    width=64.0,
    height=74.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w, shape_r=8.0),
)

circle(
    (50.0, 54.0),
    radius=22.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w),
)

circle(
    (50.0, 54.0),
    radius=6.5,
    style=fill_style(WHITE, border_color=DARK, border_units=2.2),
)

draw_round_segment((32.0, 24.0), (48.0, 44.0), width_units=w, color=DARK)

circle(
    (32.0, 24.0),
    radius=4.5,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0),
)

circle(
    (68.0, 24.0),
    radius=3.5,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0),
)

save()
