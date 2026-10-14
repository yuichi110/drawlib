# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: file_storage."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
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

polygon(
    [
        (14.0, 20.0),
        (86.0, 20.0),
        (86.0, 70.0),
        (48.0, 70.0),
        (42.0, 78.0),
        (14.0, 78.0),
    ],
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=4.5),
)

rectangle(
    (50.0, 56.0),
    width=58.0,
    height=34.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.4, shape_r=3.5),
)

rectangle(
    (50.0, 39.0),
    width=72.0,
    height=38.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=5.0),
)

circle(
    (72.0, 28.0),
    radius=4.2,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0),
)

save()
