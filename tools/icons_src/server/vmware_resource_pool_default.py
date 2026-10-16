# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Server icon: vmware_resource_pool_default."""

from drawlib.canvas import save
from drawlib.shapes import circle
from drawlib.utils import (
    VMWARE_CYAN,
    VMWARE_NAVY,
    draw_round_polyline,
    setup_icon,
    stroke_style,
)

setup_icon()

cx, cy = 50.0, 50.0
r = 38.0

# Two crisp radial divider lines from center to (88.0, 50.0) and (25.6, 20.9)
draw_round_polyline(
    [(25.6, 20.9), (cx, cy), (88.0, 50.0)],
    width_units=4.8,
    color=VMWARE_CYAN,
)

# Outer structural circle ring on top to cleanly cap divider line ends
circle(
    (cx, cy),
    radius=r,
    style=stroke_style(VMWARE_NAVY, width_units=4.8),
)

save()
