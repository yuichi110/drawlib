# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco network icon: cisco_nexus_switch (modern 2D badge variant)."""

from drawlib.canvas import save
from drawlib.shapes import circle
from drawlib.utils import Cisco, Icon

Icon.setup()

Cisco.draw_modern_badge()

# Crossing diagonal X-fabric arrows with horizontal arrow tips
sw, hl, hw = 4.4, 8.8, 12.6
Icon.draw_round_segment((37.0, 68.0), (63.0, 32.0), width_units=sw, color=Icon.WHITE)
Icon.draw_round_segment((37.0, 32.0), (63.0, 68.0), width_units=sw, color=Icon.WHITE)

Cisco.draw_arrow((37.0, 68.0), (22.0, 68.0), shaft_w=sw, head_len=hl, head_w=hw, color=Icon.WHITE)
Cisco.draw_arrow((63.0, 32.0), (78.0, 32.0), shaft_w=sw, head_len=hl, head_w=hw, color=Icon.WHITE)
Cisco.draw_arrow((37.0, 32.0), (22.0, 32.0), shaft_w=sw, head_len=hl, head_w=hw, color=Icon.WHITE)
Cisco.draw_arrow((63.0, 68.0), (78.0, 68.0), shaft_w=sw, head_len=hl, head_w=hw, color=Icon.WHITE)

circle((50.0, 50.0), radius=6.2, style=Icon.fill_style(Icon.WHITE, border_color=Cisco.BLUE, border_units=2.0))

save()
