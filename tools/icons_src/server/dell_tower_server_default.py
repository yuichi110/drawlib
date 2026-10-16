# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Server icon: dell_tower_server_default."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.styles import Colors
from drawlib.utils import (
    DELL_BLUE,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

BORDER = 4.8

# Tall vertical tower enclosure (outer x=25..75, y=10..90)
rectangle(
    (50.0, 50.0),
    width=50.0 - BORDER,
    height=80.0 - BORDER,
    style=fill_style(
        Colors.Transparent,
        border_color=DELL_BLUE,
        border_units=BORDER,
        shape_r=2.5,
    ),
)

# Top-right square power button (x=58..64, y=73..79, right-aligned with drive bars)
rectangle(
    (61.0, 76.0),
    width=6.0,
    height=6.0,
    style=no_border_fill(DELL_BLUE),
)

# 4 horizontal drive bay bars (x=36..64, height=5.0) at y=60, 48, 36, 24
for bay_y in (60.0, 48.0, 36.0, 24.0):
    rectangle(
        (50.0, bay_y),
        width=28.0,
        height=5.0,
        style=no_border_fill(DELL_BLUE),
    )

save()
