# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: backup_archive."""

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

rectangle(
    (50.0, 42.0),
    width=64.0,
    height=48.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=5.0),
)

rectangle(
    (50.0, 70.0),
    width=72.0,
    height=14.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w, shape_r=4.0),
)

rectangle(
    (50.0, 50.0),
    width=22.0,
    height=8.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.2, shape_r=4.0),
)

save()
