# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""AI icon: triton (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(75.23, 91.0), (80.1, 90.23), (84.5, 87.99), (87.99, 84.5), (90.23, 80.1), (91.0, 75.23), (91.0, 24.77), (90.23, 19.9), (87.99, 15.5), (84.5, 12.01), (80.1, 9.77), (75.23, 9.0), (24.77, 9.0), (19.9, 9.77), (15.5, 12.01), (12.01, 15.5), (9.77, 19.9), (9.0, 24.77), (9.0, 75.23), (9.77, 80.1), (12.01, 84.5), (15.5, 87.99), (19.9, 90.23), (24.77, 91.0)], style=Icon.fill_style('#1A1A1A'))
polygon([(50.0, 83.12), (58.67, 70.5), (53.55, 70.5), (53.55, 29.5), (61.04, 29.5), (50.0, 16.1), (38.96, 29.5), (46.45, 29.5), (46.45, 70.5), (41.33, 70.5)], style=Icon.fill_style('#76B900'))
polygon([(27.13, 73.65), (36.6, 63.4), (31.87, 63.4), (31.87, 46.06), (46.45, 39.75), (46.45, 32.65), (24.77, 42.12), (24.77, 63.4), (20.04, 63.4)], style=Icon.fill_style('#76B900'))
polygon([(72.87, 73.65), (79.96, 63.4), (75.23, 63.4), (75.23, 42.12), (53.55, 32.65), (53.55, 39.75), (68.13, 46.06), (68.13, 63.4), (63.4, 63.4)], style=Icon.fill_style('#76B900'))
save()
# fmt: on
