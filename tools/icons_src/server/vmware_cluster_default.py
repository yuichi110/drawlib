# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Server icon: vmware_cluster_default."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.styles import Colors
from drawlib.utils import (
    VMWARE_CYAN,
    VMWARE_NAVY,
    draw_round_polyline,
    fill_style,
    setup_icon,
)

setup_icon()

# Left and right background host wings (clipped at x=31 and x=69)
draw_round_polyline(
    [(31.0, 77.0), (13.0, 77.0), (13.0, 13.0), (31.0, 13.0)],
    width_units=4.6,
    color=VMWARE_NAVY,
    corner_r=3.5,
)
draw_round_polyline(
    [(69.0, 77.0), (87.0, 77.0), (87.0, 13.0), (69.0, 13.0)],
    width_units=4.6,
    color=VMWARE_NAVY,
    corner_r=3.5,
)

# Taller center foreground host tower (x=31..69, y=13..88)
rectangle(
    (50.0, 50.5),
    width=38.0,
    height=75.0,
    style=fill_style(Colors.Transparent, border_color=VMWARE_NAVY, border_units=4.6, shape_r=4.0),
)

# Top horizontal slot bar (x=39..61, y=74)
rectangle(
    (50.0, 74.0),
    width=22.0,
    height=4.4,
    style=fill_style(VMWARE_CYAN, shape_r=1.2),
)

# Bottom circular power button
circle(
    (50.0, 27.0),
    radius=4.8,
    style=fill_style(VMWARE_CYAN),
)

save()
