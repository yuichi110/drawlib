# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Social icon: hacker_news (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(12.0, 12.0), (12.0, 88.0), (88.0, 88.0), (88.0, 12.0), (12.0, 12.0)], holes=[[(34.01, 69.33), (47.03, 44.92), (47.03, 28.88), (52.05, 28.88), (52.05, 44.63), (65.18, 69.33), (59.64, 69.33), (51.86, 53.89), (51.64, 53.45), (51.43, 53.02), (51.22, 52.59), (51.02, 52.18), (50.83, 51.79), (50.65, 51.42), (50.49, 51.06), (50.33, 50.73), (50.19, 50.43), (50.06, 50.16), (49.95, 49.93), (49.86, 49.73), (49.78, 49.56), (49.73, 49.45), (49.69, 49.37), (49.68, 49.35), (49.67, 49.37), (49.64, 49.45), (49.59, 49.57), (49.52, 49.73), (49.43, 49.94), (49.33, 50.18), (49.21, 50.45), (49.07, 50.76), (48.93, 51.09), (48.77, 51.44), (48.6, 51.82), (48.42, 52.21), (48.23, 52.62), (48.03, 53.03), (47.83, 53.46), (47.62, 53.89), (39.96, 69.33), (34.01, 69.33)]], style=Icon.fill_style(Colors.Orange3, border_color=Icon.DARK, border_units=Icon.ORIG_STROKE))
save()
# fmt: on
