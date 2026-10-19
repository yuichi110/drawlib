# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original AI icon: triton (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(74.62, 90.0), (79.37, 89.25), (83.66, 87.06), (87.06, 83.66), (89.25, 79.37), (90.0, 74.62), (90.0, 25.38), (89.25, 20.63), (87.06, 16.34), (83.66, 12.94), (79.37, 10.75), (74.62, 10.0), (25.38, 10.0), (20.63, 10.75), (16.34, 12.94), (12.94, 16.34), (10.75, 20.63), (10.0, 25.38), (10.0, 74.62), (10.75, 79.37), (12.94, 83.66), (16.34, 87.06), (20.63, 89.25), (25.38, 90.0)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
polygon([(50.0, 82.31), (58.46, 70.0), (53.46, 70.0), (53.46, 30.0), (60.77, 30.0), (50.0, 16.92), (39.23, 30.0), (46.54, 30.0), (46.54, 70.0), (41.54, 70.0)], style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=1.8))
polygon([(27.69, 73.08), (36.92, 63.08), (32.31, 63.08), (32.31, 46.15), (46.54, 40.0), (46.54, 33.08), (25.38, 42.31), (25.38, 63.08), (20.77, 63.08)], style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=1.8))
polygon([(72.31, 73.08), (79.23, 63.08), (74.62, 63.08), (74.62, 42.31), (53.46, 33.08), (53.46, 40.0), (67.69, 46.15), (67.69, 63.08), (63.08, 63.08)], style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=1.8))
save()
# fmt: on
