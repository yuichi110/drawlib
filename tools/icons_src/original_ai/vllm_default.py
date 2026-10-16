# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original AI concept icon: vllm."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 1.9

# 1. Left tilted golden-orange triangle wing (Colors.Amber3)
left_wing = [
    (12.2, 72.0),
    (43.8, 72.0),
    (43.8, 11.4),
]
polygon(left_wing, style=no_border_fill(Colors.Amber3))
draw_round_polyline(left_wing, width_units=w, color=DARK, closed=True)

# 2. Right tall sky-blue parallelogram wing ("#58AEFA")
right_wing = [
    (59.5, 74.1),
    (87.8, 88.6),
    (66.8, 11.4),
    (43.8, 11.4),
]
polygon(right_wing, style=no_border_fill("#58AEFA"))
draw_round_polyline(right_wing, width_units=w, color=DARK, closed=True)

save()
