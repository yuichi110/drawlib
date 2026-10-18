# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility icon: iron_mountain (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import DARK, draw_round_polyline, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()

w = 2.0
tri_left = [(39.0, 64.92), (53.39, 41.5), (67.89, 18.09), (39.0, 18.09), (10.0, 18.09), (24.5, 41.5)]
tri_right = [(61.0, 81.91), (75.5, 49.94), (90.0, 18.09), (61.0, 18.09), (31.99, 18.09), (46.5, 49.94)]
tri_center = [(49.94, 72.76), (64.44, 45.42), (78.95, 18.09), (49.94, 18.09), (21.05, 18.09), (35.56, 45.42)]

polygon(tri_left, style=fill_style("#5E84B4", alpha=0.82))
polygon(tri_right, style=fill_style("#6CA6DC", alpha=0.82))
polygon(tri_center, style=fill_style("#9ADCF7", alpha=0.82))

draw_round_polyline(tri_left, width_units=w, color=DARK, closed=True)
draw_round_polyline(tri_right, width_units=w, color=DARK, closed=True)
draw_round_polyline(tri_center, width_units=w, color=DARK, closed=True)

save()
# fmt: on
