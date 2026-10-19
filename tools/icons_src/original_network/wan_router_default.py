# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Network concept icon: wan_router."""

from drawlib.canvas import save
from drawlib.shapes import circle, ellipse, rectangle
from drawlib.utils import Cisco, Icon

Icon.setup()

w = Icon.ORIG_STROKE

# Outer rounded square router card
rectangle(
    (50.0, 50.0),
    width=76.0,
    height=76.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w, shape_r=14.0),
)

# Inner circular WAN globe (white base + pastel green meridian ellipse + equator)
circle(
    (50.0, 50.0),
    radius=21.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0),
)
ellipse(
    (50.0, 50.0),
    width=20.0,
    height=42.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0),
)
Icon.draw_round_segment((29.0, 50.0), (71.0, 50.0), width_units=2.0, color=Icon.DARK)

# 4 cardinal routing arrows on the pastel blue frame (left/right inward, top/bottom outward)
Cisco.draw_arrow(
    (15.0, 50.0),
    (26.5, 50.0),
    shaft_w=3.0,
    head_len=5.5,
    head_w=7.8,
    color=Icon.DARK,
)
Cisco.draw_arrow(
    (85.0, 50.0),
    (73.5, 50.0),
    shaft_w=3.0,
    head_len=5.5,
    head_w=7.8,
    color=Icon.DARK,
)
Cisco.draw_arrow(
    (50.0, 73.5),
    (50.0, 85.0),
    shaft_w=3.0,
    head_len=5.5,
    head_w=7.8,
    color=Icon.DARK,
)
Cisco.draw_arrow(
    (50.0, 26.5),
    (50.0, 15.0),
    shaft_w=3.0,
    head_len=5.5,
    head_w=7.8,
    color=Icon.DARK,
)

save()
