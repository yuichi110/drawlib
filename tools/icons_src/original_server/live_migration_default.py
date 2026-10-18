# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Server concept icon: live_migration."""

from drawlib.canvas import save
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_chunky_arrow,
    draw_iso_cube,
    draw_round_segment,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# 2 horizontal motion trail lines behind left source VM
for y_trail in (65.0, 35.0):
    draw_round_segment((12.0, y_trail), (18.0, y_trail), width_units=2.0, color=DARK)

# Left source 3D isometric VM cube
draw_iso_cube(
    28.0,
    50.0,
    radius=16.5,
    top_color=WHITE,
    left_color=PASTEL_BLUE_LIGHT,
    right_color=WHITE,
    border_color=DARK,
    border_units=2.0,
)

# Right destination 3D isometric VM cube
draw_iso_cube(
    72.0,
    50.0,
    radius=18.5,
    top_color=WHITE,
    left_color=PASTEL_BLUE,
    right_color=PASTEL_GREEN,
    border_color=DARK,
    border_units=w,
)

# Bold horizontal live transfer arrow between source and destination
draw_chunky_arrow(
    y_center=50.0,
    x_tail=36.0,
    x_tip=60.0,
    x_head_base=50.0,
    shaft_half_h=5.0,
    head_half_h=11.0,
    fill_color=PASTEL_GREEN,
    border_units=2.0,
    border_color=DARK,
)

save()
