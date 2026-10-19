# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Facility icon: digital_realty (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(13.42, 75.78), (42.14, 90.75), (42.14, 10.23), (13.42, 25.2)], style=Icon.fill_style('#1D48A4'))
polygon([(46.81, 91.0), (51.78, 89.1), (51.78, 75.12), (56.75, 73.92), (56.75, 87.19), (71.67, 81.49), (71.67, 72.82), (76.64, 71.46), (76.64, 79.58), (86.58, 75.78), (86.58, 25.2), (56.75, 13.05), (56.75, 22.69), (51.78, 21.17), (51.78, 11.03), (46.81, 9.0)], holes=[[(51.78, 65.6), (56.75, 64.88), (56.75, 56.72), (51.78, 57.01)], [(51.78, 39.91), (56.75, 40.48), (56.75, 31.88), (51.78, 30.86)], [(56.75, 52.57), (61.72, 52.5), (61.72, 45.2), (56.75, 44.86)], [(61.72, 77.15), (66.69, 75.7), (66.69, 67.61), (61.72, 68.58)], [(61.72, 45.06), (66.69, 45.41), (66.69, 30.56), (61.72, 29.33)], [(66.69, 60.12), (71.67, 59.6), (71.67, 52.36), (66.69, 52.43)], [(71.67, 34.9), (76.64, 35.94), (76.64, 28.75), (71.67, 27.23)], [(76.64, 72.81), (81.61, 71.36), (81.61, 64.71), (76.64, 65.68)], [(76.64, 56.04), (81.61, 55.72), (81.61, 37.08), (76.64, 36.05)]], style=Icon.fill_style('#378ACA'))
save()
# fmt: on
