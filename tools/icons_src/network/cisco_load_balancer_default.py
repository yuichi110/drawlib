# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco network topology icon: load balancer (default classic 3D variant)."""

from drawlib.canvas import save
from drawlib.utils import (
    WHITE,
    draw_cisco_3d_box,
    draw_cisco_arrow,
    setup_icon,
)

setup_icon()

# 3D appliance chassis (front: [10..74] x [23..61], top/side offset: +16, +16)
draw_cisco_3d_box(10.0, 23.0, 64.0, 38.0, 16.0, 16.0)

# Input arrow on the left half of the front face
draw_cisco_arrow(
    (17.5, 42.0),
    (39.0, 42.0),
    shaft_w=4.0,
    head_len=7.2,
    head_w=9.8,
    color=WHITE,
)

# 3 fan-out load-balancing output arrows on the right half of the front face
draw_cisco_arrow(
    (43.0, 45.8),
    (65.5, 55.2),
    shaft_w=3.5,
    head_len=6.8,
    head_w=8.8,
    color=WHITE,
)
draw_cisco_arrow(
    (44.0, 42.0),
    (67.0, 42.0),
    shaft_w=3.5,
    head_len=6.8,
    head_w=8.8,
    color=WHITE,
)
draw_cisco_arrow(
    (43.0, 38.2),
    (65.5, 28.8),
    shaft_w=3.5,
    head_len=6.8,
    head_w=8.8,
    color=WHITE,
)

save()
