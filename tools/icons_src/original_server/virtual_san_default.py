# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Server concept icon: virtual_san."""

from drawlib.canvas import save
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_cylinder_tier,
    draw_iso_cube,
    draw_round_polyline,
    draw_round_segment,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

hosts = [
    (50.0, 76.0),
    (24.0, 28.0),
    (76.0, 28.0),
]

# Triangular ring interconnect between the 3 HCI hosts
draw_round_polyline(
    hosts,
    width_units=w,
    color=DARK,
    closed=True,
)

# Radial storage fabric connections from central pool to all 3 hosts
for hx, hy in hosts:
    draw_round_segment((50.0, 44.0), (hx, hy), width_units=2.2, color=DARK)

# 3 HCI host 3D isometric cubes at the triangle vertices
for hx, hy in hosts:
    draw_iso_cube(
        hx,
        hy,
        radius=12.5,
        top_color=WHITE,
        left_color=PASTEL_BLUE,
        right_color=PASTEL_BLUE_LIGHT,
        border_color=DARK,
        border_units=2.3,
    )

# Shared PASTEL_GREEN 3D storage cylinder at the center
draw_cylinder_tier(
    50.0,
    36.0,
    width=26.0,
    body_h=14.0,
    ry=5.0,
    body_color=PASTEL_GREEN,
    top_color=WHITE,
    border_color=DARK,
    border_units=2.4,
)

save()
