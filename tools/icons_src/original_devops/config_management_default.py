# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: config_management."""

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
    width=74.0,
    height=68.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w, shape_r=8.0),
)

sliders = [
    (66.0, 62.0, PASTEL_BLUE),
    (50.0, 36.0, PASTEL_GREEN),
    (34.0, 56.0, PASTEL_BLUE),
]
for y, knob_x, knob_color in sliders:
    draw_round_segment((24.0, y), (76.0, y), width_units=w, color=DARK)
    circle(
        (knob_x, y),
        radius=6.8,
        style=fill_style(knob_color, border_color=DARK, border_units=2.0),
    )

save()
