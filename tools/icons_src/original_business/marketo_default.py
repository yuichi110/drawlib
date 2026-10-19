# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Business brand icon: marketo."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
p_0 = [(83.23, 26.99), (83.23, 78.02), (63.41, 88.8), (63.41, 11.2)]
polygon(p_0, style=Icon.no_border_fill('#8377B6'))
Icon.draw_round_polyline(p_0, width_units=2.0, color=Icon.DARK, closed=True)
p_1 = [(38.22, 82.05), (54.18, 77.33), (54.18, 28.15), (38.22, 21.17)]
polygon(p_1, style=Icon.no_border_fill('#8377B6'))
Icon.draw_round_polyline(p_1, width_units=2.0, color=Icon.DARK, closed=True)
p_2 = [(28.99, 72.02), (16.83, 73.98), (16.77, 29.94), (28.99, 33.16)]
polygon(p_2, style=Icon.no_border_fill('#8377B6'))
Icon.draw_round_polyline(p_2, width_units=2.0, color=Icon.DARK, closed=True)
save()
# fmt: on
