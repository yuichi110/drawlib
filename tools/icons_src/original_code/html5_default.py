# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code icon: html5."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import (
    DARK,
    WHITE,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)

# ruff: noqa: E501
# fmt: off
setup_icon()

w_outer = 2.0
w_inner = 1.3

shield_outer = [(21.15, 18.0), (14.73, 90.0), (85.27, 90.0), (78.84, 18.01), (49.96, 10.0)]
shield_right = [(50.0, 16.12), (73.35, 22.6), (78.83, 84.12), (50.0, 84.12)]
five_l_top = [(50.0, 57.4), (38.31, 57.4), (37.5, 66.45), (50.0, 66.45), (50.0, 75.28), (27.85, 75.28), (28.07, 72.92), (30.23, 48.58), (50.0, 48.58)]
five_l_bot = [(50.0, 34.48), (49.96, 34.46), (40.13, 37.12), (39.5, 44.16), (30.63, 44.16), (31.87, 30.29), (49.96, 25.28), (50.0, 25.29)]
five_r_bot = [(49.97, 57.4), (49.97, 48.58), (60.84, 48.58), (59.81, 37.12), (49.97, 34.47), (49.97, 25.28), (68.08, 30.29), (68.2, 31.79), (70.28, 55.03), (70.5, 57.4), (68.12, 57.4)]
five_r_top = [(49.97, 75.28), (49.97, 66.45), (71.3, 66.45), (71.47, 68.44), (71.88, 72.92), (72.09, 75.28)]
five_outer = [(27.85, 75.28), (30.23, 48.58), (60.84, 48.58), (59.81, 37.12), (49.97, 34.47), (40.13, 37.12), (39.5, 44.16), (30.63, 44.16), (31.87, 30.29), (49.97, 25.28), (68.08, 30.29), (70.5, 57.4), (38.31, 57.4), (37.5, 66.45), (71.3, 66.45), (72.09, 75.28)]
# fmt: on

# 1. Flat pastel orange shield halves
polygon(shield_outer, style=no_border_fill("#F17143"))
polygon(shield_right, style=no_border_fill("#F28050"))
draw_round_polyline(shield_right, width_units=w_inner, color=DARK, closed=True)

# 2. Two-tone '#F2F4F7' (left) and WHITE (right) '5' chevrons
polygon(five_l_top, style=no_border_fill("#F2F4F7"))
polygon(five_l_bot, style=no_border_fill("#F2F4F7"))
polygon(five_r_bot, style=no_border_fill(WHITE))
polygon(five_r_top, style=no_border_fill(WHITE))
draw_round_polyline(five_outer, width_units=w_inner, color=DARK, closed=True)

# 3. Crisp DARK outer shield border
draw_round_polyline(shield_outer, width_units=w_outer, color=DARK, closed=True)

save()
