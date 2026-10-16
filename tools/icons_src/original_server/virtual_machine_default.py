# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Server concept icon: virtual_machine."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_iso_cube,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# Rounded square VM container card
rectangle(
    (50.0, 50.0),
    width=74.0,
    height=74.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w, shape_r=10.0),
)

# Centered 3D isometric VM cube
draw_iso_cube(
    50.0,
    50.0,
    radius=24.0,
    top_color=WHITE,
    left_color=PASTEL_BLUE,
    right_color=PASTEL_BLUE_LIGHT,
    border_color=DARK,
    border_units=2.5,
)

# Bottom-right active status indicator dot
circle(
    (74.0, 26.0),
    radius=4.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0),
)

save()
