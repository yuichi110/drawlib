# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: scheduler."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE
cx, cy = 50.0, 47.0

# Top trigger stem and button
Icon.draw_round_segment((cx, 81.0), (cx, 86.0), width_units=w, color=Icon.DARK)
rectangle(
    (cx, 86.5),
    width=18.0,
    height=6.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0, shape_r=2.5),
)

# Outer clock casing and inner clock face
circle(
    (cx, cy),
    radius=34.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w),
)
circle(
    (cx, cy),
    radius=25.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0),
)

# Clock hands and center pivot
Icon.draw_round_segment((cx, cy), (cx, 64.0), width_units=w, color=Icon.DARK)
Icon.draw_round_segment((cx, cy), (63.5, 39.0), width_units=w, color=Icon.DARK)
circle(
    (cx, cy),
    radius=4.5,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0),
)

save()
