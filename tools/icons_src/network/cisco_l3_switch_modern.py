# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco network icon: cisco_l3_switch (modern 2D badge variant)."""

from drawlib.canvas import save
from drawlib.utils import (
    draw_cisco_l3_star,
    draw_cisco_modern_badge,
    setup_icon,
)

setup_icon()

draw_cisco_modern_badge()
draw_cisco_l3_star(50.0, 50.0, 12.5, 29.0, shaft_w=3.2, head_len=6.5, head_w=8.8)

save()
