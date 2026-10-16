# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: test_automation."""

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

# Test suite clipboard card
rectangle(
    (50.0, 46.0),
    width=62.0,
    height=64.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w, shape_r=8.0),
)

# Top clip header
rectangle(
    (50.0, 78.0),
    width=32.0,
    height=12.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=4.0),
)

# 3 horizontal test rows with green check badges
for y in (60.0, 44.0, 28.0):
    circle(
        (32.0, y),
        radius=6.0,
        style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.2),
    )
    draw_round_polyline(
        [(29.3, y - 0.2), (31.3, y - 2.2), (35.0, y + 1.8)],
        width_units=1.8,
        color=DARK,
    )
    draw_round_segment((44.0, y), (68.0, y), width_units=3.0, color=DARK)

save()
