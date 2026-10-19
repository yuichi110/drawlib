# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco network icon: cisco_l3_switch (default classic 3D variant)."""

from drawlib.canvas import save
from drawlib.utils import Cisco, Icon

Icon.setup()

Cisco.draw_3d_box(16.0, 16.0, 54.0, 54.0, 14.0, 14.0)
Cisco.draw_l3_star(43.0, 43.0, 10.5, 22.5, shaft_w=2.6, head_len=5.2, head_w=7.2)

save()
