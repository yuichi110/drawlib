# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Server icon: dell_rack_server_default."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.styles import Colors
from drawlib.utils import (
    DELL_BLUE,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

BORDER = 4.8

# Top and middle horizontal rack enclosures (outer x=15..85, y=60..85 and y=30..55)
for cy in (72.5, 42.5):
    rectangle(
        (50.0, cy),
        width=70.0 - BORDER,
        height=25.0 - BORDER,
        style=fill_style(
            Colors.Transparent,
            border_color=DELL_BLUE,
            border_units=BORDER,
            shape_r=2.5,
        ),
    )
    # Horizontal center slot bar (x=35..65, height=5.0)
    rectangle(
        (50.0, cy),
        width=30.0,
        height=5.0,
        style=no_border_fill(DELL_BLUE),
    )

# Bottom rack bus T-pedestal (vertical stem x=50, y=15..24 + horizontal bar x=15..85, y=15)
rectangle(
    (50.0, 15.0),
    width=70.0,
    height=5.0,
    style=no_border_fill(DELL_BLUE),
)
rectangle(
    (50.0, 19.5),
    width=5.0,
    height=9.0,
    style=no_border_fill(DELL_BLUE),
)

save()
