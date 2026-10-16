# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Server icon: vmware_vswitch_default."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.styles import Colors
from drawlib.utils import (
    VMWARE_CYAN,
    VMWARE_NAVY,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

# Rectangular virtual switch chassis (x=10..90, y=26..74)
rectangle(
    (50.0, 50.0),
    width=80.0,
    height=48.0,
    style=fill_style(Colors.Transparent, border_color=VMWARE_NAVY, border_units=4.6, shape_r=3.0),
)

# 3 stepped RJ45 Ethernet port cutouts centered at x=27.0, 50.0, 73.0 (y=36..64)
for cx in (27.0, 50.0, 73.0):
    port_pts = [
        (cx - 8.2, 36.0),
        (cx + 8.2, 36.0),
        (cx + 8.2, 57.5),
        (cx + 4.0, 57.5),
        (cx + 4.0, 64.0),
        (cx - 4.0, 64.0),
        (cx - 4.0, 57.5),
        (cx - 8.2, 57.5),
    ]
    draw_round_polyline(port_pts, width_units=3.6, color=VMWARE_CYAN, closed=True)

    # 3 tiny vertical contact pins at the bottom of each RJ45 jack
    for pin_x in (cx - 3.8, cx, cx + 3.8):
        draw_round_segment((pin_x, 36.0), (pin_x, 42.5), width_units=2.4, color=VMWARE_CYAN)

save()
