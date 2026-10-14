# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: batch_job."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

rectangle(
    (54.0, 58.0),
    width=54.0,
    height=54.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=6.0),
)

rectangle(
    (44.0, 46.0),
    width=54.0,
    height=54.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w, shape_r=6.0),
)

for y_bar in (60.0, 46.0, 32.0):
    draw_round_segment((28.0, y_bar), (56.0, y_bar), width_units=3.0, color=DARK)

circle(
    (70.0, 28.0),
    radius=14.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w),
)

play_pts = [(66.0, 34.0), (66.0, 22.0), (77.0, 28.0)]
polygon(play_pts, style=no_border_fill(WHITE))
draw_round_polyline(play_pts, width_units=2.0, color=DARK, closed=True)

save()
