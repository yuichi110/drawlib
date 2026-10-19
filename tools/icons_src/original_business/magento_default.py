# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Business brand icon: magento."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
p_0 = [(50.03, 88.8), (16.4, 69.39), (16.4, 30.6), (26.01, 25.05), (25.94, 63.84), (49.97, 77.72), (73.99, 63.84), (73.99, 25.07), (83.6, 30.6), (83.6, 69.42)]
polygon(p_0, style=Icon.no_border_fill('#F58857'))
Icon.draw_round_polyline(p_0, width_units=2.0, color=Icon.DARK, closed=True)
p_1 = [(54.8, 25.05), (50.0, 22.28), (45.18, 25.04), (45.18, 63.84), (35.58, 58.29), (35.6, 19.52), (50.0, 11.2), (64.4, 19.52), (64.4, 58.29), (54.8, 63.84)]
polygon(p_1, style=Icon.no_border_fill('#F58857'))
Icon.draw_round_polyline(p_1, width_units=2.0, color=Icon.DARK, closed=True)
save()
# fmt: on
