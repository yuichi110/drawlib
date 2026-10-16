# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: coredns."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# Back 45-degree tilted rounded square (top-right offset)
rectangle(
    (56.0, 55.0),
    width=46.0,
    height=46.0,
    style=fill_style(
        PASTEL_BLUE_LIGHT,
        border_color=DARK,
        border_units=w,
        shape_r=10.0,
        angle=45.0,
    ),
)

# Main 45-degree tilted rounded square (front center-left)
rectangle(
    (45.0, 45.0),
    width=50.0,
    height=50.0,
    style=fill_style(
        PASTEL_BLUE,
        border_color=DARK,
        border_units=w,
        shape_r=11.0,
        angle=45.0,
    ),
)

# Central 45-degree tilted capsule chain-link ring
rectangle(
    (45.0, 45.0),
    width=31.0,
    height=18.0,
    style=fill_style(
        WHITE,
        border_color=DARK,
        border_units=2.4,
        shape_r=8.8,
        angle=45.0,
    ),
)
rectangle(
    (45.0, 45.0),
    width=18.0,
    height=6.8,
    style=fill_style(
        PASTEL_GREEN,
        border_color=DARK,
        border_units=2.0,
        shape_r=3.2,
        angle=45.0,
    ),
)

save()
