# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: virtual_machine."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

rectangle(
    (50.0, 50.0),
    width=72.0,
    height=72.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w, shape_r=9.0),
)

Icon.draw_iso_cube(
    50.0,
    50.0,
    radius=24.0,
    top_color=Icon.WHITE,
    left_color=Icon.PASTEL_BLUE,
    right_color=Icon.PASTEL_GREEN,
    border_color=Icon.DARK,
    border_units=2.0,
)

circle(
    (74.0, 26.0),
    radius=3.5,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0),
)

save()
