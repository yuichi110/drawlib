# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original DevOps concept icon: splunk."""

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    WHITE,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 1.9

# 1. Green3 rounded square badge with DARK w=1.9 border
rectangle(
    (50.0, 50.0),
    width=78.0,
    height=78.0,
    style=fill_style(Colors.Green3, border_color=DARK, border_units=w, shape_r=15.0),
)

# 2. Crisp WHITE '>' chevron polygon with DARK 1.7 border
chevron_pts: list[tuple[float, float]] = [
    (34.0, 66.5),
    (68.5, 54.4),
    (68.5, 45.0),
    (34.0, 30.0),
    (34.0, 36.6),
    (62.8, 49.7),
    (34.0, 59.6),
]

polygon(chevron_pts, style=no_border_fill(WHITE))
draw_round_polyline(chevron_pts, width_units=1.7, color=DARK, closed=True)

save()
