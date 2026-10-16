# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: feature_flag."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# Outer stadium/pill toggle switch track
rectangle(
    (50.0, 50.0),
    width=74.0,
    height=38.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=19.0),
)

# Left ON vertical indicator bar
rectangle(
    (31.0, 50.0),
    width=6.0,
    height=15.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.2, shape_r=3.0),
)

# Active right toggle knob
circle(
    (67.0, 50.0),
    radius=13.5,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w),
)
circle(
    (67.0, 50.0),
    radius=4.5,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0),
)

save()
