# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Client concept icon: smartwatch."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# Top and bottom watch straps
rectangle(
    (50.0, 74.0),
    width=26.0,
    height=24.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=4.0),
)
rectangle(
    (50.0, 26.0),
    width=26.0,
    height=24.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=4.0),
)

# Side digital crown button
rectangle(
    (73.0, 56.0),
    width=6.0,
    height=10.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=2.2, shape_r=2.0),
)

# Rounded watch case and WHITE face
rectangle(
    (50.0, 50.0),
    width=45.0,
    height=49.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w, shape_r=11.0),
)
rectangle(
    (50.0, 50.0),
    width=35.0,
    height=39.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0, shape_r=8.0),
)

# PASTEL_GREEN activity ring (donut)
circle(
    (50.0, 50.0),
    radius=12.5,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0),
)
circle(
    (50.0, 50.0),
    radius=6.8,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0),
)

save()
