# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: spark."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 1.9

# Outer 5-pointed tilted star vertices (tips P0..P4, valleys V0..V4)
outer_pts = [
    (45.5, 88.7),  # P0: top tip
    (59.0, 69.7),  # V0: top-right valley
    (87.7, 72.6),  # P1: right-top tip
    (69.5, 51.9),  # V1: right valley
    (79.1, 29.3),  # P2: right-bottom tip
    (54.8, 31.7),  # V2: bottom valley
    (33.1, 11.6),  # P3: bottom-left tip
    (31.8, 38.5),  # V3: left-bottom valley
    (11.6, 50.9),  # P4: left tip
    (35.2, 63.2),  # V4: top-left valley
]

# Inner 5-pointed tilted star cutout vertices (tips p0..p4, valleys v0..v4)
inner_pts = [
    (45.9, 76.8),  # p0: top inner tip
    (55.4, 61.8),  # v0: top-right inner valley
    (75.8, 66.4),  # p1: right-top inner tip
    (62.5, 51.1),  # v1: right inner valley
    (71.0, 35.4),  # p2: right-bottom inner tip
    (53.7, 40.0),  # v2: bottom inner valley
    (37.4, 22.5),  # p3: bottom-left inner tip
    (40.4, 45.5),  # v3: left-bottom inner valley
    (25.3, 51.4),  # p4: left inner tip
    (44.5, 57.4),  # v4: top-left inner valley
]

outer_radii = (4.2, 1.0, 4.2, 1.0, 4.2, 1.0, 4.2, 1.0, 4.2, 1.0)

# 1. Base tilted star filled in Colors.Orange3
polygon(
    outer_pts,
    style=fill_style(Colors.Orange3, shape_r=outer_radii),
)

# 2. Dynamic top-right burst ray accented in Colors.Amber3
burst_ray = [
    outer_pts[1],  # V0
    outer_pts[2],  # P1
    outer_pts[3],  # V1
    inner_pts[3],  # v1
    inner_pts[2],  # p1
    inner_pts[1],  # v0
]
polygon(
    burst_ray,
    style=fill_style(Colors.Amber3, shape_r=(0.0, 4.2, 0.0, 0.0, 1.2, 0.0)),
)

# 3. Inner hollow star filled in WHITE
polygon(inner_pts, style=no_border_fill(WHITE))

# 4. Crisp seam lines and inner/outer structural outlines
draw_round_segment(inner_pts[1], outer_pts[1], width_units=1.7, color=DARK)
draw_round_segment(inner_pts[3], outer_pts[3], width_units=1.7, color=DARK)
draw_round_polyline(inner_pts, width_units=1.8, color=DARK, closed=True)
polygon(
    outer_pts,
    style=fill_style(
        (0, 0, 0, 0),
        border_color=DARK,
        border_units=w,
        shape_r=outer_radii,
    ),
)

save()
