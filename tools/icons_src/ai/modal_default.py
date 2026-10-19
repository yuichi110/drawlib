# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""AI icon: modal (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(25.71, 71.97), (9.0, 43.16), (17.61, 28.13), (34.87, 28.13), (49.89, 54.5), (65.3, 28.16), (82.37, 28.03), (91.0, 42.97), (74.41, 71.85), (57.07, 71.9), (49.98, 59.61), (42.96, 71.97)], holes=[[(28.57, 69.48), (41.51, 69.48), (47.81, 58.37), (34.87, 58.37)], [(59.96, 69.41), (72.96, 69.37), (87.4, 44.24), (74.64, 44.33)], [(26.41, 68.22), (32.71, 57.13), (18.33, 31.88), (11.87, 43.16)], [(57.8, 68.18), (72.48, 43.09), (66.02, 31.87), (51.33, 56.97)], [(34.86, 55.88), (47.81, 55.88), (33.42, 30.61), (20.48, 30.61)], [(74.63, 41.84), (87.41, 41.75), (80.94, 30.54), (68.17, 30.63)]], style=Icon.fill_style('#10B981'))
save()
# fmt: on
