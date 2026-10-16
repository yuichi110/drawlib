# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco network icon: wireless LAN controller (modern 2D variant)."""

from drawlib.canvas import save
from drawlib.utils import (
    CISCO_LIGHT_BLUE,
    WHITE,
    draw_cisco_arrow,
    draw_cisco_modern_badge,
    draw_cisco_sine_waves,
    draw_round_segment,
    setup_icon,
)

setup_icon()
draw_cisco_modern_badge()

# Top central outgoing controller arrow
draw_cisco_arrow(
    (50.0, 55.5),
    (50.0, 79.0),
    shaft_w=5.8,
    head_len=10.5,
    head_w=16.5,
    color=WHITE,
)

# Three converging intake arrows in the middle section
draw_cisco_arrow(
    (31.0, 42.5),
    (44.0, 52.5),
    shaft_w=3.6,
    head_len=6.2,
    head_w=9.2,
    color=WHITE,
)
draw_cisco_arrow(
    (50.0, 39.0),
    (50.0, 52.5),
    shaft_w=3.6,
    head_len=6.2,
    head_w=9.2,
    color=WHITE,
)
draw_cisco_arrow(
    (69.0, 42.5),
    (56.0, 52.5),
    shaft_w=3.6,
    head_len=6.2,
    head_w=9.2,
    color=WHITE,
)

# Lower controller appliance bars + wireless dual sine wave symbol
draw_round_segment((22.0, 35.5), (78.0, 35.5), width_units=1.8, color=CISCO_LIGHT_BLUE)
draw_round_segment((22.0, 20.5), (78.0, 20.5), width_units=1.8, color=CISCO_LIGHT_BLUE)

# Modular controller blade ticks on right side of appliance bar
for x_tick in (70.0, 74.0):
    draw_round_segment((x_tick, 23.0), (x_tick, 33.0), width_units=1.6, color=CISCO_LIGHT_BLUE)

draw_cisco_sine_waves(
    45.0,
    28.0,
    42.0,
    4.2,
    cycles=1.5,
    stroke_w=2.4,
    color=WHITE,
    steps=120,
)

save()
