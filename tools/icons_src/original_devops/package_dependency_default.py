# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: package_dependency."""

from drawlib.canvas import save
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

# Orthogonal dependency tree lines connecting parent cube to child cubes
Icon.draw_round_segment((50.0, 52.0), (50.0, 44.5), width_units=w, color=Icon.DARK)
Icon.draw_round_polyline(
    [(27.0, 34.0), (27.0, 44.5), (73.0, 44.5), (73.0, 34.0)],
    corner_r=4.0,
    width_units=w,
    color=Icon.DARK,
)

# Top parent isometric 3D package cube
Icon.draw_iso_cube(
    50.0,
    68.5,
    radius=16.5,
    top_color=Icon.PASTEL_GREEN,
    left_color=Icon.PASTEL_BLUE,
    right_color=Icon.PASTEL_BLUE_LIGHT,
    border_color=Icon.DARK,
    border_units=w,
)

# Two child isometric 3D package cubes
for cx in (27.0, 73.0):
    Icon.draw_iso_cube(
        cx,
        24.5,
        radius=12.0,
        top_color=Icon.WHITE,
        left_color=Icon.PASTEL_BLUE,
        right_color=Icon.PASTEL_BLUE_LIGHT,
        border_color=Icon.DARK,
        border_units=2.0,
    )

save()
