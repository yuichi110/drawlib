# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code concept icon: rpc_call."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w_shape = 1.8

# 1. Left PASTEL_BLUE service block ((24, 50), width=24, height=48, shape_r=4.0)
rectangle(
    (24.0, 50.0),
    width=24.0,
    height=48.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w_shape, shape_r=4.0),
)
circle((19.0, 67.0), radius=2.2, style=fill_style(WHITE, border_color=DARK, border_units=w_shape))

# 2. Right WHITE service block ((76, 50), width=24, height=48, shape_r=4.0)
rectangle(
    (76.0, 50.0),
    width=24.0,
    height=48.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w_shape, shape_r=4.0),
)
circle((71.0, 67.0), radius=2.2, style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_shape))

# 3. Bold horizontal PASTEL_GREEN lightning-bolt arrow bridging across the center
bolt_pts = [
    (27.5, 52.0),
    (49.5, 62.0),
    (46.5, 49.5),
    (59.5, 54.0),
    (59.5, 60.5),
    (72.5, 50.0),
    (59.5, 39.5),
    (59.5, 46.0),
    (40.0, 39.0),
    (43.0, 51.5),
    (27.5, 44.0),
]
polygon(bolt_pts, style=no_border_fill(PASTEL_GREEN))
draw_round_polyline(bolt_pts, width_units=w_shape, color=DARK, closed=True)

save()
