# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security concept icon: zeek."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)

# ruff: noqa: E501
# fmt: off
setup_icon()

w_arrow = 2.2
w_z = 1.6

top_arrow: list[tuple[float, float]] = [(75.43, 70.42), (81.16, 77.58), (33.88, 77.58), (34.96, 87.61), (15.62, 70.42), (34.96, 53.22), (33.88, 63.43), (37.11, 63.43)]
bot_arrow: list[tuple[float, float]] = [(24.57, 29.58), (18.84, 22.42), (66.12, 22.42), (65.04, 12.39), (84.38, 29.58), (65.04, 46.78), (66.12, 36.57), (62.89, 36.57)]
z_poly: list[tuple[float, float]] = [(37.91, 34.1), (61.33, 34.09), (61.84, 34.19), (62.31, 34.4), (63.02, 34.99), (63.39, 35.6), (63.54, 36.13), (63.57, 36.81), (63.43, 37.39), (63.17, 37.93), (62.65, 38.5), (62.05, 38.86), (61.52, 39.02), (43.5, 39.04), (63.17, 62.05), (63.39, 62.45), (63.54, 62.98), (63.54, 63.84), (63.25, 64.64), (62.65, 65.33), (62.05, 65.7), (61.33, 65.89), (37.93, 65.89), (37.42, 65.79), (36.95, 65.57), (36.24, 64.98), (35.87, 64.37), (35.72, 63.84), (35.69, 63.16), (35.83, 62.58), (36.09, 62.05), (36.6, 61.49), (37.21, 61.12), (37.74, 60.95), (55.76, 60.94), (36.09, 37.93), (35.83, 37.39), (35.69, 36.81), (35.72, 36.13), (35.87, 35.6), (36.24, 34.99), (36.81, 34.48), (37.35, 34.21)]
# fmt: on

# 1. Framing DARK arrows (w=2.2)
draw_round_polyline(top_arrow, width_units=w_arrow, color=DARK, closed=False)
draw_round_polyline(bot_arrow, width_units=w_arrow, color=DARK, closed=False)

# 2. Central 'Z' in pastel blue (Colors.Blue3) with DARK 1.6 outline
polygon(z_poly, style=no_border_fill(Colors.Blue3))
draw_round_polyline(z_poly, width_units=w_z, color=DARK, closed=True)

save()
