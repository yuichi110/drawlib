# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco network icon: cisco_l2_switch (default classic 3D variant)."""

from drawlib.canvas import save
from drawlib.utils import Cisco, Icon

Icon.setup()

x0, y0 = 10.0, 30.0
w_front, h_front = 62.0, 22.0
dx, dy = 18.0, 16.0

Cisco.draw_3d_box(x0, y0, w_front, h_front, dx, dy)


def _top_pt(u: float, v: float) -> tuple[float, float]:
    return (x0 + w_front * u + dx * v, y0 + h_front + dy * v)


# Four alternating left/right horizontal arrows following the oblique top slant
sw, hl, hw = 1.7, 5.6, 4.0
Cisco.draw_arrow(_top_pt(0.50, 0.20), _top_pt(0.13, 0.20), shaft_w=sw, head_len=hl, head_w=hw, color=Icon.WHITE)
Cisco.draw_arrow(_top_pt(0.47, 0.39), _top_pt(0.84, 0.39), shaft_w=sw, head_len=hl, head_w=hw, color=Icon.WHITE)
Cisco.draw_arrow(_top_pt(0.50, 0.58), _top_pt(0.13, 0.58), shaft_w=sw, head_len=hl, head_w=hw, color=Icon.WHITE)
Cisco.draw_arrow(_top_pt(0.47, 0.76), _top_pt(0.84, 0.76), shaft_w=sw, head_len=hl, head_w=hw, color=Icon.WHITE)

save()
