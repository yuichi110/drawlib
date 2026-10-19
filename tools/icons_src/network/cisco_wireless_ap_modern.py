# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco network icon: wireless access point (modern 2D variant)."""

from drawlib.canvas import save
from drawlib.utils import Cisco, Icon

Icon.setup()
Cisco.draw_modern_badge()

# Signature Cisco intertwined dual sine wave motif inside the badge
Cisco.draw_sine_waves(
    50.0,
    50.0,
    56.0,
    8.5,
    cycles=2.0,
    stroke_w=3.0,
    color=Icon.WHITE,
    steps=144,
)

save()
