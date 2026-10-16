# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Server icon: dell_fc_switch_default."""

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

# Two stacked horizontal 2U switch blades (outer x=10..90, top y=55..84, bottom y=16..45)
for cy in (69.5, 30.5):
    rectangle(
        (50.0, cy),
        width=75.2,
        height=24.2,
        style=fill_style(Colors.Transparent, border_color=DELL_BLUE, border_units=4.8, shape_r=2.5),
    )

    # Right-side port slot bar (x=62..79 -> cx=70.5, width=17.0, height=5.0)
    rectangle(
        (70.5, cy),
        width=17.0,
        height=5.0,
        style=no_border_fill(DELL_BLUE),
    )

save()
