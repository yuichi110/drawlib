# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Server concept icon: tower_server."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# Upright pedestal tower chassis
rectangle(
    (50.0, 50.5),
    width=48.0,
    height=75.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=6.0),
)

# Wider base pedestal stand at bottom
rectangle(
    (50.0, 14.5),
    width=58.0,
    height=7.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w, shape_r=3.5),
)

# 3 horizontal drive bay slots
for by in (74.0, 60.0, 46.0):
    rectangle(
        (50.0, by),
        width=34.0,
        height=9.5,
        style=fill_style(WHITE, border_color=DARK, border_units=2.0, shape_r=2.5),
    )
    circle((38.0, by), radius=1.5, style=fill_style(DARK))

# Lower vertical vent lines and power button
for vx in (36.0, 41.5, 47.0):
    draw_round_segment((vx, 23.0), (vx, 33.0), width_units=2.0, color=DARK)

circle(
    (60.0, 28.0),
    radius=5.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0),
)

save()
