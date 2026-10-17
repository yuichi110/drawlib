# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Server vendor icon: amd (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import DARK, draw_round_polyline, no_border_fill, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()

w = 1.6

top_right_chevron: list[tuple[float, float]] = [(32.93, 67.73), (11.71, 88.95), (88.95, 88.95), (88.95, 11.71), (67.73, 32.91), (67.73, 67.73)]
bottom_left_arrow: list[tuple[float, float]] = [(32.9, 63.48), (11.05, 41.63), (11.05, 11.05), (41.63, 11.05), (63.48, 32.9), (32.9, 32.9)]

# 1. Top-right chevron wing in flat dark slate-gray (#4A5568)
polygon(top_right_chevron, style=no_border_fill("#4A5568"))
draw_round_polyline(top_right_chevron, width_units=w, color=DARK, closed=True)

# 2. Bottom-left arrow triangle in flat dark slate-gray (#4A5568)
polygon(bottom_left_arrow, style=no_border_fill("#4A5568"))
draw_round_polyline(bottom_left_arrow, width_units=w, color=DARK, closed=True)

save()
# fmt: on
