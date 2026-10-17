# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility icon: equinix (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import DARK, draw_round_polyline, no_border_fill, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()

w = 1.8
pts = [(74.0, 62.12), (74.0, 31.32), (90.0, 36.91), (90.0, 62.19), (84.66, 64.04), (84.66, 40.69), (79.34, 38.83), (79.34, 65.9), (63.34, 71.48), (63.34, 33.26), (58.0, 31.4), (58.0, 73.36), (50.0, 76.13), (42.0, 73.35), (42.0, 31.37), (36.67, 33.26), (36.67, 71.48), (20.67, 65.89), (20.67, 38.83), (15.34, 40.69), (15.34, 64.04), (10.0, 62.19), (10.0, 36.91), (26.0, 31.32), (26.0, 62.12), (31.34, 63.99), (31.34, 29.45), (47.34, 23.87), (47.34, 69.56), (50.0, 70.51), (52.66, 69.57), (52.66, 23.88), (68.67, 29.47), (68.67, 63.98)]
polygon(pts, style=no_border_fill("#F26B70"))
draw_round_polyline(pts, width_units=w, color=DARK, closed=True)

save()
# fmt: on
