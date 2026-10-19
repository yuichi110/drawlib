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
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

hosts = [
    (50.0, 76.0),
    (24.0, 28.0),
    (76.0, 28.0),
]

# Triangular ring interconnect between the 3 HCI hosts
Icon.draw_round_polyline(
    hosts,
    width_units=w,
    color=Icon.DARK,
    closed=True,
)

# Radial storage fabric connections from central pool to all 3 hosts
for hx, hy in hosts:
    Icon.draw_round_segment((50.0, 44.0), (hx, hy), width_units=2.0, color=Icon.DARK)

# 3 HCI host 3D isometric cubes at the triangle vertices
for hx, hy in hosts:
    Icon.draw_iso_cube(
        hx,
        hy,
        radius=12.5,
        top_color=Icon.WHITE,
        left_color=Icon.PASTEL_BLUE,
        right_color=Icon.PASTEL_BLUE_LIGHT,
        border_color=Icon.DARK,
        border_units=2.0,
    )

# Shared PASTEL_GREEN 3D storage cylinder at the center
Icon.draw_cylinder_tier(
    50.0,
    36.0,
    width=26.0,
    body_h=14.0,
    ry=5.0,
    body_color=Icon.PASTEL_GREEN,
    top_color=Icon.WHITE,
    border_color=Icon.DARK,
    border_units=2.0,
)

save()
