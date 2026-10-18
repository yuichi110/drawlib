# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: iot_device."""

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

# Lower-left IoT sensor enclosure
rectangle(
    (42.0, 42.0),
    width=48.0,
    height=48.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w, shape_r=8.0),
)

# Inner sensor core and status LED
circle(
    (42.0, 42.0),
    radius=12.5,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=2.0),
)
circle(
    (56.0, 28.0),
    radius=3.4,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0),
)

# Wireless transmitter node and concentric signal waves
tx, ty = 64.0, 62.0
circle(
    (tx, ty),
    radius=4.5,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0),
)

for r_arc in (13.0, 22.0):
    arc(
        (tx, ty),
        width=r_arc * 2.0,
        height=r_arc * 2.0,
        angle_start=0.0,
        angle_end=90.0,
        style=stroke_style(DARK, width_units=w),
    )
    draw_cap((tx + r_arc, ty), width_units=w, color=DARK)
    draw_cap((tx, ty + r_arc), width_units=w, color=DARK)

save()
