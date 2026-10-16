# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Network concept icon: server."""

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

# Vertical server tower
rectangle(
    (50.0, 50.0),
    width=52.0,
    height=76.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=8.0),
)

# 3 horizontal white drive bay slots with left status dots
for by in (72.0, 56.0, 40.0):
    rectangle(
        (50.0, by),
        width=38.0,
        height=11.0,
        style=fill_style(WHITE, border_color=DARK, border_units=2.0, shape_r=3.0),
    )
    circle((37.0, by), radius=1.8, style=fill_style(DARK))

# Lower control area: two vertical vent lines + pastel green power button
for vx in (35.0, 41.0):
    draw_round_segment((vx, 19.0), (vx, 27.0), width_units=2.2, color=DARK)

circle(
    (59.0, 23.0),
    radius=5.5,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0),
)

save()
