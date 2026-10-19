# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Social icon: twitch (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(31.0, 88.0), (17.43, 74.43), (17.43, 25.57), (33.71, 25.57), (33.71, 12.0), (47.29, 25.57), (58.14, 25.57), (82.57, 50.0), (82.57, 88.0)], holes=[[(77.14, 52.71), (66.29, 41.86), (55.43, 41.86), (45.93, 32.36), (45.93, 41.86), (33.71, 41.86), (33.71, 82.57), (77.14, 82.57)], [(48.64, 73.07), (54.07, 73.07), (54.07, 56.79), (48.64, 56.79)], [(63.57, 73.07), (69.0, 73.07), (69.0, 56.79), (63.57, 56.79)]], style=Icon.fill_style(Colors.Purple3, border_color=Icon.DARK, border_units=Icon.ORIG_STROKE))
save()
# fmt: on
