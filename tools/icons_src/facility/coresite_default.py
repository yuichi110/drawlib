# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Facility icon: coresite (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(91.0, 51.77), (91.0, 81.1), (90.92, 82.39), (90.66, 83.66), (90.25, 84.89), (89.67, 86.05), (88.95, 87.13), (88.1, 88.1), (87.13, 88.95), (86.05, 89.67), (84.89, 90.25), (83.66, 90.66), (82.39, 90.92), (81.1, 91.0), (18.9, 91.0), (17.61, 90.92), (16.34, 90.66), (15.11, 90.25), (13.95, 89.67), (12.87, 88.95), (11.9, 88.1), (11.05, 87.13), (10.33, 86.05), (9.75, 84.89), (9.34, 83.66), (9.08, 82.39), (9.0, 81.1), (9.0, 18.9), (9.08, 17.61), (9.34, 16.34), (9.75, 15.11), (10.33, 13.95), (11.05, 12.87), (11.9, 11.9), (12.87, 11.05), (13.95, 10.33), (15.11, 9.75), (16.34, 9.34), (17.61, 9.08), (18.9, 9.0), (81.1, 9.0), (82.39, 9.08), (83.66, 9.34), (84.89, 9.75), (86.05, 10.33), (87.13, 11.05), (88.1, 11.9), (88.95, 12.87), (89.67, 13.95), (90.25, 15.11), (90.66, 16.34), (90.92, 17.61), (91.0, 18.9), (91.0, 48.23), (70.5, 48.23), (70.5, 29.5), (29.5, 29.5), (29.5, 70.5), (70.5, 70.5), (70.5, 51.77)], style=Icon.fill_style('#606060'))
rectangle((50.0, 50.0), width=35.34, height=35.34, style=Icon.fill_style('#2070B0'))
save()
# fmt: on
