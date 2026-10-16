# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco network topology icon: client PC (modern 2D SAFE variant)."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import (
    CISCO_BLUE,
    WHITE,
    draw_cisco_modern_badge,
    draw_round_segment,
    no_border_fill,
    setup_icon,
)

setup_icon()

draw_cisco_modern_badge()

# Flat desktop monitor outer frame
rectangle(
    (50.0, 60.0),
    width=50.0,
    height=33.0,
    style=no_border_fill(WHITE, shape_r=4.2),
)

# Inner display screen cutout
rectangle(
    (50.0, 61.0),
    width=42.0,
    height=23.5,
    style=no_border_fill(CISCO_BLUE, shape_r=1.8),
)

# Monitor stand neck and base
rectangle(
    (50.0, 40.5),
    width=8.0,
    height=7.0,
    style=no_border_fill(WHITE),
)
rectangle(
    (50.0, 36.5),
    width=22.0,
    height=3.6,
    style=no_border_fill(WHITE, shape_r=1.8),
)

# Flat keyboard bar below stand
rectangle(
    (50.0, 26.3),
    width=46.0,
    height=6.6,
    style=no_border_fill(WHITE, shape_r=2.5),
)

# Key dots and center spacebar slot inside keyboard bar
for kx in (32.5, 38.8, 61.2, 67.5):
    circle((kx, 26.3), radius=1.4, style=no_border_fill(CISCO_BLUE))
draw_round_segment((44.5, 26.3), (55.5, 26.3), width_units=2.4, color=CISCO_BLUE)

save()
