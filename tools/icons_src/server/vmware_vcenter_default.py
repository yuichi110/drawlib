# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Server icon: vmware_vcenter."""

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
from drawlib.styles import Colors
from drawlib.utils import (
    VMWARE_CYAN,
    VMWARE_NAVY,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

# Stepped dual-square outline formed by two merged squares (x=10..62 and x=38..90, vcenter-server.svg)
merged_pts = [
    (10.0, 10.0),
    (62.0, 10.0),
    (62.0, 38.0),
    (90.0, 38.0),
    (90.0, 90.0),
    (38.0, 90.0),
    (38.0, 62.0),
    (10.0, 62.0),
]
polygon(
    merged_pts,
    style=fill_style(
        Colors.Transparent,
        border_color=VMWARE_NAVY,
        border_units=4.6,
        shape_r=(5.0, 5.0, 0.0, 5.0, 5.0, 5.0, 0.0, 5.0),
    ),
)

# Two solid filled rounded squares along the diagonal intersection
# Bottom-left solid square (x=28..48, y=28..48)
rectangle(
    (38.0, 38.0),
    width=20.0,
    height=20.0,
    style=no_border_fill(VMWARE_NAVY, shape_r=3.5),
)
# Top-right solid square (x=52..72, y=52..72)
rectangle(
    (62.0, 62.0),
    width=20.0,
    height=20.0,
    style=no_border_fill(VMWARE_CYAN, shape_r=3.5),
)

save()
