# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco network icon: wireless router (classic 3D default variant)."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.utils import Cisco, Icon

Icon.setup()

# Two rear vertical antennas drawn behind the 3D cylinder (x=27.0 and x=73.0)
for ax in (27.0, 73.0):
    # Upper antenna whip rod with seamless rounded tip (y from 65.0 to 87.5)
    Icon.draw_round_segment((ax, 65.0), (ax, 87.5), width_units=4.4, color=Cisco.BORDER)
    Icon.draw_round_segment((ax, 65.0), (ax, 87.5), width_units=2.4, color=Cisco.BLUE)

    # Lower antenna base sleeve (y from 44.0 to 66.0)
    rectangle(
        (ax, 55.0),
        width=5.8,
        height=22.0,
        style=Icon.fill_style(Cisco.BLUE, border_color=Cisco.BORDER, border_units=1.6),
    )
    # Subtle shadow strip on right edge of base sleeve
    rectangle(
        (ax + 1.4, 55.0),
        width=1.4,
        height=20.4,
        style=Icon.no_border_fill(Cisco.DARK_BLUE),
    )

# 3D cylinder router body in front (y_bot=22.0, body_h=20.0, ry=13.5 -> y in [8.5, 55.5])
Cisco.draw_3d_cylinder(
    cx=50.0,
    y_bot=22.0,
    width=76.0,
    body_h=20.0,
    ry=13.5,
)

# Classic 4 Cisco router arrows on the top ellipse (center=(50.0, 42.0))
Cisco.draw_router_top_arrows(
    cx=50.0,
    cy=42.0,
    rx=38.0,
    ry=13.5,
    color=Icon.WHITE,
)

save()
