# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Social icon: stack_overflow (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(72.01, 39.01), (78.77, 39.01), (78.77, 12.0), (17.97, 12.0), (17.97, 39.01), (24.72, 39.01), (24.72, 18.75), (72.01, 18.75)], style=Icon.fill_style((187, 187, 187)))
polygon([(36.47, 56.9), (67.21, 42.59), (70.07, 48.73), (39.34, 63.04)], style=Icon.fill_style((245, 128, 37)))
polygon([(44.98, 71.97), (71.04, 50.28), (75.38, 55.49), (49.32, 77.18)], style=Icon.fill_style((245, 128, 37)))
polygon([(61.8, 88.0), (56.36, 83.96), (76.59, 56.76), (82.03, 60.81)], style=Icon.fill_style((245, 128, 37)))
polygon([(32.08, 41.02), (65.26, 34.05), (66.66, 40.68), (33.48, 47.65)], style=Icon.fill_style((245, 128, 37)))
polygon([(31.48, 25.51), (65.26, 25.51), (65.26, 32.26), (31.48, 32.26)], style=Icon.fill_style((245, 128, 37)))
save()
# fmt: on
