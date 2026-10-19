# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco network icon: cisco_wan_router (modern 2D badge variant)."""

from drawlib.canvas import save
from drawlib.shapes import circle, ellipse
from drawlib.utils import Cisco, Icon

Icon.setup()

Cisco.draw_modern_badge()

# 1. Central WAN globe at (50, 50)
gx, gy = 50.0, 50.0
gr = 14.5
circle((gx, gy), radius=gr, style=Icon.stroke_style(Icon.WHITE, width_units=3.0))
ellipse((gx, gy), width=14.0, height=gr * 2.0, style=Icon.stroke_style(Icon.WHITE, width_units=2.3))
Icon.draw_round_segment((gx - gr, gy), (gx + gr, gy), width_units=2.3, color=Icon.WHITE)
Icon.draw_round_segment((gx - 12.2, gy + 7.2), (gx + 12.2, gy + 7.2), width_units=2.0, color=Icon.WHITE)
Icon.draw_round_segment((gx - 12.2, gy - 7.2), (gx + 12.2, gy - 7.2), width_units=2.0, color=Icon.WHITE)

# 2. Four diagonal routing arrows around the WAN globe (2 inward, 2 outward)
sw, hl, hw = 3.4, 6.5, 8.6
Cisco.draw_arrow((25.0, 75.0), (37.0, 63.0), shaft_w=sw, head_len=hl, head_w=hw, color=Icon.WHITE)
Cisco.draw_arrow((75.0, 25.0), (63.0, 37.0), shaft_w=sw, head_len=hl, head_w=hw, color=Icon.WHITE)
Cisco.draw_arrow((63.0, 63.0), (75.0, 75.0), shaft_w=sw, head_len=hl, head_w=hw, color=Icon.WHITE)
Cisco.draw_arrow((37.0, 37.0), (25.0, 25.0), shaft_w=sw, head_len=hl, head_w=hw, color=Icon.WHITE)

save()
