# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code concept icon: monolith."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

w_shape = 2.0

# 1. Heavy unified outer WHITE frame ((50, 50), width=68, height=74, shape_r=6.0, border 1.8 in DARK)
# x=16..84, y=13..87
rectangle(
    (50.0, 50.0),
    width=68.0,
    height=74.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w_shape, shape_r=6.0),
)

# 2. Three stacked full-width horizontal layer blocks inside (width=56, height=18, shape_r=3.0)
layers = [
    # (cy, fill_color)
    (72.0, PASTEL_BLUE),  # UI top
    (50.0, PASTEL_BLUE_LIGHT),  # Business middle
    (28.0, PASTEL_GREEN),  # Data bottom
]
for cy, col in layers:
    rectangle(
        (50.0, cy),
        width=56.0,
        height=18.0,
        style=fill_style(col, border_color=DARK, border_units=w_shape, shape_r=3.0),
    )

# 3. Minimal architectural layer cues (2 small window dots in UI top, short bar accents in middle/bottom)
for x_dot in (29.0, 36.0):
    circle(
        (x_dot, 72.0),
        radius=2.1,
        style=fill_style(WHITE, border_color=DARK, border_units=w_shape),
    )
draw_round_segment((28.0, 50.0), (46.0, 50.0), width_units=w_shape, color=DARK)
draw_round_segment((28.0, 28.0), (42.0, 28.0), width_units=w_shape, color=DARK)

save()
