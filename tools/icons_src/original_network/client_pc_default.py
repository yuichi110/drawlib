# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Network concept icon: client_pc."""

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

# Monitor stand neck (drawn first so bezel and keyboard borders sit cleanly over the seams)
rectangle(
    (50.0, 31.0),
    width=12.0,
    height=10.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=2.2),
)

# Monitor bezel
rectangle(
    (50.0, 60.0),
    width=72.0,
    height=48.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=7.0),
)

# Inner white screen
rectangle(
    (50.0, 61.0),
    width=60.0,
    height=34.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0, shape_r=3.5),
)

# Pastel green window / terminal prompt accent inside screen
rectangle(
    (36.0, 69.0),
    width=22.0,
    height=6.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=1.8, shape_r=2.0),
)

# Lower horizontal keyboard / base bar
rectangle(
    (50.0, 21.0),
    width=56.0,
    height=10.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w, shape_r=4.0),
)

# 4 small dark key dots along y=21.0
for kx in (35.0, 45.0, 55.0, 65.0):
    circle((kx, 21.0), radius=1.7, style=fill_style(DARK))

save()
