# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility icon: coresite (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import DARK, draw_round_polyline, no_border_fill, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()

w = 1.8
outer_c = [(90.0, 51.73), (90.0, 80.34), (89.92, 81.6), (89.67, 82.84), (89.27, 84.04), (88.7, 85.17), (88.0, 86.22), (87.17, 87.17), (86.22, 88.0), (85.17, 88.7), (84.04, 89.27), (82.84, 89.67), (81.6, 89.92), (80.34, 90.0), (19.66, 90.0), (18.4, 89.92), (17.16, 89.67), (15.96, 89.27), (14.83, 88.7), (13.78, 88.0), (12.83, 87.17), (12.0, 86.22), (11.3, 85.17), (10.73, 84.04), (10.33, 82.84), (10.08, 81.6), (10.0, 80.34), (10.0, 19.66), (10.08, 18.4), (10.33, 17.16), (10.73, 15.96), (11.3, 14.83), (12.0, 13.78), (12.83, 12.83), (13.78, 12.0), (14.83, 11.3), (15.96, 10.73), (17.16, 10.33), (18.4, 10.08), (19.66, 10.0), (80.34, 10.0), (81.6, 10.08), (82.84, 10.33), (84.04, 10.73), (85.17, 11.3), (86.22, 12.0), (87.17, 12.83), (88.0, 13.78), (88.7, 14.83), (89.27, 15.96), (89.67, 17.16), (89.92, 18.4), (90.0, 19.66), (90.0, 48.27), (70.0, 48.27), (70.0, 30.0), (30.0, 30.0), (30.0, 70.0), (70.0, 70.0), (70.0, 51.73)]
inner_sq = [(32.76, 32.76), (67.24, 32.76), (67.24, 67.24), (32.76, 67.24)]

polygon(outer_c, style=no_border_fill("#9BA4B0"))
draw_round_polyline(outer_c, width_units=w, color=DARK, closed=True)

polygon(inner_sq, style=no_border_fill("#689FD8"))
draw_round_polyline(inner_sq, width_units=w, color=DARK, closed=True)

save()
# fmt: on
