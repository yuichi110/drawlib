# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Azure icon: chaos_studio (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(55.51, 50.0), (55.51, 76.51), (8.0, 29.0), (8.0, 73.33), (8.8, 76.8), (10.12, 80.1), (11.94, 83.15), (14.21, 85.89), (17.15, 88.35), (20.49, 90.23), (24.13, 91.46), (27.93, 92.0), (71.0, 92.0), (92.0, 71.0), (71.0, 50.0)], style=Icon.fill_style("#E83231"))
polygon([(44.49, 50.0), (44.49, 23.49), (92.0, 71.0), (92.0, 26.67), (91.21, 23.18), (89.89, 19.85), (88.07, 16.78), (85.79, 14.02), (82.84, 11.59), (79.49, 9.74), (75.86, 8.53), (72.07, 8.0), (29.0, 8.0), (8.0, 29.0), (29.0, 50.0)], style=Icon.fill_style("#A80000"))
polygon([(44.49, 23.49), (92.0, 71.0), (92.0, 26.67), (91.21, 23.18), (89.89, 19.85), (88.07, 16.78), (85.79, 14.02), (82.84, 11.59), (79.49, 9.74), (75.86, 8.53), (72.07, 8.0)], style=Icon.fill_style("#A80000"))
save()
# fmt: on
