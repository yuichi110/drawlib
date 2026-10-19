# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco network icon: cisco_core_router (default classic 3D variant)."""

from drawlib.canvas import save
from drawlib.shapes import arc, circle, rectangle
from drawlib.utils import Cisco, Icon

Icon.setup()

# 1. Tall carrier-class 3D cylindrical chassis
Cisco.draw_3d_cylinder(50.0, 22.0, 74.0, 50.0, 13.0)

# 2. Classic 4 router arrows on top ellipse
Cisco.draw_router_top_arrows(50.0, 72.0, 37.0, 13.0)

# 3. Curved horizontal chassis band seam separating header from blade bay
arc(
    (50.0, 60.0),
    width=72.0,
    height=25.0,
    angle_start=184.0,
    angle_end=356.0,
    style=Icon.stroke_style(Icon.WHITE, width_units=1.6),
)

# 4. Five vertical carrier blade slots on the front chassis bay
blade_style = Icon.fill_style(Cisco.LIGHT_BLUE, border_color=Icon.WHITE, border_units=1.5, shape_r=1.5)
for bx in (26.0, 38.0, 50.0, 62.0, 74.0):
    rectangle((bx, 31.0), width=8.5, height=22.0, style=blade_style)
    circle((bx, 38.0), radius=1.4, style=Icon.no_border_fill(Icon.WHITE))
    circle((bx, 24.0), radius=1.4, style=Icon.no_border_fill(Icon.WHITE))

save()
