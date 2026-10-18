# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: etl_pipeline."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

nodes = [
    (34.0, 80.0, PASTEL_BLUE),
    (50.0, 82.0, WHITE),
    (66.0, 80.0, PASTEL_BLUE),
]
for nx, ny, ncol in nodes:
    circle(
        (nx, ny),
        radius=5.0,
        style=fill_style(ncol, border_color=DARK, border_units=2.0),
    )

funnel_pts = [
    (20.0, 68.0),
    (80.0, 68.0),
    (57.0, 42.0),
    (57.0, 26.0),
    (43.0, 26.0),
    (43.0, 42.0),
]
polygon(funnel_pts, style=fill_style(PASTEL_BLUE))
draw_round_polyline(funnel_pts, width_units=w, color=DARK, closed=True)

rectangle(
    (50.0, 68.0),
    width=64.0,
    height=8.0,
    style=fill_style(WHITE, border_color=DARK, border_units=w, shape_r=3.5),
)

rectangle(
    (50.0, 16.0),
    width=28.0,
    height=10.0,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0, shape_r=3.0),
)

save()
