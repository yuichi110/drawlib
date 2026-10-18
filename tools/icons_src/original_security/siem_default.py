# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security concept icon: siem."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w_shape = 2.0
w_line = 2.0

# Vertical flow connector from funnel outlet into dashboard card
draw_round_segment((50.0, 52.0), (50.0, 44.0), width_units=w_line, color=DARK)

# Top 3 log source circles
log_sources = [
    ((30.0, 82.0), PASTEL_BLUE_LIGHT),
    ((50.0, 84.0), WHITE),
    ((70.0, 82.0), PASTEL_BLUE_LIGHT),
]
for xy, col in log_sources:
    circle(
        xy,
        radius=4.2,
        style=fill_style(col, border_color=DARK, border_units=w_shape),
    )

# Middle PASTEL_BLUE trapezoid log aggregation funnel
funnel_pts = [
    (22.0, 72.0),
    (78.0, 72.0),
    (57.0, 52.0),
    (43.0, 52.0),
]
polygon(funnel_pts, style=no_border_fill(PASTEL_BLUE))
draw_round_polyline(
    funnel_pts,
    width_units=w_shape,
    color=DARK,
    closed=True,
)

# Bottom WHITE correlation alert dashboard card
rectangle(
    (50.0, 28.0),
    width=64.0,
    height=32.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w_shape, shape_r=5.0),
)

# PASTEL_GREEN alert circle badge with DARK exclamation mark
circle(
    (32.0, 28.0),
    radius=8.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w_shape),
)
draw_round_segment((32.0, 32.0), (32.0, 27.0), width_units=2.0, color=DARK)
circle((32.0, 23.6), radius=1.3, style=fill_style(DARK))

# 2 horizontal DARK metric bars on the right side of the dashboard
draw_round_segment((46.0, 32.5), (72.0, 32.5), width_units=w_line, color=DARK)
draw_round_segment((46.0, 23.5), (66.0, 23.5), width_units=w_line, color=DARK)

save()
