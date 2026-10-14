# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: compute."""

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

rectangle(
    (50.0, 50.0),
    width=28.0,
    height=28.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=4.5),
)

circle(
    (70.0, 30.0),
    radius=3.4,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0),
)

save()
