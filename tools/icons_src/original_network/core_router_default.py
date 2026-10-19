# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Network concept icon: core_router."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Cisco, Icon

Icon.setup()

w = Icon.ORIG_STROKE

# Tall multi-slot carrier router chassis
rectangle(
    (50.0, 50.0),
    width=64.0,
    height=78.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w, shape_r=8.0),
)

# Upper routing module bay
rectangle(
    (50.0, 66.0),
    width=52.0,
    height=34.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0, shape_r=5.0),
)

# 4 routing arrows inside upper bay (left/right inward, top/bottom outward)
Cisco.draw_arrow(
    (29.0, 66.0),
    (43.0, 66.0),
    shaft_w=2.6,
    head_len=5.2,
    head_w=6.8,
    color=Icon.DARK,
)
Cisco.draw_arrow(
    (71.0, 66.0),
    (57.0, 66.0),
    shaft_w=2.6,
    head_len=5.2,
    head_w=6.8,
    color=Icon.DARK,
)
Cisco.draw_arrow(
    (50.0, 71.8),
    (50.0, 79.8),
    shaft_w=2.6,
    head_len=4.6,
    head_w=6.8,
    color=Icon.DARK,
)
Cisco.draw_arrow(
    (50.0, 60.2),
    (50.0, 52.2),
    shaft_w=2.6,
    head_len=4.6,
    head_w=6.8,
    color=Icon.DARK,
)

# Center dot inside upper routing bay
circle(
    (50.0, 66.0),
    radius=4.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=1.8),
)

# Lower line-card bay: 4 vertical white blade slots with status LEDs
for x_slot in (30.5, 43.5, 56.5, 69.5):
    rectangle(
        (x_slot, 30.0),
        width=9.5,
        height=22.0,
        style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0, shape_r=2.5),
    )
    circle(
        (x_slot, 35.8),
        radius=2.0,
        style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=1.6),
    )

save()
