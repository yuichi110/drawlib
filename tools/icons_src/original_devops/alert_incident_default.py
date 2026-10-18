# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: alert_incident."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    WHITE,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

polygon(
    [(50.0, 84.0), (14.0, 20.0), (86.0, 20.0)],
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=7.0),
)

rectangle(
    (50.0, 52.0),
    width=8.0,
    height=22.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0, shape_r=4.0),
)
circle(
    (50.0, 29.0),
    radius=4.5,
    style=fill_style(WHITE, border_color=DARK, border_units=2.0),
)

save()
