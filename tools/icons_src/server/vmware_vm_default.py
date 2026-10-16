# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Server icon: vmware_vm."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.styles import Colors
from drawlib.utils import (
    VMWARE_CYAN,
    VMWARE_NAVY,
    draw_round_polyline,
    fill_style,
    setup_icon,
)

setup_icon()

# Middle-right square stroke: top bar starts at x=49.0 (inside top-center) to (42.0, 44.0) (inside bottom-left)
draw_round_polyline(
    [
        (49.0, 72.0),
        (88.0, 72.0),
        (88.0, 24.0),
        (42.0, 24.0),
        (42.0, 44.0),
    ],
    width_units=4.6,
    color=VMWARE_NAVY,
    corner_r=5.5,
)

# Top-center square stroke: left leg from y=58.0 (top of bottom-left) up/right to y=56.0 (inside middle-right)
draw_round_polyline(
    [
        (27.0, 58.0),
        (27.0, 88.0),
        (70.0, 88.0),
        (70.0, 56.0),
    ],
    width_units=4.6,
    color=VMWARE_CYAN,
    corner_r=5.5,
)

# Bottom-left foreground square: full rounded square border (weaves over top-center and middle-right)
rectangle(
    (35.0, 35.0),
    width=46.0,
    height=46.0,
    style=fill_style(Colors.Transparent, border_color=VMWARE_NAVY, border_units=4.6, shape_r=5.5),
)

save()
