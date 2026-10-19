# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility concept icon: branch_office."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.utils import Icon

Icon.setup()

w_outer = 2.0
w_inner = 1.6

# 1. Clean 3-story mid-rise office facade (WHITE)
rectangle(
    (50.0, 44.0),
    width=56.0,
    height=60.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_outer, shape_r=2.5),
)

# 2. Overhanging flat roof cornice cap (PASTEL_BLUE)
rectangle(
    (50.0, 77.5),
    width=64.0,
    height=7.5,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_outer, shape_r=2.5),
)

# 3. Three stories of windows (PASTEL_BLUE_LIGHT)
# Top two floors: 3 windows across
for wy in (63.5, 48.5):
    for wx in (33.5, 50.0, 66.5):
        rectangle(
            (wx, wy),
            width=10.5,
            height=8.5,
            style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_inner, shape_r=1.5),
        )

# Ground floor: flanking windows on left and right of entrance
for wx in (33.5, 66.5):
    rectangle(
        (wx, 32.5),
        width=10.5,
        height=8.5,
        style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_inner, shape_r=1.5),
    )

# 4. Main entrance double door & canopy (PASTEL_BLUE)
rectangle(
    (50.0, 23.0),
    width=13.0,
    height=18.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_inner, shape_r=1.5),
)
Icon.draw_round_segment((50.0, 14.0), (50.0, 32.0), width_units=w_inner, color=Icon.DARK)
rectangle(
    (50.0, 33.5),
    width=17.0,
    height=3.6,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_inner, shape_r=1.5),
)

# 5. Ground baseline
Icon.draw_round_segment((14.0, 14.0), (86.0, 14.0), width_units=w_outer, color=Icon.DARK)

save()
