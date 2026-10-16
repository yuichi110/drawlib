# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco network icon: cisco_router (modern 2D badge variant)."""

from drawlib.canvas import save
from drawlib.utils import (
    WHITE,
    draw_cisco_modern_badge,
    draw_round_polyline,
    draw_round_segment,
    setup_icon,
)

setup_icon()

draw_cisco_modern_badge()

w = 4.6
arm = 11.0

# Top-left arrow pointing IN toward center
draw_round_segment((27.0, 73.0), (44.5, 55.5), width_units=w, color=WHITE)
draw_round_polyline(
    [(44.5 - arm, 55.5), (44.5, 55.5), (44.5, 55.5 + arm)],
    width_units=w,
    color=WHITE,
)

# Bottom-right arrow pointing IN toward center
draw_round_segment((73.0, 27.0), (55.5, 44.5), width_units=w, color=WHITE)
draw_round_polyline(
    [(55.5 + arm, 44.5), (55.5, 44.5), (55.5, 44.5 - arm)],
    width_units=w,
    color=WHITE,
)

# Top-right arrow pointing OUT away from center
draw_round_segment((55.5, 55.5), (73.0, 73.0), width_units=w, color=WHITE)
draw_round_polyline(
    [(73.0 - arm, 73.0), (73.0, 73.0), (73.0, 73.0 - arm)],
    width_units=w,
    color=WHITE,
)

# Bottom-left arrow pointing OUT away from center
draw_round_segment((44.5, 44.5), (27.0, 27.0), width_units=w, color=WHITE)
draw_round_polyline(
    [(27.0 + arm, 27.0), (27.0, 27.0), (27.0, 27.0 + arm)],
    width_units=w,
    color=WHITE,
)

save()
