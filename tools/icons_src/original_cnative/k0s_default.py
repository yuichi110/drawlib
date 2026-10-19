# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: k0s."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()

p1 = [(60.57, 68.32), (60.57, 47.43), (39.17, 31.37), (39.17, 52.25)]
polygon(p1, style=Icon.no_border_fill('#5F6B7D'))
Icon.draw_round_polyline(p1, width_units=2.0, color=Icon.DARK, closed=True)
p2 = [(91.47, 70.65), (91.47, 8.09), (8.27, 8.09), (8.27, 8.16), (30.41, 24.79), (74.76, 24.79), (74.77, 58.09), (91.47, 70.64)]
polygon(p2, style=Icon.no_border_fill('#4CC8E0'))
Icon.draw_round_polyline(p2, width_units=2.0, color=Icon.DARK, closed=True)
p3 = [(8.27, 91.46), (8.27, 29.05), (24.97, 41.6), (24.97, 74.76), (69.14, 74.76), (91.38, 91.46)]
polygon(p3, style=Icon.no_border_fill('#5F6B7D'))
Icon.draw_round_polyline(p3, width_units=2.0, color=Icon.DARK, closed=True)

save()
# fmt: on
