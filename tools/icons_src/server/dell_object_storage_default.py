# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Server icon: dell_object_storage_default."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.styles import Colors
from drawlib.utils import Dell, Icon

Icon.setup()

# Top equilateral triangle object
polygon(
    [(50.0, 86.0), (31.0, 54.0), (69.0, 54.0)],
    style=Icon.fill_style(Colors.Transparent, border_color=Dell.BLUE, border_units=4.8, shape_r=2.0),
)

# Bottom-left square object
rectangle(
    (30.5, 30.0),
    width=29.0,
    height=29.0,
    style=Icon.fill_style(Colors.Transparent, border_color=Dell.BLUE, border_units=4.8, shape_r=2.5),
)

# Bottom-right circle object
circle(
    (70.0, 30.0),
    radius=15.5,
    style=Icon.fill_style(Colors.Transparent, border_color=Dell.BLUE, border_units=4.8),
)

save()
