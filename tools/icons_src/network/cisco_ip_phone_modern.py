# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco network topology icon: IP phone (modern 2D SAFE variant)."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Cisco, Icon

Icon.setup()

Cisco.draw_modern_badge()

# Left handset capsule (matching SAFE Arch_63_Phone)
rectangle(
    (28.0, 50.0),
    width=13.0,
    height=48.0,
    style=Icon.no_border_fill(Icon.WHITE, shape_r=6.5),
)
# Handset top receiver slot cutout
Icon.draw_round_segment((28.0, 62.5), (28.0, 74.0), width_units=3.2, color=Cisco.BLUE)

# Right VoIP desk phone body
rectangle(
    (59.0, 50.0),
    width=41.0,
    height=48.0,
    style=Icon.no_border_fill(Icon.WHITE, shape_r=5.5),
)

# LCD display screen cutout on upper-left of phone body
rectangle(
    (53.0, 59.5),
    width=20.0,
    height=18.5,
    style=Icon.no_border_fill(Cisco.BLUE, shape_r=1.8),
)

# 3 line-key pill buttons on upper-right of phone body
for btn_y in (66.0, 59.5, 53.0):
    rectangle(
        (71.2, btn_y),
        width=9.2,
        height=3.6,
        style=Icon.no_border_fill(Cisco.BLUE, shape_r=1.8),
    )

# 3x3 numeric keypad dots below LCD screen
for ky in (44.2, 38.2, 32.2):
    for kx in (46.5, 53.0, 59.5):
        circle((kx, ky), radius=2.0, style=Icon.no_border_fill(Cisco.BLUE))

save()
