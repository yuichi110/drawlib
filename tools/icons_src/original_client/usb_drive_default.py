# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Client concept icon: usb_drive."""

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

# 1. Bottom lanyard loop cap (PASTEL_BLUE_LIGHT)
rectangle(
    (50.0, 17.5),
    width=20.0,
    height=9.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=2.2, shape_r=4.2),
)
rectangle(
    (50.0, 16.5),
    width=8.5,
    height=3.2,
    style=fill_style(WHITE, border_color=DARK, border_units=1.5, shape_r=1.5),
)

# 2. Metal USB-A plug at top (WHITE) with 2 dark connector holes
rectangle(
    (50.0, 74.0),
    width=26.0,
    height=21.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w, shape_r=2.5),
)
for hole_x in (44.5, 55.5):
    rectangle(
        (hole_x, 76.0),
        width=4.6,
        height=5.8,
        style=fill_style(DARK, shape_r=0.8),
    )

# 3. Main USB flash drive / security key body (PASTEL_BLUE)
rectangle(
    (50.0, 44.0),
    width=40.0,
    height=48.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=8.0),
)

# 4. Capacitive touch / status LED circle (PASTEL_GREEN)
circle(
    (50.0, 45.0),
    radius=10.5,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.4),
)
circle(
    (50.0, 45.0),
    radius=3.2,
    style=fill_style(WHITE, border_color=DARK, border_units=1.8),
)

save()
