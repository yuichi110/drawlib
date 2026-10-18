# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Server concept icon: hypervisor_host."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_iso_cube,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# Vertical mounting stems connecting host blade to VMs
for x_stem in (32.0, 68.0):
    draw_round_segment((x_stem, 33.0), (x_stem, 46.0), width_units=w, color=DARK)

# Bottom physical hypervisor server blade
rectangle(
    (50.0, 24.0),
    width=76.0,
    height=18.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=4.5),
)
rectangle(
    (32.0, 24.0),
    width=24.0,
    height=6.5,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0, shape_r=2.0),
)
draw_round_segment((51.0, 24.0), (63.0, 24.0), width_units=2.0, color=DARK)
circle(
    (75.0, 24.0),
    radius=3.6,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0),
)

# Two 3D VM cubes hosted above the hypervisor blade
for cx in (32.0, 68.0):
    draw_iso_cube(
        cx,
        62.0,
        radius=18.0,
        top_color=WHITE,
        left_color=PASTEL_BLUE,
        right_color=PASTEL_GREEN,
        border_color=DARK,
        border_units=2.0,
    )

save()
