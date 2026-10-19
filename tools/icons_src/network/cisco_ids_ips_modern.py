# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco modern 2D icon: ids_ips (modern variant)."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import Cisco, Icon

Icon.setup()
Cisco.draw_modern_badge()

# Central inspection circle barrier (matching Arch_63_Intrusion Prevention.png)
circle((50.0, 50.0), radius=18.0, style=Icon.stroke_style(Icon.WHITE, width_units=3.4))

# Top rightward arrow and bottom leftward arrow across the barrier
Cisco.draw_arrow((22.0, 59.5), (78.0, 59.5), shaft_w=3.2, head_len=6.8, head_w=9.0, color=Icon.WHITE)
Cisco.draw_arrow((78.0, 40.5), (22.0, 40.5), shaft_w=3.2, head_len=6.8, head_w=9.0, color=Icon.WHITE)

# Crisp inner protective shield emblem at center
left_sh = Icon.build_shield_half_points(50.0, 43.2, 56.8, 5.6, side="left")
right_sh = Icon.build_shield_half_points(50.0, 43.2, 56.8, 5.6, side="right")
polygon(left_sh + list(reversed(right_sh[1:-1])), style=Icon.no_border_fill(Icon.WHITE))

save()
