# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Network concept icon: wireless_controller."""

import math

from drawlib.canvas import save
from drawlib.shapes import arc, circle, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_cap,
    draw_cisco_arrow,
    draw_round_segment,
    fill_style,
    setup_icon,
    stroke_style,
)

setup_icon()

w = ORIG_STROKE

# Stem and diagonal control arrows connecting controller box to upper nodes
draw_round_segment((50.0, 42.0), (50.0, 50.5), width_units=2.0, color=DARK)
draw_cisco_arrow(
    (34.0, 42.0),
    (25.5, 59.0),
    shaft_w=2.4,
    head_len=5.0,
    head_w=6.6,
    color=DARK,
)
draw_cisco_arrow(
    (66.0, 42.0),
    (74.5, 59.0),
    shaft_w=2.4,
    head_len=5.0,
    head_w=6.6,
    color=DARK,
)

# Lower rack controller box
rectangle(
    (50.0, 28.0),
    width=76.0,
    height=28.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=7.0),
)

# Left WHITE control screen
rectangle(
    (34.0, 28.0),
    width=32.0,
    height=14.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0, shape_r=3.5),
)

# Right 3 PASTEL_GREEN status dots
for dot_x in (58.0, 67.0, 76.0):
    circle(
        (dot_x, 28.0),
        radius=3.2,
        style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=1.8),
    )

# Central PASTEL_GREEN radio node above box
tx_cx, tx_cy = 50.0, 56.0
circle(
    (tx_cx, tx_cy),
    radius=5.5,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0),
)

# 2 upward Wi-Fi arcs above central radio node
ang_start = 40.0
ang_end = 140.0
arc_w = 2.7

for diam in (30.0, 48.0):
    r = diam / 2.0
    arc(
        (tx_cx, tx_cy),
        width=diam,
        height=diam,
        angle_start=ang_start,
        angle_end=ang_end,
        style=stroke_style(DARK, width_units=arc_w),
    )
    for ang_deg in (ang_start, ang_end):
        rad = math.radians(ang_deg)
        draw_cap(
            (tx_cx + r * math.cos(rad), tx_cy + r * math.sin(rad)),
            width_units=arc_w,
            color=DARK,
        )

# Left and right satellite AP dots
for sat_x in (22.0, 78.0):
    circle(
        (sat_x, 66.0),
        radius=5.0,
        style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=2.0),
    )

save()
