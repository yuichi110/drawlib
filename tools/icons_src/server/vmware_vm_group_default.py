# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Server icon: vmware_vm_group."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.styles import Colors
from drawlib.utils import Icon, Vmware

Icon.setup()

# Outer container frame (x=12..88, y=10..90) with folded bottom-right corner (vsphere_icons/vSphere VMs.svg)
frame_pts = [
    (12.0, 10.0),
    (72.0, 10.0),
    (88.0, 26.0),
    (88.0, 90.0),
    (12.0, 90.0),
]
Icon.draw_round_polyline(frame_pts, width_units=4.4, color=Vmware.NAVY, closed=True)

# Folded bottom-right corner inner flap
Icon.draw_round_polyline(
    [(72.0, 10.0), (72.0, 26.0), (88.0, 26.0)],
    width_units=4.0,
    color=Vmware.NAVY,
)

# Back VM square (44, 66) (x=31..57, y=53..79, clipped at front & middle squares)
Icon.draw_round_polyline(
    [(31.0, 55.0), (31.0, 79.0), (57.0, 79.0), (57.0, 65.0)],
    width_units=4.0,
    color=Vmware.CYAN,
    corner_r=2.5,
)

# Middle VM square (55, 52) (x=42..68, y=39..65, clipped at front square)
Icon.draw_round_polyline(
    [(48.0, 39.0), (68.0, 39.0), (68.0, 65.0), (42.0, 65.0), (42.0, 55.0)],
    width_units=4.0,
    color=Vmware.CYAN,
    corner_r=2.5,
)

# Front VM square (35, 42) (x=22..48, y=29..55)
rectangle(
    (35.0, 42.0),
    width=26.0,
    height=26.0,
    style=Icon.fill_style(Colors.Transparent, border_color=Vmware.CYAN, border_units=4.0, shape_r=2.5),
)

save()
