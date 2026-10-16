# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Network concept icon: ip_phone."""

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

# Base phone body
rectangle(
    (54.0, 48.0),
    width=64.0,
    height=62.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=10.0),
)

# Left vertical handset
rectangle(
    (29.0, 48.0),
    width=16.0,
    height=68.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w, shape_r=7.0),
)

# Upper white LCD screen
rectangle(
    (61.0, 63.5),
    width=36.0,
    height=18.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.2, shape_r=3.5),
)

# Lower 3x3 keypad dots
for ky in (46.5, 38.5, 30.5):
    for kx in (51.0, 61.0, 71.0):
        circle((kx, ky), radius=2.2, style=fill_style(DARK))

# Call / speaker button pill
rectangle(
    (61.0, 23.0),
    width=18.0,
    height=4.8,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=1.8, shape_r=2.4),
)

save()
