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
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

# Vertical mounting stems connecting host blade to VMs
for x_stem in (32.0, 68.0):
    Icon.draw_round_segment((x_stem, 33.0), (x_stem, 46.0), width_units=w, color=Icon.DARK)

# Bottom physical hypervisor server blade
rectangle(
    (50.0, 24.0),
    width=76.0,
    height=18.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w, shape_r=4.5),
)
rectangle(
    (32.0, 24.0),
    width=24.0,
    height=6.5,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0, shape_r=2.0),
)
Icon.draw_round_segment((51.0, 24.0), (63.0, 24.0), width_units=2.0, color=Icon.DARK)
circle(
    (75.0, 24.0),
    radius=3.6,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0),
)

# Two 3D VM cubes hosted above the hypervisor blade
for cx in (32.0, 68.0):
    Icon.draw_iso_cube(
        cx,
        62.0,
        radius=18.0,
        top_color=Icon.WHITE,
        left_color=Icon.PASTEL_BLUE,
        right_color=Icon.PASTEL_GREEN,
        border_color=Icon.DARK,
        border_units=2.0,
    )

save()
