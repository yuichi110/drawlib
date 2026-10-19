# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco network icon: cisco_l2_switch (modern 2D badge variant)."""

from drawlib.canvas import save
from drawlib.utils import Cisco, Icon

Icon.setup()

Cisco.draw_modern_badge()

# Four alternating horizontal left/right arrows (2 pointing left, 2 pointing right)
sw, hl, hw = 6.4, 9.5, 14.2
Cisco.draw_arrow((49.0, 65.0), (24.0, 65.0), shaft_w=sw, head_len=hl, head_w=hw, color=Icon.WHITE)
Cisco.draw_arrow((51.0, 55.0), (76.0, 55.0), shaft_w=sw, head_len=hl, head_w=hw, color=Icon.WHITE)
Cisco.draw_arrow((49.0, 45.0), (24.0, 45.0), shaft_w=sw, head_len=hl, head_w=hw, color=Icon.WHITE)
Cisco.draw_arrow((51.0, 35.0), (76.0, 35.0), shaft_w=sw, head_len=hl, head_w=hw, color=Icon.WHITE)

save()
