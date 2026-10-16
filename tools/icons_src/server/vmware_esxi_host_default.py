# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Server icon: vmware_esxi_host."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.styles import Colors
from drawlib.utils import (
    VMWARE_CYAN,
    VMWARE_NAVY,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

# Bottom 2 stacked physical rack server units (vvd_icons/vm-server.svg)
for cy in (21.0, 46.0):
    rectangle(
        (50.0, cy),
        width=80.0,
        height=18.0,
        style=fill_style(Colors.Transparent, border_color=VMWARE_NAVY, border_units=4.4, shape_r=2.0),
    )

    # 3 left vertical vent bars
    for vx in (17.0, 21.0, 25.0):
        rectangle(
            (vx, cy),
            width=2.5,
            height=8.0,
            style=no_border_fill(VMWARE_NAVY, shape_r=0.3),
        )

    # Center status ring
    circle(
        (50.0, cy),
        radius=4.3,
        style=fill_style(Colors.Transparent, border_color=VMWARE_CYAN, border_units=3.6),
    )

    # 3 right vertical vent bars
    for vx in (75.0, 79.0, 83.0):
        rectangle(
            (vx, cy),
            width=2.5,
            height=8.0,
            style=no_border_fill(VMWARE_NAVY, shape_r=0.3),
        )

# Top 3 square VM boxes (y=65..85) with inner geometric square detail (no text)
for vm_cx in (22.0, 50.0, 78.0):
    rectangle(
        (vm_cx, 75.0),
        width=20.0,
        height=20.0,
        style=fill_style(Colors.Transparent, border_color=VMWARE_CYAN, border_units=4.2, shape_r=2.5),
    )
    rectangle(
        (vm_cx, 75.0),
        width=8.0,
        height=8.0,
        style=fill_style(Colors.Transparent, border_color=VMWARE_NAVY, border_units=2.8, shape_r=1.0),
    )

save()
