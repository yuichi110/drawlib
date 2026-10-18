# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: containerd."""

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
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

# Outer rounded square badge
rectangle(
    (50.0, 50.0),
    width=74.0,
    height=74.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=12.0),
)

# Bold geometric white block-letter "d"
d_points = [
    (31.0, 22.0),
    (69.0, 22.0),
    (69.0, 78.0),
    (57.0, 78.0),
    (57.0, 58.0),
    (31.0, 58.0),
]
polygon(
    d_points,
    style=fill_style(
        WHITE,
        border_color=DARK,
        border_units=2.0,
        shape_r=(2.5, 2.5, 2.5, 2.5, 0.0, 2.5),
    ),
)

# Inner square cutout inside the lower bowl of "d"
rectangle(
    (50.0, 40.0),
    width=14.0,
    height=14.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0, shape_r=2.0),
)

save()
