# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud vendor icon: supabase."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    fill_style,
    setup_icon,
)

setup_icon()

w = 2.0

# Upper-left lightning bolt half (Colors.Green3)
upper_left_bolt = [
    (50.0, 88.5),  # Top rounded tip
    (12.5, 38.5),  # Outer left rounded corner
    (50.0, 38.5),  # Inner center corner
]
polygon(
    upper_left_bolt,
    style=fill_style(
        Colors.Green3,
        border_color=DARK,
        border_units=w,
        shape_r=(3.6, 6.2, 1.0),
    ),
)

# Lower-right lightning bolt half (Colors.Green4)
lower_right_bolt = [
    (50.0, 11.5),  # Bottom rounded tip
    (87.5, 61.5),  # Outer right rounded corner
    (50.0, 61.5),  # Inner center corner
]
polygon(
    lower_right_bolt,
    style=fill_style(
        Colors.Green4,
        border_color=DARK,
        border_units=w,
        shape_r=(3.6, 6.2, 1.0),
    ),
)

save()
