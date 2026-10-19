# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Business brand icon: netsuite."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
p_0 = [(62.57, 83.5), (85.14, 83.5), (85.3, 33.23), (70.05, 33.23), (70.05, 69.49), (62.57, 69.49)]
polygon(p_0, style=Icon.no_border_fill('#C4D1DD'))
Icon.draw_round_polyline(p_0, width_units=2.0, color=Icon.DARK, closed=True)
p_1 = [(59.45, 45.75), (59.45, 87.39), (11.2, 87.39), (11.2, 69.63), (40.21, 69.63)]
polygon(p_1, style=Icon.no_border_fill('#3E7094'))
Icon.draw_round_polyline(p_1, width_units=2.0, color=Icon.DARK, closed=True)
p_2 = [(37.43, 16.5), (14.86, 16.5), (14.7, 66.77), (29.96, 66.77), (29.96, 30.51), (37.43, 30.51)]
polygon(p_2, style=Icon.no_border_fill('#C4D1DD'))
Icon.draw_round_polyline(p_2, width_units=2.0, color=Icon.DARK, closed=True)
p_3 = [(40.55, 54.25), (40.55, 12.61), (88.8, 12.61), (88.8, 30.37), (59.79, 30.37)]
polygon(p_3, style=Icon.no_border_fill('#3E7094'))
Icon.draw_round_polyline(p_3, width_units=2.0, color=Icon.DARK, closed=True)
save()
# fmt: on
