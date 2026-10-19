# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Server concept icon: blade_chassis."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

# Outer modular blade enclosure
rectangle(
    (50.0, 50.0),
    width=78.0,
    height=64.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w, shape_r=7.0),
)

# Inner enclosure bay recess
rectangle(
    (50.0, 50.0),
    width=68.0,
    height=54.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=2.0, shape_r=4.5),
)

# 4 vertical server blades with top LED and bottom handle bar
for bx in (26.0, 42.0, 58.0, 74.0):
    rectangle(
        (bx, 50.0),
        width=12.0,
        height=46.0,
        style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0, shape_r=2.5),
    )
    circle(
        (bx, 66.0),
        radius=2.2,
        style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=1.8),
    )
    Icon.draw_round_segment((bx - 2.8, 34.0), (bx + 2.8, 34.0), width_units=2.0, color=Icon.DARK)

save()
