# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Security icon: zeek (default variant)."""

from drawlib.canvas import save
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
Icon.draw_round_polyline([(76.77, 71.49), (82.8, 79.03), (33.03, 79.03), (34.17, 89.59), (13.81, 71.49), (34.17, 53.39), (33.03, 64.14), (36.43, 64.14)], width_units=2.83, color='#000000', closed=False)
Icon.draw_round_polyline([(23.23, 28.51), (17.2, 20.97), (66.97, 20.97), (65.83, 10.41), (86.19, 28.51), (65.83, 46.61), (66.97, 35.86), (63.57, 35.86)], width_units=2.83, color='#000000', closed=False)
Icon.draw_round_polyline([(37.56, 64.14), (61.69, 64.14), (37.56, 35.86), (61.69, 35.86)], width_units=3.77, color='#08A9E2', closed=False)
save()
# fmt: on
