# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Network concept icon: wireless_ap."""

import math

from drawlib.canvas import save
from drawlib.shapes import arc, circle, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_cap,
    fill_style,
    setup_icon,
    stroke_style,
)

setup_icon()

w = ORIG_STROKE

# Lower rounded AP base (shifted down to leave clear space below the Wi-Fi symbol)
base_y = 22.0
rectangle(
    (50.0, base_y),
    width=64.0,
    height=24.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=10.0),
)

# Inner WHITE pill
rectangle(
    (50.0, base_y),
    width=42.0,
    height=10.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0, shape_r=5.0),
)

# PASTEL_GREEN LED dot inside pill
circle(
    (64.0, base_y),
    radius=2.8,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=1.8),
)

# Central Wi-Fi transmitter circle (separated from AP base by ~7.5 units of space)
tx_cx, tx_cy = 50.0, 49.5
circle(
    (tx_cx, tx_cy),
    radius=5.5,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0),
)

# 3 concentric upward Wi-Fi radio wave arcs
ang_start = 40.0
ang_end = 140.0
arc_w = 3.0

for diam in (34.0, 54.0, 74.0):
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

save()
