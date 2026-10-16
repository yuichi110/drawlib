# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: dapr."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# Rounded hat crown (extends down behind the brim so side walls stay straight)
rectangle(
    (50.0, 52.5),
    width=52.0,
    height=51.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=12.0),
)

# Small white highlight pill on left crown
rectangle(
    (32.5, 62.5),
    width=6.0,
    height=15.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0, shape_r=2.8),
)

# Horizontal pastel green hat ribbon band
rectangle(
    (50.0, 42.5),
    width=52.0,
    height=10.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.3),
)

# Wide curved hat brim at bottom
rectangle(
    (50.0, 31.5),
    width=78.0,
    height=15.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=7.0),
)

save()
