# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: container_cluster."""

from drawlib.canvas import save
from drawlib.utils import Icon

Icon.setup()

Icon.draw_iso_cube(
    50.0,
    64.0,
    radius=21.0,
    top_color=Icon.WHITE,
    left_color=Icon.PASTEL_BLUE,
    right_color=Icon.PASTEL_BLUE_LIGHT,
    border_color=Icon.DARK,
    border_units=2.0,
)

Icon.draw_iso_cube(
    31.0,
    34.0,
    radius=21.0,
    top_color=Icon.WHITE,
    left_color=Icon.PASTEL_BLUE,
    right_color=Icon.PASTEL_GREEN,
    border_color=Icon.DARK,
    border_units=2.0,
)

Icon.draw_iso_cube(
    69.0,
    34.0,
    radius=21.0,
    top_color=Icon.WHITE,
    left_color=Icon.PASTEL_BLUE,
    right_color=Icon.PASTEL_GREEN,
    border_color=Icon.DARK,
    border_units=2.0,
)

save()
