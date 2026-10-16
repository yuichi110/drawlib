# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco network icon: wireless access point (classic 3D default variant)."""

from drawlib.canvas import save
from drawlib.utils import (
    WHITE,
    draw_cisco_3d_box,
    draw_cisco_sine_waves,
    setup_icon,
)

setup_icon()

# Flat 3D access point box (x in [10, 90], y in [32, 68])
draw_cisco_3d_box(10.0, 32.0, 64.0, 22.0, 16.0, 14.0)

# Signature Cisco intertwined dual sine wave on the front face
draw_cisco_sine_waves(
    42.0,
    43.0,
    48.0,
    5.5,
    cycles=2.0,
    stroke_w=2.6,
    color=WHITE,
    steps=120,
)

save()
