# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Server concept icon: vm_group."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    WHITE,
    draw_iso_cube,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# Top-left folder/group tab behind the main card
rectangle(
    (32.0, 81.0),
    width=28.0,
    height=10.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=4.0),
)

# Main rounded VM group container card
rectangle(
    (50.0, 48.0),
    width=76.0,
    height=66.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w, shape_r=8.0),
)

# Three coordinated 3D VM cubes arranged in a triangle
vm_coords = (
    (50.0, 58.0),
    (33.0, 38.0),
    (67.0, 38.0),
)
for cx, cy in vm_coords:
    draw_iso_cube(
        cx,
        cy,
        radius=13.5,
        top_color=WHITE,
        left_color=PASTEL_BLUE,
        right_color=PASTEL_BLUE_LIGHT,
        border_color=DARK,
        border_units=2.0,
    )

save()
