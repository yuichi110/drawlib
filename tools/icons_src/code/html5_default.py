# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Code icon: html5 (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(20.43, 17.2), (13.85, 91.0), (86.15, 91.0), (79.56, 17.21), (49.96, 9.0)], style=Icon.fill_style('#E44D26'))
polygon([(50.0, 15.27), (73.93, 21.91), (79.55, 84.97), (50.0, 84.97)], style=Icon.fill_style('#F16529'))
polygon([(50.0, 57.59), (38.02, 57.59), (37.19, 66.86), (50.0, 66.86), (50.0, 75.91), (27.3, 75.91), (27.52, 73.49), (29.74, 48.54), (50.0, 48.54)], style=Icon.fill_style('#EBEBEB'))
polygon([(50.0, 34.09), (49.96, 34.07), (39.88, 36.8), (39.24, 44.01), (30.15, 44.01), (31.42, 29.8), (49.96, 24.66), (50.0, 24.67)], style=Icon.fill_style('#EBEBEB'))
polygon([(49.97, 57.59), (49.97, 48.54), (61.11, 48.54), (60.06, 36.8), (49.97, 34.08), (49.97, 24.66), (68.53, 29.8), (68.66, 31.33), (70.79, 55.16), (71.01, 57.59), (68.57, 57.59)], style=Icon.fill_style(Icon.WHITE))
polygon([(49.97, 75.91), (49.97, 66.86), (71.83, 66.86), (72.01, 68.9), (72.43, 73.49), (72.64, 75.91)], style=Icon.fill_style(Icon.WHITE))
save()
# fmt: on
