# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco network icon: cisco_router (default classic 3D variant)."""

from drawlib.canvas import save
from drawlib.utils import (
    draw_cisco_3d_cylinder,
    draw_cisco_router_top_arrows,
    setup_icon,
)

setup_icon()

draw_cisco_3d_cylinder(50.0, 33.0, 78.0, 22.0, 15.0)
draw_cisco_router_top_arrows(50.0, 55.0, 39.0, 15.0)

save()
