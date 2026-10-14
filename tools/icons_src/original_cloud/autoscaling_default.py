# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: autoscaling."""

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

corners = [(20.0, 80.0), (80.0, 80.0), (20.0, 20.0), (80.0, 20.0)]
for corner in corners:
    draw_round_segment((50.0, 50.0), corner, width_units=w, color=DARK)

arrow_heads = [
    [(20.0, 66.0), (20.0, 80.0), (34.0, 80.0)],
    [(66.0, 80.0), (80.0, 80.0), (80.0, 66.0)],
    [(20.0, 34.0), (20.0, 20.0), (34.0, 20.0)],
    [(66.0, 20.0), (80.0, 20.0), (80.0, 34.0)],
]
for head in arrow_heads:
    draw_round_polyline(head, width_units=w, color=DARK)

rectangle(
    (50.0, 50.0),
    width=44.0,
    height=44.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w, shape_r=6.0),
)

rectangle(
    (50.0, 50.0),
    width=24.0,
    height=24.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=2.4, shape_r=4.0),
)

circle(
    (50.0, 50.0),
    radius=4.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0),
)

save()
