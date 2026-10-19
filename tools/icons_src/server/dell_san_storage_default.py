# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Server icon: dell_san_storage_default."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.styles import Colors
from drawlib.utils import Dell, Icon

Icon.setup()

# Wide storage array enclosure (outer x=10..90, y=21..79, border=4.8 -> centerline 75.2x53.2)
rectangle(
    (50.0, 50.0),
    width=75.2,
    height=53.2,
    style=Icon.fill_style(Colors.Transparent, border_color=Dell.BLUE, border_units=4.8, shape_r=2.5),
)

# 3x3 matrix of 9 horizontal drive bay bars
for ry in (63.0, 50.0, 37.0):
    for rx in (27.0, 50.0, 73.0):
        rectangle(
            (rx, ry),
            width=11.5,
            height=5.0,
            style=Icon.no_border_fill(Dell.BLUE),
        )

save()
