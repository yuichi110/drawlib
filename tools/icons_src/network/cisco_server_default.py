# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco network topology icon: server (default classic 3D variant)."""

from drawlib.canvas import save
from drawlib.shapes import arc, rectangle
from drawlib.utils import Cisco, Icon

Icon.setup()

# Tall vertical 3D server tower (front: [24..60] x [12..74], offset: +16, +14)
Cisco.draw_3d_box(24.0, 12.0, 36.0, 62.0, 16.0, 14.0)

# Upper drive bay 1 bezel and horizontal media slot
rectangle(
    (42.0, 63.0),
    width=24.0,
    height=8.2,
    style=Icon.stroke_style(Icon.WHITE, width_units=1.6),
)
Icon.draw_round_segment((34.5, 63.0), (49.5, 63.0), width_units=1.8, color=Icon.WHITE)

# Upper drive bay 2 bezel and horizontal media slot
rectangle(
    (42.0, 52.8),
    width=24.0,
    height=7.2,
    style=Icon.stroke_style(Icon.WHITE, width_units=1.5),
)
Icon.draw_round_segment((34.5, 52.8), (49.5, 52.8), width_units=1.7, color=Icon.WHITE)

# Horizontal chassis panel seam lines (matching fileserver.jpg)
Icon.draw_round_segment((25.3, 44.0), (59.5, 44.0), width_units=1.5, color=Icon.WHITE)
Icon.draw_round_segment((25.3, 20.0), (59.5, 20.0), width_units=1.5, color=Icon.WHITE)

# Power button emblem on lower-middle front panel
arc(
    (42.0, 31.8),
    width=8.4,
    height=8.4,
    angle_start=122.0,
    angle_end=418.0,
    style=Icon.stroke_style(Icon.WHITE, width_units=1.7),
)
Icon.draw_round_segment((42.0, 32.0), (42.0, 36.6), width_units=1.7, color=Icon.WHITE)

save()
