# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco network topology icon: load balancer (modern 2D SAFE variant)."""

from drawlib.canvas import save
from drawlib.shapes import circle
from drawlib.utils import Cisco, Icon

Icon.setup()

Cisco.draw_modern_badge()

# Central load-distribution ring (matching SAFE Arch_63_Load Balancer)
circle(
    (48.0, 50.0),
    radius=13.0,
    style=Icon.stroke_style(Icon.WHITE, width_units=4.4),
)

# 1 horizontal input arrow entering from the left
Cisco.draw_arrow(
    (18.5, 50.0),
    (31.2, 50.0),
    shaft_w=4.4,
    head_len=6.2,
    head_w=10.2,
    color=Icon.WHITE,
)

# 3 fan-out output arrows exiting to the right
Cisco.draw_arrow(
    (63.2, 57.2),
    (79.5, 66.5),
    shaft_w=4.0,
    head_len=6.4,
    head_w=9.6,
    color=Icon.WHITE,
)
Cisco.draw_arrow(
    (65.0, 50.0),
    (81.5, 50.0),
    shaft_w=4.0,
    head_len=6.4,
    head_w=9.6,
    color=Icon.WHITE,
)
Cisco.draw_arrow(
    (63.2, 42.8),
    (79.5, 33.5),
    shaft_w=4.0,
    head_len=6.4,
    head_w=9.6,
    color=Icon.WHITE,
)

save()
