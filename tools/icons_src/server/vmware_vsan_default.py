# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Server icon: vmware_vsan_default."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import (
    VMWARE_CYAN,
    VMWARE_GREEN,
    VMWARE_NAVY,
    draw_round_polyline,
    fill_style,
    setup_icon,
)

setup_icon()

# Outer isometric diamond layer
polygon(
    [(50.0, 88.0), (88.0, 56.0), (50.0, 24.0), (12.0, 56.0)],
    style=fill_style(Colors.Transparent, border_color=VMWARE_NAVY, border_units=4.6, shape_r=3.5),
)

# Middle diamond ring
polygon(
    [(50.0, 75.0), (73.0, 56.0), (50.0, 37.0), (27.0, 56.0)],
    style=fill_style(Colors.Transparent, border_color=VMWARE_CYAN, border_units=4.2, shape_r=2.0),
)

# Solid center diamond core
polygon(
    [(50.0, 65.0), (61.0, 56.0), (50.0, 47.0), (39.0, 56.0)],
    style=fill_style(VMWARE_GREEN, shape_r=1.2),
)

# Bottom stacked layer V-chevron
draw_round_polyline(
    [(14.0, 39.0), (50.0, 10.0), (86.0, 39.0)],
    width_units=4.6,
    color=VMWARE_NAVY,
    corner_r=3.5,
)

save()
