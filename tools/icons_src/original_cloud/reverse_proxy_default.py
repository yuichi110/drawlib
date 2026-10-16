# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: reverse_proxy."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# Client ingress arrow entering the front reverse proxy bar
draw_round_segment((13.0, 50.0), (26.0, 50.0), width_units=w, color=DARK)
draw_round_polyline(
    [(20.0, 55.5), (26.0, 50.0), (20.0, 44.5)],
    width_units=w,
    color=DARK,
)

# Rounded orthogonal routing paths to backend servers
draw_round_polyline(
    [(44.0, 58.0), (55.0, 58.0), (55.0, 69.0), (66.0, 69.0)],
    width_units=w,
    color=DARK,
    corner_r=5.5,
)
draw_round_polyline(
    [(44.0, 42.0), (55.0, 42.0), (55.0, 31.0), (66.0, 31.0)],
    width_units=w,
    color=DARK,
    corner_r=5.5,
)

# Front reverse proxy gateway bar
rectangle(
    (36.0, 50.0),
    width=16.0,
    height=58.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w, shape_r=5.0),
)
circle(
    (36.0, 50.0),
    radius=4.5,
    style=fill_style(WHITE, border_color=DARK, border_units=2.1),
)
draw_round_segment((33.0, 66.0), (39.0, 66.0), width_units=2.2, color=DARK)
draw_round_segment((33.0, 34.0), (39.0, 34.0), width_units=2.2, color=DARK)

# 2 protected backend server nodes on the right
for by in (69.0, 31.0):
    rectangle(
        (76.0, by),
        width=20.0,
        height=20.0,
        style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=4.5),
    )
    draw_round_segment((71.5, by + 3.5), (80.5, by + 3.5), width_units=2.1, color=DARK)
    circle(
        (73.0, by - 3.5),
        radius=2.5,
        style=fill_style(WHITE, border_color=DARK, border_units=1.8),
    )

save()
