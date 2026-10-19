# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Business brand icon: sendgrid."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
p_0 = [(88.8, 88.8), (88.8, 37.06), (62.94, 37.06), (62.94, 11.2), (11.2, 11.2), (11.2, 37.06), (11.2, 62.94), (37.06, 62.94), (37.06, 88.8)]
polygon(p_0, style=Icon.no_border_fill('#B5E0EA'))
Icon.draw_round_polyline(p_0, width_units=2.0, color=Icon.DARK, closed=True)
p_1 = [(11.2, 11.2), (37.06, 11.2), (37.06, 37.06), (11.2, 37.06)]
polygon(p_1, style=Icon.no_border_fill('#6D94BF'))
Icon.draw_round_polyline(p_1, width_units=2.0, color=Icon.DARK, closed=True)
p_2 = [(62.94, 37.06), (88.8, 37.06), (88.8, 62.94), (62.94, 62.94)]
polygon(p_2, style=Icon.no_border_fill('#3DBEDC'))
Icon.draw_round_polyline(p_2, width_units=2.0, color=Icon.DARK, closed=True)
p_3 = [(37.06, 62.94), (62.94, 62.94), (62.94, 88.8), (37.06, 88.8)]
polygon(p_3, style=Icon.no_border_fill('#3DBEDC'))
Icon.draw_round_polyline(p_3, width_units=2.0, color=Icon.DARK, closed=True)
p_4 = [(37.06, 37.06), (62.94, 37.06), (62.94, 62.94), (37.06, 62.94)]
polygon(p_4, style=Icon.no_border_fill('#56ABD2'))
Icon.draw_round_polyline(p_4, width_units=2.0, color=Icon.DARK, closed=True)
p_5 = [(62.94, 62.94), (88.8, 62.94), (88.8, 88.8), (62.94, 88.8)]
polygon(p_5, style=Icon.no_border_fill('#6D94BF'))
Icon.draw_round_polyline(p_5, width_units=2.0, color=Icon.DARK, closed=True)
save()
# fmt: on
