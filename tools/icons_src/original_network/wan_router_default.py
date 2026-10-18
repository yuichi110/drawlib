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
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_cisco_arrow,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# Outer rounded square router card
rectangle(
    (50.0, 50.0),
    width=76.0,
    height=76.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=14.0),
)

# Inner circular WAN globe (white base + pastel green meridian ellipse + equator)
circle(
    (50.0, 50.0),
    radius=21.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0),
)
ellipse(
    (50.0, 50.0),
    width=20.0,
    height=42.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0),
)
draw_round_segment((29.0, 50.0), (71.0, 50.0), width_units=2.0, color=DARK)

# 4 cardinal routing arrows on the pastel blue frame (left/right inward, top/bottom outward)
draw_cisco_arrow(
    (15.0, 50.0),
    (26.5, 50.0),
    shaft_w=3.0,
    head_len=5.5,
    head_w=7.8,
    color=DARK,
)
draw_cisco_arrow(
    (85.0, 50.0),
    (73.5, 50.0),
    shaft_w=3.0,
    head_len=5.5,
    head_w=7.8,
    color=DARK,
)
draw_cisco_arrow(
    (50.0, 73.5),
    (50.0, 85.0),
    shaft_w=3.0,
    head_len=5.5,
    head_w=7.8,
    color=DARK,
)
draw_cisco_arrow(
    (50.0, 26.5),
    (50.0, 15.0),
    shaft_w=3.0,
    head_len=5.5,
    head_w=7.8,
    color=DARK,
)

save()
